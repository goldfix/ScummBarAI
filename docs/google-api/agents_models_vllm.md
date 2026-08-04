# vLLM - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/models/vllm/](https://adk.dev/agents/models/vllm/)

[ Skip to content ](<https://adk.dev/agents/models/vllm/#vllm-model-host-for-adk-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/models/vllm.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/models/vllm/index.md> "View this page as Markdown")

# vLLM model host for ADK agents[¶](<https://adk.dev/agents/models/vllm/#vllm-model-host-for-adk-agents> "Permanent link")

Supported in ADKPython v0.1.0

Tools such as [vLLM](<https://github.com/vllm-project/vllm>) allow you to host models efficiently and serve them as an OpenAI-compatible API endpoint. You can use vLLM models through the [LiteLLM](<https://adk.dev/agents/models/litellm/>) library for Python.

## Setup[¶](<https://adk.dev/agents/models/vllm/#setup> "Permanent link")

  1. **Deploy Model:** Deploy your chosen model using vLLM (or a similar tool). Note the API base URL (e.g., `https://your-vllm-endpoint.run.app/v1`).
     * _Important for ADK Tools:_ When deploying, ensure the serving tool supports and enables OpenAI-compatible tool/function calling. For vLLM, this might involve flags like `--enable-auto-tool-choice` and potentially a specific `--tool-call-parser`, depending on the model. Refer to the vLLM documentation on Tool Use.
  2. **Authentication:** Determine how your endpoint handles authentication (e.g., API key, bearer token).

## Integration Example[¶](<https://adk.dev/agents/models/vllm/#integration-example> "Permanent link")

The following example shows how to use a vLLM endpoint with ADK agents.
    
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-1>)import subprocess
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-2>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-3>)from google.adk.models.lite_llm import LiteLlm
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-4>)
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-5>)# --- Example Agent using a Gemma 4 model hosted on a vLLM endpoint ---
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-6>)
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-7>)# Endpoint URL provided by your vLLM deployment
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-8>)api_base_url = "https://your-vllm-endpoint.run.app/v1"
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-9>)
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-10>)# Model name as recognized by *your* vLLM endpoint configuration
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-11>)model_name_at_endpoint = "hosted_vllm/google/gemma-4-E4B-it" # Example from vllm_test.py
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-12>)
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-13>)# Authentication (Example: using gcloud identity token for a Cloud Run deployment)
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-14>)# Adapt this based on your endpoint's security
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-15>)try:
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-16>)    gcloud_token = subprocess.check_output(
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-17>)        ["gcloud", "auth", "print-identity-token", "-q"]
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-18>)    ).decode().strip()
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-19>)    auth_headers = {"Authorization": f"Bearer {gcloud_token}"}
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-20>)except Exception as e:
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-21>)    print(f"Warning: Could not get gcloud token - {e}. Endpoint might be unsecured or require different auth.")
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-22>)    auth_headers = None # Or handle error appropriately
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-23>)
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-24>)agent_vllm = LlmAgent(
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-25>)    model=LiteLlm(
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-26>)        model=model_name_at_endpoint,
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-27>)        api_base=api_base_url,
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-28>)        # This extra_body values specific to Gemma 4.
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-29>)        extra_body={
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-30>)            "chat_template_kwargs": {
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-31>)                "enable_thinking": True # Enable thinking
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-32>)            },
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-33>)            "skip_special_tokens": False # Should be set to False
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-34>)        },
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-35>)        # Pass authentication headers if needed
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-36>)        extra_headers=auth_headers,
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-37>)        # Alternatively, if endpoint uses an API key:
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-38>)        # api_key="YOUR_ENDPOINT_API_KEY"
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-39>)    ),
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-40>)    name="vllm_agent",
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-41>)    instruction="You are a helpful assistant running on a self-hosted vLLM endpoint.",
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-42>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/vllm/#__codelineno-0-43>))
    
Back to top 