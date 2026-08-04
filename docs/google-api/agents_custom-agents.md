# Custom template workflows - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/custom-agents/](https://adk.dev/agents/custom-agents/)

[ Skip to content ](<https://adk.dev/agents/custom-agents/#custom-agent-template-workflows>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/custom-agents.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/custom-agents/index.md> "View this page as Markdown")

# Custom agent template workflows[¶](<https://adk.dev/agents/custom-agents/#custom-agent-template-workflows> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

Custom agents and agent-based workflows allow you to define arbitrary orchestration logic by inheriting directly from `BaseAgent` and implementing your own control flow. This approach allows you to create new execution patterns similar to `SequentialAgent`, `LoopAgent`, and `ParallelAgent`, enabling you to build highly specific and complex agentic workflows.

Alternative: graph-based workflows

Starting in ADK 2.0, agent-based workflows using `BaseAgent` have been superseded

by more flexible workflow structures, including [graph-based workflows](<https://adk.dev/workflows/graphs/>) and [dynamic workflows](<https://adk.dev/workflows/dynamic/>). You should evaluate the capabilities of these workflow mechanisms **_before_** building a custom agent for your target workflow.

Advanced Concept

Building custom agents by directly implementing `_run_async_impl`, or its equivalent in other languages, provides powerful control but is more complex than using the predefined `LlmAgent` or `WorkflowAgent` types. We recommend understanding those foundational agent types first before tackling custom orchestration logic.

## Overview[¶](<https://adk.dev/agents/custom-agents/#overview> "Permanent link")

A Custom Agent is essentially any class you create that inherits from `google.adk.agents.BaseAgent` and implements its core execution logic within the `_run_async_impl` asynchronous method. You have complete control over how this method calls other sub-agents, manages state, and handles events.

![intro_components.png](https://adk.dev/assets/custom-agent-flow.png)

Note

The specific method name for implementing an agent's core asynchronous logic may vary slightly by SDK language, such as `runAsyncImpl` in Java, `_run_async_impl` in Python, or `runAsyncImpl` in TypeScript. Refer to the language-specific API documentation for details.

### Why build Custom Agents?[¶](<https://adk.dev/agents/custom-agents/#why-build-custom-agents> "Permanent link")

After reviewing exising ADK [agent workflow](<https://adk.dev/workflows/>) approaches and architectures, you may want to consider building a custom workflow agent if those mechanisms cannot meet one or more of following requirements for your project:

  * **Conditional Logic:** Executing different sub-agents or taking different paths based on runtime conditions or the results of previous steps.
  * **Complex State Management:** Implementing intricate logic for maintaining and updating state throughout the workflow beyond simple sequential passing.
  * **External Integrations:** Incorporating calls to external APIs, databases, or custom libraries directly within the orchestration flow control.
  * **Dynamic Agent Selection:** Choosing which sub-agent(s) to run next based on dynamic evaluation of the situation or input.
  * **Unique Workflow Patterns:** Implementing orchestration logic that doesn't fit the standard sequential, parallel, or loop structures.

## Implementing custom logic[¶](<https://adk.dev/agents/custom-agents/#implementing-custom-logic> "Permanent link")

The core of any custom agent is the method where you define its unique asynchronous behavior. This method allows you to orchestrate sub-agents and manage the flow of execution.

PythonTypeScriptGoJava

The heart of any custom agent is the `_run_async_impl` method. This is where you define its unique behavior.

  * **Signature:** `async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:`
  * **Asynchronous Generator:** It must be an `async def` function and return an `AsyncGenerator`. This allows it to `yield` events produced by sub-agents or its own logic back to the runner.
  * **`ctx` (InvocationContext):** Provides access to crucial runtime information, most importantly `ctx.session.state`, which is the primary way to share data between steps orchestrated by your custom agent.

The heart of any custom agent is the `runAsyncImpl` method. This is where you define its unique behavior.

  * **Signature:** `async* runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined>`
  * **Asynchronous Generator:** It must be an `async` generator function (`async*`).
  * **`ctx` (InvocationContext):** Provides access to crucial runtime information, most importantly `ctx.session.state`, which is the primary way to share data between steps orchestrated by your custom agent.

In Go, you implement the `Run` method as part of a struct that satisfies the `agent.Agent` interface. The actual logic is typically a method on your custom agent struct.

  * **Signature:** `Run(ctx agent.InvocationContext) iter.Seq2[*session.Event, error]`
  * **Iterator:** The `Run` method returns an iterator (`iter.Seq2`) that yields events and errors. This is the standard way to handle streaming results from an agent's execution.
  * **`ctx` (InvocationContext):** The `agent.InvocationContext` provides access to the session, including state, and other crucial runtime information.
  * **Session State:** You can access the session state through `ctx.Session().State()`.

The heart of any custom agent is the `runAsyncImpl` method, which you override from `BaseAgent`.

  * **Signature:** `protected Flowable<Event> runAsyncImpl(InvocationContext ctx)`
  * **Reactive Stream (`Flowable`):** It must return an `io.reactivex.rxjava3.core.Flowable<Event>`. This `Flowable` represents a stream of events that will be produced by the custom agent's logic, often by combining or transforming multiple `Flowable` from sub-agents.
  * **`ctx` (InvocationContext):** Provides access to crucial runtime information, most importantly `ctx.session().state()`, which is a `java.util.concurrent.ConcurrentMap<String, Object>`. This is the primary way to share data between steps orchestrated by your custom agent.

### Key capabilities within the core asynchronous method[¶](<https://adk.dev/agents/custom-agents/#key-capabilities-within-the-core-asynchronous-method> "Permanent link")

PythonTypeScriptGoJava

  1. **Calling Sub-Agents:** You invoke sub-agents (which are typically stored as instance attributes like `self.my_llm_agent`) using their `run_async` method and yield their events:
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-0-1>)async for event in self.some_sub_agent.run_async(ctx):
         [](<https://adk.dev/agents/custom-agents/#__codelineno-0-2>)    # Optionally inspect or log the event
         [](<https://adk.dev/agents/custom-agents/#__codelineno-0-3>)    yield event # Pass the event up
         
  2. **Managing State:** Read from and write to the session state dictionary (`ctx.session.state`) to pass data between sub-agent calls or make decisions:
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-1>)# Read data set by a previous agent
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-2>)previous_result = ctx.session.state.get("some_key")
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-3>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-4>)# Make a decision based on state
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-5>)if previous_result == "some_value":
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-6>)    # ... call a specific sub-agent ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-7>)else:
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-8>)    # ... call another sub-agent ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-9>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-10>)# Store a result for a later step (often done via a sub-agent's output_key)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-1-11>)# ctx.session.state["my_custom_result"] = "calculated_value"
         
  3. **Implementing Control Flow:** Use standard Python constructs (`if`/`elif`/`else`, `for`/`while` loops, `try`/`except`) to create sophisticated, conditional, or iterative workflows involving your sub-agents.

  1. **Calling Sub-Agents:** You invoke sub-agents (which are typically stored as instance properties like `this.myLlmAgent`) using their `run` method and yield their events:
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-2-1>)for await (const event of this.someSubAgent.runAsync(ctx)) {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-2-2>)    // Optionally inspect or log the event
         [](<https://adk.dev/agents/custom-agents/#__codelineno-2-3>)    yield event; // Pass the event up to the runner
         [](<https://adk.dev/agents/custom-agents/#__codelineno-2-4>)}
         
  2. **Managing State:** Read from and write to the session state object (`ctx.session.state`) to pass data between sub-agent calls or make decisions:
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-1>)// Read data set by a previous agent
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-2>)const previousResult = ctx.session.state['some_key'];
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-3>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-4>)// Make a decision based on state
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-5>)if (previousResult === 'some_value') {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-6>)  // ... call a specific sub-agent ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-7>)} else {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-8>)  // ... call another sub-agent ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-9>)}
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-10>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-11>)// Store a result for a later step (often done via a sub-agent's outputKey)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-3-12>)// ctx.session.state['my_custom_result'] = 'calculated_value';
         
  3. **Implementing Control Flow:** Use standard TypeScript/JavaScript constructs (`if`/`else`, `for`/`while` loops, `try`/`catch`) to create sophisticated, conditional, or iterative workflows involving your sub-agents.

  1. **Calling Sub-Agents:** You invoke sub-agents by calling their `Run` method.
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-1>)// Example: Running one sub-agent and yielding its events
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-2>)for event, err := range someSubAgent.Run(ctx) {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-3>)    if err != nil {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-4>)        // Handle or propagate the error
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-5>)        return
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-6>)    }
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-7>)    // Yield the event up to the caller
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-8>)    if !yield(event, nil) {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-9>)      return
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-10>)    }
         [](<https://adk.dev/agents/custom-agents/#__codelineno-4-11>)}
         
  2. **Managing State:** Read from and write to the session state to pass data between sub-agent calls or make decisions. 
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-1>)// The `ctx` (`agent.InvocationContext`) is passed directly to your agent's `Run` function.
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-2>)// Read data set by a previous agent
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-3>)previousResult, err := ctx.Session().State().Get("some_key")
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-4>)if err != nil {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-5>)    // Handle cases where the key might not exist yet
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-6>)}
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-7>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-8>)// Make a decision based on state
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-9>)if val, ok := previousResult.(string); ok && val == "some_value" {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-10>)    // ... call a specific sub-agent ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-11>)} else {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-12>)    // ... call another sub-agent ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-13>)}
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-14>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-15>)// Store a result for a later step
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-16>)if err := ctx.Session().State().Set("my_custom_result", "calculated_value"); err != nil {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-17>)    // Handle error
         [](<https://adk.dev/agents/custom-agents/#__codelineno-5-18>)}
         
  3. **Implementing Control Flow:** Use standard Go constructs (`if`/`else`, `for`/`switch` loops, goroutines, channels) to create sophisticated, conditional, or iterative workflows involving your sub-agents.

  1. **Calling Sub-Agents:** You invoke sub-agents (which are typically stored as instance attributes or objects) using their asynchronous run method and return their event streams:

You typically chain `Flowable`s from sub-agents using RxJava operators like `concatWith`, `flatMapPublisher`, or `concatArray`.
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-1>)// Example: Running one sub-agent
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-2>)// return someSubAgent.runAsync(ctx);
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-3>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-4>)// Example: Running sub-agents sequentially
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-5>)Flowable<Event> firstAgentEvents = someSubAgent1.runAsync(ctx)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-6>)    .doOnNext(event -> System.out.println("Event from agent 1: " + event.id()));
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-7>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-8>)Flowable<Event> secondAgentEvents = Flowable.defer(() ->
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-9>)    someSubAgent2.runAsync(ctx)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-10>)        .doOnNext(event -> System.out.println("Event from agent 2: " + event.id()))
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-11>));
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-12>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-6-13>)return firstAgentEvents.concatWith(secondAgentEvents);
         
The `Flowable.defer()` is often used for subsequent stages if their execution depends on the completion or state after prior stages.

  2. **Managing State:** Read from and write to the session state to pass data between sub-agent calls or make decisions. The session state is a `java.util.concurrent.ConcurrentMap<String, Object>` obtained via `ctx.session().state()`.
         
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-1>)// Read data set by a previous agent
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-2>)Object previousResult = ctx.session().state().get("some_key");
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-3>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-4>)// Make a decision based on state
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-5>)if ("some_value".equals(previousResult)) {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-6>)    // ... logic to include a specific sub-agent's Flowable ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-7>)} else {
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-8>)    // ... logic to include another sub-agent's Flowable ...
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-9>)}
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-10>)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-11>)// Store a result for a later step (often done via a sub-agent's output_key)
         [](<https://adk.dev/agents/custom-agents/#__codelineno-7-12>)// ctx.session().state().put("my_custom_result", "calculated_value");
         
  3. **Implementing Control Flow:** Use standard language constructs (`if`/`else`, loops, `try`/`catch`) combined with reactive operators (RxJava) to create sophisticated workflows.

     * **Conditional:** `Flowable.defer()` to choose which `Flowable` to subscribe to based on a condition, or `filter()` if you're filtering events within a stream.
     * **Iterative:** Operators like `repeat()`, `retry()`, or by structuring your `Flowable` chain to recursively call parts of itself based on conditions (often managed with `flatMapPublisher` or `concatMap`).

## Managing sub-agents and state[¶](<https://adk.dev/agents/custom-agents/#managing-sub-agents-and-state> "Permanent link")

Typically, a custom agent orchestrates other agents (like `LlmAgent`, `LoopAgent`, etc.).

  * **Initialization:** You usually pass instances of these sub-agents into your custom agent's constructor and store them as instance fields/attributes (e.g., `this.story_generator = story_generator_instance` or `self.story_generator = story_generator_instance`). This makes them accessible within the custom agent's core asynchronous execution logic (such as: `_run_async_impl` method).
  * **Sub Agents List:** When initializing the `BaseAgent` using it's `super()` constructor, you should pass a `sub agents` list. This list tells the ADK framework about the agents that are part of this custom agent's immediate hierarchy. It's important for framework features like lifecycle management, introspection, and potentially future routing capabilities, even if your core execution logic (`_run_async_impl`) calls the agents directly via `self.xxx_agent`. Include the agents that your custom logic directly invokes at the top level.
  * **State:** As mentioned, `ctx.session.state` is the standard way sub-agents (especially `LlmAgent`s using `output key`) communicate results back to the orchestrator and how the orchestrator passes necessary inputs down.

## Agent-based workflow primitives[¶](<https://adk.dev/agents/custom-agents/#agent-based-workflow-primitives> "Permanent link")

The following sections detail the core ADK primitives—such as agent hierarchy, workflow agents, and interaction mechanisms—that enable you to construct and manage these multi-agent systems effectively. ADK provides core building blocks—primitives—that enable you to structure and manage interactions within your multi-agent system.

Note

The specific parameters or method names for the primitives may vary slightly by SDK language, for example `sub_agents` in Python, and `subAgents` in Java. Refer to the language-specific API documentation for details.

### Agent hierarchy: Parent agents and sub-agents[¶](<https://adk.dev/agents/custom-agents/#agent-hierarchy-parent-agents-and-sub-agents> "Permanent link")

The foundation for structuring multi-agent systems is the parent-child relationship defined in `BaseAgent`.

  * **Establishing Hierarchy:** You create a tree structure by passing a list of agent instances to the `sub_agents` argument when initializing a parent agent. ADK automatically sets the `parent_agent` attribute on each child agent during initialization.
  * **Single Parent Rule:** An agent instance can only be added as a sub-agent once. Attempting to assign a second parent will result in a `ValueError`.
  * **Importance:** This hierarchy defines the scope for [Workflow Agents](<https://adk.dev/agents/custom-agents/#workflow-agents-as-orchestrators>) and influences the potential targets for LLM-Driven Delegation. You can navigate the hierarchy using `agent.parent_agent` or find descendants using `agent.find_agent(name)`.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-1>)# Conceptual Example: Defining Hierarchy
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-2>)from google.adk.agents import LlmAgent, BaseAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-5>)# Define individual agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-6>)greeter = LlmAgent(name="Greeter", model="gemini-flash-latest")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-7>)task_doer = BaseAgent(name="TaskExecutor") # Custom non-LLM agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-10>)# Create parent agent and assign children via sub_agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-11>)coordinator = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-12>)    name="Coordinator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-13>)    model="gemini-flash-latest",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-14>)    description="I coordinate greetings and tasks.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-15>)    sub_agents=[ # Assign sub_agents here
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-16>)        greeter,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-17>)        task_doer
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-18>)    ]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-19>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-20>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-21>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-22>)# Framework automatically sets:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-23>)# assert greeter.parent_agent == coordinator
    [](<https://adk.dev/agents/custom-agents/#__codelineno-8-24>)# assert task_doer.parent_agent == coordinator
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-1>)// Conceptual Example: Defining Hierarchy
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-2>)import { LlmAgent, BaseAgent, InvocationContext } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-3>)import type { Event, createEventActions } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-5>)class TaskExecutorAgent extends BaseAgent {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-6>)  async *runAsyncImpl(context: InvocationContext): AsyncGenerator<Event, void, void> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-7>)    yield {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-8>)      id: 'event-1',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-9>)      invocationId: context.invocationId,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-10>)      author: this.name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-11>)      content: { parts: [{ text: 'Task completed!' }] },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-12>)      actions: createEventActions(),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-13>)      timestamp: Date.now(),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-14>)    };
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-15>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-16>)  async *runLiveImpl(context: InvocationContext): AsyncGenerator<Event, void, void> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-17>)    this.runAsyncImpl(context);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-18>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-19>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-20>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-21>)// Define individual agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-22>)const greeter = new LlmAgent({name: 'Greeter', model: 'gemini-flash-latest'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-23>)const taskDoer = new TaskExecutorAgent({name: 'TaskExecutor'}); // Custom non-LLM agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-24>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-25>)// Create parent agent and assign children via subAgents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-26>)const coordinator = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-27>)    name: 'Coordinator',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-28>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-29>)    description: 'I coordinate greetings and tasks.',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-30>)    subAgents: [ // Assign subAgents here
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-31>)        greeter,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-32>)        taskDoer
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-33>)    ],
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-34>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-35>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-36>)// Framework automatically sets:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-37>)// console.assert(greeter.parentAgent === coordinator);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-9-38>)// console.assert(taskDoer.parentAgent === coordinator);
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-1>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-4>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-5>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-6>)// Conceptual Example: Defining Hierarchy
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-7>)// Define individual agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-8>)greeter, _ := llmagent.New(llmagent.Config{Name: "Greeter", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-9>)taskDoer, _ := agent.New(agent.Config{Name: "TaskExecutor"}) // Custom non-LLM agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-11>)// Create parent agent and assign children via sub_agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-12>)coordinator, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-13>)    Name:        "Coordinator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-14>)    Model:       m,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-15>)    Description: "I coordinate greetings and tasks.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-16>)    SubAgents:   []agent.Agent{greeter, taskDoer}, // Assign sub_agents here
    [](<https://adk.dev/agents/custom-agents/#__codelineno-10-17>)})
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-1>)// Conceptual Example: Defining Hierarchy
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-2>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-5>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-6>)// Define individual agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-7>)LlmAgent greeter = LlmAgent.builder().name("Greeter").model("gemini-flash-latest").build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-8>)SequentialAgent taskDoer = SequentialAgent.builder().name("TaskExecutor").subAgents(...).build(); // Sequential Agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-11>)// Create parent agent and assign sub_agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-12>)LlmAgent coordinator = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-13>)    .name("Coordinator")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-14>)    .model("gemini-flash-latest")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-15>)    .description("I coordinate greetings and tasks")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-16>)    .subAgents(greeter, taskDoer) // Assign sub_agents here
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-17>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-18>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-19>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-20>)// Framework automatically sets:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-21>)// assert greeter.parentAgent().equals(coordinator);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-11-22>)// assert taskDoer.parentAgent().equals(coordinator);
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-1>)class TaskExecutorAgent : BaseAgent(name = "TaskExecutor") {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-2>)    override fun runAsyncImpl(context: InvocationContext): Flow<Event> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-3>)        return flowOf(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-4>)            Event(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-5>)                author = name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-6>)                content = Content(parts = listOf(Part(text = "Task completed!"))),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-7>)            ),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-8>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-9>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-10>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-11>)val greeter = LlmAgent(name = "Greeter", model = model)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-12>)val taskDoer = TaskExecutorAgent()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-13>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-14>)val coordinator =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-15>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-16>)        name = "Coordinator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-17>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-18>)        description = "I coordinate greetings and tasks.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-19>)        subAgents = listOf(greeter, taskDoer),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-12-20>)    )
    
