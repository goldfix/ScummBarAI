# Agent Platform hosted - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/models/agent-platform/](https://adk.dev/agents/models/agent-platform/)

[ Skip to content ](<https://adk.dev/agents/models/agent-platform/#agent-platform-hosted-models-for-adk-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/models/agent-platform.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/models/agent-platform/index.md> "View this page as Markdown")

# Agent Platform hosted models for ADK agents[¶](<https://adk.dev/agents/models/agent-platform/#agent-platform-hosted-models-for-adk-agents> "Permanent link")

For enterprise-grade scalability, reliability, and integration with Google Cloud's MLOps ecosystem, you can use models deployed to Agent Platform Endpoints. This includes models from Model Garden or your own fine-tuned models.

**Integration Method:** Pass the full Agent Platform Endpoint resource string (`projects/PROJECT_ID/locations/LOCATION/endpoints/ENDPOINT_ID`) directly to the `model` parameter of `LlmAgent`.

## Agent Platform Setup[¶](<https://adk.dev/agents/models/agent-platform/#agent-platform-setup> "Permanent link")

For more details on connecting ADK agents to Google Cloud hosted models and services, including Gemini Enterprise Agent Platform, see the [Connect to Google Cloud and Agent Platform](<https://adk.dev/get-started/google-cloud/>) guide.

## Model Garden Deployments[¶](<https://adk.dev/agents/models/agent-platform/#model-garden-deployments> "Permanent link")

Supported in ADKPython v0.2.0Java v0.1.0

You can deploy various open and proprietary models from the [Model Garden](<https://console.cloud.google.com/vertex-ai/model-garden>) to an endpoint.

**Example:**

PythonJava
    
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-2>)from google.genai import types # For config objects
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-3>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-4>)# --- Example Agent using a Llama 3 model deployed from Model Garden ---
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-5>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-6>)# Replace with your actual Agent Platform Endpoint resource name
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-7>)llama3_endpoint = "projects/YOUR_PROJECT_ID/locations/us-central1/endpoints/YOUR_LLAMA3_ENDPOINT_ID"
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-8>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-9>)agent_llama3_vertex = LlmAgent(
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-10>)    model=llama3_endpoint,
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-11>)    name="llama3_vertex_agent",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-12>)    instruction="You are a helpful assistant based on Llama 3, hosted on Agent Platform.",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-13>)    generate_content_config=types.GenerateContentConfig(max_output_tokens=2048),
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-14>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-0-15>))
    
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-2>)import com.google.adk.models.Gemini;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-3>)import com.google.genai.types.GenerateContentConfig;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-4>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-5>)// ...
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-6>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-7>)// Replace with your actual Agent Platform Endpoint resource name
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-8>)String llama3Endpoint = "projects/YOUR_PROJECT_ID/locations/us-central1/endpoints/YOUR_LLAMA3_ENDPOINT_ID";
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-9>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-10>)LlmAgent agentLlama3Vertex = LlmAgent.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-11>)    .model(Gemini.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-12>)        .modelName(llama3Endpoint)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-13>)        .build())
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-14>)    .name("llama3_vertex_agent")
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-15>)    .instruction("You are a helpful assistant based on Llama 3, hosted on Agent Platform.")
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-16>)    .generateContentConfig(GenerateContentConfig.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-17>)        .maxOutputTokens(2048)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-18>)        .build())
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-19>)    // ... other agent parameters
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-1-20>)    .build();
    
## Fine-tuned Model Endpoints[¶](<https://adk.dev/agents/models/agent-platform/#fine-tuned-model-endpoints> "Permanent link")

Supported in ADKPython v0.2.0Java v0.1.0

Deploying your fine-tuned models (whether based on Gemini or other architectures supported by Agent Platform) results in an endpoint that can be used directly.

**Example:**

PythonJava
    
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-2>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-3>)# --- Example Agent using a fine-tuned Gemini model endpoint ---
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-4>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-5>)# Replace with your fine-tuned model's endpoint resource name
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-6>)finetuned_gemini_endpoint = "projects/YOUR_PROJECT_ID/locations/us-central1/endpoints/YOUR_FINETUNED_ENDPOINT_ID"
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-7>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-8>)agent_finetuned_gemini = LlmAgent(
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-9>)    model=finetuned_gemini_endpoint,
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-10>)    name="finetuned_gemini_agent",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-11>)    instruction="You are a specialized assistant trained on specific data.",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-12>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-2-13>))
    
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-2>)import com.google.adk.models.Gemini;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-3>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-4>)// ...
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-5>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-6>)// Replace with your fine-tuned model's endpoint resource name
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-7>)String finetunedGeminiEndpoint = "projects/YOUR_PROJECT_ID/locations/us-central1/endpoints/YOUR_FINETUNED_ENDPOINT_ID";
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-8>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-9>)LlmAgent agentFinetunedGemini = LlmAgent.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-10>)    .model(Gemini.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-11>)        .modelName(finetunedGeminiEndpoint)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-12>)        .build())
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-13>)    .name("finetuned_gemini_agent")
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-14>)    .instruction("You are a specialized assistant trained on specific data.")
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-15>)    // ... other agent parameters
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-3-16>)    .build();
    
