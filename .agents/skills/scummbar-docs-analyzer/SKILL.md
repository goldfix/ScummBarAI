---
name: scummbar-docs-analyzer
description: Strumento per esplorare, leggere e cercare la documentazione tecnica (ADK, Gemini, DeepSeek, Telegram) nella cartella docs/.
---

# Scummbar Documentation Analyzer

La cartella `docs/` contiene tutta la documentazione ufficiale dei framework utilizzati in questo progetto (ADK, DeepSeek, Telegram, e Gemini Nano Images). 

Questo skill ti fornisce gli strumenti e i comandi per cercare informazioni all'interno della documentazione.

## Setup

Nessun setup necessario. Funziona "out of the box".

## Usage

Usa `bash` e `rg`/`grep` per esplorare la cartella `docs/`.

```bash
# Cerca un concetto in tutta la documentazione
rg "SessionService" docs/

# Lista tutti i file disponibili
find docs/ -type f -name "*.md"
```

## 📚 Indice della Documentazione ADK (`docs/`)

### 1. 🚀 Getting Started

| File | Contenuto |
|------|-----------|
| `Agent Development Kit.md` | Panoramica ADK: Agent, Tool, Session, Memory, Artifact, Event, Runner |
| `Python Quickstart for ADK.md` | Installazione, struttura progetto, `adk run`, `adk web` |
| `Build a multi-tool agent.md` | Tutorial completo con più tools |

---

### 2. 🤖 Agenti

| File | Contenuto |
|------|-----------|
| `Agents.md` | Tipi di agenti, quando usare workflow |
| `Simple agents with LlmAgent.md` | `name`, `description`, `model`, `instruction`, `tools`, `input_schema`, `output_schema`, `output_key`, `include_contents`, `global_instruction`, planner |
| `Managed agents.md` | `ManagedAgent` Google first-party |
| `Build agents with Agent Config.md` | Agenti via YAML (`adk create --type=config`) |
| `Build collaborative agent teams.md` | ADK 2.0+: modalità `chat`, `task`, `single_turn` |

**📌 Quando consultare:**
- Configurare `LlmAgent` → `Simple agents with LlmAgent.md`
- `global_instruction` e `InstructionProvider` → `Simple agents with LlmAgent.md` + `State- The Session's Scratchpad.md`

---

### 3. 🔧 Tools

| File | Contenuto |
|------|-----------|
| `Function tools.md` | `FunctionTool`, parametri, `LongRunningFunctionTool`, `AgentTool` |
| `Increase tool performance with parallel execution.md` | `async def` per tool paralleli |
| `Get action confirmation for ADK Tools.md` | Conferma utente: Boolean / Advanced / Remote |

---

### 4. 🧠 Contesto, Sessioni, Stato e Memoria

| File | Contenuto |
|------|-----------|
| `Conversational Context- Session, State, and Memory.md` | Session vs State vs Memory |
| `Context.md` | `InvocationContext`, `ReadonlyContext`, `CallbackContext`, `ToolContext` |
| `Session- Tracking individual conversations.md` | `SessionService`, `InMemorySessionService`, `DatabaseSessionService`, `VertexAiSessionService` |
| `State- The Session's Scratchpad.md` | Prefissi (`user:`, `app:`, `temp:`), `output_key`, `{key}` template, `InstructionProvider` |
| `Memory- Long-Term Knowledge with MemoryService.md` | `InMemoryMemoryService`, `VertexAiMemoryBankService`, `load_memory` |
| `Session database schema migration.md` | Migrazione schema DB (ADK Python v1.22.0) |

**📌 Quando consultare:**
- Session persistence (Telegram/Slack) → `Session- Tracking individual conversations.md` (DatabaseSessionService)
- `InstructionProvider` con state → `State- The Session's Scratchpad.md`

---

### 5. 📡 Events

| File | Contenuto |
|------|-----------|
| `Events.md` | Struttura eventi, `is_final_response()`, `state_delta`, `transfer_to_agent`, `escalate` |

---

### 6. 📦 Artifacts

| File | Contenuto |
|------|-----------|
| `Artifacts.md` | `ArtifactService`, `types.Part`, namespacing, versioning, `save_artifact`, `load_artifact` |

---

### 7. 🔄 Workflow e Multi-Agent

