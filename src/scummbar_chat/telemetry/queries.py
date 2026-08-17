"""Module: queries.py
Description: Analytical aggregation queries for metrics visualization in Streamlit.
Provides summaries, percentiles, breakdowns by agent/tool, and time-series data.
"""

from .db import connection


def get_kpi_summary(channel_filter: str | None = None) -> dict:
    """Compute top-level KPI metrics across all recorded turns and tools."""
    use_filter = bool(channel_filter and channel_filter != "ALL")

    with connection() as conn:
        # Turn Aggregations
        if use_filter:
            cursor = conn.execute(
                """
                SELECT
                    COUNT(*) as total_turns,
                    AVG(total_duration_ms) as avg_duration,
                    MIN(total_duration_ms) as min_duration,
                    MAX(total_duration_ms) as max_duration,
                    SUM(artifacts_count) as total_artifacts,
                    SUM(is_error) as total_errors
                FROM turn_metrics
                WHERE channel = ?
                """,
                (channel_filter,),
            )
        else:
            cursor = conn.execute(
                """
                SELECT
                    COUNT(*) as total_turns,
                    AVG(total_duration_ms) as avg_duration,
                    MIN(total_duration_ms) as min_duration,
                    MAX(total_duration_ms) as max_duration,
                    SUM(artifacts_count) as total_artifacts,
                    SUM(is_error) as total_errors
                FROM turn_metrics
                """
            )
        row = cursor.fetchone()

        total_turns = row["total_turns"] or 0
        avg_duration = round(row["avg_duration"] or 0, 1)
        min_duration = round(row["min_duration"] or 0, 1)
        max_duration = round(row["max_duration"] or 0, 1)
        total_artifacts = row["total_artifacts"] or 0
        total_errors = row["total_errors"] or 0

        # Tool Aggregations
        tool_cursor = conn.execute("""
            SELECT
                COUNT(*) as total_calls,
                SUM(success) as success_calls,
                AVG(duration_ms) as avg_tool_duration
            FROM tool_metrics
        """)
        t_row = tool_cursor.fetchone()
        total_tools = t_row["total_calls"] or 0
        success_tools = t_row["success_calls"] or 0
        avg_tool_duration = round(t_row["avg_tool_duration"] or 0, 1)

        tool_success_rate = (
            round((success_tools / total_tools) * 100, 1) if total_tools > 0 else 100.0
        )

        return {
            "total_turns": total_turns,
            "avg_turn_duration_ms": avg_duration,
            "min_turn_duration_ms": min_duration,
            "max_turn_duration_ms": max_duration,
            "total_artifacts": total_artifacts,
            "total_errors": total_errors,
            "total_tool_calls": total_tools,
            "avg_tool_duration_ms": avg_tool_duration,
            "tool_success_rate_pct": tool_success_rate,
        }


def get_agent_breakdown(channel_filter: str | None = None) -> list[dict]:
    """Return average latency and turn count per target agent."""
    use_filter = bool(channel_filter and channel_filter != "ALL")

    with connection() as conn:
        if use_filter:
            cursor = conn.execute(
                """
                SELECT
                    target_agent,
                    COUNT(*) as turn_count,
                    ROUND(AVG(total_duration_ms), 1) as avg_latency_ms,
                    ROUND(MIN(total_duration_ms), 1) as min_latency_ms,
                    ROUND(MAX(total_duration_ms), 1) as max_latency_ms
                FROM turn_metrics
                WHERE channel = ?
                GROUP BY target_agent
                ORDER BY turn_count DESC
                """,
                (channel_filter,),
            )
        else:
            cursor = conn.execute(
                """
                SELECT
                    target_agent,
                    COUNT(*) as turn_count,
                    ROUND(AVG(total_duration_ms), 1) as avg_latency_ms,
                    ROUND(MIN(total_duration_ms), 1) as min_latency_ms,
                    ROUND(MAX(total_duration_ms), 1) as max_latency_ms
                FROM turn_metrics
                GROUP BY target_agent
                ORDER BY turn_count DESC
                """
            )
        return [dict(r) for r in cursor.fetchall()]


