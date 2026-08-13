"""
Module: tools.py
Operations:
- Provides structural SQLite function tools for cross-session narrative memory storage.
- Interacts with the local session database path via absolute filesystem queries.
- Translates ledger retrieval results into structured dictionaries for the LLM runner.
"""

import json
import logging
import os
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import google.genai.types as types
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext

from .utils import SESSION_DB_URI, get_gemini_client_kwargs

log = logging.getLogger(__name__)


def _ensure_patron_memories_table() -> None:
    """Create the patron_memories table if it does not exist yet and enable WAL mode for concurrent processes."""
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path, timeout=10.0) as conn:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=10000;")
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
        with sqlite3.connect(db_path, timeout=10.0) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT patron_name, core_traits, last_chat_summary FROM patron_memories WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)

            # Contextual prompt inject for new pirates
            return {
                "status": "unknown_patron",
                "message": "Questo pirata è uno sconosciuto. Chiedigli cordialmente il suo nome!",
            }
    except sqlite3.Error as e:
        log.error("Database error in recall_patron_memory: %s", e)
        return {"status": "error", "message": "I tuoi ricordi sono confusi al momento. Saluta normalmente."}


async def memorize_patron_chat(tool_context: ToolContext, patron_name: str, new_traits_learned: str, chat_summary: str) -> str:
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
    now_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")

    try:
        with sqlite3.connect(db_path, timeout=10.0) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT core_traits FROM patron_memories WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()

            if row:
                current_traits = row[0] or ""
                # Accumulate traits split by a standard structural pipe character
                updated_traits = current_traits
                if new_traits_learned:
                    updated_traits = f"{current_traits} | {new_traits_learned}".strip().strip("|").strip()

                cursor.execute(
                    """
                    UPDATE patron_memories
                    SET patron_name = ?, core_traits = ?, last_chat_summary = ?, last_interaction = ?
                    WHERE user_id = ?
                    """,
                    (patron_name, updated_traits, chat_summary, now_str, user_id),
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO patron_memories (user_id, patron_name, core_traits, last_chat_summary, last_interaction)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (user_id, patron_name, new_traits_learned, chat_summary, now_str),
                )
            conn.commit()
            return "Registro della taverna aggiornato con successo."
    except sqlite3.Error as e:
        log.error("Database error in memorize_patron_chat: %s", e)
        return "L'inchiostro si è rovesciato! Impossibile aggiornare il registro."


async def update_tavern_diary_tool(tool_context: ToolContext, patron_name: str = "") -> str:
    """
    Usa questo strumento per aggiornare o compilare il Diario di Bordo dell'avventore attuale.
    - patron_name: Il nome del pirata di cui stai aggiornando il diario.
    """
    from src.scummbar_chat.diary import update_tavern_diary_async

    # Retrieve patron name from DB if not passed
    user_id = tool_context.user_id
    if not patron_name:
        _ensure_patron_memories_table()
        db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
        try:
            with sqlite3.connect(db_path, timeout=10.0) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT patron_name FROM patron_memories WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                if row and row[0]:
                    patron_name = row[0]
        except sqlite3.Error:
            pass

    if not patron_name:
        patron_name = f"Avventore_{user_id}"

    # Load the current session events from DB using the real session_id (works in both
    # Streamlit and Telegram contexts) and filtered by user_id to avoid mixing other patrons.
    session_id = tool_context.session.id
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
    messages: list[dict] = []
    try:
        with sqlite3.connect(db_path, timeout=10.0) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT event_data FROM events WHERE user_id = ? AND session_id = ? ORDER BY id ASC",
                (user_id, session_id),
            )
            for row in cursor.fetchall():
                try:
                    ev = json.loads(row[0])
                    content = ev.get("content", {})
                    role = content.get("role", "")
                    parts = content.get("parts", [])
                    # Only keep plain text parts, skipping internal thought/reasoning parts
                    text_parts = [p.get("text", "") for p in parts if "text" in p and not p.get("thought", False)]
                    full_text = "\n".join(text_parts).strip()
                    if full_text and role in ["user", "model", "assistant"]:
                        norm_role = "user" if role == "user" else "assistant"
                        messages.append(
                            {
                                "role": norm_role,
                                "content": full_text,
                                "bot_name": "barnaby" if norm_role == "assistant" else None,
                            }
                        )
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
    except sqlite3.Error as e:
        log.warning("Impossibile recuperare gli eventi per il diario via tool: %s", e)

    success, status_msg, _ = await update_tavern_diary_async(patron_name, messages)
    if success:
        return f"📜 Diario di bordo aggiornato con successo per {patron_name}! ({status_msg})"
    else:
        return f"📜 Il diario di bordo di {patron_name} è già aggiornato. ({status_msg})"


