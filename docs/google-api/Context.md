# Agent context - Agent Development Kit (ADK)

> Source: [https://adk.dev/context/](https://adk.dev/context/)

[ Skip to content ](<https://adk.dev/context/#agent-context>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/context/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/context/index.md> "View this page as Markdown")

# Agent context[¶](<https://adk.dev/context/#agent-context> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0

In the Agent Development Kit (ADK), _context_ refers to the crucial bundle of information available to your agent and its tools during specific operations. Think of it as the necessary background knowledge and resources needed to handle a current task or conversation turn effectively.

Agents often need more than just the latest user message to perform well. Context is essential because it enables:

  1. **Maintaining State:** Remembering details across multiple steps in a conversation (e.g., user preferences, previous calculations, items in a shopping cart). This is primarily managed through **session state**.
  2. **Passing Data:** Sharing information discovered or generated in one step (like an LLM call or a tool execution) with subsequent steps. Session state is key here too.
  3. **Accessing Services:** Interacting with framework capabilities like:
     * **Artifact Storage:** Saving or loading files or data blobs (like PDFs, images, configuration files) associated with the session.
     * **Memory:** Searching for relevant information from past interactions or external knowledge sources connected to the user.
     * **Authentication:** Requesting and retrieving credentials needed by tools to access external APIs securely.
  4. **Identity and Tracking:** Knowing which agent is currently running (`agent.name`) and uniquely identifying the current request-response cycle (`invocation_id`) for logging and debugging.
  5. **Tool-Specific Actions:** Enabling specialized operations within tools, such as requesting authentication or searching memory, which require access to the current interaction's details.

The central piece holding all this information together for a single, complete user-request-to-final-response cycle (an **invocation**) is the `InvocationContext`. However, you typically won't create or manage this object directly. The ADK framework creates it when an invocation starts (e.g., via `runner.run_async`) and passes the relevant contextual information implicitly to your agent code, callbacks, and tools.

PythonTypeScriptGoJava
    
    [](<https://adk.dev/context/#__codelineno-0-1>)# How the framework provides context
    [](<https://adk.dev/context/#__codelineno-0-2>)from google.adk import Runner
    [](<https://adk.dev/context/#__codelineno-0-3>)
    [](<https://adk.dev/context/#__codelineno-0-4>)# 1. You initialize a Runner with your agent and services
    [](<https://adk.dev/context/#__codelineno-0-5>)runner = Runner(
    [](<https://adk.dev/context/#__codelineno-0-6>)    app_name="my_app",
    [](<https://adk.dev/context/#__codelineno-0-7>)    agent=my_root_agent,
    [](<https://adk.dev/context/#__codelineno-0-8>)    session_service=my_session_service,
    [](<https://adk.dev/context/#__codelineno-0-9>)    artifact_service=my_artifact_service,
    [](<https://adk.dev/context/#__codelineno-0-10>))
    [](<https://adk.dev/context/#__codelineno-0-11>)
    [](<https://adk.dev/context/#__codelineno-0-12>)# 2. You call run_async with the user input
    [](<https://adk.dev/context/#__codelineno-0-13>)# Note: run_async is an asynchronous generator yielding Events.
    [](<https://adk.dev/context/#__codelineno-0-14>)# The framework internally creates an InvocationContext and passes it
    [](<https://adk.dev/context/#__codelineno-0-15>)# implicitly to your agent code, callbacks, and tools.
    [](<https://adk.dev/context/#__codelineno-0-16>)async for event in runner.run_async(
    [](<https://adk.dev/context/#__codelineno-0-17>)    user_id="user123",
    [](<https://adk.dev/context/#__codelineno-0-18>)    session_id="session456",
    [](<https://adk.dev/context/#__codelineno-0-19>)    new_message=user_message
    [](<https://adk.dev/context/#__codelineno-0-20>)):
    [](<https://adk.dev/context/#__codelineno-0-21>)    print(event.stringify_content())
    [](<https://adk.dev/context/#__codelineno-0-22>)
    [](<https://adk.dev/context/#__codelineno-0-23>)# As a developer, you work with the context objects provided in method arguments.
    
    [](<https://adk.dev/context/#__codelineno-1-1>)/* Conceptual Pseudocode: How the framework provides context (Internal Logic) */
    [](<https://adk.dev/context/#__codelineno-1-2>)
    [](<https://adk.dev/context/#__codelineno-1-3>)const runner = new InMemoryRunner({ agent: myRootAgent });
    [](<https://adk.dev/context/#__codelineno-1-4>)const session = await runner.sessionService.createSession({ ... });
    [](<https://adk.dev/context/#__codelineno-1-5>)const userMessage = createUserContent(...);
    [](<https://adk.dev/context/#__codelineno-1-6>)
    [](<https://adk.dev/context/#__codelineno-1-7>)// --- Inside runner.runAsync(...) ---
    [](<https://adk.dev/context/#__codelineno-1-8>)// 1. Framework creates the main context for this specific run
    [](<https://adk.dev/context/#__codelineno-1-9>)const invocationContext = new InvocationContext({
    [](<https://adk.dev/context/#__codelineno-1-10>)  invocationId: "unique-id-for-this-run",
    [](<https://adk.dev/context/#__codelineno-1-11>)  session: session,
    [](<https://adk.dev/context/#__codelineno-1-12>)  userContent: userMessage,
    [](<https://adk.dev/context/#__codelineno-1-13>)  agent: myRootAgent, // The starting agent
    [](<https://adk.dev/context/#__codelineno-1-14>)  sessionService: runner.sessionService,
    [](<https://adk.dev/context/#__codelineno-1-15>)  pluginManager: runner.pluginManager,
    [](<https://adk.dev/context/#__codelineno-1-16>)  // ... other necessary fields ...
    [](<https://adk.dev/context/#__codelineno-1-17>)});
    [](<https://adk.dev/context/#__codelineno-1-18>)//
    [](<https://adk.dev/context/#__codelineno-1-19>)// 2. Framework calls the agent's run method, passing the context implicitly
    [](<https://adk.dev/context/#__codelineno-1-20>)await myRootAgent.runAsync(invocationContext);
    [](<https://adk.dev/context/#__codelineno-1-21>)//   --- End Internal Logic ---
    [](<https://adk.dev/context/#__codelineno-1-22>)
    [](<https://adk.dev/context/#__codelineno-1-23>)// As a developer, you work with the context objects provided in method arguments.
    
    [](<https://adk.dev/context/#__codelineno-2-1>)/* Conceptual Pseudocode: How the framework provides context (Internal Logic) */
    [](<https://adk.dev/context/#__codelineno-2-2>)sessionService := session.InMemoryService()
    [](<https://adk.dev/context/#__codelineno-2-3>)
    [](<https://adk.dev/context/#__codelineno-2-4>)r, err := runner.New(runner.Config{
    [](<https://adk.dev/context/#__codelineno-2-5>)    AppName:        appName,
    [](<https://adk.dev/context/#__codelineno-2-6>)    Agent:          myAgent,
    [](<https://adk.dev/context/#__codelineno-2-7>)    SessionService: sessionService,
    [](<https://adk.dev/context/#__codelineno-2-8>)})
    [](<https://adk.dev/context/#__codelineno-2-9>)if err != nil {
    [](<https://adk.dev/context/#__codelineno-2-10>)    log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/context/#__codelineno-2-11>)}
    [](<https://adk.dev/context/#__codelineno-2-12>)
    [](<https://adk.dev/context/#__codelineno-2-13>)s, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/context/#__codelineno-2-14>)    AppName: appName,
    [](<https://adk.dev/context/#__codelineno-2-15>)    UserID:  userID,
    [](<https://adk.dev/context/#__codelineno-2-16>)})
    [](<https://adk.dev/context/#__codelineno-2-17>)if err != nil {
    [](<https://adk.dev/context/#__codelineno-2-18>)    log.Fatalf("FATAL: Failed to create session: %v", err)
    [](<https://adk.dev/context/#__codelineno-2-19>)}
    [](<https://adk.dev/context/#__codelineno-2-20>)
    [](<https://adk.dev/context/#__codelineno-2-21>)scanner := bufio.NewScanner(os.Stdin)
    [](<https://adk.dev/context/#__codelineno-2-22>)for {
    [](<https://adk.dev/context/#__codelineno-2-23>)    fmt.Print("\nYou > ")
    [](<https://adk.dev/context/#__codelineno-2-24>)    if !scanner.Scan() {
    [](<https://adk.dev/context/#__codelineno-2-25>)        break
    [](<https://adk.dev/context/#__codelineno-2-26>)    }
    [](<https://adk.dev/context/#__codelineno-2-27>)    userInput := scanner.Text()
    [](<https://adk.dev/context/#__codelineno-2-28>)    if strings.EqualFold(userInput, "quit") {
    [](<https://adk.dev/context/#__codelineno-2-29>)        break
    [](<https://adk.dev/context/#__codelineno-2-30>)    }
    [](<https://adk.dev/context/#__codelineno-2-31>)    userMsg := genai.NewContentFromText(userInput, genai.RoleUser)
    [](<https://adk.dev/context/#__codelineno-2-32>)    events := r.Run(ctx, s.Session.UserID(), s.Session.ID(), userMsg, agent.RunConfig{
    [](<https://adk.dev/context/#__codelineno-2-33>)        StreamingMode: agent.StreamingModeNone,
    [](<https://adk.dev/context/#__codelineno-2-34>)    })
    [](<https://adk.dev/context/#__codelineno-2-35>)    fmt.Print("\nAgent > ")
    [](<https://adk.dev/context/#__codelineno-2-36>)    for event, err := range events {
    [](<https://adk.dev/context/#__codelineno-2-37>)        if err != nil {
    [](<https://adk.dev/context/#__codelineno-2-38>)            log.Printf("ERROR during agent execution: %v", err)
    [](<https://adk.dev/context/#__codelineno-2-39>)            break
    [](<https://adk.dev/context/#__codelineno-2-40>)        }
    [](<https://adk.dev/context/#__codelineno-2-41>)        if event != nil && event.Content != nil && len(event.Content.Parts) > 0 {
    [](<https://adk.dev/context/#__codelineno-2-42>)            fmt.Print(event.Content.Parts[0].Text)
    [](<https://adk.dev/context/#__codelineno-2-43>)        }
    [](<https://adk.dev/context/#__codelineno-2-44>)    }
    [](<https://adk.dev/context/#__codelineno-2-45>)}
    
    [](<https://adk.dev/context/#__codelineno-3-1>)/* How the framework provides context */
    [](<https://adk.dev/context/#__codelineno-3-2>)InMemoryRunner runner = new InMemoryRunner(agent);
    [](<https://adk.dev/context/#__codelineno-3-3>)Session session = runner
    [](<https://adk.dev/context/#__codelineno-3-4>)    .sessionService()
    [](<https://adk.dev/context/#__codelineno-3-5>)    .createSession(runner.appName(), USER_ID, initialState, SESSION_ID )
    [](<https://adk.dev/context/#__codelineno-3-6>)    .blockingGet();
    [](<https://adk.dev/context/#__codelineno-3-7>)
    [](<https://adk.dev/context/#__codelineno-3-8>)try (Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8)) {
    [](<https://adk.dev/context/#__codelineno-3-9>)  while (true) {
    [](<https://adk.dev/context/#__codelineno-3-10>)    System.out.print("\nYou > ");
    [](<https://adk.dev/context/#__codelineno-3-11>)    String userInput = scanner.nextLine();
    [](<https://adk.dev/context/#__codelineno-3-12>)    if ("quit".equalsIgnoreCase(userInput)) {
    [](<https://adk.dev/context/#__codelineno-3-13>)      break;
    [](<https://adk.dev/context/#__codelineno-3-14>)    }
    [](<https://adk.dev/context/#__codelineno-3-15>)    Content userMsg = Content.fromParts(Part.fromText(userInput));
    [](<https://adk.dev/context/#__codelineno-3-16>)    Flowable<Event> events = runner.runAsync(session.userId(), session.id(), userMsg);
    [](<https://adk.dev/context/#__codelineno-3-17>)    System.out.print("\nAgent > ");
    [](<https://adk.dev/context/#__codelineno-3-18>)    events.blockingForEach(event -> System.out.print(event.stringifyContent()));
    [](<https://adk.dev/context/#__codelineno-3-19>)  }
    [](<https://adk.dev/context/#__codelineno-3-20>)}
    
## Types of context[¶](<https://adk.dev/context/#types-of-context> "Permanent link")

ADK uses the `Context` class as the central mechanism to manage an agent's environment, state, and resources. While `Context` serves as the foundational base for all agent interactions, it manifests in specialized "flavors" designed to provide the right balance of capabilities and permissions depending on where they are used in the agent's execution flow. If you use these specific context types, ADK ensures that your agent has access to necessary information, such as memory, session state, or credentials, exactly when and where you need them. Here are the primary context flavors you will encounter:

  * **`InvocationContext`** : Used during core agent runs (`_run_async_impl`, `_run_live_impl`) to provide a comprehensive view of the entire invocation, including service references and lifecycle management.

  * **`ReadonlyContext`** : A lightweight, restricted view of fundamental contextual details used in scenarios where mutation is disallowed, such as within instruction providers.

  * **`Context`** : Used in agent lifecycle and model callbacks. It provides a robust set of features for reading/writing session state, managing artifacts, and injecting data into the memory service.

  * **`ToolContext`** : Tailored for tool execution and tool-related callbacks. In addition to the capabilities of Context, it includes specialized methods for authentication flows, memory searching, and artifact discovery.

Note

**About compatibility** : In Python and TypeScript, `CallbackContext` and `ToolContext` have been replaced by the `Context` type. The `CallbackContext` class is maintained as an alias for `Context` to ensure backward compatibility. While you may encounter `CallbackContext` in existing codebases, **you should use the`Context` class** for all new development to take advantage of the full, unified feature set.

### `InvocationContext`[¶](<https://adk.dev/context/#invocationcontext> "Permanent link")

  * **Where Used:** Received as the `ctx` argument directly within an agent's core implementation methods (`_run_async_impl`, `_run_live_impl`).
  * **Purpose:** Provides access to the entire state of the current invocation. This is the most comprehensive context object.
  * **Key Contents:** Direct access to `session` (including `state` and `events`), the current `agent` instance, `invocation_id`, initial `user_content`, references to configured services (`artifact_service`, `memory_service`, `session_service`), and fields related to live/streaming modes.
  * **Use Case:** Primarily used when the agent's core logic needs direct access to the overall session or services, though often state and artifact interactions are delegated to callbacks/tools which use their own contexts. Also used to control the invocation itself (e.g., setting `ctx.end_invocation = True`).

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-4-1>)# Agent implementation receiving InvocationContext
        [](<https://adk.dev/context/#__codelineno-4-2>)from google.adk.agents import BaseAgent
        [](<https://adk.dev/context/#__codelineno-4-3>)from google.adk.agents.invocation_context import InvocationContext
        [](<https://adk.dev/context/#__codelineno-4-4>)from google.adk.events import Event
        [](<https://adk.dev/context/#__codelineno-4-5>)from typing import AsyncGenerator
        [](<https://adk.dev/context/#__codelineno-4-6>)
        [](<https://adk.dev/context/#__codelineno-4-7>)class MyAgent(BaseAgent):
        [](<https://adk.dev/context/#__codelineno-4-8>)    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        [](<https://adk.dev/context/#__codelineno-4-9>)        # Direct access example
        [](<https://adk.dev/context/#__codelineno-4-10>)        agent_name = ctx.agent.name
        [](<https://adk.dev/context/#__codelineno-4-11>)        session_id = ctx.session.id
        [](<https://adk.dev/context/#__codelineno-4-12>)        print(f"Agent {agent_name} running in session {session_id} for invocation {ctx.invocation_id}")
        [](<https://adk.dev/context/#__codelineno-4-13>)        # ... agent logic using ctx ...
        [](<https://adk.dev/context/#__codelineno-4-14>)        yield # ... event ...
        
        [](<https://adk.dev/context/#__codelineno-5-1>)// Pseudocode: Agent implementation receiving InvocationContext
        [](<https://adk.dev/context/#__codelineno-5-2>)import { BaseAgent, InvocationContext, Event } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-5-3>)
        [](<https://adk.dev/context/#__codelineno-5-4>)class MyAgent extends BaseAgent {
        [](<https://adk.dev/context/#__codelineno-5-5>)  async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined> {
        [](<https://adk.dev/context/#__codelineno-5-6>)    // Direct access example
        [](<https://adk.dev/context/#__codelineno-5-7>)    const agentName = ctx.agent.name;
        [](<https://adk.dev/context/#__codelineno-5-8>)    const sessionId = ctx.session.id;
        [](<https://adk.dev/context/#__codelineno-5-9>)    console.log(`Agent ${agentName} running in session ${sessionId} for invocation ${ctx.invocationId}`);
        [](<https://adk.dev/context/#__codelineno-5-10>)    // ... agent logic using ctx ...
        [](<https://adk.dev/context/#__codelineno-5-11>)    yield; // ... event ...
        [](<https://adk.dev/context/#__codelineno-5-12>)  }
        [](<https://adk.dev/context/#__codelineno-5-13>)}
        
        [](<https://adk.dev/context/#__codelineno-6-1>)import (
        [](<https://adk.dev/context/#__codelineno-6-2>)    "google.golang.org/adk/v2/agent"
        [](<https://adk.dev/context/#__codelineno-6-3>)    "google.golang.org/adk/v2/session"
        [](<https://adk.dev/context/#__codelineno-6-4>))
        [](<https://adk.dev/context/#__codelineno-6-5>)
        [](<https://adk.dev/context/#__codelineno-6-6>)// Pseudocode: Agent implementation receiving InvocationContext
        [](<https://adk.dev/context/#__codelineno-6-7>)type MyAgent struct {
        [](<https://adk.dev/context/#__codelineno-6-8>)}
        [](<https://adk.dev/context/#__codelineno-6-9>)
        [](<https://adk.dev/context/#__codelineno-6-10>)func (a *MyAgent) Run(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
        [](<https://adk.dev/context/#__codelineno-6-11>)    return func(yield func(*session.Event, error) bool) {
        [](<https://adk.dev/context/#__codelineno-6-12>)        // Direct access example
        [](<https://adk.dev/context/#__codelineno-6-13>)        agentName := ctx.Agent().Name()
        [](<https://adk.dev/context/#__codelineno-6-14>)        sessionID := ctx.Session().ID()
        [](<https://adk.dev/context/#__codelineno-6-15>)        fmt.Printf("Agent %s running in session %s for invocation %s\n", agentName, sessionID, ctx.InvocationID())
        [](<https://adk.dev/context/#__codelineno-6-16>)        // ... agent logic using ctx ...
        [](<https://adk.dev/context/#__codelineno-6-17>)        yield(&session.Event{Author: agentName}, nil)
        [](<https://adk.dev/context/#__codelineno-6-18>)    }
        [](<https://adk.dev/context/#__codelineno-6-19>)}
        
        [](<https://adk.dev/context/#__codelineno-7-1>)// Example: Agent implementation receiving InvocationContext
        [](<https://adk.dev/context/#__codelineno-7-2>)import com.google.adk.agents.BaseAgent;
        [](<https://adk.dev/context/#__codelineno-7-3>)import com.google.adk.agents.InvocationContext;
        [](<https://adk.dev/context/#__codelineno-7-4>)import com.google.adk.events.Event;
        [](<https://adk.dev/context/#__codelineno-7-5>)import io.reactivex.rxjava3.core.Flowable;
        [](<https://adk.dev/context/#__codelineno-7-6>)
        [](<https://adk.dev/context/#__codelineno-7-7>)public class MyAgent extends BaseAgent {
        [](<https://adk.dev/context/#__codelineno-7-8>)    @Override
        [](<https://adk.dev/context/#__codelineno-7-9>)    protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
        [](<https://adk.dev/context/#__codelineno-7-10>)        // Direct access example
        [](<https://adk.dev/context/#__codelineno-7-11>)        String agentName = invocationContext.agent().name();
        [](<https://adk.dev/context/#__codelineno-7-12>)        String sessionId = invocationContext.session().id();
        [](<https://adk.dev/context/#__codelineno-7-13>)        String invocationId = invocationContext.invocationId();
        [](<https://adk.dev/context/#__codelineno-7-14>)        System.out.println("Agent " + agentName + " running in session " + sessionId + " for invocation " + invocationId);
        [](<https://adk.dev/context/#__codelineno-7-15>)        // ... agent logic using invocationContext ...
        [](<https://adk.dev/context/#__codelineno-7-16>)        return Flowable.empty();
        [](<https://adk.dev/context/#__codelineno-7-17>)    }
        [](<https://adk.dev/context/#__codelineno-7-18>)}
        
### `ReadonlyContext`[¶](<https://adk.dev/context/#readonlycontext> "Permanent link")

  * **Where Used:** Provided in scenarios where only read access to basic information is needed and mutation is disallowed (e.g., `InstructionProvider` functions). It's also the base class for other contexts.
  * **Purpose:** Offers a safe, read-only view of fundamental contextual details.
  * **Key Contents:** `invocation_id`, `agent_name`, and a read-only _view_ of the current `state`.

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-8-1>)# Example: Instruction provider receiving ReadonlyContext
        [](<https://adk.dev/context/#__codelineno-8-2>)from google.adk.agents.readonly_context import ReadonlyContext
        [](<https://adk.dev/context/#__codelineno-8-3>)
        [](<https://adk.dev/context/#__codelineno-8-4>)def my_instruction_provider(context: ReadonlyContext) -> str:
        [](<https://adk.dev/context/#__codelineno-8-5>)    # Read-only access example
        [](<https://adk.dev/context/#__codelineno-8-6>)    # The state property provides a read-only MappingProxyType view of the state
        [](<https://adk.dev/context/#__codelineno-8-7>)    user_tier = context.state.get("user_tier", "standard")
        [](<https://adk.dev/context/#__codelineno-8-8>)    # context.state['new_key'] = 'value' # TypeError: 'mappingproxy' object does not support item assignment
        [](<https://adk.dev/context/#__codelineno-8-9>)    return f"Process the request for a {user_tier} user."
        
        [](<https://adk.dev/context/#__codelineno-9-1>)// Pseudocode: Instruction provider receiving ReadonlyContext
        [](<https://adk.dev/context/#__codelineno-9-2>)import { ReadonlyContext } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-9-3>)
        [](<https://adk.dev/context/#__codelineno-9-4>)function myInstructionProvider(context: ReadonlyContext): string {
        [](<https://adk.dev/context/#__codelineno-9-5>)  // Read-only access example
        [](<https://adk.dev/context/#__codelineno-9-6>)  // The state object is read-only
        [](<https://adk.dev/context/#__codelineno-9-7>)  const userTier = context.state.get('user_tier') ?? 'standard';
        [](<https://adk.dev/context/#__codelineno-9-8>)  // context.state.set('new_key', 'value'); // This would fail or throw an error
        [](<https://adk.dev/context/#__codelineno-9-9>)  return `Process the request for a ${userTier} user.`;
        [](<https://adk.dev/context/#__codelineno-9-10>)}
        
        [](<https://adk.dev/context/#__codelineno-10-1>)import "google.golang.org/adk/v2/agent"
        [](<https://adk.dev/context/#__codelineno-10-2>)
        [](<https://adk.dev/context/#__codelineno-10-3>)// Pseudocode: Instruction provider receiving ReadonlyContext
        [](<https://adk.dev/context/#__codelineno-10-4>)func myInstructionProvider(ctx agent.ReadonlyContext) (string, error) {
        [](<https://adk.dev/context/#__codelineno-10-5>)    // Read-only access example
        [](<https://adk.dev/context/#__codelineno-10-6>)    userTier, err := ctx.ReadonlyState().Get("user_tier")
        [](<https://adk.dev/context/#__codelineno-10-7>)    if err != nil {
        [](<https://adk.dev/context/#__codelineno-10-8>)        userTier = "standard" // Default value
        [](<https://adk.dev/context/#__codelineno-10-9>)    }
        [](<https://adk.dev/context/#__codelineno-10-10>)    // ctx.ReadonlyState() has no Set method since State() is read-only.
        [](<https://adk.dev/context/#__codelineno-10-11>)    return fmt.Sprintf("Process the request for a %v user.", userTier), nil
        [](<https://adk.dev/context/#__codelineno-10-12>)}
        
        [](<https://adk.dev/context/#__codelineno-11-1>)// Example: Instruction provider receiving ReadonlyContext
        [](<https://adk.dev/context/#__codelineno-11-2>)import com.google.adk.agents.ReadonlyContext;
        [](<https://adk.dev/context/#__codelineno-11-3>)
        [](<https://adk.dev/context/#__codelineno-11-4>)public String myInstructionProvider(ReadonlyContext context) {
        [](<https://adk.dev/context/#__codelineno-11-5>)    // Read-only access example
        [](<https://adk.dev/context/#__codelineno-11-6>)    // state() returns an unmodifiable view of the session state
        [](<https://adk.dev/context/#__codelineno-11-7>)    String userTier = (String) context.state().getOrDefault("user_tier", "standard");
        [](<https://adk.dev/context/#__codelineno-11-8>)    // context.state().put("new_key", "value"); // UnsupportedOperationException
        [](<https://adk.dev/context/#__codelineno-11-9>)    return "Process the request for a " + userTier + " user.";
        [](<https://adk.dev/context/#__codelineno-11-10>)}
        
### `CallbackContext` and `Context`[¶](<https://adk.dev/context/#callbackcontext-and-context> "Permanent link")

  * **Where Used:** Passed as `callback_context` to agent lifecycle callbacks (`before_agent_callback`, `after_agent_callback`) and model interaction callbacks (`before_model_callback`, `after_model_callback`).
  * **Purpose:** Facilitates inspecting and modifying state, interacting with artifacts, and accessing invocation details _specifically within callbacks_.
  * **Key Capabilities (Adds to`ReadonlyContext`):**
    * **Mutable`state` Property:** Allows reading and writing to session state. Changes made here (`callback_context.state['key'] = value`) are tracked and associated with the event generated by the framework after the callback.
    * **Artifact Methods:** `load_artifact(filename)` and `save_artifact(filename, part)` methods for interacting with the configured `artifact_service`.
    * Direct `user_content` access.

Note

In Python and TypeScript, `CallbackContext` and `ToolContext` have been replaced by the `Context` type.
    
    === "Python"
    
        ```python
        # Example: Callback receiving Context (CallbackContext is unified into Context)
        from google.adk.agents.context import Context
        from google.adk.models import LlmRequest
        from google.genai import types
        from typing import Optional
    
        def my_before_model_cb(context: Context, request: LlmRequest) -> Optional[types.Content]:
            # Read/Write state example
            call_count = context.state.get("model_calls", 0)
            context.state["model_calls"] = call_count + 1 # Modify state (tracks delta)
    
            # Optionally load an artifact
            # config_part = context.load_artifact("model_config.json")
            print(f"Preparing model call #{call_count + 1} for invocation {context.invocation_id}")
            return None # Allow model call to proceed
        ```
    
    === "TypeScript"
    
        ```typescript
        // Pseudocode: Callback receiving Context
        import { Context, LlmRequest } from '@google/adk';
        import { Content } from '@google/genai';
    
        function myBeforeModelCb(context: Context, request: LlmRequest): Content | undefined {
          // Read/Write state example
          const callCount = (context.state.get('model_calls') as number) || 0;
          context.state.set('model_calls', callCount + 1); // Modify state
    
          // Optionally load an artifact
          // const configPart = await context.loadArtifact('model_config.json');
          console.log(`Preparing model call #${callCount + 1} for invocation ${context.invocationId}`);
          return undefined; // Allow model call to proceed
        }
        ```
    
    === "Go"
    
        ```go
        import (
            "google.golang.org/adk/v2/agent"
            "google.golang.org/adk/v2/model"
        )
    
        // Pseudocode: Callback receiving CallbackContext
        func myBeforeModelCb(ctx agent.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
            // Read/Write state example
            callCount, err := ctx.State().Get("model_calls")
            if err != nil {
                callCount = 0 // Default value
            }
            newCount := callCount.(int) + 1
            if err := ctx.State().Set("model_calls", newCount); err != nil {
                return nil, err
            }
    
            // Optionally load an artifact
            // configPart, err := ctx.Artifacts().Load("model_config.json")
            fmt.Printf("Preparing model call #%d for invocation %s\n", newCount, ctx.InvocationID())
            return nil, nil // Allow model call to proceed
        }
    
        ```
    
    === "Java"
    
        ```java
        // Example: Callback receiving CallbackContext
        import com.google.adk.agents.CallbackContext;
        import com.google.adk.models.LlmRequest;
        import com.google.adk.models.LlmResponse;
        import io.reactivex.rxjava3.core.Maybe;
    
        public Maybe<LlmResponse> myBeforeModelCb(CallbackContext callbackContext, LlmRequest request) {
            // Read/Write state example
            int callCount = (int) callbackContext.state().getOrDefault("model_calls", 0);
            callbackContext.state().put("model_calls", callCount + 1); // Modify state (tracks delta)
    
            // Optionally load an artifact
            // Maybe<Part> configPart = callbackContext.loadArtifact("model_config.json");
            System.out.println("Preparing model call " + (callCount + 1) + " for invocation " + callbackContext.invocationId());
            return Maybe.empty(); // Allow model call to proceed
        }
        ```
    
### `ToolContext`[¶](<https://adk.dev/context/#toolcontext> "Permanent link")

  * **Where Used:** Passed as `tool_context` to the functions backing `FunctionTool`s and to tool execution callbacks (`before_tool_callback`, `after_tool_callback`).
  * **Purpose:** Provides everything `CallbackContext` does, plus specialized methods essential for tool execution, like handling authentication, searching memory, and listing artifacts.
  * **Key Capabilities (Adds to`CallbackContext`):**

    * **Authentication Methods:** `request_credential(auth_config)` to trigger an auth flow, and `get_auth_response(auth_config)` to retrieve credentials provided by the user/system.
    * **Artifact Listing:** `list_artifacts()` to discover available artifacts in the session.
    * **Memory Search:** `search_memory(query)` to query the configured `memory_service`.
    * **`function_call_id` Property:** Identifies the specific function call from the LLM that triggered this tool execution, crucial for linking authentication requests or responses back correctly.
    * **`actions` Property:** Direct access to the `EventActions` object for this step, allowing the tool to signal state changes, auth requests, etc.

PythonTypeScriptGoJava
    
    [](<https://adk.dev/context/#__codelineno-16-1>)# Example: Tool function receiving ToolContext
    [](<https://adk.dev/context/#__codelineno-16-2>)from google.adk.tools import ToolContext
    [](<https://adk.dev/context/#__codelineno-16-3>)from typing import Dict, Any
    [](<https://adk.dev/context/#__codelineno-16-4>)
    [](<https://adk.dev/context/#__codelineno-16-5>)# Assume this function is wrapped by a FunctionTool
    [](<https://adk.dev/context/#__codelineno-16-6>)def search_external_api(query: str, tool_context: ToolContext) -> Dict[str, Any]:
    [](<https://adk.dev/context/#__codelineno-16-7>)    api_key = tool_context.state.get("api_key")
    [](<https://adk.dev/context/#__codelineno-16-8>)    if not api_key:
    [](<https://adk.dev/context/#__codelineno-16-9>)        # Define required auth config
    [](<https://adk.dev/context/#__codelineno-16-10>)        # auth_config = AuthConfig(...)
    [](<https://adk.dev/context/#__codelineno-16-11>)        # tool_context.request_credential(auth_config) # Request credentials
    [](<https://adk.dev/context/#__codelineno-16-12>)        # Use the 'actions' property to signal the auth request has been made
    [](<https://adk.dev/context/#__codelineno-16-13>)        # tool_context.actions.requested_auth_configs[tool_context.function_call_id] = auth_config
    [](<https://adk.dev/context/#__codelineno-16-14>)        return {"status": "Auth Required"}
    [](<https://adk.dev/context/#__codelineno-16-15>)
    [](<https://adk.dev/context/#__codelineno-16-16>)    # Use the API key...
    [](<https://adk.dev/context/#__codelineno-16-17>)    print(f"Tool executing for query '{query}' using API key. Invocation: {tool_context.invocation_id}")
    [](<https://adk.dev/context/#__codelineno-16-18>)
    [](<https://adk.dev/context/#__codelineno-16-19>)    # Optionally search memory or list artifacts
    [](<https://adk.dev/context/#__codelineno-16-20>)    # relevant_docs = tool_context.search_memory(f"info related to {query}")
    [](<https://adk.dev/context/#__codelineno-16-21>)    # available_files = tool_context.list_artifacts()
    [](<https://adk.dev/context/#__codelineno-16-22>)
    [](<https://adk.dev/context/#__codelineno-16-23>)    return {"result": f"Data for {query} fetched."}
    
    [](<https://adk.dev/context/#__codelineno-17-1>)// Pseudocode: Tool function receiving Context
    [](<https://adk.dev/context/#__codelineno-17-2>)import { Context } from '@google/adk';
    [](<https://adk.dev/context/#__codelineno-17-3>)
    [](<https://adk.dev/context/#__codelineno-17-4>)// __Assume this function is wrapped by a FunctionTool__
    [](<https://adk.dev/context/#__codelineno-17-5>)function searchExternalApi(query: string, context: Context): { [key: string]: string } {
    [](<https://adk.dev/context/#__codelineno-17-6>)  const apiKey = context.state.get('api_key') as string;
    [](<https://adk.dev/context/#__codelineno-17-7>)  if (!apiKey) {
    [](<https://adk.dev/context/#__codelineno-17-8>)     // Define required auth config
    [](<https://adk.dev/context/#__codelineno-17-9>)     // const authConfig = new AuthConfig(...);
    [](<https://adk.dev/context/#__codelineno-17-10>)     // context.requestCredential(authConfig); // Request credentials
    [](<https://adk.dev/context/#__codelineno-17-11>)     // The 'actions' property is now automatically updated by requestCredential
    [](<https://adk.dev/context/#__codelineno-17-12>)     return { status: 'Auth Required' };
    [](<https://adk.dev/context/#__codelineno-17-13>)  }
    [](<https://adk.dev/context/#__codelineno-17-14>)
    [](<https://adk.dev/context/#__codelineno-17-15>)  // Use the API key...
    [](<https://adk.dev/context/#__codelineno-17-16>)  console.log(`Tool executing for query '${query}' using API key. Invocation: ${context.invocationId}`);
    [](<https://adk.dev/context/#__codelineno-17-17>)
    [](<https://adk.dev/context/#__codelineno-17-18>)  // Optionally search memory or list artifacts
    [](<https://adk.dev/context/#__codelineno-17-19>)  // Note: accessing services like memory/artifacts is typically async in TS,
    [](<https://adk.dev/context/#__codelineno-17-20>)  // so you would need to mark this function 'async' if you reused them.
    [](<https://adk.dev/context/#__codelineno-17-21>)  // context.searchMemory(`info related to ${query}`).then(...)
    [](<https://adk.dev/context/#__codelineno-17-22>)  // context.listArtifacts().then(...)
    [](<https://adk.dev/context/#__codelineno-17-23>)
    [](<https://adk.dev/context/#__codelineno-17-24>)  return { result: `Data for ${query} fetched.` };
    [](<https://adk.dev/context/#__codelineno-17-25>)}
    
    [](<https://adk.dev/context/#__codelineno-18-1>)import "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/context/#__codelineno-18-2>)
    [](<https://adk.dev/context/#__codelineno-18-3>)// Pseudocode: Tool function receiving ToolContext
    [](<https://adk.dev/context/#__codelineno-18-4>)type searchExternalAPIArgs struct {
    [](<https://adk.dev/context/#__codelineno-18-5>)    Query string `json:"query" jsonschema:"The query to search for."`
    [](<https://adk.dev/context/#__codelineno-18-6>)}
    [](<https://adk.dev/context/#__codelineno-18-7>)
    [](<https://adk.dev/context/#__codelineno-18-8>)func searchExternalAPI(tc agent.Context, input searchExternalAPIArgs) (string, error) {
    [](<https://adk.dev/context/#__codelineno-18-9>)    apiKey, err := tc.State().Get("api_key")
    [](<https://adk.dev/context/#__codelineno-18-10>)    if err != nil || apiKey == "" {
    [](<https://adk.dev/context/#__codelineno-18-11>)        // In a real scenario, you would define and request credentials here.
    [](<https://adk.dev/context/#__codelineno-18-12>)        // This is a conceptual placeholder.
    [](<https://adk.dev/context/#__codelineno-18-13>)        return "", fmt.Errorf("auth required")
    [](<https://adk.dev/context/#__codelineno-18-14>)    }
    [](<https://adk.dev/context/#__codelineno-18-15>)
    [](<https://adk.dev/context/#__codelineno-18-16>)    // Use the API key...
    [](<https://adk.dev/context/#__codelineno-18-17>)    fmt.Printf("Tool executing for query '%s' using API key. Invocation: %s\n", input.Query, tc.InvocationID())
    [](<https://adk.dev/context/#__codelineno-18-18>)
    [](<https://adk.dev/context/#__codelineno-18-19>)    // Optionally search memory or list artifacts
    [](<https://adk.dev/context/#__codelineno-18-20>)    // relevantDocs, _ := tc.SearchMemory(tc, "info related to %s", input.Query))
    [](<https://adk.dev/context/#__codelineno-18-21>)    // availableFiles, _ := tc.Artifacts().List()
    [](<https://adk.dev/context/#__codelineno-18-22>)
    [](<https://adk.dev/context/#__codelineno-18-23>)    return fmt.Sprintf("Data for %s fetched.", input.Query), nil
    [](<https://adk.dev/context/#__codelineno-18-24>)}
    
    [](<https://adk.dev/context/#__codelineno-19-1>)// Example: Tool function receiving ToolContext
    [](<https://adk.dev/context/#__codelineno-19-2>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/context/#__codelineno-19-3>)import java.util.Map;
    [](<https://adk.dev/context/#__codelineno-19-4>)
    [](<https://adk.dev/context/#__codelineno-19-5>)// Assume this function is wrapped by a FunctionTool
    [](<https://adk.dev/context/#__codelineno-19-6>)public Map<String, Object> searchExternalApi(String query, ToolContext toolContext) {
    [](<https://adk.dev/context/#__codelineno-19-7>)    String apiKey = (String) toolContext.state().getOrDefault("api_key", "");
    [](<https://adk.dev/context/#__codelineno-19-8>)    if (apiKey.isEmpty()) {
    [](<https://adk.dev/context/#__codelineno-19-9>)        // Define required auth config
    [](<https://adk.dev/context/#__codelineno-19-10>)        // authConfig = AuthConfig(...);
    [](<https://adk.dev/context/#__codelineno-19-11>)        // toolContext.requestCredential(authConfig); // Request credentials
    [](<https://adk.dev/context/#__codelineno-19-12>)        // Use the 'actions' property to signal the auth request has been made
    [](<https://adk.dev/context/#__codelineno-19-13>)        return Map.of("status", "Auth Required");
    [](<https://adk.dev/context/#__codelineno-19-14>)    }
    [](<https://adk.dev/context/#__codelineno-19-15>)
    [](<https://adk.dev/context/#__codelineno-19-16>)    // Use the API key...
    [](<https://adk.dev/context/#__codelineno-19-17>)    System.out.println("Tool executing for query " + query + " using API key.");
    [](<https://adk.dev/context/#__codelineno-19-18>)
    [](<https://adk.dev/context/#__codelineno-19-19>)    // Optionally list artifacts
    [](<https://adk.dev/context/#__codelineno-19-20>)    // Single<List<String>> availableFiles = toolContext.listArtifacts();
    [](<https://adk.dev/context/#__codelineno-19-21>)
    [](<https://adk.dev/context/#__codelineno-19-22>)    return Map.of("result", "Data for " + query + " fetched");
    [](<https://adk.dev/context/#__codelineno-19-23>)}
    
Understanding these different context objects and when to use them is key to effectively managing state, accessing services, and controlling the flow of your ADK application. The next section will detail common tasks you can perform using these contexts.

## Common tasks using context[¶](<https://adk.dev/context/#common-tasks-using-context> "Permanent link")

Now that you understand the different context objects, let's focus on how to use them for common tasks when building your agents and tools.

### Access information[¶](<https://adk.dev/context/#access-information> "Permanent link")

You'll frequently need to read information stored within the context.

  * **Read session state:** Access data saved in previous steps or user/app-level settings. Use dictionary-like access on the `state` property.

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-20-1>)# Example: In a Tool function
        [](<https://adk.dev/context/#__codelineno-20-2>)from google.adk.tools import ToolContext
        [](<https://adk.dev/context/#__codelineno-20-3>)
        [](<https://adk.dev/context/#__codelineno-20-4>)def my_tool(tool_context: ToolContext, **kwargs):
        [](<https://adk.dev/context/#__codelineno-20-5>)    user_pref = tool_context.state.get("user_display_preference", "default_mode")
        [](<https://adk.dev/context/#__codelineno-20-6>)    api_endpoint = tool_context.state.get("app:api_endpoint") # Read app-level state
        [](<https://adk.dev/context/#__codelineno-20-7>)
        [](<https://adk.dev/context/#__codelineno-20-8>)    if user_pref == "dark_mode":
        [](<https://adk.dev/context/#__codelineno-20-9>)        # ... apply dark mode logic ...
        [](<https://adk.dev/context/#__codelineno-20-10>)        pass
        [](<https://adk.dev/context/#__codelineno-20-11>)    print(f"Using API endpoint: {api_endpoint}")
        [](<https://adk.dev/context/#__codelineno-20-12>)    # ... rest of tool logic ...
        [](<https://adk.dev/context/#__codelineno-20-13>)
        [](<https://adk.dev/context/#__codelineno-20-14>)# Example: In a Callback function
        [](<https://adk.dev/context/#__codelineno-20-15>)from google.adk.agents.context import Context
        [](<https://adk.dev/context/#__codelineno-20-16>)
        [](<https://adk.dev/context/#__codelineno-20-17>)def my_callback(context: Context, **kwargs):
        [](<https://adk.dev/context/#__codelineno-20-18>)    last_tool_result = context.state.get("temp:last_api_result") # Read temporary state
        [](<https://adk.dev/context/#__codelineno-20-19>)    if last_tool_result:
        [](<https://adk.dev/context/#__codelineno-20-20>)        print(f"Found temporary result from last tool: {last_tool_result}")
        [](<https://adk.dev/context/#__codelineno-20-21>)    # ... callback logic ...
        
        [](<https://adk.dev/context/#__codelineno-21-1>)// Pseudocode: In a Tool function
        [](<https://adk.dev/context/#__codelineno-21-2>)import { Context } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-21-3>)
        [](<https://adk.dev/context/#__codelineno-21-4>)async function myTool(context: Context) {
        [](<https://adk.dev/context/#__codelineno-21-5>)  const userPref = context.state.get('user_display_preference', 'default_mode');
        [](<https://adk.dev/context/#__codelineno-21-6>)  const apiEndpoint = context.state.get('app:api_endpoint'); // Read app-level state
        [](<https://adk.dev/context/#__codelineno-21-7>)
        [](<https://adk.dev/context/#__codelineno-21-8>)  if (userPref === 'dark_mode') {
        [](<https://adk.dev/context/#__codelineno-21-9>)    // ... apply dark mode logic ...
        [](<https://adk.dev/context/#__codelineno-21-10>)  }
        [](<https://adk.dev/context/#__codelineno-21-11>)  console.log(`Using API endpoint: ${apiEndpoint}`);
        [](<https://adk.dev/context/#__codelineno-21-12>)  // ... rest of tool logic ...
        [](<https://adk.dev/context/#__codelineno-21-13>)}
        [](<https://adk.dev/context/#__codelineno-21-14>)
        [](<https://adk.dev/context/#__codelineno-21-15>)// Pseudocode: In a Callback function
        [](<https://adk.dev/context/#__codelineno-21-16>)import { Context } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-21-17>)
        [](<https://adk.dev/context/#__codelineno-21-18>)function myCallback(context: Context) {
        [](<https://adk.dev/context/#__codelineno-21-19>)  const lastToolResult = context.state.get('temp:last_api_result'); // Read temporary state
        [](<https://adk.dev/context/#__codelineno-21-20>)  if (lastToolResult) {
        [](<https://adk.dev/context/#__codelineno-21-21>)    console.log(`Found temporary result from last tool: ${lastToolResult}`);
        [](<https://adk.dev/context/#__codelineno-21-22>)  }
        [](<https://adk.dev/context/#__codelineno-21-23>)  // ... callback logic ...
        [](<https://adk.dev/context/#__codelineno-21-24>)}
        
        [](<https://adk.dev/context/#__codelineno-22-1>)import (
        [](<https://adk.dev/context/#__codelineno-22-2>)    "google.golang.org/adk/v2/agent"
        [](<https://adk.dev/context/#__codelineno-22-3>)    "google.golang.org/adk/v2/session"
        [](<https://adk.dev/context/#__codelineno-22-4>)    "google.golang.org/adk/v2/tool"
        [](<https://adk.dev/context/#__codelineno-22-5>)    "google.golang.org/genai"
        [](<https://adk.dev/context/#__codelineno-22-6>))
        [](<https://adk.dev/context/#__codelineno-22-7>)
        [](<https://adk.dev/context/#__codelineno-22-8>)// Pseudocode: In a Tool function
        [](<https://adk.dev/context/#__codelineno-22-9>)type toolArgs struct {
        [](<https://adk.dev/context/#__codelineno-22-10>)    // Define tool-specific arguments here
        [](<https://adk.dev/context/#__codelineno-22-11>)}
        [](<https://adk.dev/context/#__codelineno-22-12>)
        [](<https://adk.dev/context/#__codelineno-22-13>)type toolResults struct {
        [](<https://adk.dev/context/#__codelineno-22-14>)    // Define tool-specific results here
        [](<https://adk.dev/context/#__codelineno-22-15>)}
        [](<https://adk.dev/context/#__codelineno-22-16>)
        [](<https://adk.dev/context/#__codelineno-22-17>)// Example tool function demonstrating state access
        [](<https://adk.dev/context/#__codelineno-22-18>)func myTool(tc agent.Context, input toolArgs) (toolResults, error) {
        [](<https://adk.dev/context/#__codelineno-22-19>)    userPref, err := tc.State().Get("user_display_preference")
        [](<https://adk.dev/context/#__codelineno-22-20>)    if err != nil {
        [](<https://adk.dev/context/#__codelineno-22-21>)        userPref = "default_mode"
        [](<https://adk.dev/context/#__codelineno-22-22>)    }
        [](<https://adk.dev/context/#__codelineno-22-23>)    apiEndpoint, _ := tc.State().Get("app:api_endpoint") // Read app-level state
        [](<https://adk.dev/context/#__codelineno-22-24>)
        [](<https://adk.dev/context/#__codelineno-22-25>)    if userPref == "dark_mode" {
        [](<https://adk.dev/context/#__codelineno-22-26>)        // ... apply dark mode logic ...
        [](<https://adk.dev/context/#__codelineno-22-27>)    }
        [](<https://adk.dev/context/#__codelineno-22-28>)    fmt.Printf("Using API endpoint: %v\n", apiEndpoint)
        [](<https://adk.dev/context/#__codelineno-22-29>)    // ... rest of tool logic ...
        [](<https://adk.dev/context/#__codelineno-22-30>)    return toolResults{}, nil
        [](<https://adk.dev/context/#__codelineno-22-31>)}
        [](<https://adk.dev/context/#__codelineno-22-32>)
        [](<https://adk.dev/context/#__codelineno-22-33>)
        [](<https://adk.dev/context/#__codelineno-22-34>)// Pseudocode: In a Callback function
        [](<https://adk.dev/context/#__codelineno-22-35>)func myCallback(ctx agent.Context) (*genai.Content, error) {
        [](<https://adk.dev/context/#__codelineno-22-36>)    lastToolResult, err := ctx.State().Get("temp:last_api_result") // Read temporary state
        [](<https://adk.dev/context/#__codelineno-22-37>)    if err == nil {
        [](<https://adk.dev/context/#__codelineno-22-38>)        fmt.Printf("Found temporary result from last tool: %v\n", lastToolResult)
        [](<https://adk.dev/context/#__codelineno-22-39>)    } else {
        [](<https://adk.dev/context/#__codelineno-22-40>)        fmt.Println("No temporary result found.")
        [](<https://adk.dev/context/#__codelineno-22-41>)    }
        [](<https://adk.dev/context/#__codelineno-22-42>)    // ... callback logic ...
        [](<https://adk.dev/context/#__codelineno-22-43>)    return nil, nil
        [](<https://adk.dev/context/#__codelineno-22-44>)}
        
        [](<https://adk.dev/context/#__codelineno-23-1>)// Example: In a Tool function
        [](<https://adk.dev/context/#__codelineno-23-2>)import com.google.adk.tools.ToolContext;
        [](<https://adk.dev/context/#__codelineno-23-3>)
        [](<https://adk.dev/context/#__codelineno-23-4>)public void myTool(ToolContext toolContext) {
        [](<https://adk.dev/context/#__codelineno-23-5>)    String userPref = (String) toolContext.state().getOrDefault("user_display_preference", "default_mode");
        [](<https://adk.dev/context/#__codelineno-23-6>)    String apiEndpoint = (String) toolContext.state().get("app:api_endpoint"); // Read app-level state
        [](<https://adk.dev/context/#__codelineno-23-7>)
        [](<https://adk.dev/context/#__codelineno-23-8>)    if ("dark_mode".equals(userPref)) {
        [](<https://adk.dev/context/#__codelineno-23-9>)        // ... apply dark mode logic ...
        [](<https://adk.dev/context/#__codelineno-23-10>)    }
        [](<https://adk.dev/context/#__codelineno-23-11>)    System.out.println("Using API endpoint: " + apiEndpoint);
        [](<https://adk.dev/context/#__codelineno-23-12>)    // ... rest of tool logic ...
        [](<https://adk.dev/context/#__codelineno-23-13>)}
        [](<https://adk.dev/context/#__codelineno-23-14>)
        [](<https://adk.dev/context/#__codelineno-23-15>)// Example: In a Callback function
        [](<https://adk.dev/context/#__codelineno-23-16>)import com.google.adk.agents.CallbackContext;
        [](<https://adk.dev/context/#__codelineno-23-17>)
        [](<https://adk.dev/context/#__codelineno-23-18>)public void myCallback(CallbackContext callbackContext) {
        [](<https://adk.dev/context/#__codelineno-23-19>)    String lastToolResult = (String) callbackContext.state().get("temp:last_api_result"); // Read temporary state
        [](<https://adk.dev/context/#__codelineno-23-20>)
        [](<https://adk.dev/context/#__codelineno-23-21>)    if (lastToolResult != null && !lastToolResult.isEmpty()) {
        [](<https://adk.dev/context/#__codelineno-23-22>)        System.out.println("Found temporary result from last tool: " + lastToolResult);
        [](<https://adk.dev/context/#__codelineno-23-23>)    }
        [](<https://adk.dev/context/#__codelineno-23-24>)    // ... callback logic ...
        [](<https://adk.dev/context/#__codelineno-23-25>)}
        
  * **Get current identifiers:** Useful for logging or custom logic based on the current operation.

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-24-1>)# Example: In any context (ToolContext shown)
        [](<https://adk.dev/context/#__codelineno-24-2>)from google.adk.tools import ToolContext
        [](<https://adk.dev/context/#__codelineno-24-3>)
        [](<https://adk.dev/context/#__codelineno-24-4>)def log_tool_usage(tool_context: ToolContext, **kwargs):
        [](<https://adk.dev/context/#__codelineno-24-5>)    agent_name = tool_context.agent_name
        [](<https://adk.dev/context/#__codelineno-24-6>)    inv_id = tool_context.invocation_id
        [](<https://adk.dev/context/#__codelineno-24-7>)    func_call_id = getattr(tool_context, 'function_call_id', 'N/A') # Specific to ToolContext
        [](<https://adk.dev/context/#__codelineno-24-8>)
        [](<https://adk.dev/context/#__codelineno-24-9>)    print(f"Log: Invocation={inv_id}, Agent={agent_name}, FunctionCallID={func_call_id} - Tool Executed.")
        
        [](<https://adk.dev/context/#__codelineno-25-1>)// Pseudocode: In any context
        [](<https://adk.dev/context/#__codelineno-25-2>)import { Context } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-25-3>)
        [](<https://adk.dev/context/#__codelineno-25-4>)function logToolUsage(context: Context) {
        [](<https://adk.dev/context/#__codelineno-25-5>)  const agentName = context.agentName;
        [](<https://adk.dev/context/#__codelineno-25-6>)  const invId = context.invocationId;
        [](<https://adk.dev/context/#__codelineno-25-7>)  const functionCallId = context.functionCallId ?? 'N/A'; // Available when executing a tool
        [](<https://adk.dev/context/#__codelineno-25-8>)
        [](<https://adk.dev/context/#__codelineno-25-9>)  console.log(`Log: Invocation=${invId}, Agent=${agentName}, FunctionCallID=${functionCallId} - Tool Executed.`);
        [](<https://adk.dev/context/#__codelineno-25-10>)}
        
        [](<https://adk.dev/context/#__codelineno-26-1>)import "google.golang.org/adk/v2/tool"
        [](<https://adk.dev/context/#__codelineno-26-2>)
        [](<https://adk.dev/context/#__codelineno-26-3>)// Pseudocode: In any context (ToolContext shown)
        [](<https://adk.dev/context/#__codelineno-26-4>)type logToolUsageArgs struct{}
        [](<https://adk.dev/context/#__codelineno-26-5>)type logToolUsageResult struct {
        [](<https://adk.dev/context/#__codelineno-26-6>)    Status string `json:"status"`
        [](<https://adk.dev/context/#__codelineno-26-7>)}
        [](<https://adk.dev/context/#__codelineno-26-8>)
        [](<https://adk.dev/context/#__codelineno-26-9>)func logToolUsage(tc agent.Context, args logToolUsageArgs) (logToolUsageResult, error) {
        [](<https://adk.dev/context/#__codelineno-26-10>)    agentName := tc.AgentName()
        [](<https://adk.dev/context/#__codelineno-26-11>)    invID := tc.InvocationID()
        [](<https://adk.dev/context/#__codelineno-26-12>)    funcCallID := tc.FunctionCallID()
        [](<https://adk.dev/context/#__codelineno-26-13>)
        [](<https://adk.dev/context/#__codelineno-26-14>)    fmt.Printf("Log: Invocation=%s, Agent=%s, FunctionCallID=%s - Tool Executed.\n", invID, agentName, funcCallID)
        [](<https://adk.dev/context/#__codelineno-26-15>)    return logToolUsageResult{Status: "Logged successfully"}, nil
        [](<https://adk.dev/context/#__codelineno-26-16>)}
        
        [](<https://adk.dev/context/#__codelineno-27-1>)// Example: In any context (ToolContext shown)
        [](<https://adk.dev/context/#__codelineno-27-2>)import com.google.adk.tools.ToolContext;
        [](<https://adk.dev/context/#__codelineno-27-3>)
        [](<https://adk.dev/context/#__codelineno-27-4>)public void logToolUsage(ToolContext toolContext) {
        [](<https://adk.dev/context/#__codelineno-27-5>)    String agentName = toolContext.agentName();
        [](<https://adk.dev/context/#__codelineno-27-6>)    String invId = toolContext.invocationId();
        [](<https://adk.dev/context/#__codelineno-27-7>)    String functionCallId = toolContext.functionCallId().orElse("N/A"); // Specific to ToolContext
        [](<https://adk.dev/context/#__codelineno-27-8>)    System.out.println("Log: Invocation= " + invId + " Agent= " + agentName + " FunctionCallID= " + functionCallId);
        [](<https://adk.dev/context/#__codelineno-27-9>)}
        
  * **Access the initial user input:** Refer back to the message that started the current invocation.

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-28-1>)# Example: In a Callback
        [](<https://adk.dev/context/#__codelineno-28-2>)from google.adk.agents.context import Context
        [](<https://adk.dev/context/#__codelineno-28-3>)
        [](<https://adk.dev/context/#__codelineno-28-4>)def check_initial_intent(context: Context, **kwargs):
        [](<https://adk.dev/context/#__codelineno-28-5>)    initial_text = "N/A"
        [](<https://adk.dev/context/#__codelineno-28-6>)    if context.user_content and context.user_content.parts:
        [](<https://adk.dev/context/#__codelineno-28-7>)        initial_text = context.user_content.parts[0].text or "Non-text input"
        [](<https://adk.dev/context/#__codelineno-28-8>)
        [](<https://adk.dev/context/#__codelineno-28-9>)    print(f"This invocation started with user input: '{initial_text}'")
        [](<https://adk.dev/context/#__codelineno-28-10>)
        [](<https://adk.dev/context/#__codelineno-28-11>)# Example: In an Agent's _run_async_impl
        [](<https://adk.dev/context/#__codelineno-28-12>)# async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        [](<https://adk.dev/context/#__codelineno-28-13>)#     if ctx.user_content and ctx.user_content.parts:
        [](<https://adk.dev/context/#__codelineno-28-14>)#         initial_text = ctx.user_content.parts[0].text
        [](<https://adk.dev/context/#__codelineno-28-15>)#         print(f"Agent logic remembering initial query: {initial_text}")
        [](<https://adk.dev/context/#__codelineno-28-16>)#     ...
        
        [](<https://adk.dev/context/#__codelineno-29-1>)// Pseudocode: In a Callback
        [](<https://adk.dev/context/#__codelineno-29-2>)import { Context } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-29-3>)
        [](<https://adk.dev/context/#__codelineno-29-4>)function checkInitialIntent(context: Context) {
        [](<https://adk.dev/context/#__codelineno-29-5>)  let initialText = 'N/A';
        [](<https://adk.dev/context/#__codelineno-29-6>)  const userContent = context.userContent;
        [](<https://adk.dev/context/#__codelineno-29-7>)  if (userContent?.parts?.length) {
        [](<https://adk.dev/context/#__codelineno-29-8>)    initialText = userContent.parts[0].text ?? 'Non-text input';
        [](<https://adk.dev/context/#__codelineno-29-9>)  }
        [](<https://adk.dev/context/#__codelineno-29-10>)
        [](<https://adk.dev/context/#__codelineno-29-11>)  console.log(`This invocation started with user input: '${initialText}'`);
        [](<https://adk.dev/context/#__codelineno-29-12>)}
        
        [](<https://adk.dev/context/#__codelineno-30-1>)import (
        [](<https://adk.dev/context/#__codelineno-30-2>)    "google.golang.org/adk/v2/agent"
        [](<https://adk.dev/context/#__codelineno-30-3>)    "google.golang.org/genai"
        [](<https://adk.dev/context/#__codelineno-30-4>))
        [](<https://adk.dev/context/#__codelineno-30-5>)
        [](<https://adk.dev/context/#__codelineno-30-6>)// Pseudocode: In a Callback
        [](<https://adk.dev/context/#__codelineno-30-7>)func logInitialUserInput(ctx agent.Context) (*genai.Content, error) {
        [](<https://adk.dev/context/#__codelineno-30-8>)    userContent := ctx.UserContent()
        [](<https://adk.dev/context/#__codelineno-30-9>)    if userContent != nil && len(userContent.Parts) > 0 {
        [](<https://adk.dev/context/#__codelineno-30-10>)        if text := userContent.Parts[0].Text; text != "" {
        [](<https://adk.dev/context/#__codelineno-30-11>)            fmt.Printf("User's initial input for this turn: '%s'\n", text)
        [](<https://adk.dev/context/#__codelineno-30-12>)        }
        [](<https://adk.dev/context/#__codelineno-30-13>)    }
        [](<https://adk.dev/context/#__codelineno-30-14>)    return nil, nil // No modification
        [](<https://adk.dev/context/#__codelineno-30-15>)}
        
        [](<https://adk.dev/context/#__codelineno-31-1>)// Example: In a Callback
        [](<https://adk.dev/context/#__codelineno-31-2>)import com.google.adk.agents.CallbackContext;
        [](<https://adk.dev/context/#__codelineno-31-3>)import com.google.genai.types.Content;
        [](<https://adk.dev/context/#__codelineno-31-4>)
        [](<https://adk.dev/context/#__codelineno-31-5>)public void checkInitialIntent(CallbackContext callbackContext) {
        [](<https://adk.dev/context/#__codelineno-31-6>)    String initialText = "N/A";
        [](<https://adk.dev/context/#__codelineno-31-7>)    if (callbackContext.userContent().isPresent() && callbackContext.userContent().get().parts() != null && !callbackContext.userContent().get().parts().get().isEmpty()) {
        [](<https://adk.dev/context/#__codelineno-31-8>)        initialText = callbackContext.userContent().get().parts().get().get(0).text().orElse("Non-text input");
        [](<https://adk.dev/context/#__codelineno-31-9>)        // ...
        [](<https://adk.dev/context/#__codelineno-31-10>)        System.out.println("This invocation started with user input: " + initialText);
        [](<https://adk.dev/context/#__codelineno-31-11>)    }
        [](<https://adk.dev/context/#__codelineno-31-12>)}
        
### Manage state[¶](<https://adk.dev/context/#manage-state> "Permanent link")

State is crucial for memory and data flow. When you modify state using `CallbackContext` or `ToolContext`, the changes are automatically tracked and persisted by the framework.

  * **How it Works:** Writing to `callback_context.state['my_key'] = my_value` or `tool_context.state['my_key'] = my_value` adds this change to the `EventActions.state_delta` associated with the current step's event. The `SessionService` then applies these deltas when persisting the event.

  * **Pass data between tools**

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-32-1>)# Example: Tool 1 - Fetches user ID
        [](<https://adk.dev/context/#__codelineno-32-2>)from google.adk.tools import ToolContext
        [](<https://adk.dev/context/#__codelineno-32-3>)import uuid
        [](<https://adk.dev/context/#__codelineno-32-4>)
        [](<https://adk.dev/context/#__codelineno-32-5>)def get_user_profile(tool_context: ToolContext) -> dict:
        [](<https://adk.dev/context/#__codelineno-32-6>)    user_id = str(uuid.uuid4()) # Simulate fetching ID
        [](<https://adk.dev/context/#__codelineno-32-7>)    # Save the ID to state for the next tool
        [](<https://adk.dev/context/#__codelineno-32-8>)    tool_context.state["temp:current_user_id"] = user_id
        [](<https://adk.dev/context/#__codelineno-32-9>)    return {"profile_status": "ID generated"}
        [](<https://adk.dev/context/#__codelineno-32-10>)
        [](<https://adk.dev/context/#__codelineno-32-11>)# Example: Tool 2 - Uses user ID from state
        [](<https://adk.dev/context/#__codelineno-32-12>)def get_user_orders(tool_context: ToolContext) -> dict:
        [](<https://adk.dev/context/#__codelineno-32-13>)    user_id = tool_context.state.get("temp:current_user_id")
        [](<https://adk.dev/context/#__codelineno-32-14>)    if not user_id:
        [](<https://adk.dev/context/#__codelineno-32-15>)        return {"error": "User ID not found in state"}
        [](<https://adk.dev/context/#__codelineno-32-16>)
        [](<https://adk.dev/context/#__codelineno-32-17>)    print(f"Fetching orders for user ID: {user_id}")
        [](<https://adk.dev/context/#__codelineno-32-18>)    # ... logic to fetch orders using user_id ...
        [](<https://adk.dev/context/#__codelineno-32-19>)    return {"orders": ["order123", "order456"]}
        
        [](<https://adk.dev/context/#__codelineno-33-1>)// Pseudocode: Tool 1 - Fetches user ID
        [](<https://adk.dev/context/#__codelineno-33-2>)import { Context } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-33-3>)import { v4 as uuidv4 } from 'uuid';
        [](<https://adk.dev/context/#__codelineno-33-4>)
        [](<https://adk.dev/context/#__codelineno-33-5>)function getUserProfile(context: Context): Record<string, string> {
        [](<https://adk.dev/context/#__codelineno-33-6>)  const userId = uuidv4(); // Simulate fetching ID
        [](<https://adk.dev/context/#__codelineno-33-7>)  // Save the ID to state for the next tool
        [](<https://adk.dev/context/#__codelineno-33-8>)  context.state.set('temp:current_user_id', userId);
        [](<https://adk.dev/context/#__codelineno-33-9>)  return { profile_status: 'ID generated' };
        [](<https://adk.dev/context/#__codelineno-33-10>)}
        [](<https://adk.dev/context/#__codelineno-33-11>)
        [](<https://adk.dev/context/#__codelineno-33-12>)// Pseudocode: Tool 2 - Uses user ID from state
        [](<https://adk.dev/context/#__codelineno-33-13>)function getUserOrders(context: Context): Record<string, string | string[]> {
        [](<https://adk.dev/context/#__codelineno-33-14>)  const userId = context.state.get('temp:current_user_id');
        [](<https://adk.dev/context/#__codelineno-33-15>)  if (!userId) {
        [](<https://adk.dev/context/#__codelineno-33-16>)    return { error: 'User ID not found in state' };
        [](<https://adk.dev/context/#__codelineno-33-17>)  }
        [](<https://adk.dev/context/#__codelineno-33-18>)
        [](<https://adk.dev/context/#__codelineno-33-19>)  console.log(`Fetching orders for user ID: ${userId}`);
        [](<https://adk.dev/context/#__codelineno-33-20>)  // ... logic to fetch orders using user_id ...
        [](<https://adk.dev/context/#__codelineno-33-21>)  return { orders: ['order123', 'order456'] };
        [](<https://adk.dev/context/#__codelineno-33-22>)}
        
        [](<https://adk.dev/context/#__codelineno-34-1>)import "google.golang.org/adk/v2/tool"
        [](<https://adk.dev/context/#__codelineno-34-2>)
        [](<https://adk.dev/context/#__codelineno-34-3>)// Pseudocode: Tool 1 - Fetches user ID
        [](<https://adk.dev/context/#__codelineno-34-4>)type GetUserProfileArgs struct {
        [](<https://adk.dev/context/#__codelineno-34-5>)}
        [](<https://adk.dev/context/#__codelineno-34-6>)
        [](<https://adk.dev/context/#__codelineno-34-7>)func getUserProfile(tc agent.Context, input GetUserProfileArgs) (string, error) {
        [](<https://adk.dev/context/#__codelineno-34-8>)    // A random user ID for demonstration purposes
        [](<https://adk.dev/context/#__codelineno-34-9>)    userID := "random_user_456"
        [](<https://adk.dev/context/#__codelineno-34-10>)
        [](<https://adk.dev/context/#__codelineno-34-11>)    // Save the ID to state for the next tool
        [](<https://adk.dev/context/#__codelineno-34-12>)    if err := tc.State().Set("temp:current_user_id", userID); err != nil {
        [](<https://adk.dev/context/#__codelineno-34-13>)        return "", fmt.Errorf("failed to set user ID in state: %w", err)
        [](<https://adk.dev/context/#__codelineno-34-14>)    }
        [](<https://adk.dev/context/#__codelineno-34-15>)    return "ID generated", nil
        [](<https://adk.dev/context/#__codelineno-34-16>)}
        [](<https://adk.dev/context/#__codelineno-34-17>)
        [](<https://adk.dev/context/#__codelineno-34-18>)
        [](<https://adk.dev/context/#__codelineno-34-19>)// Pseudocode: Tool 2 - Uses user ID from state
        [](<https://adk.dev/context/#__codelineno-34-20>)type GetUserOrdersArgs struct {
        [](<https://adk.dev/context/#__codelineno-34-21>)}
        [](<https://adk.dev/context/#__codelineno-34-22>)
        [](<https://adk.dev/context/#__codelineno-34-23>)type getUserOrdersResult struct {
        [](<https://adk.dev/context/#__codelineno-34-24>)    Orders []string `json:"orders"`
        [](<https://adk.dev/context/#__codelineno-34-25>)}
        [](<https://adk.dev/context/#__codelineno-34-26>)
        [](<https://adk.dev/context/#__codelineno-34-27>)func getUserOrders(tc agent.Context, input GetUserOrdersArgs) (*getUserOrdersResult, error) {
        [](<https://adk.dev/context/#__codelineno-34-28>)    userID, err := tc.State().Get("temp:current_user_id")
        [](<https://adk.dev/context/#__codelineno-34-29>)    if err != nil {
        [](<https://adk.dev/context/#__codelineno-34-30>)        return &getUserOrdersResult{}, fmt.Errorf("user ID not found in state")
        [](<https://adk.dev/context/#__codelineno-34-31>)    }
        [](<https://adk.dev/context/#__codelineno-34-32>)
        [](<https://adk.dev/context/#__codelineno-34-33>)    fmt.Printf("Fetching orders for user ID: %v\n", userID)
        [](<https://adk.dev/context/#__codelineno-34-34>)    // ... logic to fetch orders using user_id ...
        [](<https://adk.dev/context/#__codelineno-34-35>)    return &getUserOrdersResult{Orders: []string{"order123", "order456"}}, nil
        [](<https://adk.dev/context/#__codelineno-34-36>)}
        
        [](<https://adk.dev/context/#__codelineno-35-1>)// Example: Tool 1 - Fetches user ID
        [](<https://adk.dev/context/#__codelineno-35-2>)import com.google.adk.tools.ToolContext;
        [](<https://adk.dev/context/#__codelineno-35-3>)import java.util.Map;
        [](<https://adk.dev/context/#__codelineno-35-4>)import java.util.UUID;
        [](<https://adk.dev/context/#__codelineno-35-5>)
        [](<https://adk.dev/context/#__codelineno-35-6>)public Map<String, String> getUserProfile(ToolContext toolContext) {
        [](<https://adk.dev/context/#__codelineno-35-7>)    String userId = UUID.randomUUID().toString();
        [](<https://adk.dev/context/#__codelineno-35-8>)    // Save the ID to state for the next tool
        [](<https://adk.dev/context/#__codelineno-35-9>)    toolContext.state().put("temp:current_user_id", userId);
        [](<https://adk.dev/context/#__codelineno-35-10>)    return Map.of("profile_status", "ID generated");
        [](<https://adk.dev/context/#__codelineno-35-11>)}
        [](<https://adk.dev/context/#__codelineno-35-12>)
        [](<https://adk.dev/context/#__codelineno-35-13>)// Example: Tool 2 - Uses user ID from state
        [](<https://adk.dev/context/#__codelineno-35-14>)public Map<String, String> getUserOrders(ToolContext toolContext) {
        [](<https://adk.dev/context/#__codelineno-35-15>)    String userId = (String) toolContext.state().get("temp:current_user_id");
        [](<https://adk.dev/context/#__codelineno-35-16>)    if (userId == null || userId.isEmpty()) {
        [](<https://adk.dev/context/#__codelineno-35-17>)        return Map.of("error", "User ID not found in state");
        [](<https://adk.dev/context/#__codelineno-35-18>)    }
        [](<https://adk.dev/context/#__codelineno-35-19>)    System.out.println("Fetching orders for user id: " + userId);
        [](<https://adk.dev/context/#__codelineno-35-20>)    // ... logic to fetch orders using userId ...
        [](<https://adk.dev/context/#__codelineno-35-21>)    return Map.of("orders", "order123");
        [](<https://adk.dev/context/#__codelineno-35-22>)}
        
  * **Update user preferences:**

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-36-1>)# Example: Tool or Callback identifies a preference
        [](<https://adk.dev/context/#__codelineno-36-2>)from google.adk.tools import ToolContext # Or Context
        [](<https://adk.dev/context/#__codelineno-36-3>)
        [](<https://adk.dev/context/#__codelineno-36-4>)def set_user_preference(tool_context: ToolContext, preference: str, value: str) -> dict:
        [](<https://adk.dev/context/#__codelineno-36-5>)    # Use 'user:' prefix for user-level state (if using a persistent SessionService)
        [](<https://adk.dev/context/#__codelineno-36-6>)    state_key = f"user:{preference}"
        [](<https://adk.dev/context/#__codelineno-36-7>)    tool_context.state[state_key] = value
        [](<https://adk.dev/context/#__codelineno-36-8>)    print(f"Set user preference '{preference}' to '{value}'")
        [](<https://adk.dev/context/#__codelineno-36-9>)    return {"status": "Preference updated"}
        
        [](<https://adk.dev/context/#__codelineno-37-1>)// Pseudocode: Tool or Callback identifies a preference
        [](<https://adk.dev/context/#__codelineno-37-2>)import { Context } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-37-3>)
        [](<https://adk.dev/context/#__codelineno-37-4>)function setUserPreference(context: Context, preference: string, value: string): Record<string, string> {
        [](<https://adk.dev/context/#__codelineno-37-5>)  // Use 'user:' prefix for user-level state (if using a persistent SessionService)
        [](<https://adk.dev/context/#__codelineno-37-6>)  const stateKey = `user:${preference}`;
        [](<https://adk.dev/context/#__codelineno-37-7>)  context.state.set(stateKey, value);
        [](<https://adk.dev/context/#__codelineno-37-8>)  console.log(`Set user preference '${preference}' to '${value}'`);
        [](<https://adk.dev/context/#__codelineno-37-9>)  return { status: 'Preference updated' };
        [](<https://adk.dev/context/#__codelineno-37-10>)}
        
        [](<https://adk.dev/context/#__codelineno-38-1>)import "google.golang.org/adk/v2/tool"
        [](<https://adk.dev/context/#__codelineno-38-2>)
        [](<https://adk.dev/context/#__codelineno-38-3>)// Pseudocode: Tool or Callback identifies a preference
        [](<https://adk.dev/context/#__codelineno-38-4>)type setUserPreferenceArgs struct {
        [](<https://adk.dev/context/#__codelineno-38-5>)    Preference string `json:"preference" jsonschema:"The name of the preference to set."`
        [](<https://adk.dev/context/#__codelineno-38-6>)    Value      string `json:"value" jsonschema:"The value to set for the preference."`
        [](<https://adk.dev/context/#__codelineno-38-7>)}
        [](<https://adk.dev/context/#__codelineno-38-8>)
        [](<https://adk.dev/context/#__codelineno-38-9>)type setUserPreferenceResult struct {
        [](<https://adk.dev/context/#__codelineno-38-10>)    Status string `json:"status"`
        [](<https://adk.dev/context/#__codelineno-38-11>)}
        [](<https://adk.dev/context/#__codelineno-38-12>)
        [](<https://adk.dev/context/#__codelineno-38-13>)func setUserPreference(tc agent.Context, args setUserPreferenceArgs) (setUserPreferenceResult, error) {
        [](<https://adk.dev/context/#__codelineno-38-14>)    // Use 'user:' prefix for user-level state (if using a persistent SessionService)
        [](<https://adk.dev/context/#__codelineno-38-15>)    stateKey := fmt.Sprintf("user:%s", args.Preference)
        [](<https://adk.dev/context/#__codelineno-38-16>)    if err := tc.State().Set(stateKey, args.Value); err != nil {
        [](<https://adk.dev/context/#__codelineno-38-17>)        return setUserPreferenceResult{}, fmt.Errorf("failed to set preference in state: %w", err)
        [](<https://adk.dev/context/#__codelineno-38-18>)    }
        [](<https://adk.dev/context/#__codelineno-38-19>)    fmt.Printf("Set user preference '%s' to '%s'\n", args.Preference, args.Value)
        [](<https://adk.dev/context/#__codelineno-38-20>)    return setUserPreferenceResult{Status: "Preference updated"}, nil
        [](<https://adk.dev/context/#__codelineno-38-21>)}
        
        [](<https://adk.dev/context/#__codelineno-39-1>)// Example: Tool or Callback identifies a preference
        [](<https://adk.dev/context/#__codelineno-39-2>)import com.google.adk.tools.ToolContext; // Or CallbackContext
        [](<https://adk.dev/context/#__codelineno-39-3>)
        [](<https://adk.dev/context/#__codelineno-39-4>)public Map<String, String> setUserPreference(ToolContext toolContext, String preference, String value) {
        [](<https://adk.dev/context/#__codelineno-39-5>)    // Use 'user:' prefix for user-level state (if using a persistent SessionService)
        [](<https://adk.dev/context/#__codelineno-39-6>)    String stateKey = "user:" + preference;
        [](<https://adk.dev/context/#__codelineno-39-7>)    toolContext.state().put(stateKey, value);
        [](<https://adk.dev/context/#__codelineno-39-8>)    System.out.println("Set user preference '" + preference + "' to '" + value + "'");
        [](<https://adk.dev/context/#__codelineno-39-9>)    return Map.of("status", "Preference updated");
        [](<https://adk.dev/context/#__codelineno-39-10>)}
        
  * **State prefixes:** While basic state is session-specific, prefixes like `app:` and `user:` can be used with persistent `SessionService` implementations (like `DatabaseSessionService` or `VertexAiSessionService`) to indicate broader scope (app-wide or user-wide across sessions). `temp:` can denote data only relevant within the current invocation.

### Work with artifacts[¶](<https://adk.dev/context/#work-with-artifacts> "Permanent link")

Use artifacts to handle files or large data blobs associated with the session. Common use case: processing uploaded documents.

  * **Document summarizer example flow:**

    1. **Ingest Reference (e.g., in a Setup Tool or Callback):** Save the _path or URI_ of the document, not the entire content, as an artifact.

PythonTypeScriptGoJava
           
           [](<https://adk.dev/context/#__codelineno-40-1>)# Example: In a callback or initial tool
           [](<https://adk.dev/context/#__codelineno-40-2>)from google.adk.agents.context import Context # Or ToolContext
           [](<https://adk.dev/context/#__codelineno-40-3>)from google.genai import types
           [](<https://adk.dev/context/#__codelineno-40-4>)
           [](<https://adk.dev/context/#__codelineno-40-5>)def save_document_reference(context: Context, file_path: str) -> None:
           [](<https://adk.dev/context/#__codelineno-40-6>)    # Assume file_path is something like "gs://my-bucket/docs/report.pdf" or "/local/path/to/report.pdf"
           [](<https://adk.dev/context/#__codelineno-40-7>)    try:
           [](<https://adk.dev/context/#__codelineno-40-8>)        # Create a Part containing the path/URI text
           [](<https://adk.dev/context/#__codelineno-40-9>)        artifact_part = types.Part.from_text(file_path)
           [](<https://adk.dev/context/#__codelineno-40-10>)        version = context.save_artifact("document_to_summarize.txt", artifact_part)
           [](<https://adk.dev/context/#__codelineno-40-11>)        print(f"Saved document reference '{file_path}' as artifact version {version}")
           [](<https://adk.dev/context/#__codelineno-40-12>)        # Store the filename in state if needed by other tools
           [](<https://adk.dev/context/#__codelineno-40-13>)        context.state["temp:doc_artifact_name"] = "document_to_summarize.txt"
           [](<https://adk.dev/context/#__codelineno-40-14>)    except ValueError as e:
           [](<https://adk.dev/context/#__codelineno-40-15>)        print(f"Error saving artifact: {e}") # E.g., Artifact service not configured
           [](<https://adk.dev/context/#__codelineno-40-16>)    except Exception as e:
           [](<https://adk.dev/context/#__codelineno-40-17>)        print(f"Unexpected error saving artifact reference: {e}")
           [](<https://adk.dev/context/#__codelineno-40-18>)
           [](<https://adk.dev/context/#__codelineno-40-19>)# Example usage:
           [](<https://adk.dev/context/#__codelineno-40-20>)# save_document_reference(context, "gs://my-bucket/docs/report.pdf")
           
           [](<https://adk.dev/context/#__codelineno-41-1>)// Pseudocode: In a callback or initial tool
           [](<https://adk.dev/context/#__codelineno-41-2>)import { Context } from '@google/adk';
           [](<https://adk.dev/context/#__codelineno-41-3>)import type { Part } from '@google/genai';
           [](<https://adk.dev/context/#__codelineno-41-4>)
           [](<https://adk.dev/context/#__codelineno-41-5>)async function saveDocumentReference(context: Context, filePath: string) {
           [](<https://adk.dev/context/#__codelineno-41-6>)  // Assume filePath is something like "gs://my-bucket/docs/report.pdf" or "/local/path/to/report.pdf"
           [](<https://adk.dev/context/#__codelineno-41-7>)  try {
           [](<https://adk.dev/context/#__codelineno-41-8>)    // Create a Part containing the path/URI text
           [](<https://adk.dev/context/#__codelineno-41-9>)    const artifactPart: Part = { text: filePath };
           [](<https://adk.dev/context/#__codelineno-41-10>)    const version = await context.saveArtifact('document_to_summarize.txt', artifactPart);
           [](<https://adk.dev/context/#__codelineno-41-11>)    console.log(`Saved document reference '${filePath}' as artifact version ${version}`);
           [](<https://adk.dev/context/#__codelineno-41-12>)    // Store the filename in state if needed by other tools
           [](<https://adk.dev/context/#__codelineno-41-13>)    context.state.set('temp:doc_artifact_name', 'document_to_summarize.txt');
           [](<https://adk.dev/context/#__codelineno-41-14>)  } catch (e) {
           [](<https://adk.dev/context/#__codelineno-41-15>)    console.error(`Unexpected error saving artifact reference: ${e}`);
           [](<https://adk.dev/context/#__codelineno-41-16>)  }
           [](<https://adk.dev/context/#__codelineno-41-17>)}
           [](<https://adk.dev/context/#__codelineno-41-18>)
           [](<https://adk.dev/context/#__codelineno-41-19>)// Example usage:
           [](<https://adk.dev/context/#__codelineno-41-20>)// saveDocumentReference(context, "gs://my-bucket/docs/report.pdf");
           
           [](<https://adk.dev/context/#__codelineno-42-1>)import (
           [](<https://adk.dev/context/#__codelineno-42-2>)    "google.golang.org/adk/v2/tool"
           [](<https://adk.dev/context/#__codelineno-42-3>)    "google.golang.org/genai"
           [](<https://adk.dev/context/#__codelineno-42-4>))
           [](<https://adk.dev/context/#__codelineno-42-5>)
           [](<https://adk.dev/context/#__codelineno-42-6>)// Adapt the saveDocumentReference callback into a tool for this example.
           [](<https://adk.dev/context/#__codelineno-42-7>)type saveDocRefArgs struct {
           [](<https://adk.dev/context/#__codelineno-42-8>)    FilePath string `json:"file_path" jsonschema:"The path to the file to save."`
           [](<https://adk.dev/context/#__codelineno-42-9>)}
           [](<https://adk.dev/context/#__codelineno-42-10>)
           [](<https://adk.dev/context/#__codelineno-42-11>)type saveDocRefResult struct {
           [](<https://adk.dev/context/#__codelineno-42-12>)    Status string `json:"status"`
           [](<https://adk.dev/context/#__codelineno-42-13>)}
           [](<https://adk.dev/context/#__codelineno-42-14>)
           [](<https://adk.dev/context/#__codelineno-42-15>)func saveDocRef(tc agent.Context, args saveDocRefArgs) (saveDocRefResult, error) {
           [](<https://adk.dev/context/#__codelineno-42-16>)    artifactPart := genai.NewPartFromText(args.FilePath)
           [](<https://adk.dev/context/#__codelineno-42-17>)    _, err := tc.Artifacts().Save(tc, "document_to_summarize.txt", artifactPart)
           [](<https://adk.dev/context/#__codelineno-42-18>)    if err != nil {
           [](<https://adk.dev/context/#__codelineno-42-19>)        return saveDocRefResult{}, err
           [](<https://adk.dev/context/#__codelineno-42-20>)    }
           [](<https://adk.dev/context/#__codelineno-42-21>)    fmt.Printf("Saved document reference '%s' as artifact\n", args.FilePath)
           [](<https://adk.dev/context/#__codelineno-42-22>)    if err := tc.State().Set("temp:doc_artifact_name", "document_to_summarize.txt"); err != nil {
           [](<https://adk.dev/context/#__codelineno-42-23>)        return saveDocRefResult{}, fmt.Errorf("failed to set artifact name in state")
           [](<https://adk.dev/context/#__codelineno-42-24>)    }
           [](<https://adk.dev/context/#__codelineno-42-25>)    return saveDocRefResult{"Reference saved"}, nil
           [](<https://adk.dev/context/#__codelineno-42-26>)}
           
           [](<https://adk.dev/context/#__codelineno-43-1>)// Example: In a callback or initial tool
           [](<https://adk.dev/context/#__codelineno-43-2>)import com.google.adk.agents.CallbackContext;
           [](<https://adk.dev/context/#__codelineno-43-3>)import com.google.genai.types.Content;
           [](<https://adk.dev/context/#__codelineno-43-4>)import com.google.genai.types.Part;
           [](<https://adk.dev/context/#__codelineno-43-5>)import java.util.Optional;
           [](<https://adk.dev/context/#__codelineno-43-6>)
           [](<https://adk.dev/context/#__codelineno-43-7>)public void saveDocumentReference(CallbackContext context, String filePath) {
           [](<https://adk.dev/context/#__codelineno-43-8>)    // Assume file_path is something like "gs://my-bucket/docs/report.pdf" or "/local/path/to/report.pdf"
           [](<https://adk.dev/context/#__codelineno-43-9>)    try {
           [](<https://adk.dev/context/#__codelineno-43-10>)        // Create a Part containing the path/URI text
           [](<https://adk.dev/context/#__codelineno-43-11>)        Part artifactPart = Part.fromText(filePath);
           [](<https://adk.dev/context/#__codelineno-43-12>)        Optional<Integer> version = context.saveArtifact("document_to_summarize.txt", artifactPart);
           [](<https://adk.dev/context/#__codelineno-43-13>)        System.out.println("Saved document reference" + filePath + " as artifact version " + version.orElse(-1));
           [](<https://adk.dev/context/#__codelineno-43-14>)        // Store the filename in state if needed by other tools
           [](<https://adk.dev/context/#__codelineno-43-15>)        context.state().put("temp:doc_artifact_name", "document_to_summarize.txt");
           [](<https://adk.dev/context/#__codelineno-43-16>)    } catch (Exception e) {
           [](<https://adk.dev/context/#__codelineno-43-17>)        System.out.println("Unexpected error saving artifact reference: " + e);
           [](<https://adk.dev/context/#__codelineno-43-18>)    }
           [](<https://adk.dev/context/#__codelineno-43-19>)}
           [](<https://adk.dev/context/#__codelineno-43-20>)
           [](<https://adk.dev/context/#__codelineno-43-21>)// Example usage:
           [](<https://adk.dev/context/#__codelineno-43-22>)// saveDocumentReference(context, "gs://my-bucket/docs/report.pdf")
           
    2. **Summarizer Tool:** Load the artifact to get the path/URI, read the actual document content using appropriate libraries, summarize, and return the result.

PythonTypeScriptGoJava
           
           [](<https://adk.dev/context/#__codelineno-44-1>)# Example: In the Summarizer tool function
           [](<https://adk.dev/context/#__codelineno-44-2>)from google.adk.tools import ToolContext
           [](<https://adk.dev/context/#__codelineno-44-3>)from google.genai import types
           [](<https://adk.dev/context/#__codelineno-44-4>)# Assume libraries like google.cloud.storage or built-in open are available
           [](<https://adk.dev/context/#__codelineno-44-5>)# Assume a 'summarize_text' function exists
           [](<https://adk.dev/context/#__codelineno-44-6>)# from my_summarizer_lib import summarize_text
           [](<https://adk.dev/context/#__codelineno-44-7>)
           [](<https://adk.dev/context/#__codelineno-44-8>)def summarize_document_tool(tool_context: ToolContext) -> dict:
           [](<https://adk.dev/context/#__codelineno-44-9>)    artifact_name = tool_context.state.get("temp:doc_artifact_name")
           [](<https://adk.dev/context/#__codelineno-44-10>)    if not artifact_name:
           [](<https://adk.dev/context/#__codelineno-44-11>)        return {"error": "Document artifact name not found in state."}
           [](<https://adk.dev/context/#__codelineno-44-12>)
           [](<https://adk.dev/context/#__codelineno-44-13>)    try:
           [](<https://adk.dev/context/#__codelineno-44-14>)        # 1. Load the artifact part containing the path/URI
           [](<https://adk.dev/context/#__codelineno-44-15>)        artifact_part = tool_context.load_artifact(artifact_name)
           [](<https://adk.dev/context/#__codelineno-44-16>)        if not artifact_part or not artifact_part.text:
           [](<https://adk.dev/context/#__codelineno-44-17>)            return {"error": f"Could not load artifact or artifact has no text path: {artifact_name}"}
           [](<https://adk.dev/context/#__codelineno-44-18>)
           [](<https://adk.dev/context/#__codelineno-44-19>)        file_path = artifact_part.text
           [](<https://adk.dev/context/#__codelineno-44-20>)        print(f"Loaded document reference: {file_path}")
           [](<https://adk.dev/context/#__codelineno-44-21>)
           [](<https://adk.dev/context/#__codelineno-44-22>)        # 2. Read the actual document content (outside ADK context)
           [](<https://adk.dev/context/#__codelineno-44-23>)        document_content = ""
           [](<https://adk.dev/context/#__codelineno-44-24>)        if file_path.startswith("gs://"):
           [](<https://adk.dev/context/#__codelineno-44-25>)            # Example: Use GCS client library to download/read
           [](<https://adk.dev/context/#__codelineno-44-26>)            pass # Replace with actual GCS reading logic
           [](<https://adk.dev/context/#__codelineno-44-27>)        elif file_path.startswith("/"):
           [](<https://adk.dev/context/#__codelineno-44-28>)             # Example: Use local file system
           [](<https://adk.dev/context/#__codelineno-44-29>)             with open(file_path, 'r', encoding='utf-8') as f:
           [](<https://adk.dev/context/#__codelineno-44-30>)                 document_content = f.read()
           [](<https://adk.dev/context/#__codelineno-44-31>)        else:
           [](<https://adk.dev/context/#__codelineno-44-32>)            return {"error": f"Unsupported file path scheme: {file_path}"}
           [](<https://adk.dev/context/#__codelineno-44-33>)
           [](<https://adk.dev/context/#__codelineno-44-34>)        # 3. Summarize the content
           [](<https://adk.dev/context/#__codelineno-44-35>)        if not document_content:
           [](<https://adk.dev/context/#__codelineno-44-36>)             return {"error": "Failed to read document content."}
           [](<https://adk.dev/context/#__codelineno-44-37>)
           [](<https://adk.dev/context/#__codelineno-44-38>)        # summary = summarize_text(document_content) # Call your summarization logic
           [](<https://adk.dev/context/#__codelineno-44-39>)        summary = f"Summary of content from {file_path}" # Placeholder
           [](<https://adk.dev/context/#__codelineno-44-40>)
           [](<https://adk.dev/context/#__codelineno-44-41>)        return {"summary": summary}
           [](<https://adk.dev/context/#__codelineno-44-42>)
           [](<https://adk.dev/context/#__codelineno-44-43>)    except ValueError as e:
           [](<https://adk.dev/context/#__codelineno-44-44>)         return {"error": f"Artifact service error: {e}"}
           [](<https://adk.dev/context/#__codelineno-44-45>)    except FileNotFoundError:
           [](<https://adk.dev/context/#__codelineno-44-46>)         return {"error": f"Local file not found: {file_path}"}
           
           [](<https://adk.dev/context/#__codelineno-45-1>)// Pseudocode: In the Summarizer tool function
           [](<https://adk.dev/context/#__codelineno-45-2>)import { Context } from '@google/adk';
           [](<https://adk.dev/context/#__codelineno-45-3>)
           [](<https://adk.dev/context/#__codelineno-45-4>)async function summarizeDocumentTool(context: Context): Promise<Record<string, string>> {
           [](<https://adk.dev/context/#__codelineno-45-5>)  const artifactName = context.state.get('temp:doc_artifact_name') as string;
           [](<https://adk.dev/context/#__codelineno-45-6>)  if (!artifactName) {
           [](<https://adk.dev/context/#__codelineno-45-7>)    return { error: 'Document artifact name not found in state.' };
           [](<https://adk.dev/context/#__codelineno-45-8>)  }
           [](<https://adk.dev/context/#__codelineno-45-9>)
           [](<https://adk.dev/context/#__codelineno-45-10>)  try {
           [](<https://adk.dev/context/#__codelineno-45-11>)    // 1. Load the artifact part containing the path/URI
           [](<https://adk.dev/context/#__codelineno-45-12>)    const artifactPart = await context.loadArtifact(artifactName);
           [](<https://adk.dev/context/#__codelineno-45-13>)    if (!artifactPart?.text) {
           [](<https://adk.dev/context/#__codelineno-45-14>)      return { error: `Could not load artifact or artifact has no text path: ${artifactName}` };
           [](<https://adk.dev/context/#__codelineno-45-15>)    }
           [](<https://adk.dev/context/#__codelineno-45-16>)
           [](<https://adk.dev/context/#__codelineno-45-17>)    const filePath = artifactPart.text;
           [](<https://adk.dev/context/#__codelineno-45-18>)    console.log(`Loaded document reference: ${filePath}`);
           [](<https://adk.dev/context/#__codelineno-45-19>)
           [](<https://adk.dev/context/#__codelineno-45-20>)    // 2. Read the actual document content (outside ADK context)
           [](<https://adk.dev/context/#__codelineno-45-21>)    let documentContent = '';
           [](<https://adk.dev/context/#__codelineno-45-22>)    if (filePath.startsWith('gs://')) {
           [](<https://adk.dev/context/#__codelineno-45-23>)      // Example: Use GCS client library to download/read
           [](<https://adk.dev/context/#__codelineno-45-24>)      // const storage = new Storage();
           [](<https://adk.dev/context/#__codelineno-45-25>)      // const bucket = storage.bucket('my-bucket');
           [](<https://adk.dev/context/#__codelineno-45-26>)      // const file = bucket.file(filePath.replace('gs://my-bucket/', ''));
           [](<https://adk.dev/context/#__codelineno-45-27>)      // const [contents] = await file.download();
           [](<https://adk.dev/context/#__codelineno-45-28>)      // documentContent = contents.toString();
           [](<https://adk.dev/context/#__codelineno-45-29>)    } else if (filePath.startsWith('/')) {
           [](<https://adk.dev/context/#__codelineno-45-30>)      // Example: Use local file system
           [](<https://adk.dev/context/#__codelineno-45-31>)      // import { readFile } from 'fs/promises';
           [](<https://adk.dev/context/#__codelineno-45-32>)      // documentContent = await readFile(filePath, 'utf8');
           [](<https://adk.dev/context/#__codelineno-45-33>)    } else {
           [](<https://adk.dev/context/#__codelineno-45-34>)      return { error: `Unsupported file path scheme: ${filePath}` };
           [](<https://adk.dev/context/#__codelineno-45-35>)    }
           [](<https://adk.dev/context/#__codelineno-45-36>)
           [](<https://adk.dev/context/#__codelineno-45-37>)    // 3. Summarize the content
           [](<https://adk.dev/context/#__codelineno-45-38>)    if (!documentContent) {
           [](<https://adk.dev/context/#__codelineno-45-39>)       return { error: 'Failed to read document content.' };
           [](<https://adk.dev/context/#__codelineno-45-40>)    }
           [](<https://adk.dev/context/#__codelineno-45-41>)
           [](<https://adk.dev/context/#__codelineno-45-42>)    // const summary = summarizeText(documentContent); // Call your summarization logic
           [](<https://adk.dev/context/#__codelineno-45-43>)    const summary = `Summary of content from ${filePath}`; // Placeholder
           [](<https://adk.dev/context/#__codelineno-45-44>)
           [](<https://adk.dev/context/#__codelineno-45-45>)    return { summary };
           [](<https://adk.dev/context/#__codelineno-45-46>)
           [](<https://adk.dev/context/#__codelineno-45-47>)  } catch (e) {
           [](<https://adk.dev/context/#__codelineno-45-48>)     return { error: `Error processing artifact: ${e}` };
           [](<https://adk.dev/context/#__codelineno-45-49>)  }
           [](<https://adk.dev/context/#__codelineno-45-50>)}
           
           [](<https://adk.dev/context/#__codelineno-46-1>)import "google.golang.org/adk/v2/tool"
           [](<https://adk.dev/context/#__codelineno-46-2>)
           [](<https://adk.dev/context/#__codelineno-46-3>)// Pseudocode: In the Summarizer tool function
           [](<https://adk.dev/context/#__codelineno-46-4>)type summarizeDocumentArgs struct{}
           [](<https://adk.dev/context/#__codelineno-46-5>)
           [](<https://adk.dev/context/#__codelineno-46-6>)type summarizeDocumentResult struct {
           [](<https://adk.dev/context/#__codelineno-46-7>)    Summary string `json:"summary"`
           [](<https://adk.dev/context/#__codelineno-46-8>)}
           [](<https://adk.dev/context/#__codelineno-46-9>)
           [](<https://adk.dev/context/#__codelineno-46-10>)func summarizeDocumentTool(tc agent.Context, input summarizeDocumentArgs) (summarizeDocumentResult, error) {
           [](<https://adk.dev/context/#__codelineno-46-11>)    artifactName, err := tc.State().Get("temp:doc_artifact_name")
           [](<https://adk.dev/context/#__codelineno-46-12>)    if err != nil {
           [](<https://adk.dev/context/#__codelineno-46-13>)        return summarizeDocumentResult{}, fmt.Errorf("No document artifact name found in state")
           [](<https://adk.dev/context/#__codelineno-46-14>)    }
           [](<https://adk.dev/context/#__codelineno-46-15>)
           [](<https://adk.dev/context/#__codelineno-46-16>)    // 1. Load the artifact part containing the path/URI
           [](<https://adk.dev/context/#__codelineno-46-17>)    artifactPart, err := tc.Artifacts().Load(tc, artifactName.(string))
           [](<https://adk.dev/context/#__codelineno-46-18>)    if err != nil {
           [](<https://adk.dev/context/#__codelineno-46-19>)        return summarizeDocumentResult{}, err
           [](<https://adk.dev/context/#__codelineno-46-20>)    }
           [](<https://adk.dev/context/#__codelineno-46-21>)
           [](<https://adk.dev/context/#__codelineno-46-22>)    if artifactPart.Part.Text == "" {
           [](<https://adk.dev/context/#__codelineno-46-23>)        return summarizeDocumentResult{}, fmt.Errorf("Could not load artifact or artifact has no text path.")
           [](<https://adk.dev/context/#__codelineno-46-24>)    }
           [](<https://adk.dev/context/#__codelineno-46-25>)    filePath := artifactPart.Part.Text
           [](<https://adk.dev/context/#__codelineno-46-26>)    fmt.Printf("Loaded document reference: %s\n", filePath)
           [](<https://adk.dev/context/#__codelineno-46-27>)
           [](<https://adk.dev/context/#__codelineno-46-28>)    // 2. Read the actual document content (outside ADK context)
           [](<https://adk.dev/context/#__codelineno-46-29>)    // In a real implementation, you would use a GCS client or local file reader.
           [](<https://adk.dev/context/#__codelineno-46-30>)    documentContent := "This is the fake content of the document at " + filePath
           [](<https://adk.dev/context/#__codelineno-46-31>)    _ = documentContent // Avoid unused variable error.
           [](<https://adk.dev/context/#__codelineno-46-32>)
           [](<https://adk.dev/context/#__codelineno-46-33>)    // 3. Summarize the content
           [](<https://adk.dev/context/#__codelineno-46-34>)    summary := "Summary of content from " + filePath // Placeholder
           [](<https://adk.dev/context/#__codelineno-46-35>)
           [](<https://adk.dev/context/#__codelineno-46-36>)    return summarizeDocumentResult{Summary: summary}, nil
           [](<https://adk.dev/context/#__codelineno-46-37>)}
           
           [](<https://adk.dev/context/#__codelineno-47-1>)// Example: In the Summarizer tool function
           [](<https://adk.dev/context/#__codelineno-47-2>)import com.google.adk.tools.ToolContext;
           [](<https://adk.dev/context/#__codelineno-47-3>)import com.google.genai.types.Content;
           [](<https://adk.dev/context/#__codelineno-47-4>)import com.google.genai.types.Part;
           [](<https://adk.dev/context/#__codelineno-47-5>)import java.util.Map;
           [](<https://adk.dev/context/#__codelineno-47-6>)import java.util.Optional;
           [](<https://adk.dev/context/#__codelineno-47-7>)import java.io.FileNotFoundException;
           [](<https://adk.dev/context/#__codelineno-47-8>)
           [](<https://adk.dev/context/#__codelineno-47-9>)public Map<String, String> summarizeDocumentTool(ToolContext toolContext) {
           [](<https://adk.dev/context/#__codelineno-47-10>)    String artifactName = (String) toolContext.state().get("temp:doc_artifact_name");
           [](<https://adk.dev/context/#__codelineno-47-11>)    if (artifactName == null || artifactName.isEmpty()) {
           [](<https://adk.dev/context/#__codelineno-47-12>)        return Map.of("error", "Document artifact name not found in state.");
           [](<https://adk.dev/context/#__codelineno-47-13>)    }
           [](<https://adk.dev/context/#__codelineno-47-14>)    try {
           [](<https://adk.dev/context/#__codelineno-47-15>)        // 1. Load the artifact part containing the path/URI
           [](<https://adk.dev/context/#__codelineno-47-16>)        Optional<Part> artifactPart = toolContext.loadArtifact(artifactName);
           [](<https://adk.dev/context/#__codelineno-47-17>)        if (!artifactPart.isPresent() || !artifactPart.get().text().isPresent() || artifactPart.get().text().get().isEmpty()) {
           [](<https://adk.dev/context/#__codelineno-47-18>)            return Map.of("error", "Could not load artifact or artifact has no text path: " + artifactName);
           [](<https://adk.dev/context/#__codelineno-47-19>)        }
           [](<https://adk.dev/context/#__codelineno-47-20>)        String filePath = artifactPart.get().text().get();
           [](<https://adk.dev/context/#__codelineno-47-21>)        System.out.println("Loaded document reference: " + filePath);
           [](<https://adk.dev/context/#__codelineno-47-22>)
           [](<https://adk.dev/context/#__codelineno-47-23>)        // 2. Read the actual document content (outside ADK context)
           [](<https://adk.dev/context/#__codelineno-47-24>)        String documentContent = "";
           [](<https://adk.dev/context/#__codelineno-47-25>)        if (filePath.startsWith("gs://")) {
           [](<https://adk.dev/context/#__codelineno-47-26>)            // Example: Use GCS client library to download/read into documentContent
           [](<https://adk.dev/context/#__codelineno-47-27>)            // Replace with actual GCS reading logic
           [](<https://adk.dev/context/#__codelineno-47-28>)        } else if (filePath.startsWith("/")) {
           [](<https://adk.dev/context/#__codelineno-47-29>)            // Example: Use local file system to download/read into documentContent
           [](<https://adk.dev/context/#__codelineno-47-30>)        } else {
           [](<https://adk.dev/context/#__codelineno-47-31>)            return Map.of("error", "Unsupported file path scheme: " + filePath);
           [](<https://adk.dev/context/#__codelineno-47-32>)        }
           [](<https://adk.dev/context/#__codelineno-47-33>)
           [](<https://adk.dev/context/#__codelineno-47-34>)        // 3. Summarize the content
           [](<https://adk.dev/context/#__codelineno-47-35>)        if (documentContent.isEmpty()) {
           [](<https://adk.dev/context/#__codelineno-47-36>)            return Map.of("error", "Failed to read document content.");
           [](<https://adk.dev/context/#__codelineno-47-37>)        }
           [](<https://adk.dev/context/#__codelineno-47-38>)
           [](<https://adk.dev/context/#__codelineno-47-39>)        // summary = summarizeText(documentContent) // Call your summarization logic
           [](<https://adk.dev/context/#__codelineno-47-40>)        String summary = "Summary of content from " + filePath; // Placeholder
           [](<https://adk.dev/context/#__codelineno-47-41>)
           [](<https://adk.dev/context/#__codelineno-47-42>)        return Map.of("summary", summary);
           [](<https://adk.dev/context/#__codelineno-47-43>)    } catch (IllegalArgumentException e) {
           [](<https://adk.dev/context/#__codelineno-47-44>)        return Map.of("error", "Artifact service error " + e);
           [](<https://adk.dev/context/#__codelineno-47-45>)    } catch (Exception e) {
           [](<https://adk.dev/context/#__codelineno-47-46>)        return Map.of("error", "Error reading document " + e);
           [](<https://adk.dev/context/#__codelineno-47-47>)    }
           [](<https://adk.dev/context/#__codelineno-47-48>)}
           
  * **List Artifacts:** Discover what files are available.

PythonTypeScriptGoJava
        
        [](<https://adk.dev/context/#__codelineno-48-1>)# Example: In a tool function
        [](<https://adk.dev/context/#__codelineno-48-2>)from google.adk.tools import ToolContext
        [](<https://adk.dev/context/#__codelineno-48-3>)
        [](<https://adk.dev/context/#__codelineno-48-4>)def check_available_docs(tool_context: ToolContext) -> dict:
        [](<https://adk.dev/context/#__codelineno-48-5>)    try:
        [](<https://adk.dev/context/#__codelineno-48-6>)        artifact_keys = tool_context.list_artifacts()
        [](<https://adk.dev/context/#__codelineno-48-7>)        print(f"Available artifacts: {artifact_keys}")
        [](<https://adk.dev/context/#__codelineno-48-8>)        return {"available_docs": artifact_keys}
        [](<https://adk.dev/context/#__codelineno-48-9>)    except ValueError as e:
        [](<https://adk.dev/context/#__codelineno-48-10>)        return {"error": f"Artifact service error: {e}"}
        
        [](<https://adk.dev/context/#__codelineno-49-1>)// Pseudocode: In a tool function
        [](<https://adk.dev/context/#__codelineno-49-2>)import { Context } from '@google/adk';
        [](<https://adk.dev/context/#__codelineno-49-3>)
        [](<https://adk.dev/context/#__codelineno-49-4>)async function checkAvailableDocs(context: Context): Promise<Record<string, string[] | string>> {
        [](<https://adk.dev/context/#__codelineno-49-5>)  try {
        [](<https://adk.dev/context/#__codelineno-49-6>)    const artifactKeys = await context.listArtifacts();
        [](<https://adk.dev/context/#__codelineno-49-7>)    console.log(`Available artifacts: ${artifactKeys}`);
        [](<https://adk.dev/context/#__codelineno-49-8>)    return { available_docs: artifactKeys };
        [](<https://adk.dev/context/#__codelineno-49-9>)  } catch (e) {
        [](<https://adk.dev/context/#__codelineno-49-10>)    return { error: `Artifact service error: ${e}` };
        [](<https://adk.dev/context/#__codelineno-49-11>)  }
        [](<https://adk.dev/context/#__codelineno-49-12>)}
        
        [](<https://adk.dev/context/#__codelineno-50-1>)import "google.golang.org/adk/v2/tool"
        [](<https://adk.dev/context/#__codelineno-50-2>)
        [](<https://adk.dev/context/#__codelineno-50-3>)// Pseudocode: In a tool function
        [](<https://adk.dev/context/#__codelineno-50-4>)type checkAvailableDocsArgs struct{}
        [](<https://adk.dev/context/#__codelineno-50-5>)
        [](<https://adk.dev/context/#__codelineno-50-6>)type checkAvailableDocsResult struct {
        [](<https://adk.dev/context/#__codelineno-50-7>)    AvailableDocs []string `json:"available_docs"`
        [](<https://adk.dev/context/#__codelineno-50-8>)}
        [](<https://adk.dev/context/#__codelineno-50-9>)
        [](<https://adk.dev/context/#__codelineno-50-10>)func checkAvailableDocs(tc agent.Context, args checkAvailableDocsArgs) (checkAvailableDocsResult, error) {
        [](<https://adk.dev/context/#__codelineno-50-11>)    artifactKeys, err := tc.Artifacts().List(tc)
        [](<https://adk.dev/context/#__codelineno-50-12>)    if err != nil {
        [](<https://adk.dev/context/#__codelineno-50-13>)        return checkAvailableDocsResult{}, err
        [](<https://adk.dev/context/#__codelineno-50-14>)    }
        [](<https://adk.dev/context/#__codelineno-50-15>)    fmt.Printf("Available artifacts: %v\n", artifactKeys)
        [](<https://adk.dev/context/#__codelineno-50-16>)    return checkAvailableDocsResult{AvailableDocs: artifactKeys.FileNames}, nil
        [](<https://adk.dev/context/#__codelineno-50-17>)}
        
        [](<https://adk.dev/context/#__codelineno-51-1>)// Example: In a tool function
        [](<https://adk.dev/context/#__codelineno-51-2>)import com.google.adk.tools.ToolContext;
        [](<https://adk.dev/context/#__codelineno-51-3>)import io.reactivex.rxjava3.core.Single;
        [](<https://adk.dev/context/#__codelineno-51-4>)import java.util.List;
        [](<https://adk.dev/context/#__codelineno-51-5>)import java.util.Map;
        [](<https://adk.dev/context/#__codelineno-51-6>)
        [](<https://adk.dev/context/#__codelineno-51-7>)public Map<String, Object> checkAvailableDocs(ToolContext toolContext) {
        [](<https://adk.dev/context/#__codelineno-51-8>)    try {
        [](<https://adk.dev/context/#__codelineno-51-9>)        Single<List<String>> artifactKeys = toolContext.listArtifacts();
        [](<https://adk.dev/context/#__codelineno-51-10>)        System.out.println("Available artifacts: " + artifactKeys.blockingGet().toString());
        [](<https://adk.dev/context/#__codelineno-51-11>)        return Map.of("availableDocs", artifactKeys.blockingGet());
        [](<https://adk.dev/context/#__codelineno-51-12>)    } catch (IllegalArgumentException e) {
        [](<https://adk.dev/context/#__codelineno-51-13>)        return Map.of("error", "Artifact service error: " + e);
        [](<https://adk.dev/context/#__codelineno-51-14>)    }
        [](<https://adk.dev/context/#__codelineno-51-15>)}
        
### Handle tool authentication[¶](<https://adk.dev/context/#handle-tool-authentication> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Java v0.2.0

Securely manage API keys or other credentials needed by tools.

PythonTypeScriptJava
    
    [](<https://adk.dev/context/#__codelineno-52-1>)# Example: Tool requiring auth
    [](<https://adk.dev/context/#__codelineno-52-2>)from google.adk.tools import ToolContext
    [](<https://adk.dev/context/#__codelineno-52-3>)from google.adk.auth import AuthConfig # Assume appropriate AuthConfig is defined
    [](<https://adk.dev/context/#__codelineno-52-4>)
    [](<https://adk.dev/context/#__codelineno-52-5>)# Define your required auth configuration (e.g., OAuth, API Key)
    [](<https://adk.dev/context/#__codelineno-52-6>)MY_API_AUTH_CONFIG = AuthConfig(...)
    [](<https://adk.dev/context/#__codelineno-52-7>)AUTH_STATE_KEY = "user:my_api_credential" # Key to store retrieved credential
    [](<https://adk.dev/context/#__codelineno-52-8>)
    [](<https://adk.dev/context/#__codelineno-52-9>)def call_secure_api(tool_context: ToolContext, request_data: str) -> dict:
    [](<https://adk.dev/context/#__codelineno-52-10>)    # 1. Check if credential already exists in state
    [](<https://adk.dev/context/#__codelineno-52-11>)    credential = tool_context.state.get(AUTH_STATE_KEY)
    [](<https://adk.dev/context/#__codelineno-52-12>)
    [](<https://adk.dev/context/#__codelineno-52-13>)    if not credential:
    [](<https://adk.dev/context/#__codelineno-52-14>)        # 2. If not, request it
    [](<https://adk.dev/context/#__codelineno-52-15>)        print("Credential not found, requesting...")
    [](<https://adk.dev/context/#__codelineno-52-16>)        try:
    [](<https://adk.dev/context/#__codelineno-52-17>)            tool_context.request_credential(MY_API_AUTH_CONFIG)
    [](<https://adk.dev/context/#__codelineno-52-18>)            # The framework handles yielding the event. The tool execution stops here for this turn.
    [](<https://adk.dev/context/#__codelineno-52-19>)            return {"status": "Authentication required. Please provide credentials."}
    [](<https://adk.dev/context/#__codelineno-52-20>)        except ValueError as e:
    [](<https://adk.dev/context/#__codelineno-52-21>)            return {"error": f"Auth error: {e}"} # e.g., function_call_id missing
    [](<https://adk.dev/context/#__codelineno-52-22>)        except Exception as e:
    [](<https://adk.dev/context/#__codelineno-52-23>)            return {"error": f"Failed to request credential: {e}"}
    [](<https://adk.dev/context/#__codelineno-52-24>)
    [](<https://adk.dev/context/#__codelineno-52-25>)    # 3. If credential exists (might be from a previous turn after request)
    [](<https://adk.dev/context/#__codelineno-52-26>)    #    or if this is a subsequent call after auth flow completed externally
    [](<https://adk.dev/context/#__codelineno-52-27>)    try:
    [](<https://adk.dev/context/#__codelineno-52-28>)        # Optionally, re-validate/retrieve if needed, or use directly
    [](<https://adk.dev/context/#__codelineno-52-29>)        # This might retrieve the credential if the external flow just completed
    [](<https://adk.dev/context/#__codelineno-52-30>)        auth_credential_obj = tool_context.get_auth_response(MY_API_AUTH_CONFIG)
    [](<https://adk.dev/context/#__codelineno-52-31>)        api_key = auth_credential_obj.api_key # Or access_token, etc.
    [](<https://adk.dev/context/#__codelineno-52-32>)
    [](<https://adk.dev/context/#__codelineno-52-33>)        # Store it back in state for future calls within the session
    [](<https://adk.dev/context/#__codelineno-52-34>)        tool_context.state[AUTH_STATE_KEY] = auth_credential_obj.model_dump() # Persist retrieved credential
    [](<https://adk.dev/context/#__codelineno-52-35>)
    [](<https://adk.dev/context/#__codelineno-52-36>)        print(f"Using retrieved credential to call API with data: {request_data}")
    [](<https://adk.dev/context/#__codelineno-52-37>)        # ... Make the actual API call using api_key ...
    [](<https://adk.dev/context/#__codelineno-52-38>)        api_result = f"API result for {request_data}"
    [](<https://adk.dev/context/#__codelineno-52-39>)
    [](<https://adk.dev/context/#__codelineno-52-40>)        return {"result": api_result}
    [](<https://adk.dev/context/#__codelineno-52-41>)    except Exception as e:
    [](<https://adk.dev/context/#__codelineno-52-42>)        # Handle errors retrieving/using the credential
    [](<https://adk.dev/context/#__codelineno-52-43>)        print(f"Error using credential: {e}")
    [](<https://adk.dev/context/#__codelineno-52-44>)        # Maybe clear the state key if credential is invalid?
    [](<https://adk.dev/context/#__codelineno-52-45>)        # tool_context.state[AUTH_STATE_KEY] = None
    [](<https://adk.dev/context/#__codelineno-52-46>)        return {"error": "Failed to use credential"}
    
    [](<https://adk.dev/context/#__codelineno-53-1>)// Pseudocode: Tool requiring auth
    [](<https://adk.dev/context/#__codelineno-53-2>)import { Context } from '@google/adk'; // AuthConfig from ADK or custom
    [](<https://adk.dev/context/#__codelineno-53-3>)
    [](<https://adk.dev/context/#__codelineno-53-4>)// Define a local AuthConfig interface as it's not publicly exported by ADK
    [](<https://adk.dev/context/#__codelineno-53-5>)interface AuthConfig {
    [](<https://adk.dev/context/#__codelineno-53-6>)  credentialKey: string;
    [](<https://adk.dev/context/#__codelineno-53-7>)  authScheme: { type: string }; // Minimal representation for the example
    [](<https://adk.dev/context/#__codelineno-53-8>)  // Add other properties if they become relevant for the example
    [](<https://adk.dev/context/#__codelineno-53-9>)}
    [](<https://adk.dev/context/#__codelineno-53-10>)
    [](<https://adk.dev/context/#__codelineno-53-11>)// Define your required auth configuration (e.g., OAuth, API Key)
    [](<https://adk.dev/context/#__codelineno-53-12>)const MY_API_AUTH_CONFIG: AuthConfig = {
    [](<https://adk.dev/context/#__codelineno-53-13>)  credentialKey: 'my-api-key', // Example key
    [](<https://adk.dev/context/#__codelineno-53-14>)  authScheme: { type: 'api-key' }, // Example scheme type
    [](<https://adk.dev/context/#__codelineno-53-15>)};
    [](<https://adk.dev/context/#__codelineno-53-16>)const AUTH_STATE_KEY = 'user:my_api_credential'; // Key to store retrieved credential
    [](<https://adk.dev/context/#__codelineno-53-17>)
    [](<https://adk.dev/context/#__codelineno-53-18>)async function callSecureApi(context: Context, requestData: string): Promise<Record<string, string>> {
    [](<https://adk.dev/context/#__codelineno-53-19>)  // 1. Check if credential already exists in state
    [](<https://adk.dev/context/#__codelineno-53-20>)  const credential = context.state.get(AUTH_STATE_KEY);
    [](<https://adk.dev/context/#__codelineno-53-21>)
    [](<https://adk.dev/context/#__codelineno-53-22>)  if (!credential) {
    [](<https://adk.dev/context/#__codelineno-53-23>)    // 2. If not, request it
    [](<https://adk.dev/context/#__codelineno-53-24>)    console.log('Credential not found, requesting...');
    [](<https://adk.dev/context/#__codelineno-53-25>)    try {
    [](<https://adk.dev/context/#__codelineno-53-26>)      context.requestCredential(MY_API_AUTH_CONFIG);
    [](<https://adk.dev/context/#__codelineno-53-27>)      // The framework handles yielding the event. The tool execution stops here for this turn.
    [](<https://adk.dev/context/#__codelineno-53-28>)      return { status: 'Authentication required. Please provide credentials.' };
    [](<https://adk.dev/context/#__codelineno-53-29>)    } catch (e) {
    [](<https://adk.dev/context/#__codelineno-53-30>)      return { error: `Auth or credential request error: ${e}` };
    [](<https://adk.dev/context/#__codelineno-53-31>)    }
    [](<https://adk.dev/context/#__codelineno-53-32>)  }
    [](<https://adk.dev/context/#__codelineno-53-33>)
    [](<https://adk.dev/context/#__codelineno-53-34>)  // 3. If credential exists (might be from a previous turn after request)
    [](<https://adk.dev/context/#__codelineno-53-35>)  //    or if this is a subsequent call after auth flow completed externally
    [](<https://adk.dev/context/#__codelineno-53-36>)  try {
    [](<https://adk.dev/context/#__codelineno-53-37>)    // Optionally, re-validate/retrieve if needed, or use directly
    [](<https://adk.dev/context/#__codelineno-53-38>)    // This might retrieve the credential if the external flow just completed
    [](<https://adk.dev/context/#__codelineno-53-39>)    const authCredentialObj = context.getAuthResponse(MY_API_AUTH_CONFIG);
    [](<https://adk.dev/context/#__codelineno-53-40>)    const apiKey = authCredentialObj?.apiKey; // Or accessToken, etc.
    [](<https://adk.dev/context/#__codelineno-53-41>)
    [](<https://adk.dev/context/#__codelineno-53-42>)    // Store it back in state for future calls within the session
    [](<https://adk.dev/context/#__codelineno-53-43>)    // Note: In strict TS, might need to cast or serialize authCredentialObj
    [](<https://adk.dev/context/#__codelineno-53-44>)    context.state.set(AUTH_STATE_KEY, JSON.stringify(authCredentialObj));
    [](<https://adk.dev/context/#__codelineno-53-45>)
    [](<https://adk.dev/context/#__codelineno-53-46>)    console.log(`Using retrieved credential to call API with data: ${requestData}`);
    [](<https://adk.dev/context/#__codelineno-53-47>)    // ... Make the actual API call using apiKey ...
    [](<https://adk.dev/context/#__codelineno-53-48>)    const apiResult = `API result for ${requestData}`;
    [](<https://adk.dev/context/#__codelineno-53-49>)
    [](<https://adk.dev/context/#__codelineno-53-50>)    return { result: apiResult };
    [](<https://adk.dev/context/#__codelineno-53-51>)  } catch (e) {
    [](<https://adk.dev/context/#__codelineno-53-52>)    // Handle errors retrieving/using the credential
    [](<https://adk.dev/context/#__codelineno-53-53>)    console.error(`Error using credential: ${e}`);
    [](<https://adk.dev/context/#__codelineno-53-54>)    // Maybe clear the state key if credential is invalid?
    [](<https://adk.dev/context/#__codelineno-53-55>)    // toolContext.state.set(AUTH_STATE_KEY, null);
    [](<https://adk.dev/context/#__codelineno-53-56>)    return { error: 'Failed to use credential' };
    [](<https://adk.dev/context/#__codelineno-53-57>)  }
    [](<https://adk.dev/context/#__codelineno-53-58>)}
    
    [](<https://adk.dev/context/#__codelineno-54-1>)// Example: Tool requiring auth
    [](<https://adk.dev/context/#__codelineno-54-2>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/context/#__codelineno-54-3>)import java.util.Map;
    [](<https://adk.dev/context/#__codelineno-54-4>)
    [](<https://adk.dev/context/#__codelineno-54-5>)// Note: AuthConfig, requestCredential, and getAuthResponse are not yet
    [](<https://adk.dev/context/#__codelineno-54-6>)// fully implemented in the Java ADK public API.
    [](<https://adk.dev/context/#__codelineno-54-7>)// This example relies on external auth population into the session state.
    [](<https://adk.dev/context/#__codelineno-54-8>)
    [](<https://adk.dev/context/#__codelineno-54-9>)public class SecureApiTool {
    [](<https://adk.dev/context/#__codelineno-54-10>)  private static final String AUTH_STATE_KEY = "user:my_api_credential";
    [](<https://adk.dev/context/#__codelineno-54-11>)
    [](<https://adk.dev/context/#__codelineno-54-12>)  public Map<String, String> callSecureApi(ToolContext context, String requestData) {
    [](<https://adk.dev/context/#__codelineno-54-13>)    // 1. Check if credential already exists in state
    [](<https://adk.dev/context/#__codelineno-54-14>)    Object credential = context.state().get(AUTH_STATE_KEY);
    [](<https://adk.dev/context/#__codelineno-54-15>)
    [](<https://adk.dev/context/#__codelineno-54-16>)    if (credential == null) {
    [](<https://adk.dev/context/#__codelineno-54-17>)      // 2. If not, request it
    [](<https://adk.dev/context/#__codelineno-54-18>)      System.out.println("Credential not found, requesting...");
    [](<https://adk.dev/context/#__codelineno-54-19>)      try {
    [](<https://adk.dev/context/#__codelineno-54-20>)        // context.requestCredential(MY_API_AUTH_CONFIG); // Not yet implemented in Java ADK
    [](<https://adk.dev/context/#__codelineno-54-21>)        // The framework handles yielding the event. The tool execution stops here for this turn.
    [](<https://adk.dev/context/#__codelineno-54-22>)        return Map.of("status", "Authentication required. Please provide credentials.");
    [](<https://adk.dev/context/#__codelineno-54-23>)      } catch (Exception e) {
    [](<https://adk.dev/context/#__codelineno-54-24>)        return Map.of("error", "Auth or credential request error: " + e.getMessage());
    [](<https://adk.dev/context/#__codelineno-54-25>)      }
    [](<https://adk.dev/context/#__codelineno-54-26>)    }
    [](<https://adk.dev/context/#__codelineno-54-27>)
    [](<https://adk.dev/context/#__codelineno-54-28>)    // 3. If credential exists (might be from a previous turn after request)
    [](<https://adk.dev/context/#__codelineno-54-29>)    //    or if this is a subsequent call after auth flow completed externally
    [](<https://adk.dev/context/#__codelineno-54-30>)    try {
    [](<https://adk.dev/context/#__codelineno-54-31>)      // Optionally, re-validate/retrieve if needed, or use directly
    [](<https://adk.dev/context/#__codelineno-54-32>)      // String apiKey = context.getAuthResponse(MY_API_AUTH_CONFIG).getApiKey();
    [](<https://adk.dev/context/#__codelineno-54-33>)      String apiKey = credential.toString(); // Simplified for example
    [](<https://adk.dev/context/#__codelineno-54-34>)
    [](<https://adk.dev/context/#__codelineno-54-35>)      // Store it back in state for future calls within the session
    [](<https://adk.dev/context/#__codelineno-54-36>)      context.state().put(AUTH_STATE_KEY, apiKey);
    [](<https://adk.dev/context/#__codelineno-54-37>)
    [](<https://adk.dev/context/#__codelineno-54-38>)      System.out.println("Using retrieved credential to call API with data: " + requestData);
    [](<https://adk.dev/context/#__codelineno-54-39>)      // ... Make the actual API call using apiKey ...
    [](<https://adk.dev/context/#__codelineno-54-40>)      String apiResult = "API result for " + requestData;
    [](<https://adk.dev/context/#__codelineno-54-41>)
    [](<https://adk.dev/context/#__codelineno-54-42>)      return Map.of("result", apiResult);
    [](<https://adk.dev/context/#__codelineno-54-43>)    } catch (Exception e) {
    [](<https://adk.dev/context/#__codelineno-54-44>)      // Handle errors retrieving/using the credential
    [](<https://adk.dev/context/#__codelineno-54-45>)      System.err.println("Error using credential: " + e.getMessage());
    [](<https://adk.dev/context/#__codelineno-54-46>)      return Map.of("error", "Failed to use credential");
    [](<https://adk.dev/context/#__codelineno-54-47>)    }
    [](<https://adk.dev/context/#__codelineno-54-48>)  }
    [](<https://adk.dev/context/#__codelineno-54-49>)}
    
_Remember:`request_credential` pauses the tool and signals the need for authentication. The user/system provides credentials, and on a subsequent call, `get_auth_response` (or checking state again) allows the tool to proceed._ The `tool_context.function_call_id` is used implicitly by the framework to link the request and response.

### Leveraging Memory[¶](<https://adk.dev/context/#leveraging-memory> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Java v0.2.0

Access relevant information from the past or external sources.

PythonTypeScriptJava
    
    [](<https://adk.dev/context/#__codelineno-55-1>)# Example: Tool using memory search
    [](<https://adk.dev/context/#__codelineno-55-2>)from google.adk.tools import ToolContext
    [](<https://adk.dev/context/#__codelineno-55-3>)
    [](<https://adk.dev/context/#__codelineno-55-4>)def find_related_info(tool_context: ToolContext, topic: str) -> dict:
    [](<https://adk.dev/context/#__codelineno-55-5>)    try:
    [](<https://adk.dev/context/#__codelineno-55-6>)        search_results = tool_context.search_memory(f"Information about {topic}")
    [](<https://adk.dev/context/#__codelineno-55-7>)        if search_results.results:
    [](<https://adk.dev/context/#__codelineno-55-8>)            print(f"Found {len(search_results.results)} memory results for '{topic}'")
    [](<https://adk.dev/context/#__codelineno-55-9>)            # Process search_results.results (which are SearchMemoryResponseEntry)
    [](<https://adk.dev/context/#__codelineno-55-10>)            top_result_text = search_results.results[0].text
    [](<https://adk.dev/context/#__codelineno-55-11>)            return {"memory_snippet": top_result_text}
    [](<https://adk.dev/context/#__codelineno-55-12>)        else:
    [](<https://adk.dev/context/#__codelineno-55-13>)            return {"message": "No relevant memories found."}
    [](<https://adk.dev/context/#__codelineno-55-14>)    except ValueError as e:
    [](<https://adk.dev/context/#__codelineno-55-15>)        return {"error": f"Memory service error: {e}"} # e.g., Service not configured
    [](<https://adk.dev/context/#__codelineno-55-16>)    except Exception as e:
    [](<https://adk.dev/context/#__codelineno-55-17>)        return {"error": f"Unexpected error searching memory: {e}"}
    
    [](<https://adk.dev/context/#__codelineno-56-1>)// Pseudocode: Tool using memory search
    [](<https://adk.dev/context/#__codelineno-56-2>)import { Context } from '@google/adk';
    [](<https://adk.dev/context/#__codelineno-56-3>)
    [](<https://adk.dev/context/#__codelineno-56-4>)async function findRelatedInfo(context: Context, topic: string): Promise<Record<string, string>> {
    [](<https://adk.dev/context/#__codelineno-56-5>)  try {
    [](<https://adk.dev/context/#__codelineno-56-6>)    const searchResults = await context.searchMemory(`Information about ${topic}`);
    [](<https://adk.dev/context/#__codelineno-56-7>)    if (searchResults.results?.length) {
    [](<https://adk.dev/context/#__codelineno-56-8>)      console.log(`Found ${searchResults.results.length} memory results for '${topic}'`);
    [](<https://adk.dev/context/#__codelineno-56-9>)      // Process searchResults.results
    [](<https://adk.dev/context/#__codelineno-56-10>)      const topResultText = searchResults.results[0].text;
    [](<https://adk.dev/context/#__codelineno-56-11>)      return { memory_snippet: topResultText };
    [](<https://adk.dev/context/#__codelineno-56-12>)    } else {
    [](<https://adk.dev/context/#__codelineno-56-13>)      return { message: 'No relevant memories found.' };
    [](<https://adk.dev/context/#__codelineno-56-14>)    }
    [](<https://adk.dev/context/#__codelineno-56-15>)  } catch (e) {
    [](<https://adk.dev/context/#__codelineno-56-16>)     return { error: `Memory service error: ${e}` }; // e.g., Service not configured
    [](<https://adk.dev/context/#__codelineno-56-17>)  }
    [](<https://adk.dev/context/#__codelineno-56-18>)}
    
    [](<https://adk.dev/context/#__codelineno-57-1>)// Example: Tool using memory search
    [](<https://adk.dev/context/#__codelineno-57-2>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/context/#__codelineno-57-3>)import com.google.adk.memory.SearchMemoryResponse;
    [](<https://adk.dev/context/#__codelineno-57-4>)import io.reactivex.rxjava3.core.Single;
    [](<https://adk.dev/context/#__codelineno-57-5>)import java.util.Map;
    [](<https://adk.dev/context/#__codelineno-57-6>)
    [](<https://adk.dev/context/#__codelineno-57-7>)public class MemorySearchTool {
    [](<https://adk.dev/context/#__codelineno-57-8>)  public Single<Map<String, String>> findRelatedInfo(ToolContext context, String topic) {
    [](<https://adk.dev/context/#__codelineno-57-9>)    return context.searchMemory("Information about " + topic)
    [](<https://adk.dev/context/#__codelineno-57-10>)        .map(searchResults -> {
    [](<https://adk.dev/context/#__codelineno-57-11>)          if (searchResults != null && searchResults.results() != null && !searchResults.results().isEmpty()) {
    [](<https://adk.dev/context/#__codelineno-57-12>)            System.out.println("Found " + searchResults.results().size() + " memory results for '" + topic + "'");
    [](<https://adk.dev/context/#__codelineno-57-13>)            // Process searchResults.results
    [](<https://adk.dev/context/#__codelineno-57-14>)            String topResultText = searchResults.results().get(0).text();
    [](<https://adk.dev/context/#__codelineno-57-15>)            return Map.of("memory_snippet", topResultText);
    [](<https://adk.dev/context/#__codelineno-57-16>)          } else {
    [](<https://adk.dev/context/#__codelineno-57-17>)            return Map.of("message", "No relevant memories found.");
    [](<https://adk.dev/context/#__codelineno-57-18>)          }
    [](<https://adk.dev/context/#__codelineno-57-19>)        })
    [](<https://adk.dev/context/#__codelineno-57-20>)        .onErrorReturnItem(Map.of("error", "Memory service error"));
    [](<https://adk.dev/context/#__codelineno-57-21>)  }
    [](<https://adk.dev/context/#__codelineno-57-22>)}
    
### Advanced: Direct `InvocationContext` Usage[¶](<https://adk.dev/context/#advanced-direct-invocationcontext-usage> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Java v0.2.0

While most interactions happen via `CallbackContext` or `ToolContext`, sometimes the agent's core logic (`_run_async_impl`/`_run_live_impl`) needs direct access.

PythonTypeScriptJava
    
    [](<https://adk.dev/context/#__codelineno-58-1>)# Example: Inside agent's _run_async_impl
    [](<https://adk.dev/context/#__codelineno-58-2>)from google.adk.agents import BaseAgent
    [](<https://adk.dev/context/#__codelineno-58-3>)from google.adk.agents.invocation_context import InvocationContext
    [](<https://adk.dev/context/#__codelineno-58-4>)from google.adk.events import Event
    [](<https://adk.dev/context/#__codelineno-58-5>)from typing import AsyncGenerator
    [](<https://adk.dev/context/#__codelineno-58-6>)
    [](<https://adk.dev/context/#__codelineno-58-7>)class MyControllingAgent(BaseAgent):
    [](<https://adk.dev/context/#__codelineno-58-8>)    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    [](<https://adk.dev/context/#__codelineno-58-9>)        # Example: Check if a specific service is available
    [](<https://adk.dev/context/#__codelineno-58-10>)        if not ctx.memory_service:
    [](<https://adk.dev/context/#__codelineno-58-11>)            print("Memory service is not available for this invocation.")
    [](<https://adk.dev/context/#__codelineno-58-12>)            # Potentially change agent behavior
    [](<https://adk.dev/context/#__codelineno-58-13>)
    [](<https://adk.dev/context/#__codelineno-58-14>)        # Example: Early termination based on some condition
    [](<https://adk.dev/context/#__codelineno-58-15>)        if ctx.session.state.get("critical_error_flag"):
    [](<https://adk.dev/context/#__codelineno-58-16>)            print("Critical error detected, ending invocation.")
    [](<https://adk.dev/context/#__codelineno-58-17>)            ctx.end_invocation = True # Signal framework to stop processing
    [](<https://adk.dev/context/#__codelineno-58-18>)            yield Event(author=self.name, invocation_id=ctx.invocation_id, content="Stopping due to critical error.")
    [](<https://adk.dev/context/#__codelineno-58-19>)            return # Stop this agent's execution
    [](<https://adk.dev/context/#__codelineno-58-20>)
    [](<https://adk.dev/context/#__codelineno-58-21>)        # ... Normal agent processing ...
    [](<https://adk.dev/context/#__codelineno-58-22>)        yield # ... event ...
    
    [](<https://adk.dev/context/#__codelineno-59-1>)// Pseudocode: Inside agent's runAsyncImpl
    [](<https://adk.dev/context/#__codelineno-59-2>)import { BaseAgent, InvocationContext } from '@google/adk';
    [](<https://adk.dev/context/#__codelineno-59-3>)import type { Event } from '@google/adk';
    [](<https://adk.dev/context/#__codelineno-59-4>)
    [](<https://adk.dev/context/#__codelineno-59-5>)class MyControllingAgent extends BaseAgent {
    [](<https://adk.dev/context/#__codelineno-59-6>)  async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined> {
    [](<https://adk.dev/context/#__codelineno-59-7>)    // Example: Check if a specific service is available
    [](<https://adk.dev/context/#__codelineno-59-8>)    if (!ctx.memoryService) {
    [](<https://adk.dev/context/#__codelineno-59-9>)      console.log('Memory service is not available for this invocation.');
    [](<https://adk.dev/context/#__codelineno-59-10>)      // Potentially change agent behavior
    [](<https://adk.dev/context/#__codelineno-59-11>)    }
    [](<https://adk.dev/context/#__codelineno-59-12>)
    [](<https://adk.dev/context/#__codelineno-59-13>)    // Example: Early termination based on some condition
    [](<https://adk.dev/context/#__codelineno-59-14>)    // Direct access to state via ctx.session.state or through ctx.session.state property if wrapped
    [](<https://adk.dev/context/#__codelineno-59-15>)    if ((ctx.session.state as { 'critical_error_flag': boolean })['critical_error_flag']) {
    [](<https://adk.dev/context/#__codelineno-59-16>)      console.log('Critical error detected, ending invocation.');
    [](<https://adk.dev/context/#__codelineno-59-17>)      ctx.endInvocation = true; // Signal framework to stop processing
    [](<https://adk.dev/context/#__codelineno-59-18>)      yield {
    [](<https://adk.dev/context/#__codelineno-59-19>)        author: this.name,
    [](<https://adk.dev/context/#__codelineno-59-20>)        invocationId: ctx.invocationId,
    [](<https://adk.dev/context/#__codelineno-59-21>)        content: { parts: [{ text: 'Stopping due to critical error.' }] }
    [](<https://adk.dev/context/#__codelineno-59-22>)      } as Event;
    [](<https://adk.dev/context/#__codelineno-59-23>)      return; // Stop this agent's execution
    [](<https://adk.dev/context/#__codelineno-59-24>)    }
    [](<https://adk.dev/context/#__codelineno-59-25>)
    [](<https://adk.dev/context/#__codelineno-59-26>)    // ... Normal agent processing ...
    [](<https://adk.dev/context/#__codelineno-59-27>)    yield; // ... event ...
    [](<https://adk.dev/context/#__codelineno-59-28>)  }
    [](<https://adk.dev/context/#__codelineno-59-29>)}
    
    [](<https://adk.dev/context/#__codelineno-60-1>)// Example: Inside agent's runAsyncImpl
    [](<https://adk.dev/context/#__codelineno-60-2>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/context/#__codelineno-60-3>)import com.google.adk.agents.InvocationContext;
    [](<https://adk.dev/context/#__codelineno-60-4>)import com.google.adk.events.Event;
    [](<https://adk.dev/context/#__codelineno-60-5>)import com.google.genai.types.Content;
    [](<https://adk.dev/context/#__codelineno-60-6>)import com.google.genai.types.Part;
    [](<https://adk.dev/context/#__codelineno-60-7>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/context/#__codelineno-60-8>)import java.util.List;
    [](<https://adk.dev/context/#__codelineno-60-9>)
    [](<https://adk.dev/context/#__codelineno-60-10>)public class MyControllingAgent extends BaseAgent {
    [](<https://adk.dev/context/#__codelineno-60-11>)
    [](<https://adk.dev/context/#__codelineno-60-12>)  @Override
    [](<https://adk.dev/context/#__codelineno-60-13>)  protected Flowable<Event> runAsyncImpl(InvocationContext ctx) {
    [](<https://adk.dev/context/#__codelineno-60-14>)    // Example: Check if a specific service is available
    [](<https://adk.dev/context/#__codelineno-60-15>)    if (ctx.memoryService() == null) {
    [](<https://adk.dev/context/#__codelineno-60-16>)      System.out.println("Memory service is not available for this invocation.");
    [](<https://adk.dev/context/#__codelineno-60-17>)      // Potentially change agent behavior
    [](<https://adk.dev/context/#__codelineno-60-18>)    }
    [](<https://adk.dev/context/#__codelineno-60-19>)
    [](<https://adk.dev/context/#__codelineno-60-20>)    // Example: Early termination based on some condition
    [](<https://adk.dev/context/#__codelineno-60-21>)    Boolean criticalError = (Boolean) ctx.session().state().getOrDefault("critical_error_flag", false);
    [](<https://adk.dev/context/#__codelineno-60-22>)    if (criticalError != null && criticalError) {
    [](<https://adk.dev/context/#__codelineno-60-23>)      System.out.println("Critical error detected, ending invocation.");
    [](<https://adk.dev/context/#__codelineno-60-24>)      ctx.setEndInvocation(true); // Signal framework to stop processing
    [](<https://adk.dev/context/#__codelineno-60-25>)
    [](<https://adk.dev/context/#__codelineno-60-26>)      Event errorEvent = Event.builder()
    [](<https://adk.dev/context/#__codelineno-60-27>)          .author(name())
    [](<https://adk.dev/context/#__codelineno-60-28>)          .invocationId(ctx.invocationId())
    [](<https://adk.dev/context/#__codelineno-60-29>)          .content(Content.builder().parts(List.of(Part.builder().text("Stopping due to critical error.").build())).build())
    [](<https://adk.dev/context/#__codelineno-60-30>)          .build();
    [](<https://adk.dev/context/#__codelineno-60-31>)
    [](<https://adk.dev/context/#__codelineno-60-32>)      return Flowable.just(errorEvent); // Stop this agent's execution
    [](<https://adk.dev/context/#__codelineno-60-33>)    }
    [](<https://adk.dev/context/#__codelineno-60-34>)
    [](<https://adk.dev/context/#__codelineno-60-35>)    // ... Normal agent processing ...
    [](<https://adk.dev/context/#__codelineno-60-36>)    // return Flowable.just(normalEvent);
    [](<https://adk.dev/context/#__codelineno-60-37>)    return Flowable.empty();
    [](<https://adk.dev/context/#__codelineno-60-38>)  }
    [](<https://adk.dev/context/#__codelineno-60-39>)}
    
Setting `ctx.end_invocation = True` is a way to gracefully stop the entire request-response cycle from within the agent or its callbacks/tools (via their respective context objects which also have access to modify the underlying `InvocationContext`'s flag).

## Key Takeaways & Best Practices[¶](<https://adk.dev/context/#key-takeaways-best-practices> "Permanent link")

  * **Use the Right Context:** Always use the most specific context object provided (`ToolContext` in tools/tool-callbacks, `CallbackContext` in agent/model-callbacks, `ReadonlyContext` where applicable). Use the full `InvocationContext` (`ctx`) directly in `_run_async_impl` / `_run_live_impl` only when necessary.
  * **State for Data Flow:** `context.state` is the primary way to share data, remember preferences, and manage conversational memory _within_ an invocation. Use prefixes (`app:`, `user:`, `temp:`) thoughtfully when using persistent storage.
  * **Artifacts for Files:** Use `context.save_artifact` and `context.load_artifact` for managing file references (like paths or URIs) or larger data blobs. Store references, load content on demand.
  * **Tracked Changes:** Modifications to state or artifacts made via context methods are automatically linked to the current step's `EventActions` and handled by the `SessionService`.
  * **Start Simple:** Focus on `state` and basic artifact usage first. Explore authentication, memory, and advanced `InvocationContext` fields (like those for live streaming) as your needs become more complex.

By understanding and effectively using these context objects, you can build more sophisticated, stateful, and capable agents with ADK.

Back to top 