---
name: scummbar-docs-analyzer
description: Strumento RAG ibrido (FTS5 BM25 + Vector Cosine Similarity gemini-embedding-2) per esplorare, cercare ed indicizzare la documentazione tecnica nella cartella docs/.
---

# Scummbar Documentation Analyzer & RAG Engine

La cartella `docs/` contiene tutta la documentazione ufficiale dei framework e delle tecnologie utilizzate nel progetto (ADK, Gemini, DeepSeek, Telegram Bot API, Cheshire Cat AI, Pydantic, FastAPI, HTTPX, SQLite-Vector, BeautifulSoup4, html2text).

Questa skill fornisce il **motore di ricerca RAG ibrido locale** per trovare istantaneamente informazioni pertinenti tra tutti i 435 documenti (11.688 chunk) senza dover scorrere manualmente indici o file statici.

---

## ⚠️ REGOLE OPERATIVE PER L'ANALISI E L'AGGIORNAMENTO

Quando utilizzi questa skill o ti viene chiesto di consultare/aggiornare la documentazione:

1. **🔎 Ricerca Semantica & Keyword via RAG**:
   Quando devi rispondere a domande tecniche o consultare guide, usa SEMPRE il motore RAG tramite `bash`:
   ```bash
   PYTHONPATH=.agents/skills/scummbar-docs-analyzer python3 .agents/skills/scummbar-docs-analyzer/rag/search.py "query di ricerca" --top_k 5
   ```

2. **📖 Lettura Integrale del Documento Trovato**:
   I risultati del RAG restituiscono i chunk più rilevanti con indicazione del percorso file e dei numeri di riga (`start_line`-`end_line`). Prima di implementare del codice basandoti su un risultato, usa SEMPRE il tool `read` sul file Markdown completo per comprendere tutte le firme, i parametri e le eccezioni.

3. **⚡ Indicizzazione Incrementale Automatica**:
   Ogni volta che vengono aggiunti o modificati file `.md` nella cartella `docs/`, DEVI eseguire l'indicizzatore incrementale per aggiornare il database vettoriale:
   ```bash
   PYTHONPATH=.agents/skills/scummbar-docs-analyzer python3 .agents/skills/scummbar-docs-analyzer/rag/indexer.py
   ```
   L'indicizzatore verifica gli hash MD5 dei file: ri-vettorializza solo i documenti nuovi o modificati, saltando istantaneamente quelli invariati.

4. **📋 Importazione Sequenziale di URL/Documenti**:
   Se ti viene chiesto di importare nuovi documenti web, usa la skill `scummbar-web-to-markdown` per convertirli e salvarli in `docs/`, quindi esegui immediatamente `indexer.py` per indicizzarli nel RAG.

5. **🚫 Nessun Aggiornamento a `MEMORY.md`**:
   Non aggiornare `MEMORY.md` per le singole importazioni o consultazioni di documentazione. `MEMORY.md` rimane riservato alla storia e alle decisioni architetturali dell'applicazione.

---

## 🏗️ Architettura Interna del RAG

Il motore RAG è modulare ed è situato sotto `.agents/skills/scummbar-docs-analyzer/`:

- **`data/docs_rag.db`**: Database SQLite contenente le tabelle per i documenti, i chunk, l'indice FTS5 ed i vettori `sqlite-vec` (virtual table `vec0`).
- **`rag/config.py`**: Configurazione dei percorsi, modello consigliato da Google **`gemini-embedding-2`** (768 dimensioni) e client GenAI con auth duale (API Key / Service Account).
- **`rag/chunker.py`**: Parser Markdown che preserva la gerarchia degli header (`#`, `##`, `###`), i blocchi di codice e genera la struttura autoconsistente secondo le best practice Google:
  `title: {doc_path} | section: {breadcrumbs} | text: {content}`
- **`rag/db.py`**: Manager database SQLite con tabella `documents` (hash MD5), `chunks`, `chunks_fts` (FTS5 BM25) e `vec_chunks` (`sqlite-vec`).
- **`rag/embedder.py`**: Generazione multithread concorrente degli embedding con Google GenAI SDK.
- **`rag/indexer.py`**: Script di indicizzazione incrementale ricorsiva.
- **`rag/search.py`**: Engine di ricerca ibrida basato su **Reciprocal Rank Fusion (RRF)**:
  `score(chunk) = w_fts * (1 / (60 + rank_fts)) + w_vec * (1 / (60 + rank_vec))`

---

## 🛠️ Comandi CLI Rapidi

```bash
# Ricerca ibrida RAG (Top 5 risultati)
PYTHONPATH=.agents/skills/scummbar-docs-analyzer python3 .agents/skills/scummbar-docs-analyzer/rag/search.py "query di ricerca" --top_k 5

# Re-indicizzazione incrementale (solo file nuovi/modificati)
PYTHONPATH=.agents/skills/scummbar-docs-analyzer python3 .agents/skills/scummbar-docs-analyzer/rag/indexer.py

# Re-indicizzazione forzata di tutti i documenti
PYTHONPATH=.agents/skills/scummbar-docs-analyzer python3 .agents/skills/scummbar-docs-analyzer/rag/indexer.py --force
```
