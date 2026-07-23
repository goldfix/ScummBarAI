# 🍺 ScummBar AI

> *"Here sabers rest, and stories float."*

A multi-bot interactive chat set in a Caribbean pirate tavern, built with **Google Agent Development Kit (ADK)** and integrated with **Telegram**.

This is a **study project** — no commercial purpose, just learning how to build multi-agent systems with AI.

---

## The Story

The **Scummbar** is a Caribbean pirate tavern. A place where tired sailors put down their swords, order a mug of grog, and sit down to listen.

Three characters run the bar:

| Character | Role | Personality |
|-----------|------|-------------|
| 🍺 **Barnaby** | Bartender | Always listening, knows the sea, makes unforgettable grogs |
| 🐱 **Barnacle** | The bar cat | Mysterious, solitary, speaks rarely — but when he does, it's worth hearing |
| 🔮 **Isolde** | Fortune Teller | Sitting in the shadow corner, she reads tarot cards and sees the unspoken truth |

All of them are AI-powered. All of them have a story.

---

## Getting Started

### Prerequisites

- Python 3.11+
- [Google Cloud ADC](https://cloud.google.com/docs/authentication/application-default-credentials) (for Gemini on Vertex AI)
- A [DeepSeek API key](https://platform.deepseek.com/api_keys) (optional, for DeepSeek models)

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/goldfix/ScummBarAI.git
cd ScummBarAI

# 2. Initialize the environment (creates py-env/, installs dependencies)
bash py_env.sh init_py

# 3. Activate it (each new terminal session)
bash py_env.sh active

# 4. Configure the environment
# Edit src/scummbar_chat/.env with your API keys and project settings
```

### Quick activate (existing environment)

```bash
bash py_env.sh active
```

### Environment File

Configure `src/scummbar_chat/.env`:

```env
# Google Cloud (for Gemini on Vertex AI + context compaction)
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=True

# Model selection — change this one line to switch providers
# Gemini:   LLM_MODEL=gemini-3.5-flash
# DeepSeek: LLM_MODEL=deepseek/deepseek-v4-flash
LLM_MODEL=gemini-3.5-flash
LLM_THINKING_LEVEL=medium

# DeepSeek (optional — only if using DeepSeek models)
DEEPSEEK_API_KEY=your-api-key-here
DEEPSEEK_REASONING_EFFORT=high

# Context compaction — default Gemini (requires ADC); can use DeepSeek with DEEPSEEK_API_KEY
COMPACTION_MODEL=gemini-3.5-flash   # model used for session summarization
COMPACTION_INTERVAL=30              # events before triggering compaction
COMPACTION_OVERLAP=2                # events retained after compaction

# Telegram (optional — only for Telegram integration)
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_BOT_USERNAME=your_bot_username
TELEGRAM_GROUP_LINK=https://t.me/your-group

# Image Generation (Isolde)
IMAGE_MODEL=gemini-3.1-flash-lite-image
# Optional: Google AI Studio API key to bypass Vertex AI for image generation
# GEMINI_API_KEY=your-api-key-here
```

---

## Running

### Web Interface (ADK Web)

```bash
# With SQLite persistence:
./start.sh

# Without persistence:
adk web src/

# Debug mode:
adk web src/ --log_level DEBUG
```

Open [http://localhost:8000](http://localhost:8000) to chat with the bots.

### Telegram Bot

Start the Telegram long-polling adapter:

```bash
python telegram_bot.py
```

#### BotFather Setup

On Telegram, chat with [@BotFather](https://t.me/botfather):

```
/newbot      → create your bot → get the token
/setprivacy  → Disable (so the bot sees all messages)
/setcommands → register commands:

start - Enter the Scummbar
grog - Order a special grog
menu - Check the galley
barnaby - Talk to the bartender
barnacle - Bother the cat
isolde - Seek a tarot vision from the shadow corner
help - Help and available commands
```

Then make the bot a **group admin** (for Barnacle's ephemeral messages).

#### How it works

- Users can engage bots via **@mention** (`@barnaby`, `@barnacle`, `@isolde`) or **keywords** (e.g. `grog`, `gatto`, `carte`)
- @mention always takes priority over keyword matching
- Barnaby and Isolde reply publicly in the group
- Barnacle replies with ephemeral messages (visible only to the requester)
- Private messages to the bot get an in-character redirect to the group
- One user at a time per bot (asyncio locks with 15s timeout)

---

## Architecture

### Project Structure

```
src/scummbar_chat/
├── agent.py                 # Root agent (coordinator)
├── utils.py                 # Model factory, shared config, file loading
├── time_context.py          # Real-time → bar atmosphere mapping
├── tools.py                 # FunctionTools: recall_patron_memory, memorize_patron_chat, write_secret_scroll_tool
├── .env                     # Environment configuration
├── world/
│   └── scummbar.md          # World context + narrator rules
├── bots/
│   ├── barnaby/
│   │   ├── agent.py         # Barnaby agent + SkillToolset + memory/artifact tools
│   │   └── persona.md       # Barnaby's personality prompt
│   ├── barnacle/
│   │   ├── agent.py         # Barnacle agent + recall_patron_tool
│   │   └── persona.md       # Barnacle's personality prompt
│   └── isolde/
│       ├── agent.py         # Isolde agent + recall_patron_tool + draw_tarot_card_tool
│       └── persona.md       # Isolde's personality prompt (mysterious tarot reader)
├── skills/                  # Auto-discovered ADK skills
│   ├── grog/SKILL.md        # Dynamic grog generation
│   └── menu/SKILL.md        # Menu: quick serve + recipes
└── telegram/                # Telegram adapter
    ├── adapter.py           # Long polling, semantic routing, per-bot locks, narrator
    ├── formatter.py         # ADK output → HTML for Telegram
    └── runner.py            # ADK Runner + compaction + session pruning

telegram_bot.py              # Telegram entry point (--debug flag, rotating logs)
start.sh                     # ADK web + SQLite launcher
data/sessions.db             # SQLite session persistence (auto-created)
data/logs/bot.log            # Rotating log — all levels (auto-created)
data/logs/errors.log         # Rotating log — WARNING+ only (auto-created)
```

### Agent Hierarchy

```
root_agent (scummbar_chat)
├── global_instruction = InstructionProvider
│   └── WORLD_CONTEXT + get_time_description()
├── instruction = coordinator prompt
└── sub_agents:
    ├── barnaby → persona.md + SkillToolset (skills auto-discovery)
    ├── barnacle → persona.md
    └── isolde → persona.md
```

The root agent never responds directly — it **delegates** to the appropriate sub-agent
based on a routing hint prepended to the message (`[Risponde BARNABY]`, `[Risponde BARNACLE]`, or `[Risponde ISOLDE]`).

### Time Context

`time_context.py` maps real time to six atmospheric moods in the bar:

| Time | Period | Vibe |
|------|--------|------|
| 07–09 | Dawn | Bar opens, quiet, first pink light |
| 09–12 | Morning | Bar wakes up, first customers |
| 12–14 | Noon | Peak activity, crowded counter |
| 14–16 | Afternoon | Post-lunch calm, Barnacle naps |
| 16–18 | Sunset | Golden light, candles lit |
| 18+ | Night | Bar never closes, candlelight |

The description is injected into every model call via `InstructionProvider`,
so the AI always knows the current bar atmosphere.

### Skills (Auto-Discovery)

Skills are modular prompt bundles loaded dynamically from the `skills/` directory.
**Adding a new skill = creating a new folder with an `SKILL.md` file** — zero code changes.

| Skill | Description |
|-------|-------------|
| `grog/` | Generates unique grogs based on user context, mood, and preferences |
| `menu/` | Level 1: quick dish serve. Level 2: real recipe in pirate jargon |

### Semantic Routing

Messages are routed to the right bot through `_resolve_intent()`, which applies two
priority levels in order:

1. **Explicit @ tag** — `@barnaby`, `@barnacle`, or `@isolde` in the message text (always wins)
2. **Keyword matching** — if no tag is found, the message is scanned against `_INTENT_MAP`

```python
_INTENT_MAP = {
    "barnaby":  ["barnaby", "barista", "grog", "birra", "bere", "drink", ...],
    "barnacle": ["barnacle", "micio", "gatto", "felino", "fusa", ...],
    "isolde":   ["isolde", "carte", "giocare", "gioco", "dadi", "tarocchi", "segreto", ...]
}
```

If neither matches, the message is silently ignored — bots don’t respond to
conversations not addressed to them.

Keywords are fully configurable: edit `_INTENT_MAP` in `adapter.py` to add or remove
trigger words without touching any other logic.

---

### Narrator System

Every **3rd message** in a group session, the adapter automatically appends a system
prompt to the bot’s input, asking it to add a short atmospheric description at the
end of its reply.

```
message 1: Barnaby replies normally
message 2: Barnaby replies normally
message 3: Barnaby replies + adds an ambient description in italics
message 4: Barnaby replies normally
...
```

The narrator description is formatted as a full `_cursive line_` (mapped to
`<blockquote><i>...</i></blockquote>` in Telegram HTML) so it visually stands apart
from dialogue.

Narrator rules and style guidelines live in `world/scummbar.md`, so the content can
be tuned without touching code.

---

### Telegram Adapter

```
src/scummbar_chat/telegram/
├── adapter.py    # Long polling, semantic routing, per-bot locks, narrator injection
├── formatter.py  # ADK output → HTML (3 formatting levels)
└── runner.py     # ADK Runner + compaction + session pruning
```

**Message flow:**

```
Incoming group message
        │
        ▼
  chat.type == "private"?
        │ yes → in-character redirect to group, stop
        ▼ no
  _resolve_intent(text)
        │ None → ignore (not addressed to any bot)
        ▼ bot_name
  asyncio.wait_for(lock.acquire(), timeout=15s)
        │ timeout → send "bot is busy" message, stop
        ▼ acquired
  sendChatAction(typing)
  message_counter[session] += 1
        │ counter % 3 == 0 → append Narrator system prompt
        ▼
  augmented = "[Risponde BOT_NAME] {text}"
  response  = run_agent(user_id, session_id, augmented)
  formatted = format_response(response)
        │
        ▼
  barnaby  → sendMessage(chat_id, HTML)                    # public
  barnacle → sendMessage(chat_id, HTML, receiver=user_id)  # ephemeral
             fallback: public + 🐱 whisper note if not admin
        │
  finally → lock.release()
```

**Text formatting (3 levels):**

| Pattern in agent output | Telegram rendering |
|-------------------------|--------------------|
| `Plain text` | plain text (dialogue) |
| `*action text*` | `<i>action text</i>` (character narration) |
| `_full line_` | `<blockquote><i>full line</i></blockquote>` (atmosphere) |

---

### Model Support

Switching models = **one line** in `.env`. A factory function in `utils.py` builds the
correct `BaseLlm` instance automatically based on the model name prefix.

| `LLM_MODEL` | Provider | Notes |
|-------------|----------|-------|
| `gemini-3.5-flash` | Vertex AI (Gemini) | Requires ADC + enabled Vertex AI API |
| `gemini-3.1-flash-lite` | Vertex AI (Gemini) | Faster, less powerful |
| `deepseek/deepseek-v4-flash` | DeepSeek via LiteLlm | Requires `DEEPSEEK_API_KEY` |
| `deepseek/deepseek-v4-pro` | DeepSeek via LiteLlm | More powerful, slower |

---

### Context & Memory Management

Managing context across long conversations is one of the core technical challenges
this project explores. Four mechanisms work together:

#### 1. Time-Aware Context (`time_context.py`)

The `global_instruction` is an **`InstructionProvider`** — a function called at every
model invocation that injects the current bar atmosphere alongside the world context.

```
global_instruction = WORLD_CONTEXT + get_time_description()
                                            ↑
                               updates every hour automatically
```

This means the AI always knows whether the bar is quiet at dawn or packed at noon,
without storing this in the session.

#### 2. Session Persistence (SQLite)

Conversations are stored in a local SQLite database via ADK’s `DatabaseSessionService`.
Each Telegram group maps to a single shared session (`session_id = chat_id`), so all
patrons in the group share the same conversation history.

```bash
./start.sh  # Uses sqlite+aiosqlite:///data/sessions.db
```

A background task runs **hourly** to delete events older than 24 hours, keeping the
database from growing unbounded.

#### 3. Context Compaction (`runner.py`)

Long sessions would eventually exceed the model’s context window. To prevent this,
the runner wraps the ADK agent in an **`App`** with `EventsCompactionConfig`:

```
Conversation history (events)
  ┌────────────────────────────┐
  │  events 1 → 28        │─►  replaced by a compact summary
  │  (summarized by LLM)  │    generated by COMPACTION_MODEL
  └────────────────────────────┘
  events 29–30  ─►  kept verbatim as narrative overlap
```

After every `COMPACTION_INTERVAL` events (default: 30), the older portion is replaced
by a summary. The last `COMPACTION_OVERLAP` events are kept verbatim as a bridge.

| Variable | Default | Description |
|----------|---------|-------------|
| `COMPACTION_MODEL` | `gemini-3.5-flash` | Model used for summarization |
| `COMPACTION_INTERVAL` | `30` | Events before compaction triggers |
| `COMPACTION_OVERLAP` | `2` | Events kept verbatim after compaction |

`COMPACTION_MODEL` supports both Gemini (requires ADC) and DeepSeek (requires
`DEEPSEEK_API_KEY`). It is independent from `LLM_MODEL`.

> `EventsCompactionConfig` is currently marked **experimental** by ADK.

#### 4. Patron Memory (`tools.py` + `patron_memories`)

Barnaby and Barnacle remember patrons across sessions using two ADK `FunctionTool`s
that read and write a dedicated SQLite table.

```
 patron_memories
 ┌───────────┬────────────┬────────────┬───────────────────┬─────────────────┐
 │ user_id   │ patron_name │ core_traits │ last_chat_summary  │ last_interaction │
 └───────────┴────────────┴────────────┴───────────────────┴─────────────────┘
   ↑ PK
   Telegram user ID (numeric)
```

A key design choice: the `user_id` is **never passed as an LLM parameter** —
the model could hallucinate it. Instead, ADK injects the real Telegram user ID
automatically via `ToolContext`:

```python
async def recall_patron_memory(tool_context: ToolContext) -> dict:
    user_id = tool_context.user_id  # ← real Telegram ID from the ADK session
```

The table is created automatically on first use (`CREATE TABLE IF NOT EXISTS`).

#### 5. Artifact & Media Delivery (`InMemoryArtifactService`, `write_secret_scroll`, `draw_tarot_card`)

To support tangible digital handovers (like "Secret Recipes", "Treasure Maps", or "Tarot Card Visions"), we configured ADK's `InMemoryArtifactService` on the Runner.

Depending on the mime type/extension, artifacts are delivered dynamically to Telegram:

##### A. Text-Based Scrolls (Barnaby's Bartending Recipes / Maps)
1. Barnaby calls the `write_secret_scroll` tool supplying `title` and `content`.
2. The file is saved as an ADK Artifact (`types.Part.from_bytes` under `text/plain`).
3. `runner.py` intercepts `event.actions.artifact_delta` during execution and extracts the raw bytes.
4. `adapter.py` streams the file to Telegram as a downloadable attachment using the native `sendDocument` API:
   ```python
   # Streams from RAM as multipart/form-data
   await _send_document(http, chat_id, filename, file_bytes)
   ```

##### B. Visual Images (Isolde's Mystic Tarot Card Visions)
1. Isolde calls the `draw_tarot_card` tool supplying a `card_name` and a visual `scene_description`.
2. The tool attempts to generate an AI image using the Google GenAI SDK. If `GEMINI_API_KEY` is provided in `.env`, the client will automatically authenticate and generate high-quality AI images.
3. **Robust Fallback**: If the AI model fails or is blocked by network/security issues, the tool gracefully falls back to generating a beautiful, custom-drawn in-character tarot card `.png` in-memory using **Pillow**.
4. The file is saved as a `.png` or `.jpg` artifact (automatically detected from the bytes) and intercepted.
5. `adapter.py` detects the extension and uploads it as an inline, beautifully rendered chat photo using the Telegram `sendPhoto` API:
   ```python
   # Renders inline in the chat
   await _send_photo(http, chat_id, filename, file_bytes)
   ```

All models are fully parameterized. All settings (e.g. `IMAGE_MODEL` and the API key) are configured centrally in `.env`. No cloud storage or Google GCS buckets are used, making the artifact generation fast, secure, and entirely locally-contained.

---

## A Note

The project — code and documentation — was built with the active support of **Generative AI** (Claude by Anthropic), used as a development assistant throughout the process. That too is part of the study.

---

*Inspired by the Scumm Bar from Monkey Island. No affiliation with LucasArts.*
