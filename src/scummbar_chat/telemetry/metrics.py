"""Module: metrics.py
Description: Performance metrics tracking, measurement decorators, and recording engines.
Persists execution timings for turns, agents, and tools to the SQLite telemetry database.
"""

import functools
import json
import logging
import re
import time
from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any

from .context import turn_id_var
from .db import connection, init_observability_db

log = logging.getLogger(__name__)

# Initialize database tables on import
init_observability_db()


def record_turn_metric(
    turn_id: str,
    channel: str,
    session_id: str,
    user_id: str,
    target_agent: str,
    total_duration_ms: float,
    patron_name: str | None = None,
    prompt_length: int = 0,
    response_length: int = 0,
    artifacts_count: int = 0,
    workflow_steps: int = 0,
    is_error: bool = False,
    error_message: str | None = None,
    input_tokens: int | None = None,
    output_tokens: int | None = None,
    total_tokens: int | None = None,
    timestamp: datetime | None = None,
) -> None:
    """Record an end-to-end conversation turn measurement into the telemetry DB."""
    now_dt = timestamp or datetime.now(UTC)
    now_iso = now_dt.strftime("%Y-%m-%d %H:%M:%S")

    try:
        with connection() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO turn_metrics (
                    turn_id, timestamp, channel, session_id, user_id, patron_name,
                    target_agent, total_duration_ms, prompt_length, response_length,
                    artifacts_count, workflow_steps, is_error, error_message, input_tokens,
                    output_tokens, total_tokens
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    turn_id,
                    now_iso,
                    channel,
                    session_id,
                    user_id,
                    patron_name,
                    target_agent,
                    round(total_duration_ms, 2),
                    prompt_length,
                    response_length,
                    artifacts_count,
                    workflow_steps,
                    1 if is_error else 0,
                    error_message,
                    input_tokens,
                    output_tokens,
                    total_tokens,
                ),
            )
    except Exception as exc:
        log.warning("Failed to record turn metric (turn_id=%s): %s", turn_id, exc)


def record_tool_metric(
    tool_name: str,
    duration_ms: float,
    success: bool = True,
    turn_id: str | None = None,
    error_type: str | None = None,
    error_message: str | None = None,
    artifact_filename: str | None = None,
    metadata: dict | None = None,
    timestamp: datetime | None = None,
) -> None:
    """Record a tool execution measurement into the telemetry DB."""
    resolved_turn_id = turn_id or turn_id_var.get() or "untracked"
    now_dt = timestamp or datetime.now(UTC)
    now_iso = now_dt.strftime("%Y-%m-%d %H:%M:%S")
    meta_json = json.dumps(metadata) if metadata else None

    try:
        with connection() as conn:
            conn.execute(
                """
                INSERT INTO tool_metrics (
                    turn_id, timestamp, tool_name, duration_ms, success,
                    error_type, error_message, artifact_filename, metadata_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    resolved_turn_id,
                    now_iso,
                    tool_name,
                    round(duration_ms, 2),
                    1 if success else 0,
                    error_type,
                    error_message,
                    artifact_filename,
                    meta_json,
                ),
            )
    except Exception as exc:
        log.warning("Failed to record tool metric (%s): %s", tool_name, exc)


def record_agent_metric(
    agent_name: str,
    duration_ms: float,
    turn_id: str | None = None,
    model_name: str | None = None,
    status: str = "success",
    timestamp: datetime | None = None,
) -> None:
    """Record execution timing for an agent or coordinator into the telemetry DB."""
    resolved_turn_id = turn_id or turn_id_var.get() or "untracked"
    now_dt = timestamp or datetime.now(UTC)
    now_iso = now_dt.strftime("%Y-%m-%d %H:%M:%S")

    try:
        with connection() as conn:
            conn.execute(
                """
                INSERT INTO agent_metrics (
                    turn_id, timestamp, agent_name, duration_ms, model_name, status
                ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    resolved_turn_id,
                    now_iso,
                    agent_name,
                    round(duration_ms, 2),
                    model_name,
                    status,
                ),
            )
    except Exception as exc:
        log.warning("Failed to record agent metric (%s): %s", agent_name, exc)


# Regex to detect generated artifact filenames in return messages
_ARTIFACT_FILENAME_RE = re.compile(
    r"(?:Salvata come|Pergamena|assets/)\s*['\"]?([a-zA-Z0-9_\.]+\.(?:png|jpg|jpeg|txt))['\"]?",
    re.IGNORECASE,
)


def measure_tool(tool_name: str) -> Callable:
    """Decorator to automatically measure and record async tool execution metrics."""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            t0 = time.perf_counter()
            success = True
            err_type = None
            err_msg = None
            artifact_file = None

            try:
                result = await func(*args, **kwargs)

                # Scan result for generated artifacts if string or dict
                if isinstance(result, str):
                    m = _ARTIFACT_FILENAME_RE.search(result)
                    if m:
                        artifact_file = m.group(1)
                elif isinstance(result, dict) and result.get("status") == "error":
                    success = False
                    err_msg = result.get("message")

                return result

            except Exception as exc:
                success = False
                err_type = exc.__class__.__name__
                err_msg = str(exc)
                raise

            finally:
                elapsed_ms = (time.perf_counter() - t0) * 1000.0
                record_tool_metric(
                    tool_name=tool_name,
                    duration_ms=elapsed_ms,
                    success=success,
                    error_type=err_type,
                    error_message=err_msg,
                    artifact_filename=artifact_file,
                )

        return wrapper

    return decorator
