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
import sqlite3
from pathlib import Path

import streamlit as st

# Import core Scummbar components
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
from src.scummbar_chat.utils import SESSION_DB_URI

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


def _get_user_id(patron_name: str) -> str:
    """Generates a stable numerical user_id hash from patron_name for ADK patron_memories."""
    hash_object = hashlib.sha256(patron_name.strip().lower().encode("utf-8"))
    # Return numerical string to fit Telegram-style user_id schema
    return str(int(hash_object.hexdigest()[:10], 16))


def load_session_chat_history(user_id: str, session_id: str) -> list[dict]:
    """
    Queries SQLite 'events' table for historical dialogue events associated
    with the given user_id and session_id, restoring full past chat history.
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
            for r in rows:
                try:
                    data = json.loads(r["event_data"])
                    content = data.get("content", {})
                    parts = content.get("parts", [])
                    role = content.get("role", "")

                    # Extract plain text from user or assistant turns
                    text_parts: list[str] = []
                    for p in parts:
                        if "text" in p and not p.get("thought", False):
                            text = p["text"]
                            # Clean up internal prompt tags if user message
                            if role == "user" and "[avventore:" in text:
                                idx = text.rfind("] ")
                                if idx != -1:
                                    text = text[idx + 2 :]
                                # Strip bot routing tag prefix if present
                                for tag in ["[BARNABY] ", "[ISOLDE] ", "[BALTHAZAR] ", "[BARNACLE] "]:
                                    if text.startswith(tag):
                                        text = text[len(tag) :]
                                        break
                            text_parts.append(text)

                    if text_parts:
                        full_text = "\n".join(text_parts).strip()
                        if full_text and role in ["user", "model", "assistant"]:
                            norm_role = "user" if role == "user" else "assistant"
                            messages.append(
                                {
                                    "role": norm_role,
                                    "content": full_text,
                                    "bot_name": "barnaby" if norm_role == "assistant" else None,
                                    "artifacts": [],
                                }
                            )
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue

            return messages
    except sqlite3.Error:
        return []


def main() -> None:
    """Main Streamlit application loop."""
    # 1. Render Sidebar & retrieve user preferences
    controls = render_sidebar()
    patron_name = controls["patron_name"]

    # Derive numerical user_id and deterministic session_id from patron_name
    user_id = _get_user_id(patron_name)
    session_id = f"st_session_{user_id}"

    # Restore or switch chat history when patron_name changes
    if st.session_state.get("current_patron_name") != patron_name:
        st.session_state["current_patron_name"] = patron_name
        st.session_state["session_id"] = session_id

        past_messages = load_session_chat_history(user_id, session_id)
        if past_messages:
            st.session_state["messages"] = past_messages
        else:
            welcome_intro = (
                f"_*Un'insegna di legno scricchiola al vento caraibico. Entri nello Scummbar, "
                f"l'aria profuma di rum speziato e salsedine. Dietro il bancone, Barnaby ti osserva "
                f"in silenzio pulendo un boccale._*\n\n"
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

    # 2. Header & Live Atmosphere Banner
    st.title("🍺 Scummbar AI — Taverna dei Pirati")
    current_time_desc = get_time_description()
    st.info(f"🌆 **Atmosfera in Taverna**: {current_time_desc}")

    # 3. Render Historical Chat Messages
    for msg in st.session_state.get("messages", []):
        role = msg["role"]
        bot_name = msg.get("bot_name")
        avatar = get_avatar_for_role(role, bot_name)

        with st.chat_message(role, avatar=avatar):
            formatted_text = format_streamlit_narrative(msg["content"])
            st.markdown(formatted_text, unsafe_allow_html=True)
            if msg.get("artifacts"):
                render_artifacts(msg["artifacts"])

    # 4. User Chat Input (Automatic Semantic Routing)
    if prompt := st.chat_input("Rivolgiti alla taverna, al barista, alla maga o al navigatore..."):
        # A. Display user message immediately
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

        # B. Automatic intent routing via names or appellations ("maga", "navigatore", etc.)
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

        # C. Execute ADK agent turn asynchronously with a spinner
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

            # D. Render formatted assistant response and artifacts
            formatted_response = format_streamlit_narrative(response_text)
            st.markdown(formatted_response, unsafe_allow_html=True)
            if artifacts:
                render_artifacts(artifacts)

        # E. Save response to session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text,
                "bot_name": detected_bot or "barnaby",
                "artifacts": artifacts,
            }
        )


if __name__ == "__main__":
    main()
