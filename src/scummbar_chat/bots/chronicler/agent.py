"""Chronicler — the Scummbar scribe agent dedicated to compiling patron diaries."""

import pathlib

from google.adk.agents import Agent

from ...utils import COMPACTION_LLM, DEFAULT_RETRY_CONFIG, THINKING_CONFIG, load_md

_PERSONA = load_md(pathlib.Path(__file__).parent / "persona.md")

# --- Agent ---
chronicler_agent = Agent(
    name="chronicler",
    model=COMPACTION_LLM,
    description="Il Cronista dello Scummbar. Custode delle memorie e redattore del Diario di Bordo dei pirati.",
    instruction=_PERSONA,
    generate_content_config=THINKING_CONFIG,
    retry_config=DEFAULT_RETRY_CONFIG,
)
