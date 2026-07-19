"""Barnaby — the Scummbar bartender agent."""

import pathlib

from google.adk.agents import Agent
from google.adk.tools import skill_toolset

from ...utils import MODEL, THINKING_CONFIG, load_all_skills, load_md
# Import the memory tools we created earlier
from ...tools import recall_patron_tool, memorize_patron_tool

_PERSONA = load_md(pathlib.Path(__file__).parent / "persona.md")

# --- Skills (auto-discovery) ---
# Every folder in skills/ with an SKILL.md is auto-loaded.
# Adding a new skill = create a new folder, zero code.
_SKILLS_DIR = pathlib.Path(__file__).parent.parent.parent / "skills"

_barnaby_toolset = skill_toolset.SkillToolset(
    skills=load_all_skills(_SKILLS_DIR),
)

# --- Agent ---
barnaby_agent = Agent(
    name="barnaby",
    model=MODEL,
    description="Barnaby, il barista dello Scummbar. Gestisce il bancone e interagisce con i clienti.",
    instruction=_PERSONA,
    generate_content_config=THINKING_CONFIG,
    # Inject both the dynamic skills and the database memory tools
    tools=[_barnaby_toolset, recall_patron_tool, memorize_patron_tool],
)
