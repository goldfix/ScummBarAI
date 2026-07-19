"""Telegram formatter — converts ADK output to HTML for Telegram.

Three formatting levels:
  - Dialogue (bot direct speech)      → plain text
  - Action/narration (*text*)         → <i>text</i>
  - Atmosphere     (_full line_)      → <blockquote><i>text</i></blockquote>
"""

import html
import re

# Inline markdown pattern: *text* or _text_
_INLINE_MD = re.compile(r'(\*[^*\n]+\*|_[^_\n]+_)')

# Full-line atmosphere pattern: _text_ on its own line
_FULL_LINE_MD = re.compile(r'^_(.+)_$')


def format_response(text: str) -> str:
    """Convert the agent's text to HTML for Telegram."""
    if not text:
        return ""

    lines = text.split("\n")
    result = []

    for line in lines:
        stripped = line.strip()

        # Full line = atmosphere → italic blockquote
        m = _FULL_LINE_MD.match(stripped)
        if m:
            inner = html.escape(m.group(1))
            result.append(f"<blockquote><i>{inner}</i></blockquote>")
        else:
            # Process inline patterns
            result.append(_inline(line))

    return "\n".join(result)


def _inline(text: str) -> str:
    """Convert inline patterns *text* and _text_ to <i>text</i>."""
    parts: list[str] = []
    last = 0

    for match in _INLINE_MD.finditer(text):
        # Normal text before the match → HTML escape
        plain = text[last:match.start()]
        if plain:
            parts.append(html.escape(plain))

        # Markdown content → italic with HTML escaping
        inner = html.escape(match.group()[1:-1])
        parts.append(f"<i>{inner}</i>")
        last = match.end()

    # Remaining text
    if last < len(text):
        parts.append(html.escape(text[last:]))

    return "".join(parts)
