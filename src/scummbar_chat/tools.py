"""
Module: tools.py
Operations:
- Provides structural SQLite function tools for cross-session narrative memory storage.
- Interacts with the local session database path via absolute filesystem queries.
- Translates ledger retrieval results into structured dictionaries for the LLM runner.
"""

import sqlite3
import logging
import google.genai.types as types
from datetime import datetime, timezone
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from .utils import SESSION_DB_URI

log = logging.getLogger(__name__)


def _ensure_patron_memories_table() -> None:
    """Create the patron_memories table if it does not exist yet."""
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patron_memories (
                user_id           TEXT PRIMARY KEY,
                patron_name       TEXT,
                core_traits       TEXT,
                last_chat_summary TEXT,
                last_interaction  DATETIME
            )
        """)
        conn.commit()


async def recall_patron_memory(tool_context: ToolContext) -> dict:
    """
    Recupera la memoria narrativa di uno specifico avventore della taverna Scummbar.
    Usa questo strumento IMMEDIATAMENTE non appena un cliente ti rivolge la parola,
    in modo da poterlo salutare adeguatamente e con cognizione di causa.
    Se il dizionario restituito contiene il campo 'last_chat_summary', sei OBBLIGATO
    a usarlo per riallacciarti in modo naturale e coerente all'ultima discussione.
    """
    user_id = tool_context.user_id
    _ensure_patron_memories_table()
    # Clean up the DB engine prefix to get a regular sqlite file path
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")

    try:
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                "SELECT patron_name, core_traits, last_chat_summary FROM patron_memories WHERE user_id = ?",
                (user_id,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)

            # Contextual prompt inject for new pirates
            return {"status": "unknown_patron", "message": "Questo pirata è uno sconosciuto. Chiedigli cordialmente il suo nome!"}
    except sqlite3.Error as e:
        log.error("Database error in recall_patron_memory: %s", e)
        return {"status": "error", "message": "I tuoi ricordi sono confusi al momento. Saluta normalmente."}

async def memorize_patron_chat(
    tool_context: ToolContext,
    patron_name: str,
    new_traits_learned: str,
    chat_summary: str
) -> str:
    """
    Aggiorna o crea la memoria a lungo termine di un avventore nel registro dello Scummbar.
    Esegui questo strumento solo quando una conversazione giunge a una conclusione naturale
    o se l'avventore rivela dettagli biografici determinanti.

    REGOLE TASSATIVE:
    - new_traits_learned: solo caratteristiche permanenti stabili (es. 'Teme i fantasmi',
      'Ha una gamba di legno'). Massimo 10 tratti totali per utente. Lascia vuoto se non
      hai appreso nulla di nuovo.
    - chat_summary: riassunto telegrafico dei fatti cruciali dell'incontro attuale.
      MASSIMO 300 caratteri. Sovrascrive interamente il riassunto precedente.
    """
    user_id = tool_context.user_id
    _ensure_patron_memories_table()
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT core_traits FROM patron_memories WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if row:
                current_traits = row[0] or ""
                # Accumulate traits split by a standard structural pipe character
                updated_traits = current_traits
                if new_traits_learned:
                    updated_traits = f"{current_traits} | {new_traits_learned}".strip(" | ")

                cursor.execute(
                    """
                    UPDATE patron_memories
                    SET patron_name = ?, core_traits = ?, last_chat_summary = ?, last_interaction = ?
                    WHERE user_id = ?
                    """,
                    (patron_name, updated_traits, chat_summary, now_str, user_id)
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO patron_memories (user_id, patron_name, core_traits, last_chat_summary, last_interaction)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, patron_name, new_traits_learned, chat_summary, now_str)
                )
            conn.commit()
            return "Registro della taverna aggiornato con successo."
    except sqlite3.Error as e:
        log.error("Database error in memorize_patron_chat: %s", e)
        return "L'inchiostro si è rovesciato! Impossibile aggiornare il registro."

async def write_secret_scroll(
    tool_context: ToolContext,
    title: str,
    content: str
) -> str:
    """
    Usa questo strumento per scrivere fisicamente una pergamena, una ricetta segreta o una
    mappa del tesoro da consegnare a mano al pirata. Genererà un file reale scaricabile in chat.
    - title: Il titolo del documento (es. 'Ricetta Grog Ombra').
    - content: Il testo completo che vuoi scrivere sulla pergamena. Sii creativo e descrittivo.
    """
    file_bytes = content.encode("utf-8")
    
    artifact_part = types.Part.from_bytes(
        data=file_bytes,
        mime_type="text/plain"
    )
    
    # Sanitize the title to make it a valid filename
    safe_title = "".join(c if c.isalnum() else "_" for c in title.strip().lower())
    filename = f"{safe_title}.txt"
    
    try:
        # InMemoryArtifactService handles storage under the session/user namespace
        version = await tool_context.save_artifact(
            filename=filename,
            artifact=artifact_part
        )
        return f"Pergamena {filename} (versione {version}) scritta e arrotolata con successo! Il cliente la riceverà a breve."
    except Exception as e:
        log.error("Errore salvataggio artifact in write_secret_scroll: %s", e)
        return "La penna si è rotta e l'inchiostro si è sparso! Non sono riuscito a scrivere la pergamena."

# Wrapped ADK primitives exported for agent binding
recall_patron_tool = FunctionTool(recall_patron_memory)
memorize_patron_tool = FunctionTool(memorize_patron_chat)
write_secret_scroll_tool = FunctionTool(write_secret_scroll)
