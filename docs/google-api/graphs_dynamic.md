# Dynamic workflows - Agent Development Kit (ADK)

> Source: [https://adk.dev/graphs/dynamic/](https://adk.dev/graphs/dynamic/)

[ Skip to content ](<https://adk.dev/graphs/dynamic/#dynamic-agent-workflows>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/graphs/dynamic.md> "Edit this page on GitHub") [ ](<https://adk.dev/graphs/dynamic/index.md> "View this page as Markdown")

# Dynamic agent workflows[¶](<https://adk.dev/graphs/dynamic/#dynamic-agent-workflows> "Permanent link")

Supported in ADKPython v2.0.0Go v2.0.0

The ADK framework provides a programmatic way to define workflows as a more flexible and powerful alternative to [graph-based workflows](<https://adk.dev/graphs/>). Using a graph-based approach provides a convenient way to compose multi-step, static process structures with workflow nodes. However, if the logic path for your workflow is more complex, with iterative loops or complex branching logic, a graph-based approach may not suit your needs, or may become too unwieldy to manage.

Dynamic workflows in ADK allow you to put aside graph-based path structures and use the full power of your chosen programming language to build workflows. With dynamic workflows, you can create workflows with simple decorators (Python) or constructor functions (Go), invoke workflow nodes as functions, and build complex routing logic. Here are some of the benefits of dynamic workflows in ADK:

  * **Flexible Control Flow:** Define execution order dynamically using loops, conditionals, and recursion which are difficult or impossible to represent in static graphs.
  * **Programmatic Experience:** Use familiar constructs like `while` loops and `async/await` (Python) or `for` loops and `workflow.RunNode` (Go) instead of graph-based routing.
  * **Automatic Checkpointing:** Dynamic workflows track each node execution. Successful sub-nodes are automatically skipped when resuming the workflow, making complex logic durable and resumable by default.
  * **Encapsulation:** Wrap business logic into _parent_ nodes that internally compose lower-level nodes, keeping the overall workflow clean and manageable.

## Get started[¶](<https://adk.dev/graphs/dynamic/#get-started> "Permanent link")

The following dynamic workflow code example shows how to define a basic workflow containing a single node with a function:

PythonGo
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-1>)from google.adk import Context
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-2>)from google.adk import Workflow
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-3>)from google.adk.workflow import node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-4>)from typing import Any
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-5>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-6>)@node(name="hello_node")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-7>)def my_node(node_input: Any):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-8>)    return "Hello World"
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-9>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-10>)# define a dynamic workflow node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-11>)@node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-12>)async def my_workflow(ctx: Context, node_input: str) -> str:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-13>)    # run_node executes a node and returns its output
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-14>)    result = await ctx.run_node(my_node, node_input="hello")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-15>)    return result
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-16>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-17>)# Run the workflow
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-18>)root_agent = Workflow(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-19>)    name="root_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-20>)    edges=[("START", my_workflow)],
    [](<https://adk.dev/graphs/dynamic/#__codelineno-0-21>))
    
This example uses the [**_@node_**](<https://adk.dev/graphs/dynamic/#node>) annotation for convenience and to keep the written code as simple as possible. This annotation generates wrappers that allow the code to be run in the context of an ADK dynamic workflow.

In Go, `workflow.NewFunctionNode` replaces the `@node` decorator and `workflow.NewDynamicNode` replaces the `@node(rerun_on_resume=True)` async orchestrator. `workflow.RunNode` is the direct equivalent of `ctx.run_node()`. `workflowagent.New` with `workflow.Chain` replaces `Workflow(edges=[...])`.

Resume behaviour after a human-in-the-loop pause is controlled by `NodeConfig.RerunOnResume` — see [Nodes](<https://adk.dev/graphs/dynamic/#node>) below for details.
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-1>)// helloNode is a simple FunctionNode that returns "Hello World".
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-2>)// In Python this would be written as:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-3>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-4>)//  @node(name="hello_node")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-5>)//  def my_node(node_input: Any):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-6>)//      return "Hello World"
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-7>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-8>)// In Go, workflow.NewFunctionNode wraps the same logic with the
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-9>)// required node interface, inferring input and output types from
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-10>)// the generic parameters.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-11>)var helloNode = workflow.NewFunctionNode("hello_node",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-12>)    func(_ agent.Context, _ string) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-13>)        return "Hello World", nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-14>)    },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-15>)    workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-16>))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-17>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-18>)// myWorkflow is a dynamic orchestrator node. It calls workflow.RunNode
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-19>)// to schedule helloNode as a child and returns its output.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-20>)// In Python this would be:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-21>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-22>)//  @node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-23>)//  async def my_workflow(ctx: Context, node_input: str) -> str:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-24>)//      result = await ctx.run_node(my_node, node_input="hello")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-25>)//      return result
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-26>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-27>)// workflow.NewDynamicNode defaults RerunOnResume to &true, matching the
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-28>)// Python @node(rerun_on_resume=True) behaviour.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-29>)var myWorkflow = workflow.NewDynamicNode[string, string]("my_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-30>)    func(ctx agent.Context, _ string, _ func(*session.Event) error) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-31>)        return workflow.RunNode[string](ctx, helloNode, "hello")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-32>)    },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-33>)    workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-34>))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-35>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-36>)func runGetStarted() error {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-37>)    ctx := context.Background()
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-38>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-39>)    // workflowagent.New creates an agent.Agent backed by the workflow engine.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-40>)    // workflow.Chain(workflow.Start, myWorkflow) produces the edges slice
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-41>)    // equivalent to Python's edges=[("START", my_workflow)].
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-42>)    wa, err := workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-43>)        Name:        "root_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-44>)        Description: "A minimal dynamic workflow.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-45>)        Edges:       workflow.Chain(workflow.Start, myWorkflow),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-46>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-47>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-48>)        return fmt.Errorf("workflowagent.New: %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-49>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-50>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-51>)    l := full.NewLauncher()
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-52>)    return l.Execute(ctx, &launcher.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-53>)        AgentLoader: agent.NewSingleLoader(wa),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-54>)    }, os.Args[1:])
    [](<https://adk.dev/graphs/dynamic/#__codelineno-1-55>)}
    
## Building blocks: nodes and workflows[¶](<https://adk.dev/graphs/dynamic/#building-blocks-nodes-and-workflows> "Permanent link")

Nodes and workflows represent the basic building blocks of ADK's dynamic workflows. These types and functions provide the functionality required to wrap your code so it can be integrated into code-based workflows in ADK.

### Nodes[¶](<https://adk.dev/graphs/dynamic/#node> "Permanent link")

A dynamic workflow in ADK is composed of _nodes_. A simple version of a usable workflow node wraps a plain function with the metadata required to run within a workflow.

PythonGo

In Python, the **_@node_** annotation generates the node wrapper, keeping boilerplate to a minimum:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-2-1>)@node(name="hello_node")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-2-2>)def my_function_node(node_input: Any):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-2-3>)    return "Hello World"
    
