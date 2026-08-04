# Tool limitations - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools/limitations/](https://adk.dev/tools/limitations/)

[ Skip to content ](<https://adk.dev/tools/limitations/#limitations-for-adk-tools>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools/limitations.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools/limitations/index.md> "View this page as Markdown")

# Limitations for ADK tools[¶](<https://adk.dev/tools/limitations/#limitations-for-adk-tools> "Permanent link")

Some ADK tools have limitations that can impact how you implement them within an agent workflow. This page lists these tool limitations and workarounds, if available.

## One tool per agent limitation[¶](<https://adk.dev/tools/limitations/#one-tool-one-agent> "Permanent link")

ONLY for Search in ADK Python v1.15.0 and lower

This limitation only applies to the use of Google Search and Agent Search tools in ADK Python v1.15.0 and lower. ADK Python release v1.16.0 and higher provides a built-in workaround to remove this limitation.

In general, you can use more than one tool in an agent, but use of specific tools within an agent excludes the use of any other tools in that agent. The following ADK Tools can only be used by themselves, without any other tools, in a single agent object:

  * [Code Execution](<https://adk.dev/integrations/code-execution/>) with Gemini API (Note: in TypeScript, this requires Gemini 2.0+ and does not have this limitation)
  * [Google Search](<https://adk.dev/integrations/google-search/>) with Gemini API (Note: limitation only applies to Gemini 1.x models in TypeScript)
  * [Agent Search](<https://adk.dev/integrations/agent-search/>) (Note: currently unavailable in TypeScript)

For example, the following approach that uses one of these tools along with other tools, within a single agent, is **_not supported_** :

PythonTypeScriptJavaKotlin
    
    [](<https://adk.dev/tools/limitations/#__codelineno-0-1>)root_agent = Agent(
    [](<https://adk.dev/tools/limitations/#__codelineno-0-2>)    name="RootAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-0-3>)    model="gemini-flash-latest",
    [](<https://adk.dev/tools/limitations/#__codelineno-0-4>)    description="Code Agent",
    [](<https://adk.dev/tools/limitations/#__codelineno-0-5>)    tools=[custom_function],
    [](<https://adk.dev/tools/limitations/#__codelineno-0-6>)    code_executor=BuiltInCodeExecutor() # <-- NOT supported when used with tools
    [](<https://adk.dev/tools/limitations/#__codelineno-0-7>))
    
    [](<https://adk.dev/tools/limitations/#__codelineno-1-1>)import {Agent, BuiltInCodeExecutor} from '@google/adk';
    [](<https://adk.dev/tools/limitations/#__codelineno-1-2>)
    [](<https://adk.dev/tools/limitations/#__codelineno-1-3>)const rootAgent = new Agent({
    [](<https://adk.dev/tools/limitations/#__codelineno-1-4>)  name: 'RootAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-1-5>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-1-6>)  description: 'Code Agent',
    [](<https://adk.dev/tools/limitations/#__codelineno-1-7>)  tools: [myCustomTool], // Assume myCustomTool is defined
    [](<https://adk.dev/tools/limitations/#__codelineno-1-8>)  codeExecutor: new BuiltInCodeExecutor(), // <-- NOT supported when used with tools
    [](<https://adk.dev/tools/limitations/#__codelineno-1-9>)});
    
    [](<https://adk.dev/tools/limitations/#__codelineno-2-1>) LlmAgent searchAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-2-2>)        LlmAgent.builder()
    [](<https://adk.dev/tools/limitations/#__codelineno-2-3>)            .model(MODEL_ID)
    [](<https://adk.dev/tools/limitations/#__codelineno-2-4>)            .name("SearchAgent")
    [](<https://adk.dev/tools/limitations/#__codelineno-2-5>)            .instruction("You're a specialist in Google Search")
    [](<https://adk.dev/tools/limitations/#__codelineno-2-6>)            .tools(new GoogleSearchTool(), new YourCustomTool()) // <-- NOT supported
    [](<https://adk.dev/tools/limitations/#__codelineno-2-7>)            .build();
    
    [](<https://adk.dev/tools/limitations/#__codelineno-3-1>)val searchAgent = LlmAgent(
    [](<https://adk.dev/tools/limitations/#__codelineno-3-2>)    name = "SearchAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-3-3>)    model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools/limitations/#__codelineno-3-4>)    instruction = Instruction("You're a specialist in Google Search"),
    [](<https://adk.dev/tools/limitations/#__codelineno-3-5>)    tools = listOf(GoogleSearchTool(), YourCustomTool()) // <-- NOT supported
    [](<https://adk.dev/tools/limitations/#__codelineno-3-6>))
    
### Workaround #1: AgentTool.create() method[¶](<https://adk.dev/tools/limitations/#workaround-1-agenttoolcreate-method> "Permanent link")

Supported in ADKPythonTypeScript (v0.6.1+)JavaKotlin v0.1.0

The following code sample demonstrates how to use multiple built-in tools or how to use built-in tools with other tools by using multiple agents:

PythonTypeScriptJavaKotlin
    
    [](<https://adk.dev/tools/limitations/#__codelineno-4-1>)from google.adk.tools.agent_tool import AgentTool
    [](<https://adk.dev/tools/limitations/#__codelineno-4-2>)from google.adk.agents import Agent
    [](<https://adk.dev/tools/limitations/#__codelineno-4-3>)from google.adk.tools import google_search
    [](<https://adk.dev/tools/limitations/#__codelineno-4-4>)from google.adk.code_executors import BuiltInCodeExecutor
    [](<https://adk.dev/tools/limitations/#__codelineno-4-5>)
    [](<https://adk.dev/tools/limitations/#__codelineno-4-6>)search_agent = Agent(
    [](<https://adk.dev/tools/limitations/#__codelineno-4-7>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-4-8>)    name='SearchAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-4-9>)    instruction="""
    [](<https://adk.dev/tools/limitations/#__codelineno-4-10>)    You're a specialist in Google Search
    [](<https://adk.dev/tools/limitations/#__codelineno-4-11>)    """,
    [](<https://adk.dev/tools/limitations/#__codelineno-4-12>)    tools=[google_search],
    [](<https://adk.dev/tools/limitations/#__codelineno-4-13>))
    [](<https://adk.dev/tools/limitations/#__codelineno-4-14>)coding_agent = Agent(
    [](<https://adk.dev/tools/limitations/#__codelineno-4-15>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-4-16>)    name='CodeAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-4-17>)    instruction="""
    [](<https://adk.dev/tools/limitations/#__codelineno-4-18>)    You're a specialist in Code Execution
    [](<https://adk.dev/tools/limitations/#__codelineno-4-19>)    """,
    [](<https://adk.dev/tools/limitations/#__codelineno-4-20>)    code_executor=BuiltInCodeExecutor(),
    [](<https://adk.dev/tools/limitations/#__codelineno-4-21>))
    [](<https://adk.dev/tools/limitations/#__codelineno-4-22>)root_agent = Agent(
    [](<https://adk.dev/tools/limitations/#__codelineno-4-23>)    name="RootAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-4-24>)    model="gemini-flash-latest",
    [](<https://adk.dev/tools/limitations/#__codelineno-4-25>)    description="Root Agent",
    [](<https://adk.dev/tools/limitations/#__codelineno-4-26>)    tools=[AgentTool(agent=search_agent), AgentTool(agent=coding_agent)],
    [](<https://adk.dev/tools/limitations/#__codelineno-4-27>))
    
    [](<https://adk.dev/tools/limitations/#__codelineno-5-1>)import {Agent, AgentTool, BuiltInCodeExecutor, GOOGLE_SEARCH} from '@google/adk';
    [](<https://adk.dev/tools/limitations/#__codelineno-5-2>)
    [](<https://adk.dev/tools/limitations/#__codelineno-5-3>)const searchAgent = new Agent({
    [](<https://adk.dev/tools/limitations/#__codelineno-5-4>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-5-5>)  name: 'SearchAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-5-6>)  instruction: "You're a specialist in Google Search",
    [](<https://adk.dev/tools/limitations/#__codelineno-5-7>)  tools: [GOOGLE_SEARCH],
    [](<https://adk.dev/tools/limitations/#__codelineno-5-8>)});
    [](<https://adk.dev/tools/limitations/#__codelineno-5-9>)
    [](<https://adk.dev/tools/limitations/#__codelineno-5-10>)const codingAgent = new Agent({
    [](<https://adk.dev/tools/limitations/#__codelineno-5-11>)  model: 'gemini-flash-latest', // Built-in code execution requires Gemini 2.0+ in ADK JS
    [](<https://adk.dev/tools/limitations/#__codelineno-5-12>)  name: 'CodeAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-5-13>)  instruction: "You're a specialist in Code Execution",
    [](<https://adk.dev/tools/limitations/#__codelineno-5-14>)  codeExecutor: new BuiltInCodeExecutor(),
    [](<https://adk.dev/tools/limitations/#__codelineno-5-15>)});
    [](<https://adk.dev/tools/limitations/#__codelineno-5-16>)
    [](<https://adk.dev/tools/limitations/#__codelineno-5-17>)const rootAgent = new Agent({
    [](<https://adk.dev/tools/limitations/#__codelineno-5-18>)  name: 'RootAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-5-19>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-5-20>)  description: 'Root Agent',
    [](<https://adk.dev/tools/limitations/#__codelineno-5-21>)  tools: [new AgentTool({agent: searchAgent}), new AgentTool({agent: codingAgent})],
    [](<https://adk.dev/tools/limitations/#__codelineno-5-22>)});
    
    [](<https://adk.dev/tools/limitations/#__codelineno-6-1>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/tools/limitations/#__codelineno-6-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools/limitations/#__codelineno-6-3>)import com.google.adk.tools.AgentTool;
    [](<https://adk.dev/tools/limitations/#__codelineno-6-4>)import com.google.adk.tools.BuiltInCodeExecutionTool;
    [](<https://adk.dev/tools/limitations/#__codelineno-6-5>)import com.google.adk.tools.GoogleSearchTool;
    [](<https://adk.dev/tools/limitations/#__codelineno-6-6>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/tools/limitations/#__codelineno-6-7>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-8>)public class NestedAgentApp {
    [](<https://adk.dev/tools/limitations/#__codelineno-6-9>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-10>)  private static final String MODEL_ID = "gemini-flash-latest";
    [](<https://adk.dev/tools/limitations/#__codelineno-6-11>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-12>)  public static void main(String[] args) {
    [](<https://adk.dev/tools/limitations/#__codelineno-6-13>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-14>)    // Define the SearchAgent
    [](<https://adk.dev/tools/limitations/#__codelineno-6-15>)    LlmAgent searchAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-6-16>)        LlmAgent.builder()
    [](<https://adk.dev/tools/limitations/#__codelineno-6-17>)            .model(MODEL_ID)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-18>)            .name("SearchAgent")
    [](<https://adk.dev/tools/limitations/#__codelineno-6-19>)            .instruction("You're a specialist in Google Search")
    [](<https://adk.dev/tools/limitations/#__codelineno-6-20>)            .tools(new GoogleSearchTool()) // Instantiate GoogleSearchTool
    [](<https://adk.dev/tools/limitations/#__codelineno-6-21>)            .build();
    [](<https://adk.dev/tools/limitations/#__codelineno-6-22>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-23>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-24>)    // Define the CodingAgent
    [](<https://adk.dev/tools/limitations/#__codelineno-6-25>)    LlmAgent codingAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-6-26>)        LlmAgent.builder()
    [](<https://adk.dev/tools/limitations/#__codelineno-6-27>)            .model(MODEL_ID)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-28>)            .name("CodeAgent")
    [](<https://adk.dev/tools/limitations/#__codelineno-6-29>)            .instruction("You're a specialist in Code Execution")
    [](<https://adk.dev/tools/limitations/#__codelineno-6-30>)            .tools(new BuiltInCodeExecutionTool()) // Instantiate BuiltInCodeExecutionTool
    [](<https://adk.dev/tools/limitations/#__codelineno-6-31>)            .build();
    [](<https://adk.dev/tools/limitations/#__codelineno-6-32>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-33>)    // Define the RootAgent, which uses AgentTool.create() to wrap SearchAgent and CodingAgent
    [](<https://adk.dev/tools/limitations/#__codelineno-6-34>)    BaseAgent rootAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-6-35>)        LlmAgent.builder()
    [](<https://adk.dev/tools/limitations/#__codelineno-6-36>)            .name("RootAgent")
    [](<https://adk.dev/tools/limitations/#__codelineno-6-37>)            .model(MODEL_ID)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-38>)            .description("Root Agent")
    [](<https://adk.dev/tools/limitations/#__codelineno-6-39>)            .tools(
    [](<https://adk.dev/tools/limitations/#__codelineno-6-40>)                AgentTool.create(searchAgent), // Use create method
    [](<https://adk.dev/tools/limitations/#__codelineno-6-41>)                AgentTool.create(codingAgent)   // Use create method
    [](<https://adk.dev/tools/limitations/#__codelineno-6-42>)             )
    [](<https://adk.dev/tools/limitations/#__codelineno-6-43>)            .build();
    [](<https://adk.dev/tools/limitations/#__codelineno-6-44>)
    [](<https://adk.dev/tools/limitations/#__codelineno-6-45>)    // Note: This sample only demonstrates the agent definitions.
    [](<https://adk.dev/tools/limitations/#__codelineno-6-46>)    // To run these agents, you'd need to integrate them with a Runner and SessionService,
    [](<https://adk.dev/tools/limitations/#__codelineno-6-47>)    // similar to the previous examples.
    [](<https://adk.dev/tools/limitations/#__codelineno-6-48>)    System.out.println("Agents defined successfully:");
    [](<https://adk.dev/tools/limitations/#__codelineno-6-49>)    System.out.println("  Root Agent: " + rootAgent.name());
    [](<https://adk.dev/tools/limitations/#__codelineno-6-50>)    System.out.println("  Search Agent (nested): " + searchAgent.name());
    [](<https://adk.dev/tools/limitations/#__codelineno-6-51>)    System.out.println("  Code Agent (nested): " + codingAgent.name());
    [](<https://adk.dev/tools/limitations/#__codelineno-6-52>)  }
    [](<https://adk.dev/tools/limitations/#__codelineno-6-53>)}
    
    [](<https://adk.dev/tools/limitations/#__codelineno-7-1>)// Define the SearchAgent
    [](<https://adk.dev/tools/limitations/#__codelineno-7-2>)val searchAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-7-3>)    LlmAgent(
    [](<https://adk.dev/tools/limitations/#__codelineno-7-4>)        name = "SearchAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-7-5>)        model = Gemini(name = modelId),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-6>)        instruction = Instruction("You're a specialist in Google Search"),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-7>)        tools = listOf(GoogleSearchTool()),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-8>)    )
    [](<https://adk.dev/tools/limitations/#__codelineno-7-9>)
    [](<https://adk.dev/tools/limitations/#__codelineno-7-10>)// Define another agent (e.g., for specialized tasks)
    [](<https://adk.dev/tools/limitations/#__codelineno-7-11>)val taskAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-7-12>)    LlmAgent(
    [](<https://adk.dev/tools/limitations/#__codelineno-7-13>)        name = "TaskAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-7-14>)        model = Gemini(name = modelId),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-15>)        instruction = Instruction("You're a specialist in performing specific tasks."),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-16>)    )
    [](<https://adk.dev/tools/limitations/#__codelineno-7-17>)
    [](<https://adk.dev/tools/limitations/#__codelineno-7-18>)// Define the RootAgent, which uses AgentTool to wrap SearchAgent and TaskAgent
    [](<https://adk.dev/tools/limitations/#__codelineno-7-19>)val rootAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-7-20>)    LlmAgent(
    [](<https://adk.dev/tools/limitations/#__codelineno-7-21>)        name = "RootAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-7-22>)        model = Gemini(name = modelId),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-23>)        description = "Root Agent",
    [](<https://adk.dev/tools/limitations/#__codelineno-7-24>)        tools =
    [](<https://adk.dev/tools/limitations/#__codelineno-7-25>)            listOf(
    [](<https://adk.dev/tools/limitations/#__codelineno-7-26>)                AgentTool(agent = searchAgent),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-27>)                AgentTool(agent = taskAgent),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-28>)            ),
    [](<https://adk.dev/tools/limitations/#__codelineno-7-29>)    )
    
### Workaround #2: bypass_multi_tools_limit[¶](<https://adk.dev/tools/limitations/#workaround-2-bypass_multi_tools_limit> "Permanent link")

Supported in ADKPythonJavaKotlin v0.1.0

ADK Python has a built-in workaround which bypasses this limitation for `GoogleSearchTool` and `VertexAiSearchTool` (use `bypass_multi_tools_limit=True` to enable it), as shown in the [built_in_multi_tools](<https://github.com/google/adk-python/tree/main/contributing/samples/tools/built_in_multi_tools>). sample agent.

Warning

Built-in tools cannot be used within a sub-agent, with the exception of `GoogleSearchTool` and `VertexAiSearchTool` in ADK Python because of the workaround mentioned above.

For example, the following approach that uses built-in tools within sub-agents is **not supported** :

PythonTypeScriptJavaKotlin
    
    [](<https://adk.dev/tools/limitations/#__codelineno-8-1>)url_context_agent = Agent(
    [](<https://adk.dev/tools/limitations/#__codelineno-8-2>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-8-3>)    name='UrlContextAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-8-4>)    instruction="""
    [](<https://adk.dev/tools/limitations/#__codelineno-8-5>)    You're a specialist in URL Context
    [](<https://adk.dev/tools/limitations/#__codelineno-8-6>)    """,
    [](<https://adk.dev/tools/limitations/#__codelineno-8-7>)    tools=[url_context],
    [](<https://adk.dev/tools/limitations/#__codelineno-8-8>))
    [](<https://adk.dev/tools/limitations/#__codelineno-8-9>)coding_agent = Agent(
    [](<https://adk.dev/tools/limitations/#__codelineno-8-10>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-8-11>)    name='CodeAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-8-12>)    instruction="""
    [](<https://adk.dev/tools/limitations/#__codelineno-8-13>)    You're a specialist in Code Execution
    [](<https://adk.dev/tools/limitations/#__codelineno-8-14>)    """,
    [](<https://adk.dev/tools/limitations/#__codelineno-8-15>)    code_executor=BuiltInCodeExecutor(),
    [](<https://adk.dev/tools/limitations/#__codelineno-8-16>))
    [](<https://adk.dev/tools/limitations/#__codelineno-8-17>)root_agent = Agent(
    [](<https://adk.dev/tools/limitations/#__codelineno-8-18>)    name="RootAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-8-19>)    model="gemini-flash-latest",
    [](<https://adk.dev/tools/limitations/#__codelineno-8-20>)    description="Root Agent",
    [](<https://adk.dev/tools/limitations/#__codelineno-8-21>)    sub_agents=[
    [](<https://adk.dev/tools/limitations/#__codelineno-8-22>)        url_context_agent,
    [](<https://adk.dev/tools/limitations/#__codelineno-8-23>)        coding_agent
    [](<https://adk.dev/tools/limitations/#__codelineno-8-24>)    ],
    [](<https://adk.dev/tools/limitations/#__codelineno-8-25>))
    
    [](<https://adk.dev/tools/limitations/#__codelineno-9-1>)import {Agent, BuiltInCodeExecutor} from '@google/adk';
    [](<https://adk.dev/tools/limitations/#__codelineno-9-2>)
    [](<https://adk.dev/tools/limitations/#__codelineno-9-3>)const urlContextAgent = new Agent({
    [](<https://adk.dev/tools/limitations/#__codelineno-9-4>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-9-5>)  name: 'UrlContextAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-9-6>)  instruction: "You're a specialist in URL Context",
    [](<https://adk.dev/tools/limitations/#__codelineno-9-7>)  tools: [myCustomTool], // Assume myCustomTool is defined
    [](<https://adk.dev/tools/limitations/#__codelineno-9-8>)});
    [](<https://adk.dev/tools/limitations/#__codelineno-9-9>)
    [](<https://adk.dev/tools/limitations/#__codelineno-9-10>)const codingAgent = new Agent({
    [](<https://adk.dev/tools/limitations/#__codelineno-9-11>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-9-12>)  name: 'CodeAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-9-13>)  instruction: "You're a specialist in Code Execution",
    [](<https://adk.dev/tools/limitations/#__codelineno-9-14>)  codeExecutor: new BuiltInCodeExecutor(),
    [](<https://adk.dev/tools/limitations/#__codelineno-9-15>)});
    [](<https://adk.dev/tools/limitations/#__codelineno-9-16>)
    [](<https://adk.dev/tools/limitations/#__codelineno-9-17>)const rootAgent = new Agent({
    [](<https://adk.dev/tools/limitations/#__codelineno-9-18>)  name: 'RootAgent',
    [](<https://adk.dev/tools/limitations/#__codelineno-9-19>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tools/limitations/#__codelineno-9-20>)  description: 'Root Agent',
    [](<https://adk.dev/tools/limitations/#__codelineno-9-21>)  subAgents: [urlContextAgent, codingAgent], // NOT supported when sub-agents use built-in tools
    [](<https://adk.dev/tools/limitations/#__codelineno-9-22>)});
    
    [](<https://adk.dev/tools/limitations/#__codelineno-10-1>)LlmAgent searchAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-10-2>)    LlmAgent.builder()
    [](<https://adk.dev/tools/limitations/#__codelineno-10-3>)        .model("gemini-flash-latest")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-4>)        .name("SearchAgent")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-5>)        .instruction("You're a specialist in Google Search")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-6>)        .tools(new GoogleSearchTool())
    [](<https://adk.dev/tools/limitations/#__codelineno-10-7>)        .build();
    [](<https://adk.dev/tools/limitations/#__codelineno-10-8>)
    [](<https://adk.dev/tools/limitations/#__codelineno-10-9>)LlmAgent codingAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-10-10>)    LlmAgent.builder()
    [](<https://adk.dev/tools/limitations/#__codelineno-10-11>)        .model("gemini-flash-latest")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-12>)        .name("CodeAgent")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-13>)        .instruction("You're a specialist in Code Execution")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-14>)        .tools(new BuiltInCodeExecutionTool())
    [](<https://adk.dev/tools/limitations/#__codelineno-10-15>)        .build();
    [](<https://adk.dev/tools/limitations/#__codelineno-10-16>)
    [](<https://adk.dev/tools/limitations/#__codelineno-10-17>)
    [](<https://adk.dev/tools/limitations/#__codelineno-10-18>)LlmAgent rootAgent =
    [](<https://adk.dev/tools/limitations/#__codelineno-10-19>)    LlmAgent.builder()
    [](<https://adk.dev/tools/limitations/#__codelineno-10-20>)        .name("RootAgent")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-21>)        .model("gemini-flash-latest")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-22>)        .description("Root Agent")
    [](<https://adk.dev/tools/limitations/#__codelineno-10-23>)        .subAgents(searchAgent, codingAgent) // Not supported, as the sub agents use built in tools.
    [](<https://adk.dev/tools/limitations/#__codelineno-10-24>)        .build();
    
    [](<https://adk.dev/tools/limitations/#__codelineno-11-1>)val searchAgent = LlmAgent(
    [](<https://adk.dev/tools/limitations/#__codelineno-11-2>)    model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools/limitations/#__codelineno-11-3>)    name = "SearchAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-11-4>)    instruction = Instruction("You're a specialist in Google Search"),
    [](<https://adk.dev/tools/limitations/#__codelineno-11-5>)    tools = listOf(GoogleSearchTool())
    [](<https://adk.dev/tools/limitations/#__codelineno-11-6>))
    [](<https://adk.dev/tools/limitations/#__codelineno-11-7>)
    [](<https://adk.dev/tools/limitations/#__codelineno-11-8>)val codingAgent = LlmAgent(
    [](<https://adk.dev/tools/limitations/#__codelineno-11-9>)    model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools/limitations/#__codelineno-11-10>)    name = "CodeAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-11-11>)    instruction = Instruction("You're a specialist in Code Execution")
    [](<https://adk.dev/tools/limitations/#__codelineno-11-12>)    // Kotlin currently doesn't have a BuiltInCodeExecutionTool in core
    [](<https://adk.dev/tools/limitations/#__codelineno-11-13>))
    [](<https://adk.dev/tools/limitations/#__codelineno-11-14>)
    [](<https://adk.dev/tools/limitations/#__codelineno-11-15>)
    [](<https://adk.dev/tools/limitations/#__codelineno-11-16>)val rootAgent = LlmAgent(
    [](<https://adk.dev/tools/limitations/#__codelineno-11-17>)    name = "RootAgent",
    [](<https://adk.dev/tools/limitations/#__codelineno-11-18>)    model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools/limitations/#__codelineno-11-19>)    description = "Root Agent",
    [](<https://adk.dev/tools/limitations/#__codelineno-11-20>)    subAgents = listOf(searchAgent, codingAgent) // Not supported when sub-agents use built-in tools
    [](<https://adk.dev/tools/limitations/#__codelineno-11-21>))
    
Back to top 