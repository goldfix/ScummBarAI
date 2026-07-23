# MEMORY.md — Memoria del Progetto Scummbar

> Questo file è la **memoria viva** del progetto: storia, decisioni, stato corrente, roadmap e attività aperte.
> Viene aggiornato ad ogni sessione di lavoro significativa.
> Gli agenti AI devono leggerlo prima di qualsiasi attività (vedi `AGENTS.md`).

---

## 🍺 STATO DEL PROGETTO (aggiornato: 2026-07-21)

### Cos'è Scummbar
Chat interattiva multi-bot ambientata in una taverna piratesca caraibica.
I partecipanti includono bot gestiti da AI (Barnaby il barista, Barnacle il gatto, Isolde la veggente).
Sviluppato con **Google ADK 2.4.0** + **Gemini / DeepSeek** via Vertex AI / LiteLlm.
Integrazione Telegram: **completata** ✅.

---

### 📁 Struttura del Progetto

```
scummbar/
├── docs/                              # Documentazione (ADK, DeepSeek, Telegram)
│   ├── *.md                           # Documentazione ADK (53 file)
│   ├── deepseek/                      # Documentazione DeepSeek API (5 file)
│   ├── gemini-nano-img/               # Documentazione Nano Banana / image generation (3 file)
│   └── telegram/                      # Documentazione Telegram Bot API (4 file)
├── src/
│   └── scummbar_chat/                 # ← progetto attivo
│       ├── __init__.py
│       ├── agent.py                   # root agent + InstructionProvider temporale
│       ├── utils.py                   # config condivisa, model factory (_build_model_instance), load_md(), load_all_skills()
│       ├── time_context.py            # mappatura orario reale → momento del giorno
│       ├── tools.py                   # FunctionTool: recall, memorize, write_secret_scroll, draw_tarot_card
│       ├── .env                       # config ambiente (NON committare)
│       ├── world/
│       │   └── scummbar.md            # world context + regole narrazione + logica Narratore
│       ├── bots/
│       │   ├── __init__.py            # esporta barnaby_agent, barnacle_agent, isolde_agent
│       │   ├── barnaby/
│       │   │   ├── agent.py           # LlmAgent Barnaby + SkillToolset + memory tools
│       │   │   └── persona.md         # chi è Barnaby, come parla
│       │   ├── barnacle/
│       │   │   ├── agent.py           # LlmAgent Barnacle + recall_patron_memory tool
│       │   │   └── persona.md         # chi è Barnacle, come si comporta
│       │   └── isolde/
│       │       ├── agent.py           # LlmAgent Isolde + recall_patron_memory + draw_tarot_card_tool
│       │       └── persona.md         # chi è Isolde, veggente dell'Angolo Oscuro
│       ├── skills/                    # Skills ADK (auto-discovery)
│       │   ├── grog/
│       │   │   └── SKILL.md           # skill dinamica: genera grog unici per contesto
│       │   └── menu/
│       │       └── SKILL.md           # skill menu: livello 1 rapido + livello 2 ricetta
│       └── telegram/                  # Adapter Telegram
│           ├── __init__.py
│           ├── adapter.py             # long polling, semantic routing, lock+timeout, Narratore
│           ├── formatter.py           # ADK output → HTML Telegram (3 livelli)
│           └── runner.py              # ADK Runner + DatabaseSessionService + compaction + session pruning
├── data/
│   ├── sessions.db                    # SQLite persistence (creato automaticamente)
│   └── logs/                          # Log rotativi (creati automaticamente)
│       ├── bot.log                    # tutti i livelli — 5 MB × 3 file
│       └── errors.log                 # WARNING+ — 2 MB × 2 file
├── start.sh                           # avvio ADK web con persistenza SQLite
├── py_env.sh                          # setup ambiente Python (venv + poetry)
├── telegram_bot.py                    # avvio bot Telegram (--debug flag, log su file)
├── requirements.txt                   # bootstrap: poetry + uv
├── pyproject.toml                     # dipendenze progetto
├── AGENTS.md                          # istruzioni per agenti AI
├── MEMORY.md                          # questo file — memoria del progetto
└── ruff.toml
```

---

### ⚙️ Configurazione Tecnica

**File `.env`** (`src/scummbar_chat/.env`):
```env
# Google Cloud (per Gemini + compaction)
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=True
# GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json # Decommenta per Service Account in prod

# Modello attivo (cambia solo questa riga per switchare)
# Gemini:   LLM_MODEL=gemini-3.5-flash
# DeepSeek: LLM_MODEL=deepseek/deepseek-v4-flash
LLM_MODEL=deepseek/deepseek-v4-flash
LLM_THINKING_LEVEL=medium

# DeepSeek
DEEPSEEK_API_KEY=...                    # da platform.deepseek.com/api_keys
DEEPSEEK_REASONING_EFFORT=high          # high | max

# Context Compaction (default Gemini, requires ADC; oppure deepseek/... con DEEPSEEK_API_KEY)
COMPACTION_MODEL=gemini-3.5-flash       # modello usato per i riassunti
COMPACTION_INTERVAL=30                  # eventi prima di triggerare la compaction
COMPACTION_OVERLAP=2                    # eventi di overlap mantenuti dopo la compaction

# Telegram
TELEGRAM_BOT_TOKEN=...                  # da BotFather
TELEGRAM_BOT_USERNAME=scummbar_bot      # senza @
TELEGRAM_GROUP_LINK=https://t.me/...   # mostrato nel redirect dai DM
```

**Auth Google**: Due opzioni disponibili:
1. **Sviluppo (ADC)**: eseguire `gcloud auth application-default login`
   - Account: `your-account@example.com`
2. **Produzione (Service Account)**: impostare `GOOGLE_APPLICATION_CREDENTIALS` nel file `.env`
   - Es. `GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json`

**Requisiti GCP**:
- Progetto: `your-gcp-project-id` (Vertex AI + Gemini 3.5 abilitati)
- Location: `global` (necessaria per `gemini-3.5-flash`)
- ⚠️ Verificare che Vertex AI API sia abilitata sul progetto GCP

**Dipendenze** (`pyproject.toml`):
```
google-adk[db]==2.4.0   litellm      aiohttp
greenlet                orjson       python-dotenv
```

