"""scummbar_chat — Root Agent (coordinatore della chat)."""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext

from .bots import barnaby_agent, barnacle_agent
from .time_context import get_time_description
from .utils import MODEL, THINKING_CONFIG, WORLD_CONTEXT

_COORDINATOR_INSTRUCTION = """\
Sei il coordinatore della chat dello Scummbar.
Il tuo compito è delegare la risposta al bot corretto:

- Se il messaggio contiene "[Risponde BARNABY]" → delega SEMPRE a `barnaby`
- Se il messaggio contiene "[Risponde BARNACLE]" → delega SEMPRE a `barnacle`
- In tutti gli altri casi usa il contesto per decidere:
  - `barnaby` per il bancone, bevande, cibo, clienti
  - `barnacle` per il gatto o la sua prospettiva

Non rispondere mai direttamente: delega sempre a uno dei due bot.
"""


def _world_instruction_provider(context: ReadonlyContext) -> str:
    """Assembla il global_instruction con il world context + il momento del giorno."""
    return f"{WORLD_CONTEXT}\n\n{get_time_description()}"


root_agent = Agent(
    name="scummbar_chat",
    model=MODEL,
    description="Coordinatore della chat dello Scummbar.",
    global_instruction=_world_instruction_provider,
    instruction=_COORDINATOR_INSTRUCTION,
    generate_content_config=THINKING_CONFIG,
    sub_agents=[barnaby_agent, barnacle_agent],
)
