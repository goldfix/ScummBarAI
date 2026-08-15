"""Balthazar — the Scummbar navigator and cartographer agent."""

import pathlib

from google.adk.agents import Agent
from google.adk.tools import skill_toolset

from ...tools import (
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
        fetch_news_feed_tool,
    ],
)
