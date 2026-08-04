# Gemini - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/models/google-gemini/](https://adk.dev/agents/models/google-gemini/)

[ Skip to content ](<https://adk.dev/agents/models/google-gemini/#google-gemini-models-for-adk-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/models/google-gemini.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/models/google-gemini/index.md> "View this page as Markdown")

# Google Gemini models for ADK agents[¶](<https://adk.dev/agents/models/google-gemini/#google-gemini-models-for-adk-agents> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.2.0Kotlin v0.1.0

ADK supports the Google Gemini family of generative AI models that provide a powerful set of models with a wide range of features. ADK provides support for many Gemini features, including [Code Execution](<https://adk.dev/integrations/code-execution/>), [Google Search](<https://adk.dev/integrations/google-search/>), [Context caching](<https://adk.dev/context/caching/>), [Computer use](<https://adk.dev/integrations/computer-use/>) and the [Interactions API](<https://adk.dev/agents/models/google-gemini/#interactions-api>).

## Get started[¶](<https://adk.dev/agents/models/google-gemini/#get-started> "Permanent link")

The following code examples show a basic implementation for using Gemini models in your agents:

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-2>)
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-3>)# --- Example using a stable Gemini Flash model ---
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-4>)agent_gemini_flash = LlmAgent(
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-5>)    # Use the latest stable Flash model identifier
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-6>)    model="gemini-flash-latest",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-7>)    name="gemini_flash_agent",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-8>)    instruction="You are a fast and helpful Gemini assistant.",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-9>)    # ... other agent parameters
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-0-10>))
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-1>)import {LlmAgent} from '@google/adk';
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-2>)
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-3>)// --- Example #2: using a powerful Gemini Pro model with API Key in model ---
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-4>)export const rootAgent = new LlmAgent({
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-5>)  name: 'hello_time_agent',
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-6>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-7>)  description: 'Gemini flash agent',
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-8>)  instruction: `You are a fast and helpful Gemini assistant.`,
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-1-9>)});
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-1>)import (
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-2>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-3>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-4>)    "google.golang.org/genai"
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-5>))
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-6>)
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-7>)// --- Example using a stable Gemini Flash model ---
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-8>)modelFlash, err := gemini.NewModel(ctx, "gemini-2.0-flash", &genai.ClientConfig{})
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-9>)if err != nil {
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-10>)    log.Fatalf("failed to create model: %v", err)
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-11>)}
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-12>)agentGeminiFlash, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-13>)    // Use the latest stable Flash model identifier
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-14>)    Model:       modelFlash,
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-15>)    Name:        "gemini_flash_agent",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-16>)    Instruction: "You are a fast and helpful Gemini assistant.",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-17>)    // ... other agent parameters
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-18>)})
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-19>)if err != nil {
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-20>)    log.Fatalf("failed to create agent: %v", err)
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-2-21>)}
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-1>)// --- Example #1: using a stable Gemini Flash model with ENV variables---
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-2>)LlmAgent agentGeminiFlash =
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-3>)    LlmAgent.builder()
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-4>)        // Use the latest stable Flash model identifier
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-5>)        .model("gemini-flash-latest") // Set ENV variables to use this model
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-6>)        .name("gemini_flash_agent")
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-7>)        .instruction("You are a fast and helpful Gemini assistant.")
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-8>)        // ... other agent parameters
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-3-9>)        .build();
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-1>)import com.google.adk.kt.agents.Instruction
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-2>)import com.google.adk.kt.agents.LlmAgent
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-3>)import com.google.adk.kt.models.Gemini
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-4>)
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-5>)// --- Example using a stable Gemini Flash model ---
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-6>)val agentGeminiFlash = LlmAgent(
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-7>)    // Use the latest stable Flash model identifier
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-8>)    name = "gemini_flash_agent",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-9>)    model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-10>)    instruction = Instruction("You are a fast and helpful Gemini assistant."),
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-11>)    // ... other agent parameters
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-4-12>))
    
Note: Gemini model selector `gemini-flash-latest`

