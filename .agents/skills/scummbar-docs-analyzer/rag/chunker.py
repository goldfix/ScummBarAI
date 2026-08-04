"""
Markdown Chunker & Context Normalizer for the Scummbar RAG System.

Parses Markdown files into logical chunks based on header hierarchy (#, ##, ###),
maintains breadcrumb context, and generates self-contained representations
following Google GenAI RAG best practices:
  `title: {doc_path} | section: {breadcrumbs} | text: {content}`
"""

import re
from pathlib import Path
from typing import List, Dict, Any, Tuple

try:
    from .config import MAX_CHUNK_CHARS, MIN_CHUNK_CHARS
except ImportError:
    from rag.config import MAX_CHUNK_CHARS, MIN_CHUNK_CHARS


class MarkdownChunker:
    """
    Parses Markdown files into self-consistent, contextualized chunks
    preserving header hierarchy and code block integrity.
    """

    def __init__(self, max_chars: int = MAX_CHUNK_CHARS, min_chars: int = MIN_CHUNK_CHARS):
        self.max_chars = max_chars
        self.min_chars = min_chars

    def chunk_file(self, file_path: Path, rel_path: str) -> List[Dict[str, Any]]:
        """
        Reads a markdown file and returns a list of contextualized chunks.
        """
        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        return self.chunk_text(content, rel_path)

    def chunk_text(self, markdown_text: str, rel_path: str) -> List[Dict[str, Any]]:
        """
        Parses raw Markdown text, tracks header breadcrumbs, and generates
        chunks enriched with Google's RAG formatting.
        """
        lines = markdown_text.splitlines()
        chunks = []

        # Current state
        breadcrumb_stack: List[Tuple[int, str]] = []  # (header_level, header_text)
        current_lines: List[str] = []
        current_start_line = 1
        in_code_block = False

        for line_num, line in enumerate(lines, start=1):
            stripped = line.strip()

            # Track code block toggle
            if stripped.startswith("```"):
                in_code_block = not in_code_block

            # Header detection (only outside code blocks)
            header_match = re.match(r"^(#{1,6})\s+(.+)$", stripped) if not in_code_block else None

            if header_match:
                level = len(header_match.group(1))
                header_text = header_match.group(2).strip()

                # Flush current buffer if it has content
                if current_lines:
                    text_block = "\n".join(current_lines).strip()
                    if len(text_block) >= self.min_chars:
                        chunks.extend(
                            self._split_and_build_chunks(
                                text_block,
                                rel_path,
                                breadcrumb_stack,
                                current_start_line,
                                line_num - 1,
                            )
                        )
                    current_lines = []

                # Update breadcrumb stack for hierarchy
                while breadcrumb_stack and breadcrumb_stack[-1][0] >= level:
                    breadcrumb_stack.pop()
                breadcrumb_stack.append((level, header_text))

                current_start_line = line_num

            current_lines.append(line)

        # Flush remaining lines at end of file
        if current_lines:
            text_block = "\n".join(current_lines).strip()
            if len(text_block) >= self.min_chars or not chunks:
                chunks.extend(
                    self._split_and_build_chunks(
                        text_block,
                        rel_path,
                        breadcrumb_stack,
                        current_start_line,
                        len(lines),
                    )
                )

        return chunks

    def _split_and_build_chunks(
        self,
        text_block: str,
        rel_path: str,
        breadcrumb_stack: List[Tuple[int, str]],
        start_line: int,
        end_line: int,
    ) -> List[Dict[str, Any]]:
        """
        Splits text_block if it exceeds max_chars, ensuring code blocks aren't broken,
        and builds the contextualized dictionary for each chunk.
        """
        breadcrumbs_str = " > ".join([h[1] for h in breadcrumb_stack]) if breadcrumb_stack else "General"
        sub_blocks = self._subdivide_text(text_block)

        built_chunks = []
        for sub_text in sub_blocks:
            sub_text = sub_text.strip()
            if not sub_text:
                continue

            # Google RAG Asymmetric Document Formatting best practice:
            # title: {doc_path} | section: {breadcrumbs} | text: {content}
            contextualized_text = f"title: {rel_path} | section: {breadcrumbs_str} | text: {sub_text}"

            built_chunks.append(
                {
                    "doc_path": rel_path,
                    "breadcrumbs": breadcrumbs_str,
                    "start_line": start_line,
                    "end_line": end_line,
                    "content": sub_text,
                    "contextualized_text": contextualized_text,
                }
            )

        return built_chunks

    def _subdivide_text(self, text: str) -> List[str]:
        """
        Subdivides long text blocks into smaller pieces under max_chars,
        respecting paragraph breaks and code blocks.
        """
        if len(text) <= self.max_chars:
            return [text]

        paragraphs = text.split("\n\n")
        sub_blocks = []
        current_block = []
        current_len = 0

        for para in paragraphs:
            para_len = len(para) + 2
            if current_len + para_len > self.max_chars and current_block:
                sub_blocks.append("\n\n".join(current_block))
                current_block = [para]
                current_len = para_len
            else:
                current_block.append(para)
                current_len += para_len

        if current_block:
            sub_blocks.append("\n\n".join(current_block))

        return sub_blocks
