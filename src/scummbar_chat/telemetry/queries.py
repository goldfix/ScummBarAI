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
