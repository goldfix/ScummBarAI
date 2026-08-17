# AGENTS.md — Istruzioni per Agenti AI

> Questo file è rivolto agli assistenti AI (es. Claude, Gemini, Codex) che lavorano su questo progetto.
> Leggi sempre questo file prima di iniziare qualsiasi attività.

---

## 📖 Prima di tutto: leggi MEMORY.md

**`MEMORY.md`** è la memoria principale del progetto. Contiene:
- Stato attuale del progetto (cosa è completato, cosa è in corso, cosa è aperto)
- Architettura dettagliata di tutti i componenti
- Decisioni architetturali già prese e la loro motivazione
- Roadmap e attività aperte
- Log delle sessioni di lavoro significative
- Tabella dei problemi noti e le relative soluzioni

**Non procedere su nessuna attività senza aver letto `MEMORY.md`** — eviterai di rifare
lavoro già fatto, di contraddire scelte architetturali deliberate o di introdurre
incongruenze nel progetto.

---

## 🗺️ Struttura del Progetto (rapida)

```
scummbar/
├── AGENTS.md                          # questo file
├── MEMORY.md                          # memoria e storia del progetto ← LEGGI SEMPRE
├── README.md                          # documentazione pubblica (English)
├── telegram_bot.py                    # entry point Telegram (--debug flag)
├── start.sh                           # avvio ADK web con SQLite persistence
├── start_streamlit.sh                 # avvio RPG single-player Streamlit
├── src/scummbar_chat/                 # 🤖 Applicazione Google ADK + Telegram + Streamlit
│   ├── agent.py                       # root agent + InstructionProvider temporale
│   ├── utils.py                       # factory modello, config, load_md, load_all_skills
│   ├── time_context.py                # real time → tavern atmosphere
│   ├── tools.py                       # FunctionTool ADK: recall, memorize, write_secret_scroll, draw_tarot_card, draw_nautical_map, fetch_news_feed
│   ├── diary.py                       # Diario di Bordo (Captain's Log) in prima persona (tramite chronicler_agent)
│   ├── telemetry/                     # 🔬 Osservabilità: context, logging, db, metrics, queries, tracing, viewer
│   ├── .env                           # ⚠️ NON committare — contiene token e API key
│   ├── world/scummbar.md              # world context + regole Narratore (prompt)
│   ├── bots/barnaby/                  # agente Barnaby
│   ├── bots/barnacle/                 # agente Barnacle
│   ├── bots/isolde/                   # agente Isolde
│   ├── bots/balthazar/                # agente Balthazar (+ consult_barnaby/consult_barnacle AgentTool infra-agent)
│   ├── bots/chronicler/               # agente Cronista (compilazione Diario di Bordo)
│   ├── skills/                        # ADK skills auto-discovery
│   ├── telegram/                      # adapter Telegram (adapter, formatter, runner)
│   └── streamlit/                     # 🎮 frontend Web RPG (app.py, components.py)
├── .agents/skills/                    # 🤖 Pi-Agent Skills di sistema
│   ├── scummbar-docs-analyzer/        # RAG ibrido (FTS5 + sqlite-vec + gemini-embedding-2)
│   ├── scummbar-kroki-diagrams/       # Generatore di diagrammi e mappe tramite Kroki (Excalidraw, Mermaid, ecc.)
│   ├── scummbar-memory-updater/       # regole aggiornamento MEMORY/README/AGENTS
│   └── scummbar-web-to-markdown/      # convertitore web → Markdown
├── data/                              # Dati e log persistenti dell'applicazione
│   └── scummbar_chat/                 # Dati ADK / Telegram / Streamlit
│       ├── sessions.db                # Database sessioni SQLite (auto-creato)
│       ├── observability.db           # 🔬 Metriche & trace (turn_metrics, tool_metrics, agent_metrics, trace_spans)
│       ├── diaries/                   # 📜 Diari di bordo (Diary_Nome.md)
│       └── logs/                      # Log rotativi app.log ed errors.log
└── docs/                              # documentazione ADK, DeepSeek, Telegram, Streamlit, ecc.
```

