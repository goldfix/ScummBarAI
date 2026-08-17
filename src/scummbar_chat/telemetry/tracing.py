"""Module: tracing.py
Description: OpenTelemetry distributed tracing integration with local SQLite persistence.
Captures hierarchical GenAI spans (agents, workflows, tool calls, model generations)
using per-turn InMemorySpanExporters that flush to `observability.db` at turn completion.

Each turn gets its OWN in-memory exporter (registered in a fan-out list) so that
concurrent turns (different Telegram bots or parallel Streamlit sessions) never
steal or overwrite each other's spans.
"""

import json
import logging
import threading
from collections.abc import Generator, Sequence
from contextlib import contextmanager
from datetime import UTC, datetime
from typing import Any

import opentelemetry.trace as trace
from google.adk.telemetry.setup import OTelHooks, maybe_set_otel_providers
from opentelemetry.sdk.trace import ReadableSpan
from opentelemetry.sdk.trace.export import (
    SimpleSpanProcessor,
    SpanExporter,
    SpanExportResult,
)
from opentelemetry.sdk.trace.export.in_memory_span_exporter import (
    InMemorySpanExporter,
)

from .context import turn_id_var
from .db import connection, init_observability_db

log = logging.getLogger(__name__)

# Registry of active per-turn exporters (thread-safe via lock).
_exporters: list[InMemorySpanExporter] = []
_exporters_lock = threading.Lock()
_tracing_initialized: bool = False


class _FanOutSpanExporter(SpanExporter):
    """SpanExporter that fans out every finished span to all registered exporters.

    The global TracerProvider is configured ONCE with this exporter; each active
    turn registers its own InMemorySpanExporter, so spans are isolated per turn.
    """

    def export(self, spans: Sequence[ReadableSpan]) -> SpanExportResult:
        with _exporters_lock:
            targets = list(_exporters)
        for exporter in targets:
            exporter.export(list(spans))
        return SpanExportResult.SUCCESS

    def shutdown(self) -> None:
        return None

    def force_flush(self, timeout_millis: int = 30000) -> bool:
        return True


def init_tracing() -> None:
    """Initialize OpenTelemetry tracer provider with a fan-out span exporter.

    Configures Google ADK's telemetry hooks so all internal agent interactions,
    tool executions, and model calls automatically generate spans.
    """
    global _tracing_initialized
    if _tracing_initialized:
        return

    init_observability_db()

    processor = SimpleSpanProcessor(_FanOutSpanExporter())
    hooks = OTelHooks(span_processors=[processor])

    try:
        maybe_set_otel_providers([hooks])
        log.info("OpenTelemetry tracing initialized (fan-out InMemorySpanExporters)")
    except Exception as exc:
        log.warning("Failed to initialize OTel providers in ADK: %s", exc)

    _tracing_initialized = True


def get_tracer() -> trace.Tracer:
    """Return the application-level OpenTelemetry tracer."""
    init_tracing()
    return trace.get_tracer("scummbar_chat")


@contextmanager
def turn_tracing(turn_id: str | None = None) -> Generator[InMemorySpanExporter, None, None]:
    """Scope a turn with a dedicated in-memory span exporter.

    A root span is started to anchor the whole trace; on exit, only the spans
    belonging to this turn's trace_id are flushed to SQLite and the exporter is
    removed from the registry (isolating concurrent turns).
    """
    init_tracing()

    exporter = InMemorySpanExporter()
    with _exporters_lock:
        _exporters.append(exporter)

    tracer = get_tracer()
    try:
        # Anchor the turn: ADK spans (invoke_agent, execute_tool, generate_content)
        # nest under this root span and therefore share the same trace_id.
        with tracer.start_as_current_span("invoke_agent:scummbar_turn") as root_span:
            span_context = root_span.get_span_context()
            root_trace_id = f"{span_context.trace_id:032x}" if span_context else None
            yield exporter
    finally:
        try:
            flush_spans_to_db(exporter, turn_id=turn_id, trace_id=root_trace_id)
        finally:
            with _exporters_lock:
                if exporter in _exporters:
                    _exporters.remove(exporter)


