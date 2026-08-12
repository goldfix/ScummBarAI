"""
Module: components.py
Description: UI components and rendering helpers for the Streamlit Scummbar frontend.
Provides avatar mapping, custom narrative & action formatting, artifact rendering,
and sidebar controls.
"""

import re

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
    "isolde": "Isolde (La Veggente / Maga)",
    "balthazar": "Balthazar (Il Navigatore)",
}

# Regex patterns for parsing narrative vs speech
_FULL_LINE_ENV_PATTERN = re.compile(r"^\s*_\s*(.+?)\s*_\s*$")
_INLINE_ACTION_PATTERN = re.compile(r"\*([^*]+)\*")


def get_avatar_for_role(role: str, bot_name: str | None = None) -> str:
    """Returns the appropriate avatar emoji based on role and active bot name."""
    if role == "user":
        return BOT_AVATARS["user"]
    if bot_name in BOT_AVATARS:
        return BOT_AVATARS[bot_name]
    return BOT_AVATARS["system"]


def format_streamlit_narrative(text: str) -> str:
    """
    Transforms agent response text into visually distinct layers:
    1. Full-line Environmental Narration (_text_): Monospace dark callout box with gold left border.
    2. Character Physical Actions (*action*): Monospace code badge with action symbols (✦).
    3. Spoken Dialogue: Normal, unstyled sans-serif text so speech stands out prominently.
    """
    if not text:
        return ""

    lines = text.split("\n")
    formatted_lines: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append("")
            continue

        # 1. Full-line Environmental Narration (_text_) -> Monospace Box
        m_full = _FULL_LINE_ENV_PATTERN.match(stripped)
        if m_full:
            inner_text = m_full.group(1).strip()
            formatted_lines.append(
                f'<div style="font-family: monospace !important; font-size: 0.9em; '
                f"background-color: #1a202c; border: 1px solid #2d3748; "
                f"border-left: 4px solid #d4af37; padding: 10px 14px; margin: 8px 0; "
                f'border-radius: 6px; color: #cbd5e0; line-height: 1.5;">'
                f"📜 <i>{inner_text}</i></div>"
            )
            continue

        # 2. Inline Character Physical Actions (*action*) -> Monospace Code Badge
        def _replace_action(match: re.Match) -> str:
            action_text = match.group(1).strip()
            return (
                f'<code style="font-family: monospace !important; font-size: 0.88em; '
                f"color: #f6ad55; background-color: rgba(246, 173, 85, 0.12); "
                f"padding: 2px 6px; border-radius: 4px; "
                f'border: 1px solid rgba(246, 173, 85, 0.25);">✦ {action_text} ✦</code>'
            )

        formatted_line = _INLINE_ACTION_PATTERN.sub(_replace_action, line)
        formatted_lines.append(formatted_line)

    return "\n".join(formatted_lines)


def render_sidebar() -> dict:
    """
    Renders the Streamlit sidebar containing player identity, tavern legend,
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

    # 2. Informational Tavern Legend (Automatic Routing)
    st.sidebar.subheader("📍 Personaggi in Taverna")
    st.sidebar.markdown(
        "Rivolgiti liberamente alla taverna usando **nomi o appellativi**:\n\n"
        "- 🍺 **Barnaby** (*barista, grog, menu, oste*)\n"
        "- 🐱 **Barnacle** (*gatto, micio, fusa*)\n"
        "- 🔮 **Isolde** (*veggente, maga, tarocchi, oracolo*)\n"
        "- 🧭 **Balthazar** (*navigatore, cartografo, mappe, notizie*)"
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
