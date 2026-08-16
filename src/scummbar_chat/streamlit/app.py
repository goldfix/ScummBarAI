"""
Module: app.py
Description: Main Streamlit application entry point for the Scummbar single-player RPG frontend.
Connects the Streamlit UI to the Google ADK runner (run_agent), manages session state,
restores past chat history automatically based on Patron Name, uses automatic semantic intent routing,
and formats narration vs speech distinctly.
"""

import asyncio
import hashlib
import json
import re
import sqlite3
from pathlib import Path

import streamlit as st

# Import core Scummbar components
from src.scummbar_chat.diary import (
    get_diary_file_path,
    read_diary_content,
    read_diary_metadata,
    update_tavern_diary,
)
from src.scummbar_chat.streamlit.components import (
    BOT_AVATARS,
    format_streamlit_narrative,
    get_avatar_for_role,
    render_artifacts,
    render_sidebar,
)
from src.scummbar_chat.telegram.adapter import _resolve_intent
from src.scummbar_chat.telegram.runner import run_agent
from src.scummbar_chat.time_context import get_time_description
from src.scummbar_chat.utils import ASSETS_DIR, SESSION_DB_URI

NARRATOR_SYSTEM_PROMPT = (
    "\n\n[NOTA DI SISTEMA: È il momento del Narratore. Alla fine assoluta della tua risposta, "
    "DEVI aggiungere una riga vuota e poi una singola descrizione d'ambiente in corsivo, "
    "racchiusa ESATTAMENTE tra due trattini bassi, seguendo le regole del file scummbar.md.]"
)

