#!/usr/bin/env python3
"""Avvia il bot Telegram dello Scummbar.

Uso:
    source py-env/bin/activate
    python telegram_bot.py
"""

import asyncio
import logging
import sys
from pathlib import Path

# Aggiunge src/ al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

from scummbar_chat.telegram import run_polling  # noqa: E402


if __name__ == "__main__":
    try:
        asyncio.run(run_polling())
    except KeyboardInterrupt:
        print("\n👋 Scummbar chiuso. Alla prossima!")
