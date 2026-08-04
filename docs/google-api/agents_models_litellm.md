# LiteLLM - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/models/litellm/](https://adk.dev/agents/models/litellm/)

[ Skip to content ](<https://adk.dev/agents/models/litellm/#litellm-model-connector-for-adk-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/models/litellm.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/models/litellm/index.md> "View this page as Markdown")

# LiteLLM model connector for ADK agents[¶](<https://adk.dev/agents/models/litellm/#litellm-model-connector-for-adk-agents> "Permanent link")

Supported in ADKPython v0.1.0

ADK Python Security Advisory: LiteLLM supply chain compromise

Unauthorized code was identified in LiteLLM versions 1.82.7 and 1.82.8 on PyPI on March 24, 2026. If you use ADK Python with the `eval` or `extensions` extras, update to the latest version of ADK Python immediately. If you installed or upgraded LiteLLM during this period, rotate all secrets and credentials. For details and required actions, refer to the [ADK security advisory](<https://github.com/google/adk-python/issues/5005>) and [LiteLLM's Security Update: Suspected Supply Chain Incident](<https://docs.litellm.ai/blog/security-update-march-2026>).

[LiteLLM](<https://docs.litellm.ai/>) is a Python library that acts as a translation layer for models and model hosting services, providing a standardized, OpenAI-compatible interface to over 100+ LLMs. ADK provides integration through the LiteLLM library, allowing you to access a vast range of LLMs from providers such as OpenAI, Anthropic, Ollama, Mistral, DeepSeek, and Cohere, and many others. You can run open-source models locally or self-host them and integrate them using LiteLLM for operational control, cost savings, privacy, or offline use cases.

You can use the LiteLLM library to access remote or locally hosted AI models:

  * **Remote model host:** Use the `LiteLlm` wrapper class and set it as the `model` parameter of `LlmAgent`.
  * **Local model host:** Use the `LiteLlm` wrapper class configured to point to your local model server. For examples of local model hosting solutions, see the [Ollama](<https://adk.dev/agents/models/ollama/>) or [vLLM](<https://adk.dev/agents/models/vllm/>) documentation.

Windows Encoding with LiteLLM

When using ADK agents with LiteLLM on Windows, you might encounter a `UnicodeDecodeError`. This error occurs because LiteLLM may attempt to read cached files using the default Windows encoding (`cp1252`) instead of UTF-8. Prevent this error by setting the `PYTHONUTF8` environment variable to `1`. This forces Python to use UTF-8 for all file I/O.

**Example (PowerShell):**
    
    [](<https://adk.dev/agents/models/litellm/#__codelineno-0-1>)# Set for the current session
    [](<https://adk.dev/agents/models/litellm/#__codelineno-0-2>)$env:PYTHONUTF8 = "1"
    [](<https://adk.dev/agents/models/litellm/#__codelineno-0-3>)
    [](<https://adk.dev/agents/models/litellm/#__codelineno-0-4>)# Set persistently for the user
    [](<https://adk.dev/agents/models/litellm/#__codelineno-0-5>)[System.Environment]::SetEnvironmentVariable('PYTHONUTF8', '1', [System.EnvironmentVariableTarget]::User)
    
## Setup[¶](<https://adk.dev/agents/models/litellm/#setup> "Permanent link")

  1. **Install LiteLLM:** ADK requires `litellm>=1.84`. 
         
         [](<https://adk.dev/agents/models/litellm/#__codelineno-1-1>)pip install "litellm>=1.84"
         
  2. **Set Provider API Keys:** Configure API keys as environment variables for the specific providers you intend to use.

     * _Example for OpenAI:_
           
           [](<https://adk.dev/agents/models/litellm/#__codelineno-2-1>)export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
           
     * _Example for Anthropic (non-Agent Platform):_
           
           [](<https://adk.dev/agents/models/litellm/#__codelineno-3-1>)export ANTHROPIC_API_KEY="YOUR_ANTHROPIC_API_KEY"
           
     * _Consult the[LiteLLM Providers Documentation](<https://docs.litellm.ai/docs/providers>) for the correct environment variable names for other providers._

## Example implementation[¶](<https://adk.dev/agents/models/litellm/#example-implementation> "Permanent link")
    
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-2>)from google.adk.models.lite_llm import LiteLlm
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-3>)
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-4>)# --- Example Agent using OpenAI's GPT-4o ---
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-5>)# (Requires OPENAI_API_KEY)
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-6>)agent_openai = LlmAgent(
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-7>)    model=LiteLlm(model="openai/gpt-4o"), # LiteLLM model string format
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-8>)    name="openai_agent",
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-9>)    instruction="You are a helpful assistant powered by GPT-4o.",
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-10>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-11>))
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-12>)
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-13>)# --- Example Agent using Anthropic's Claude Haiku (non-Vertex) ---
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-14>)# (Requires ANTHROPIC_API_KEY)
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-15>)agent_claude_direct = LlmAgent(
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-16>)    model=LiteLlm(model="anthropic/claude-3-haiku-20240307"),
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-17>)    name="claude_direct_agent",
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-18>)    instruction="You are an assistant powered by Claude Haiku.",
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-19>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/litellm/#__codelineno-4-20>))
    
## Anthropic thinking blocks[¶](<https://adk.dev/agents/models/litellm/#anthropic-thinking-blocks> "Permanent link")

Supported in ADKPython v1.28.0

When you use Anthropic Claude models (such as Claude 3.7 Sonnet) through the `LiteLlm` connector, ADK supports Anthropic's structured reasoning feature, known as "thinking blocks". ADK automatically extracts the `thinking_blocks` and their signatures.

Anthropic requires these signatures to be sent back in multi-turn conversations, and otherwise silently drops thinking after the first turn. ADK rebuilds the `thinking_blocks` with their signatures on each outbound request, so Claude's reasoning is preserved across tool calls and multi-turn interactions without any custom state management on your part.

Back to top 