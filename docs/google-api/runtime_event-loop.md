# Event Loop - Agent Development Kit (ADK)

> Source: [https://adk.dev/runtime/event-loop/](https://adk.dev/runtime/event-loop/)

[ Skip to content ](<https://adk.dev/runtime/event-loop/#runtime-event-loop>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/runtime/event-loop.md> "Edit this page on GitHub") [ ](<https://adk.dev/runtime/event-loop/index.md> "View this page as Markdown")

# Runtime Event Loop[¶](<https://adk.dev/runtime/event-loop/#runtime-event-loop> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

The ADK Runtime is the underlying engine that powers your agent application during user interactions. It's the system that takes your defined agents, tools, and callbacks and orchestrates their execution in response to user input, managing the flow of information, state changes, and interactions with external services like LLMs or storage.

Think of the Runtime as the **"engine"** of your agentic application. You define the parts (agents, tools), and the Runtime handles how they connect and run together to fulfill a user's request.

## Core Idea: The Event Loop[¶](<https://adk.dev/runtime/event-loop/#core-idea-the-event-loop> "Permanent link")

At its heart, the ADK Runtime operates on an **Event Loop**. This loop facilitates a back-and-forth communication between the `Runner` component and your defined "Execution Logic" (which includes your Agents, the LLM calls they make, Callbacks, and Tools).

![intro_components.png](https://adk.dev/assets/event-loop.png)

In simple terms:

  1. The `Runner` receives a user query and asks the main `Agent` to start processing.
  2. The `Agent` (and its associated logic) runs until it has something to report (like a response, a request to use a tool, or a state change) – it then **yields** or **emits** an `Event`.
  3. The `Runner` receives this `Event`, processes any associated actions (like saving state changes via `Services`), and forwards the event onwards (e.g., to the user interface).
  4. The `Agent`'s logic **resumes** from where it paused only _after_ the `Runner` has processed the event, and then potentially sees the effects of the changes committed by the Runner.
  5. This cycle repeats until the agent has no more events to yield for the current user query.

This event-driven loop is the fundamental pattern governing how ADK executes your agent code.

## The Heartbeat: The Event Loop - Inner workings[¶](<https://adk.dev/runtime/event-loop/#the-heartbeat-the-event-loop-inner-workings> "Permanent link")

The Event Loop is the core operational pattern defining the interaction between the `Runner` and your custom code (Agents, Tools, Callbacks, collectively referred to as "Execution Logic" or "Logic Components" in the design document). It establishes a clear division of responsibilities:

Note

The specific method names and parameter names may vary slightly by SDK language (e.g., `agent.run_async(...)` in Python, `agent.Run(...)` in Go, `agent.runAsync(...)` in Java and TypeScript). Refer to the language-specific API documentation for details.

### Runner's Role (Orchestrator)[¶](<https://adk.dev/runtime/event-loop/#runners-role-orchestrator> "Permanent link")

The `Runner` acts as the central coordinator for a single user invocation. Its responsibilities in the loop are:

  1. **Initiation:** Receives the end user's query (`new_message`) and typically appends it to the session history via the `SessionService`.
  2. **Kick-off:** Starts the event generation process by calling the main agent's execution method (e.g., `agent_to_run.run_async(...)`).
  3. **Receive & Process:** Waits for the agent logic to `yield` or `emit` an `Event`. Upon receiving an event, the Runner **promptly processes** it. This involves:
     * Using configured `Services` (`SessionService`, `ArtifactService`, `MemoryService`) to commit changes indicated in `event.actions` (like `state_delta`, `artifact_delta`).
     * Performing other internal bookkeeping.
  4. **Yield Upstream:** Forwards the processed event onwards (e.g., to the calling application or UI for rendering).
  5. **Iterate:** Signals the agent logic that processing is complete for the yielded event, allowing it to resume and generate the _next_ event.

_Conceptual Runner Loop:_

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-1>)# Simplified view of Runner's main loop logic
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-2>)def run(new_query, ...) -> Generator[Event]:
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-3>)    # 1. Append new_query to session event history (via SessionService)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-4>)    session_service.append_event(session, Event(author='user', content=new_query))
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-5>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-6>)    # 2. Kick off event loop by calling the agent
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-7>)    agent_event_generator = agent_to_run.run_async(context)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-8>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-9>)    async for event in agent_event_generator:
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-10>)        # 3. Process the generated event and commit changes
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-11>)        session_service.append_event(session, event) # Commits state/artifact deltas etc.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-12>)        # memory_service.update_memory(...) # If applicable
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-13>)        # artifact_service might have already been called via context during agent run
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-14>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-15>)        # 4. Yield event for upstream processing (e.g., UI rendering)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-16>)        yield event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-0-17>)        # Runner implicitly signals agent generator can continue after yielding
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-1>)// Simplified view of Runner's main loop logic
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-2>)async * runAsync(newQuery: Content, ...): AsyncGenerator<Event, void, void> {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-3>)    // 1. Append newQuery to session event history (via SessionService)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-4>)    await sessionService.appendEvent({
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-5>)        session,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-6>)        event: createEvent({author: 'user', content: newQuery})
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-7>)    });
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-8>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-9>)    // 2. Kick off event loop by calling the agent
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-10>)    const agentEventGenerator = agentToRun.runAsync(context);
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-11>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-12>)    for await (const event of agentEventGenerator) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-13>)        // 3. Process the generated event and commit changes
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-14>)        // Commits state/artifact deltas etc.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-15>)        await sessionService.appendEvent({session, event});
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-16>)        // memoryService.updateMemory(...) // If applicable
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-17>)        // artifactService might have already been called via context during agent run
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-18>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-19>)        // 4. Yield event for upstream processing (e.g., UI rendering)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-20>)        yield event;
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-21>)        // Runner implicitly signals agent generator can continue after yielding
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-22>)    }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-1-23>)}
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-1>)// Simplified conceptual view of the Runner's main loop logic in Go
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-2>)func (r *Runner) RunConceptual(ctx context.Context, session *session.Session, newQuery *genai.Content) iter.Seq2[*Event, error] {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-3>)    return func(yield func(*Event, error) bool) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-4>)        // 1. Append new_query to session event history (via SessionService)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-5>)        // ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-6>)        userEvent := session.NewEvent(ctx, ctx.InvocationID()) // Simplified for conceptual view
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-7>)        userEvent.Author = "user"
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-8>)        userEvent.LLMResponse = model.LLMResponse{Content: newQuery}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-9>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-10>)        if _, err := r.sessionService.Append(ctx, &session.AppendRequest{Event: userEvent}); err != nil {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-11>)            yield(nil, err)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-12>)            return
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-13>)        }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-14>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-15>)        // 2. Kick off event stream by calling the agent
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-16>)        // Assuming agent.Run also returns iter.Seq2[*Event, error]
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-17>)        agentEventsAndErrs := r.agent.Run(ctx, &agent.RunRequest{Session: session, Input: newQuery})
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-18>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-19>)        for event, err := range agentEventsAndErrs {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-20>)            if err != nil {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-21>)                if !yield(event, err) { // Yield event even if there's an error, then stop
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-22>)                    return
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-23>)                }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-24>)                return // Agent finished with an error
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-25>)            }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-26>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-27>)            // 3. Process the generated event and commit changes
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-28>)            // Only commit non-partial event to a session service (as seen in actual code)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-29>)            if !event.LLMResponse.Partial {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-30>)                if _, err := r.sessionService.Append(ctx, &session.AppendRequest{Event: event}); err != nil {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-31>)                    yield(nil, err)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-32>)                    return
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-33>)                }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-34>)            }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-35>)            // memory_service.update_memory(...) // If applicable
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-36>)            // artifact_service might have already been called via context during agent run
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-37>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-38>)            // 4. Yield event for upstream processing
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-39>)            if !yield(event, nil) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-40>)                return // Upstream consumer stopped
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-41>)            }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-42>)        }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-43>)        // Agent finished successfully
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-44>)    }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-2-45>)}
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-1>)// Simplified conceptual view of the Runner's main loop logic in Java.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-2>)public Flowable<Event> runConceptual(
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-3>)    Session session,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-4>)    InvocationContext invocationContext,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-5>)    Content newQuery
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-6>)    ) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-7>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-8>)    // 1. Append new_query to session event history (via SessionService)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-9>)    // ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-10>)    sessionService.appendEvent(session, userEvent).blockingGet();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-11>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-12>)    // 2. Kick off event stream by calling the agent
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-13>)    Flowable<Event> agentEventStream = agentToRun.runAsync(invocationContext);
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-14>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-15>)    // 3. Process each generated event, commit changes, and "yield" or "emit"
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-16>)    return agentEventStream.map(event -> {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-17>)        // This mutates the session object (adds event, applies stateDelta).
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-18>)        // The return value of appendEvent (a Single<Event>) is conceptually
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-19>)        // just the event itself after processing.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-20>)        sessionService.appendEvent(session, event).blockingGet(); // Simplified blocking call
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-21>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-22>)        // memory_service.update_memory(...) // If applicable - conceptual
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-23>)        // artifact_service might have already been called via context during agent run
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-24>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-25>)        // 4. "Yield" event for upstream processing
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-26>)        //    In RxJava, returning the event in map effectively yields it to the next operator or subscriber.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-27>)        return event;
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-28>)    });
    [](<https://adk.dev/runtime/event-loop/#__codelineno-3-29>)}
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-1>)/**
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-2>) * Simplified view of Runner's main loop logic in Kotlin
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-3>) */
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-4>)fun runAsync(
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-5>)    userId: String,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-6>)    sessionId: String,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-7>)    newMessage: Content,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-8>)    runner: InMemoryRunner,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-9>)    sessionService: InMemorySessionService,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-10>)): Flow<Event> {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-11>)    // 1. Append newMessage to session event history (via SessionService)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-12>)    // 2. Kick off event loop by calling the agent
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-13>)    // 3. Process generated events, commit changes, and yield upstream
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-14>)    return runner
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-15>)        .runAsync(
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-16>)            userId = userId,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-17>)            sessionId = sessionId,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-18>)            newMessage = newMessage,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-19>)        ).onEach { event ->
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-20>)            // Process the event and commit changes to services (done internally by Runner)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-21>)            // sessionService.appendEvent(...)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-22>)        }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-4-23>)}
    