**Avvio**:
```bash
# Setup iniziale (prima volta)
bash py_env.sh init_py

# Attiva ambiente (ogni nuova sessione)
bash py_env.sh active

# Avvio
./start.sh                              # avvio con SQLite persistence
adk web src/                            # avvio senza persistence (InMemory)
adk web src/ --log_level DEBUG          # debug verboso

# Telegram
python telegram_bot.py                  # avvio normale
python telegram_bot.py --debug          # log DEBUG su console + file
```

---

### 🤖 Architettura Agenti

```
root_agent  (scummbar_chat)
├── global_instruction = _world_instruction_provider()   ← funzione, aggiornata ad ogni turno
│     └── WORLD_CONTEXT + get_time_description()         ← world context + momento del giorno
├── instruction = COORDINATOR_INSTRUCTION
└── sub_agents:
    ├── barnaby   → instruction = persona.md + tools=[SkillToolset]
    └── barnacle  → instruction = persona.md
```

### Sistema Narratore (`scummbar.md` + `adapter.py`)

Ogni **3 messaggi** nel gruppo, l'adapter inietta automaticamente una nota di sistema al bot attivo,
chiedendogli di aggiungere una descrizione d'ambiente in corsivo alla fine della risposta.

**Logica in `adapter.py`:**
```python
_message_counters[session_id] += 1
if _message_counters[session_id] % 3 == 0:
    augmented += "\n\n[NOTA DI SISTEMA: È il momento del Narratore...]"
```

**Regole del Narratore (in `scummbar.md`):**
- Frequenza: ~ogni 3 messaggi nel canale
- Formattazione: sempre in corsivo (`_testo_`) per distinguersi dai dialoghi
- Stile: evocativo, sensoriale (suoni, odori, luci, azioni fisiche dei personaggi)
- Tipologie: dettagli ambiente, azioni di Barnaby, stranezze di Barnacle

---

### 🧭 Semantic Routing (`adapter.py`)

`_resolve_intent(text)` sostituisce il vecchio `_detect_bot`. Usa due livelli di priorità:

1. **@mention esplicita** — `@barnacle` o `@barnaby` nel testo (sempre prioritaria)
2. **Keyword matching** — se non c'è @mention, cerca parole chiave in `_INTENT_MAP`

```python
_INTENT_MAP = {
    "barnaby": ["barnaby", "barista", "grog", "birra", "bere", "drink", ...],
    "barnacle": ["barnacle", "micio", "gatto", "felino", "fusa", ...]
}
```

Se nessun pattern corrisponde, il messaggio viene ignorato (nessun bot risponde).

**Keyword** — estendibili direttamente in `_INTENT_MAP` senza toccare la logica.

---

### 🧠 Memoria Avventori (`tools.py` + `patron_memories`)

Barnaby, Barnacle e Isolde ricordano i clienti tra una sessione e l'altra grazie a due
`FunctionTool` ADK che leggono/scrivono su una tabella SQLite dedicata.

**Schema tabella `patron_memories`:**

```sql
CREATE TABLE IF NOT EXISTS patron_memories (
    user_id           TEXT PRIMARY KEY,   -- Telegram user ID (numerico)
    patron_name       TEXT,               -- nome del pirata
    core_traits       TEXT,               -- tratti separati da ' | '
    last_chat_summary TEXT,               -- riassunto ultima chat (max 300 chars)
    last_interaction  DATETIME            -- timestamp UTC ultimo aggiornamento
)
```

**Tool disponibili:**

| Tool | Chi lo usa | Quando |
|------|-----------|--------|
| `recall_patron_memory` | Barnaby + Barnacle + Isolde | All'inizio di ogni interazione |
| `memorize_patron_chat` | Barnaby | A fine conversazione o su rivelazione biografica |
| `draw_tarot_card` | Isolde | Per proiettare visioni / tarocchi (genera immagini con fallback PIL) |

**`user_id` affidabile via `ToolContext`:**

Il `user_id` Telegram (numerico) non viene mai passato come parametro LLM
— l'LLM potrebbe inventarlo. ADK lo inietta automaticamente via `ToolContext`:

```python
async def recall_patron_memory(tool_context: ToolContext) -> dict:
    user_id = tool_context.user_id   # ← Telegram ID reale, dalla sessione ADK
    ...
```

Il messaggio augmentato include anche `[avventore_id: {user_id}]` come
contesto visivo per il personaggio, ma i tool non lo leggono da lì.

**La tabella viene creata automaticamente** al primo utilizzo di qualsiasi tool
tramite `_ensure_patron_memories_table()` (`CREATE TABLE IF NOT EXISTS`).

---

### 🟡 Logging e gestione errori (`telegram_bot.py` + `adapter.py`)

**`telegram_bot.py`** è ora un entry point robusto con:
- `--debug` flag: attiva livello DEBUG su console e file
- `_check_env()`: pre-flight al boot — verifica token, logga modello e path
- Log rotativi su `data/logs/bot.log` (5 MB × 3) e `data/logs/errors.log` (2 MB × 2)
- `_dump_exception()`: scrive traceback completo con timestamp in caso di crash
- Exit code `1` su errore fatale

**`adapter.py`** ora cattura eccezioni a tutti i livelli:
- `_handle_update` wrappa `_handle_update_inner` con `try/except + log.exception()`
- `_on_task_done` callback: logga eccezioni dai task asyncio
- `gather` finale al shutdown: logga eccezioni residue
- `_session_cleaner_cron`: usa `log.exception()` invece di `log.error()`

Tutti gli errori a livello WARNING+ finiscono in `data/logs/errors.log`.

```bash
python telegram_bot.py           # INFO su console, tutto su bot.log
python telegram_bot.py --debug   # DEBUG su console, tutto su bot.log
```

Invece di attendere indefinitamente il lock, viene usato `asyncio.wait_for` con timeout di 15 secondi.
Se il lock non si libera entro 15s, l'utente riceve il messaggio "è occupato".

```python
try:
    await asyncio.wait_for(lock.acquire(), timeout=15.0)
except asyncio.TimeoutError:
    await _send_message(http, chat_id, _BOT_BUSY[bot_name])
    return
```

---

### 🧹 Session Pruning (`runner.py` + `adapter.py`)

`runner.py` espone `purge_old_sessions(hours=24)` che rimuove eventi SQLite più vecchi di X ore.
`adapter.py` avvia un background cron (`_session_cleaner_cron`) ogni ora al lancio del bot.

