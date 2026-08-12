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

# Regex patterns for parsing narrative vs speech.
# Full-line env: matches _text_ and _*text*_ (optional inner asterisks for emphasis).
# Inline actions: matches *action* but NOT **bold** markdown (negative lookarounds).
_FULL_LINE_ENV_PATTERN = re.compile(r"^_\s*(.+?)\s*_$")
_FULL_LINE_ENV_EMPH_PATTERN = re.compile(r"^_\*\s*(.+?)\s*\*_$")
_INLINE_ACTION_PATTERN = re.compile(r"(?<!\*)\*([^*\n]+)\*(?!\*)")


def get_avatar_for_role(role: str, bot_name: str | None = None) -> str:
    """Returns the appropriate avatar emoji based on role and active bot name."""
    if role == "user":
        return BOT_AVATARS["user"]
    if bot_name in BOT_AVATARS:
        return BOT_AVATARS[bot_name]
    return BOT_AVATARS["system"]


def _extract_env_text(line: str) -> str | None:
    """Extracts narration text from a full-line environment line (_text_ or _*text*_)."""
    # Order matters: _*...*_ must be tried first, otherwise _..._ captures it
    # and leaves the inner asterisks in the extracted text.
    for pattern in (_FULL_LINE_ENV_EMPH_PATTERN, _FULL_LINE_ENV_PATTERN):
        match = pattern.match(line.strip())
        if match:
            return match.group(1).strip() or None
    return None


def format_streamlit_narrative(text: str) -> str:
    """
    Transforms agent response text into visually distinct layers:
    1. Full-line Environmental Narration (_text_): Italic quoted text on a light grey box.
    2. Character Physical Actions (*action*): Italic quoted text on a light grey inline badge.
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

        # 1. Full-line Environmental Narration (_text_ or _*text*_) -> Grey italic quoted box
        env_text = _extract_env_text(stripped)
        if env_text:
            formatted_lines.append(
                f'<div style="font-style: italic; color: #333333 !important; '
                f"background-color: #e9ecef; padding: 8px 12px; margin: 6px 0; "
                f'border-radius: 6px; line-height: 1.5;">'
                f"«{env_text}»</div>"
            )
            continue

        # 2. Inline Character Physical Actions (*action*) -> Grey italic quoted badge
        def _replace_action(match: re.Match) -> str:
            action_text = match.group(1).strip()
            return (
                f'<span style="font-style: italic; color: #333333 !important; '
                f'background-color: #e9ecef; padding: 2px 6px; border-radius: 4px;">'
                f"«{action_text}»</span>"
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

    # 1. Player Identity (Mandatory)
    st.sidebar.subheader("👤 Il Tuo Pirata")
    patron_name = st.sidebar.text_input(
        "Nome Avventore (Obbligatorio):",
        value=st.session_state.get("patron_name", ""),
        placeholder="Es. Guybrush Threepwood...",
        help="Inserisci il tuo nome da pirata per entrare nello Scummbar e farti riconoscere dal barista.",
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
        # Artifacts live inside messages[i]["artifacts"], so clearing messages is enough.
        st.session_state.messages = []
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
        # Note: use_container_width is deprecated in Streamlit >= 1.4x; use width="stretch".
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            st.image(data, caption=f"🖼️ {filename}", width="stretch")
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
