# Callbacks: Observe, Customize, and Control Agent Behavior - Agent Development Kit (ADK)

> Source: [https://adk.dev/callbacks/](https://adk.dev/callbacks/)

[ Skip to content ](<https://adk.dev/callbacks/#callbacks-observe-customize-and-control-agent-behavior>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/callbacks/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/callbacks/index.md> "View this page as Markdown")

# Callbacks: Observe, Customize, and Control Agent Behavior[¶](<https://adk.dev/callbacks/#callbacks-observe-customize-and-control-agent-behavior> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

Callbacks are a cornerstone feature of ADK, providing a powerful mechanism to hook into an agent's execution process. They allow you to observe, customize, and even control the agent's behavior at specific, predefined points without modifying the core ADK framework code.

**What are they?** In essence, callbacks are standard functions that you define. You then associate these functions with an agent when you create it. The ADK framework automatically calls your functions at key stages, letting you observe or intervene. Think of it like checkpoints during the agent's process:

  * **Before the agent starts its main work on a request, and after it finishes:** When you ask an agent to do something (e.g., answer a question), it runs its internal logic to figure out the response.
  * The `Before Agent` callback executes _right before_ this main work begins for that specific request.
  * The `After Agent` callback executes _right after_ the agent has finished all its steps for that request and has prepared the final result, but just before the result is returned.
  * This "main work" encompasses the agent's _entire_ process for handling that single request. This might involve deciding to call an LLM, actually calling the LLM, deciding to use a tool, using the tool, processing the results, and finally putting together the answer. These callbacks essentially wrap the whole sequence from receiving the input to producing the final output for that one interaction.
  * **Before sending a request to, or after receiving a response from, the Large Language Model (LLM):** These callbacks (`Before Model`, `After Model`) allow you to inspect or modify the data going to and coming from the LLM specifically.
  * **Before executing a tool (like a Python function or another agent) or after it finishes:** Similarly, `Before Tool` and `After Tool` callbacks give you control points specifically around the execution of tools invoked by the agent.

![intro_components.png](https://adk.dev/assets/callback_flow.png)

**Why use them?** Callbacks unlock significant flexibility and enable advanced agent capabilities:

  * **Observe & Debug:** Log detailed information at critical steps for monitoring and troubleshooting.
  * **Customize & Control:** Modify data flowing through the agent (like LLM requests or tool results) or even bypass certain steps entirely based on your logic.
  * **Implement Guardrails:** Enforce safety rules, validate inputs/outputs, or prevent disallowed operations.
  * **Manage State:** Read or dynamically update the agent's session state during execution.
  * **Integrate & Enhance:** Trigger external actions (API calls, notifications) or add features like caching.

Tip

When implementing security guardrails and policies, use ADK Plugins for better modularity and flexibility than Callbacks. For more details, see [Callbacks and Plugins for Security Guardrails](<https://adk.dev/safety/#callbacks-and-plugins-for-security-guardrails>).

**How are they added:**

Code

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/callbacks/#__codelineno-0-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/#__codelineno-0-2>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/callbacks/#__codelineno-0-3>)from google.adk.models import LlmResponse, LlmRequest
    [](<https://adk.dev/callbacks/#__codelineno-0-4>)from typing import Optional
    [](<https://adk.dev/callbacks/#__codelineno-0-5>)
    [](<https://adk.dev/callbacks/#__codelineno-0-6>)# --- Define your callback function ---
    [](<https://adk.dev/callbacks/#__codelineno-0-7>)def my_before_model_logic(
    [](<https://adk.dev/callbacks/#__codelineno-0-8>)    callback_context: CallbackContext, llm_request: LlmRequest
    [](<https://adk.dev/callbacks/#__codelineno-0-9>)) -> Optional[LlmResponse]:
    [](<https://adk.dev/callbacks/#__codelineno-0-10>)    print(f"Callback running before model call for agent: {callback_context.agent_name}")
    [](<https://adk.dev/callbacks/#__codelineno-0-11>)    # ... your custom logic here ...
    [](<https://adk.dev/callbacks/#__codelineno-0-12>)    return None # Allow the model call to proceed
    [](<https://adk.dev/callbacks/#__codelineno-0-13>)
    [](<https://adk.dev/callbacks/#__codelineno-0-14>)# --- Register it during Agent creation ---
    [](<https://adk.dev/callbacks/#__codelineno-0-15>)my_agent = LlmAgent(
    [](<https://adk.dev/callbacks/#__codelineno-0-16>)    name="MyCallbackAgent",
    [](<https://adk.dev/callbacks/#__codelineno-0-17>)    model="gemini-2.0-flash", # Or your desired model
    [](<https://adk.dev/callbacks/#__codelineno-0-18>)    instruction="Be helpful.",
    [](<https://adk.dev/callbacks/#__codelineno-0-19>)    # Other agent parameters...
    [](<https://adk.dev/callbacks/#__codelineno-0-20>)    before_model_callback=my_before_model_logic # Pass the function here
    [](<https://adk.dev/callbacks/#__codelineno-0-21>))
    
    [](<https://adk.dev/callbacks/#__codelineno-1-1>)import { LlmAgent, InMemoryRunner, Context, LlmRequest, LlmResponse, Event, isFinalResponse } from '@google/adk';
    [](<https://adk.dev/callbacks/#__codelineno-1-2>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/#__codelineno-1-3>)import type { Content } from "@google/genai";
    [](<https://adk.dev/callbacks/#__codelineno-1-4>)
    [](<https://adk.dev/callbacks/#__codelineno-1-5>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/#__codelineno-1-6>)const APP_NAME = "basic_callback_app";
    [](<https://adk.dev/callbacks/#__codelineno-1-7>)const USER_ID = "test_user_basic";
    [](<https://adk.dev/callbacks/#__codelineno-1-8>)const SESSION_ID = "session_basic_001";
    [](<https://adk.dev/callbacks/#__codelineno-1-9>)
    [](<https://adk.dev/callbacks/#__codelineno-1-10>)
    [](<https://adk.dev/callbacks/#__codelineno-1-11>)// --- Define your callback function ---
    [](<https://adk.dev/callbacks/#__codelineno-1-12>)function myBeforeModelLogic({
    [](<https://adk.dev/callbacks/#__codelineno-1-13>)  context,
    [](<https://adk.dev/callbacks/#__codelineno-1-14>)  request,
    [](<https://adk.dev/callbacks/#__codelineno-1-15>)}: {
    [](<https://adk.dev/callbacks/#__codelineno-1-16>)  context: Context;
    [](<https://adk.dev/callbacks/#__codelineno-1-17>)  request: LlmRequest;
    [](<https://adk.dev/callbacks/#__codelineno-1-18>)}): LlmResponse | undefined {
    [](<https://adk.dev/callbacks/#__codelineno-1-19>)  console.log(
    [](<https://adk.dev/callbacks/#__codelineno-1-20>)    `Callback running before model call for agent: ${context.agentName}`
    [](<https://adk.dev/callbacks/#__codelineno-1-21>)  );
    [](<https://adk.dev/callbacks/#__codelineno-1-22>)  // ... your custom logic here ...
    [](<https://adk.dev/callbacks/#__codelineno-1-23>)  return undefined; // Allow the model call to proceed
    [](<https://adk.dev/callbacks/#__codelineno-1-24>)}
    [](<https://adk.dev/callbacks/#__codelineno-1-25>)
    [](<https://adk.dev/callbacks/#__codelineno-1-26>)// --- Register it during Agent creation ---
    [](<https://adk.dev/callbacks/#__codelineno-1-27>)const myAgent = new LlmAgent({
    [](<https://adk.dev/callbacks/#__codelineno-1-28>)  name: "MyCallbackAgent",
    [](<https://adk.dev/callbacks/#__codelineno-1-29>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/#__codelineno-1-30>)  instruction: "Be helpful.",
    [](<https://adk.dev/callbacks/#__codelineno-1-31>)  beforeModelCallback: myBeforeModelLogic,
    [](<https://adk.dev/callbacks/#__codelineno-1-32>)});
    
    [](<https://adk.dev/callbacks/#__codelineno-2-1>)package main
    [](<https://adk.dev/callbacks/#__codelineno-2-2>)
    [](<https://adk.dev/callbacks/#__codelineno-2-3>)import (
    [](<https://adk.dev/callbacks/#__codelineno-2-4>)    "context"
    [](<https://adk.dev/callbacks/#__codelineno-2-5>)    "fmt"
    [](<https://adk.dev/callbacks/#__codelineno-2-6>)    "log"
    [](<https://adk.dev/callbacks/#__codelineno-2-7>)    "strings"
    [](<https://adk.dev/callbacks/#__codelineno-2-8>)
    [](<https://adk.dev/callbacks/#__codelineno-2-9>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/#__codelineno-2-10>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/#__codelineno-2-11>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/#__codelineno-2-12>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/#__codelineno-2-13>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/#__codelineno-2-14>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/#__codelineno-2-15>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/#__codelineno-2-16>))
    [](<https://adk.dev/callbacks/#__codelineno-2-17>)
    [](<https://adk.dev/callbacks/#__codelineno-2-18>)
    [](<https://adk.dev/callbacks/#__codelineno-2-19>)
    [](<https://adk.dev/callbacks/#__codelineno-2-20>)// onBeforeModel is a callback function that gets triggered before an LLM call.
    [](<https://adk.dev/callbacks/#__codelineno-2-21>)func onBeforeModel(ctx agent.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
    [](<https://adk.dev/callbacks/#__codelineno-2-22>)    log.Println("--- onBeforeModel Callback Triggered ---")
    [](<https://adk.dev/callbacks/#__codelineno-2-23>)    log.Printf("Model Request to be sent: %v\n", req)
    [](<https://adk.dev/callbacks/#__codelineno-2-24>)    // Returning nil allows the default LLM call to proceed.
    [](<https://adk.dev/callbacks/#__codelineno-2-25>)    return nil, nil
    [](<https://adk.dev/callbacks/#__codelineno-2-26>)}
    [](<https://adk.dev/callbacks/#__codelineno-2-27>)
    [](<https://adk.dev/callbacks/#__codelineno-2-28>)func runBasicExample() {
    [](<https://adk.dev/callbacks/#__codelineno-2-29>)    const (
    [](<https://adk.dev/callbacks/#__codelineno-2-30>)        appName = "CallbackBasicApp"
    [](<https://adk.dev/callbacks/#__codelineno-2-31>)        userID  = "test_user_123"
    [](<https://adk.dev/callbacks/#__codelineno-2-32>)    )
    [](<https://adk.dev/callbacks/#__codelineno-2-33>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/#__codelineno-2-34>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/#__codelineno-2-35>)    if err != nil {
    [](<https://adk.dev/callbacks/#__codelineno-2-36>)        log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/#__codelineno-2-37>)    }
    [](<https://adk.dev/callbacks/#__codelineno-2-38>)
    [](<https://adk.dev/callbacks/#__codelineno-2-39>)    // Register the callback function in the agent configuration.
    [](<https://adk.dev/callbacks/#__codelineno-2-40>)    agentCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/#__codelineno-2-41>)        Name:                 "SimpleAgent",
    [](<https://adk.dev/callbacks/#__codelineno-2-42>)        Model:                geminiModel,
    [](<https://adk.dev/callbacks/#__codelineno-2-43>)        BeforeModelCallbacks: []llmagent.BeforeModelCallback{onBeforeModel},
    [](<https://adk.dev/callbacks/#__codelineno-2-44>)    }
    [](<https://adk.dev/callbacks/#__codelineno-2-45>)    simpleAgent, err := llmagent.New(agentCfg)
    [](<https://adk.dev/callbacks/#__codelineno-2-46>)    if err != nil {
    [](<https://adk.dev/callbacks/#__codelineno-2-47>)        log.Fatalf("Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/#__codelineno-2-48>)    }
    [](<https://adk.dev/callbacks/#__codelineno-2-49>)
    [](<https://adk.dev/callbacks/#__codelineno-2-50>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/#__codelineno-2-51>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/callbacks/#__codelineno-2-52>)        AppName:        appName,
    [](<https://adk.dev/callbacks/#__codelineno-2-53>)        Agent:          simpleAgent,
    [](<https://adk.dev/callbacks/#__codelineno-2-54>)        SessionService: sessionService,
    [](<https://adk.dev/callbacks/#__codelineno-2-55>)    })
    [](<https://adk.dev/callbacks/#__codelineno-2-56>)    if err != nil {
    [](<https://adk.dev/callbacks/#__codelineno-2-57>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/#__codelineno-2-58>)    }
    
    [](<https://adk.dev/callbacks/#__codelineno-3-1>)import com.google.adk.agents.CallbackContext;
    [](<https://adk.dev/callbacks/#__codelineno-3-2>)import com.google.adk.agents.Callbacks;
    [](<https://adk.dev/callbacks/#__codelineno-3-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/#__codelineno-3-4>)import com.google.adk.models.LlmRequest;
    [](<https://adk.dev/callbacks/#__codelineno-3-5>)import java.util.Optional;
    [](<https://adk.dev/callbacks/#__codelineno-3-6>)
    [](<https://adk.dev/callbacks/#__codelineno-3-7>)public class AgentWithBeforeModelCallback {
    [](<https://adk.dev/callbacks/#__codelineno-3-8>)
    [](<https://adk.dev/callbacks/#__codelineno-3-9>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/#__codelineno-3-10>)    // --- Define your callback logic ---
    [](<https://adk.dev/callbacks/#__codelineno-3-11>)    Callbacks.BeforeModelCallbackSync myBeforeModelLogic =
    [](<https://adk.dev/callbacks/#__codelineno-3-12>)        (CallbackContext callbackContext, LlmRequest llmRequest) -> {
    [](<https://adk.dev/callbacks/#__codelineno-3-13>)          System.out.println(
    [](<https://adk.dev/callbacks/#__codelineno-3-14>)              "Callback running before model call for agent: " + callbackContext.agentName());
    [](<https://adk.dev/callbacks/#__codelineno-3-15>)          // ... your custom logic here ...
    [](<https://adk.dev/callbacks/#__codelineno-3-16>)
    [](<https://adk.dev/callbacks/#__codelineno-3-17>)          // Return Optional.empty() to allow the model call to proceed,
    [](<https://adk.dev/callbacks/#__codelineno-3-18>)          // similar to returning None in the Python example.
    [](<https://adk.dev/callbacks/#__codelineno-3-19>)          // If you wanted to return a response and skip the model call,
    [](<https://adk.dev/callbacks/#__codelineno-3-20>)          // you would return Optional.of(yourLlmResponse).
    [](<https://adk.dev/callbacks/#__codelineno-3-21>)          return Optional.empty();
    [](<https://adk.dev/callbacks/#__codelineno-3-22>)        };
    [](<https://adk.dev/callbacks/#__codelineno-3-23>)
    [](<https://adk.dev/callbacks/#__codelineno-3-24>)    // --- Register it during Agent creation ---
    [](<https://adk.dev/callbacks/#__codelineno-3-25>)    LlmAgent myAgent =
    [](<https://adk.dev/callbacks/#__codelineno-3-26>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/#__codelineno-3-27>)            .name("MyCallbackAgent")
    [](<https://adk.dev/callbacks/#__codelineno-3-28>)            .model("gemini-2.0-flash") // Or your desired model
    [](<https://adk.dev/callbacks/#__codelineno-3-29>)            .instruction("Be helpful.")
    [](<https://adk.dev/callbacks/#__codelineno-3-30>)            // Other agent parameters...
    [](<https://adk.dev/callbacks/#__codelineno-3-31>)            .beforeModelCallbackSync(myBeforeModelLogic) // Pass the callback implementation here
    [](<https://adk.dev/callbacks/#__codelineno-3-32>)            .build();
    [](<https://adk.dev/callbacks/#__codelineno-3-33>)  }
    [](<https://adk.dev/callbacks/#__codelineno-3-34>)}
    
    [](<https://adk.dev/callbacks/#__codelineno-4-1>)val agent =
    [](<https://adk.dev/callbacks/#__codelineno-4-2>)    LlmAgent(
    [](<https://adk.dev/callbacks/#__codelineno-4-3>)        name = "callback_agent",
    [](<https://adk.dev/callbacks/#__codelineno-4-4>)        model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/callbacks/#__codelineno-4-5>)        beforeAgentCallbacks =
    [](<https://adk.dev/callbacks/#__codelineno-4-6>)            listOf(
    [](<https://adk.dev/callbacks/#__codelineno-4-7>)                BeforeAgentCallback { context ->
    [](<https://adk.dev/callbacks/#__codelineno-4-8>)                    println("Before Agent Callback triggered")
    [](<https://adk.dev/callbacks/#__codelineno-4-9>)                    CallbackChoice.Continue(context.eventActions)
    [](<https://adk.dev/callbacks/#__codelineno-4-10>)                },
    [](<https://adk.dev/callbacks/#__codelineno-4-11>)            ),
    [](<https://adk.dev/callbacks/#__codelineno-4-12>)        afterAgentCallbacks =
    [](<https://adk.dev/callbacks/#__codelineno-4-13>)            listOf(
    [](<https://adk.dev/callbacks/#__codelineno-4-14>)                AfterAgentCallback { context ->
    [](<https://adk.dev/callbacks/#__codelineno-4-15>)                    println("After Agent Callback triggered")
    [](<https://adk.dev/callbacks/#__codelineno-4-16>)                    CallbackChoice.Continue(Unit)
    [](<https://adk.dev/callbacks/#__codelineno-4-17>)                },
    [](<https://adk.dev/callbacks/#__codelineno-4-18>)            ),
    [](<https://adk.dev/callbacks/#__codelineno-4-19>)        beforeModelCallbacks =
    [](<https://adk.dev/callbacks/#__codelineno-4-20>)            listOf(
    [](<https://adk.dev/callbacks/#__codelineno-4-21>)                BeforeModelCallback { context, request ->
    [](<https://adk.dev/callbacks/#__codelineno-4-22>)                    println("Before Model Callback triggered")
    [](<https://adk.dev/callbacks/#__codelineno-4-23>)                    CallbackChoice.Continue(request)
    [](<https://adk.dev/callbacks/#__codelineno-4-24>)                },
    [](<https://adk.dev/callbacks/#__codelineno-4-25>)            ),
    [](<https://adk.dev/callbacks/#__codelineno-4-26>)        afterModelCallbacks =
    [](<https://adk.dev/callbacks/#__codelineno-4-27>)            listOf(
    [](<https://adk.dev/callbacks/#__codelineno-4-28>)                AfterModelCallback { context, response ->
    [](<https://adk.dev/callbacks/#__codelineno-4-29>)                    println("After Model Callback triggered")
    [](<https://adk.dev/callbacks/#__codelineno-4-30>)                    response
    [](<https://adk.dev/callbacks/#__codelineno-4-31>)                },
    [](<https://adk.dev/callbacks/#__codelineno-4-32>)            ),
    [](<https://adk.dev/callbacks/#__codelineno-4-33>)        beforeToolCallbacks =
    [](<https://adk.dev/callbacks/#__codelineno-4-34>)            listOf(
    [](<https://adk.dev/callbacks/#__codelineno-4-35>)                BeforeToolCallback { context, tool, args ->
    [](<https://adk.dev/callbacks/#__codelineno-4-36>)                    println("Before Tool Callback triggered for ${tool.name}")
    [](<https://adk.dev/callbacks/#__codelineno-4-37>)                    CallbackChoice.Continue(args)
    [](<https://adk.dev/callbacks/#__codelineno-4-38>)                },
    [](<https://adk.dev/callbacks/#__codelineno-4-39>)            ),
    [](<https://adk.dev/callbacks/#__codelineno-4-40>)        afterToolCallbacks =
    [](<https://adk.dev/callbacks/#__codelineno-4-41>)            listOf(
    [](<https://adk.dev/callbacks/#__codelineno-4-42>)                AfterToolCallback { context, tool, args, result ->
    [](<https://adk.dev/callbacks/#__codelineno-4-43>)                    println("After Tool Callback triggered for ${tool.name}")
    [](<https://adk.dev/callbacks/#__codelineno-4-44>)                    result
    [](<https://adk.dev/callbacks/#__codelineno-4-45>)                },
    [](<https://adk.dev/callbacks/#__codelineno-4-46>)            ),
    [](<https://adk.dev/callbacks/#__codelineno-4-47>)    )
    
## The Callback Mechanism: Interception and Control[¶](<https://adk.dev/callbacks/#the-callback-mechanism-interception-and-control> "Permanent link")

When the ADK framework encounters a point where a callback can run (e.g., just before calling the LLM), it checks if you provided a corresponding callback function for that agent. If you did, the framework executes your function.

**Context is Key:** Your callback function isn't called in isolation. The framework provides special **context objects** (`CallbackContext` or `ToolContext`) as arguments. These objects contain vital information about the current state of the agent's execution, including the invocation details, session state, and potentially references to services like artifacts or memory. You use these context objects to understand the situation and interact with the framework. (See the dedicated "Context Objects" section for full details).

**Controlling the Flow (The Core Mechanism):** The most powerful aspect of callbacks lies in how their **return value** influences the agent's subsequent actions. This is how you intercept and control the execution flow:

  1. **`return None` (Allow Default Behavior):**

     * The specific return type can vary depending on the language. In Java, the equivalent return type is `Optional.empty()`. In Kotlin, it is `CallbackChoice.Continue(value)` (for `before_*` callbacks) or returning the original object (for `after_*` callbacks). Refer to the API documentation for language specific guidance.
     * This is the standard way to signal that your callback has finished its work (e.g., logging, inspection, minor modifications to input arguments) and that the ADK agent should **proceed with its normal operation**.
     * For `before_*` callbacks (`before_agent`, `before_model`, `before_tool`), returning `CallbackChoice.Continue(...)` means the next step in the sequence (running the agent logic, calling the LLM, executing the tool) will occur.
     * For `after_*` callbacks (`after_agent`, `after_model`, `after_tool`), returning the result just produced (the agent's output, the LLM's response, the tool's result) as is means the framework will continue processing.
  2. **`return<Specific Object>` (Override Default Behavior):**

     * Returning a _specific type of object_ (instead of signaling "Continue") is how you **override** the ADK agent's default behavior. In Kotlin, this is achieved by returning `CallbackChoice.Break(value)` (for `before_*` callbacks) or a replacement object (for `after_*` callbacks). The framework will use the object you return and _skip_ the step that would normally follow or _replace_ the result that was just generated.
     * **`before_agent_callback` → `CallbackChoice.Break(Content)`**: Skips the agent's main execution logic. The returned `Content` object is immediately treated as the agent's final output for this turn. Useful for handling simple requests directly or enforcing access control.
     * **`before_model_callback` → `CallbackChoice.Break(LlmResponse)`**: Skips the call to the external Large Language Model. The returned `LlmResponse` object is processed as if it were the actual response from the LLM. Ideal for implementing input guardrails, prompt validation, or serving cached responses.
     * **`before_tool_callback` → `CallbackChoice.Break(Map<String, Any>)`**: Skips the execution of the actual tool function (or sub-agent). The returned `Map` is used as the result of the tool call, which is then typically passed back to the LLM. Perfect for validating tool arguments, applying policy restrictions, or returning mocked/cached tool results.
     * **`after_agent_callback` → `Content`**: _Replaces_ the `Content` that the agent's run logic just produced.
     * **`after_model_callback` → `LlmResponse`**: _Replaces_ the `LlmResponse` received from the LLM. Useful for sanitizing outputs, adding standard disclaimers, or modifying the LLM's response structure.
     * **`after_tool_callback` → `Map<String, Any>`**: _Replaces_ the `Map` result returned by the tool. Allows for post-processing or standardization of tool outputs before they are sent back to the LLM.

**Conceptual Code Example (Guardrail):**

This example demonstrates the common pattern for a guardrail using `before_model_callback`.

Code

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/callbacks/#__codelineno-5-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/#__codelineno-5-2>)#
    [](<https://adk.dev/callbacks/#__codelineno-5-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/#__codelineno-5-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/#__codelineno-5-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/#__codelineno-5-6>)#
    [](<https://adk.dev/callbacks/#__codelineno-5-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/#__codelineno-5-8>)#
    [](<https://adk.dev/callbacks/#__codelineno-5-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/#__codelineno-5-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/#__codelineno-5-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/#__codelineno-5-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/#__codelineno-5-13>)# limitations under the License.
    [](<https://adk.dev/callbacks/#__codelineno-5-14>)
    [](<https://adk.dev/callbacks/#__codelineno-5-15>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/#__codelineno-5-16>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/callbacks/#__codelineno-5-17>)from google.adk.models import LlmResponse, LlmRequest
    [](<https://adk.dev/callbacks/#__codelineno-5-18>)from google.adk.runners import Runner
    [](<https://adk.dev/callbacks/#__codelineno-5-19>)from typing import Optional
    [](<https://adk.dev/callbacks/#__codelineno-5-20>)from google.genai import types 
    [](<https://adk.dev/callbacks/#__codelineno-5-21>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/callbacks/#__codelineno-5-22>)
    [](<https://adk.dev/callbacks/#__codelineno-5-23>)GEMINI_2_FLASH="gemini-2.0-flash"
    [](<https://adk.dev/callbacks/#__codelineno-5-24>)
    [](<https://adk.dev/callbacks/#__codelineno-5-25>)# --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/#__codelineno-5-26>)def simple_before_model_modifier(
    [](<https://adk.dev/callbacks/#__codelineno-5-27>)    callback_context: CallbackContext, llm_request: LlmRequest
    [](<https://adk.dev/callbacks/#__codelineno-5-28>)) -> Optional[LlmResponse]:
    [](<https://adk.dev/callbacks/#__codelineno-5-29>)    """Inspects/modifies the LLM request or skips the call."""
    [](<https://adk.dev/callbacks/#__codelineno-5-30>)    agent_name = callback_context.agent_name
    [](<https://adk.dev/callbacks/#__codelineno-5-31>)    print(f"[Callback] Before model call for agent: {agent_name}")
    [](<https://adk.dev/callbacks/#__codelineno-5-32>)
    [](<https://adk.dev/callbacks/#__codelineno-5-33>)    # Inspect the last user message in the request contents
    [](<https://adk.dev/callbacks/#__codelineno-5-34>)    last_user_message = ""
    [](<https://adk.dev/callbacks/#__codelineno-5-35>)    if llm_request.contents and llm_request.contents[-1].role == 'user':
    [](<https://adk.dev/callbacks/#__codelineno-5-36>)         if llm_request.contents[-1].parts:
    [](<https://adk.dev/callbacks/#__codelineno-5-37>)            last_user_message = llm_request.contents[-1].parts[0].text
    [](<https://adk.dev/callbacks/#__codelineno-5-38>)    print(f"[Callback] Inspecting last user message: '{last_user_message}'")
    [](<https://adk.dev/callbacks/#__codelineno-5-39>)
    [](<https://adk.dev/callbacks/#__codelineno-5-40>)    # --- Modification Example ---
    [](<https://adk.dev/callbacks/#__codelineno-5-41>)    # Add a prefix to the system instruction
    [](<https://adk.dev/callbacks/#__codelineno-5-42>)    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
    [](<https://adk.dev/callbacks/#__codelineno-5-43>)    prefix = "[Modified by Callback] "
    [](<https://adk.dev/callbacks/#__codelineno-5-44>)    # Ensure system_instruction is Content and parts list exists
    [](<https://adk.dev/callbacks/#__codelineno-5-45>)    if not isinstance(original_instruction, types.Content):
    [](<https://adk.dev/callbacks/#__codelineno-5-46>)         # Handle case where it might be a string (though config expects Content)
    [](<https://adk.dev/callbacks/#__codelineno-5-47>)         original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    [](<https://adk.dev/callbacks/#__codelineno-5-48>)    if not original_instruction.parts:
    [](<https://adk.dev/callbacks/#__codelineno-5-49>)        original_instruction.parts.append(types.Part(text="")) # Add an empty part if none exist
    [](<https://adk.dev/callbacks/#__codelineno-5-50>)
    [](<https://adk.dev/callbacks/#__codelineno-5-51>)    # Modify the text of the first part
    [](<https://adk.dev/callbacks/#__codelineno-5-52>)    modified_text = prefix + (original_instruction.parts[0].text or "")
    [](<https://adk.dev/callbacks/#__codelineno-5-53>)    original_instruction.parts[0].text = modified_text
    [](<https://adk.dev/callbacks/#__codelineno-5-54>)    llm_request.config.system_instruction = original_instruction
    [](<https://adk.dev/callbacks/#__codelineno-5-55>)    print(f"[Callback] Modified system instruction to: '{modified_text}'")
    [](<https://adk.dev/callbacks/#__codelineno-5-56>)
    [](<https://adk.dev/callbacks/#__codelineno-5-57>)    # --- Skip Example ---
    [](<https://adk.dev/callbacks/#__codelineno-5-58>)    # Check if the last user message contains "BLOCK"
    [](<https://adk.dev/callbacks/#__codelineno-5-59>)    if "BLOCK" in last_user_message.upper():
    [](<https://adk.dev/callbacks/#__codelineno-5-60>)        print("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
    [](<https://adk.dev/callbacks/#__codelineno-5-61>)        # Return an LlmResponse to skip the actual LLM call
    [](<https://adk.dev/callbacks/#__codelineno-5-62>)        return LlmResponse(
    [](<https://adk.dev/callbacks/#__codelineno-5-63>)            content=types.Content(
    [](<https://adk.dev/callbacks/#__codelineno-5-64>)                role="model",
    [](<https://adk.dev/callbacks/#__codelineno-5-65>)                parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
    [](<https://adk.dev/callbacks/#__codelineno-5-66>)            )
    [](<https://adk.dev/callbacks/#__codelineno-5-67>)        )
    [](<https://adk.dev/callbacks/#__codelineno-5-68>)    else:
    [](<https://adk.dev/callbacks/#__codelineno-5-69>)        print("[Callback] Proceeding with LLM call.")
    [](<https://adk.dev/callbacks/#__codelineno-5-70>)        # Return None to allow the (modified) request to go to the LLM
    [](<https://adk.dev/callbacks/#__codelineno-5-71>)        return None
    [](<https://adk.dev/callbacks/#__codelineno-5-72>)
    [](<https://adk.dev/callbacks/#__codelineno-5-73>)
    [](<https://adk.dev/callbacks/#__codelineno-5-74>)# Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/#__codelineno-5-75>)my_llm_agent = LlmAgent(
    [](<https://adk.dev/callbacks/#__codelineno-5-76>)        name="ModelCallbackAgent",
    [](<https://adk.dev/callbacks/#__codelineno-5-77>)        model=GEMINI_2_FLASH,
    [](<https://adk.dev/callbacks/#__codelineno-5-78>)        instruction="You are a helpful assistant.", # Base instruction
    [](<https://adk.dev/callbacks/#__codelineno-5-79>)        description="An LLM agent demonstrating before_model_callback",
    [](<https://adk.dev/callbacks/#__codelineno-5-80>)        before_model_callback=simple_before_model_modifier # Assign the function here
    [](<https://adk.dev/callbacks/#__codelineno-5-81>))
    [](<https://adk.dev/callbacks/#__codelineno-5-82>)
    [](<https://adk.dev/callbacks/#__codelineno-5-83>)APP_NAME = "guardrail_app"
    [](<https://adk.dev/callbacks/#__codelineno-5-84>)USER_ID = "user_1"
    [](<https://adk.dev/callbacks/#__codelineno-5-85>)SESSION_ID = "session_001"
    [](<https://adk.dev/callbacks/#__codelineno-5-86>)
    [](<https://adk.dev/callbacks/#__codelineno-5-87>)# Session and Runner
    [](<https://adk.dev/callbacks/#__codelineno-5-88>)async def setup_session_and_runner():
    [](<https://adk.dev/callbacks/#__codelineno-5-89>)    session_service = InMemorySessionService()
    [](<https://adk.dev/callbacks/#__codelineno-5-90>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/callbacks/#__codelineno-5-91>)    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/callbacks/#__codelineno-5-92>)    return session, runner
    [](<https://adk.dev/callbacks/#__codelineno-5-93>)
    [](<https://adk.dev/callbacks/#__codelineno-5-94>)
    [](<https://adk.dev/callbacks/#__codelineno-5-95>)# Agent Interaction
    [](<https://adk.dev/callbacks/#__codelineno-5-96>)async def call_agent_async(query):
    [](<https://adk.dev/callbacks/#__codelineno-5-97>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/callbacks/#__codelineno-5-98>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/callbacks/#__codelineno-5-99>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/callbacks/#__codelineno-5-100>)
    [](<https://adk.dev/callbacks/#__codelineno-5-101>)    async for event in events:
    [](<https://adk.dev/callbacks/#__codelineno-5-102>)        if event.is_final_response():
    [](<https://adk.dev/callbacks/#__codelineno-5-103>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/callbacks/#__codelineno-5-104>)            print("Agent Response: ", final_response)
    [](<https://adk.dev/callbacks/#__codelineno-5-105>)
    [](<https://adk.dev/callbacks/#__codelineno-5-106>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/callbacks/#__codelineno-5-107>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/callbacks/#__codelineno-5-108>)await call_agent_async("write a joke on BLOCK")
    
    [](<https://adk.dev/callbacks/#__codelineno-6-1>)/**
    [](<https://adk.dev/callbacks/#__codelineno-6-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/#__codelineno-6-3>) *
    [](<https://adk.dev/callbacks/#__codelineno-6-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/#__codelineno-6-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/#__codelineno-6-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/#__codelineno-6-7>) *
    [](<https://adk.dev/callbacks/#__codelineno-6-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/#__codelineno-6-9>) *
    [](<https://adk.dev/callbacks/#__codelineno-6-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/#__codelineno-6-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/#__codelineno-6-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/#__codelineno-6-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/#__codelineno-6-14>) * limitations under the License.
    [](<https://adk.dev/callbacks/#__codelineno-6-15>) */
    [](<https://adk.dev/callbacks/#__codelineno-6-16>)
    [](<https://adk.dev/callbacks/#__codelineno-6-17>)import { LlmAgent, InMemoryRunner, Context, isFinalResponse } from '@google/adk';
    [](<https://adk.dev/callbacks/#__codelineno-6-18>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/#__codelineno-6-19>)
    [](<https://adk.dev/callbacks/#__codelineno-6-20>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/#__codelineno-6-21>)const APP_NAME = "before_model_callback_app";
    [](<https://adk.dev/callbacks/#__codelineno-6-22>)const USER_ID = "test_user_before_model";
    [](<https://adk.dev/callbacks/#__codelineno-6-23>)const SESSION_ID_BLOCK = "session_block_model_call";
    [](<https://adk.dev/callbacks/#__codelineno-6-24>)const SESSION_ID_NORMAL = "session_normal_model_call";
    [](<https://adk.dev/callbacks/#__codelineno-6-25>)
    [](<https://adk.dev/callbacks/#__codelineno-6-26>)// --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/#__codelineno-6-27>)function simpleBeforeModelModifier({
    [](<https://adk.dev/callbacks/#__codelineno-6-28>)  context,
    [](<https://adk.dev/callbacks/#__codelineno-6-29>)  request,
    [](<https://adk.dev/callbacks/#__codelineno-6-30>)}: {
    [](<https://adk.dev/callbacks/#__codelineno-6-31>)  context: Context;
    [](<https://adk.dev/callbacks/#__codelineno-6-32>)  request: any;
    [](<https://adk.dev/callbacks/#__codelineno-6-33>)}): any | undefined {
    [](<https://adk.dev/callbacks/#__codelineno-6-34>)  console.log(`[Callback] Before model call for agent: ${context.agentName}`);
    [](<https://adk.dev/callbacks/#__codelineno-6-35>)
    [](<https://adk.dev/callbacks/#__codelineno-6-36>)  // Inspect the last user message in the request contents
    [](<https://adk.dev/callbacks/#__codelineno-6-37>)  const lastUserMessage = request.contents?.at(-1)?.parts?.[0]?.text ?? "";
    [](<https://adk.dev/callbacks/#__codelineno-6-38>)  console.log(`[Callback] Inspecting last user message: '${lastUserMessage}'`);
    [](<https://adk.dev/callbacks/#__codelineno-6-39>)
    [](<https://adk.dev/callbacks/#__codelineno-6-40>)  // --- Modification Example ---
    [](<https://adk.dev/callbacks/#__codelineno-6-41>)  // Add a prefix to the system instruction.
    [](<https://adk.dev/callbacks/#__codelineno-6-42>)  // We create a deep copy to avoid modifying the original agent's config object.
    [](<https://adk.dev/callbacks/#__codelineno-6-43>)  const modifiedConfig = JSON.parse(JSON.stringify(request.config));
    [](<https://adk.dev/callbacks/#__codelineno-6-44>)  const originalInstructionText =
    [](<https://adk.dev/callbacks/#__codelineno-6-45>)    modifiedConfig.systemInstruction?.parts?.[0]?.text ?? "";
    [](<https://adk.dev/callbacks/#__codelineno-6-46>)  const prefix = "[Modified by Callback] ";
    [](<https://adk.dev/callbacks/#__codelineno-6-47>)  modifiedConfig.systemInstruction = {
    [](<https://adk.dev/callbacks/#__codelineno-6-48>)    role: "system",
    [](<https://adk.dev/callbacks/#__codelineno-6-49>)    parts: [{ text: prefix + originalInstructionText }],
    [](<https://adk.dev/callbacks/#__codelineno-6-50>)  };
    [](<https://adk.dev/callbacks/#__codelineno-6-51>)  request.config = modifiedConfig; // Assign the modified config back to the request
    [](<https://adk.dev/callbacks/#__codelineno-6-52>)  console.log(
    [](<https://adk.dev/callbacks/#__codelineno-6-53>)    `[Callback] Modified system instruction to: '${modifiedConfig.systemInstruction.parts[0].text}'`
    [](<https://adk.dev/callbacks/#__codelineno-6-54>)  );
    [](<https://adk.dev/callbacks/#__codelineno-6-55>)
    [](<https://adk.dev/callbacks/#__codelineno-6-56>)  // --- Skip Example ---
    [](<https://adk.dev/callbacks/#__codelineno-6-57>)  // Check if the last user message contains "BLOCK"
    [](<https://adk.dev/callbacks/#__codelineno-6-58>)  if (lastUserMessage.toUpperCase().includes("BLOCK")) {
    [](<https://adk.dev/callbacks/#__codelineno-6-59>)    console.log("[Callback] 'BLOCK' keyword found. Skipping LLM call.");
    [](<https://adk.dev/callbacks/#__codelineno-6-60>)    // Return an LlmResponse to skip the actual LLM call
    [](<https://adk.dev/callbacks/#__codelineno-6-61>)    return {
    [](<https://adk.dev/callbacks/#__codelineno-6-62>)      content: {
    [](<https://adk.dev/callbacks/#__codelineno-6-63>)        role: "model",
    [](<https://adk.dev/callbacks/#__codelineno-6-64>)        parts: [
    [](<https://adk.dev/callbacks/#__codelineno-6-65>)          { text: "LLM call was blocked by the before_model_callback." },
    [](<https://adk.dev/callbacks/#__codelineno-6-66>)        ],
    [](<https://adk.dev/callbacks/#__codelineno-6-67>)      },
    [](<https://adk.dev/callbacks/#__codelineno-6-68>)    };
    [](<https://adk.dev/callbacks/#__codelineno-6-69>)  }
    [](<https://adk.dev/callbacks/#__codelineno-6-70>)
    [](<https://adk.dev/callbacks/#__codelineno-6-71>)  console.log("[Callback] Proceeding with LLM call.");
    [](<https://adk.dev/callbacks/#__codelineno-6-72>)  // Return undefined to allow the (modified) request to go to the LLM
    [](<https://adk.dev/callbacks/#__codelineno-6-73>)  return undefined;
    [](<https://adk.dev/callbacks/#__codelineno-6-74>)}
    [](<https://adk.dev/callbacks/#__codelineno-6-75>)
    [](<https://adk.dev/callbacks/#__codelineno-6-76>)// --- Create LlmAgent and Assign Callback ---
    [](<https://adk.dev/callbacks/#__codelineno-6-77>)const myLlmAgent = new LlmAgent({
    [](<https://adk.dev/callbacks/#__codelineno-6-78>)  name: "ModelCallbackAgent",
    [](<https://adk.dev/callbacks/#__codelineno-6-79>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/#__codelineno-6-80>)  instruction: "You are a helpful assistant.", // Base instruction
    [](<https://adk.dev/callbacks/#__codelineno-6-81>)  description: "An LLM agent demonstrating before_model_callback",
    [](<https://adk.dev/callbacks/#__codelineno-6-82>)  beforeModelCallback: simpleBeforeModelModifier, // Assign the function here
    [](<https://adk.dev/callbacks/#__codelineno-6-83>)});
    [](<https://adk.dev/callbacks/#__codelineno-6-84>)
    [](<https://adk.dev/callbacks/#__codelineno-6-85>)// --- Agent Interaction Logic ---
    [](<https://adk.dev/callbacks/#__codelineno-6-86>)async function callAgentAndPrint(
    [](<https://adk.dev/callbacks/#__codelineno-6-87>)  runner: InMemoryRunner,
    [](<https://adk.dev/callbacks/#__codelineno-6-88>)  query: string,
    [](<https://adk.dev/callbacks/#__codelineno-6-89>)  sessionId: string
    [](<https://adk.dev/callbacks/#__codelineno-6-90>)) {
    [](<https://adk.dev/callbacks/#__codelineno-6-91>)  console.log(`\n>>> Calling Agent with query: "${query}"`);
    [](<https://adk.dev/callbacks/#__codelineno-6-92>)
    [](<https://adk.dev/callbacks/#__codelineno-6-93>)  let finalResponseContent = "No final response received.";
    [](<https://adk.dev/callbacks/#__codelineno-6-94>)  const events = runner.runAsync({ userId: USER_ID, sessionId, newMessage: createUserContent(query) });
    [](<https://adk.dev/callbacks/#__codelineno-6-95>)
    [](<https://adk.dev/callbacks/#__codelineno-6-96>)  for await (const event of events) {
    [](<https://adk.dev/callbacks/#__codelineno-6-97>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/#__codelineno-6-98>)      finalResponseContent = event.content.parts
    [](<https://adk.dev/callbacks/#__codelineno-6-99>)        .map((part: { text?: string }) => part.text ?? "")
    [](<https://adk.dev/callbacks/#__codelineno-6-100>)        .join("");
    [](<https://adk.dev/callbacks/#__codelineno-6-101>)    }
    [](<https://adk.dev/callbacks/#__codelineno-6-102>)  }
    [](<https://adk.dev/callbacks/#__codelineno-6-103>)  console.log("<<< Agent Response: ", finalResponseContent);
    [](<https://adk.dev/callbacks/#__codelineno-6-104>)}
    [](<https://adk.dev/callbacks/#__codelineno-6-105>)
    [](<https://adk.dev/callbacks/#__codelineno-6-106>)// --- Run Interactions ---
    [](<https://adk.dev/callbacks/#__codelineno-6-107>)async function main() {
    [](<https://adk.dev/callbacks/#__codelineno-6-108>)  const runner = new InMemoryRunner({ agent: myLlmAgent, appName: APP_NAME });
    [](<https://adk.dev/callbacks/#__codelineno-6-109>)
    [](<https://adk.dev/callbacks/#__codelineno-6-110>)  // Scenario 1: The callback will find "BLOCK" and skip the model call
    [](<https://adk.dev/callbacks/#__codelineno-6-111>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/#__codelineno-6-112>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/#__codelineno-6-113>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/#__codelineno-6-114>)    sessionId: SESSION_ID_BLOCK,
    [](<https://adk.dev/callbacks/#__codelineno-6-115>)  });
    [](<https://adk.dev/callbacks/#__codelineno-6-116>)  await callAgentAndPrint(
    [](<https://adk.dev/callbacks/#__codelineno-6-117>)    runner,
    [](<https://adk.dev/callbacks/#__codelineno-6-118>)    "write a joke about BLOCK",
    [](<https://adk.dev/callbacks/#__codelineno-6-119>)    SESSION_ID_BLOCK
    [](<https://adk.dev/callbacks/#__codelineno-6-120>)  );
    [](<https://adk.dev/callbacks/#__codelineno-6-121>)
    [](<https://adk.dev/callbacks/#__codelineno-6-122>)  // Scenario 2: The callback will modify the instruction and proceed
    [](<https://adk.dev/callbacks/#__codelineno-6-123>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/#__codelineno-6-124>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/#__codelineno-6-125>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/#__codelineno-6-126>)    sessionId: SESSION_ID_NORMAL,
    [](<https://adk.dev/callbacks/#__codelineno-6-127>)  });
    [](<https://adk.dev/callbacks/#__codelineno-6-128>)  await callAgentAndPrint(runner, "write a short poem", SESSION_ID_NORMAL);
    [](<https://adk.dev/callbacks/#__codelineno-6-129>)}
    [](<https://adk.dev/callbacks/#__codelineno-6-130>)
    [](<https://adk.dev/callbacks/#__codelineno-6-131>)main();
    
    [](<https://adk.dev/callbacks/#__codelineno-7-1>)package main
    [](<https://adk.dev/callbacks/#__codelineno-7-2>)
    [](<https://adk.dev/callbacks/#__codelineno-7-3>)import (
    [](<https://adk.dev/callbacks/#__codelineno-7-4>)    "context"
    [](<https://adk.dev/callbacks/#__codelineno-7-5>)    "fmt"
    [](<https://adk.dev/callbacks/#__codelineno-7-6>)    "log"
    [](<https://adk.dev/callbacks/#__codelineno-7-7>)    "strings"
    [](<https://adk.dev/callbacks/#__codelineno-7-8>)
    [](<https://adk.dev/callbacks/#__codelineno-7-9>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/#__codelineno-7-10>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/#__codelineno-7-11>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/#__codelineno-7-12>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/#__codelineno-7-13>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/#__codelineno-7-14>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/#__codelineno-7-15>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/#__codelineno-7-16>))
    [](<https://adk.dev/callbacks/#__codelineno-7-17>)
    [](<https://adk.dev/callbacks/#__codelineno-7-18>)
    [](<https://adk.dev/callbacks/#__codelineno-7-19>)
    [](<https://adk.dev/callbacks/#__codelineno-7-20>)// onBeforeModelGuardrail is a callback that inspects the LLM request.
    [](<https://adk.dev/callbacks/#__codelineno-7-21>)// If it contains a forbidden topic, it blocks the request and returns a
    [](<https://adk.dev/callbacks/#__codelineno-7-22>)// predefined response. Otherwise, it allows the request to proceed.
    [](<https://adk.dev/callbacks/#__codelineno-7-23>)func onBeforeModelGuardrail(ctx agent.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
    [](<https://adk.dev/callbacks/#__codelineno-7-24>)    log.Println("--- onBeforeModelGuardrail Callback Triggered ---")
    [](<https://adk.dev/callbacks/#__codelineno-7-25>)
    [](<https://adk.dev/callbacks/#__codelineno-7-26>)    // Inspect the request content for forbidden topics.
    [](<https://adk.dev/callbacks/#__codelineno-7-27>)    for _, content := range req.Contents {
    [](<https://adk.dev/callbacks/#__codelineno-7-28>)        for _, part := range content.Parts {
    [](<https://adk.dev/callbacks/#__codelineno-7-29>)            if strings.Contains(part.Text, "finance") {
    [](<https://adk.dev/callbacks/#__codelineno-7-30>)                log.Println("Forbidden topic 'finance' detected. Blocking LLM call.")
    [](<https://adk.dev/callbacks/#__codelineno-7-31>)                // By returning a non-nil response, we override the default behavior
    [](<https://adk.dev/callbacks/#__codelineno-7-32>)                // and prevent the actual LLM call.
    [](<https://adk.dev/callbacks/#__codelineno-7-33>)                return &model.LLMResponse{
    [](<https://adk.dev/callbacks/#__codelineno-7-34>)                    Content: &genai.Content{
    [](<https://adk.dev/callbacks/#__codelineno-7-35>)                        Parts: []*genai.Part{{Text: "I'm sorry, but I cannot discuss financial topics."}},
    [](<https://adk.dev/callbacks/#__codelineno-7-36>)                        Role:  "model",
    [](<https://adk.dev/callbacks/#__codelineno-7-37>)                    },
    [](<https://adk.dev/callbacks/#__codelineno-7-38>)                }, nil
    [](<https://adk.dev/callbacks/#__codelineno-7-39>)            }
    [](<https://adk.dev/callbacks/#__codelineno-7-40>)        }
    [](<https://adk.dev/callbacks/#__codelineno-7-41>)    }
    [](<https://adk.dev/callbacks/#__codelineno-7-42>)
    [](<https://adk.dev/callbacks/#__codelineno-7-43>)    log.Println("No forbidden topics found. Allowing LLM call to proceed.")
    [](<https://adk.dev/callbacks/#__codelineno-7-44>)    // Returning nil allows the default LLM call to proceed.
    [](<https://adk.dev/callbacks/#__codelineno-7-45>)    return nil, nil
    [](<https://adk.dev/callbacks/#__codelineno-7-46>)}
    [](<https://adk.dev/callbacks/#__codelineno-7-47>)
    [](<https://adk.dev/callbacks/#__codelineno-7-48>)func runGuardrailExample() {
    [](<https://adk.dev/callbacks/#__codelineno-7-49>)    const (
    [](<https://adk.dev/callbacks/#__codelineno-7-50>)        appName = "GuardrailApp"
    [](<https://adk.dev/callbacks/#__codelineno-7-51>)        userID  = "test_user_456"
    [](<https://adk.dev/callbacks/#__codelineno-7-52>)    )
    [](<https://adk.dev/callbacks/#__codelineno-7-53>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/#__codelineno-7-54>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/#__codelineno-7-55>)    if err != nil {
    [](<https://adk.dev/callbacks/#__codelineno-7-56>)        log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/#__codelineno-7-57>)    }
    [](<https://adk.dev/callbacks/#__codelineno-7-58>)
    [](<https://adk.dev/callbacks/#__codelineno-7-59>)    agentCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/#__codelineno-7-60>)        Name:                 "ChatAgent",
    [](<https://adk.dev/callbacks/#__codelineno-7-61>)        Model:                geminiModel,
    [](<https://adk.dev/callbacks/#__codelineno-7-62>)        BeforeModelCallbacks: []llmagent.BeforeModelCallback{onBeforeModelGuardrail},
    [](<https://adk.dev/callbacks/#__codelineno-7-63>)    }
    [](<https://adk.dev/callbacks/#__codelineno-7-64>)    chatAgent, err := llmagent.New(agentCfg)
    [](<https://adk.dev/callbacks/#__codelineno-7-65>)    if err != nil {
    [](<https://adk.dev/callbacks/#__codelineno-7-66>)        log.Fatalf("Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/#__codelineno-7-67>)    }
    [](<https://adk.dev/callbacks/#__codelineno-7-68>)
    [](<https://adk.dev/callbacks/#__codelineno-7-69>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/#__codelineno-7-70>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/callbacks/#__codelineno-7-71>)        AppName:        appName,
    [](<https://adk.dev/callbacks/#__codelineno-7-72>)        Agent:          chatAgent,
    [](<https://adk.dev/callbacks/#__codelineno-7-73>)        SessionService: sessionService,
    [](<https://adk.dev/callbacks/#__codelineno-7-74>)    })
    [](<https://adk.dev/callbacks/#__codelineno-7-75>)    if err != nil {
    [](<https://adk.dev/callbacks/#__codelineno-7-76>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/#__codelineno-7-77>)    }
    
    [](<https://adk.dev/callbacks/#__codelineno-8-1>)import com.google.adk.agents.CallbackContext;
    [](<https://adk.dev/callbacks/#__codelineno-8-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/#__codelineno-8-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/callbacks/#__codelineno-8-4>)import com.google.adk.models.LlmRequest;
    [](<https://adk.dev/callbacks/#__codelineno-8-5>)import com.google.adk.models.LlmResponse;
    [](<https://adk.dev/callbacks/#__codelineno-8-6>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/callbacks/#__codelineno-8-7>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/callbacks/#__codelineno-8-8>)import com.google.genai.types.Content;
    [](<https://adk.dev/callbacks/#__codelineno-8-9>)import com.google.genai.types.GenerateContentConfig;
    [](<https://adk.dev/callbacks/#__codelineno-8-10>)import com.google.genai.types.Part;
    [](<https://adk.dev/callbacks/#__codelineno-8-11>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/callbacks/#__codelineno-8-12>)import java.util.ArrayList;
    [](<https://adk.dev/callbacks/#__codelineno-8-13>)import java.util.List;
    [](<https://adk.dev/callbacks/#__codelineno-8-14>)import java.util.Optional;
    [](<https://adk.dev/callbacks/#__codelineno-8-15>)import java.util.stream.Collectors;
    [](<https://adk.dev/callbacks/#__codelineno-8-16>)
    [](<https://adk.dev/callbacks/#__codelineno-8-17>)public class BeforeModelGuardrailExample {
    [](<https://adk.dev/callbacks/#__codelineno-8-18>)
    [](<https://adk.dev/callbacks/#__codelineno-8-19>)  private static final String MODEL_ID = "gemini-2.0-flash";
    [](<https://adk.dev/callbacks/#__codelineno-8-20>)  private static final String APP_NAME = "guardrail_app";
    [](<https://adk.dev/callbacks/#__codelineno-8-21>)  private static final String USER_ID = "user_1";
    [](<https://adk.dev/callbacks/#__codelineno-8-22>)
    [](<https://adk.dev/callbacks/#__codelineno-8-23>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/#__codelineno-8-24>)    BeforeModelGuardrailExample example = new BeforeModelGuardrailExample();
    [](<https://adk.dev/callbacks/#__codelineno-8-25>)    example.defineAgentAndRun("Tell me about quantum computing. This is a test.");
    [](<https://adk.dev/callbacks/#__codelineno-8-26>)  }
    [](<https://adk.dev/callbacks/#__codelineno-8-27>)
    [](<https://adk.dev/callbacks/#__codelineno-8-28>)  // --- Define your callback logic ---
    [](<https://adk.dev/callbacks/#__codelineno-8-29>)  // Looks for the word "BLOCK" in the user prompt and blocks the call to LLM if found.
    [](<https://adk.dev/callbacks/#__codelineno-8-30>)  // Otherwise the LLM call proceeds as usual.
    [](<https://adk.dev/callbacks/#__codelineno-8-31>)  public Optional<LlmResponse> simpleBeforeModelModifier(
    [](<https://adk.dev/callbacks/#__codelineno-8-32>)      CallbackContext callbackContext, LlmRequest llmRequest) {
    [](<https://adk.dev/callbacks/#__codelineno-8-33>)    System.out.println("[Callback] Before model call for agent: " + callbackContext.agentName());
    [](<https://adk.dev/callbacks/#__codelineno-8-34>)
    [](<https://adk.dev/callbacks/#__codelineno-8-35>)    // Inspect the last user message in the request contents
    [](<https://adk.dev/callbacks/#__codelineno-8-36>)    String lastUserMessageText = "";
    [](<https://adk.dev/callbacks/#__codelineno-8-37>)    List<Content> requestContents = llmRequest.contents();
    [](<https://adk.dev/callbacks/#__codelineno-8-38>)    if (requestContents != null && !requestContents.isEmpty()) {
    [](<https://adk.dev/callbacks/#__codelineno-8-39>)      Content lastContent = requestContents.get(requestContents.size() - 1);
    [](<https://adk.dev/callbacks/#__codelineno-8-40>)      if (lastContent.role().isPresent() && "user".equals(lastContent.role().get())) {
    [](<https://adk.dev/callbacks/#__codelineno-8-41>)        lastUserMessageText =
    [](<https://adk.dev/callbacks/#__codelineno-8-42>)            lastContent.parts().orElse(List.of()).stream()
    [](<https://adk.dev/callbacks/#__codelineno-8-43>)                .flatMap(part -> part.text().stream())
    [](<https://adk.dev/callbacks/#__codelineno-8-44>)                .collect(Collectors.joining(" ")); // Concatenate text from all parts
    [](<https://adk.dev/callbacks/#__codelineno-8-45>)      }
    [](<https://adk.dev/callbacks/#__codelineno-8-46>)    }
    [](<https://adk.dev/callbacks/#__codelineno-8-47>)    System.out.println("[Callback] Inspecting last user message: '" + lastUserMessageText + "'");
    [](<https://adk.dev/callbacks/#__codelineno-8-48>)
    [](<https://adk.dev/callbacks/#__codelineno-8-49>)    String prefix = "[Modified by Callback] ";
    [](<https://adk.dev/callbacks/#__codelineno-8-50>)    GenerateContentConfig currentConfig =
    [](<https://adk.dev/callbacks/#__codelineno-8-51>)        llmRequest.config().orElse(GenerateContentConfig.builder().build());
    [](<https://adk.dev/callbacks/#__codelineno-8-52>)    Optional<Content> optOriginalSystemInstruction = currentConfig.systemInstruction();
    [](<https://adk.dev/callbacks/#__codelineno-8-53>)
    [](<https://adk.dev/callbacks/#__codelineno-8-54>)    Content conceptualModifiedSystemInstruction;
    [](<https://adk.dev/callbacks/#__codelineno-8-55>)    if (optOriginalSystemInstruction.isPresent()) {
    [](<https://adk.dev/callbacks/#__codelineno-8-56>)      Content originalSystemInstruction = optOriginalSystemInstruction.get();
    [](<https://adk.dev/callbacks/#__codelineno-8-57>)      List<Part> originalParts =
    [](<https://adk.dev/callbacks/#__codelineno-8-58>)          new ArrayList<>(originalSystemInstruction.parts().orElse(List.of()));
    [](<https://adk.dev/callbacks/#__codelineno-8-59>)      String originalText = "";
    [](<https://adk.dev/callbacks/#__codelineno-8-60>)
    [](<https://adk.dev/callbacks/#__codelineno-8-61>)      if (!originalParts.isEmpty()) {
    [](<https://adk.dev/callbacks/#__codelineno-8-62>)        Part firstPart = originalParts.get(0);
    [](<https://adk.dev/callbacks/#__codelineno-8-63>)        if (firstPart.text().isPresent()) {
    [](<https://adk.dev/callbacks/#__codelineno-8-64>)          originalText = firstPart.text().get();
    [](<https://adk.dev/callbacks/#__codelineno-8-65>)        }
    [](<https://adk.dev/callbacks/#__codelineno-8-66>)        originalParts.set(0, Part.fromText(prefix + originalText));
    [](<https://adk.dev/callbacks/#__codelineno-8-67>)      } else {
    [](<https://adk.dev/callbacks/#__codelineno-8-68>)        originalParts.add(Part.fromText(prefix));
    [](<https://adk.dev/callbacks/#__codelineno-8-69>)      }
    [](<https://adk.dev/callbacks/#__codelineno-8-70>)      conceptualModifiedSystemInstruction =
    [](<https://adk.dev/callbacks/#__codelineno-8-71>)          originalSystemInstruction.toBuilder().parts(originalParts).build();
    [](<https://adk.dev/callbacks/#__codelineno-8-72>)    } else {
    [](<https://adk.dev/callbacks/#__codelineno-8-73>)      conceptualModifiedSystemInstruction =
    [](<https://adk.dev/callbacks/#__codelineno-8-74>)          Content.builder()
    [](<https://adk.dev/callbacks/#__codelineno-8-75>)              .role("system")
    [](<https://adk.dev/callbacks/#__codelineno-8-76>)              .parts(List.of(Part.fromText(prefix)))
    [](<https://adk.dev/callbacks/#__codelineno-8-77>)              .build();
    [](<https://adk.dev/callbacks/#__codelineno-8-78>)    }
    [](<https://adk.dev/callbacks/#__codelineno-8-79>)
    [](<https://adk.dev/callbacks/#__codelineno-8-80>)    // This demonstrates building a new LlmRequest with the modified config.
    [](<https://adk.dev/callbacks/#__codelineno-8-81>)    llmRequest =
    [](<https://adk.dev/callbacks/#__codelineno-8-82>)        llmRequest.toBuilder()
    [](<https://adk.dev/callbacks/#__codelineno-8-83>)            .config(
    [](<https://adk.dev/callbacks/#__codelineno-8-84>)                currentConfig.toBuilder()
    [](<https://adk.dev/callbacks/#__codelineno-8-85>)                    .systemInstruction(conceptualModifiedSystemInstruction)
    [](<https://adk.dev/callbacks/#__codelineno-8-86>)                    .build())
    [](<https://adk.dev/callbacks/#__codelineno-8-87>)            .build();
    [](<https://adk.dev/callbacks/#__codelineno-8-88>)
    [](<https://adk.dev/callbacks/#__codelineno-8-89>)    System.out.println(
    [](<https://adk.dev/callbacks/#__codelineno-8-90>)        "[Callback] Conceptually modified system instruction is: '"
    [](<https://adk.dev/callbacks/#__codelineno-8-91>)            + llmRequest.config().get().systemInstruction().get().parts().get().get(0).text().get());
    [](<https://adk.dev/callbacks/#__codelineno-8-92>)
    [](<https://adk.dev/callbacks/#__codelineno-8-93>)    // --- Skip Example ---
    [](<https://adk.dev/callbacks/#__codelineno-8-94>)    // Check if the last user message contains "BLOCK"
    [](<https://adk.dev/callbacks/#__codelineno-8-95>)    if (lastUserMessageText.toUpperCase().contains("BLOCK")) {
    [](<https://adk.dev/callbacks/#__codelineno-8-96>)      System.out.println("[Callback] 'BLOCK' keyword found. Skipping LLM call.");
    [](<https://adk.dev/callbacks/#__codelineno-8-97>)      LlmResponse skipResponse =
    [](<https://adk.dev/callbacks/#__codelineno-8-98>)          LlmResponse.builder()
    [](<https://adk.dev/callbacks/#__codelineno-8-99>)              .content(
    [](<https://adk.dev/callbacks/#__codelineno-8-100>)                  Content.builder()
    [](<https://adk.dev/callbacks/#__codelineno-8-101>)                      .role("model")
    [](<https://adk.dev/callbacks/#__codelineno-8-102>)                      .parts(
    [](<https://adk.dev/callbacks/#__codelineno-8-103>)                          List.of(
    [](<https://adk.dev/callbacks/#__codelineno-8-104>)                              Part.builder()
    [](<https://adk.dev/callbacks/#__codelineno-8-105>)                                  .text("LLM call was blocked by before_model_callback.")
    [](<https://adk.dev/callbacks/#__codelineno-8-106>)                                  .build()))
    [](<https://adk.dev/callbacks/#__codelineno-8-107>)                      .build())
    [](<https://adk.dev/callbacks/#__codelineno-8-108>)              .build();
    [](<https://adk.dev/callbacks/#__codelineno-8-109>)      return Optional.of(skipResponse);
    [](<https://adk.dev/callbacks/#__codelineno-8-110>)    }
    [](<https://adk.dev/callbacks/#__codelineno-8-111>)    System.out.println("[Callback] Proceeding with LLM call.");
    [](<https://adk.dev/callbacks/#__codelineno-8-112>)    // Return Optional.empty() to allow the (modified) request to go to the LLM
    [](<https://adk.dev/callbacks/#__codelineno-8-113>)    return Optional.empty();
    [](<https://adk.dev/callbacks/#__codelineno-8-114>)  }
    [](<https://adk.dev/callbacks/#__codelineno-8-115>)
    [](<https://adk.dev/callbacks/#__codelineno-8-116>)  public void defineAgentAndRun(String prompt) {
    [](<https://adk.dev/callbacks/#__codelineno-8-117>)    // --- Create LlmAgent and Assign Callback ---
    [](<https://adk.dev/callbacks/#__codelineno-8-118>)    LlmAgent myLlmAgent =
    [](<https://adk.dev/callbacks/#__codelineno-8-119>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/#__codelineno-8-120>)            .name("ModelCallbackAgent")
    [](<https://adk.dev/callbacks/#__codelineno-8-121>)            .model(MODEL_ID)
    [](<https://adk.dev/callbacks/#__codelineno-8-122>)            .instruction("You are a helpful assistant.") // Base instruction
    [](<https://adk.dev/callbacks/#__codelineno-8-123>)            .description("An LLM agent demonstrating before_model_callback")
    [](<https://adk.dev/callbacks/#__codelineno-8-124>)            .beforeModelCallbackSync(this::simpleBeforeModelModifier) // Assign the callback here
    [](<https://adk.dev/callbacks/#__codelineno-8-125>)            .build();
    [](<https://adk.dev/callbacks/#__codelineno-8-126>)
    [](<https://adk.dev/callbacks/#__codelineno-8-127>)    // Session and Runner
    [](<https://adk.dev/callbacks/#__codelineno-8-128>)    InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME);
    [](<https://adk.dev/callbacks/#__codelineno-8-129>)    // InMemoryRunner automatically creates a session service. Create a session using the service
    [](<https://adk.dev/callbacks/#__codelineno-8-130>)    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    [](<https://adk.dev/callbacks/#__codelineno-8-131>)    Content userMessage =
    [](<https://adk.dev/callbacks/#__codelineno-8-132>)        Content.fromParts(Part.fromText(prompt));
    [](<https://adk.dev/callbacks/#__codelineno-8-133>)
    [](<https://adk.dev/callbacks/#__codelineno-8-134>)    // Run the agent
    [](<https://adk.dev/callbacks/#__codelineno-8-135>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/callbacks/#__codelineno-8-136>)
    [](<https://adk.dev/callbacks/#__codelineno-8-137>)    // Stream event response
    [](<https://adk.dev/callbacks/#__codelineno-8-138>)    eventStream.blockingForEach(
    [](<https://adk.dev/callbacks/#__codelineno-8-139>)        event -> {
    [](<https://adk.dev/callbacks/#__codelineno-8-140>)          if (event.finalResponse()) {
    [](<https://adk.dev/callbacks/#__codelineno-8-141>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/callbacks/#__codelineno-8-142>)          }
    [](<https://adk.dev/callbacks/#__codelineno-8-143>)        });
    [](<https://adk.dev/callbacks/#__codelineno-8-144>)  }
    [](<https://adk.dev/callbacks/#__codelineno-8-145>)}
    
    [](<https://adk.dev/callbacks/#__codelineno-9-1>)val guardrailCallback =
    [](<https://adk.dev/callbacks/#__codelineno-9-2>)    BeforeModelCallback { context, request ->
    [](<https://adk.dev/callbacks/#__codelineno-9-3>)        val userQuery = request.contents.lastOrNull()?.parts?.firstOrNull()?.text ?: ""
    [](<https://adk.dev/callbacks/#__codelineno-9-4>)
    [](<https://adk.dev/callbacks/#__codelineno-9-5>)        if (userQuery.contains("sensitive info", ignoreCase = true)) {
    [](<https://adk.dev/callbacks/#__codelineno-9-6>)            println("Guardrail triggered: Sensitive information requested.")
    [](<https://adk.dev/callbacks/#__codelineno-9-7>)            CallbackChoice.Break(
    [](<https://adk.dev/callbacks/#__codelineno-9-8>)                LlmResponse(
    [](<https://adk.dev/callbacks/#__codelineno-9-9>)                    content =
    [](<https://adk.dev/callbacks/#__codelineno-9-10>)                        Content(
    [](<https://adk.dev/callbacks/#__codelineno-9-11>)                            role = Role.MODEL,
    [](<https://adk.dev/callbacks/#__codelineno-9-12>)                            parts =
    [](<https://adk.dev/callbacks/#__codelineno-9-13>)                                listOf(
    [](<https://adk.dev/callbacks/#__codelineno-9-14>)                                    Part(
    [](<https://adk.dev/callbacks/#__codelineno-9-15>)                                        text = "I'm sorry, I cannot provide sensitive information.",
    [](<https://adk.dev/callbacks/#__codelineno-9-16>)                                    ),
    [](<https://adk.dev/callbacks/#__codelineno-9-17>)                                ),
    [](<https://adk.dev/callbacks/#__codelineno-9-18>)                        ),
    [](<https://adk.dev/callbacks/#__codelineno-9-19>)                ),
    [](<https://adk.dev/callbacks/#__codelineno-9-20>)            )
    [](<https://adk.dev/callbacks/#__codelineno-9-21>)        } else {
    [](<https://adk.dev/callbacks/#__codelineno-9-22>)            CallbackChoice.Continue(request)
    [](<https://adk.dev/callbacks/#__codelineno-9-23>)        }
    [](<https://adk.dev/callbacks/#__codelineno-9-24>)    }
    
By understanding this mechanism of returning `None` versus returning specific objects, you can precisely control the agent's execution path, making callbacks an essential tool for building sophisticated and reliable agents with ADK.

Back to top 