```python
# runner.py — DELETE diretta sulla tabella 'events' di ADK
cursor.execute("DELETE FROM events WHERE timestamp < ?", (cutoff_str,))

# adapter.py — cron ogni 3600s
asyncio.create_task(_session_cleaner_cron())
```

⚠️ **Nota tecnica**: la DELETE usa lo schema interno di ADK (`events` table). Se ADK cambia
lo schema in future versioni, la query può fallire con `sqlite3.OperationalError` — già gestita
con try/except e log.

---

### 🕐 Contesto Temporale (`time_context.py`)

Mappa l'orario reale ai momenti della giornata nello Scummbar:

| Orario | Momento | Atmosfera |
|--------|---------|-----------|
| 07-09 | Alba | Bar che apre, silenzio, prima luce rosata |
| 09-12 | Mattino | Bar si sveglia, primi clienti |
| 12-14 | Mezzogiorno | Massima attività, ressa al bancone |
| 14-16 | Pomeriggio | Calma post-pranzo, Barnacle sonnecchia |
| 16-18 | Tramonto | Luce dorata, candele accese |
| 18-∞ | Notte | Bar mai chiuso, candele, pirati notturni |

Funzioni esposte: `get_time_description()`, `get_current_period()`

---

### 🎯 Skills ADK — Auto-discovery

**Come funziona**: Barnaby scansiona automaticamente `skills/` e carica tutte le cartelle con `SKILL.md`.

```python
# utils.py — load_all_skills()
# Scansiona skills/ → carica ogni cartella con SKILL.md → niente codice da modificare
```

**Aggiungere una nuova skill:**
```bash
mkdir src/scummbar_chat/skills/nuova-skill
# creare src/scummbar_chat/skills/nuova-skill/SKILL.md
# riavviare adk web → skill disponibile automaticamente
```

**Skill attive:**

| Skill | Contenuto |
|-------|-----------|
| `grog/` | Generazione dinamica grog: Barnaby legge il contesto dell'utente e crea un grog unico con nome evocativo, ingredienti contestuali e rituale di preparazione. |
| `menu/` | Menu cambusa: Livello 1 (risposta rapida con piatto) + Livello 2 (ricetta reale in gergo piratesco). |

**Formato `SKILL.md`** (ADK Skills spec):
```markdown
---
name: nome-skill
description: Descrizione breve per la discovery (L1)
---

# Titolo

Istruzioni per l'agente (L2) — tutto self-contained, no references
```

---

### 🔄 Switch Modello

Cambiare modello = **una riga nel `.env`**:

| `LLM_MODEL` | Provider | Note |
|-------------|----------|------|
| `gemini-3.5-flash` | Vertex AI | Richiede ADC + progetto abilitato |
| `gemini-3.1-flash-lite` | Vertex AI | Più veloce, meno potente |
| `deepseek/deepseek-v4-flash` | DeepSeek via LiteLlm | Richiede `DEEPSEEK_API_KEY` |
| `deepseek/deepseek-v4-pro` | DeepSeek via LiteLlm | Più potente |

`utils.py` espone un **factory `_build_model_instance(model_name, is_main_model)`** che restituisce
il corretto `BaseLlm` in base al prefisso del modello:
- `deepseek/...` → `LiteLlm(thinking=enabled, reasoning_effort=high)` (solo per main model)
- qualsiasi altro → `Gemini(model=...)`

Variabili esportate:
- `MODEL` — istanza per gli agenti (Barnaby, Barnacle, root)
- `COMPACTION_LLM` — istanza dedicata al riassunto sessioni (default Gemini, configurabile)
- `THINKING_CONFIG` — `GenerateContentConfig` per Gemini, `None` per DeepSeek

---

### 💾 Session Persistence (SQLite)

```bash
./start.sh   # equivale a:
adk web src/ --session_service_uri "sqlite+aiosqlite:///$(pwd)/data/sessions.db"
```

`SESSION_DB_URI` disponibile in `utils.py` per uso programmatico.

---

### 🧹 Context Compaction (`runner.py`)

Per evitare che le sessioni lunghe facciano crescere il context window all'infinito,
`runner.py` usa `App` + `EventsCompactionConfig` + `LlmEventSummarizer` di ADK.

Dopo ogni `COMPACTION_INTERVAL` eventi, ADK riassume automaticamente la conversazione
passata con un modello Gemini dedicato, mantenendo solo gli ultimi `COMPACTION_OVERLAP`
eventi come contesto attivo.

```python
# runner.py — schema semplificato
compaction_summarizer = LlmEventSummarizer(llm=COMPACTION_LLM)
compaction_config = EventsCompactionConfig(
    compaction_interval=COMPACTION_INTERVAL,  # default: 30
    overlap_size=COMPACTION_OVERLAP,          # default: 2
    summarizer=compaction_summarizer,
)
scummbar_app = App(
    name=APP_NAME,
    root_agent=root_agent,
    events_compaction_config=compaction_config,
)
_runner = Runner(app=scummbar_app, session_service=_session_service)
```

⚠️ **Note importanti:**
- `EventsCompactionConfig` è marcata **[EXPERIMENTAL]** da ADK — può cambiare senza preavviso
- `COMPACTION_LLM` usa di default `gemini-3.5-flash` — richiede **Google ADC**
- Può essere configurata su DeepSeek (`COMPACTION_MODEL=deepseek/...`) — richiede `DEEPSEEK_API_KEY`
- I valori di default (interval=30, overlap=2) sono configurabili nel `.env`

---

### 📝 File Markdown da gestire (contenuti)

| File | Chi lo gestisce | Stato |
|------|----------------|-------|
| `world/scummbar.md` | Utente | ✅ completo — include regole Narratore |
| `bots/barnaby/persona.md` | Utente | ✅ completo |
| `bots/barnacle/persona.md` | Utente | ✅ completo |
| `skills/grog/SKILL.md` | Utente | ✅ completo |
| `skills/menu/SKILL.md` | Utente | ✅ completo |

**⚠️ Regola**: i prompt sono canale-agnostici (nessun riferimento a Telegram).

---

### 🗺️ Roadmap