### Workflow agents as orchestrators[¶](<https://adk.dev/agents/custom-agents/#workflow-agents-as-orchestrators> "Permanent link")

ADK includes specialized agents derived from `BaseAgent` that don't perform tasks themselves but orchestrate the execution flow of their `sub_agents`.

  * **[`SequentialAgent`](<https://adk.dev/agents/workflow-agents/sequential-agents/>):** Executes its `sub_agents` one after another in the order they are listed.
    * **Context:** Passes the _same_ [`InvocationContext`](<https://adk.dev/runtime/>) sequentially, allowing agents to easily pass results via shared state.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-1>)# Conceptual Example: Sequential Pipeline
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-2>)from google.adk.agents import SequentialAgent, LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-4>)step1 = LlmAgent(name="Step1_Fetch", output_key="data") # Saves output to state['data']
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-5>)step2 = LlmAgent(name="Step2_Process", instruction="Process data from {data}.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-7>)pipeline = SequentialAgent(name="MyPipeline", sub_agents=[step1, step2])
    [](<https://adk.dev/agents/custom-agents/#__codelineno-13-8>)# When pipeline runs, Step2 can access the state['data'] set by Step1.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-1>)// Conceptual Example: Sequential Pipeline
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-2>)import { SequentialAgent, LlmAgent } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-4>)const step1 = new LlmAgent({name: 'Step1_Fetch', outputKey: 'data'}); // Saves output to state['data']
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-5>)const step2 = new LlmAgent({name: 'Step2_Process', instruction: 'Process data from {data}.'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-7>)const pipeline = new SequentialAgent({name: 'MyPipeline', subAgents: [step1, step2]});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-14-8>)// When pipeline runs, Step2 can access the state['data'] set by Step1.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-1>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-4>)    "google.golang.org/adk/v2/agent/workflowagents/sequentialagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-5>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-7>)// Conceptual Example: Sequential Pipeline
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-8>)step1, _ := llmagent.New(llmagent.Config{Name: "Step1_Fetch", OutputKey: "data", Model: m}) // Saves output to state["data"]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-9>)step2, _ := llmagent.New(llmagent.Config{Name: "Step2_Process", Instruction: "Process data from {data}.", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-11>)pipeline, _ := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-12>)    AgentConfig: agent.Config{Name: "MyPipeline", SubAgents: []agent.Agent{step1, step2}},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-13>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-15-14>)// When pipeline runs, Step2 can access the state["data"] set by Step1.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-1>)// Conceptual Example: Sequential Pipeline
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-2>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-5>)LlmAgent step1 = LlmAgent.builder().name("Step1_Fetch").outputKey("data").build(); // Saves output to state.get("data")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-6>)LlmAgent step2 = LlmAgent.builder().name("Step2_Process").instruction("Process data from {data}.").build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-7>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-8>)SequentialAgent pipeline = SequentialAgent.builder().name("MyPipeline").subAgents(step1, step2).build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-16-9>)// When pipeline runs, Step2 can access the state.get("data") set by Step1.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-1>)val step1 = LlmAgent(name = "Step1_Fetch", model = model)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-2>)val step2 =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-3>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-4>)        name = "Step2_Process",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-5>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-6>)        instruction = Instruction("Process data from state."),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-7>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-17-9>)val pipeline = SequentialAgent(name = "MyPipeline", subAgents = listOf(step1, step2))
    
  * **[`ParallelAgent`](<https://adk.dev/agents/workflow-agents/parallel-agents/>):** Executes its `sub_agents` in parallel. Events from sub-agents may be interleaved.
    * **Context:** Modifies the `InvocationContext.branch` for each child agent (e.g., `ParentBranch.ChildName`), providing a distinct contextual path which can be useful for isolating history in some memory implementations.
    * **State:** Despite different branches, all parallel children access the _same shared_ `session.state`, enabling them to read initial state and write results (use distinct keys to avoid race conditions).

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-1>)# Conceptual Example: Parallel Execution
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-2>)from google.adk.agents import ParallelAgent, LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-4>)fetch_weather = LlmAgent(name="WeatherFetcher", output_key="weather")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-5>)fetch_news = LlmAgent(name="NewsFetcher", output_key="news")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-7>)gatherer = ParallelAgent(name="InfoGatherer", sub_agents=[fetch_weather, fetch_news])
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-8>)# When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-18-9>)# A subsequent agent could read state['weather'] and state['news'].
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-1>)// Conceptual Example: Parallel Execution
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-2>)import { ParallelAgent, LlmAgent } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-4>)const fetchWeather = new LlmAgent({name: 'WeatherFetcher', outputKey: 'weather'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-5>)const fetchNews = new LlmAgent({name: 'NewsFetcher', outputKey: 'news'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-7>)const gatherer = new ParallelAgent({name: 'InfoGatherer', subAgents: [fetchWeather, fetchNews]});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-8>)// When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-19-9>)// A subsequent agent could read state['weather'] and state['news'].
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-1>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-4>)    "google.golang.org/adk/v2/agent/workflowagents/parallelagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-5>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-7>)// Conceptual Example: Parallel Execution
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-8>)fetchWeather, _ := llmagent.New(llmagent.Config{Name: "WeatherFetcher", OutputKey: "weather", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-9>)fetchNews, _ := llmagent.New(llmagent.Config{Name: "NewsFetcher", OutputKey: "news", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-11>)gatherer, _ := parallelagent.New(parallelagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-12>)    AgentConfig: agent.Config{Name: "InfoGatherer", SubAgents: []agent.Agent{fetchWeather, fetchNews}},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-13>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-14>)// When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-20-15>)// A subsequent agent could read state["weather"] and state["news"].
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-1>)// Conceptual Example: Parallel Execution
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-3>)import com.google.adk.agents.ParallelAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-5>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-6>)LlmAgent fetchWeather = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-7>)    .name("WeatherFetcher")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-8>)    .outputKey("weather")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-9>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-11>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-12>)LlmAgent fetchNews = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-13>)    .name("NewsFetcher")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-14>)    .instruction("news")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-15>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-16>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-17>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-18>)ParallelAgent gatherer = ParallelAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-19>)    .name("InfoGatherer")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-20>)    .subAgents(fetchWeather, fetchNews)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-21>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-22>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-24>)// When gatherer runs, WeatherFetcher and NewsFetcher run concurrently.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-21-25>)// A subsequent agent could read state['weather'] and state['news'].
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-22-1>)val fetchWeather = LlmAgent(name = "WeatherFetcher", model = model)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-22-2>)val fetchNews = LlmAgent(name = "NewsFetcher", model = model)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-22-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-22-4>)val gatherer = ParallelAgent(name = "InfoGatherer", subAgents = listOf(fetchWeather, fetchNews))
    
  * **[`LoopAgent`](<https://adk.dev/agents/workflow-agents/loop-agents/>):** Executes its `sub_agents` sequentially in a loop.
    * **Termination:** The loop stops if the optional `max_iterations` is reached, or if any sub-agent returns an [`Event`](<https://adk.dev/events/>) with `escalate=True` in its Event Actions.
    * **Context & State:** Passes the _same_ `InvocationContext` in each iteration, allowing state changes (e.g., counters, flags) to persist across loops.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-1>)# Conceptual Example: Loop with Condition
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-2>)from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-3>)from google.adk.events import Event, EventActions
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-4>)from google.adk.agents.invocation_context import InvocationContext
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-5>)from typing import AsyncGenerator
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-7>)class CheckCondition(BaseAgent): # Custom agent to check state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-8>)    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-9>)        status = ctx.session.state.get("status", "pending")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-10>)        is_done = (status == "completed")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-11>)        yield Event(author=self.name, actions=EventActions(escalate=is_done)) # Escalate if done
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-13>)process_step = LlmAgent(name="ProcessingStep") # Agent that might update state['status']
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-14>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-15>)poller = LoopAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-16>)    name="StatusPoller",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-17>)    max_iterations=10,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-18>)    sub_agents=[process_step, CheckCondition(name="Checker")]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-19>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-20>)# When poller runs, it executes process_step then Checker repeatedly
    [](<https://adk.dev/agents/custom-agents/#__codelineno-23-21>)# until Checker escalates (state['status'] == 'completed') or 10 iterations pass.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-1>)// Conceptual Example: Loop with Condition
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-2>)import { LoopAgent, LlmAgent, BaseAgent, InvocationContext } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-3>)import type { Event, createEventActions, EventActions } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-5>)class CheckConditionAgent extends BaseAgent { // Custom agent to check state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-6>)    async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-7>)        const status = ctx.session.state['status'] || 'pending';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-8>)        const isDone = status === 'completed';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-9>)        yield createEvent({ author: 'check_condition', actions: createEventActions({ escalate: isDone }) });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-10>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-11>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-12>)    async *runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-13>)        // This is not implemented.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-14>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-15>)};
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-16>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-17>)const processStep = new LlmAgent({name: 'ProcessingStep'}); // Agent that might update state['status']
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-18>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-19>)const poller = new LoopAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-20>)    name: 'StatusPoller',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-21>)    maxIterations: 10,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-22>)    // Executes its sub_agents sequentially in a loop
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-23>)    subAgents: [processStep, new CheckConditionAgent ({name: 'Checker'})]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-24>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-25>)// When poller runs, it executes processStep then Checker repeatedly
    [](<https://adk.dev/agents/custom-agents/#__codelineno-24-26>)// until Checker escalates (state['status'] === 'completed') or 10 iterations pass.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-1>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-2>)    "iter"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-3>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-4>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-5>)    "google.golang.org/adk/v2/agent/workflowagents/loopagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-6>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-7>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-9>)// Conceptual Example: Loop with Condition
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-10>)// Custom agent to check state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-11>)checkCondition, _ := agent.New(agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-12>)    Name: "Checker",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-13>)    Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-14>)        return func(yield func(*session.Event, error) bool) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-15>)            status, err := ctx.Session().State().Get("status")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-16>)            // If "status" is not in the state, default to "pending".
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-17>)            // This is idiomatic Go for handling a potential error on lookup.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-18>)            if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-19>)                status = "pending"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-20>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-21>)            isDone := status == "completed"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-22>)            yield(&session.Event{Author: "Checker", Actions: session.EventActions{Escalate: isDone}}, nil)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-23>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-24>)    },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-25>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-26>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-27>)processStep, _ := llmagent.New(llmagent.Config{Name: "ProcessingStep", Model: m}) // Agent that might update state["status"]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-28>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-29>)poller, _ := loopagent.New(loopagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-30>)    MaxIterations: 10,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-31>)    AgentConfig:   agent.Config{Name: "StatusPoller", SubAgents: []agent.Agent{processStep, checkCondition}},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-32>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-33>)// When poller runs, it executes processStep then Checker repeatedly
    [](<https://adk.dev/agents/custom-agents/#__codelineno-25-34>)// until Checker escalates (state["status"] == "completed") or 10 iterations pass.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-1>)// Conceptual Example: Loop with Condition
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-2>)// Custom agent to check state and potentially escalate
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-3>)public static class CheckConditionAgent extends BaseAgent {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-4>)  public CheckConditionAgent(String name, String description) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-5>)    super(name, description, List.of(), null, null);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-6>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-7>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-8>)  @Override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-9>)  protected Flowable<Event> runAsyncImpl(InvocationContext ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-10>)    String status = (String) ctx.session().state().getOrDefault("status", "pending");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-11>)    boolean isDone = "completed".equalsIgnoreCase(status);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-13>)    // Emit an event that signals to escalate (exit the loop) if the condition is met.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-14>)    // If not done, the escalate flag will be false or absent, and the loop continues.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-15>)    Event checkEvent = Event.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-16>)            .author(name())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-17>)            .id(Event.generateEventId()) // Important to give events unique IDs
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-18>)            .actions(EventActions.builder().escalate(isDone).build()) // Escalate if done
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-19>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-20>)    return Flowable.just(checkEvent);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-21>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-22>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-24>)// Agent that might update state.put("status")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-25>)LlmAgent processingStepAgent = LlmAgent.builder().name("ProcessingStep").build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-26>)// Custom agent instance for checking the condition
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-27>)CheckConditionAgent conditionCheckerAgent = new CheckConditionAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-28>)    "ConditionChecker",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-29>)    "Checks if the status is 'completed'."
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-30>));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-31>)LoopAgent poller = LoopAgent.builder().name("StatusPoller").maxIterations(10).subAgents(processingStepAgent, conditionCheckerAgent).build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-32>)// When poller runs, it executes processingStepAgent then conditionCheckerAgent repeatedly
    [](<https://adk.dev/agents/custom-agents/#__codelineno-26-33>)// until Checker escalates (state.get("status") == "completed") or 10 iterations pass.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-1>)class CheckConditionAgent(name: String) : BaseAgent(name = name) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-2>)    override fun runAsyncImpl(context: InvocationContext): Flow<Event> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-3>)        val status = context.session.state["status"] as? String ?: "pending"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-4>)        val isDone = status == "completed"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-5>)        return flowOf(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-6>)            Event(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-7>)                author = name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-8>)                actions = EventActions(escalate = isDone),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-9>)            ),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-10>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-11>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-12>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-13>)val processStep = LlmAgent(name = "ProcessingStep", model = model)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-14>)val checker = CheckConditionAgent(name = "Checker")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-15>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-16>)val poller =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-17>)    LoopAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-18>)        name = "StatusPoller",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-19>)        maxIterations = 10,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-20>)        subAgents = listOf(processStep, checker),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-27-21>)    )
    
### Interaction and communication mechanisms[¶](<https://adk.dev/agents/custom-agents/#interaction-and-communication-mechanisms> "Permanent link")

Agents within a system often need to exchange data or trigger actions in one another. ADK facilitates this through:

#### Shared session state[¶](<https://adk.dev/agents/custom-agents/#shared-session-state> "Permanent link")

The most fundamental way for agents operating within the same invocation (and thus sharing the same [`Session`](<https://adk.dev/sessions/session/>) object via the `InvocationContext`) to communicate passively.

  * **Mechanism:** One agent (or its tool/callback) writes a value (`context.state['data_key'] = processed_data`), and a subsequent agent reads it (`data = context.state.get('data_key')`). State changes are tracked via [`CallbackContext`](<https://adk.dev/callbacks/>).
  * **Convenience:** The `output_key` property on [`LlmAgent`](<https://adk.dev/agents/llm-agents/>) automatically saves the agent's final response text (or structured output) to the specified state key.
  * **Nature:** Asynchronous, passive communication. Ideal for pipelines orchestrated by `SequentialAgent` or passing data across `LoopAgent` iterations.
  * **See Also:** [State Management](<https://adk.dev/sessions/state/>)

Invocation Context and `temp:` State

When a parent agent invokes a sub-agent, it passes the same `InvocationContext`. This means they share the same temporary (`temp:`) state, which is ideal for passing data that is only relevant for the current turn.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-1>)# Conceptual Example: Using output_key and reading state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-2>)from google.adk.agents import LlmAgent, SequentialAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-5>)agent_A = LlmAgent(name="AgentA", instruction="Find the capital of France.", output_key="capital_city")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-6>)agent_B = LlmAgent(name="AgentB", instruction="Tell me about the city stored in {capital_city}.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-7>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-9>)pipeline = SequentialAgent(name="CityInfo", sub_agents=[agent_A, agent_B])
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-10>)# AgentA runs, saves "Paris" to state['capital_city'].
    [](<https://adk.dev/agents/custom-agents/#__codelineno-28-11>)# AgentB runs, its instruction processor reads state['capital_city'] to get "Paris".
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-1>)// Conceptual Example: Using outputKey and reading state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-2>)import { LlmAgent, SequentialAgent } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-4>)const agentA = new LlmAgent({name: 'AgentA', instruction: 'Find the capital of France.', outputKey: 'capital_city'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-5>)const agentB = new LlmAgent({name: 'AgentB', instruction: 'Tell me about the city stored in {capital_city}.'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-7>)const pipeline = new SequentialAgent({name: 'CityInfo', subAgents: [agentA, agentB]});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-8>)// AgentA runs, saves "Paris" to state['capital_city'].
    [](<https://adk.dev/agents/custom-agents/#__codelineno-29-9>)// AgentB runs, its instruction processor reads state['capital_city'] to get "Paris".
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-1>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-4>)    "google.golang.org/adk/v2/agent/workflowagents/sequentialagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-5>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-7>)// Conceptual Example: Using output_key and reading state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-8>)agentA, _ := llmagent.New(llmagent.Config{Name: "AgentA", Instruction: "Find the capital of France.", OutputKey: "capital_city", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-9>)agentB, _ := llmagent.New(llmagent.Config{Name: "AgentB", Instruction: "Tell me about the city stored in {capital_city}.", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-11>)pipeline2, _ := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-12>)    AgentConfig: agent.Config{Name: "CityInfo", SubAgents: []agent.Agent{agentA, agentB}},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-13>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-14>)// AgentA runs, saves "Paris" to state["capital_city"].
    [](<https://adk.dev/agents/custom-agents/#__codelineno-30-15>)// AgentB runs, its instruction processor reads state["capital_city"] to get "Paris".
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-1>)// Conceptual Example: Using outputKey and reading state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-3>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-5>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-6>)LlmAgent agentA = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-7>)    .name("AgentA")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-8>)    .instruction("Find the capital of France.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-9>)    .outputKey("capital_city")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-10>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-11>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-13>)LlmAgent agentB = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-14>)    .name("AgentB")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-15>)    .instruction("Tell me about the city stored in {capital_city}.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-16>)    .outputKey("capital_city")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-17>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-18>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-19>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-20>)SequentialAgent pipeline = SequentialAgent.builder().name("CityInfo").subAgents(agentA, agentB).build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-21>)// AgentA runs, saves "Paris" to state('capital_city').
    [](<https://adk.dev/agents/custom-agents/#__codelineno-31-22>)// AgentB runs, its instruction processor reads state.get("capital_city") to get "Paris".
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-1>)val agentA =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-2>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-3>)        name = "AgentA",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-4>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-5>)        instruction = Instruction("Find the capital of France."),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-6>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-7>)val agentB =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-8>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-9>)        name = "AgentB",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-10>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-11>)        instruction = Instruction("Tell me about the city stored in state."),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-12>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-13>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-32-14>)val cityPipeline = SequentialAgent(name = "CityInfo", subAgents = listOf(agentA, agentB))
    
