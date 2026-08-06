"""
Incremental Indexer Coordinator for the Scummbar Documentation RAG system.

Scans the `docs/` folder recursively, checks MD5 hashes to skip unchanged files,
extracts contextualized chunks, generates Gemini embeddings, and populates SQLite.
"""

import hashlib
from pathlib import Path
from typing import Any

try:
    from .chunker import MarkdownChunker
    from .config import DOCS_DIR
    from .db import RAGDatabase
    from .embedder import Embedder
except ImportError:
    from rag.chunker import MarkdownChunker
    from rag.config import DOCS_DIR
    from rag.db import RAGDatabase
    from rag.embedder import Embedder


class RAGIndexer:
    """
    Coordinates incremental indexing of Markdown documentation into SQLite.
    """

    def __init__(self, docs_dir: Path = DOCS_DIR):
        self.docs_dir = docs_dir
        self.chunker = MarkdownChunker()
        self.db = RAGDatabase()
        self.embedder = Embedder()

    def _compute_md5(self, file_path: Path) -> str:
        """
        Computes MD5 hash of a file for incremental indexing checks.
        """
        hasher = hashlib.md5()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def index_all(self, force_reindex: bool = False) -> dict[str, Any]:
        """
        Scans docs/ directory recursively, indexes new or modified markdown files,
        and purges documents deleted from disk from the database.
        """
        if not self.docs_dir.exists():
            print(f"❌ Docs directory does not exist: {self.docs_dir}")
            return {"indexed": 0, "skipped": 0, "deleted": 0, "total_chunks": 0}

        md_files = sorted(list(self.docs_dir.rglob("*.md")))
        disk_rel_paths = {str(f.relative_to(self.docs_dir.parent)) for f in md_files}
        stored_paths = set(self.db.get_all_doc_paths())

        # Purge deleted files
        deleted_paths = stored_paths - disk_rel_paths
        deleted_count = len(deleted_paths)
        if deleted_paths:
            print(f"🧹 Purging {deleted_count} deleted documents from database...")
            for del_path in deleted_paths:
                self.db.delete_doc(del_path)

        stats = {
            "total_files": len(md_files),
            "indexed": 0,
            "skipped": 0,
            "deleted": deleted_count,
            "total_chunks": 0,
        }

        print(f"🔍 Found {len(md_files)} Markdown files in {self.docs_dir}. Starting indexing...")

        for md_file in md_files:
            rel_path = str(md_file.relative_to(self.docs_dir.parent))
            current_md5 = self._compute_md5(md_file)

            # Incremental check
            stored_md5 = self.db.get_doc_hash(rel_path)
            if not force_reindex and stored_md5 == current_md5:
                stats["skipped"] += 1
                continue

            print(f"⚡ Indexing: {rel_path}...")

            # 1. Chunk document
            chunks = self.chunker.chunk_file(md_file, rel_path)
            if not chunks:
                stats["skipped"] += 1
                continue

            # 2. Extract contextualized text representations for embedding
            contextualized_texts = [c["contextualized_text"] for c in chunks]

            # 3. Generate embeddings batch
            embeddings = self.embedder.embed_batch(contextualized_texts)

            # 4. Save to SQLite database (documents, chunks, fts5, vec_chunks)
            saved_count = self.db.save_document_chunks(
                doc_path=rel_path,
                md5_hash=current_md5,
                chunks=chunks,
                embeddings=embeddings,
            )

            stats["indexed"] += 1
            stats["total_chunks"] += saved_count

        print(
            f"✅ Indexing complete: {stats['indexed']} indexed, {stats['skipped']} skipped, {stats['deleted']} purged, {stats['total_chunks']} chunks stored."
        )
        return stats


if __name__ == "__main__":
    import sys

    force = "--force" in sys.argv or "-f" in sys.argv
    indexer = RAGIndexer()
    indexer.index_all(force_reindex=force)