---

## ⚙️ Regole di Codice

### Lingua
- **Python** (commenti `#`, docstring `"""`): **inglese** — standard di sviluppo
- **Prompt e file Markdown** (`persona.md`, `scummbar.md`, `SKILL.md`): **italiano** — sono input/output del modello
- **Messaggi di ritorno dei tool** verso l'LLM: **italiano**

### Qualità del Codice
- Mantenere l'implementazione **piccola, precisa, leggibile**. Cercare il design più minimale e funzionale.
- **Non introdurre codice superfluo**: niente workaround fragili, codice morto, o complessità non necessaria.
- Commentare le parti in cui i meccanismi non sono evidenti dal codice locale (il "perché", non il "cosa").
- Preferire commenti vicini all'implementazione rispetto a documenti separati.

### Sicurezza
- **Non committare mai `.env`** — contiene token Telegram, API key DeepSeek, credenziali GCP.
- Il file `.env` è in `.gitignore`. Verificare sempre prima di fare commit.
- `GOOGLE_APPLICATION_CREDENTIALS` (se usato) deve puntare a un percorso **assoluto** in produzione.

## 🤖 Pi-Agent Skills
Il progetto fornisce delle skill di sistema sotto `.agents/skills/` che devi invocare o consultare:
- `/skill:scummbar-docs-analyzer`: Motore RAG ibrido (FTS5 + Vector `gemini-embedding-2`) per cercare semanticamente tra gli **908 documenti** (15.430 chunk in formato `.md`, `.adoc`, `.yaml`, ecc.) nella cartella `docs/`.
- `/skill:scummbar-kroki-diagrams`: Genera diagrammi, schemi e mappe vettoriali (C4-PlantUML di default, Excalidraw, Mermaid, Graphviz, PlantUML, D2, ecc.) tramite codifica URL zlib+Base64 per Kroki.io.
- `/skill:scummbar-memory-updater`: Per aggiornare `MEMORY.md`, `README.md` e `AGENTS.md` alla fine di una sessione di sviluppo o per modifiche rilevanti.
- `/skill:scummbar-web-to-markdown`: Per convertire una pagina web in un file Markdown salvato nella cartella specificata dall'utente e auto-indicizzarlo nel RAG.

### Come usare le skill

| Situazione | Skill da invocare | Comando / esempio |
|-----------|-------------------|-------------------|
| Devo rispondere a una domanda tecnica su ADK/DeepSeek/Telegram/Streamlit | `scummbar-docs-analyzer` | `python3 .agents/skills/scummbar-docs-analyzer/rag/search.py "query" --top_k 5` |
| Ho aggiunto/modificato documentazione in `docs/` | `scummbar-docs-analyzer` (re-index) | `python3 .agents/skills/scummbar-docs-analyzer/rag/indexer.py` |
| Devo creare/aggiornare un diagramma nel README o in `docs/` | `scummbar-kroki-diagrams` | `python3 .agents/skills/scummbar-kroki-diagrams/scripts/kroki_generator.py "Sistema\nComponente" --markdown` |
| Devo rendere offline i diagrammi di un file Markdown | `scummbar-kroki-diagrams` (--localize) | `python3 .agents/skills/scummbar-kroki-diagrams/scripts/kroki_generator.py --localize README.md` (salva SVG in `assets/`) |
| Devo convertire una pagina web in Markdown e indicizzarla | `scummbar-web-to-markdown` | `python3 .agents/skills/scummbar-web-to-markdown/scripts/convert.py "URL" "docs/cartella/"` |
| Ho chiuso una sessione di sviluppo / preso decisioni architetturali | `scummbar-memory-updater` | `/skill:scummbar-memory-updater` (aggiorna MEMORY/README/AGENTS) |

---

## 🔑 Comandi Essenziali