async def write_secret_scroll(tool_context: ToolContext, title: str, content: str) -> str:
    """
    Usa questo strumento per scrivere fisicamente una pergamena, una ricetta segreta o una
    mappa del tesoro da consegnare a mano al pirata. Genererà un file reale scaricabile in chat.
    - title: Il titolo del documento (es. 'Ricetta Grog Ombra').
    - content: Il testo completo che vuoi scrivere sulla pergamena. Sii creativo e descrittivo.
    """
    file_bytes = content.encode("utf-8")

    artifact_part = types.Part.from_bytes(data=file_bytes, mime_type="text/plain")

    # Sanitize the title to make it a valid filename
    safe_title = "".join(c if c.isalnum() else "_" for c in title.strip().lower())
    filename = f"{safe_title}.txt"

    try:
        # InMemoryArtifactService handles storage under the session/user namespace
        version = await tool_context.save_artifact(filename=filename, artifact=artifact_part)
        return f"Pergamena {filename} (versione {version}) scritta e arrotolata con successo! Il cliente la riceverà a breve."
    except Exception as e:
        log.error("Errore salvataggio artifact in write_secret_scroll: %s", e)
        return "La penna si è rotta e l'inchiostro si è sparso! Non sono riuscito a scrivere la pergamena."


def _draw_tarot_card_fallback(card_name: str, description: str) -> bytes:
    """Generates a stylized in-character tarot card PNG using PIL."""
    import io
    import math

    from PIL import Image, ImageDraw, ImageFont

    width, height = 400, 600
    img = Image.new("RGB", (width, height), color="#161412")
    draw = ImageDraw.Draw(img)

    # Bordo esterno dorato a doppia linea
    draw.rectangle([(10, 10), (width - 10, height - 10)], outline="#c5a059", width=2)
    draw.rectangle([(18, 18), (width - 18, height - 18)], outline="#c5a059", width=1)

    # Decorazioni agli angoli: piccole stelle dorate (*)
    font = ImageFont.load_default()
    for sx, sy in [(25, 25), (width - 35, 25), (25, height - 35), (width - 35, height - 35)]:
        draw.text((sx, sy), "*", fill="#c5a059", font=font)

    # Glifo mistico al centro
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

    # Onde marittime stilizzate all'interno del glifo centrale
    draw.arc([(cx - r // 3, cy + r // 8), (cx, cy + r // 2)], start=0, end=180, fill="#7d6c54", width=1)
    draw.arc([(cx, cy + r // 8), (cx + r // 3, cy + r // 2)], start=0, end=180, fill="#7d6c54", width=1)

    # Luna crescente stilizzata in alto a sinistra del glifo
    draw.arc([(cx - r // 2, cy - r // 2), (cx - r // 4, cy - r // 4)], start=90, end=270, fill="#c5a059", width=1)

    draw.ellipse([(cx - 10, cy - 10), (cx + 10, cy + 10)], fill="#c5a059")

    title_text = card_name.strip().upper()

    # Title banner rectangle at the bottom
    draw.rectangle([(30, height - 100), (width - 30, height - 40)], outline="#c5a059", width=2, fill="#1e1b18")

    # Testo centrato
    tx = width // 2
    ty = height - 75
    draw.text((tx - len(title_text) * 3, ty), title_text, fill="#c5a059", font=font)

    sub_text = "TAROCCO DELLO SCUMMBAR"
    draw.text((tx - len(sub_text) * 3, height - 30), sub_text, fill="#7d6c54", font=font)

    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


async def draw_tarot_card(
    tool_context: ToolContext,
    card_name: str,
    scene_description: str,
) -> str:
    """
    Usa questo strumento ESCLUSIVAMENTE per estrarre una carta dei Tarocchi dal tuo mazzo e svelarne l'immagine all'avventore.
    - card_name: Il titolo o nome dell'arcano (es. 'Il Leviatano', 'La Taverna', 'Il Naufragio').
    - scene_description: Dettagliata descrizione visiva e marinaresca di ciò che appare nell'illustrazione della carta.
    """

    from google import genai

    # Retrieve the configured image model
    image_model = os.getenv("IMAGE_MODEL", "gemini-3.1-flash-lite-image")

    log.info("Isolde draws tarot card: %s (%s)", card_name, scene_description)

    img_bytes = None

    try:
        # Initialize the standard Google GenAI Client with independent image credentials
        client = genai.Client(**get_gemini_client_kwargs(prefix="IMAGE_"))

        tarot_prompt = (
            f"A vintage mystical tarot card showing {scene_description}. "
            f"Card title at the bottom: {card_name}. "
            "Hand-drawn 2d pirate cartoon style, esoteric gold borders, dark parchment paper texture."
        )

        # Use the modern Gemini 3.1 Flash Image API to generate native images
        response = client.models.generate_content(
            model=image_model,
            contents=tarot_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    image_size="1K",
                ),
            ),
        )
        # Extract raw image bytes from the response parts
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                img_bytes = part.inline_data.data
                log.info("Tarot card generated successfully via Gemini multimodal generate_content.")
                break

    except Exception as e:
        log.warning("Errore generazione immagine AI: %s. Attivazione fallback PIL.", e)
        img_bytes = _draw_tarot_card_fallback(card_name, scene_description)

    # 2. Register the image as an Artifact in ADK
    # Dynamically detect if the bytes represent PNG or JPEG to apply the correct extension and mime type
    if img_bytes.startswith(b"\x89PNG"):
        file_ext = "png"
        mime_type = "image/png"
    elif img_bytes.startswith(b"\xff\xd8"):
        file_ext = "jpg"
        mime_type = "image/jpeg"
    else:
        file_ext = "png"
        mime_type = "image/png"

    artifact_part = types.Part.from_bytes(data=img_bytes, mime_type=mime_type)

    safe_title = "".join(c if c.isalnum() else "_" for c in card_name.strip().lower())
    filename = f"tarocco_{safe_title}.{file_ext}"

    # Save the artifact to the current ADK session
    version = await tool_context.save_artifact(filename=filename, artifact=artifact_part)

    return f"La carta '{card_name}' è stata svelata sul tavolo! L'immagine è ora visibile all'avventore (Salvata come {filename}, v{version})."


async def fetch_news_feed(tool_context: ToolContext, category: str = "politica_italiana") -> dict:
    """
    Recupera gli ultimi dispacci e notizie reali focalizzati esclusivamente su 3 argomenti:
    - Politica Italiana ('politica_italiana', 'politica', 'italia', 'governo')
    - Politica Americana ed Estera ('politica_americana', 'usa', 'america', 'esteri', 'mondo')
    - Tecnologia ed Alchimie Moderne ('tecnologia', 'tech', 'alchimia', 'scienza', 'gadget')

    Usa questo strumento quando un avventore ti chiede notizie sui bisticci dei governanti,
    sulle dispute dei consigli italiani o americani, o sulle invenzioni e specchi incantati della tecnologia.
    """
    import xml.etree.ElementTree as ET

    import httpx

    rss_feeds = {
        "politica_italiana": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "politica": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "italia": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "governo": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "politica_americana": "https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
        "usa": "https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
        "america": "https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
        "esteri": "https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
        "mondo": "https://www.ansa.it/sito/notizie/mondo/mondo_rss.xml",
        "tecnologia": "https://www.ansa.it/sito/notizie/tecnologia/tecnologia_rss.xml",
        "tech": "https://www.ansa.it/sito/notizie/tecnologia/tecnologia_rss.xml",
        "alchimia": "https://www.ansa.it/sito/notizie/tecnologia/tecnologia_rss.xml",
        "scienza": "https://www.ansa.it/sito/notizie/tecnologia/tecnologia_rss.xml",
        "gadget": "https://www.hdblog.it/feed/",
    }

    cat_key = category.lower().strip()
    url = rss_feeds.get(cat_key, "https://www.ansa.it/sito/notizie/politica/politica_rss.xml")
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()

            root = ET.fromstring(resp.content)
            items = root.findall(".//item")
            if not items:
                items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

            items = items[:5]

            headlines = []
            for item in items:
                title_elem = item.find("title")
                desc_elem = item.find("description")
                date_elem = item.find("pubDate")
                link_elem = item.find("link")
                guid_elem = item.find("guid")

                title = title_elem.text.strip() if title_elem is not None and title_elem.text else "Senza titolo"
                desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                date = date_elem.text.strip() if date_elem is not None and date_elem.text else ""

                link = ""
                if link_elem is not None and link_elem.text:
                    link = link_elem.text.strip()
                elif guid_elem is not None and guid_elem.text and guid_elem.text.startswith("http"):
                    link = guid_elem.text.strip()

                headlines.append({"titolo_originale": title, "sintesi_originale": desc, "ora_dispaccio": date, "link_sorgente": link})

            return {
                "status": "success",
                "categoria_richiesta": cat_key,
                "numero_dispacci": len(headlines),
                "dispacci": headlines,
                "istruzione_traduzione": (
                    "Riferisci queste notizie all'avventore con drammatica, pomposa e ridicola solennità teatrale! "
                    "Trasponi i bisticci politici italiani/americani o i fatti tecnologici nella tua ambientazione "
                    "fantasy-marittima (es: 'Il Senato dei Senatori Borbottanti', 'La Gilda della Mela d'Oro', "
                    "'Il Gran Mogol d'Oltreoceano'). "
                    "Includi SEMPRE per ogni notizia il link HTML originale fornito da 'link_sorgente' "
                    "(es. '<a href=\"LINK\">Srotola il pergamena originale</a>')."
                ),
            }

    except Exception as e:
        log.error("Errore nel recupero feed RSS (%s): %s", url, e)
        return {
            "status": "error",
            "message": "I venti si sono placati e le gagliotte delle staffette non sono giunte al porto. Nessun dispaccio disponibile al momento.",
        }


# Esportazione degli strumenti ADK
recall_patron_tool = FunctionTool(recall_patron_memory)
memorize_patron_tool = FunctionTool(memorize_patron_chat)
update_tavern_diary_tool = FunctionTool(update_tavern_diary_tool)
write_secret_scroll_tool = FunctionTool(write_secret_scroll)
draw_tarot_card_tool = FunctionTool(draw_tarot_card)
fetch_news_feed_tool = FunctionTool(fetch_news_feed)
