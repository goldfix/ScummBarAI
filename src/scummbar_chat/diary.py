"""scummbar_chat — Tavern Journal / Captain's Log Module

Handles reading, updating, and saving first-person pirate diaries for patrons.
Diaries are stored in Markdown format under `data/scummbar_chat/diaries/Diary_NOME.md`.
Incremental updates track the exact integer message index (`last_saved_index`) to ensure
that only new conversation messages are summarized into new chapters.
"""

import asyncio
import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path

from google.adk.models import LlmRequest
from google.genai import types

from src.scummbar_chat.telemetry import record_agent_metric
from src.scummbar_chat.utils import COMPACTION_MODEL

log = logging.getLogger("scummbar.diary")

# Directory where patron diaries are stored
DIARIES_DIR = Path(__file__).parent.parent.parent / "data" / "scummbar_chat" / "diaries"


def sanitize_patron_name(patron_name: str) -> str:
    """Sanitizes patron name to be safe for filenames."""
    cleaned = "".join(c if c.isalnum() else "_" for c in patron_name.strip())
    # Collapse multiple consecutive underscores
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "Avventore_Anonimo"


def get_diary_file_path(patron_name: str) -> Path:
    """Returns the absolute Path for a patron's diary Markdown file."""
    DIARIES_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = sanitize_patron_name(patron_name)
    return DIARIES_DIR / f"Diary_{safe_name}.md"


def read_diary_metadata(file_path: Path) -> dict:
    """
    Reads the HTML comment metadata line at the top of a diary file.
    Example comment: <!-- DIARY_METADATA: {"last_saved_index": 10, "patron_name": "Guybrush"} -->
    """
    if not file_path.exists():
        return {"last_saved_index": 0}

    try:
        content = file_path.read_text(encoding="utf-8")
        match = re.search(r"<!--\s*DIARY_METADATA:\s*({.*?})\s*-->", content)
        if match:
            return json.loads(match.group(1))
    except Exception as e:
        log.warning("Failed to read metadata from diary %s: %s", file_path, e)

    return {"last_saved_index": 0}


def read_diary_content(patron_name: str) -> str:
    """Reads and returns the Markdown content of a patron's diary file if it exists."""
    file_path = get_diary_file_path(patron_name)
    if file_path.exists():
        return file_path.read_text(encoding="utf-8")
    return ""


def _extract_artifact_filename(art: object) -> str | None:
    """Extracts only the clean filename string from an artifact (string or dict with bytes)."""
    if isinstance(art, str):
        return Path(art).name
    if isinstance(art, dict):
        fn = art.get("filename")
        if fn and isinstance(fn, str):
            return Path(fn).name
    return None


def _build_transcript(patron_name: str, new_messages: list[dict], start_idx: int) -> str:
    """Builds the plain-text transcript of new messages for the LLM prompt, noting any illustrations."""
    transcript_lines = []
    for idx, msg in enumerate(new_messages, start=start_idx + 1):
        role = msg.get("role", "user")
        bot_name = msg.get("bot_name")
        content = msg.get("content", "").strip()

        # Extract only clean filename strings (never binary bytes or dict objects!)
        raw_artifacts = msg.get("artifacts", [])
        artifact_filenames: list[str] = []
        for art in raw_artifacts:
            fn = _extract_artifact_filename(art)
            if fn and fn not in artifact_filenames:
                artifact_filenames.append(fn)

        # Also search for filenames in content as fallback
        found_files = re.findall(r"(?:tarocco|mappa|[a-zA-Z0-9_]+)_[a-zA-Z0-9_]+\.(?:png|jpg|jpeg|txt)", content, re.IGNORECASE)
        for fn in found_files:
            if fn not in artifact_filenames:
                artifact_filenames.append(fn)

        if role == "user":
            speaker = f"Avventore {patron_name}"
        elif bot_name:
            speaker = f"Bot {bot_name.capitalize()}"
        else:
            speaker = "Taverna / Narratore"

        line = f"- [Msg #{idx} - {speaker}]: {content}"
        if artifact_filenames:
            for fn in artifact_filenames:
                if fn.lower().endswith((".png", ".jpg", ".jpeg")):
                    line += f"\n  [ILLUSTRAZIONE SVELATA: assets/{fn}]"
                else:
                    line += f"\n  [PERGAMENA CONSEGNATA: assets/{fn}]"

        transcript_lines.append(line)

    return "\n".join(transcript_lines)