## Anthropic Claude on Agent Platform[¶](<https://adk.dev/agents/models/agent-platform/#anthropic-claude> "Permanent link")

Supported in ADKPython v0.2.0Java v0.1.0

Some providers, like Anthropic, make their models available directly through Agent Platform.

**Example:**

PythonJava

**Integration Method:** Uses the direct model string (e.g., `"claude-3-sonnet@20240229"`).

**How Resolution Works:** ADK's registry automatically recognizes `gemini-*` strings and standard Agent Platform endpoint strings (`projects/.../locations/.../endpoints/...`) and routes them via the `google-genai` library. Claude model strings matching `claude-3-*` or `claude-*-4*` route to the `Claude` wrapper class the same way. For a Claude model identifier that does not match those patterns, import `Claude` from `google.adk.models` and pass an instance instead of a string: `LlmAgent(model=Claude(model="..."), ...)`.

**Setup:**

  1. **Agent Platform Environment:** Ensure the consolidated Agent Platform setup (ADC, Env Vars, `GOOGLE_GENAI_USE_ENTERPRISE=TRUE`) is complete.

  2. **Install Provider Library:** Install the necessary client library configured for Agent Platform.
         
         [](<https://adk.dev/agents/models/agent-platform/#__codelineno-4-1>)pip install "anthropic[vertex]"
         
  3. **Create the Agent:** Pass the Claude model string to `LlmAgent`:

    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-2>)from google.genai import types
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-3>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-4>)# --- Example Agent using Claude 3 Sonnet on Agent Platform ---
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-5>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-6>)# Standard model name for Claude 3 Sonnet on Agent Platform
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-7>)claude_model_vertexai = "claude-3-sonnet@20240229"
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-8>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-9>)agent_claude_vertexai = LlmAgent(
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-10>)    model=claude_model_vertexai, # Pass the direct model string
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-11>)    name="claude_vertexai_agent",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-12>)    instruction="You are an assistant powered by Claude 3 Sonnet on Agent Platform.",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-13>)    generate_content_config=types.GenerateContentConfig(max_output_tokens=4096),
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-14>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-5-15>))
    
**Integration Method:** Directly instantiate the provider-specific model class (e.g., `com.google.adk.models.Claude`) and configure it with an Agent Platform backend.

**Why Direct Instantiation?** The Java ADK's `LlmRegistry` primarily handles Gemini models by default. For third-party models like Claude on Agent Platform, you directly provide an instance of the ADK's wrapper class (e.g., `Claude`) to the `LlmAgent`. This wrapper class is responsible for interacting with the model via its specific client library, configured for Agent Platform.

**Setup:**

  1. **Agent Platform Environment:**

     * Ensure your Google Cloud project and region are correctly set up.
     * **Application Default Credentials (ADC):** Make sure ADC is configured correctly in your environment. This is typically done by running `gcloud auth application-default login`. The Java client libraries use these credentials to authenticate with Agent Platform. Follow the [Google Cloud Java documentation on ADC](<https://cloud.google.com/java/docs/reference/google-auth-library/latest/com.google.auth.oauth2.GoogleCredentials#com_google_auth_oauth2_GoogleCredentials_getApplicationDefault__>) for detailed setup.
  2. **Provider Library Dependencies:**

     * **Third-Party Client Libraries (Often Transitive):** The ADK core library often includes the necessary client libraries for common third-party models on Agent Platform (like Anthropic's required classes) as **transitive dependencies**. This means you might not need to explicitly add a separate dependency for the Anthropic Vertex SDK in your `pom.xml` or `build.gradle`.
  3. **Instantiate and Configure the Model:** When creating your `LlmAgent`, instantiate the `Claude` class (or the equivalent for another provider) and configure its `VertexBackend`.

    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-1>)import com.anthropic.client.AnthropicClient;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-2>)import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-3>)import com.anthropic.vertex.backends.VertexBackend;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-4>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-5>)import com.google.adk.models.Claude; // ADK's wrapper for Claude
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-6>)import com.google.auth.oauth2.GoogleCredentials;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-7>)import java.io.IOException;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-8>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-9>)// ... other imports
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-10>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-11>)public class ClaudeVertexAiAgent {
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-12>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-13>)    public static LlmAgent createAgent() throws IOException {
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-14>)        // Model name for Claude 3 Sonnet on Agent Platform (or other versions)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-15>)        String claudeModelVertexAi = "claude-3-7-sonnet"; // Or any other Claude model
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-16>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-17>)        // Configure the AnthropicOkHttpClient with the VertexBackend
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-18>)        AnthropicClient anthropicClient = AnthropicOkHttpClient.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-19>)            .backend(
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-20>)                VertexBackend.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-21>)                    .region("us-east5") // Specify your Agent Platform region
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-22>)                    .project("your-gcp-project-id") // Specify your GCP Project ID
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-23>)                    .googleCredentials(GoogleCredentials.getApplicationDefault())
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-24>)                    .build())
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-25>)            .build();
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-26>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-27>)        // Instantiate LlmAgent with the ADK Claude wrapper
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-28>)        LlmAgent agentClaudeVertexAi = LlmAgent.builder()
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-29>)            .model(new Claude(claudeModelVertexAi, anthropicClient)) // Pass the Claude instance
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-30>)            .name("claude_vertexai_agent")
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-31>)            .instruction("You are an assistant powered by Claude 3 Sonnet on Agent Platform.")
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-32>)            // .generateContentConfig(...) // Optional: Add generation config if needed
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-33>)            // ... other agent parameters
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-34>)            .build();
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-35>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-36>)        return agentClaudeVertexAi;
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-37>)    }
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-38>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-39>)    public static void main(String[] args) {
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-40>)        try {
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-41>)            LlmAgent agent = createAgent();
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-42>)            System.out.println("Successfully created agent: " + agent.name());
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-43>)            // Here you would typically set up a Runner and Session to interact with the agent
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-44>)        } catch (IOException e) {
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-45>)            System.err.println("Failed to create agent: " + e.getMessage());
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-46>)            e.printStackTrace();
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-47>)        }
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-48>)    }
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-6-49>)}
    
