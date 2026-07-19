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
from datetime import datetime, timedelta

from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from ..agent import root_agent
from ..utils import SESSION_DB_URI

log = logging.getLogger(__name__)

APP_NAME = "scummbar_chat"

# Singleton structures: shared globally across the module execution lifespan
_session_service: DatabaseSessionService | None = None
_runner: Runner | None = None

async def purge_old_sessions(hours: int = 24) -> int:
    """Removes historical events older than X hours from the ADK SQLite backend."""
    cutoff_time = datetime.utcnow() - timedelta(hours=hours)
    # ADK typically handles timestamps in standard string formats for SQLite
    cutoff_str = cutoff_time.strftime("%Y-%m-%d %H:%M:%S")

    # Clean the connection uri to extract the true absolute or relative file path
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "")
    loop = asyncio.get_running_loop()

    def _execute_purge() -> int:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                # Prune old entries from the 'events' table to contain token window inflation.
                # We target 'events' as defined by the ADK DDL schema,
                # leaving the 'sessions' keys intact.
                cursor.execute(
                    "DELETE FROM events WHERE timestamp < ?",
                    (cutoff_str,)
                )
                conn.commit()
                return cursor.rowcount
        except sqlite3.OperationalError as e:
            log.error("Database error during session purging: %s", e)
            return 0

    # Execute synchronous I/O on a separate thread pool to keep the event loop non-blocking
    deleted_rows = await loop.run_in_executor(None, _execute_purge)
    if deleted_rows > 0:
        log.info("🧹 Galley cleanup: removed %d old events from the database.", deleted_rows)

    return deleted_rows

def _get_runner() -> Runner:
    """Lazy initializer ensuring the ADK runner and DB session layer exist as a singleton."""
    global _session_service, _runner
    if _runner is None:
        _session_service = DatabaseSessionService(db_url=SESSION_DB_URI)
        _runner = Runner(
            agent=root_agent,
            app_name=APP_NAME,
            session_service=_session_service,
        )
        log.info("ADK Runner initialized (DatabaseSessionService)")
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
) -> str:
    """Dispatches augmented textual updates through the ADK coordinator and extracts generation content."""
    runner = _get_runner()
    await _ensure_session(user_id, session_id)

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=text)],
    )

    response_parts: list[str] = []
    # Async stream processing of agent event cycles
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                # Omit thought processing tokens to keep the public output clean
                if part.text and not getattr(part, 'thought', False):
                    response_parts.append(part.text)

    return "".join(response_parts).strip()
