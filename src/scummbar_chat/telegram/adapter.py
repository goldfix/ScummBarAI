"""
Module: adapter.py
Operations:
- Orchestrates the Telegram Bot runtime via long polling (`getUpdates`).
- Implements concurrent request serialization using per-bot asynchronous locks.
- Manages request queueing timeouts (15 seconds) to prevent starvation.
- Handles multi-bot character routing based on mentions (@barnaby vs @barnacle).
- Implements a group-shared message counter to dynamically inject Narrator prompts.
- Runs a background cron task that triggers hourly database pruning for 24-hour retention.
"""

import asyncio
import logging
import os
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

from .formatter import format_response
from .runner import run_agent, purge_old_sessions

load_dotenv(Path(__file__).parent.parent / ".env")

log = logging.getLogger(__name__)

# --- Config ---
TOKEN     = os.getenv("TELEGRAM_BOT_TOKEN", "")
BOT_USER  = os.getenv("TELEGRAM_BOT_USERNAME", "").lower()
GROUP_URL = os.getenv("TELEGRAM_GROUP_LINK", "")
BASE      = f"https://api.telegram.org/bot{TOKEN}"

# --- Per-bot lock: prevents race conditions when updating the same session history ---
_locks: dict[str, asyncio.Lock] = {
    "barnaby":  asyncio.Lock(),
    "barnacle": asyncio.Lock(),
}

# --- Shared group message counters for Narrator logic ---
_message_counters: dict[str, int] = {}

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

# --- Semantic router: defines which bot should respond ---
_INTENT_MAP = {
    "barnaby": [
        "barnaby", "barista", "grog", "birra", "bere", "drink",
        "ordinare", "conto", "pulire", "servire"
    ],
    "barnacle": [
        "barnacle", "micio", "gatto", "felino", "bestia",
        "peloso", "dormire", "fusa", "soffia"
    ]
}

def _resolve_intent(text: str) -> str | None:
    """
    Detect which bot should respond, using @ tags or keyword matching.
    Tags have priority, followed by semantic keyword matching.
    """
    tl = text.lower()

    # 1. Priorità ai Tag (Metodo esplicito @)
    if "@barnacle" in tl: return "barnacle"
    if "@barnaby" in tl: return "barnaby"

    # 2. Semantic routing (keyword matching)
    for bot, keywords in _INTENT_MAP.items():
        if any(keyword in tl for keyword in keywords):
            return bot

    return None

async def _send_typing(http: aiohttp.ClientSession, chat_id: int) -> None:
    """Sends the standard Telegram 'typing...' chat action."""
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
    """Helper to dispatch HTML messages, supporting ephemeral targets via receiver_user_id."""
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
        log.error("Error in sendMessage: %s", e)
        return False

def _augment_text(text: str, bot_name: str) -> str:
    """Appends routing metadata so the core coordinator knows who is responding."""
    label = bot_name.upper()
    return f"[Risponde {label}] {text}"

async def _handle_update(http: aiohttp.ClientSession, update: dict) -> None:
    """Processes a single incoming Telegram update under a concurrency lock."""
    message = update.get("message")
    if not message or not message.get("text"):
        return

    chat      = message["chat"]
    from_user = message["from"]
    chat_id   = int(chat["id"])
    user_id   = str(from_user["id"])
    text      = message["text"]
    chat_type = chat["type"]

    # Redirect private messages to preserve the public tavern structure
    if chat_type == "private":
        await _send_message(http, chat_id, _PRIVATE_REDIRECT)
        return

    # Use semantic router instead of simple @mention detection
    bot_name = _resolve_intent(text)
    if not bot_name:
        return

    lock = _locks[bot_name]
    TIMEOUT_CODA = 15.0
    lock_acquired = False

    # Attempt to acquire lock within timeout to handle concurrent message spikes safely
    try:
        await asyncio.wait_for(lock.acquire(), timeout=TIMEOUT_CODA)
        lock_acquired = True
    except asyncio.TimeoutError:
        await _send_message(http, chat_id, _BOT_BUSY[bot_name])
        return

    try:
        await _send_typing(http, chat_id)
        session_id = str(chat_id)

        # Track message cadence per session to trigger the Narrator every 3rd message
        _message_counters[session_id] = _message_counters.get(session_id, 0) + 1
        augmented = _augment_text(text, bot_name)

        if _message_counters[session_id] % 3 == 0:
            _message_counters[session_id] = 0
            augmented += (
                "\n\n[NOTA DI SISTEMA: È il momento del Narratore. Alla fine assoluta della tua risposta, "
                "DEVI aggiungere una riga vuota e poi una singola descrizione d'ambiente in corsivo, "
                "racchiusa ESATTAMENTE tra due trattini bassi, seguendo le regole del file scummbar.md.]"
            )

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

        # Barnacle answers ephemerally (visible only to target), Barnaby answers publicly
        if bot_name == "barnacle":
            sent = await _send_message(http, chat_id, formatted, receiver_user_id=int(user_id))
            if not sent:
                fallback = formatted + "\n\n<i>🐱 (whisper — just for you)</i>"
                await _send_message(http, chat_id, fallback)
        else:
            await _send_message(http, chat_id, formatted)

    finally:
        # Guarantee lock release even if generation or communication fails, only if acquired
        if lock_acquired:
            lock.release()

async def _session_cleaner_cron() -> None:
    """Background loop that executes the database pruning every hour."""
    while True:
        try:
            await purge_old_sessions(hours=24)
        except Exception as e:
            log.error("Error in session cleaner background task: %s", e)
        await asyncio.sleep(3600)

async def run_polling() -> None:
    """Start the Telegram long-polling loop. Blocks until interrupted."""
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN not configured in .env")

    offset = 0
    pending: set[asyncio.Task] = set()

    log.info("🍺 Scummbar Telegram bot started (long polling)")

    # Fire and forget the background pruning cron task
    asyncio.create_task(_session_cleaner_cron())

    async with aiohttp.ClientSession() as http:
        while True:
            try:
                url = (
                    f"{BASE}/getUpdates"
                    f"?offset={offset}&timeout=30"
                    f'&allowed_updates=["message"]'
                )
                async with http.get(url, timeout=aiohttp.ClientTimeout(total=40)) as resp:
                    data = await resp.json()

                for upd in data.get("result", []):
                    offset = upd["update_id"] + 1
                    task = asyncio.create_task(_handle_update(http, upd))
                    pending.add(task)
                    # Clean up completed tasks from the tracking set
                    task.add_done_callback(pending.discard)

            except asyncio.CancelledError:
                log.info("Polling stopped.")
                break
            except Exception as e:
                log.error("Polling error: %s", e)
                await asyncio.sleep(5)

        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
