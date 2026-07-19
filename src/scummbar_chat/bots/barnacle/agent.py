"""Barnacle — Scummbar cat agent."""

import pathlib

from google.adk.agents import Agent
from google.adk.tools import skill_toolset

from ...utils import MODEL, THINKING_CONFIG, load_all_skills, load_md
# Il gatto ha bisogno SOLO dello strumento di lettura (olfatto)
from ...tools import recall_patron_tool

_PERSONA = load_md(pathlib.Path(__file__).parent / "persona.md")

# --- Skills (auto-discovery) ---
# Every folder in skills/ with an SKILL.md is auto-loaded.
_SKILLS_DIR = pathlib.Path(__file__).parent.parent.parent / "skills"

_barnacle_toolset = skill_toolset.SkillToolset(
    skills=load_all_skills(_SKILLS_DIR),
)

# --- Agent ---
barnacle_agent = Agent(
    name="barnacle",
    model=MODEL,
    description="Barnacle, il gatto dello Scummbar. Vive nel bar, osserva tutto e ricorda gli odori dei clienti.",
    instruction=_PERSONA,
    generate_content_config=THINKING_CONFIG,
    # Barnacle è "read-only": usa il recall tool ma non può memorizzare/scrivere
    tools=[_barnacle_toolset, recall_patron_tool],
)
