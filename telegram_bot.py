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
from logging.handlers import RotatingFileHandler
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).parent
LOG_DIR  = ROOT_DIR / "data" / "logs"
LOG_FILE = LOG_DIR / "bot.log"
ERR_FILE = LOG_DIR / "errors.log"

sys.path.insert(0, str(ROOT_DIR / "src"))


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def _setup_logging(debug: bool = False) -> None:
    """Configure console + rotating file handlers."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    level = logging.DEBUG if debug else logging.INFO
    fmt   = "%(asctime)s [%(levelname)-8s] %(name)s: %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)   # capture everything; handlers filter by level

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(level)
    console.setFormatter(logging.Formatter(fmt, datefmt))
    root.addHandler(console)

    # Rotating file handler — all levels, 5 MB × 3 files
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(fmt, datefmt))
    root.addHandler(file_handler)

    # Dedicated error file handler — WARNING and above only
    err_handler = RotatingFileHandler(
        ERR_FILE, maxBytes=2 * 1024 * 1024, backupCount=2, encoding="utf-8"
    )
    err_handler.setLevel(logging.WARNING)
    err_handler.setFormatter(logging.Formatter(fmt, datefmt))
    root.addHandler(err_handler)


def _dump_exception(exc: BaseException) -> None:
    """Append a full traceback to errors.log with a timestamp header."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with ERR_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n{'='*60}\n")
        f.write(f"CRASH @ {datetime.now().isoformat()}\n")
        f.write(f"{'='*60}\n")
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
    ok  = True

    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    if not token or token == "il-tuo-token-qui":
        log.error("❌  TELEGRAM_BOT_TOKEN not set in .env")
        ok = False

    username = os.getenv("TELEGRAM_BOT_USERNAME", "")
    if not username:
        log.warning("⚠️   TELEGRAM_BOT_USERNAME not set — some features may misbehave")

    model = os.getenv("LLM_MODEL", "gemini-3.5-flash")
    log.info("🤖  LLM_MODEL        = %s", model)
    log.info("🧠  COMPACTION_MODEL = %s", os.getenv("COMPACTION_MODEL", "gemini-3.5-flash"))
    log.info("📦  SESSION_DB       = data/sessions.db")
    log.info("📋  LOG_FILE         = %s", LOG_FILE)
    log.info("🚨  ERROR_FILE       = %s", ERR_FILE)

    return ok


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Scummbar Telegram Bot")
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable DEBUG log level (very verbose)"
    )
    args = parser.parse_args()

    _setup_logging(debug=args.debug)
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