async def generate_chapter_async(patron_name: str, new_messages: list[dict], start_idx: int, end_idx: int) -> str:
    """Invokes the Chronicler agent to generate a first-person narrative chapter."""
    from src.scummbar_chat.bots.chronicler.agent import chronicler_agent

    transcript_text = _build_transcript(patron_name, new_messages, start_idx)

    user_prompt = (
        f"Avventore attuale: '{patron_name}'\n"
        f"Trascrizione degli avvenimenti recenti nello Scummbar (dal messaggio #{start_idx + 1} al messaggio #{end_idx}):\n\n"
        f"--- INIZIO TRASCRIZIONE ---\n"
        f"{transcript_text}\n"
        f"--- FINE TRASCRIZIONE ---\n\n"
        f"COMPITO:\n"
        f"Redigi il nuovo capitolo per il Diario di Bordo di '{patron_name}' in prima persona ('Io') "
        f"seguendo scrupolosamente le tue istruzioni e il tuo stile."
    )

    full_prompt = f"{chronicler_agent.instruction}\n\n---\n\n{user_prompt}"

    t0 = time.perf_counter()
    status = "success"

    try:
        # Use chronicler_agent's configured model instance
        llm = chronicler_agent.model
        request = LlmRequest(
            model=COMPACTION_MODEL,
            contents=[types.Content(role="user", parts=[types.Part(text=full_prompt)])],
        )
        async for response in llm.generate_content_async(request):
            if response.content and response.content.parts:
                text_parts = [p.text for p in response.content.parts if getattr(p, "text", None)]
                if text_parts:
                    elapsed_ms = (time.perf_counter() - t0) * 1000.0
                    record_agent_metric(
                        agent_name="chronicler",
                        duration_ms=elapsed_ms,
                        model_name=COMPACTION_MODEL,
                        status="success",
                    )
                    return "\n".join(text_parts).strip()
    except Exception as e:
        status = "error"
        log.error("Failed to generate diary chapter with Chronicler agent: %s", e)
    finally:
        if status == "error":
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            record_agent_metric(
                agent_name="chronicler",
                duration_ms=elapsed_ms,
                model_name=COMPACTION_MODEL,
                status="error",
            )

    # Fallback if LLM call fails
    return (
        f"Oggi ho scambiato diverse battute con i pirati della taverna. "
        f"Abbiamo discusso di eventi recenti e rotta da seguire (Messaggi #{start_idx + 1} - #{end_idx})."
    )


def _write_chapter_to_file(
    patron_name: str,
    total_messages: int,
    chapter_text: str,
    last_saved_index: int,
) -> tuple[bool, str, str]:
    """Appends a new chapter to the diary file (creating it if needed) and returns the full content."""
    file_path = get_diary_file_path(patron_name)
    now_str = datetime.now().strftime("%d %B %Y - %H:%M")
    updated_metadata = json.dumps({"last_saved_index": total_messages, "patron_name": patron_name})

    if file_path.exists():
        content = file_path.read_text(encoding="utf-8")
        new_metadata_comment = f"<!-- DIARY_METADATA: {updated_metadata} -->"

        if "<!-- DIARY_METADATA:" in content:
            content = re.sub(r"<!--\s*DIARY_METADATA:.*-->", new_metadata_comment, content, count=1)
        else:
            content = f"{new_metadata_comment}\n\n" + content

        new_chapter_block = f"\n\n---\n\n## ⚓ Capitolo (Messaggi #{last_saved_index + 1} - #{total_messages})\n*_Registrato il {now_str}_*\n\n{chapter_text}"
        content += new_chapter_block
    else:
        metadata_comment = f"<!-- DIARY_METADATA: {updated_metadata} -->"
        header_block = f"{metadata_comment}\n\n# 📜 Il Diario di Bordo di {patron_name}\n*_Memorie personali, avventure e sbornie nello Scummbar_*\n\n---"
        first_chapter_block = f"\n\n## ⚓ Capitolo 1 (Messaggi #1 - #{total_messages})\n*_Registrato il {now_str}_*\n\n{chapter_text}"
        content = header_block + first_chapter_block

    file_path.write_text(content, encoding="utf-8")
    log.info("Captain's log updated for patron '%s': %d total messages recorded.", patron_name, total_messages)

    return (
        True,
        f"Diario aggiornato con successo! Registrati messaggi da #{last_saved_index + 1} a #{total_messages}.",
        content,
    )


async def update_tavern_diary_async(patron_name: str, messages: list[dict]) -> tuple[bool, str, str]:
    """
    Incrementally updates or creates the patron's diary Markdown file (async).

    Returns:
        (success: bool, status_message: str, full_file_content: str)
    """
    if not patron_name or not patron_name.strip():
        return False, "Nome avventore non specificato.", ""

    patron_name = patron_name.strip()
    total_messages = len(messages)
    if total_messages == 0:
        return False, "Nessun messaggio presente nella cronologia.", ""

    file_path = get_diary_file_path(patron_name)
    metadata = read_diary_metadata(file_path)
    last_saved_index = metadata.get("last_saved_index", 0)

    if total_messages <= last_saved_index:
        return (
            False,
            f"Nessun nuovo messaggio da registrare. (Ultimo messaggio salvato: #{last_saved_index})",
            read_diary_content(patron_name),
        )

    # Slice only new messages from last_saved_index to total_messages
    new_messages = messages[last_saved_index:total_messages]

    # Generate first-person narrative text for this new chapter
    chapter_text = await generate_chapter_async(patron_name, new_messages, last_saved_index, total_messages)

    return _write_chapter_to_file(patron_name, total_messages, chapter_text, last_saved_index)


def update_tavern_diary(patron_name: str, messages: list[dict]) -> tuple[bool, str, str]:
    """
    Synchronous wrapper around `update_tavern_diary_async` for non-async callers
    (e.g. Streamlit script context). Returns the same tuple.
    """
    return asyncio.run(update_tavern_diary_async(patron_name, messages))
