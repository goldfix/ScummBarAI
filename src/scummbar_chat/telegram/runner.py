"""ADK Runner for the Telegram adapter.

Manages persistent sessions (SQLite) and invokes agents.
"""

import logging
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.genai import types

from ..agent import root_agent
from ..utils import SESSION_DB_URI

log = logging.getLogger(__name__)

APP_NAME = "scummbar_chat"

# Singleton: shared Runner + SessionService
_session_service: DatabaseSessionService | None = None
_runner: Runner | None = None


def _get_runner() -> Runner:
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
    """Create the session if it doesn't exist."""
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
    """Invoke the root_agent and return the final response text.

    Args:
        user_id:    Telegram user ID (str).
        session_id: ADK session ID (= group chat_id).
        text:       Message text already augmented with routing hint.

    Returns:
        Final response text from the agent, or empty string.
    """
    runner = _get_runner()
    await _ensure_session(user_id, session_id)

    user_message = types.Content(
        role="user",
        parts=[types.Part(text=text)],
    )

    response_parts: list[str] = []
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                # Skip thought parts (DeepSeek/Gemini internal reasoning)
                if part.text and not getattr(part, 'thought', False):
                    response_parts.append(part.text)

    return "".join(response_parts).strip()