#### LLM delegation and agent transfer[¶](<https://adk.dev/agents/custom-agents/#delegation> "Permanent link")

Leverages an [`LlmAgent`](<https://adk.dev/agents/llm-agents/>)'s understanding to dynamically route tasks to other suitable agents within the hierarchy.

  * **Mechanism:** The agent's LLM generates a specific function call: `transfer_to_agent(agent_name='target_agent_name')`.
  * **Handling:** The `AutoFlow`, used by default when sub-agents are present or transfer isn't disallowed, intercepts this call. It identifies the target agent using `root_agent.find_agent()` and updates the `InvocationContext` to switch execution focus.
  * **Requires:** The calling `LlmAgent` needs clear `instructions` on when to transfer, and potential target agents need distinct `description`s for the LLM to make informed decisions. Transfer scope (parent, sub-agent, siblings) can be configured on the `LlmAgent`.
  * **Nature:** Dynamic, flexible routing based on LLM interpretation.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-1>)# Conceptual Setup: LLM Transfer
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-2>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-5>)booking_agent = LlmAgent(name="Booker", description="Handles flight and hotel bookings.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-6>)info_agent = LlmAgent(name="Info", description="Provides general information and answers questions.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-7>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-9>)coordinator = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-10>)    name="Coordinator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-11>)    model="gemini-flash-latest",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-12>)    instruction="You are an assistant. Delegate booking tasks to Booker and info requests to Info.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-13>)    description="Main coordinator.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-14>)    # AutoFlow is typically used implicitly here
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-15>)    sub_agents=[booking_agent, info_agent]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-16>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-17>)# If coordinator receives "Book a flight", its LLM should generate:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-18>)# FunctionCall(name='transfer_to_agent', args={'agent_name': 'Booker'})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-33-19>)# ADK framework then routes execution to booking_agent.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-1>)// Conceptual Setup: LLM Transfer
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-2>)import { LlmAgent } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-4>)const bookingAgent = new LlmAgent({name: 'Booker', description: 'Handles flight and hotel bookings.'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-5>)const infoAgent = new LlmAgent({name: 'Info', description: 'Provides general information and answers questions.'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-7>)const coordinator = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-8>)    name: 'Coordinator',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-9>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-10>)    instruction: 'You are an assistant. Delegate booking tasks to Booker and info requests to Info.',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-11>)    description: 'Main coordinator.',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-12>)    // AutoFlow is typically used implicitly here
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-13>)    subAgents: [bookingAgent, infoAgent]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-14>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-15>)// If coordinator receives "Book a flight", its LLM should generate:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-16>)// {functionCall: {name: 'transfer_to_agent', args: {agent_name: 'Booker'}}}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-34-17>)// ADK framework then routes execution to bookingAgent.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-1>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-2>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-3>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-5>)// Conceptual Setup: LLM Transfer
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-6>)bookingAgent, _ := llmagent.New(llmagent.Config{Name: "Booker", Description: "Handles flight and hotel bookings.", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-7>)infoAgent, _ := llmagent.New(llmagent.Config{Name: "Info", Description: "Provides general information and answers questions.", Model: m})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-9>)coordinator, _ = llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-10>)    Name:        "Coordinator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-11>)    Model:       m,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-12>)    Instruction: "You are an assistant. Delegate booking tasks to Booker and info requests to Info.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-13>)    Description: "Main coordinator.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-14>)    SubAgents:   []agent.Agent{bookingAgent, infoAgent},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-15>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-16>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-17>)// If coordinator receives "Book a flight", its LLM should generate:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-18>)// FunctionCall{Name: "transfer_to_agent", Args: map[string]any{"agent_name": "Booker"}}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-35-19>)// ADK framework then routes execution to bookingAgent.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-1>)// Conceptual Setup: LLM Transfer
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-5>)LlmAgent bookingAgent = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-6>)    .name("Booker")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-7>)    .description("Handles flight and hotel bookings.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-8>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-11>)LlmAgent infoAgent = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-12>)    .name("Info")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-13>)    .description("Provides general information and answers questions.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-14>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-15>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-16>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-17>)// Define the coordinator agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-18>)LlmAgent coordinator = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-19>)    .name("Coordinator")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-20>)    .model("gemini-flash-latest") // Or your desired model
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-21>)    .instruction("You are an assistant. Delegate booking tasks to Booker and info requests to Info.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-22>)    .description("Main coordinator.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-23>)    // AutoFlow will be used by default (implicitly) because subAgents are present
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-24>)    // and transfer is not disallowed.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-25>)    .subAgents(bookingAgent, infoAgent)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-26>)    .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-27>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-28>)// If coordinator receives "Book a flight", its LLM should generate:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-29>)// FunctionCall.builder.name("transferToAgent").args(ImmutableMap.of("agent_name", "Booker")).build()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-36-30>)// ADK framework then routes execution to bookingAgent.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-1>)val bookingAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-2>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-3>)        name = "Booker",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-4>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-5>)        description = "Handles flight and hotel bookings.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-6>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-7>)val infoAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-8>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-9>)        name = "Info",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-10>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-11>)        description = "Provides general information and answers questions.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-12>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-13>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-14>)val transferCoordinator =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-15>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-16>)        name = "Coordinator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-17>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-18>)        instruction =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-19>)            Instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-20>)                "You are an assistant. Delegate booking tasks to Booker and info requests to Info.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-21>)            ),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-22>)        description = "Main coordinator.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-23>)        subAgents = listOf(bookingAgent, infoAgent),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-37-24>)    )
    
#### Explicit invocation with `AgentTool`[¶](<https://adk.dev/agents/custom-agents/#explicit-invocation-with-agenttool> "Permanent link")

Allows an [`LlmAgent`](<https://adk.dev/agents/llm-agents/>) to treat another `BaseAgent` instance as a callable function or [Tool](<https://adk.dev/tools-custom/>).

  * **Mechanism:** Wrap the target agent instance in `AgentTool` and include it in the parent `LlmAgent`'s `tools` list. `AgentTool` generates a corresponding function declaration for the LLM.
  * **Handling:** When the parent LLM generates a function call targeting the `AgentTool`, the framework executes `AgentTool.run_async`. This method runs the target agent, captures its final response, forwards any state/artifact changes back to the parent's context, and returns the response as the tool's result.
  * **Nature:** Synchronous (within the parent's flow), explicit, controlled invocation like any other tool.
  * **(Note:** `AgentTool` needs to be imported and used explicitly).

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-1>)# Conceptual Setup: Agent as a Tool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-2>)from google.adk import Event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-3>)from google.adk.agents import LlmAgent, BaseAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-4>)from google.adk.tools import agent_tool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-5>)from google.genai import types
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-6>)from pydantic import BaseModel
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-7>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-9>)# Define a target agent (could be LlmAgent or custom BaseAgent)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-10>)class ImageGeneratorAgent(BaseAgent): # Example custom agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-11>)    name: str = "ImageGen"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-12>)    description: str = "Generates an image based on a prompt."
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-13>)    # ... internal logic ...
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-14>)    async def _run_async_impl(self, ctx): # Simplified run logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-15>)        prompt = ctx.session.state.get("image_prompt", "default prompt")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-16>)        # ... generate image bytes ...
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-17>)        image_bytes = b"..."
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-18>)        yield Event(author=self.name, content=types.Content(parts=[types.Part.from_bytes(image_bytes, "image/png")]))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-19>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-20>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-21>)image_agent = ImageGeneratorAgent()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-22>)image_tool = agent_tool.AgentTool(agent=image_agent) # Wrap the agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-24>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-25>)# Parent agent uses the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-26>)artist_agent = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-27>)    name="Artist",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-28>)    model="gemini-flash-latest",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-29>)    instruction="Create a prompt and use the ImageGen tool to generate the image.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-30>)    tools=[image_tool] # Include the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-31>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-32>)# Artist LLM generates a prompt, then calls:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-33>)# FunctionCall(name='ImageGen', args={'image_prompt': 'a cat wearing a hat'})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-34>)# Framework calls image_tool.run_async(...), which runs ImageGeneratorAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-38-35>)# The resulting image Part is returned to the Artist agent as the tool result.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-1>)// Conceptual Setup: Agent as a Tool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-2>)import { LlmAgent, BaseAgent, AgentTool, InvocationContext } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-3>)import type { Part, createEvent, Event } from '@google/genai';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-5>)// Define a target agent (could be LlmAgent or custom BaseAgent)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-6>)class ImageGeneratorAgent extends BaseAgent { // Example custom agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-7>)    constructor() {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-8>)        super({name: 'ImageGen', description: 'Generates an image based on a prompt.'});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-9>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-10>)    // ... internal logic ...
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-11>)    async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event> { // Simplified run logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-12>)        const prompt = ctx.session.state['image_prompt'] || 'default prompt';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-13>)        // ... generate image bytes ...
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-14>)        const imageBytes = new Uint8Array(); // placeholder
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-15>)        const imagePart: Part = {inlineData: {data: Buffer.from(imageBytes).toString('base64'), mimeType: 'image/png'}};
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-16>)        yield createEvent({content: {parts: [imagePart]}});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-17>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-18>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-19>)    async *runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event, void, void> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-20>)        // Not implemented for this agent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-21>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-22>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-24>)const imageAgent = new ImageGeneratorAgent();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-25>)const imageTool = new AgentTool({agent: imageAgent}); // Wrap the agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-26>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-27>)// Parent agent uses the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-28>)const artistAgent = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-29>)    name: 'Artist',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-30>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-31>)    instruction: 'Create a prompt and use the ImageGen tool to generate the image.',
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-32>)    tools: [imageTool] // Include the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-33>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-34>)// Artist LLM generates a prompt, then calls:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-35>)// {functionCall: {name: 'ImageGen', args: {image_prompt: 'a cat wearing a hat'}}}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-36>)// Framework calls imageTool.runAsync(...), which runs ImageGeneratorAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-39-37>)// The resulting image Part is returned to the Artist agent as the tool result.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-1>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-2>)    "fmt"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-3>)    "iter"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-4>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-5>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-6>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-7>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-8>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-9>)    "google.golang.org/adk/v2/tool/agenttool"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-10>)    "google.golang.org/genai"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-11>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-13>)// Conceptual Setup: Agent as a Tool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-14>)// Define a target agent (could be LlmAgent or custom BaseAgent)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-15>)imageAgent, _ := agent.New(agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-16>)    Name:        "ImageGen",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-17>)    Description: "Generates an image based on a prompt.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-18>)    Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-19>)        return func(yield func(*session.Event, error) bool) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-20>)            prompt, _ := ctx.Session().State().Get("image_prompt")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-21>)            fmt.Printf("Generating image for prompt: %v\n", prompt)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-22>)            imageBytes := []byte("...") // Simulate image bytes
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-23>)            yield(&session.Event{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-24>)                Author: "ImageGen",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-25>)                LLMResponse: model.LLMResponse{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-26>)                    Content: &genai.Content{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-27>)                        Parts: []*genai.Part{genai.NewPartFromBytes(imageBytes, "image/png")},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-28>)                    },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-29>)                },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-30>)            }, nil)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-31>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-32>)    },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-33>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-34>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-35>)// Wrap the agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-36>)imageTool := agenttool.New(imageAgent, nil)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-37>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-38>)// Now imageTool can be used as a tool by other agents.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-39>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-40>)// Parent agent uses the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-41>)artistAgent, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-42>)    Name:        "Artist",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-43>)    Model:       m,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-44>)    Instruction: "Create a prompt and use the ImageGen tool to generate the image.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-45>)    Tools:       []tool.Tool{imageTool}, // Include the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-46>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-47>)// Artist LLM generates a prompt, then calls:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-48>)// FunctionCall{Name: "ImageGen", Args: map[string]any{"image_prompt": "a cat wearing a hat"}}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-49>)// Framework calls imageTool.Run(...), which runs ImageGeneratorAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-40-50>)// The resulting image Part is returned to the Artist agent as the tool result.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-1>)// Conceptual Setup: Agent as a Tool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-2>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-4>)import com.google.adk.tools.AgentTool;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-5>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-6>)// Example custom agent (could be LlmAgent or custom BaseAgent)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-7>)public class ImageGeneratorAgent extends BaseAgent  {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-10>)  public ImageGeneratorAgent(String name, String description) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-11>)    super(name, description, List.of(), null, null);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-12>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-13>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-14>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-15>)  // ... internal logic ...
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-16>)  @Override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-17>)  protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) { // Simplified run logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-18>)    invocationContext.session().state().get("image_prompt");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-19>)    // Generate image bytes
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-20>)    // ...
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-21>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-22>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-23>)    Event responseEvent = Event.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-24>)        .author(this.name())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-25>)        .content(Content.fromParts(Part.fromText("...")))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-26>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-27>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-28>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-29>)    return Flowable.just(responseEvent);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-30>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-31>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-32>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-33>)  @Override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-34>)  protected Flowable<Event> runLiveImpl(InvocationContext invocationContext) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-35>)    return null;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-36>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-37>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-38>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-39>)// Wrap the agent using AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-40>)ImageGeneratorAgent imageAgent = new ImageGeneratorAgent("image_agent", "generates images");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-41>)AgentTool imageTool = AgentTool.create(imageAgent);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-42>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-43>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-44>)// Parent agent uses the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-45>)LlmAgent artistAgent = LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-46>)        .name("Artist")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-47>)        .model("gemini-flash-latest")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-48>)        .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-49>)                "You are an artist. Create a detailed prompt for an image and then " +
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-50>)                        "use the 'ImageGen' tool to generate the image. " +
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-51>)                        "The 'ImageGen' tool expects a single string argument named 'request' " +
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-52>)                        "containing the image prompt. The tool will return a JSON string in its " +
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-53>)                        "'result' field, containing 'image_base64', 'mime_type', and 'status'."
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-54>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-55>)        .description("An agent that can create images using a generation tool.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-56>)        .tools(imageTool) // Include the AgentTool
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-57>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-58>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-59>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-60>)// Artist LLM generates a prompt, then calls:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-61>)// FunctionCall(name='ImageGen', args={'imagePrompt': 'a cat wearing a hat'})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-62>)// Framework calls imageTool.runAsync(...), which runs ImageGeneratorAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-41-63>)// The resulting image Part is returned to the Artist agent as the tool result.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-1>)val imageAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-2>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-3>)        name = "ImageGen",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-4>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-5>)        description = "Generates an image based on a prompt.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-6>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-7>)val imageTool = AgentTool(agent = imageAgent)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-9>)val artistAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-10>)    LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-11>)        name = "Artist",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-12>)        model = model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-13>)        instruction =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-14>)            Instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-15>)                "Create a prompt and use the ImageGen tool to generate the image.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-16>)            ),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-17>)        tools = listOf(imageTool),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-42-18>)    )
    
