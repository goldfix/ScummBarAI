---
name: scummbar-web-to-markdown
description: Convertitore e Aggiornatore di Pagine Web in Markdown. Usa questa skill quando l'utente richiede di convertire, scaricare o AGGIORNARE una o più pagine web salvandole in formato Markdown (.md) in una specifica cartella.
---

# Web to Markdown Converter & Updater Skill

Questa skill permette di convertire qualsiasi pagina web (URL) o lista di URL in file `.md` puliti, completi e ben leggibili, inserendo sempre l'header con la sorgente originaria e permettendo l'aggiornamento automatico della documentazione.

---

## 📌 1. HEADER SORGENTE STANDARD INCLUSO
Ogni documento generato da questa skill riporta **obbligatoriamente all'inizio del file** l'intestazione standardizzata con il link alla pagina web sorgente:

```markdown
# Titolo della Pagina

> Source: [https://url-sorgente.com/pagina](https://url-sorgente.com/pagina)
```

Questa riga è fondamentale perché permette di automatizzare i successivi aggiornamenti del documento senza dover specificare nuovamente l'URL.

---

## 🔄 2. AGGIORNAMENTO AUTOMATICO DI DOCUMENTI ESISTENTI
Quando l'utente richiede di **aggiornare o ri-scaricare** un file Markdown esistente (es: *"Aggiorna il documento docs/cheshire-cat-ai/docs_quickstart_message.md"*):

1. L'Agente esegue lo script in modalità `--update`:
   ```bash
   python3 .agents/skills/scummbar-web-to-markdown/scripts/convert.py --update "<PATH_AL_FILE.md>"
   ```
2. Lo script legge l'header del file `.md` per estrarre l'URL sorgente originario (`> Source: [URL](URL)`).
3. **Se l'URL sorgente viene trovato**: Lo script riscarica la pagina web aggiornata e sovrascrive il file Markdown.
4. **Se l'URL sorgente NON è presente nell'header**: Lo script si arresta con l'errore `🛑 NO_SOURCE_URL`. L'Agente **DEVE FERMARSI** e informare l'utente:
   *Esempio:* `"Impossibile aggiornare automaticamente il file 'docs/manuale.md': l'intestazione con l'URL sorgente non è stata trovata. Per favore forniscimi l'URL della pagina web da cui riscaricarlo."`

---

## ⚠️ 3. REGOLE E CONDIZIONI PER I NUOVI DOWNLOAD
Per il download di **nuove pagine web**, l'Agente **DEVE VERIFICARE** che l'utente abbia fornito **ENTRAMBE** le seguenti informazioni:

1. **L'URL o lista di URL della pagina web** (es: `https://example.com/articolo`).
2. **La cartella di destinazione** dove salvare i file `.md` (es: `docs/`, `notes/`, `data/`).

### 🛑 Se una o entrambe le informazioni MANCANO:
**NON eseguire la skill e NON inventare i parametri.** 
Chiedi le informazioni mancanti:
*Esempio:* `"Per convertire la pagina web in Markdown, per favore forniscimi: 1. L'URL della pagina 2. La cartella dove vuoi salvare il file .md"`.

### 🛑 Se il file ESISTE GIÀ e l'utente NON ha chiesto un aggiornamento/sovrascrizione:
Se il file esiste già e lo script si arresta con `⚠️ FILE_EXISTS`:
- Chiedi prima conferma esplicita all'utente:
  *Esempio:* `"Il file 'docs/cheshire-cat-ai/docs_quickstart_message.md' esiste già. Vuoi sostituirlo con la nuova versione?"`
- Se l'utente conferma (o se ha usato parole come *"sovrascrivi"*, *"sostituisci"*, *"aggiorna"*, `"overwrite"`), riesegui lo script aggiungendo il flag `--force`.

---

## 📋 4. GESTIONE DI LISTE MULTIPLE E INDICIZZAZIONE AUTOMATICA RAG

Ogni volta che un file `.md` viene creato o aggiornato all'interno della cartella `docs/` tramite questa skill:

1. **Download & Conversione**: Esegui lo script `convert.py` per generare o aggiornare il file `.md`.
2. **Indicizzazione Automatica nel Database RAG**: Se il file è stato salvato dentro la cartella `docs/`, DEVI eseguire l'indicizzatore incrementale RAG per aggiornare istantaneamente il database vettoriale (`docs_rag.db`):
   ```bash
   PYTHONPATH=.agents/skills/scummbar-docs-analyzer python3 .agents/skills/scummbar-docs-analyzer/rag/indexer.py
   ```
   L'indicizzatore calcolerà l'hash MD5 del nuovo file, estrarrà i chunk contestualizzati con breadcrumbs e genererà gli embedding con Google `gemini-embedding-2`.
3. **Lettura Integrale del Documento**: Effettua la lettura completa (100%) del file `.md` appena generato usando il tool `read` per acquisirne la conoscenza prima di procedere con il compito successivo.

---

## 🛠️ Come funziona la conversione
La conversione viene eseguita tramite lo script Python dedicato:
- Estrae il contenuto principale della pagina HTML gestendo le codifiche UTF-8/charset HTTP via Beautiful Soup 4.
- Converte tutti gli URL relativi (link `a href` e immagini `img src`) in URL assoluti funzionanti.
- Configura `html2text` con `unicode_snob = True` per preservare emoji e caratteri accentati senza converli in ASCII.
- **Immagini**: Mantiene i link di riferimento ai server esterni (`![alt](https://...)`), **senza scaricarle in locale**.

---

## 🚀 Usage e Comandi

```bash
# 1. Download di un nuovo URL (si arresta in sicurezza se il file esiste già)
python3 .agents/skills/scummbar-web-to-markdown/scripts/convert.py "<URL>" "<OUTPUT_FOLDER>" ["<FILENAME.md>"]

# 2. Download con sovrascrizione forzata (dopo conferma o richiesta esplicita)
python3 .agents/skills/scummbar-web-to-markdown/scripts/convert.py "<URL>" "<OUTPUT_FOLDER>" ["<FILENAME.md>"] --force

# 3. Aggiornamento automatico di un file esistente leggendo la sorgente dal suo header
python3 .agents/skills/scummbar-web-to-markdown/scripts/convert.py --update "<PATH_AL_FILE.md>"
```