### Adaptive thinking[¶](<https://adk.dev/agents/models/agent-platform/#adaptive-thinking> "Permanent link")

Supported in ADKPython v1.34.0

Newer Claude models support _adaptive_ extended thinking, where the model chooses its reasoning depth itself rather than using a fixed token budget. On the native Claude path, a negative `thinking_budget` maps to adaptive thinking.

The recommended way to control reasoning depth is the `effort` field on `AnthropicGenerateContentConfig`:
    
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-2>)from google.adk.models import AnthropicGenerateContentConfig
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-3>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-4>)agent = LlmAgent(
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-5>)    model="claude-sonnet-4@20250514",  # Your Agent Platform Claude model ID.
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-6>)    name="claude_reasoning_agent",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-7>)    instruction="You are a helpful assistant.",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-8>)    generate_content_config=AnthropicGenerateContentConfig(
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-9>)        effort="high",  # One of: "low", "medium", "high", "xhigh", "max".
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-10>)    ),
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-7-11>))
    
  * The standard `thinking_config.thinking_level` is not supported for Claude. Setting it on `AnthropicGenerateContentConfig` raises a validation error; on a plain `types.GenerateContentConfig` it is ignored with a warning. Use `effort` instead.

## Open Models on Agent Platform[¶](<https://adk.dev/agents/models/agent-platform/#open-models> "Permanent link")

Supported in ADKPython v0.1.0Java v0.1.0

Agent Platform offers a curated selection of open-source models, such as Meta Llama, through Model-as-a-Service (MaaS). These models are accessible via managed APIs, allowing you to deploy and scale without managing the underlying infrastructure. For a full list of available options, see the [Agent Platform open models for MaaS](<https://docs.cloud.google.com/vertex-ai/generative-ai/docs/maas/use-open-models#open-models>) documentation.

Python

You can use the [LiteLLM](<https://docs.litellm.ai/>) library to access open models like Meta's Llama on Agent Platform MaaS

**Integration Method:** Use the `LiteLlm` wrapper class and set it as the `model` parameter of `LlmAgent`. Make sure you go through the [LiteLLM model connector for ADK agents](<https://adk.dev/agents/models/litellm/#litellm-model-connector-for-adk-agents>) documentation on how to use LiteLLM in ADK

**Setup:**

  1. **Agent Platform Environment:** Ensure the consolidated Agent Platform setup (ADC, Env Vars, `GOOGLE_GENAI_USE_ENTERPRISE=TRUE`) is complete.

  2. **Install LiteLLM:** ADK requires `litellm>=1.84`. 
         
         [](<https://adk.dev/agents/models/agent-platform/#__codelineno-8-1>)pip install "litellm>=1.84"
         
**Example:**
    
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-2>)from google.adk.models.lite_llm import LiteLlm
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-3>)
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-4>)# --- Example Agent using Meta's Llama 4 Scout ---
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-5>)agent_llama_vertexai = LlmAgent(
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-6>)    model=LiteLlm(model="vertex_ai/meta/llama-4-scout-17b-16e-instruct-maas"), # LiteLLM model string format
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-7>)    name="llama4_agent",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-8>)    instruction="You are a helpful assistant powered by Llama 4 Scout.",
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-9>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/agent-platform/#__codelineno-9-10>))
    
Back to top 