### Execution Logic's Role (Agent, Tool, Callback)[¶](<https://adk.dev/runtime/event-loop/#execution-logics-role-agent-tool-callback> "Permanent link")

Your code within agents, tools, and callbacks is responsible for the actual computation and decision-making. Its interaction with the loop involves:

  1. **Execute:** Runs its logic based on the current `InvocationContext`, including the session state _as it was when execution resumed_.
  2. **Yield:** When the logic needs to communicate (send a message, call a tool, report a state change), it constructs an `Event` containing the relevant content and actions, and then `yield`s this event back to the `Runner`.
  3. **Pause:** Crucially, execution of the agent logic **pauses immediately** after the `yield` statement (or `return` in RxJava). It waits for the `Runner` to complete step 3 (processing and committing).
  4. **Resume:** _Only after_ the `Runner` has processed the yielded event does the agent logic resume execution from the statement immediately following the `yield`.
  5. **See Updated State:** Upon resumption, the agent logic can now reliably access the session state (`ctx.session.state`) reflecting the changes that were committed by the `Runner` from the _previously yielded_ event.

_Conceptual Execution Logic:_

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-1>)# Simplified view of logic inside Agent.run_async, callbacks, or tools
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-2>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-3>)# ... previous code runs based on current state ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-4>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-5>)# 1. Determine a change or output is needed, construct the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-6>)# Example: Updating state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-7>)update_data = {'field_1': 'value_2'}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-8>)event_with_state_change = Event(
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-9>)    author=self.name,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-10>)    actions=EventActions(state_delta=update_data),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-11>)    content=types.Content(parts=[types.Part(text="State updated.")])
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-12>)    # ... other event fields ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-13>))
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-14>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-15>)# 2. Yield the event to the Runner for processing & commit
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-16>)yield event_with_state_change
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-17>)# <<<<<<<<<<<< EXECUTION PAUSES HERE >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-18>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-19>)# <<<<<<<<<<<< RUNNER PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-20>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-21>)# 3. Resume execution ONLY after Runner is done processing the above event.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-22>)# Now, the state committed by the Runner is reliably reflected.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-23>)# Subsequent code can safely assume the change from the yielded event happened.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-24>)val = ctx.session.state['field_1']
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-25>)# here `val` is guaranteed to be "value_2" (assuming Runner committed successfully)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-26>)print(f"Resumed execution. Value of field_1 is now: {val}")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-27>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-28>)# ... subsequent code continues ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-5-29>)# Maybe yield another event later...
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-1>)// Simplified view of logic inside Agent.runAsync, callbacks, or tools
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-2>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-3>)// ... previous code runs based on current state ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-4>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-5>)// 1. Determine a change or output is needed, construct the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-6>)// Example: Updating state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-7>)const updateData = {'field_1': 'value_2'};
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-8>)const eventWithStateChange = createEvent({
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-9>)    author: this.name,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-10>)    actions: createEventActions({stateDelta: updateData}),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-11>)    content: {parts: [{text: "State updated."}]}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-12>)    // ... other event fields ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-13>)});
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-14>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-15>)// 2. Yield the event to the Runner for processing & commit
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-16>)yield eventWithStateChange;
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-17>)// <<<<<<<<<<<< EXECUTION PAUSES HERE >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-18>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-19>)// <<<<<<<<<<<< RUNNER PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-20>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-21>)// 3. Resume execution ONLY after Runner is done processing the above event.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-22>)// Now, the state committed by the Runner is reliably reflected.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-23>)// Subsequent code can safely assume the change from the yielded event happened.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-24>)const val = ctx.session.state['field_1'];
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-25>)// here `val` is guaranteed to be "value_2" (assuming Runner committed successfully)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-26>)console.log(`Resumed execution. Value of field_1 is now: ${val}`);
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-27>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-28>)// ... subsequent code continues ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-6-29>)// Maybe yield another event later...
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-1>)// Simplified view of logic inside Agent.Run, callbacks, or tools
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-2>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-3>)// ... previous code runs based on current state ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-4>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-5>)// 1. Determine a change or output is needed, construct the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-6>)// Example: Updating state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-7>)updateData := map[string]interface{}{"field_1": "value_2"}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-8>)eventWithStateChange := &Event{
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-9>)    Author: self.Name(),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-10>)    Actions: &EventActions{StateDelta: updateData},
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-11>)    Content: genai.NewContentFromText("State updated.", "model"),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-12>)    // ... other event fields ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-13>)}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-14>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-15>)// 2. Yield the event to the Runner for processing & commit
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-16>)// In Go, this is done by sending the event to a channel.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-17>)eventsChan <- eventWithStateChange
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-18>)// <<<<<<<<<<<< EXECUTION PAUSES HERE (conceptually) >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-19>)// The Runner on the other side of the channel will receive and process the event.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-20>)// The agent's goroutine might continue, but the logical flow waits for the next input or step.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-21>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-22>)// <<<<<<<<<<<< RUNNER PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-23>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-24>)// 3. Resume execution ONLY after Runner is done processing the above event.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-25>)// In a real Go implementation, this would likely be handled by the agent receiving
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-26>)// a new RunRequest or context indicating the next step. The updated state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-27>)// would be part of the session object in that new request.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-28>)// For this conceptual example, we'll just check the state.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-29>)val := ctx.State.Get("field_1")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-30>)// here `val` is guaranteed to be "value_2" because the Runner would have
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-31>)// updated the session state before calling the agent again.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-32>)fmt.Printf("Resumed execution. Value of field_1 is now: %v\n", val)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-33>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-34>)// ... subsequent code continues ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-7-35>)// Maybe send another event to the channel later...
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-1>)// Simplified view of logic inside Agent.runAsync, callbacks, or tools
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-2>)// ... previous code runs based on current state ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-3>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-4>)// 1. Determine a change or output is needed, construct the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-5>)// Example: Updating state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-6>)ConcurrentMap<String, Object> updateData = new ConcurrentHashMap<>();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-7>)updateData.put("field_1", "value_2");
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-8>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-9>)EventActions actions = EventActions.builder().stateDelta(updateData).build();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-10>)Content eventContent = Content.builder().parts(Part.fromText("State updated.")).build();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-11>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-12>)Event eventWithStateChange = Event.builder()
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-13>)    .author(self.name())
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-14>)    .actions(actions)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-15>)    .content(Optional.of(eventContent))
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-16>)    // ... other event fields ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-17>)    .build();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-18>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-19>)// 2. "Yield" the event. In RxJava, this means emitting it into the stream.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-20>)//    The Runner (or upstream consumer) will subscribe to this Flowable.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-21>)//    When the Runner receives this event, it will process it (e.g., call sessionService.appendEvent).
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-22>)//    The 'appendEvent' in Java ADK mutates the 'Session' object held within 'ctx' (InvocationContext).
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-23>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-24>)// <<<<<<<<<<<< CONCEPTUAL PAUSE POINT >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-25>)// In RxJava, the emission of 'eventWithStateChange' happens, and then the stream
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-26>)// might continue with a 'flatMap' or 'concatMap' operator that represents
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-27>)// the logic *after* the Runner has processed this event.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-28>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-29>)// To model the "resume execution ONLY after Runner is done processing":
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-30>)// The Runner's `appendEvent` is usually an async operation itself (returns Single<Event>).
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-31>)// The agent's flow needs to be structured such that subsequent logic
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-32>)// that depends on the committed state runs *after* that `appendEvent` completes.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-33>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-34>)// This is how the Runner typically orchestrates it:
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-35>)// Runner:
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-36>)//   agent.runAsync(ctx)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-37>)//     .concatMapEager(eventFromAgent ->
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-38>)//         sessionService.appendEvent(ctx.session(), eventFromAgent) // This updates ctx.session().state()
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-39>)//             .toFlowable() // Emits the event after it's processed
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-40>)//     )
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-41>)//     .subscribe(processedEvent -> { /* UI renders processedEvent */ });
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-42>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-43>)// So, within the agent's own logic, if it needs to do something *after* an event it yielded
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-44>)// has been processed and its state changes are reflected in ctx.session().state(),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-45>)// that subsequent logic would typically be in another step of its reactive chain.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-46>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-47>)// For this conceptual example, we'll emit the event, and then simulate the "resume"
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-48>)// as a subsequent operation in the Flowable chain.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-49>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-50>)return Flowable.just(eventWithStateChange) // Step 2: Yield the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-51>)    .concatMap(yieldedEvent -> {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-52>)        // <<<<<<<<<<<< RUNNER CONCEPTUALLY PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-53>)        // At this point, in a real runner, ctx.session().appendEvent(yieldedEvent) would have been called
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-54>)        // by the Runner, and ctx.session().state() would be updated.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-55>)        // Since we are *inside* the agent's conceptual logic trying to model this,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-56>)        // we assume the Runner's action has implicitly updated our 'ctx.session()'.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-57>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-58>)        // 3. Resume execution.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-59>)        // Now, the state committed by the Runner (via sessionService.appendEvent)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-60>)        // is reliably reflected in ctx.session().state().
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-61>)        Object val = ctx.session().state().get("field_1");
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-62>)        // here `val` is guaranteed to be "value_2" because the `sessionService.appendEvent`
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-63>)        // called by the Runner would have updated the session state within the `ctx` object.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-64>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-65>)        System.out.println("Resumed execution. Value of field_1 is now: " + val);
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-66>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-67>)        // ... subsequent code continues ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-8-68>)        // If this subsequent code needs to yield another event, it would do so here.
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-1>)/**
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-2>) * Simplified view of logic inside Agent.runAsync, callbacks, or tools in Kotlin
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-3>) */
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-4>)suspend fun executionLogic(ctx: InvocationContext) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-5>)    // ... previous code runs based on current state ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-6>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-7>)    // 1. Determine a change or output is needed, construct the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-8>)    val updateData = mapOf("field_1" to "value_2")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-9>)    val eventWithStateChange =
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-10>)        Event(
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-11>)            author = "my_agent",
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-12>)            actions = EventActions(stateDelta = updateData.toMutableMap()),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-13>)            content = Content.fromText(Role.MODEL, "State updated."),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-14>)        )
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-15>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-16>)    // 2. Yield the event to the Runner for processing & commit
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-17>)    // In Kotlin, this is done by emitting to the Flow
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-18>)    // emit(eventWithStateChange)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-19>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-20>)    // <<<<<<<<<<<< EXECUTION PAUSES HERE >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-21>)    // (Implicitly, when the Flow consumer collects the event and processes it)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-22>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-23>)    // <<<<<<<<<<<< RUNNER PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-24>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-25>)    // 3. Resume execution ONLY after Runner is done processing.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-26>)    // Now, the state committed by the Runner is reliably reflected.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-27>)    val val1 = ctx.session.state["field_1"]
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-28>)    println("Resumed execution. Value of field_1 is now: $val1")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-9-29>)}
    
