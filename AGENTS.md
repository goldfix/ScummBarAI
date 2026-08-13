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
│   ├── tools.py                       # FunctionTool ADK: recall, memorize, write_secret_scroll, draw_tarot_card, fetch_news_feed, update_tavern_diary
│   ├── diary.py                       # Diario di Bordo (Captain's Log) in prima persona
│   ├── .env                           # ⚠️ NON committare — contiene token e API key
│   ├── world/scummbar.md              # world context + regole Narratore (prompt)
│   ├── bots/barnaby/                  # agente Barnaby
│   ├── bots/barnacle/                 # agente Barnacle
│   ├── bots/isolde/                   # agente Isolde
│   ├── bots/balthazar/                # agente Balthazar
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
│       ├── diaries/                   # 📜 Diari di bordo (Diary_Nome.md)
│       └── logs/                      # Log rotativi bot.log ed errors.log
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
- `/skill:scummbar-docs-analyzer`: Motore RAG ibrido (FTS5 + Vector `gemini-embedding-2`) per cercare semanticamente tra gli **897 documenti** (14.881 chunk in formato `.md`, `.adoc`, `.yaml`, ecc.) nella cartella `docs/`.
- `/skill:scummbar-kroki-diagrams`: Genera diagrammi, schemi e mappe vettoriali (Excalidraw di default, Mermaid, Graphviz, PlantUML, D2, ecc.) tramite codifica URL zlib+Base64 per Kroki.io.
- `/skill:scummbar-memory-updater`: Per aggiornare `MEMORY.md`, `README.md` e `AGENTS.md` alla fine di una sessione di sviluppo o per modifiche rilevanti.
- `/skill:scummbar-web-to-markdown`: Per convertire una pagina web in un file Markdown salvato nella cartella specificata dall'utente e auto-indicizzarlo nel RAG.

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

## 🚫 Cosa NON Fare

- **Non aggiungere riferimenti a Telegram** nei file di prompt (`.md`) — i prompt sono canale-agnostici
- **Non passare `user_id` come parametro LLM** nei tool — usare sempre `tool_context.user_id`
- **Non modificare lo schema della tabella `patron_memories`** senza verificare le query nei tool
- **Non usare `adk web src/`** per test di persistenza — usare sempre `./start.sh`
- **Non usare `temperature`** con DeepSeek in thinking mode — parametro ignorato silenziosamente
- **Non modificare `EventsCompactionConfig`** senza leggere le note [EXPERIMENTAL] in `MEMORY.md`

---

## 📚 Dove Trovare la Documentazione

Tutta la documentazione è nella cartella `docs/` (**897 file di testo, 14.881 chunk vettorializzati**).
Usa la skill **`scummbar-docs-analyzer`** (`/skill:scummbar-docs-analyzer`) per effettuare ricerche ibride (semantiche + keyword) sul database RAG locale.

---

## ✅ Checklist Prima di un Commit

- [ ] `.env` non è incluso nel commit
- [ ] Nessuna API key o token hardcoded nel codice
- [ ] I prompt in `*.md` non contengono riferimenti a Telegram
- [ ] `user_id` nei tool viene da `ToolContext`, non da parametri LLM
- [ ] `MEMORY.md` aggiornato se sono state prese nuove decisioni architetturali o completate attività
- [ ] I commenti nel codice Python sono in inglese
