"""Package: scummbar_chat.telemetry
Description: Centralized observability infrastructure (Logging, Metrics, Tracing).
"""

from .context import (
    agent_name_var,
    channel_var,
    format_context_prefix,
    get_log_context,
    log_context,
    reset_log_context,
    session_id_var,
    set_log_context,
    turn_id_var,
    user_id_var,
)
from .db import (
    DEFAULT_OBSERVABILITY_DB,
    connection,
    get_connection,
    init_observability_db,
)
from .logging import (
    APP_LOG_FILE,
    DEFAULT_LOG_DIR,
    ERRORS_LOG_FILE,
    format_log_line_html,
    get_available_log_files,
    read_log_tail,
    render_logs_html,
    setup_logging,
)
from .metrics import (
    measure_tool,
    record_agent_metric,
    record_tool_metric,
    record_turn_metric,
)
from .queries import (
    get_agent_breakdown,
    get_kpi_summary,
    get_recent_trace_turns,
    get_recent_turns,
    get_time_series_data,
    get_tool_breakdown,
    get_turn_trace_tree,
)
from .tracing import (
    flush_spans_to_db,
    get_tracer,
    init_tracing,
    trace_span,
    turn_tracing,
)
from .viewer import render_waterfall_html

__all__ = [
    "APP_LOG_FILE",
    "DEFAULT_LOG_DIR",
    "DEFAULT_OBSERVABILITY_DB",
    "ERRORS_LOG_FILE",
    "agent_name_var",
    "channel_var",
    "connection",
    "flush_spans_to_db",
    "format_context_prefix",
    "format_log_line_html",
    "get_agent_breakdown",
    "get_available_log_files",
    "get_connection",
    "get_kpi_summary",
    "get_log_context",
    "get_recent_trace_turns",
    "get_recent_turns",
    "get_time_series_data",
    "get_tool_breakdown",
    "get_tracer",
    "get_turn_trace_tree",
    "init_observability_db",
    "init_tracing",
    "log_context",
    "measure_tool",
    "read_log_tail",
    "record_agent_metric",
    "record_tool_metric",
    "record_turn_metric",
    "render_logs_html",
    "render_waterfall_html",
    "reset_log_context",
    "session_id_var",
    "set_log_context",
    "setup_logging",
    "trace_span",
    "turn_id_var",
    "turn_tracing",
    "user_id_var",
]