These primitives provide the flexibility to design multi-agent interactions ranging from tightly coupled sequential workflows to dynamic, LLM-driven delegation networks.

## Design pattern example: StoryFlow Agent[¶](<https://adk.dev/agents/custom-agents/#design-pattern-example-storyflow-agent> "Permanent link")

Let's illustrate the power of custom agents with an example pattern: a multi-stage content generation workflow with conditional logic.

**Goal:** Create a system that generates a story, iteratively refines it through critique and revision, performs final checks, and crucially, _regenerates the story if the final tone check fails_.

**Why Custom?** The core requirement driving the need for a custom agent here is the **conditional regeneration based on the tone check**. Standard workflow agents don't have built-in conditional branching based on the outcome of a sub-agent's task. We need custom logic (`if tone == "negative": ...`) within the orchestrator.

* * *

### Part 1: Simplified custom agent initialization[¶](<https://adk.dev/agents/custom-agents/#part-1-simplified-custom-agent-initialization> "Permanent link")

PythonTypeScriptGoJava

We define the `StoryFlowAgent` inheriting from `BaseAgent`. In `__init__`, we store the necessary sub-agents (passed in) as instance attributes and tell the `BaseAgent` framework about the top-level agents this custom agent will directly orchestrate.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-1>)class StoryFlowAgent(BaseAgent):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-2>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-3>)    Custom agent for a story generation and refinement workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-5>)    This agent orchestrates a sequence of LLM agents to generate a story,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-6>)    critique it, revise it, check grammar and tone, and potentially
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-7>)    regenerate the story if the tone is negative.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-8>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-10>)    # --- Field Declarations for Pydantic ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-11>)    # Declare the agents passed during initialization as class attributes with type hints
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-12>)    story_generator: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-13>)    critic: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-14>)    reviser: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-15>)    grammar_check: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-16>)    tone_check: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-17>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-18>)    loop_agent: LoopAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-19>)    sequential_agent: SequentialAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-20>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-21>)    # model_config allows setting Pydantic configurations if needed, e.g., arbitrary_types_allowed
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-22>)    model_config = {"arbitrary_types_allowed": True}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-24>)    def __init__(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-25>)        self,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-26>)        name: str,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-27>)        story_generator: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-28>)        critic: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-29>)        reviser: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-30>)        grammar_check: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-31>)        tone_check: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-32>)    ):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-33>)        """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-34>)        Initializes the StoryFlowAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-35>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-36>)        Args:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-37>)            name: The name of the agent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-38>)            story_generator: An LlmAgent to generate the initial story.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-39>)            critic: An LlmAgent to critique the story.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-40>)            reviser: An LlmAgent to revise the story based on criticism.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-41>)            grammar_check: An LlmAgent to check the grammar.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-42>)            tone_check: An LlmAgent to analyze the tone.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-43>)        """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-44>)        # Create internal agents *before* calling super().__init__
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-45>)        loop_agent = LoopAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-46>)            name="CriticReviserLoop", sub_agents=[critic, reviser], max_iterations=2
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-47>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-48>)        sequential_agent = SequentialAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-49>)            name="PostProcessing", sub_agents=[grammar_check, tone_check]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-50>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-51>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-52>)        # Define the sub_agents list for the framework
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-53>)        sub_agents_list = [
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-54>)            story_generator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-55>)            loop_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-56>)            sequential_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-57>)        ]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-58>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-59>)        # Pydantic will validate and assign them based on the class annotations.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-60>)        super().__init__(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-61>)            name=name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-62>)            story_generator=story_generator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-63>)            critic=critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-64>)            reviser=reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-65>)            grammar_check=grammar_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-66>)            tone_check=tone_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-67>)            loop_agent=loop_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-68>)            sequential_agent=sequential_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-69>)            sub_agents=sub_agents_list, # Pass the sub_agents list directly
    [](<https://adk.dev/agents/custom-agents/#__codelineno-43-70>)        )
    
We define the `StoryFlowAgent` by extending `BaseAgent`. In its constructor, we: 1\. Create any internal composite agents (like `LoopAgent` or `SequentialAgent`). 2\. Pass the list of all top-level sub-agents to the `super()` constructor. 3\. Store the sub-agents (passed in or created internally) as instance properties (e.g., `this.storyGenerator`) so they can be accessed in the custom `runImpl` logic.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-1>)class StoryFlowAgent extends BaseAgent {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-2>)  // --- Property Declarations for TypeScript ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-3>)  private storyGenerator: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-4>)  private critic: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-5>)  private reviser: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-6>)  private grammarCheck: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-7>)  private toneCheck: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-9>)  private loopAgent: LoopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-10>)  private sequentialAgent: SequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-11>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-12>)  constructor(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-13>)    name: string,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-14>)    storyGenerator: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-15>)    critic: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-16>)    reviser: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-17>)    grammarCheck: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-18>)    toneCheck: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-19>)  ) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-20>)    // Create internal composite agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-21>)    const loopAgent = new LoopAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-22>)      name: "CriticReviserLoop",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-23>)      subAgents: [critic, reviser],
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-24>)      maxIterations: 2,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-25>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-26>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-27>)    const sequentialAgent = new SequentialAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-28>)      name: "PostProcessing",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-29>)      subAgents: [grammarCheck, toneCheck],
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-30>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-31>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-32>)    // Define the sub-agents for the framework to know about
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-33>)    const subAgentsList = [
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-34>)      storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-35>)      loopAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-36>)      sequentialAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-37>)    ];
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-38>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-39>)    // Call the parent constructor
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-40>)    super({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-41>)      name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-42>)      subAgents: subAgentsList,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-43>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-44>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-45>)    // Assign agents to class properties for use in the custom run logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-46>)    this.storyGenerator = storyGenerator;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-47>)    this.critic = critic;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-48>)    this.reviser = reviser;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-49>)    this.grammarCheck = grammarCheck;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-50>)    this.toneCheck = toneCheck;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-51>)    this.loopAgent = loopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-52>)    this.sequentialAgent = sequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-44-53>)  }
    
We define the `StoryFlowAgent` struct and a constructor. In the constructor, we store the necessary sub-agents and tell the `BaseAgent` framework about the top-level agents this custom agent will directly orchestrate.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-1>)// StoryFlowAgent is a custom agent that orchestrates a story generation workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-2>)// It encapsulates the logic of running sub-agents in a specific sequence.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-3>)type StoryFlowAgent struct {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-4>)    storyGenerator     agent.Agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-5>)    revisionLoopAgent  agent.Agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-6>)    postProcessorAgent agent.Agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-7>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-9>)// NewStoryFlowAgent creates and configures the entire custom agent workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-10>)// It takes individual LLM agents as input and internally creates the necessary
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-11>)// workflow agents (loop, sequential), returning the final orchestrator agent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-12>)func NewStoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-13>)    storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-14>)    critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-15>)    reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-16>)    grammarCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-17>)    toneCheck agent.Agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-18>)) (agent.Agent, error) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-19>)    loopAgent, err := loopagent.New(loopagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-20>)        MaxIterations: 2,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-21>)        AgentConfig: agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-22>)            Name:      "CriticReviserLoop",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-23>)            SubAgents: []agent.Agent{critic, reviser},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-24>)        },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-25>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-26>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-27>)        return nil, fmt.Errorf("failed to create loop agent: %w", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-28>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-29>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-30>)    sequentialAgent, err := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-31>)        AgentConfig: agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-32>)            Name:      "PostProcessing",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-33>)            SubAgents: []agent.Agent{grammarCheck, toneCheck},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-34>)        },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-35>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-36>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-37>)        return nil, fmt.Errorf("failed to create sequential agent: %w", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-38>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-39>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-40>)    // The StoryFlowAgent struct holds the agents needed for the Run method.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-41>)    orchestrator := &StoryFlowAgent{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-42>)        storyGenerator:     storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-43>)        revisionLoopAgent:  loopAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-44>)        postProcessorAgent: sequentialAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-45>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-46>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-47>)    // agent.New creates the final agent, wiring up the Run method.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-48>)    return agent.New(agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-49>)        Name:        "StoryFlowAgent",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-50>)        Description: "Orchestrates story generation, critique, revision, and checks.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-51>)        SubAgents:   []agent.Agent{storyGenerator, loopAgent, sequentialAgent},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-52>)        Run:         orchestrator.Run,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-53>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-45-54>)}
    
We define the `StoryFlowAgentExample` by extending `BaseAgent`. In its **constructor** , we store the necessary sub-agent instances (passed as parameters) as instance fields. These top-level sub-agents, which this custom agent will directly orchestrate, are also passed to the `super` constructor of `BaseAgent` as a list.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-1>)private final LlmAgent storyGenerator;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-2>)private final LoopAgent loopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-3>)private final SequentialAgent sequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-4>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-5>)public StoryFlowAgentExample(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-6>)    String name, LlmAgent storyGenerator, LoopAgent loopAgent, SequentialAgent sequentialAgent) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-7>)  super(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-8>)      name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-9>)      "Orchestrates story generation, critique, revision, and checks.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-10>)      List.of(storyGenerator, loopAgent, sequentialAgent),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-11>)      null,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-12>)      null);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-13>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-14>)  this.storyGenerator = storyGenerator;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-15>)  this.loopAgent = loopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-16>)  this.sequentialAgent = sequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-46-17>)}
    
* * *

### Part 2: Define custom execution logic[¶](<https://adk.dev/agents/custom-agents/#part-2-define-custom-execution-logic> "Permanent link")

PythonTypeScriptGoJava

This method orchestrates the sub-agents using standard Python async/await and control flow.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-1>)@override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-2>)async def _run_async_impl(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-3>)    self, ctx: InvocationContext
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-4>)) -> AsyncGenerator[Event, None]:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-5>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-6>)    Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-7>)    Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-8>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-9>)    logger.info(f"[{self.name}] Starting story generation workflow.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-11>)    # 1. Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-12>)    logger.info(f"[{self.name}] Running StoryGenerator...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-13>)    async for event in self.story_generator.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-14>)        logger.info(f"[{self.name}] Event from StoryGenerator: {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-15>)        yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-16>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-17>)    # Check if story was generated before proceeding
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-18>)    if "current_story" not in ctx.session.state or not ctx.session.state["current_story"]:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-19>)         logger.error(f"[{self.name}] Failed to generate initial story. Aborting workflow.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-20>)         return # Stop processing if initial story failed
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-21>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-22>)    logger.info(f"[{self.name}] Story state after generator: {ctx.session.state.get('current_story')}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-24>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-25>)    # 2. Critic-Reviser Loop
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-26>)    logger.info(f"[{self.name}] Running CriticReviserLoop...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-27>)    # Use the loop_agent instance attribute assigned during init
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-28>)    async for event in self.loop_agent.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-29>)        logger.info(f"[{self.name}] Event from CriticReviserLoop: {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-30>)        yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-31>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-32>)    logger.info(f"[{self.name}] Story state after loop: {ctx.session.state.get('current_story')}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-33>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-34>)    # 3. Sequential Post-Processing (Grammar and Tone Check)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-35>)    logger.info(f"[{self.name}] Running PostProcessing...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-36>)    # Use the sequential_agent instance attribute assigned during init
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-37>)    async for event in self.sequential_agent.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-38>)        logger.info(f"[{self.name}] Event from PostProcessing: {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-39>)        yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-40>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-41>)    # 4. Tone-Based Conditional Logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-42>)    tone_check_result = ctx.session.state.get("tone_check_result")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-43>)    logger.info(f"[{self.name}] Tone check result: {tone_check_result}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-44>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-45>)    if tone_check_result == "negative":
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-46>)        logger.info(f"[{self.name}] Tone is negative. Regenerating story...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-47>)        async for event in self.story_generator.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-48>)            logger.info(f"[{self.name}] Event from StoryGenerator (Regen): {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-49>)            yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-50>)    else:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-51>)        logger.info(f"[{self.name}] Tone is not negative. Keeping current story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-52>)        pass
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-53>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-47-54>)    logger.info(f"[{self.name}] Workflow finished.")
    
**Explanation of Logic:**

  1. The initial `story_generator` runs. Its output is expected to be in `ctx.session.state["current_story"]`.
  2. The `loop_agent` runs, which internally calls the `critic` and `reviser` sequentially for `max_iterations` times. They read/write `current_story` and `criticism` from/to the state.
  3. The `sequential_agent` runs, calling `grammar_check` then `tone_check`, reading `current_story` and writing `grammar_suggestions` and `tone_check_result` to the state.
  4. **Custom Part:** The `if` statement checks the `tone_check_result` from the state. If it's "negative", the `story_generator` is called _again_ , overwriting the `current_story` in the state. Otherwise, the flow ends.

The `runImpl` method orchestrates the sub-agents using standard TypeScript `async`/`await` and control flow. The `runLiveImpl` is also added to handle live streaming scenarios.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-1>)// Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-2>)async* runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-3>)  yield* this.runAsyncImpl(ctx);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-4>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-5>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-6>)// Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-7>)async* runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-8>)  console.log(`[${this.name}] Starting story generation workflow.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-10>)  // 1. Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-11>)  console.log(`[${this.name}] Running StoryGenerator...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-12>)  for await (const event of this.storyGenerator.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-13>)    console.log(`[${this.name}] Event from StoryGenerator: ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-14>)    yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-15>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-16>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-17>)  // Check if the story was generated before proceeding
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-18>)  if (!ctx.session.state["current_story"]) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-19>)    console.error(`[${this.name}] Failed to generate initial story. Aborting workflow.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-20>)    return; // Stop processing
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-21>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-22>)  console.log(`[${this.name}] Story state after generator: ${ctx.session.state['current_story']}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-24>)  // 2. Critic-Reviser Loop
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-25>)  console.log(`[${this.name}] Running CriticReviserLoop...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-26>)  for await (const event of this.loopAgent.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-27>)    console.log(`[${this.name}] Event from CriticReviserLoop: ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-28>)    yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-29>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-30>)  console.log(`[${this.name}] Story state after loop: ${ctx.session.state['current_story']}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-31>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-32>)  // 3. Sequential Post-Processing (Grammar and Tone Check)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-33>)  console.log(`[${this.name}] Running PostProcessing...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-34>)  for await (const event of this.sequentialAgent.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-35>)    console.log(`[${this.name}] Event from PostProcessing: ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-36>)    yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-37>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-38>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-39>)  // 4. Tone-Based Conditional Logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-40>)  const toneCheckResult = ctx.session.state["tone_check_result"] as string;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-41>)  console.log(`[${this.name}] Tone check result: ${toneCheckResult}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-42>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-43>)  if (toneCheckResult === "negative") {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-44>)    console.log(`[${this.name}] Tone is negative. Regenerating story...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-45>)    for await (const event of this.storyGenerator.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-46>)      console.log(`[${this.name}] Event from StoryGenerator (Regen): ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-47>)      yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-48>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-49>)  } else {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-50>)    console.log(`[${this.name}] Tone is not negative. Keeping current story.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-51>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-52>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-53>)  console.log(`[${this.name}] Workflow finished.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-48-54>)}
    
