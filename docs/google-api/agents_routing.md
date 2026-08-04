# Agent routing - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/routing/](https://adk.dev/agents/routing/)

[ Skip to content ](<https://adk.dev/agents/routing/#route-between-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/routing.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/routing/index.md> "View this page as Markdown")

# Route between agents[¶](<https://adk.dev/agents/routing/#route-between-agents> "Permanent link")

Supported in ADKTypeScript v1.0.0Experimental

Experimental

Agent routing is experimental and may change in future releases. We welcome your [feedback](<https://github.com/google/adk-js/issues/new?template=feature_request.md>)!

When building agents for different tasks, you can define a routing function that selects which one handles each invocation at runtime. `RoutedAgent` provides this capability, enabling agent fallback on error, A/B testing, planning modes, and auto-routing by input complexity. If the selected agent fails before producing any output, the routing function is called again with error context so it can select a fallback.

`RoutedAgent` is different from [workflow agents](<https://adk.dev/agents/workflow-agents/>) like `SequentialAgent` or `ParallelAgent`, which orchestrate multiple agents in a fixed pattern, and from [LLM-driven delegation](<https://adk.dev/agents/custom-agents/#delegation>), where the LLM decides which agent to hand off to. With `RoutedAgent`, you write an explicit routing function that selects **one** agent per invocation. For model-level routing, see [Model routing](<https://adk.dev/agents/models/routing/>).

## How routing works[¶](<https://adk.dev/agents/routing/#how-routing-works> "Permanent link")

Both `RoutedAgent` and [`RoutedLlm`](<https://adk.dev/agents/models/routing/>) are powered by a shared routing utility that handles selection and failover.

The router function receives the map of available agents and the current context, and returns the key of the agent to run. It can be synchronous or async:

TypeScript
    
    [](<https://adk.dev/agents/routing/#__codelineno-0-1>)type AgentRouter = (
    [](<https://adk.dev/agents/routing/#__codelineno-0-2>)  agents: Readonly<Record<string, BaseAgent>>,
    [](<https://adk.dev/agents/routing/#__codelineno-0-3>)  context: InvocationContext,
    [](<https://adk.dev/agents/routing/#__codelineno-0-4>)  errorContext?: { failedKeys: ReadonlySet<string>; lastError: unknown },
    [](<https://adk.dev/agents/routing/#__codelineno-0-5>)) => Promise<string | undefined> | string | undefined;
    
**The`agents` parameter** accepts either a `Record<string, BaseAgent>` with explicit keys, or an array of agents. If an array is provided, each agent's `name` property is used as its key.

**Failover behavior:**

  * The router is first called without `errorContext` to make the initial selection.
  * If the selected agent throws an error **before yielding any events** , the router is called again with `errorContext` containing `failedKeys` and `lastError`.
  * If the selected agent throws an error **after yielding events** , the error propagates directly without retry, because partial results have already been emitted.
  * A key that has already been tried cannot be re-selected. If the router returns a previously failed key, the error propagates.
  * If the router returns `undefined`, routing stops and the last error is thrown.

## Basic usage[¶](<https://adk.dev/agents/routing/#basic-usage> "Permanent link")

Create multiple agents, define a router function that returns a key, and wrap them in a `RoutedAgent`. The following example routes between two agents based on an external configuration value that can change between invocations:

TypeScript
    
    [](<https://adk.dev/agents/routing/#__codelineno-1-1>)import { LlmAgent, RoutedAgent, InMemoryRunner } from '@google/adk';
    [](<https://adk.dev/agents/routing/#__codelineno-1-2>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-3>)const agentA = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-1-4>)  name: 'agent_a',
    [](<https://adk.dev/agents/routing/#__codelineno-1-5>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-1-6>)  instruction: 'You are Agent A. Always identify yourself as Agent A.',
    [](<https://adk.dev/agents/routing/#__codelineno-1-7>)});
    [](<https://adk.dev/agents/routing/#__codelineno-1-8>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-9>)const agentB = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-1-10>)  name: 'agent_b',
    [](<https://adk.dev/agents/routing/#__codelineno-1-11>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-1-12>)  instruction: 'You are Agent B. Always identify yourself as Agent B.',
    [](<https://adk.dev/agents/routing/#__codelineno-1-13>)});
    [](<https://adk.dev/agents/routing/#__codelineno-1-14>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-15>)// External configuration that can change at runtime
    [](<https://adk.dev/agents/routing/#__codelineno-1-16>)const config = { selectedAgent: 'agent_a' };
    [](<https://adk.dev/agents/routing/#__codelineno-1-17>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-18>)const routedAgent = new RoutedAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-1-19>)  name: 'my_routed_agent',
    [](<https://adk.dev/agents/routing/#__codelineno-1-20>)  agents: { agent_a: agentA, agent_b: agentB },
    [](<https://adk.dev/agents/routing/#__codelineno-1-21>)  router: () => config.selectedAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-1-22>)});
    [](<https://adk.dev/agents/routing/#__codelineno-1-23>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-24>)const runner = new InMemoryRunner({
    [](<https://adk.dev/agents/routing/#__codelineno-1-25>)  agent: routedAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-1-26>)  appName: 'my_app',
    [](<https://adk.dev/agents/routing/#__codelineno-1-27>)});
    [](<https://adk.dev/agents/routing/#__codelineno-1-28>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-29>)const session = await runner.sessionService.createSession({
    [](<https://adk.dev/agents/routing/#__codelineno-1-30>)  appName: 'my_app',
    [](<https://adk.dev/agents/routing/#__codelineno-1-31>)  userId: 'user_1',
    [](<https://adk.dev/agents/routing/#__codelineno-1-32>)});
    [](<https://adk.dev/agents/routing/#__codelineno-1-33>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-34>)const run = runner.runAsync({
    [](<https://adk.dev/agents/routing/#__codelineno-1-35>)  userId: 'user_1',
    [](<https://adk.dev/agents/routing/#__codelineno-1-36>)  sessionId: session.id,
    [](<https://adk.dev/agents/routing/#__codelineno-1-37>)  newMessage: { role: 'user', parts: [{ text: 'Who are you?' }] },
    [](<https://adk.dev/agents/routing/#__codelineno-1-38>)});
    [](<https://adk.dev/agents/routing/#__codelineno-1-39>)
    [](<https://adk.dev/agents/routing/#__codelineno-1-40>)for await (const event of run) {
    [](<https://adk.dev/agents/routing/#__codelineno-1-41>)  if (event.content?.parts?.[0]?.text) {
    [](<https://adk.dev/agents/routing/#__codelineno-1-42>)    console.log(event.content.parts[0].text);
    [](<https://adk.dev/agents/routing/#__codelineno-1-43>)  }
    [](<https://adk.dev/agents/routing/#__codelineno-1-44>)}
    
Change `config.selectedAgent` to `'agent_b'` before the next invocation to route to a different agent.

## Fallback on error[¶](<https://adk.dev/agents/routing/#fallback-on-error> "Permanent link")

When an agent fails, the router is called again with `errorContext` so it can select a fallback. Failover only applies if the agent fails before yielding any events (see [How routing works](<https://adk.dev/agents/routing/#how-routing-works>)). The following example checks `errorContext.failedKeys` to avoid re-selecting the failed agent:

TypeScript
    
    [](<https://adk.dev/agents/routing/#__codelineno-2-1>)import {
    [](<https://adk.dev/agents/routing/#__codelineno-2-2>)  BaseAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-2-3>)  InvocationContext,
    [](<https://adk.dev/agents/routing/#__codelineno-2-4>)  LlmAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-2-5>)  RoutedAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-2-6>)} from '@google/adk';
    [](<https://adk.dev/agents/routing/#__codelineno-2-7>)
    [](<https://adk.dev/agents/routing/#__codelineno-2-8>)const primaryAgent = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-2-9>)  name: 'primary',
    [](<https://adk.dev/agents/routing/#__codelineno-2-10>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-2-11>)  instruction: 'You are the primary agent.',
    [](<https://adk.dev/agents/routing/#__codelineno-2-12>)});
    [](<https://adk.dev/agents/routing/#__codelineno-2-13>)
    [](<https://adk.dev/agents/routing/#__codelineno-2-14>)const fallbackAgent = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-2-15>)  name: 'fallback',
    [](<https://adk.dev/agents/routing/#__codelineno-2-16>)  model: 'gemini-pro-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-2-17>)  instruction: 'You are the fallback agent.',
    [](<https://adk.dev/agents/routing/#__codelineno-2-18>)});
    [](<https://adk.dev/agents/routing/#__codelineno-2-19>)
    [](<https://adk.dev/agents/routing/#__codelineno-2-20>)const router = (
    [](<https://adk.dev/agents/routing/#__codelineno-2-21>)  agents: Readonly<Record<string, BaseAgent>>,
    [](<https://adk.dev/agents/routing/#__codelineno-2-22>)  context: InvocationContext,
    [](<https://adk.dev/agents/routing/#__codelineno-2-23>)  // errorContext is provided when a previously selected agent fails
    [](<https://adk.dev/agents/routing/#__codelineno-2-24>)  errorContext?: { failedKeys: ReadonlySet<string>; lastError: unknown },
    [](<https://adk.dev/agents/routing/#__codelineno-2-25>)) => {
    [](<https://adk.dev/agents/routing/#__codelineno-2-26>)  if (!errorContext) {
    [](<https://adk.dev/agents/routing/#__codelineno-2-27>)    return 'primary'; // Try primary first
    [](<https://adk.dev/agents/routing/#__codelineno-2-28>)  }
    [](<https://adk.dev/agents/routing/#__codelineno-2-29>)  if (errorContext.failedKeys.has('primary')) {
    [](<https://adk.dev/agents/routing/#__codelineno-2-30>)    return 'fallback'; // Fall back if primary failed
    [](<https://adk.dev/agents/routing/#__codelineno-2-31>)  }
    [](<https://adk.dev/agents/routing/#__codelineno-2-32>)  return undefined; // No more options, propagate the error
    [](<https://adk.dev/agents/routing/#__codelineno-2-33>)};
    [](<https://adk.dev/agents/routing/#__codelineno-2-34>)
    [](<https://adk.dev/agents/routing/#__codelineno-2-35>)const routedAgent = new RoutedAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-2-36>)  name: 'my_routed_agent',
    [](<https://adk.dev/agents/routing/#__codelineno-2-37>)  agents: { primary: primaryAgent, fallback: fallbackAgent },
    [](<https://adk.dev/agents/routing/#__codelineno-2-38>)  router,
    [](<https://adk.dev/agents/routing/#__codelineno-2-39>)});
    
## Planning mode[¶](<https://adk.dev/agents/routing/#planning-mode> "Permanent link")

A router can read any external state to select between agents with different instructions, models, and tools. This lets you implement a planning mode where the agent switches behavior dynamically. For example, a basic agent might have read and write tools, while a planning agent is restricted to read-only access and uses a more powerful model for analysis.

The following example shows a different `RoutedAgent` configuration. See [basic usage](<https://adk.dev/agents/routing/#basic-usage>) for the full runner setup.

TypeScript
    
    [](<https://adk.dev/agents/routing/#__codelineno-3-1>)import {
    [](<https://adk.dev/agents/routing/#__codelineno-3-2>)  FunctionTool,
    [](<https://adk.dev/agents/routing/#__codelineno-3-3>)  LlmAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-3-4>)  RoutedAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-3-5>)} from '@google/adk';
    [](<https://adk.dev/agents/routing/#__codelineno-3-6>)import { z } from 'zod';
    [](<https://adk.dev/agents/routing/#__codelineno-3-7>)
    [](<https://adk.dev/agents/routing/#__codelineno-3-8>)const readFileTool = new FunctionTool({
    [](<https://adk.dev/agents/routing/#__codelineno-3-9>)  name: 'read_file',
    [](<https://adk.dev/agents/routing/#__codelineno-3-10>)  description: 'Reads content from a file.',
    [](<https://adk.dev/agents/routing/#__codelineno-3-11>)  parameters: z.object({ filePath: z.string() }),
    [](<https://adk.dev/agents/routing/#__codelineno-3-12>)  execute: (args) => ({ content: `Contents of ${args.filePath}` }),
    [](<https://adk.dev/agents/routing/#__codelineno-3-13>)});
    [](<https://adk.dev/agents/routing/#__codelineno-3-14>)
    [](<https://adk.dev/agents/routing/#__codelineno-3-15>)const writeFileTool = new FunctionTool({
    [](<https://adk.dev/agents/routing/#__codelineno-3-16>)  name: 'write_file',
    [](<https://adk.dev/agents/routing/#__codelineno-3-17>)  description: 'Writes content to a file.',
    [](<https://adk.dev/agents/routing/#__codelineno-3-18>)  parameters: z.object({ filePath: z.string(), content: z.string() }),
    [](<https://adk.dev/agents/routing/#__codelineno-3-19>)  execute: (args) => ({ result: `Wrote to ${args.filePath}` }),
    [](<https://adk.dev/agents/routing/#__codelineno-3-20>)});
    [](<https://adk.dev/agents/routing/#__codelineno-3-21>)
    [](<https://adk.dev/agents/routing/#__codelineno-3-22>)const basicAgent = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-3-23>)  name: 'basic',
    [](<https://adk.dev/agents/routing/#__codelineno-3-24>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-3-25>)  instruction: 'You are a basic assistant. Use tools to help the user.',
    [](<https://adk.dev/agents/routing/#__codelineno-3-26>)  tools: [readFileTool, writeFileTool],
    [](<https://adk.dev/agents/routing/#__codelineno-3-27>)});
    [](<https://adk.dev/agents/routing/#__codelineno-3-28>)
    [](<https://adk.dev/agents/routing/#__codelineno-3-29>)const planningAgent = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-3-30>)  name: 'planning',
    [](<https://adk.dev/agents/routing/#__codelineno-3-31>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-3-32>)  instruction: 'You are a planning expert. Analyze carefully. You can only read files.',
    [](<https://adk.dev/agents/routing/#__codelineno-3-33>)  tools: [readFileTool],
    [](<https://adk.dev/agents/routing/#__codelineno-3-34>)});
    [](<https://adk.dev/agents/routing/#__codelineno-3-35>)
    [](<https://adk.dev/agents/routing/#__codelineno-3-36>)// Toggle this to switch between basic and planning agents
    [](<https://adk.dev/agents/routing/#__codelineno-3-37>)let planningMode = false;
    [](<https://adk.dev/agents/routing/#__codelineno-3-38>)
    [](<https://adk.dev/agents/routing/#__codelineno-3-39>)const routedAgent = new RoutedAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-3-40>)  name: 'my_routed_agent',
    [](<https://adk.dev/agents/routing/#__codelineno-3-41>)  agents: { basic: basicAgent, planning: planningAgent },
    [](<https://adk.dev/agents/routing/#__codelineno-3-42>)  router: () => (planningMode ? 'planning' : 'basic'),
    [](<https://adk.dev/agents/routing/#__codelineno-3-43>)});
    
Set `planningMode = true` before an invocation to route to the planning agent with its restricted tool set and different instructions.

## Auto-routing by complexity[¶](<https://adk.dev/agents/routing/#auto-routing-by-complexity> "Permanent link")

The router function can call a lightweight classifier model to categorize input and route to different agents accordingly. Because the router can be async, you can make LLM calls inside it before selecting an agent.

The following example shows a different `RoutedAgent` configuration. See [basic usage](<https://adk.dev/agents/routing/#basic-usage>) for the full runner setup.

TypeScript
    
    [](<https://adk.dev/agents/routing/#__codelineno-4-1>)import {
    [](<https://adk.dev/agents/routing/#__codelineno-4-2>)  BaseAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-4-3>)  Gemini,
    [](<https://adk.dev/agents/routing/#__codelineno-4-4>)  InvocationContext,
    [](<https://adk.dev/agents/routing/#__codelineno-4-5>)  LlmAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-4-6>)  RoutedAgent,
    [](<https://adk.dev/agents/routing/#__codelineno-4-7>)} from '@google/adk';
    [](<https://adk.dev/agents/routing/#__codelineno-4-8>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-9>)const simpleAgent = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-4-10>)  name: 'simple',
    [](<https://adk.dev/agents/routing/#__codelineno-4-11>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-4-12>)  instruction: 'You are a simple assistant for basic questions.',
    [](<https://adk.dev/agents/routing/#__codelineno-4-13>)});
    [](<https://adk.dev/agents/routing/#__codelineno-4-14>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-15>)const complexAgent = new LlmAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-4-16>)  name: 'complex',
    [](<https://adk.dev/agents/routing/#__codelineno-4-17>)  model: 'gemini-pro-latest',
    [](<https://adk.dev/agents/routing/#__codelineno-4-18>)  instruction: 'You are an expert assistant for complex analysis.',
    [](<https://adk.dev/agents/routing/#__codelineno-4-19>)});
    [](<https://adk.dev/agents/routing/#__codelineno-4-20>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-21>)// Lightweight model to classify input complexity
    [](<https://adk.dev/agents/routing/#__codelineno-4-22>)const classifierModel = new Gemini({ model: 'gemini-flash-latest' });
    [](<https://adk.dev/agents/routing/#__codelineno-4-23>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-24>)const router = async (
    [](<https://adk.dev/agents/routing/#__codelineno-4-25>)  agents: Readonly<Record<string, BaseAgent>>,
    [](<https://adk.dev/agents/routing/#__codelineno-4-26>)  context: InvocationContext,
    [](<https://adk.dev/agents/routing/#__codelineno-4-27>)) => {
    [](<https://adk.dev/agents/routing/#__codelineno-4-28>)  // Extract the user's input text
    [](<https://adk.dev/agents/routing/#__codelineno-4-29>)  const text = context.userContent?.parts?.[0]?.text || '';
    [](<https://adk.dev/agents/routing/#__codelineno-4-30>)  if (!text) return 'simple';
    [](<https://adk.dev/agents/routing/#__codelineno-4-31>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-32>)  const prompt =
    [](<https://adk.dev/agents/routing/#__codelineno-4-33>)    `Classify this request as 'simple' or 'complex'. ` +
    [](<https://adk.dev/agents/routing/#__codelineno-4-34>)    `Reply with ONLY that word.\nRequest: "${text}"`;
    [](<https://adk.dev/agents/routing/#__codelineno-4-35>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-36>)  const generator = classifierModel.generateContentAsync({
    [](<https://adk.dev/agents/routing/#__codelineno-4-37>)    contents: [{ role: 'user', parts: [{ text: prompt }] }],
    [](<https://adk.dev/agents/routing/#__codelineno-4-38>)    toolsDict: {},
    [](<https://adk.dev/agents/routing/#__codelineno-4-39>)    liveConnectConfig: {},
    [](<https://adk.dev/agents/routing/#__codelineno-4-40>)  });
    [](<https://adk.dev/agents/routing/#__codelineno-4-41>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-42>)  let classification = '';
    [](<https://adk.dev/agents/routing/#__codelineno-4-43>)  for await (const resp of generator) {
    [](<https://adk.dev/agents/routing/#__codelineno-4-44>)    if (resp.content?.parts?.[0]?.text) {
    [](<https://adk.dev/agents/routing/#__codelineno-4-45>)      classification += resp.content.parts[0].text;
    [](<https://adk.dev/agents/routing/#__codelineno-4-46>)    }
    [](<https://adk.dev/agents/routing/#__codelineno-4-47>)  }
    [](<https://adk.dev/agents/routing/#__codelineno-4-48>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-49>)  return classification.toLowerCase().includes('complex')
    [](<https://adk.dev/agents/routing/#__codelineno-4-50>)    ? 'complex'
    [](<https://adk.dev/agents/routing/#__codelineno-4-51>)    : 'simple';
    [](<https://adk.dev/agents/routing/#__codelineno-4-52>)};
    [](<https://adk.dev/agents/routing/#__codelineno-4-53>)
    [](<https://adk.dev/agents/routing/#__codelineno-4-54>)const routedAgent = new RoutedAgent({
    [](<https://adk.dev/agents/routing/#__codelineno-4-55>)  name: 'my_routed_agent',
    [](<https://adk.dev/agents/routing/#__codelineno-4-56>)  agents: { simple: simpleAgent, complex: complexAgent },
    [](<https://adk.dev/agents/routing/#__codelineno-4-57>)  router,
    [](<https://adk.dev/agents/routing/#__codelineno-4-58>)});
    
Back to top 