@contextmanager
def trace_span(
    name: str,
    attributes: dict[str, Any] | None = None,
) -> Generator[trace.Span, None, None]:
    """Context manager to create a custom span in the current active turn."""
    tracer = get_tracer()
    with tracer.start_as_current_span(name) as span:
        if attributes:
            for k, v in attributes.items():
                if v is not None:
                    span.set_attribute(k, v)
        yield span


def flush_spans_to_db(
    exporter: InMemorySpanExporter,
    turn_id: str | None = None,
    trace_id: str | None = None,
) -> list[dict]:
    """Extract finished spans from an exporter, write them to SQLite, clear memory.

    When ``trace_id`` is provided, only spans belonging to that trace are
    persisted (concurrent turns share the fan-out but stay isolated).
    """
    if exporter is None:
        return []

    finished_spans = exporter.get_finished_spans()
    if not finished_spans:
        return []

    resolved_turn_id = turn_id or turn_id_var.get() or "untracked"
    parsed_records: list[dict] = []
    db_rows: list[tuple] = []

    for span in finished_spans:
        # Skip spans without a valid context (defensive against malformed spans)
        if span.context is None:
            continue

        # Filter spans by the turn's trace_id when anchored (concurrency isolation)
        if trace_id and f"{span.context.trace_id:032x}" != trace_id:
            continue

        span_id = f"{span.context.span_id:016x}"
        trace_id = f"{span.context.trace_id:032x}"
        parent_span_id = (
            f"{span.parent.span_id:016x}" if span.parent is not None else None
        )

        start_ns = span.start_time or 0
        end_ns = span.end_time or start_ns
        duration_ms = round((end_ns - start_ns) / 1_000_000.0, 2)

        start_iso = datetime.fromtimestamp(start_ns / 1e9, tz=UTC).strftime(
            "%Y-%m-%d %H:%M:%S.%f"
        )[:-3]

        status_code = span.status.status_code.name if span.status else "OK"
        status_desc = span.status.description if span.status else None

        attr_dict = dict(span.attributes or {})
        attr_json = json.dumps(attr_dict, default=str) if attr_dict else None

        events_list = [
            {
                "name": e.name,
                "timestamp": e.timestamp,
                "attributes": dict(e.attributes or {}),
            }
            for e in span.events
        ]
        events_json = json.dumps(events_list, default=str) if events_list else None

        db_rows.append(
            (
                span_id,
                trace_id,
                parent_span_id,
                resolved_turn_id,
                span.name,
                start_ns,
                end_ns,
                start_iso,
                duration_ms,
                status_code,
                status_desc,
                attr_json,
                events_json,
            )
        )

        parsed_records.append(
            {
                "span_id": span_id,
                "trace_id": trace_id,
                "parent_span_id": parent_span_id,
                "turn_id": resolved_turn_id,
                "name": span.name,
                "start_time_iso": start_iso,
                "duration_ms": duration_ms,
                "status_code": status_code,
                "attributes": attr_dict,
            }
        )

    if not db_rows:
        return []

    try:
        with connection() as conn:
            conn.executemany(
                """
                INSERT OR REPLACE INTO trace_spans (
                    span_id, trace_id, parent_span_id, turn_id, name,
                    start_time_ns, end_time_ns, start_time_iso, duration_ms,
                    status_code, status_description, attributes_json, events_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                db_rows,
            )
        log.debug(
            "Flushed %d trace spans to observability.db (turn_id=%s)",
            len(db_rows),
            resolved_turn_id,
        )
    except Exception as exc:
        log.warning("Failed to flush trace spans to SQLite: %s", exc)
    finally:
        exporter.clear()

    return parsed_records