| File | Contenuto |
|------|-----------|
| `Workflows- multi-agent, multi-node applications.md` | Tipi workflow |
| `Sequential template workflow agent.md` | `SequentialAgent` |
| `Parallel template workflow agent.md` | `ParallelAgent` |
| `Loop template workflow agent.md` | `LoopAgent`, `max_iterations`, `escalate` |
| `Multi-agent workflow patterns.md` | Coordinator, Pipeline, Fan-out, Hierarchical, Human-in-the-loop |
| `Build collaborative agent teams.md` | Modalità collaborative ADK 2.0+ |

---

### 8. ⚙️ Runtime e Configurazione

| File | Contenuto |
|------|-----------|
| `Runtime Event Loop.md` | Event Loop, Runner, yield/pause/resume |
| `Runtime Configuration.md` | `RunConfig`: `streaming_mode`, `max_llm_calls` |
| `Agent activity logging.md` | Logging, OpenTelemetry, `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` |
| `Compress agent context for performance.md` | Context compaction: token-based, sliding window |
| `Context caching with Gemini.md` | Cache: `min_tokens`, `ttl_seconds`, `cache_intervals` |
| `Resume stopped agents.md` | `ResumabilityConfig`, resume via API/Runner |

**📌 Quando consultare:**
- Warning "System instructions modified" → usare `global_instruction` con parte statica comune
- Performance sessioni lunghe → `Compress agent context for performance.md`

---

### 9. 🛠️ Developer Tools

| File | Contenuto |
|------|-----------|
| `Use the Command Line.md` | `adk run`, `--save_session`, `--resume` |
| `Use the Web Interface.md` | `adk web`, `--port`, `--host`, `--reload` |
| `Use the API Server.md` | `adk api_server`, `/run`, `/run_sse`, Swagger su `/docs` |

---

### 10. 🌐 Models & Integrations

| File | Contenuto |
|------|-----------|
| `Google Gemini models for ADK agents.md` | Modelli, auth, Live API, retry 429 |
| `ai-google-dev-gemini-api-docs-whats-new-gemini-3-5.md` | **Gemini 3.5**: `thinking_level` (non `thinking_budget`), no temperature, 1M context |

#### 🖼️ Nano Banana / Image Generation (`docs/gemini-nano-img/`)

| File | Contenuto |
|------|-----------|
| `ai-google-dev-gemini-api-docs-image-generation.md` | Guida completa: text-to-image, image editing, multi-turn, video-to-image, aspect ratio, modelli disponibili |
| `ai-google-dev-gemini-api-docs-models-gemini-3-1-flash-image.md` | **Nano Banana 2** (`gemini-3.1-flash-image`): 1K-4K, Search Grounding, no Function calling, no Caching |
| `ai-google-dev-gemini-api-docs-models-gemini-3-1-flash-lite-i.md` | **Nano Banana 2 Lite** (`gemini-3.1-flash-lite-image`): sub-2s latency, Function calling ✅, Thinking ✅, 1K only |

**📌 Note sulla generazione di immagini (Google GenAI):**
- **Generazione Nativa Gemini**: Il tool utilizza direttamente l'API standard `client.models.generate_content` impostando `response_modalities=["IMAGE"]`, per generare immagini tramite i modelli della famiglia Gemini 3.1 Flash Image (es. `gemini-3.1-flash-lite-image`).
- **Rilevamento Formato Dinamico**: Il tool analizza l'intestazione dei byte generati (PNG o JPEG) per applicare l'estensione di file corretta (`.png` o `.jpg`) e il rispettivo MIME-type.
- **Integrazione API Key**: Il client viene inizializzato usando la configurazione standard di `google-genai`. Se nel `.env` è presente `GEMINI_API_KEY` (Google AI Studio), il tool si connette direttamente ad AI Studio.
- **Fallback PIL Robusto**: Se la generazione AI fallisce, interviene immediatamente il fallback PIL (`_draw_tarot_card_fallback`) che genera splendide carte dei tarocchi in-character in RAM (con dettagli di onde, stelle e lune), funzionante al 100% offline.

---

### 11. 🔌 A2A

| File | Contenuto |
|------|-----------|
| `Introduction to A2A.md` | Quando usarlo, `A2AServer`, `RemoteA2aAgent` |
| `Quickstart- Exposing a remote agent via A2A.md` | Esporre agente come servizio |
| `Quickstart- Consuming a remote agent via A2A.md` | Consumare agente remoto |

---

### 12. ✨ Skills

| File | Contenuto |
|------|-----------|
| `Skills for ADK agents.md` | `SkillToolset`, struttura `SKILL.md` (L1/L2/L3), `load_skill_from_dir`, inline vs filesystem |

---
