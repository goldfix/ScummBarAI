"""
Module: tools.py
Operations:
- Provides structural SQLite function tools for cross-session narrative memory storage.
- Interacts with the local session database path via absolute filesystem queries.
- Translates ledger retrieval results into structured dictionaries for the LLM runner.
"""

import sqlite3
import logging
from datetime import datetime
from google.adk.tools import FunctionTool
from .utils import SESSION_DB_URI

log = logging.getLogger(__name__)

async def recall_patron_memory(user_id: str) -> dict:
    """
    Recupera la memoria narrativa di uno specifico avventore della taverna Scummbar.
    Usa questo strumento IMMEDIATAMENTE non appena un cliente ti rivolge la parola o entra in una conversazione, in modo da poterlo salutare adeguatamente.
    Se il dizionario restituito contiene il campo 'last_chat_summary', sei OBBLIGATO a usarlo per riallacciarti in modo naturale e coerente all'ultima discussione avvenuta.
    """
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
    user_id: str,
    patron_name: str,
    new_traits_learned: str,
    chat_summary: str
) -> str:
    """
    Aggiorna o crea la memoria a lungo termine di un avventore nel registro dello Scummbar.
    Esegui questo strumento solo quando una conversazione giunge a una conclusione naturale o se l'avventore rivela dettagli biografici determinanti.

    REGOLE TASSATIVE DI COMPILAZIONE DEL PROMPT:
    - new_traits_learned: Inserisci solo caratteristiche permanenti stabili o oggetti di inventario (es. 'Teme i fantasmi', 'Ha una gamba di legno'). Sii schematico (massimo 10 tratti in totale per utente). Se non ci sono novità, lascia questa stringa vuota.
    - chat_summary: Un riassunto telegrafico dei fatti cruciali emersi nell'incontro attuale. MASSIMO 300 caratteri. Questo testo sovrascriverà interamente il riassunto precedente.
    """
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

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

# Wrapped ADK primitives exported for agent binding
recall_patron_tool = FunctionTool(recall_patron_memory)
memorize_patron_tool = FunctionTool(memorize_patron_chat)