This cooperative yield/pause/resume cycle between the `Runner` and your Execution Logic, mediated by `Event` objects, forms the core of the ADK Runtime.

## Key components of the Runtime[¶](<https://adk.dev/runtime/event-loop/#key-components-of-the-runtime> "Permanent link")

Several components work together within the ADK Runtime to execute an agent invocation. Understanding their roles clarifies how the event loop functions:

  1. ### `Runner`[¶](<https://adk.dev/runtime/event-loop/#runner> "Permanent link")

     * **Role:** The main entry point and orchestrator for a single user query (`run_async`).
     * **Function:** Manages the overall Event Loop, receives events yielded by the Execution Logic, coordinates with Services to process and commit event actions (state/artifact changes), and forwards processed events upstream (e.g., to the UI). It essentially drives the conversation turn by turn based on yielded events. (Defined in `google.adk.runners.runner`).
  2. ### Execution Logic Components[¶](<https://adk.dev/runtime/event-loop/#execution-logic-components> "Permanent link")

     * **Role:** The parts containing your custom code and the core agent capabilities.
     * **Components:**
       * `Agent` (`BaseAgent`, `LlmAgent`, etc.): Your primary logic units that process information and decide on actions. They implement the `_run_async_impl` method which yields events.
       * `Tools` (`BaseTool`, `FunctionTool`, `AgentTool`, etc.): External functions or capabilities used by agents (often `LlmAgent`) to interact with the outside world or perform specific tasks. They execute and return results, which are then wrapped in events.
       * `Callbacks` (Functions): User-defined functions attached to agents (e.g., `before_agent_callback`, `after_model_callback`) that hook into specific points in the execution flow, potentially modifying behavior or state, whose effects are captured in events.
     * **Function:** Perform the actual thinking, calculation, or external interaction. They communicate their results or needs by **yielding`Event` objects** and pausing until the Runner processes them.
  3. ### `Event`[¶](<https://adk.dev/runtime/event-loop/#event> "Permanent link")

     * **Role:** The message passed back and forth between the `Runner` and the Execution Logic.
     * **Function:** Represents an atomic occurrence (user input, agent text, tool call/result, state change request, control signal). It carries both the content of the occurrence and the intended side effects (`actions` like `state_delta`).
  4. ### `Services`[¶](<https://adk.dev/runtime/event-loop/#services> "Permanent link")

     * **Role:** Backend components responsible for managing persistent or shared resources. Used primarily by the `Runner` during event processing.
     * **Components:**
       * `SessionService` (`BaseSessionService`, `InMemorySessionService`, etc.): Manages `Session` objects, including saving/loading them, applying `state_delta` to the session state, and appending events to the `event history`.
       * `ArtifactService` (`BaseArtifactService`, `InMemoryArtifactService`, `GcsArtifactService`, etc.): Manages the storage and retrieval of binary artifact data. Although `save_artifact` is called via context during execution logic, the `artifact_delta` in the event confirms the action for the Runner/SessionService.
       * `MemoryService` (`BaseMemoryService`, etc.): (Optional) Manages long-term semantic memory across sessions for a user.
     * **Function:** Provide the persistence layer. The `Runner` interacts with them to ensure changes signaled by `event.actions` are reliably stored _before_ the Execution Logic resumes.
  5. ### `Session`[¶](<https://adk.dev/runtime/event-loop/#session> "Permanent link")

     * **Role:** A data container holding the state and history for _one specific conversation_ between a user and the application.
     * **Function:** Stores the current `state` dictionary, the list of all past `events` (`event history`), and references to associated artifacts. It's the primary record of the interaction, managed by the `SessionService`.
  6. ### `Invocation`[¶](<https://adk.dev/runtime/event-loop/#invocation> "Permanent link")

     * **Role:** A conceptual term representing everything that happens in response to a _single_ user query, from the moment the `Runner` receives it until the agent logic finishes yielding events for that query.
     * **Function:** An invocation might involve multiple agent runs (if using agent transfer or `AgentTool`), multiple LLM calls, tool executions, and callback executions, all tied together by a single `invocation_id` within the `InvocationContext`. State variables prefixed with `temp:` are strictly scoped to a single invocation and discarded afterwards.

