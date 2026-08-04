# Events - Agent Development Kit (ADK)

> Source: [https://adk.dev/events/](https://adk.dev/events/)

[ Skip to content ](<https://adk.dev/events/#events>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/events/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/events/index.md> "View this page as Markdown")

# Events[¶](<https://adk.dev/events/#events> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

Events are the fundamental units of information flow within the Agent Development Kit (ADK). They represent every significant occurrence during an agent's interaction lifecycle, from initial user input to the final response and all the steps in between. Understanding events is crucial because they are the primary way components communicate, state is managed, and control flow is directed.

## What Events Are and Why They Matter[¶](<https://adk.dev/events/#what-events-are-and-why-they-matter> "Permanent link")

An `Event` in ADK is an immutable record representing a specific point in the agent's execution. It captures user messages, agent replies, requests to use tools (function calls), tool results, state changes, control signals, and errors.

PythonTypeScriptGoJavaKotlin

Technically, it's an instance of the `google.adk.events.Event` class, which builds upon the basic `LlmResponse` structure by adding essential ADK-specific metadata and an `actions` payload.
    
    [](<https://adk.dev/events/#__codelineno-0-1>)# Conceptual Structure of an Event (Python)
    [](<https://adk.dev/events/#__codelineno-0-2>)# from google.adk.events import Event, EventActions
    [](<https://adk.dev/events/#__codelineno-0-3>)# from google.genai import types
    [](<https://adk.dev/events/#__codelineno-0-4>)
    [](<https://adk.dev/events/#__codelineno-0-5>)# class Event(LlmResponse): # Simplified view
    [](<https://adk.dev/events/#__codelineno-0-6>)#     # --- LlmResponse fields ---
    [](<https://adk.dev/events/#__codelineno-0-7>)#     content: Optional[types.Content]
    [](<https://adk.dev/events/#__codelineno-0-8>)#     partial: Optional[bool]
    [](<https://adk.dev/events/#__codelineno-0-9>)#     # ... other response fields ...
    [](<https://adk.dev/events/#__codelineno-0-10>)
    [](<https://adk.dev/events/#__codelineno-0-11>)#     # --- ADK specific additions ---
    [](<https://adk.dev/events/#__codelineno-0-12>)#     author: str          # 'user' or agent name
    [](<https://adk.dev/events/#__codelineno-0-13>)#     invocation_id: str   # ID for the whole interaction run
    [](<https://adk.dev/events/#__codelineno-0-14>)#     id: str              # Unique ID for this specific event
    [](<https://adk.dev/events/#__codelineno-0-15>)#     timestamp: float     # Creation time
    [](<https://adk.dev/events/#__codelineno-0-16>)#     actions: EventActions # Important for side-effects & control
    [](<https://adk.dev/events/#__codelineno-0-17>)#     branch: Optional[str] # Hierarchy path
    [](<https://adk.dev/events/#__codelineno-0-18>)#     # ...
    
In TypeScript, this is an interface of type `Event`.
    
    [](<https://adk.dev/events/#__codelineno-1-1>)import {Content} from '@google/genai';
    [](<https://adk.dev/events/#__codelineno-1-2>)
    [](<https://adk.dev/events/#__codelineno-1-3>)/**
    [](<https://adk.dev/events/#__codelineno-1-4>) * Conceptual Structure of an Event (TypeScript)
    [](<https://adk.dev/events/#__codelineno-1-5>) */
    [](<https://adk.dev/events/#__codelineno-1-6>)export interface Event extends LlmResponse {
    [](<https://adk.dev/events/#__codelineno-1-7>)  /** Unique ID for this specific event. */
    [](<https://adk.dev/events/#__codelineno-1-8>)  id: string;
    [](<https://adk.dev/events/#__codelineno-1-9>)  /** ID for the whole interaction run. */
    [](<https://adk.dev/events/#__codelineno-1-10>)  invocationId: string;
    [](<https://adk.dev/events/#__codelineno-1-11>)  /** 'user' or agent name. */
    [](<https://adk.dev/events/#__codelineno-1-12>)  author?: string;
    [](<https://adk.dev/events/#__codelineno-1-13>)  /** Important for side-effects & control. */
    [](<https://adk.dev/events/#__codelineno-1-14>)  actions: EventActions;
    [](<https://adk.dev/events/#__codelineno-1-15>)  /** Creation time. */
    [](<https://adk.dev/events/#__codelineno-1-16>)  timestamp: number;
    [](<https://adk.dev/events/#__codelineno-1-17>)  /** Is it streaming output? */
    [](<https://adk.dev/events/#__codelineno-1-18>)  partial?: boolean;
    [](<https://adk.dev/events/#__codelineno-1-19>)  /** Is the turn finished? */
    [](<https://adk.dev/events/#__codelineno-1-20>)  turnComplete?: boolean;
    [](<https://adk.dev/events/#__codelineno-1-21>)  /** Hierarchy path. */
    [](<https://adk.dev/events/#__codelineno-1-22>)  branch?: string;
    [](<https://adk.dev/events/#__codelineno-1-23>)  /** List of IDs for long-running tools. */
    [](<https://adk.dev/events/#__codelineno-1-24>)  longRunningToolIds?: string[];
    [](<https://adk.dev/events/#__codelineno-1-25>)  /** The content of the response. */
    [](<https://adk.dev/events/#__codelineno-1-26>)  content?: Content;
    [](<https://adk.dev/events/#__codelineno-1-27>)  // ... other LlmResponse fields like errorCode, errorMessage
    [](<https://adk.dev/events/#__codelineno-1-28>)}
    
In Go, this is a struct of type `google.golang.org/adk/v2/session.Event`.
    
    [](<https://adk.dev/events/#__codelineno-2-1>)// Conceptual Structure of an Event (Go - See session/session.go)
    [](<https://adk.dev/events/#__codelineno-2-2>)// Simplified view based on the session.Event struct
    [](<https://adk.dev/events/#__codelineno-2-3>)type Event struct {
    [](<https://adk.dev/events/#__codelineno-2-4>)    // --- Fields from embedded model.LLMResponse ---
    [](<https://adk.dev/events/#__codelineno-2-5>)    model.LLMResponse
    [](<https://adk.dev/events/#__codelineno-2-6>)
    [](<https://adk.dev/events/#__codelineno-2-7>)    // --- ADK specific additions ---
    [](<https://adk.dev/events/#__codelineno-2-8>)    Author       string         // 'user' or agent name
    [](<https://adk.dev/events/#__codelineno-2-9>)    InvocationID string         // ID for the whole interaction run
    [](<https://adk.dev/events/#__codelineno-2-10>)    ID           string         // Unique ID for this specific event
    [](<https://adk.dev/events/#__codelineno-2-11>)    Timestamp    time.Time      // Creation time
    [](<https://adk.dev/events/#__codelineno-2-12>)    Actions      EventActions   // Important for side-effects & control
    [](<https://adk.dev/events/#__codelineno-2-13>)    Branch       string         // Hierarchy path
    [](<https://adk.dev/events/#__codelineno-2-14>)    // ... other fields
    [](<https://adk.dev/events/#__codelineno-2-15>)}
    [](<https://adk.dev/events/#__codelineno-2-16>)
    [](<https://adk.dev/events/#__codelineno-2-17>)// model.LLMResponse contains the Content field
    [](<https://adk.dev/events/#__codelineno-2-18>)type LLMResponse struct {
    [](<https://adk.dev/events/#__codelineno-2-19>)    Content *genai.Content
    [](<https://adk.dev/events/#__codelineno-2-20>)    // ... other fields
    [](<https://adk.dev/events/#__codelineno-2-21>)}
    
In Java, this is an instance of the `com.google.adk.events.Event` class. It also builds upon a basic response structure by adding essential ADK-specific metadata and an `actions` payload.
    
    [](<https://adk.dev/events/#__codelineno-3-1>)// Conceptual Structure of an Event (Java - See com.google.adk.events.Event.java)
    [](<https://adk.dev/events/#__codelineno-3-2>)// Simplified view based on the provided com.google.adk.events.Event.java
    [](<https://adk.dev/events/#__codelineno-3-3>)// public class Event extends JsonBaseModel {
    [](<https://adk.dev/events/#__codelineno-3-4>)//     // --- Fields analogous to LlmResponse ---
    [](<https://adk.dev/events/#__codelineno-3-5>)//     private Optional<Content> content;
    [](<https://adk.dev/events/#__codelineno-3-6>)//     private Optional<Boolean> partial;
    [](<https://adk.dev/events/#__codelineno-3-7>)//     // ... other response fields like errorCode, errorMessage ...
    [](<https://adk.dev/events/#__codelineno-3-8>)
    [](<https://adk.dev/events/#__codelineno-3-9>)//     // --- ADK specific additions ---
    [](<https://adk.dev/events/#__codelineno-3-10>)//     private String author;         // 'user' or agent name
    [](<https://adk.dev/events/#__codelineno-3-11>)//     private String invocationId;   // ID for the whole interaction run
    [](<https://adk.dev/events/#__codelineno-3-12>)//     private String id;             // Unique ID for this specific event
    [](<https://adk.dev/events/#__codelineno-3-13>)//     private long timestamp;        // Creation time (epoch milliseconds)
    [](<https://adk.dev/events/#__codelineno-3-14>)//     private EventActions actions;  // Important for side-effects & control
    [](<https://adk.dev/events/#__codelineno-3-15>)//     private Optional<String> branch; // Hierarchy path
    [](<https://adk.dev/events/#__codelineno-3-16>)//     // ... other fields like turnComplete, longRunningToolIds etc.
    [](<https://adk.dev/events/#__codelineno-3-17>)// }
    
In Kotlin, this is an instance of the `com.google.adk.kt.events.Event` class.
    
    [](<https://adk.dev/events/#__codelineno-4-1>)// Conceptual Structure of an Event (Kotlin)
    [](<https://adk.dev/events/#__codelineno-4-2>)// data class Event(
    [](<https://adk.dev/events/#__codelineno-4-3>)//     val author: String,
    [](<https://adk.dev/events/#__codelineno-4-4>)//     val content: Content? = null,
    [](<https://adk.dev/events/#__codelineno-4-5>)//     val actions: EventActions = EventActions(),
    [](<https://adk.dev/events/#__codelineno-4-6>)//     val invocationId: String? = null,
    [](<https://adk.dev/events/#__codelineno-4-7>)//     val branch: String? = null,
    [](<https://adk.dev/events/#__codelineno-4-8>)//     val timestamp: Long = Clock.System.now().toEpochMilliseconds(),
    [](<https://adk.dev/events/#__codelineno-4-9>)//     val id: String = Uuid.random(),
    [](<https://adk.dev/events/#__codelineno-4-10>)//     val partial: Boolean = false,
    [](<https://adk.dev/events/#__codelineno-4-11>)//     val turnComplete: Boolean = false,
    [](<https://adk.dev/events/#__codelineno-4-12>)//     val longRunningToolIds: Set<String> = emptySet()
    [](<https://adk.dev/events/#__codelineno-4-13>)// )
    
Events are central to ADK's operation for several key reasons:

  1. **Communication:** They serve as the standard message format between the user interface, the `Runner`, agents, the LLM, and tools. Everything flows as an `Event`.

  2. **Signaling State & Artifact Changes:** Events carry instructions for state modifications and track artifact updates. The `SessionService` uses these signals to ensure persistence. In Python changes are signaled via `event.actions.state_delta` and `event.actions.artifact_delta`.

  3. **Control Flow:** Specific fields like `event.actions.transfer_to_agent` or `event.actions.escalate` act as signals that direct the framework, determining which agent runs next or if a loop should terminate.

  4. **History & Observability:** The sequence of events recorded in `session.events` provides a complete, chronological history of an interaction, invaluable for debugging, auditing, and understanding agent behavior step-by-step.

In essence, the entire process, from a user's query to the agent's final answer, is orchestrated through the generation, interpretation, and processing of `Event` objects.

## Understanding and Using Events[¶](<https://adk.dev/events/#understanding-and-using-events> "Permanent link")

As a developer, you'll primarily interact with the stream of events yielded by the `Runner`. Here's how to understand and extract information from them:

Note

The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `event.content()` in Python, `event.content().get().parts()` in Java). Refer to the language-specific API documentation for details.

### Identifying Event Origin and Type[¶](<https://adk.dev/events/#identifying-event-origin-and-type> "Permanent link")

Quickly determine what an event represents by checking:

  * **Who sent it? (`event.author`)**
    * `'user'`: Indicates input directly from the end-user.
    * `'AgentName'`: Indicates output or action from a specific agent (e.g., `'WeatherAgent'`, `'SummarizerAgent'`).
  * **What's the main payload? (`event.content` and `event.content.parts`)**

    * **Text:** Indicates a conversational message. For Python, check if `event.content.parts[0].text` exists. For Java, check if `event.content()` is present, its `parts()` are present and not empty, and the first part's `text()` is present.
    * **Tool Call Request:** Check `event.get_function_calls()`. If not empty, the LLM is asking to execute one or more tools. Each item in the list has `.name` and `.args`.
    * **Tool Result:** Check `event.get_function_responses()`. If not empty, this event carries the result(s) from tool execution(s). Each item has `.name` and `.response` (the dictionary returned by the tool). _Note:_ For history structuring, the `role` inside the `content` is often `'user'`, but the event `author` is typically the agent that requested the tool call.
  * **Is it streaming output? (`event.partial`)** Indicates whether this is an incomplete chunk of text from the LLM.

    * `True`: More text will follow.
    * `False` or `None`/`Optional.empty()`: This part of the content is complete (though the overall turn might not be finished if `turn_complete` is also false).

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/events/#__codelineno-5-1>)# Pseudocode: Basic event identification (Python)
    [](<https://adk.dev/events/#__codelineno-5-2>)# async for event in runner.run_async(...):
    [](<https://adk.dev/events/#__codelineno-5-3>)#     print(f"Event from: {event.author}")
    [](<https://adk.dev/events/#__codelineno-5-4>)#
    [](<https://adk.dev/events/#__codelineno-5-5>)#     if event.content and event.content.parts:
    [](<https://adk.dev/events/#__codelineno-5-6>)#         if event.get_function_calls():
    [](<https://adk.dev/events/#__codelineno-5-7>)#             print("  Type: Tool Call Request")
    [](<https://adk.dev/events/#__codelineno-5-8>)#         elif event.get_function_responses():
    [](<https://adk.dev/events/#__codelineno-5-9>)#             print("  Type: Tool Result")
    [](<https://adk.dev/events/#__codelineno-5-10>)#         elif event.content.parts[0].text:
    [](<https://adk.dev/events/#__codelineno-5-11>)#             if event.partial:
    [](<https://adk.dev/events/#__codelineno-5-12>)#                 print("  Type: Streaming Text Chunk")
    [](<https://adk.dev/events/#__codelineno-5-13>)#             else:
    [](<https://adk.dev/events/#__codelineno-5-14>)#                 print("  Type: Complete Text Message")
    [](<https://adk.dev/events/#__codelineno-5-15>)#         else:
    [](<https://adk.dev/events/#__codelineno-5-16>)#             print("  Type: Other Content (e.g., code result)")
    [](<https://adk.dev/events/#__codelineno-5-17>)#     elif event.actions and (event.actions.state_delta or event.actions.artifact_delta):
    [](<https://adk.dev/events/#__codelineno-5-18>)#         print("  Type: State/Artifact Update")
    [](<https://adk.dev/events/#__codelineno-5-19>)#     else:
    [](<https://adk.dev/events/#__codelineno-5-20>)#         print("  Type: Control Signal or Other")
    
    [](<https://adk.dev/events/#__codelineno-6-1>)// Pseudocode: Basic event identification (TypeScript)
    [](<https://adk.dev/events/#__codelineno-6-2>)import {
    [](<https://adk.dev/events/#__codelineno-6-3>)  Event,
    [](<https://adk.dev/events/#__codelineno-6-4>)  getFunctionCalls,
    [](<https://adk.dev/events/#__codelineno-6-5>)  getFunctionResponses
    [](<https://adk.dev/events/#__codelineno-6-6>)} from '@google/adk';
    [](<https://adk.dev/events/#__codelineno-6-7>)
    [](<https://adk.dev/events/#__codelineno-6-8>)export async function processEvents(runnerEvents: AsyncIterable<Event>) {
    [](<https://adk.dev/events/#__codelineno-6-9>)  for await (const event of runnerEvents) {
    [](<https://adk.dev/events/#__codelineno-6-10>)    console.log(`Event from: ${event.author}`);
    [](<https://adk.dev/events/#__codelineno-6-11>)
    [](<https://adk.dev/events/#__codelineno-6-12>)    if (event.content && event.content.parts && event.content.parts.length > 0) {
    [](<https://adk.dev/events/#__codelineno-6-13>)      if (getFunctionCalls(event).length > 0) {
    [](<https://adk.dev/events/#__codelineno-6-14>)        console.log('  Type: Tool Call Request');
    [](<https://adk.dev/events/#__codelineno-6-15>)      } else if (getFunctionResponses(event).length > 0) {
    [](<https://adk.dev/events/#__codelineno-6-16>)        console.log('  Type: Tool Result');
    [](<https://adk.dev/events/#__codelineno-6-17>)      } else if (event.content.parts[0].text) {
    [](<https://adk.dev/events/#__codelineno-6-18>)        if (event.partial) {
    [](<https://adk.dev/events/#__codelineno-6-19>)          console.log('  Type: Streaming Text Chunk');
    [](<https://adk.dev/events/#__codelineno-6-20>)        } else {
    [](<https://adk.dev/events/#__codelineno-6-21>)          console.log('  Type: Complete Text Message');
    [](<https://adk.dev/events/#__codelineno-6-22>)        }
    [](<https://adk.dev/events/#__codelineno-6-23>)      } else {
    [](<https://adk.dev/events/#__codelineno-6-24>)        console.log('  Type: Other Content (e.g., code result)');
    [](<https://adk.dev/events/#__codelineno-6-25>)      }
    [](<https://adk.dev/events/#__codelineno-6-26>)    } else if (
    [](<https://adk.dev/events/#__codelineno-6-27>)      event.actions &&
    [](<https://adk.dev/events/#__codelineno-6-28>)      (Object.keys(event.actions.stateDelta).length > 0 ||
    [](<https://adk.dev/events/#__codelineno-6-29>)        Object.keys(event.actions.artifactDelta).length > 0)
    [](<https://adk.dev/events/#__codelineno-6-30>)    ) {
    [](<https://adk.dev/events/#__codelineno-6-31>)      console.log('  Type: State/Artifact Update');
    [](<https://adk.dev/events/#__codelineno-6-32>)    } else {
    [](<https://adk.dev/events/#__codelineno-6-33>)      console.log('  Type: Control Signal or Other');
    [](<https://adk.dev/events/#__codelineno-6-34>)    }
    [](<https://adk.dev/events/#__codelineno-6-35>)  }
    [](<https://adk.dev/events/#__codelineno-6-36>)}
    
    [](<https://adk.dev/events/#__codelineno-7-1>)  // Pseudocode: Basic event identification (Go)
    [](<https://adk.dev/events/#__codelineno-7-2>)import (
    [](<https://adk.dev/events/#__codelineno-7-3>)  "fmt"
    [](<https://adk.dev/events/#__codelineno-7-4>)  "google.golang.org/adk/v2/session"
    [](<https://adk.dev/events/#__codelineno-7-5>)  "google.golang.org/genai"
    [](<https://adk.dev/events/#__codelineno-7-6>))
    [](<https://adk.dev/events/#__codelineno-7-7>)
    [](<https://adk.dev/events/#__codelineno-7-8>)func hasFunctionCalls(content *genai.Content) bool {
    [](<https://adk.dev/events/#__codelineno-7-9>)  if content == nil {
    [](<https://adk.dev/events/#__codelineno-7-10>)    return false
    [](<https://adk.dev/events/#__codelineno-7-11>)  }
    [](<https://adk.dev/events/#__codelineno-7-12>)  for _, part := range content.Parts {
    [](<https://adk.dev/events/#__codelineno-7-13>)    if part.FunctionCall != nil {
    [](<https://adk.dev/events/#__codelineno-7-14>)      return true
    [](<https://adk.dev/events/#__codelineno-7-15>)    }
    [](<https://adk.dev/events/#__codelineno-7-16>)  }
    [](<https://adk.dev/events/#__codelineno-7-17>)  return false
    [](<https://adk.dev/events/#__codelineno-7-18>)}
    [](<https://adk.dev/events/#__codelineno-7-19>)
    [](<https://adk.dev/events/#__codelineno-7-20>)func hasFunctionResponses(content *genai.Content) bool {
    [](<https://adk.dev/events/#__codelineno-7-21>)  if content == nil {
    [](<https://adk.dev/events/#__codelineno-7-22>)    return false
    [](<https://adk.dev/events/#__codelineno-7-23>)  }
    [](<https://adk.dev/events/#__codelineno-7-24>)  for _, part := range content.Parts {
    [](<https://adk.dev/events/#__codelineno-7-25>)    if part.FunctionResponse != nil {
    [](<https://adk.dev/events/#__codelineno-7-26>)      return true
    [](<https://adk.dev/events/#__codelineno-7-27>)    }
    [](<https://adk.dev/events/#__codelineno-7-28>)  }
    [](<https://adk.dev/events/#__codelineno-7-29>)  return false
    [](<https://adk.dev/events/#__codelineno-7-30>)}
    [](<https://adk.dev/events/#__codelineno-7-31>)
    [](<https://adk.dev/events/#__codelineno-7-32>)func processEvents(events <-chan *session.Event) {
    [](<https://adk.dev/events/#__codelineno-7-33>)  for event := range events {
    [](<https://adk.dev/events/#__codelineno-7-34>)    fmt.Printf("Event from: %s\n", event.Author)
    [](<https://adk.dev/events/#__codelineno-7-35>)
    [](<https://adk.dev/events/#__codelineno-7-36>)    if event.LLMResponse != nil && event.LLMResponse.Content != nil {
    [](<https://adk.dev/events/#__codelineno-7-37>)      if hasFunctionCalls(event.LLMResponse.Content) {
    [](<https://adk.dev/events/#__codelineno-7-38>)        fmt.Println("  Type: Tool Call Request")
    [](<https://adk.dev/events/#__codelineno-7-39>)      } else if hasFunctionResponses(event.LLMResponse.Content) {
    [](<https://adk.dev/events/#__codelineno-7-40>)        fmt.Println("  Type: Tool Result")
    [](<https://adk.dev/events/#__codelineno-7-41>)      } else if len(event.LLMResponse.Content.Parts) > 0 {
    [](<https://adk.dev/events/#__codelineno-7-42>)        if event.LLMResponse.Content.Parts[0].Text != "" {
    [](<https://adk.dev/events/#__codelineno-7-43>)          if event.LLMResponse.Partial {
    [](<https://adk.dev/events/#__codelineno-7-44>)            fmt.Println("  Type: Streaming Text Chunk")
    [](<https://adk.dev/events/#__codelineno-7-45>)          } else {
    [](<https://adk.dev/events/#__codelineno-7-46>)            fmt.Println("  Type: Complete Text Message")
    [](<https://adk.dev/events/#__codelineno-7-47>)          }
    [](<https://adk.dev/events/#__codelineno-7-48>)        } else {
    [](<https://adk.dev/events/#__codelineno-7-49>)          fmt.Println("  Type: Other Content (e.g., code result)")
    [](<https://adk.dev/events/#__codelineno-7-50>)        }
    [](<https://adk.dev/events/#__codelineno-7-51>)      }
    [](<https://adk.dev/events/#__codelineno-7-52>)    } else if len(event.Actions.StateDelta) > 0 {
    [](<https://adk.dev/events/#__codelineno-7-53>)      fmt.Println("  Type: State Update")
    [](<https://adk.dev/events/#__codelineno-7-54>)    } else {
    [](<https://adk.dev/events/#__codelineno-7-55>)      fmt.Println("  Type: Control Signal or Other")
    [](<https://adk.dev/events/#__codelineno-7-56>)    }
    [](<https://adk.dev/events/#__codelineno-7-57>)  }
    [](<https://adk.dev/events/#__codelineno-7-58>)}
    
    [](<https://adk.dev/events/#__codelineno-8-1>)// Pseudocode: Basic event identification (Java)
    [](<https://adk.dev/events/#__codelineno-8-2>)// import com.google.genai.types.Content;
    [](<https://adk.dev/events/#__codelineno-8-3>)// import com.google.adk.events.Event;
    [](<https://adk.dev/events/#__codelineno-8-4>)// import com.google.adk.events.EventActions;
    [](<https://adk.dev/events/#__codelineno-8-5>)
    [](<https://adk.dev/events/#__codelineno-8-6>)// runner.runAsync(...).forEach(event -> { // Assuming a synchronous stream or reactive stream
    [](<https://adk.dev/events/#__codelineno-8-7>)//     System.out.println("Event from: " + event.author());
    [](<https://adk.dev/events/#__codelineno-8-8>)//
    [](<https://adk.dev/events/#__codelineno-8-9>)//     if (event.content().isPresent()) {
    [](<https://adk.dev/events/#__codelineno-8-10>)//         Content content = event.content().get();
    [](<https://adk.dev/events/#__codelineno-8-11>)//         if (!event.functionCalls().isEmpty()) {
    [](<https://adk.dev/events/#__codelineno-8-12>)//             System.out.println("  Type: Tool Call Request");
    [](<https://adk.dev/events/#__codelineno-8-13>)//         } else if (!event.functionResponses().isEmpty()) {
    [](<https://adk.dev/events/#__codelineno-8-14>)//             System.out.println("  Type: Tool Result");
    [](<https://adk.dev/events/#__codelineno-8-15>)//         } else if (content.parts().isPresent() && !content.parts().get().isEmpty() &&
    [](<https://adk.dev/events/#__codelineno-8-16>)//                    content.parts().get().get(0).text().isPresent()) {
    [](<https://adk.dev/events/#__codelineno-8-17>)//             if (event.partial().orElse(false)) {
    [](<https://adk.dev/events/#__codelineno-8-18>)//                 System.out.println("  Type: Streaming Text Chunk");
    [](<https://adk.dev/events/#__codelineno-8-19>)//             } else {
    [](<https://adk.dev/events/#__codelineno-8-20>)//                 System.out.println("  Type: Complete Text Message");
    [](<https://adk.dev/events/#__codelineno-8-21>)//             }
    [](<https://adk.dev/events/#__codelineno-8-22>)//         } else {
    [](<https://adk.dev/events/#__codelineno-8-23>)//             System.out.println("  Type: Other Content (e.g., code result)");
    [](<https://adk.dev/events/#__codelineno-8-24>)//         }
    [](<https://adk.dev/events/#__codelineno-8-25>)//     } else if (event.actions() != null &&
    [](<https://adk.dev/events/#__codelineno-8-26>)//                ((event.actions().stateDelta() != null && !event.actions().stateDelta().isEmpty()) ||
    [](<https://adk.dev/events/#__codelineno-8-27>)//                 (event.actions().artifactDelta() != null && !event.actions().artifactDelta().isEmpty()))) {
    [](<https://adk.dev/events/#__codelineno-8-28>)//         System.out.println("  Type: State/Artifact Update");
    [](<https://adk.dev/events/#__codelineno-8-29>)//     } else {
    [](<https://adk.dev/events/#__codelineno-8-30>)//         System.out.println("  Type: Control Signal or Other");
    [](<https://adk.dev/events/#__codelineno-8-31>)//     }
    [](<https://adk.dev/events/#__codelineno-8-32>)// });
    
    [](<https://adk.dev/events/#__codelineno-9-1>)// Pseudocode: Basic event identification (Kotlin)
    [](<https://adk.dev/events/#__codelineno-9-2>)// runner.runAsync(...).collect { event ->
    [](<https://adk.dev/events/#__codelineno-9-3>)//     println("Event from: ${event.author}")
    [](<https://adk.dev/events/#__codelineno-9-4>)//
    [](<https://adk.dev/events/#__codelineno-9-5>)//     val content = event.content
    [](<https://adk.dev/events/#__codelineno-9-6>)//     if (content != null && content.parts.isNotEmpty()) {
    [](<https://adk.dev/events/#__codelineno-9-7>)//         if (event.functionCalls().isNotEmpty()) {
    [](<https://adk.dev/events/#__codelineno-9-8>)//             println("  Type: Tool Call Request")
    [](<https://adk.dev/events/#__codelineno-9-9>)//         } else if (event.functionResponses().isNotEmpty()) {
    [](<https://adk.dev/events/#__codelineno-9-10>)//             println("  Type: Tool Result")
    [](<https://adk.dev/events/#__codelineno-9-11>)//         } else if (content.parts[0].text != null) {
    [](<https://adk.dev/events/#__codelineno-9-12>)//             if (event.partial) {
    [](<https://adk.dev/events/#__codelineno-9-13>)//                 println("  Type: Streaming Text Chunk")
    [](<https://adk.dev/events/#__codelineno-9-14>)//             } else {
    [](<https://adk.dev/events/#__codelineno-9-15>)//                 println("  Type: Complete Text Message")
    [](<https://adk.dev/events/#__codelineno-9-16>)//             }
    [](<https://adk.dev/events/#__codelineno-9-17>)//         } else {
    [](<https://adk.dev/events/#__codelineno-9-18>)//             println("  Type: Other Content (e.g., code result)")
    [](<https://adk.dev/events/#__codelineno-9-19>)//         }
    [](<https://adk.dev/events/#__codelineno-9-20>)//     } else if (event.actions.stateDelta.isNotEmpty() || event.actions.artifactDelta.isNotEmpty()) {
    [](<https://adk.dev/events/#__codelineno-9-21>)//         println("  Type: State/Artifact Update")
    [](<https://adk.dev/events/#__codelineno-9-22>)//     } else {
    [](<https://adk.dev/events/#__codelineno-9-23>)//         println("  Type: Control Signal or Other")
    [](<https://adk.dev/events/#__codelineno-9-24>)//     }
    [](<https://adk.dev/events/#__codelineno-9-25>)// }
    
### Extracting Key Information[¶](<https://adk.dev/events/#extracting-key-information> "Permanent link")

Once you know the event type, access the relevant data:

  * **Text Content:** Always check for the presence of content and parts before accessing text. In Python its `text = event.content.parts[0].text`.

  * **Function Call Details:**

PythonTypeScriptGoJava
        
        [](<https://adk.dev/events/#__codelineno-10-1>)calls = event.get_function_calls()
        [](<https://adk.dev/events/#__codelineno-10-2>)if calls:
        [](<https://adk.dev/events/#__codelineno-10-3>)    for call in calls:
        [](<https://adk.dev/events/#__codelineno-10-4>)        tool_name = call.name
        [](<https://adk.dev/events/#__codelineno-10-5>)        arguments = call.args # This is usually a dictionary
        [](<https://adk.dev/events/#__codelineno-10-6>)        print(f"  Tool: {tool_name}, Args: {arguments}")
        [](<https://adk.dev/events/#__codelineno-10-7>)        # Application might dispatch execution based on this
        
        [](<https://adk.dev/events/#__codelineno-11-1>)export function handleFunctionCalls(event: Event) {
        [](<https://adk.dev/events/#__codelineno-11-2>)    const calls = getFunctionCalls(event);
        [](<https://adk.dev/events/#__codelineno-11-3>)    if (calls.length > 0) {
        [](<https://adk.dev/events/#__codelineno-11-4>)        for (const call of calls) {
        [](<https://adk.dev/events/#__codelineno-11-5>)            const toolName = call.name;
        [](<https://adk.dev/events/#__codelineno-11-6>)            const argumentsDict = call.args; // This is an object
        [](<https://adk.dev/events/#__codelineno-11-7>)            console.log(`  Tool: ${toolName}, Args: ${JSON.stringify(argumentsDict)}`);
        [](<https://adk.dev/events/#__codelineno-11-8>)        }
        [](<https://adk.dev/events/#__codelineno-11-9>)    }
        [](<https://adk.dev/events/#__codelineno-11-10>)}
        
        [](<https://adk.dev/events/#__codelineno-12-1>)import (
        [](<https://adk.dev/events/#__codelineno-12-2>)    "fmt"
        [](<https://adk.dev/events/#__codelineno-12-3>)    "google.golang.org/adk/v2/session"
        [](<https://adk.dev/events/#__codelineno-12-4>)    "google.golang.org/genai"
        [](<https://adk.dev/events/#__codelineno-12-5>))
        [](<https://adk.dev/events/#__codelineno-12-6>)
        [](<https://adk.dev/events/#__codelineno-12-7>)func handleFunctionCalls(event *session.Event) {
        [](<https://adk.dev/events/#__codelineno-12-8>)    if event.LLMResponse == nil || event.LLMResponse.Content == nil {
        [](<https://adk.dev/events/#__codelineno-12-9>)        return
        [](<https://adk.dev/events/#__codelineno-12-10>)    }
        [](<https://adk.dev/events/#__codelineno-12-11>)    calls := event.Content.FunctionCalls()
        [](<https://adk.dev/events/#__codelineno-12-12>)    if len(calls) > 0 {
        [](<https://adk.dev/events/#__codelineno-12-13>)        for _, call := range calls {
        [](<https://adk.dev/events/#__codelineno-12-14>)            toolName := call.Name
        [](<https://adk.dev/events/#__codelineno-12-15>)            arguments := call.Args
        [](<https://adk.dev/events/#__codelineno-12-16>)            fmt.Printf("  Tool: %s, Args: %v\n", toolName, arguments)
        [](<https://adk.dev/events/#__codelineno-12-17>)            // Application might dispatch execution based on this
        [](<https://adk.dev/events/#__codelineno-12-18>)        }
        [](<https://adk.dev/events/#__codelineno-12-19>)    }
        [](<https://adk.dev/events/#__codelineno-12-20>)}
        
        [](<https://adk.dev/events/#__codelineno-13-1>)import com.google.genai.types.FunctionCall;
        [](<https://adk.dev/events/#__codelineno-13-2>)import com.google.common.collect.ImmutableList;
        [](<https://adk.dev/events/#__codelineno-13-3>)import java.util.Map;
        [](<https://adk.dev/events/#__codelineno-13-4>)
        [](<https://adk.dev/events/#__codelineno-13-5>)ImmutableList<FunctionCall> calls = event.functionCalls(); // from Event.java
        [](<https://adk.dev/events/#__codelineno-13-6>)if (!calls.isEmpty()) {
        [](<https://adk.dev/events/#__codelineno-13-7>)  for (FunctionCall call : calls) {
        [](<https://adk.dev/events/#__codelineno-13-8>)    String toolName = call.name().get();
        [](<https://adk.dev/events/#__codelineno-13-9>)    // args is Optional<Map<String, Object>>
        [](<https://adk.dev/events/#__codelineno-13-10>)    Map<String, Object> arguments = call.args().get();
        [](<https://adk.dev/events/#__codelineno-13-11>)           System.out.println("  Tool: " + toolName + ", Args: " + arguments);
        [](<https://adk.dev/events/#__codelineno-13-12>)    // Application might dispatch execution based on this
        [](<https://adk.dev/events/#__codelineno-13-13>)  }
        [](<https://adk.dev/events/#__codelineno-13-14>)}
        
  * **Function Response Details:**

PythonTypeScriptGoJava
        
        [](<https://adk.dev/events/#__codelineno-14-1>)responses = event.get_function_responses()
        [](<https://adk.dev/events/#__codelineno-14-2>)if responses:
        [](<https://adk.dev/events/#__codelineno-14-3>)    for response in responses:
        [](<https://adk.dev/events/#__codelineno-14-4>)        tool_name = response.name
        [](<https://adk.dev/events/#__codelineno-14-5>)        result_dict = response.response # The dictionary returned by the tool
        [](<https://adk.dev/events/#__codelineno-14-6>)        print(f"  Tool Result: {tool_name} -> {result_dict}")
        
        [](<https://adk.dev/events/#__codelineno-15-1>)// Pseudocode: Handle function responses (TypeScript)
        [](<https://adk.dev/events/#__codelineno-15-2>)export function handleFunctionResponses(event: Event) {
        [](<https://adk.dev/events/#__codelineno-15-3>)    const responses = getFunctionResponses(event);
        [](<https://adk.dev/events/#__codelineno-15-4>)    if (responses.length > 0) {
        [](<https://adk.dev/events/#__codelineno-15-5>)        for (const response of responses) {
        [](<https://adk.dev/events/#__codelineno-15-6>)            const toolName = response.name;
        [](<https://adk.dev/events/#__codelineno-15-7>)            const result = response.response; // The object returned by the tool
        [](<https://adk.dev/events/#__codelineno-15-8>)            console.log(`  Tool Result: ${toolName} -> ${JSON.stringify(result)}`);
        [](<https://adk.dev/events/#__codelineno-15-9>)        }
        [](<https://adk.dev/events/#__codelineno-15-10>)    }
        [](<https://adk.dev/events/#__codelineno-15-11>)}
        
        [](<https://adk.dev/events/#__codelineno-16-1>)import (
        [](<https://adk.dev/events/#__codelineno-16-2>)    "fmt"
        [](<https://adk.dev/events/#__codelineno-16-3>)    "google.golang.org/adk/v2/session"
        [](<https://adk.dev/events/#__codelineno-16-4>)    "google.golang.org/genai"
        [](<https://adk.dev/events/#__codelineno-16-5>))
        [](<https://adk.dev/events/#__codelineno-16-6>)
        [](<https://adk.dev/events/#__codelineno-16-7>)func handleFunctionResponses(event *session.Event) {
        [](<https://adk.dev/events/#__codelineno-16-8>)    if event.LLMResponse == nil || event.LLMResponse.Content == nil {
        [](<https://adk.dev/events/#__codelineno-16-9>)        return
        [](<https://adk.dev/events/#__codelineno-16-10>)    }
        [](<https://adk.dev/events/#__codelineno-16-11>)    responses := event.Content.FunctionResponses()
        [](<https://adk.dev/events/#__codelineno-16-12>)    if len(responses) > 0 {
        [](<https://adk.dev/events/#__codelineno-16-13>)        for _, response := range responses {
        [](<https://adk.dev/events/#__codelineno-16-14>)            toolName := response.Name
        [](<https://adk.dev/events/#__codelineno-16-15>)            result := response.Response
        [](<https://adk.dev/events/#__codelineno-16-16>)            fmt.Printf("  Tool Result: %s -> %v\n", toolName, result)
        [](<https://adk.dev/events/#__codelineno-16-17>)        }
        [](<https://adk.dev/events/#__codelineno-16-18>)    }
        [](<https://adk.dev/events/#__codelineno-16-19>)}
        
        [](<https://adk.dev/events/#__codelineno-17-1>)import com.google.genai.types.FunctionResponse;
        [](<https://adk.dev/events/#__codelineno-17-2>)import com.google.common.collect.ImmutableList;
        [](<https://adk.dev/events/#__codelineno-17-3>)import java.util.Map;
        [](<https://adk.dev/events/#__codelineno-17-4>)
        [](<https://adk.dev/events/#__codelineno-17-5>)ImmutableList<FunctionResponse> responses = event.functionResponses(); // from Event.java
        [](<https://adk.dev/events/#__codelineno-17-6>)if (!responses.isEmpty()) {
        [](<https://adk.dev/events/#__codelineno-17-7>)    for (FunctionResponse response : responses) {
        [](<https://adk.dev/events/#__codelineno-17-8>)        String toolName = response.name().get();
        [](<https://adk.dev/events/#__codelineno-17-9>)        Map<String, String> result= response.response().get(); // Check before getting the response
        [](<https://adk.dev/events/#__codelineno-17-10>)        System.out.println("  Tool Result: " + toolName + " -> " + result);
        [](<https://adk.dev/events/#__codelineno-17-11>)    }
        [](<https://adk.dev/events/#__codelineno-17-12>)}
        
  * **Identifiers:**

    * `event.id`: Unique ID for this specific event instance.
    * `event.invocation_id`: ID for the entire user-request-to-final-response cycle this event belongs to. Useful for logging and tracing.

### Detecting Actions and Side Effects[¶](<https://adk.dev/events/#detecting-actions-and-side-effects> "Permanent link")

The `event.actions` object signals changes that occurred or should occur. Always check if `event.actions` and it's fields/ methods exists before accessing them.

  * **State Changes:** Gives you a collection of key-value pairs that were modified in the session state during the step that produced this event.

PythonTypeScriptGoJava

`delta = event.actions.state_delta` (a dictionary of `{key: value}` pairs). 
        
        [](<https://adk.dev/events/#__codelineno-18-1>)if event.actions and event.actions.state_delta:
        [](<https://adk.dev/events/#__codelineno-18-2>)    print(f"  State changes: {event.actions.state_delta}")
        [](<https://adk.dev/events/#__codelineno-18-3>)    # Update local UI or application state if necessary
        
`delta = event.actions.stateDelta` (an object of `{key: value}` pairs). 
        
        [](<https://adk.dev/events/#__codelineno-19-1>)export function handleStateChanges(event: Event) {
        [](<https://adk.dev/events/#__codelineno-19-2>)    if (event.actions && Object.keys(event.actions.stateDelta).length > 0) {
        [](<https://adk.dev/events/#__codelineno-19-3>)        console.log(`  State changes: ${JSON.stringify(event.actions.stateDelta)}`);
        [](<https://adk.dev/events/#__codelineno-19-4>)        // Update local UI or application state if necessary
        [](<https://adk.dev/events/#__codelineno-19-5>)    }
        [](<https://adk.dev/events/#__codelineno-19-6>)}
        
`delta := event.Actions.StateDelta` (a `map[string]any`) 
        
        [](<https://adk.dev/events/#__codelineno-20-1>)import (
        [](<https://adk.dev/events/#__codelineno-20-2>)    "fmt"
        [](<https://adk.dev/events/#__codelineno-20-3>)    "google.golang.org/adk/v2/session"
        [](<https://adk.dev/events/#__codelineno-20-4>))
        [](<https://adk.dev/events/#__codelineno-20-5>)
        [](<https://adk.dev/events/#__codelineno-20-6>)func handleStateChanges(event *session.Event) {
        [](<https://adk.dev/events/#__codelineno-20-7>)    if len(event.Actions.StateDelta) > 0 {
        [](<https://adk.dev/events/#__codelineno-20-8>)        fmt.Printf("  State changes: %v\n", event.Actions.StateDelta)
        [](<https://adk.dev/events/#__codelineno-20-9>)        // Update local UI or application state if necessary
        [](<https://adk.dev/events/#__codelineno-20-10>)    }
        [](<https://adk.dev/events/#__codelineno-20-11>)}
        
`ConcurrentMap<String, Object> delta = event.actions().stateDelta();`
        
        [](<https://adk.dev/events/#__codelineno-21-1>)import java.util.concurrent.ConcurrentMap;
        [](<https://adk.dev/events/#__codelineno-21-2>)import com.google.adk.events.EventActions;
        [](<https://adk.dev/events/#__codelineno-21-3>)
        [](<https://adk.dev/events/#__codelineno-21-4>)EventActions actions = event.actions(); // Assuming event.actions() is not null
        [](<https://adk.dev/events/#__codelineno-21-5>)if (actions != null && actions.stateDelta() != null && !actions.stateDelta().isEmpty()) {
        [](<https://adk.dev/events/#__codelineno-21-6>)    ConcurrentMap<String, Object> stateChanges = actions.stateDelta();
        [](<https://adk.dev/events/#__codelineno-21-7>)    System.out.println("  State changes: " + stateChanges);
        [](<https://adk.dev/events/#__codelineno-21-8>)    // Update local UI or application state if necessary
        [](<https://adk.dev/events/#__codelineno-21-9>)}
        
  * **Artifact Saves:** Gives you a collection indicating which artifacts were saved and their new version number (or relevant `Part` information).

PythonTypeScriptGoJava

`artifact_changes = event.actions.artifact_delta` (a dictionary of `{filename: version}`). 
        
        [](<https://adk.dev/events/#__codelineno-22-1>)if event.actions and event.actions.artifact_delta:
        [](<https://adk.dev/events/#__codelineno-22-2>)    print(f"  Artifacts saved: {event.actions.artifact_delta}")
        [](<https://adk.dev/events/#__codelineno-22-3>)    # UI might refresh an artifact list
        
`artifact_changes = event.actions.artifactDelta` (an object of `{filename: version}`). 
        
        [](<https://adk.dev/events/#__codelineno-23-1>)export function handleArtifactChanges(event: Event) {
        [](<https://adk.dev/events/#__codelineno-23-2>)    if (event.actions && Object.keys(event.actions.artifactDelta).length > 0) {
        [](<https://adk.dev/events/#__codelineno-23-3>)        console.log(`  Artifacts saved: ${JSON.stringify(event.actions.artifactDelta)}`);
        [](<https://adk.dev/events/#__codelineno-23-4>)        // UI might refresh an artifact list
        [](<https://adk.dev/events/#__codelineno-23-5>)    }
        [](<https://adk.dev/events/#__codelineno-23-6>)}
        
`artifactChanges := event.Actions.ArtifactDelta` (a `map[string]int64`) 
        
        [](<https://adk.dev/events/#__codelineno-24-1>)import (
        [](<https://adk.dev/events/#__codelineno-24-2>)    "fmt"
        [](<https://adk.dev/events/#__codelineno-24-3>)    "google.golang.org/adk/v2/artifact"
        [](<https://adk.dev/events/#__codelineno-24-4>)    "google.golang.org/adk/v2/session"
        [](<https://adk.dev/events/#__codelineno-24-5>))
        [](<https://adk.dev/events/#__codelineno-24-6>)
        [](<https://adk.dev/events/#__codelineno-24-7>)func handleArtifactChanges(event *session.Event) {
        [](<https://adk.dev/events/#__codelineno-24-8>)    if len(event.Actions.ArtifactDelta) > 0 {
        [](<https://adk.dev/events/#__codelineno-24-9>)        fmt.Printf("  Artifacts saved: %v\n", event.Actions.ArtifactDelta)
        [](<https://adk.dev/events/#__codelineno-24-10>)        // UI might refresh an artifact list
        [](<https://adk.dev/events/#__codelineno-24-11>)        // Iterate through event.Actions.ArtifactDelta to get filename and artifact.Artifact details
        [](<https://adk.dev/events/#__codelineno-24-12>)        for filename, version := range event.Actions.ArtifactDelta {
        [](<https://adk.dev/events/#__codelineno-24-13>)            fmt.Printf("    Filename: %s, Version: %d\n", filename, version)
        [](<https://adk.dev/events/#__codelineno-24-14>)        }
        [](<https://adk.dev/events/#__codelineno-24-15>)    }
        [](<https://adk.dev/events/#__codelineno-24-16>)}
        
`ConcurrentMap<String, Part> artifactChanges = event.actions().artifactDelta();`
        
        [](<https://adk.dev/events/#__codelineno-25-1>)import java.util.concurrent.ConcurrentMap;
        [](<https://adk.dev/events/#__codelineno-25-2>)import com.google.genai.types.Part;
        [](<https://adk.dev/events/#__codelineno-25-3>)import com.google.adk.events.EventActions;
        [](<https://adk.dev/events/#__codelineno-25-4>)
        [](<https://adk.dev/events/#__codelineno-25-5>)EventActions actions = event.actions(); // Assuming event.actions() is not null
        [](<https://adk.dev/events/#__codelineno-25-6>)if (actions != null && actions.artifactDelta() != null && !actions.artifactDelta().isEmpty()) {
        [](<https://adk.dev/events/#__codelineno-25-7>)    ConcurrentMap<String, Part> artifactChanges = actions.artifactDelta();
        [](<https://adk.dev/events/#__codelineno-25-8>)    System.out.println("  Artifacts saved: " + artifactChanges);
        [](<https://adk.dev/events/#__codelineno-25-9>)    // UI might refresh an artifact list
        [](<https://adk.dev/events/#__codelineno-25-10>)    // Iterate through artifactChanges.entrySet() to get filename and Part details
        [](<https://adk.dev/events/#__codelineno-25-11>)}
        
  * **Control Flow Signals:** Check boolean flags or string values:

PythonTypeScriptGoJava

    * `event.actions.transfer_to_agent` (string): Control should pass to the named agent.
    * `event.actions.escalate` (bool): A loop should terminate.
    * `event.actions.skip_summarization` (bool): A tool result should not be summarized by the LLM. 
          
          [](<https://adk.dev/events/#__codelineno-26-1>)if event.actions:
          [](<https://adk.dev/events/#__codelineno-26-2>)    if event.actions.transfer_to_agent:
          [](<https://adk.dev/events/#__codelineno-26-3>)        print(f"  Signal: Transfer to {event.actions.transfer_to_agent}")
          [](<https://adk.dev/events/#__codelineno-26-4>)    if event.actions.escalate:
          [](<https://adk.dev/events/#__codelineno-26-5>)        print("  Signal: Escalate (terminate loop)")
          [](<https://adk.dev/events/#__codelineno-26-6>)    if event.actions.skip_summarization:
          [](<https://adk.dev/events/#__codelineno-26-7>)        print("  Signal: Skip summarization for tool result")
          
    * `event.actions.transferToAgent` (string): Control should pass to the named agent.
    * `event.actions.escalate` (boolean): A loop should terminate.
    * `event.actions.skipSummarization` (boolean): A tool result should not be summarized by the LLM. 
          
          [](<https://adk.dev/events/#__codelineno-27-1>)export function handleControlFlow(event: Event) {
          [](<https://adk.dev/events/#__codelineno-27-2>)    if (event.actions) {
          [](<https://adk.dev/events/#__codelineno-27-3>)        if (event.actions.transferToAgent) {
          [](<https://adk.dev/events/#__codelineno-27-4>)            console.log(`  Signal: Transfer to ${event.actions.transferToAgent}`);
          [](<https://adk.dev/events/#__codelineno-27-5>)        }
          [](<https://adk.dev/events/#__codelineno-27-6>)        if (event.actions.escalate) {
          [](<https://adk.dev/events/#__codelineno-27-7>)            console.log('  Signal: Escalate (terminate loop)');
          [](<https://adk.dev/events/#__codelineno-27-8>)        }
          [](<https://adk.dev/events/#__codelineno-27-9>)        if (event.actions.skipSummarization) {
          [](<https://adk.dev/events/#__codelineno-27-10>)            console.log('  Signal: Skip summarization for tool result');
          [](<https://adk.dev/events/#__codelineno-27-11>)        }
          [](<https://adk.dev/events/#__codelineno-27-12>)    }
          [](<https://adk.dev/events/#__codelineno-27-13>)}
          
    * `event.Actions.TransferToAgent` (string): Control should pass to the named agent.
    * `event.Actions.Escalate` (bool): A loop should terminate.
    * `event.Actions.SkipSummarization` (bool): A tool result should not be summarized by the LLM. 
          
          [](<https://adk.dev/events/#__codelineno-28-1>)import (
          [](<https://adk.dev/events/#__codelineno-28-2>)    "fmt"
          [](<https://adk.dev/events/#__codelineno-28-3>)    "google.golang.org/adk/v2/session"
          [](<https://adk.dev/events/#__codelineno-28-4>))
          [](<https://adk.dev/events/#__codelineno-28-5>)
          [](<https://adk.dev/events/#__codelineno-28-6>)func handleControlFlow(event *session.Event) {
          [](<https://adk.dev/events/#__codelineno-28-7>)    if event.Actions.TransferToAgent != "" {
          [](<https://adk.dev/events/#__codelineno-28-8>)        fmt.Printf("  Signal: Transfer to %s\n", event.Actions.TransferToAgent)
          [](<https://adk.dev/events/#__codelineno-28-9>)    }
          [](<https://adk.dev/events/#__codelineno-28-10>)    if event.Actions.Escalate {
          [](<https://adk.dev/events/#__codelineno-28-11>)        fmt.Println("  Signal: Escalate (terminate loop)")
          [](<https://adk.dev/events/#__codelineno-28-12>)    }
          [](<https://adk.dev/events/#__codelineno-28-13>)    if event.Actions.SkipSummarization {
          [](<https://adk.dev/events/#__codelineno-28-14>)        fmt.Println("  Signal: Skip summarization for tool result")
          [](<https://adk.dev/events/#__codelineno-28-15>)    }
          [](<https://adk.dev/events/#__codelineno-28-16>)}
          
    * `event.actions().transferToAgent()` (returns `Optional<String>`): Control should pass to the named agent.
    * `event.actions().escalate()` (returns `Optional<Boolean>`): A loop should terminate.
    * `event.actions().skipSummarization()` (returns `Optional<Boolean>`): A tool result should not be summarized by the LLM.
    
    [](<https://adk.dev/events/#__codelineno-29-1>)import com.google.adk.events.EventActions;
    [](<https://adk.dev/events/#__codelineno-29-2>)import java.util.Optional;
    [](<https://adk.dev/events/#__codelineno-29-3>)
    [](<https://adk.dev/events/#__codelineno-29-4>)EventActions actions = event.actions(); // Assuming event.actions() is not null
    [](<https://adk.dev/events/#__codelineno-29-5>)if (actions != null) {
    [](<https://adk.dev/events/#__codelineno-29-6>)    Optional<String> transferAgent = actions.transferToAgent();
    [](<https://adk.dev/events/#__codelineno-29-7>)    if (transferAgent.isPresent()) {
    [](<https://adk.dev/events/#__codelineno-29-8>)        System.out.println("  Signal: Transfer to " + transferAgent.get());
    [](<https://adk.dev/events/#__codelineno-29-9>)    }
    [](<https://adk.dev/events/#__codelineno-29-10>)
    [](<https://adk.dev/events/#__codelineno-29-11>)    Optional<Boolean> escalate = actions.escalate();
    [](<https://adk.dev/events/#__codelineno-29-12>)    if (escalate.orElse(false)) { // or escalate.isPresent() && escalate.get()
    [](<https://adk.dev/events/#__codelineno-29-13>)        System.out.println("  Signal: Escalate (terminate loop)");
    [](<https://adk.dev/events/#__codelineno-29-14>)    }
    [](<https://adk.dev/events/#__codelineno-29-15>)
    [](<https://adk.dev/events/#__codelineno-29-16>)    Optional<Boolean> skipSummarization = actions.skipSummarization();
    [](<https://adk.dev/events/#__codelineno-29-17>)    if (skipSummarization.orElse(false)) { // or skipSummarization.isPresent() && skipSummarization.get()
    [](<https://adk.dev/events/#__codelineno-29-18>)        System.out.println("  Signal: Skip summarization for tool result");
    [](<https://adk.dev/events/#__codelineno-29-19>)    }
    [](<https://adk.dev/events/#__codelineno-29-20>)}
    
### Determining if an Event is a "Final" Response[¶](<https://adk.dev/events/#determining-if-an-event-is-a-final-response> "Permanent link")

Use the built-in helper method `event.is_final_response()` to identify events suitable for display as the agent's complete output for a turn.

  * **Purpose:** Filters out intermediate steps (like tool calls, partial streaming text, internal state updates) from the final user-facing message(s).
  * **When`True`?**
    1. The event contains a tool result (`function_response`) and `skip_summarization` is `True`.
    2. The event contains a tool call (`function_call`) for a tool marked as `is_long_running=True`. In Java, check if the `longRunningToolIds` list is empty:
       * `event.longRunningToolIds().isPresent() && !event.longRunningToolIds().get().isEmpty()` is `true`.
    3. OR, **all** of the following are met:
       * No function calls (`get_function_calls()` is empty).
       * No function responses (`get_function_responses()` is empty).
       * Not a partial stream chunk (`partial` is not `True`).
       * Doesn't end with a code execution result that might need further processing/display.
  * **Usage:** Filter the event stream in your application logic.

PythonTypeScriptGoJava
        
        [](<https://adk.dev/events/#__codelineno-30-1>)# Pseudocode: Handling final responses in application (Python)
        [](<https://adk.dev/events/#__codelineno-30-2>)# full_response_text = ""
        [](<https://adk.dev/events/#__codelineno-30-3>)# async for event in runner.run_async(...):
        [](<https://adk.dev/events/#__codelineno-30-4>)#     # Accumulate streaming text if needed...
        [](<https://adk.dev/events/#__codelineno-30-5>)#     if event.partial and event.content and event.content.parts and event.content.parts[0].text:
        [](<https://adk.dev/events/#__codelineno-30-6>)#         full_response_text += event.content.parts[0].text
        [](<https://adk.dev/events/#__codelineno-30-7>)#
        [](<https://adk.dev/events/#__codelineno-30-8>)#     # Check if it's a final, displayable event
        [](<https://adk.dev/events/#__codelineno-30-9>)#     if event.is_final_response():
        [](<https://adk.dev/events/#__codelineno-30-10>)#         print("\n--- Final Output Detected ---")
        [](<https://adk.dev/events/#__codelineno-30-11>)#         if event.content and event.content.parts and event.content.parts[0].text:
        [](<https://adk.dev/events/#__codelineno-30-12>)#              # If it's the final part of a stream, use accumulated text
        [](<https://adk.dev/events/#__codelineno-30-13>)#              final_text = full_response_text + (event.content.parts[0].text if not event.partial else "")
        [](<https://adk.dev/events/#__codelineno-30-14>)#              print(f"Display to user: {final_text.strip()}")
        [](<https://adk.dev/events/#__codelineno-30-15>)#              full_response_text = "" # Reset accumulator
        [](<https://adk.dev/events/#__codelineno-30-16>)#         elif event.actions and event.actions.skip_summarization and event.get_function_responses():
        [](<https://adk.dev/events/#__codelineno-30-17>)#              # Handle displaying the raw tool result if needed
        [](<https://adk.dev/events/#__codelineno-30-18>)#              response_data = event.get_function_responses()[0].response
        [](<https://adk.dev/events/#__codelineno-30-19>)#              print(f"Display raw tool result: {response_data}")
        [](<https://adk.dev/events/#__codelineno-30-20>)#         elif hasattr(event, 'long_running_tool_ids') and event.long_running_tool_ids:
        [](<https://adk.dev/events/#__codelineno-30-21>)#              print("Display message: Tool is running in background...")
        [](<https://adk.dev/events/#__codelineno-30-22>)#         else:
        [](<https://adk.dev/events/#__codelineno-30-23>)#              # Handle other types of final responses if applicable
        [](<https://adk.dev/events/#__codelineno-30-24>)#              print("Display: Final non-textual response or signal.")
        
        [](<https://adk.dev/events/#__codelineno-31-1>)// Pseudocode: Handling final responses in application (TypeScript)
        [](<https://adk.dev/events/#__codelineno-31-2>)import {
        [](<https://adk.dev/events/#__codelineno-31-3>)    Event,
        [](<https://adk.dev/events/#__codelineno-31-4>)    getFunctionResponses,
        [](<https://adk.dev/events/#__codelineno-31-5>)    isFinalResponse,
        [](<https://adk.dev/events/#__codelineno-31-6>)    stringifyContent
        [](<https://adk.dev/events/#__codelineno-31-7>)} from '@google/adk';
        [](<https://adk.dev/events/#__codelineno-31-8>)
        [](<https://adk.dev/events/#__codelineno-31-9>)async function handleFinalResponses(runnerEvents: AsyncIterable<Event>) {
        [](<https://adk.dev/events/#__codelineno-31-10>)    let fullResponseText = '';
        [](<https://adk.dev/events/#__codelineno-31-11>)
        [](<https://adk.dev/events/#__codelineno-31-12>)    for await (const event of runnerEvents) {
        [](<https://adk.dev/events/#__codelineno-31-13>)        // Accumulate streaming text if needed...
        [](<https://adk.dev/events/#__codelineno-31-14>)        if (event.partial) {
        [](<https://adk.dev/events/#__codelineno-31-15>)            fullResponseText += stringifyContent(event);
        [](<https://adk.dev/events/#__codelineno-31-16>)        }
        [](<https://adk.dev/events/#__codelineno-31-17>)
        [](<https://adk.dev/events/#__codelineno-31-18>)        // Check if it's a final, displayable event
        [](<https://adk.dev/events/#__codelineno-31-19>)        if (isFinalResponse(event)) {
        [](<https://adk.dev/events/#__codelineno-31-20>)            console.log('\n--- Final Output Detected ---');
        [](<https://adk.dev/events/#__codelineno-31-21>)
        [](<https://adk.dev/events/#__codelineno-31-22>)            const eventText = stringifyContent(event);
        [](<https://adk.dev/events/#__codelineno-31-23>)            if (fullResponseText || eventText) {
        [](<https://adk.dev/events/#__codelineno-31-24>)                // If it's the final part of a stream (or a single message), use accumulated text
        [](<https://adk.dev/events/#__codelineno-31-25>)                const finalText = fullResponseText + (event.partial ? '' : eventText);
        [](<https://adk.dev/events/#__codelineno-31-26>)                console.log(`Display to user: ${finalText.trim()}`);
        [](<https://adk.dev/events/#__codelineno-31-27>)                fullResponseText = ''; // Reset accumulator
        [](<https://adk.dev/events/#__codelineno-31-28>)            } else if (
        [](<https://adk.dev/events/#__codelineno-31-29>)                event.actions?.skipSummarization &&
        [](<https://adk.dev/events/#__codelineno-31-30>)                getFunctionResponses(event).length > 0
        [](<https://adk.dev/events/#__codelineno-31-31>)            ) {
        [](<https://adk.dev/events/#__codelineno-31-32>)                // Handle displaying the raw tool result if needed
        [](<https://adk.dev/events/#__codelineno-31-33>)                const responseData = getFunctionResponses(event)[0].response;
        [](<https://adk.dev/events/#__codelineno-31-34>)                console.log(`Display raw tool result: ${JSON.stringify(responseData)}`);
        [](<https://adk.dev/events/#__codelineno-31-35>)            } else if (event.longRunningToolIds && event.longRunningToolIds.length > 0) {
        [](<https://adk.dev/events/#__codelineno-31-36>)                console.log('Display message: Tool is running in background...');
        [](<https://adk.dev/events/#__codelineno-31-37>)            } else {
        [](<https://adk.dev/events/#__codelineno-31-38>)                // Handle other types of final responses if applicable
        [](<https://adk.dev/events/#__codelineno-31-39>)                console.log('Display: Final non-textual response or signal.');
        [](<https://adk.dev/events/#__codelineno-31-40>)            }
        [](<https://adk.dev/events/#__codelineno-31-41>)        }
        [](<https://adk.dev/events/#__codelineno-31-42>)    }
        [](<https://adk.dev/events/#__codelineno-31-43>)}
        
        [](<https://adk.dev/events/#__codelineno-32-1>)// Pseudocode: Handling final responses in application (Go)
        [](<https://adk.dev/events/#__codelineno-32-2>)import (
        [](<https://adk.dev/events/#__codelineno-32-3>)    "fmt"
        [](<https://adk.dev/events/#__codelineno-32-4>)    "strings"
        [](<https://adk.dev/events/#__codelineno-32-5>)    "google.golang.org/adk/v2/session"
        [](<https://adk.dev/events/#__codelineno-32-6>)    "google.golang.org/genai"
        [](<https://adk.dev/events/#__codelineno-32-7>))
        [](<https://adk.dev/events/#__codelineno-32-8>)
        [](<https://adk.dev/events/#__codelineno-32-9>)// isFinalResponse checks if an event is a final response suitable for display.
        [](<https://adk.dev/events/#__codelineno-32-10>)func isFinalResponse(event *session.Event) bool {
        [](<https://adk.dev/events/#__codelineno-32-11>)    if event.LLMResponse != nil {
        [](<https://adk.dev/events/#__codelineno-32-12>)        // Condition 1: Tool result with skip summarization.
        [](<https://adk.dev/events/#__codelineno-32-13>)        if event.LLMResponse.Content != nil && len(event.LLMResponse.Content.FunctionResponses()) > 0 && event.Actions.SkipSummarization {
        [](<https://adk.dev/events/#__codelineno-32-14>)            return true
        [](<https://adk.dev/events/#__codelineno-32-15>)        }
        [](<https://adk.dev/events/#__codelineno-32-16>)        // Condition 2: Long-running tool call.
        [](<https://adk.dev/events/#__codelineno-32-17>)        if len(event.LongRunningToolIDs) > 0 {
        [](<https://adk.dev/events/#__codelineno-32-18>)            return true
        [](<https://adk.dev/events/#__codelineno-32-19>)        }
        [](<https://adk.dev/events/#__codelineno-32-20>)        // Condition 3: A complete message without tool calls or responses.
        [](<https://adk.dev/events/#__codelineno-32-21>)        if (event.LLMResponse.Content == nil ||
        [](<https://adk.dev/events/#__codelineno-32-22>)            (len(event.LLMResponse.Content.FunctionCalls()) == 0 && len(event.LLMResponse.Content.FunctionResponses()) == 0)) &&
        [](<https://adk.dev/events/#__codelineno-32-23>)            !event.LLMResponse.Partial {
        [](<https://adk.dev/events/#__codelineno-32-24>)            return true
        [](<https://adk.dev/events/#__codelineno-32-25>)        }
        [](<https://adk.dev/events/#__codelineno-32-26>)    }
        [](<https://adk.dev/events/#__codelineno-32-27>)    return false
        [](<https://adk.dev/events/#__codelineno-32-28>)}
        [](<https://adk.dev/events/#__codelineno-32-29>)
        [](<https://adk.dev/events/#__codelineno-32-30>)func handleFinalResponses() {
        [](<https://adk.dev/events/#__codelineno-32-31>)    var fullResponseText strings.Builder
        [](<https://adk.dev/events/#__codelineno-32-32>)    // for event := range runner.Run(...) { // Example loop
        [](<https://adk.dev/events/#__codelineno-32-33>)    //  // Accumulate streaming text if needed...
        [](<https://adk.dev/events/#__codelineno-32-34>)    //  if event.LLMResponse != nil && event.LLMResponse.Partial && event.LLMResponse.Content != nil {
        [](<https://adk.dev/events/#__codelineno-32-35>)    //      if len(event.LLMResponse.Content.Parts) > 0 && event.LLMResponse.Content.Parts[0].Text != "" {
        [](<https://adk.dev/events/#__codelineno-32-36>)    //          fullResponseText.WriteString(event.LLMResponse.Content.Parts[0].Text)
        [](<https://adk.dev/events/#__codelineno-32-37>)    //      }
        [](<https://adk.dev/events/#__codelineno-32-38>)    //  }
        [](<https://adk.dev/events/#__codelineno-32-39>)    //
        [](<https://adk.dev/events/#__codelineno-32-40>)    //  // Check if it's a final, displayable event
        [](<https://adk.dev/events/#__codelineno-32-41>)    //  if isFinalResponse(event) {
        [](<https://adk.dev/events/#__codelineno-32-42>)    //      fmt.Println("\n--- Final Output Detected ---")
        [](<https://adk.dev/events/#__codelineno-32-43>)    //      if event.LLMResponse != nil && event.LLMResponse.Content != nil {
        [](<https://adk.dev/events/#__codelineno-32-44>)    //          if len(event.LLMResponse.Content.Parts) > 0 && event.LLMResponse.Content.Parts[0].Text != "" {
        [](<https://adk.dev/events/#__codelineno-32-45>)    //              // If it's the final part of a stream, use accumulated text
        [](<https://adk.dev/events/#__codelineno-32-46>)    //              finalText := fullResponseText.String()
        [](<https://adk.dev/events/#__codelineno-32-47>)    //              if !event.LLMResponse.Partial {
        [](<https://adk.dev/events/#__codelineno-32-48>)    //                  finalText += event.LLMResponse.Content.Parts[0].Text
        [](<https://adk.dev/events/#__codelineno-32-49>)    //              }
        [](<https://adk.dev/events/#__codelineno-32-50>)    //              fmt.Printf("Display to user: %s\n", strings.TrimSpace(finalText))
        [](<https://adk.dev/events/#__codelineno-32-51>)    //              fullResponseText.Reset() // Reset accumulator
        [](<https://adk.dev/events/#__codelineno-32-52>)    //          }
        [](<https://adk.dev/events/#__codelineno-32-53>)    //      } else if event.Actions.SkipSummarization && event.LLMResponse.Content != nil && len(event.LLMResponse.Content.FunctionResponses()) > 0 {
        [](<https://adk.dev/events/#__codelineno-32-54>)    //          // Handle displaying the raw tool result if needed
        [](<https://adk.dev/events/#__codelineno-32-55>)    //          responseData := event.LLMResponse.Content.FunctionResponses()[0].Response
        [](<https://adk.dev/events/#__codelineno-32-56>)    //          fmt.Printf("Display raw tool result: %v\n", responseData)
        [](<https://adk.dev/events/#__codelineno-32-57>)    //      } else if len(event.LongRunningToolIDs) > 0 {
        [](<https://adk.dev/events/#__codelineno-32-58>)    //          fmt.Println("Display message: Tool is running in background...")
        [](<https://adk.dev/events/#__codelineno-32-59>)    //      } else {
        [](<https://adk.dev/events/#__codelineno-32-60>)    //          // Handle other types of final responses if applicable
        [](<https://adk.dev/events/#__codelineno-32-61>)    //          fmt.Println("Display: Final non-textual response or signal.")
        [](<https://adk.dev/events/#__codelineno-32-62>)    //      }
        [](<https://adk.dev/events/#__codelineno-32-63>)    //  }
        [](<https://adk.dev/events/#__codelineno-32-64>)    // }
        [](<https://adk.dev/events/#__codelineno-32-65>)}
        
        [](<https://adk.dev/events/#__codelineno-33-1>)// Pseudocode: Handling final responses in application (Java)
        [](<https://adk.dev/events/#__codelineno-33-2>)import com.google.adk.events.Event;
        [](<https://adk.dev/events/#__codelineno-33-3>)import com.google.genai.types.Content;
        [](<https://adk.dev/events/#__codelineno-33-4>)import com.google.genai.types.FunctionResponse;
        [](<https://adk.dev/events/#__codelineno-33-5>)import java.util.Map;
        [](<https://adk.dev/events/#__codelineno-33-6>)
        [](<https://adk.dev/events/#__codelineno-33-7>)StringBuilder fullResponseText = new StringBuilder();
        [](<https://adk.dev/events/#__codelineno-33-8>)runner.run(...).forEach(event -> { // Assuming a stream of events
        [](<https://adk.dev/events/#__codelineno-33-9>)     // Accumulate streaming text if needed...
        [](<https://adk.dev/events/#__codelineno-33-10>)     if (event.partial().orElse(false) && event.content().isPresent()) {
        [](<https://adk.dev/events/#__codelineno-33-11>)         event.content().flatMap(Content::parts).ifPresent(parts -> {
        [](<https://adk.dev/events/#__codelineno-33-12>)             if (!parts.isEmpty() && parts.get(0).text().isPresent()) {
        [](<https://adk.dev/events/#__codelineno-33-13>)                 fullResponseText.append(parts.get(0).text().get());
        [](<https://adk.dev/events/#__codelineno-33-14>)            }
        [](<https://adk.dev/events/#__codelineno-33-15>)         });
        [](<https://adk.dev/events/#__codelineno-33-16>)     }
        [](<https://adk.dev/events/#__codelineno-33-17>)
        [](<https://adk.dev/events/#__codelineno-33-18>)     // Check if it's a final, displayable event
        [](<https://adk.dev/events/#__codelineno-33-19>)     if (event.finalResponse()) { // Using the method from Event.java
        [](<https://adk.dev/events/#__codelineno-33-20>)         System.out.println("\n--- Final Output Detected ---");
        [](<https://adk.dev/events/#__codelineno-33-21>)         if (event.content().isPresent() &&
        [](<https://adk.dev/events/#__codelineno-33-22>)             event.content().flatMap(Content::parts).map(parts -> !parts.isEmpty() && parts.get(0).text().isPresent()).orElse(false)) {
        [](<https://adk.dev/events/#__codelineno-33-23>)             // If it's the final part of a stream, use accumulated text
        [](<https://adk.dev/events/#__codelineno-33-24>)             String eventText = event.content().get().parts().get().get(0).text().get();
        [](<https://adk.dev/events/#__codelineno-33-25>)             String finalText = fullResponseText.toString() + (event.partial().orElse(false) ? "" : eventText);
        [](<https://adk.dev/events/#__codelineno-33-26>)             System.out.println("Display to user: " + finalText.trim());
        [](<https://adk.dev/events/#__codelineno-33-27>)             fullResponseText.setLength(0); // Reset accumulator
        [](<https://adk.dev/events/#__codelineno-33-28>)         } else if (event.actions() != null && event.actions().skipSummarization().orElse(false)
        [](<https://adk.dev/events/#__codelineno-33-29>)                    && !event.functionResponses().isEmpty()) {
        [](<https://adk.dev/events/#__codelineno-33-30>)             // Handle displaying the raw tool result if needed,
        [](<https://adk.dev/events/#__codelineno-33-31>)             // especially if finalResponse() was true due to other conditions
        [](<https://adk.dev/events/#__codelineno-33-32>)             // or if you want to display skipped summarization results regardless of finalResponse()
        [](<https://adk.dev/events/#__codelineno-33-33>)             Map<String, Object> responseData = event.functionResponses().get(0).response().get();
        [](<https://adk.dev/events/#__codelineno-33-34>)             System.out.println("Display raw tool result: " + responseData);
        [](<https://adk.dev/events/#__codelineno-33-35>)         } else if (event.longRunningToolIds().isPresent() && !event.longRunningToolIds().get().isEmpty()) {
        [](<https://adk.dev/events/#__codelineno-33-36>)             // This case is covered by event.finalResponse()
        [](<https://adk.dev/events/#__codelineno-33-37>)             System.out.println("Display message: Tool is running in background...");
        [](<https://adk.dev/events/#__codelineno-33-38>)         } else {
        [](<https://adk.dev/events/#__codelineno-33-39>)             // Handle other types of final responses if applicable
        [](<https://adk.dev/events/#__codelineno-33-40>)             System.out.println("Display: Final non-textual response or signal.");
        [](<https://adk.dev/events/#__codelineno-33-41>)         }
        [](<https://adk.dev/events/#__codelineno-33-42>)     }
        [](<https://adk.dev/events/#__codelineno-33-43>) });
        
By carefully examining these aspects of an event, you can build robust applications that react appropriately to the rich information flowing through the ADK system.

## How Events Flow: Generation and Processing[¶](<https://adk.dev/events/#how-events-flow-generation-and-processing> "Permanent link")

Events are created at different points and processed systematically by the framework. Understanding this flow helps clarify how actions and history are managed.

  * **Generation Sources:**

    * **User Input:** The `Runner` typically wraps initial user messages or mid-conversation inputs into an `Event` with `author='user'`.
    * **Agent Logic:** Agents (`BaseAgent`, `LlmAgent`) explicitly `yield Event(...)` objects (setting `author=self.name`) to communicate responses or signal actions.
    * **LLM Responses:** The ADK model integration layer translates raw LLM output (text, function calls, errors) into `Event` objects, authored by the calling agent.
    * **Tool Results:** After a tool executes, the framework generates an `Event` containing the `function_response`. The `author` is typically the agent that requested the tool, while the `role` inside the `content` is set to `'user'` for the LLM history.
  * **Processing Flow:**

    1. **Yield/Return:** An event is generated and yielded (Python) or returned/emitted (Java) by its source.
    2. **Runner Receives:** The main `Runner` executing the agent receives the event.
    3. **SessionService Processing:** The `Runner` sends the event to the configured `SessionService`. This is a critical step:
       * **Applies Deltas:** The service merges `event.actions.state_delta` into `session.state` and updates internal records based on `event.actions.artifact_delta`. (Note: The actual artifact _saving_ usually happened earlier when `context.save_artifact` was called).
       * **Finalizes Metadata:** Assigns a unique `event.id` if not present, may update `event.timestamp`.
       * **Persists to History:** Appends the processed event to the `session.events` list.
    4. **External Yield:** The `Runner` yields (Python) or returns/emits (Java) the processed event outwards to the calling application (e.g., the code that invoked `runner.run_async`).

This flow ensures that state changes and history are consistently recorded alongside the communication content of each event.

## Common Event Examples (Illustrative Patterns)[¶](<https://adk.dev/events/#common-event-examples-illustrative-patterns> "Permanent link")

Here are concise examples of typical events you might see in the stream:

  * **User Input:**
        
        [](<https://adk.dev/events/#__codelineno-34-1>){
        [](<https://adk.dev/events/#__codelineno-34-2>)  "author": "user",
        [](<https://adk.dev/events/#__codelineno-34-3>)  "invocation_id": "e-xyz...",
        [](<https://adk.dev/events/#__codelineno-34-4>)  "content": {"parts": [{"text": "Book a flight to London for next Tuesday"}]}
        [](<https://adk.dev/events/#__codelineno-34-5>)  // actions usually empty
        [](<https://adk.dev/events/#__codelineno-34-6>)}
        
  * **Agent Final Text Response:** (`is_final_response() == True`) 
        
        [](<https://adk.dev/events/#__codelineno-35-1>){
        [](<https://adk.dev/events/#__codelineno-35-2>)  "author": "TravelAgent",
        [](<https://adk.dev/events/#__codelineno-35-3>)  "invocation_id": "e-xyz...",
        [](<https://adk.dev/events/#__codelineno-35-4>)  "content": {"parts": [{"text": "Okay, I can help with that. Could you confirm the departure city?"}]},
        [](<https://adk.dev/events/#__codelineno-35-5>)  "partial": false,
        [](<https://adk.dev/events/#__codelineno-35-6>)  "turn_complete": true
        [](<https://adk.dev/events/#__codelineno-35-7>)  // actions might have state delta, etc.
        [](<https://adk.dev/events/#__codelineno-35-8>)}
        
  * **Agent Streaming Text Response:** (`is_final_response() == False`) 
        
        [](<https://adk.dev/events/#__codelineno-36-1>){
        [](<https://adk.dev/events/#__codelineno-36-2>)  "author": "SummaryAgent",
        [](<https://adk.dev/events/#__codelineno-36-3>)  "invocation_id": "e-abc...",
        [](<https://adk.dev/events/#__codelineno-36-4>)  "content": {"parts": [{"text": "The document discusses three main points:"}]},
        [](<https://adk.dev/events/#__codelineno-36-5>)  "partial": true,
        [](<https://adk.dev/events/#__codelineno-36-6>)  "turn_complete": false
        [](<https://adk.dev/events/#__codelineno-36-7>)}
        [](<https://adk.dev/events/#__codelineno-36-8>)// ... more partial=True events follow ...
        
  * **Tool Call Request (by LLM):** (`is_final_response() == False`) 
        
        [](<https://adk.dev/events/#__codelineno-37-1>){
        [](<https://adk.dev/events/#__codelineno-37-2>)  "author": "TravelAgent",
        [](<https://adk.dev/events/#__codelineno-37-3>)  "invocation_id": "e-xyz...",
        [](<https://adk.dev/events/#__codelineno-37-4>)  "content": {"parts": [{"function_call": {"name": "find_airports", "args": {"city": "London"}}}]}
        [](<https://adk.dev/events/#__codelineno-37-5>)  // actions usually empty
        [](<https://adk.dev/events/#__codelineno-37-6>)}
        
  * **Tool Result Provided (to LLM):** (`is_final_response()` depends on `skip_summarization`) 
        
        [](<https://adk.dev/events/#__codelineno-38-1>){
        [](<https://adk.dev/events/#__codelineno-38-2>)  "author": "TravelAgent", // Author is agent that requested the call
        [](<https://adk.dev/events/#__codelineno-38-3>)  "invocation_id": "e-xyz...",
        [](<https://adk.dev/events/#__codelineno-38-4>)  "content": {
        [](<https://adk.dev/events/#__codelineno-38-5>)    "role": "user", // Role for LLM history
        [](<https://adk.dev/events/#__codelineno-38-6>)    "parts": [{"function_response": {"name": "find_airports", "response": {"result": ["LHR", "LGW", "STN"]}}}]
        [](<https://adk.dev/events/#__codelineno-38-7>)  }
        [](<https://adk.dev/events/#__codelineno-38-8>)  // actions might have skip_summarization=True
        [](<https://adk.dev/events/#__codelineno-38-9>)}
        
  * **State/Artifact Update Only:** (`is_final_response() == False`) 
        
        [](<https://adk.dev/events/#__codelineno-39-1>){
        [](<https://adk.dev/events/#__codelineno-39-2>)  "author": "InternalUpdater",
        [](<https://adk.dev/events/#__codelineno-39-3>)  "invocation_id": "e-def...",
        [](<https://adk.dev/events/#__codelineno-39-4>)  "content": null,
        [](<https://adk.dev/events/#__codelineno-39-5>)  "actions": {
        [](<https://adk.dev/events/#__codelineno-39-6>)    "state_delta": {"user_status": "verified"},
        [](<https://adk.dev/events/#__codelineno-39-7>)    "artifact_delta": {"verification_doc.pdf": 2}
        [](<https://adk.dev/events/#__codelineno-39-8>)  }
        [](<https://adk.dev/events/#__codelineno-39-9>)}
        
  * **Agent Transfer Signal:** (`is_final_response() == False`) 
        
        [](<https://adk.dev/events/#__codelineno-40-1>){
        [](<https://adk.dev/events/#__codelineno-40-2>)  "author": "OrchestratorAgent",
        [](<https://adk.dev/events/#__codelineno-40-3>)  "invocation_id": "e-789...",
        [](<https://adk.dev/events/#__codelineno-40-4>)  "content": {"parts": [{"function_call": {"name": "transfer_to_agent", "args": {"agent_name": "BillingAgent"}}}]},
        [](<https://adk.dev/events/#__codelineno-40-5>)  "actions": {"transfer_to_agent": "BillingAgent"} // Added by framework
        [](<https://adk.dev/events/#__codelineno-40-6>)}
        
  * **Loop Escalation Signal:** (`is_final_response() == False`) 
        
        [](<https://adk.dev/events/#__codelineno-41-1>){
        [](<https://adk.dev/events/#__codelineno-41-2>)  "author": "CheckerAgent",
        [](<https://adk.dev/events/#__codelineno-41-3>)  "invocation_id": "e-loop...",
        [](<https://adk.dev/events/#__codelineno-41-4>)  "content": {"parts": [{"text": "Maximum retries reached."}]}, // Optional content
        [](<https://adk.dev/events/#__codelineno-41-5>)  "actions": {"escalate": true}
        [](<https://adk.dev/events/#__codelineno-41-6>)}
        
## Additional Context and Event Details[¶](<https://adk.dev/events/#additional-context-and-event-details> "Permanent link")

Beyond the core concepts, here are a few specific details about context and events that are important for certain use cases:

  1. **`ToolContext.function_call_id` (Linking Tool Actions):**

     * When an LLM requests a tool (FunctionCall), that request has an ID. The `ToolContext` provided to your tool function includes this `function_call_id`.
     * **Importance:** This ID is crucial for linking actions like authentication back to the specific tool request that initiated them, especially if multiple tools are called in one turn. The framework uses this ID internally.
  2. **How State/Artifact Changes are Recorded:**

     * When you modify state or save an artifact using `CallbackContext` or `ToolContext`, these changes aren't immediately written to persistent storage.
     * Instead, they populate the `state_delta` and `artifact_delta` fields within the `EventActions` object.
     * This `EventActions` object is attached to the _next event_ generated after the change (e.g., the agent's response or a tool result event).
     * The `SessionService.append_event` method reads these deltas from the incoming event and applies them to the session's persistent state and artifact records. This ensures changes are tied chronologically to the event stream.
  3. **State Scope Prefixes (`app:`, `user:`, `temp:`):**

     * When managing state via `context.state`, you can optionally use prefixes:
       * `app:my_setting`: Suggests state relevant to the entire application (requires a persistent `SessionService`).
       * `user:user_preference`: Suggests state relevant to the specific user across sessions (requires a persistent `SessionService`).
       * `temp:intermediate_result` or no prefix: Typically session-specific or temporary state for the current invocation.
     * The underlying `SessionService` determines how these prefixes are handled for persistence.
  4. **Error Events:**

     * An `Event` can represent an error. Check the `event.error_code` and `event.error_message` fields (inherited from `LlmResponse`).
     * Errors might originate from the LLM (e.g., safety filters, resource limits) or potentially be packaged by the framework if a tool fails critically. Check tool `FunctionResponse` content for typical tool-specific errors. 
           
           [](<https://adk.dev/events/#__codelineno-42-1>)// Example Error Event (conceptual)
           [](<https://adk.dev/events/#__codelineno-42-2>){
           [](<https://adk.dev/events/#__codelineno-42-3>)  "author": "LLMAgent",
           [](<https://adk.dev/events/#__codelineno-42-4>)  "invocation_id": "e-err...",
           [](<https://adk.dev/events/#__codelineno-42-5>)  "content": null,
           [](<https://adk.dev/events/#__codelineno-42-6>)  "error_code": "SAFETY_FILTER_TRIGGERED",
           [](<https://adk.dev/events/#__codelineno-42-7>)  "error_message": "Response blocked due to safety settings.",
           [](<https://adk.dev/events/#__codelineno-42-8>)  "actions": {}
           [](<https://adk.dev/events/#__codelineno-42-9>)}
           
These details provide a more complete picture for advanced use cases involving tool authentication, state persistence scope, and error handling within the event stream.

## Best Practices for Working with Events[¶](<https://adk.dev/events/#best-practices-for-working-with-events> "Permanent link")

To use events effectively in your ADK applications:

  * **Clear Authorship:** When building custom agents, ensure correct attribution for agent actions in the history. The framework generally handles authorship correctly for LLM/tool events.

PythonTypeScriptGoJava

Use `yield Event(author=self.name, ...)` in `BaseAgent` subclasses.

When constructing an `Event` in your custom agent logic, set the author, for example: `createEvent({ author: this.name, ... })`

In custom agent `Run` methods, the framework typically handles authorship. If creating an event manually, set the author: `yield(&session.Event{Author: a.name, ...}, nil)`

When constructing an `Event` in your custom agent logic, set the author, for example: `Event.builder().author(this.getAgentName()) // ... .build();`

  * **Semantic Content & Actions:** Use `event.content` for the core message/data (text, function call/response). Use `event.actions` specifically for signaling side effects (state/artifact deltas) or control flow (`transfer`, `escalate`, `skip_summarization`).

  * **Idempotency Awareness:** Understand that the `SessionService` is responsible for applying the state/artifact changes signaled in `event.actions`. While ADK services aim for consistency, consider potential downstream effects if your application logic re-processes events.
  * **Use`is_final_response()`:** Rely on this helper method in your application/UI layer to identify complete, user-facing text responses. Avoid manually replicating its logic.
  * **Leverage History:** The session's event list is your primary debugging tool. Examine the sequence of authors, content, and actions to trace execution and diagnose issues.
  * **Use Metadata:** Use `invocation_id` to correlate all events within a single user interaction. Use `event.id` to reference specific, unique occurrences.

Treating events as structured messages with clear purposes for their content and actions is key to building, debugging, and managing complex agent behaviors in ADK.

Back to top 