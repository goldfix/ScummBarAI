"""scummbar_chat — shared utilities

Configuration loading and markdown prompt file management.
Supports both Gemini (Vertex AI) and DeepSeek (via LiteLlm).
"""

import os
import pathlib

from dotenv import load_dotenv
from google.genai import types

# --- Load .env ---
_ENV_PATH = pathlib.Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)

# --- Model configuration ---
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-3.5-flash")
LLM_THINKING_LEVEL: str = os.getenv("LLM_THINKING_LEVEL", "medium")
DEEPSEEK_REASONING_EFFORT: str = os.getenv("DEEPSEEK_REASONING_EFFORT", "high")

_is_deepseek = LLM_MODEL.startswith("deepseek/")

if _is_deepseek:
    # DeepSeek via LiteLlm: thinking configured via native kwargs
    from google.adk.models import LiteLlm
    MODEL = LiteLlm(
        model=LLM_MODEL,
        thinking={"type": "enabled"},
        reasoning_effort=DEEPSEEK_REASONING_EFFORT,
        drop_params=True,          # ignore unsupported params
    )
    THINKING_CONFIG = None   # not used with DeepSeek
else:
    # Gemini: thinking configured via GenerateContentConfig
    MODEL = LLM_MODEL
    THINKING_CONFIG = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=LLM_THINKING_LEVEL,
            include_thoughts=False,
        ),
    )

# --- Reference directories ---
CHAT_DIR = pathlib.Path(__file__).parent
WORLD_DIR = CHAT_DIR / "world"
BOTS_DIR = CHAT_DIR / "bots"

# --- Session persistence ---
_DB_PATH = CHAT_DIR.parent.parent / "data" / "sessions.db"
SESSION_DB_URI: str = f"sqlite+aiosqlite:///{_DB_PATH}"


def load_md(path: pathlib.Path) -> str:
    """Load a markdown file and return the cleaned text."""
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_all_skills(skills_dir: pathlib.Path) -> list:
    """Dynamically load all skills found in skills_dir.

    Each subdirectory containing an SKILL.md is loaded as a skill.
    Adding a new skill = create a new folder with SKILL.md.
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
    """Build an agent instruction by concatenating parts."""
    return "\n\n---\n\n".join(p.strip() for p in parts if p.strip())


# --- World context (shared by all bots) ---
WORLD_CONTEXT: str = load_md(WORLD_DIR / "scummbar.md")
