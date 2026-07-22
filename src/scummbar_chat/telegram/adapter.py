"""
Module: adapter.py
Operations:
- Orchestrates the Telegram Bot runtime via long polling (`getUpdates`).
- Implements concurrent request serialization using per-bot asynchronous locks.
- Manages request queueing timeouts (15 seconds) to prevent starvation.
- Routes messages via semantic intent resolution: @ tags first, then keyword matching.
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

# --- Per-bot lock: serializes updates to prevent race conditions in LLM session history ---
_locks: dict[str, asyncio.Lock] = {
    "barnaby":  asyncio.Lock(),
    "barnacle": asyncio.Lock(),
    "isolde":   asyncio.Lock(),
}

# --- Tracks user message counts per chat room to trigger Narrator events ---
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
    "isolde": (
        "<i>Isolde giocherella con le carte senza alzare lo sguardo. "
        "«Il tavolo è pieno, pirata. Aspetta il tuo turno...»</i>"
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
    ],
    "isolde": [
        "isolde", "carte", "giocare", "gioco", "dadi", "tarocchi",
        "barare", "trucco", "scommessa", "predizione", "segreto", "pettegolezzo",
        "maga"
    ]
}

def _resolve_intent(text: str) -> str | None:
    """
    Detect which bot should respond, using @ tags or keyword matching.
    Tags have priority, followed by semantic keyword matching.
    """
    tl = text.lower()

    # 1. Explicit @ tags take priority
    if "@barnacle" in tl: return "barnacle"
    if "@barnaby" in tl: return "barnaby"
    if "@isolde" in tl:  return "isolde"

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

async def _send_document(
    http: aiohttp.ClientSession,
    chat_id: int,
    filename: str,
    file_bytes: bytes,
    receiver_user_id: int | None = None,
) -> bool:
    """
    Upload raw byte artifacts as files directly to Telegram using multipart/form-data.
    Bypasses local disk storage, streaming directly from RAM.
    """
    data = aiohttp.FormData()
    data.add_field("chat_id", str(chat_id))
    data.add_field(
        "document",
        file_bytes,
        filename=filename,
        content_type="text/plain"
    )
    if receiver_user_id:
        data.add_field("receiver_user_id", str(receiver_user_id))

    try:
        async with http.post(f"{BASE}/sendDocument", data=data) as resp:
            resp_data = await resp.json()
            if not resp_data.get("ok"):
                log.warning("sendDocument failed: %s", resp_data.get("description", resp_data))
                return False
            return True
    except Exception as e:
        log.error("Error in sendDocument: %s", e)
        return False

async def _send_photo(
    http: aiohttp.ClientSession,
    chat_id: int,
    filename: str,
    file_bytes: bytes,
    receiver_user_id: int | None = None,
) -> bool:
    """
    Upload raw byte artifacts as photos directly to Telegram using multipart/form-data.
    Renders inline in the chat interface.
    """
    data = aiohttp.FormData()
    data.add_field("chat_id", str(chat_id))
    data.add_field(
        "photo",
        file_bytes,
        filename=filename,
        content_type="image/png"
    )
    if receiver_user_id:
        data.add_field("receiver_user_id", str(receiver_user_id))

    try:
        async with http.post(f"{BASE}/sendPhoto", data=data) as resp:
            resp_data = await resp.json()
            if not resp_data.get("ok"):
                log.warning("sendPhoto failed: %s", resp_data.get("description", resp_data))
                return False
            return True
    except Exception as e:
        log.error("Error in sendPhoto: %s", e)
        return False

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

def _augment_text(text: str, bot_name: str, user_id: str) -> str:
    """Prepends routing hint and patron ID for context. user_id is used by tools via ToolContext."""
    label = bot_name.upper()
    return f"[Risponde {label}] [avventore_id: {user_id}] {text}"

def _on_task_done(task: asyncio.Task) -> None:
    """Callback attached to every update task — logs unhandled exceptions."""
    if task.cancelled():
        return
    exc = task.exception()
    if exc:
        log.exception(
            "Unhandled exception in update task [%s]: %s",
            task.get_name(), exc,
            exc_info=exc,
        )

async def _handle_update(http: aiohttp.ClientSession, update: dict) -> None:
    """Processes a single incoming Telegram update under a concurrency lock."""
    try:
        await _handle_update_inner(http, update)
    except Exception as exc:
        log.exception(
            "Unhandled exception in _handle_update (update_id=%s): %s",
            update.get("update_id"), exc,
        )

async def _handle_update_inner(http: aiohttp.ClientSession, update: dict) -> None:
    """Core update processing logic — called by _handle_update."""
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

    # Use semantic router to match message to a specific bot persona
    bot_name = _resolve_intent(text)
    if not bot_name:
        return

    lock = _locks[bot_name]
    TIMEOUT_CODA = 15.0
    lock_acquired = False

    # Attempt to acquire lock within a 15-second window to prevent Telegram request piling/starvation
    try:
        await asyncio.wait_for(lock.acquire(), timeout=TIMEOUT_CODA)
        lock_acquired = True
    except asyncio.TimeoutError:
        # Notify user that the character is currently busy (lock timeout)
        await _send_message(http, chat_id, _BOT_BUSY[bot_name])
        return

    try:
        await _send_typing(http, chat_id)
        session_id = str(chat_id)

        # Increment message count. On every 3rd message, inject the Narrator prompt.
        _message_counters[session_id] = _message_counters.get(session_id, 0) + 1
        augmented = _augment_text(text, bot_name, user_id)

        if _message_counters[session_id] % 3 == 0:
            _message_counters[session_id] = 0
            augmented += (
                "\n\n[NOTA DI SISTEMA: È il momento del Narratore. Alla fine assoluta della tua risposta, "
                "DEVI aggiungere una riga vuota e poi una singola descrizione d'ambiente in corsivo, "
                "racchiusa ESATTAMENTE tra due trattini bassi, seguendo le regole del file scummbar.md.]"
            )

        response, files = await run_agent(
            user_id=user_id,
            session_id=session_id,
            text=augmented,
        )

        if not response:
            log.warning("[%s] empty response from agent", bot_name)
            return

        log.info("[%s] %s: %s", bot_name, from_user.get('username', user_id), text[:60])
        formatted = format_response(response)

        # Barnacle answers ephemerally (visible only to target), Barnaby/Isolde answer publicly
        if bot_name == "barnacle":
            sent = await _send_message(http, chat_id, formatted, receiver_user_id=int(user_id))
            if not sent:
                fallback = formatted + "\n\n<i>🐱 (whisper — just for you)</i>"
                await _send_message(http, chat_id, fallback)
            for f in files:
                if f["filename"].endswith(".png") or f["filename"].endswith(".jpg"):
                    await _send_photo(http, chat_id, f["filename"], f["bytes"], receiver_user_id=int(user_id))
                else:
                    await _send_document(http, chat_id, f["filename"], f["bytes"], receiver_user_id=int(user_id))
        else:
            await _send_message(http, chat_id, formatted)
            for f in files:
                if f["filename"].endswith(".png") or f["filename"].endswith(".jpg"):
                    await _send_photo(http, chat_id, f["filename"], f["bytes"])
                else:
                    await _send_document(http, chat_id, f["filename"], f["bytes"])

    finally:
        # Guarantee lock release even if generation or communication fails, only if acquired
        if lock_acquired:
            lock.release()

async def _session_cleaner_cron() -> None:
    """Background loop that executes the database pruning every hour."""
    while True:
        try:
            await purge_old_sessions(hours=24)
        except Exception as exc:
            log.exception("Error in session cleaner background task: %s", exc)
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
                    task.add_done_callback(pending.discard)
                    task.add_done_callback(_on_task_done)

            except asyncio.CancelledError:
                log.info("Polling stopped.")
                break
            except Exception as e:
                log.error("Polling error: %s", e)
                await asyncio.sleep(5)

        # Drain pending tasks; log any exceptions that surface
        if pending:
            results = await asyncio.gather(*pending, return_exceptions=True)
            for r in results:
                if isinstance(r, Exception):
                    log.exception("Exception in pending task at shutdown: %s", r, exc_info=r)
