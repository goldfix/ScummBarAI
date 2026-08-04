# OpenAI - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/models/openai/](https://adk.dev/agents/models/openai/)

[ Skip to content ](<https://adk.dev/agents/models/openai/#openai-models-for-adk-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/models/openai.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/models/openai/index.md> "View this page as Markdown")

# OpenAI models for ADK agents[¶](<https://adk.dev/agents/models/openai/#openai-models-for-adk-agents> "Permanent link")

Supported in ADKGo v2.1.0Experimental

Experimental

The `openaimodel` package is experimental and its behavior may change or be removed in the future. We welcome your [feedback](<https://github.com/google/adk-go/issues/new?template=feature_request.md>)!

You can use OpenAI models with ADK. How you connect depends on the language:

  * **Go — native support:** ADK Go provides a direct `openaimodel` package that implements the `model.LLM` interface, targeting the OpenAI Responses API. [Get started](<https://adk.dev/agents/models/openai/#get-started>).
  * **Python — via LiteLLM:** ADK Python accesses OpenAI models (and many other providers) through the LiteLLM connector. See [LiteLLM](<https://adk.dev/agents/models/litellm/>).

## Get started[¶](<https://adk.dev/agents/models/openai/#get-started> "Permanent link")

The `openaimodel` package provides a client for interacting with OpenAI's API. It implements the `model.LLM` interface, making it compatible with providers that expose the OpenAI Responses API surface. The following code example shows a basic implementation for using OpenAI models in your agents:

Go
    
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-1>)import (
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-2>)    "context"
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-3>)    "log"
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-4>)
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-5>)    "github.com/openai/openai-go/v3"
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-6>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-7>)    "google.golang.org/adk/v2/model/openaimodel"
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-8>))
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-9>)
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-10>)// Instantiate the model
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-11>)llm, err := openaimodel.NewModel(context.Background(), openai.ChatModelGPT4oMini, &openaimodel.ClientConfig{})
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-12>)if err != nil {
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-13>)  log.Fatal(err)
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-14>)}
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-15>)
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-16>)// Create the agent
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-17>)agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-18>)  Name:        "openai_agent",
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-19>)  Model:       llm,
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-20>)  Instruction: "You are a helpful AI assistant.",
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-21>)})
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-22>)if err != nil {
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-23>)  log.Fatal(err)
    [](<https://adk.dev/agents/models/openai/#__codelineno-0-24>)}
    
For a complete, runnable sample, see [examples/openai/](<https://github.com/google/adk-go/tree/main/examples/openai>) in the ADK Go repository.

## Supported features[¶](<https://adk.dev/agents/models/openai/#supported-features> "Permanent link")

  * Text generation (streaming and non-streaming)
  * Function (tool) calling
  * Structured output via `OutputSchema` (JSON schema)
  * Reasoning models (e.g. o-series), including reasoning-token accounting
  * Token logprobs

## Limitations[¶](<https://adk.dev/agents/models/openai/#limitations> "Permanent link")

  * **Text only** — multimodal input (images, audio, files) is not supported.
  * **Function tools only** — built-in tools (Google Search, code execution, etc.) are not supported.
  * **Structured output uses OpenAI strict mode** — every field declared in an `OutputSchema` is treated as required.
  * Some `GenerateContentConfig` options return an error rather than being silently ignored: `TopK`, stop sequences, multiple candidates, frequency/presence penalties, request labels, and safety settings.

## Configuration options[¶](<https://adk.dev/agents/models/openai/#configuration-options> "Permanent link")

The `ClientConfig` provides several options for configuring the client:

  * `APIKey`: Your OpenAI API key.
  * `BaseURL`: Custom endpoint URL, which can be useful for OpenAI-compatible endpoints.
  * `HTTPClient`: A custom `*http.Client`.
  * `Options`: Advanced `openai-go` request options (`[]option.RequestOption`).

If `APIKey` or `BaseURL` are left empty, they will automatically fall back to the `OPENAI_API_KEY` and `OPENAI_BASE_URL` environment variables, handled by the default behavior of the underlying `openai-go` SDK.

## OpenAI model authentication[¶](<https://adk.dev/agents/models/openai/#openai-model-authentication> "Permanent link")

When using OpenAI models, you must provide an API key to authenticate with the OpenAI API. The most direct way to provide this information is to use environment variables or an `.env` file.

The `openaimodel` package also supports OpenAI-compatible endpoints (such as local models served via Ollama, LM Studio, or vLLM) by configuring the base URL.

OpenAI APIOpenAI-compatible Endpoint
    
    [](<https://adk.dev/agents/models/openai/#__codelineno-1-1>)# .env configuration file
    [](<https://adk.dev/agents/models/openai/#__codelineno-1-2>)OPENAI_API_KEY="PASTE_YOUR_OPENAI_API_KEY_HERE"
    
    [](<https://adk.dev/agents/models/openai/#__codelineno-2-1>)# .env configuration file
    [](<https://adk.dev/agents/models/openai/#__codelineno-2-2>)OPENAI_API_KEY="api-key-if-required"
    [](<https://adk.dev/agents/models/openai/#__codelineno-2-3>)OPENAI_BASE_URL="http://localhost:11434/v1" # example: local Ollama endpoint
    
Back to top 