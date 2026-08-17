"""Module: context.py
Description: Asynchronous context variables management using Python standard library `contextvars`.
Enables correlation of logs and telemetry with channel, session, user, agent, and turn identifiers.
"""

from collections.abc import Generator
from contextlib import contextmanager
from contextvars import ContextVar, Token
from typing import Any

# Module-level Context Variables (PEP 567)
# NOTE: ContextVars MUST be created at module level, never inside closures
# (see https://docs.python.org/3.12/library/contextvars.html — 'Context Variables').
channel_var: ContextVar[str] = ContextVar("channel", default="")
session_id_var: ContextVar[str] = ContextVar("session_id", default="")
user_id_var: ContextVar[str] = ContextVar("user_id", default="")
agent_name_var: ContextVar[str] = ContextVar("agent_name", default="")
turn_id_var: ContextVar[str] = ContextVar("turn_id", default="")

# Short display aliases for channels (keeps log prefixes compact).
_CHANNEL_ABBR = {
    "telegram": "tg",
    "streamlit": "st",
}


def get_log_context() -> dict[str, str]:
    """Retrieve the current telemetry context dictionary."""
    return {
        "channel": channel_var.get(),
        "session_id": session_id_var.get(),
        "user_id": user_id_var.get(),
        "agent_name": agent_name_var.get(),
        "turn_id": turn_id_var.get(),
    }


def format_context_prefix() -> str:
    """Build a concise formatted prefix string for log records.

    Example outputs:
      "[tg:balthazar:u:123:t:45] "
      "[st:barnaby:u:8741] "
      ""
    """
    parts: list[str] = []

    channel = channel_var.get()
    if channel:
        parts.append(_CHANNEL_ABBR.get(channel, channel))

    agent = agent_name_var.get()
    if agent:
        parts.append(agent)

    user = user_id_var.get()
    if user:
        parts.append(f"u:{user}" if not user.startswith("u:") else user)

    turn = turn_id_var.get()
    if turn:
        parts.append(f"t:{turn}" if not turn.startswith("t:") else turn)

    if not parts:
        return ""

    return f"[{':'.join(parts)}] "


def set_log_context(
    channel: str | None = None,
    session_id: str | None = None,
    user_id: str | None = None,
    agent_name: str | None = None,
    turn_id: str | None = None,
) -> list[tuple[ContextVar[Any], Token[Any]]]:
    """Set one or more context variables, returning tokens for resetting."""
    tokens: list[tuple[ContextVar[Any], Token[Any]]] = []

    if channel is not None:
        tokens.append((channel_var, channel_var.set(channel)))
    if session_id is not None:
        tokens.append((session_id_var, session_id_var.set(session_id)))
    if user_id is not None:
        tokens.append((user_id_var, user_id_var.set(user_id)))
    if agent_name is not None:
        tokens.append((agent_name_var, agent_name_var.set(agent_name)))
    if turn_id is not None:
        tokens.append((turn_id_var, turn_id_var.set(turn_id)))

    return tokens


def reset_log_context(tokens: list[tuple[ContextVar[Any], Token[Any]]]) -> None:
    """Reset context variables using previously saved tokens."""
    for var, token in reversed(tokens):
        var.reset(token)


@contextmanager
def log_context(
    channel: str | None = None,
    session_id: str | None = None,
    user_id: str | None = None,
    agent_name: str | None = None,
    turn_id: str | None = None,
) -> Generator[None, None, None]:
    """Context manager to scope context variables across a block or turn execution."""
    tokens = set_log_context(
        channel=channel,
        session_id=session_id,
        user_id=user_id,
        agent_name=agent_name,
        turn_id=turn_id,
    )
    try:
        yield
    finally:
        reset_log_context(tokens)
