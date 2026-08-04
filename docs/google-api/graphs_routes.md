# Graph routes - Agent Development Kit (ADK)

> Source: [https://adk.dev/graphs/routes/](https://adk.dev/graphs/routes/)

[ Skip to content ](<https://adk.dev/graphs/routes/#build-graph-routes-for-agent-workflows>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/graphs/routes.md> "Edit this page on GitHub") [ ](<https://adk.dev/graphs/routes/index.md> "View this page as Markdown")

# Build graph routes for agent workflows[¶](<https://adk.dev/graphs/routes/#build-graph-routes-for-agent-workflows> "Permanent link")

Supported in ADKPython v2.0.0Go v2.0.0

Graph-based workflows in ADK define agent logic as a graph of execution nodes and edges, allowing you to build more reliable processes that combine artificial intelligence (AI) reasoning and code logic. These workflows allow you to create logical routes of execution nodes that can encapsulate code functions, AI-powered agents, Tools, and human input. By explicitly mapping out routing logic, this approach allows you to define a specific, step-wise process workflow in code, providing improved precision and reliability over purely prompt-based agents.

![Task graph with conditional routing between nodes](https://adk.dev/assets/graph-workflow-router.svg)

**Figure 1.** Visualization of a task graph and the routing code to implement it.

PythonGo
    
    [](<https://adk.dev/graphs/routes/#__codelineno-0-1>)root_agent = Workflow(
    [](<https://adk.dev/graphs/routes/#__codelineno-0-2>)  name="routing_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-0-3>)  edges=[
    [](<https://adk.dev/graphs/routes/#__codelineno-0-4>)    ("START", process_message, router),
    [](<https://adk.dev/graphs/routes/#__codelineno-0-5>)    (router,
    [](<https://adk.dev/graphs/routes/#__codelineno-0-6>)      {
    [](<https://adk.dev/graphs/routes/#__codelineno-0-7>)        "output-1": response_1,
    [](<https://adk.dev/graphs/routes/#__codelineno-0-8>)        "output-2": response_2,
    [](<https://adk.dev/graphs/routes/#__codelineno-0-9>)        "output-3": response_3,
    [](<https://adk.dev/graphs/routes/#__codelineno-0-10>)      },
    [](<https://adk.dev/graphs/routes/#__codelineno-0-11>)    ),
    [](<https://adk.dev/graphs/routes/#__codelineno-0-12>)  ],
    [](<https://adk.dev/graphs/routes/#__codelineno-0-13>))
    
ADK Go v2.0.0 provides the following approach to graph-based workflows:

**Graph engine** (`workflowagent` \+ `workflow.Edge`): A node-and-edges graph API that maps directly to Python's `Workflow(edges=[...])`. Nodes are defined with `workflow.NewFunctionNode`, `workflow.NewAgentNode`, or `workflow.NewDynamicNode`, edges are declared as `[]workflow.Edge`, and the whole graph is wrapped in a `workflowagent.New` call:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-1-1>)edges := workflow.Concat(
    [](<https://adk.dev/graphs/routes/#__codelineno-1-2>)    workflow.Chain(workflow.Start, classifyNode),
    [](<https://adk.dev/graphs/routes/#__codelineno-1-3>)    []workflow.Edge{
    [](<https://adk.dev/graphs/routes/#__codelineno-1-4>)        {From: classifyNode, To: responseA, Route: workflow.StringRoute("output-1")},
    [](<https://adk.dev/graphs/routes/#__codelineno-1-5>)        {From: classifyNode, To: responseB, Route: workflow.StringRoute("output-2")},
    [](<https://adk.dev/graphs/routes/#__codelineno-1-6>)        {From: classifyNode, To: responseC, Route: workflow.StringRoute("output-3")},
    [](<https://adk.dev/graphs/routes/#__codelineno-1-7>)    },
    [](<https://adk.dev/graphs/routes/#__codelineno-1-8>))
    [](<https://adk.dev/graphs/routes/#__codelineno-1-9>)rootAgent, _ := workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-1-10>)    Name:  "routing_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-1-11>)    Edges: edges,
    [](<https://adk.dev/graphs/routes/#__codelineno-1-12>)})
    
The advantage of using a graph-based agent workflow is the significant increase in control, predictability, and reliability over prompt-based agents. By defining the overall process workflow in code, you gain more control over how tasks are routed and executed. This structured node definition improves the predictability of agents and enhances reliability for complex tasks that require defined steps and process management.

Get started with graph-based workflows in ADK by checking out [Graph-based agent workflows](<https://adk.dev/graphs/>).

## Nodes[¶](<https://adk.dev/graphs/routes/#nodes> "Permanent link")

A graph is composed of execution nodes. These _nodes_ can be **_Agents_** , ADK **_Tools_** , human input tasks, or code functions you write. Nodes can take inputs from previously executed nodes, and emit data through **_Event_** objects.

PythonGo

The following shows a simple **_FunctionNode_** that handles text inputs and sends a text output:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-2-1>)from google.adk import Event
    [](<https://adk.dev/graphs/routes/#__codelineno-2-2>)
    [](<https://adk.dev/graphs/routes/#__codelineno-2-3>)def my_function_node(node_input: str):
    [](<https://adk.dev/graphs/routes/#__codelineno-2-4>)    input_text_modified = node_input.upper()
    [](<https://adk.dev/graphs/routes/#__codelineno-2-5>)    return Event(output=input_text_modified)
    
In ADK Go v2.0.0, the primary node type is `workflow.NewFunctionNode`. A `FunctionNode` wraps a plain Go function: the function returns a typed value, and the framework automatically wraps it in a `session.Event`, setting `event.Output`. The successor node receives this value as its typed `input` parameter — no manual state writes or event construction needed:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-3-1>)// newFunctionNodePipeline demonstrates workflow.NewFunctionNode as the primary
    [](<https://adk.dev/graphs/routes/#__codelineno-3-2>)// v2 node type. A FunctionNode wraps a plain Go function: the function returns
    [](<https://adk.dev/graphs/routes/#__codelineno-3-3>)// a typed value, and the framework automatically wraps it in a session.Event,
    [](<https://adk.dev/graphs/routes/#__codelineno-3-4>)// setting event.Output. The successor node receives this value as its typed
    [](<https://adk.dev/graphs/routes/#__codelineno-3-5>)// input parameter.
    [](<https://adk.dev/graphs/routes/#__codelineno-3-6>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-3-7>)// This is the direct Go equivalent of the Python FunctionNode:
    [](<https://adk.dev/graphs/routes/#__codelineno-3-8>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-3-9>)//  def my_function_node(node_input: str):
    [](<https://adk.dev/graphs/routes/#__codelineno-3-10>)//      return Event(output=node_input.upper())
    [](<https://adk.dev/graphs/routes/#__codelineno-3-11>)func newFunctionNodePipeline() (agent.Agent, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-3-12>)    upperFn := func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-3-13>)        return strings.ToUpper(input), nil
    [](<https://adk.dev/graphs/routes/#__codelineno-3-14>)    }
    [](<https://adk.dev/graphs/routes/#__codelineno-3-15>)
    [](<https://adk.dev/graphs/routes/#__codelineno-3-16>)    suffixFn := func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-3-17>)        return input + " IS AWESOME!", nil
    [](<https://adk.dev/graphs/routes/#__codelineno-3-18>)    }
    [](<https://adk.dev/graphs/routes/#__codelineno-3-19>)
    [](<https://adk.dev/graphs/routes/#__codelineno-3-20>)    // workflow.NewFunctionNode wraps each function as a graph node.
    [](<https://adk.dev/graphs/routes/#__codelineno-3-21>)    // workflow.Chain wires them in order: START → upper → suffix.
    [](<https://adk.dev/graphs/routes/#__codelineno-3-22>)    // The output of upperFn is delivered as the typed input of suffixFn
    [](<https://adk.dev/graphs/routes/#__codelineno-3-23>)    // via event.Output — no session state writes are needed.
    [](<https://adk.dev/graphs/routes/#__codelineno-3-24>)    nodeA := workflow.NewFunctionNode("upper", upperFn, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-3-25>)    nodeB := workflow.NewFunctionNode("suffix", suffixFn, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-3-26>)
    [](<https://adk.dev/graphs/routes/#__codelineno-3-27>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-3-28>)        Name:        "function_node_pipeline",
    [](<https://adk.dev/graphs/routes/#__codelineno-3-29>)        Description: "Demonstrates workflow.NewFunctionNode data flow via Event.Output.",
    [](<https://adk.dev/graphs/routes/#__codelineno-3-30>)        Edges:       workflow.Chain(workflow.Start, nodeA, nodeB),
    [](<https://adk.dev/graphs/routes/#__codelineno-3-31>)    })
    [](<https://adk.dev/graphs/routes/#__codelineno-3-32>)}
    
For more information about transferring data between nodes, see [Data handling for agent workflows](<https://adk.dev/graphs/data-handling/>).

## Workflow graphs syntax[¶](<https://adk.dev/graphs/routes/#workflow-graphs-syntax> "Permanent link")

You define a graph by composing workflow agents. This section provides an overview of the common routing patterns.

Caution: Workflow agent limitations

You can add **_LlmAgents_** to graph-based workflows. However, they must be configured for single-turn or task mode. For more information about agent modes, see [Build collaborative agent teams](<https://adk.dev/workflows/collaboration/#mode-configuration-and-behaviors>).

### Route sequences[¶](<https://adk.dev/graphs/routes/#route-sequences> "Permanent link")

A sequential route runs each node once, in the listed order.

PythonGo

The `edges` array uses the `START` keyword to indicate the beginning of a graph execution, with each listed node executed in sequence:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-4-1>)edges=[("START", task_A_node)]  # single node run
    [](<https://adk.dev/graphs/routes/#__codelineno-4-2>)edges=[("START",
    [](<https://adk.dev/graphs/routes/#__codelineno-4-3>)        task_A_node,
    [](<https://adk.dev/graphs/routes/#__codelineno-4-4>)        task_B_node,
    [](<https://adk.dev/graphs/routes/#__codelineno-4-5>)        task_C_node)]           # 3 nodes run in order
    
`workflow.Chain(workflow.Start, nodeA, nodeB, nodeC)` wires nodes into a sequential edge slice. Each node's typed return value is forwarded to the next node via `event.Output` — no session state writes needed:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-5-1>)// newSequentialNodes builds a two-step sequential workflow using the v2 graph
    [](<https://adk.dev/graphs/routes/#__codelineno-5-2>)// engine. workflow.Chain wires the nodes in order; each node's typed return
    [](<https://adk.dev/graphs/routes/#__codelineno-5-3>)// value is forwarded to the next node via event.Output.
    [](<https://adk.dev/graphs/routes/#__codelineno-5-4>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-5-5>)// This is the Go equivalent of:
    [](<https://adk.dev/graphs/routes/#__codelineno-5-6>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-5-7>)//  edges=[("START", task_A_node, task_B_node)]
    [](<https://adk.dev/graphs/routes/#__codelineno-5-8>)func newSequentialNodes() (agent.Agent, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-5-9>)    // task_A_node: transforms the user's input.
    [](<https://adk.dev/graphs/routes/#__codelineno-5-10>)    taskANode := workflow.NewFunctionNode("task_A_node",
    [](<https://adk.dev/graphs/routes/#__codelineno-5-11>)        func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-5-12>)            return "Summary: " + strings.TrimSpace(input), nil
    [](<https://adk.dev/graphs/routes/#__codelineno-5-13>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-5-14>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-5-15>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-5-16>)
    [](<https://adk.dev/graphs/routes/#__codelineno-5-17>)    // task_B_node: receives task A's output as its typed input and produces
    [](<https://adk.dev/graphs/routes/#__codelineno-5-18>)    // the final result. No session state reads needed.
    [](<https://adk.dev/graphs/routes/#__codelineno-5-19>)    taskBNode := workflow.NewFunctionNode("task_B_node",
    [](<https://adk.dev/graphs/routes/#__codelineno-5-20>)        func(_ agent.Context, summary string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-5-21>)            return strings.ToUpper(summary), nil
    [](<https://adk.dev/graphs/routes/#__codelineno-5-22>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-5-23>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-5-24>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-5-25>)
    [](<https://adk.dev/graphs/routes/#__codelineno-5-26>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-5-27>)        Name:        "sequential_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-5-28>)        Description: "Runs task A then task B in order via workflow.Chain.",
    [](<https://adk.dev/graphs/routes/#__codelineno-5-29>)        Edges:       workflow.Chain(workflow.Start, taskANode, taskBNode),
    [](<https://adk.dev/graphs/routes/#__codelineno-5-30>)    })
    [](<https://adk.dev/graphs/routes/#__codelineno-5-31>)}
    
### Route branches and conditional execution[¶](<https://adk.dev/graphs/routes/#route-branches-and-conditional-execution> "Permanent link")

PythonGo

In Python, branching is handled by a `FunctionNode` that returns an `Event(route=...)` value, which the `edges` dict dispatches to different nodes.
    
    [](<https://adk.dev/graphs/routes/#__codelineno-6-1>)from google.adk import Event, Workflow
    [](<https://adk.dev/graphs/routes/#__codelineno-6-2>)from google.adk.agents import Agent
    [](<https://adk.dev/graphs/routes/#__codelineno-6-3>)
    [](<https://adk.dev/graphs/routes/#__codelineno-6-4>)
    [](<https://adk.dev/graphs/routes/#__codelineno-6-5>)def router(node_input: str):
    [](<https://adk.dev/graphs/routes/#__codelineno-6-6>)    """Route to task B or C based on node_input."""
    [](<https://adk.dev/graphs/routes/#__codelineno-6-7>)    if condition(node_input):
    [](<https://adk.dev/graphs/routes/#__codelineno-6-8>)        return Event(route="RUN_TASK_C")
    [](<https://adk.dev/graphs/routes/#__codelineno-6-9>)    return Event(route="RUN_TASK_B")
    [](<https://adk.dev/graphs/routes/#__codelineno-6-10>)
    [](<https://adk.dev/graphs/routes/#__codelineno-6-11>)task_B_node = Agent(name="task_B_agent") # An agent to execute node B
    [](<https://adk.dev/graphs/routes/#__codelineno-6-12>)
    [](<https://adk.dev/graphs/routes/#__codelineno-6-13>)def task_C_node(node_input: str):
    [](<https://adk.dev/graphs/routes/#__codelineno-6-14>)    """A FunctionNode to execute node C."""
    [](<https://adk.dev/graphs/routes/#__codelineno-6-15>)    return Event(output="Task C completed")
    [](<https://adk.dev/graphs/routes/#__codelineno-6-16>)
    [](<https://adk.dev/graphs/routes/#__codelineno-6-17>)root_agent = Workflow(
    [](<https://adk.dev/graphs/routes/#__codelineno-6-18>)    name="routing_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-6-19>)    edges=[
    [](<https://adk.dev/graphs/routes/#__codelineno-6-20>)        ("START", task_A_node, router),
    [](<https://adk.dev/graphs/routes/#__codelineno-6-21>)        (router,
    [](<https://adk.dev/graphs/routes/#__codelineno-6-22>)          {
    [](<https://adk.dev/graphs/routes/#__codelineno-6-23>)            # "route value": node_to_run
    [](<https://adk.dev/graphs/routes/#__codelineno-6-24>)            "RUN_TASK_B": task_B_node,
    [](<https://adk.dev/graphs/routes/#__codelineno-6-25>)            "RUN_TASK_C": task_C_node,
    [](<https://adk.dev/graphs/routes/#__codelineno-6-26>)          },
    [](<https://adk.dev/graphs/routes/#__codelineno-6-27>)        ),
    [](<https://adk.dev/graphs/routes/#__codelineno-6-28>)    ],
    [](<https://adk.dev/graphs/routes/#__codelineno-6-29>))
    
In ADK Go v2.0.0, conditional dispatch uses the `workflow` graph engine. A node sets `Event.Routes` to one or more string route keys, and each `workflow.Edge` selects its successor using a `workflow.Route` matcher:

  * `workflow.StringRoute("category")` — matches a single string value
  * `workflow.IntRoute(n)` or `workflow.MultiRoute[int]{1, 2, 3}` — matches integer values
  * `workflow.BoolRoute(true)` — matches a boolean value
  * `workflow.Default` — matches when no other route on the same source node matches

The following pattern is the Go equivalent of the Python router:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-7-1>)// classifyNode emits an Event with Routes=[]string{"BUG"},
    [](<https://adk.dev/graphs/routes/#__codelineno-7-2>)// ["CUSTOMER_SUPPORT"], or ["LOGISTICS"] based on the message.
    [](<https://adk.dev/graphs/routes/#__codelineno-7-3>)edges := workflow.Concat(
    [](<https://adk.dev/graphs/routes/#__codelineno-7-4>)    workflow.Chain(workflow.Start, processMessage, classifyNode),
    [](<https://adk.dev/graphs/routes/#__codelineno-7-5>)    []workflow.Edge{
    [](<https://adk.dev/graphs/routes/#__codelineno-7-6>)        {From: classifyNode, To: bugHandler,       Route: workflow.StringRoute("BUG")},
    [](<https://adk.dev/graphs/routes/#__codelineno-7-7>)        {From: classifyNode, To: supportHandler,   Route: workflow.StringRoute("CUSTOMER_SUPPORT")},
    [](<https://adk.dev/graphs/routes/#__codelineno-7-8>)        {From: classifyNode, To: logisticsHandler, Route: workflow.StringRoute("LOGISTICS")},
    [](<https://adk.dev/graphs/routes/#__codelineno-7-9>)    },
    [](<https://adk.dev/graphs/routes/#__codelineno-7-10>))
    [](<https://adk.dev/graphs/routes/#__codelineno-7-11>)rootAgent, _ := workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-7-12>)    Name:  "routing_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-7-13>)    Edges: edges,
    [](<https://adk.dev/graphs/routes/#__codelineno-7-14>)})
    
`workflow.EdgeBuilder` provides a fluent alternative to assembling the `[]workflow.Edge` slice by hand. The builder's `Add`, `AddFanOut`, and `AddFanIn` methods express the same topology with less repetition:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-8-1>)eb := workflow.NewEdgeBuilder()
    [](<https://adk.dev/graphs/routes/#__codelineno-8-2>)eb.Add(workflow.Start, processMessage)
    [](<https://adk.dev/graphs/routes/#__codelineno-8-3>)eb.Add(processMessage, classifyNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-8-4>)eb.AddRoute(classifyNode, bugHandler,       workflow.StringRoute("BUG"))
    [](<https://adk.dev/graphs/routes/#__codelineno-8-5>)eb.AddRoute(classifyNode, supportHandler,   workflow.StringRoute("CUSTOMER_SUPPORT"))
    [](<https://adk.dev/graphs/routes/#__codelineno-8-6>)eb.AddRoute(classifyNode, logisticsHandler, workflow.StringRoute("LOGISTICS"))
    [](<https://adk.dev/graphs/routes/#__codelineno-8-7>)
    [](<https://adk.dev/graphs/routes/#__codelineno-8-8>)rootAgent, _ := workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-8-9>)    Name:  "routing_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-8-10>)    Edges: eb.Build(),
    [](<https://adk.dev/graphs/routes/#__codelineno-8-11>)})
    
For complete, runnable routing examples see: [string routing](<https://github.com/google/adk-go/tree/v2/examples/workflow/routing/string>), [int / multi-value routing](<https://github.com/google/adk-go/tree/v2/examples/workflow/routing/int>), and [LLM-driven routing](<https://github.com/google/adk-go/tree/v2/examples/workflow/routing/llm>).

Prebuilt agents: encoding routing in state

When using `sequentialagent` / `parallelagent` / `loopagent` instead of the graph engine, there is no `Event.Routes` dispatch. Encode the routing decision in session state via `OutputKey` and let downstream agents inspect it in their `Instruction` template, or use a `loopagent` with an `Escalate`-based exit — see the [loop and escalation example](<https://adk.dev/graphs/routes/#loop-and-escalation-exit>) below.

## Parallel tasks: fan out and join paths[¶](<https://adk.dev/graphs/routes/#parallel-tasks-fan-out-and-join-paths> "Permanent link")

You can create graphs that split execution across multiple, parallel nodes, and typically you need to assemble the output of each node for further processing. This task execution pattern has two stages. The workflow first fans out when it starts multiple parallel tasks, and then it re-joins those paths when those tasks are completed before proceeding to the next step.

![Tasks connecting to a JoinNode](https://adk.dev/assets/graph-joinnode.svg)

**Figure 2.** The output of parallel task nodes can be assembled and joined before passing results to the next step.

PythonGo

You accomplish the join step by using a **_JoinNode_** object, which waits for each parallel task to complete and then passes the collection of outputs from these nodes to the next node.
    
    [](<https://adk.dev/graphs/routes/#__codelineno-9-1>)from google.adk.workflow import JoinNode
    [](<https://adk.dev/graphs/routes/#__codelineno-9-2>)
    [](<https://adk.dev/graphs/routes/#__codelineno-9-3>)my_join_node = JoinNode(name="my_join_node")
    [](<https://adk.dev/graphs/routes/#__codelineno-9-4>)
    [](<https://adk.dev/graphs/routes/#__codelineno-9-5>)edges=[
    [](<https://adk.dev/graphs/routes/#__codelineno-9-6>)    ("START", parallel_task_A, my_join_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-9-7>)    ("START", parallel_task_B, my_join_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-9-8>)    ("START", parallel_task_C, my_join_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-9-9>)    (my_join_node, final_task_D),
    [](<https://adk.dev/graphs/routes/#__codelineno-9-10>)]
    
Caution: Stuck JoinNode from incomplete nodes

The **_JoinNode_** object proceeds only after all its upstream nodes have provided an Event output. If one of the upstream nodes fails to provide output, the JoinNode is stuck and workflow execution stops. Make sure to include failsafe output from any node that outputs to a **_JoinNode_**.

ADK Go v2.0.0 provides `workflow.NewJoinNode` for true fan-in in the graph engine: fan-out edges from `workflow.Start` (or any shared source node) feed in parallel to the join node, which waits for all of them to complete before emitting a `map[string]any` keyed by predecessor node name to the next node.

`workflow.EdgeBuilder` makes the fan-out / fan-in wiring concise with its dedicated `AddFanOut` and `AddFanIn` helpers (as shown in the [complex workflow example](<https://github.com/google/adk-go/tree/v2/examples/workflow/complex>)):
    
    [](<https://adk.dev/graphs/routes/#__codelineno-10-1>)gatherNode := workflow.NewJoinNode("gather")
    [](<https://adk.dev/graphs/routes/#__codelineno-10-2>)
    [](<https://adk.dev/graphs/routes/#__codelineno-10-3>)eb := workflow.NewEdgeBuilder()
    [](<https://adk.dev/graphs/routes/#__codelineno-10-4>)eb.AddFanOut(workflow.Start, researchNodeA, researchNodeB, researchNodeC)
    [](<https://adk.dev/graphs/routes/#__codelineno-10-5>)eb.AddFanIn(gatherNode, researchNodeA, researchNodeB, researchNodeC)
    [](<https://adk.dev/graphs/routes/#__codelineno-10-6>)eb.Add(gatherNode, formatNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-10-7>)eb.Add(formatNode, synthesisNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-10-8>)
    [](<https://adk.dev/graphs/routes/#__codelineno-10-9>)rootAgent, _ := workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-10-10>)    Name:  "research_pipeline",
    [](<https://adk.dev/graphs/routes/#__codelineno-10-11>)    Edges: eb.Build(),
    [](<https://adk.dev/graphs/routes/#__codelineno-10-12>)})
    
The following snippet shows the complete fan-out / join pattern using `workflow.NewJoinNode` and `EdgeBuilder.AddFanOut` / `AddFanIn`:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-11-1>)// newParallelFanOut builds a fan-out / join workflow using the v2 graph engine.
    [](<https://adk.dev/graphs/routes/#__codelineno-11-2>)// Three research nodes run in parallel from Start; workflow.NewJoinNode waits
    [](<https://adk.dev/graphs/routes/#__codelineno-11-3>)// for all of them to complete and emits a map[nodeName]output to the format
    [](<https://adk.dev/graphs/routes/#__codelineno-11-4>)// node, which assembles the results for a synthesis node.
    [](<https://adk.dev/graphs/routes/#__codelineno-11-5>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-11-6>)// Graph topology:
    [](<https://adk.dev/graphs/routes/#__codelineno-11-7>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-11-8>)//  START ─┬─> research_A ──┐
    [](<https://adk.dev/graphs/routes/#__codelineno-11-9>)//         ├─> research_B ──┼─> gather (JoinNode) ─> format ─> synthesis
    [](<https://adk.dev/graphs/routes/#__codelineno-11-10>)//         └─> research_C ──┘
    [](<https://adk.dev/graphs/routes/#__codelineno-11-11>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-11-12>)// Python equivalent:
    [](<https://adk.dev/graphs/routes/#__codelineno-11-13>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-11-14>)//  edges=[
    [](<https://adk.dev/graphs/routes/#__codelineno-11-15>)//      ("START", research_A, my_join_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-11-16>)//      ("START", research_B, my_join_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-11-17>)//      ("START", research_C, my_join_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-11-18>)//      (my_join_node, format_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-11-19>)//      (format_node, synthesis_node),
    [](<https://adk.dev/graphs/routes/#__codelineno-11-20>)//  ]
    [](<https://adk.dev/graphs/routes/#__codelineno-11-21>)func newParallelFanOut() (agent.Agent, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-11-22>)    researchA := workflow.NewFunctionNode("research_A",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-23>)        func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-11-24>)            return "Fact about renewable energy.", nil
    [](<https://adk.dev/graphs/routes/#__codelineno-11-25>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-11-26>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-11-27>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-11-28>)    researchB := workflow.NewFunctionNode("research_B",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-29>)        func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-11-30>)            return "Fact about electric vehicles.", nil
    [](<https://adk.dev/graphs/routes/#__codelineno-11-31>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-11-32>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-11-33>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-11-34>)    researchC := workflow.NewFunctionNode("research_C",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-35>)        func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-11-36>)            return "Fact about carbon capture.", nil
    [](<https://adk.dev/graphs/routes/#__codelineno-11-37>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-11-38>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-11-39>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-11-40>)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-41>)    // workflow.NewJoinNode waits for all predecessors (research_A, research_B,
    [](<https://adk.dev/graphs/routes/#__codelineno-11-42>)    // research_C) to complete and emits a map[nodeName]output to its successor.
    [](<https://adk.dev/graphs/routes/#__codelineno-11-43>)    gatherNode := workflow.NewJoinNode("gather")
    [](<https://adk.dev/graphs/routes/#__codelineno-11-44>)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-45>)    // formatNode receives map[string]any from gatherNode and assembles a
    [](<https://adk.dev/graphs/routes/#__codelineno-11-46>)    // combined prompt string.
    [](<https://adk.dev/graphs/routes/#__codelineno-11-47>)    formatNode := workflow.NewFunctionNode("format",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-48>)        func(_ agent.Context, results map[string]any) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-11-49>)            return fmt.Sprintf("A: %v\nB: %v\nC: %v",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-50>)                results["research_A"],
    [](<https://adk.dev/graphs/routes/#__codelineno-11-51>)                results["research_B"],
    [](<https://adk.dev/graphs/routes/#__codelineno-11-52>)                results["research_C"],
    [](<https://adk.dev/graphs/routes/#__codelineno-11-53>)            ), nil
    [](<https://adk.dev/graphs/routes/#__codelineno-11-54>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-11-55>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-11-56>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-11-57>)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-58>)    synthesisNode := workflow.NewFunctionNode("synthesis",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-59>)        func(_ agent.Context, prompt string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-11-60>)            return "Combined report: " + prompt, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-11-61>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-11-62>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-11-63>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-11-64>)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-65>)    // EdgeBuilder.AddFanOut fans workflow.Start out to all three research nodes.
    [](<https://adk.dev/graphs/routes/#__codelineno-11-66>)    // EdgeBuilder.AddFanIn routes all three research nodes into gatherNode.
    [](<https://adk.dev/graphs/routes/#__codelineno-11-67>)    eb := workflow.NewEdgeBuilder()
    [](<https://adk.dev/graphs/routes/#__codelineno-11-68>)    eb.AddFanOut(workflow.Start, researchA, researchB, researchC)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-69>)    eb.AddFanIn(gatherNode, researchA, researchB, researchC)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-70>)    eb.Add(gatherNode, formatNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-71>)    eb.Add(formatNode, synthesisNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-72>)
    [](<https://adk.dev/graphs/routes/#__codelineno-11-73>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-11-74>)        Name:        "fan_out_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-75>)        Description: "Parallel research fan-out with JoinNode barrier and synthesis.",
    [](<https://adk.dev/graphs/routes/#__codelineno-11-76>)        Edges:       eb.Build(),
    [](<https://adk.dev/graphs/routes/#__codelineno-11-77>)    })
    [](<https://adk.dev/graphs/routes/#__codelineno-11-78>)}
    
Caution: Stuck JoinNode from incomplete nodes

`workflow.NewJoinNode` proceeds only after every predecessor node has emitted an `event.Output`. If a predecessor fails without emitting output, the JoinNode is stuck and workflow execution stops. Attach a `RetryConfig` to flaky predecessor nodes to guard against transient failures.

## Nested workflows[¶](<https://adk.dev/graphs/routes/#nested-workflows> "Permanent link")

When building more complex workflows, you may want to encapsulate the functionality for specific tasks into reusable workflows. One or more workflow agents can be used as a sub-agent within another workflow agent to accomplish this goal.

![Nested Workflows inside a parent Workflow](https://adk.dev/assets/graph-workflow-nodes.svg)

**Figure 3.** Nested workflow agents as sub-agents inside a parent workflow.

PythonGo
    
    [](<https://adk.dev/graphs/routes/#__codelineno-12-1>)from google.adk import Workflow
    [](<https://adk.dev/graphs/routes/#__codelineno-12-2>)
    [](<https://adk.dev/graphs/routes/#__codelineno-12-3>)root_agent = Workflow(
    [](<https://adk.dev/graphs/routes/#__codelineno-12-4>)    name="parent_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-12-5>)    edges=[
    [](<https://adk.dev/graphs/routes/#__codelineno-12-6>)       ("START", task_A1, router),
    [](<https://adk.dev/graphs/routes/#__codelineno-12-7>)       (router, {
    [](<https://adk.dev/graphs/routes/#__codelineno-12-8>)            "RUN_WORKFLOW_B": workflow_B,
    [](<https://adk.dev/graphs/routes/#__codelineno-12-9>)            "RUN_WORKFLOW_C": workflow_C,
    [](<https://adk.dev/graphs/routes/#__codelineno-12-10>)            },
    [](<https://adk.dev/graphs/routes/#__codelineno-12-11>)       ),
    [](<https://adk.dev/graphs/routes/#__codelineno-12-12>)    ],
    [](<https://adk.dev/graphs/routes/#__codelineno-12-13>))
    
#### Nested workflow data output[¶](<https://adk.dev/graphs/routes/#nested-workflow-data-output> "Permanent link")

Output for nested Workflow objects works slightly differently from individual nodes. When the nested workflow completes one of its nodes, it transmits data to the next node in the nested workflow's graph _and_ the system bubbles up the Event for that node to the parent workflow for process traceability. When the nested workflow completes the last node in its process, the parent node extracts data from the final leaf nodes and emits it as the output of the nested workflow.

ADK Go v2.0.0 supports nested workflows in two complementary ways:

**Graph engine** (`workflowagent` \+ `workflow.Edge`): A `workflowagent` created with `workflowagent.New` is itself an `agent.Agent`, so it can be wrapped with `workflow.NewAgentNode` and used as a node inside another workflow's `edges` slice. The inner workflow runs to completion as a single node from the outer graph's perspective, and its terminal output is emitted as the node output on the outer graph's edge:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-13-1>)innerNode, _ := workflow.NewAgentNode(innerWorkflowAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-13-2>)
    [](<https://adk.dev/graphs/routes/#__codelineno-13-3>)outerEdges := workflow.Chain(workflow.Start, outerStepNode, innerNode, finalNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-13-4>)rootAgent, _ := workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-13-5>)    Name:  "parent_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-13-6>)    Edges: outerEdges,
    [](<https://adk.dev/graphs/routes/#__codelineno-13-7>)})
    
The following snippet shows both the inner and outer graph construction. `workflow.NewAgentNode` wraps the inner `workflowagent` so it can be placed in the outer graph's `workflow.Chain`:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-14-1>)// newNestedWorkflows shows how to nest one workflowagent inside another using
    [](<https://adk.dev/graphs/routes/#__codelineno-14-2>)// the v2 graph engine. The inner workflowagent is wrapped with
    [](<https://adk.dev/graphs/routes/#__codelineno-14-3>)// workflow.NewAgentNode and placed as a node in the outer graph's edge slice.
    [](<https://adk.dev/graphs/routes/#__codelineno-14-4>)// From the outer graph's perspective the inner workflow is a single node that
    [](<https://adk.dev/graphs/routes/#__codelineno-14-5>)// runs to completion before the edge to finalNode is followed.
    [](<https://adk.dev/graphs/routes/#__codelineno-14-6>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-14-7>)// Python equivalent:
    [](<https://adk.dev/graphs/routes/#__codelineno-14-8>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-14-9>)//  root_agent = Workflow(
    [](<https://adk.dev/graphs/routes/#__codelineno-14-10>)//      name="parent_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-11>)//      edges=[("START", task_A1, workflow_B, final_node)],
    [](<https://adk.dev/graphs/routes/#__codelineno-14-12>)//  )
    [](<https://adk.dev/graphs/routes/#__codelineno-14-13>)func newNestedWorkflows() (agent.Agent, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-14-14>)    // --- Inner workflow B ---
    [](<https://adk.dev/graphs/routes/#__codelineno-14-15>)    innerStep1 := workflow.NewFunctionNode("inner_step_1",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-16>)        func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-14-17>)            return "[ES] " + input, nil // simulate translation to Spanish
    [](<https://adk.dev/graphs/routes/#__codelineno-14-18>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-14-19>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-14-20>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-14-21>)    innerStep2 := workflow.NewFunctionNode("inner_step_2",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-22>)        func(_ agent.Context, spanish string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-14-23>)            return "[EN] " + spanish, nil // simulate translation back to English
    [](<https://adk.dev/graphs/routes/#__codelineno-14-24>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-14-25>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-14-26>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-14-27>)
    [](<https://adk.dev/graphs/routes/#__codelineno-14-28>)    // workflowB is a self-contained inner graph.
    [](<https://adk.dev/graphs/routes/#__codelineno-14-29>)    workflowB, err := workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-14-30>)        Name:        "workflow_B",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-31>)        Description: "Translates input to Spanish then back to English.",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-32>)        Edges:       workflow.Chain(workflow.Start, innerStep1, innerStep2),
    [](<https://adk.dev/graphs/routes/#__codelineno-14-33>)    })
    [](<https://adk.dev/graphs/routes/#__codelineno-14-34>)    if err != nil {
    [](<https://adk.dev/graphs/routes/#__codelineno-14-35>)        return nil, fmt.Errorf("workflowB: %w", err)
    [](<https://adk.dev/graphs/routes/#__codelineno-14-36>)    }
    [](<https://adk.dev/graphs/routes/#__codelineno-14-37>)
    [](<https://adk.dev/graphs/routes/#__codelineno-14-38>)    // --- Outer graph ---
    [](<https://adk.dev/graphs/routes/#__codelineno-14-39>)    taskA1 := workflow.NewFunctionNode("task_A1",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-40>)        func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-14-41>)            return "Summary: " + strings.TrimSpace(input), nil
    [](<https://adk.dev/graphs/routes/#__codelineno-14-42>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-14-43>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-14-44>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-14-45>)
    [](<https://adk.dev/graphs/routes/#__codelineno-14-46>)    finalNode := workflow.NewFunctionNode("final_node",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-47>)        func(_ agent.Context, result string) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-14-48>)            return "Final: " + result, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-14-49>)        },
    [](<https://adk.dev/graphs/routes/#__codelineno-14-50>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/routes/#__codelineno-14-51>)    )
    [](<https://adk.dev/graphs/routes/#__codelineno-14-52>)
    [](<https://adk.dev/graphs/routes/#__codelineno-14-53>)    // workflow.NewAgentNode wraps workflowB so it can be placed as a node
    [](<https://adk.dev/graphs/routes/#__codelineno-14-54>)    // in the outer graph's edges slice.
    [](<https://adk.dev/graphs/routes/#__codelineno-14-55>)    innerNode, err := workflow.NewAgentNode(workflowB, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-14-56>)    if err != nil {
    [](<https://adk.dev/graphs/routes/#__codelineno-14-57>)        return nil, fmt.Errorf("NewAgentNode(workflowB): %w", err)
    [](<https://adk.dev/graphs/routes/#__codelineno-14-58>)    }
    [](<https://adk.dev/graphs/routes/#__codelineno-14-59>)
    [](<https://adk.dev/graphs/routes/#__codelineno-14-60>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-14-61>)        Name:        "parent_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-62>)        Description: "Runs task_A1 then the nested workflow_B then final_node.",
    [](<https://adk.dev/graphs/routes/#__codelineno-14-63>)        Edges:       workflow.Chain(workflow.Start, taskA1, innerNode, finalNode),
    [](<https://adk.dev/graphs/routes/#__codelineno-14-64>)        SubAgents:   []agent.Agent{workflowB},
    [](<https://adk.dev/graphs/routes/#__codelineno-14-65>)    })
    [](<https://adk.dev/graphs/routes/#__codelineno-14-66>)}
    
## Loop and escalation exit[¶](<https://adk.dev/graphs/routes/#loop-and-escalation-exit> "Permanent link")

A loop repeats a set of steps until a termination condition is met. In Python this is expressed as a back-edge in the `edges` graph that routes back to an earlier node. In ADK Go v2.0.0, the graph engine supports the same pattern directly: add an edge from a downstream node back to an earlier node with a route condition, and the engine re-activates the target node with a fresh lifecycle on each iteration.

PythonGo
    
    [](<https://adk.dev/graphs/routes/#__codelineno-15-1>)from google.adk import Event, Workflow
    [](<https://adk.dev/graphs/routes/#__codelineno-15-2>)
    [](<https://adk.dev/graphs/routes/#__codelineno-15-3>)
    [](<https://adk.dev/graphs/routes/#__codelineno-15-4>)def router(node_input: str):
    [](<https://adk.dev/graphs/routes/#__codelineno-15-5>)    """Route to task B or C based on node_input."""
    [](<https://adk.dev/graphs/routes/#__codelineno-15-6>)    if condition(node_input):
    [](<https://adk.dev/graphs/routes/#__codelineno-15-7>)        return Event(route="RUN_TASK_C")
    [](<https://adk.dev/graphs/routes/#__codelineno-15-8>)    return Event(route="RUN_TASK_B")
    [](<https://adk.dev/graphs/routes/#__codelineno-15-9>)
    [](<https://adk.dev/graphs/routes/#__codelineno-15-10>)root_agent = Workflow(
    [](<https://adk.dev/graphs/routes/#__codelineno-15-11>)    name="routing_workflow",
    [](<https://adk.dev/graphs/routes/#__codelineno-15-12>)    edges=[
    [](<https://adk.dev/graphs/routes/#__codelineno-15-13>)        ("START", task_A_node, router),
    [](<https://adk.dev/graphs/routes/#__codelineno-15-14>)        (router,
    [](<https://adk.dev/graphs/routes/#__codelineno-15-15>)          {
    [](<https://adk.dev/graphs/routes/#__codelineno-15-16>)            "RUN_TASK_B": task_B_node,
    [](<https://adk.dev/graphs/routes/#__codelineno-15-17>)            "RUN_TASK_C": task_C_node,
    [](<https://adk.dev/graphs/routes/#__codelineno-15-18>)          },
    [](<https://adk.dev/graphs/routes/#__codelineno-15-19>)        ),
    [](<https://adk.dev/graphs/routes/#__codelineno-15-20>)    ],
    [](<https://adk.dev/graphs/routes/#__codelineno-15-21>))
    
The following example uses the graph engine with `workflow.EdgeBuilder`. The critic node returns a verdict, a router node sets `Event.Routes`, and a back-edge from the refiner to the critic creates the loop. When the critic is satisfied it routes to the terminal `done` node instead:
    
    [](<https://adk.dev/graphs/routes/#__codelineno-16-1>)// draft carries the working document through the refinement loop.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-2>)type draft struct {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-3>)    Text string `json:"text"`
    [](<https://adk.dev/graphs/routes/#__codelineno-16-4>)}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-5>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-6>)// criticResult is emitted by the critic node with the review verdict and
    [](<https://adk.dev/graphs/routes/#__codelineno-16-7>)// optional suggestions. The router reads Verdict to set Event.Routes.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-8>)type criticResult struct {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-9>)    Verdict     string `json:"verdict"`     // "REFINE" or "DONE"
    [](<https://adk.dev/graphs/routes/#__codelineno-16-10>)    Suggestions string `json:"suggestions"` // non-empty when Verdict == "REFINE"
    [](<https://adk.dev/graphs/routes/#__codelineno-16-11>)}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-12>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-13>)// writeDraft is the initial writer node: produces the first draft from the
    [](<https://adk.dev/graphs/routes/#__codelineno-16-14>)// user's topic. Its typed return value becomes the input to the critic node
    [](<https://adk.dev/graphs/routes/#__codelineno-16-15>)// via Event.Output — no session state writes needed.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-16>)func writeDraft(_ agent.Context, topic string) (draft, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-17>)    // In a real workflow this would call an LLM; here we return a stub.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-18>)    return draft{Text: "Draft about " + topic + ": placeholder content."}, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-16-19>)}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-20>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-21>)// reviewDraft is the critic node: inspects the draft and returns a verdict.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-22>)// "DONE" exits the loop; "REFINE" triggers a back-edge to the refiner.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-23>)func reviewDraft(_ agent.Context, d draft) (criticResult, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-24>)    // Simulate a critic: approve once the draft contains "improved".
    [](<https://adk.dev/graphs/routes/#__codelineno-16-25>)    if strings.Contains(d.Text, "improved") {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-26>)        return criticResult{Verdict: "DONE"}, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-16-27>)    }
    [](<https://adk.dev/graphs/routes/#__codelineno-16-28>)    return criticResult{
    [](<https://adk.dev/graphs/routes/#__codelineno-16-29>)        Verdict:     "REFINE",
    [](<https://adk.dev/graphs/routes/#__codelineno-16-30>)        Suggestions: "Add more detail and mark the text as improved.",
    [](<https://adk.dev/graphs/routes/#__codelineno-16-31>)    }, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-16-32>)}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-33>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-34>)// routeVerdict reads the critic's verdict and sets Event.Routes so the
    [](<https://adk.dev/graphs/routes/#__codelineno-16-35>)// graph engine dispatches to either the refiner or the done node.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-36>)// Returning nil suppresses the automatic terminal event.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-37>)func routeVerdict(ctx agent.Context, r criticResult, emit func(*session.Event) error) (any, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-38>)    ev := session.NewEvent(ctx, ctx.InvocationID())
    [](<https://adk.dev/graphs/routes/#__codelineno-16-39>)    ev.Routes = []string{r.Verdict}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-40>)    ev.Output = r // forward the full result to the chosen successor
    [](<https://adk.dev/graphs/routes/#__codelineno-16-41>)    if err := emit(ev); err != nil {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-42>)        return nil, err
    [](<https://adk.dev/graphs/routes/#__codelineno-16-43>)    }
    [](<https://adk.dev/graphs/routes/#__codelineno-16-44>)    return nil, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-16-45>)}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-46>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-47>)// refineDraft applies the critic's suggestions and returns the improved draft.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-48>)// Its output feeds back to the critic node via the back-edge.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-49>)func refineDraft(_ agent.Context, r criticResult) (draft, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-50>)    return draft{Text: "improved draft incorporating: " + r.Suggestions}, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-16-51>)}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-52>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-53>)// reportDone is the terminal node, reached only when the critic is satisfied.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-54>)func reportDone(_ agent.Context, r criticResult) (string, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-55>)    return "Refinement complete. Final verdict: " + r.Verdict, nil
    [](<https://adk.dev/graphs/routes/#__codelineno-16-56>)}
    [](<https://adk.dev/graphs/routes/#__codelineno-16-57>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-58>)// newLoopEscalate builds an iterative document-refinement workflow using the
    [](<https://adk.dev/graphs/routes/#__codelineno-16-59>)// graph engine. The critic node emits a route ("REFINE" or "DONE") and the
    [](<https://adk.dev/graphs/routes/#__codelineno-16-60>)// engine dispatches to either the refiner (which loops back to the critic via
    [](<https://adk.dev/graphs/routes/#__codelineno-16-61>)// a back-edge) or the terminal done node.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-62>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-16-63>)// Graph topology:
    [](<https://adk.dev/graphs/routes/#__codelineno-16-64>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-16-65>)//  START → writer → critic → router ─┬─ "REFINE" → refiner ──┐
    [](<https://adk.dev/graphs/routes/#__codelineno-16-66>)//                                     └─ "DONE"   → done       │
    [](<https://adk.dev/graphs/routes/#__codelineno-16-67>)//                   ▲_______________________________┘ (back-edge)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-68>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-16-69>)// Python equivalent:
    [](<https://adk.dev/graphs/routes/#__codelineno-16-70>)//
    [](<https://adk.dev/graphs/routes/#__codelineno-16-71>)//  edges=[
    [](<https://adk.dev/graphs/routes/#__codelineno-16-72>)//      ("START", writer_node, critic_node, router),
    [](<https://adk.dev/graphs/routes/#__codelineno-16-73>)//      (router, {"REFINE": refiner_node, "DONE": done_node}),
    [](<https://adk.dev/graphs/routes/#__codelineno-16-74>)//      (refiner_node, critic_node),  # back-edge creates the loop
    [](<https://adk.dev/graphs/routes/#__codelineno-16-75>)//  ]
    [](<https://adk.dev/graphs/routes/#__codelineno-16-76>)func newLoopEscalate() (agent.Agent, error) {
    [](<https://adk.dev/graphs/routes/#__codelineno-16-77>)    writerNode := workflow.NewFunctionNode("writer", writeDraft, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-16-78>)    criticNode := workflow.NewFunctionNode("critic", reviewDraft, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-16-79>)    routerNode := workflow.NewEmittingFunctionNode("router", routeVerdict, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-16-80>)    refinerNode := workflow.NewFunctionNode("refiner", refineDraft, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-16-81>)    doneNode := workflow.NewFunctionNode("done", reportDone, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/routes/#__codelineno-16-82>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-83>)    // Build the edges. The back-edge from refinerNode to criticNode creates
    [](<https://adk.dev/graphs/routes/#__codelineno-16-84>)    // the loop; the graph engine re-activates criticNode with a fresh
    [](<https://adk.dev/graphs/routes/#__codelineno-16-85>)    // lifecycle on each iteration.
    [](<https://adk.dev/graphs/routes/#__codelineno-16-86>)    eb := workflow.NewEdgeBuilder()
    [](<https://adk.dev/graphs/routes/#__codelineno-16-87>)    eb.Add(workflow.Start, writerNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-88>)    eb.Add(writerNode, criticNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-89>)    eb.Add(criticNode, routerNode)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-90>)    eb.AddRoute(routerNode, refinerNode, workflow.StringRoute("REFINE"))
    [](<https://adk.dev/graphs/routes/#__codelineno-16-91>)    eb.AddRoute(routerNode, doneNode, workflow.StringRoute("DONE"))
    [](<https://adk.dev/graphs/routes/#__codelineno-16-92>)    eb.AddRoute(refinerNode, criticNode, workflow.Default) // back-edge: loop back for another review
    [](<https://adk.dev/graphs/routes/#__codelineno-16-93>)
    [](<https://adk.dev/graphs/routes/#__codelineno-16-94>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/routes/#__codelineno-16-95>)        Name:        "iterative_writer",
    [](<https://adk.dev/graphs/routes/#__codelineno-16-96>)        Description: "Writes then iteratively refines a document using a critic/refiner loop.",
    [](<https://adk.dev/graphs/routes/#__codelineno-16-97>)        Edges:       eb.Build(),
    [](<https://adk.dev/graphs/routes/#__codelineno-16-98>)    })
    [](<https://adk.dev/graphs/routes/#__codelineno-16-99>)}
    
Back to top 