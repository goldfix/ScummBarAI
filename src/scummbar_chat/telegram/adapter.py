"""Telegram Adapter per Scummbar.

Gestisce:
- Long polling (getUpdates)
- Redirect messaggi privati al gruppo
- Rilevamento @barnaby / @barnacle
- Lock per bot (un utente alla volta)
- Risposte pubbliche (Barnaby) e effimere (Barnacle)
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

# --- Lock per bot: un utente alla volta ---
_locks: dict[str, asyncio.Lock] = {
    "barnaby":  asyncio.Lock(),
    "barnacle": asyncio.Lock(),
}

# --- Messaggi in-character ---
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
    """Invia l'indicatore 'sta scrivendo...'"""
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
    """Invia un messaggio HTML. Se receiver_user_id è presente → ephemeral.

    Returns:
        True se inviato con successo, False altrimenti.
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
                log.warning("sendMessage fallito: %s", data.get("description", data))
                return False
            return True
    except Exception as e:
        log.error("Errore sendMessage: %s", e)
        return False


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------

def _detect_bot(text: str) -> str | None:
    """Rileva quale bot è menzionato. Barnacle ha priorità (più raro).

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
    """Aggiunge un routing hint al testo per il coordinatore ADK."""
    label = bot_name.upper()
    return f"[Risponde {label}] {text}"


# ---------------------------------------------------------------------------
# Handler singolo update
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

    # 1. Messaggi privati → redirect in-character
    if chat_type == "private":
        await _send_message(http, chat_id, _PRIVATE_REDIRECT)
        return

    # 2. Solo messaggi con @mention ai bot
    bot_name = _detect_bot(text)
    if not bot_name:
        return  # utenti che si parlano tra loro — noi non interveniamo

    # 3. Lock del bot
    lock = _locks[bot_name]
    if lock.locked():
        await _send_message(http, chat_id, _BOT_BUSY[bot_name])
        return

    # 4. Elaborazione
    async with lock:
        await _send_typing(http, chat_id)

        # session_id condivisa per il gruppo (tutti gli avventori condividono la stessa storia)
        session_id = str(chat_id)

        # Arricchisco il testo con routing hint per il coordinatore
        augmented = _augment_text(text, bot_name)

        response = await run_agent(
            user_id=user_id,
            session_id=session_id,
            text=augmented,
        )

        if not response:
            log.warning("[%s] risposta vuota dall'agente", bot_name)
            return

        log.info("[%s] %s: %s", bot_name, from_user.get('username', user_id), text[:60])

        formatted = format_response(response)

        # Barnacle → prova ephemeral, fallback pubblico se il bot non è admin
        # Barnaby  → sempre pubblico nel gruppo
        if bot_name == "barnacle":
            sent = await _send_message(
                http, chat_id, formatted,
                receiver_user_id=int(user_id),
            )
            if not sent:
                # Fallback: risposta pubblica con nota che è un sussurro
                log.warning(
                    "Ephemeral fallita (bot non admin?). "
                    "Suggerimento: rendi il bot admin del gruppo."
                )
                fallback = formatted + "\n\n<i>🐱 (sussurro — solo per te)</i>"
                await _send_message(http, chat_id, fallback)
        else:
            await _send_message(http, chat_id, formatted)


# ---------------------------------------------------------------------------
# Long polling loop
# ---------------------------------------------------------------------------

async def run_polling() -> None:
    """Avvia il long polling Telegram."""
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN non configurato nel .env")

    offset = 0
    pending: set[asyncio.Task] = set()

    log.info("🍺 Scummbar Telegram bot avviato (long polling)")

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
                log.info("Polling interrotto.")
                break
            except Exception as e:
                log.error("Errore polling: %s", e)
                await asyncio.sleep(5)

        # Attende i task in corso prima di chiudere
        if pending:
            await asyncio.gather(*pending, return_exceptions=True)
