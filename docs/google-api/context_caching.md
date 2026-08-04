# Model context caching - Agent Development Kit (ADK)

> Source: [https://adk.dev/context/caching/](https://adk.dev/context/caching/)

[ Skip to content ](<https://adk.dev/context/caching/#context-caching-with-gemini>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/context/caching.md> "Edit this page on GitHub") [ ](<https://adk.dev/context/caching/index.md> "View this page as Markdown")

# Context caching with Gemini[¶](<https://adk.dev/context/caching/#context-caching-with-gemini> "Permanent link")

Supported in ADKPython v1.15.0Java v0.1.0

When working with agents to complete tasks, you may want to reuse extended instructions or large sets of data across multiple agent requests to a generative AI model. Resending this data for each agent request is slow, inefficient, and can be expensive. Using context caching features in generative AI models can significantly speed up responses and lower the number of tokens sent to the model for each request.

The ADK Context Caching feature allows you to cache request data with generative AI models that support it, including Gemini 2.0 and higher models. This document explains how to configure and use this feature.

## Configure context caching[¶](<https://adk.dev/context/caching/#configure-context-caching> "Permanent link")

You configure the context caching feature at the ADK `App` object level, which wraps your agent. Use the `ContextCacheConfig` class to configure these settings, as shown in the following code sample:

PythonJava
    
    [](<https://adk.dev/context/caching/#__codelineno-0-1>)from google.adk import Agent
    [](<https://adk.dev/context/caching/#__codelineno-0-2>)from google.adk.apps.app import App
    [](<https://adk.dev/context/caching/#__codelineno-0-3>)from google.adk.agents.context_cache_config import ContextCacheConfig
    [](<https://adk.dev/context/caching/#__codelineno-0-4>)
    [](<https://adk.dev/context/caching/#__codelineno-0-5>)root_agent = Agent(
    [](<https://adk.dev/context/caching/#__codelineno-0-6>)  # configure an agent using Gemini 2.0 or higher
    [](<https://adk.dev/context/caching/#__codelineno-0-7>))
    [](<https://adk.dev/context/caching/#__codelineno-0-8>)
    [](<https://adk.dev/context/caching/#__codelineno-0-9>)# Create the app with context caching configuration
    [](<https://adk.dev/context/caching/#__codelineno-0-10>)app = App(
    [](<https://adk.dev/context/caching/#__codelineno-0-11>)    name='my-caching-agent-app',
    [](<https://adk.dev/context/caching/#__codelineno-0-12>)    root_agent=root_agent,
    [](<https://adk.dev/context/caching/#__codelineno-0-13>)    context_cache_config=ContextCacheConfig(
    [](<https://adk.dev/context/caching/#__codelineno-0-14>)        min_tokens=2048,    # Minimum tokens to trigger caching
    [](<https://adk.dev/context/caching/#__codelineno-0-15>)        ttl_seconds=600,    # Store for up to 10 minutes
    [](<https://adk.dev/context/caching/#__codelineno-0-16>)        cache_intervals=5,  # Refresh after 5 uses
    [](<https://adk.dev/context/caching/#__codelineno-0-17>)    ),
    [](<https://adk.dev/context/caching/#__codelineno-0-18>))
    
    [](<https://adk.dev/context/caching/#__codelineno-1-1>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/context/caching/#__codelineno-1-2>)import com.google.adk.agents.ContextCacheConfig;
    [](<https://adk.dev/context/caching/#__codelineno-1-3>)import com.google.adk.apps.App;
    [](<https://adk.dev/context/caching/#__codelineno-1-4>)import java.time.Duration;
    [](<https://adk.dev/context/caching/#__codelineno-1-5>)
    [](<https://adk.dev/context/caching/#__codelineno-1-6>)// Create the app with context caching configuration
    [](<https://adk.dev/context/caching/#__codelineno-1-7>)App app = App.builder()
    [](<https://adk.dev/context/caching/#__codelineno-1-8>)             .name("my-caching-agent-app")
    [](<https://adk.dev/context/caching/#__codelineno-1-9>)             .rootAgent(rootAgent)
    [](<https://adk.dev/context/caching/#__codelineno-1-10>)             .contextCacheConfig(
    [](<https://adk.dev/context/caching/#__codelineno-1-11>)                 new ContextCacheConfig(
    [](<https://adk.dev/context/caching/#__codelineno-1-12>)                     5, /* cache_intervals (max invocations) */
    [](<https://adk.dev/context/caching/#__codelineno-1-13>)                     Duration.ofMinutes(10), /* ttl */
    [](<https://adk.dev/context/caching/#__codelineno-1-14>)                     2048 /* min_tokens */))
    [](<https://adk.dev/context/caching/#__codelineno-1-15>)             .build();
    
## Configuration settings[¶](<https://adk.dev/context/caching/#configuration-settings> "Permanent link")

The `ContextCacheConfig` class has the following settings that control how caching works for your agent. When you configure these settings, they apply to all agents within your app.

  * **`min_tokens`** (int): The minimum number of tokens required in a request to enable caching. This setting allows you to avoid the overhead of caching for very small requests where the performance benefit would be negligible. Defaults to `0`.
  * **`ttl_seconds`** (int): The time-to-live (TTL) for the cache in seconds. This setting determines how long the cached content is stored before it is refreshed. Defaults to `1800` (30 minutes).
  * **`cache_intervals`** (int): The maximum number of times the same cached content can be used before it expires. This setting allows you to control how frequently the cache is updated, even if the TTL has not expired. Defaults to `10`.

## Next steps[¶](<https://adk.dev/context/caching/#next-steps> "Permanent link")

For a full implementation of how to use and test the context caching feature, see the following sample:

  * [`cache_analysis`](<https://github.com/google/adk-python/tree/main/contributing/samples/context_management/cache_analysis>): A code sample that demonstrates how to analyze the performance of context caching.

If your use case requires that you provide instructions that are used throughout a session, consider using the `static_instruction` parameter for an agent, which allows you to amend the system instructions for a generative model. For more details, see this sample code:

  * [`static_instruction`](<https://github.com/google/adk-python/tree/main/contributing/samples/context_management/static_instruction>): An implementation of a digital pet agent using static instructions.

Back to top 