```bash
# Setup iniziale (prima volta)
bash py_env.sh init_py

# Attiva ambiente (ogni nuova sessione di terminale)
bash py_env.sh active
# oppure: source py-env/bin/activate

# Avvio ADK web
./start.sh                          # con SQLite persistence
adk web src/                        # senza persistence (InMemory, per test rapidi)
adk web src/ --log_level DEBUG      # debug verboso

# Avvio bot Telegram
python telegram_bot.py              # normale (INFO)
python telegram_bot.py --debug      # DEBUG su console + file

# Avvio RPG Streamlit single-player
./start_streamlit.sh                # http://localhost:8501
```

---

## 🏗️ Pattern Architetturali Chiave

### Aggiungere contenuto (zero codice)
| Cosa | Come |
|------|------|
| Nuova skill per Barnaby | `mkdir src/scummbar_chat/skills/nome/` + `SKILL.md` → riavviare |
| Cambiare il mondo / atmosfera | Modificare `world/scummbar.md` |
| Cambiare personalità di un bot | Modificare `bots/barnaby/persona.md`, `bots/barnacle/persona.md`, `bots/isolde/persona.md` o `bots/balthazar/persona.md` |
| Nuovo tipo di grog | Modificare `skills/grog/SKILL.md` |
| Nuovo piatto nel menu | Modificare `skills/menu/SKILL.md` |
| Cambiare stile diario di bordo | Modificare il prompt in `diary.py` (`generate_chapter_async`) |

### Aggiungere un nuovo bot
1. Creare `bots/nomepersonaggio/` con `agent.py` + `persona.md`
2. Aggiornare `bots/__init__.py` per esportare il nuovo agente
3. Aggiornare `agent.py` per includerlo nei `sub_agents`
4. Aggiungere keywords in `_INTENT_MAP` in `telegram/adapter.py`

### Switch modello (solo `.env`)
```env
LLM_MODEL=gemini-3.6-flash           # Gemini via Vertex AI (ADC o Service Account)
LLM_MODEL=gemini-3.5-flash-lite      # Gemini Lite
LLM_MODEL=deepseek/deepseek-v4-flash # DeepSeek Flash (richiede DEEPSEEK_API_KEY)
LLM_MODEL=deepseek/deepseek-v4-pro   # DeepSeek Pro
```

### Autenticazione Google (per modelli Gemini)
- **Sviluppo**: `gcloud auth application-default login`
- **Produzione/Service Account**: aggiungere `GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json` nel `.env`
  - Il bot verifica l'esistenza del file al boot e logga un errore esplicito se mancante

---

## 📡 Direttive Osservabilità (Logging, Metrics, Tracing)

> Il progetto dispone di un'infrastruttura di osservabilità completa e local-first in `src/scummbar_chat/telemetry/`
> (vedi sezione 7 del README). **In OGNI futura iterazione, le nuove funzionalità DEVONO essere strumentate** con
> le primitive seguenti, senza eccezioni. Tutti i messaggi di log e i return dei tool restano in italiano/inglese
> secondo le regole della sezione Lingua; i commenti Python in inglese.

### Come strumentare il codice

| Situazione | Da usare | Esempio |
|-----------|----------|---------|
| Avvolgere un turno/operazione con contesto correlato | `log_context` (da `telemetry.context`) | `with log_context(channel="streamlit", session_id=..., user_id=..., agent_name=..., turn_id=...):` — imposta `session/user/agent/turn` automaticamente su ogni log emesso dentro il blocco |
| Loggare eventi di vita dell'app | `logging.getLogger(__name__)` | `log.info("...")`, `log.warning(...)`, `log.exception(...)` — il prefisso `[tg:bot:u:id:t:turn]` è iniettato dal `ContextualFilter` |
| Misurare un FunctionTool (latenza + successo + artefatti) | decoratore `@measure_tool` (da `telemetry.metrics`) | `@measure_tool("draw_nautical_map")` sopra la funzione async del tool |
| Registrare la durata di un turno utente | `record_turn_metric(...)` (da `telemetry.metrics`) | chiamare dopo `run_agent()` con `total_duration_ms`, `prompt_length`, `response_length`, `artifacts_count`, `workflow_steps`, `input/output/total_tokens` |
| Registrare un tempo di agente/coordinatore/cronista | `record_agent_metric(...)` | es. per `chronicler_agent` in `diary.py` |
| Generare uno span applicativo custom | `trace_span("nome", attributes={...})` (da `telemetry.tracing`) | per operazioni fuori dallo stream ADK (es. fetch RSS, salvataggio file) |
| Avvolgere un run ADK con tracing automatico | `turn_tracing()` (da `telemetry.tracing`) | già integrato in `telegram/runner.py` — NON duplicare il flush manuale |