The following code snippet shows the equivalent code _without_ the **_@node_** annotation:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-1>)# base function
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-2>)def my_function_node(node_input: Any):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-3>)    return "Hello World"
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-4>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-5>)# FunctionNode wrapper with options
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-6>)success_node = FunctionNode(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-7>)    my_function_node,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-8>)    name="hello",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-9>)    rerun_on_resume=True,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-3-10>))
    
Creating the node wrapper code yourself can be useful if you are wrapping functions from an external library, need to create multiple nodes from the same function with different configurations, or if you are managing node references in a registry for advanced orchestration.

In Go, `workflow.NewFunctionNode[IN, OUT]` wraps a plain function as a workflow node, inferring input and output types from the generic parameters. There is no decorator syntax; the node is a value that you pass as a child to `workflow.RunNode` inside a dynamic orchestrator:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-1>)// myFunctionNode demonstrates the explicit NewFunctionNode constructor —
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-2>)// equivalent to wrapping a function in a FunctionNode manually in Python:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-3>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-4>)//  success_node = FunctionNode(my_function_node, name="hello", rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-5>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-6>)// Creating the node directly (rather than via @node) is useful when you
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-7>)// need multiple nodes from the same function with different configurations,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-8>)// or when wrapping functions from an external library.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-9>)var myFunctionNode = workflow.NewFunctionNode("hello",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-10>)    func(_ agent.Context, _ any) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-11>)        return "Hello World", nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-12>)    },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-13>)    workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-14>))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-15>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-16>)// myFormattingNode is a second function node that the dynamic orchestrator
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-17>)// calls in sequence, mirroring:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-18>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-19>)//  result_formatted = await ctx.run_node(my_formatting_node, node_input=result)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-20>)var myFormattingNode = workflow.NewFunctionNode("format",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-21>)    func(_ agent.Context, in string) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-22>)        return fmt.Sprintf("[formatted] %s", in), nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-23>)    },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-24>)    workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-4-25>))
    
