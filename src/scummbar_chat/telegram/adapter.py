"""Telegram Adapter for Scummbar.

Handles:
- Long polling (getUpdates)
- Private message redirect to group
- @barnaby / @barnacle detection
- Per-bot lock (one user at a time)
- Public replies (Barnaby) and ephemeral (Barnacle)
"""

import asyncio
import logging
import os
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

from .formatter import format_response
from .runner import run_agent

load_dotenv(Path(__file__).parent.parent / ".env")

log = logging.getLogger(__name__)

# --- Config ---
TOKEN     = os.getenv("TELEGRAM_BOT_TOKEN", "")
BOT_USER  = os.getenv("TELEGRAM_BOT_USERNAME", "").lower()
GROUP_URL = os.getenv("TELEGRAM_GROUP_LINK", "")
BASE      = f"https://api.telegram.org/bot{TOKEN}"

# --- Per-bot lock: one user at a time ---
_locks: dict[str, asyncio.Lock] = {
    "barnaby":  asyncio.Lock(),
    "barnacle": asyncio.Lock(),
}

# --- In-character messages ---
_PRIVATE_REDIRECT = (
    "🍺 <i>La porta dello Scummbar è sempre aperta, compagno, "
    "ma le conversazioni private non fanno per me. "
    f"Vieni al bancone!</i>"
    + (f"\n👉 {GROUP_URL}" if GROUP_URL else "")
)

_BOT_BUSY = {
    "barnaby": (
        "<i>Barnaby alza un dito senza smettere di versare. "
        "«Un momento, compagno, sto servendo qualcuno...»</i>"
    ),
    "barnacle": (
        "<i>Barnacle ti lancia un'occhiataccia con l'occhio grigio. "
        "È occupato. Riprova tra poco.</i>"
    ),
}


# ---------------------------------------------------------------------------
# Helpers HTTP
# ---------------------------------------------------------------------------

async def _send_typing(http: aiohttp.ClientSession, chat_id: int) -> None:
    """Send the 'typing...' indicator."""
    try:
        await http.post(
            f"{BASE}/sendChatAction",
            json={"chat_id": chat_id, "action": "typing"},
        )
    except Exception:
        pass


async def _send_message(
    http: aiohttp.ClientSession,
    chat_id: int,
    text: str,
    receiver_user_id: int | None = None,
) -> bool:
    """Send an HTML message. If receiver_user_id is set → ephemeral.

    Returns:
        True if sent successfully, False otherwise.
    """
    payload: dict = {
        "chat_id":    chat_id,
        "text":       text,
        "parse_mode": "HTML",
    }
    if receiver_user_id:
        payload["receiver_user_id"] = receiver_user_id

    try:
        async with http.post(f"{BASE}/sendMessage", json=payload) as resp:
            data = await resp.json()
            if not data.get("ok"):
                log.warning("sendMessage failed: %s", data.get("description", data))
                return False
            return True
    except Exception as e:
        log.error("Errore sendMessage: %s", e)
        return False


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def _detect_bot(text: str) -> str | None:
    """Detect which bot is mentioned. Barnacle has priority (rarer).

    Returns:
        'barnaby' | 'barnacle' | None
    """
    tl = text.lower()
    if "@barnacle" in tl:
        return "barnacle"
    if "@barnaby" in tl:
        return "barnaby"
    return None


def _augment_text(text: str, bot_name: str) -> str:
    """Add a routing hint to the text for the ADK coordinator."""
    label = bot_name.upper()
    return f"[Risponde {label}] {text}"


# ---------------------------------------------------------------------------
# Single update handler
# ---------------------------------------------------------------------------

async def _handle_update(http: aiohttp.ClientSession, update: dict) -> None:
    message = update.get("message")
    if not message or not message.get("text"):
        return

    chat      = message["chat"]
    from_user = message["from"]
    chat_id   = int(chat["id"])
    user_id   = str(from_user["id"])
    text      = message["text"]
    chat_type = chat["type"]  # "private" | "group" | "supergroup"

    # 1. Private messages → in-character redirect
    if chat_type == "private":
        await _send_message(http, chat_id, _PRIVATE_REDIRECT)
        return

    # 2. Only messages with @mention to bots
    bot_name = _detect_bot(text)
    if not bot_name:
        return  # users chatting among themselves — we don't intervene

    # 3. Bot lock
    lock = _locks[bot_name]
    if lock.locked():
        await _send_message(http, chat_id, _BOT_BUSY[bot_name])
        return

    # 4. Processing
    async with lock:
        await _send_typing(http, chat_id)

        # Shared session_id for the group (all patrons share the same story)
        session_id = str(chat_id)

        # Augment text with routing hint for the coordinator
        augmented = _augment_text(text, bot_name)

        response = await run_agent(
            user_id=user_id,
            session_id=session_id,
            text=augmented,
        )

        if not response:
            log.warning("[%s] empty response from agent", bot_name)
            return

        log.info("[%s] %s: %s", bot_name, from_user.get('username', user_id), text[:60])

        formatted = format_response(response)

        # Barnacle → try ephemeral, fallback to public if bot is not admin
        # Barnaby  → always public in group
        if bot_name == "barnacle":
            sent = await _send_message(
                http, chat_id, formatted,
                receiver_user_id=int(user_id),
            )
            if not sent:
                # Fallback: public reply with a whisper note
                log.warning(
                    "Ephemeral failed (bot not admin?). "
                    "Tip: make the bot a group admin."
                )
                fallback = formatted + "\n\n<i>🐱 (whisper — just for you)</i>"
                await _send_message(http, chat_id, fallback)
        else:
            await _send_message(http, chat_id, formatted)


# ---------------------------------------------------------------------------
# Long polling loop
# ---------------------------------------------------------------------------

async def run_polling() -> None:
    """Start the Telegram long polling."""
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not configured in .env")

    offset = 0
    pending: set[asyncio.Task] = set()

    log.info("🍺 Scummbar Telegram bot started (long polling)")

    async with aiohttp.ClientSession() as http:
        while True:
            try:
                url = (
                    f"{BASE}/getUpdates"
                    f"?offset={offset}&timeout=30"
                    f'&allowed_updates=["message"]'
                )
                async with http.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=40),
                ) as resp:
                    data = await resp.json()

                for upd in data.get("result", []):
                    offset = upd["update_id"] + 1
                    task = asyncio.create_task(_handle_update(http, upd))
                    pending.add(task)
                    task.add_done_callback(pending.discard)

            except asyncio.CancelledError:
                log.info("Polling stopped.")
                break
            except Exception as e:
                log.error("Polling error: %s", e)
                await asyncio.sleep(5)

        # Wait for pending tasks before closing
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