| Fase | Stato | Note |
|------|-------|------|
| Setup ambiente + struttura | ✅ | ADK 2.4, py-env pulito |
| World context (`scummbar.md`) | ✅ | Atmosfera, regole, geografia, narrazione |
| Persona Barnaby | ✅ | Completa |
| Persona Barnacle | ✅ | Completa |
| InstructionProvider temporale | ✅ | 6 fasce orarie, bar mai chiuso |
| global_instruction (cache fix) | ✅ | Risolto "System instructions modified" warning |
| Skills auto-discovery | ✅ | `load_all_skills()` in utils.py |
| Skill grog dinamico | ✅ | Barnaby crea grog unici per contesto |
| Skill menu | ✅ | Livello 1 rapido + Livello 2 ricetta reale |
| Session persistence (SQLite) | ✅ | `DatabaseSessionService` + `start.sh` |
| Switch modello via .env | ✅ | Gemini e DeepSeek supportati |
| DeepSeek thinking | ✅ | `LiteLlm(reasoning_effort=high)` |
| Primo test `adk web` | ✅ | Funzionante |
| Integrazione Telegram | ✅ | Adapter aiohttp: polling, routing @mention, lock+timeout, ephemeral |
| Sistema Narratore | ✅ | Ogni 3 messaggi, iniezione prompt descrizione ambientale |
| Session pruning (24h) | ✅ | `purge_old_sessions()` + cron orario |
| Lock con timeout (15s) | ✅ | `asyncio.wait_for` invece di wait indefinito |
| Context Compaction (LLM-based) | ✅ | `App` + `EventsCompactionConfig` + `LlmEventSummarizer` |
| Semantic routing | ✅ | `_resolve_intent()`: @mention + keyword matching via `_INTENT_MAP` |
| Memoria avventori | ✅ | `patron_memories` SQLite + `recall_patron_memory` + `memorize_patron_chat` |
| Artefatti e Pergamene | ✅ | `InMemoryArtifactService` + `write_secret_scroll` + `sendDocument` |
| Logging verboso + error export | ✅ | `--debug`, `bot.log`, `errors.log`, `_dump_exception()` |
| Nuove skills | 🔲 | Aggiungere cartelle in `skills/` |
| Integrazione Slack | 🔲 | Future |
| Webhook Telegram (vs long polling) | 🔲 | Per deployment su server pubblico |
| Supporto duale autenticazione (Service Account ↔ API Key) | 🔲 | Permettere al bot di funzionare in modo flessibile sia con Service Account GCP che con classica GEMINI_API_KEY per tutti i modelli (conversazione, compaction, tools) |
| Autenticazione Gemini via Service Account | ✅ | `.env` + `GOOGLE_APPLICATION_CREDENTIALS`; pre-flight check in `telegram_bot.py` |
| Reorganizzazione docs AI (`AGENTS.md` + `MEMORY.md`) | ✅ | `CLAUDE.md` sostituito; memoria e istruzioni separate |
| Sistema Pi-Agent Skills (`scummbar-*`) | ✅ | Introduzione di skill per progressive disclosure documentale |
| Unificazione API Immagini | ✅ | Deprecato branch Imagen, architettura unificata su `generate_content` Gemini Nano |

---

### 💡 Decisioni architetturali

