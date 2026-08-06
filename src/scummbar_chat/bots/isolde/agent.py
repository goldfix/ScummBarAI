"""Isolde — Scummbar mysterious regular / gambler agent."""

import pathlib

from google.adk.agents import Agent

from ...tools import draw_tarot_card_tool, recall_patron_tool
from ...utils import DEFAULT_RETRY_CONFIG, MODEL, THINKING_CONFIG, load_md

_PERSONA = load_md(pathlib.Path(__file__).parent / "persona.md")

# --- Agent ---
isolde_agent = Agent(
    name="isolde",
    model=MODEL,
    description="Isolde, avventrice misteriosa e giocatrice di carte che siede nell'angolo oscuro dello Scummbar.",
    instruction=_PERSONA,
    generate_content_config=THINKING_CONFIG,
    retry_config=DEFAULT_RETRY_CONFIG,
    # Isolde usa la memoria e lo strumento di estrazione dei tarocchi
    tools=[recall_patron_tool, draw_tarot_card_tool],
)
