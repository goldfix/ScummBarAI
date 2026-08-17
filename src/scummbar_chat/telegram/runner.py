"""
Module: runner.py
Operations:
- Initializes and manages the Google ADK Runner instance alongside the session tracking architecture.
- Handles persistent conversation tracking utilizing ADK's `DatabaseSessionService` linked to SQLite.
- Integrates an off-thread SQLite worker (`run_in_executor`) to periodically wipe dialogue history older than 24 hours.
- Handles incoming context packaging, payload framing, and yields final synthesized LLM tokens while stripping internal thoughts.
"""

import asyncio
import logging
import sqlite3
import time
from datetime import UTC, datetime, timedelta

from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from ..agent import root_agent
from ..telemetry import init_tracing, turn_tracing

# Utilities imports: pre-built model instances for agents and compaction
from ..utils import (
    COMPACTION_INTERVAL,
    COMPACTION_LLM,
    COMPACTION_MODEL,
    COMPACTION_OVERLAP,
    CONTEXT_CACHE_CONFIG,
    SESSION_DB_URI,
)

log = logging.getLogger(__name__)

APP_NAME = "scummbar_chat"

# Singleton structures: shared globally across the module execution lifespan
_session_service: DatabaseSessionService | None = None
_artifact_service: InMemoryArtifactService | None = None
_runner: Runner | None = None


async def purge_old_sessions(hours: int = 24) -> int:
    """Removes historical events older than X hours from the ADK SQLite backend."""
    cutoff_time = datetime.now(UTC) - timedelta(hours=hours)
    cutoff_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")

    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
    loop = asyncio.get_running_loop()

    def _execute_purge() -> int:
        try:
            with sqlite3.connect(db_path, timeout=10.0) as conn:
                cursor = conn.cursor()
                cursor.execute("PRAGMA busy_timeout=10000;")
                # Targets the standard ADK 'events' table to clear bulky raw dialogue rows
                cursor.execute("DELETE FROM events WHERE timestamp < ?", (cutoff_str,))
                conn.commit()
                return cursor.rowcount
        except sqlite3.OperationalError as e:
            log.error("Database error during session purging: %s", e)
            return 0

    deleted_rows = await loop.run_in_executor(None, _execute_purge)
    if deleted_rows > 0:
        log.info("🧹 Galley cleanup: removed %d old events from the database.", deleted_rows)

    return deleted_rows


def _get_runner() -> Runner:
    """Lazy initializer ensuring the ADK runner and DB session layer exist as a singleton."""
    global _session_service, _artifact_service, _runner
    if _runner is None:
        _session_service = DatabaseSessionService(db_url=SESSION_DB_URI)
        _artifact_service = InMemoryArtifactService()

        # Inject the compaction model into the LLM-based summarizer
        compaction_summarizer = LlmEventSummarizer(llm=COMPACTION_LLM)

        compaction_config = EventsCompactionConfig(compaction_interval=COMPACTION_INTERVAL, overlap_size=COMPACTION_OVERLAP, summarizer=compaction_summarizer)

        scummbar_app = App(
            name=APP_NAME,
            root_agent=root_agent,
            events_compaction_config=compaction_config,
            context_cache_config=CONTEXT_CACHE_CONFIG,
        )

        # Attach the App instance (with compaction config) and Artifacts to the Runner
        _runner = Runner(
            app=scummbar_app,
            session_service=_session_service,
            artifact_service=_artifact_service,
        )

        # Initialize OpenTelemetry distributed tracing with InMemorySpanExporter
        init_tracing()

        log.info(
            "ADK Runner initialized (Model: %s, Compaction Interval: %d, Overlap: %d, Context Cache: %s)",
            COMPACTION_MODEL,
            COMPACTION_INTERVAL,
            COMPACTION_OVERLAP,
            "enabled" if CONTEXT_CACHE_CONFIG else "disabled",
        )
    return _runner


async def _ensure_session(user_id: str, session_id: str) -> None:
    """Checks for active session tracking blocks and provisions them if missing."""
    svc = _get_runner().session_service
    session = await svc.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    if session is None:
        await svc.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id,
        )


async def run_agent(
    user_id: str,
    session_id: str,
    text: str,
) -> tuple[str, list[dict], dict]:
    """
    Dispatches augmented textual updates through the ADK coordinator.
    Returns a tuple: (text_response, list_of_artifacts, usage_summary)
    where usage_summary contains input/output/total tokens and workflow step count.
    """
    t0 = time.perf_counter()
    runner = _get_runner()
    await _ensure_session(user_id, session_id)

    log.debug("Dispatching turn to ADK coordinator (text_len=%d)", len(text))

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=text)],
    )

    response_parts: list[str] = []
    generated_files: list[dict] = []
    input_tokens = output_tokens = total_tokens = None
    workflow_steps = 0

    # Scope the whole ADK turn with a dedicated per-turn span exporter.
    # All spans generated during run_async are flushed to SQLite on exit.
    with turn_tracing():
        # Async stream loop consuming real-time tokens and events
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message,
        ):
            # 1. Extract Artifacts if Barnaby/Balthazar/Isolde generated any
            if event.actions and event.actions.artifact_delta:
                for filename, version in event.actions.artifact_delta.items():
                    # Load the bytes from the in-memory service
                    part = await _artifact_service.load_artifact(
                        app_name=APP_NAME,
                        user_id=user_id,
                        session_id=session_id,
                        filename=filename,
                        version=version,
                    )
                    if part and part.inline_data:
                        generated_files.append({"filename": filename, "bytes": part.inline_data.data})
                        log.info("Loaded generated artifact: '%s' (%d bytes)", filename, len(part.inline_data.data))

            # 2. Count workflow steps: one per model-generated response event (reasoning loop)
            if event.author == "model" and event.content and event.content.parts:
                workflow_steps += 1

            # 3. Collect token usage metadata (when provided by the model)
            usage = event.usage_metadata
            if usage is not None:
                if getattr(usage, "prompt_token_count", None) is not None:
                    input_tokens = usage.prompt_token_count
                if getattr(usage, "candidates_token_count", None) is not None:
                    output_tokens = usage.candidates_token_count
                if getattr(usage, "total_token_count", None) is not None:
                    total_tokens = usage.total_token_count

            # 4. Extract final textual dialogue
            if event.is_final_response() and event.content and event.content.parts:
                for part in event.content.parts:
                    # Discard internal thoughts to preserve standard dialogue formatting
                    if part.text and not getattr(part, "thought", False):
                        response_parts.append(part.text)

    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    final_text = "".join(response_parts).strip()

    log.debug(
        "ADK turn completed in %.1f ms (response_len=%d, artifacts=%d, steps=%d, tokens=%s/%s/%s)",
        elapsed_ms,
        len(final_text),
        len(generated_files),
        workflow_steps,
        input_tokens,
        output_tokens,
        total_tokens,
    )

    usage_summary = {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "workflow_steps": workflow_steps,
    }

    return final_text, generated_files, usage_summary
