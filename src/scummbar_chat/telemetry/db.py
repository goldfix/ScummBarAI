"""Module: db.py
Description: SQLite storage and schema management for Scummbar observability & metrics.
Maintains high-performance WAL mode connections and guarantees proper closing via a
context manager (sqlite3 connections are NOT closed by the plain `with conn:` pattern).
"""

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

# Path to the dedicated observability database
DEFAULT_OBSERVABILITY_DB = (
    Path(__file__).parent.parent.parent.parent
    / "data"
    / "scummbar_chat"
    / "observability.db"
)


def get_db_path(db_path: Path | None = None) -> Path:
    """Resolve and ensure the directory for the observability database."""
    target = db_path or DEFAULT_OBSERVABILITY_DB
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def get_connection(db_path: Path | None = None) -> sqlite3.Connection:
    """Return a raw configured SQLite connection with WAL mode and row factory.

    Prefer the :func:`connection` context manager, which also closes the
    connection when the block exits.
    """
    path = get_db_path(db_path)
    conn = sqlite3.connect(path, timeout=15.0)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA busy_timeout=15000;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


@contextmanager
def connection(db_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    """Context manager yielding a connection that is committed and closed on exit."""
    conn = get_connection(db_path)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _ensure_column(conn: sqlite3.Connection, table: str, column: str, ddl: str) -> None:
    """Add a column to an existing table if it is missing (lightweight migration)."""
    columns = [row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()]
    if column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {ddl}")


def init_observability_db(db_path: Path | None = None) -> None:
    """Create the observability tables and indexes if they do not exist."""
    with connection(db_path) as conn:
        # 1. Turn Metrics: end-to-end conversation turn measurements
        conn.execute("""
            CREATE TABLE IF NOT EXISTS turn_metrics (
                turn_id             TEXT PRIMARY KEY,
                timestamp           DATETIME NOT NULL,
                channel             TEXT NOT NULL,
                session_id          TEXT NOT NULL,
                user_id             TEXT NOT NULL,
                patron_name         TEXT,
                target_agent        TEXT NOT NULL,
                total_duration_ms   REAL NOT NULL,
                prompt_length       INTEGER DEFAULT 0,
                response_length     INTEGER DEFAULT 0,
                artifacts_count     INTEGER DEFAULT 0,
                workflow_steps      INTEGER DEFAULT 0,
                is_error            INTEGER DEFAULT 0,
                error_message       TEXT,
                input_tokens        INTEGER,
                output_tokens       INTEGER,
                total_tokens        INTEGER
            );
        """)

        # 2. Tool Metrics: execution duration & status for individual tool calls
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tool_metrics (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                turn_id             TEXT NOT NULL,
                timestamp           DATETIME NOT NULL,
                tool_name           TEXT NOT NULL,
                duration_ms         REAL NOT NULL,
                success             INTEGER NOT NULL,
                error_type          TEXT,
                error_message       TEXT,
                artifact_filename   TEXT,
                metadata_json       TEXT
            );
        """)

        # 3. Agent Metrics: granular execution times for coordinators, sub-agents, chronicler
        conn.execute("""
            CREATE TABLE IF NOT EXISTS agent_metrics (
                id                  INTEGER PRIMARY KEY AUTOINCREMENT,
                turn_id             TEXT NOT NULL,
                timestamp           DATETIME NOT NULL,
                agent_name          TEXT NOT NULL,
                duration_ms         REAL NOT NULL,
                model_name          TEXT,
                status              TEXT DEFAULT 'success'
            );
        """)

        # 4. Trace Spans: hierarchical OpenTelemetry waterfall spans per turn
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trace_spans (
                span_id             TEXT PRIMARY KEY,
                trace_id            TEXT NOT NULL,
                parent_span_id      TEXT,
                turn_id             TEXT NOT NULL,
                name                TEXT NOT NULL,
                start_time_ns       INTEGER NOT NULL,
                end_time_ns         INTEGER NOT NULL,
                start_time_iso      TEXT NOT NULL,
                duration_ms         REAL NOT NULL,
                status_code         TEXT DEFAULT 'OK',
                status_description  TEXT,
                attributes_json     TEXT,
                events_json         TEXT
            );
        """)

        # Lightweight migration for pre-existing databases
        _ensure_column(
            conn,
            "turn_metrics",
            "workflow_steps",
            "workflow_steps INTEGER DEFAULT 0",
        )

        # Indexes for fast filtering and time-series aggregation
        conn.execute("CREATE INDEX IF NOT EXISTS idx_turn_timestamp ON turn_metrics(timestamp);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_turn_agent ON turn_metrics(target_agent);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_turn_channel ON turn_metrics(channel);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tool_turn_id ON tool_metrics(turn_id);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_tool_name ON tool_metrics(tool_name);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_agent_turn_id ON agent_metrics(turn_id);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_agent_name ON agent_metrics(agent_name);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_span_turn_id ON trace_spans(turn_id);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_span_trace_id ON trace_spans(trace_id);")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_span_parent ON trace_spans(parent_span_id);")

        conn.commit()