These players interact continuously through the Event Loop to process a user's request.

## How It Works: A Simplified Invocation[¶](<https://adk.dev/runtime/event-loop/#how-it-works-a-simplified-invocation> "Permanent link")

Let's trace a simplified flow for a typical user query that involves an LLM agent calling a tool:

![intro_components.png](https://adk.dev/assets/invocation-flow.png)

### Step-by-Step Breakdown[¶](<https://adk.dev/runtime/event-loop/#step-by-step-breakdown> "Permanent link")

  1. **User Input:** The User sends a query (e.g., "What's the capital of France?").
  2. **Runner Starts:** `Runner.run_async` begins. It interacts with the `SessionService` to load the relevant `Session` and adds the user query as the first `Event` to the session history. An `InvocationContext` (`ctx`) is prepared.
  3. **Agent Execution:** The `Runner` calls `agent.run_async(ctx)` on the designated root agent (e.g., an `LlmAgent`).
  4. **LLM Call (Example):** The `Agent_Llm` determines it needs information, perhaps by calling a tool. It prepares a request for the `LLM`. Let's assume the LLM decides to call `MyTool`.
  5. **Yield FunctionCall Event:** The `Agent_Llm` receives the `FunctionCall` response from the LLM, wraps it in an `Event(author='Agent_Llm', content=Content(parts=[Part(function_call=...)]))`, and `yields` or `emits` this event.
  6. **Agent Pauses:** The `Agent_Llm`'s execution pauses immediately after the `yield`.
  7. **Runner Processes:** The `Runner` receives the FunctionCall event. It passes it to the `SessionService` to record it in the history. The `Runner` then yields the event upstream to the `User` (or application).
  8. **Agent Resumes:** The `Runner` signals that the event is processed, and `Agent_Llm` resumes execution.
  9. **Tool Execution:** The `Agent_Llm`'s internal flow now proceeds to execute the requested `MyTool`. It calls `tool.run_async(...)`.
  10. **Tool Returns Result:** `MyTool` executes and returns its result (e.g., `{'result': 'Paris'}`).
  11. **Yield FunctionResponse Event:** The agent (`Agent_Llm`) wraps the tool result into an `Event` containing a `FunctionResponse` part (e.g., `Event(author='Agent_Llm', content=Content(role='user', parts=[Part(function_response=...)]))`). This event might also contain `actions` if the tool modified state (`state_delta`) or saved artifacts (`artifact_delta`). The agent `yield`s this event.
  12. **Agent Pauses:** `Agent_Llm` pauses again.
  13. **Runner Processes:** `Runner` receives the FunctionResponse event. It passes it to `SessionService` which applies any `state_delta`/`artifact_delta` and adds the event to history. `Runner` yields the event upstream.
  14. **Agent Resumes:** `Agent_Llm` resumes, now knowing the tool result and any state changes are committed.
  15. **Final LLM Call (Example):** `Agent_Llm` sends the tool result back to the `LLM` to generate a natural language response.
  16. **Yield Final Text Event:** `Agent_Llm` receives the final text from the `LLM`, wraps it in an `Event(author='Agent_Llm', content=Content(parts=[Part(text=...)]))`, and `yield`s it.
  17. **Agent Pauses:** `Agent_Llm` pauses.
  18. **Runner Processes:** `Runner` receives the final text event, passes it to `SessionService` for history, and yields it upstream to the `User`. This is likely marked as the `is_final_response()`.
  19. **Agent Resumes & Finishes:** `Agent_Llm` resumes. Having completed its task for this invocation, its `run_async` generator finishes.
  20. **Runner Completes:** The `Runner` sees the agent's generator is exhausted and finishes its loop for this invocation.

This yield/pause/process/resume cycle ensures that state changes are consistently applied and that the execution logic always operates on the most recently committed state after yielding an event.

## Important Runtime Behaviors[¶](<https://adk.dev/runtime/event-loop/#important-runtime-behaviors> "Permanent link")

Understanding a few key aspects of how the ADK Runtime handles state, streaming, and asynchronous operations is crucial for building predictable and efficient agents.

### State Updates & Commitment Timing[¶](<https://adk.dev/runtime/event-loop/#state-updates-commitment-timing> "Permanent link")

  * **The Rule:** When your code (in an agent, tool, or callback) modifies the session state (e.g., `context.state['my_key'] = 'new_value'`), this change is initially recorded locally within the current `InvocationContext`. The change is only **guaranteed to be persisted** (saved by the `SessionService`) _after_ the `Event` carrying the corresponding `state_delta` in its `actions` has been `yield`-ed by your code and subsequently processed by the `Runner`.

  * **Implication:** Code that runs _after_ resuming from a `yield` can reliably assume that the state changes signaled in the _yielded event_ have been committed.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-1>)# Inside agent logic (conceptual)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-2>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-3>)# 1. Modify state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-4>)ctx.session.state['status'] = 'processing'
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-5>)event1 = Event(..., actions=EventActions(state_delta={'status': 'processing'}))
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-6>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-7>)# 2. Yield event with the delta
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-8>)yield event1
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-9>)# --- PAUSE --- Runner processes event1, SessionService commits 'status' = 'processing' ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-10>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-11>)# 3. Resume execution
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-12>)# Now it's safe to rely on the committed state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-13>)current_status = ctx.session.state['status'] # Guaranteed to be 'processing'
    [](<https://adk.dev/runtime/event-loop/#__codelineno-10-14>)print(f"Status after resuming: {current_status}")
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-1>)// Inside agent logic (conceptual)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-2>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-3>)// 1. Modify state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-4>)// In TypeScript, you modify state via the context, which tracks the change.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-5>)ctx.state.set('status', 'processing');
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-6>)// The framework will automatically populate actions with the state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-7>)// delta from the context. For illustration, it's shown here.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-8>)const event1 = createEvent({
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-9>)    actions: createEventActions({stateDelta: {'status': 'processing'}}),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-10>)    // ... other event fields
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-11>)});
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-12>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-13>)// 2. Yield event with the delta
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-14>)yield event1;
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-15>)// --- PAUSE --- Runner processes event1, SessionService commits 'status' = 'processing' ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-16>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-17>)// 3. Resume execution
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-18>)// Now it's safe to rely on the committed state in the session object.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-19>)const currentStatus = ctx.session.state['status']; // Guaranteed to be 'processing'
    [](<https://adk.dev/runtime/event-loop/#__codelineno-11-20>)console.log(`Status after resuming: ${currentStatus}`);
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-1>)  // Inside agent logic (conceptual)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-2>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-3>)func (a *Agent) RunConceptual(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-4>)  // The entire logic is wrapped in a function that will be returned as an iterator.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-5>)  return func(yield func(*session.Event, error) bool) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-6>)      // ... previous code runs based on current state from the input `ctx` ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-7>)      // e.g., val := ctx.State().Get("field_1") might return "value_1" here.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-8>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-9>)      // 1. Determine a change or output is needed, construct the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-10>)      updateData := map[string]interface{}{"field_1": "value_2"}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-11>)      eventWithStateChange := session.NewEvent(ctx, ctx.InvocationID())
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-12>)      eventWithStateChange.Author = a.Name()
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-13>)      eventWithStateChange.Actions = &session.EventActions{StateDelta: updateData}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-14>)      // ... other event fields ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-15>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-16>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-17>)      // 2. Yield the event to the Runner for processing & commit.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-18>)      // The agent's execution continues immediately after this call.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-19>)      if !yield(eventWithStateChange, nil) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-20>)          // If yield returns false, it means the consumer (the Runner)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-21>)          // has stopped listening, so we should stop producing events.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-22>)          return
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-23>)      }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-24>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-25>)      // <<<<<<<<<<<< RUNNER PROCESSES & COMMITS THE EVENT >>>>>>>>>>>>
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-26>)      // This happens outside the agent, after the agent's iterator has
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-27>)      // produced the event.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-28>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-29>)      // 3. The agent CANNOT immediately see the state change it just yielded.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-30>)      // The state is immutable within a single `Run` invocation.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-31>)      val := ctx.State().Get("field_1")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-32>)      // `val` here is STILL "value_1" (or whatever it was at the start).
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-33>)      // The updated state ("value_2") will only be available in the `ctx`
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-34>)      // of the *next* `Run` invocation in a subsequent turn.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-35>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-36>)      // ... subsequent code continues, potentially yielding more events ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-37>)      finalEvent := session.NewEvent(ctx, ctx.InvocationID())
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-38>)      finalEvent.Author = a.Name()
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-39>)      // ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-40>)      yield(finalEvent, nil)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-41>)  }
    [](<https://adk.dev/runtime/event-loop/#__codelineno-12-42>)}
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-1>)// Inside agent logic (conceptual)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-2>)// ... previous code runs based on current state ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-3>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-4>)// 1. Prepare state modification and construct the event
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-5>)ConcurrentHashMap<String, Object> stateChanges = new ConcurrentHashMap<>();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-6>)stateChanges.put("status", "processing");
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-7>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-8>)EventActions actions = EventActions.builder().stateDelta(stateChanges).build();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-9>)Content content = Content.builder().parts(Part.fromText("Status update: processing")).build();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-10>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-11>)Event event1 = Event.builder()
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-12>)    .actions(actions)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-13>)    // ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-14>)    .build();
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-15>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-16>)// 2. Yield event with the delta
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-17>)return Flowable.just(event1)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-18>)    .map(
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-19>)        emittedEvent -> {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-20>)            // --- CONCEPTUAL PAUSE & RUNNER PROCESSING ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-21>)            // 3. Resume execution (conceptually)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-22>)            // Now it's safe to rely on the committed state.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-23>)            String currentStatus = (String) ctx.session().state().get("status");
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-24>)            System.out.println("Status after resuming (inside agent logic): " + currentStatus); // Guaranteed to be 'processing'
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-25>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-26>)            // The event itself (event1) is passed on.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-27>)            // If subsequent logic within this agent step produced *another* event,
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-28>)            // you'd use concatMap to emit that new event.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-29>)            return emittedEvent;
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-30>)        });
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-31>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-32>)// ... subsequent agent logic might involve further reactive operators
    [](<https://adk.dev/runtime/event-loop/#__codelineno-13-33>)// or emitting more events based on the now-updated `ctx.session().state()`.
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-1>)/**
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-2>) * Conceptual view of state update timing in Kotlin
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-3>) */
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-4>)suspend fun stateUpdateTiming(ctx: InvocationContext) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-5>)    // 1. Modify state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-6>)    ctx.session.state["status"] = "processing"
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-7>)    val event1 =
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-8>)        Event(
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-9>)            author = "my_agent",
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-10>)            actions = EventActions(stateDelta = mutableMapOf("status" to "processing")),
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-11>)        )
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-12>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-13>)    // 2. Yield event with the delta (emit to flow)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-14>)    // emit(event1)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-15>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-16>)    // --- PAUSE --- Runner processes event1, SessionService commits 'status' = 'processing' ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-17>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-18>)    // 3. Resume execution
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-19>)    // Now it's safe to rely on the committed state
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-20>)    val currentStatus = ctx.session.state["status"] // Guaranteed to be 'processing'
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-21>)    println("Status after resuming: $currentStatus")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-14-22>)}
    
