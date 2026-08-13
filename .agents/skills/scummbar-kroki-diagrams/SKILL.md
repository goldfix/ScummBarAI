---
name: scummbar-kroki-diagrams
description: Genera grafici, mappe mentali e diagrammi vettoriali (Excalidraw, Mermaid, PlantUML, Graphviz, D2, ecc.) tramite Kroki usando la codifica URL zlib+Base64. Stile di default: Excalidraw.
---

# Scummbar Kroki Diagram Generator

Questa skill permette di generare diagrammi, schemi architetturali, mappe piratesche ed infografiche vettoriali (SVG/PNG) tramite il servizio **[Kroki.io](https://kroki.io)**.

L'integrazione si basa sull'interfaccia HTTP `GET` con codifica del contenuto tramite **zlib deflate (livello 9) + Base64 URL-safe**.

---

## 📐 Regole di Default e Comportamento

1. **Stile di Default (Excalidraw)**:
   Se l'utente o la richiesta **non specifica uno stile**, il tipo di diagramma predefinito è **`excalidraw`** (stile fatto a mano / hand-drawn, ideale per mappe e schemi informali).
2. **Formato Output Predefinito**:
   Di default l'output è generato in formato **`svg`** (vettoriale scalabile), ma sono supportati anche `png`, `jpeg` e `pdf`.
3. **Algoritmo di Codifica URL**:
   Il testo sorgente del grafico viene compresso in Python tramite:
   ```python
   import base64
   import zlib

   compressed = zlib.compress(source_text.encode('utf-8'), level=9)
   payload = base64.urlsafe_b64encode(compressed).decode('ascii')
   url = f"https://kroki.io/{diagram_type}/{output_format}/{payload}"
   ```

---

## 🎨 Tipi di Diagramma Supportati

| Tipo (`diagram_type`) | Descrizione |
| :--- | :--- |
| **`excalidraw`** *(Default)* | Diagrammi in stile bozza/fatto a mano. Accetta sia JSON Excalidraw completo sia righe di testo per nodi veloci. |
| **`mermaid`** | Diagrammi di flusso (`flowchart`), sequenze, class diagram, ER e Gantt. |
| **`graphviz`** / **`dot`** | Grafi orientati e reti tramite la sintassi DOT. |
| **`plantuml`** / **`c4plantuml`** | Modelli UML complessi e architettura C4. |
| **`d2`** | Linguaggio moderno per diagrammi architetturali e di sistema. |
| **`bpmn`** | Diagrammi di processo di business. |
| **`blockdiag`** / **`nwdiag`** | Schemi a blocchi e di rete. |
| **`erd`** | Entity-Relationship diagram. |
| **`structurizr`** | Diagrammi architetturali C4 as code. |
| **`svgbob`** | Conversione da ASCII art a grafici SVG vettoriali! |

---

## 💻 Uso dello Script CLI integrato

Lo script `.agents/skills/scummbar-kroki-diagrams/scripts/kroki_generator.py` fornisce un'interfaccia da riga di comando pronta all'uso.

### Esempi di utilizzo:

```bash
# 1. Grafico Excalidraw di default (solo testo per nodi rapidi)
python3 .agents/skills/scummbar-kroki-diagrams/scripts/kroki_generator.py "Taverna Scummbar
Tavolo di Barnaby
Mappa di Balthazar" --markdown

# 2. Grafico Mermaid con output Markdown
python3 .agents/skills/scummbar-kroki-diagrams/scripts/kroki_generator.py "graph TD; A[Taverna]-->B[Barista];" --type mermaid --markdown

# 3. Grafico Graphviz scaricato su disco come file SVG
python3 .agents/skills/scummbar-kroki-diagrams/scripts/kroki_generator.py "digraph G { Taverna -> Grog; }" --type graphviz --output docs/images/taverna.svg

# 4. Input da file sorgente
python3 .agents/skills/scummbar-kroki-diagrams/scripts/kroki_generator.py --file schema.dot --type graphviz --markdown
```

---

## 🐍 Integrazione in Python / ADK

```python
import base64
import zlib

def generate_kroki_url(
    source_text: str,
    diagram_type: str = "excalidraw",
    output_format: str = "svg",
) -> str:
    """Genera l'URL Kroki per il diagramma fornito."""
    diagram_type = (diagram_type or "excalidraw").lower().strip()
    output_format = (output_format or "svg").lower().strip()
    
    compressed = zlib.compress(source_text.encode('utf-8'), level=9)
    payload = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    return f"https://kroki.io/{diagram_type}/{output_format}/{payload}"
```