- **Progressive Disclosure tramite Pi-Agent Skills**: Le istruzioni gravose per l'Agente AI (come l'esplorazione dei manuali o l'aggiornamento strutturato del progetto) sono incapsulate in skill specifiche (`scummbar-docs-analyzer`, `scummbar-memory-updater`). L'indice documentale è stato migrato dentro la skill dell'analyzer. Questo svuota il system prompt base (`AGENTS.md` e `MEMORY.md`), riducendo il consumo di token e migliorando il focus dell'LLM.
- **Unificazione API Immagini**: Abbiamo deprecato il branch "Imagen" per l'estrazione dei Tarocchi, uniformando tutto al metodo moderno `generate_content` di Gemini 3.1 Flash Image. Questo azzera il debito tecnico legato alle regioni Vertex AI (`IMAGE_LOCATION`) e supporta nativamente l'auth duale (Service Account e API Key).
- **Lingua Mista (Code vs Prompts)**: Tutti i commenti tecnici in Python e la documentazione del codice (`#` o `"""`) sono in **Inglese** (per mantenere lo standard di sviluppo). I messaggi di ritorno dei tools per l'LLM e i file Markdown dei prompt sono in **Italiano** (perché fanno parte dell'input/output del modello).
- **Prompt in Markdown** — editabili senza toccare codice
- **`global_instruction` = InstructionProvider** — world context + orario aggiornato ad ogni turno, cachabile da Gemini
- **Ogni bot ha solo la sua `persona.md`** — world context arriva via global_instruction
- **Skills auto-discovery** — aggiungere skill = creare cartella, zero codice
- **Skill = self-contained** — no references directory, tutto nel SKILL.md
- **Prompt canale-agnostici** — nessun riferimento a Telegram nei file markdown
- **`LLM_MODEL` generico** (non `GEMINI_MODEL`) — supporta sia Gemini che DeepSeek
- **`_build_model_instance()` factory** in `utils.py` — restituisce `BaseLlm` corretto dal prefisso del modello
- **`MODEL` vs `COMPACTION_LLM`** — istanze separate: conversazione vs riassunto sessioni
- **`COMPACTION_LLM`** — segue `COMPACTION_MODEL` nel `.env`; default `gemini-3.5-flash` (richiede ADC); supporta anche DeepSeek
- **`thinking_level=medium`** / **`reasoning_effort=high`** per Gemini/DeepSeek
- **`include_thoughts=False`** / filtro `part.thought=True` — reasoning rimane interno
- **`location=global`** per `gemini-3.5-flash` su Vertex AI
- **Context Compaction** — `App` + `EventsCompactionConfig` [EXPERIMENTAL] + `LlmEventSummarizer`; usa `COMPACTION_LLM` (default Gemini, configurabile)
- **Telegram adapter**: solo `aiohttp` (già installato), nessuna libreria aggiuntiva
- **Session mapping**: `session_id = chat_id` (storia condivisa del gruppo), `user_id = from.id`
- **Barnacle ephemeral**: richiede bot admin nel gruppo; fallback pubblico con nota `🐱` se non admin
- **Narratore via injection**: ogni 3 messaggi, `adapter.py` aggiunge prompt di sistema al testo
- **Lock timeout 15s**: `asyncio.wait_for(lock.acquire(), timeout=15)` invece di wait indefinito
- **Session pruning 24h**: `purge_old_sessions()` + cron orario — mantiene il DB pulito
- **`drop_params=True`** in `LiteLlm` — ignora parametri non supportati da DeepSeek
- **Semantic routing**: `_resolve_intent()` — @mention con priorità, poi keyword matching; keywords estendibili in `_INTENT_MAP`
- **Memoria avventori**: `patron_memories` SQLite; `user_id` da `ToolContext` (mai dall'LLM) — impossibile inventarlo
- **Gestione Artefatti (Pergamene)**: `InMemoryArtifactService` abilitato nel Runner; `write_secret_scroll` genera file di testo in memoria; l'adapter intercetta `artifact_delta` ed esegue l'upload diretto su Telegram via `sendDocument` usando `aiohttp.FormData` multipart.
- **`_augment_text` con `avventore_id`**: inietta `[avventore_id: {user_id}]` nel testo — contesto visivo per il personaggio
- **Logging su file**: `data/logs/bot.log` + `data/logs/errors.log` (rotativi); `--debug` flag
- **Error propagation**: `_handle_update` wrappa con `try/except`, `_on_task_done` callback, `gather` finale logga residui
- **Autenticazione Gemini**: supporta sia ADC (`gcloud auth application-default login`) sia Service Account (`GOOGLE_APPLICATION_CREDENTIALS` nel `.env`); l'SDK `google-auth` li risolve automaticamente all'avvio
- **Pre-flight check Service Account**: `telegram_bot.py` verifica l'esistenza del file JSON al boot e si arresta con errore esplicito se mancante
- **`AGENTS.md` + `MEMORY.md`**: sostituiscono `CLAUDE.md`; `AGENTS.md` = istruzioni operative per agenti AI; `MEMORY.md` = memoria e storia del progetto

---

## 📱 Telegram — Integrazione

### Documentazione disponibile (`docs/telegram/`)

#### `Bots- An introduction for developers.md` (145 righe)
| Sezione | Contenuto |
|---------|-----------|
| How Do Bots Work | Architettura: bot → Bot API server → Telegram API |
| How Are Bots Different | Nessun "last seen", storage limitato, non possono iniziare conversazioni, privacy mode |
| How Do I Create a Bot | BotFather, token (es. `4839574812:AAFD39kkdpWt3ywyRZergyOLMaJhac60qc`) |

#### `From BotFather to 'Hello World'.md` (679 righe)
| Sezione | Contenuto |
|---------|-----------|
| Obtain Your Bot Token | `/newbot` su BotFather, formato token |
| Creating a Bot Class | Long polling con `TelegramLongPollingBot` (Java, pattern identico in Python) |
| Receiving Messages | `update.getMessage()`, `update.getMessage().getFrom()` |
| Sending Messages | `sendMessage(chat_id, text)` |
| Echo Bot | Copia messaggio in risposta |
| Commands | `/scream`, `/whisper` — `msg.isCommand()`, `msg.getText()` |
| Buttons & Keyboards | `InlineKeyboardMarkup`, `CallbackQuery`, `callbackData` |
| Database | SQLite per persistenza |
| Hosting | VPS, packaging, deploy |

#### `Telegram Bot Features.md` (854 righe)
| Sezione | Riga | Contenuto |
|---------|------|-----------|
| Commands | 55 | `/keyword`, max 32 chars, scopes per utente/gruppo |
| Global Commands | 116 | `/start`, `/help`, `/settings` obbligatori |
| Keyboards (Reply) | 86 | `ReplyKeyboardMarkup` — sostituisce tastiera con opzioni predefinite |
| Inline Keyboards | 98 | `InlineKeyboardMarkup` — pulsanti sotto il messaggio |
| Menu Button | 108 | Pulsante menù vicino al campo testo |
| Ephemeral Messages | 211 | **Messaggi privati in gruppo**: visibili solo a un utente + bot |
| Privacy Mode | 649 | **Default ON**: bot vede solo comandi e reply dirette |
| Advanced Formatting | 592 | MarkdownV2, HTML, Rich Messages |
| Rich Messages | 603 | Streaming AI replies, headings, tables, code, LaTeX |
| Regular Messages | 622 | MarkdownV2 e HTML per testo semplice |
| Bot-to-Bot | 405 | Comunicazione tra bot (con Bot-to-Bot Mode abilitata) |
| Guest Bots | 460 | Bot risponde in chat dove non è membro (via @menzione) |
| BotFather | 760 | Comandi: `/newbot`, `/setcommands`, `/setprivacy`, `/token` |

#### `Telegram Bot API.md` (14177 righe — riferimento completo)
| Sezione | Riga | Contenuto |
|---------|------|-----------|
| **Autorizzazione** | 139 | `Authorization: Bearer {TOKEN}` in ogni richiesta |
| **Making Requests** | 143 | `https://api.telegram.org/bot{TOKEN}/{method}` |
| **getUpdates** | 283 | Long polling: `offset`, `limit`, `timeout`, `allowed_updates` |
| **setWebhook** | 311 | Webhook HTTPS per produzione, `secret_token` |
| **Update object** | 193 | Struttura update: `update_id`, `message`, `callback_query`... |
| **User object** | 413 | `id`, `first_name`, `username`, `language_code` |
| **Chat object** | 475 | `id`, `type` (private/group/supergroup/channel) |
| **Message object** | 674 | `message_id`, `from`, `chat`, `text`, `entities`... |
| **sendMessage** | 5572 | Invia testo: `chat_id`, `text`, `parse_mode`, `reply_markup` |
| **Formatting options** | 5648 | MarkdownV2 e HTML: regole di escaping complete |
| **MarkdownV2 syntax** | 5680 | Bold, italic, code, links, blockquote + **regole escaping** |
| **HTML syntax** | 5730 | Tag HTML supportati (`<b>`, `<i>`, `<code>`, `<blockquote>`) |
| **Ephemeral Messages** | 5801 | API: `receiver_user_id`, `callback_query_id`, 15s window |
| **sendChatAction** | 7396 | "sta scrivendo...": `typing`, `upload_photo`, ecc. |
| **sendRichMessage** | 10747 | Rich messages strutturate |
| **sendRichMessageDraft** | 10803 | **Streaming AI replies** — invia risposta progressivamente |
| **Rich Markdown syntax** | 10416 | GFM + headings, tables, LaTeX, media blocks |
| **Rich HTML syntax** | 10580 | Tag HTML estesi per rich messages |

---

### Concetti chiave per l'integrazione

**URL base**: `https://api.telegram.org/bot{TOKEN}/{method}`

**Oggetti fondamentali:**
```
Update
  └─ message
       ├─ from (User)  → id, username, first_name
       ├─ chat (Chat)  → id, type (private/group)
       └─ text         → testo del messaggio
```

**Session mapping ADK ← Telegram:**
```python
session_id = str(update["message"]["chat"]["id"])  # per chat
user_id    = str(update["message"]["from"]["id"])   # per utente
```

**Implementazione senza librerie (aiohttp):**
```python
BASE = f"https://api.telegram.org/bot{TOKEN}"

# Long polling
async with session.get(f"{BASE}/getUpdates?offset={offset}&timeout=30") as r:
    updates = (await r.json())["result"]

# "sta scrivendo..."
await session.post(f"{BASE}/sendChatAction",
    json={"chat_id": chat_id, "action": "typing"})

# Invia messaggio (HTML più semplice di MarkdownV2)
await session.post(f"{BASE}/sendMessage",
    json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
```

---

### Formatting: MarkdownV2 vs HTML (riga 5648 Bot API)

**MarkdownV2** (riga 5680) — ⚠️ caratteri da escapare con `\`:
```
_ * [ ] ( ) ~ ` > # + - = | { } . !
```

**HTML** (riga 5730) — consigliato per la narrazione ambientale:
```html
<b>grassetto</b>   <i>corsivo</i>   <code>codice</code>
<blockquote>citazione</blockquote>
```
Con HTML si escapano solo `<` → `&lt;`, `>` → `&gt;`, `&` → `&amp;`

---

### Privacy Mode (riga 649 Features — cruciale per i gruppi)

Default ON: bot in gruppo vede solo comandi, reply dirette, @menzioni.

**Soluzioni per Scummbar:**
- **A)** Disabilitare via BotFather (`/setprivacy`) — bot vede tutto
- **B)** Usare comandi `/barnaby` o `/barnacle`
- **C)** Aggiungere il bot come admin del gruppo

