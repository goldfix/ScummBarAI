"""Module: logging.py
Description: Centralized logging configuration and utilities for Scummbar.
Provides context-aware rotating file handlers, console streaming, and HTML-formatted log viewers.
"""

import html
import logging
import re
from logging.handlers import RotatingFileHandler
from pathlib import Path

from .context import (
    agent_name_var,
    channel_var,
    format_context_prefix,
    session_id_var,
    turn_id_var,
    user_id_var,
)

# Standard Log Paths
DEFAULT_LOG_DIR = (
    Path(__file__).parent.parent.parent.parent
    / "data"
    / "scummbar_chat"
    / "logs"
)
APP_LOG_FILE = DEFAULT_LOG_DIR / "app.log"
ERRORS_LOG_FILE = DEFAULT_LOG_DIR / "errors.log"

LOG_FORMAT = "%(asctime)s [%(levelname)-8s] %(context_prefix)s%(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class ContextualFilter(logging.Filter):
    """Logging filter that injects contextual variables into the LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.channel = channel_var.get()
        record.session_id = session_id_var.get()
        record.user_id = user_id_var.get()
        record.agent_name = agent_name_var.get()
        record.turn_id = turn_id_var.get()
        record.context_prefix = format_context_prefix()
        return True


_logging_initialized = False


def setup_logging(
    debug: bool = False,
    log_dir: Path | None = None,
    force: bool = False,
) -> None:
    """Initialize console and rotating file logging handlers idempotently.

    Safe to call multiple times (e.g. Streamlit reruns): handlers are added
    only once unless ``force=True``, which first removes all root handlers.
    """
    global _logging_initialized
    if _logging_initialized and not force:
        return

    target_dir = log_dir or DEFAULT_LOG_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    app_log = target_dir / "app.log"
    err_log = target_dir / "errors.log"

    level = logging.DEBUG if debug else logging.INFO
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)  # Root captures all; handlers filter

    # Remove existing handlers if forcing re-initialization
    if force:
        for handler in list(root.handlers):
            root.removeHandler(handler)

    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    ctx_filter = ContextualFilter()

    # 1. Console Handler
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)
    console.addFilter(ctx_filter)
    root.addHandler(console)

    # 2. Main Rotating File Handler (app.log — 10 MB x 5 files)
    file_handler = RotatingFileHandler(
        app_log,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(ctx_filter)
    root.addHandler(file_handler)

    # 3. Dedicated Error Rotating Handler (errors.log — 5 MB x 3 files)
    err_handler = RotatingFileHandler(
        err_log,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(formatter)
    err_handler.addFilter(ctx_filter)
    root.addHandler(err_handler)

    _logging_initialized = True


def get_available_log_files(log_dir: Path | None = None) -> dict[str, Path]:
    """Discover all active log files in the target directory."""
    target_dir = log_dir or DEFAULT_LOG_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    files: dict[str, Path] = {}
    for path in sorted(target_dir.glob("*.log")):
        files[path.name] = path
    return files


def _read_tail_bytes(file_path: Path, max_bytes: int = 2 * 1024 * 1024) -> str:
    """Read only the trailing portion of a (potentially large) log file.

    Avoids loading the whole file into memory on every Streamlit refresh.
    """
    size = file_path.stat().st_size
    with file_path.open("rb") as f:
        if size > max_bytes:
            f.seek(size - max_bytes)
            data = f.read().decode("utf-8", errors="replace")
            # Drop the first (possibly truncated) partial line.
            first_nl = data.find("\n")
            if first_nl != -1:
                data = data[first_nl + 1 :]
        else:
            data = f.read().decode("utf-8", errors="replace")
    return data


def read_log_tail(
    file_path: Path,
    max_lines: int = 150,
    level_filter: str | None = None,
    search_query: str | None = None,
) -> list[str]:
    """Read the last N lines from a log file with optional level and keyword filtering."""
    if not file_path.exists():
        return [f"[Log file not found: {file_path.name}]"]

    try:
        data = _read_tail_bytes(file_path)
    except Exception as exc:
        return [f"[Error reading log file: {exc}]"]

    lines = data.splitlines()

    # Normalize filter parameters
    target_level = level_filter.strip().upper() if level_filter and level_filter != "ALL" else None
    query = search_query.strip().lower() if search_query else None

    filtered_lines: list[str] = []
    for line in lines:
        if target_level and f"[{target_level}" not in line.upper():
            continue
        if query and query not in line.lower():
            continue
        filtered_lines.append(line)

    return filtered_lines[-max_lines:]


# Regex pattern to identify structured log elements
# e.g.: "2026-07-26 15:30:00 [INFO    ] [tg:balthazar:u123] module_name: message text"
_LOG_LINE_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2})\s+\[([A-Z]+)\s*\]\s+(?:(\[[^\]]+\])\s+)?([^:]+):\s+(.*)$"
)

# Semantic Colors for Dark-Themed Log Terminal
_LEVEL_COLORS = {
    "DEBUG": "#89b4fa",     # Light Blue
    "INFO": "#a6e3a1",      # Emerald Green
    "WARNING": "#f9e2af",   # Warm Amber / Yellow
    "ERROR": "#f38ba8",     # Crimson Red
    "CRITICAL": "#ff5555",  # Bold Red
}


def format_log_line_html(raw_line: str) -> str:
    """Transform a raw text log line into a syntax-highlighted HTML string."""
    match = _LOG_LINE_RE.match(raw_line)
    if not match:
        # Traceback or unstructured continuation line
        escaped = html.escape(raw_line)
        if "Error" in raw_line or "Exception" in raw_line or "Traceback" in raw_line:
            return f'<div style="color: #f38ba8; padding-left: 20px;">{escaped}</div>'
        return f'<div style="color: #a6adc8; padding-left: 20px;">{escaped}</div>'

    ts, level, ctx, logger_name, msg = match.groups()
    lvl_color = _LEVEL_COLORS.get(level, "#cdd6f4")
    escaped_msg = html.escape(msg)
    escaped_logger = html.escape(logger_name.strip())

    ctx_html = (
        f'<span style="color: #cba6f7; font-weight: 500;">{html.escape(ctx)} </span>'
        if ctx
        else ""
    )

    return (
        f'<div style="line-height: 1.45; margin-bottom: 2px;">'
        f'<span style="color: #6c7086;">{ts}</span> '
        f'<span style="color: {lvl_color}; font-weight: bold; width: 65px; display: inline-block;">[{level}]</span> '
        f'{ctx_html}'
        f'<span style="color: #94e2d5;">{escaped_logger}</span>: '
        f'<span style="color: #cdd6f4;">{escaped_msg}</span>'
        f'</div>'
    )


def render_logs_html(lines: list[str]) -> str:
    """Package a list of log lines into a responsive dark terminal HTML container."""
    if not lines:
        return (
            '<div style="background-color: #1e1e2e; color: #6c7086; padding: 18px; '
            'border-radius: 8px; font-family: monospace; font-size: 0.9em; text-align: center;">'
            'Nessun record di log trovato per i filtri selezionati.</div>'
        )

    formatted_lines = [format_log_line_html(line) for line in lines]
    inner_html = "".join(formatted_lines)

    return (
        f'<div style="background-color: #181825; color: #cdd6f4; border: 1px solid #313244; '
        f'border-radius: 8px; padding: 14px 18px; font-family: \'JetBrains Mono\', \'Fira Code\', monospace; '
        f'font-size: 0.85em; max-height: 550px; overflow-y: auto; box-shadow: inset 0 2px 8px rgba(0,0,0,0.5);">'
        f'{inner_html}'
        f'</div>'
    )
