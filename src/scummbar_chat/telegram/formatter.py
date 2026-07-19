"""
Module: formatter.py
Operations:
- Converts model Markdown responses into HTML compatible with Telegram's styling rules.
- Matches single-line ambient descriptions wrapped in underscores (`_text_`) and converts them into HTML `<blockquote><i>` tags.
- Processes remaining lines to handle inline emphasis (`*bold*` or `_italic_` markdown flavors) into corresponding `<i>` elements.
- Strictly escapes raw strings to prevent Telegram from crashing due to malformed HTML tags.
"""

import html
import re

# Inline markdown tokens: captures either *text* or _text_ blocks
_INLINE_MD = re.compile(r'(\*[^*\n]+\*|_[^_\n]+_)')

# Full line check for environment atmosphere: matches if a line is solely wrapped in underscores
_FULL_LINE_MD = re.compile(r'^\s*_\s*(.+?)\s*_\s*$', re.DOTALL)

def format_response(text: str) -> str:
    """Converts raw multi-line agent strings into Telegram HTML format."""
    if not text:
        return ""

    lines = text.split("\n")
    result = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append("")
            continue

        # Check if the line represents standalone environmental narrative/atmosphere
        m = _FULL_LINE_MD.match(stripped)
        if m:
            inner = html.escape(m.group(1))
            result.append(f"<blockquote><i>{inner}</i></blockquote>")
        else:
            # Otherwise, evaluate standard text and inline structures
            result.append(_inline(line))

    return "\n".join(result)

def _inline(text: str) -> str:
    """Escapes regular text and maps captured inline markdown markers to HTML italics."""
    parts: list[str] = []
    last = 0

    for match in _INLINE_MD.finditer(text):
        # Escape any standard characters occurring before the match
        plain = text[last:match.start()]
        if plain:
            parts.append(html.escape(plain))

        # Strip markdown wrappers, escape payload, and wrap in italics
        inner = html.escape(match.group()[1:-1])
        parts.append(f"<i>{inner}</i>")
        last = match.end()

    # Append any remaining string trailing after the final match
    if last < len(text):
        parts.append(html.escape(text[last:]))

    return "".join(parts)
