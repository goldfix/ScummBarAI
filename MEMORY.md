# MEMORY.md — Memoria del Progetto Scummbar

> Questo file è la **memoria viva** del progetto: storia, decisioni, stato corrente, roadmap e attività aperte.
> Viene aggiornato ad ogni sessione di lavoro significativa.
> Gli agenti AI devono leggerlo prima di qualsiasi attività (vedi `AGENTS.md`).

---

## 🍺 STATO DEL PROGETTO (aggiornato: 2026-08-13)

### Cos'è Scummbar
Chat interattiva multi-bot ambientata in una taverna piratesca caraibica.
I partecipanti includono bot gestiti da AI (Barnaby il barista, Barnacle il gatto, Isolde la veggente, Balthazar il navigatore).
- **Applicazione Principale (Google ADK 2.6+ + Telegram + Streamlit Web RPG)**: **attiva e completata** ✅.
- **Frontend Streamlit Single-Player RPG**: **attivo e completato** ✅ (`src/scummbar_chat/streamlit/`, avvio con `./start_streamlit.sh`).
- **Diario di Bordo (Captain's Log)**: **attivo e completato** ✅ (`src/scummbar_chat/diary.py`, aggiornamento incrementale ogni 10 messaggi).
- **Cheshire Cat AI**: esperimento concluso e rimosso; il progetto è focalizzato al 100% su Google ADK + Telegram/Streamlit.

---

### 📁 Struttura del Progetto

```
scummbar/
├── docs/                              # Documentazione tecnica (ADK, DeepSeek, Telegram, Streamlit, ecc.)
├── src/
│   └── scummbar_chat/                 # 🤖 Applicazione Principale (Google ADK)
│       ├── __init__.py
│       ├── agent.py                   # root agent + InstructionProvider temporale
│       ├── utils.py                   # config condivisa, model factory, load_md(), load_all_skills()
│       ├── time_context.py            # mappatura orario reale → momento del giorno
│       ├── tools.py                   # FunctionTool: recall, memorize, write_secret_scroll, draw_tarot_card, draw_nautical_map, fetch_news_feed
│       ├── diary.py                   # 📜 Diario di Bordo (Captain's Log) incrementale in prima persona (via Chronicler)
│       ├── .env                       # config ambiente (NON committare)
│       ├── world/                     # scummbar.md (world context + regole narrazione)
│       ├── bots/                      # barnaby, barnacle, isolde, balthazar, chronicler (agent.py + persona.md)
│       ├── skills/                    # Skills ADK (grog, menu)
│       ├── telegram/                  # Adapter Telegram (adapter, formatter, runner)
│       └── streamlit/                 # 🎮 Frontend Web Streamlit (app.py, components.py)
├── data/                              # Dati e log persistenti
│   └── scummbar_chat/                 # Dati ADK / Telegram / Streamlit (sessions.db + diaries/ + logs/)
├── start.sh                           # avvio ADK web con persistenza SQLite
├── start_streamlit.sh                 # avvio frontend Streamlit Web RPG Single-Player
├── py_env.sh                          # setup ambiente Python (venv + uv)
├── telegram_bot.py                    # avvio bot Telegram (--debug flag, log su file)
├── pyproject.toml                     # dipendenze progetto (PEP 621 + uv)
├── AGENTS.md                          # istruzioni per agenti AI
├── MEMORY.md                          # questo file — memoria del progetto
└── README.md                          # documentazione pubblica (English)
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

**Dipendenze** (`pyproject.toml`, PEP 621 + `uv`):
```
google-adk[db]>=2.4.0   litellm      aiohttp
greenlet>=3.1.0         streamlit>=1.40.0   python-dotenv

[dependency-groups.dev]  # skill Pi-Agent
ruff   html2text   beautifulsoup4   sqlite-vec   jupyter
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
├── static_instruction = WORLD_CONTEXT (scummbar.md)   ← statico, cache-friendly
├── global_instruction = _time_instruction_provider()   ← funzione, aggiornata ad ogni turno
│     └── get_time_description()                        ← momento del giorno
├── instruction = COORDINATOR_INSTRUCTION
└── sub_agents:
    ├── barnaby   → persona.md + tools=[SkillToolset, recall, memorize, write_secret_scroll]
    ├── barnacle  → persona.md + tools=[SkillToolset, recall] (read-only)
    ├── isolde    → persona.md + tools=[recall, draw_tarot_card]
    ├── balthazar → persona.md + tools=[SkillToolset, recall, memorize, write_secret_scroll, draw_nautical_map, fetch_news_feed]
    └── chronicler → persona.md (agente scriba dedicato alla redazione del Diario di Bordo)
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
    "barnacle": ["barnacle", "micio", "gatto", "felino", "fusa", ...],
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
    user_id = tool_context.user_id  # ← Telegram ID reale, dalla sessione ADK
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
- Log rotativi su `data/scummbar_chat/logs/bot.log` (5 MB × 3) e `data/scummbar_chat/logs/errors.log` (2 MB × 2)
- `_dump_exception()`: scrive traceback completo con timestamp in caso di crash
- Exit code `1` su errore fatale

**`adapter.py`** ora cattura eccezioni a tutti i livelli:
- `_handle_update` wrappa `_handle_update_inner` con `try/except + log.exception()`
- `_on_task_done` callback: logga eccezioni dai task asyncio
- `gather` finale al shutdown: logga eccezioni residue
- `_session_cleaner_cron`: usa `log.exception()` invece di `log.error()`

Tutti gli errori a livello WARNING+ finiscono in `data/scummbar_chat/logs/errors.log`.

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
| `gemini-3.6-flash` | Vertex AI | **Default attivo** — richiede ADC + progetto abilitato |
| `gemini-3.5-flash-lite` | Vertex AI | Più veloce, meno potente |
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
    overlap_size=COMPACTION_OVERLAP,  # default: 2
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
| Generatore Diagrammi Kroki (`scummbar-kroki-diagrams`) | ✅ | Skill Pi-Agent in `.agents/skills/scummbar-kroki-diagrams/` con script `kroki_generator.py` (C4-PlantUML default, zlib+Base64 URL-safe) per la generazione di diagrammi per documentazione e README |
| Webhook Telegram (vs long polling) | 🔲 | Per deployment su server pubblico |
| Importazione Documentazione (Pydantic, FastAPI, HTTPX, DeepSeek, ADK, Streamlit, Kroki, UV, Ruff) | ✅ | docs/ indicizzati nel RAG (897 documenti, 14.881 chunk in `.md`, `.adoc`, `.yaml`, ecc.) |
| Supporto duale autenticazione (Service Account ↔ API Key) | ✅ | Permettere al bot di funzionare in modo flessibile sia con Service Account GCP che con classica GEMINI_API_KEY per tutti i modelli (conversazione, compaction, tools) |
| Autenticazione Gemini via Service Account | ✅ | `.env` + `GOOGLE_APPLICATION_CREDENTIALS`; pre-flight check in `telegram_bot.py` |
| Reorganizzazione docs AI (`AGENTS.md` + `MEMORY.md`) | ✅ | `CLAUDE.md` sostituito; memoria e istruzioni separate |
| Sistema Pi-Agent Skills (`scummbar-*`) | ✅ | Introduzione di skill per progressive disclosure documentale |
| Unificazione API Immagini | ✅ | Deprecato branch Imagen, architettura unificata su `generate_content` Gemini Nano |
| Frontend Web Streamlit (Single-Player RPG) | ✅ | `src/scummbar_chat/streamlit/` (`app.py`, `components.py`), routing automatico, recupero storico da DB, WAL mode, segmented control per chat input sticky |
| Diario di Bordo Narrativo in Prima Persona | ✅ | `src/scummbar_chat/diary.py`: file `data/scummbar_chat/diaries/Diary_NOME.md`, tracciamento `last_saved_index` (idempotente), aggiornamento automatico ogni 10 messaggi + pulsante manuale nel Tab "📜 Diario di Bordo", download `.md`, redazione affidata all'agente dedicato `chronicler` (`bots/chronicler/`) |
| Fase 2a Streamlit: Sacca del Pirata (Inventario) | 🔲 | Registro persistente nella sidebar per collezionare e riscaricare pergamene, mappe, ricette e carte tarocchi |
| Fase 2b Streamlit: Ispezione Memoria Avventore | 🔲 | Visualizzatore nella sidebar dei tratti e ricordi registrati su di te da Barnaby (`recall_patron_memory`) |
| Fase 2c Streamlit: Selettore Modello in UI | 🔲 | Dropdown nella sidebar per switchare il modello attivo (Gemini 3.6 ↔ DeepSeek v4) al volo dall'interfaccia web |
| Fase 3 Streamlit: Mappa della Taverna & Selezione Luogo | 🔲 | Spostamento visivo tra i tavoli della taverna (*Bancone, Cassa del Gatto, Angolo d'Ombra, Cartografo*) e controllo dell'ora |
| Dialoghi Bot-to-Bot controllati | 🔲 | Interazioni guidate cross-agente senza loop infiniti (es. Barnaby ↔ Balthazar) |

---

### 💡 Decisioni architetturali

- **Diario di Bordo Narrativo in Prima Persona & Agente Cronista**: Implementata la funzionalità di cronaca personale in `src/scummbar_chat/diary.py`. Ogni avventore possiede un file Markdown dedicato `data/scummbar_chat/diaries/Diary_NOME_Pirata.md`. Il sistema traccia deterministicamente l'indice dell'ultimo messaggio elaborato (`last_saved_index` nei metadati in testa al file) ed effettua aggiornamenti incrementali sintetizzando in stile romanzato caraibico ("Io") solo i messaggi non ancora registrati.
  - **Agente Cronista Dedicato (`bots/chronicler/`)**: La scrittura del diario è stata disaccoppiata dai bot di conversazione (rimosso `update_tavern_diary_tool` da Barnaby e Balthazar per non appesantirne il contesto) ed affidata all'agente dedicato `chronicler_agent` con prompt specializzato in `bots/chronicler/persona.md`.
  - **Pipeline asincrona dual-provider**: `generate_chapter_async()` usa `chronicler_agent.model` (`COMPACTION_LLM`) + `LlmRequest`/`generate_content_async`, funzionando sia con Gemini (API Key/Vertex) sia con DeepSeek.
  - **Trigger deterministici**: In Streamlit scatta automaticamente ogni 10 messaggi (con toast) e manualmente con il pulsante "Compila / Aggiorna Diario ORA" con download `.md`. In Telegram la redazione può essere invocata a livello di sistema/runner.
- **Esperimento Cheshire Cat AI (Concluso)**: Sviluppato in parallelo un plugin nativo `plugins/scummbar/` per sperimentare le primitive di Cheshire Cat AI (`cat.Agent`, `user` store, `Directive`, `@tool`). L'esperimento è stato completato con successo ed è ora archiviato per mantenere il focus del repository sull'applicazione principale Google ADK + Telegram (`src/scummbar_chat/`).
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
- **Isolamento dell'Autenticazione delle Immagini**: Abbiamo progettato l'autenticazione del modello di generazione delle immagini (`IMAGE_MODEL`) in modo che sia indipendente rispetto alla conversazione principale e alla compattazione. La factory `get_gemini_client_kwargs()` accetta un prefisso (es: `IMAGE_`) che isola le chiavi API o i Service Account dedicati. Per Vertex AI, le credenziali del Service Account per le immagini vengono istanziate in RAM come oggetto, evitando modifiche globali distruttive alle variabili di ambiente e garantendo una perfetta stabilità multi-thread.
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
- **Logging su file**: `data/scummbar_chat/logs/bot.log` + `data/scummbar_chat/logs/errors.log` (rotativi); `--debug` flag
- **Error propagation**: `_handle_update` wrappa con `try/except`, `_on_task_done` callback, `gather` finale logga residui
- **Autenticazione Gemini**: supporta sia ADC (`gcloud auth application-default login`) sia Service Account (`GOOGLE_APPLICATION_CREDENTIALS` nel `.env`); l'SDK `google-auth` li risolve automaticamente all'avvio
- **Pre-flight check Service Account**: `telegram_bot.py` verifica l'esistenza del file JSON al boot e si arresta con errore esplicito se mancante
- **`AGENTS.md` + `MEMORY.md`**: sostituiscono `CLAUDE.md`; `AGENTS.md` = istruzioni operative per agenti AI; `MEMORY.md` = memoria e storia del progetto

---

## 📱 Telegram — Integrazione

> 💡 **Nota**: La mappa completa e l'indice di dettaglio dei file di documentazione di Telegram in `docs/telegram/` sono gestiti ed indicizzati all'interno della skill `/skill:scummbar-docs-analyzer` (Sezione 16).

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
user_id = str(update["message"]["from"]["id"])  # per utente
```

**Implementazione senza librerie (aiohttp):**
```python
BASE = f"https://api.telegram.org/bot{TOKEN}"

# Long polling
async with session.get(f"{BASE}/getUpdates?offset={offset}&timeout=30") as r:
    updates = (await r.json())["result"]

# "sta scrivendo..."
await session.post(f"{BASE}/sendChatAction", json={"chat_id": chat_id, "action": "typing"})

# Invia messaggio (HTML più semplice di MarkdownV2)
await session.post(f"{BASE}/sendMessage", json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})
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
    callback_query_id=query_id,  # entro 15 secondi
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

> 💡 **Nota**: La mappa completa e l'indice di dettaglio dei file di documentazione di DeepSeek in `docs/deepseek/` sono gestiti ed indicizzati all'interno della skill `/skill:scummbar-docs-analyzer` (Sezione 15).

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
response.usage.prompt_cache_hit_tokens  # token serviti dalla cache
response.usage.prompt_cache_miss_tokens  # token calcolati ex novo
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
| Il Narratore si attiva ad ogni messaggio invece che 1 volta su 3 | Il modello leggeva le regole di attivazione generiche in `scummbar.md` e provava a simulare la probabilità del 33% di sua iniziativa. Risolto impostando un divieto di iniziativa esplicito in `scummbar.md` e vincolando l'attivazione solo alla presenza dell'esplicita `[NOTA DI SISTEMA: È il momento del Narratore...]` iniettata dall'adapter Telegram. |
| `static_instruction` non sembra abilitare il caching | Per ADK 2.6+ il caching esplicito richiede `context_cache_config` a livello `App` (`ContextCacheConfig`); `static_instruction` da sola sfrutta solo l'implicit cache del provider. Vedere `docs/google-api/context_caching.md`. |

---

## 📋 Log delle Sessioni di Lavoro

### 2026-08-15 — Mappe Nautiche Multimodali per Balthazar, Isolamento Thinking Immagini & Refactoring Feed

**Obiettivo**: Dotare l'agente Balthazar ("Il Navigatore") della capacità di generare mappe nautiche vintage di arcipelaghi pirateschi tramite il modello di generazione immagini, isolare la configurazione di thinking per le immagini in `.env` e perfezionare le regole di sistema.

**Attività svolte**:
- **Centralizzazione e Isolamento Thinking Immagini (`.env` / `utils.py`)**:
  - Aggiunta in Sezione 4 di `.env` della variabile dedicata `IMAGE_THINKING_LEVEL=high`, mantenendo `LLM_THINKING_LEVEL=medium` per la sola chat.
  - Esportata `IMAGE_THINKING_LEVEL` in `utils.py` e integrata nel `types.GenerateContentConfig(thinking_config=...)` delle chiamate di generazione visiva.
- **File Prompt & Template Dedicato Mappe (`bots/balthazar/map_prompt.md`)**:
  - Creato file dedicato con i requisiti grafici da mastro cartografo del XVII-XVIII secolo (pergamena brunita/bruciata, incisione vintage a tratteggio, tonalità seppia/oro/carbone e accenti scarlatti per rotte/"X" dei tesori).
  - Incluso template di prompt per `IMAGE_MODEL` strutturato in 5 sezioni (Cartiglio, Geografia arcipelago, Navigazione/Tesori, Mostri/Pericoli marini, Rosa dei venti/Accessori marginali).
- **Nuovo Tool `draw_nautical_map` (`src/scummbar_chat/tools.py`)**:
  - Implementata funzione asincrona `draw_nautical_map(tool_context, archipelago_name, map_details)` collegata a `IMAGE_MODEL` via `get_gemini_client_kwargs(prefix="IMAGE_")` con aspect ratio `4:3` (1200x896) e `IMAGE_THINKING_LEVEL`.
  - Implementato generatore di fallback in PIL `_draw_nautical_map_fallback` che disegna pergamena, coste/isole, rosa dei venti a 8 punte, rotte tratteggiate rosse e cartiglio.
  - Registrazione automatica dell'immagine come artifact di sessione (`mappa_{safe_title}.jpg/png`).
- **Aggiornamento Agente Balthazar & Persona (`bots/balthazar/`)**:
  - Registrato `draw_nautical_map_tool` nella lista strumenti di `balthazar_agent`.
  - Aggiunta regola 6 nel system prompt `persona.md` per srotolare e descrivere con epica solennità le mappe su richiesta degli avventori.
- **Refactoring Feed Notizie Live**:
  - Ristretto `fetch_news_feed` alle sole categorie **Politica Italiana** (ANSA) e **Politica Americana** (Google News USA in italiano).
  - Ordinamento cronologico decrescente con parsing RFC 822 / ISO `<pubDate>`.
- **Verifica**: Testate con successo la generazione sia tramite Gemini Flash Lite Image (JPEG 1200x896 C2PA) sia tramite fallback PIL, e verificata la validità del grafo ADK.

---

### 2026-08-13 — Skill Kroki per Pi-Agent & Localizzazione SVG (`scummbar-kroki-diagrams`)

**Obiettivo**: Creare una nuova skill Pi-Agent `.agents/skills/scummbar-kroki-diagrams/` per generare diagrammi ed infografiche vettoriali a supporto della documentazione e del README tramite Kroki.io (C4-PlantUML di default, zlib deflate + Base64 URL-safe), con supporto al salvataggio locale ed alla localizzazione automatica dei file SVG.

**Attività svolte**:
- **Estensione RAG per file `.adoc` e codice**: Aggiornato `rag/chunker.py` per riconoscere intestazioni AsciiDoc (`= Title`) e `rag/indexer.py` per indicizzare 37 file in `docs/kroki/` (totale RAG: 897 documenti, 14.881 chunk).
- **Nuova Skill Pi-Agent (`.agents/skills/scummbar-kroki-diagrams/`)**:
  - `SKILL.md`: Documentazione della skill per Pi-Agent, tipi di diagramma supportati, e regole di default (C4-PlantUML).
  - `scripts/kroki_generator.py`: Script CLI Python con codifica `zlib.compress(text, 9)` + `base64.urlsafe_b64encode`. Supporta flag `--type`, `--format`, `--output`, `--markdown`, `--html`, e la modalità `--localize` per scaricare automaticamente tutti gli SVG da un file Markdown e riscrivere i link con percorsi locali relativi.
- **Localizzazione Diagrammi README**: Generati i 5 diagrammi C4-PlantUML, scaricati gli SVG in `assets/*.svg` ed aggiornato `README.md` per puntare ai file locali, garantendo il rendering offline e la totale indipendenza da API esterne.
- **Verifica**: Testati con successo lo script CLI (`kroki_generator.py`), la modalità `--localize`, ed il rendering vettoriale SVG locale dei 5 diagrammi del README.

---

### 2026-08-13 — Diario di Bordo, Fix Chat Input e Ristrutturazione README

**Obiettivo**: Implementare il Diario di Bordo narrativo (Captain's Log), correggere il bug del chat input Streamlit e ristrutturare completamente il README in inglese.

**Attività svolte**:
- **Diario di Bordo (`src/scummbar_chat/diary.py`)** (nuovo modulo):
  - File Markdown per avventore in `data/scummbar_chat/diaries/Diary_NOME.md` con metadati `last_saved_index` in testa al file.
  - Aggiornamento **incrementale e deterministico**: legge `last_saved_index`, estrae solo i messaggi nuovi (`messages[last_saved_index:]`), genera un capitolo in prima persona ("Io") e appende — idempotente se nessun messaggio nuovo.
  - Pipeline **async dual-provider**: `generate_chapter_async()` usa `_build_model_instance(COMPACTION_MODEL)` + `LlmRequest`/`generate_content_async` → funziona con Gemini (API Key/Vertex) e DeepSeek.
  - Fix critico: `LlmResponse` espone `content.parts` (non `parts` diretto).
  - Tool ADK `update_tavern_diary_tool` (Barnaby + Balthazar): usa `tool_context.session.id` reale (non `st_session_` hardcodato — errato su Telegram dove `session_id = chat_id`), filtra per `user_id` (evita mescolanza in gruppo) e per i `thought` parts.
  - Streamlit: trigger automatico ogni 10 messaggi (toast di conferma), pulsante manuale "Compila / Aggiorna Diario ORA", pulsante download `.md`, anteprima Markdown nel Tab "📜 Diario di Bordo".
- **Fix Bug Chat Input Streamlit**: `st.chat_input` dentro `st.tabs` perdeva l'ancoraggio sticky in fondo alla pagina (bug noto). Sostituiti i `tabs` con `st.segmented_control` + rendering condizionale → il chat input resta a livello top-level e si ancora correttamente in fondo.
- **Ristrutturazione completa README.md in inglese**: nuova struttura a 9 sezioni (Project Purpose, Story & Characters, Quick Start, The ADK Core, Telegram Frontend, Streamlit Frontend, Pi-Agent, Project Structure, Environment Configuration) con 2 diagrammi ASCII del core, tabelle dettagliate su agenti/tools/skills/diario, e verifica automatica degli anchor TOC (fix variation selector U+FE0F nei link).
- **Verifica lingua**: codice Python tutto in inglese (commenti + docstring confermati), README in inglese, MEMORY.md/AGENTS.md restano in italiano (documentazione interna per l'agente).

---

### 2026-07-25 — Implementazione RAG Ibrido per `scummbar-docs-analyzer`

**Obiettivo**: Evolvere la skill Pi-Agent `scummbar-docs-analyzer` implementando un motore di ricerca RAG locale ibrido (FTS5 BM25 + Vector Cosine Similarity `gemini-embedding-2`) con architettura modulare in Python.

**Attività svolte**:
- **Importazione Documentazione di Riferimento**:
  - Convertita ed indicizzata la guida ufficiale Google Gemini Embeddings (`docs/ai-google-dev-gemini-api-docs-embeddings.md`).
  - Convertite ed indicizzate 5 guide ufficiali di SQLite-Vector (`docs/sqlite-vec/`) in Sezione 20 di `SKILL.md`.
- **Integrazione Dipendenze**: Aggiunto `sqlite-vec` (`^0.1.9`) a Poetry; rimosso `numpy` (non necessario).
- **Sviluppo Moduli RAG (`rag/`)**:
  - `config.py`: Gestione percorsi, modello `gemini-embedding-2` (768 dim) e client dual-auth `genai.Client`.
  - `chunker.py`: Parser Markdown strutturato con tracking gerarchico degli header (breadcrumbs) e formattazione autoconsistente secondo le best practice Google (`title: ... | section: ... | text: ...`).
  - `db.py`: Database SQLite ibrido con tabelle `documents` (hash MD5 incrementale), `chunks`, `chunks_fts` (FTS5 BM25) e `vec_chunks` (`sqlite-vec` virtual table `vec0`).
  - `embedder.py`: Generatore di vettori tramite `client.models.embed_content` con esecuzione concorrente multithread.
  - `indexer.py`: Indicizzatore incrementale con verifica hash MD5 (**353 file markdown scansionati, 11.078 chunk salvati**).
  - `search.py`: Engine di ricerca ibrida e CLI che unisce FTS5 e Vector Similarity con **Reciprocal Rank Fusion (RRF)**.
- **Refactoring e Pulizia**: Rinominato `src/` → `rag/` per evitare collisione namespace con `src/` del progetto. Rimosse 3 import inutilizzati, aggiunto `__init__.py`. Database RAG spostato in `.agents/skills/scummbar-docs-analyzer/data/`.
- **Importazione Documenti ADK Eval & Optimization**: Scaricate ed indicizzate 6 nuove guide da `adk.dev` (`evaluate.md`, `evaluate_criteria.md`, `evaluate_user-sim.md`, `evaluate_environment_simulation.md`, `evaluate_custom_metrics.md`, `optimize.md`) sotto `docs/google-api/`.
- **Nuovo Personaggio Balthazar "Il Navigatore" & Tool RSS Feed**:
  - Creato `src/scummbar_chat/bots/balthazar/` con `persona.md` (eccentrico cartografo, astronomo e cronista dei mari d'Oriente, canale-agnostico) con tabella di trasposizione notizie reali → ambientazione marittima/fantasy.
  - Esteso ed arricchito `persona.md` per focalizzare Balthazar su 3 argomenti principali (**Politica Italiana**, **Politica Americana** e **Tecnologia/Gadget**) con tono solenne, teatrale e comico (es. *L'Arengo dei Senatori Borbottanti*, *La Gilda della Mela d'Oro*, *I Golem d'Inchiostro*), includendo sempre il link HTML sorgente.
  - Implementato ed aggiornato il tool `fetch_news_feed` in `src/scummbar_chat/tools.py` (`fetch_news_feed_tool`), collegato ai feed RSS specializzati di ANSA Politica, ANSA Mondo/USA, ANSA Tecnologia e HDBlog.
  - Collegato `fetch_news_feed_tool` all'agente Balthazar in `src/scummbar_chat/bots/balthazar/agent.py`.
  - Aggiornato `src/scummbar_chat/agent.py` per includere `balthazar_agent` nei `sub_agents` e le relative regole di delega coordinatore.
  - Aggiornato `src/scummbar_chat/telegram/adapter.py` con lock di concorrenza `_locks["balthazar"]`, messaggio di occupato `_BOT_BUSY["balthazar"]` ed instradamento semantico per keyword (es. *mappa, rotta, stelle, bussola, coordinate, portolano, notizie, dispacci*).
- **Aggiornamento e Revisione Completa `README.md`**: Revisionato il file sezione per sezione; aggiornata la sezione Artifacts per includere le mappe e portolani di Balthazar, aggiunto `gemini-3.6` al supporto modelli Gemini ed allineato il totale del RAG a **353 documenti (11.087 chunk)**.
- **Rimozione Cheshire Cat AI**: Rimosse completamente le cartelle `src/scummbar_cat/`, `data/scummbar_cat/` e lo script `start_cat.sh`. Aggiornati `AGENTS.md`, `README.md`, `MEMORY.md` e `.gitignore` per rispecchiare la rimozione ed eliminare ogni riferimento orfano.
- **Adozione Completa di Astral `uv` per la Gestione dell'Ambiente Virtuale**:
  - Convertito `pyproject.toml` dallo schema proprietario `[tool.poetry]` allo standard **PEP 621** (`[project]` e `[dependency-groups]`) con `[tool.uv] package = false`.
  - Rimosso `requirements.txt` (ora obsoleto, gestito interamente da `pyproject.toml` e `uv.lock`).
  - Rimosso `poetry.lock` e generato il file di lock nativo `uv.lock`.
  - Aggiornato `py_env.sh` per utilizzare direttamente `uv` pre-installato sul sistema (`uv venv` e `uv sync`): rimossa ogni auto-installazione locale di `uv`.
- **Indicizzazione Documentazione UV e Aggiornamento RAG**:
  - Rilevati e indicizzati 81 nuovi documenti nella cartella `docs/uv/` (documentazione ufficiale del package manager UV).
  - Eseguito `rag/indexer.py` per l'indicizzazione incrementale: database aggiornato a **406 documenti (11.647 chunk)**.
  - Aggiornati `README.md`, `AGENTS.md` e `SKILL.md` di `scummbar-docs-analyzer` con i nuovi conteggi.

---

### 2026-08-05 — Download Documentazione Ufficiale DeepSeek API e Indicizzazione RAG

**Obiettivo**: Scaricare la documentazione API completa di DeepSeek da `api-docs.deepseek.com`, salvarla in `docs/deepseek/` ed indicizzarla nel motore RAG locale.

**Attività svolte**:
- **Scarico ed Estrazione 14 Documenti**:
  - Scaricate 14 pagine ufficiali via script `convert.py` della skill `scummbar-web-to-markdown`:
    1. `api-docs_deepseek_com.md` (Homepage, base URLs, formati OpenAI/Anthropic)
    2. `quick_start_pricing.md` (Prezzi `deepseek-v4-flash` / `deepseek-v4-pro`, token input/output/cache hit, regole)
    3. `quick_start_token_usage.md` (Conteggio e dettagli token)
    4. `quick_start_rate_limit.md` (Limiti di concorrenza 2500/500, isolamento `user_id`, keep-alive SSE)
    5. `quick_start_error_codes.md` (Codici errore 400, 401, 402, 422, 429, 500, 503)
    6. `guides_thinking_mode.md` (Thinking mode: toggle `thinking`, `reasoning_effort`, multi-turn, tool calls)
    7. `guides_multi_round_chat.md` (Conversazioni multi-turno)
    8. `guides_chat_prefix_completion.md` (Chat Prefix Completion Beta)
    9. `guides_fim_completion.md` (FIM Completion Beta)
    10. `guides_json_mode.md` (Output JSON strutturato)
    11. `guides_tool_calls.md` (Tool calls in thinking e non-thinking mode, mode `strict`)
    12. `guides_kv_cache.md` (KV Cache automatico server-side su disco)
    13. `guides_responses_api.md` (Responses API per `deepseek-v4-flash`, integrazione Codex, SSE streaming)
    14. `guides_anthropic_api.md` (Endpoint compatibile Anthropic `/anthropic`)
- **Indicizzazione RAG SQLite (`docs_rag.db`)**:
  - Eseguito `indexer.py`: indicizzati i 14 file (122 nuovi chunk) e purgati 6 documenti orfani.
  - Verificato l'allineamento 1:1:1:1 su tutte e 4 le tabelle: **443 documenti**, **11.748 chunk**, **11.748 righe FTS5**, **11.748 vettori `sqlite-vec`** (768 dim, `gemini-embedding-2`).
- **Aggiornamento Skill e Conoscenza**:
  - Aggiornato `.agents/skills/scummbar-docs-analyzer/SKILL.md` con i nuovi conteggi (443 docs, 11.748 chunk).
  - Verificato tramite lettura integrale dei documenti che la configurazione del progetto (`reasoning_effort=high`, `user_id` via `ToolContext`, `RetryConfig`) è al 100% conforme con le specifiche ufficiali DeepSeek.

---

### 2026-08-05 — Aggiornamento Documentazione Google ADK 2.6.0 e Refactoring Agenti

**Obiettivo**: Scaricare, convertire ed indicizzare la documentazione aggiornata di Google ADK 2.6.0 da `adk.dev` in `docs/google-api/`, ed allineare l'architettura degli agenti con le nuove funzionalità ufficiali (`static_instruction` e `RetryConfig`).

**Attività svolte**:
- **Scarico e Conversione Documentazione ADK 2.6.0**:
  - Convertite e salvate in `docs/google-api/` oltre 80 pagine ufficiali da `adk.dev` (Get Started, Tutorials, Agents, Workflows, Graphs, Models, Runtime, Deploy, Observability, Evaluation, Optimization, MCP, A2A, e l'intero API Reference Python `google-adk.html`).
- **Indicizzazione RAG Vettoriale**:
  - Eseguito `indexer.py`: database RAG aggiornato a **435 file Markdown (11.688 chunk)** con vettori `gemini-embedding-2`.
- **Ottimizzazione Context Caching (`static_instruction`)**:
  - Aggiornato `src/scummbar_chat/agent.py` per passare il contesto del mondo statico `WORLD_CONTEXT` (`scummbar.md`, ~6.2k chars) tramite il parametro nativo `static_instruction` di `Agent`/`LlmAgent`.
  - Mantenuto dinamico solo il contesto atmosferico temporale (`get_time_description()`) in `global_instruction`, garantendo l'Hit automatico della Context Cache su Gemini e DeepSeek ad ogni richiesta.
- **Resilienza API (`RetryConfig`)**:
  - Introdotta la configurazione condivisa `DEFAULT_RETRY_CONFIG` (`RetryConfig(max_attempts=3, initial_delay=1.0, max_delay=10.0, backoff_factor=2.0)`) in `src/scummbar_chat/utils.py`.
  - Applicato `retry_config=DEFAULT_RETRY_CONFIG` sia al `root_agent` sia a tutti i sub-agenti (`barnaby`, `barnacle`, `isolde`, `balthazar`), fornendo gestione nativa automatica di retry con backoff esponenziale per transient error o rate limits.
- **Fix scoperto dal check documentazione: Explicit Context Caching (`ContextCacheConfig`)**:
  - La doc ADK 2.6.0 (`docs/google-api/context_caching.md`) chiarisce che `static_instruction` da sola **NON abilita** il caching esplicito: serve configurare `context_cache_config` a livello `App`.
  - Aggiunto in `src/scummbar_chat/utils.py` il builder `build_context_cache_config()` che restituisce `ContextCacheConfig(min_tokens=2048, ttl_seconds=600, cache_intervals=5)` per modelli Gemini, `None` per DeepSeek (KV cache server-side automatico).
  - Passato `context_cache_config=CONTEXT_CACHE_CONFIG` all'`App` in `src/scummbar_chat/telegram/runner.py`.
- **Riorganizzazione Dipendenze Pi-Agent Skills (`pyproject.toml` e `py_env.sh`)**:
  - Spostate le librerie per le skill Pi-Agent (`html2text`, `beautifulsoup4`, `sqlite-vec`, `ruff`) ed aggiunta `jupyter` (`>=1.1.1`) nel gruppo `[dependency-groups.dev]` in `pyproject.toml`.
  - Aggiornato `py_env.sh` per eseguire esplicitamente `uv sync --group dev` in fase di inizializzazione locale dell'ambiente virtuale (`init` / `init_py`).
  - Sincronizzato l'ambiente virtuale tramite `uv lock` e `uv sync --active --group dev`.
- **Snellimento e Pulizia Dipendenze (`pyproject.toml`)**:
  - Rimosse le dipendenze ridondanti `greenlet` e `orjson` da `[project.dependencies]`, in quanto già soddisfatte transitivamente da `google-adk[db]` / `sqlalchemy` e `litellm`.
  - Verificato tramite `uv lock && uv sync` la corretta risoluzione dei pacchetti e confermata l'inizializzazione priva di errori sia dei modelli Gemini che dei modelli DeepSeek via `LiteLlm`.
  - Aggiunte variabili `.env` `CONTEXT_CACHE_ENABLED`, `CONTEXT_CACHE_MIN_TOKENS`, `CONTEXT_CACHE_TTL_SECONDS`, `CONTEXT_CACHE_INTERVALS` (Sezione 3b).
- **Realizzazione Frontend Web Single-Player Streamlit (`src/scummbar_chat/streamlit/`)**:
  - Aggiunte dipendenze `streamlit>=1.40.0` e `greenlet>=3.1.0` (richiesta da SQLAlchemy/aiosqlite async engine in Python 3.12 per l'ispezione DB di ADK) in `pyproject.toml` e sincronizzato l'ambiente con `uv sync`.
  - Creata cartella ad-hoc `src/scummbar_chat/streamlit/` con `app.py` (entry point UI) e `components.py` (componenti di rendering e sidebar).
  - Implementata l'esperienza di gioco RPG single-player: identità pirata con ID numerico per `patron_memories`, header atmosfera dinamica (`time_context.py`), chat interattiva (`st.chat_message`) e renderizzatore di artefatti (pergamene scaricabili ed immagini tarocchi).
  - Rimosso il selettore manuale dal menu laterale ed integrato l'instradamento semantico automatico `_resolve_intent()` per nomi o appellativi (*maga, veggente, navigatore, cartografo, gatto, micio, barista, oste*).
  - Perfezionata la funzione `format_streamlit_narrative()`: la narrazione ambientale (`_testo_`) e le azioni dei personaggi (`*azione*`) vengono renderizzate in **corsivo, racchiuse tra apicini (`«...»`) e con background grigio chiaro** (`#e9ecef`), mentre il testo parlato del bot rimane nel font normale sans-serif non stilizzato per la massima leggibilità.
  - **Campo "Nome Avventore" Obbligatorio**: Impostato `value=""` di default al boot dell'interfaccia Streamlit. Inserito un guard bloccante `if not patron_name:` che mostra un avviso piratesco (`st.warning`) e disabilita `st.chat_input`, costringendo il giocatore ad inserire il proprio nome nella sidebar prima di poter accedere allo Scummbar.
  - **Check Generale & Hardening dell'Implementazione Streamlit**:
    - Corretto il parsing della narrazione: nuovi pattern `_FULL_LINE_ENV_EMPH_PATTERN` e `_extract_env_text()` per gestire sia `_testo_` che `_*testo*_` (wrapper annidato prodotto talvolta dal modello) senza lasciare asterischi interni; ordinati i pattern (prima l'annidato, poi il semplice).
    - Escluso il markdown bold `**...**` dal match delle azioni inline tramite lookaround negativi (`(?<!\*)\*([^*\n]+)\*(?!\*)`): `**Barnaby**` non viene più trasformato in badge mono.
    - Corretto il messaggio di benvenuto in `app.py` (da `_*...*_` a `_..._` puro) per essere riconosciuto correttamente dal formatter.
    - Rimossa la nota `[NOTA DI SISTEMA: È il momento del Narratore...]` residua dal testo utente ripristinato dallo storico (`_NARRATOR_NOTE_PATTERN`), evitando che il prompt iniettato riapparisse nella chat ripristinata.
    - Reso robusto il cleanup dei tag di prefisso (`_AUGMENT_PREFIX_PATTERN` con regex `^(?:\[[^\]]+\]\s*)+`) al posto del fragile `rfind("] ")` che troncava testo utente contenente `] `.
    - Rimosso il codice morto (`BOT_DISPLAY_NAMES` inutilizzato e la chiave `st.session_state.artifacts` non necessaria nel clear button).
    - Verificato il funzionamento con loop eventi multipli (`asyncio.run` consecutivi come da rerun Streamlit), avvio server headless OK, e ripristino storico reale (42 messaggi dalla sessione `st_session_795704699102`).
  - Creato script di avvio `./start_streamlit.sh`.

---

### 2026-08-12 — Implementazione Frontend Web Streamlit (Single-Player RPG)

**Obiettivo**: Arricchire l'applicazione con un secondo frontend web nativo in Streamlit per trasformare lo Scummbar in un gioco avventura/RPG single-player interattivo, mantenendo la condivisione totale del database e della logica ADK con la versione Telegram.

**Attività svolte**:
- **Importazione Documentazione Streamlit (`docs/Streamlit/`) ed Indicizzazione RAG**:
  - Convertiti ed indicizzati **402 nuovi documenti Markdown** ufficiali da Streamlit in `docs/Streamlit/`.
  - Eseguito `rag/indexer.py`: database RAG incrementale aggiornato a **860 documenti (14.728 chunk)**.
- **Implementazione Package Streamlit (`src/scummbar_chat/streamlit/`)**:
  - Creata la cartella ad-hoc `src/scummbar_chat/streamlit/` con `app.py` (entry point UI) e `components.py` (componenti di rendering).
  - Implementato l'instradamento semantico automatico via `_resolve_intent()` per nomi o appellativi (*maga, veggente, navigatore, cartografo, gatto, micio, barista, oste*).
  - Creata la funzione `format_streamlit_narrative()` con resa visiva distinta: narrazione d'ambiente (`_testo_`) in box scuro monospaziato con bordo dorato (`📜`), azioni fisiche del personaggio (`*azione*`) in font monospaziato nero su badge chiaro (`color: #000000 !important; font-weight: 600`), e dialogo parlato in font normale sans-serif.
  - Implementata la funzione `load_session_chat_history()` e `session_id` deterministico (`st_session_{user_id}`): inserendo o cambiando il "Nome Avventore" nella sidebar, Streamlit ripristina all'istante l'intera cronologia della conversazione passata da SQLite.
  - Sincronizzato il contatore `narrator_counter` per iniettare la nota di sistema `[NOTA DI SISTEMA: È il momento del Narratore...]` ogni 3 turni.
  - **Check Finale contro Documentazione Ufficiale Streamlit (`docs/Streamlit/`)**:
    - Verificata la conformità API della versione installata (1.61.1) per tutti i componenti usati: `st.chat_message(name, avatar)`, `st.chat_input(placeholder)`, `st.markdown(unsafe_allow_html)`, `st.download_button`, `st.expander`, `st.spinner`.
    - Corretto `st.image`: sostituito `use_container_width=True` (deprecato e in rimozione) con il nuovo parametro `width="stretch"`, come raccomandato dalla docstring ufficiale.
    - Confermata la sicurezza di `unsafe_allow_html=True` sul testo LLM: Streamlit sanifica con DOMPurify e ignora il JavaScript di default.
    - Validato il pattern di `st.session_state.messages` con dizionari `role`/`content` contro i tutorial ufficiali (chat-response-feedback/revision).
- **Sicurezza e Concorrenza Database Multi-Processo**:
  - Forzata la modalità WAL (`PRAGMA journal_mode=WAL;`) e `PRAGMA busy_timeout=10000;` con `timeout=10.0` su `data/scummbar_chat/sessions.db`, garantendo la perfetta coesistenza e scrittura simultanea senza blocchi tra Telegram e Streamlit.
- **Documentazione Pubblica (`README.md`)**:
  - Creata la nuova Sezione 4 **🎮 Streamlit Single-Player RPG Frontend** in `README.md` con dettagli su architettura, routing automatico, recupero storico, concorrenza e formattazione narrativa.
  - Aggiornati la Table of Contents ed il Quick Start con lo script `./start_streamlit.sh`.


**Obiettivo**: Eseguire un controllo approfondito di `README.md` ed aggiornare schemi, riferimenti ed errori di battitura.

**Attività svolte**:
- **Diagramma Pi-Agent Skills**: Aggiornato lo schema ASCII per includere tutte e 3 le skill (`scummbar-docs-analyzer`, `scummbar-memory-updater`, `scummbar-web-to-markdown`).
- **Sezione Skills**: Aggiunta la documentazione della skill `scummbar-web-to-markdown` con esempi di invocazione.
- **Percorsi e Strutture**: Corretto il percorso del DB SQLite (`data/scummbar_chat/sessions.db`) e l'albero delle directory di Cheshire Cat AI (`data/scummbar_cat/`).
- **Refusi**: Corretto typo "Criptic" -> "Cryptic" nella tabella dei personaggi e verificato il bilanciamento dei marcatori code block.

---

### 2026-07-23/25 — Esperimento Cheshire Cat AI (Archiviato)

Esperimento concluso e rimosso (plugin `src/scummbar_cat/`, data `scummbar_cat/`, `start_cat.sh`).
Il progetto è focalizzato al 100% su Google ADK + Telegram/Streamlit. Dettagli storici: condivisione
storico multi-agente via hook `after_agent_run` + `tavern_shared_history`, direttiva temporale, test positivo.

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