**Explanation of Logic:**

  1. The initial `storyGenerator` runs. Its output is expected to be in `ctx.session.state['current_story']`.
  2. The `loopAgent` runs, which internally calls the `critic` and `reviser` sequentially for `maxIterations` times. They read/write `current_story` and `criticism` from/to the state.
  3. The `sequentialAgent` runs, calling `grammarCheck` then `toneCheck`, reading `current_story` and writing `grammar_suggestions` and `tone_check_result` to the state.
  4. **Custom Part:** The `if` statement checks the `tone_check_result` from the state. If it's "negative", the `storyGenerator` is called _again_ , overwriting the `current_story` in the state. Otherwise, the flow ends.

The `Run` method orchestrates the sub-agents by calling their respective `Run` methods in a loop and yielding their events.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-1>)// Run defines the custom execution logic for the StoryFlowAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-2>)func (s *StoryFlowAgent) Run(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-3>)    return func(yield func(*session.Event, error) bool) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-4>)        // Stage 1: Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-5>)        for event, err := range s.storyGenerator.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-6>)            if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-7>)                yield(nil, fmt.Errorf("story generator failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-8>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-9>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-10>)            if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-11>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-12>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-13>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-14>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-15>)        // Check if story was generated before proceeding
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-16>)        currentStory, err := ctx.Session().State().Get("current_story")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-17>)        if err != nil || currentStory == "" {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-18>)            log.Println("Failed to generate initial story. Aborting workflow.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-19>)            return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-20>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-21>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-22>)        // Stage 2: Critic-Reviser Loop
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-23>)        for event, err := range s.revisionLoopAgent.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-24>)            if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-25>)                yield(nil, fmt.Errorf("loop agent failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-26>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-27>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-28>)            if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-29>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-30>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-31>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-32>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-33>)        // Stage 3: Post-Processing
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-34>)        for event, err := range s.postProcessorAgent.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-35>)            if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-36>)                yield(nil, fmt.Errorf("sequential agent failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-37>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-38>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-39>)            if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-40>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-41>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-42>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-43>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-44>)        // Stage 4: Conditional Regeneration
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-45>)        toneResult, err := ctx.Session().State().Get("tone_check_result")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-46>)        if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-47>)            log.Printf("Could not read tone_check_result from state: %v. Assuming tone is not negative.", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-48>)            return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-49>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-50>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-51>)        if tone, ok := toneResult.(string); ok && tone == "negative" {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-52>)            log.Println("Tone is negative. Regenerating story...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-53>)            for event, err := range s.storyGenerator.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-54>)                if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-55>)                    yield(nil, fmt.Errorf("story regeneration failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-56>)                    return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-57>)                }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-58>)                if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-59>)                    return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-60>)                }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-61>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-62>)        } else {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-63>)            log.Println("Tone is not negative. Keeping current story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-64>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-65>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-49-66>)}
    
**Explanation of Logic:**

  1. The initial `storyGenerator` runs. Its output is expected to be in the session state under the key `"current_story"`.
  2. The `revisionLoopAgent` runs, which internally calls the `critic` and `reviser` sequentially for `max_iterations` times. They read/write `current_story` and `criticism` from/to the state.
  3. The `postProcessorAgent` runs, calling `grammar_check` then `tone_check`, reading `current_story` and writing `grammar_suggestions` and `tone_check_result` to the state.
  4. **Custom Part:** The code checks the `tone_check_result` from the state. If it's "negative", the `story_generator` is called _again_ , overwriting the `current_story` in the state. Otherwise, the flow ends.

The `runAsyncImpl` method orchestrates the sub-agents using RxJava's Flowable streams and operators for asynchronous control flow.
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-1>)@Override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-2>)protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-3>)  // Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-4>)  // Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-5>)  logger.log(Level.INFO, () -> String.format("[%s] Starting story generation workflow.", name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-6>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-7>)  // Stage 1. Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-8>)  Flowable<Event> storyGenFlow = runStage(storyGenerator, invocationContext, "StoryGenerator");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-10>)  // Stage 2: Critic-Reviser Loop (runs after story generation completes)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-11>)  Flowable<Event> criticReviserFlow = Flowable.defer(() -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-12>)    if (!isStoryGenerated(invocationContext)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-13>)      logger.log(Level.SEVERE,() ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-14>)          String.format("[%s] Failed to generate initial story. Aborting after StoryGenerator.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-15>)              name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-16>)      return Flowable.empty(); // Stop further processing if no story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-17>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-18>)      logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-19>)          String.format("[%s] Story state after generator: %s",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-20>)              name(), invocationContext.session().state().get("current_story")));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-21>)      return runStage(loopAgent, invocationContext, "CriticReviserLoop");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-22>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-24>)  // Stage 3: Post-Processing (runs after critic-reviser loop completes)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-25>)  Flowable<Event> postProcessingFlow = Flowable.defer(() -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-26>)    logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-27>)        String.format("[%s] Story state after loop: %s",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-28>)            name(), invocationContext.session().state().get("current_story")));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-29>)    return runStage(sequentialAgent, invocationContext, "PostProcessing");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-30>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-31>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-32>)  // Stage 4: Conditional Regeneration (runs after post-processing completes)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-33>)  Flowable<Event> conditionalRegenFlow = Flowable.defer(() -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-34>)    String toneCheckResult = (String) invocationContext.session().state().get("tone_check_result");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-35>)    logger.log(Level.INFO, () -> String.format("[%s] Tone check result: %s", name(), toneCheckResult));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-36>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-37>)    if ("negative".equalsIgnoreCase(toneCheckResult)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-38>)      logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-39>)          String.format("[%s] Tone is negative. Regenerating story...", name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-40>)      return runStage(storyGenerator, invocationContext, "StoryGenerator (Regen)");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-41>)    } else {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-42>)      logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-43>)          String.format("[%s] Tone is not negative. Keeping current story.", name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-44>)      return Flowable.empty(); // No regeneration needed
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-45>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-46>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-47>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-48>)  return Flowable.concatArray(storyGenFlow, criticReviserFlow, postProcessingFlow, conditionalRegenFlow)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-49>)      .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] Workflow finished.", name())));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-50>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-51>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-52>)// Helper method for a single agent run stage with logging
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-53>)private Flowable<Event> runStage(BaseAgent agentToRun, InvocationContext ctx, String stageName) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-54>)  logger.log(Level.INFO, () -> String.format("[%s] Running %s...", name(), stageName));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-55>)  return agentToRun
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-56>)      .runAsync(ctx)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-57>)      .doOnNext(event ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-58>)          logger.log(Level.INFO,() ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-59>)              String.format("[%s] Event from %s: %s", name(), stageName, event.toJson())))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-60>)      .doOnError(err ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-61>)          logger.log(Level.SEVERE,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-62>)              String.format("[%s] Error in %s", name(), stageName), err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-63>)      .doOnComplete(() ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-64>)          logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-65>)              String.format("[%s] %s finished.", name(), stageName)));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-50-66>)}
    
**Explanation of Logic:**

  1. The initial `storyGenerator.runAsync(invocationContext)` Flowable is executed. Its output is expected to be in `invocationContext.session().state().get("current_story")`.
  2. The `loopAgent's` Flowable runs next (due to `Flowable.concatArray` and `Flowable.defer`). The LoopAgent internally calls the `critic` and `reviser` sub-agents sequentially for up to `maxIterations`. They read/write `current_story` and `criticism` from/to the state.
  3. Then, the `sequentialAgent's` Flowable executes. It calls the `grammar_check` then `tone_check`, reading `current_story` and writing `grammar_suggestions` and `tone_check_result` to the state.
  4. **Custom Part:** After the sequentialAgent completes, logic within a `Flowable.defer` checks the "tone_check_result" from `invocationContext.session().state()`. If it's "negative", the `storyGenerator` Flowable is _conditionally concatenated_ and executed again, overwriting "current_story". Otherwise, an empty Flowable is used, and the overall workflow proceeds to completion.

* * *

### Part 3: Define LLM sub-agents[¶](<https://adk.dev/agents/custom-agents/#part-3-define-llm-sub-agents> "Permanent link")

These are standard `LlmAgent` definitions, responsible for specific tasks. Their `output key` parameter is crucial for placing results into the `session.state` where other agents or the custom orchestrator can access them.

Direct State Injection in Instructions

Notice the `story_generator`'s instruction. The `{var}` syntax is a placeholder. Before the instruction is sent to the LLM, the ADK framework automatically replaces (Example:`{topic}`) with the value of `session.state['topic']`. This is the recommended way to provide context to an agent, using templating in the instructions. For more details, see the [State documentation](<https://adk.dev/sessions/state/#accessing-session-state-in-agent-instructions>).