### Regole d'oro

1. **turn_id univoco globale**: formati `tg:{update_id}` (Telegram) e `st:{session_id}:{counter}` (Streamlit).
   MAI turn_id numerici nudi (collidono tra sessioni e canali).
2. **Contesto sempre attivo**: usare `log_context` appena si entra in una richiesta/operazione; non loggare a mano `session_id` nel messaggio.
3. **Errori dentro il contesto**: i `log.exception`/`record_*` per gli errori vanno eseguiti DENTRO lo scope `log_context`, non dopo (il contesto verrebbe già resettato).
4. **Niente byte in DB/LLM**: nei metadati salvare SOLO riferimenti puliti (es. `mappa_x.jpg`), mai il binario.
5. **SQLite**: usare SEMPRE il context manager `telemetry.db.connection()` (chiude la connessione); mai `get_connection()` nudo.
6. **Trace concorrenti isolati**: gli span OTel sono già isolati per-turno (fan-out + filtro `trace_id`) — non creare altri `InMemorySpanExporter` globali.
7. **Nuove tabelle**: se servono nuove metriche, aggiungere lo schema in `telemetry/db.py` (con `_ensure_column` per migrazioni leggere) e le query in `telemetry/queries.py`.
8. **UI**: se la feature produce dati quantitativi o temporali, esporli nel cockpit Streamlit (sezione 7 del README) seguendo i pattern esistenti.

---

## 🚫 Cosa NON Fare

- **Non aggiungere riferimenti a Telegram** nei file di prompt (`.md`) — i prompt sono canale-agnostici
- **Non passare `user_id` come parametro LLM** nei tool — usare sempre `tool_context.user_id`
- **Non modificare lo schema della tabella `patron_memories`** senza verificare le query nei tool
- **Non usare `adk web src/`** per test di persistenza — usare sempre `./start.sh`
- **Non usare `temperature`** con DeepSeek in thinking mode — parametro ignorato silenziosamente
- **Non modificare `EventsCompactionConfig`** senza leggere le note [EXPERIMENTAL] in `MEMORY.md`

---

## 📚 Dove Trovare la Documentazione

Tutta la documentazione è nella cartella `docs/` (**908 file di testo, 15.430 chunk vettorializzati**).
Usa la skill **`scummbar-docs-analyzer`** (`/skill:scummbar-docs-analyzer`) per effettuare ricerche ibride (semantiche + keyword) sul database RAG locale.

---

## ✅ Checklist Prima di un Commit

- [ ] `.env` non è incluso nel commit
- [ ] Nessuna API key o token hardcoded nel codice
- [ ] I prompt in `*.md` non contengono riferimenti a Telegram
- [ ] `user_id` nei tool viene da `ToolContext`, non da parametri LLM
- [ ] Le nuove funzionalità sono strumentate con `log_context`, `@measure_tool`/`record_*` e `trace_span`/`turn_tracing` (vedi Direttive Osservabilità)
- [ ] `turn_id` rispetta i formati globali (`tg:...` / `st:{session}:{counter}`)
- [ ] Le connessioni SQLite telemetry usano `telemetry.db.connection()` (mai `get_connection()` nudo)
- [ ] `MEMORY.md` aggiornato se sono state prese nuove decisioni architetturali o completate attività
- [ ] I commenti nel codice Python sono in inglese
