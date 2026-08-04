# Graph-based agent workflows - Agent Development Kit (ADK)

> Source: [https://adk.dev/graphs/](https://adk.dev/graphs/)

[ Skip to content ](<https://adk.dev/graphs/#graph-based-agent-workflows>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/graphs/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/graphs/index.md> "View this page as Markdown")

# Graph-based agent workflows[¶](<https://adk.dev/graphs/#graph-based-agent-workflows> "Permanent link")

Supported in ADKPython v2.0.0Go v2.0.0

Graph-based agent workflows in ADK let you build agents with more precise control, creating deterministic processes that combine code logic and AI reasoning capabilities. Graph-based workflows allow you to define your agent logic as a graph of execution nodes and edges, combining AI-powered agent reasoning with deterministic tools and code.

![Graph-based flight upgrade agent](https://adk.dev/assets/workflow-design.svg)

**Figure 1.** A graph-based agent design for flight upgrades, combining workflow nodes of different types, including Functions, human input, Tools, and LLM capabilities.

Prebuilt ADK [template workflows](<https://adk.dev/agents/workflow-agents/>), such as [Sequential Agents](<https://adk.dev/agents/workflow-agents/sequential-agents/>), provide a defined process flow control only across a set of agents. You can continue to build standard ADK agents with long prompts, tools, and use them in graph-based workflow agents. When you need more precise control, workflow agent graphs give you more flexibility over how tasks are routed and executed. Graph-based workflows provide the following advantages:

  * **Define precise logic:** Explicitly map out routing logic to manage transitions between different nodes.
  * **Implement complex structures:** Build agent workflows that support branching and state management.
  * **Run chains of functions without AI:** Call agent tools and your own code without invoking a generative AI model.
  * **Enhance reliability:** Improve the predictability of your agents by relying on structured node definitions rather than prompts alone.

Workflow styles in ADK

ADK offers three complementary ways to compose multi-step work:

  * **Graph-based workflows** (this section): a declarative graph of nodes and edges with explicit routing — best for deterministic, structured processes.
  * **[Dynamic workflows](<https://adk.dev/graphs/dynamic/>):** programmatic orchestration in your own code (loops, conditionals, recursion) — best when the control flow is too complex or iterative for a static graph.
  * **[Prebuilt workflow agents](<https://adk.dev/agents/workflow-agents/>)** (sequential, parallel, loop): higher-level building blocks for common patterns without assembling a graph yourself.

## Get started[¶](<https://adk.dev/graphs/#get-started> "Permanent link")

This section describes how to get started with graph-based agents. The following example shows how to create a sequential graph-based agent workflow that generates a city name, looks up the current time in that city with a code function, and the final agent reports the information.

PythonGo
    
    [](<https://adk.dev/graphs/#__codelineno-0-1>)from google.adk import Agent
    [](<https://adk.dev/graphs/#__codelineno-0-2>)from google.adk import Workflow
    [](<https://adk.dev/graphs/#__codelineno-0-3>)from google.adk import Event
    [](<https://adk.dev/graphs/#__codelineno-0-4>)from pydantic import BaseModel
    [](<https://adk.dev/graphs/#__codelineno-0-5>)
    [](<https://adk.dev/graphs/#__codelineno-0-6>)city_generator_agent = Agent(
    [](<https://adk.dev/graphs/#__codelineno-0-7>)    name="city_generator_agent",
    [](<https://adk.dev/graphs/#__codelineno-0-8>)    model="gemini-flash-latest",
    [](<https://adk.dev/graphs/#__codelineno-0-9>)    instruction="""Return the name of a random city.
    [](<https://adk.dev/graphs/#__codelineno-0-10>)      Return only the name, nothing else.""",
    [](<https://adk.dev/graphs/#__codelineno-0-11>)    output_schema=str,
    [](<https://adk.dev/graphs/#__codelineno-0-12>))
    [](<https://adk.dev/graphs/#__codelineno-0-13>)
    [](<https://adk.dev/graphs/#__codelineno-0-14>)class CityTime(BaseModel):
    [](<https://adk.dev/graphs/#__codelineno-0-15>)    time_info: str  # time information
    [](<https://adk.dev/graphs/#__codelineno-0-16>)    city: str       # city name
    [](<https://adk.dev/graphs/#__codelineno-0-17>)
    [](<https://adk.dev/graphs/#__codelineno-0-18>)def lookup_time_function(node_input: str):
    [](<https://adk.dev/graphs/#__codelineno-0-19>)    """Simulate returning the current time in the specified city."""
    [](<https://adk.dev/graphs/#__codelineno-0-20>)    return CityTime(time_info="10:10 AM", city=node_input)
    [](<https://adk.dev/graphs/#__codelineno-0-21>)
    [](<https://adk.dev/graphs/#__codelineno-0-22>)city_report_agent = Agent(
    [](<https://adk.dev/graphs/#__codelineno-0-23>)    name="city_report_agent",
    [](<https://adk.dev/graphs/#__codelineno-0-24>)    model="gemini-flash-latest",
    [](<https://adk.dev/graphs/#__codelineno-0-25>)    input_schema=CityTime,
    [](<https://adk.dev/graphs/#__codelineno-0-26>)    instruction="""Output following line:
    [](<https://adk.dev/graphs/#__codelineno-0-27>)    It is {CityTime.time_info} in {CityTime.city} right now.""",
    [](<https://adk.dev/graphs/#__codelineno-0-28>)    output_schema=str,
    [](<https://adk.dev/graphs/#__codelineno-0-29>))
    [](<https://adk.dev/graphs/#__codelineno-0-30>)
    [](<https://adk.dev/graphs/#__codelineno-0-31>)def completed_message_function(node_input: str):
    [](<https://adk.dev/graphs/#__codelineno-0-32>)    return Event(
    [](<https://adk.dev/graphs/#__codelineno-0-33>)        message=f"{node_input}\n WORKFLOW COMPLETED.",
    [](<https://adk.dev/graphs/#__codelineno-0-34>)    )
    [](<https://adk.dev/graphs/#__codelineno-0-35>)
    [](<https://adk.dev/graphs/#__codelineno-0-36>)root_agent = Workflow(
    [](<https://adk.dev/graphs/#__codelineno-0-37>)    name="root_agent",
    [](<https://adk.dev/graphs/#__codelineno-0-38>)    edges=[
    [](<https://adk.dev/graphs/#__codelineno-0-39>)        ("START", city_generator_agent, lookup_time_function,
    [](<https://adk.dev/graphs/#__codelineno-0-40>)          city_report_agent, completed_message_function)
    [](<https://adk.dev/graphs/#__codelineno-0-41>)    ],
    [](<https://adk.dev/graphs/#__codelineno-0-42>))
    
In ADK Go v2.0.0, sequential workflows use the graph engine: `workflow.NewFunctionNode` wraps each step, and `workflow.Chain` wires the nodes into a sequential `edges` slice. The framework automatically passes each node's typed return value to the next node via `event.Output` — no session state writes are needed. The whole graph is wrapped in `workflowagent.New`, which produces a standard `agent.Agent`.
    
    [](<https://adk.dev/graphs/#__codelineno-1-1>)// cityTime holds the data passed from the lookup step to the report step.
    [](<https://adk.dev/graphs/#__codelineno-1-2>)type cityTime struct {
    [](<https://adk.dev/graphs/#__codelineno-1-3>)    City     string
    [](<https://adk.dev/graphs/#__codelineno-1-4>)    TimeInfo string
    [](<https://adk.dev/graphs/#__codelineno-1-5>)}
    [](<https://adk.dev/graphs/#__codelineno-1-6>)
    [](<https://adk.dev/graphs/#__codelineno-1-7>)// newSequentialGetStarted builds a three-node sequential workflow using the
    [](<https://adk.dev/graphs/#__codelineno-1-8>)// v2 graph engine. Each node is a workflow.NewFunctionNode whose return value
    [](<https://adk.dev/graphs/#__codelineno-1-9>)// is automatically wrapped in session.Event.Output and forwarded to the next
    [](<https://adk.dev/graphs/#__codelineno-1-10>)// node as its typed input.
    [](<https://adk.dev/graphs/#__codelineno-1-11>)//
    [](<https://adk.dev/graphs/#__codelineno-1-12>)// This is the Go equivalent of the Python Workflow example:
    [](<https://adk.dev/graphs/#__codelineno-1-13>)//
    [](<https://adk.dev/graphs/#__codelineno-1-14>)//  root_agent = Workflow(
    [](<https://adk.dev/graphs/#__codelineno-1-15>)//      name="root_agent",
    [](<https://adk.dev/graphs/#__codelineno-1-16>)//      edges=[("START", city_generator_agent, lookup_time_function,
    [](<https://adk.dev/graphs/#__codelineno-1-17>)//               city_report_agent, completed_message_function)],
    [](<https://adk.dev/graphs/#__codelineno-1-18>)//  )
    [](<https://adk.dev/graphs/#__codelineno-1-19>)func newSequentialGetStarted() (agent.Agent, error) {
    [](<https://adk.dev/graphs/#__codelineno-1-20>)    // Step 1: return a city name. The string is set as event.Output and
    [](<https://adk.dev/graphs/#__codelineno-1-21>)    // becomes the typed input of the next node.
    [](<https://adk.dev/graphs/#__codelineno-1-22>)    cityGeneratorNode := workflow.NewFunctionNode("city_generator_agent",
    [](<https://adk.dev/graphs/#__codelineno-1-23>)        func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/#__codelineno-1-24>)            return "Tokyo", nil
    [](<https://adk.dev/graphs/#__codelineno-1-25>)        },
    [](<https://adk.dev/graphs/#__codelineno-1-26>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/#__codelineno-1-27>)    )
    [](<https://adk.dev/graphs/#__codelineno-1-28>)
    [](<https://adk.dev/graphs/#__codelineno-1-29>)    // Step 2: receive the city name and return structured time data.
    [](<https://adk.dev/graphs/#__codelineno-1-30>)    lookupTimeNode := workflow.NewFunctionNode("lookup_time_function",
    [](<https://adk.dev/graphs/#__codelineno-1-31>)        func(_ agent.Context, city string) (cityTime, error) {
    [](<https://adk.dev/graphs/#__codelineno-1-32>)            return cityTime{City: city, TimeInfo: "10:10 AM"}, nil
    [](<https://adk.dev/graphs/#__codelineno-1-33>)        },
    [](<https://adk.dev/graphs/#__codelineno-1-34>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/#__codelineno-1-35>)    )
    [](<https://adk.dev/graphs/#__codelineno-1-36>)
    [](<https://adk.dev/graphs/#__codelineno-1-37>)    // Step 3: receive the cityTime struct and produce the final report string.
    [](<https://adk.dev/graphs/#__codelineno-1-38>)    cityReportNode := workflow.NewFunctionNode("city_report_agent",
    [](<https://adk.dev/graphs/#__codelineno-1-39>)        func(_ agent.Context, ct cityTime) (string, error) {
    [](<https://adk.dev/graphs/#__codelineno-1-40>)            return fmt.Sprintf("It is %s in %s right now.\nWORKFLOW COMPLETED.",
    [](<https://adk.dev/graphs/#__codelineno-1-41>)                ct.TimeInfo, ct.City), nil
    [](<https://adk.dev/graphs/#__codelineno-1-42>)        },
    [](<https://adk.dev/graphs/#__codelineno-1-43>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/#__codelineno-1-44>)    )
    [](<https://adk.dev/graphs/#__codelineno-1-45>)
    [](<https://adk.dev/graphs/#__codelineno-1-46>)    // workflow.Chain wires START → cityGeneratorNode → lookupTimeNode → cityReportNode.
    [](<https://adk.dev/graphs/#__codelineno-1-47>)    // Data flows through event.Output: no session state writes needed.
    [](<https://adk.dev/graphs/#__codelineno-1-48>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/#__codelineno-1-49>)        Name:        "root_agent",
    [](<https://adk.dev/graphs/#__codelineno-1-50>)        Description: "Sequential workflow: generate city → look up time → report.",
    [](<https://adk.dev/graphs/#__codelineno-1-51>)        Edges:       workflow.Chain(workflow.Start, cityGeneratorNode, lookupTimeNode, cityReportNode),
    [](<https://adk.dev/graphs/#__codelineno-1-52>)    })
    [](<https://adk.dev/graphs/#__codelineno-1-53>)}
    
This sample code demonstrates how you can assemble a simple, sequential workflow and alternate between agent processing and code execution. While you could perform these steps using a single agent with a longer prompt and a tool call, the graph-based approach gives you precise control over the task execution order and the data output from each step.

For more information about data handling with graph-based workflows, see [Data handling with workflow nodes and agents](<https://adk.dev/graphs/data-handling/>).

## Build processes with graphs[¶](<https://adk.dev/graphs/#build-processes-with-graphs> "Permanent link")

You can use prompt-based agents to define multiple step processes with descriptions of tasks and procedures using the instructions field of an ADK agent. However, as your instructions and procedures become longer and more complicated, making sure that the agent is following each step and guideline becomes more complicated and less reliable.

Graph-based workflow agents provide a significant advantage over prompt-based agents by allowing you to specifically define the overall process workflow in code. With graph-based agent workflows, each step of the process can be defined as an execution **_Node_** in a graph and each node can be an AI agent, Tool, or your programmed code. The following diagram illustrates how a simple prompt-based agent would translate into a workflow agent graph:

![Prompt-based agent to graph-based workflow](https://adk.dev/assets/prompts-to-graphs.svg)

**Figure 2.** Structure of prompt-based agent instructions translated into a graph-based workflow.

Moving from prompt-based agents to graph-based workflow agents allows you to explicitly break out the tasks of a procedure to define a specific execution flow. Once defined, the agent application flows the steps in the graph, switching between non-deterministic AI-powered agents and deterministic code as needed.

The following code sample shows how the workflow graph in Figure 2 could be translated into a graph-based agent:

PythonGo
    
    [](<https://adk.dev/graphs/#__codelineno-2-1>)process_message = Agent(
    [](<https://adk.dev/graphs/#__codelineno-2-2>)    name="process_message",
    [](<https://adk.dev/graphs/#__codelineno-2-3>)    model="gemini-flash-latest",
    [](<https://adk.dev/graphs/#__codelineno-2-4>)    instruction="""Classify user message into either "BUG", "CUSTOMER_SUPPORT",
    [](<https://adk.dev/graphs/#__codelineno-2-5>)      or "LOGISTICS". If you think a message applies to more than one category,
    [](<https://adk.dev/graphs/#__codelineno-2-6>)      reply with a comma separated list of categories.
    [](<https://adk.dev/graphs/#__codelineno-2-7>)   """,
    [](<https://adk.dev/graphs/#__codelineno-2-8>)    output_schema=str,
    [](<https://adk.dev/graphs/#__codelineno-2-9>))
    [](<https://adk.dev/graphs/#__codelineno-2-10>)
    [](<https://adk.dev/graphs/#__codelineno-2-11>)def router(node_input: str):
    [](<https://adk.dev/graphs/#__codelineno-2-12>)    routes = node_input.split(",")
    [](<https://adk.dev/graphs/#__codelineno-2-13>)    routes = [route.strip() for route in routes]
    [](<https://adk.dev/graphs/#__codelineno-2-14>)    return Event(route=routes)
    [](<https://adk.dev/graphs/#__codelineno-2-15>)
    [](<https://adk.dev/graphs/#__codelineno-2-16>)def response_1_bug():
    [](<https://adk.dev/graphs/#__codelineno-2-17>)    return Event(message="Handling bug...")
    [](<https://adk.dev/graphs/#__codelineno-2-18>)
    [](<https://adk.dev/graphs/#__codelineno-2-19>)def response_2_support():
    [](<https://adk.dev/graphs/#__codelineno-2-20>)    return Event(message="Handling customer support...")
    [](<https://adk.dev/graphs/#__codelineno-2-21>)
    [](<https://adk.dev/graphs/#__codelineno-2-22>)def response_3_logistics():
    [](<https://adk.dev/graphs/#__codelineno-2-23>)    return Event(message="Handling logistics...")
    [](<https://adk.dev/graphs/#__codelineno-2-24>)
    [](<https://adk.dev/graphs/#__codelineno-2-25>)root_agent = Workflow(
    [](<https://adk.dev/graphs/#__codelineno-2-26>)   name="routing_workflow",
    [](<https://adk.dev/graphs/#__codelineno-2-27>)   edges=[
    [](<https://adk.dev/graphs/#__codelineno-2-28>)       ("START", process_message, router),
    [](<https://adk.dev/graphs/#__codelineno-2-29>)       ( router,
    [](<https://adk.dev/graphs/#__codelineno-2-30>)           {
    [](<https://adk.dev/graphs/#__codelineno-2-31>)               "BUG": response_1_bug,
    [](<https://adk.dev/graphs/#__codelineno-2-32>)               "CUSTOMER_SUPPORT": response_2_support,
    [](<https://adk.dev/graphs/#__codelineno-2-33>)               "LOGISTICS": response_3_logistics,
    [](<https://adk.dev/graphs/#__codelineno-2-34>)           }
    [](<https://adk.dev/graphs/#__codelineno-2-35>)       )
    [](<https://adk.dev/graphs/#__codelineno-2-36>)   ],
    [](<https://adk.dev/graphs/#__codelineno-2-37>))
    
In ADK Go v2.0.0, conditional routing uses `workflow.NewEmittingFunctionNode` to set `event.Routes` and `workflow.StringRoute` edges to dispatch to the matching handler — the direct equivalent of Python's `router` function and dict dispatch. `workflow.Concat` merges the chain and the conditional edges into a single `edges` slice passed to `workflowagent.New`.
    
    [](<https://adk.dev/graphs/#__codelineno-3-1>)// classifyMessage is the router node. It emits ev.Routes to select which
    [](<https://adk.dev/graphs/#__codelineno-3-2>)// branch to follow — the Go equivalent of Python's:
    [](<https://adk.dev/graphs/#__codelineno-3-3>)//
    [](<https://adk.dev/graphs/#__codelineno-3-4>)//  def router(node_input: str):
    [](<https://adk.dev/graphs/#__codelineno-3-5>)//      return Event(route=["BUG"])
    [](<https://adk.dev/graphs/#__codelineno-3-6>)func classifyMessage(ctx agent.Context, msg string, emit func(*session.Event) error) (any, error) {
    [](<https://adk.dev/graphs/#__codelineno-3-7>)    // In a real workflow this step calls an LLM; here we classify by keyword.
    [](<https://adk.dev/graphs/#__codelineno-3-8>)    category := "LOGISTICS"
    [](<https://adk.dev/graphs/#__codelineno-3-9>)    lower := strings.ToLower(msg)
    [](<https://adk.dev/graphs/#__codelineno-3-10>)    switch {
    [](<https://adk.dev/graphs/#__codelineno-3-11>)    case strings.Contains(lower, "bug") || strings.Contains(lower, "error"):
    [](<https://adk.dev/graphs/#__codelineno-3-12>)        category = "BUG"
    [](<https://adk.dev/graphs/#__codelineno-3-13>)    case strings.Contains(lower, "help") || strings.Contains(lower, "support"):
    [](<https://adk.dev/graphs/#__codelineno-3-14>)        category = "CUSTOMER_SUPPORT"
    [](<https://adk.dev/graphs/#__codelineno-3-15>)    }
    [](<https://adk.dev/graphs/#__codelineno-3-16>)
    [](<https://adk.dev/graphs/#__codelineno-3-17>)    ev := session.NewEvent(ctx, ctx.InvocationID())
    [](<https://adk.dev/graphs/#__codelineno-3-18>)    ev.Routes = []string{category} // drives edge dispatch
    [](<https://adk.dev/graphs/#__codelineno-3-19>)    ev.Output = msg                // forward original message to the chosen handler
    [](<https://adk.dev/graphs/#__codelineno-3-20>)    if err := emit(ev); err != nil {
    [](<https://adk.dev/graphs/#__codelineno-3-21>)        return nil, err
    [](<https://adk.dev/graphs/#__codelineno-3-22>)    }
    [](<https://adk.dev/graphs/#__codelineno-3-23>)    return nil, nil // nil suppresses the automatic terminal event
    [](<https://adk.dev/graphs/#__codelineno-3-24>)}
    [](<https://adk.dev/graphs/#__codelineno-3-25>)
    [](<https://adk.dev/graphs/#__codelineno-3-26>)// newProcessPipeline builds a classification + conditional-routing workflow
    [](<https://adk.dev/graphs/#__codelineno-3-27>)// using the v2 graph engine. The classifyMessage emitting node sets
    [](<https://adk.dev/graphs/#__codelineno-3-28>)// ev.Routes, and the graph engine dispatches to the matching handler via
    [](<https://adk.dev/graphs/#__codelineno-3-29>)// workflow.StringRoute.
    [](<https://adk.dev/graphs/#__codelineno-3-30>)//
    [](<https://adk.dev/graphs/#__codelineno-3-31>)// This is the Go equivalent of the Python Workflow example:
    [](<https://adk.dev/graphs/#__codelineno-3-32>)//
    [](<https://adk.dev/graphs/#__codelineno-3-33>)//  root_agent = Workflow(
    [](<https://adk.dev/graphs/#__codelineno-3-34>)//      name="routing_workflow",
    [](<https://adk.dev/graphs/#__codelineno-3-35>)//      edges=[
    [](<https://adk.dev/graphs/#__codelineno-3-36>)//          ("START", process_message, router),
    [](<https://adk.dev/graphs/#__codelineno-3-37>)//          (router, {
    [](<https://adk.dev/graphs/#__codelineno-3-38>)//              "BUG": response_1_bug,
    [](<https://adk.dev/graphs/#__codelineno-3-39>)//              "CUSTOMER_SUPPORT": response_2_support,
    [](<https://adk.dev/graphs/#__codelineno-3-40>)//              "LOGISTICS": response_3_logistics,
    [](<https://adk.dev/graphs/#__codelineno-3-41>)//          }),
    [](<https://adk.dev/graphs/#__codelineno-3-42>)//      ],
    [](<https://adk.dev/graphs/#__codelineno-3-43>)//  )
    [](<https://adk.dev/graphs/#__codelineno-3-44>)func newProcessPipeline() (agent.Agent, error) {
    [](<https://adk.dev/graphs/#__codelineno-3-45>)    classifyNode := workflow.NewEmittingFunctionNode(
    [](<https://adk.dev/graphs/#__codelineno-3-46>)        "process_message", classifyMessage, workflow.NodeConfig{},
    [](<https://adk.dev/graphs/#__codelineno-3-47>)    )
    [](<https://adk.dev/graphs/#__codelineno-3-48>)
    [](<https://adk.dev/graphs/#__codelineno-3-49>)    bugNode := workflow.NewFunctionNode("response_1_bug",
    [](<https://adk.dev/graphs/#__codelineno-3-50>)        func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/#__codelineno-3-51>)            return "Handling bug...", nil
    [](<https://adk.dev/graphs/#__codelineno-3-52>)        },
    [](<https://adk.dev/graphs/#__codelineno-3-53>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/#__codelineno-3-54>)    )
    [](<https://adk.dev/graphs/#__codelineno-3-55>)
    [](<https://adk.dev/graphs/#__codelineno-3-56>)    supportNode := workflow.NewFunctionNode("response_2_support",
    [](<https://adk.dev/graphs/#__codelineno-3-57>)        func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/#__codelineno-3-58>)            return "Handling customer support...", nil
    [](<https://adk.dev/graphs/#__codelineno-3-59>)        },
    [](<https://adk.dev/graphs/#__codelineno-3-60>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/#__codelineno-3-61>)    )
    [](<https://adk.dev/graphs/#__codelineno-3-62>)
    [](<https://adk.dev/graphs/#__codelineno-3-63>)    logisticsNode := workflow.NewFunctionNode("response_3_logistics",
    [](<https://adk.dev/graphs/#__codelineno-3-64>)        func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/#__codelineno-3-65>)            return "Handling logistics...", nil
    [](<https://adk.dev/graphs/#__codelineno-3-66>)        },
    [](<https://adk.dev/graphs/#__codelineno-3-67>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/#__codelineno-3-68>)    )
    [](<https://adk.dev/graphs/#__codelineno-3-69>)
    [](<https://adk.dev/graphs/#__codelineno-3-70>)    // workflow.Concat merges the sequential chain with the conditional edges.
    [](<https://adk.dev/graphs/#__codelineno-3-71>)    // Each workflow.Edge carries a workflow.StringRoute matcher that the engine
    [](<https://adk.dev/graphs/#__codelineno-3-72>)    // checks against ev.Routes emitted by classifyNode.
    [](<https://adk.dev/graphs/#__codelineno-3-73>)    edges := workflow.Concat(
    [](<https://adk.dev/graphs/#__codelineno-3-74>)        workflow.Chain(workflow.Start, classifyNode),
    [](<https://adk.dev/graphs/#__codelineno-3-75>)        []workflow.Edge{
    [](<https://adk.dev/graphs/#__codelineno-3-76>)            {From: classifyNode, To: bugNode, Route: workflow.StringRoute("BUG")},
    [](<https://adk.dev/graphs/#__codelineno-3-77>)            {From: classifyNode, To: supportNode, Route: workflow.StringRoute("CUSTOMER_SUPPORT")},
    [](<https://adk.dev/graphs/#__codelineno-3-78>)            {From: classifyNode, To: logisticsNode, Route: workflow.StringRoute("LOGISTICS")},
    [](<https://adk.dev/graphs/#__codelineno-3-79>)        },
    [](<https://adk.dev/graphs/#__codelineno-3-80>)    )
    [](<https://adk.dev/graphs/#__codelineno-3-81>)
    [](<https://adk.dev/graphs/#__codelineno-3-82>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/#__codelineno-3-83>)        Name:        "routing_workflow",
    [](<https://adk.dev/graphs/#__codelineno-3-84>)        Description: "Classifies a message and routes it to the appropriate handler.",
    [](<https://adk.dev/graphs/#__codelineno-3-85>)        Edges:       edges,
    [](<https://adk.dev/graphs/#__codelineno-3-86>)    })
    [](<https://adk.dev/graphs/#__codelineno-3-87>)}
    
This sample code demonstrates how you can compose a sequence of agents to define a graph with routes between a set of _nodes_ , which are discrete tasks that can include agents, Tools, your code, and even additional workflow agents. For information about building advanced pipelines, see [Build graph routes for workflow agents](<https://adk.dev/graphs/routes/>).

## Known limitations[¶](<https://adk.dev/graphs/#known-limitations> "Permanent link")

There are some known limitations with graph-based workflows. They are _not compatible_ with the following ADK features:

  * **Live streaming:** Not supported in graph-based workflows.
  * **Integrations:** Some third-party [integrations](<https://adk.dev/integrations/>) may not be compatible with graph-based workflows.

Go: graph workflow API

The `workflow` package in ADK Go v2.0.0 is the direct equivalent of the Python `Workflow` class. Use `workflow.NewFunctionNode` and `workflow.NewAgentNode` to define nodes, `workflow.Chain` or `workflow.Concat` with `[]workflow.Edge` to wire them, and `workflowagent.New` to wrap the graph as a runnable agent. Conditional routing uses `workflow.StringRoute`, `workflow.IntRoute`, or `workflow.BoolRoute` matched against `event.Routes`. Fan-in is handled by `workflow.NewJoinNode`.

For advanced routing patterns and fan-out/join examples, see [Build graph routes for workflow agents](<https://adk.dev/graphs/routes/>). For prebuilt higher-level alternatives (sequential, parallel, loop), see [Prebuilt workflow agents](<https://adk.dev/agents/workflow-agents/>).

Back to top 