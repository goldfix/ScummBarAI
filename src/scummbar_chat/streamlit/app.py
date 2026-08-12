"""
Module: app.py
Description: Main Streamlit application entry point for the Scummbar single-player RPG frontend.
Connects the Streamlit UI to the Google ADK runner (run_agent), manages session state,
and renders real-time tavern atmosphere, chat dialogue, and artifacts.
"""

import asyncio
import hashlib
import uuid

import streamlit as st

# Import core Scummbar components
from src.scummbar_chat.streamlit.components import (
    BOT_AVATARS,
    get_avatar_for_role,
    render_artifacts,
    render_sidebar,
)
from src.scummbar_chat.telegram.runner import run_agent
from src.scummbar_chat.time_context import get_time_description

# Configure page layout and title
st.set_page_config(
    page_title="ScummBar AI — Taverna dei Pirati",
    page_icon="🍺",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _init_session_state() -> None:
    """Initializes Streamlit session state variables for chat history and user tracking."""
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = f"st_{uuid.uuid4().hex[:12]}"

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "_Un'insegna di legno scricchiola al vento caraibico. Entri nello Scummbar, l'aria profuma di rum Speziato e salsedine. Dietro il bancone, Barnaby ti osserva in silenzio pulendo un boccale._\n\n**Barnaby**: Benvenuto allo Scummbar, avventore. Cosa ti porta qui oggi?",
                "bot_name": "barnaby",
                "artifacts": [],
            }
        ]


def _get_user_id(patron_name: str) -> str:
    """Generates a stable numerical user_id hash from patron_name for ADK patron_memories."""
    hash_object = hashlib.sha256(patron_name.strip().lower().encode("utf-8"))
    # Return numerical string to fit Telegram-style user_id schema
    return str(int(hash_object.hexdigest()[:10], 16))


def main() -> None:
    """Main Streamlit application loop."""
    _init_session_state()

    # 1. Render Sidebar & retrieve user preferences
    controls = render_sidebar()
    patron_name = controls["patron_name"]
    selected_bot = controls["selected_bot"]

    # Derive numerical user_id for ADK memory tools
    user_id = _get_user_id(patron_name)
    session_id = st.session_state["session_id"]

    # 2. Header & Live Atmosphere Banner
    st.title("🍺 Scummbar AI — Taverna dei Pirati")
    current_time_desc = get_time_description()
    st.info(f"🌆 **Atmosfera in Taverna**: {current_time_desc}")

    # 3. Render Historical Chat Messages
    for msg in st.session_state.messages:
        role = msg["role"]
        bot_name = msg.get("bot_name")
        avatar = get_avatar_for_role(role, bot_name)

        with st.chat_message(role, avatar=avatar):
            st.markdown(msg["content"])
            if msg.get("artifacts"):
                render_artifacts(msg["artifacts"])

    # 4. User Chat Input
    prompt = st.chat_input("Scrivi un messaggio a Barnaby o alla taverna...")
    if prompt:
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

        # B. Format prompt with routing prefix if a specific bot is selected
        augmented_prompt = prompt
        if selected_bot and selected_bot != "auto":
            bot_tag = f"[{selected_bot.upper()}]"
            augmented_prompt = f"[{bot_tag}] {prompt}"

        # Inject patron ID context for memory recall
        augmented_prompt = f"[avventore: {patron_name}] [avventore_id: {user_id}] {augmented_prompt}"

        # C. Execute ADK agent turn asynchronously with a spinner
        with st.chat_message("assistant", avatar="🏴‍☠️"):
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

            # D. Render assistant response and artifacts
            st.markdown(response_text)
            if artifacts:
                render_artifacts(artifacts)

        # E. Save response to session state
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": response_text,
                "bot_name": selected_bot if selected_bot != "auto" else "barnaby",
                "artifacts": artifacts,
            }
        )


if __name__ == "__main__":
    main()