PythonTypeScriptGoJava
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-1>)GEMINI_2_FLASH = "gemini-flash-latest" # Define model constant
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-2>)# --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-3>)story_generator = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-4>)    name="StoryGenerator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-5>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-6>)    instruction="""You are a story writer. Write a short story (around 100 words), on the following topic: {topic}""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-7>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-8>)    output_key="current_story",  # Key for storing output in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-9>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-11>)critic = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-12>)    name="Critic",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-13>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-14>)    instruction="""You are a story critic. Review the story provided: {{current_story}}. Provide 1-2 sentences of constructive criticism
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-15>)on how to improve it. Focus on plot or character.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-16>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-17>)    output_key="criticism",  # Key for storing criticism in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-18>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-19>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-20>)reviser = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-21>)    name="Reviser",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-22>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-23>)    instruction="""You are a story reviser. Revise the story provided: {{current_story}}, based on the criticism in
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-24>){{criticism}}. Output only the revised story.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-25>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-26>)    output_key="current_story",  # Overwrites the original story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-27>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-28>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-29>)grammar_check = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-30>)    name="GrammarCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-31>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-32>)    instruction="""You are a grammar checker. Check the grammar of the story provided: {current_story}. Output only the suggested
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-33>)corrections as a list, or output 'Grammar is good!' if there are no errors.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-34>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-35>)    output_key="grammar_suggestions",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-36>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-37>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-38>)tone_check = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-39>)    name="ToneCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-40>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-41>)    instruction="""You are a tone analyzer. Analyze the tone of the story provided: {current_story}. Output only one word: 'positive' if
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-42>)the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-43>)otherwise.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-44>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-45>)    output_key="tone_check_result", # This agent's output determines the conditional flow
    [](<https://adk.dev/agents/custom-agents/#__codelineno-51-46>))
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-1>)// --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-2>)const storyGenerator = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-3>)    name: "StoryGenerator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-4>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-5>)    instruction: `You are a story writer. Write a short story (around 100 words), on the following topic: {topic}`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-6>)    outputKey: "current_story",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-7>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-8>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-9>)const critic = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-10>)    name: "Critic",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-11>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-12>)    instruction: `You are a story critic. Review the story provided: {{current_story}}. Provide 1-2 sentences of constructive criticism
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-13>)on how to improve it. Focus on plot or character.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-14>)    outputKey: "criticism",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-15>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-16>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-17>)const reviser = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-18>)    name: "Reviser",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-19>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-20>)    instruction: `You are a story reviser. Revise the story provided: {{current_story}}, based on the criticism in
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-21>){{criticism}}. Output only the revised story.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-22>)    outputKey: "current_story", // Overwrites the original story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-23>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-24>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-25>)const grammarCheck = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-26>)    name: "GrammarCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-27>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-28>)    instruction: `You are a grammar checker. Check the grammar of the story provided: {current_story}. Output only the suggested
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-29>)corrections as a list, or output 'Grammar is good!' if there are no errors.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-30>)    outputKey: "grammar_suggestions",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-31>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-32>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-33>)const toneCheck = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-34>)    name: "ToneCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-35>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-36>)    instruction: `You are a tone analyzer. Analyze the tone of the story provided: {current_story}. Output only one word: 'positive' if
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-37>)the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-38>)otherwise.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-39>)    outputKey: "tone_check_result",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-52-40>)});
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-1>)// --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-2>)storyGenerator, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-3>)    Name:        "StoryGenerator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-4>)    Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-5>)    Description: "Generates the initial story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-6>)    Instruction: "You are a story writer. Write a short story (around 100 words) about a cat, based on the topic: {topic}",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-7>)    OutputKey:   "current_story",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-8>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-9>)if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-10>)    log.Fatalf("Failed to create StoryGenerator agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-11>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-13>)critic, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-14>)    Name:        "Critic",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-15>)    Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-16>)    Description: "Critiques the story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-17>)    Instruction: "You are a story critic. Review the story: {current_story}. Provide 1-2 sentences of constructive criticism on how to improve it. Focus on plot or character.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-18>)    OutputKey:   "criticism",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-19>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-20>)if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-21>)    log.Fatalf("Failed to create Critic agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-22>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-24>)reviser, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-25>)    Name:        "Reviser",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-26>)    Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-27>)    Description: "Revises the story based on criticism.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-28>)    Instruction: "You are a story reviser. Revise the story: {current_story}, based on the criticism: {criticism}. Output only the revised story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-29>)    OutputKey:   "current_story",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-30>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-31>)if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-32>)    log.Fatalf("Failed to create Reviser agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-33>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-34>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-35>)grammarCheck, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-36>)    Name:        "GrammarCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-37>)    Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-38>)    Description: "Checks grammar and suggests corrections.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-39>)    Instruction: "You are a grammar checker. Check the grammar of the story: {current_story}. Output only the suggested corrections as a list, or output 'Grammar is good!' if there are no errors.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-40>)    OutputKey:   "grammar_suggestions",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-41>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-42>)if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-43>)    log.Fatalf("Failed to create GrammarCheck agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-44>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-45>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-46>)toneCheck, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-47>)    Name:        "ToneCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-48>)    Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-49>)    Description: "Analyzes the tone of the story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-50>)    Instruction: "You are a tone analyzer. Analyze the tone of the story: {current_story}. Output only one word: 'positive' if the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral' otherwise.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-51>)    OutputKey:   "tone_check_result",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-52>)})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-53>)if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-54>)    log.Fatalf("Failed to create ToneCheck agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-53-55>)}
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-1>)// --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-2>)LlmAgent storyGenerator =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-3>)    LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-4>)        .name("StoryGenerator")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-5>)        .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-6>)        .description("Generates the initial story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-7>)        .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-8>)            """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-9>)          You are a story writer. Write a short story (around 100 words) about a cat,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-10>)          based on the topic: {topic}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-11>)          """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-12>)        .inputSchema(null)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-13>)        .outputKey("current_story") // Key for storing output in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-14>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-15>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-16>)LlmAgent critic =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-17>)    LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-18>)        .name("Critic")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-19>)        .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-20>)        .description("Critiques the story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-21>)        .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-22>)            """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-23>)          You are a story critic. Review the story: {current_story}. Provide 1-2 sentences of constructive criticism
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-24>)          on how to improve it. Focus on plot or character.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-25>)          """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-26>)        .inputSchema(null)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-27>)        .outputKey("criticism") // Key for storing criticism in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-28>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-29>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-30>)LlmAgent reviser =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-31>)    LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-32>)        .name("Reviser")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-33>)        .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-34>)        .description("Revises the story based on criticism.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-35>)        .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-36>)            """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-37>)          You are a story reviser. Revise the story: {current_story}, based on the criticism: {criticism}. Output only the revised story.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-38>)          """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-39>)        .inputSchema(null)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-40>)        .outputKey("current_story") // Overwrites the original story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-41>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-42>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-43>)LlmAgent grammarCheck =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-44>)    LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-45>)        .name("GrammarCheck")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-46>)        .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-47>)        .description("Checks grammar and suggests corrections.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-48>)        .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-49>)            """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-50>)           You are a grammar checker. Check the grammar of the story: {current_story}. Output only the suggested
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-51>)           corrections as a list, or output 'Grammar is good!' if there are no errors.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-52>)           """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-53>)        .outputKey("grammar_suggestions")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-54>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-55>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-56>)LlmAgent toneCheck =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-57>)    LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-58>)        .name("ToneCheck")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-59>)        .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-60>)        .description("Analyzes the tone of the story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-61>)        .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-62>)            """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-63>)          You are a tone analyzer. Analyze the tone of the story: {current_story}. Output only one word: 'positive' if
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-64>)          the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-65>)          otherwise.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-66>)          """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-67>)        .outputKey("tone_check_result") // This agent's output determines the conditional flow
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-68>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-69>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-70>)LoopAgent loopAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-71>)    LoopAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-72>)        .name("CriticReviserLoop")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-73>)        .description("Iteratively critiques and revises the story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-74>)        .subAgents(critic, reviser)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-75>)        .maxIterations(2)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-76>)        .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-77>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-78>)SequentialAgent sequentialAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-79>)    SequentialAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-80>)        .name("PostProcessing")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-81>)        .description("Performs grammar and tone checks sequentially.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-82>)        .subAgents(grammarCheck, toneCheck)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-54-83>)        .build();
    
* * *

### Part 4: Instantiate and run the custom agent[¶](<https://adk.dev/agents/custom-agents/#part-4-instantiate-and-run-the-custom-agent> "Permanent link")

Finally, you instantiate your `StoryFlowAgent` and use the `Runner` as usual.

PythonTypeScriptGoJava
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-1>)# --- Create the custom agent instance ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-2>)story_flow_agent = StoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-3>)    name="StoryFlowAgent",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-4>)    story_generator=story_generator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-5>)    critic=critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-6>)    reviser=reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-7>)    grammar_check=grammar_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-8>)    tone_check=tone_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-9>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-11>)INITIAL_STATE = {"topic": "a brave kitten exploring a haunted house"}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-13>)# --- Setup Runner and Session ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-14>)async def setup_session_and_runner():
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-15>)    session_service = InMemorySessionService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-16>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID, state=INITIAL_STATE)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-17>)    logger.info(f"Initial session state: {session.state}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-18>)    runner = Runner(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-19>)        agent=story_flow_agent, # Pass the custom orchestrator agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-20>)        app_name=APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-21>)        session_service=session_service
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-22>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-23>)    return session_service, runner
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-24>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-25>)# --- Function to Interact with the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-26>)async def call_agent_async(user_input_topic: str):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-27>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-28>)    Sends a new topic to the agent (overwriting the initial one if needed)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-29>)    and runs the workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-30>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-31>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-32>)    session_service, runner = await setup_session_and_runner()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-33>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-34>)    current_session = session_service.sessions[APP_NAME][USER_ID][SESSION_ID]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-35>)    current_session.state["topic"] = user_input_topic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-36>)    logger.info(f"Updated session state topic to: {user_input_topic}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-37>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-38>)    content = types.Content(role='user', parts=[types.Part(text=f"Generate a story about the preset topic.")])
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-39>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-40>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-41>)    final_response = "No final response captured."
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-42>)    async for event in events:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-43>)        if event.is_final_response() and event.content and event.content.parts:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-44>)            logger.info(f"Potential final response from [{event.author}]: {event.content.parts[0].text}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-45>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-46>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-47>)    print("\n--- Agent Interaction Result ---")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-48>)    print("Agent Final Response: ", final_response)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-49>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-50>)    final_session = await session_service.get_session(app_name=APP_NAME, 
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-51>)                                                user_id=USER_ID, 
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-52>)                                                session_id=SESSION_ID)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-53>)    print("Final Session State:")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-54>)    import json
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-55>)    print(json.dumps(final_session.state, indent=2))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-56>)    print("-------------------------------\n")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-57>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-58>)# --- Run the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-59>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-60>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-55-61>)await call_agent_async("a lonely robot finding a friend in a junkyard")
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-1>)// --- Create the custom agent instance ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-2>)const storyFlowAgent = new StoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-3>)    "StoryFlowAgent",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-4>)    storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-5>)    critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-6>)    reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-7>)    grammarCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-8>)    toneCheck
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-9>));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-11>)const INITIAL_STATE = { "topic": "a brave kitten exploring a haunted house" };
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-13>)// --- Setup Runner and Session ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-14>)async function setupRunnerAndSession() {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-15>)  const runner = new InMemoryRunner({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-16>)    agent: storyFlowAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-17>)    appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-18>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-19>)  const session = await runner.sessionService.createSession({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-20>)    appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-21>)    userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-22>)    sessionId: SESSION_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-23>)    state: INITIAL_STATE,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-24>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-25>)  console.log(`Initial session state: ${JSON.stringify(session.state, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-26>)  return runner;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-27>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-28>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-29>)// --- Function to Interact with the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-30>)async function callAgent(runner: InMemoryRunner, userInputTopic: string) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-31>)  const currentSession = await runner.sessionService.getSession({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-32>)      appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-33>)      userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-34>)      sessionId: SESSION_ID
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-35>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-36>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-37>)  if (!currentSession) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-38>)      return;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-39>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-40>)  // Update the state with the new topic for this run
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-41>)  currentSession.state["topic"] = userInputTopic;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-42>)  console.log(`Updated session state topic to: ${userInputTopic}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-43>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-44>)  let finalResponse = "No final response captured.";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-45>)  for await (const event of runner.runAsync({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-46>)    userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-47>)    sessionId: SESSION_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-48>)    newMessage: createUserContent(`Generate a story about: ${userInputTopic}`)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-49>)  })) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-50>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-51>)      console.log(`Potential final response from [${event.author}]: ${event.content.parts.map(part => part.text ?? '').join('')}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-52>)      finalResponse = event.content.parts.map(part => part.text ?? '').join('');
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-53>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-54>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-55>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-56>)  const finalSession = await runner.sessionService.getSession({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-57>)    appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-58>)    userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-59>)    sessionId: SESSION_ID
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-60>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-61>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-62>)  console.log("\n--- Agent Interaction Result ---");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-63>)  console.log("Agent Final Response: ", finalResponse);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-64>)  console.log("Final Session State:");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-65>)  console.log(JSON.stringify(finalSession?.state, null, 2));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-66>)  console.log("-------------------------------\n");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-67>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-68>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-69>)// --- Run the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-70>)async function main() {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-71>)  const runner = await setupRunnerAndSession();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-72>)  await callAgent(runner, "a lonely robot finding a friend in a junkyard");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-73>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-74>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-56-75>)main();
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-1>)    // Instantiate the custom agent, which encapsulates the workflow agents.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-2>)    storyFlowAgent, err := NewStoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-3>)        storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-4>)        critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-5>)        reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-6>)        grammarCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-7>)        toneCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-8>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-9>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-10>)        log.Fatalf("Failed to create story flow agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-11>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-13>)    // --- Run the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-14>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-15>)    initialState := map[string]any{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-16>)        "topic": "a brave kitten exploring a haunted house",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-17>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-18>)    sessionInstance, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-19>)        AppName: appName,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-20>)        UserID:  userID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-21>)        State:   initialState,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-22>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-23>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-24>)        log.Fatalf("Failed to create session: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-25>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-26>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-27>)    userTopic := "a lonely robot finding a friend in a junkyard"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-28>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-29>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-30>)        AppName:        appName,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-31>)        Agent:          storyFlowAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-32>)        SessionService: sessionService,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-33>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-34>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-35>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-36>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-37>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-38>)    input := genai.NewContentFromText("Generate a story about: "+userTopic, genai.RoleUser)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-39>)    events := r.Run(ctx, userID, sessionInstance.Session.ID(), input, agent.RunConfig{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-40>)        StreamingMode: agent.StreamingModeSSE,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-41>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-42>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-43>)    var finalResponse string
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-44>)    for event, err := range events {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-45>)        if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-46>)            log.Fatalf("An error occurred during agent execution: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-47>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-48>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-49>)        for _, part := range event.Content.Parts {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-50>)            // Accumulate text from all parts of the final response.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-51>)            finalResponse += part.Text
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-52>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-53>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-54>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-55>)    fmt.Println("\n--- Agent Interaction Result ---")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-56>)    fmt.Println("Agent Final Response: " + finalResponse)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-57>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-58>)    finalSession, err := sessionService.Get(ctx, &session.GetRequest{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-59>)        UserID:    userID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-60>)        AppName:   appName,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-61>)        SessionID: sessionInstance.Session.ID(),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-62>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-63>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-64>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-65>)        log.Fatalf("Failed to retrieve final session: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-66>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-67>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-68>)    fmt.Println("Final Session State:", finalSession.Session.State())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-57-69>)}
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-1>)// --- Function to Interact with the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-2>)// Sends a new topic to the agent (overwriting the initial one if needed)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-3>)// and runs the workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-4>)public static void runAgent(StoryFlowAgentExample agent, String userTopic) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-5>)  // --- Setup Runner and Session ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-6>)  InMemoryRunner runner = new InMemoryRunner(agent);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-7>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-8>)  Map<String, Object> initialState = new HashMap<>();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-9>)  initialState.put("topic", "a brave kitten exploring a haunted house");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-10>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-11>)  Session session =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-12>)      runner
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-13>)          .sessionService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-14>)          .createSession(APP_NAME, USER_ID, new ConcurrentHashMap<>(initialState), SESSION_ID)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-15>)          .blockingGet();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-16>)  logger.log(Level.INFO, () -> String.format("Initial session state: %s", session.state()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-17>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-18>)  session.state().put("topic", userTopic); // Update the state in the retrieved session
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-19>)  logger.log(Level.INFO, () -> String.format("Updated session state topic to: %s", userTopic));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-20>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-21>)  Content userMessage = Content.fromParts(Part.fromText("Generate a story about: " + userTopic));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-22>)  // Use the modified session object for the run
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-23>)  Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-24>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-25>)  final String[] finalResponse = {"No final response captured."};
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-26>)  eventStream.blockingForEach(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-27>)      event -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-28>)        if (event.finalResponse() && event.content().isPresent()) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-29>)          String author = event.author() != null ? event.author() : "UNKNOWN_AUTHOR";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-30>)          Optional<String> textOpt =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-31>)              event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-32>)                  .content()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-33>)                  .flatMap(Content::parts)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-34>)                  .filter(parts -> !parts.isEmpty())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-35>)                  .map(parts -> parts.get(0).text().orElse(""));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-36>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-37>)          logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-38>)              String.format("Potential final response from [%s]: %s", author, textOpt.orElse("N/A")));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-39>)          textOpt.ifPresent(text -> finalResponse[0] = text);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-40>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-41>)      });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-42>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-43>)  System.out.println("\n--- Agent Interaction Result ---");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-44>)  System.out.println("Agent Final Response: " + finalResponse[0]);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-45>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-46>)  // Retrieve session again to see the final state after the run
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-47>)  Session finalSession =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-48>)      runner
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-49>)          .sessionService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-50>)          .getSession(APP_NAME, USER_ID, SESSION_ID, Optional.empty())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-51>)          .blockingGet();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-52>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-53>)  assert finalSession != null;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-54>)  System.out.println("Final Session State:" + finalSession.state());
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-55>)  System.out.println("-------------------------------\n");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-58-56>)}
    
_(Note: The full runnable code, including imports and execution logic, can be found linked below.)_

* * *

### Storyflow Agent code listing[¶](<https://adk.dev/agents/custom-agents/#storyflow-agent-code-listing> "Permanent link")

Storyflow Agent

PythonTypeScriptGoJava
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-1>)# Full runnable code for the StoryFlowAgent example
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-2>)# Copyright 2025 Google LLC
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-3>)#
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-4>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-5>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-6>)# You may obtain a copy of the License at
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-7>)#
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-8>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-9>)#
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-10>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-11>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-12>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-13>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-14>)# limitations under the License.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-15>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-16>)import logging
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-17>)from typing import AsyncGenerator
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-18>)from typing_extensions import override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-19>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-20>)from google.adk.agents import LlmAgent, BaseAgent, LoopAgent, SequentialAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-21>)from google.adk.agents.invocation_context import InvocationContext
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-22>)from google.genai import types
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-23>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-24>)from google.adk.runners import Runner
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-25>)from google.adk.events import Event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-26>)from pydantic import BaseModel, Field
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-27>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-28>)# --- Constants ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-29>)APP_NAME = "story_app"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-30>)USER_ID = "12345"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-31>)SESSION_ID = "123344"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-32>)GEMINI_2_FLASH = "gemini-2.0-flash"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-33>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-34>)# --- Configure Logging ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-35>)logging.basicConfig(level=logging.INFO)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-36>)logger = logging.getLogger(__name__)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-37>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-38>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-39>)# --- Custom Orchestrator Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-40>)class StoryFlowAgent(BaseAgent):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-41>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-42>)    Custom agent for a story generation and refinement workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-43>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-44>)    This agent orchestrates a sequence of LLM agents to generate a story,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-45>)    critique it, revise it, check grammar and tone, and potentially
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-46>)    regenerate the story if the tone is negative.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-47>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-48>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-49>)    # --- Field Declarations for Pydantic ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-50>)    # Declare the agents passed during initialization as class attributes with type hints
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-51>)    story_generator: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-52>)    critic: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-53>)    reviser: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-54>)    grammar_check: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-55>)    tone_check: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-56>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-57>)    loop_agent: LoopAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-58>)    sequential_agent: SequentialAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-59>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-60>)    # model_config allows setting Pydantic configurations if needed, e.g., arbitrary_types_allowed
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-61>)    model_config = {"arbitrary_types_allowed": True}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-62>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-63>)    def __init__(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-64>)        self,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-65>)        name: str,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-66>)        story_generator: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-67>)        critic: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-68>)        reviser: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-69>)        grammar_check: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-70>)        tone_check: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-71>)    ):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-72>)        """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-73>)        Initializes the StoryFlowAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-74>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-75>)        Args:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-76>)            name: The name of the agent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-77>)            story_generator: An LlmAgent to generate the initial story.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-78>)            critic: An LlmAgent to critique the story.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-79>)            reviser: An LlmAgent to revise the story based on criticism.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-80>)            grammar_check: An LlmAgent to check the grammar.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-81>)            tone_check: An LlmAgent to analyze the tone.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-82>)        """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-83>)        # Create internal agents *before* calling super().__init__
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-84>)        loop_agent = LoopAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-85>)            name="CriticReviserLoop", sub_agents=[critic, reviser], max_iterations=2
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-86>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-87>)        sequential_agent = SequentialAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-88>)            name="PostProcessing", sub_agents=[grammar_check, tone_check]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-89>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-90>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-91>)        # Define the sub_agents list for the framework
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-92>)        sub_agents_list = [
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-93>)            story_generator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-94>)            loop_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-95>)            sequential_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-96>)        ]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-97>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-98>)        # Pydantic will validate and assign them based on the class annotations.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-99>)        super().__init__(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-100>)            name=name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-101>)            story_generator=story_generator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-102>)            critic=critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-103>)            reviser=reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-104>)            grammar_check=grammar_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-105>)            tone_check=tone_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-106>)            loop_agent=loop_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-107>)            sequential_agent=sequential_agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-108>)            sub_agents=sub_agents_list, # Pass the sub_agents list directly
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-109>)        )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-110>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-111>)    @override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-112>)    async def _run_async_impl(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-113>)        self, ctx: InvocationContext
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-114>)    ) -> AsyncGenerator[Event, None]:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-115>)        """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-116>)        Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-117>)        Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-118>)        """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-119>)        logger.info(f"[{self.name}] Starting story generation workflow.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-120>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-121>)        # 1. Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-122>)        logger.info(f"[{self.name}] Running StoryGenerator...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-123>)        async for event in self.story_generator.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-124>)            logger.info(f"[{self.name}] Event from StoryGenerator: {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-125>)            yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-126>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-127>)        # Check if story was generated before proceeding
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-128>)        if "current_story" not in ctx.session.state or not ctx.session.state["current_story"]:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-129>)             logger.error(f"[{self.name}] Failed to generate initial story. Aborting workflow.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-130>)             return # Stop processing if initial story failed
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-131>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-132>)        logger.info(f"[{self.name}] Story state after generator: {ctx.session.state.get('current_story')}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-133>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-134>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-135>)        # 2. Critic-Reviser Loop
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-136>)        logger.info(f"[{self.name}] Running CriticReviserLoop...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-137>)        # Use the loop_agent instance attribute assigned during init
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-138>)        async for event in self.loop_agent.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-139>)            logger.info(f"[{self.name}] Event from CriticReviserLoop: {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-140>)            yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-141>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-142>)        logger.info(f"[{self.name}] Story state after loop: {ctx.session.state.get('current_story')}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-143>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-144>)        # 3. Sequential Post-Processing (Grammar and Tone Check)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-145>)        logger.info(f"[{self.name}] Running PostProcessing...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-146>)        # Use the sequential_agent instance attribute assigned during init
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-147>)        async for event in self.sequential_agent.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-148>)            logger.info(f"[{self.name}] Event from PostProcessing: {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-149>)            yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-150>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-151>)        # 4. Tone-Based Conditional Logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-152>)        tone_check_result = ctx.session.state.get("tone_check_result")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-153>)        logger.info(f"[{self.name}] Tone check result: {tone_check_result}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-154>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-155>)        if tone_check_result == "negative":
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-156>)            logger.info(f"[{self.name}] Tone is negative. Regenerating story...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-157>)            async for event in self.story_generator.run_async(ctx):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-158>)                logger.info(f"[{self.name}] Event from StoryGenerator (Regen): {event.model_dump_json(indent=2, exclude_none=True)}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-159>)                yield event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-160>)        else:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-161>)            logger.info(f"[{self.name}] Tone is not negative. Keeping current story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-162>)            pass
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-163>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-164>)        logger.info(f"[{self.name}] Workflow finished.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-165>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-166>)# --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-167>)story_generator = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-168>)    name="StoryGenerator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-169>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-170>)    instruction="""You are a story writer. Write a short story (around 100 words), on the following topic: {topic}""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-171>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-172>)    output_key="current_story",  # Key for storing output in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-173>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-174>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-175>)critic = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-176>)    name="Critic",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-177>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-178>)    instruction="""You are a story critic. Review the story provided: {{current_story}}. Provide 1-2 sentences of constructive criticism
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-179>)on how to improve it. Focus on plot or character.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-180>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-181>)    output_key="criticism",  # Key for storing criticism in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-182>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-183>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-184>)reviser = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-185>)    name="Reviser",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-186>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-187>)    instruction="""You are a story reviser. Revise the story provided: {{current_story}}, based on the criticism in
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-188>){{criticism}}. Output only the revised story.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-189>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-190>)    output_key="current_story",  # Overwrites the original story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-191>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-192>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-193>)grammar_check = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-194>)    name="GrammarCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-195>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-196>)    instruction="""You are a grammar checker. Check the grammar of the story provided: {current_story}. Output only the suggested
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-197>)corrections as a list, or output 'Grammar is good!' if there are no errors.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-198>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-199>)    output_key="grammar_suggestions",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-200>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-201>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-202>)tone_check = LlmAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-203>)    name="ToneCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-204>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-205>)    instruction="""You are a tone analyzer. Analyze the tone of the story provided: {current_story}. Output only one word: 'positive' if
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-206>)the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-207>)otherwise.""",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-208>)    input_schema=None,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-209>)    output_key="tone_check_result", # This agent's output determines the conditional flow
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-210>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-211>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-212>)# --- Create the custom agent instance ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-213>)story_flow_agent = StoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-214>)    name="StoryFlowAgent",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-215>)    story_generator=story_generator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-216>)    critic=critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-217>)    reviser=reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-218>)    grammar_check=grammar_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-219>)    tone_check=tone_check,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-220>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-221>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-222>)INITIAL_STATE = {"topic": "a brave kitten exploring a haunted house"}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-223>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-224>)# --- Setup Runner and Session ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-225>)async def setup_session_and_runner():
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-226>)    session_service = InMemorySessionService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-227>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID, state=INITIAL_STATE)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-228>)    logger.info(f"Initial session state: {session.state}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-229>)    runner = Runner(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-230>)        agent=story_flow_agent, # Pass the custom orchestrator agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-231>)        app_name=APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-232>)        session_service=session_service
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-233>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-234>)    return session_service, runner
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-235>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-236>)# --- Function to Interact with the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-237>)async def call_agent_async(user_input_topic: str):
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-238>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-239>)    Sends a new topic to the agent (overwriting the initial one if needed)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-240>)    and runs the workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-241>)    """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-242>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-243>)    session_service, runner = await setup_session_and_runner()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-244>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-245>)    current_session = session_service.sessions[APP_NAME][USER_ID][SESSION_ID]
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-246>)    current_session.state["topic"] = user_input_topic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-247>)    logger.info(f"Updated session state topic to: {user_input_topic}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-248>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-249>)    content = types.Content(role='user', parts=[types.Part(text=f"Generate a story about the preset topic.")])
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-250>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-251>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-252>)    final_response = "No final response captured."
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-253>)    async for event in events:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-254>)        if event.is_final_response() and event.content and event.content.parts:
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-255>)            logger.info(f"Potential final response from [{event.author}]: {event.content.parts[0].text}")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-256>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-257>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-258>)    print("\n--- Agent Interaction Result ---")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-259>)    print("Agent Final Response: ", final_response)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-260>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-261>)    final_session = await session_service.get_session(app_name=APP_NAME, 
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-262>)                                                user_id=USER_ID, 
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-263>)                                                session_id=SESSION_ID)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-264>)    print("Final Session State:")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-265>)    import json
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-266>)    print(json.dumps(final_session.state, indent=2))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-267>)    print("-------------------------------\n")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-268>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-269>)# --- Run the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-270>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-271>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-59-272>)await call_agent_async("a lonely robot finding a friend in a junkyard")
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-1>)// Full runnable code for the StoryFlowAgent example
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-2>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-3>)/**
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-4>) * Copyright 2025 Google LLC
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-5>) *
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-6>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-7>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-8>) * You may obtain a copy of the License at
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-9>) *
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-10>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-11>) *
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-12>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-13>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-14>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-15>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-16>) * limitations under the License.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-17>) */
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-18>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-19>)import { LlmAgent, BaseAgent, LoopAgent, SequentialAgent, InMemoryRunner, InvocationContext, Event, isFinalResponse } from '@google/adk';
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-20>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-21>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-22>)// --- Constants ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-23>)const APP_NAME = "story_app_ts";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-24>)const USER_ID = "12345";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-25>)const SESSION_ID = "123344_ts";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-26>)const GEMINI_MODEL = "gemini-2.5-flash";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-27>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-28>)// --- Custom Orchestrator Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-29>)class StoryFlowAgent extends BaseAgent {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-30>)  // --- Property Declarations for TypeScript ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-31>)  private storyGenerator: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-32>)  private critic: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-33>)  private reviser: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-34>)  private grammarCheck: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-35>)  private toneCheck: LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-36>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-37>)  private loopAgent: LoopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-38>)  private sequentialAgent: SequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-39>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-40>)  constructor(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-41>)    name: string,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-42>)    storyGenerator: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-43>)    critic: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-44>)    reviser: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-45>)    grammarCheck: LlmAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-46>)    toneCheck: LlmAgent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-47>)  ) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-48>)    // Create internal composite agents
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-49>)    const loopAgent = new LoopAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-50>)      name: "CriticReviserLoop",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-51>)      subAgents: [critic, reviser],
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-52>)      maxIterations: 2,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-53>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-54>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-55>)    const sequentialAgent = new SequentialAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-56>)      name: "PostProcessing",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-57>)      subAgents: [grammarCheck, toneCheck],
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-58>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-59>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-60>)    // Define the sub-agents for the framework to know about
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-61>)    const subAgentsList = [
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-62>)      storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-63>)      loopAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-64>)      sequentialAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-65>)    ];
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-66>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-67>)    // Call the parent constructor
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-68>)    super({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-69>)      name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-70>)      subAgents: subAgentsList,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-71>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-72>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-73>)    // Assign agents to class properties for use in the custom run logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-74>)    this.storyGenerator = storyGenerator;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-75>)    this.critic = critic;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-76>)    this.reviser = reviser;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-77>)    this.grammarCheck = grammarCheck;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-78>)    this.toneCheck = toneCheck;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-79>)    this.loopAgent = loopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-80>)    this.sequentialAgent = sequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-81>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-82>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-83>)  // Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-84>)  async* runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-85>)    yield* this.runAsyncImpl(ctx);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-86>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-87>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-88>)  // Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-89>)  async* runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event, void, undefined> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-90>)    console.log(`[${this.name}] Starting story generation workflow.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-91>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-92>)    // 1. Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-93>)    console.log(`[${this.name}] Running StoryGenerator...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-94>)    for await (const event of this.storyGenerator.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-95>)      console.log(`[${this.name}] Event from StoryGenerator: ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-96>)      yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-97>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-98>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-99>)    // Check if the story was generated before proceeding
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-100>)    if (!ctx.session.state["current_story"]) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-101>)      console.error(`[${this.name}] Failed to generate initial story. Aborting workflow.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-102>)      return; // Stop processing
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-103>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-104>)    console.log(`[${this.name}] Story state after generator: ${ctx.session.state['current_story']}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-105>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-106>)    // 2. Critic-Reviser Loop
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-107>)    console.log(`[${this.name}] Running CriticReviserLoop...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-108>)    for await (const event of this.loopAgent.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-109>)      console.log(`[${this.name}] Event from CriticReviserLoop: ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-110>)      yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-111>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-112>)    console.log(`[${this.name}] Story state after loop: ${ctx.session.state['current_story']}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-113>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-114>)    // 3. Sequential Post-Processing (Grammar and Tone Check)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-115>)    console.log(`[${this.name}] Running PostProcessing...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-116>)    for await (const event of this.sequentialAgent.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-117>)      console.log(`[${this.name}] Event from PostProcessing: ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-118>)      yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-119>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-120>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-121>)    // 4. Tone-Based Conditional Logic
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-122>)    const toneCheckResult = ctx.session.state["tone_check_result"] as string;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-123>)    console.log(`[${this.name}] Tone check result: ${toneCheckResult}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-124>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-125>)    if (toneCheckResult === "negative") {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-126>)      console.log(`[${this.name}] Tone is negative. Regenerating story...`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-127>)      for await (const event of this.storyGenerator.runAsync(ctx)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-128>)        console.log(`[${this.name}] Event from StoryGenerator (Regen): ${JSON.stringify(event, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-129>)        yield event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-130>)      }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-131>)    } else {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-132>)      console.log(`[${this.name}] Tone is not negative. Keeping current story.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-133>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-134>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-135>)    console.log(`[${this.name}] Workflow finished.`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-136>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-137>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-138>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-139>)// --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-140>)const storyGenerator = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-141>)    name: "StoryGenerator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-142>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-143>)    instruction: `You are a story writer. Write a short story (around 100 words), on the following topic: {topic}`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-144>)    outputKey: "current_story",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-145>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-146>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-147>)const critic = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-148>)    name: "Critic",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-149>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-150>)    instruction: `You are a story critic. Review the story provided: {{current_story}}. Provide 1-2 sentences of constructive criticism
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-151>)on how to improve it. Focus on plot or character.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-152>)    outputKey: "criticism",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-153>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-154>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-155>)const reviser = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-156>)    name: "Reviser",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-157>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-158>)    instruction: `You are a story reviser. Revise the story provided: {{current_story}}, based on the criticism in
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-159>){{criticism}}. Output only the revised story.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-160>)    outputKey: "current_story", // Overwrites the original story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-161>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-162>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-163>)const grammarCheck = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-164>)    name: "GrammarCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-165>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-166>)    instruction: `You are a grammar checker. Check the grammar of the story provided: {current_story}. Output only the suggested
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-167>)corrections as a list, or output 'Grammar is good!' if there are no errors.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-168>)    outputKey: "grammar_suggestions",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-169>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-170>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-171>)const toneCheck = new LlmAgent({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-172>)    name: "ToneCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-173>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-174>)    instruction: `You are a tone analyzer. Analyze the tone of the story provided: {current_story}. Output only one word: 'positive' if
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-175>)the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-176>)otherwise.`,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-177>)    outputKey: "tone_check_result",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-178>)});
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-179>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-180>)// --- Create the custom agent instance ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-181>)const storyFlowAgent = new StoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-182>)    "StoryFlowAgent",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-183>)    storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-184>)    critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-185>)    reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-186>)    grammarCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-187>)    toneCheck
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-188>));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-189>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-190>)const INITIAL_STATE = { "topic": "a brave kitten exploring a haunted house" };
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-191>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-192>)// --- Setup Runner and Session ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-193>)async function setupRunnerAndSession() {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-194>)  const runner = new InMemoryRunner({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-195>)    agent: storyFlowAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-196>)    appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-197>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-198>)  const session = await runner.sessionService.createSession({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-199>)    appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-200>)    userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-201>)    sessionId: SESSION_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-202>)    state: INITIAL_STATE,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-203>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-204>)  console.log(`Initial session state: ${JSON.stringify(session.state, null, 2)}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-205>)  return runner;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-206>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-207>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-208>)// --- Function to Interact with the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-209>)async function callAgent(runner: InMemoryRunner, userInputTopic: string) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-210>)  const currentSession = await runner.sessionService.getSession({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-211>)      appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-212>)      userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-213>)      sessionId: SESSION_ID
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-214>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-215>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-216>)  if (!currentSession) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-217>)      return;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-218>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-219>)  // Update the state with the new topic for this run
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-220>)  currentSession.state["topic"] = userInputTopic;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-221>)  console.log(`Updated session state topic to: ${userInputTopic}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-222>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-223>)  let finalResponse = "No final response captured.";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-224>)  for await (const event of runner.runAsync({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-225>)    userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-226>)    sessionId: SESSION_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-227>)    newMessage: createUserContent(`Generate a story about: ${userInputTopic}`)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-228>)  })) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-229>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-230>)      console.log(`Potential final response from [${event.author}]: ${event.content.parts.map(part => part.text ?? '').join('')}`);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-231>)      finalResponse = event.content.parts.map(part => part.text ?? '').join('');
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-232>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-233>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-234>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-235>)  const finalSession = await runner.sessionService.getSession({
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-236>)    appName: APP_NAME,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-237>)    userId: USER_ID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-238>)    sessionId: SESSION_ID
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-239>)  });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-240>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-241>)  console.log("\n--- Agent Interaction Result ---");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-242>)  console.log("Agent Final Response: ", finalResponse);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-243>)  console.log("Final Session State:");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-244>)  console.log(JSON.stringify(finalSession?.state, null, 2));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-245>)  console.log("-------------------------------\n");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-246>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-247>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-248>)// --- Run the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-249>)async function main() {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-250>)  const runner = await setupRunnerAndSession();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-251>)  await callAgent(runner, "a lonely robot finding a friend in a junkyard");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-252>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-253>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-60-254>)main();
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-1>)# Full runnable code for the StoryFlowAgent example
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-2>)package main
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-3>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-4>)import (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-5>)    "context"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-6>)    "fmt"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-7>)    "iter"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-8>)    "log"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-9>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-10>)    "google.golang.org/adk/v2/agent/workflowagents/loopagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-11>)    "google.golang.org/adk/v2/agent/workflowagents/sequentialagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-12>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-13>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-14>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-15>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-16>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-17>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-18>)    "google.golang.org/genai"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-19>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-20>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-21>)// StoryFlowAgent is a custom agent that orchestrates a story generation workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-22>)// It encapsulates the logic of running sub-agents in a specific sequence.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-23>)type StoryFlowAgent struct {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-24>)    storyGenerator     agent.Agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-25>)    revisionLoopAgent  agent.Agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-26>)    postProcessorAgent agent.Agent
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-27>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-28>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-29>)// NewStoryFlowAgent creates and configures the entire custom agent workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-30>)// It takes individual LLM agents as input and internally creates the necessary
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-31>)// workflow agents (loop, sequential), returning the final orchestrator agent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-32>)func NewStoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-33>)    storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-34>)    critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-35>)    reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-36>)    grammarCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-37>)    toneCheck agent.Agent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-38>)) (agent.Agent, error) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-39>)    loopAgent, err := loopagent.New(loopagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-40>)        MaxIterations: 2,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-41>)        AgentConfig: agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-42>)            Name:      "CriticReviserLoop",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-43>)            SubAgents: []agent.Agent{critic, reviser},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-44>)        },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-45>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-46>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-47>)        return nil, fmt.Errorf("failed to create loop agent: %w", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-48>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-49>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-50>)    sequentialAgent, err := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-51>)        AgentConfig: agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-52>)            Name:      "PostProcessing",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-53>)            SubAgents: []agent.Agent{grammarCheck, toneCheck},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-54>)        },
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-55>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-56>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-57>)        return nil, fmt.Errorf("failed to create sequential agent: %w", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-58>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-59>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-60>)    // The StoryFlowAgent struct holds the agents needed for the Run method.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-61>)    orchestrator := &StoryFlowAgent{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-62>)        storyGenerator:     storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-63>)        revisionLoopAgent:  loopAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-64>)        postProcessorAgent: sequentialAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-65>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-66>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-67>)    // agent.New creates the final agent, wiring up the Run method.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-68>)    return agent.New(agent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-69>)        Name:        "StoryFlowAgent",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-70>)        Description: "Orchestrates story generation, critique, revision, and checks.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-71>)        SubAgents:   []agent.Agent{storyGenerator, loopAgent, sequentialAgent},
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-72>)        Run:         orchestrator.Run,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-73>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-74>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-75>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-76>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-77>)// Run defines the custom execution logic for the StoryFlowAgent.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-78>)func (s *StoryFlowAgent) Run(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-79>)    return func(yield func(*session.Event, error) bool) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-80>)        // Stage 1: Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-81>)        for event, err := range s.storyGenerator.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-82>)            if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-83>)                yield(nil, fmt.Errorf("story generator failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-84>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-85>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-86>)            if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-87>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-88>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-89>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-90>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-91>)        // Check if story was generated before proceeding
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-92>)        currentStory, err := ctx.Session().State().Get("current_story")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-93>)        if err != nil || currentStory == "" {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-94>)            log.Println("Failed to generate initial story. Aborting workflow.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-95>)            return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-96>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-97>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-98>)        // Stage 2: Critic-Reviser Loop
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-99>)        for event, err := range s.revisionLoopAgent.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-100>)            if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-101>)                yield(nil, fmt.Errorf("loop agent failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-102>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-103>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-104>)            if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-105>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-106>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-107>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-108>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-109>)        // Stage 3: Post-Processing
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-110>)        for event, err := range s.postProcessorAgent.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-111>)            if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-112>)                yield(nil, fmt.Errorf("sequential agent failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-113>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-114>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-115>)            if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-116>)                return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-117>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-118>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-119>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-120>)        // Stage 4: Conditional Regeneration
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-121>)        toneResult, err := ctx.Session().State().Get("tone_check_result")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-122>)        if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-123>)            log.Printf("Could not read tone_check_result from state: %v. Assuming tone is not negative.", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-124>)            return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-125>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-126>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-127>)        if tone, ok := toneResult.(string); ok && tone == "negative" {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-128>)            log.Println("Tone is negative. Regenerating story...")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-129>)            for event, err := range s.storyGenerator.Run(ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-130>)                if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-131>)                    yield(nil, fmt.Errorf("story regeneration failed: %w", err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-132>)                    return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-133>)                }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-134>)                if !yield(event, nil) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-135>)                    return
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-136>)                }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-137>)            }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-138>)        } else {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-139>)            log.Println("Tone is not negative. Keeping current story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-140>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-141>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-142>)}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-143>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-144>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-145>)const (
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-146>)    modelName = "gemini-flash-latest"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-147>)    appName   = "story_app"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-148>)    userID    = "user_12345"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-149>))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-150>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-151>)func main() {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-152>)    ctx := context.Background()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-153>)    model, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-154>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-155>)        log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-156>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-157>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-158>)    // --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-159>)    storyGenerator, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-160>)        Name:        "StoryGenerator",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-161>)        Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-162>)        Description: "Generates the initial story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-163>)        Instruction: "You are a story writer. Write a short story (around 100 words) about a cat, based on the topic: {topic}",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-164>)        OutputKey:   "current_story",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-165>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-166>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-167>)        log.Fatalf("Failed to create StoryGenerator agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-168>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-169>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-170>)    critic, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-171>)        Name:        "Critic",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-172>)        Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-173>)        Description: "Critiques the story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-174>)        Instruction: "You are a story critic. Review the story: {current_story}. Provide 1-2 sentences of constructive criticism on how to improve it. Focus on plot or character.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-175>)        OutputKey:   "criticism",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-176>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-177>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-178>)        log.Fatalf("Failed to create Critic agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-179>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-180>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-181>)    reviser, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-182>)        Name:        "Reviser",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-183>)        Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-184>)        Description: "Revises the story based on criticism.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-185>)        Instruction: "You are a story reviser. Revise the story: {current_story}, based on the criticism: {criticism}. Output only the revised story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-186>)        OutputKey:   "current_story",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-187>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-188>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-189>)        log.Fatalf("Failed to create Reviser agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-190>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-191>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-192>)    grammarCheck, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-193>)        Name:        "GrammarCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-194>)        Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-195>)        Description: "Checks grammar and suggests corrections.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-196>)        Instruction: "You are a grammar checker. Check the grammar of the story: {current_story}. Output only the suggested corrections as a list, or output 'Grammar is good!' if there are no errors.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-197>)        OutputKey:   "grammar_suggestions",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-198>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-199>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-200>)        log.Fatalf("Failed to create GrammarCheck agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-201>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-202>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-203>)    toneCheck, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-204>)        Name:        "ToneCheck",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-205>)        Model:       model,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-206>)        Description: "Analyzes the tone of the story.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-207>)        Instruction: "You are a tone analyzer. Analyze the tone of the story: {current_story}. Output only one word: 'positive' if the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral' otherwise.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-208>)        OutputKey:   "tone_check_result",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-209>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-210>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-211>)        log.Fatalf("Failed to create ToneCheck agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-212>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-213>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-214>)    // Instantiate the custom agent, which encapsulates the workflow agents.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-215>)    storyFlowAgent, err := NewStoryFlowAgent(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-216>)        storyGenerator,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-217>)        critic,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-218>)        reviser,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-219>)        grammarCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-220>)        toneCheck,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-221>)    )
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-222>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-223>)        log.Fatalf("Failed to create story flow agent: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-224>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-225>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-226>)    // --- Run the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-227>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-228>)    initialState := map[string]any{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-229>)        "topic": "a brave kitten exploring a haunted house",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-230>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-231>)    sessionInstance, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-232>)        AppName: appName,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-233>)        UserID:  userID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-234>)        State:   initialState,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-235>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-236>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-237>)        log.Fatalf("Failed to create session: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-238>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-239>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-240>)    userTopic := "a lonely robot finding a friend in a junkyard"
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-241>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-242>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-243>)        AppName:        appName,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-244>)        Agent:          storyFlowAgent,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-245>)        SessionService: sessionService,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-246>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-247>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-248>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-249>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-250>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-251>)    input := genai.NewContentFromText("Generate a story about: "+userTopic, genai.RoleUser)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-252>)    events := r.Run(ctx, userID, sessionInstance.Session.ID(), input, agent.RunConfig{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-253>)        StreamingMode: agent.StreamingModeSSE,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-254>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-255>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-256>)    var finalResponse string
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-257>)    for event, err := range events {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-258>)        if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-259>)            log.Fatalf("An error occurred during agent execution: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-260>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-261>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-262>)        for _, part := range event.Content.Parts {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-263>)            // Accumulate text from all parts of the final response.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-264>)            finalResponse += part.Text
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-265>)        }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-266>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-267>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-268>)    fmt.Println("\n--- Agent Interaction Result ---")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-269>)    fmt.Println("Agent Final Response: " + finalResponse)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-270>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-271>)    finalSession, err := sessionService.Get(ctx, &session.GetRequest{
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-272>)        UserID:    userID,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-273>)        AppName:   appName,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-274>)        SessionID: sessionInstance.Session.ID(),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-275>)    })
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-276>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-277>)    if err != nil {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-278>)        log.Fatalf("Failed to retrieve final session: %v", err)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-279>)    }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-280>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-281>)    fmt.Println("Final Session State:", finalSession.Session.State())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-61-282>)}
    
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-1>)# Full runnable code for the StoryFlowAgent example
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-2>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-4>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-5>)import com.google.adk.agents.InvocationContext;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-6>)import com.google.adk.agents.LoopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-7>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-8>)import com.google.adk.events.Event;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-9>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-10>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-11>)import com.google.genai.types.Content;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-12>)import com.google.genai.types.Part;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-13>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-14>)import java.util.HashMap;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-15>)import java.util.List;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-16>)import java.util.Map;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-17>)import java.util.Optional;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-18>)import java.util.concurrent.ConcurrentHashMap;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-19>)import java.util.logging.Level;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-20>)import java.util.logging.Logger;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-21>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-22>)public class StoryFlowAgentExample extends BaseAgent {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-23>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-24>)  // --- Constants ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-25>)  private static final String APP_NAME = "story_app";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-26>)  private static final String USER_ID = "user_12345";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-27>)  private static final String SESSION_ID = "session_123344";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-28>)  private static final String MODEL_NAME = "gemini-2.0-flash"; // Ensure this model is available
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-29>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-30>)  private static final Logger logger = Logger.getLogger(StoryFlowAgentExample.class.getName());
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-31>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-32>)  private final LlmAgent storyGenerator;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-33>)  private final LoopAgent loopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-34>)  private final SequentialAgent sequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-35>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-36>)  public StoryFlowAgentExample(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-37>)      String name, LlmAgent storyGenerator, LoopAgent loopAgent, SequentialAgent sequentialAgent) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-38>)    super(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-39>)        name,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-40>)        "Orchestrates story generation, critique, revision, and checks.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-41>)        List.of(storyGenerator, loopAgent, sequentialAgent),
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-42>)        null,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-43>)        null);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-44>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-45>)    this.storyGenerator = storyGenerator;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-46>)    this.loopAgent = loopAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-47>)    this.sequentialAgent = sequentialAgent;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-48>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-49>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-50>)  public static void main(String[] args) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-51>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-52>)    // --- Define the individual LLM agents ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-53>)    LlmAgent storyGenerator =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-54>)        LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-55>)            .name("StoryGenerator")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-56>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-57>)            .description("Generates the initial story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-58>)            .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-59>)                """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-60>)              You are a story writer. Write a short story (around 100 words) about a cat,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-61>)              based on the topic: {topic}
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-62>)              """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-63>)            .inputSchema(null)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-64>)            .outputKey("current_story") // Key for storing output in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-65>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-66>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-67>)    LlmAgent critic =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-68>)        LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-69>)            .name("Critic")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-70>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-71>)            .description("Critiques the story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-72>)            .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-73>)                """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-74>)              You are a story critic. Review the story: {current_story}. Provide 1-2 sentences of constructive criticism
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-75>)              on how to improve it. Focus on plot or character.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-76>)              """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-77>)            .inputSchema(null)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-78>)            .outputKey("criticism") // Key for storing criticism in session state
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-79>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-80>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-81>)    LlmAgent reviser =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-82>)        LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-83>)            .name("Reviser")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-84>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-85>)            .description("Revises the story based on criticism.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-86>)            .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-87>)                """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-88>)              You are a story reviser. Revise the story: {current_story}, based on the criticism: {criticism}. Output only the revised story.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-89>)              """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-90>)            .inputSchema(null)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-91>)            .outputKey("current_story") // Overwrites the original story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-92>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-93>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-94>)    LlmAgent grammarCheck =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-95>)        LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-96>)            .name("GrammarCheck")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-97>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-98>)            .description("Checks grammar and suggests corrections.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-99>)            .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-100>)                """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-101>)               You are a grammar checker. Check the grammar of the story: {current_story}. Output only the suggested
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-102>)               corrections as a list, or output 'Grammar is good!' if there are no errors.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-103>)               """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-104>)            .outputKey("grammar_suggestions")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-105>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-106>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-107>)    LlmAgent toneCheck =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-108>)        LlmAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-109>)            .name("ToneCheck")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-110>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-111>)            .description("Analyzes the tone of the story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-112>)            .instruction(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-113>)                """
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-114>)              You are a tone analyzer. Analyze the tone of the story: {current_story}. Output only one word: 'positive' if
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-115>)              the tone is generally positive, 'negative' if the tone is generally negative, or 'neutral'
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-116>)              otherwise.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-117>)              """)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-118>)            .outputKey("tone_check_result") // This agent's output determines the conditional flow
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-119>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-120>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-121>)    LoopAgent loopAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-122>)        LoopAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-123>)            .name("CriticReviserLoop")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-124>)            .description("Iteratively critiques and revises the story.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-125>)            .subAgents(critic, reviser)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-126>)            .maxIterations(2)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-127>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-128>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-129>)    SequentialAgent sequentialAgent =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-130>)        SequentialAgent.builder()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-131>)            .name("PostProcessing")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-132>)            .description("Performs grammar and tone checks sequentially.")
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-133>)            .subAgents(grammarCheck, toneCheck)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-134>)            .build();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-135>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-136>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-137>)    StoryFlowAgentExample storyFlowAgentExample =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-138>)        new StoryFlowAgentExample(APP_NAME, storyGenerator, loopAgent, sequentialAgent);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-139>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-140>)    // --- Run the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-141>)    runAgent(storyFlowAgentExample, "a lonely robot finding a friend in a junkyard");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-142>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-143>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-144>)  // --- Function to Interact with the Agent ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-145>)  // Sends a new topic to the agent (overwriting the initial one if needed)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-146>)  // and runs the workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-147>)  public static void runAgent(StoryFlowAgentExample agent, String userTopic) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-148>)    // --- Setup Runner and Session ---
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-149>)    InMemoryRunner runner = new InMemoryRunner(agent);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-150>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-151>)    Map<String, Object> initialState = new HashMap<>();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-152>)    initialState.put("topic", "a brave kitten exploring a haunted house");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-153>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-154>)    Session session =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-155>)        runner
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-156>)            .sessionService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-157>)            .createSession(APP_NAME, USER_ID, new ConcurrentHashMap<>(initialState), SESSION_ID)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-158>)            .blockingGet();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-159>)    logger.log(Level.INFO, () -> String.format("Initial session state: %s", session.state()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-160>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-161>)    session.state().put("topic", userTopic); // Update the state in the retrieved session
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-162>)    logger.log(Level.INFO, () -> String.format("Updated session state topic to: %s", userTopic));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-163>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-164>)    Content userMessage = Content.fromParts(Part.fromText("Generate a story about: " + userTopic));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-165>)    // Use the modified session object for the run
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-166>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-167>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-168>)    final String[] finalResponse = {"No final response captured."};
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-169>)    eventStream.blockingForEach(
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-170>)        event -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-171>)          if (event.finalResponse() && event.content().isPresent()) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-172>)            String author = event.author() != null ? event.author() : "UNKNOWN_AUTHOR";
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-173>)            Optional<String> textOpt =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-174>)                event
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-175>)                    .content()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-176>)                    .flatMap(Content::parts)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-177>)                    .filter(parts -> !parts.isEmpty())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-178>)                    .map(parts -> parts.get(0).text().orElse(""));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-179>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-180>)            logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-181>)                String.format("Potential final response from [%s]: %s", author, textOpt.orElse("N/A")));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-182>)            textOpt.ifPresent(text -> finalResponse[0] = text);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-183>)          }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-184>)        });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-185>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-186>)    System.out.println("\n--- Agent Interaction Result ---");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-187>)    System.out.println("Agent Final Response: " + finalResponse[0]);
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-188>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-189>)    // Retrieve session again to see the final state after the run
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-190>)    Session finalSession =
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-191>)        runner
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-192>)            .sessionService()
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-193>)            .getSession(APP_NAME, USER_ID, SESSION_ID, Optional.empty())
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-194>)            .blockingGet();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-195>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-196>)    assert finalSession != null;
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-197>)    System.out.println("Final Session State:" + finalSession.state());
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-198>)    System.out.println("-------------------------------\n");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-199>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-200>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-201>)  private boolean isStoryGenerated(InvocationContext ctx) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-202>)    Object currentStoryObj = ctx.session().state().get("current_story");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-203>)    return currentStoryObj != null && !String.valueOf(currentStoryObj).isEmpty();
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-204>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-205>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-206>)  @Override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-207>)  protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-208>)    // Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-209>)    // Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-210>)    logger.log(Level.INFO, () -> String.format("[%s] Starting story generation workflow.", name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-211>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-212>)    // Stage 1. Initial Story Generation
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-213>)    Flowable<Event> storyGenFlow = runStage(storyGenerator, invocationContext, "StoryGenerator");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-214>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-215>)    // Stage 2: Critic-Reviser Loop (runs after story generation completes)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-216>)    Flowable<Event> criticReviserFlow = Flowable.defer(() -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-217>)      if (!isStoryGenerated(invocationContext)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-218>)        logger.log(Level.SEVERE,() ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-219>)            String.format("[%s] Failed to generate initial story. Aborting after StoryGenerator.",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-220>)                name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-221>)        return Flowable.empty(); // Stop further processing if no story
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-222>)      }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-223>)        logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-224>)            String.format("[%s] Story state after generator: %s",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-225>)                name(), invocationContext.session().state().get("current_story")));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-226>)        return runStage(loopAgent, invocationContext, "CriticReviserLoop");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-227>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-228>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-229>)    // Stage 3: Post-Processing (runs after critic-reviser loop completes)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-230>)    Flowable<Event> postProcessingFlow = Flowable.defer(() -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-231>)      logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-232>)          String.format("[%s] Story state after loop: %s",
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-233>)              name(), invocationContext.session().state().get("current_story")));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-234>)      return runStage(sequentialAgent, invocationContext, "PostProcessing");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-235>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-236>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-237>)    // Stage 4: Conditional Regeneration (runs after post-processing completes)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-238>)    Flowable<Event> conditionalRegenFlow = Flowable.defer(() -> {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-239>)      String toneCheckResult = (String) invocationContext.session().state().get("tone_check_result");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-240>)      logger.log(Level.INFO, () -> String.format("[%s] Tone check result: %s", name(), toneCheckResult));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-241>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-242>)      if ("negative".equalsIgnoreCase(toneCheckResult)) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-243>)        logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-244>)            String.format("[%s] Tone is negative. Regenerating story...", name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-245>)        return runStage(storyGenerator, invocationContext, "StoryGenerator (Regen)");
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-246>)      } else {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-247>)        logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-248>)            String.format("[%s] Tone is not negative. Keeping current story.", name()));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-249>)        return Flowable.empty(); // No regeneration needed
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-250>)      }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-251>)    });
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-252>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-253>)    return Flowable.concatArray(storyGenFlow, criticReviserFlow, postProcessingFlow, conditionalRegenFlow)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-254>)        .doOnComplete(() -> logger.log(Level.INFO, () -> String.format("[%s] Workflow finished.", name())));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-255>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-256>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-257>)  // Helper method for a single agent run stage with logging
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-258>)  private Flowable<Event> runStage(BaseAgent agentToRun, InvocationContext ctx, String stageName) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-259>)    logger.log(Level.INFO, () -> String.format("[%s] Running %s...", name(), stageName));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-260>)    return agentToRun
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-261>)        .runAsync(ctx)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-262>)        .doOnNext(event ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-263>)            logger.log(Level.INFO,() ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-264>)                String.format("[%s] Event from %s: %s", name(), stageName, event.toJson())))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-265>)        .doOnError(err ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-266>)            logger.log(Level.SEVERE,
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-267>)                String.format("[%s] Error in %s", name(), stageName), err))
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-268>)        .doOnComplete(() ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-269>)            logger.log(Level.INFO, () ->
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-270>)                String.format("[%s] %s finished.", name(), stageName)));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-271>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-272>)
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-273>)  @Override
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-274>)  protected Flowable<Event> runLiveImpl(InvocationContext invocationContext) {
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-275>)    return Flowable.error(new UnsupportedOperationException("runLive not implemented."));
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-276>)  }
    [](<https://adk.dev/agents/custom-agents/#__codelineno-62-277>)}
    
Back to top 