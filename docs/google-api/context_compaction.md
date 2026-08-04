# Context compression - Agent Development Kit (ADK)

> Source: [https://adk.dev/context/compaction/](https://adk.dev/context/compaction/)

[ Skip to content ](<https://adk.dev/context/compaction/#compress-agent-context-for-performance>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/context/compaction.md> "Edit this page on GitHub") [ ](<https://adk.dev/context/compaction/index.md> "View this page as Markdown")

# Compress agent context for performance[¶](<https://adk.dev/context/compaction/#compress-agent-context-for-performance> "Permanent link")

Supported in ADKPython v1.16.0Java v0.2.0TypeScript v0.6.0

As an ADK agent runs it collects _context_ information, including user instructions, retrieved data, tool responses, and generated content. As the size of this context data grows, agent processing times typically also increase. More and more data is sent to the generative AI model used by the agent, increasing processing time and slowing down responses. ADK Context Compaction feature is designed to reduce the size of context as an agent is running by summarizing older session history—including instructions, inputs, and model responses. By maintaining a compact context window, this process **optimizes latency and reduces costs** while ensuring the agent retains access to essential recent interactions.

Compaction is integrated directly into SingleFlow via the `CompactionRequestProcessor`, allowing automatic event compaction based on the rules you set in the `EventsCompactionConfig`.

## Choose your strategy[¶](<https://adk.dev/context/compaction/#choose-your-strategy> "Permanent link")

You can manage your session's data using the following strategies within `EventsCompactionConfig`:

  * **Token-Based (Primary)** : Triggers cleanup based on the actual volume of tokens consumed. This acts as an absolute safety net and is ideal for unpredictable workloads, like when users paste massive code blocks or upload large files.
  * **Sliding Window (Turn-Based)** : Triggers cleanup after a fixed number of conversational turns. This is useful for regular, predictable text chats.

If you configure both compaction strategies, the system prioritizes token-based compaction. When the session length exceeds your defined token threshold, the system triggers token-based compaction and skips sliding-window compaction for that turn.

## Token-based compaction[¶](<https://adk.dev/context/compaction/#token-based-compaction> "Permanent link")

Token-based compaction triggers context management based on the volume of tokens or data, rather than the number of events or turns.

### Configuration settings[¶](<https://adk.dev/context/compaction/#configuration-settings> "Permanent link")

Add token-based compaction to your agent workflow by adding an `EventsCompactionConfig` setting to the App object. You must specify the following:

  * **`token_threshold`** : The safety limit of tokens that automatically triggers tail-retention compaction once reached.
  * **`event_retention_size`** : The number of recent events/interactions kept in "raw" un-compacted format when compaction is triggered. This maintains immediate conversational context and pronoun resolution.

To implement this in your project, use the following configuration:
    
    [](<https://adk.dev/context/compaction/#__codelineno-0-1>)# 1. Correct the import path to use the google.adk namespace
    [](<https://adk.dev/context/compaction/#__codelineno-0-2>)from google.adk.apps.app import App, EventsCompactionConfig
    [](<https://adk.dev/context/compaction/#__codelineno-0-3>)from google.adk.agents import Agent
    [](<https://adk.dev/context/compaction/#__codelineno-0-4>)
    [](<https://adk.dev/context/compaction/#__codelineno-0-5>)# 2. Initialize your root agent (required for App setup)
    [](<https://adk.dev/context/compaction/#__codelineno-0-6>)root_agent = Agent(
    [](<https://adk.dev/context/compaction/#__codelineno-0-7>)    name="my_root_agent",
    [](<https://adk.dev/context/compaction/#__codelineno-0-8>)    description="Main coordinating agent for the workflow."
    [](<https://adk.dev/context/compaction/#__codelineno-0-9>))
    [](<https://adk.dev/context/compaction/#__codelineno-0-10>)
    [](<https://adk.dev/context/compaction/#__codelineno-0-11>)# 3. Token-based configuration: Activates the priority/pre-call layer
    [](<https://adk.dev/context/compaction/#__codelineno-0-12>)compaction_config = EventsCompactionConfig(
    [](<https://adk.dev/context/compaction/#__codelineno-0-13>)    token_threshold=4000,     # Triggers compaction when actual token count exceeds this
    [](<https://adk.dev/context/compaction/#__codelineno-0-14>)    event_retention_size=5    # Number of recent raw events to keep intact when token limit is hit
    [](<https://adk.dev/context/compaction/#__codelineno-0-15>))
    [](<https://adk.dev/context/compaction/#__codelineno-0-16>)
    [](<https://adk.dev/context/compaction/#__codelineno-0-17>)# 4. Register with required name and root_agent fields, and the config object
    [](<https://adk.dev/context/compaction/#__codelineno-0-18>)app = App(
    [](<https://adk.dev/context/compaction/#__codelineno-0-19>)    name="my_compacting_agent_app",
    [](<https://adk.dev/context/compaction/#__codelineno-0-20>)    root_agent=root_agent,
    [](<https://adk.dev/context/compaction/#__codelineno-0-21>)    events_compaction_config=compaction_config
    [](<https://adk.dev/context/compaction/#__codelineno-0-22>))
    
## Sliding window compaction[¶](<https://adk.dev/context/compaction/#sliding-window-compaction> "Permanent link")

The Context Compaction feature uses a _sliding window_ approach for collecting and summarizing agent workflow event data within a [Session](<https://adk.dev/sessions/session/>). When you configure this feature in your agent, it summarizes data from older events once it reaches a threshold of a specific number of workflow events, or invocations, with the current Session.
    
    [](<https://adk.dev/context/compaction/#__codelineno-1-1>)# (Optional) Event-based, sliding window as supplementary setting
    [](<https://adk.dev/context/compaction/#__codelineno-1-2>)compaction_config = EventsCompactionConfig(
    [](<https://adk.dev/context/compaction/#__codelineno-1-3>)    compaction_interval=10,   # Number of turns between standard compactions
    [](<https://adk.dev/context/compaction/#__codelineno-1-4>)    overlap_size=2,           # Number of events to retain as overlapping context
    
## Configure context compaction[¶](<https://adk.dev/context/compaction/#configure-context-compaction> "Permanent link")

Add context compaction to your agent workflow by adding an Events Compaction Configuration setting to the App object (Python/Java) or by configuring `contextCompactors` on the `LlmAgent` (TypeScript). As part of the configuration, you must specify a compaction interval and overlap size (Python/Java) or a token threshold and event retention size (TypeScript), as shown in the following sample code:

PythonJavaTypeScript
    
    [](<https://adk.dev/context/compaction/#__codelineno-2-1>)from google.adk.apps.app import App
    [](<https://adk.dev/context/compaction/#__codelineno-2-2>)from google.adk.apps.app import EventsCompactionConfig
    [](<https://adk.dev/context/compaction/#__codelineno-2-3>)
    [](<https://adk.dev/context/compaction/#__codelineno-2-4>)app = App(
    [](<https://adk.dev/context/compaction/#__codelineno-2-5>)    name='my-agent',
    [](<https://adk.dev/context/compaction/#__codelineno-2-6>)    root_agent=root_agent,
    [](<https://adk.dev/context/compaction/#__codelineno-2-7>)    events_compaction_config=EventsCompactionConfig(
    [](<https://adk.dev/context/compaction/#__codelineno-2-8>)        compaction_interval=3,  # Trigger compaction every 3 new invocations.
    [](<https://adk.dev/context/compaction/#__codelineno-2-9>)        overlap_size=1          # Include last invocation from the previous window.
    [](<https://adk.dev/context/compaction/#__codelineno-2-10>)    ),
    [](<https://adk.dev/context/compaction/#__codelineno-2-11>))
    
    [](<https://adk.dev/context/compaction/#__codelineno-3-1>)import com.google.adk.apps.App;
    [](<https://adk.dev/context/compaction/#__codelineno-3-2>)import com.google.adk.summarizer.EventsCompactionConfig;
    [](<https://adk.dev/context/compaction/#__codelineno-3-3>)
    [](<https://adk.dev/context/compaction/#__codelineno-3-4>)App app = App.builder()
    [](<https://adk.dev/context/compaction/#__codelineno-3-5>)    .name("my-agent")
    [](<https://adk.dev/context/compaction/#__codelineno-3-6>)    .rootAgent(rootAgent)
    [](<https://adk.dev/context/compaction/#__codelineno-3-7>)    .eventsCompactionConfig(EventsCompactionConfig.builder()
    [](<https://adk.dev/context/compaction/#__codelineno-3-8>)        .compactionInterval(3)  // Trigger compaction every 3 new invocations.
    [](<https://adk.dev/context/compaction/#__codelineno-3-9>)        .overlapSize(1)         // Include last invocation from the previous window.
    [](<https://adk.dev/context/compaction/#__codelineno-3-10>)        .build())
    [](<https://adk.dev/context/compaction/#__codelineno-3-11>)    .build();
    
    [](<https://adk.dev/context/compaction/#__codelineno-4-1>)import {Gemini, LlmAgent, LlmSummarizer, TokenBasedContextCompactor} from '@google/adk';
    [](<https://adk.dev/context/compaction/#__codelineno-4-2>)
    [](<https://adk.dev/context/compaction/#__codelineno-4-3>)const agent = new LlmAgent({
    [](<https://adk.dev/context/compaction/#__codelineno-4-4>)  name: 'my-agent',
    [](<https://adk.dev/context/compaction/#__codelineno-4-5>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/context/compaction/#__codelineno-4-6>)  contextCompactors: [
    [](<https://adk.dev/context/compaction/#__codelineno-4-7>)    new TokenBasedContextCompactor({
    [](<https://adk.dev/context/compaction/#__codelineno-4-8>)      tokenThreshold: 1000, // Trigger compaction when session exceeds 1000 tokens.
    [](<https://adk.dev/context/compaction/#__codelineno-4-9>)      eventRetentionSize: 1, // Keep at least 1 raw event (overlap).
    [](<https://adk.dev/context/compaction/#__codelineno-4-10>)      summarizer: new LlmSummarizer({
    [](<https://adk.dev/context/compaction/#__codelineno-4-11>)        llm: new Gemini({model: 'gemini-flash-latest'}),
    [](<https://adk.dev/context/compaction/#__codelineno-4-12>)      }),
    [](<https://adk.dev/context/compaction/#__codelineno-4-13>)    }),
    [](<https://adk.dev/context/compaction/#__codelineno-4-14>)  ],
    [](<https://adk.dev/context/compaction/#__codelineno-4-15>)});
    
Once configured, the ADK `Runner` handles the compaction process in the background each time the session reaches the interval.

## Example of context compaction[¶](<https://adk.dev/context/compaction/#example-of-context-compaction> "Permanent link")

If you set `compaction_interval` to 3 and `overlap_size` to 1, the event data is compressed upon completion of events 3, 6, 9, and so on. The overlap setting increases size of the second summary compression, and each summary afterwards, as shown in Figure 1.

![Context compaction example illustration](https://adk.dev/assets/context-compaction.svg) **Figure 1.** Illustration of event compaction configuration with an interval of 3 and overlap of 1.

With this example configuration, the context compression tasks happen as follows:

  1. **Event 3 completes** : All 3 events are compressed into a summary
  2. **Event 6 completes** : Events 3 to 6 are compressed, including the overlap of 1 prior event
  3. **Event 9 completes** : Events 6 to 9 are compressed, including the overlap of 1 prior event

## Configuration settings[¶](<https://adk.dev/context/compaction/#configuration-settings_1> "Permanent link")

The configuration settings for this feature control how frequently event data is compressed and how much data is retained as the agent workflow runs. Optionally, you can configure a compactor object

  * **`compaction_interval`** : Set the number of completed events that triggers compaction of the prior event data.
  * **`overlap_size`** : Set how many of the previously compacted events are included in a newly compacted context set.
  * **`summarizer`** : (Optional) Define a summarizer object including a specific AI model to use for summarization. For more information, see [Define a Summarizer](<https://adk.dev/context/compaction/#define-summarizer>).

### Define a Summarizer[¶](<https://adk.dev/context/compaction/#define-summarizer> "Permanent link")

You can customize the process of context compression by defining a summarizer. The `LlmEventSummarizer` (Python/Java) or `LlmSummarizer` (TypeScript) class allows you to specify a particular model for summarization. The following code example demonstrates how to define and configure a custom summarizer:

PythonJavaTypeScript
    
    [](<https://adk.dev/context/compaction/#__codelineno-5-1>)from google.adk.apps.app import App, EventsCompactionConfig
    [](<https://adk.dev/context/compaction/#__codelineno-5-2>)from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
    [](<https://adk.dev/context/compaction/#__codelineno-5-3>)from google.adk.models import Gemini
    [](<https://adk.dev/context/compaction/#__codelineno-5-4>)
    [](<https://adk.dev/context/compaction/#__codelineno-5-5>)# Define the AI model to be used for summarization:
    [](<https://adk.dev/context/compaction/#__codelineno-5-6>)summarization_llm = Gemini(model="gemini-flash-latest")
    [](<https://adk.dev/context/compaction/#__codelineno-5-7>)
    [](<https://adk.dev/context/compaction/#__codelineno-5-8>)# Create the summarizer with the custom model:
    [](<https://adk.dev/context/compaction/#__codelineno-5-9>)my_summarizer = LlmEventSummarizer(llm=summarization_llm)
    [](<https://adk.dev/context/compaction/#__codelineno-5-10>)
    [](<https://adk.dev/context/compaction/#__codelineno-5-11>)# Configure the App with the custom summarizer and compaction settings:
    [](<https://adk.dev/context/compaction/#__codelineno-5-12>)app = App(
    [](<https://adk.dev/context/compaction/#__codelineno-5-13>)    name='my-agent',
    [](<https://adk.dev/context/compaction/#__codelineno-5-14>)    root_agent=root_agent,
    [](<https://adk.dev/context/compaction/#__codelineno-5-15>)    events_compaction_config=EventsCompactionConfig(
    [](<https://adk.dev/context/compaction/#__codelineno-5-16>)        compaction_interval=3,
    [](<https://adk.dev/context/compaction/#__codelineno-5-17>)        overlap_size=1,
    [](<https://adk.dev/context/compaction/#__codelineno-5-18>)        summarizer=my_summarizer,
    [](<https://adk.dev/context/compaction/#__codelineno-5-19>)    ),
    [](<https://adk.dev/context/compaction/#__codelineno-5-20>))
    
    [](<https://adk.dev/context/compaction/#__codelineno-6-1>)import com.google.adk.apps.App;
    [](<https://adk.dev/context/compaction/#__codelineno-6-2>)import com.google.adk.models.Gemini;
    [](<https://adk.dev/context/compaction/#__codelineno-6-3>)import com.google.adk.summarizer.EventsCompactionConfig;
    [](<https://adk.dev/context/compaction/#__codelineno-6-4>)import com.google.adk.summarizer.LlmEventSummarizer;
    [](<https://adk.dev/context/compaction/#__codelineno-6-5>)
    [](<https://adk.dev/context/compaction/#__codelineno-6-6>)// Define the AI model to be used for summarization:
    [](<https://adk.dev/context/compaction/#__codelineno-6-7>)Gemini summarizationLlm = Gemini.builder()
    [](<https://adk.dev/context/compaction/#__codelineno-6-8>)    .model("gemini-flash-latest")
    [](<https://adk.dev/context/compaction/#__codelineno-6-9>)    .build();
    [](<https://adk.dev/context/compaction/#__codelineno-6-10>)
    [](<https://adk.dev/context/compaction/#__codelineno-6-11>)// Create the summarizer with the custom model:
    [](<https://adk.dev/context/compaction/#__codelineno-6-12>)LlmEventSummarizer mySummarizer = new LlmEventSummarizer(summarizationLlm);
    [](<https://adk.dev/context/compaction/#__codelineno-6-13>)
    [](<https://adk.dev/context/compaction/#__codelineno-6-14>)// Configure the App with the custom summarizer and compaction settings:
    [](<https://adk.dev/context/compaction/#__codelineno-6-15>)App app = App.builder()
    [](<https://adk.dev/context/compaction/#__codelineno-6-16>)    .name("my-agent")
    [](<https://adk.dev/context/compaction/#__codelineno-6-17>)    .rootAgent(rootAgent)
    [](<https://adk.dev/context/compaction/#__codelineno-6-18>)    .eventsCompactionConfig(EventsCompactionConfig.builder()
    [](<https://adk.dev/context/compaction/#__codelineno-6-19>)        .compactionInterval(3)
    [](<https://adk.dev/context/compaction/#__codelineno-6-20>)        .overlapSize(1)
    [](<https://adk.dev/context/compaction/#__codelineno-6-21>)        .summarizer(mySummarizer)
    [](<https://adk.dev/context/compaction/#__codelineno-6-22>)        .build())
    [](<https://adk.dev/context/compaction/#__codelineno-6-23>)    .build();
    
    [](<https://adk.dev/context/compaction/#__codelineno-7-1>)import {Gemini, LlmAgent, LlmSummarizer, TokenBasedContextCompactor} from '@google/adk';
    [](<https://adk.dev/context/compaction/#__codelineno-7-2>)
    [](<https://adk.dev/context/compaction/#__codelineno-7-3>)// Define the AI model to be used for summarization:
    [](<https://adk.dev/context/compaction/#__codelineno-7-4>)const summarizationLlm = new Gemini({model: 'gemini-flash-latest'});
    [](<https://adk.dev/context/compaction/#__codelineno-7-5>)
    [](<https://adk.dev/context/compaction/#__codelineno-7-6>)// Create the summarizer with the custom model:
    [](<https://adk.dev/context/compaction/#__codelineno-7-7>)const mySummarizer = new LlmSummarizer({llm: summarizationLlm});
    [](<https://adk.dev/context/compaction/#__codelineno-7-8>)
    [](<https://adk.dev/context/compaction/#__codelineno-7-9>)// Configure the agent with the custom summarizer and compaction settings:
    [](<https://adk.dev/context/compaction/#__codelineno-7-10>)const agent = new LlmAgent({
    [](<https://adk.dev/context/compaction/#__codelineno-7-11>)  name: 'my-agent',
    [](<https://adk.dev/context/compaction/#__codelineno-7-12>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/context/compaction/#__codelineno-7-13>)  contextCompactors: [
    [](<https://adk.dev/context/compaction/#__codelineno-7-14>)    new TokenBasedContextCompactor({
    [](<https://adk.dev/context/compaction/#__codelineno-7-15>)      tokenThreshold: 1000,
    [](<https://adk.dev/context/compaction/#__codelineno-7-16>)      eventRetentionSize: 1,
    [](<https://adk.dev/context/compaction/#__codelineno-7-17>)      summarizer: mySummarizer,
    [](<https://adk.dev/context/compaction/#__codelineno-7-18>)    }),
    [](<https://adk.dev/context/compaction/#__codelineno-7-19>)  ],
    [](<https://adk.dev/context/compaction/#__codelineno-7-20>)});
    
You can further refine the compactor by modifying its summarizer. In Python and Java, customize the `prompt_template` on `LlmEventSummarizer`. In TypeScript, customize the `prompt` on `LlmSummarizer`. For more details, see the [`LlmEventSummarizer` code](<https://github.com/google/adk-python/blob/main/src/google/adk/apps/llm_event_summarizer.py#L60>) or [`LlmSummarizer` code](<https://github.com/google/adk-js/blob/main/core/src/context/summarizers/llm_summarizer.ts>).

Back to top 