def get_tool_breakdown() -> list[dict]:
    """Return performance and invocation metrics grouped by tool name."""
    with connection() as conn:
        cursor = conn.execute("""
            SELECT
                tool_name,
                COUNT(*) as call_count,
                SUM(success) as success_count,
                COUNT(*) - SUM(success) as error_count,
                ROUND(AVG(duration_ms), 1) as avg_latency_ms,
                ROUND(MIN(duration_ms), 1) as min_latency_ms,
                ROUND(MAX(duration_ms), 1) as max_latency_ms,
                ROUND((CAST(SUM(success) AS FLOAT) / COUNT(*)) * 100, 1) as success_rate_pct
            FROM tool_metrics
            GROUP BY tool_name
            ORDER BY call_count DESC
        """)
        return [dict(r) for r in cursor.fetchall()]


def get_recent_turns(
    limit: int = 50,
    channel_filter: str | None = None,
    agent_filter: str | None = None,
) -> list[dict]:
    """Return recent turn records with joined tool summary."""
    use_channel = bool(channel_filter and channel_filter != "ALL")
    use_agent = bool(agent_filter and agent_filter != "ALL")

    with connection() as conn:
        if use_channel and use_agent:
            cursor = conn.execute(
                """
                SELECT
                    turn_id, timestamp, channel, session_id, user_id, patron_name,
                    target_agent, total_duration_ms, prompt_length, response_length,
                    artifacts_count, workflow_steps, is_error, error_message,
                    input_tokens, output_tokens, total_tokens
                FROM turn_metrics
                WHERE channel = ? AND target_agent = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (channel_filter, agent_filter, limit),
            )
        elif use_channel:
            cursor = conn.execute(
                """
                SELECT
                    turn_id, timestamp, channel, session_id, user_id, patron_name,
                    target_agent, total_duration_ms, prompt_length, response_length,
                    artifacts_count, workflow_steps, is_error, error_message,
                    input_tokens, output_tokens, total_tokens
                FROM turn_metrics
                WHERE channel = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (channel_filter, limit),
            )
        elif use_agent:
            cursor = conn.execute(
                """
                SELECT
                    turn_id, timestamp, channel, session_id, user_id, patron_name,
                    target_agent, total_duration_ms, prompt_length, response_length,
                    artifacts_count, workflow_steps, is_error, error_message,
                    input_tokens, output_tokens, total_tokens
                FROM turn_metrics
                WHERE target_agent = ?
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (agent_filter, limit),
            )
        else:
            cursor = conn.execute(
                """
                SELECT
                    turn_id, timestamp, channel, session_id, user_id, patron_name,
                    target_agent, total_duration_ms, prompt_length, response_length,
                    artifacts_count, workflow_steps, is_error, error_message,
                    input_tokens, output_tokens, total_tokens
                FROM turn_metrics
                ORDER BY timestamp DESC
                LIMIT ?
                """,
                (limit,),
            )
        turns = [dict(r) for r in cursor.fetchall()]

        # Query and attach tool execution counts for each turn
        for turn in turns:
            t_cursor = conn.execute(
                """
                SELECT tool_name, duration_ms, success, artifact_filename
                FROM tool_metrics
                WHERE turn_id = ?
                """,
                (turn["turn_id"],),
            )
            turn["tools"] = [dict(tr) for tr in t_cursor.fetchall()]

        return turns


def get_time_series_data(limit: int = 50) -> list[dict]:
    """Return timestamp and latency data for trend charts."""
    with connection() as conn:
        cursor = conn.execute(
            """
            SELECT timestamp, total_duration_ms, target_agent, channel
            FROM turn_metrics
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )
        rows = [dict(r) for r in cursor.fetchall()]
        rows.reverse()  # Chronological order for plotting
        return rows


