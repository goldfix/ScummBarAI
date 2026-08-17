#!/usr/bin/env python3
"""Start the Scummbar Telegram bot.

Usage:
    source py-env/bin/activate
    python telegram_bot.py           # INFO level
    python telegram_bot.py --debug   # DEBUG level (very verbose)
"""

import argparse
import asyncio
import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths & Telemetry
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR / "src"))

from scummbar_chat.telemetry import APP_LOG_FILE, DEFAULT_LOG_DIR, ERRORS_LOG_FILE, setup_logging  # noqa: E402  (needs sys.path above)

LOG_DIR = DEFAULT_LOG_DIR
LOG_FILE = APP_LOG_FILE
ERR_FILE = ERRORS_LOG_FILE


# ---------------------------------------------------------------------------
# Crash dump helper
# ---------------------------------------------------------------------------


def _dump_exception(exc: BaseException) -> None:
    """Append a full traceback to errors.log with a timestamp header."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with ERR_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n{'=' * 60}\n")
        f.write(f"CRASH @ {datetime.now().isoformat()}\n")
        f.write(f"{'=' * 60}\n")
        traceback.print_exc(file=f)
        f.write("\n")


# ---------------------------------------------------------------------------
# Startup checks
# ---------------------------------------------------------------------------


def _check_env() -> bool:
    """Verify critical environment variables are set before starting the bot."""
    import os

    from dotenv import load_dotenv

    load_dotenv(ROOT_DIR / "src" / "scummbar_chat" / ".env")

    log = logging.getLogger("startup")
    ok = True

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token or token == "il-tuo-token-qui":
        log.error("❌  TELEGRAM_BOT_TOKEN not set in .env")
        ok = False

    username = os.getenv("TELEGRAM_BOT_USERNAME", "")
    if not username:
        log.warning("⚠️   TELEGRAM_BOT_USERNAME not set — some features may misbehave")

    model = os.getenv("LLM_MODEL", "gemini-3.5-flash")
    compaction_model = os.getenv("COMPACTION_MODEL", "gemini-3.5-flash")

    # Verifica Credenziali se si usano modelli Gemini per Dialogo/Compattazione
    uses_gemini = (not model.startswith("deepseek/")) or (not compaction_model.startswith("deepseek/"))
    if uses_gemini:
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if api_key:
            log.info("🔑  Google API Key rilevata per Chat/Compattazione. Utilizzo diretto di Google AI Studio.")
        else:
            sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
            if sa_path:
                sa_file = Path(sa_path)
                if not sa_file.is_absolute():
                    # Se relativo, risolviamo rispetto alla root del progetto
                    sa_file = (ROOT_DIR / sa_path).resolve()

                if not sa_file.exists():
                    log.error("❌  GOOGLE_APPLICATION_CREDENTIALS è impostato ma il file JSON non esiste: %s", sa_path)
                    ok = False
                else:
                    log.info("🔑  Google Service Account rilevato e valido per Chat/Compattazione: %s", sa_file)
            else:
                log.info(
                    "ℹ️   Nessuna API Key o Service Account espliciti per Chat/Compattazione. Verranno utilizzate le Application Default Credentials (ADC)."
                )

    # Verifica Credenziali Indipendenti per Modello Immagini
    image_model = os.getenv("IMAGE_MODEL", "")
    if image_model and (not image_model.startswith("deepseek/")):
        img_api_key = os.getenv("IMAGE_GEMINI_API_KEY") or os.getenv("IMAGE_GOOGLE_API_KEY")
        if img_api_key:
            log.info("🖼️   Google API Key indipendente rilevata per la generazione immagini. Utilizzo diretto di Google AI Studio.")
        else:
            img_sa_path = os.getenv("IMAGE_GOOGLE_APPLICATION_CREDENTIALS", "")
            if img_sa_path:
                img_sa_file = Path(img_sa_path)
                if not img_sa_file.is_absolute():
                    img_sa_file = (ROOT_DIR / img_sa_path).resolve()

                if not img_sa_file.exists():
                    log.error(
                        "❌  IMAGE_GOOGLE_APPLICATION_CREDENTIALS è impostato ma il file JSON non esiste: %s",
                        img_sa_path,
                    )
                    ok = False
                else:
                    log.info(
                        "🖼️   Google Service Account indipendente rilevato e valido per la generazione immagini: %s",
                        img_sa_file,
                    )
            else:
                log.info(
                    "ℹ️   Nessuna API Key o Service Account espliciti per la generazione immagini. Verranno utilizzate le Application Default Credentials (ADC) o l'ambiente globale."
                )

    log.info("🤖  LLM_MODEL        = %s", model)
    log.info("🧠  COMPACTION_MODEL = %s", compaction_model)
    log.info("📦  SESSION_DB       = data/scummbar_chat/sessions.db")
    log.info("📋  LOG_FILE         = %s", LOG_FILE)
    log.info("🚨  ERROR_FILE       = %s", ERR_FILE)

    return ok


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Scummbar Telegram Bot")
    parser.add_argument("--debug", action="store_true", help="Enable DEBUG log level (very verbose)")
    args = parser.parse_args()

    setup_logging(debug=args.debug)
    log = logging.getLogger("main")

    log.info("🍺  Scummbar — starting up (debug=%s)", args.debug)

    # Pre-flight checks
    if not _check_env():
        log.error("Startup aborted: fix the errors above and restart.")
        sys.exit(1)

    # Import here so that import-time errors (model init, ADK, etc.) are caught
    try:
        from scummbar_chat.telegram import run_polling
    except Exception as exc:
        log.exception("Import failed — check dependencies and .env: %s", exc)
        _dump_exception(exc)
        sys.exit(1)

    # Run
    try:
        asyncio.run(run_polling())

    except KeyboardInterrupt:
        log.info("👋  Interrupted by user. Goodbye.")

    except Exception as exc:
        log.exception("💥  Unhandled exception — bot crashed: %s", exc)
        _dump_exception(exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
