"""scummbar_chat — shared utilities

Configuration loading, model factories, and markdown prompt file management.
Supports dynamic switching between Gemini (Vertex AI) and DeepSeek (via LiteLlm).
"""

import os
import pathlib

from dotenv import load_dotenv
from google.adk.models import BaseLlm
from google.adk.workflow import RetryConfig
from google.genai import types

# --- Load .env (override=True so .env values take precedence over shell env vars) ---
_ENV_PATH = pathlib.Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH, override=True)

# --- Environment Variables ---
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemini-3.5-flash")
LLM_THINKING_LEVEL: str = os.getenv("LLM_THINKING_LEVEL", "medium").strip().lower()
DEEPSEEK_REASONING_EFFORT: str = os.getenv("DEEPSEEK_REASONING_EFFORT", "high")

COMPACTION_MODEL: str = os.getenv("COMPACTION_MODEL", "gemini-3.5-flash")
COMPACTION_INTERVAL: int = int(os.getenv("COMPACTION_INTERVAL", "30"))
COMPACTION_OVERLAP: int = int(os.getenv("COMPACTION_OVERLAP", "2"))

# --- Explicit Context Caching (Gemini only; DeepSeek uses automatic KV cache) ---
CONTEXT_CACHE_ENABLED: bool = os.getenv("CONTEXT_CACHE_ENABLED", "true").lower() in ("true", "1")
CONTEXT_CACHE_MIN_TOKENS: int = int(os.getenv("CONTEXT_CACHE_MIN_TOKENS", "2048"))
CONTEXT_CACHE_TTL_SECONDS: int = int(os.getenv("CONTEXT_CACHE_TTL_SECONDS", "600"))
CONTEXT_CACHE_INTERVALS: int = int(os.getenv("CONTEXT_CACHE_INTERVALS", "5"))

IMAGE_MODEL: str = os.getenv("IMAGE_MODEL", "gemini-3.1-flash-lite-image")


def get_gemini_client_kwargs(prefix: str = "") -> dict:
    """Prepare client_kwargs for Gemini/Google GenAI constructor based on .env config.

    Supports both standard API Key (Google AI Studio) and Vertex AI (Service Account/ADC).
    If a prefix is supplied (e.g. 'IMAGE_'), it looks up independent variables.
    """
    kwargs = {}

    # Resolve keys dynamically based on the prefix (e.g. "", "IMAGE_")
    api_key_var = f"{prefix}GEMINI_API_KEY" if prefix else "GEMINI_API_KEY"
    alt_api_key_var = f"{prefix}GOOGLE_API_KEY" if prefix else "GOOGLE_API_KEY"
    use_vertex_var = f"{prefix}GOOGLE_GENAI_USE_VERTEXAI" if prefix else "GOOGLE_GENAI_USE_VERTEXAI"
    alt_use_vertex_var = f"{prefix}GOOGLE_GENAI_USE_ENTERPRISE" if prefix else "GOOGLE_GENAI_USE_ENTERPRISE"
    project_var = f"{prefix}GOOGLE_CLOUD_PROJECT" if prefix else "GOOGLE_CLOUD_PROJECT"
    location_var = f"{prefix}GOOGLE_CLOUD_LOCATION" if prefix else "GOOGLE_CLOUD_LOCATION"
    sa_var = f"{prefix}GOOGLE_APPLICATION_CREDENTIALS" if prefix else "GOOGLE_APPLICATION_CREDENTIALS"

    api_key = os.getenv(api_key_var) or os.getenv(alt_api_key_var)
    use_vertex_env = os.getenv(use_vertex_var) or os.getenv(alt_use_vertex_var)

    if api_key:
        kwargs["api_key"] = api_key
        kwargs["vertexai"] = False
        # Force project and location to None to override any inherited environment variables
        # which would otherwise trigger 'mutually exclusive' conflicts in the SDK constructor.
        kwargs["project"] = None
        kwargs["location"] = None
    else:
        # If no API Key is found, we fall back to Vertex AI / GCP Service Account
        project = os.getenv(project_var)
        if project or (use_vertex_env and use_vertex_env.lower() in ("true", "1")):
            kwargs["vertexai"] = True
            if project:
                kwargs["project"] = project
            kwargs["location"] = os.getenv(location_var, "us-central1")

            # Load credentials object explicitly from SA path if specified and exists
            sa_path = os.getenv(sa_var)
            if sa_path:
                import pathlib

                sa_file = pathlib.Path(sa_path)
                if not sa_file.is_absolute():
                    # Resolve relative to project root
                    sa_file = (pathlib.Path(__file__).parent.parent.parent / sa_path).resolve()

                if sa_file.exists():
                    from google.oauth2 import service_account

                    kwargs["credentials"] = service_account.Credentials.from_service_account_file(
                        str(sa_file), scopes=["https://www.googleapis.com/auth/cloud-platform"]
                    )

    return kwargs


