"""scummbar_chat — Root Agent (chat coordinator)."""

from google.adk.agents import Agent
from google.adk.agents.readonly_context import ReadonlyContext

from .bots import balthazar_agent, barnaby_agent, barnacle_agent, isolde_agent
from .time_context import get_time_description
from .utils import DEFAULT_RETRY_CONFIG, MODEL, THINKING_CONFIG, WORLD_CONTEXT

_COORDINATOR_INSTRUCTION = """\
Sei il coordinatore della chat dello Scummbar.
Il tuo compito è delegare la risposta al bot corretto:

- Se il messaggio contiene "[Risponde BARNABY]" → delega SEMPRE a `barnaby`
- Se il messaggio contiene "[Risponde BARNACLE]" → delega SEMPRE a `barnacle`
- Se il messaggio contiene "[Risponde ISOLDE]" → delega SEMPRE a `isolde`
- Se il messaggio contiene "[Risponde BALTHAZAR]" → delega SEMPRE a `balthazar`
- In tutti gli altri casi usa il contesto per decidere:
  - `barnaby` per il bancone, bevande, cibo, clienti
  - `barnacle` per il gatto o la sua prospettiva
  - `isolde` per giochi di carte, dadi, segreti, pettegolezzi, tarocchi o l'angolo oscuro
  - `balthazar` per mappe, rotte, navigazione, ma anche notizie e cronache di politica italiana e politica americana/estera dai regni lontani

Non rispondere mai direttamente: delega sempre a uno dei sub-agenti.
"""


def _time_instruction_provider(context: ReadonlyContext) -> str:
    """Provide dynamic time-of-day context for the global atmosphere."""
    return get_time_description()


root_agent = Agent(
    name="scummbar_chat",
    model=MODEL,
    description="Coordinatore della chat dello Scummbar.",
    static_instruction=WORLD_CONTEXT,
    global_instruction=_time_instruction_provider,
    instruction=_COORDINATOR_INSTRUCTION,
    generate_content_config=THINKING_CONFIG,
    retry_config=DEFAULT_RETRY_CONFIG,
    sub_agents=[barnaby_agent, barnacle_agent, isolde_agent, balthazar_agent],
)
