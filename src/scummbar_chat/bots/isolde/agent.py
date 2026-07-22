"""Isolde — Scummbar mysterious regular / gambler agent."""

import pathlib

from google.adk.agents import Agent

from ...utils import MODEL, THINKING_CONFIG, load_md
from ...tools import recall_patron_tool, draw_tarot_card_tool

_PERSONA = load_md(pathlib.Path(__file__).parent / "persona.md")

# --- Agent ---
isolde_agent = Agent(
    name="isolde",
    model=MODEL,
    description="Isolde, avventrice misteriosa e giocatrice di carte che siede nell'angolo oscuro dello Scummbar.",
    instruction=_PERSONA,
    generate_content_config=THINKING_CONFIG,
    # Isolde usa la memoria e lo strumento di estrazione dei tarocchi
    tools=[recall_patron_tool, draw_tarot_card_tool],
)
