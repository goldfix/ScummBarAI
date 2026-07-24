# 🍺 ScummBar AI — A Collaborative Multi-Agent Study Project

> *"Where sabers rest, stories float, and agents run the bar."*

Welcome to the **Scummbar AI**! This is an open-source, hands-on **study repository** designed to teach developers how to build, orchestrate, and maintain a complex, multi-agent conversational application using the **Google Agent Development Kit (ADK)**, Gemini, and DeepSeek, integrated directly into **Telegram**.

Instead of a dry reference manual, this documentation is structured **didactically** to guide you through the architectural decisions, the code design, and the modern AI-assisted workflows used to build and evolve this project.

---

## 🗺️ Table of Contents
1. [📖 The Story & The Characters](#-the-story--the-characters)
2. [🚀 Quick Start (Run First, Learn Later)](#-quick-start-run-first-learn-later)
3. [🏗️ Architectural Blueprint & Technical Choices](#️-architectural-blueprint--technical-choices)
4. [🤖 AI-Assisted Development: The Pi-Agent Autopilot](#-ai-assisted-development-the-pi-agent-autopilot)

---

## 📖 The Story & The Characters

The **Scummbar** is a legendary Caribbean pirate tavern. It is a shared Telegram group session where multiple AI-powered characters live, listen, and interact with patrons in real-time.

| Character | Role | Didactic Purpose | Personality Vibe |
|-----------|------|------------------|------------------|
| 🍺 **Barnaby** | Bartender | Demonstrates **Tool Calling** (Memory Read/Write, Text Artifact generation) and ADK **Skills Auto-Discovery** | Empathetic, quiet, knows every pirate's secret, mixes unforgettable custom grogs. |
| 🐱 **Barnacle** | Tavern Cat | Demonstrates **Read-Only Shared Memory** and **Ephemeral Telegram Messaging** (whispering to specific users) | Crotchety, speaks rarely, sleeps on ammo crates, dislikes loud patrons. |
| 🔮 **Isolde** | Fortune Teller | Demonstrates **Independent Multi-Auth Routing** and **Multimodal Image Generation** (native Gemini 3.1 Flash Image + Pillow PIL fallback) | Criptic, majestic, sits in the Shadow Corner, extracts mystical tarot cards. |

---

## 🚀 Quick Start (Run First, Learn Later)

Follow these steps to get the Scummbar running on your local machine or Telegram group in minutes.

### 1. Prerequisites
- Python 3.11+
- A Google Gemini API Key (from [Google AI Studio](https://aistudio.google.com/)) OR a Google Cloud Service Account (Vertex AI).
- A Telegram Bot Token from [@BotFather](https://t.me/botfather) (optional, for Telegram delivery).

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/goldfix/ScummBarAI.git
cd ScummBarAI

# Initialize and create the virtual environment
bash py_env.sh init_py

# Activate the environment
source py-env/bin/activate  # or: bash py_env.sh active
```

### 3. Environment Configuration
Copy `.env.example` or create a file named `src/scummbar_chat/.env`. This file is divided into **6 logical sections** based on purpose:

```env
# ===========================================================================
# 🔐 SECTION 1: CORE GEMINI AUTHENTICATION (Chat & Compaction Auth)
# ===========================================================================
# Choose ONE of the two options (A or B) and comment out the other.

# --- OPTION A: Google AI Studio (API Key) — Simple, no GCP project needed ---
GEMINI_API_KEY=your-api-key-here

# --- OPTION B: Vertex AI / Google Cloud (Service Account) — GCP Enterprise ---
# GOOGLE_CLOUD_PROJECT=your-gcp-project-id
# GOOGLE_CLOUD_LOCATION=global
# GOOGLE_GENAI_USE_VERTEXAI=True
# GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/key.json

# ===========================================================================
# 💬 SECTION 2: CHAT CONVERSATION (Core LLM Settings)
# ===========================================================================
LLM_MODEL=gemini-3.1-flash-lite
LLM_THINKING_LEVEL=medium

# ===========================================================================
# 🗜️ SECTION 3: CONTEXT COMPACTION (Compression Settings)
# ===========================================================================
# Summarization settings (inherits credentials automatically from Section 1)
COMPACTION_MODEL=gemini-3.5-flash
COMPACTION_INTERVAL=30
COMPACTION_OVERLAP=2

# ===========================================================================
# 🔮 SECTION 4: IMAGE GENERATION (Isolde Settings & INDEPENDENT AUTH)
# ===========================================================================
# Isolde's Tarot model and its FULLY INDEPENDENT, isolated authentication.
IMAGE_MODEL=gemini-3.1-flash-lite-image

# --- OPTION A: Google AI Studio (Dedicated API Key for Images) ---
IMAGE_GEMINI_API_KEY=your-dedicated-image-api-key-here

# --- OPTION B: Vertex AI / Google Cloud (Dedicated Service Account for Images) ---
# IMAGE_GOOGLE_CLOUD_PROJECT=another-gcp-project-id
# IMAGE_GOOGLE_CLOUD_LOCATION=europe-west1
# IMAGE_GOOGLE_GENAI_USE_VERTEXAI=True
# IMAGE_GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/another-key.json

# ===========================================================================
# 🧠 SECTION 5: DEEPSEEK PROVIDER OVERRIDES (Optional)
# ===========================================================================
DEEPSEEK_API_KEY=your-deepseek-api-key-here
DEEPSEEK_REASONING_EFFORT=high

# ===========================================================================
# 📡 SECTION 6: TELEGRAM INTEGRATION (Optional)
# ===========================================================================
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_BOT_USERNAME=your_bot_username
TELEGRAM_GROUP_LINK=https://t.me/your-group-link
```

### 4. Running the Tavern

#### Option A: Web Interface (ADK Web)
Perfect for rapid testing and prototyping.
```bash
./start.sh  # Launches with persistent SQLite session tracking
```
Open `http://localhost:8000` to chat with the coordinator and characters in your browser.

#### Option B: Telegram Bot (Group Delivery)
```bash
python telegram_bot.py --debug
```

---

## 🏗️ Architectural Blueprint & Technical Choices

The Scummbar is designed around clean software engineering and multi-agent patterns. Here is how the system is organized:

### 1. Collaborative Multi-Agent Coordination
Instead of a single monolith prompt, the Scummbar uses a **Hierarchical Router-Delegate** pattern using Google ADK's `root_agent` and `sub_agents`.

```
                    [Telegram / Web Input]
                              │
                              ▼
                        [root_agent]
                    (Shared Coordinator)
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
    [Barnaby]             [Barnacle]            [Isolde]
 (The Bartender)         (The Tavern Cat)    (The Fortune Teller)
  - Memory read/write     - Read-only Memory   - Independent Auth
  - Auto-discovered       - Ephemeral replies  - Gemini Nano Image
    Skills (Grog/Menu)                           generation tool
```

*   **How routing works**: In `src/scummbar_chat/telegram/adapter.py`, the function `_resolve_intent()` applies two priority levels:
    1.  **Explicit Mention**: `@barnaby`, `@barnacle`, `@isolde` (always wins).
    2.  **Semantic Keyword Matching**: The message is scanned against `_INTENT_MAP` (e.g., `grog` routes to Barnaby, `tarocchi` or `carte` to Isolde).
*   **Routing Prefix**: Once resolved, the router prepends `[Risponde NAME]` to the text, which instructs the coordinator (`root_agent`) to route the call to the corresponding sub-agent.

### 2. Core Architectural Choices

#### A. Centralized Temporal World Context (InstructionProvider)
To create an immersive atmosphere, the bar never closes but changes its mood in real-time. In `src/scummbar_chat/time_context.py`, the day is split into 6 periods (Dawn, Noon, Sunset, Night, etc.).
*   **The Choice**: Instead of passing the world description statically, we use ADK's `global_instruction` bound to an **`InstructionProvider`** function. This dynamically updates the bar's description *at every model turn* based on the actual system hour.
*   **Why**: This is cache-friendly for Gemini and ensures the agents always know if it's sunset or dawn without manual prompt editing.

#### B. SQLite Session Persistence & Database Compaction
All group chats are mapped to a single persistent SQLite database (`data/sessions.db`) via ADK's `DatabaseSessionService`.
*   **Context Compaction**: As history grows, the context window fills up. We configured an automated, LLM-based compaction scheme (`EventsCompactionConfig` + `LlmEventSummarizer`):
    *   After every **30 events**, the older portion of the conversation is replaced by an LLM-generated summary (`COMPACTION_MODEL`).
    *   The last **2 events** are kept verbatim to maintain immediate conversational context.

#### C. Smart Dual-Authentication & Isolation
One of the key technical highlights of this repository is how authentication is parameterized:
*   **The Problem**: The standard Google GenAI SDK throws a fatal error if you supply both an API Key and Vertex AI variables globally in the environment (they are mutually exclusive).
*   **The Solution**: We built `get_gemini_client_kwargs(prefix="")` in `utils.py`.
    *   If `GEMINI_API_KEY` is present, it forces `vertexai=False` and programmatically overrides `project=None` and `location=None`, shielding the client from environment pollution.
    *   If `prefix="IMAGE_"` is specified, it isolates the **Image Generation** auth entirely, allowing Isolde to run on a separate billing project, key, or Vertex regional project without affecting Chat/Compaction!
    *   **Thread Safety**: For Vertex AI Service Accounts, we load the JSON directly as an in-memory `Credentials` object rather than mutating `os.environ` globally, ensuring perfect safety during async concurrent loops.

#### D. Tangible Media Delivery (Artifacts)
We wanted the agents to be able to "hand over" items to players:
*   **Barnaby's Scrolls**: Generates recipes as `.txt` files using ADK's `InMemoryArtifactService` via the `write_secret_scroll` tool. Delivered as downloadable Telegram documents.
*   **Isolde's Tarot Images**: Uses `draw_tarot_card` tool via Gemini's native `response_modalities=["IMAGE"]` or a customized **Pillow (PIL) local rendering fallback** if the API is offline. Automatically detects the file format (PNG vs. JPEG) via byte headers and delivers it as an inline native photo via `/sendPhoto`.

---

## 🤖 AI-Assisted Development: The Pi-Agent Autopilot

This repository was designed to be developed, refactored, and maintained **collaboratively with an AI coding assistant (Pi-Agent)**.

To achieve this, we configured a specialized autonomous system directly in the codebase using **Agent Skills**.

```
                           [.agents/skills/]
                                   │
         ┌─────────────────────────┴─────────────────────────┐
         ▼                                                   ▼
[scummbar-docs-analyzer]                            [scummbar-memory-updater]
  - Progressive disclosure of docs                    - Automated logging rules
  - Offloads docs index from prompt                   - Roadmap state compiler
  - Handles multi-directory searches                  - Markdown fence validator
```

### 1. What is an Agent Skill?
A Pi-Agent skill is a self-contained, capability package located in `.agents/skills/`. At startup, Pi-Agent scans this directory and learns about the available capabilities via the skill's description. The full instructions are kept separate and loaded **on-demand** when the skill is called.

This implements **Progressive Disclosure**: it keeps the AI's initial context window incredibly clean, saving tokens, speeding up response times, and maximizing the LLM's reasoning focus.

### 2. Our Customized Skills

#### A. Documentation Analyzer (`/skill:scummbar-docs-analyzer`)
-   **Why**: The `docs/` folder contains dozens of framework guides. Storing their indexes in the main developer instructions (`AGENTS.md` or `MEMORY.md`) wasted thousands of tokens.
-   **What it does**: This skill encapsulates the entire documentation index. When the AI needs to understand an ADK concept (like *Memory Bank* or *Workflow Loops*), it invokes this skill, parses the local index, uses `rg` or `find` to find the exact markdown file under `docs/`, and reads it.

#### B. Memory & Documentation Updater (`/skill:scummbar-memory-updater`)
-   **Why**: Keeping architectural decisions (`MEMORY.md`), developer guides (`AGENTS.md`), and public manuals (`README.md`) synchronized across dozens of commits is extremely error-prone for humans and AIs alike.
-   **What it does**: Standardizes how the AI must document changes. It enforces rules on how to append session logs, update the roadmap, register design decisions, and includes an automated Python validator to ensure no markdown code blocks are left open or broken.

### 3. How to Use the Autopilot (For Developers)
If you are developing this repository using Pi-Agent, you can invoke these skills directly:

```bash
# Explore framework documentation in the docs/ folder
/skill:scummbar-docs-analyzer search "compaction"

# Update memory, roadmap, and check markdown health after a refactoring
/skill:scummbar-memory-updater log_changes
```

By combining Google ADK for multi-agent execution and Pi-Agent Skills for autonomous workspace organization, this repository stands as a **state-of-the-art template for modern, AI-collaborative software engineering**.

---

![scummbar](scummbar.png)

---

*Inspired by the Scumm Bar from Monkey Island. Built for learning and study purposes. No commercial affiliation.*