Most code examples in ADK documentation use `gemini-flash-latest` to select the [latest available](<https://ai.google.dev/gemini-api/docs/models#latest>) Gemini Flash version. However, if you access Gemini from a regional endpoint, such as `us-central1`, this selection string may not work. In that case, use a specific model version string from the [Gemini models](<https://ai.google.dev/gemini-api/docs/models>) page or Google Cloud [Gemini models](<https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models>) list.

## Gemini model authentication[¶](<https://adk.dev/agents/models/google-gemini/#gemini-model-authentication> "Permanent link")

When using an AI model through a service, such as the Gemini API or Gemini Enterprise Agent Platform on Google Cloud, you must provide an API key or authenticate with the service. The most direct way to provide this information is to use environment variables or an `.env` file. The following examples show the most common way to configure an agent for use with the Gemini API or Gemini Enterprise Agent Platform.

Gemini APIGoogle Cloud Agent Platform
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-5-1>)# .env configuration file
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-5-2>)GOOGLE_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-6-1>)# .env configuration file
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-6-2>)GOOGLE_CLOUD_PROJECT=your-project-id
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-6-3>)GOOGLE_CLOUD_LOCATION=location-code        # example: us-central1
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-6-4>)GOOGLE_GENAI_USE_ENTERPRISE=True
    
For more details on connecting ADK agents to Google Cloud hosted models and services, including Gemini Enterprise Agent Platform, see the [Connect to Google Cloud and Agent Platform](<https://adk.dev/get-started/google-cloud/>) guide.

## Voice and video streaming support[¶](<https://adk.dev/agents/models/google-gemini/#voice-and-video-streaming-support> "Permanent link")

In order to use voice/video streaming in ADK, you will need to use Gemini models that support the Live API. You can find the **model ID(s)** that support the Gemini Live API in the documentation:

  * [Google AI Studio: Gemini Live API](<https://ai.google.dev/gemini-api/docs/models#live-api>)
  * [Agent Platform: Gemini Live API](<https://cloud.google.com/vertex-ai/generative-ai/docs/live-api>)

## Gemini Interactions API[¶](<https://adk.dev/agents/models/google-gemini/#interactions-api> "Permanent link")

Supported in ADKPython v1.21.0

The Gemini [Interactions API](<https://ai.google.dev/gemini-api/docs/interactions>) is an alternative to the **_generateContent_** inference API, which provides stateful conversation capabilities, allowing you to chain interactions using a `previous_interaction_id` instead of sending the full conversation history with each request. Using this feature can be more efficient for long conversations.

You can enable the Interactions API by setting the `use_interactions_api=True` parameter in the Gemini model configuration, as shown in the following code snippet:

Python
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-1>)from google.adk.agents.llm_agent import Agent
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-2>)from google.adk.models.google_llm import Gemini
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-3>)from google.adk.tools.google_search_tool import GoogleSearchTool
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-4>)
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-5>)root_agent = Agent(
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-6>)    model=Gemini(
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-7>)        model="gemini-flash-latest",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-8>)        use_interactions_api=True,  # Enable Interactions API
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-9>)    ),
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-10>)    name="interactions_test_agent",
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-11>)    tools=[
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-12>)        GoogleSearchTool(bypass_multi_tools_limit=True),  # Converted to function tool
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-13>)        get_current_weather,  # Custom function tool
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-14>)    ],
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-7-15>))
    
