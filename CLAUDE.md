# CLAUDE.md — Guida al Progetto Scummbar

---

## 🍺 STATO DEL PROGETTO (aggiornato: 2026-07-19)

### Cos'è Scummbar
Chat interattiva multi-bot ambientata in una taverna piratesca caraibica.
I partecipanti includono bot gestiti da AI (Barnaby il barista, Barnacle il gatto).
Sviluppato con **Google ADK 2.4.0** + **Gemini / DeepSeek** via Vertex AI / LiteLlm.
Integrazione Telegram: **completata** ✅.

---

### 📁 Struttura del Progetto

```
scummbar/
├── docs/                              # Documentazione (ADK, DeepSeek, Telegram)
│   ├── *.md                           # Documentazione ADK (53 file)
│   ├── deepseek/                      # Documentazione DeepSeek API (5 file)
│   └── telegram/                      # Documentazione Telegram Bot API (4 file)
├── src/
│   └── scummbar_chat/                 # ← progetto attivo
│       ├── __init__.py
│       ├── agent.py                   # root agent + InstructionProvider temporale
│       ├── utils.py                   # config condivisa, model factory (_build_model_instance), load_md(), load_all_skills()
│       ├── time_context.py            # mappatura orario reale → momento del giorno
│       ├── tools.py                   # tools condivisi (placeholder)
│       ├── .env                       # config ambiente (NON committare)
│       ├── world/
│       │   └── scummbar.md            # world context + regole narrazione + logica Narratore
│       ├── bots/
│       │   ├── __init__.py            # esporta barnaby_agent, barnacle_agent
│       │   ├── barnaby/
│       │   │   ├── agent.py           # LlmAgent Barnaby + SkillToolset (auto-discovery)
│       │   │   └── persona.md         # chi è Barnaby, come parla
│       │   └── barnacle/
│       │       ├── agent.py           # LlmAgent Barnacle
│       │       └── persona.md         # chi è Barnacle, come si comporta
│       ├── skills/                    # Skills ADK (auto-discovery)
│       │   ├── grog/
│       │   │   └── SKILL.md           # skill dinamica: genera grog unici per contesto
│       │   └── menu/
│       │       └── SKILL.md           # skill menu: livello 1 rapido + livello 2 ricetta
│       └── telegram/                  # Adapter Telegram
│           ├── __init__.py
│           ├── adapter.py             # long polling, routing @mention, lock+timeout, Narratore
│           ├── formatter.py           # ADK output → HTML Telegram (3 livelli)
│           └── runner.py              # ADK Runner + DatabaseSessionService + session pruning
├── data/
│   └── sessions.db                    # SQLite persistence (creato automaticamente)
├── start.sh                           # avvio ADK web con persistenza SQLite
├── py_env.sh                          # setup ambiente Python (venv + poetry)
├── telegram_bot.py                    # avvio bot Telegram
├── requirements.txt                   # bootstrap: poetry + uv
├── pyproject.toml                     # dipendenze progetto
├── CLAUDE.md                          # questo file
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

**Auth Google**: `gcloud auth application-default login`
- Account: `your-account@example.com`
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

### 🧑‍🏫 Sistema Narratore (`scummbar.md` + `adapter.py`)

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

### 🔒 Lock con Timeout (`adapter.py`)

Invece di attendere indefinitamente il lock, ora viene usato `asyncio.wait_for` con timeout di 15 secondi.
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
- `COMPACTION_LLM` — istanza dedicata al riassunto sessioni (sempre Gemini)
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
- La compaction usa **sempre Gemini** (`COMPACTION_LLM`) anche se `LLM_MODEL=deepseek/...`
- Richiede quindi **Google ADC attivo** in entrambi i casi
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
| Nuove skills | 🔲 | Aggiungere cartelle in `skills/` |
| Integrazione Slack | 🔲 | Future |
| Webhook Telegram (vs long polling) | 🔲 | Per deployment su server pubblico |

---

### 💡 Decisioni architetturali

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
    ▼  (solo se contiene @barnaby o @barnacle)
chat.type == "private"? → redirect in-character al gruppo
    │
    ▼
bot_name = _detect_bot(text)   # barnacle ha priorità
    │
asyncio.wait_for(lock.acquire(), timeout=15s)
    errore timeout → "è occupato..."
    │
sendChatAction(typing)
    │
_message_counters[session_id] += 1
    se counter % 3 == 0 → aggiunge nota Narratore al testo
    │
augmented = "[Risponde BARNABY/BARNACLE] {text}"
response = run_agent(user_id, session_id=chat_id, augmented)
formatted = format_response(response)
    │
barnaby  → sendMessage(chat_id, formatted)           # pubblico
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
| Compaction fallisce con 403/ADC error | `COMPACTION_LLM` usa sempre Gemini — eseguire `gcloud auth application-default login` |
