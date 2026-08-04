"""
Embedding generation service for the Scummbar Documentation RAG system.

Uses Google GenAI SDK (`gemini-embedding-2`) to compute float vectors
for document chunks and search queries with ThreadPoolExecutor for speed.
"""

import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

from google.genai import types

try:
    from .config import EMBEDDING_MODEL, EMBEDDING_DIM, get_genai_client
except ImportError:
    from rag.config import EMBEDDING_MODEL, EMBEDDING_DIM, get_genai_client


class Embedder:
    """
    Wrapper around Google GenAI Client for generating text embeddings.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL, dim: int = EMBEDDING_DIM):
        self.model_name = model_name
        self.dim = dim
        self.client = get_genai_client()

    def embed_text(self, text: str, max_retries: int = 3) -> List[float]:
        """
        Embeds a single string of text.
        """
        for attempt in range(max_retries):
            try:
                response = self.client.models.embed_content(
                    model=self.model_name,
                    contents=text,
                    config=types.EmbedContentConfig(output_dimensionality=self.dim),
                )
                return list(response.embeddings[0].values)
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"❌ Error generating embedding for text: {e}")
                    raise e
                time.sleep(1.5 ** attempt)
        return []

    def embed_batch(self, texts: List[str], max_workers: int = 8) -> List[List[float]]:
        """
        Embeds a list of strings concurrently using a thread pool.
        """
        if not texts:
            return []

        # Execute requests concurrently to maximize throughput
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            embeddings = list(executor.map(self.embed_text, texts))

        return embeddings
