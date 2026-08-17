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
import time
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
from src.scummbar_chat.telemetry import (
    get_agent_breakdown,
    get_available_log_files,
    get_kpi_summary,
    get_recent_trace_turns,
    get_recent_turns,
    get_time_series_data,
    get_tool_breakdown,
    get_turn_trace_tree,
    log_context,
    read_log_tail,
    record_agent_metric,
    record_turn_metric,
    render_logs_html,
    render_waterfall_html,
    setup_logging,
)
from src.scummbar_chat.time_context import get_time_description
from src.scummbar_chat.utils import ASSETS_DIR, SESSION_DB_URI

# Initialize centralized logging for the Streamlit process
setup_logging(debug=False)

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

    # 4. Main Interface Views: Chat vs Captain's Log vs Metrics vs Traces vs Logs
    # NOTE: st.chat_input must NOT be placed inside st.tabs/st.container/st.expander
    # or it loses its sticky bottom anchoring. We use a segmented control for
    # navigation and render the chat input at top-level so it stays pinned.
    view = st.segmented_control(
        "Vista",
        options=[
            "💬 Chat Taverna",
            "📜 Diario di Bordo",
            "📊 Metriche & Performance",
            "🔍 Traces & Waterfall",
            "🪵 Log di Sistema",
        ],
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

            # Monotonic turn counter for telemetry correlation (turn_id)
            turn_counter = st.session_state.get("turn_counter", 0) + 1
            st.session_state["turn_counter"] = turn_counter
            # Globally unique turn id (session-scoped counter keeps disjoint from
            # Telegram turn ids in the shared turn_metrics table).
            turn_id = f"st:{session_id}:{turn_counter}"

            # Execute ADK agent turn asynchronously with a spinner
            active_avatar = BOT_AVATARS.get(detected_bot, "🍺") if detected_bot else "🍺"
            target_bot_name = detected_bot or "barnaby"
            t0_turn = time.perf_counter()

            with st.chat_message("assistant", avatar=active_avatar):
                with st.spinner("La taverna sta elaborando la tua richiesta..."):
                    try:
                        with log_context(
                            channel="streamlit",
                            session_id=session_id,
                            user_id=user_id,
                            agent_name=target_bot_name,
                            turn_id=turn_id,
                        ):
                            response_text, artifacts, usage = asyncio.run(
                                run_agent(
                                    user_id=user_id,
                                    session_id=session_id,
                                    text=augmented_prompt,
                                )
                            )
                            elapsed_turn_ms = (time.perf_counter() - t0_turn) * 1000.0

                            record_turn_metric(
                                turn_id=turn_id,
                                channel="streamlit",
                                session_id=session_id,
                                user_id=user_id,
                                patron_name=patron_name,
                                target_agent=target_bot_name,
                                total_duration_ms=elapsed_turn_ms,
                                prompt_length=len(prompt),
                                response_length=len(response_text),
                                artifacts_count=len(artifacts),
                                workflow_steps=usage.get("workflow_steps", 0),
                                input_tokens=usage.get("input_tokens"),
                                output_tokens=usage.get("output_tokens"),
                                total_tokens=usage.get("total_tokens"),
                                is_error=False,
                            )
                            record_agent_metric(
                                agent_name=target_bot_name,
                                duration_ms=elapsed_turn_ms,
                                turn_id=turn_id,
                                status="success",
                            )

                    except Exception as e:
                        elapsed_turn_ms = (time.perf_counter() - t0_turn) * 1000.0
                        response_text = f"⚠️ *Si è verificato un errore nello Scummbar*: {e}"
                        artifacts = []
                        record_turn_metric(
                            turn_id=turn_id,
                            channel="streamlit",
                            session_id=session_id,
                            user_id=user_id,
                            patron_name=patron_name,
                            target_agent=target_bot_name,
                            total_duration_ms=elapsed_turn_ms,
                            prompt_length=len(prompt),
                            is_error=True,
                            error_message=str(e),
                        )

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
                # Scope diary generation with the current turn context for metric correlation
                with log_context(channel="streamlit", session_id=session_id, user_id=user_id, agent_name="chronicler", turn_id=turn_id):
                    success, status_msg, _ = update_tavern_diary(patron_name, st.session_state.messages)
                if success:
                    st.toast("📜 Il tuo Diario di Bordo si è arricchito di un nuovo capitolo!", icon="📜")

    elif view == "📜 Diario di Bordo":
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
                    with log_context(channel="streamlit", session_id=session_id, user_id=user_id, agent_name="chronicler", turn_id=f"st:{session_id}:manual"):
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

    elif view == "📊 Metriche & Performance":
        # Metrics Cockpit view
        st.subheader("📊 Cockpit Osservabilità — Metriche & Performance")
        st.caption("Analisi delle latenze end-to-end, performance degli agenti, chiamate tool e consumi in tempo reale.")

        col_f1, col_f2 = st.columns([3, 1])
        with col_f1:
            channel_filter = st.selectbox(
                "Filtra Canale",
                options=["ALL", "streamlit", "telegram"],
                index=0,
                key="metrics_channel_selector",
            )
        with col_f2:
            st.write("")
            st.write("")
            if st.button("🔄 Ricarica Metriche", key="btn_refresh_metrics", use_container_width=True):
                st.rerun()

        # Top KPI Cards
        kpi = get_kpi_summary(channel_filter)
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                label="⏱️ Latenza Media Turno",
                value=f"{kpi['avg_turn_duration_ms']:.0f} ms" if kpi["total_turns"] > 0 else "N/D",
                delta=f"min: {kpi['min_turn_duration_ms']:.0f} ms / max: {kpi['max_turn_duration_ms']:.0f} ms" if kpi["total_turns"] > 0 else None,
                help="Tempo di risposta end-to-end registrato per iterazione utente.",
            )
        with m2:
            st.metric(
                label="💬 Turni Totali",
                value=str(kpi["total_turns"]),
                delta=f"{kpi['total_errors']} errori" if kpi["total_errors"] > 0 else "0 errori",
                delta_color="inverse" if kpi["total_errors"] > 0 else "normal",
                help="Numero totale di iterazioni conversazionali registrate.",
            )
        with m3:
            st.metric(
                label="🛠️ Esecuzioni Tool",
                value=str(kpi["total_tool_calls"]),
                delta=f"{kpi['tool_success_rate_pct']:.1f}% successo",
                help="Chiamate ai FunctionTool (ricette, tarocchi, mappe, memoria, RSS).",
            )
        with m4:
            st.metric(
                label="🖼️ Artefatti Prodotti",
                value=str(kpi["total_artifacts"]),
                help="Totale immagini (tarocchi/mappe) e pergamene .txt generate.",
            )

        st.markdown("---")

        # Two-Column Breakdown: Agents vs Tools
        col_agents, col_tools = st.columns(2)

        with col_agents:
            st.markdown("##### 🤖 Latenza Media per Agente (ms)")
            agents_data = get_agent_breakdown(channel_filter)
            if agents_data:
                chart_data = {row["target_agent"]: row["avg_latency_ms"] for row in agents_data}
                st.bar_chart(chart_data)
                # Formatted Table
                st.dataframe(
                    agents_data,
                    column_config={
                        "target_agent": "Agente",
                        "turn_count": "Turni",
                        "avg_latency_ms": "Media (ms)",
                        "min_latency_ms": "Min (ms)",
                        "max_latency_ms": "Max (ms)",
                    },
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("Nessuna metrica di agente ancora registrata.")

        with col_tools:
            st.markdown("##### 🛠️ Performance & Success Rate dei Tool")
            tools_data = get_tool_breakdown()
            if tools_data:
                tool_chart = {row["tool_name"]: row["avg_latency_ms"] for row in tools_data}
                st.bar_chart(tool_chart)
                st.dataframe(
                    tools_data,
                    column_config={
                        "tool_name": "Nome Tool",
                        "call_count": "Chiamate",
                        "avg_latency_ms": "Media (ms)",
                        "success_rate_pct": "% Successo",
                        "error_count": "Errori",
                    },
                    use_container_width=True,
                    hide_index=True,
                )
            else:
                st.info("Nessuna invocazione di tool ancora registrata.")

        st.markdown("---")

        # Latency Trend Time-Series
        st.markdown("##### 📈 Trend Latenza Ultimi Turni (ms)")
        ts_data = get_time_series_data(limit=50)
        if ts_data:
            latencies = [row["total_duration_ms"] for row in ts_data]
            st.line_chart(latencies)
        else:
            st.info("Dati cronologici insufficienti per il grafico.")

        # Detailed Recent Turns Log
        st.markdown("##### 📜 Registro Dettagliato degli Ultimi Turni")
        recent_turns = get_recent_turns(limit=25, channel_filter=channel_filter)
        if recent_turns:
            for t in recent_turns:
                status_icon = "❌" if t["is_error"] else "✅"
                channel_badge = "📱 Telegram" if t["channel"] == "telegram" else "💻 Streamlit"
                agent_name = t["target_agent"]
                duration = t["total_duration_ms"]
                ts = t["timestamp"]
                patron = t["patron_name"] or t["user_id"]
                tools_used = t.get("tools", [])

                with st.expander(
                    f"{status_icon} [{ts}] {channel_badge} — **{agent_name}** ({patron}) — ⏱️ {duration:.0f} ms ({len(tools_used)} tool)"
                ):
                    steps = t.get("workflow_steps", 0)
                    tokens_info = ""
                    if t.get("total_tokens") is not None:
                        tokens_info = (
                            f" | 🪙 Token: {t['input_tokens']} in / {t['output_tokens']} out / "
                            f"{t['total_tokens']} tot"
                        )
                    st.write(
                        f"**Turn ID**: `{t['turn_id']}` | **Prompt**: {t['prompt_length']} car. | "
                        f"**Risposta**: {t['response_length']} car. | **Artefatti**: {t['artifacts_count']} | "
                        f"**Step di lavoro**: {steps}{tokens_info}"
                    )
                    if t["is_error"] and t["error_message"]:
                        st.error(f"Errore: {t['error_message']}")

                    if tools_used:
                        st.markdown("**Tool eseguiti in questo turno:**")
                        for tool in tools_used:
                            t_icon = "✅" if tool["success"] else "❌"
                            art_info = f" (File: `{tool['artifact_filename']}`)" if tool.get("artifact_filename") else ""
                            st.caption(f"- {t_icon} `{tool['tool_name']}`: **{tool['duration_ms']:.1f} ms**{art_info}")
        else:
            st.info("Nessun turno registrato.")

    elif view == "🔍 Traces & Waterfall":
        # Distributed Traces & Waterfall Inspector view
        st.subheader("🔍 Traces & Waterfall Inspector")
        st.caption(
            "Esplora l'albero gerarchico dei trace a cascata (OpenTelemetry GenAI Spans): "
            "agenti, modelli, tool execution e latenze relative."
        )

        trace_turns = get_recent_trace_turns(limit=50)

        if not trace_turns:
            st.info(
                "Nessun trace OpenTelemetry ancora registrato. "
                "Invia un messaggio nella Taverna o su Telegram per osservare la cascata di esecuzione!"
            )
        else:
            turn_options = {}
            for t in trace_turns:
                badge = "📱 Telegram" if t["channel"] == "telegram" else "💻 Streamlit"
                agent_name = t["target_agent"]
                patron = t["patron_name"] or "Avventore"
                dur = t["total_duration_ms"]
                ts = t["timestamp"]
                spans_n = t["span_count"]
                status = "❌" if t["is_error"] else "✅"
                turn_options[t["turn_id"]] = (
                    f"{status} [{ts}] {badge} — {agent_name} ({patron}) — ⏱️ {dur:.0f} ms ({spans_n} spans)"
                )

            c_pick, c_btn = st.columns([4, 1])
            with c_pick:
                selected_turn_id = st.selectbox(
                    "Seleziona Turno da Ispezionare",
                    options=list(turn_options.keys()),
                    format_func=lambda tid: turn_options[tid],
                    key="trace_turn_selector",
                )
            with c_btn:
                st.write("")
                st.write("")
                if st.button("🔄 Aggiorna Trace", key="btn_refresh_trace", use_container_width=True):
                    st.rerun()

            if selected_turn_id:
                tree = get_turn_trace_tree(selected_turn_id)
                spans = tree.get("spans", [])

                # Header Overview Card
                st.markdown(
                    f'<div style="background-color: #1e1e2e; border: 1px solid #313244; border-radius: 8px; '
                    f'padding: 12px 18px; margin-bottom: 14px; font-family: monospace; font-size: 0.88em; color: #cdd6f4;">'
                    f'🆔 <strong>Trace ID:</strong> <code style="color: #fab387;">{tree.get("trace_id") or "N/D"}</code> | '
                    f'⏱️ <strong>Durata Totale:</strong> <strong style="color: #a6e3a1;">{tree.get("total_duration_ms"):.1f} ms</strong> | '
                    f'🌲 <strong>Spans:</strong> <strong style="color: #89b4fa;">{tree.get("span_count")}</strong>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

                # Waterfall Timeline Gantt Chart
                st.markdown("##### 📊 Timeline a Cascata (Waterfall Gantt)")
                waterfall_html = render_waterfall_html(tree)
                st.markdown(waterfall_html, unsafe_allow_html=True)

                st.markdown("---")

                # Detailed Span Inspector
                st.markdown("##### 🔎 Dettaglio & Metadati degli Span")
                for s in spans:
                    status_badge = "❌ ERROR" if s["status_code"] == "ERROR" else "✅ OK"
                    cat_label = s["category"].upper()

                    expander_label = (
                        f"{s['icon']} [{cat_label}] {s['name']} — ⏱️ {s['duration_ms']:.1f} ms "
                        f"(offset: {s['offset_ms']:.1f} ms, {status_badge})"
                    )

                    with st.expander(expander_label):
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            st.write(f"**Span ID**: `{s['span_id']}`")
                            st.write(f"**Parent ID**: `{s['parent_span_id'] or 'root'}`")
                        with c2:
                            st.write(f"**Inizio**: `{s['start_time_iso']}`")
                            st.write(f"**Durata**: **{s['duration_ms']:.1f} ms**")
                        with c3:
                            st.write(f"**Stato**: `{s['status_code']}`")
                            st.write(f"**Livello Albero**: `{s['depth']}`")

                        if s.get("attributes"):
                            st.markdown("**Attributi OpenTelemetry GenAI:**")
                            st.json(s["attributes"])

                        if s.get("events"):
                            st.markdown("**Eventi / Eccezioni nello Span:**")
                            st.json(s["events"])

    elif view == "🪵 Log di Sistema":
        # System Log Viewer (Terminal View)
        st.subheader("🪵 Registro di Bordo & Log di Sistema")
        st.caption("Visualizza i log operativi, errori e diagnostica in tempo reale.")

        available_files = get_available_log_files()

        # Controls Row
        c1, c2, c3, c4 = st.columns([2, 2, 2, 1])

        with c1:
            file_options = list(available_files.keys())
            default_index = file_options.index("app.log") if "app.log" in file_options else 0
            selected_file_name = st.selectbox(
                "File di Log",
                options=file_options,
                index=default_index,
                key="log_file_selector",
            )

        with c2:
            level_filter = st.selectbox(
                "Livello Minimo / Filtro",
                options=["ALL", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                index=0,
                key="log_level_filter",
            )

        with c3:
            max_lines = st.selectbox(
                "Righe da mostrare",
                options=[50, 100, 200, 500, 1000],
                index=2,  # default 200
                key="log_max_lines",
            )

        with c4:
            st.write("")  # Vertical spacing
            st.write("")
            if st.button("🔄 Aggiorna", key="btn_refresh_logs", use_container_width=True):
                st.rerun()

        # Search Query Bar
        search_query = st.text_input(
            "🔍 Filtra testo / Ricerca rapida nei log:",
            placeholder="es. balthazar, draw_nautical_map, error, patron...",
            key="log_search_query",
        )

        target_file_path = available_files.get(selected_file_name)
        if target_file_path and target_file_path.exists():
            log_lines = read_log_tail(
                target_file_path,
                max_lines=max_lines,
                level_filter=level_filter,
                search_query=search_query,
            )

            # Render styled dark monospace terminal
            terminal_html = render_logs_html(log_lines)
            st.markdown(terminal_html, unsafe_allow_html=True)

            st.caption(
                f"📁 File: `{target_file_path}` | Righe visualizzate: **{len(log_lines)}** | "
                f"Dimensione: **{target_file_path.stat().st_size / 1024:.1f} KB**"
            )
        else:
            st.warning("Nessun file di log trovato nella cartella `data/scummbar_chat/logs/`.")


if __name__ == "__main__":
    main()