# Configure page layout and title
st.set_page_config(
    page_title="ScummBar AI — Taverna dei Pirati",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Regex to strip routing/tag prefixes at the start of a stored user message
# (e.g. "[avventore: X] [avventore_id: Y] [BARNABY] " -> user text only).
_AUGMENT_PREFIX_PATTERN = re.compile(r"^(?:\[[^\]]+\]\s*)+")
# Regex to remove the injected Narratore system note appended to the user prompt
# (e.g. "\n\n[NOTA DI SISTEMA: È il momento del Narratore...]").
_NARRATOR_NOTE_PATTERN = re.compile(r"\n*\[NOTA DI SISTEMA:[^\]]*\]")


def _render_diary_html(diary_markdown: str, assets_dir: Path) -> str:
    """
    Converts local relative Markdown image links and text scroll links into
    browser-renderable HTML elements (Base64 Data URIs, inline preview cards, and download buttons).
    """
    import base64
    import html

    # 1. Replace Images with Base64 Data URIs for browser rendering
    def _replace_image(match: re.Match) -> str:
        alt_text = match.group(1)
        filename = Path(match.group(2)).name
        file_path = assets_dir / filename
        if file_path.exists():
            mime = "image/jpeg" if filename.lower().endswith((".jpg", ".jpeg")) else "image/png"
            b64_data = base64.b64encode(file_path.read_bytes()).decode("utf-8")
            return (
                f'<div style="text-align: center; margin: 16px 0;">'
                f'<img src="data:{mime};base64,{b64_data}" alt="{alt_text}" '
                f'style="max-width: 100%; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3);"><br>'
                f'<em style="font-size: 0.9em; color: #555;">{alt_text}</em>'
                f'</div>'
            )
        return match.group(0)

    # 2. Replace Text Scrolls (.txt) with styled preview cards and instant download links
    def _replace_text_file(match: re.Match) -> str:
        link_title = match.group(1)
        filename = Path(match.group(2)).name
        file_path = assets_dir / filename
        if file_path.exists():
            text_bytes = file_path.read_bytes()
            b64_data = base64.b64encode(text_bytes).decode("utf-8")
            data_uri = f"data:text/plain;charset=utf-8;base64,{b64_data}"
            escaped_content = html.escape(text_bytes.decode("utf-8", errors="replace"))
            return (
                f'<div style="background-color: #f8f9fa; border: 1px solid #ced4da; border-left: 4px solid #f39c12; '
                f'border-radius: 6px; padding: 12px 16px; margin: 14px 0; box-shadow: 0 2px 6px rgba(0,0,0,0.08);">'
                f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">'
                f'<strong style="color: #2c3e50; font-size: 1em;">{link_title}</strong>'
                f'<a href="{data_uri}" download="{filename}" style="background-color: #34495e; color: #ffffff !important; '
                f'text-decoration: none; padding: 4px 10px; border-radius: 4px; font-size: 0.85em; font-weight: bold;">💾 Scarica {filename}</a>'
                f'</div>'
                f'<pre style="background-color: #ffffff; border: 1px solid #e9ecef; color: #212529; padding: 10px; border-radius: 4px; '
                f'font-size: 0.88em; white-space: pre-wrap; font-family: monospace; margin: 0; max-height: 250px; overflow-y: auto;">{escaped_content}</pre>'
                f'</div>'
            )
        return match.group(0)

    rendered = re.sub(
        r"!\[(.*?)\]\((?:assets/)?([^\)]+\.(?:jpg|jpeg|png|webp))\)",
        _replace_image,
        diary_markdown,
        flags=re.IGNORECASE,
    )

    rendered = re.sub(
        r"\[(.*?)\]\((?:assets/)?([^\)]+\.txt)\)",
        _replace_text_file,
        rendered,
        flags=re.IGNORECASE,
    )
    return rendered


def _get_user_id(patron_name: str) -> str:
    """Generates a stable numerical user_id hash from patron_name for ADK patron_memories."""
    hash_object = hashlib.sha256(patron_name.strip().lower().encode("utf-8"))
    # Return numerical string to fit Telegram-style user_id schema
    return str(int(hash_object.hexdigest()[:10], 16))


def load_session_chat_history(user_id: str, session_id: str) -> list[dict]:
    """
    Queries SQLite 'events' table for historical dialogue events associated
    with the given user_id and session_id, restoring full past chat history
    alongside any generated artifacts/images.
    """
    db_path = SESSION_DB_URI.replace("sqlite+aiosqlite:///", "").replace("sqlite:///", "")
    if not Path(db_path).exists():
        return []

    try:
        with sqlite3.connect(db_path, timeout=10.0) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute(
                "SELECT event_data FROM events WHERE user_id = ? AND session_id = ? ORDER BY timestamp ASC",
                (user_id, session_id),
            ).fetchall()

            messages: list[dict] = []
            pending_artifacts: list[dict] = []

            for r in rows:
                try:
                    data = json.loads(r["event_data"])
                    content = data.get("content", {})
                    parts = content.get("parts", [])
                    role = content.get("role", "")
                    author = data.get("author", "barnaby")

                    # Extract plain text and artifacts from user or assistant turns
                    text_parts: list[str] = []
                    for p in parts:
                        if "function_response" in p:
                            fr = p["function_response"]
                            res = fr.get("response", {})
                            if isinstance(res, dict) and "result" in res and isinstance(res["result"], str):
                                for fn in re.findall(r"(?:Salvata come|Pergamena)\s+['\"]?([a-zA-Z0-9_\.]+\.(?:png|jpg|jpeg|txt))['\"]?", res["result"], re.IGNORECASE):
                                    if (ASSETS_DIR / fn).exists() and not any(a.get("filename") == fn for a in pending_artifacts):
                                        is_img = fn.lower().endswith((".png", ".jpg", ".jpeg"))
                                        pending_artifacts.append({
                                            "filename": fn,
                                            "type": "image" if is_img else "text",
                                            "path": str(ASSETS_DIR / fn),
                                            "url": f"assets/{fn}",
                                        })
                        elif "text" in p and not p.get("thought", False):
                            text = p["text"]
                            # Clean up internal prompt tags if user message
                            if role == "user" and "[avventore:" in text:
                                text = _AUGMENT_PREFIX_PATTERN.sub("", text).strip()
                                # Remove the Narratore system note if it was injected on this turn
                                text = _NARRATOR_NOTE_PATTERN.sub("", text).strip()
                            text_parts.append(text)

                    if text_parts:
                        full_text = "\n".join(text_parts).strip()
                        if full_text and role in ["user", "model", "assistant"]:
                            norm_role = "user" if role == "user" else "assistant"
                            attached_artifacts = list(pending_artifacts) if norm_role == "assistant" else []
                            # Fallback scan: check if text itself references any saved artifact filename
                            if norm_role == "assistant":
                                for fn in re.findall(r"(?:Salvata come|Pergamena)\s+['\"]?([a-zA-Z0-9_\.]+\.(?:png|jpg|jpeg|txt))['\"]?", full_text, re.IGNORECASE):
                                    if (ASSETS_DIR / fn).exists() and not any(a.get("filename") == fn for a in attached_artifacts):
                                        is_img = fn.lower().endswith((".png", ".jpg", ".jpeg"))
                                        attached_artifacts.append({
                                            "filename": fn,
                                            "type": "image" if is_img else "text",
                                            "path": str(ASSETS_DIR / fn),
                                            "url": f"assets/{fn}",
                                        })

                            messages.append(
                                {
                                    "role": norm_role,
                                    "content": full_text,
                                    "bot_name": author if norm_role == "assistant" else None,
                                    "artifacts": attached_artifacts,
                                }
                            )
                            if norm_role == "assistant":
                                pending_artifacts.clear()
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue

            return messages
    except sqlite3.Error:
        return []


def main() -> None:
    """Main Streamlit application loop."""
    # 1. Render Sidebar & retrieve user preferences
    controls = render_sidebar()
    patron_name = controls["patron_name"].strip()

    # 2. Header & Live Atmosphere Banner
    st.title("🍺 Scummbar AI — Taverna dei Pirati")
    current_time_desc = get_time_description()
    st.info(f"🌆 **Atmosfera in Taverna**: {current_time_desc}")

    # 3. Mandatory Patron Name Guard
    if not patron_name:
        st.warning(
            "🏴‍☠️ **Alt, Pirata!** Per varcare la soglia dello Scummbar e farti riconoscere dal barista, "
            "inserisci prima il tuo **Nome Avventore** nel menu a sinistra!"
        )
        st.chat_input(
            "⚠️ Inserisci prima il tuo Nome Avventore nel menu a sinistra per iniziare a parlare...",
            disabled=True,
        )
        return

    # Derive numerical user_id and deterministic session_id from patron_name
    user_id = _get_user_id(patron_name)
    session_id = f"st_session_{user_id}"

    # Restore or switch chat history when patron_name changes
    if st.session_state.get("current_patron_name") != patron_name:
        st.session_state["current_patron_name"] = patron_name
        st.session_state["session_id"] = session_id
        # Reset automatic diary check baseline for the new patron
        st.session_state["last_auto_diary_check"] = 0

        past_messages = load_session_chat_history(user_id, session_id)
        if past_messages:
            st.session_state["messages"] = past_messages
        else:
            welcome_intro = (
                f"_Un'insegna di legno scricchiola al vento caraibico. Entri nello Scummbar, "
                f"l'aria profuma di rum speziato e salsedine. Dietro il bancone, Barnaby ti osserva "
                f"in silenzio pulendo un boccale._\n\n"
                f"**Barnaby**: Benvenuto allo Scummbar, **{patron_name}**. Cosa ti porta qui oggi?"
            )
            st.session_state["messages"] = [
                {
                    "role": "assistant",
                    "content": welcome_intro,
                    "bot_name": "barnaby",
                    "artifacts": [],
                }
            ]

    # 4. Main Interface Views: Chat vs Captain's Log
    # NOTE: st.chat_input must NOT be placed inside st.tabs/st.container/st.expander
    # or it loses its sticky bottom anchoring. We use a segmented control for
    # navigation and render the chat input at top-level so it stays pinned.
    view = st.segmented_control(
        "Vista",
        options=["💬 Chat Taverna", "📜 Diario di Bordo"],
        default="💬 Chat Taverna",
        key="view_selector",
    )

    if view == "💬 Chat Taverna":
        # A. Render Historical Chat Messages
        for msg in st.session_state.get("messages", []):
            role = msg["role"]
            bot_name = msg.get("bot_name")
            avatar = get_avatar_for_role(role, bot_name)

            with st.chat_message(role, avatar=avatar):
                formatted_text = format_streamlit_narrative(msg["content"])
                st.markdown(formatted_text, unsafe_allow_html=True)
                if msg.get("artifacts"):
                    render_artifacts(msg["artifacts"])

        # B. User Chat Input (Automatic Semantic Routing) — top-level for sticky bottom
        if prompt := st.chat_input("Rivolgiti alla taverna, al barista, alla maga o al navigatore..."):
            # Display user message immediately
            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": prompt,
                    "bot_name": None,
                    "artifacts": [],
                }
            )
            with st.chat_message("user", avatar=BOT_AVATARS["user"]):
                st.markdown(prompt)

            # Automatic intent routing via names or appellations ("maga", "navigatore", etc.)
            detected_bot = _resolve_intent(prompt)
            augmented_prompt = prompt

            if detected_bot:
                augmented_prompt = f"[{detected_bot.upper()}] {prompt}"

            # Inject patron ID context for memory recall
            augmented_prompt = f"[avventore: {patron_name}] [avventore_id: {user_id}] {augmented_prompt}"

            # Increment session message counter to trigger Narrator prompt every 3 turns
            st.session_state["narrator_counter"] = st.session_state.get("narrator_counter", 0) + 1
            if st.session_state["narrator_counter"] % 3 == 0:
                st.session_state["narrator_counter"] = 0
                augmented_prompt += NARRATOR_SYSTEM_PROMPT

            # Execute ADK agent turn asynchronously with a spinner
            active_avatar = BOT_AVATARS.get(detected_bot, "🍺") if detected_bot else "🍺"
            with st.chat_message("assistant", avatar=active_avatar):
                with st.spinner("La taverna sta elaborando la tua richiesta..."):
                    try:
                        response_text, artifacts = asyncio.run(
                            run_agent(
                                user_id=user_id,
                                session_id=session_id,
                                text=augmented_prompt,
                            )
                        )
                    except Exception as e:
                        response_text = f"⚠️ *Si è verificato un errore nello Scummbar*: {e}"
                        artifacts = []

                # Render formatted assistant response and artifacts
                formatted_response = format_streamlit_narrative(response_text)
                st.markdown(formatted_response, unsafe_allow_html=True)
                if artifacts:
                    render_artifacts(artifacts)

            # Convert raw artifacts to clean lightweight link descriptors
            clean_artifacts = []
            if artifacts:
                for a in artifacts:
                    fn = a.get("filename") if isinstance(a, dict) else str(a)
                    if fn:
                        is_img = fn.lower().endswith((".png", ".jpg", ".jpeg"))
                        clean_artifacts.append({
                            "filename": fn,
                            "type": "image" if is_img else "text",
                            "path": str(ASSETS_DIR / fn),
                            "url": f"assets/{fn}",
                        })

            # Save response to session state
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": response_text,
                    "bot_name": detected_bot or "barnaby",
                    "artifacts": clean_artifacts,
                }
            )

            # C. Automatic Diary Update Check (Every 10 messages)
            total_msgs = len(st.session_state.messages)
            last_auto = st.session_state.get("last_auto_diary_check", 0)
            if total_msgs >= last_auto + 10:
                st.session_state["last_auto_diary_check"] = total_msgs
                success, status_msg, _ = update_tavern_diary(patron_name, st.session_state.messages)
                if success:
                    st.toast("📜 Il tuo Diario di Bordo si è arricchito di un nuovo capitolo!", icon="📜")

    else:
        # Captain's Log view
        st.subheader(f"📜 Il Diario di Bordo di {patron_name}")

        file_path = get_diary_file_path(patron_name)
        meta = read_diary_metadata(file_path)
        last_saved = meta.get("last_saved_index", 0)
        current_msgs = len(st.session_state.get("messages", []))

        col1, col2 = st.columns([2, 1])

        with col1:
            st.caption(f"📊 Messaggi registrati nel Diario: **{last_saved}** / **{current_msgs}** presenti in chat.")

        with col2:
            if st.button("🔄 Compila / Aggiorna Diario ORA", key="btn_manual_diary", use_container_width=True):
                with st.spinner("Compilazione del Diario di Bordo in corso..."):
                    success, status_msg, _ = update_tavern_diary(patron_name, st.session_state.get("messages", []))
                    if success:
                        st.success(status_msg)
                        st.rerun()
                    else:
                        st.info(status_msg)

        diary_content = read_diary_content(patron_name)

        if diary_content:
            st.download_button(
                label="📥 Scarica Diario (.md)",
                data=diary_content,
                file_name=file_path.name,
                mime="text/markdown",
            )
            st.markdown("---")
            # Resolve relative 'assets/' into base64 Data URIs on-the-fly for instant browser rendering
            rendered_diary = _render_diary_html(diary_content, ASSETS_DIR)
            st.markdown(rendered_diary, unsafe_allow_html=True)
        else:
            st.info(
                "📜 *Il tuo diario di bordo è ancora intonso.* "
                "Parla con gli abitanti dello Scummbar per accumulare ricordi, "
                "oppure premi **'Compila / Aggiorna Diario ORA'** per iniziare a scrivere la tua storia!"
            )


if __name__ == "__main__":
    main()
