"""
Module: components.py
Description: UI components and rendering helpers for the Streamlit Scummbar frontend.
Provides avatar mapping, message formatting, artifact rendering (scrolls/images),
and sidebar controls.
"""

import streamlit as st

# Map bot names to custom emojis/avatars for st.chat_message
BOT_AVATARS = {
    "barnaby": "🍺",
    "barnacle": "🐱",
    "isolde": "🔮",
    "balthazar": "🧭",
    "user": "🏴‍☠️",
    "system": "📜",
}

BOT_DISPLAY_NAMES = {
    "barnaby": "Barnaby (Il Barista)",
    "barnacle": "Barnacle (Il Gatto)",
    "isolde": "Isolde (La Veggente)",
    "balthazar": "Balthazar (Il Navigatore)",
    "auto": "🎯 Routing Automatico",
}


def get_avatar_for_role(role: str, bot_name: str | None = None) -> str:
    """Returns the appropriate avatar emoji based on role and active bot name."""
    if role == "user":
        return BOT_AVATARS["user"]
    if bot_name in BOT_AVATARS:
        return BOT_AVATARS[bot_name]
    return BOT_AVATARS["system"]


def render_sidebar() -> dict:
    """
    Renders the Streamlit sidebar containing player identity, bot selector,
    and game session management controls.
    """
    st.sidebar.title("🏴‍☠️ Scummbar Tavern")
    st.sidebar.markdown("---")

    # 1. Player Identity
    st.sidebar.subheader("👤 Il Tuo Pirata")
    patron_name = st.sidebar.text_input(
        "Nome Avventore:",
        value=st.session_state.get("patron_name", "Guybrush"),
        help="Il nome con cui Barnaby e la taverna ti ricorderanno.",
    )
    st.session_state["patron_name"] = patron_name

    st.sidebar.markdown("---")

    # 2. Target Bot Selector
    st.sidebar.subheader("💬 Chi vuoi interpellare?")
    selected_bot = st.sidebar.radio(
        "Seleziona interlocutore:",
        options=["auto", "barnaby", "barnacle", "isolde", "balthazar"],
        format_func=lambda x: BOT_DISPLAY_NAMES.get(x, x),
        help="Forza la risposta di un bot specifico o lascia che la taverna decida in base al contesto.",
    )

    st.sidebar.markdown("---")

    # 3. Session Controls
    st.sidebar.subheader("🛠️ Gestione Partita")
    if st.sidebar.button("🧹 Pulisci Cronologia Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.artifacts = []
        st.rerun()

    return {
        "patron_name": patron_name,
        "selected_bot": selected_bot,
    }


def render_artifacts(artifacts: list[dict]) -> None:
    """
    Renders artifacts (secret scrolls, tarot images, portolans) returned by ADK agents.
    - Text files (.txt): Shown in expanders with a download button.
    - Images (.png/.jpg): Rendered using st.image().
    """
    if not artifacts:
        return

    for artifact in artifacts:
        filename = artifact.get("filename", "artefatto.txt")
        data = artifact.get("bytes", b"")

        # Handle Images (e.g. Tarot cards or generated artwork)
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            st.image(data, caption=f"🖼️ {filename}", use_container_width=True)
        else:
            # Handle Text Artifacts (Scrolls, recipes, portolans)
            try:
                text_content = data.decode("utf-8")
            except UnicodeDecodeError:
                text_content = "[Contenuto binario non decodificabile]"

            with st.expander(f"📜 Pergamena Ricevuta: {filename}", expanded=True):
                st.code(text_content, language="markdown")
                st.download_button(
                    label=f"💾 Scarica {filename}",
                    data=data,
                    file_name=filename,
                    mime="text/plain",
                    key=f"dl_{filename}_{hash(data)}",
                )
