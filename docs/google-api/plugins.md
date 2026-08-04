# Plugins - Agent Development Kit (ADK)

> Source: [https://adk.dev/plugins/](https://adk.dev/plugins/)

[ Skip to content ](<https://adk.dev/plugins/#plugins>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/plugins/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/plugins/index.md> "View this page as Markdown")

# Plugins[¶](<https://adk.dev/plugins/#plugins> "Permanent link")

Supported in ADKPython v1.7.0TypeScript v0.2.5Go v0.4.0Java v0.3.0

A Plugin in Agent Development Kit (ADK) is a custom code module that can be executed at various stages of an agent workflow lifecycle using callback hooks. You use Plugins for functionality that is applicable across your agent workflow. Some typical applications of Plugins are as follows:

  * **Logging and tracing** : Create detailed logs of agent, tool, and generative AI model activity for debugging and performance analysis.
  * **Policy enforcement** : Implement security guardrails, such as a function that checks if users are authorized to use a specific tool and prevent its execution if they do not have permission.
  * **Monitoring and metrics** : Collect and export metrics on token usage, execution times, and invocation counts to monitoring systems such as Prometheus or [Google Cloud Observability](<https://cloud.google.com/stackdriver/docs>) (formerly Stackdriver).
  * **Response caching** : Check if a request has been made before, so you can return a cached response, skipping expensive or time consuming AI model or tool calls.
  * **Request or response modification** : Dynamically add information to AI model prompts or standardize tool output responses.

Tip: Use Plugins for safety features

When implementing security guardrails and policies, use ADK Plugins for better modularity and flexibility than Callbacks. For more details, see [Callbacks and Plugins for Security Guardrails](<https://adk.dev/safety/#callbacks-and-plugins-for-security-guardrails>).

Tip: ADK Integrations

For a list of pre-built plugins and other integrations for ADK, see [Tools and Integrations](<https://adk.dev/integrations/>).

## How do Plugins work?[¶](<https://adk.dev/plugins/#how-do-plugins-work> "Permanent link")

An ADK Plugin extends the `BasePlugin` class and contains one or more `callback` methods, indicating where in the agent lifecycle the Plugin should be executed. You integrate Plugins into an agent by registering them in your agent's `Runner` class. For more information on how and where you can trigger Plugins in your agent application, see [Plugin callback hooks](<https://adk.dev/plugins/#plugin-callback-hooks>).

Plugin functionality builds on [Callbacks](<https://adk.dev/callbacks/>), which is a key design element of the ADK's extensible architecture. While a typical Agent Callback is configured on a _single agent, a single tool_ for a _specific task_ , a Plugin is registered _once_ on the `Runner` and its callbacks apply _globally_ to every agent, tool, and LLM call managed by that runner. Plugins let you package related callback functions together to be used across a workflow. This makes Plugins an ideal solution for implementing features that cut across your entire agent application.

## Prebuilt Plugins[¶](<https://adk.dev/plugins/#prebuilt-plugins> "Permanent link")

ADK includes several plugins that you can add to your agent workflows immediately:

  * [**Reflect and Retry Tools**](<https://adk.dev/integrations/reflect-and-retry/>): Tracks tool failures and intelligently retries tool requests.
  * [**BigQuery Analytics**](<https://adk.dev/integrations/bigquery-agent-analytics/>): Enables agent logging and analysis with BigQuery.
  * [**Context Filter**](<https://github.com/google/adk-python/blob/main/src/google/adk/plugins/context_filter_plugin.py>): Filters the generative AI context to reduce its size.
  * [**Global Instruction**](<https://github.com/google/adk-python/blob/main/src/google/adk/plugins/global_instruction_plugin.py>): Plugin that provides global instructions functionality at the App level.
  * [**Save Files as Artifacts**](<https://github.com/google/adk-python/blob/main/src/google/adk/plugins/save_files_as_artifacts_plugin.py>): Saves files included in user messages as Artifacts.
  * [**Logging**](<https://github.com/google/adk-python/blame/main/src/google/adk/plugins/logging_plugin.py>): Log important information at each agent workflow callback point.

## Define and register Plugins[¶](<https://adk.dev/plugins/#define-and-register-plugins> "Permanent link")

This section explains how to define Plugin classes and register them as part of your agent workflow. For a complete code example, see [Plugin Basic](<https://github.com/google/adk-python/tree/main/contributing/samples/plugin/plugin_basic>) in the repository.

### Create Plugin class[¶](<https://adk.dev/plugins/#create-plugin-class> "Permanent link")

Start by extending the `BasePlugin` class and add one or more `callback` methods, as shown in the following code example:

PythonTypescriptJavaGo

count_plugin.py
    
    [](<https://adk.dev/plugins/#__codelineno-0-1>)from google.adk.agents.base_agent import BaseAgent
    [](<https://adk.dev/plugins/#__codelineno-0-2>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/plugins/#__codelineno-0-3>)from google.adk.models.llm_request import LlmRequest
    [](<https://adk.dev/plugins/#__codelineno-0-4>)from google.adk.plugins.base_plugin import BasePlugin
    [](<https://adk.dev/plugins/#__codelineno-0-5>)
    [](<https://adk.dev/plugins/#__codelineno-0-6>)class CountInvocationPlugin(BasePlugin):
    [](<https://adk.dev/plugins/#__codelineno-0-7>)"""A custom plugin that counts agent and tool invocations."""
    [](<https://adk.dev/plugins/#__codelineno-0-8>)
    [](<https://adk.dev/plugins/#__codelineno-0-9>)def __init__(self) -> None:
    [](<https://adk.dev/plugins/#__codelineno-0-10>)    """Initialize the plugin with counters."""
    [](<https://adk.dev/plugins/#__codelineno-0-11>)    super().__init__(name="count_invocation")
    [](<https://adk.dev/plugins/#__codelineno-0-12>)    self.agent_count: int = 0
    [](<https://adk.dev/plugins/#__codelineno-0-13>)    self.tool_count: int = 0
    [](<https://adk.dev/plugins/#__codelineno-0-14>)    self.llm_request_count: int = 0
    [](<https://adk.dev/plugins/#__codelineno-0-15>)
    [](<https://adk.dev/plugins/#__codelineno-0-16>)async def before_agent_callback(
    [](<https://adk.dev/plugins/#__codelineno-0-17>)    self, *, agent: BaseAgent, callback_context: CallbackContext
    [](<https://adk.dev/plugins/#__codelineno-0-18>)) -> None:
    [](<https://adk.dev/plugins/#__codelineno-0-19>)    """Count agent runs."""
    [](<https://adk.dev/plugins/#__codelineno-0-20>)    self.agent_count += 1
    [](<https://adk.dev/plugins/#__codelineno-0-21>)    print(f"[Plugin] Agent run count: {self.agent_count}")
    [](<https://adk.dev/plugins/#__codelineno-0-22>)
    [](<https://adk.dev/plugins/#__codelineno-0-23>)async def before_model_callback(
    [](<https://adk.dev/plugins/#__codelineno-0-24>)    self, *, callback_context: CallbackContext, llm_request: LlmRequest
    [](<https://adk.dev/plugins/#__codelineno-0-25>)) -> None:
    [](<https://adk.dev/plugins/#__codelineno-0-26>)    """Count LLM requests."""
    [](<https://adk.dev/plugins/#__codelineno-0-27>)    self.llm_request_count += 1
    [](<https://adk.dev/plugins/#__codelineno-0-28>)    print(f"[Plugin] LLM request count: {self.llm_request_count}")
    
count_plugin.ts
    
    [](<https://adk.dev/plugins/#__codelineno-1-1>)import { BaseAgent, BasePlugin, Context } from "@google/adk";
    [](<https://adk.dev/plugins/#__codelineno-1-2>)import type { LlmRequest, LlmResponse } from "@google/adk";
    [](<https://adk.dev/plugins/#__codelineno-1-3>)import type { Content } from "@google/genai";
    [](<https://adk.dev/plugins/#__codelineno-1-4>)
    [](<https://adk.dev/plugins/#__codelineno-1-5>)
    [](<https://adk.dev/plugins/#__codelineno-1-6>)/**
    [](<https://adk.dev/plugins/#__codelineno-1-7>) * A custom plugin that counts agent and tool invocations.
    [](<https://adk.dev/plugins/#__codelineno-1-8>) */
    [](<https://adk.dev/plugins/#__codelineno-1-9>)export class CountInvocationPlugin extends BasePlugin {
    [](<https://adk.dev/plugins/#__codelineno-1-10>)    public agentCount = 0;
    [](<https://adk.dev/plugins/#__codelineno-1-11>)    public toolCount = 0;
    [](<https://adk.dev/plugins/#__codelineno-1-12>)    public llmRequestCount = 0;
    [](<https://adk.dev/plugins/#__codelineno-1-13>)
    [](<https://adk.dev/plugins/#__codelineno-1-14>)    constructor() {
    [](<https://adk.dev/plugins/#__codelineno-1-15>)        super("count_invocation");
    [](<https://adk.dev/plugins/#__codelineno-1-16>)    }
    [](<https://adk.dev/plugins/#__codelineno-1-17>)
    [](<https://adk.dev/plugins/#__codelineno-1-18>)    /**
    [](<https://adk.dev/plugins/#__codelineno-1-19>)     * Count agent runs.
    [](<https://adk.dev/plugins/#__codelineno-1-20>)     */
    [](<https://adk.dev/plugins/#__codelineno-1-21>)    async beforeAgentCallback(
    [](<https://adk.dev/plugins/#__codelineno-1-22>)        agent: BaseAgent,
    [](<https://adk.dev/plugins/#__codelineno-1-23>)        context: Context
    [](<https://adk.dev/plugins/#__codelineno-1-24>)    ): Promise<Content | undefined> {
    [](<https://adk.dev/plugins/#__codelineno-1-25>)        this.agentCount++;
    [](<https://adk.dev/plugins/#__codelineno-1-26>)        console.log(`[Plugin] Agent run count: ${this.agentCount}`);
    [](<https://adk.dev/plugins/#__codelineno-1-27>)        return undefined;
    [](<https://adk.dev/plugins/#__codelineno-1-28>)    }
    [](<https://adk.dev/plugins/#__codelineno-1-29>)
    [](<https://adk.dev/plugins/#__codelineno-1-30>)    /**
    [](<https://adk.dev/plugins/#__codelineno-1-31>)     * Count LLM requests.
    [](<https://adk.dev/plugins/#__codelineno-1-32>)     */
    [](<https://adk.dev/plugins/#__codelineno-1-33>)    async beforeModelCallback(
    [](<https://adk.dev/plugins/#__codelineno-1-34>)        context: Context,
    [](<https://adk.dev/plugins/#__codelineno-1-35>)        llmRequest: LlmRequest
    [](<https://adk.dev/plugins/#__codelineno-1-36>)    ): Promise<LlmResponse | undefined> {
    [](<https://adk.dev/plugins/#__codelineno-1-37>)        this.llmRequestCount++;
    [](<https://adk.dev/plugins/#__codelineno-1-38>)        console.log(`[Plugin] LLM request count: ${this.llmRequestCount}`);
    [](<https://adk.dev/plugins/#__codelineno-1-39>)        return undefined;
    [](<https://adk.dev/plugins/#__codelineno-1-40>)    }
    [](<https://adk.dev/plugins/#__codelineno-1-41>)}
    
CountInvocationPlugin.java
    
    [](<https://adk.dev/plugins/#__codelineno-2-1>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/plugins/#__codelineno-2-2>)import com.google.adk.agents.CallbackContext;
    [](<https://adk.dev/plugins/#__codelineno-2-3>)import com.google.adk.models.LlmRequest;
    [](<https://adk.dev/plugins/#__codelineno-2-4>)import com.google.adk.models.LlmResponse;
    [](<https://adk.dev/plugins/#__codelineno-2-5>)import com.google.adk.plugins.BasePlugin;
    [](<https://adk.dev/plugins/#__codelineno-2-6>)import com.google.genai.types.Content;
    [](<https://adk.dev/plugins/#__codelineno-2-7>)import io.reactivex.rxjava3.core.Maybe;
    [](<https://adk.dev/plugins/#__codelineno-2-8>)
    [](<https://adk.dev/plugins/#__codelineno-2-9>)/** A custom plugin that counts agent and tool invocations. */
    [](<https://adk.dev/plugins/#__codelineno-2-10>)public class CountInvocationPlugin extends BasePlugin {
    [](<https://adk.dev/plugins/#__codelineno-2-11>)  public int agentCount = 0;
    [](<https://adk.dev/plugins/#__codelineno-2-12>)  public int toolCount = 0;
    [](<https://adk.dev/plugins/#__codelineno-2-13>)  public int llmRequestCount = 0;
    [](<https://adk.dev/plugins/#__codelineno-2-14>)
    [](<https://adk.dev/plugins/#__codelineno-2-15>)  public CountInvocationPlugin() {
    [](<https://adk.dev/plugins/#__codelineno-2-16>)    super("count_invocation");
    [](<https://adk.dev/plugins/#__codelineno-2-17>)  }
    [](<https://adk.dev/plugins/#__codelineno-2-18>)
    [](<https://adk.dev/plugins/#__codelineno-2-19>)  /** Count agent runs. */
    [](<https://adk.dev/plugins/#__codelineno-2-20>)  @Override
    [](<https://adk.dev/plugins/#__codelineno-2-21>)  public Maybe<Content> beforeAgentCallback(BaseAgent agent, CallbackContext callbackContext) {
    [](<https://adk.dev/plugins/#__codelineno-2-22>)    agentCount++;
    [](<https://adk.dev/plugins/#__codelineno-2-23>)    System.out.println("[Plugin] Agent run count: " + agentCount);
    [](<https://adk.dev/plugins/#__codelineno-2-24>)    return Maybe.empty();
    [](<https://adk.dev/plugins/#__codelineno-2-25>)  }
    [](<https://adk.dev/plugins/#__codelineno-2-26>)
    [](<https://adk.dev/plugins/#__codelineno-2-27>)  /** Count LLM requests. */
    [](<https://adk.dev/plugins/#__codelineno-2-28>)  @Override
    [](<https://adk.dev/plugins/#__codelineno-2-29>)  public Maybe<LlmResponse> beforeModelCallback(
    [](<https://adk.dev/plugins/#__codelineno-2-30>)      CallbackContext callbackContext, LlmRequest.Builder llmRequest) {
    [](<https://adk.dev/plugins/#__codelineno-2-31>)    llmRequestCount++;
    [](<https://adk.dev/plugins/#__codelineno-2-32>)    System.out.println("[Plugin] LLM request count: " + llmRequestCount);
    [](<https://adk.dev/plugins/#__codelineno-2-33>)    return Maybe.empty();
    [](<https://adk.dev/plugins/#__codelineno-2-34>)  }
    [](<https://adk.dev/plugins/#__codelineno-2-35>)}
    
count_plugin.go
    
    [](<https://adk.dev/plugins/#__codelineno-3-1>)package main
    [](<https://adk.dev/plugins/#__codelineno-3-2>)
    [](<https://adk.dev/plugins/#__codelineno-3-3>)import (
    [](<https://adk.dev/plugins/#__codelineno-3-4>)    "fmt"
    [](<https://adk.dev/plugins/#__codelineno-3-5>)
    [](<https://adk.dev/plugins/#__codelineno-3-6>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/plugins/#__codelineno-3-7>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/plugins/#__codelineno-3-8>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/plugins/#__codelineno-3-9>)    "google.golang.org/adk/v2/plugin"
    [](<https://adk.dev/plugins/#__codelineno-3-10>)    "google.golang.org/genai"
    [](<https://adk.dev/plugins/#__codelineno-3-11>))
    [](<https://adk.dev/plugins/#__codelineno-3-12>)
    [](<https://adk.dev/plugins/#__codelineno-3-13>)/**
    [](<https://adk.dev/plugins/#__codelineno-3-14>) * A custom plugin that counts agent and tool invocations.
    [](<https://adk.dev/plugins/#__codelineno-3-15>) */
    [](<https://adk.dev/plugins/#__codelineno-3-16>)type CountInvocationPlugin struct {
    [](<https://adk.dev/plugins/#__codelineno-3-17>)    AgentCount      int
    [](<https://adk.dev/plugins/#__codelineno-3-18>)    ToolCount       int
    [](<https://adk.dev/plugins/#__codelineno-3-19>)    LlmRequestCount int
    [](<https://adk.dev/plugins/#__codelineno-3-20>)}
    [](<https://adk.dev/plugins/#__codelineno-3-21>)
    [](<https://adk.dev/plugins/#__codelineno-3-22>)func NewCountInvocationPlugin() (*plugin.Plugin, error) {
    [](<https://adk.dev/plugins/#__codelineno-3-23>)    p := &CountInvocationPlugin{}
    [](<https://adk.dev/plugins/#__codelineno-3-24>)    return plugin.New(plugin.Config{
    [](<https://adk.dev/plugins/#__codelineno-3-25>)        Name:                "count_invocation",
    [](<https://adk.dev/plugins/#__codelineno-3-26>)        BeforeAgentCallback: p.BeforeAgentCallback,
    [](<https://adk.dev/plugins/#__codelineno-3-27>)        BeforeModelCallback: p.BeforeModelCallback,
    [](<https://adk.dev/plugins/#__codelineno-3-28>)    })
    [](<https://adk.dev/plugins/#__codelineno-3-29>)}
    [](<https://adk.dev/plugins/#__codelineno-3-30>)
    [](<https://adk.dev/plugins/#__codelineno-3-31>)/**
    [](<https://adk.dev/plugins/#__codelineno-3-32>) * Count agent runs.
    [](<https://adk.dev/plugins/#__codelineno-3-33>) */
    [](<https://adk.dev/plugins/#__codelineno-3-34>)func (p *CountInvocationPlugin) BeforeAgentCallback(ctx agent.CallbackContext) (*genai.Content, error) {
    [](<https://adk.dev/plugins/#__codelineno-3-35>)    p.AgentCount++
    [](<https://adk.dev/plugins/#__codelineno-3-36>)    fmt.Printf("[Plugin] Agent run count: %d\n", p.AgentCount)
    [](<https://adk.dev/plugins/#__codelineno-3-37>)    return nil, nil
    [](<https://adk.dev/plugins/#__codelineno-3-38>)}
    [](<https://adk.dev/plugins/#__codelineno-3-39>)
    [](<https://adk.dev/plugins/#__codelineno-3-40>)/**
    [](<https://adk.dev/plugins/#__codelineno-3-41>) * Count LLM requests.
    [](<https://adk.dev/plugins/#__codelineno-3-42>) */
    [](<https://adk.dev/plugins/#__codelineno-3-43>)func (p *CountInvocationPlugin) BeforeModelCallback(ctx agent.CallbackContext, req *model.LLMRequest) (*model.LLMResponse, error) {
    [](<https://adk.dev/plugins/#__codelineno-3-44>)    p.LlmRequestCount++
    [](<https://adk.dev/plugins/#__codelineno-3-45>)    fmt.Printf("[Plugin] LLM request count: %d\n", p.LlmRequestCount)
    [](<https://adk.dev/plugins/#__codelineno-3-46>)    return nil, nil
    [](<https://adk.dev/plugins/#__codelineno-3-47>)}
    
This example code implements callbacks for `before_agent_callback` and `before_model_callback` to count execution of these tasks during the lifecycle of the agent.

### Register Plugin class[¶](<https://adk.dev/plugins/#register-plugin-class> "Permanent link")

Integrate your Plugin class by registering it during your agent initialization as part of your `Runner` class, using the `plugins` parameter. You can specify multiple Plugins with this parameter. The following code example shows how to register the `CountInvocationPlugin` plugin defined in the previous section with a simple ADK agent.

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-4-1>)from google.adk.runners import InMemoryRunner
    [](<https://adk.dev/plugins/#__codelineno-4-2>)from google.adk import Agent
    [](<https://adk.dev/plugins/#__codelineno-4-3>)from google.adk.tools.tool_context import ToolContext
    [](<https://adk.dev/plugins/#__codelineno-4-4>)from google.genai import types
    [](<https://adk.dev/plugins/#__codelineno-4-5>)import asyncio
    [](<https://adk.dev/plugins/#__codelineno-4-6>)
    [](<https://adk.dev/plugins/#__codelineno-4-7>)# Import the plugin.
    [](<https://adk.dev/plugins/#__codelineno-4-8>)from .count_plugin import CountInvocationPlugin
    [](<https://adk.dev/plugins/#__codelineno-4-9>)
    [](<https://adk.dev/plugins/#__codelineno-4-10>)async def hello_world(tool_context: ToolContext, query: str):
    [](<https://adk.dev/plugins/#__codelineno-4-11>)    print(f'Hello world: query is [{query}]')
    [](<https://adk.dev/plugins/#__codelineno-4-12>)
    [](<https://adk.dev/plugins/#__codelineno-4-13>)    root_agent = Agent(
    [](<https://adk.dev/plugins/#__codelineno-4-14>)        model='gemini-flash-latest',
    [](<https://adk.dev/plugins/#__codelineno-4-15>)        name='hello_world',
    [](<https://adk.dev/plugins/#__codelineno-4-16>)        description='Prints hello world with user query.',
    [](<https://adk.dev/plugins/#__codelineno-4-17>)        instruction="""Use hello_world tool to print hello world and user query.
    [](<https://adk.dev/plugins/#__codelineno-4-18>)        """,
    [](<https://adk.dev/plugins/#__codelineno-4-19>)        tools=[hello_world],
    [](<https://adk.dev/plugins/#__codelineno-4-20>)    )
    [](<https://adk.dev/plugins/#__codelineno-4-21>)
    [](<https://adk.dev/plugins/#__codelineno-4-22>)async def main():
    [](<https://adk.dev/plugins/#__codelineno-4-23>)    """Main entry point for the agent."""
    [](<https://adk.dev/plugins/#__codelineno-4-24>)    prompt = 'hello world'
    [](<https://adk.dev/plugins/#__codelineno-4-25>)    runner = InMemoryRunner(
    [](<https://adk.dev/plugins/#__codelineno-4-26>)        agent=root_agent,
    [](<https://adk.dev/plugins/#__codelineno-4-27>)        app_name='test_app_with_plugin',
    [](<https://adk.dev/plugins/#__codelineno-4-28>)
    [](<https://adk.dev/plugins/#__codelineno-4-29>)        # Add your plugin here. You can add multiple plugins.
    [](<https://adk.dev/plugins/#__codelineno-4-30>)        plugins=[CountInvocationPlugin()],
    [](<https://adk.dev/plugins/#__codelineno-4-31>)    )
    [](<https://adk.dev/plugins/#__codelineno-4-32>)
    [](<https://adk.dev/plugins/#__codelineno-4-33>)    # The rest is the same as starting a regular ADK runner.
    [](<https://adk.dev/plugins/#__codelineno-4-34>)    session = await runner.session_service.create_session(
    [](<https://adk.dev/plugins/#__codelineno-4-35>)        user_id='user',
    [](<https://adk.dev/plugins/#__codelineno-4-36>)        app_name='test_app_with_plugin',
    [](<https://adk.dev/plugins/#__codelineno-4-37>)    )
    [](<https://adk.dev/plugins/#__codelineno-4-38>)
    [](<https://adk.dev/plugins/#__codelineno-4-39>)    async for event in runner.run_async(
    [](<https://adk.dev/plugins/#__codelineno-4-40>)        user_id='user',
    [](<https://adk.dev/plugins/#__codelineno-4-41>)        session_id=session.id,
    [](<https://adk.dev/plugins/#__codelineno-4-42>)        new_message=types.Content(
    [](<https://adk.dev/plugins/#__codelineno-4-43>)            role='user', parts=[types.Part.from_text(text=prompt)]
    [](<https://adk.dev/plugins/#__codelineno-4-44>)        )
    [](<https://adk.dev/plugins/#__codelineno-4-45>)    ):
    [](<https://adk.dev/plugins/#__codelineno-4-46>)        print(f'** Got event from {event.author}')
    [](<https://adk.dev/plugins/#__codelineno-4-47>)
    [](<https://adk.dev/plugins/#__codelineno-4-48>)if __name__ == "__main__":
    [](<https://adk.dev/plugins/#__codelineno-4-49>)    asyncio.run(main())
    
    [](<https://adk.dev/plugins/#__codelineno-5-1>)import { InMemoryRunner, LlmAgent, FunctionTool } from "@google/adk";
    [](<https://adk.dev/plugins/#__codelineno-5-2>)import type { Content } from "@google/genai";
    [](<https://adk.dev/plugins/#__codelineno-5-3>)import { z } from "zod";
    [](<https://adk.dev/plugins/#__codelineno-5-4>)
    [](<https://adk.dev/plugins/#__codelineno-5-5>)// Import the plugin.
    [](<https://adk.dev/plugins/#__codelineno-5-6>)import { CountInvocationPlugin } from "./count_plugin.ts";
    [](<https://adk.dev/plugins/#__codelineno-5-7>)
    [](<https://adk.dev/plugins/#__codelineno-5-8>)const HelloWorldInput = z.object({
    [](<https://adk.dev/plugins/#__codelineno-5-9>)    query: z.string().describe("The query string to print."),
    [](<https://adk.dev/plugins/#__codelineno-5-10>)});
    [](<https://adk.dev/plugins/#__codelineno-5-11>)
    [](<https://adk.dev/plugins/#__codelineno-5-12>)async function helloWorld({ query }: z.infer<typeof HelloWorldInput>): Promise<{ result: string }> {
    [](<https://adk.dev/plugins/#__codelineno-5-13>)    const output = `Hello world: query is [${query}]`;
    [](<https://adk.dev/plugins/#__codelineno-5-14>)    console.log(output);
    [](<https://adk.dev/plugins/#__codelineno-5-15>)    // Tools should return a string or JSON-compatible object
    [](<https://adk.dev/plugins/#__codelineno-5-16>)    return { result: output };
    [](<https://adk.dev/plugins/#__codelineno-5-17>)}
    [](<https://adk.dev/plugins/#__codelineno-5-18>)
    [](<https://adk.dev/plugins/#__codelineno-5-19>)const helloWorldTool = new FunctionTool({
    [](<https://adk.dev/plugins/#__codelineno-5-20>)    name: "hello_world",
    [](<https://adk.dev/plugins/#__codelineno-5-21>)    description: "Prints hello world with user query.",
    [](<https://adk.dev/plugins/#__codelineno-5-22>)    parameters: HelloWorldInput,
    [](<https://adk.dev/plugins/#__codelineno-5-23>)    execute: helloWorld,
    [](<https://adk.dev/plugins/#__codelineno-5-24>)});
    [](<https://adk.dev/plugins/#__codelineno-5-25>)
    [](<https://adk.dev/plugins/#__codelineno-5-26>)const rootAgent = new LlmAgent({
    [](<https://adk.dev/plugins/#__codelineno-5-27>)    model: "gemini-flash-latest", // Preserved from your Python code
    [](<https://adk.dev/plugins/#__codelineno-5-28>)    name: "hello_world",
    [](<https://adk.dev/plugins/#__codelineno-5-29>)    description: "Prints hello world with user query.",
    [](<https://adk.dev/plugins/#__codelineno-5-30>)    instruction: `Use hello_world tool to print hello world and user query.`,
    [](<https://adk.dev/plugins/#__codelineno-5-31>)    tools: [helloWorldTool],
    [](<https://adk.dev/plugins/#__codelineno-5-32>)});
    [](<https://adk.dev/plugins/#__codelineno-5-33>)
    [](<https://adk.dev/plugins/#__codelineno-5-34>)/**
    [](<https://adk.dev/plugins/#__codelineno-5-35>)* Main entry point for the agent.
    [](<https://adk.dev/plugins/#__codelineno-5-36>)*/
    [](<https://adk.dev/plugins/#__codelineno-5-37>)async function main(): Promise<void> {
    [](<https://adk.dev/plugins/#__codelineno-5-38>)    const prompt = "hello world";
    [](<https://adk.dev/plugins/#__codelineno-5-39>)    const runner = new InMemoryRunner({
    [](<https://adk.dev/plugins/#__codelineno-5-40>)        agent: rootAgent,
    [](<https://adk.dev/plugins/#__codelineno-5-41>)        appName: "test_app_with_plugin",
    [](<https://adk.dev/plugins/#__codelineno-5-42>)
    [](<https://adk.dev/plugins/#__codelineno-5-43>)        // Add your plugin here. You can add multiple plugins.
    [](<https://adk.dev/plugins/#__codelineno-5-44>)        plugins: [new CountInvocationPlugin()],
    [](<https://adk.dev/plugins/#__codelineno-5-45>)    });
    [](<https://adk.dev/plugins/#__codelineno-5-46>)
    [](<https://adk.dev/plugins/#__codelineno-5-47>)    // The rest is the same as starting a regular ADK runner.
    [](<https://adk.dev/plugins/#__codelineno-5-48>)    const session = await runner.sessionService.createSession({
    [](<https://adk.dev/plugins/#__codelineno-5-49>)        userId: "user",
    [](<https://adk.dev/plugins/#__codelineno-5-50>)        appName: "test_app_with_plugin",
    [](<https://adk.dev/plugins/#__codelineno-5-51>)    });
    [](<https://adk.dev/plugins/#__codelineno-5-52>)
    [](<https://adk.dev/plugins/#__codelineno-5-53>)    // runAsync returns an async iterable stream in TypeScript
    [](<https://adk.dev/plugins/#__codelineno-5-54>)    const runStream = runner.runAsync({
    [](<https://adk.dev/plugins/#__codelineno-5-55>)        userId: "user",
    [](<https://adk.dev/plugins/#__codelineno-5-56>)        sessionId: session.id,
    [](<https://adk.dev/plugins/#__codelineno-5-57>)        newMessage: {
    [](<https://adk.dev/plugins/#__codelineno-5-58>)        role: "user",
    [](<https://adk.dev/plugins/#__codelineno-5-59>)        parts: [{ text: prompt }],
    [](<https://adk.dev/plugins/#__codelineno-5-60>)        },
    [](<https://adk.dev/plugins/#__codelineno-5-61>)    });
    [](<https://adk.dev/plugins/#__codelineno-5-62>)
    [](<https://adk.dev/plugins/#__codelineno-5-63>)    // Use 'for await...of' to loop through the async stream
    [](<https://adk.dev/plugins/#__codelineno-5-64>)    for await (const event of runStream) {
    [](<https://adk.dev/plugins/#__codelineno-5-65>)        console.log(`** Got event from ${event.author}`);
    [](<https://adk.dev/plugins/#__codelineno-5-66>)    }
    [](<https://adk.dev/plugins/#__codelineno-5-67>)}
    [](<https://adk.dev/plugins/#__codelineno-5-68>)
    [](<https://adk.dev/plugins/#__codelineno-5-69>)main();
    
    [](<https://adk.dev/plugins/#__codelineno-6-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/plugins/#__codelineno-6-2>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/plugins/#__codelineno-6-3>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/plugins/#__codelineno-6-4>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/plugins/#__codelineno-6-5>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/plugins/#__codelineno-6-6>)import com.google.genai.types.Content;
    [](<https://adk.dev/plugins/#__codelineno-6-7>)import com.google.genai.types.Part;
    [](<https://adk.dev/plugins/#__codelineno-6-8>)import java.util.Collections;
    [](<https://adk.dev/plugins/#__codelineno-6-9>)import java.util.List;
    [](<https://adk.dev/plugins/#__codelineno-6-10>)import java.util.Map;
    [](<https://adk.dev/plugins/#__codelineno-6-11>)
    [](<https://adk.dev/plugins/#__codelineno-6-12>)// Import the plugin.
    [](<https://adk.dev/plugins/#__codelineno-6-13>)// import com.example.CountInvocationPlugin;
    [](<https://adk.dev/plugins/#__codelineno-6-14>)
    [](<https://adk.dev/plugins/#__codelineno-6-15>)public class Main {
    [](<https://adk.dev/plugins/#__codelineno-6-16>)
    [](<https://adk.dev/plugins/#__codelineno-6-17>)  public static class HelloTool {
    [](<https://adk.dev/plugins/#__codelineno-6-18>)    @Schema(name = "hello_world", description = "Prints hello world with user query.")
    [](<https://adk.dev/plugins/#__codelineno-6-19>)    public static Map<String, Object> helloWorld(
    [](<https://adk.dev/plugins/#__codelineno-6-20>)        @Schema(name = "query", description = "The query string to print.") String query) {
    [](<https://adk.dev/plugins/#__codelineno-6-21>)      String output = "Hello world: query is [" + query + "]";
    [](<https://adk.dev/plugins/#__codelineno-6-22>)      System.out.println(output);
    [](<https://adk.dev/plugins/#__codelineno-6-23>)      return Map.of("result", output);
    [](<https://adk.dev/plugins/#__codelineno-6-24>)    }
    [](<https://adk.dev/plugins/#__codelineno-6-25>)  }
    [](<https://adk.dev/plugins/#__codelineno-6-26>)
    [](<https://adk.dev/plugins/#__codelineno-6-27>)  public static void main(String[] args) {
    [](<https://adk.dev/plugins/#__codelineno-6-28>)    LlmAgent rootAgent = LlmAgent.builder()
    [](<https://adk.dev/plugins/#__codelineno-6-29>)        .model("gemini-flash-latest")
    [](<https://adk.dev/plugins/#__codelineno-6-30>)        .name("hello_world")
    [](<https://adk.dev/plugins/#__codelineno-6-31>)        .description("Prints hello world with user query.")
    [](<https://adk.dev/plugins/#__codelineno-6-32>)        .instruction("Use hello_world tool to print hello world and user query.")
    [](<https://adk.dev/plugins/#__codelineno-6-33>)        .tools(FunctionTool.create(HelloTool.class, "helloWorld"))
    [](<https://adk.dev/plugins/#__codelineno-6-34>)        .build();
    [](<https://adk.dev/plugins/#__codelineno-6-35>)
    [](<https://adk.dev/plugins/#__codelineno-6-36>)    // Add your plugin here. You can add multiple plugins.
    [](<https://adk.dev/plugins/#__codelineno-6-37>)    InMemoryRunner runner = new InMemoryRunner(
    [](<https://adk.dev/plugins/#__codelineno-6-38>)        rootAgent,
    [](<https://adk.dev/plugins/#__codelineno-6-39>)        "test_app_with_plugin",
    [](<https://adk.dev/plugins/#__codelineno-6-40>)        Collections.singletonList(new CountInvocationPlugin())
    [](<https://adk.dev/plugins/#__codelineno-6-41>)    );
    [](<https://adk.dev/plugins/#__codelineno-6-42>)
    [](<https://adk.dev/plugins/#__codelineno-6-43>)    // The rest is the same as starting a regular ADK runner.
    [](<https://adk.dev/plugins/#__codelineno-6-44>)    Session session = runner.sessionService().createSession(
    [](<https://adk.dev/plugins/#__codelineno-6-45>)        "test_app_with_plugin",
    [](<https://adk.dev/plugins/#__codelineno-6-46>)        "user"
    [](<https://adk.dev/plugins/#__codelineno-6-47>)    ).blockingGet();
    [](<https://adk.dev/plugins/#__codelineno-6-48>)
    [](<https://adk.dev/plugins/#__codelineno-6-49>)    String prompt = "hello world";
    [](<https://adk.dev/plugins/#__codelineno-6-50>)    Content newContent = Content.builder()
    [](<https://adk.dev/plugins/#__codelineno-6-51>)        .role("user")
    [](<https://adk.dev/plugins/#__codelineno-6-52>)        .parts(List.of(Part.builder().text(prompt).build()))
    [](<https://adk.dev/plugins/#__codelineno-6-53>)        .build();
    [](<https://adk.dev/plugins/#__codelineno-6-54>)
    [](<https://adk.dev/plugins/#__codelineno-6-55>)    runner.runAsync(
    [](<https://adk.dev/plugins/#__codelineno-6-56>)        "user",
    [](<https://adk.dev/plugins/#__codelineno-6-57>)        session.id(),
    [](<https://adk.dev/plugins/#__codelineno-6-58>)        newContent
    [](<https://adk.dev/plugins/#__codelineno-6-59>)    ).blockingForEach(event -> {
    [](<https://adk.dev/plugins/#__codelineno-6-60>)         if (event.author() != null) {
    [](<https://adk.dev/plugins/#__codelineno-6-61>)            System.out.println("** Got event from " + event.author());
    [](<https://adk.dev/plugins/#__codelineno-6-62>)        }
    [](<https://adk.dev/plugins/#__codelineno-6-63>)    });
    [](<https://adk.dev/plugins/#__codelineno-6-64>)  }
    [](<https://adk.dev/plugins/#__codelineno-6-65>)}
    
    [](<https://adk.dev/plugins/#__codelineno-7-1>)package main
    [](<https://adk.dev/plugins/#__codelineno-7-2>)
    [](<https://adk.dev/plugins/#__codelineno-7-3>)import (
    [](<https://adk.dev/plugins/#__codelineno-7-4>)    "context"
    [](<https://adk.dev/plugins/#__codelineno-7-5>)    "fmt"
    [](<https://adk.dev/plugins/#__codelineno-7-6>)    "log"
    [](<https://adk.dev/plugins/#__codelineno-7-7>)
    [](<https://adk.dev/plugins/#__codelineno-7-8>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/plugins/#__codelineno-7-9>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/plugins/#__codelineno-7-10>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/plugins/#__codelineno-7-11>)    "google.golang.org/adk/v2/plugin"
    [](<https://adk.dev/plugins/#__codelineno-7-12>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/plugins/#__codelineno-7-13>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/plugins/#__codelineno-7-14>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/plugins/#__codelineno-7-15>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/plugins/#__codelineno-7-16>)    "google.golang.org/genai"
    [](<https://adk.dev/plugins/#__codelineno-7-17>))
    [](<https://adk.dev/plugins/#__codelineno-7-18>)
    [](<https://adk.dev/plugins/#__codelineno-7-19>)type helloWorldArgs struct {
    [](<https://adk.dev/plugins/#__codelineno-7-20>)    Query string `json:"query"`
    [](<https://adk.dev/plugins/#__codelineno-7-21>)}
    [](<https://adk.dev/plugins/#__codelineno-7-22>)
    [](<https://adk.dev/plugins/#__codelineno-7-23>)type helloWorldResult struct {
    [](<https://adk.dev/plugins/#__codelineno-7-24>)    Result string `json:"result"`
    [](<https://adk.dev/plugins/#__codelineno-7-25>)}
    [](<https://adk.dev/plugins/#__codelineno-7-26>)
    [](<https://adk.dev/plugins/#__codelineno-7-27>)func helloWorld(ctx tool.Context, args helloWorldArgs) (helloWorldResult, error) {
    [](<https://adk.dev/plugins/#__codelineno-7-28>)    output := fmt.Sprintf("Hello world: query is [%s]", args.Query)
    [](<https://adk.dev/plugins/#__codelineno-7-29>)    fmt.Println(output)
    [](<https://adk.dev/plugins/#__codelineno-7-30>)    return helloWorldResult{Result: output}, nil
    [](<https://adk.dev/plugins/#__codelineno-7-31>)}
    [](<https://adk.dev/plugins/#__codelineno-7-32>)
    [](<https://adk.dev/plugins/#__codelineno-7-33>)func main() {
    [](<https://adk.dev/plugins/#__codelineno-7-34>)    ctx := context.Background()
    [](<https://adk.dev/plugins/#__codelineno-7-35>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/plugins/#__codelineno-7-36>)    if err != nil {
    [](<https://adk.dev/plugins/#__codelineno-7-37>)        log.Fatalf("failed to create model: %v", err)
    [](<https://adk.dev/plugins/#__codelineno-7-38>)    }
    [](<https://adk.dev/plugins/#__codelineno-7-39>)
    [](<https://adk.dev/plugins/#__codelineno-7-40>)    helloWorldTool, err := functiontool.New(functiontool.Config{
    [](<https://adk.dev/plugins/#__codelineno-7-41>)        Name:        "hello_world",
    [](<https://adk.dev/plugins/#__codelineno-7-42>)        Description: "Prints hello world with user query.",
    [](<https://adk.dev/plugins/#__codelineno-7-43>)    }, helloWorld)
    [](<https://adk.dev/plugins/#__codelineno-7-44>)    if err != nil {
    [](<https://adk.dev/plugins/#__codelineno-7-45>)        log.Fatalf("failed to create tool: %v", err)
    [](<https://adk.dev/plugins/#__codelineno-7-46>)    }
    [](<https://adk.dev/plugins/#__codelineno-7-47>)
    [](<https://adk.dev/plugins/#__codelineno-7-48>)    rootAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/plugins/#__codelineno-7-49>)        Model:       model,
    [](<https://adk.dev/plugins/#__codelineno-7-50>)        Name:        "hello_world",
    [](<https://adk.dev/plugins/#__codelineno-7-51>)        Description: "Prints hello world with user query.",
    [](<https://adk.dev/plugins/#__codelineno-7-52>)        Instruction: "Use hello_world tool to print hello world and user query.",
    [](<https://adk.dev/plugins/#__codelineno-7-53>)        Tools:       []tool.Tool{helloWorldTool},
    [](<https://adk.dev/plugins/#__codelineno-7-54>)    })
    [](<https://adk.dev/plugins/#__codelineno-7-55>)    if err != nil {
    [](<https://adk.dev/plugins/#__codelineno-7-56>)        log.Fatalf("failed to create agent: %v", err)
    [](<https://adk.dev/plugins/#__codelineno-7-57>)    }
    [](<https://adk.dev/plugins/#__codelineno-7-58>)
    [](<https://adk.dev/plugins/#__codelineno-7-59>)    // Create your plugin.
    [](<https://adk.dev/plugins/#__codelineno-7-60>)    countPlugin, err := NewCountInvocationPlugin()
    [](<https://adk.dev/plugins/#__codelineno-7-61>)    if err != nil {
    [](<https://adk.dev/plugins/#__codelineno-7-62>)        log.Fatalf("failed to create plugin: %v", err)
    [](<https://adk.dev/plugins/#__codelineno-7-63>)    }
    [](<https://adk.dev/plugins/#__codelineno-7-64>)
    [](<https://adk.dev/plugins/#__codelineno-7-65>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/plugins/#__codelineno-7-66>)    // Add your plugin here. You can add multiple plugins.
    [](<https://adk.dev/plugins/#__codelineno-7-67>)    r, err := runner.New(runner.Config{
    [](<https://adk.dev/plugins/#__codelineno-7-68>)        AppName:        "test_app_with_plugin",
    [](<https://adk.dev/plugins/#__codelineno-7-69>)        Agent:          rootAgent,
    [](<https://adk.dev/plugins/#__codelineno-7-70>)        SessionService: sessionService,
    [](<https://adk.dev/plugins/#__codelineno-7-71>)        PluginConfig: runner.PluginConfig{
    [](<https://adk.dev/plugins/#__codelineno-7-72>)            Plugins: []*plugin.Plugin{countPlugin},
    [](<https://adk.dev/plugins/#__codelineno-7-73>)        },
    [](<https://adk.dev/plugins/#__codelineno-7-74>)    })
    [](<https://adk.dev/plugins/#__codelineno-7-75>)    if err != nil {
    [](<https://adk.dev/plugins/#__codelineno-7-76>)        log.Fatalf("failed to create runner: %v", err)
    [](<https://adk.dev/plugins/#__codelineno-7-77>)    }
    [](<https://adk.dev/plugins/#__codelineno-7-78>)
    [](<https://adk.dev/plugins/#__codelineno-7-79>)    // The rest is the same as starting a regular ADK runner.
    [](<https://adk.dev/plugins/#__codelineno-7-80>)    sessResp, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/plugins/#__codelineno-7-81>)        AppName: "test_app_with_plugin",
    [](<https://adk.dev/plugins/#__codelineno-7-82>)        UserID:  "user",
    [](<https://adk.dev/plugins/#__codelineno-7-83>)    })
    [](<https://adk.dev/plugins/#__codelineno-7-84>)    if err != nil {
    [](<https://adk.dev/plugins/#__codelineno-7-85>)        log.Fatalf("failed to create session: %v", err)
    [](<https://adk.dev/plugins/#__codelineno-7-86>)    }
    [](<https://adk.dev/plugins/#__codelineno-7-87>)    sess := sessResp.Session
    [](<https://adk.dev/plugins/#__codelineno-7-88>)
    [](<https://adk.dev/plugins/#__codelineno-7-89>)    prompt := "hello world"
    [](<https://adk.dev/plugins/#__codelineno-7-90>)    input := genai.NewContentFromText(prompt, genai.RoleUser)
    [](<https://adk.dev/plugins/#__codelineno-7-91>)
    [](<https://adk.dev/plugins/#__codelineno-7-92>)    for event, err := range r.Run(ctx, "user", sess.ID(), input, agent.RunConfig{}) {
    [](<https://adk.dev/plugins/#__codelineno-7-93>)        if err != nil {
    [](<https://adk.dev/plugins/#__codelineno-7-94>)            log.Printf("AGENT_ERROR: %v", err)
    [](<https://adk.dev/plugins/#__codelineno-7-95>)            continue
    [](<https://adk.dev/plugins/#__codelineno-7-96>)        }
    [](<https://adk.dev/plugins/#__codelineno-7-97>)        if event.Author != "" {
    [](<https://adk.dev/plugins/#__codelineno-7-98>)            fmt.Printf("** Got event from %s\n", event.Author)
    [](<https://adk.dev/plugins/#__codelineno-7-99>)        }
    [](<https://adk.dev/plugins/#__codelineno-7-100>)    }
    [](<https://adk.dev/plugins/#__codelineno-7-101>)}
    
### Run the agent with the Plugin[¶](<https://adk.dev/plugins/#run-the-agent-with-the-plugin> "Permanent link")

Run the plugin as you typically would. The following shows how to run the command line:

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-8-1>)python3 -m path.to.main.py
    
    [](<https://adk.dev/plugins/#__codelineno-9-1>)npx ts-node path.to.main.ts
    
    [](<https://adk.dev/plugins/#__codelineno-10-1>)./mvnw -q clean compile exec:java -Dexec.mainClass="com.example.Main"
    
    [](<https://adk.dev/plugins/#__codelineno-11-1>)go run path/to/main.go
    
The output of this previously described agent should look similar to the following:
    
    [](<https://adk.dev/plugins/#__codelineno-12-1>)[Plugin] Agent run count: 1
    [](<https://adk.dev/plugins/#__codelineno-12-2>)[Plugin] LLM request count: 1
    [](<https://adk.dev/plugins/#__codelineno-12-3>)** Got event from hello_world
    [](<https://adk.dev/plugins/#__codelineno-12-4>)Hello world: query is [hello world]
    [](<https://adk.dev/plugins/#__codelineno-12-5>)** Got event from hello_world
    [](<https://adk.dev/plugins/#__codelineno-12-6>)[Plugin] LLM request count: 2
    [](<https://adk.dev/plugins/#__codelineno-12-7>)** Got event from hello_world
    
For more information on running ADK agents, see the [Agent Runtime](<https://adk.dev/runtime/#ways-to-run-agents>) guides.

## Build workflows with Plugins[¶](<https://adk.dev/plugins/#build-workflows-with-plugins> "Permanent link")

Plugin callback hooks are a mechanism for implementing logic that intercepts, modifies, and even controls the agent's execution lifecycle. Each hook is a specific method in your Plugin class that you can implement to run code at a key moment. You have a choice between two modes of operation based on your hook's return value:

  * **To Observe:** Implement a hook with no return value (`None`). This approach is for tasks such as logging or collecting metrics, as it allows the agent's workflow to proceed to the next step without interruption. For example, you could use `after_tool_callback` in a Plugin to log every tool's result for debugging.
  * **To Intervene:** Implement a hook and return a value. This approach short-circuits the workflow. The `Runner` halts processing, skips any subsequent plugins and the original intended action, like a Model call, and use a Plugin callback's return value as the result. A common use case is implementing `before_model_callback` to return a cached `LlmResponse`, preventing a redundant and costly API call.
  * **To Amend:** Implement a hook and modify the Context object. This approach allows you to modify the context data for the module to be executed without otherwise interrupting the execution of that module. For example, adding additional, standardized prompt text for Model object execution.

**Caution:** Plugin callback functions have precedence over callbacks implemented at the object level. This behavior means that Any Plugin callbacks code is executed _before_ any Agent, Model, or Tool objects callbacks are executed. Furthermore, if a Plugin-level agent callback returns any value, and not an empty (`None`) response, the Agent, Model, or Tool-level callback is _not executed_ (skipped).

The Plugin design establishes a hierarchy of code execution and separates global concerns from local agent logic. A Plugin is the stateful _module_ you build, such as `PerformanceMonitoringPlugin`, while the callback hooks are the specific _functions_ within that module that get executed. This architecture differs fundamentally from standard Agent Callbacks in these critical ways:

  * **Scope:** Plugin hooks are _global_. You register a Plugin once on the `Runner`, and its hooks apply universally to every Agent, Model, and Tool it manages. In contrast, Agent Callbacks are _local_ , configured individually on a specific agent instance.
  * **Execution Order:** Plugins have _precedence_. For any given event, the Plugin hooks always run before any corresponding Agent Callback. This system behavior makes Plugins the correct architectural choice for implementing cross-cutting features like security policies, universal caching, and consistent logging across your entire application.

### Agent Callbacks and Plugins[¶](<https://adk.dev/plugins/#agent-callbacks-and-plugins> "Permanent link")

As mentioned in the previous section, there are some functional similarities between Plugins and Agent Callbacks. The following table compares the differences between Plugins and Agent Callbacks in more detail.

| **Plugins** | **Agent Callbacks**  
---|---|---  
**Scope** | **Global** : Apply to all agents/tools/LLMs in the `Runner`. | **Local** : Apply only to the specific agent instance they are configured on.  
**Primary Use Case** | **Horizontal Features** : Logging, policy, monitoring, global caching. | **Specific Agent Logic** : Modifying the behavior or state of a single agent.  
**Configuration** | Configure once on the `Runner`. | Configure individually on each `BaseAgent` instance.  
**Execution Order** | Plugin callbacks run **before** Agent Callbacks. | Agent callbacks run **after** Plugin callbacks.  
  
## Plugin callback hooks[¶](<https://adk.dev/plugins/#plugin-callback-hooks> "Permanent link")

You define when a Plugin is called with the callback functions to define in your Plugin class. Callbacks are available when a user message is received, before and after an `Runner`, `Agent`, `Model`, or `Tool` is called, for `Events`, and when a `Model`, or `Tool` error occurs. These callbacks include, and take precedence over, the any callbacks defined within your Agent, Model, and Tool classes.

The following diagram illustrates callback points where you can attach and run Plugin functionality during your agents workflow:

![ADK Plugin callback hooks](https://adk.dev/assets/workflow-plugin-hooks.svg) **Figure 1.** Diagram of ADK agent workflow with Plugin callback hook locations.

The following sections describe the available callback hooks for Plugins in more detail.

  * [User Message callbacks](<https://adk.dev/plugins/#user-message-callbacks>)
  * [Runner start callbacks](<https://adk.dev/plugins/#runner-start-callbacks>)
  * [Agent execution callbacks](<https://adk.dev/plugins/#agent-execution-callbacks>)
  * [Model callbacks](<https://adk.dev/plugins/#model-callbacks>)
  * [Tool callbacks](<https://adk.dev/plugins/#tool-callbacks>)
  * [Runner end callbacks](<https://adk.dev/plugins/#runner-end-callbacks>)

### User Message callbacks[¶](<https://adk.dev/plugins/#user-message-callbacks> "Permanent link")

_A User Message c_ allback (`on_user_message_callback`) happens when a user sends a message. The `on_user_message_callback` is the very first hook to run, giving you a chance to inspect or modify the initial input.\

  * **When It Runs:** This callback happens immediately after `runner.run()`, before any other processing.
  * **Purpose:** The first opportunity to inspect or modify the user's raw input.
  * **Flow Control:** Returns a `types.Content` object to **replace** the user's original message.

The following code example shows the basic syntax of this callback:

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-13-1>)async def on_user_message_callback(
    [](<https://adk.dev/plugins/#__codelineno-13-2>)    self,
    [](<https://adk.dev/plugins/#__codelineno-13-3>)    *,
    [](<https://adk.dev/plugins/#__codelineno-13-4>)    invocation_context: InvocationContext,
    [](<https://adk.dev/plugins/#__codelineno-13-5>)    user_message: types.Content,
    [](<https://adk.dev/plugins/#__codelineno-13-6>)) -> Optional[types.Content]:
    
    [](<https://adk.dev/plugins/#__codelineno-14-1>)async onUserMessageCallback(
    [](<https://adk.dev/plugins/#__codelineno-14-2>)    invocationContext: InvocationContext,
    [](<https://adk.dev/plugins/#__codelineno-14-3>)    user_message: Content
    [](<https://adk.dev/plugins/#__codelineno-14-4>)): Promise<Content | undefined> {
    [](<https://adk.dev/plugins/#__codelineno-14-5>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-14-6>)}
    
    [](<https://adk.dev/plugins/#__codelineno-15-1>)@Override
    [](<https://adk.dev/plugins/#__codelineno-15-2>)public Maybe<Content> onUserMessageCallback(
    [](<https://adk.dev/plugins/#__codelineno-15-3>)  InvocationContext invocationContext, Content userMessage) {
    [](<https://adk.dev/plugins/#__codelineno-15-4>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-15-5>)  return Maybe.empty();
    [](<https://adk.dev/plugins/#__codelineno-15-6>)}
    
    [](<https://adk.dev/plugins/#__codelineno-16-1>)func (p *MyPlugin) OnUserMessageCallback(ctx agent.InvocationContext, msg *genai.Content) (*genai.Content, error) {
    [](<https://adk.dev/plugins/#__codelineno-16-2>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-16-3>)  return nil, nil
    [](<https://adk.dev/plugins/#__codelineno-16-4>)}
    
### Runner start callbacks[¶](<https://adk.dev/plugins/#runner-start-callbacks> "Permanent link")

A _Runner start_ callback (`before_run_callback`) happens when the `Runner` object takes the potentially modified user message and prepares for execution. The `before_run_callback` fires here, allowing for global setup before any agent logic begins.

  * **When It Runs:** After the `on_user_message_callback`, when the `Runner` prepares for execution and before any agent logic begins.
  * **Purpose:** Global setup or initialization before the invocation runs.
  * **Flow Control:** Return a `types.Content` object to **halt execution** : the `Runner` exits early and ends the run with that content as the result. Return `None` to proceed normally.

The following code example shows the basic syntax of this callback:

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-17-1>)async def before_run_callback(
    [](<https://adk.dev/plugins/#__codelineno-17-2>)    self, *, invocation_context: InvocationContext
    [](<https://adk.dev/plugins/#__codelineno-17-3>)) -> Optional[types.Content]:
    
    [](<https://adk.dev/plugins/#__codelineno-18-1>)async beforeRunCallback(invocationContext: InvocationContext): Promise<Content | undefined> {
    [](<https://adk.dev/plugins/#__codelineno-18-2>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-18-3>)}
    
    [](<https://adk.dev/plugins/#__codelineno-19-1>)@Override
    [](<https://adk.dev/plugins/#__codelineno-19-2>)public Maybe<Content> beforeRunCallback(InvocationContext invocationContext) {
    [](<https://adk.dev/plugins/#__codelineno-19-3>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-19-4>)  return Maybe.empty();
    [](<https://adk.dev/plugins/#__codelineno-19-5>)}
    
    [](<https://adk.dev/plugins/#__codelineno-20-1>)func (p *MyPlugin) BeforeRunCallback(ctx agent.InvocationContext) (*genai.Content, error) {
    [](<https://adk.dev/plugins/#__codelineno-20-2>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-20-3>)  return nil, nil
    [](<https://adk.dev/plugins/#__codelineno-20-4>)}
    
### Agent execution callbacks[¶](<https://adk.dev/plugins/#agent-execution-callbacks> "Permanent link")

_Agent execution_ callbacks (`before_agent`, `after_agent`) happen when a `Runner` object invokes an agent. The `before_agent_callback` runs immediately before the agent's main work begins. The main work encompasses the agent's entire process for handling the request, which could involve calling models or tools. After the agent has finished all its steps and prepared a result, the `after_agent_callback` runs.

**Caution:** Plugins that implement these callbacks are executed _before_ the Agent-level callbacks are executed. Furthermore, if a Plugin-level agent callback returns anything other than a `None` or null response, the Agent-level callback is _not executed_ (skipped).

For more information about Agent callbacks defined as part of an Agent object, see [Types of Callbacks](<https://adk.dev/callbacks/types-of-callbacks/#agent-lifecycle-callbacks>).

### Model callbacks[¶](<https://adk.dev/plugins/#model-callbacks> "Permanent link")

Model callbacks **(`before_model`, `after_model`, `on_model_error`)** happen before and after a Model object executes. The Plugins feature also supports a callback in the event of an error, as detailed below:

  * If an agent needs to call an AI model, `before_model_callback` runs first.
  * If the model call is successful, `after_model_callback` runs next.
  * If the model call fails with an exception, the `on_model_error_callback` is triggered instead, allowing for graceful recovery.

**Caution:** Plugins that implement the **`before_model`** and `**after_model` __callback methods are executed_ before_ the Model-level callbacks are executed. Furthermore, if a Plugin-level model callback returns anything other than a `None` or null response, the Model-level callback is _not executed_ (skipped).

#### Model on error callback details[¶](<https://adk.dev/plugins/#model-on-error-callback-details> "Permanent link")

The on error callback for Model objects is only supported by the Plugins feature works as follows:

  * **When It Runs:** When an exception is raised during the model call.
  * **Common Use Cases:** Graceful error handling, logging the specific error, or returning a fallback response, such as "The AI service is currently unavailable."
  * **Flow Control:**
    * Returns an `LlmResponse` object to **suppress the exception** and provide a fallback result.
    * Returns `None` to allow the original exception to be raised.

**Note** : If the execution of the Model object returns a `LlmResponse`, the system resumes the execution flow, and `after_model_callback` will be triggered normally.****

The following code example shows the basic syntax of this callback:

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-21-1>)async def on_model_error_callback(
    [](<https://adk.dev/plugins/#__codelineno-21-2>)    self,
    [](<https://adk.dev/plugins/#__codelineno-21-3>)    *,
    [](<https://adk.dev/plugins/#__codelineno-21-4>)    callback_context: CallbackContext,
    [](<https://adk.dev/plugins/#__codelineno-21-5>)    llm_request: LlmRequest,
    [](<https://adk.dev/plugins/#__codelineno-21-6>)    error: Exception,
    [](<https://adk.dev/plugins/#__codelineno-21-7>)) -> Optional[LlmResponse]:
    
    [](<https://adk.dev/plugins/#__codelineno-22-1>)async onModelErrorCallback(
    [](<https://adk.dev/plugins/#__codelineno-22-2>)    context: Context,
    [](<https://adk.dev/plugins/#__codelineno-22-3>)    llmRequest: LlmRequest,
    [](<https://adk.dev/plugins/#__codelineno-22-4>)    error: Error
    [](<https://adk.dev/plugins/#__codelineno-22-5>)): Promise<LlmResponse | undefined> {
    [](<https://adk.dev/plugins/#__codelineno-22-6>)    // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-22-7>)}
    
    [](<https://adk.dev/plugins/#__codelineno-23-1>)@Override
    [](<https://adk.dev/plugins/#__codelineno-23-2>)public Maybe<LlmResponse> onModelErrorCallback(
    [](<https://adk.dev/plugins/#__codelineno-23-3>)  CallbackContext callbackContext, LlmRequest.Builder llmRequest, Throwable error) {
    [](<https://adk.dev/plugins/#__codelineno-23-4>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-23-5>)  return Maybe.empty();
    [](<https://adk.dev/plugins/#__codelineno-23-6>)}
    
    [](<https://adk.dev/plugins/#__codelineno-24-1>)func (p *MyPlugin) OnModelErrorCallback(ctx agent.CallbackContext, req *model.LLMRequest, err error) (*model.LLMResponse, error) {
    [](<https://adk.dev/plugins/#__codelineno-24-2>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-24-3>)  return nil, nil
    [](<https://adk.dev/plugins/#__codelineno-24-4>)}
    
### Tool callbacks[¶](<https://adk.dev/plugins/#tool-callbacks> "Permanent link")

Tool callbacks **(`before_tool`, `after_tool`, `on_tool_error`)** for Plugins happen before or after the execution of a tool, or when an error occurs. The Plugins feature also supports a callback in the event of an error, as detailed below:\

  * When an agent executes a Tool, `before_tool_callback` runs first.
  * If the tool executes successfully, `after_tool_callback` runs next.
  * If the tool raises an exception, the `on_tool_error_callback` is triggered instead, giving you a chance to handle the failure. If `on_tool_error_callback` returns a dict, `after_tool_callback` will be triggered normally.

**Caution:** Plugins that implement these callbacks are executed _before_ the Tool-level callbacks are executed. Furthermore, if a Plugin-level tool callback returns anything other than a `None` or null response, the Tool-level callback is _not executed_ (skipped).

#### Tool on error callback details[¶](<https://adk.dev/plugins/#tool-on-error-callback-details> "Permanent link")

The on error callback for Tool objects is only supported by the Plugins feature works as follows:

  * **When It Runs:** When an exception is raised during the execution of a tool's `run` method.
  * **Purpose:** Catching specific tool exceptions (like `APIError`), logging the failure, and providing a user-friendly error message back to the LLM.
  * **Flow Control:** Return a `dict` to **suppress the exception** , provide a fallback result. Return `None` to allow the original exception to be raised.

**Note** : By returning a `dict`, this resumes the execution flow, and `after_tool_callback` will be triggered normally.

The following code example shows the basic syntax of this callback:

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-25-1>)async def on_tool_error_callback(
    [](<https://adk.dev/plugins/#__codelineno-25-2>)    self,
    [](<https://adk.dev/plugins/#__codelineno-25-3>)    *,
    [](<https://adk.dev/plugins/#__codelineno-25-4>)    tool: BaseTool,
    [](<https://adk.dev/plugins/#__codelineno-25-5>)    tool_args: dict[str, Any],
    [](<https://adk.dev/plugins/#__codelineno-25-6>)    tool_context: ToolContext,
    [](<https://adk.dev/plugins/#__codelineno-25-7>)    error: Exception,
    [](<https://adk.dev/plugins/#__codelineno-25-8>)) -> Optional[dict]:
    
    [](<https://adk.dev/plugins/#__codelineno-26-1>)async onToolErrorCallback(
    [](<https://adk.dev/plugins/#__codelineno-26-2>)    tool: BaseTool,
    [](<https://adk.dev/plugins/#__codelineno-26-3>)    toolArgs: { [key: string]: any },
    [](<https://adk.dev/plugins/#__codelineno-26-4>)    context: Context,
    [](<https://adk.dev/plugins/#__codelineno-26-5>)    error: Error
    [](<https://adk.dev/plugins/#__codelineno-26-6>)): Promise<{ [key:string]: any } | undefined> {
    [](<https://adk.dev/plugins/#__codelineno-26-7>)    // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-26-8>)}
    
    [](<https://adk.dev/plugins/#__codelineno-27-1>)@Override
    [](<https://adk.dev/plugins/#__codelineno-27-2>)public Maybe<Map<String, Object>> onToolErrorCallback(
    [](<https://adk.dev/plugins/#__codelineno-27-3>)  BaseTool tool, Map<String, Object> toolArgs, ToolContext toolContext, Throwable error) {
    [](<https://adk.dev/plugins/#__codelineno-27-4>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-27-5>)  return Maybe.empty();
    [](<https://adk.dev/plugins/#__codelineno-27-6>)}
    
    [](<https://adk.dev/plugins/#__codelineno-28-1>)func (p *MyPlugin) OnToolErrorCallback(ctx tool.Context, t tool.Tool, args map[string]any, err error) (map[string]any, error) {
    [](<https://adk.dev/plugins/#__codelineno-28-2>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-28-3>)  return nil, nil
    [](<https://adk.dev/plugins/#__codelineno-28-4>)}
    
### Event callbacks[¶](<https://adk.dev/plugins/#event-callbacks> "Permanent link")

An _Event callback_ (`on_event_callback`) happens when an agent produces outputs such as a text response or a tool call result, it yields them as `Event` objects. The `on_event_callback` fires for each event, allowing you to modify it before it's streamed to the client.

  * **When It Runs:** After an agent yields an `Event` but before it's sent to the user. An agent's run may produce multiple events.
  * **Purpose:** Useful for modifying or enriching events (e.g., adding metadata) or for triggering side effects based on specific events.
  * **Flow Control:** Return an `Event` object to **replace** the original event.

The following code example shows the basic syntax of this callback:

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-29-1>)async def on_event_callback(
    [](<https://adk.dev/plugins/#__codelineno-29-2>)    self, *, invocation_context: InvocationContext, event: Event
    [](<https://adk.dev/plugins/#__codelineno-29-3>)) -> Optional[Event]:
    
    [](<https://adk.dev/plugins/#__codelineno-30-1>)async onEventCallback(
    [](<https://adk.dev/plugins/#__codelineno-30-2>)    invocationContext: InvocationContext,
    [](<https://adk.dev/plugins/#__codelineno-30-3>)    event: Event
    [](<https://adk.dev/plugins/#__codelineno-30-4>)): Promise<Event | undefined> {
    [](<https://adk.dev/plugins/#__codelineno-30-5>)    // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-30-6>)}
    
    [](<https://adk.dev/plugins/#__codelineno-31-1>)@Override
    [](<https://adk.dev/plugins/#__codelineno-31-2>)public Maybe<Event> onEventCallback(InvocationContext invocationContext, Event event) {
    [](<https://adk.dev/plugins/#__codelineno-31-3>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-31-4>)  return Maybe.empty();
    [](<https://adk.dev/plugins/#__codelineno-31-5>)}
    
    [](<https://adk.dev/plugins/#__codelineno-32-1>)func (p *MyPlugin) OnEventCallback(ctx agent.InvocationContext, event *session.Event) (*session.Event, error) {
    [](<https://adk.dev/plugins/#__codelineno-32-2>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-32-3>)  return nil, nil
    [](<https://adk.dev/plugins/#__codelineno-32-4>)}
    
### Runner end callbacks[¶](<https://adk.dev/plugins/#runner-end-callbacks> "Permanent link")

The _Runner end_ callback **(`after_run_callback`)** happens when the agent has finished its entire process and all events have been handled, the `Runner` completes its run. The `after_run_callback` is the final hook, perfect for cleanup and final reporting.

  * **When It Runs:** After the `Runner` fully completes the execution of a request.
  * **Purpose:** Ideal for global cleanup tasks, such as closing connections or finalizing logs and metrics data.
  * **Flow Control:** This callback is for teardown only and cannot alter the final result.

The following code example shows the basic syntax of this callback:

PythonTypescriptJavaGo
    
    [](<https://adk.dev/plugins/#__codelineno-33-1>)async def after_run_callback(
    [](<https://adk.dev/plugins/#__codelineno-33-2>)    self, *, invocation_context: InvocationContext
    [](<https://adk.dev/plugins/#__codelineno-33-3>)) -> Optional[None]:
    
    [](<https://adk.dev/plugins/#__codelineno-34-1>)async afterRunCallback(invocationContext: InvocationContext): Promise<void> {
    [](<https://adk.dev/plugins/#__codelineno-34-2>)    // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-34-3>)}
    
    [](<https://adk.dev/plugins/#__codelineno-35-1>)@Override
    [](<https://adk.dev/plugins/#__codelineno-35-2>)public Completable afterRunCallback(InvocationContext invocationContext) {
    [](<https://adk.dev/plugins/#__codelineno-35-3>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-35-4>)  return Completable.complete();
    [](<https://adk.dev/plugins/#__codelineno-35-5>)}
    
    [](<https://adk.dev/plugins/#__codelineno-36-1>)func (p *MyPlugin) AfterRunCallback(ctx agent.InvocationContext) {
    [](<https://adk.dev/plugins/#__codelineno-36-2>)  // Your implementation here
    [](<https://adk.dev/plugins/#__codelineno-36-3>)}
    
## Next steps[¶](<https://adk.dev/plugins/#next-steps> "Permanent link")

Check out these resources for developing and applying Plugins to your ADK projects:

  * For more ADK Plugin code examples, see the [ADK Samples repository](<https://github.com/google/adk-samples>).
  * For information on applying Plugins for security purposes, see [Callbacks and Plugins for Security Guardrails](<https://adk.dev/safety/#callbacks-and-plugins-for-security-guardrails>).

Back to top 