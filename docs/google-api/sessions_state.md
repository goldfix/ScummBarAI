# State - Agent Development Kit (ADK)

> Source: [https://adk.dev/sessions/state/](https://adk.dev/sessions/state/)

[ Skip to content ](<https://adk.dev/sessions/state/#state-the-sessions-scratchpad>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/sessions/state.md> "Edit this page on GitHub") [ ](<https://adk.dev/sessions/state/index.md> "View this page as Markdown")

# State: The Session's Scratchpad[¶](<https://adk.dev/sessions/state/#state-the-sessions-scratchpad> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

Within each `Session` (our conversation thread), the **`state`** attribute acts like the agent's dedicated scratchpad for that specific interaction. While `session.events` holds the full history, `session.state` is where the agent stores and updates dynamic details needed _during_ the conversation.

## What is `session.state`?[¶](<https://adk.dev/sessions/state/#what-is-sessionstate> "Permanent link")

Conceptually, `session.state` is a collection (dictionary or Map) holding key-value pairs. It's designed for information the agent needs to recall or track to make the current conversation effective:

  * **Personalize Interaction:** Remember user preferences mentioned earlier (e.g., `'user_preference_theme': 'dark'`).
  * **Track Task Progress:** Keep tabs on steps in a multi-turn process (e.g., `'booking_step': 'confirm_payment'`).
  * **Accumulate Information:** Build lists or summaries (e.g., `'shopping_cart_items': ['book', 'pen']`).
  * **Make Informed Decisions:** Store flags or values influencing the next response (e.g., `'user_is_authenticated': True`).

### Key Characteristics of `State`[¶](<https://adk.dev/sessions/state/#key-characteristics-of-state> "Permanent link")

  1. **Structure: Serializable Key-Value Pairs**

     * Data is stored as `key: value`.
     * **Keys:** Always strings (`str`). Use clear names (e.g., `'departure_city'`, `'user:language_preference'`).
     * **Values:** Must be **serializable**. This means they can be easily saved and loaded by the `SessionService`. Stick to basic types in the specific languages (Python/Go/Java/TypeScript) like strings, numbers, booleans, and simple lists or dictionaries containing _only_ these basic types. (See API documentation for precise details).
     * **⚠️ Avoid Complex Objects:** **Do not store non-serializable objects** (custom class instances, functions, connections, etc.) directly in the state. Store simple identifiers if needed, and retrieve the complex object elsewhere.
  2. **Mutability: It Changes**

     * The contents of the `state` are expected to change as the conversation evolves.
  3. **Persistence: Depends on`SessionService`**

     * Whether state survives application restarts depends on your chosen service:

     * `InMemorySessionService`: **Not Persistent.** State is lost on restart.

     * `DatabaseSessionService` / `VertexAiSessionService`: **Persistent.** State is saved reliably.

Note

The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `session.state['current_intent'] = 'book_flight'` in Python,`context.State().Set("current_intent", "book_flight")` in Go, `session.state().put("current_intent", "book_flight)` in Java, or `context.state.set("current_intent", "book_flight")` in TypeScript). Refer to the language-specific API documentation for details.

### Organizing State with Prefixes: Scope Matters[¶](<https://adk.dev/sessions/state/#organizing-state-with-prefixes-scope-matters> "Permanent link")

Prefixes on state keys define their scope and persistence behavior, especially with persistent services:

  * **No Prefix (Session State):**

    * **Scope:** Specific to the _current_ session (`id`).
    * **Persistence:** Only persists if the `SessionService` is persistent (`Database`, `VertexAI`).
    * **Use Cases:** Tracking progress within the current task (e.g., `'current_booking_step'`), temporary flags for this interaction (e.g., `'needs_clarification'`).
    * **Example:** `session.state['current_intent'] = 'book_flight'`
  * **`user:` Prefix (User State):**

    * **Scope:** Tied to the `user_id`, shared across _all_ sessions for that user (within the same `app_name`).
    * **Persistence:** Persistent with `Database` or `VertexAI`. (Stored by `InMemory` but lost on restart).
    * **Use Cases:** User preferences (e.g., `'user:theme'`), profile details (e.g., `'user:name'`).
    * **Example:** `session.state['user:preferred_language'] = 'fr'`
  * **`app:` Prefix (App State):**

    * **Scope:** Tied to the `app_name`, shared across _all_ users and sessions for that application.
    * **Persistence:** Persistent with `Database` or `VertexAI`. (Stored by `InMemory` but lost on restart).
    * **Use Cases:** Global settings (e.g., `'app:api_endpoint'`), shared templates.
    * **Example:** `session.state['app:global_discount_code'] = 'SAVE10'`
  * **`temp:` Prefix (Temporary Invocation State):**

    * **Scope:** Specific to the current **invocation** (the entire process from an agent receiving user input to generating the final output for that input).
    * **Persistence:** **Not Persistent.** Discarded after the invocation completes and does not carry over to the next one.
    * **Use Cases:** Storing intermediate calculations, flags, or data passed between tool calls within a single invocation.
    * **When Not to Use:** For information that must persist across different invocations, such as user preferences, conversation history summaries, or accumulated data.
    * **Example:** `session.state['temp:raw_api_response'] = {...}`

Sub-Agents and Invocation Context

When a parent agent calls a sub-agent (e.g., using `SequentialAgent` or `ParallelAgent`), it passes its `InvocationContext` to the sub-agent. This means the entire chain of agent calls shares the same invocation ID and, therefore, the same `temp:` state.

**How the Agent Sees It:** Your agent code interacts with the _combined_ state through the single `session.state` collection (dict/ Map). The `SessionService` handles fetching/merging state from the correct underlying storage based on prefixes.

### Accessing Session State in Agent Instructions[¶](<https://adk.dev/sessions/state/#accessing-session-state-in-agent-instructions> "Permanent link")

When working with `LlmAgent` instances, you can directly inject session state values into the agent's instruction string using a simple templating syntax. This allows you to create dynamic and context-aware instructions without relying solely on natural language directives.

#### Using `{key}` Templating[¶](<https://adk.dev/sessions/state/#using-key-templating> "Permanent link")

To inject a value from the session state, enclose the key of the desired state variable within curly braces: `{key}`. The framework will automatically replace this placeholder with the corresponding value from `session.state` before passing the instruction to the LLM.

**Example:**

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/state/#__codelineno-0-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/sessions/state/#__codelineno-0-2>)
    [](<https://adk.dev/sessions/state/#__codelineno-0-3>)story_generator = LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-0-4>)    name="StoryGenerator",
    [](<https://adk.dev/sessions/state/#__codelineno-0-5>)    model="gemini-flash-latest",
    [](<https://adk.dev/sessions/state/#__codelineno-0-6>)    instruction="""Write a short story about a cat, focusing on the theme: {topic}."""
    [](<https://adk.dev/sessions/state/#__codelineno-0-7>))
    [](<https://adk.dev/sessions/state/#__codelineno-0-8>)
    [](<https://adk.dev/sessions/state/#__codelineno-0-9>)# Assuming session.state['topic'] is set to "friendship", the LLM
    [](<https://adk.dev/sessions/state/#__codelineno-0-10>)# will receive the following instruction:
    [](<https://adk.dev/sessions/state/#__codelineno-0-11>)# "Write a short story about a cat, focusing on the theme: friendship."
    
    [](<https://adk.dev/sessions/state/#__codelineno-1-1>)import { LlmAgent } from "@google/adk";
    [](<https://adk.dev/sessions/state/#__codelineno-1-2>)
    [](<https://adk.dev/sessions/state/#__codelineno-1-3>)const storyGenerator = new LlmAgent({
    [](<https://adk.dev/sessions/state/#__codelineno-1-4>)    name: "StoryGenerator",
    [](<https://adk.dev/sessions/state/#__codelineno-1-5>)    model: "gemini-flash-latest",
    [](<https://adk.dev/sessions/state/#__codelineno-1-6>)    instruction: "Write a short story about a cat, focusing on the theme: {topic}."
    [](<https://adk.dev/sessions/state/#__codelineno-1-7>)});
    [](<https://adk.dev/sessions/state/#__codelineno-1-8>)
    [](<https://adk.dev/sessions/state/#__codelineno-1-9>)// Assuming session.state['topic'] is set to "friendship", the LLM
    [](<https://adk.dev/sessions/state/#__codelineno-1-10>)// will receive the following instruction:
    [](<https://adk.dev/sessions/state/#__codelineno-1-11>)// "Write a short story about a cat, focusing on the theme: friendship."
    
    [](<https://adk.dev/sessions/state/#__codelineno-2-1>)func main() {
    [](<https://adk.dev/sessions/state/#__codelineno-2-2>)    ctx := context.Background()
    [](<https://adk.dev/sessions/state/#__codelineno-2-3>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/sessions/state/#__codelineno-2-4>)
    [](<https://adk.dev/sessions/state/#__codelineno-2-5>)    // 1. Initialize a session with a 'topic' in its state.
    [](<https://adk.dev/sessions/state/#__codelineno-2-6>)    _, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/sessions/state/#__codelineno-2-7>)        AppName:   appName,
    [](<https://adk.dev/sessions/state/#__codelineno-2-8>)        UserID:    userID,
    [](<https://adk.dev/sessions/state/#__codelineno-2-9>)        SessionID: sessionID,
    [](<https://adk.dev/sessions/state/#__codelineno-2-10>)        State: map[string]any{
    [](<https://adk.dev/sessions/state/#__codelineno-2-11>)            "topic": "friendship",
    [](<https://adk.dev/sessions/state/#__codelineno-2-12>)        },
    [](<https://adk.dev/sessions/state/#__codelineno-2-13>)    })
    [](<https://adk.dev/sessions/state/#__codelineno-2-14>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-2-15>)        log.Fatalf("Failed to create session: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-2-16>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-2-17>)
    [](<https://adk.dev/sessions/state/#__codelineno-2-18>)    // 2. Create an agent with an instruction that uses a {topic} placeholder.
    [](<https://adk.dev/sessions/state/#__codelineno-2-19>)    //    The ADK will automatically inject the value of "topic" from the
    [](<https://adk.dev/sessions/state/#__codelineno-2-20>)    //    session state into the instruction before calling the LLM.
    [](<https://adk.dev/sessions/state/#__codelineno-2-21>)    model, err := gemini.NewModel(ctx, modelID, nil)
    [](<https://adk.dev/sessions/state/#__codelineno-2-22>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-2-23>)        log.Fatalf("Failed to create Gemini model: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-2-24>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-2-25>)    storyGenerator, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/sessions/state/#__codelineno-2-26>)        Name:        "StoryGenerator",
    [](<https://adk.dev/sessions/state/#__codelineno-2-27>)        Model:       model,
    [](<https://adk.dev/sessions/state/#__codelineno-2-28>)        Instruction: "Write a short story about a cat, focusing on the theme: {topic}.",
    [](<https://adk.dev/sessions/state/#__codelineno-2-29>)    })
    [](<https://adk.dev/sessions/state/#__codelineno-2-30>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-2-31>)        log.Fatalf("Failed to create agent: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-2-32>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-2-33>)
    [](<https://adk.dev/sessions/state/#__codelineno-2-34>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/sessions/state/#__codelineno-2-35>)        AppName:        appName,
    [](<https://adk.dev/sessions/state/#__codelineno-2-36>)        Agent:          agent.Agent(storyGenerator),
    [](<https://adk.dev/sessions/state/#__codelineno-2-37>)        SessionService: sessionService,
    [](<https://adk.dev/sessions/state/#__codelineno-2-38>)    })
    [](<https://adk.dev/sessions/state/#__codelineno-2-39>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-2-40>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-2-41>)    }
    
    [](<https://adk.dev/sessions/state/#__codelineno-3-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/sessions/state/#__codelineno-3-2>)
    [](<https://adk.dev/sessions/state/#__codelineno-3-3>)LlmAgent storyGenerator = LlmAgent.builder()
    [](<https://adk.dev/sessions/state/#__codelineno-3-4>)    .name("StoryGenerator")
    [](<https://adk.dev/sessions/state/#__codelineno-3-5>)    .model(geminiModel)
    [](<https://adk.dev/sessions/state/#__codelineno-3-6>)    .instruction("Write a short story about a cat, focusing on the theme: " + topic)
    [](<https://adk.dev/sessions/state/#__codelineno-3-7>)    .build();
    [](<https://adk.dev/sessions/state/#__codelineno-3-8>)
    [](<https://adk.dev/sessions/state/#__codelineno-3-9>)// Assuming session.state().put("topic", "friendship"), the LLM
    [](<https://adk.dev/sessions/state/#__codelineno-3-10>)// will receive the following instruction:
    [](<https://adk.dev/sessions/state/#__codelineno-3-11>)// "Write a short story about a cat, focusing on the theme: friendship."
    
    [](<https://adk.dev/sessions/state/#__codelineno-4-1>)fun instructionTemplating(model: Gemini) {
    [](<https://adk.dev/sessions/state/#__codelineno-4-2>)    val storyGenerator =
    [](<https://adk.dev/sessions/state/#__codelineno-4-3>)        LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-4-4>)            name = "StoryGenerator",
    [](<https://adk.dev/sessions/state/#__codelineno-4-5>)            model = model,
    [](<https://adk.dev/sessions/state/#__codelineno-4-6>)            instruction =
    [](<https://adk.dev/sessions/state/#__codelineno-4-7>)                Instruction(
    [](<https://adk.dev/sessions/state/#__codelineno-4-8>)                    "Write a short story about a cat, focusing on the theme: {topic}.",
    [](<https://adk.dev/sessions/state/#__codelineno-4-9>)                ),
    [](<https://adk.dev/sessions/state/#__codelineno-4-10>)        )
    [](<https://adk.dev/sessions/state/#__codelineno-4-11>)
    [](<https://adk.dev/sessions/state/#__codelineno-4-12>)    // Assuming session.state["topic"] is set to "friendship", the LLM
    [](<https://adk.dev/sessions/state/#__codelineno-4-13>)    // will receive the following instruction:
    [](<https://adk.dev/sessions/state/#__codelineno-4-14>)    // "Write a short story about a cat, focusing on the theme: friendship."
    [](<https://adk.dev/sessions/state/#__codelineno-4-15>)}
    
#### Important Considerations[¶](<https://adk.dev/sessions/state/#important-considerations> "Permanent link")

  * Key Existence: Ensure that the key you reference in the instruction string exists in the session.state. If the key is missing, the agent will throw an error. To use a key that may or may not be present, you can include a question mark (?) after the key (e.g. {topic?}).
  * Data Types: The value associated with the key should be a string or a type that can be easily converted to a string.
  * Literal Curly Braces: The `{key}` syntax matches any valid Python identifier inside single curly braces. If you need literal curly braces in your instruction, such as for JSON formatting or templating syntax, use an `InstructionProvider` function instead of a string (see below).

f-strings and double braces

Some ADK examples use Python f-strings in instructions, such as `f"Topic: {{initial_topic}}"`. The `{{` and `}}` in those examples are **Python f-string escaping** , not ADK syntax. At runtime, Python converts `{{initial_topic}}` to `{initial_topic}`, which ADK then treats as a normal state variable placeholder. If you are not using f-strings, use single braces `{key}` directly.

#### Using `InstructionProvider` for Full Control[¶](<https://adk.dev/sessions/state/#using-instructionprovider-for-full-control> "Permanent link")

In some cases, you may need full control over the instruction string — for example, when your instructions contain literal curly braces (e.g., JSON examples, templating syntax) that would otherwise be interpreted as state variable placeholders.

To achieve this, provide a function to the `instruction` parameter instead of a string. This function is called an `InstructionProvider`. When you use an `InstructionProvider`, the ADK will **not** attempt to inject state variables, and the returned string will be passed to the model as-is.

The `InstructionProvider` function receives a `ReadonlyContext` object, which you can use to access session state or other contextual information if you need to build the instruction dynamically.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/state/#__codelineno-5-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/sessions/state/#__codelineno-5-2>)from google.adk.agents.readonly_context import ReadonlyContext
    [](<https://adk.dev/sessions/state/#__codelineno-5-3>)
    [](<https://adk.dev/sessions/state/#__codelineno-5-4>)# This is an InstructionProvider
    [](<https://adk.dev/sessions/state/#__codelineno-5-5>)def my_instruction_provider(context: ReadonlyContext) -> str:
    [](<https://adk.dev/sessions/state/#__codelineno-5-6>)    # No state injection occurs — curly braces are treated as literal text.
    [](<https://adk.dev/sessions/state/#__codelineno-5-7>)    return 'Format your output as JSON: {"city": "<name>", "population": <number>}'
    [](<https://adk.dev/sessions/state/#__codelineno-5-8>)
    [](<https://adk.dev/sessions/state/#__codelineno-5-9>)agent = LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-5-10>)    model="gemini-flash-latest",
    [](<https://adk.dev/sessions/state/#__codelineno-5-11>)    name="template_helper_agent",
    [](<https://adk.dev/sessions/state/#__codelineno-5-12>)    instruction=my_instruction_provider
    [](<https://adk.dev/sessions/state/#__codelineno-5-13>))
    
    [](<https://adk.dev/sessions/state/#__codelineno-6-1>)import { LlmAgent, ReadonlyContext } from "@google/adk";
    [](<https://adk.dev/sessions/state/#__codelineno-6-2>)
    [](<https://adk.dev/sessions/state/#__codelineno-6-3>)// This is an InstructionProvider
    [](<https://adk.dev/sessions/state/#__codelineno-6-4>)function myInstructionProvider(context: ReadonlyContext): string {
    [](<https://adk.dev/sessions/state/#__codelineno-6-5>)    // No state injection occurs — curly braces are treated as literal text.
    [](<https://adk.dev/sessions/state/#__codelineno-6-6>)    return 'Format your output as JSON: {"city": "<name>", "population": <number>}';
    [](<https://adk.dev/sessions/state/#__codelineno-6-7>)}
    [](<https://adk.dev/sessions/state/#__codelineno-6-8>)
    [](<https://adk.dev/sessions/state/#__codelineno-6-9>)const agent = new LlmAgent({
    [](<https://adk.dev/sessions/state/#__codelineno-6-10>)    model: "gemini-flash-latest",
    [](<https://adk.dev/sessions/state/#__codelineno-6-11>)    name: "template_helper_agent",
    [](<https://adk.dev/sessions/state/#__codelineno-6-12>)    instruction: myInstructionProvider
    [](<https://adk.dev/sessions/state/#__codelineno-6-13>)});
    
    [](<https://adk.dev/sessions/state/#__codelineno-7-1>)//  1. This InstructionProvider returns a static string.
    [](<https://adk.dev/sessions/state/#__codelineno-7-2>)//     Because it's a provider function, the ADK will not attempt to inject
    [](<https://adk.dev/sessions/state/#__codelineno-7-3>)//     state, and the instruction will be passed to the model as-is,
    [](<https://adk.dev/sessions/state/#__codelineno-7-4>)//     preserving the literal braces.
    [](<https://adk.dev/sessions/state/#__codelineno-7-5>)func staticInstructionProvider(ctx agent.ReadonlyContext) (string, error) {
    [](<https://adk.dev/sessions/state/#__codelineno-7-6>)    return "This is an instruction with {{literal_braces}} that will not be replaced.", nil
    [](<https://adk.dev/sessions/state/#__codelineno-7-7>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-8-1>)import com.google.adk.agents.Instruction;
    [](<https://adk.dev/sessions/state/#__codelineno-8-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/sessions/state/#__codelineno-8-3>)import com.google.adk.agents.ReadonlyContext;
    [](<https://adk.dev/sessions/state/#__codelineno-8-4>)import io.reactivex.rxjava3.core.Single;
    [](<https://adk.dev/sessions/state/#__codelineno-8-5>)
    [](<https://adk.dev/sessions/state/#__codelineno-8-6>)// This is an Instruction.Provider
    [](<https://adk.dev/sessions/state/#__codelineno-8-7>)Instruction.Provider myInstructionProvider = new Instruction.Provider(
    [](<https://adk.dev/sessions/state/#__codelineno-8-8>)    (ReadonlyContext context) -> {
    [](<https://adk.dev/sessions/state/#__codelineno-8-9>)        // No state injection occurs — curly braces are treated as literal text.
    [](<https://adk.dev/sessions/state/#__codelineno-8-10>)        return Single.just("Format your output as JSON: {\"city\": \"<name>\", \"population\": <number>}");
    [](<https://adk.dev/sessions/state/#__codelineno-8-11>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-8-12>));
    [](<https://adk.dev/sessions/state/#__codelineno-8-13>)
    [](<https://adk.dev/sessions/state/#__codelineno-8-14>)LlmAgent agent = LlmAgent.builder()
    [](<https://adk.dev/sessions/state/#__codelineno-8-15>)    .model("gemini-flash-latest")
    [](<https://adk.dev/sessions/state/#__codelineno-8-16>)    .name("template_helper_agent")
    [](<https://adk.dev/sessions/state/#__codelineno-8-17>)    .instruction(myInstructionProvider)
    [](<https://adk.dev/sessions/state/#__codelineno-8-18>)    .build();
    
    [](<https://adk.dev/sessions/state/#__codelineno-9-1>)fun instructionProvider(model: Gemini) {
    [](<https://adk.dev/sessions/state/#__codelineno-9-2>)    // This is an Instruction.Provider
    [](<https://adk.dev/sessions/state/#__codelineno-9-3>)    val myInstructionProvider =
    [](<https://adk.dev/sessions/state/#__codelineno-9-4>)        Instruction { context: ReadonlyContext ->
    [](<https://adk.dev/sessions/state/#__codelineno-9-5>)            // No state injection occurs — curly braces are treated as literal text.
    [](<https://adk.dev/sessions/state/#__codelineno-9-6>)            Content(
    [](<https://adk.dev/sessions/state/#__codelineno-9-7>)                parts =
    [](<https://adk.dev/sessions/state/#__codelineno-9-8>)                    listOf(
    [](<https://adk.dev/sessions/state/#__codelineno-9-9>)                        Part(
    [](<https://adk.dev/sessions/state/#__codelineno-9-10>)                            text = "Format your output as JSON: {\"city\": \"<name>\", \"population\": <number>}",
    [](<https://adk.dev/sessions/state/#__codelineno-9-11>)                        ),
    [](<https://adk.dev/sessions/state/#__codelineno-9-12>)                    ),
    [](<https://adk.dev/sessions/state/#__codelineno-9-13>)            )
    [](<https://adk.dev/sessions/state/#__codelineno-9-14>)        }
    [](<https://adk.dev/sessions/state/#__codelineno-9-15>)
    [](<https://adk.dev/sessions/state/#__codelineno-9-16>)    val agent =
    [](<https://adk.dev/sessions/state/#__codelineno-9-17>)        LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-9-18>)            model = model,
    [](<https://adk.dev/sessions/state/#__codelineno-9-19>)            name = "template_helper_agent",
    [](<https://adk.dev/sessions/state/#__codelineno-9-20>)            instruction = myInstructionProvider,
    [](<https://adk.dev/sessions/state/#__codelineno-9-21>)        )
    [](<https://adk.dev/sessions/state/#__codelineno-9-22>)}
    
If you want to both use an `InstructionProvider` _and_ inject state into your instructions, you can use the `inject_session_state` utility function. Only `{key}` placeholders matching valid state variable names will be replaced; other text (including curly braces that don't match valid identifiers) will be left as-is.

PythonGoJava
    
    [](<https://adk.dev/sessions/state/#__codelineno-10-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/sessions/state/#__codelineno-10-2>)from google.adk.agents.readonly_context import ReadonlyContext
    [](<https://adk.dev/sessions/state/#__codelineno-10-3>)from google.adk.utils import instructions_utils
    [](<https://adk.dev/sessions/state/#__codelineno-10-4>)
    [](<https://adk.dev/sessions/state/#__codelineno-10-5>)async def my_dynamic_instruction_provider(context: ReadonlyContext) -> str:
    [](<https://adk.dev/sessions/state/#__codelineno-10-6>)    template = "This is a {adjective} instruction. Use JSON like: {\"key\": \"value\"}."
    [](<https://adk.dev/sessions/state/#__codelineno-10-7>)    # This will inject the 'adjective' state variable.
    [](<https://adk.dev/sessions/state/#__codelineno-10-8>)    # The JSON braces are left alone because their content is not a valid identifier.
    [](<https://adk.dev/sessions/state/#__codelineno-10-9>)    return await instructions_utils.inject_session_state(template, context)
    [](<https://adk.dev/sessions/state/#__codelineno-10-10>)
    [](<https://adk.dev/sessions/state/#__codelineno-10-11>)agent = LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-10-12>)    model="gemini-flash-latest",
    [](<https://adk.dev/sessions/state/#__codelineno-10-13>)    name="dynamic_template_helper_agent",
    [](<https://adk.dev/sessions/state/#__codelineno-10-14>)    instruction=my_dynamic_instruction_provider
    [](<https://adk.dev/sessions/state/#__codelineno-10-15>))
    
    [](<https://adk.dev/sessions/state/#__codelineno-11-1>)//  2. This InstructionProvider demonstrates how to manually inject state
    [](<https://adk.dev/sessions/state/#__codelineno-11-2>)//     while also preserving literal braces. It uses the instructionutil helper.
    [](<https://adk.dev/sessions/state/#__codelineno-11-3>)func dynamicInstructionProvider(ctx agent.ReadonlyContext) (string, error) {
    [](<https://adk.dev/sessions/state/#__codelineno-11-4>)    template := "This is a {adjective} instruction with {{literal_braces}}."
    [](<https://adk.dev/sessions/state/#__codelineno-11-5>)    // This will inject the 'adjective' state variable but leave the literal braces.
    [](<https://adk.dev/sessions/state/#__codelineno-11-6>)    return instructionutil.InjectSessionState(ctx, template)
    [](<https://adk.dev/sessions/state/#__codelineno-11-7>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-12-1>)import com.google.adk.agents.Instruction;
    [](<https://adk.dev/sessions/state/#__codelineno-12-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/sessions/state/#__codelineno-12-3>)import com.google.adk.agents.ReadonlyContext;
    [](<https://adk.dev/sessions/state/#__codelineno-12-4>)import com.google.adk.utils.InstructionUtils;
    [](<https://adk.dev/sessions/state/#__codelineno-12-5>)import io.reactivex.rxjava3.core.Single;
    [](<https://adk.dev/sessions/state/#__codelineno-12-6>)
    [](<https://adk.dev/sessions/state/#__codelineno-12-7>)Instruction.Provider myDynamicInstructionProvider = new Instruction.Provider(
    [](<https://adk.dev/sessions/state/#__codelineno-12-8>)    (ReadonlyContext context) -> {
    [](<https://adk.dev/sessions/state/#__codelineno-12-9>)        String template = "This is a " + adjective + " instruction. Use JSON like: {\"key\": \"value\"}.";
    [](<https://adk.dev/sessions/state/#__codelineno-12-10>)        // This will inject the 'adjective' state variable.
    [](<https://adk.dev/sessions/state/#__codelineno-12-11>)        // The JSON braces are left alone because their content is not a valid identifier.
    [](<https://adk.dev/sessions/state/#__codelineno-12-12>)        return InstructionUtils.injectSessionState(context.invocationContext(), template);
    [](<https://adk.dev/sessions/state/#__codelineno-12-13>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-12-14>));
    [](<https://adk.dev/sessions/state/#__codelineno-12-15>)
    [](<https://adk.dev/sessions/state/#__codelineno-12-16>)LlmAgent agent = LlmAgent.builder()
    [](<https://adk.dev/sessions/state/#__codelineno-12-17>)    .model("gemini-flash-latest")
    [](<https://adk.dev/sessions/state/#__codelineno-12-18>)    .name("dynamic_template_helper_agent")
    [](<https://adk.dev/sessions/state/#__codelineno-12-19>)    .instruction(myDynamicInstructionProvider)
    [](<https://adk.dev/sessions/state/#__codelineno-12-20>)    .build();
    
**Benefits of Direct Injection**

  * Clarity: Makes it explicit which parts of the instruction are dynamic and based on session state.
  * Reliability: Avoids relying on the LLM to correctly interpret natural language instructions to access state.
  * Maintainability: Simplifies instruction strings and reduces the risk of errors when updating state variable names.

**Relation to Other State Access Methods**

This direct injection method is specific to LlmAgent instructions. Refer to the following section for more information on other state access methods.

### How State is Updated: Recommended Methods[¶](<https://adk.dev/sessions/state/#how-state-is-updated-recommended-methods> "Permanent link")

The Right Way to Modify State

When you need to change the session state, the correct and safest method is to **directly modify the`state` object on the `Context`** provided to your function (e.g., `callback_context.state['my_key'] = 'new_value'`). This is considered "direct state manipulation" in the right way, as the framework automatically tracks these changes.

This is critically different from directly modifying the `state` on a `Session` object you retrieve from the `SessionService` (e.g., `my_session.state['my_key'] = 'new_value'`). **You should avoid this** , as it bypasses the ADK's event tracking and can lead to lost data. The "Warning" section at the end of this page has more details on this important distinction.

State should **always** be updated as part of adding an `Event` to the session history using `session_service.append_event()`. This ensures changes are tracked, persistence works correctly, and updates are thread-safe.

**1\. The Easy Way:`output_key` (for Agent Text Responses)**

This is the simplest method for saving an agent's final text response directly into the state. When defining your `LlmAgent`, specify the `output_key`:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/sessions/state/#__codelineno-13-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/sessions/state/#__codelineno-13-2>)from google.adk.sessions import InMemorySessionService, Session
    [](<https://adk.dev/sessions/state/#__codelineno-13-3>)from google.adk.runners import Runner
    [](<https://adk.dev/sessions/state/#__codelineno-13-4>)from google.genai.types import Content, Part
    [](<https://adk.dev/sessions/state/#__codelineno-13-5>)
    [](<https://adk.dev/sessions/state/#__codelineno-13-6>)# Define agent with output_key
    [](<https://adk.dev/sessions/state/#__codelineno-13-7>)greeting_agent = LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-13-8>)    name="Greeter",
    [](<https://adk.dev/sessions/state/#__codelineno-13-9>)    model="gemini-flash-latest", # Use a valid model
    [](<https://adk.dev/sessions/state/#__codelineno-13-10>)    instruction="Generate a short, friendly greeting.",
    [](<https://adk.dev/sessions/state/#__codelineno-13-11>)    output_key="last_greeting" # Save response to state['last_greeting']
    [](<https://adk.dev/sessions/state/#__codelineno-13-12>))
    [](<https://adk.dev/sessions/state/#__codelineno-13-13>)
    [](<https://adk.dev/sessions/state/#__codelineno-13-14>)# --- Setup Runner and Session ---
    [](<https://adk.dev/sessions/state/#__codelineno-13-15>)app_name, user_id, session_id = "state_app", "user1", "session1"
    [](<https://adk.dev/sessions/state/#__codelineno-13-16>)session_service = InMemorySessionService()
    [](<https://adk.dev/sessions/state/#__codelineno-13-17>)runner = Runner(
    [](<https://adk.dev/sessions/state/#__codelineno-13-18>)    agent=greeting_agent,
    [](<https://adk.dev/sessions/state/#__codelineno-13-19>)    app_name=app_name,
    [](<https://adk.dev/sessions/state/#__codelineno-13-20>)    session_service=session_service
    [](<https://adk.dev/sessions/state/#__codelineno-13-21>))
    [](<https://adk.dev/sessions/state/#__codelineno-13-22>)session = await session_service.create_session(app_name=app_name,
    [](<https://adk.dev/sessions/state/#__codelineno-13-23>)                                    user_id=user_id,
    [](<https://adk.dev/sessions/state/#__codelineno-13-24>)                                    session_id=session_id)
    [](<https://adk.dev/sessions/state/#__codelineno-13-25>)print(f"Initial state: {session.state}")
    [](<https://adk.dev/sessions/state/#__codelineno-13-26>)
    [](<https://adk.dev/sessions/state/#__codelineno-13-27>)# --- Run the Agent ---
    [](<https://adk.dev/sessions/state/#__codelineno-13-28>)# Runner handles calling append_event, which uses the output_key
    [](<https://adk.dev/sessions/state/#__codelineno-13-29>)# to automatically create the state_delta.
    [](<https://adk.dev/sessions/state/#__codelineno-13-30>)user_message = Content(parts=[Part(text="Hello")])
    [](<https://adk.dev/sessions/state/#__codelineno-13-31>)for event in runner.run(user_id=user_id,
    [](<https://adk.dev/sessions/state/#__codelineno-13-32>)                        session_id=session_id,
    [](<https://adk.dev/sessions/state/#__codelineno-13-33>)                        new_message=user_message):
    [](<https://adk.dev/sessions/state/#__codelineno-13-34>)    if event.is_final_response():
    [](<https://adk.dev/sessions/state/#__codelineno-13-35>)      print(f"Agent responded.") # Response text is also in event.content
    [](<https://adk.dev/sessions/state/#__codelineno-13-36>)
    [](<https://adk.dev/sessions/state/#__codelineno-13-37>)# --- Check Updated State ---
    [](<https://adk.dev/sessions/state/#__codelineno-13-38>)updated_session = await session_service.get_session(app_name=app_name, user_id=user_id, session_id=session_id)
    [](<https://adk.dev/sessions/state/#__codelineno-13-39>)print(f"State after agent run: {updated_session.state}")
    [](<https://adk.dev/sessions/state/#__codelineno-13-40>)# Expected output might include: {'last_greeting': 'Hello there! How can I help you today?'}
    
    [](<https://adk.dev/sessions/state/#__codelineno-14-1>)import { LlmAgent, Runner, InMemorySessionService, isFinalResponse } from "@google/adk";
    [](<https://adk.dev/sessions/state/#__codelineno-14-2>)import { Content } from "@google/genai";
    [](<https://adk.dev/sessions/state/#__codelineno-14-3>)
    [](<https://adk.dev/sessions/state/#__codelineno-14-4>)// Define agent with outputKey
    [](<https://adk.dev/sessions/state/#__codelineno-14-5>)const greetingAgent = new LlmAgent({
    [](<https://adk.dev/sessions/state/#__codelineno-14-6>)    name: "Greeter",
    [](<https://adk.dev/sessions/state/#__codelineno-14-7>)    model: "gemini-flash-latest",
    [](<https://adk.dev/sessions/state/#__codelineno-14-8>)    instruction: "Generate a short, friendly greeting.",
    [](<https://adk.dev/sessions/state/#__codelineno-14-9>)    outputKey: "last_greeting" // Save response to state['last_greeting']
    [](<https://adk.dev/sessions/state/#__codelineno-14-10>)});
    [](<https://adk.dev/sessions/state/#__codelineno-14-11>)
    [](<https://adk.dev/sessions/state/#__codelineno-14-12>)// --- Setup Runner and Session ---
    [](<https://adk.dev/sessions/state/#__codelineno-14-13>)const appName = "state_app";
    [](<https://adk.dev/sessions/state/#__codelineno-14-14>)const userId = "user1";
    [](<https://adk.dev/sessions/state/#__codelineno-14-15>)const sessionId = "session1";
    [](<https://adk.dev/sessions/state/#__codelineno-14-16>)const sessionService = new InMemorySessionService();
    [](<https://adk.dev/sessions/state/#__codelineno-14-17>)const runner = new Runner({
    [](<https://adk.dev/sessions/state/#__codelineno-14-18>)    agent: greetingAgent,
    [](<https://adk.dev/sessions/state/#__codelineno-14-19>)    appName: appName,
    [](<https://adk.dev/sessions/state/#__codelineno-14-20>)    sessionService: sessionService
    [](<https://adk.dev/sessions/state/#__codelineno-14-21>)});
    [](<https://adk.dev/sessions/state/#__codelineno-14-22>)const session = await sessionService.createSession({
    [](<https://adk.dev/sessions/state/#__codelineno-14-23>)    appName,
    [](<https://adk.dev/sessions/state/#__codelineno-14-24>)    userId,
    [](<https://adk.dev/sessions/state/#__codelineno-14-25>)    sessionId
    [](<https://adk.dev/sessions/state/#__codelineno-14-26>)});
    [](<https://adk.dev/sessions/state/#__codelineno-14-27>)console.log(`Initial state: ${JSON.stringify(session.state)}`);
    [](<https://adk.dev/sessions/state/#__codelineno-14-28>)
    [](<https://adk.dev/sessions/state/#__codelineno-14-29>)// --- Run the Agent ---
    [](<https://adk.dev/sessions/state/#__codelineno-14-30>)// Runner handles calling appendEvent, which uses the outputKey
    [](<https://adk.dev/sessions/state/#__codelineno-14-31>)// to automatically create the stateDelta.
    [](<https://adk.dev/sessions/state/#__codelineno-14-32>)const userMessage: Content = { parts: [{ text: "Hello" }] };
    [](<https://adk.dev/sessions/state/#__codelineno-14-33>)for await (const event of runner.runAsync({
    [](<https://adk.dev/sessions/state/#__codelineno-14-34>)    userId,
    [](<https://adk.dev/sessions/state/#__codelineno-14-35>)    sessionId,
    [](<https://adk.dev/sessions/state/#__codelineno-14-36>)    newMessage: userMessage
    [](<https://adk.dev/sessions/state/#__codelineno-14-37>)})) {
    [](<https://adk.dev/sessions/state/#__codelineno-14-38>)    if (isFinalResponse(event)) {
    [](<https://adk.dev/sessions/state/#__codelineno-14-39>)      console.log("Agent responded."); // Response text is also in event.content
    [](<https://adk.dev/sessions/state/#__codelineno-14-40>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-14-41>)}
    [](<https://adk.dev/sessions/state/#__codelineno-14-42>)
    [](<https://adk.dev/sessions/state/#__codelineno-14-43>)// --- Check Updated State ---
    [](<https://adk.dev/sessions/state/#__codelineno-14-44>)const updatedSession = await sessionService.getSession({ appName, userId, sessionId });
    [](<https://adk.dev/sessions/state/#__codelineno-14-45>)console.log(`State after agent run: ${JSON.stringify(updatedSession?.state)}`);
    [](<https://adk.dev/sessions/state/#__codelineno-14-46>)// Expected output might include: {"last_greeting":"Hello there! How can I help you today?"}
    
    [](<https://adk.dev/sessions/state/#__codelineno-15-1>)//  1. GreetingAgent demonstrates using `OutputKey` to save an agent's
    [](<https://adk.dev/sessions/state/#__codelineno-15-2>)//     final text response directly into the session state.
    [](<https://adk.dev/sessions/state/#__codelineno-15-3>)func greetingAgentExample(sessionService session.Service) {
    [](<https://adk.dev/sessions/state/#__codelineno-15-4>)    fmt.Println("--- Running GreetingAgent (output_key) Example ---")
    [](<https://adk.dev/sessions/state/#__codelineno-15-5>)    ctx := context.Background()
    [](<https://adk.dev/sessions/state/#__codelineno-15-6>)
    [](<https://adk.dev/sessions/state/#__codelineno-15-7>)    modelGreeting, err := gemini.NewModel(ctx, modelID, nil)
    [](<https://adk.dev/sessions/state/#__codelineno-15-8>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-15-9>)        log.Fatalf("Failed to create Gemini model for greeting agent: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-15-10>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-15-11>)    greetingAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/sessions/state/#__codelineno-15-12>)        Name:        "Greeter",
    [](<https://adk.dev/sessions/state/#__codelineno-15-13>)        Model:       modelGreeting,
    [](<https://adk.dev/sessions/state/#__codelineno-15-14>)        Instruction: "Generate a short, friendly greeting.",
    [](<https://adk.dev/sessions/state/#__codelineno-15-15>)        OutputKey:   "last_greeting",
    [](<https://adk.dev/sessions/state/#__codelineno-15-16>)    })
    [](<https://adk.dev/sessions/state/#__codelineno-15-17>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-15-18>)        log.Fatalf("Failed to create greeting agent: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-15-19>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-15-20>)
    [](<https://adk.dev/sessions/state/#__codelineno-15-21>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/sessions/state/#__codelineno-15-22>)        AppName:        appName,
    [](<https://adk.dev/sessions/state/#__codelineno-15-23>)        Agent:          agent.Agent(greetingAgent),
    [](<https://adk.dev/sessions/state/#__codelineno-15-24>)        SessionService: sessionService,
    [](<https://adk.dev/sessions/state/#__codelineno-15-25>)    })
    [](<https://adk.dev/sessions/state/#__codelineno-15-26>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-15-27>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-15-28>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-15-29>)
    [](<https://adk.dev/sessions/state/#__codelineno-15-30>)    // Run the agent
    [](<https://adk.dev/sessions/state/#__codelineno-15-31>)    userMessage := genai.NewContentFromText("Hello", "user")
    [](<https://adk.dev/sessions/state/#__codelineno-15-32>)    for event, err := range r.Run(ctx, userID, sessionID, userMessage, agent.RunConfig{}) {
    [](<https://adk.dev/sessions/state/#__codelineno-15-33>)        if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-15-34>)            log.Printf("Agent Error: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-15-35>)            continue
    [](<https://adk.dev/sessions/state/#__codelineno-15-36>)        }
    [](<https://adk.dev/sessions/state/#__codelineno-15-37>)        if isFinalResponse(event) {
    [](<https://adk.dev/sessions/state/#__codelineno-15-38>)            if event.LLMResponse.Content != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-15-39>)                fmt.Printf("Agent responded with: %q\n", textParts(event.LLMResponse.Content))
    [](<https://adk.dev/sessions/state/#__codelineno-15-40>)            } else {
    [](<https://adk.dev/sessions/state/#__codelineno-15-41>)                fmt.Println("Agent responded.")
    [](<https://adk.dev/sessions/state/#__codelineno-15-42>)            }
    [](<https://adk.dev/sessions/state/#__codelineno-15-43>)        }
    [](<https://adk.dev/sessions/state/#__codelineno-15-44>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-15-45>)
    [](<https://adk.dev/sessions/state/#__codelineno-15-46>)    // Check the updated state
    [](<https://adk.dev/sessions/state/#__codelineno-15-47>)    resp, err := sessionService.Get(ctx, &session.GetRequest{AppName: appName, UserID: userID, SessionID: sessionID})
    [](<https://adk.dev/sessions/state/#__codelineno-15-48>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-15-49>)        log.Fatalf("Failed to get session: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-15-50>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-15-51>)    lastGreeting, _ := resp.Session.State().Get("last_greeting")
    [](<https://adk.dev/sessions/state/#__codelineno-15-52>)    fmt.Printf("State after agent run: last_greeting = %q\n\n", lastGreeting)
    [](<https://adk.dev/sessions/state/#__codelineno-15-53>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-16-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/sessions/state/#__codelineno-16-2>)import com.google.adk.agents.RunConfig;
    [](<https://adk.dev/sessions/state/#__codelineno-16-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/sessions/state/#__codelineno-16-4>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/sessions/state/#__codelineno-16-5>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/sessions/state/#__codelineno-16-6>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/sessions/state/#__codelineno-16-7>)import com.google.genai.types.Content;
    [](<https://adk.dev/sessions/state/#__codelineno-16-8>)import com.google.genai.types.Part;
    [](<https://adk.dev/sessions/state/#__codelineno-16-9>)import java.util.List;
    [](<https://adk.dev/sessions/state/#__codelineno-16-10>)import java.util.Optional;
    [](<https://adk.dev/sessions/state/#__codelineno-16-11>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-12>)public class GreetingAgentExample {
    [](<https://adk.dev/sessions/state/#__codelineno-16-13>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-14>)  public static void main(String[] args) {
    [](<https://adk.dev/sessions/state/#__codelineno-16-15>)    // Define agent with output_key
    [](<https://adk.dev/sessions/state/#__codelineno-16-16>)    LlmAgent greetingAgent =
    [](<https://adk.dev/sessions/state/#__codelineno-16-17>)        LlmAgent.builder()
    [](<https://adk.dev/sessions/state/#__codelineno-16-18>)            .name("Greeter")
    [](<https://adk.dev/sessions/state/#__codelineno-16-19>)            .model("gemini-2.5-flash")
    [](<https://adk.dev/sessions/state/#__codelineno-16-20>)            .instruction("Generate a short, friendly greeting.")
    [](<https://adk.dev/sessions/state/#__codelineno-16-21>)            .description("Greeting agent")
    [](<https://adk.dev/sessions/state/#__codelineno-16-22>)            .outputKey("last_greeting") // Save response to state['last_greeting']
    [](<https://adk.dev/sessions/state/#__codelineno-16-23>)            .build();
    [](<https://adk.dev/sessions/state/#__codelineno-16-24>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-25>)    // --- Setup Runner and Session ---
    [](<https://adk.dev/sessions/state/#__codelineno-16-26>)    String appName = "state_app";
    [](<https://adk.dev/sessions/state/#__codelineno-16-27>)    String userId = "user1";
    [](<https://adk.dev/sessions/state/#__codelineno-16-28>)    String sessionId = "session1";
    [](<https://adk.dev/sessions/state/#__codelineno-16-29>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-30>)    InMemorySessionService sessionService = new InMemorySessionService();
    [](<https://adk.dev/sessions/state/#__codelineno-16-31>)    Runner runner = Runner.builder()
    [](<https://adk.dev/sessions/state/#__codelineno-16-32>)      .agent(greetingAgent)
    [](<https://adk.dev/sessions/state/#__codelineno-16-33>)      .appName(appName)
    [](<https://adk.dev/sessions/state/#__codelineno-16-34>)      .sessionService(sessionService)
    [](<https://adk.dev/sessions/state/#__codelineno-16-35>)      .build();
    [](<https://adk.dev/sessions/state/#__codelineno-16-36>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-37>)    Session session =
    [](<https://adk.dev/sessions/state/#__codelineno-16-38>)        sessionService.createSession(appName, userId, null, sessionId).blockingGet();
    [](<https://adk.dev/sessions/state/#__codelineno-16-39>)    System.out.println("Initial state: " + session.state().entrySet());
    [](<https://adk.dev/sessions/state/#__codelineno-16-40>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-41>)    // --- Run the Agent ---
    [](<https://adk.dev/sessions/state/#__codelineno-16-42>)    // Runner handles calling appendEvent, which uses the output_key
    [](<https://adk.dev/sessions/state/#__codelineno-16-43>)    // to automatically create the stateDelta.
    [](<https://adk.dev/sessions/state/#__codelineno-16-44>)    Content userMessage = Content.builder().parts(List.of(Part.fromText("Hello"))).build();
    [](<https://adk.dev/sessions/state/#__codelineno-16-45>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-46>)    // RunConfig is needed for runner.runAsync in Java
    [](<https://adk.dev/sessions/state/#__codelineno-16-47>)    RunConfig runConfig = RunConfig.builder().build();
    [](<https://adk.dev/sessions/state/#__codelineno-16-48>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-49>)    for (Event event : runner.runAsync(userId, sessionId, userMessage, runConfig).blockingIterable()) {
    [](<https://adk.dev/sessions/state/#__codelineno-16-50>)      if (event.finalResponse()) {
    [](<https://adk.dev/sessions/state/#__codelineno-16-51>)        System.out.println("Agent responded."); // Response text is also in event.content
    [](<https://adk.dev/sessions/state/#__codelineno-16-52>)      }
    [](<https://adk.dev/sessions/state/#__codelineno-16-53>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-16-54>)
    [](<https://adk.dev/sessions/state/#__codelineno-16-55>)    // --- Check Updated State ---
    [](<https://adk.dev/sessions/state/#__codelineno-16-56>)    Session updatedSession =
    [](<https://adk.dev/sessions/state/#__codelineno-16-57>)        sessionService.getSession(appName, userId, sessionId, Optional.empty()).blockingGet();
    [](<https://adk.dev/sessions/state/#__codelineno-16-58>)    assert updatedSession != null;
    [](<https://adk.dev/sessions/state/#__codelineno-16-59>)    System.out.println("State after agent run: " + updatedSession.state().entrySet());
    [](<https://adk.dev/sessions/state/#__codelineno-16-60>)    // Expected output might include: {'last_greeting': 'Hello there! How can I help you today?'}
    [](<https://adk.dev/sessions/state/#__codelineno-16-61>)  }
    [](<https://adk.dev/sessions/state/#__codelineno-16-62>)}
    
Behind the scenes, the `Runner` uses the `output_key` to create the necessary `EventActions` with a `state_delta` and calls `append_event`.

**2\. The Standard Way:`EventActions.state_delta` (for Complex Updates)**

For more complex scenarios (updating multiple keys, non-string values, specific scopes like `user:` or `app:`, or updates not tied directly to the agent's final text), you manually construct the `state_delta` within `EventActions`.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/state/#__codelineno-17-1>)from google.adk.sessions import InMemorySessionService, Session
    [](<https://adk.dev/sessions/state/#__codelineno-17-2>)from google.adk.events import Event, EventActions
    [](<https://adk.dev/sessions/state/#__codelineno-17-3>)from google.genai.types import Part, Content
    [](<https://adk.dev/sessions/state/#__codelineno-17-4>)import time
    [](<https://adk.dev/sessions/state/#__codelineno-17-5>)
    [](<https://adk.dev/sessions/state/#__codelineno-17-6>)# --- Setup ---
    [](<https://adk.dev/sessions/state/#__codelineno-17-7>)session_service = InMemorySessionService()
    [](<https://adk.dev/sessions/state/#__codelineno-17-8>)app_name, user_id, session_id = "state_app_manual", "user2", "session2"
    [](<https://adk.dev/sessions/state/#__codelineno-17-9>)session = await session_service.create_session(
    [](<https://adk.dev/sessions/state/#__codelineno-17-10>)    app_name=app_name,
    [](<https://adk.dev/sessions/state/#__codelineno-17-11>)    user_id=user_id,
    [](<https://adk.dev/sessions/state/#__codelineno-17-12>)    session_id=session_id,
    [](<https://adk.dev/sessions/state/#__codelineno-17-13>)    state={"user:login_count": 0, "task_status": "idle"}
    [](<https://adk.dev/sessions/state/#__codelineno-17-14>))
    [](<https://adk.dev/sessions/state/#__codelineno-17-15>)print(f"Initial state: {session.state}")
    [](<https://adk.dev/sessions/state/#__codelineno-17-16>)
    [](<https://adk.dev/sessions/state/#__codelineno-17-17>)# --- Define State Changes ---
    [](<https://adk.dev/sessions/state/#__codelineno-17-18>)current_time = time.time()
    [](<https://adk.dev/sessions/state/#__codelineno-17-19>)state_changes = {
    [](<https://adk.dev/sessions/state/#__codelineno-17-20>)    "task_status": "active",              # Update session state
    [](<https://adk.dev/sessions/state/#__codelineno-17-21>)    "user:login_count": session.state.get("user:login_count", 0) + 1, # Update user state
    [](<https://adk.dev/sessions/state/#__codelineno-17-22>)    "user:last_login_ts": current_time,   # Add user state
    [](<https://adk.dev/sessions/state/#__codelineno-17-23>)    "temp:validation_needed": True        # Add temporary state (will be discarded)
    [](<https://adk.dev/sessions/state/#__codelineno-17-24>)}
    [](<https://adk.dev/sessions/state/#__codelineno-17-25>)
    [](<https://adk.dev/sessions/state/#__codelineno-17-26>)# --- Create Event with Actions ---
    [](<https://adk.dev/sessions/state/#__codelineno-17-27>)actions_with_update = EventActions(state_delta=state_changes)
    [](<https://adk.dev/sessions/state/#__codelineno-17-28>)# This event might represent an internal system action, not just an agent response
    [](<https://adk.dev/sessions/state/#__codelineno-17-29>)system_event = Event(
    [](<https://adk.dev/sessions/state/#__codelineno-17-30>)    invocation_id="inv_login_update",
    [](<https://adk.dev/sessions/state/#__codelineno-17-31>)    author="system", # Or 'agent', 'tool' etc.
    [](<https://adk.dev/sessions/state/#__codelineno-17-32>)    actions=actions_with_update,
    [](<https://adk.dev/sessions/state/#__codelineno-17-33>)    timestamp=current_time
    [](<https://adk.dev/sessions/state/#__codelineno-17-34>)    # content might be None or represent the action taken
    [](<https://adk.dev/sessions/state/#__codelineno-17-35>))
    [](<https://adk.dev/sessions/state/#__codelineno-17-36>)
    [](<https://adk.dev/sessions/state/#__codelineno-17-37>)# --- Append the Event (This updates the state) ---
    [](<https://adk.dev/sessions/state/#__codelineno-17-38>)await session_service.append_event(session, system_event)
    [](<https://adk.dev/sessions/state/#__codelineno-17-39>)print("`append_event` called with explicit state delta.")
    [](<https://adk.dev/sessions/state/#__codelineno-17-40>)
    [](<https://adk.dev/sessions/state/#__codelineno-17-41>)# --- Check Updated State ---
    [](<https://adk.dev/sessions/state/#__codelineno-17-42>)updated_session = await session_service.get_session(app_name=app_name,
    [](<https://adk.dev/sessions/state/#__codelineno-17-43>)                                            user_id=user_id,
    [](<https://adk.dev/sessions/state/#__codelineno-17-44>)                                            session_id=session_id)
    [](<https://adk.dev/sessions/state/#__codelineno-17-45>)print(f"State after event: {updated_session.state}")
    [](<https://adk.dev/sessions/state/#__codelineno-17-46>)# Expected: {'user:login_count': 1, 'task_status': 'active', 'user:last_login_ts': <timestamp>}
    [](<https://adk.dev/sessions/state/#__codelineno-17-47>)# Note: 'temp:validation_needed' is NOT present.
    
    [](<https://adk.dev/sessions/state/#__codelineno-18-1>)import { InMemorySessionService, createEvent, createEventActions } from "@google/adk";
    [](<https://adk.dev/sessions/state/#__codelineno-18-2>)
    [](<https://adk.dev/sessions/state/#__codelineno-18-3>)// --- Setup ---
    [](<https://adk.dev/sessions/state/#__codelineno-18-4>)const sessionService = new InMemorySessionService();
    [](<https://adk.dev/sessions/state/#__codelineno-18-5>)const appName = "state_app_manual";
    [](<https://adk.dev/sessions/state/#__codelineno-18-6>)const userId = "user2";
    [](<https://adk.dev/sessions/state/#__codelineno-18-7>)const sessionId = "session2";
    [](<https://adk.dev/sessions/state/#__codelineno-18-8>)const session = await sessionService.createSession({
    [](<https://adk.dev/sessions/state/#__codelineno-18-9>)    appName,
    [](<https://adk.dev/sessions/state/#__codelineno-18-10>)    userId,
    [](<https://adk.dev/sessions/state/#__codelineno-18-11>)    sessionId,
    [](<https://adk.dev/sessions/state/#__codelineno-18-12>)    state: { "user:login_count": 0, "task_status": "idle" }
    [](<https://adk.dev/sessions/state/#__codelineno-18-13>)});
    [](<https://adk.dev/sessions/state/#__codelineno-18-14>)console.log(`Initial state: ${JSON.stringify(session.state)}`);
    [](<https://adk.dev/sessions/state/#__codelineno-18-15>)
    [](<https://adk.dev/sessions/state/#__codelineno-18-16>)// --- Define State Changes ---
    [](<https://adk.dev/sessions/state/#__codelineno-18-17>)const currentTime = Date.now();
    [](<https://adk.dev/sessions/state/#__codelineno-18-18>)const stateChanges = {
    [](<https://adk.dev/sessions/state/#__codelineno-18-19>)    "task_status": "active",              // Update session state
    [](<https://adk.dev/sessions/state/#__codelineno-18-20>)    "user:login_count": (session.state["user:login_count"] as number || 0) + 1, // Update user state
    [](<https://adk.dev/sessions/state/#__codelineno-18-21>)    "user:last_login_ts": currentTime,   // Add user state
    [](<https://adk.dev/sessions/state/#__codelineno-18-22>)    "temp:validation_needed": true        // Add temporary state (will be discarded)
    [](<https://adk.dev/sessions/state/#__codelineno-18-23>)};
    [](<https://adk.dev/sessions/state/#__codelineno-18-24>)
    [](<https://adk.dev/sessions/state/#__codelineno-18-25>)// --- Create Event with Actions ---
    [](<https://adk.dev/sessions/state/#__codelineno-18-26>)const actionsWithUpdate = createEventActions({
    [](<https://adk.dev/sessions/state/#__codelineno-18-27>)    stateDelta: stateChanges,
    [](<https://adk.dev/sessions/state/#__codelineno-18-28>)});
    [](<https://adk.dev/sessions/state/#__codelineno-18-29>)// This event might represent an internal system action, not just an agent response
    [](<https://adk.dev/sessions/state/#__codelineno-18-30>)const systemEvent = createEvent({
    [](<https://adk.dev/sessions/state/#__codelineno-18-31>)    invocationId: "inv_login_update",
    [](<https://adk.dev/sessions/state/#__codelineno-18-32>)    author: "system", // Or 'agent', 'tool' etc.
    [](<https://adk.dev/sessions/state/#__codelineno-18-33>)    actions: actionsWithUpdate,
    [](<https://adk.dev/sessions/state/#__codelineno-18-34>)    timestamp: currentTime
    [](<https://adk.dev/sessions/state/#__codelineno-18-35>)    // content might be null or represent the action taken
    [](<https://adk.dev/sessions/state/#__codelineno-18-36>)});
    [](<https://adk.dev/sessions/state/#__codelineno-18-37>)
    [](<https://adk.dev/sessions/state/#__codelineno-18-38>)// --- Append the Event (This updates the state) ---
    [](<https://adk.dev/sessions/state/#__codelineno-18-39>)await sessionService.appendEvent({ session, event: systemEvent });
    [](<https://adk.dev/sessions/state/#__codelineno-18-40>)console.log("`appendEvent` called with explicit state delta.");
    [](<https://adk.dev/sessions/state/#__codelineno-18-41>)
    [](<https://adk.dev/sessions/state/#__codelineno-18-42>)// --- Check Updated State ---
    [](<https://adk.dev/sessions/state/#__codelineno-18-43>)const updatedSession = await sessionService.getSession({
    [](<https://adk.dev/sessions/state/#__codelineno-18-44>)    appName,
    [](<https://adk.dev/sessions/state/#__codelineno-18-45>)    userId,
    [](<https://adk.dev/sessions/state/#__codelineno-18-46>)    sessionId
    [](<https://adk.dev/sessions/state/#__codelineno-18-47>)});
    [](<https://adk.dev/sessions/state/#__codelineno-18-48>)console.log(`State after event: ${JSON.stringify(updatedSession?.state)}`);
    [](<https://adk.dev/sessions/state/#__codelineno-18-49>)// Expected: {"user:login_count":1,"task_status":"active","user:last_login_ts":<timestamp>}
    [](<https://adk.dev/sessions/state/#__codelineno-18-50>)// Note: 'temp:validation_needed' is NOT present.
    
    [](<https://adk.dev/sessions/state/#__codelineno-19-1>)//  2. manualStateUpdateExample demonstrates creating an event with explicit
    [](<https://adk.dev/sessions/state/#__codelineno-19-2>)//     state changes (a "state_delta") to update multiple keys, including
    [](<https://adk.dev/sessions/state/#__codelineno-19-3>)//     those with user- and temp- prefixes.
    [](<https://adk.dev/sessions/state/#__codelineno-19-4>)func manualStateUpdateExample(sessionService session.Service) {
    [](<https://adk.dev/sessions/state/#__codelineno-19-5>)    fmt.Println("--- Running Manual State Update (EventActions) Example ---")
    [](<https://adk.dev/sessions/state/#__codelineno-19-6>)    ctx := context.Background()
    [](<https://adk.dev/sessions/state/#__codelineno-19-7>)    s, err := sessionService.Get(ctx, &session.GetRequest{AppName: appName, UserID: userID, SessionID: sessionID})
    [](<https://adk.dev/sessions/state/#__codelineno-19-8>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-19-9>)        log.Fatalf("Failed to get session: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-19-10>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-19-11>)    retrievedSession := s.Session
    [](<https://adk.dev/sessions/state/#__codelineno-19-12>)
    [](<https://adk.dev/sessions/state/#__codelineno-19-13>)    // Define state changes
    [](<https://adk.dev/sessions/state/#__codelineno-19-14>)    loginCount, _ := retrievedSession.State().Get("user:login_count")
    [](<https://adk.dev/sessions/state/#__codelineno-19-15>)    newLoginCount := 1
    [](<https://adk.dev/sessions/state/#__codelineno-19-16>)    if lc, ok := loginCount.(int); ok {
    [](<https://adk.dev/sessions/state/#__codelineno-19-17>)        newLoginCount = lc + 1
    [](<https://adk.dev/sessions/state/#__codelineno-19-18>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-19-19>)
    [](<https://adk.dev/sessions/state/#__codelineno-19-20>)    stateChanges := map[string]any{
    [](<https://adk.dev/sessions/state/#__codelineno-19-21>)        "task_status":            "active",
    [](<https://adk.dev/sessions/state/#__codelineno-19-22>)        "user:login_count":       newLoginCount,
    [](<https://adk.dev/sessions/state/#__codelineno-19-23>)        "user:last_login_ts":     time.Now().Unix(),
    [](<https://adk.dev/sessions/state/#__codelineno-19-24>)        "temp:validation_needed": true,
    [](<https://adk.dev/sessions/state/#__codelineno-19-25>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-19-26>)
    [](<https://adk.dev/sessions/state/#__codelineno-19-27>)    // Create an event with the state changes
    [](<https://adk.dev/sessions/state/#__codelineno-19-28>)    systemEvent := session.NewEvent(ctx, "inv_login_update")
    [](<https://adk.dev/sessions/state/#__codelineno-19-29>)    systemEvent.Author = "system"
    [](<https://adk.dev/sessions/state/#__codelineno-19-30>)    systemEvent.Actions.StateDelta = stateChanges
    [](<https://adk.dev/sessions/state/#__codelineno-19-31>)
    [](<https://adk.dev/sessions/state/#__codelineno-19-32>)    // Append the event to update the state
    [](<https://adk.dev/sessions/state/#__codelineno-19-33>)    if err := sessionService.AppendEvent(ctx, retrievedSession, systemEvent); err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-19-34>)        log.Fatalf("Failed to append event: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-19-35>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-19-36>)    fmt.Println("`append_event` called with explicit state delta.")
    [](<https://adk.dev/sessions/state/#__codelineno-19-37>)
    [](<https://adk.dev/sessions/state/#__codelineno-19-38>)    // Check the updated state
    [](<https://adk.dev/sessions/state/#__codelineno-19-39>)    updatedResp, err := sessionService.Get(ctx, &session.GetRequest{AppName: appName, UserID: userID, SessionID: sessionID})
    [](<https://adk.dev/sessions/state/#__codelineno-19-40>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-19-41>)        log.Fatalf("Failed to get session: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-19-42>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-19-43>)    taskStatus, _ := updatedResp.Session.State().Get("task_status")
    [](<https://adk.dev/sessions/state/#__codelineno-19-44>)    loginCount, _ = updatedResp.Session.State().Get("user:login_count")
    [](<https://adk.dev/sessions/state/#__codelineno-19-45>)    lastLogin, _ := updatedResp.Session.State().Get("user:last_login_ts")
    [](<https://adk.dev/sessions/state/#__codelineno-19-46>)    temp, err := updatedResp.Session.State().Get("temp:validation_needed") // This should fail or be nil
    [](<https://adk.dev/sessions/state/#__codelineno-19-47>)
    [](<https://adk.dev/sessions/state/#__codelineno-19-48>)    fmt.Printf("State after event: task_status=%q, user:login_count=%v, user:last_login_ts=%v\n", taskStatus, loginCount, lastLogin)
    [](<https://adk.dev/sessions/state/#__codelineno-19-49>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-19-50>)        fmt.Printf("As expected, temp state was not persisted: %v\n\n", err)
    [](<https://adk.dev/sessions/state/#__codelineno-19-51>)    } else {
    [](<https://adk.dev/sessions/state/#__codelineno-19-52>)        fmt.Printf("Unexpected temp state value: %v\n\n", temp)
    [](<https://adk.dev/sessions/state/#__codelineno-19-53>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-19-54>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-20-1>)import com.google.adk.events.Event;
    [](<https://adk.dev/sessions/state/#__codelineno-20-2>)import com.google.adk.events.EventActions;
    [](<https://adk.dev/sessions/state/#__codelineno-20-3>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/sessions/state/#__codelineno-20-4>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/sessions/state/#__codelineno-20-5>)import java.time.Instant;
    [](<https://adk.dev/sessions/state/#__codelineno-20-6>)import java.util.Optional;
    [](<https://adk.dev/sessions/state/#__codelineno-20-7>)import java.util.concurrent.ConcurrentHashMap;
    [](<https://adk.dev/sessions/state/#__codelineno-20-8>)import java.util.concurrent.ConcurrentMap;
    [](<https://adk.dev/sessions/state/#__codelineno-20-9>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-10>)public class ManualStateUpdateExample {
    [](<https://adk.dev/sessions/state/#__codelineno-20-11>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-12>)  public static void main(String[] args) {
    [](<https://adk.dev/sessions/state/#__codelineno-20-13>)    // --- Setup ---
    [](<https://adk.dev/sessions/state/#__codelineno-20-14>)    InMemorySessionService sessionService = new InMemorySessionService();
    [](<https://adk.dev/sessions/state/#__codelineno-20-15>)    String appName = "state_app_manual";
    [](<https://adk.dev/sessions/state/#__codelineno-20-16>)    String userId = "user2";
    [](<https://adk.dev/sessions/state/#__codelineno-20-17>)    String sessionId = "session2";
    [](<https://adk.dev/sessions/state/#__codelineno-20-18>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-19>)    ConcurrentMap<String, Object> initialState = new ConcurrentHashMap<>();
    [](<https://adk.dev/sessions/state/#__codelineno-20-20>)    initialState.put("user:login_count", 0);
    [](<https://adk.dev/sessions/state/#__codelineno-20-21>)    initialState.put("task_status", "idle");
    [](<https://adk.dev/sessions/state/#__codelineno-20-22>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-23>)    Session session =
    [](<https://adk.dev/sessions/state/#__codelineno-20-24>)        sessionService.createSession(appName, userId, initialState, sessionId).blockingGet();
    [](<https://adk.dev/sessions/state/#__codelineno-20-25>)    System.out.println("Initial state: " + session.state().entrySet());
    [](<https://adk.dev/sessions/state/#__codelineno-20-26>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-27>)    // --- Define State Changes ---
    [](<https://adk.dev/sessions/state/#__codelineno-20-28>)    long currentTimeMillis = Instant.now().toEpochMilli(); // Use milliseconds for Java Event
    [](<https://adk.dev/sessions/state/#__codelineno-20-29>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-30>)    ConcurrentMap<String, Object> stateChanges = new ConcurrentHashMap<>();
    [](<https://adk.dev/sessions/state/#__codelineno-20-31>)    stateChanges.put("task_status", "active"); // Update session state
    [](<https://adk.dev/sessions/state/#__codelineno-20-32>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-33>)    // Retrieve and increment login_count
    [](<https://adk.dev/sessions/state/#__codelineno-20-34>)    Object loginCountObj = session.state().get("user:login_count");
    [](<https://adk.dev/sessions/state/#__codelineno-20-35>)    int currentLoginCount = 0;
    [](<https://adk.dev/sessions/state/#__codelineno-20-36>)    if (loginCountObj instanceof Number) {
    [](<https://adk.dev/sessions/state/#__codelineno-20-37>)      currentLoginCount = ((Number) loginCountObj).intValue();
    [](<https://adk.dev/sessions/state/#__codelineno-20-38>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-20-39>)    stateChanges.put("user:login_count", currentLoginCount + 1); // Update user state
    [](<https://adk.dev/sessions/state/#__codelineno-20-40>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-41>)    stateChanges.put("user:last_login_ts", currentTimeMillis); // Add user state (as long milliseconds)
    [](<https://adk.dev/sessions/state/#__codelineno-20-42>)    stateChanges.put("temp:validation_needed", true); // Add temporary state
    [](<https://adk.dev/sessions/state/#__codelineno-20-43>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-44>)    // --- Create Event with Actions ---
    [](<https://adk.dev/sessions/state/#__codelineno-20-45>)    EventActions actionsWithUpdate = EventActions.builder().stateDelta(stateChanges).build();
    [](<https://adk.dev/sessions/state/#__codelineno-20-46>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-47>)    // This event might represent an internal system action, not just an agent response
    [](<https://adk.dev/sessions/state/#__codelineno-20-48>)    Event systemEvent =
    [](<https://adk.dev/sessions/state/#__codelineno-20-49>)        Event.builder()
    [](<https://adk.dev/sessions/state/#__codelineno-20-50>)            .invocationId("inv_login_update")
    [](<https://adk.dev/sessions/state/#__codelineno-20-51>)            .author("system") // Or 'agent', 'tool' etc.
    [](<https://adk.dev/sessions/state/#__codelineno-20-52>)            .actions(actionsWithUpdate)
    [](<https://adk.dev/sessions/state/#__codelineno-20-53>)            .timestamp(currentTimeMillis)
    [](<https://adk.dev/sessions/state/#__codelineno-20-54>)            // content might be None or represent the action taken
    [](<https://adk.dev/sessions/state/#__codelineno-20-55>)            .build();
    [](<https://adk.dev/sessions/state/#__codelineno-20-56>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-57>)    // --- Append the Event (This updates the state) ---
    [](<https://adk.dev/sessions/state/#__codelineno-20-58>)    sessionService.appendEvent(session, systemEvent).blockingGet();
    [](<https://adk.dev/sessions/state/#__codelineno-20-59>)    System.out.println("`appendEvent` called with explicit state delta.");
    [](<https://adk.dev/sessions/state/#__codelineno-20-60>)
    [](<https://adk.dev/sessions/state/#__codelineno-20-61>)    // --- Check Updated State ---
    [](<https://adk.dev/sessions/state/#__codelineno-20-62>)    Session updatedSession =
    [](<https://adk.dev/sessions/state/#__codelineno-20-63>)        sessionService.getSession(appName, userId, sessionId, Optional.empty()).blockingGet();
    [](<https://adk.dev/sessions/state/#__codelineno-20-64>)    assert updatedSession != null;
    [](<https://adk.dev/sessions/state/#__codelineno-20-65>)    System.out.println("State after event: " + updatedSession.state().entrySet());
    [](<https://adk.dev/sessions/state/#__codelineno-20-66>)    // Expected: {'user:login_count': 1, 'task_status': 'active', 'user:last_login_ts': <timestamp_millis>}
    [](<https://adk.dev/sessions/state/#__codelineno-20-67>)    // Note: 'temp:validation_needed' is NOT present because InMemorySessionService's appendEvent
    [](<https://adk.dev/sessions/state/#__codelineno-20-68>)    // applies delta to its internal user/app state maps IF keys have prefixes,
    [](<https://adk.dev/sessions/state/#__codelineno-20-69>)    // and to the session's own state map (which is then merged on getSession).
    [](<https://adk.dev/sessions/state/#__codelineno-20-70>)  }
    [](<https://adk.dev/sessions/state/#__codelineno-20-71>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-21-1>)fun main() =
    [](<https://adk.dev/sessions/state/#__codelineno-21-2>)    runBlocking {
    [](<https://adk.dev/sessions/state/#__codelineno-21-3>)        // --- Constants ---
    [](<https://adk.dev/sessions/state/#__codelineno-21-4>)        val appName = "state_example_app"
    [](<https://adk.dev/sessions/state/#__codelineno-21-5>)        val userId = "state_user"
    [](<https://adk.dev/sessions/state/#__codelineno-21-6>)        val model = Gemini(name = "gemini-flash-latest")
    [](<https://adk.dev/sessions/state/#__codelineno-21-7>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-8>)        // --- Services ---
    [](<https://adk.dev/sessions/state/#__codelineno-21-9>)        val sessionService = InMemorySessionService()
    [](<https://adk.dev/sessions/state/#__codelineno-21-10>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-11>)        // --- 1. Instruction Templating ---
    [](<https://adk.dev/sessions/state/#__codelineno-21-12>)        // Inject state values into agent instructions using {key} syntax.
    [](<https://adk.dev/sessions/state/#__codelineno-21-13>)        val templateAgent =
    [](<https://adk.dev/sessions/state/#__codelineno-21-14>)            LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-21-15>)                name = "TemplateAgent",
    [](<https://adk.dev/sessions/state/#__codelineno-21-16>)                model = model,
    [](<https://adk.dev/sessions/state/#__codelineno-21-17>)                instruction =
    [](<https://adk.dev/sessions/state/#__codelineno-21-18>)                    Instruction(
    [](<https://adk.dev/sessions/state/#__codelineno-21-19>)                        "Greet the user and mention their favorite color: {favorite_color}.",
    [](<https://adk.dev/sessions/state/#__codelineno-21-20>)                    ),
    [](<https://adk.dev/sessions/state/#__codelineno-21-21>)            )
    [](<https://adk.dev/sessions/state/#__codelineno-21-22>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-23>)        // --- 2. State Updates in Callbacks ---
    [](<https://adk.dev/sessions/state/#__codelineno-21-24>)        // Update state directly in a callback using context.updateState()
    [](<https://adk.dev/sessions/state/#__codelineno-21-25>)        val logTurnCallback =
    [](<https://adk.dev/sessions/state/#__codelineno-21-26>)            AfterAgentCallback { context ->
    [](<https://adk.dev/sessions/state/#__codelineno-21-27>)                val turnCount = context.state["turn_count"] as? Int ?: 0
    [](<https://adk.dev/sessions/state/#__codelineno-21-28>)                context.updateState("turn_count", turnCount + 1)
    [](<https://adk.dev/sessions/state/#__codelineno-21-29>)                println("Turn #$turnCount logged in callback.")
    [](<https://adk.dev/sessions/state/#__codelineno-21-30>)                CallbackChoice.Continue(Unit)
    [](<https://adk.dev/sessions/state/#__codelineno-21-31>)            }
    [](<https://adk.dev/sessions/state/#__codelineno-21-32>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-33>)        val callbackAgent =
    [](<https://adk.dev/sessions/state/#__codelineno-21-34>)            LlmAgent(
    [](<https://adk.dev/sessions/state/#__codelineno-21-35>)                name = "CallbackAgent",
    [](<https://adk.dev/sessions/state/#__codelineno-21-36>)                model = model,
    [](<https://adk.dev/sessions/state/#__codelineno-21-37>)                instruction = Instruction("Answer concisely."),
    [](<https://adk.dev/sessions/state/#__codelineno-21-38>)                afterAgentCallbacks = listOf(logTurnCallback),
    [](<https://adk.dev/sessions/state/#__codelineno-21-39>)            )
    [](<https://adk.dev/sessions/state/#__codelineno-21-40>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-41>)        // --- 3. Manual State Updates via EventActions ---
    [](<https://adk.dev/sessions/state/#__codelineno-21-42>)        println("--- Manual State Update ---")
    [](<https://adk.dev/sessions/state/#__codelineno-21-43>)        val sessionId = "manual_session"
    [](<https://adk.dev/sessions/state/#__codelineno-21-44>)        val sessionKey = SessionKey(appName, userId, sessionId)
    [](<https://adk.dev/sessions/state/#__codelineno-21-45>)        val session =
    [](<https://adk.dev/sessions/state/#__codelineno-21-46>)            sessionService.createSession(
    [](<https://adk.dev/sessions/state/#__codelineno-21-47>)                key = sessionKey,
    [](<https://adk.dev/sessions/state/#__codelineno-21-48>)                state = mapOf("favorite_color" to "blue", "turn_count" to 0),
    [](<https://adk.dev/sessions/state/#__codelineno-21-49>)            )
    [](<https://adk.dev/sessions/state/#__codelineno-21-50>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-51>)        val stateUpdateEvent =
    [](<https://adk.dev/sessions/state/#__codelineno-21-52>)            Event(
    [](<https://adk.dev/sessions/state/#__codelineno-21-53>)                invocationId = "manual_update",
    [](<https://adk.dev/sessions/state/#__codelineno-21-54>)                author = "system",
    [](<https://adk.dev/sessions/state/#__codelineno-21-55>)                actions =
    [](<https://adk.dev/sessions/state/#__codelineno-21-56>)                    EventActions(
    [](<https://adk.dev/sessions/state/#__codelineno-21-57>)                        stateDelta = mutableMapOf("user:preferred_language" to "en"),
    [](<https://adk.dev/sessions/state/#__codelineno-21-58>)                    ),
    [](<https://adk.dev/sessions/state/#__codelineno-21-59>)                timestamp = System.currentTimeMillis(),
    [](<https://adk.dev/sessions/state/#__codelineno-21-60>)            )
    [](<https://adk.dev/sessions/state/#__codelineno-21-61>)        val unused = sessionService.appendEvent(session, stateUpdateEvent)
    [](<https://adk.dev/sessions/state/#__codelineno-21-62>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-63>)        val updatedSession = sessionService.getSession(sessionKey)
    [](<https://adk.dev/sessions/state/#__codelineno-21-64>)        println("Updated State: ${updatedSession?.state}")
    [](<https://adk.dev/sessions/state/#__codelineno-21-65>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-66>)        // --- 4. Running with Templating ---
    [](<https://adk.dev/sessions/state/#__codelineno-21-67>)        println("\n--- Running with Templating ---")
    [](<https://adk.dev/sessions/state/#__codelineno-21-68>)        val runner =
    [](<https://adk.dev/sessions/state/#__codelineno-21-69>)            InMemoryRunner(
    [](<https://adk.dev/sessions/state/#__codelineno-21-70>)                agent = templateAgent,
    [](<https://adk.dev/sessions/state/#__codelineno-21-71>)                appName = appName,
    [](<https://adk.dev/sessions/state/#__codelineno-21-72>)                sessionService = sessionService,
    [](<https://adk.dev/sessions/state/#__codelineno-21-73>)            )
    [](<https://adk.dev/sessions/state/#__codelineno-21-74>)        val userMessage = Content.fromText(Role.USER, "Hello!")
    [](<https://adk.dev/sessions/state/#__codelineno-21-75>)
    [](<https://adk.dev/sessions/state/#__codelineno-21-76>)        runner.runAsync(
    [](<https://adk.dev/sessions/state/#__codelineno-21-77>)            userId = userId,
    [](<https://adk.dev/sessions/state/#__codelineno-21-78>)            sessionId = sessionId,
    [](<https://adk.dev/sessions/state/#__codelineno-21-79>)            newMessage = userMessage,
    [](<https://adk.dev/sessions/state/#__codelineno-21-80>)        ).collect { event ->
    [](<https://adk.dev/sessions/state/#__codelineno-21-81>)            event.content?.parts?.forEach { part ->
    [](<https://adk.dev/sessions/state/#__codelineno-21-82>)                if (!part.text.isNullOrBlank()) {
    [](<https://adk.dev/sessions/state/#__codelineno-21-83>)                    println("Agent Response: ${part.text}")
    [](<https://adk.dev/sessions/state/#__codelineno-21-84>)                }
    [](<https://adk.dev/sessions/state/#__codelineno-21-85>)            }
    [](<https://adk.dev/sessions/state/#__codelineno-21-86>)        }
    [](<https://adk.dev/sessions/state/#__codelineno-21-87>)    }
    
**3\. Via`CallbackContext` or `ToolContext` (Recommended for Callbacks and Tools)**

_(Note: In TypeScript, this is done via the unified`Context` type.)_

Modifying state within agent callbacks (e.g., `on_before_agent_call`, `on_after_agent_call`) or tool functions is best done using the `state` attribute of the `CallbackContext` or `ToolContext` provided to your function.

  * `callback_context.state['my_key'] = my_value`
  * `tool_context.state['my_key'] = my_value`

These context objects are specifically designed to manage state changes within their respective execution scopes. When you modify `context.state`, the ADK framework ensures that these changes are automatically captured and correctly routed into the `EventActions.state_delta` for the event being generated by the callback or tool. This delta is then processed by the `SessionService` when the event is appended, ensuring proper persistence and tracking.

This method abstracts away the manual creation of `EventActions` and `state_delta` for most common state update scenarios within callbacks and tools, making your code cleaner and less error-prone.

For more comprehensive details on context objects, refer to the [Context documentation](<https://adk.dev/context/>).

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/state/#__codelineno-22-1>)# In an agent callback or tool function
    [](<https://adk.dev/sessions/state/#__codelineno-22-2>)from google.adk.agents import CallbackContext # or ToolContext
    [](<https://adk.dev/sessions/state/#__codelineno-22-3>)
    [](<https://adk.dev/sessions/state/#__codelineno-22-4>)def my_callback_or_tool_function(context: CallbackContext, # Or ToolContext
    [](<https://adk.dev/sessions/state/#__codelineno-22-5>)                                 # ... other parameters ...
    [](<https://adk.dev/sessions/state/#__codelineno-22-6>)                                ):
    [](<https://adk.dev/sessions/state/#__codelineno-22-7>)    # Update existing state
    [](<https://adk.dev/sessions/state/#__codelineno-22-8>)    count = context.state.get("user_action_count", 0)
    [](<https://adk.dev/sessions/state/#__codelineno-22-9>)    context.state["user_action_count"] = count + 1
    [](<https://adk.dev/sessions/state/#__codelineno-22-10>)
    [](<https://adk.dev/sessions/state/#__codelineno-22-11>)    # Add new state
    [](<https://adk.dev/sessions/state/#__codelineno-22-12>)    context.state["temp:last_operation_status"] = "success"
    [](<https://adk.dev/sessions/state/#__codelineno-22-13>)
    [](<https://adk.dev/sessions/state/#__codelineno-22-14>)    # State changes are automatically part of the event's state_delta
    [](<https://adk.dev/sessions/state/#__codelineno-22-15>)    # ... rest of callback/tool logic ...
    
    [](<https://adk.dev/sessions/state/#__codelineno-23-1>)// In an agent callback or tool function
    [](<https://adk.dev/sessions/state/#__codelineno-23-2>)import { Context } from "@google/adk";
    [](<https://adk.dev/sessions/state/#__codelineno-23-3>)
    [](<https://adk.dev/sessions/state/#__codelineno-23-4>)function myCallbackOrToolFunction(
    [](<https://adk.dev/sessions/state/#__codelineno-23-5>)    context: Context,
    [](<https://adk.dev/sessions/state/#__codelineno-23-6>)    // ... other parameters ...
    [](<https://adk.dev/sessions/state/#__codelineno-23-7>)) {
    [](<https://adk.dev/sessions/state/#__codelineno-23-8>)    // Update existing state
    [](<https://adk.dev/sessions/state/#__codelineno-23-9>)    const count = context.state.get("user_action_count", 0);
    [](<https://adk.dev/sessions/state/#__codelineno-23-10>)    context.state.set("user_action_count", count + 1);
    [](<https://adk.dev/sessions/state/#__codelineno-23-11>)
    [](<https://adk.dev/sessions/state/#__codelineno-23-12>)    // Add new state
    [](<https://adk.dev/sessions/state/#__codelineno-23-13>)    context.state.set("temp:last_operation_status", "success");
    [](<https://adk.dev/sessions/state/#__codelineno-23-14>)
    [](<https://adk.dev/sessions/state/#__codelineno-23-15>)    // State changes are automatically part of the event's stateDelta
    [](<https://adk.dev/sessions/state/#__codelineno-23-16>)    // ... rest of callback/tool logic ...
    [](<https://adk.dev/sessions/state/#__codelineno-23-17>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-24-1>)//  3. contextStateUpdateExample demonstrates the recommended way to modify state
    [](<https://adk.dev/sessions/state/#__codelineno-24-2>)//     from within a tool function using the provided `agent.Context`.
    [](<https://adk.dev/sessions/state/#__codelineno-24-3>)func contextStateUpdateExample(sessionService session.Service) {
    [](<https://adk.dev/sessions/state/#__codelineno-24-4>)    fmt.Println("--- Running Context State Update (ToolContext) Example ---")
    [](<https://adk.dev/sessions/state/#__codelineno-24-5>)    ctx := context.Background()
    [](<https://adk.dev/sessions/state/#__codelineno-24-6>)
    [](<https://adk.dev/sessions/state/#__codelineno-24-7>)    // Define the tool that modifies state
    [](<https://adk.dev/sessions/state/#__codelineno-24-8>)    updateActionCountTool, err := functiontool.New(
    [](<https://adk.dev/sessions/state/#__codelineno-24-9>)        functiontool.Config{Name: "update_action_count", Description: "Updates the user action count in the state."},
    [](<https://adk.dev/sessions/state/#__codelineno-24-10>)        func(actx agent.Context, args struct{}) (struct{}, error) {
    [](<https://adk.dev/sessions/state/#__codelineno-24-11>)            s, err := actx.State().Get("user_action_count")
    [](<https://adk.dev/sessions/state/#__codelineno-24-12>)            if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-13>)                log.Printf("could not get user_action_count: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-14>)            }
    [](<https://adk.dev/sessions/state/#__codelineno-24-15>)            newCount := 1
    [](<https://adk.dev/sessions/state/#__codelineno-24-16>)            if c, ok := s.(int); ok {
    [](<https://adk.dev/sessions/state/#__codelineno-24-17>)                newCount = c + 1
    [](<https://adk.dev/sessions/state/#__codelineno-24-18>)            }
    [](<https://adk.dev/sessions/state/#__codelineno-24-19>)            if err := actx.State().Set("user_action_count", newCount); err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-20>)                log.Printf("could not set user_action_count: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-21>)            }
    [](<https://adk.dev/sessions/state/#__codelineno-24-22>)            if err := actx.State().Set("temp:last_operation_status", "success from tool"); err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-23>)                log.Printf("could not set temp:last_operation_status: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-24>)            }
    [](<https://adk.dev/sessions/state/#__codelineno-24-25>)            fmt.Println("Tool: Updated state via agent.Context.")
    [](<https://adk.dev/sessions/state/#__codelineno-24-26>)            return struct{}{}, nil
    [](<https://adk.dev/sessions/state/#__codelineno-24-27>)        },
    [](<https://adk.dev/sessions/state/#__codelineno-24-28>)    )
    [](<https://adk.dev/sessions/state/#__codelineno-24-29>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-30>)        log.Fatalf("Failed to create tool: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-31>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-24-32>)
    [](<https://adk.dev/sessions/state/#__codelineno-24-33>)    // Define an agent that uses the tool
    [](<https://adk.dev/sessions/state/#__codelineno-24-34>)    modelTool, err := gemini.NewModel(ctx, modelID, nil)
    [](<https://adk.dev/sessions/state/#__codelineno-24-35>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-36>)        log.Fatalf("Failed to create Gemini model for tool agent: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-37>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-24-38>)    toolAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/sessions/state/#__codelineno-24-39>)        Name:        "ToolAgent",
    [](<https://adk.dev/sessions/state/#__codelineno-24-40>)        Model:       modelTool,
    [](<https://adk.dev/sessions/state/#__codelineno-24-41>)        Instruction: "Use the update_action_count tool.",
    [](<https://adk.dev/sessions/state/#__codelineno-24-42>)        Tools:       []tool.Tool{updateActionCountTool},
    [](<https://adk.dev/sessions/state/#__codelineno-24-43>)    })
    [](<https://adk.dev/sessions/state/#__codelineno-24-44>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-45>)        log.Fatalf("Failed to create tool agent: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-46>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-24-47>)
    [](<https://adk.dev/sessions/state/#__codelineno-24-48>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/sessions/state/#__codelineno-24-49>)        AppName:        appName,
    [](<https://adk.dev/sessions/state/#__codelineno-24-50>)        Agent:          agent.Agent(toolAgent),
    [](<https://adk.dev/sessions/state/#__codelineno-24-51>)        SessionService: sessionService,
    [](<https://adk.dev/sessions/state/#__codelineno-24-52>)    })
    [](<https://adk.dev/sessions/state/#__codelineno-24-53>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-54>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-55>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-24-56>)
    [](<https://adk.dev/sessions/state/#__codelineno-24-57>)    // Run the agent to trigger the tool
    [](<https://adk.dev/sessions/state/#__codelineno-24-58>)    userMessage := genai.NewContentFromText("Please update the action count.", "user")
    [](<https://adk.dev/sessions/state/#__codelineno-24-59>)    for _, err := range r.Run(ctx, userID, sessionID, userMessage, agent.RunConfig{}) {
    [](<https://adk.dev/sessions/state/#__codelineno-24-60>)        if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-61>)            log.Printf("Agent Error: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-62>)        }
    [](<https://adk.dev/sessions/state/#__codelineno-24-63>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-24-64>)
    [](<https://adk.dev/sessions/state/#__codelineno-24-65>)    // Check the updated state
    [](<https://adk.dev/sessions/state/#__codelineno-24-66>)    resp, err := sessionService.Get(ctx, &session.GetRequest{AppName: appName, UserID: userID, SessionID: sessionID})
    [](<https://adk.dev/sessions/state/#__codelineno-24-67>)    if err != nil {
    [](<https://adk.dev/sessions/state/#__codelineno-24-68>)        log.Fatalf("Failed to get session: %v", err)
    [](<https://adk.dev/sessions/state/#__codelineno-24-69>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-24-70>)    actionCount, _ := resp.Session.State().Get("user_action_count")
    [](<https://adk.dev/sessions/state/#__codelineno-24-71>)    fmt.Printf("State after tool run: user_action_count = %v\n", actionCount)
    [](<https://adk.dev/sessions/state/#__codelineno-24-72>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-25-1>)// In an agent callback or tool method
    [](<https://adk.dev/sessions/state/#__codelineno-25-2>)import com.google.adk.agents.CallbackContext; // or ToolContext
    [](<https://adk.dev/sessions/state/#__codelineno-25-3>)// ... other imports ...
    [](<https://adk.dev/sessions/state/#__codelineno-25-4>)
    [](<https://adk.dev/sessions/state/#__codelineno-25-5>)public class MyAgentCallbacks {
    [](<https://adk.dev/sessions/state/#__codelineno-25-6>)    public void onAfterAgent(CallbackContext callbackContext) {
    [](<https://adk.dev/sessions/state/#__codelineno-25-7>)        // Update existing state
    [](<https://adk.dev/sessions/state/#__codelineno-25-8>)        Integer count = (Integer) callbackContext.state().getOrDefault("user_action_count", 0);
    [](<https://adk.dev/sessions/state/#__codelineno-25-9>)        callbackContext.state().put("user_action_count", count + 1);
    [](<https://adk.dev/sessions/state/#__codelineno-25-10>)
    [](<https://adk.dev/sessions/state/#__codelineno-25-11>)        // Add new state
    [](<https://adk.dev/sessions/state/#__codelineno-25-12>)        callbackContext.state().put("temp:last_operation_status", "success");
    [](<https://adk.dev/sessions/state/#__codelineno-25-13>)
    [](<https://adk.dev/sessions/state/#__codelineno-25-14>)        // State changes are automatically part of the event's state_delta
    [](<https://adk.dev/sessions/state/#__codelineno-25-15>)        // ... rest of callback logic ...
    [](<https://adk.dev/sessions/state/#__codelineno-25-16>)    }
    [](<https://adk.dev/sessions/state/#__codelineno-25-17>)}
    
    [](<https://adk.dev/sessions/state/#__codelineno-26-1>)fun myCallbackFunction(context: CallbackContext) {
    [](<https://adk.dev/sessions/state/#__codelineno-26-2>)    // Update existing state using updateState helper
    [](<https://adk.dev/sessions/state/#__codelineno-26-3>)    val count = context.state["user_action_count"] as? Int ?: 0
    [](<https://adk.dev/sessions/state/#__codelineno-26-4>)    context.updateState("user_action_count", count + 1)
    [](<https://adk.dev/sessions/state/#__codelineno-26-5>)
    [](<https://adk.dev/sessions/state/#__codelineno-26-6>)    // Add new state
    [](<https://adk.dev/sessions/state/#__codelineno-26-7>)    context.updateState("temp:last_operation_status", "success")
    [](<https://adk.dev/sessions/state/#__codelineno-26-8>)}
    [](<https://adk.dev/sessions/state/#__codelineno-26-9>)
    [](<https://adk.dev/sessions/state/#__codelineno-26-10>)suspend fun myToolFunction(
    [](<https://adk.dev/sessions/state/#__codelineno-26-11>)    context: ToolContext,
    [](<https://adk.dev/sessions/state/#__codelineno-26-12>)    args: Map<String, Any>,
    [](<https://adk.dev/sessions/state/#__codelineno-26-13>)) {
    [](<https://adk.dev/sessions/state/#__codelineno-26-14>)    // Access state via context.context.state
    [](<https://adk.dev/sessions/state/#__codelineno-26-15>)    val count = context.context.state["user_action_count"] as? Int ?: 0
    [](<https://adk.dev/sessions/state/#__codelineno-26-16>)
    [](<https://adk.dev/sessions/state/#__codelineno-26-17>)    // Update state via context.actions.stateDelta
    [](<https://adk.dev/sessions/state/#__codelineno-26-18>)    context.actions.stateDelta["user_action_count"] = count + 1
    [](<https://adk.dev/sessions/state/#__codelineno-26-19>)    context.actions.stateDelta["temp:last_operation_status"] = "success"
    [](<https://adk.dev/sessions/state/#__codelineno-26-20>)}
    
**What`append_event` Does:**

  * Adds the `Event` to `session.events`.
  * Reads the `state_delta` from the event's `actions`.
  * Applies these changes to the state managed by the `SessionService`, correctly handling prefixes and persistence based on the service type.
  * Updates the session's `last_update_time`.
  * Ensures thread-safety for concurrent updates.

### ⚠️ A Warning About Direct State Modification[¶](<https://adk.dev/sessions/state/#a-warning-about-direct-state-modification> "Permanent link")

Avoid directly modifying the `session.state` collection (dictionary/Map) on a `Session` object that was obtained directly from the `SessionService` (e.g., via `session_service.get_session()` or `session_service.create_session()`) _outside_ of the managed lifecycle of an agent invocation (i.e., not through a `CallbackContext` or `ToolContext`). For example, code like `retrieved_session = await session_service.get_session(...); retrieved_session.state['key'] = value` is problematic.

State modifications _within_ callbacks or tools using `CallbackContext.state` or `ToolContext.state` are the correct way to ensure changes are tracked, as these context objects handle the necessary integration with the event system.

**Why direct modification (outside of contexts) is strongly discouraged:**

  1. **Bypasses Event History:** The change isn't recorded as an `Event`, losing auditability.
  2. **Breaks Persistence:** Changes made this way **will likely NOT be saved** by `DatabaseSessionService` or `VertexAiSessionService`. They rely on `append_event` to trigger saving.
  3. **Not Thread-Safe:** Can lead to race conditions and lost updates.
  4. **Ignores Timestamps/Logic:** Doesn't update `last_update_time` or trigger related event logic.

**Recommendation:** Stick to updating state via `output_key`, `EventActions.state_delta` (when manually creating events), or by modifying the `state` property of `CallbackContext` or `ToolContext` objects when within their respective scopes. These methods ensure reliable, trackable, and persistent state management. Use direct access to `session.state` (from a `SessionService`-retrieved session) only for _reading_ state.

### Best Practices for State Design Recap[¶](<https://adk.dev/sessions/state/#best-practices-for-state-design-recap> "Permanent link")

  * **Minimalism:** Store only essential, dynamic data.
  * **Serialization:** Use basic, serializable types.
  * **Descriptive Keys & Prefixes:** Use clear names and appropriate prefixes (`user:`, `app:`, `temp:`, or none).
  * **Shallow Structures:** Avoid deep nesting where possible.
  * **Standard Update Flow:** Rely on `append_event`.

Back to top 