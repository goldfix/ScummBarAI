"""
Database persistence layer for the Scummbar Documentation RAG system.

Manages SQLite database initialization, incremental indexing tracking (MD5 hashes),
Full-Text Search (FTS5 BM25), and Vector Search via the `sqlite-vec` extension.
"""

import datetime
import sqlite3
from pathlib import Path
from typing import Any

import sqlite_vec

try:
    from .config import DB_PATH, EMBEDDING_DIM
except ImportError:
    from rag.config import DB_PATH, EMBEDDING_DIM


class RAGDatabase:
    """
    SQLite Database manager providing hybrid search (FTS5 + Vector Similarity).
    """

    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        """
        Creates and returns a SQLite connection with sqlite-vec extension loaded.
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        return conn

    def init_db(self) -> None:
        """
        Initializes schema tables for documents, chunks, FTS5, and sqlite-vec.
        """
        with self.get_connection() as conn:
            # 1. Document metadata table (for incremental indexing)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                doc_path TEXT PRIMARY KEY,
                md5_hash TEXT NOT NULL,
                last_indexed TIMESTAMP NOT NULL
            )
            """)

            # 2. Main chunks table
            conn.execute("""
            CREATE TABLE IF NOT EXISTS chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_path TEXT NOT NULL,
                breadcrumbs TEXT NOT NULL,
                start_line INTEGER NOT NULL,
                end_line INTEGER NOT NULL,
                content TEXT NOT NULL,
                contextualized_text TEXT NOT NULL,
                FOREIGN KEY (doc_path) REFERENCES documents(doc_path) ON DELETE CASCADE
            )
            """)

            # 3. FTS5 Full-Text Search virtual table
            conn.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
                breadcrumbs,
                content,
                contextualized_text,
                content='chunks',
                content_rowid='id'
            )
            """)

            # 4. sqlite-vec Virtual Table (768 dimensions for gemini-embedding-2)
            conn.execute(f"""
            CREATE VIRTUAL TABLE IF NOT EXISTS vec_chunks USING vec0(
                chunk_id INTEGER PRIMARY KEY,
                embedding float[{EMBEDDING_DIM}]
            )
            """)

            conn.commit()

    def get_doc_hash(self, doc_path: str) -> str | None:
        """
        Returns the stored MD5 hash for a document if indexed, else None.
        """
        with self.get_connection() as conn:
            row = conn.execute(
                "SELECT md5_hash FROM documents WHERE doc_path = ?", (doc_path,)
            ).fetchone()
            return row["md5_hash"] if row else None

    def get_all_doc_paths(self) -> list[str]:
        """
        Returns a list of all indexed document paths stored in the database.
        """
        with self.get_connection() as conn:
            rows = conn.execute("SELECT doc_path FROM documents").fetchall()
            return [r["doc_path"] for r in rows]

    def delete_doc(self, doc_path: str) -> None:
        """
        Deletes a document and all its associated chunks, FTS5 rows, and vectors.
        """
        with self.get_connection() as conn:
            chunk_rows = conn.execute(
                "SELECT id FROM chunks WHERE doc_path = ?", (doc_path,)
            ).fetchall()

            for r in chunk_rows:
                cid = r["id"]
                conn.execute("DELETE FROM vec_chunks WHERE chunk_id = ?", (cid,))
                conn.execute("DELETE FROM chunks_fts WHERE rowid = ?", (cid,))

            conn.execute("DELETE FROM chunks WHERE doc_path = ?", (doc_path,))
            conn.execute("DELETE FROM documents WHERE doc_path = ?", (doc_path,))
            conn.commit()

    def save_document_chunks(
        self,
        doc_path: str,
        md5_hash: str,
        chunks: list[dict[str, Any]],
        embeddings: list[list[float]],
    ) -> int:
        """
        Saves document metadata, chunks, FTS5 rows, and vector embeddings in a single transaction.
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Chunks count and embeddings count must match.")

        with self.get_connection() as conn:
            # First, clean any existing entries for this doc_path
            self.delete_doc(doc_path)

            now = datetime.datetime.now(datetime.UTC).isoformat()
            conn.execute(
                "INSERT INTO documents (doc_path, md5_hash, last_indexed) VALUES (?, ?, ?)",
                (doc_path, md5_hash, now),
            )

            inserted_count = 0
            for chunk, emb in zip(chunks, embeddings):
                # Insert chunk
                cursor = conn.execute(
                    """
                    INSERT INTO chunks (doc_path, breadcrumbs, start_line, end_line, content, contextualized_text)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        doc_path,
                        chunk["breadcrumbs"],
                        chunk["start_line"],
                        chunk["end_line"],
                        chunk["content"],
                        chunk["contextualized_text"],
                    ),
                )
                chunk_id = cursor.lastrowid

                # Insert FTS5
                conn.execute(
                    """
                    INSERT INTO chunks_fts (rowid, breadcrumbs, content, contextualized_text)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        chunk_id,
                        chunk["breadcrumbs"],
                        chunk["content"],
                        chunk["contextualized_text"],
                    ),
                )

                # Insert sqlite-vec vector
                serialized_vector = sqlite_vec.serialize_float32(emb)
                conn.execute(
                    "INSERT INTO vec_chunks (chunk_id, embedding) VALUES (?, ?)",
                    (chunk_id, serialized_vector),
                )

                inserted_count += 1

            conn.commit()
            return inserted_count

    def search_fts(self, query: str, top_k: int = 10) -> list[dict[str, Any]]:
        """
        Executes Full-Text Search (BM25) over chunks.
        """
        # Escape special FTS syntax characters for safety
        safe_query = f'"{query.replace('"', '""')}"'

        sql = """
        SELECT c.id, c.doc_path, c.breadcrumbs, c.start_line, c.end_line,
               c.content, c.contextualized_text, f.rank AS score
        FROM chunks_fts f
        JOIN chunks c ON f.rowid = c.id
        WHERE chunks_fts MATCH ?
        ORDER BY f.rank
        LIMIT ?
        """

        with self.get_connection() as conn:
            try:
                rows = conn.execute(sql, (safe_query, top_k)).fetchall()
                return [dict(r) for r in rows]
            except sqlite3.OperationalError:
                # Fallback to simple LIKE search if MATCH expression fails
                fallback_sql = """
                SELECT id, doc_path, breadcrumbs, start_line, end_line, content, contextualized_text, 0.0 as score
                FROM chunks
                WHERE content LIKE ? OR breadcrumbs LIKE ?
                LIMIT ?
                """
                pattern = f"%{query}%"
                rows = conn.execute(fallback_sql, (pattern, pattern, top_k)).fetchall()
                return [dict(r) for r in rows]

    def search_vector(self, query_embedding: list[float], top_k: int = 10) -> list[dict[str, Any]]:
        """
        Executes Vector Cosine Similarity Search using sqlite-vec.
        """
        serialized_query = sqlite_vec.serialize_float32(query_embedding)
        limit_val = int(top_k)

        sql = """
        SELECT c.id, c.doc_path, c.breadcrumbs, c.start_line, c.end_line,
               c.content, c.contextualized_text, v.distance AS score
        FROM vec_chunks v
        JOIN chunks c ON v.chunk_id = c.id
        WHERE v.embedding MATCH ? AND k = ?
        ORDER BY v.distance
        """

        with self.get_connection() as conn:
            rows = conn.execute(sql, (serialized_query, limit_val)).fetchall()
            return [dict(r) for r in rows]
