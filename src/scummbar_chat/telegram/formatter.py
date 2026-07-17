"""Telegram formatter — converte output ADK in HTML per Telegram.

Tre livelli di formattazione:
  - Dialogo (risposta diretta del bot)  → testo normale
  - Azione/narrazione (*testo*)         → <i>testo</i>
  - Ambientazione (_riga intera_)       → <blockquote><i>testo</i></blockquote>
"""

import html
import re

# Pattern markdown inline: *testo* oppure _testo_
_INLINE_MD = re.compile(r'(\*[^*\n]+\*|_[^_\n]+_)')

# Pattern riga intera di ambientazione: _testo_ su una riga da sola
_FULL_LINE_MD = re.compile(r'^_(.+)_$')


def format_response(text: str) -> str:
    """Converte il testo dell'agente in HTML per Telegram."""
    if not text:
        return ""

    lines = text.split("\n")
    result = []

    for line in lines:
        stripped = line.strip()

        # Riga intera = ambientazione  →  blockquote corsivo
        m = _FULL_LINE_MD.match(stripped)
        if m:
            inner = html.escape(m.group(1))
            result.append(f"<blockquote><i>{inner}</i></blockquote>")
        else:
            # Processo pattern inline
            result.append(_inline(line))

    return "\n".join(result)


def _inline(text: str) -> str:
    """Converte pattern inline *testo* e _testo_ in <i>testo</i>."""
    parts: list[str] = []
    last = 0

    for match in _INLINE_MD.finditer(text):
        # Testo normale prima del match → escapa HTML
        plain = text[last:match.start()]
        if plain:
            parts.append(html.escape(plain))

        # Contenuto markdown → corsivo con HTML escaped
        inner = html.escape(match.group()[1:-1])
        parts.append(f"<i>{inner}</i>")
        last = match.end()

    # Testo rimanente
    if last < len(text):
        parts.append(html.escape(text[last:]))

    return "".join(parts)