`NodeConfig` holds the same options as Python's `@node` arguments. The most important field is `RerunOnResume *bool`, which controls what happens when a workflow resumes after a human-in-the-loop pause:

  * **`&true` (re-entry mode)**: the interrupted node is re-run from the beginning on resume. Use this for dynamic orchestrator nodes that call `workflow.RunNode` in a loop — the body re-executes and already-completed child activations are skipped automatically (checkpointing). This mirrors Python's `@node(rerun_on_resume=True)`.
  * **`&false` (handoff mode)**: the resume payload is routed directly to the node's successor as input, bypassing the interrupted node entirely. Use this for leaf nodes that simply emit a pause event and expect the human response to flow to the next step.
  * **`nil`** : the default depends on node type. `workflow.NewDynamicNode` automatically sets `nil → &true` (re-entry mode), because an orchestrator body must be re-entered on resume to deliver cached child results. `workflow.NewFunctionNode` and other leaf node constructors leave `nil` as-is, which the engine treats as handoff (`&false`). Explicit `&false` is always respected on any node type.

    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-1>)// NewDynamicNode: nil RerunOnResume is automatically set to &true.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-2>)// Passing &rerun explicitly is equivalent and makes the intent clear.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-3>)rerun := true
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-4>)orchestratorNode := workflow.NewDynamicNode[string, string]("my_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-5>)    myOrchestratorfn,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-6>)    workflow.NodeConfig{RerunOnResume: &rerun}, // re-entry: node body re-runs on resume
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-7>))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-8>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-9>)// NewFunctionNode: nil RerunOnResume stays nil → engine treats as handoff.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-10>)handoffNode := workflow.NewFunctionNode("leaf_node",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-11>)    myLeafFn,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-12>)    workflow.NodeConfig{}, // nil RerunOnResume → handoff for FunctionNode
    [](<https://adk.dev/graphs/dynamic/#__codelineno-5-13>))
    
### Workflows[¶](<https://adk.dev/graphs/dynamic/#workflows> "Permanent link")

In an ADK dynamic workflow, you use a dynamic node as the primary orchestrator for nodes. A dynamic node manages running child nodes and the execution logic (order and paths) for those nodes.

PythonGo
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-1>)@node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-2>)async def my_workflow(ctx):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-3>)    # run_node executes a node and returns its output
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-4>)    result = await ctx.run_node(my_function_node, node_input="Hello")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-5>)    result_formatted = await ctx.run_node(my_formatting_node, node_input=result)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-6>)    return result_formatted
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-7>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-8>)# Run the workflow
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-9>)root_agent = Workflow(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-10>)    name="root_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-11>)    edges=[("START", my_workflow)],
    [](<https://adk.dev/graphs/dynamic/#__codelineno-6-12>))
    
`workflow.NewDynamicNode` creates an orchestrator whose body calls `workflow.RunNode` for each child step. `workflowagent.New` with `workflow.Chain(workflow.Start, myWorkflow)` is the equivalent of `Workflow(edges=[("START", my_workflow)])`:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-1>)// orchestratorWorkflow is a dynamic node that schedules two children in
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-2>)// sequence via workflow.RunNode, equivalent to:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-3>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-4>)//  @node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-5>)//  async def my_workflow(ctx):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-6>)//      result = await ctx.run_node(my_function_node, node_input="Hello")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-7>)//      result_formatted = await ctx.run_node(my_formatting_node, node_input=result)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-8>)//      return result_formatted
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-9>)var orchestratorWorkflow = workflow.NewDynamicNode[string, string]("my_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-10>)    func(ctx agent.Context, _ string, _ func(*session.Event) error) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-11>)        result, err := workflow.RunNode[string](ctx, myFunctionNode, "Hello")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-12>)        if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-13>)            return "", err
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-14>)        }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-15>)        return workflow.RunNode[string](ctx, myFormattingNode, result)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-16>)    },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-17>)    workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-7-18>))
    
## Data handling[¶](<https://adk.dev/graphs/dynamic/#data-handling> "Permanent link")

When using dynamic workflows with ADK, passing data is simpler than [graph-based workflows](<https://adk.dev/graphs/>) because `workflow.RunNode` returns the child node's output directly as a typed Go value — eliminating the need to manually read and write session state keys for data transfer.

PythonGo
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-1>)from google.adk import Context
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-2>)from google.adk.workflow import node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-3>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-4>)@node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-5>)async def editorial_workflow(ctx: Context, user_request: str):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-6>)    # Agent Node generates output
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-7>)    raw_draft = await ctx.run_node(draft_agent, user_request)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-8>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-9>)    # Function Node formats text
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-10>)    formatted_text = await ctx.run_node(format_function_node, raw_draft)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-11>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-8-12>)    return formatted_text
    
