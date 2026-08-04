# Model routing - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/models/routing/](https://adk.dev/agents/models/routing/)

[ Skip to content ](<https://adk.dev/agents/models/routing/#route-between-models>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/models/routing.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/models/routing/index.md> "View this page as Markdown")

# Route between models[¶](<https://adk.dev/agents/models/routing/#route-between-models> "Permanent link")

Supported in ADKTypeScript v1.0.0Experimental

Experimental

Model routing is experimental and may change in future releases. We welcome your [feedback](<https://github.com/google/adk-js/issues/new?template=feature_request.md>)!

An `LlmAgent` uses a single model by default. When you need to dynamically select between different models for each request, you can define a routing function that chooses which model to use. `RoutedLlm` provides this capability, enabling model fallback on error, A/B testing between models, and auto-routing by input complexity. If the selected model fails before producing any output, the routing function is called again with error context so it can select a different model.

Pass a `RoutedLlm` as an `LlmAgent`'s `model` parameter. Use `RoutedLlm` when only the model varies between routes. If you also need to switch instructions, tools, or sub-agents, use [`RoutedAgent`](<https://adk.dev/agents/routing/>) instead.

## How routing works[¶](<https://adk.dev/agents/models/routing/#how-routing-works> "Permanent link")

The `LlmRouter` function receives the map of available models and the current `LlmRequest`, and returns the key of the model to use:

TypeScript
    
    [](<https://adk.dev/agents/models/routing/#__codelineno-0-1>)type LlmRouter = (
    [](<https://adk.dev/agents/models/routing/#__codelineno-0-2>)  models: Readonly<Record<string, BaseLlm>>,
    [](<https://adk.dev/agents/models/routing/#__codelineno-0-3>)  request: LlmRequest,
    [](<https://adk.dev/agents/models/routing/#__codelineno-0-4>)  errorContext?: { failedKeys: ReadonlySet<string>; lastError: unknown },
    [](<https://adk.dev/agents/models/routing/#__codelineno-0-5>)) => Promise<string | undefined> | string | undefined;
    
The `models` parameter accepts either a `Record<string, BaseLlm>` with explicit keys, or an array of `BaseLlm` instances. If an array is provided, each model's name is used as its key.

Failover follows the same rules as [`RoutedAgent`](<https://adk.dev/agents/routing/#how-routing-works>): the router is re-called with `errorContext` only if the selected model fails before yielding any response. After yielding, errors propagate without retry. The router can return `undefined` to stop retrying and propagate the last error.

**Live connections:** `RoutedLlm.connect()` selects the model at connection time. Once a live connection is established, the model cannot be switched mid-stream.

## Basic usage[¶](<https://adk.dev/agents/models/routing/#basic-usage> "Permanent link")

The following example creates a `RoutedLlm` that tries a primary model first and falls back to a secondary model if the primary fails. The router checks `errorContext.failedKeys` to avoid re-selecting the failed model:

TypeScript
    
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-1>)import {
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-2>)  BaseLlm,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-3>)  Gemini,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-4>)  LlmRequest,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-5>)  LlmAgent,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-6>)  RoutedLlm,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-7>)  InMemoryRunner,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-8>)} from '@google/adk';
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-9>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-10>)const primaryModel = new Gemini({ model: 'gemini-flash-latest' });
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-11>)const fallbackModel = new Gemini({ model: 'gemini-pro-latest' });
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-12>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-13>)const router = (
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-14>)  models: Readonly<Record<string, BaseLlm>>,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-15>)  request: LlmRequest,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-16>)  // errorContext is provided when a previously selected model fails
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-17>)  errorContext?: { failedKeys: ReadonlySet<string>; lastError: unknown },
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-18>)) => {
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-19>)  if (!errorContext) {
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-20>)    return 'primary'; // Try primary first
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-21>)  }
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-22>)  if (errorContext.failedKeys.has('primary')) {
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-23>)    return 'fallback'; // Fall back if primary failed
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-24>)  }
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-25>)  return undefined; // No more options, propagate the error
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-26>)};
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-27>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-28>)const routedLlm = new RoutedLlm({
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-29>)  models: { primary: primaryModel, fallback: fallbackModel },
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-30>)  router,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-31>)});
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-32>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-33>)// Use RoutedLlm as the model for an LlmAgent
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-34>)const agent = new LlmAgent({
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-35>)  name: 'my_agent',
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-36>)  model: routedLlm,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-37>)  instruction: 'You are a helpful assistant.',
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-38>)});
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-39>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-40>)const runner = new InMemoryRunner({ agent, appName: 'my_app' });
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-41>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-42>)const session = await runner.sessionService.createSession({
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-43>)  appName: 'my_app',
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-44>)  userId: 'user_1',
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-45>)});
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-46>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-47>)const run = runner.runAsync({
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-48>)  userId: 'user_1',
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-49>)  sessionId: session.id,
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-50>)  newMessage: { role: 'user', parts: [{ text: 'Hello!' }] },
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-51>)});
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-52>)
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-53>)for await (const event of run) {
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-54>)  if (event.content?.parts?.[0]?.text) {
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-55>)    console.log(event.content.parts[0].text);
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-56>)  }
    [](<https://adk.dev/agents/models/routing/#__codelineno-1-57>)}
    
Back to top 