---

### Ephemeral Messages (riga 5801 Bot API)

Messaggi visibili solo al destinatario nel gruppo:
```python
await send_message(
    chat_id=chat_id,
    text="Solo tu puoi leggere questo...",
    receiver_user_id=user_id,
    callback_query_id=query_id   # entro 15 secondi
)
```

---

### Comandi da registrare su BotFather

```
/start    - Entra nello Scummbar
/grog     - Ordina un grog speciale
/menu     - Consulta la cambusa
/barnaby  - Parla con il barista
/barnacle - Disturba il gatto
/help     - Aiuto e comandi disponibili
```

---

### Adapter Telegram — Architettura implementata

```
src/scummbar_chat/telegram/
├── adapter.py    # long polling, routing @mention, lock per bot, ephemeral
├── formatter.py  # ADK output → HTML Telegram (3 livelli)
├── runner.py     # ADK Runner + DatabaseSessionService
└── __init__.py

telegram_bot.py   # entry point: python telegram_bot.py
```

**Avvio bot Telegram:**
```bash
source py-env/bin/activate
python telegram_bot.py
```

**Flusso messaggi:**
```
messaggio gruppo
    │
    ▼
chat.type == "private"? → redirect in-character al gruppo
    │
    ▼
bot_name = _resolve_intent(text)   # @mention prima, poi keyword matching
    se None → ignora (nessun bot coinvolto)
    │
asyncio.wait_for(lock.acquire(), timeout=15s)
    errore timeout → "è occupato..."
    │
sendChatAction(typing)
    │
_message_counters[session_id] += 1
    se counter % 3 == 0 → aggiunge nota Narratore al testo
    │
augmented = "[Risponde BARNABY/BARNACLE] [avventore_id: {user_id}] {text}"
response, files = run_agent(user_id, session_id=chat_id, augmented)
formatted = format_response(response)
    │
barnaby  → sendMessage(chat_id, formatted)           # pubblico
         → sendDocument(chat_id, file.bytes)         # per ogni file generato
barnacle → sendMessage(chat_id, formatted,           # ephemeral
                       receiver_user_id=user_id)     # solo per te
          fallback pubblico se bot non è admin
    │
finally: lock.release()  # sempre, anche in caso di errore
```

**Formattazione HTML (3 livelli):**

| Pattern nel testo ADK | Resa Telegram |
|-----------------------|---------------|
| Testo normale | testo normale (dialogo) |
| `*azione*` | `<i>azione</i>` (narrazione personaggio) |
| `_riga intera_` | `<blockquote><i>testo</i></blockquote>` (ambientazione) |

**Config `.env` necessaria:**
```env
TELEGRAM_BOT_TOKEN=token-da-botfather
TELEGRAM_BOT_USERNAME=nome_bot_senza_@
TELEGRAM_GROUP_LINK=https://t.me/nome-gruppo
```

**Ephemeral Messages (Barnacle):**
- Richiedono che il bot sia **admin del gruppo**
- Senza admin: fallback risposta pubblica con nota `🐱 (sussurro — solo per te)`
- Per rendere il bot admin: gruppo → Amministratori → Aggiungi → seleziona bot

---

### 🔗 Problemi Comuni Telegram

