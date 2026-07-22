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
from .utils import SESSION_DB_URI, IMAGE_MODEL, IMAGE_LOCATION

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

def _draw_tarot_card_fallback(card_name: str, description: str) -> bytes:
    """Generates a stylized in-character tarot card PNG using PIL."""
    from PIL import Image, ImageDraw, ImageFont
    import io
    import math
    
    width, height = 400, 600
    img = Image.new("RGB", (width, height), color="#161412")
    draw = ImageDraw.Draw(img)
    
    # Outer Border: golden line
    draw.rectangle([(10, 10), (width - 10, height - 10)], outline="#c5a059", width=2)
    # Inner Border: thin gold line
    draw.rectangle([(18, 18), (width - 18, height - 18)], outline="#c5a059", width=1)
    
    # Draw a mystical glyph/star in the center
    cx, cy = width // 2, height // 2 - 20
    r = 80
    for i in range(8):
        angle_rad = i * (math.pi / 4)
        x1 = cx + int(r * math.cos(angle_rad))
        y1 = cy + int(r * math.sin(angle_rad))
        x2 = cx - int(r * math.cos(angle_rad))
        y2 = cy - int(r * math.sin(angle_rad))
        draw.line([(x1, y1), (x2, y2)], fill="#c5a059", width=1)
    
    draw.ellipse([(cx - r // 2, cy - r // 2), (cx + r // 2, cy + r // 2)], outline="#c5a059", width=2)
    draw.ellipse([(cx - 10, cy - 10), (cx + 10, cy + 10)], fill="#c5a059")
    
    font = ImageFont.load_default()
    title_text = card_name.strip().upper()
    
    # Gold banner rectangle at the bottom
    draw.rectangle([(30, height - 100), (width - 30, height - 40)], outline="#c5a059", width=2, fill="#1e1b18")
    
    # Centered text using default font
    tx = width // 2
    ty = height - 75
    draw.text((tx - len(title_text)*3, ty), title_text, fill="#c5a059", font=font)
    
    sub_text = "TAROCCO DELLO SCUMMBAR"
    draw.text((tx - len(sub_text)*3, height - 30), sub_text, fill="#7d6c54", font=font)
    
    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()

async def cast_vision(
    tool_context: ToolContext,
    title: str,
    description: str,
) -> str:
    """
    Usa questo strumento per proiettare una visione mistica ed evocarne l'immagine per l'avventore.
    - title: Il titolo o nome della visione (es. 'La Torre', 'Il Naufragio').
    - description: Dettagliata descrizione visiva di ciò che appare nella visione (es. 'un pirata sotto la pioggia che guarda una mappa').
    """
    from google import genai
    import os
    
    log.info("Isolde casts vision: %s (%s)", title, description)
    
    img_bytes = None
    
    try:
        use_vertex = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False") == "True"
        project = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        if use_vertex:
            client = genai.Client(
                vertexai=True,
                project=project,
                location=IMAGE_LOCATION
            )
        else:
            client = genai.Client()
            
        result = client.models.generate_images(
            model=IMAGE_MODEL,
            prompt=f"A vintage mystical tarot card showing {description}, hand-drawn 2d pirate cartoon style, gold borders, dark paper texture",
            config=dict(
                number_of_images=1,
                output_mime_type="image/png",
                aspect_ratio="1:1"
            )
        )
        if result and result.generated_images:
            img_bytes = result.generated_images[0].image.image_bytes
            log.info("Tarot card image generated successfully via AI model.")
    except Exception as e:
        log.warning("AI Image generation failed (falling back to PIL drawing): %s", e)
        
    if not img_bytes:
        img_bytes = _draw_tarot_card_fallback(title, description)
        
    artifact_part = types.Part.from_bytes(
        data=img_bytes,
        mime_type="image/png"
    )
    
    safe_title = "".join(c if c.isalnum() else "_" for c in title.strip().lower())
    filename = f"vision_{safe_title}.png"
    
    try:
        version = await tool_context.save_artifact(
            filename=filename,
            artifact=artifact_part
        )
        return (
            f"La visione '{title}' è stata proiettata con successo! "
            f"L'immagine è stata disegnata nelle nebbie e consegnata (Salvata come {filename}, v{version})."
        )
    except Exception as e:
        log.error("Errore salvataggio artifact in cast_vision: %s", e)
        return f"Ho visto la visione '{title}', ma le candele si sono spente e non sono riuscita a mostrarti la figura!"

# Wrapped ADK primitives exported for agent binding
recall_patron_tool = FunctionTool(recall_patron_memory)
memorize_patron_tool = FunctionTool(memorize_patron_chat)
write_secret_scroll_tool = FunctionTool(write_secret_scroll)
cast_vision_tool = FunctionTool(cast_vision)