def _build_model_instance(model_name: str, is_main_model: bool = False) -> BaseLlm:
    """Factory to build the appropriate ADK BaseLlm instance based on the provider prefix."""
    if model_name.startswith("deepseek/"):
        from google.adk.models import LiteLlm

        # We only enable heavy thinking mode for the main conversational agents
        thinking_cfg = {"type": "enabled"} if is_main_model else None
        effort_cfg = DEEPSEEK_REASONING_EFFORT if is_main_model else None

        return LiteLlm(
            model=model_name,
            thinking=thinking_cfg,
            reasoning_effort=effort_cfg,
            drop_params=True,
        )
    else:
        # Default fallback to Google's native Gemini models with parameterized auth
        from google.adk.models import Gemini

        return Gemini(model=model_name, client_kwargs=get_gemini_client_kwargs())


# --- Exported Ready-to-Use Model Instances ---
MODEL: BaseLlm = _build_model_instance(LLM_MODEL, is_main_model=True)
COMPACTION_LLM: BaseLlm = _build_model_instance(COMPACTION_MODEL, is_main_model=False)

# Configure native Gemini thinking (ignored if DeepSeek is active)
if LLM_MODEL.startswith("deepseek/"):
    THINKING_CONFIG = None
else:
    THINKING_CONFIG = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level=LLM_THINKING_LEVEL,
            include_thoughts=False,
        )
    )

# --- Standard Retry Configuration for ADK Agents ---
DEFAULT_RETRY_CONFIG = RetryConfig(
    max_attempts=3,
    initial_delay=1.0,
    max_delay=10.0,
    backoff_factor=2.0,
)


# --- Explicit Context Caching config for the App (Gemini 2.0+ only) ---
# static_instruction alone does NOT enable caching; per ADK docs you must
# configure ContextCacheConfig at App level. DeepSeek skips this because it
# provides automatic server-side KV caching.
def build_context_cache_config():
    """Return a ContextCacheConfig for Gemini models, None otherwise."""
    if not CONTEXT_CACHE_ENABLED or LLM_MODEL.startswith("deepseek/"):
        return None
    from google.adk.agents.context_cache_config import ContextCacheConfig

    return ContextCacheConfig(
        min_tokens=CONTEXT_CACHE_MIN_TOKENS,
        ttl_seconds=CONTEXT_CACHE_TTL_SECONDS,
        cache_intervals=CONTEXT_CACHE_INTERVALS,
    )


CONTEXT_CACHE_CONFIG = build_context_cache_config()


# --- Reference directories ---
CHAT_DIR = pathlib.Path(__file__).parent
WORLD_DIR = CHAT_DIR / "world"
BOTS_DIR = CHAT_DIR / "bots"

# --- Session persistence ---
_DB_PATH = CHAT_DIR.parent.parent / "data" / "scummbar_chat" / "sessions.db"
_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
SESSION_DB_URI: str = f"sqlite+aiosqlite:///{_DB_PATH}"

# --- Context Compaction configuration ---
# COMPACTION_MODEL, COMPACTION_INTERVAL, COMPACTION_OVERLAP already defined above.
# COMPACTION_LLM defaults to Gemini (requires ADC). Can be set to deepseek/...
# (requires DEEPSEEK_API_KEY) via COMPACTION_MODEL in .env.


def load_md(path: pathlib.Path) -> str:
    """Load a markdown file and return the cleaned text."""
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_all_skills(skills_dir: pathlib.Path) -> list:
    """Dynamically load all skills found in skills_dir.

    Each subdirectory containing an SKILL.md is loaded as a skill.
    Adding a new skill = create a new folder with SKILL.md.
    """
    from google.adk.skills import load_skill_from_dir

    skills = []
    if not skills_dir.exists():
        return skills
    for skill_dir in sorted(skills_dir.iterdir()):
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            skills.append(load_skill_from_dir(skill_dir))
    return skills


def build_instruction(*parts: str) -> str:
    """Build an agent instruction by concatenating parts."""
    return "\n\n---\n\n".join(p.strip() for p in parts if p.strip())


# --- World context (shared by all bots) ---
WORLD_CONTEXT: str = load_md(WORLD_DIR / "scummbar.md")