| Problema | Soluzione |
|----------|-----------|
| Bot non risponde nel gruppo | Privacy Mode ON (riga 649) → disabilitare o usare @menzione |
| Errore parsing MarkdownV2 | Usa HTML — molto più semplice |
| MarkdownV2: caratteri da escapare | `_ * [ ] ( ) ~ \` > # + - = \| { } . !` con `\` |
| Token non funziona | `/token` su BotFather per rigenerare |
| Aggiornamenti duplicati | Aggiornare sempre `offset = update_id + 1` |
| getUpdates e webhook insieme | Non possono coesistere — uno alla volta |

---

## 🤖 DeepSeek — Integrazione con ADK

### Documentazione disponibile (`docs/deepseek/`)

| File | Contenuto |
|------|-----------|
| `api-docs-deepseek-com.md` | Quick start, modelli disponibili, chiamata API (OpenAI-compatible) |
| `api-docs-deepseek-com-guides-thinking-mode.md` | Thinking mode: toggle, effort control, multi-turn, tool calls |
| `api-docs-deepseek-com-guides-kv-cache.md` | Context caching su disco: automatico, regole di hit, `prompt_cache_hit_tokens` |
| `markdown-1784208769971.md` | Multi-round conversation: API stateless, concatenazione history, gestita automaticamente da ADK |
| `api-docs-deepseek-com-quick-start-error-codes.md` | Codici di errore (400, 401, 402, 422, 429, 500, 503) |
| `medium-com-yusuf4iaty-integrating-deepseek-with-google-adk-a.md` | Custom `BaseLlm` adapter per ADK Java (pattern riutilizzabile in Python) |

---

### Modelli disponibili

| Modello | Note |
|---------|------|
| `deepseek-v4-flash` | Veloce, economico — equivalente di gemini-flash |
| `deepseek-v4-pro` | Più potente — equivalente di gemini-pro |
| `deepseek-chat` | ⚠️ Deprecato il 2026/07/24 (→ usa `deepseek-v4-flash`) |
| `deepseek-reasoner` | ⚠️ Deprecato il 2026/07/24 (→ usa `deepseek-v4-pro` con thinking) |

---

### Configurazione API

```env
# .env — per usare DeepSeek al posto di Gemini
DEEPSEEK_API_KEY=la-tua-key  # da platform.deepseek.com/api_keys
LLM_MODEL=deepseek/deepseek-v4-flash
```

L'API è **OpenAI-compatible** → si usa l'SDK `openai` con `base_url` personalizzato.
In ADK si usa `LiteLlm` che gestisce tutto automaticamente.

---

### Thinking mode

| Parametro | Valore | Note |
|-----------|--------|------|
| `thinking` | `{"type": "enabled"}` | Default: enabled |
| `reasoning_effort` | `high` / `max` | Default: `high`; `low`/`medium` → mappati a `high` |
| `temperature`, `top_p` | — | **Non supportati** in thinking mode (ignorati silenziosamente) |
| `reasoning_content` | campo risposta | Contiene la CoT; **da ripassare** all'API se ci sono tool calls |

---

### Multi-round Conversation

L'API DeepSeek `/chat/completions` è **stateless** — il server non memorizza la cronologia.
Ad ogni request bisogna passare **tutta la history** precedente.

⚠️ **Nessun impatto sul codice**: ADK gestisce automaticamente la concatenazione della history
tramite il `SessionService`. DeepSeek riceve la storia completa ad ogni turno
esattamente come si aspetta.

**Sinergia con KV Cache**: dato che ogni request include la history completa,
il prefisso comune (system prompt + history) viene cachato automaticamente → meno token addebitati.

---

### Context Caching (KV Cache)

DeepSeek ha un sistema di caching su disco **abilitato di default**, senza modifiche al codice.

**Rilevanza per Scummbar:**
- Il `WORLD_CONTEXT` (statico, ~5.7k chars) sarà cachato dopo le prime richieste → riduce latenza e costo
- La `time_description` cambia ogni ora → possibili cache miss al cambio fascia oraria

**Verifica hit nella risposta:**
```python
response.usage.prompt_cache_hit_tokens    # token serviti dalla cache
response.usage.prompt_cache_miss_tokens   # token calcolati ex novo
```

---

### Differenze chiave vs Gemini

| Aspetto | Gemini 3.x | DeepSeek |
|---------|-----------|----------|
| SDK | `google-genai` | `openai` (compatible) via LiteLlm |
| Auth | ADC / Vertex AI | `DEEPSEEK_API_KEY` |
| Thinking | `thinking_level: medium` | `reasoning_effort: high` + `thinking: enabled` |
| Tool calls + thinking | automatico | `reasoning_content` va ripassato all'API |
| `temperature` | non raccomandato | ignorato in thinking mode |

---


## 🔑 Reference rapido

### Avvio
```bash
# Setup iniziale (prima volta)
bash py_env.sh init_py

# Attiva ambiente (ogni nuova sessione)
bash py_env.sh active

# ADK web
./start.sh                          # con SQLite persistence
adk web src/                        # senza persistence (InMemory)
adk web src/ --log_level DEBUG      # debug verboso

