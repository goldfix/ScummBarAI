# Cancel Agent Runs - Agent Development Kit (ADK)

> Source: [https://adk.dev/runtime/cancel/](https://adk.dev/runtime/cancel/)

[ Skip to content ](<https://adk.dev/runtime/cancel/#cancel-agent-runs>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/runtime/cancel.md> "Edit this page on GitHub") [ ](<https://adk.dev/runtime/cancel/index.md> "View this page as Markdown")

# Cancel agent runs[¶](<https://adk.dev/runtime/cancel/#cancel-agent-runs> "Permanent link")

Supported in ADKTypeScript v1.0.0

When an agent run takes too long, encounters changing conditions, or is no longer needed, you may want to cancel it without losing the work already completed. Cancellation in ADK is non-destructive: events already committed to the session remain persisted.

ADK supports graceful cancellation using `AbortController` and `AbortSignal`. Pass an `AbortSignal` to `runner.runAsync()` to cancel the entire invocation at any point in the execution stack, including agent execution, LLM generation, tool execution, and plugin callbacks.

## Get started[¶](<https://adk.dev/runtime/cancel/#get-started> "Permanent link")

Create an `AbortController`, pass its `signal` to `runner.runAsync()`, and call `controller.abort()` when you want to cancel execution:

TypeScript
    
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-1>)import { Runner, InMemorySessionService, LlmAgent, FunctionTool } from '@google/adk';
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-2>)import { z } from 'zod';
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-3>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-4>)const getInfo = new FunctionTool({
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-5>)  name: 'get_info',
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-6>)  description: 'Gets information about a topic.',
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-7>)  parameters: z.object({ topic: z.string() }),
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-8>)  execute: (args) => ({ result: `Info about ${args.topic}` }),
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-9>)});
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-10>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-11>)const agent = new LlmAgent({
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-12>)  name: 'my_agent',
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-13>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-14>)  instruction: 'Always use the get_info tool before answering.',
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-15>)  tools: [getInfo],
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-16>)});
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-17>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-18>)const sessionService = new InMemorySessionService();
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-19>)const runner = new Runner({ agent, appName: 'my_app', sessionService });
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-20>)const session = await sessionService.createSession({ appName: 'my_app', userId: 'user_1' });
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-21>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-22>)const controller = new AbortController();
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-23>)const run = runner.runAsync({
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-24>)  userId: session.userId,
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-25>)  sessionId: session.id,
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-26>)  newMessage: { role: 'user', parts: [{ text: 'Tell me about quantum computing.' }] },
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-27>)  abortSignal: controller.signal,
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-28>)});
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-29>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-30>)let count = 0;
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-31>)for await (const event of run) {
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-32>)  count++;
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-33>)  console.log('Event:', event.author);
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-34>)  controller.abort(); // Without this, 3+ events; with it, only 1.
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-35>)}
    [](<https://adk.dev/runtime/cancel/#__codelineno-0-36>)console.log(`Done. Received ${count} event(s).`);
    
## How cancellation propagates[¶](<https://adk.dev/runtime/cancel/#how-cancellation-propagates> "Permanent link")

When you abort the signal, cancellation propagates down through the entire execution stack. Each component checks `abortSignal.aborted` at critical lifecycle points and terminates early when it detects cancellation:

Component | What happens on abort  
---|---  
**Runner** | Stops before session fetch, after plugin callbacks, and within the event streaming loop.  
**LlmAgent** | Stops between execution steps, before/after model callbacks, and within response streaming.  
**LoopAgent** | Stops between loop iterations and between sub-agent executions.  
**ParallelAgent** | Stops when merging results from concurrent sub-agent runs.  
**Models (Gemini)** | The signal is passed to the underlying Google GenAI SDK via `config.abortSignal`, cancelling the in-flight HTTP request.  
**AgentTool** | Passes the signal to the sub-agent runner and checks for abort after session creation.  
**MCPTool** | Passes the signal to the MCP client's `callTool` method.  
  
The `InvocationContext` also registers a listener on the signal that automatically sets `endInvocation = true` when triggered, signaling all components to wind down.

### Behavior on cancellation[¶](<https://adk.dev/runtime/cancel/#behavior-on-cancellation> "Permanent link")

When an `AbortSignal` is triggered, the following applies:

  * **Graceful termination:** The async generator returned by `runner.runAsync()` completes (stops yielding events) without throwing an error.
  * **Committed events persist:** Any events that were already yielded and processed by the Runner before the abort remain committed to the session history.
  * **No partial events:** Events that were in progress but not yet yielded are discarded.
  * **Resource cleanup:** In-flight LLM requests to the Gemini API are cancelled through the SDK's native `AbortSignal` support, freeing network resources.

## Advanced examples[¶](<https://adk.dev/runtime/cancel/#advanced-examples> "Permanent link")

The following examples show additional cancellation patterns beyond the basic `AbortController` usage.

### Cancellation with a timeout[¶](<https://adk.dev/runtime/cancel/#cancellation-with-a-timeout> "Permanent link")

Use `AbortSignal.timeout()` to automatically cancel an agent run after a specified duration. This is useful for enforcing time limits on agent execution.

Using the same agent and runner setup from the get started example, replace everything from `const controller` onwards with:

TypeScript
    
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-1>)const run = runner.runAsync({
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-2>)  userId: session.userId,
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-3>)  sessionId: session.id,
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-4>)  newMessage: { role: 'user', parts: [{ text: 'Tell me about quantum computing.' }] },
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-5>)  abortSignal: AbortSignal.timeout(2_000), // Cancel after 2 seconds
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-6>)});
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-7>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-8>)let count = 0;
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-9>)for await (const event of run) {
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-10>)  count++;
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-11>)  console.log('Event:', event.author);
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-12>)}
    [](<https://adk.dev/runtime/cancel/#__codelineno-1-13>)console.log(`Done. Received ${count} event(s).`);
    
You can also combine a timeout with programmatic cancellation using `AbortSignal.any()`. Using the same setup, replace everything from `const controller` onwards with:

TypeScript
    
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-1>)const controller = new AbortController();
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-2>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-3>)// Cancel on timeout OR programmatically via controller.abort()
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-4>)// e.g.: cancelButton.addEventListener('click', () => controller.abort());
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-5>)const combinedSignal = AbortSignal.any([
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-6>)  controller.signal,
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-7>)  AbortSignal.timeout(60_000),
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-8>)]);
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-9>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-10>)const run = runner.runAsync({
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-11>)  userId: session.userId,
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-12>)  sessionId: session.id,
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-13>)  newMessage: { role: 'user', parts: [{ text: 'Tell me about quantum computing.' }] },
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-14>)  abortSignal: combinedSignal,
    [](<https://adk.dev/runtime/cancel/#__codelineno-2-15>)});
    
### AbortSignal in custom tools[¶](<https://adk.dev/runtime/cancel/#abortsignal-in-custom-tools> "Permanent link")

When you pass an `AbortSignal` to `runner.runAsync()`, it is available on `toolContext.abortSignal` inside your custom tools. The following example shows the pattern for checking the abort signal inside a custom tool:

TypeScript
    
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-1>)import { FunctionTool } from '@google/adk';
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-2>)import { z } from 'zod';
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-3>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-4>)const fetchItems = async (id: string) => ['item1', 'item2', 'item3'];
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-5>)const processItem = async (item: string) => ({ processed: item });
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-6>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-7>)const longRunningTool = new FunctionTool({
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-8>)  name: 'process_data',
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-9>)  description: 'Processes data in multiple steps.',
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-10>)  parameters: z.object({
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-11>)    dataId: z.string(),
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-12>)  }),
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-13>)  execute: async (args, toolContext) => {
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-14>)    const items = await fetchItems(args.dataId);
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-15>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-16>)    const results = [];
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-17>)    for (const item of items) {
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-18>)      // Check the abort signal before each step
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-19>)      if (toolContext?.abortSignal?.aborted) {
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-20>)        return { status: 'cancelled', processed: results.length };
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-21>)      }
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-22>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-23>)      results.push(await processItem(item));
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-24>)    }
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-25>)
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-26>)    return { status: 'complete', processed: results.length };
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-27>)  },
    [](<https://adk.dev/runtime/cancel/#__codelineno-3-28>)});
    
Back to top 