### "Dirty Reads" of Session State[¶](<https://adk.dev/runtime/event-loop/#dirty-reads-of-session-state> "Permanent link")

  * **Definition:** While commitment happens _after_ the yield, code running _later within the same invocation_ , but _before_ the state-changing event is actually yielded and processed, **can often see the local, uncommitted changes**. This is sometimes called a "dirty read".
  * **Example:**

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-1>)# Code in before_agent_callback
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-2>)callback_context.state['field_1'] = 'value_1'
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-3>)# State is locally set to 'value_1', but not yet committed by Runner
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-4>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-5>)# ... agent runs ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-6>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-7>)# Code in a tool called later *within the same invocation*
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-8>)# Readable (dirty read), but 'value_1' isn't guaranteed persistent yet.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-9>)val = tool_context.state['field_1'] # 'val' will likely be 'value_1' here
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-10>)print(f"Dirty read value in tool: {val}")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-11>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-12>)# Assume the event carrying the state_delta={'field_1': 'value_1'}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-15-13>)# is yielded *after* this tool runs and is processed by the Runner.
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-1>)// Code in beforeAgentCallback
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-2>)callbackContext.state.set('field_1', 'value_1');
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-3>)// State is locally set to 'value_1', but not yet committed by Runner
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-4>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-5>)// --- agent runs ... ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-6>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-7>)// --- Code in a tool called later *within the same invocation* ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-8>)// Readable (dirty read), but 'value_1' isn't guaranteed persistent yet.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-9>)const val = toolContext.state.get('field_1'); // 'val' will likely be 'value_1' here
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-10>)console.log(`Dirty read value in tool: ${val}`);
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-11>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-12>)// Assume the event carrying the state_delta={'field_1': 'value_1'}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-16-13>)// is yielded *after* this tool runs and is processed by the Runner.
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-1>)// Code in before_agent_callback
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-2>)// The callback would modify the context's session state directly.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-3>)// This change is local to the current invocation context.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-4>)ctx.State.Set("field_1", "value_1")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-5>)// State is locally set to 'value_1', but not yet committed by Runner
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-6>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-7>)// ... agent runs ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-8>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-9>)// Code in a tool called later *within the same invocation*
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-10>)// Readable (dirty read), but 'value_1' isn't guaranteed persistent yet.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-11>)val := ctx.State.Get("field_1") // 'val' will likely be 'value_1' here
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-12>)fmt.Printf("Dirty read value in tool: %v\n", val)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-13>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-14>)// Assume the event carrying the state_delta={'field_1': 'value_1'}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-17-15>)// is yielded *after* this tool runs and is processed by the Runner.
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-1>)// Modify state - Code in BeforeAgentCallback
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-2>)// AND stages this change in callbackContext.eventActions().stateDelta().
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-3>)callbackContext.state().put("field_1", "value_1");
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-4>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-5>)// --- agent runs ... ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-6>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-7>)// --- Code in a tool called later *within the same invocation* ---
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-8>)// Readable (dirty read), but 'value_1' isn't guaranteed persistent yet.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-9>)Object val = toolContext.state().get("field_1"); // 'val' will likely be 'value_1' here
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-10>)System.out.println("Dirty read value in tool: " + val);
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-11>)// Assume the event carrying the state_delta={'field_1': 'value_1'}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-18-12>)// is yielded *after* this tool runs and is processed by the Runner.
    
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-1>)/**
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-2>) * Conceptual view of dirty reads in Kotlin
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-3>) */
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-4>)fun dirtyRead(ctx: InvocationContext) {
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-5>)    // Code in a callback
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-6>)    ctx.session.state["field_1"] = "value_1"
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-7>)    // State is locally set to 'value_1', but not yet committed by Runner
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-8>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-9>)    // ... agent runs ...
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-10>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-11>)    // Code in a tool called later *within the same invocation*
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-12>)    // Readable (dirty read), but 'value_1' isn't guaranteed persistent yet.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-13>)    val val1 = ctx.session.state["field_1"] // 'val' will likely be 'value_1' here
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-14>)    println("Dirty read value in tool: $val1")
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-15>)
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-16>)    // Assume the event carrying the state_delta={'field_1': 'value_1'}
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-17>)    // is yielded *after* this tool runs and is processed by the Runner.
    [](<https://adk.dev/runtime/event-loop/#__codelineno-19-18>)}
    
  * **Implications:**
  * **Benefit:** Allows different parts of your logic within a single complex step (e.g., multiple callbacks or tool calls before the next LLM turn) to coordinate using state without waiting for a full yield/commit cycle.
  * **Caveat:** Relying heavily on dirty reads for critical logic can be risky. If the invocation fails _before_ the event carrying the `state_delta` is yielded and processed by the `Runner`, the uncommitted state change will be lost. For critical state transitions, ensure they are associated with an event that gets successfully processed.

### Streaming vs. Non-Streaming Output (`partial=True`)[¶](<https://adk.dev/runtime/event-loop/#streaming-vs-non-streaming-output-partialtrue> "Permanent link")

This primarily relates to how responses from the LLM are handled, especially when using streaming generation APIs.

  * **Streaming:** The LLM generates its response token-by-token or in small chunks.
  * The framework (often within `BaseLlmFlow`) yields multiple `Event` objects for a single conceptual response. Most of these events will have `partial=True`.
  * The `Runner`, upon receiving an event with `partial=True`, typically **forwards it immediately** upstream (for UI display) but **skips processing its`actions`** (like `state_delta`).
  * Eventually, the framework yields a final event for that response, marked as non-partial (`partial=False` or implicitly via `turn_complete=True`).
  * The `Runner` **fully processes only this final event** , committing any associated `state_delta` or `artifact_delta`.
  * **Non-Streaming:** The LLM generates the entire response at once. The framework yields a single event marked as non-partial, which the `Runner` processes fully.
  * **Why it Matters:** Ensures that state changes are applied atomically and only once based on the _complete_ response from the LLM, while still allowing the UI to display text progressively as it's generated.

## Async is Primary (`run_async`)[¶](<https://adk.dev/runtime/event-loop/#async-is-primary-run_async> "Permanent link")

  * **Core Design:** The ADK Runtime is fundamentally built on asynchronous patterns and libraries (like Python's `asyncio`, Java's `RxJava`, and native `Promise`s and `AsyncGenerator`s in TypeScript) to handle concurrent operations (like waiting for LLM responses or tool executions) efficiently without blocking.
  * **Main Entry Point:** `Runner.run_async` is the primary method for executing agent invocations. All core runnable components (Agents, specific flows) use `asynchronous` methods internally.
  * **Synchronous Convenience (`run`):** A synchronous `Runner.run` method exists mainly for convenience (e.g., in simple scripts or testing environments). However, internally, `Runner.run` typically just calls `Runner.run_async` and manages the async event loop execution for you.
  * **Developer Experience:** We recommend designing your applications (e.g., web servers using ADK) to be asynchronous for best performance. In Python, this means using `asyncio`; in Java, leverage `RxJava`'s reactive programming model; and in TypeScript, this means building using native `Promise`s and `AsyncGenerator`s.
  * **Sync Callbacks/Tools:** The ADK framework supports both asynchronous and synchronous functions for tools and callbacks.
    * **Blocking I/O:** For long-running synchronous I/O operations, the framework attempts to prevent stalls. Python ADK may use asyncio.to_thread, while Java ADK often relies on appropriate RxJava schedulers or wrappers for blocking calls. In TypeScript, the framework simply awaits the function; if a synchronous function performs blocking I/O, it will stall the event loop. Developers should use asynchronous I/O APIs (which return a Promise) whenever possible.
    * **CPU-Bound Work:** Purely CPU-intensive synchronous tasks will still block their execution thread in both environments.

Understanding these behaviors helps you write more robust ADK applications and debug issues related to state consistency, streaming updates, and asynchronous execution.

Back to top 