# Telegram
python telegram_bot.py
```

### Switch modello (solo `.env`)
```env
LLM_MODEL=gemini-3.5-flash          # Gemini via Vertex AI
LLM_MODEL=gemini-3.1-flash-lite     # Gemini Lite
LLM_MODEL=deepseek/deepseek-v4-flash # DeepSeek Flash
LLM_MODEL=deepseek/deepseek-v4-pro  # DeepSeek Pro
```

### Aggiungere contenuti
| Cosa | Come |
|------|------|
| Nuovo tipo di grog | Modificare `skills/grog/SKILL.md` |
| Nuovo piatto nel menu | Modificare `skills/menu/SKILL.md` |
| Nuova skill per Barnaby | `mkdir skills/nuova/` + `SKILL.md` → riavviare |
| Nuovo bot | Creare `bots/nomepersonaggio/` con `agent.py` + `persona.md` → aggiornare `bots/__init__.py` + `agent.py` |
| Cambiare orari giorno | Modificare `_TIME_PERIODS` in `time_context.py` |
| Cambiare atmosfera oraria | Modificare `_DESCRIPTIONS` in `time_context.py` |

### Prefissi State ADK
| Prefisso | Scope | Persistenza |
|----------|-------|-------------|
| (nessuno) | Session corrente | Solo con servizio persistente |
| `user:` | Tutti i session dell'utente | Solo con servizio persistente |
| `app:` | Tutti gli utenti dell'app | Solo con servizio persistente |
| `temp:` | Solo invocazione corrente | Mai |

### SessionService
| Tipo | Persistenza | Uso |
|------|-------------|-----|
| `InMemorySessionService` | ❌ | Dev/test (default ADK web) |
| `DatabaseSessionService` | ✅ | Produzione self-managed (SQLite/PostgreSQL) |
| `VertexAiSessionService` | ✅ | Google Cloud |

### 🔗 Problemi Comuni

| Problema | Soluzione |
|----------|-----------|
| Warning "System instructions modified" | Usare `global_instruction` con parte statica comune tra agenti |
| `gemini-3.5-flash` 404 su Vertex AI | Usare `GOOGLE_CLOUD_LOCATION=global` |
| Vertex AI 403 SERVICE_DISABLED | Verificare che Vertex AI API sia abilitata sul progetto GCP |
| ADC scadute | `gcloud auth application-default login` |
| Agente lento (molti tool calls) | `Increase tool performance with parallel execution.md` |
| Context window pieno | `Compress agent context for performance.md` |
| Dati persi al restart | Usare `./start.sh` (SQLite) invece di `adk web src/` |
| Skill non caricata | Verificare che la cartella abbia un `SKILL.md` valido con frontmatter `---` |
| Debug richieste LLM | `Agent activity logging.md` + `adk web --log_level DEBUG` |
| DeepSeek `orjson` error | `pip install orjson` |
| DeepSeek `greenlet` error | `pip install greenlet` |
| DeepSeek mostra il reasoning interno | Filtro `part.thought=True` già attivo in `runner.py` |
| Telegram bot non risponde nel gruppo | Privacy Mode ON → disabilitare via BotFather (`/setprivacy`) |
| Telegram MarkdownV2 error | Usa `parse_mode="HTML"` — molto più semplice |
| Barnacle non risponde / ephemeral fallisce | Rendere il bot admin del gruppo |
| Session DB cresce troppo | `purge_old_sessions()` già attivo (cron orario, 24h retention) |
| `purge_old_sessions` lancia OperationalError | Schema ADK cambiato — verificare nome tabella `events` nel DB |
| EventsCompactionConfig breaking change | Feature [EXPERIMENTAL] — verificare ADK changelog ad ogni upgrade |
| Compaction fallisce con 403/ADC error | `COMPACTION_MODEL` usa Gemini per default — eseguire `gcloud auth application-default login` |
| `patron_memories` non trovata | Prima chiamata ai tool la crea automaticamente — verificare che il DB esista (`./start.sh` almeno una volta) |
| `patron_memories` righe duplicate con user_id inventati | `user_id` viene da `ToolContext`, non dall'LLM — se succede, `DELETE FROM patron_memories WHERE user_id NOT GLOB '[0-9]*'` |
| Gemini: auth fallisce in produzione senza ADC | Usare `GOOGLE_APPLICATION_CREDENTIALS=/path/assoluto/key.json` nel `.env`; il bot verifica il file al boot |
| Service Account: file JSON non trovato al boot | `telegram_bot.py` stampa errore esplicito e si arresta — verificare il path in `.env` |

---

## 📋 Log delle Sessioni di Lavoro

### 2026-07-23 — Semplificazione Immagini e Pi-Agent Skills

**Obiettivo**: Unificare la pipeline di generazione immagini, rimuovere debito tecnico legato a Vertex AI per le immagini e introdurre le Skill di Pi-Agent per ottimizzare il workflow documentale.

**Attività svolte**:
1. **Generazione Immagini Unificata**:
   - Rimossa la dipendenza dai modelli "Imagen" (`imagen-3.0-generate-002`) e le configurazioni `IMAGE_LOCATION` da `tools.py` e `.env`.
   - La pipeline ora utilizza unicamente l'API standard `generate_content` con `response_modalities=["IMAGE"]` e i modelli multimodali Gemini Nano (es. `gemini-3.1-flash-lite-image`).
   - Il client Google GenAI viene ora inizializzato in modo neutro (`client = genai.Client()`), offrendo supporto implicito sia per Service Account che per `GEMINI_API_KEY`.
2. **Integrazione Pi-Agent Skills**:
   - Creata la skill `.agents/skills/scummbar-docs-analyzer` contenente l'indice della documentazione tecnica, rimuovendolo da `MEMORY.md` per alleggerire il context-window.
   - Creata la skill `.agents/skills/scummbar-memory-updater` per standardizzare gli aggiornamenti alla documentazione.
3. **Aggiornamento Documentazione**:
   - Aggiunta Isolde alla tabella introduttiva del `README.md`.
   - Aggiornato l'esempio del file `.env` nel `README.md` includendo `IMAGE_MODEL` e `GEMINI_API_KEY`.
   - Pulito e snellito `AGENTS.md` grazie all'introduzione delle skill.

---


### 2026-07-21 — Service Account + Riorganizzazione Documentazione

**Obiettivo**: supportare autenticazione Gemini tramite Service Account (oltre ad ADC) e riorganizzare la documentazione del progetto.

**Attività svolte**:
1. **Autenticazione Gemini via Service Account**
   - Analisi del flusso di autenticazione: `utils.py` chiama `load_dotenv()` prima di istanziare `Gemini`, quindi `GOOGLE_APPLICATION_CREDENTIALS` è disponibile nell'ambiente prima che `google-auth` venga interpellato
   - Aggiunto commento/variabile `GOOGLE_APPLICATION_CREDENTIALS` (commentata) in `src/scummbar_chat/.env`
   - Aggiornato `telegram_bot.py` → `_check_env()`: se il modello attivo è Gemini, verifica la presenza e validità del file JSON del Service Account al boot, con messaggio di errore esplicito e halt se il file non esiste
   - Nessuna modifica necessaria a `utils.py` o al costruttore `Gemini` — il meccanismo standard `google-auth` gestisce tutto automaticamente

2. **Riorganizzazione documentazione AI**
   - `CLAUDE.md` → sostituito da due file separati con ruoli distinti
   - `AGENTS.md`: istruzioni operative per agenti AI (regole codice, pattern, checklist, quick reference)
   - `MEMORY.md`: memoria del progetto (storia, decisioni, roadmap, problemi noti, log sessioni)
   - Aggiornato albero file in `MEMORY.md`
   - Aggiunti nuovi voci in Roadmap, Decisioni architetturali e Problemi Comuni

**File modificati**: `src/scummbar_chat/.env`, `telegram_bot.py`, `AGENTS.md` (riscritto), `MEMORY.md` (aggiornato da CLAUDE.md)

---

### 2026-07-19 — Sessioni precedenti (riepilogo)

Tutte le feature completate fino a questa data sono documentate nella sezione **Roadmap** con stato ✅.
Le decisioni architetturali prese sono registrate nella sezione **Decisioni architetturali**.
