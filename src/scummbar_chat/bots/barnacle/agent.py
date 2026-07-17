"""Barnacle — agente del gatto dello Scummbar."""

import pathlib

from google.adk.agents import Agent

from ...utils import MODEL, THINKING_CONFIG, load_md

_PERSONA = load_md(pathlib.Path(__file__).parent / "persona.md")

barnacle_agent = Agent(
    name="barnacle",
    model=MODEL,
    description="Barnacle, il gatto dello Scummbar. Vive nel bar e osserva tutto.",
    instruction=_PERSONA,
    generate_content_config=THINKING_CONFIG,
)