You can also pass specific data schemas using a defined class and configure input and output schemas, similar to graph-based workflow nodes:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-1>)from google.adk import Agent
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-2>)from google.adk import Context
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-3>)from google.adk.workflow import node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-4>)from pydantic import BaseModel
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-5>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-6>)class CityTime(BaseModel):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-7>)    time_info: str  # time information
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-8>)    city: str       # city name
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-9>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-10>)@node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-11>)def city_time_function(city: str):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-12>)    """Simulate returning the current time in a specified city."""
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-13>)    return CityTime(time_info="10:10 AM", city=city)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-14>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-15>)city_report_agent = Agent(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-16>)    name="city_report_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-17>)    model="gemini-flash-latest",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-18>)    input_schema=CityTime,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-19>)    instruction="""output the data provided by the previous node.""",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-20>))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-21>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-22>)@node # workflow node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-23>)async def city_workflow(ctx: Context):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-24>)    city_time = await ctx.run_node(city_time_function, "Paris")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-25>)    report_text = await ctx.run_node(city_report_agent, city_time)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-26>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-9-27>)    return report_text
    
In Go, `workflow.NewAgentNode` wraps an `agent.Agent` so it can be invoked via `workflow.RunNode` inside a dynamic orchestrator. The output of each `RunNode` call is returned as a typed value — no session state reads are required:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-1>)// newDataHandlingWorkflow demonstrates how to pass data between a dynamic
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-2>)// orchestrator and an LlmAgent-backed node. workflow.NewAgentNode wraps an
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-3>)// agent.Agent so it can be invoked via workflow.RunNode.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-4>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-5>)// In Python this mirrors:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-6>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-7>)//  city_report_agent = Agent(name="city_report_agent", ...)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-8>)//  @node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-9>)//  async def city_workflow(ctx: Context):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-10>)//      city_time = await ctx.run_node(city_time_function, "Paris")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-11>)//      report_text = await ctx.run_node(city_report_agent, city_time)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-12>)//      return report_text
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-13>)func newDataHandlingWorkflow(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-14>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-15>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-16>)        return nil, fmt.Errorf("gemini.NewModel: %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-17>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-18>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-19>)    // cityTimeNode is a FunctionNode that returns a formatted city-time string.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-20>)    cityTimeNode := workflow.NewFunctionNode("city_time_function",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-21>)        func(_ agent.Context, city string) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-22>)            return fmt.Sprintf("10:10 AM in %s", city), nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-23>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-24>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-25>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-26>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-27>)    // cityReportAgent is an LlmAgent that receives the city-time string and
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-28>)    // produces a human-friendly report.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-29>)    cityReportAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-30>)        Name:        "city_report_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-31>)        Model:       model,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-32>)        Description: "Reports city time information.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-33>)        Instruction: "Output the data provided by the previous node in a friendly sentence.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-34>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-35>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-36>)        return nil, fmt.Errorf("llmagent.New (cityReport): %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-37>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-38>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-39>)    // workflow.NewAgentNode wraps cityReportAgent so it can be called from
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-40>)    // inside a dynamic node via workflow.RunNode.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-41>)    cityReportNode, err := workflow.NewAgentNode(cityReportAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-42>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-43>)        return nil, fmt.Errorf("workflow.NewAgentNode: %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-44>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-45>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-46>)    cityWorkflow := workflow.NewDynamicNode[string, string]("city_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-47>)        func(ctx agent.Context, _ string, _ func(*session.Event) error) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-48>)            cityTime, err := workflow.RunNode[string](ctx, cityTimeNode, "Paris")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-49>)            if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-50>)                return "", err
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-51>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-52>)            return workflow.RunNode[string](ctx, cityReportNode, cityTime)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-53>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-54>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-55>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-56>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-57>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-58>)        Name:      "data_handling_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-59>)        SubAgents: []agent.Agent{cityReportAgent},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-60>)        Edges:     workflow.Chain(workflow.Start, cityWorkflow),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-61>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-10-62>)}
    
For more information on data handling between workflow nodes, see [Data handling for agent workflows](<https://adk.dev/graphs/data-handling/>).

## Workflow routes[¶](<https://adk.dev/graphs/dynamic/#workflow-routes> "Permanent link")

Dynamic workflows in ADK provide more flexibility in terms of routing logic compared to [graph-based workflows](<https://adk.dev/graphs/>), including iterative loops or more complex branching logic. This section describes some of the techniques that you can use for routing.

### Sequence route[¶](<https://adk.dev/graphs/dynamic/#sequence-route> "Permanent link")

You can create sequential task processing with dynamic workflows in ADK, just as you can with graph-based workflows.

PythonGo

The following code snippet shows a dynamic workflow with an agent, a function node, and a second agent:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-11-1>)@node # workflow node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-11-2>)async def city_workflow(ctx: Context):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-11-3>)    city = await ctx.run_node(city_generator_agent)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-11-4>)    city_time = await ctx.run_node(city_time_function, city)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-11-5>)    report_text = await ctx.run_node(city_report_agent, city_time)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-11-6>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-11-7>)    return report_text
    
Call `workflow.RunNode` sequentially inside a `NewDynamicNode` body — each call awaits the child before the next one starts. The [data handling example above](<https://adk.dev/graphs/dynamic/#data-handling>) demonstrates exactly this pattern: `cityWorkflow` calls `workflow.RunNode` for `cityTimeNode` and then `cityReportNode` in order, passing each node's typed output to the next.

### Loop route[¶](<https://adk.dev/graphs/dynamic/#loop-route> "Permanent link")

For workflows where you want to use an iterative loop for a task, dynamic workflows offer much more flexibility to define the routing logic you need.

PythonGo

The following code example shows how to use dynamic workflows to construct a workflow loop for generating, reviewing, and updating code:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-1>)from google.adk import Context
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-2>)from google.adk import Event
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-3>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-4>)from google.adk.workflow import node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-5>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-6>)coder_agent = LlmAgent(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-7>)    name="generator_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-8>)    model="gemini-flash-latest",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-9>)    instruction="Write python code for user request.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-10>)    output_schema=str,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-11>))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-12>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-13>)@node(name="lint_reviewer")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-14>)async def compile_lint_check(ctx: Context, code: str):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-15>)    # Simulate API call or lint check
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-16>)    class Response:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-17>)        findings = ""
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-18>)    return Response()
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-19>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-20>)fixer_agent = LlmAgent(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-21>)    name="fixer_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-22>)    model="gemini-flash-latest",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-23>)    instruction="""Refactor current code {code}.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-24>)        Based on compile & lint review: {findings}""",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-25>)    output_schema=str,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-26>))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-27>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-28>)@node # workflow node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-29>)async def code_workflow(ctx: Context, user_request: str):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-30>)  code = await ctx.run_node(coder_agent, user_request)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-31>)  check_resp = await ctx.run_node(compile_lint_check, code)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-32>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-33>)  while check_resp.findings:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-34>)    yield Event(state={"code": code, "findings": check_resp.findings})
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-35>)    code = await ctx.run_node(fixer_agent, {"code": code, "findings": check_resp.findings})
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-36>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-37>)    check_resp = await ctx.run_node(compile_lint_check, code)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-38>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-12-39>)  return code
    
In Go, the loop is a plain `for` loop inside the dynamic node body. The lint check node returns an empty string when there are no findings, which signals the loop to exit:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-1>)// newLoopWorkflow demonstrates an iterative loop inside a dynamic node.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-2>)// The orchestrator body uses a plain Go for loop to keep calling the
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-3>)// lintCheckNode until there are no findings — equivalent to Python's:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-4>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-5>)//  @node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-6>)//  async def code_workflow(ctx: Context, user_request: str):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-7>)//      code = await ctx.run_node(coder_agent, user_request)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-8>)//      check_resp = await ctx.run_node(compile_lint_check, code)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-9>)//      while check_resp.findings:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-10>)//          code = await ctx.run_node(fixer_agent, ...)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-11>)//          check_resp = await ctx.run_node(compile_lint_check, code)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-12>)//      return code
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-13>)func newLoopWorkflow(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-14>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-15>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-16>)        return nil, fmt.Errorf("gemini.NewModel: %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-17>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-18>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-19>)    coderAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-20>)        Name:        "generator_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-21>)        Model:       model,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-22>)        Description: "Writes Go code for the user request.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-23>)        Instruction: "Write Go code for the user request. Output only the code.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-24>)        OutputKey:   "generated_code",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-25>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-26>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-27>)        return nil, fmt.Errorf("llmagent.New (coder): %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-28>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-29>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-30>)    coderNode, err := workflow.NewAgentNode(coderAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-31>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-32>)        return nil, fmt.Errorf("workflow.NewAgentNode (coder): %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-33>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-34>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-35>)    // lintCheckNode simulates a lint/compile check. It returns an empty
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-36>)    // string when there are no findings, signalling the loop to exit.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-37>)    lintCheckNode := workflow.NewFunctionNode("lint_reviewer",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-38>)        func(_ agent.Context, code string) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-39>)            // Simulate a lint check: return findings or empty string when clean.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-40>)            if len(code) < 50 {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-41>)                return "Code is too short; add error handling.", nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-42>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-43>)            return "", nil // no findings — loop exits
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-44>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-45>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-46>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-47>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-48>)    fixerAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-49>)        Name:        "fixer_agent",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-50>)        Model:       model,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-51>)        Description: "Refactors code based on lint findings.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-52>)        Instruction: "Refactor the provided code to address the review findings. Output only the improved code.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-53>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-54>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-55>)        return nil, fmt.Errorf("llmagent.New (fixer): %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-56>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-57>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-58>)    fixerNode, err := workflow.NewAgentNode(fixerAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-59>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-60>)        return nil, fmt.Errorf("workflow.NewAgentNode (fixer): %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-61>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-62>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-63>)    codeWorkflow := workflow.NewDynamicNode[string, string]("code_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-64>)        func(ctx agent.Context, userRequest string, _ func(*session.Event) error) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-65>)            code, err := workflow.RunNode[string](ctx, coderNode, userRequest)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-66>)            if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-67>)                return "", err
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-68>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-69>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-70>)            findings, err := workflow.RunNode[string](ctx, lintCheckNode, code)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-71>)            if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-72>)                return "", err
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-73>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-74>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-75>)            // Loop until the lint check reports no findings.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-76>)            for findings != "" {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-77>)                code, err = workflow.RunNode[string](ctx, fixerNode, code)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-78>)                if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-79>)                    return "", err
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-80>)                }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-81>)                findings, err = workflow.RunNode[string](ctx, lintCheckNode, code)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-82>)                if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-83>)                    return "", err
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-84>)                }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-85>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-86>)            return code, nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-87>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-88>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-89>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-90>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-91>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-92>)        Name:      "code_pipeline",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-93>)        SubAgents: []agent.Agent{coderAgent, fixerAgent},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-94>)        Edges:     workflow.Chain(workflow.Start, codeWorkflow),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-95>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-13-96>)}
    
### Parallel execution routes[¶](<https://adk.dev/graphs/dynamic/#parallel-execution-routes> "Permanent link")

Dynamic workflows in ADK can support parallel execution.

PythonGo

In Python, you can use `asyncio.gather` to build parallel execution:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-1>)import asyncio
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-2>)from typing import Any
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-3>)from google.adk import Context
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-4>)from google.adk.workflow import BaseNode, node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-5>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-6>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-7>)@node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-8>)async def parallel_supervisor(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-9>)    ctx: Context, node_input: list[Any], real_node: BaseNode
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-10>)):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-11>)    """Runs a worker node in parallel for each item in the input list."""
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-12>)    tasks = []
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-13>)    for item in node_input:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-14>)        # ctx.run_node returns a future. Append instead of awaiting immediately.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-15>)        tasks.append(ctx.run_node(real_node, item))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-16>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-17>)    # Collect all results in parallel
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-18>)    results = await asyncio.gather(*tasks)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-14-19>)    return results
    
Tip: Resuming parallel nodes

The workflow framework ensures that if a dynamic workflow is resumed, only failed or interrupted worker nodes are re-executed, including parallel worker nodes.

In Go, `workflow.NewParallelWorker` wraps a child node and runs it concurrently for each element of a list input, collecting results into a single output slice. The `maxConcurrency` parameter caps how many concurrent activations may run simultaneously; `0` means unlimited:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-1>)// newParallelWorkflow demonstrates parallel execution using
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-2>)// workflow.NewParallelWorker. The worker node runs a wrapped child node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-3>)// concurrently for each element in a list input, collecting results.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-4>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-5>)// This is the Go equivalent of using asyncio.gather in Python:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-6>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-7>)//  @node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-8>)//  async def parallel_supervisor(ctx, node_input, real_node):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-9>)//      tasks = [ctx.run_node(real_node, item) for item in node_input]
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-10>)//      results = await asyncio.gather(*tasks)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-11>)//      return results
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-12>)func newParallelWorkflow() (agent.Agent, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-13>)    // workerNode processes a single item. NewParallelWorker will call it
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-14>)    // once per element of the list input, concurrently.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-15>)    workerNode := workflow.NewFunctionNode("worker",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-16>)        func(_ agent.Context, item string) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-17>)            return fmt.Sprintf("processed: %s", item), nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-18>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-19>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-20>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-21>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-22>)    // NewParallelWorker wraps workerNode so it runs concurrently for each
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-23>)    // element of a []string input. maxConcurrency=0 means unlimited.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-24>)    parallelWorker, err := workflow.NewParallelWorker(
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-25>)        "parallel_supervisor",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-26>)        workerNode,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-27>)        0, // maxConcurrency: 0 = unlimited
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-28>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-29>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-30>)    if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-31>)        return nil, fmt.Errorf("workflow.NewParallelWorker: %w", err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-32>)    }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-33>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-34>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-35>)        Name:        "parallel_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-36>)        Description: "Runs a worker node in parallel for each item in the input list.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-37>)        Edges:       workflow.Chain(workflow.Start, parallelWorker),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-38>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-15-39>)}
    
Tip: Resuming parallel nodes

The workflow framework ensures that if a dynamic workflow is resumed, only failed or interrupted worker nodes are re-executed, including parallel worker nodes managed by `NewParallelWorker`.

## Human input[¶](<https://adk.dev/graphs/dynamic/#human-input> "Permanent link")

Dynamic workflows in ADK can also include human input or human in the loop (HITL) steps.

PythonGo

You build human input into workflows by yielding a **_RequestInput_** from a node, which pauses the workflow and waits for user input. The following code example shows how to build a human input node and include it in a workflow:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-1>)from typing import Any
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-2>)from google.adk import Context
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-3>)from google.adk.events import RequestInput
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-4>)from google.adk.workflow import node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-5>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-6>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-7>)@node(rerun_on_resume=False)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-8>)async def get_user_approval(ctx: Context, node_input: Any):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-9>)    """Yields a RequestInput to pause the workflow and wait for user input."""
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-10>)    yield RequestInput(message="Please approve this request (Yes/No)")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-11>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-12>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-13>)@node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-14>)async def handle_process(ctx: Context, node_input: Any):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-15>)    """The orchestrator calling the interactive step."""
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-16>)    user_response = await ctx.run_node(get_user_approval)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-17>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-18>)    if user_response.lower() == "yes":
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-19>)        return "Approved"
    [](<https://adk.dev/graphs/dynamic/#__codelineno-16-20>)    return "Denied"
    
Important: Parent nodes with `ctx.run_node`

Parent nodes in dynamic workflows that call `ctx.run_node` must set `rerun_on_resume=True` to handle interruptions properly.

In Go, use `workflow.NewEmittingFunctionNode` with `workflow.ResumeOrRequestInput` to implement the re-entry HITL pattern. On the first pass `ResumeOrRequestInput` emits a `session.RequestInput` event and returns `ErrNodeInterrupted`, pausing the workflow. After the human replies, the node is re-run from the top (`RerunOnResume: &true`) and `ResumeOrRequestInput` returns the human's reply directly:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-1>)// newHITLWorkflow demonstrates the re-entry HITL pattern using
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-2>)// workflow.ResumeOrRequestInput. On the first pass the node emits a
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-3>)// RequestInput event and returns ErrNodeInterrupted (pausing the workflow).
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-4>)// After the human replies, the same node is re-run from the top
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-5>)// (RerunOnResume=&true) and ResumeOrRequestInput returns the human's reply.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-6>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-7>)// In Python this is equivalent to:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-8>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-9>)//  @node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-10>)//  async def get_user_approval(ctx, node_input):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-11>)//      yield RequestInput(message="Please approve this request (Yes/No)")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-12>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-13>)//  @node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-14>)//  async def handle_process(ctx, node_input):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-15>)//      user_response = await ctx.run_node(get_user_approval)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-16>)//      if user_response.lower() == "yes":
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-17>)//          return "Approved"
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-18>)//      return "Denied"
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-19>)func newHITLWorkflow() (agent.Agent, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-20>)    rerun := true
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-21>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-22>)    // approvalNode pauses on the first pass to ask the user for a Yes/No
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-23>)    // approval, then resolves their decision on resume.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-24>)    // workflow.ResumeOrRequestInput handles both phases.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-25>)    approvalNode := workflow.NewEmittingFunctionNode[any, any]("get_user_approval",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-26>)        func(nc agent.Context, _ any, emit func(*session.Event) error) (any, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-27>)            // ResumeOrRequestInput: on first pass, emits the prompt and
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-28>)            // returns ErrNodeInterrupted. On re-run after the human replies,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-29>)            // it returns the reply payload directly.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-30>)            reply, err := workflow.ResumeOrRequestInput(nc, emit, session.RequestInput{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-31>)                InterruptID: "user_approval",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-32>)                Message:     "Please approve this request (Yes/No)",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-33>)            })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-34>)            if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-35>)                return nil, err
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-36>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-37>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-38>)            response, _ := reply.(string)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-39>)            if response == "" {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-40>)                response = "No"
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-41>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-42>)            if response == "yes" || response == "Yes" {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-43>)                return "Approved", nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-44>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-45>)            return "Denied", nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-46>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-47>)        workflow.NodeConfig{RerunOnResume: &rerun},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-48>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-49>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-50>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-51>)        Name:        "hitl_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-52>)        Description: "Pauses for user approval before completing a task.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-53>)        Edges:       workflow.Chain(workflow.Start, approvalNode),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-54>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-17-55>)}
    
## Advanced features[¶](<https://adk.dev/graphs/dynamic/#advanced-features> "Permanent link")

Dynamic workflows offer some advanced features designed to handle more complex development scenarios. These capabilities allow for finer control over execution and better integration with existing technical infrastructure.

### Execution IDs[¶](<https://adk.dev/graphs/dynamic/#execution-ids> "Permanent link")

The ADK framework generates a deterministic identifier (ID) for child node executions based on the parent ID and a counter. ADK workflows use deterministic IDs for each scheduled node to identify previous results. These IDs are generated based on the order of dynamic node schedules, and are used for checkpointing and to re-run tasks in the correct order in the case of a resumed or re-run workflow.

#### Custom execution IDs[¶](<https://adk.dev/graphs/dynamic/#custom-execution-ids> "Permanent link")

In some rare cases, you may need to have stable identifiers, such as when processing a reorderable list. In general, you should avoid this due to the impacts to workflow task retries and process resumes. Specifically, these IDs are used to check node states and skip execution if a node was already run. If you provide custom IDs, make sure they are deterministic for workflow re-runs and logically remain the same for the input.

Warning: Custom execution IDs

Avoid creating custom execution IDs. Since execution IDs are used to determine the execution order of nodes, custom execution IDs can cause problems when the system attempts to re-run those nodes in your workflow.

PythonGo
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-1>)from google.adk import Context
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-2>)from google.adk.workflow import node
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-3>)from pydantic import BaseModel
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-4>)from typing import Any
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-5>)import asyncio
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-6>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-7>)class Order(BaseModel):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-8>)  order_id: str
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-9>)  cart_items: list[Product]
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-10>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-11>)@node(rerun_on_resume=True)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-12>)async def process_all_orders(ctx: Context, node_input: Any):
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-13>)  orders = await get_orders()
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-14>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-15>)  process_tasks = []
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-16>)  for order in orders:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-17>)    # Use run_id to provide a custom identifier.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-18>)    # Custom run_ids must contain at least one non-numeric character
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-19>)    # to avoid collision with auto-generated sequential numeric IDs.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-20>)    task = ctx.run_node(process_order, order, run_id=f"order-{order.order_id}")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-21>)    process_tasks.append(task)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-22>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-23>)  results = await asyncio.gather(*process_tasks)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-18-24>)  return results
    
By default, auto-generated run IDs are sequential integers starting from `"1"` (represented as strings). Custom `run_id` values must contain at least one non-numeric character to avoid collisions with these auto-generated IDs.

In Go, pass `workflow.WithRunID("order-x")` as a trailing option to `workflow.RunNode`. The ID must contain at least one non-numeric character to avoid collision with the auto-generated sequential counter IDs:
    
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-1>)// newCustomIDWorkflow demonstrates supplying stable custom run IDs via
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-2>)// workflow.WithRunID — equivalent to Python's:
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-3>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-4>)//  task = ctx.run_node(process_order, order, run_id=f"order-{order.order_id}")
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-5>)//
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-6>)// Custom run IDs must contain at least one non-numeric character to avoid
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-7>)// collision with auto-generated sequential integer IDs.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-8>)func newCustomIDWorkflow() (agent.Agent, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-9>)    processOrderNode := workflow.NewFunctionNode("process_order",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-10>)        func(_ agent.Context, orderID string) (string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-11>)            return fmt.Sprintf("processed order %s", orderID), nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-12>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-13>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-14>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-15>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-16>)    orders := []string{"ord-001", "ord-002", "ord-003"}
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-17>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-18>)    processAllOrders := workflow.NewDynamicNode[any, []string]("process_all_orders",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-19>)        func(ctx agent.Context, _ any, _ func(*session.Event) error) ([]string, error) {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-20>)            results := make([]string, 0, len(orders))
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-21>)            for _, orderID := range orders {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-22>)                // WithRunID supplies a stable, deterministic identifier for
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-23>)                // each child invocation. IDs must contain at least one
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-24>)                // non-numeric character to avoid collision with the
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-25>)                // auto-generated sequential counter IDs.
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-26>)                result, err := workflow.RunNode[string](
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-27>)                    ctx,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-28>)                    processOrderNode,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-29>)                    orderID,
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-30>)                    workflow.WithRunID(fmt.Sprintf("order-%s", orderID)),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-31>)                )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-32>)                if err != nil {
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-33>)                    return nil, fmt.Errorf("process order %s: %w", orderID, err)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-34>)                }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-35>)                results = append(results, result)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-36>)            }
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-37>)            return results, nil
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-38>)        },
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-39>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-40>)    )
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-41>)
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-42>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-43>)        Name:        "custom_id_workflow",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-44>)        Description: "Processes orders with stable per-order execution IDs.",
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-45>)        Edges:       workflow.Chain(workflow.Start, processAllOrders),
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-46>)    })
    [](<https://adk.dev/graphs/dynamic/#__codelineno-19-47>)}
    
Back to top 