For a complete code sample, see the [Interactions API sample](<https://github.com/google/adk-python/tree/main/contributing/samples/models/interactions_api>).

### Known limitations[¶](<https://adk.dev/agents/models/google-gemini/#known-limitations> "Permanent link")

The Interactions API **does not** support mixing custom function calling tools with built-in tools, such as the [Google Search](<https://adk.dev/integrations/google-search/>), tool, within the same agent. You can work around this limitation by configuring the built-in tool to operate as a custom tool using the `bypass_multi_tools_limit` parameter:

Python
    
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-8-1>)# Use bypass_multi_tools_limit=True to convert google_search to a function tool
    [](<https://adk.dev/agents/models/google-gemini/#__codelineno-8-2>)GoogleSearchTool(bypass_multi_tools_limit=True)
    
In this example, this option converts the built-in `google_search` to a function calling tool (via `GoogleSearchAgentTool`), which allows it to work alongside custom function tools.

## Troubleshooting[¶](<https://adk.dev/agents/models/google-gemini/#troubleshooting> "Permanent link")

### Error Code 429 - RESOURCE_EXHAUSTED[¶](<https://adk.dev/agents/models/google-gemini/#error-code-429-resource_exhausted> "Permanent link")

This error usually happens if the number of your requests exceeds the capacity allocated to process requests.

To mitigate this, you can do one of the following:

  1. Request higher quota limits for the model you are trying to use.

  2. Enable client-side retries. Retries allow the client to automatically retry the request after a delay, which can help if the quota issue is temporary.

There are two ways you can set retry options:

**Option 1:** Set retry options on the Agent as a part of `generate_content_config`.

You would use this option if you are passing the model as a name string and letting ADK create the model adapter for you.

PythonJava
         
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-1>)from google.genai import types
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-2>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-3>)# ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-4>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-5>)root_agent = Agent(
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-6>)    model='gemini-flash-latest',
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-7>)    # ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-8>)    generate_content_config=types.GenerateContentConfig(
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-9>)        # ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-10>)        http_options=types.HttpOptions(
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-11>)            # ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-12>)            retry_options=types.HttpRetryOptions(initial_delay=1, attempts=2),
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-13>)            # ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-14>)        ),
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-15>)        # ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-16>)    ),
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-9-17>))
         
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-1>)import com.google.adk.agents.LlmAgent;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-2>)import com.google.genai.types.GenerateContentConfig;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-3>)import com.google.genai.types.HttpOptions;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-4>)import com.google.genai.types.HttpRetryOptions;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-5>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-6>)// ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-7>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-8>)LlmAgent rootAgent = LlmAgent.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-9>)    .model("gemini-flash-latest")
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-10>)    // ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-11>)    .generateContentConfig(GenerateContentConfig.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-12>)        // ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-13>)        .httpOptions(HttpOptions.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-14>)            // ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-15>)            .retryOptions(HttpRetryOptions.builder().initialDelay(1.0).attempts(2).build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-16>)            // ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-17>)            .build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-18>)        // ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-19>)        .build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-10-20>)    .build();
         
**Option 2:** Retry options on this model adapter.

You would use this option if you were instantiating the instance of adapter by yourself.

PythonJavaKotlin
         
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-1>)from google.genai import types
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-2>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-3>)# ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-4>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-5>)agent = Agent(
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-6>)    model=Gemini(
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-7>)    retry_options=types.HttpRetryOptions(initial_delay=1, attempts=2),
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-8>)    )
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-11-9>))
         
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-1>)import com.google.adk.agents.LlmAgent;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-2>)import com.google.adk.models.Gemini;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-3>)import com.google.genai.Client;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-4>)import com.google.genai.types.HttpOptions;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-5>)import com.google.genai.types.HttpRetryOptions;
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-6>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-7>)// ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-8>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-9>)LlmAgent agent = LlmAgent.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-10>)    .model(Gemini.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-11>)        .modelName("gemini-flash-latest")
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-12>)        .apiClient(Client.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-13>)            .httpOptions(HttpOptions.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-14>)                .retryOptions(HttpRetryOptions.builder().initialDelay(1.0).attempts(2).build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-15>)                .build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-16>)            .build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-17>)        .build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-12-18>)    .build();
         
In Kotlin, you can achieve this by creating the `Client` instance yourself and passing it to the `Gemini` constructor.
         
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-1>)import com.google.adk.kt.agents.LlmAgent
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-2>)import com.google.adk.kt.models.Gemini
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-3>)import com.google.genai.Client
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-4>)import com.google.genai.types.HttpOptions
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-5>)import com.google.genai.types.HttpRetryOptions
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-6>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-7>)val client = Client.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-8>)    .apiKey("YOUR_API_KEY")
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-9>)    .httpOptions(HttpOptions.builder()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-10>)        .retryOptions(HttpRetryOptions.builder().initialDelay(1.0).attempts(2).build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-11>)        .build())
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-12>)    .build()
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-13>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-14>)val model = Gemini(client = client, name = "gemini-flash-latest")
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-15>)
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-16>)val agent = LlmAgent(
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-17>)    name = "my_agent",
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-18>)    model = model
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-19>)    // ...
         [](<https://adk.dev/agents/models/google-gemini/#__codelineno-13-20>))
         
Back to top 