"""
Configuration settings for the Scummbar Documentation RAG system.

Centralizes paths, embedding model choices (Google gemini-embedding-2),
database locations, and Google GenAI client initialization using dual-auth settings.
"""

import sys
from pathlib import Path

# Project paths
# .agents/skills/scummbar-docs-analyzer/rag/config.py -> skill root is 1 level up
SKILL_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = SKILL_ROOT.parent.parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
DATA_DIR = SKILL_ROOT / "data"
DB_PATH = DATA_DIR / "docs_rag.db"

# Official Google Embedding Model recommended in Gemini API docs
EMBEDDING_MODEL = "gemini-embedding-2"
EMBEDDING_DIM = 768

# Chunking limits
MAX_CHUNK_CHARS = 1200
MIN_CHUNK_CHARS = 100

# Ensure project root is in sys.path for internal imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def get_genai_client():
    """
    Initialize and return a google.genai.Client instance using the project's
    dual-authentication settings (API Key or Service Account).
    """
    try:
        from google import genai

        from src.scummbar_chat.utils import get_gemini_client_kwargs

        kwargs = get_gemini_client_kwargs()
        return genai.Client(**kwargs)
    except Exception as e:
        print(f"❌ Error initializing GenAI Client for RAG Embeddings: {e}")
        raise e
