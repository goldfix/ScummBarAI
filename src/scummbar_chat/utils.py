"""scummbar_chat — utilities condivise

Caricamento configurazione e file markdown dei prompt.
Supporta sia Gemini (Vertex AI) che DeepSeek (via LiteLlm).
"""

import os
import pathlib

from dotenv import load_dotenv
from google.genai import types

# --- Carica .env ---
_ENV_PATH = pathlib.Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)

# --- Configurazione modello ---
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-3.5-flash")
LLM_THINKING_LEVEL: str = os.getenv("LLM_THINKING_LEVEL", "medium")
DEEPSEEK_REASONING_EFFORT: str = os.getenv("DEEPSEEK_REASONING_EFFORT", "high")

_is_deepseek = LLM_MODEL.startswith("deepseek/")

if _is_deepseek:
    # DeepSeek via LiteLlm: thinking configurato tramite kwargs nativi
    from google.adk.models import LiteLlm
    MODEL = LiteLlm(
        model=LLM_MODEL,
        thinking={"type": "enabled"},
        reasoning_effort=DEEPSEEK_REASONING_EFFORT,
        drop_params=True,          # ignora parametri non supportati
    )
    THINKING_CONFIG = None   # non usato con DeepSeek
else:
    # Gemini: thinking configurato tramite GenerateContentConfig
    MODEL = LLM_MODEL
    THINKING_CONFIG = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=LLM_THINKING_LEVEL,
            include_thoughts=False,
        ),
    )

# --- Directory di riferimento ---
CHAT_DIR = pathlib.Path(__file__).parent
WORLD_DIR = CHAT_DIR / "world"
BOTS_DIR = CHAT_DIR / "bots"

# --- Session persistence ---
_DB_PATH = CHAT_DIR.parent.parent / "data" / "sessions.db"
SESSION_DB_URI: str = f"sqlite+aiosqlite:///{_DB_PATH}"


def load_md(path: pathlib.Path) -> str:
    """Carica un file markdown e restituisce il testo pulito."""
    if not path.exists():
        raise FileNotFoundError(f"Prompt file non trovato: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_all_skills(skills_dir: pathlib.Path) -> list:
    """Carica dinamicamente tutte le skill trovate in skills_dir.

    Ogni sottocartella contenente un SKILL.md viene caricata come skill.
    Aggiungere una nuova skill = creare una nuova cartella con SKILL.md.
    """
    from google.adk.skills import load_skill_from_dir
    skills = []
    if not skills_dir.exists():
        return skills
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            skills.append(load_skill_from_dir(skill_dir))
    return skills


def build_instruction(*parts: str) -> str:
    """Assembla l'instruction di un agente concatenando le parti."""
    return "\n\n---\n\n".join(p.strip() for p in parts if p.strip())


# --- World context (condiviso da tutti i bot) ---
WORLD_CONTEXT: str = load_md(WORLD_DIR / "scummbar.md")
