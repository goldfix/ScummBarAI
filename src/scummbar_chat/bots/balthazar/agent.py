"""Balthazar — the Scummbar navigator and cartographer agent."""

import pathlib

from google.adk.agents import Agent
from google.adk.tools import skill_toolset
from google.adk.tools.agent_tool import AgentTool

from ...tools import (
    draw_nautical_map_tool,
    fetch_news_feed_tool,
    memorize_patron_tool,
    recall_patron_tool,
    write_secret_scroll_tool,
)
from ...utils import DEFAULT_RETRY_CONFIG, MODEL, THINKING_CONFIG, load_all_skills, load_md

_PERSONA = load_md(pathlib.Path(__file__).parent / "persona.md")

# --- Skills (auto-discovery) ---
_SKILLS_DIR = pathlib.Path(__file__).parent.parent.parent / "skills"

_balthazar_toolset = skill_toolset.SkillToolset(
    skills=load_all_skills(_SKILLS_DIR),
)

# --- Infra-Agent Advisors (Single-Turn ADK Consultants) ---
_barnaby_advisor = Agent(
    name="consult_barnaby",
    model=MODEL,
    instruction=(
        "Sei Barnaby, il barista dello Scummbar. Balthazar ti chiede un consiglio, aneddoto o diceria da taverna "
        "su un'isola, mare o arcipelago per arricchire la sua mappa. "
        "Rispondi in 1-2 frasi sintetiche con il tuo tono empatico e un aneddoto/diceria da pirati."
    ),
    description="Consulta Barnaby il barista per ottenere voci da bancone, covi segreti e dicerie di pirati su un'isola o arcipelago.",
)

_barnacle_advisor = Agent(
    name="consult_barnacle",
    model=MODEL,
    instruction=(
        "Sei Barnacle, il vecchio e burbero gatto dello Scummbar. Balthazar ti chiede un consiglio felino "
        "su un'isola, scogli o pericoli. Rispondi in 1-2 frasi con miagolii, soffi o istinti felini su pesci, topi e scogliere aguzze."
    ),
    description="Consulta Barnacle il gatto per il suo istinto felino, soffi di pericolo, pesci o scogli aguzzi su una rotta.",
)

consult_barnaby_tool = AgentTool(agent=_barnaby_advisor)
consult_barnacle_tool = AgentTool(agent=_barnacle_advisor)

# --- Agent ---
balthazar_agent = Agent(
    name="balthazar",
    model=MODEL,
    description="Balthazar, il navigatore e cartografo dello Scummbar. Traccia rotte, legge le stelle e disegna mappe.",
    instruction=_PERSONA,
    generate_content_config=THINKING_CONFIG,
    retry_config=DEFAULT_RETRY_CONFIG,
    tools=[
        _balthazar_toolset,
        recall_patron_tool,
        memorize_patron_tool,
        write_secret_scroll_tool,
        draw_nautical_map_tool,
        consult_barnaby_tool,
        consult_barnacle_tool,
        fetch_news_feed_tool,
    ],
)
