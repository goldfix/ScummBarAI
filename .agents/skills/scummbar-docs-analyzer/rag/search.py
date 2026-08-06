"""
Hybrid Search Engine & CLI Interface for the Scummbar Documentation RAG system.

Combines Full-Text Search (FTS5 BM25) and Vector Similarity Search (`sqlite-vec`)
using Reciprocal Rank Fusion (RRF) for optimal precision and recall.
"""

import argparse
from typing import Any

try:
    from .db import RAGDatabase
    from .embedder import Embedder
except ImportError:
    from rag.db import RAGDatabase
    from rag.embedder import Embedder


class RAGSearchEngine:
    """
    Hybrid Search Engine combining FTS5 and Vector Search via Reciprocal Rank Fusion (RRF).
    """

    def __init__(self):
        self.db = RAGDatabase()
        self.embedder = Embedder()

    def search(
        self,
        query: str,
        top_k: int = 5,
        vector_weight: float = 1.0,
        fts_weight: float = 1.0,
        rrf_k: int = 60,
    ) -> list[dict[str, Any]]:
        """
        Performs hybrid search (FTS5 + Vector Similarity) using Reciprocal Rank Fusion (RRF).
        """
        # 1. Format query following Google GenAI RAG Asymmetric Query best practice:
        # task: search result | query: {query}
        formatted_query = f"task: search result | query: {query}"
        query_embedding = self.embedder.embed_text(formatted_query)

        # 2. Retrieve candidates from both indices
        vector_results = self.db.search_vector(query_embedding, top_k=top_k * 3)
        fts_results = self.db.search_fts(query, top_k=top_k * 3)

        # 3. Reciprocal Rank Fusion (RRF)
        rrf_scores: dict[int, float] = {}
        chunks_map: dict[int, dict[str, Any]] = {}

        # Process Vector results
        for rank, item in enumerate(vector_results, start=1):
            cid = item["id"]
            chunks_map[cid] = item
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (
                vector_weight * (1.0 / (rrf_k + rank))
            )

        # Process FTS results
        for rank, item in enumerate(fts_results, start=1):
            cid = item["id"]
            chunks_map[cid] = item
            rrf_scores[cid] = rrf_scores.get(cid, 0.0) + (
                fts_weight * (1.0 / (rrf_k + rank))
            )

        # 4. Sort candidates by final RRF score
        sorted_candidates = sorted(
            rrf_scores.items(), key=lambda x: x[1], reverse=True
        )

        final_results = []
        for cid, score in sorted_candidates[:top_k]:
            chunk_data = chunks_map[cid]
            chunk_data["rrf_score"] = round(score, 5)
            final_results.append(chunk_data)

        return final_results


def main():
    parser = argparse.ArgumentParser(
        description="Search Scummbar documentation using Hybrid RAG (FTS5 + Vector)."
    )
    parser.add_argument("query", type=str, help="Search query string")
    parser.add_argument(
        "--top_k", "-k", type=int, default=5, help="Number of results to return (default: 5)"
    )

    args = parser.parse_args()

    engine = RAGSearchEngine()
    results = engine.search(args.query, top_k=args.top_k)

    print(f"\n🔎 Query: '{args.query}' — Top {len(results)} results:\n" + "=" * 60)

    for i, res in enumerate(results, start=1):
        print(f"\n[{i}] RRF Score: {res['rrf_score']} | File: {res['doc_path']} (Lines {res['start_line']}-{res['end_line']})")
        print(f"📌 Section: {res['breadcrumbs']}")
        print("-" * 60)
        print(res["content"])
        print("-" * 60)


if __name__ == "__main__":
    main()
