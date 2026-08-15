"""
Module: tools.py
Operations:
- Provides structural SQLite function tools for cross-session narrative memory storage.
- Interacts with the local session database path via absolute filesystem queries.
- Translates ledger retrieval results into structured dictionaries for the LLM runner.
"""

import logging
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import google.genai.types as types
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext

from .utils import IMAGE_MODEL, IMAGE_THINKING_LEVEL, SESSION_DB_URI, get_gemini_client_kwargs

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
    image_model = IMAGE_MODEL

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

        # Use the modern Gemini 3.1 Flash Image API to generate native images with configured thinking level
        response = client.models.generate_content(
            model=image_model,
            contents=tarot_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="1:1",
                    image_size="1K",
                ),
                thinking_config=types.ThinkingConfig(
                    thinking_level=IMAGE_THINKING_LEVEL,
                    include_thoughts=False,
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


def _draw_nautical_map_fallback(archipelago_name: str, map_details: str = "") -> bytes:
    """Generates a stylized in-character nautical map PNG using PIL (4:3 aspect ratio)."""
    import io
    import math

    from PIL import Image, ImageDraw, ImageFont

    width, height = 800, 600
    img = Image.new("RGB", (width, height), color="#e8dcbf")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    # Vintage parchment double border
    draw.rectangle([(15, 15), (width - 15, height - 15)], outline="#4a3b2c", width=3)
    draw.rectangle([(22, 22), (width - 22, height - 22)], outline="#8a735c", width=1)

    # Decorative corner markers
    for cx, cy in [(30, 30), (width - 30, 30), (25, height - 30), (width - 30, height - 30)]:
        draw.text((cx, cy), "+", fill="#4a3b2c", font=font)

    # Landmasses / Islands (organic shapes)
    islands = [
        [(150, 180), (240, 140), (320, 200), (290, 320), (200, 340), (140, 260)],  # Main island
        [(420, 280), (480, 250), (510, 300), (460, 340)],  # Eastern island
        [(280, 420), (340, 390), (360, 450), (300, 470)],  # Southern isle
        [(520, 160), (560, 140), (580, 180), (540, 200)],  # Northeast atoll
    ]
    for isl in islands:
        draw.polygon(isl, fill="#cfbe9b", outline="#5c4a38")

    # Mountains on main island
    for mx, my in [(200, 220), (230, 200), (260, 240), (220, 270)]:
        draw.polygon([(mx, my - 15), (mx - 12, my + 10), (mx + 12, my + 10)], outline="#4a3b2c", fill="#bda884")

    # Sea Waves (hatching)
    for wx, wy in [(80, 100), (380, 120), (620, 280), (120, 480), (600, 460)]:
        draw.arc([(wx, wy), (wx + 30, wy + 10)], start=0, end=180, fill="#9e8c74", width=1)
        draw.arc([(wx + 25, wy), (wx + 55, wy + 10)], start=0, end=180, fill="#9e8c74", width=1)

    # Compass Rose at bottom-right
    rx, ry, r = 680, 480, 45
    for i in range(8):
        angle_rad = i * (math.pi / 4)
        x1 = rx + int(r * math.cos(angle_rad))
        y1 = ry + int(r * math.sin(angle_rad))
        col = "#8c2d19" if i % 2 == 0 else "#5a4530"
        draw.line([(rx, ry), (x1, y1)], fill=col, width=2)
    draw.ellipse([(rx - 6, ry - 6), (rx + 6, ry + 6)], fill="#4a3b2c")
    draw.text((rx - 3, ry - r - 12), "N", fill="#8c2d19", font=font)
    draw.text((rx + r + 5, ry - 4), "E", fill="#5a4530", font=font)
    draw.text((rx - 3, ry + r + 3), "S", fill="#5a4530", font=font)
    draw.text((rx - r - 12, ry - 4), "W", fill="#5a4530", font=font)

    # Red dashed navigation route & Treasure Xs
    route_points = [(80, 280), (160, 250), (270, 280), (380, 360), (450, 310), (550, 180)]
    for i in range(len(route_points) - 1):
        p1, p2 = route_points[i], route_points[i + 1]
        draw.line([p1, p2], fill="#b32d20", width=2)

    # Treasure X marks
    for tx, ty, label in [(270, 280, "Cripta del Re"), (550, 180, "Tesoro Perduto")]:
        draw.text((tx - 4, ty - 6), "X", fill="#b32d20", font=font)
        draw.text((tx + 8, ty - 4), label, fill="#8c2d19", font=font)

    # Sea Monster & Danger zones
    draw.text((460, 420), "~ KRAKEN TRENCH ~", fill="#6e5b47", font=font)
    draw.text((100, 400), "! MAELSTROM !", fill="#8c2d19", font=font)

    # Title Cartouche banner at top-left
    title = f"CHARTA NAUTICA: {archipelago_name.upper()}"
    draw.rectangle([(40, 35), (420, 75)], outline="#4a3b2c", width=2, fill="#ded0b2")
    draw.text((55, 48), title, fill="#3b2c1e", font=font)

    # Subtitle at bottom
    sub = "REGISTRATA DALL'ASTROLABIO DI BALTHAZAR - SCUMMBAR"
    draw.text((45, height - 38), sub, fill="#7a6652", font=font)

    out = io.BytesIO()
    img.save(out, format="PNG")
    return out.getvalue()


async def draw_nautical_map(
    tool_context: ToolContext,
    archipelago_name: str,
    map_details: str = "",
) -> str:
    """
    Usa questo strumento ESCLUSIVAMENTE per srotolare e illustrare una mappa nautica cartografica di un arcipelago o isola per l'avventore.
    - archipelago_name: Nome dell'arcipelago, isola o regione marina (es. 'Arcipelago dei Denti di Drago', 'Isole della Nebbia', 'Isola del Teschio').
    - map_details: Dettagli facoltativi su rotte, pericoli o cripte/tesori specifici richiesti dall'avventore o descritti da Balthazar.
    """
    from google import genai

    image_model = IMAGE_MODEL
    log.info("Balthazar draws nautical map: %s (details: %s)", archipelago_name, map_details)

    img_bytes = None

    try:
        # Initialize Google GenAI Client with dedicated image credentials
        client = genai.Client(**get_gemini_client_kwargs(prefix="IMAGE_"))

        map_prompt = (
            f"Antique pirate treasure map and celestial nautical chart of {archipelago_name}, drafted by the master navigator Balthazar, "
            "highly detailed hand-drawn ink engraving on heavily aged, stained, and burnt tattered parchment paper. "
            "Multi-island archipelago layout with jagged coastlines, shaded mountains, and dense jungles. "
            "Fine astronomical charting symbols, celestial constellations, brass astrolabe sketches, and engraved rhumb lines. "
            "Red dashed navigation route winding through dangerous waters, marked with distinct red 'X' spots for buried vaults. "
            "Filled with vintage nautical illustrations: a giant kraken attacking a Spanish galleon, sea serpents, sirens, "
            "swirling whirlpools, and pirate raid warning markers. Features an ornate compass rose with gold accents, "
            "oriental-baroque cartouche calligraphy, water stains, rum spots, and historical maritime symbols, "
            f"masterwork line art, 8k, authentic 17th-century aesthetic. {map_details}".strip()
        )

        # Use the modern Gemini Flash Image API with 4:3 aspect ratio and configured thinking level
        response = client.models.generate_content(
            model=image_model,
            contents=map_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="4:3",
                    image_size="1K",
                ),
                thinking_config=types.ThinkingConfig(
                    thinking_level=IMAGE_THINKING_LEVEL,
                    include_thoughts=False,
                ),
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.data:
                img_bytes = part.inline_data.data
                log.info("Nautical map generated successfully via Gemini multimodal generate_content.")
                break

    except Exception as e:
        log.warning("Errore generazione mappa nautica AI: %s. Attivazione fallback PIL.", e)
        img_bytes = _draw_nautical_map_fallback(archipelago_name, map_details)

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

    safe_title = "".join(c if c.isalnum() else "_" for c in archipelago_name.strip().lower())
    filename = f"mappa_{safe_title}.{file_ext}"

    version = await tool_context.save_artifact(filename=filename, artifact=artifact_part)

    return (
        f"La mappa nautica di '{archipelago_name}' è stata srotolata e incisa sul tavolo da carteggio! "
        f"L'illustrazione è ora visibile all'avventore (Salvata come {filename}, v{version})."
    )


async def fetch_news_feed(tool_context: ToolContext, category: str = "politica_italiana") -> dict:
    """
    Recupera gli ultimi dispacci e notizie reali focalizzati esclusivamente su 2 argomenti:
    - Politica Italiana ('politica_italiana', 'politica', 'italia', 'governo', 'senato', 'parlamento')
    - Politica Americana ('politica_americana', 'usa', 'america', 'stati_uniti', 'washington', 'casa_bianca')

    Usa questo strumento quando un avventore ti chiede notizie sui bisticci dei governanti italiani
    o sulle contese del Grande Impero d'Oltreoceano (USA).
    """
    import xml.etree.ElementTree as ET
    from email.utils import parsedate_to_datetime

    import httpx

    rss_feeds = {
        # Politica Italiana
        "politica_italiana": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "politica": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "italia": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "governo": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "senato": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        "parlamento": "https://www.ansa.it/sito/notizie/politica/politica_rss.xml",
        # Politica Americana
        "politica_americana": 'https://news.google.com/rss/search?q=politica+USA+or+Trump+or+"Casa+Bianca"+or+"governo+USA"+when:7d&hl=it&gl=IT&ceid=IT:it',
        "usa": 'https://news.google.com/rss/search?q=politica+USA+or+Trump+or+"Casa+Bianca"+or+"governo+USA"+when:7d&hl=it&gl=IT&ceid=IT:it',
        "america": 'https://news.google.com/rss/search?q=politica+USA+or+Trump+or+"Casa+Bianca"+or+"governo+USA"+when:7d&hl=it&gl=IT&ceid=IT:it',
        "stati_uniti": 'https://news.google.com/rss/search?q=politica+USA+or+Trump+or+"Casa+Bianca"+or+"governo+USA"+when:7d&hl=it&gl=IT&ceid=IT:it',
        "washington": 'https://news.google.com/rss/search?q=politica+USA+or+Trump+or+"Casa+Bianca"+or+"governo+USA"+when:7d&hl=it&gl=IT&ceid=IT:it',
        "casa_bianca": 'https://news.google.com/rss/search?q=politica+USA+or+Trump+or+"Casa+Bianca"+or+"governo+USA"+when:7d&hl=it&gl=IT&ceid=IT:it',
    }

    cat_key = category.lower().strip()
    url = rss_feeds.get(cat_key, rss_feeds["politica_italiana"])
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()

            root = ET.fromstring(resp.content)
            raw_items = root.findall(".//item")
            if not raw_items:
                raw_items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

            parsed_items = []
            for item in raw_items:
                title_elem = item.find("title")
                desc_elem = item.find("description")
                date_elem = item.find("pubDate")
                if date_elem is None:
                    date_elem = item.find("{http://www.w3.org/2005/Atom}updated")
                link_elem = item.find("link")
                guid_elem = item.find("guid")

                title = title_elem.text.strip() if title_elem is not None and title_elem.text else "Senza titolo"
                desc = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else ""
                date_str = date_elem.text.strip() if date_elem is not None and date_elem.text else ""

                # Robust datetime parsing to sort chronologically
                dt = None
                if date_str:
                    try:
                        dt = parsedate_to_datetime(date_str)
                    except Exception:
                        try:
                            dt = datetime.fromisoformat(date_str)
                        except Exception:
                            dt = None

                if dt is None:
                    dt = datetime.min.replace(tzinfo=UTC)

                link = ""
                if link_elem is not None and link_elem.text:
                    link = link_elem.text.strip()
                elif link_elem is not None and link_elem.attrib.get("href"):
                    link = link_elem.attrib.get("href", "").strip()
                elif guid_elem is not None and guid_elem.text and guid_elem.text.startswith("http"):
                    link = guid_elem.text.strip()

                formatted_date = dt.strftime("%d/%m/%Y alle ore %H:%M") if dt.year > 1 else "Recente"

                parsed_items.append({
                    "titolo_originale": title,
                    "sintesi_originale": desc,
                    "datetime": dt,
                    "ora_pubblicazione": formatted_date,
                    "link_sorgente": link,
                })

            # Rigorously sort items in descending order so the FRESHEST / MOST RECENT news come first
            parsed_items.sort(key=lambda x: x["datetime"], reverse=True)

            # Keep only the top 3 freshest dispatches
            top_headlines = parsed_items[:3]

            cleaned_headlines = [
                {
                    "titolo_originale": h["titolo_originale"],
                    "sintesi_originale": h["sintesi_originale"],
                    "ora_pubblicazione": h["ora_pubblicazione"],
                    "link_sorgente": h["link_sorgente"],
                }
                for h in top_headlines
            ]

            category_label = "Politica Americana" if "america" in cat_key or "usa" in cat_key else "Politica Italiana"

            return {
                "status": "success",
                "categoria_richiesta": category_label,
                "numero_dispacci": len(cleaned_headlines),
                "dispacci": cleaned_headlines,
                "istruzione_traduzione": (
                    "Riferisci queste notizie freschissime all'avventore con drammatica, pomposa e ridicola solennità teatrale! "
                    "Trasponi i bisticci politici italiani o americani nella tua ambientazione "
                    "fantasy-marittima (es: 'L\\'Arengo dei Senatori Borbottanti', 'Il Primo Visir del Ducato', "
                    "'Il Gran Mogol d\\'Oltreoceano', 'L\\'Impero delle Cinquanta Province'). "
                    "Includi SEMPRE per ogni notizia il link HTML originale fornito da 'link_sorgente' "
                    "(es. '<a href=\"LINK\">Srotola la pergamena originale</a>' o '<a href=\"LINK\">Fonte del dispaccio</a>')."
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
write_secret_scroll_tool = FunctionTool(write_secret_scroll)
draw_tarot_card_tool = FunctionTool(draw_tarot_card)
draw_nautical_map_tool = FunctionTool(draw_nautical_map)
fetch_news_feed_tool = FunctionTool(fetch_news_feed)