def get_recent_trace_turns(limit: int = 30) -> list[dict]:
    """Return turns that have recorded trace spans available."""
    with connection() as conn:
        cursor = conn.execute(
            """
            SELECT DISTINCT
                t.turn_id,
                t.timestamp,
                t.channel,
                t.session_id,
                t.patron_name,
                t.target_agent,
                t.total_duration_ms,
                t.is_error,
                COUNT(s.span_id) as span_count
            FROM turn_metrics t
            JOIN trace_spans s ON t.turn_id = s.turn_id
            GROUP BY t.turn_id
            ORDER BY t.timestamp DESC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(r) for r in cursor.fetchall()]


def _classify_span(name: str, status_code: str, attr: dict) -> tuple[str, str, str]:
    """Classify span into category, semantic color, and badge icon.

    Returns:
        tuple of (category, hex_color, icon)
    """
    if status_code == "ERROR":
        return "error", "#f38ba8", "🔴"

    n_lower = name.lower()
    if "invoke_agent" in n_lower or "invoke_workflow" in n_lower:
        return "agent", "#cba6f7", "🟣"
    if "execute_tool" in n_lower:
        return "tool", "#fab387", "🟠"
    if "image" in n_lower or "tarot" in n_lower or "map" in n_lower:
        return "image", "#a6e3a1", "🟢"
    if "generate_content" in n_lower or "llm" in n_lower:
        return "llm", "#89b4fa", "🔵"

    return "generic", "#cdd6f4", "⚪"


def get_turn_trace_tree(turn_id: str) -> dict:
    """Retrieve and compute hierarchical waterfall timeline data for a turn."""
    import json

    with connection() as conn:
        cursor = conn.execute(
            """
            SELECT
                span_id, trace_id, parent_span_id, turn_id, name,
                start_time_ns, end_time_ns, start_time_iso, duration_ms,
                status_code, status_description, attributes_json, events_json
            FROM trace_spans
            WHERE turn_id = ?
            ORDER BY start_time_ns ASC
            """,
            (turn_id,),
        )
        rows = [dict(r) for r in cursor.fetchall()]

    if not rows:
        return {
            "turn_id": turn_id,
            "trace_id": None,
            "total_duration_ms": 0,
            "span_count": 0,
            "spans": [],
        }

    trace_id = rows[0]["trace_id"]
    min_start_ns = min(r["start_time_ns"] for r in rows)
    max_end_ns = max(r["end_time_ns"] for r in rows)
    total_duration_ms = round((max_end_ns - min_start_ns) / 1_000_000.0, 2)
    if total_duration_ms <= 0:
        total_duration_ms = max(r["duration_ms"] for r in rows) or 1.0

    # Build parent-child mapping to calculate hierarchy depth
    id_to_row = {r["span_id"]: r for r in rows}

    def _calc_depth(span_id: str, visited: set | None = None) -> int:
        if visited is None:
            visited = set()
        if span_id in visited:
            return 0
        visited.add(span_id)
        parent_id = id_to_row.get(span_id, {}).get("parent_span_id")
        if not parent_id or parent_id not in id_to_row:
            return 0
        return 1 + _calc_depth(parent_id, visited)

    timeline_spans: list[dict] = []
    for r in rows:
        offset_ms = round((r["start_time_ns"] - min_start_ns) / 1_000_000.0, 2)
        offset_pct = max(0.0, min(99.0, (offset_ms / total_duration_ms) * 100))
        width_pct = max(1.5, min(100.0 - offset_pct, (r["duration_ms"] / total_duration_ms) * 100))
        depth = _calc_depth(r["span_id"])

        attr = json.loads(r["attributes_json"]) if r["attributes_json"] else {}
        events = json.loads(r["events_json"]) if r["events_json"] else []

        category, color, icon = _classify_span(r["name"], r["status_code"], attr)

        timeline_spans.append(
            {
                "span_id": r["span_id"],
                "parent_span_id": r["parent_span_id"],
                "name": r["name"],
                "duration_ms": r["duration_ms"],
                "offset_ms": offset_ms,
                "offset_pct": round(offset_pct, 2),
                "width_pct": round(width_pct, 2),
                "depth": depth,
                "category": category,
                "color": color,
                "icon": icon,
                "status_code": r["status_code"],
                "status_description": r["status_description"],
                "start_time_iso": r["start_time_iso"],
                "attributes": attr,
                "events": events,
            }
        )

    return {
        "turn_id": turn_id,
        "trace_id": trace_id,
        "total_duration_ms": total_duration_ms,
        "span_count": len(timeline_spans),
        "spans": timeline_spans,
    }
