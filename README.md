# 🍺 ScummBar AI

> *"Here sabers rest, and stories float."*

A multi-bot interactive chat set in a Caribbean pirate tavern, built with **Google Agent Development Kit (ADK)** and integrated with **Telegram**.

This is a **study project** — no commercial purpose, just learning how to build multi-agent systems with AI.

---

## The Story

The **Scummbar** is a Caribbean pirate tavern. A place where tired sailors put down their swords, order a mug of grog, and sit down to listen.

Two characters run the bar:

| Character | Role | Personality |
|-----------|------|-------------|
| 🍺 **Barnaby** | Bartender | Always listening, knows the sea, makes unforgettable grogs |
| 🐱 **Barnacle** | The bar cat | Mysterious, solitary, speaks rarely — but when he does, it's worth hearing |

Both are AI-powered. Both have a story.

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

# Context compaction — always uses Gemini, requires Google ADC
COMPACTION_MODEL=gemini-3.5-flash   # model used for session summarization
COMPACTION_INTERVAL=30              # events before triggering compaction
COMPACTION_OVERLAP=2                # events retained after compaction

# Telegram (optional — only for Telegram integration)
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_BOT_USERNAME=your_bot_username
TELEGRAM_GROUP_LINK=https://t.me/your-group
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
help - Help and available commands
```

Then make the bot a **group admin** (for Barnacle's ephemeral messages).

#### How it works

- Users in a group mention `@barnaby` or `@barnacle`
- Only mentioned bots respond
- Barnaby replies publicly
- Barnacle replies with ephemeral messages (visible only to the requester)
- Private messages to the bot get an in-character redirect to the group
- One user at a time per bot (asyncio locks)

---

## Architecture

### Project Structure

```
src/scummbar_chat/
├── agent.py                 # Root agent (coordinator)
├── utils.py                 # Model factory, shared config, file loading
├── time_context.py          # Real-time → bar atmosphere mapping
├── tools.py                 # Placeholder shared tools
├── .env                     # Environment configuration
├── world/
│   └── scummbar.md          # World context + narrator rules
├── bots/
│   ├── barnaby/
│   │   ├── agent.py         # Barnaby agent + SkillToolset
│   │   └── persona.md       # Barnaby's personality prompt
│   └── barnacle/
│       ├── agent.py         # Barnacle agent
│       └── persona.md       # Barnacle's personality prompt
├── skills/                  # Auto-discovered ADK skills
│   ├── grog/SKILL.md        # Dynamic grog generation
│   └── menu/SKILL.md        # Menu: quick serve + recipes
└── telegram/                # Telegram adapter
    ├── adapter.py           # Long polling, @mention routing, locks, narrator
    ├── formatter.py         # ADK output → HTML for Telegram
    └── runner.py            # ADK Runner + compaction + session pruning

telegram_bot.py              # Telegram entry point
start.sh                     # ADK web + SQLite launcher
data/sessions.db             # SQLite session persistence (auto-created)
```

### Agent Hierarchy

```
root_agent (scummbar_chat)
├── global_instruction = InstructionProvider
│   └── WORLD_CONTEXT + get_time_description()
├── instruction = coordinator prompt
└── sub_agents:
    ├── barnaby → persona.md + SkillToolset (skills auto-discovery)
    └── barnacle → persona.md
```

The root agent never responds directly — it **delegates** to the appropriate sub-agent
based on a routing hint prepended to the message (`[Risponde BARNABY]` or `[Risponde BARNACLE]`).

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

### Telegram Adapter

```
src/scummbar_chat/telegram/
├── adapter.py    # Long polling, @barnaby/@barnacle detection, per-bot locks
├── formatter.py  # ADK output → HTML (3 formatting levels)
└── runner.py     # ADK Runner + DatabaseSessionService (SQLite)
```

**Message flow:**

```
User: @barnaby serve me a grog
        │
        ▼ (detect @mention → bot_name = "barnaby")
    asyncio.wait_for(lock.acquire(), timeout=15s)
        │
        ▼ (timeout → "Barnaby is busy...")
    message_counter[session] += 1
        │
        ▼ (every 3rd message → inject Narrator prompt)
    prepend routing hint: "[Risponde BARNABY] ..."
        │
        ▼
    ADK Runner → root_agent → barnaby_agent → response
        │
        ▼ (format response)
    Barnaby  → sendMessage(chat_id, formatted)          # public
    Barnacle → sendMessage(chat_id, formatted,          # ephemeral
                           receiver_user_id=user_id)
               fallback: public with 🐱 whisper note
```

**Text formatting (3 levels):**

| Pattern | Rendered As |
|---------|-------------|
| `Plain text` | `Plain text` (dialogue) |
| `*action*` | `<i>action</i>` (character narration) |
| `_full line_` | `<blockquote><i>...</i></blockquote>` (atmosphere) |

### Model Support

Switching models = **one line** in `.env`. A factory function in `utils.py` builds the correct
`BaseLlm` instance automatically based on the model name prefix.

| `LLM_MODEL` | Provider | Notes |
|-------------|----------|-------|
| `gemini-3.5-flash` | Vertex AI (Gemini) | Requires ADC + enabled Vertex AI API |
| `gemini-3.1-flash-lite` | Vertex AI (Gemini) | Faster, less powerful |
| `deepseek/deepseek-v4-flash` | DeepSeek via LiteLlm | Requires `DEEPSEEK_API_KEY` |
| `deepseek/deepseek-v4-pro` | DeepSeek via LiteLlm | More powerful, slower |

> **Note:** regardless of `LLM_MODEL`, context compaction always uses a dedicated Gemini model
> (`COMPACTION_MODEL`). Google ADC must be configured even when running DeepSeek.

### Session Persistence

Conversations persist across restarts via **SQLite** and `DatabaseSessionService`:

```bash
./start.sh  # Uses sqlite+aiosqlite:///data/sessions.db
```

Session mapping for Telegram: `session_id = chat_id`, `user_id = from.id`.

A background task runs hourly to prune events older than 24 hours, keeping the database lean.

---

### Context Compaction

Long conversations would eventually exceed the model's context window. To prevent this,
the runner uses ADK's **`App` + `EventsCompactionConfig` + `LlmEventSummarizer`** to
automatically summarize old dialogue in the background.

```
Conversation history
  event 1  ┌───────────────┐
  event 2  │ summarized  │─► compact summary (stored back in session)
  ...      │ by Gemini   │
  event 28 └───────────────┘
  event 29 ─► kept as active overlap
  event 30 ─► kept as active overlap  (COMPACTION_OVERLAP=2)
```

After every `COMPACTION_INTERVAL` events (default: 30), the older portion is replaced by
a concise summary. Only the last `COMPACTION_OVERLAP` events are preserved verbatim as
an active narrative bridge.

| Variable | Default | Description |
|----------|---------|-------------|
| `COMPACTION_MODEL` | `gemini-3.5-flash` | Gemini model used for summarization |
| `COMPACTION_INTERVAL` | `30` | Events before triggering compaction |
| `COMPACTION_OVERLAP` | `2` | Events kept verbatim after compaction |

> This feature uses ADK's `EventsCompactionConfig`, currently marked **experimental**.

---

## A Note

The entire project — code, architecture, documentation — was built with the active support of **Generative AI** (Claude by Anthropic), used as a development assistant throughout the process. That too is part of the study.

---

*Inspired by the Scumm Bar from Monkey Island. No affiliation with LucasArts.*
