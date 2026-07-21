"""scummbar_chat — Root Agent (chat coordinator)."""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext

from .bots import barnaby_agent, barnacle_agent, isolde_agent
from .time_context import get_time_description
from .utils import MODEL, THINKING_CONFIG, WORLD_CONTEXT

_COORDINATOR_INSTRUCTION = """\
Sei il coordinatore della chat dello Scummbar.
Il tuo compito è delegare la risposta al bot corretto:

- Se il messaggio contiene "[Risponde BARNABY]" → delega SEMPRE a `barnaby`
- Se il messaggio contiene "[Risponde BARNACLE]" → delega SEMPRE a `barnacle`
- Se il messaggio contiene "[Risponde ISOLDE]" → delega SEMPRE a `isolde`
- In tutti gli altri casi usa il contesto per decidere:
  - `barnaby` per il bancone, bevande, cibo, clienti
  - `barnacle` per il gatto o la sua prospettiva
  - `isolde` per giochi di carte, dadi, segreti, pettegolezzi, tarocchi o l'angolo oscuro

Non rispondere mai direttamente: delega sempre a uno dei due bot.
"""


def _world_instruction_provider(context: ReadonlyContext) -> str:
    """Build the global_instruction with world context + time of day."""
    return f"{WORLD_CONTEXT}\n\n{get_time_description()}"


root_agent = Agent(
    name="scummbar_chat",
    model=MODEL,
    description="Coordinatore della chat dello Scummbar.",
    global_instruction=_world_instruction_provider,
    instruction=_COORDINATOR_INSTRUCTION,
    generate_content_config=THINKING_CONFIG,
    sub_agents=[barnaby_agent, barnacle_agent, isolde_agent],
)
