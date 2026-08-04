# Data handling - Agent Development Kit (ADK)

> Source: [https://adk.dev/graphs/data-handling/](https://adk.dev/graphs/data-handling/)

[ Skip to content ](<https://adk.dev/graphs/data-handling/#data-handling-for-agent-workflows>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/graphs/data-handling.md> "Edit this page on GitHub") [ ](<https://adk.dev/graphs/data-handling/index.md> "View this page as Markdown")

# Data handling for agent workflows[¶](<https://adk.dev/graphs/data-handling/#data-handling-for-agent-workflows> "Permanent link")

Supported in ADKPython v2.0.0Go v2.0.0

Structuring and managing data between agents and graph-based nodes is critical for building reliable processes with ADK. This guide explains data handling within graph-based workflows and collaboration agents, including how information is transmitted and received between graph nodes. It covers the essential parameters for passing data, content, and state, and explains how to implement structured data transfer for both function and agent nodes using data format schemas and specific instruction syntax.

## Workflow data flow[¶](<https://adk.dev/graphs/data-handling/#workflow-data-flow> "Permanent link")

Within a graph-based workflow, nodes pass data to downstream steps through events. A step writes its output to a named event field, and the next step receives it as its typed input.

PythonGo

In Python, data is exchanged between graph nodes using **_Events_**. The key parameters for node data handling are:

  * **`output`** : Parameter for passing information between _nodes_.
  * **`message`** : Data intended as a response to a user.
  * **`state`** : Data automatically persisted across nodes via **_Events_** throughout an ADK session.

In ADK Go v2.0.0, the data-passing mechanism depends on which agent style you use:

**workflow package** (`FunctionNode`, `AgentNode`, `DynamicNode`): nodes communicate through `session.Event` fields, mirroring Python closely:

  * **`Event.Output`** : the node's return value, set automatically by the framework when a `FunctionNode` returns a non-`*genai.Content` value. The successor node receives this as its typed `input` parameter.
  * **`Event.Routes`** : routing keys set explicitly by an emitting node to select which conditional edge to follow — the Go equivalent of Python's `Event(route=...)`.
  * **`Event.NodeInfo`** : scheduler metadata (`path`, `MessageAsOutput`, `OutputFor`). Set by the workflow engine; nodes do not set this directly.

**Prebuilt workflow agents** (`sequentialagent`, `parallelagent`, `loopagent`): these agents communicate through session state:

  * **`OutputKey`** on `llmagent.Config`: the framework writes the agent's final text response to `state[OutputKey]` after each turn.
  * **`ctx.Session().State().Set` / `.Get`**: write or read arbitrary values from state inside custom code.
  * **`{key}` in `Instruction`**: the framework substitutes `state["key"]` into the prompt before calling the model.

State keys may carry a prefix that controls their lifetime and scope:

Prefix constant | Prefix string | Scope  
---|---|---  
`session.KeyPrefixApp` | `"app:"` | Shared across all users and sessions for the app  
`session.KeyPrefixUser` | `"user:"` | Tied to the user, shared across their sessions  
`session.KeyPrefixTemp` | `"temp:"` | Discarded after the current invocation ends  
_(none)_ | — | Persists for the lifetime of the session  
  
### Node output[¶](<https://adk.dev/graphs/data-handling/#node-output> "Permanent link")

Each step in a workflow produces output for its successor.

PythonGo

Use the **_return_** or **_yield_** syntax to hand off data to the next node:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-0-1>)from google.adk import Event
    [](<https://adk.dev/graphs/data-handling/#__codelineno-0-2>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-0-3>)def my_function_node(node_input: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-0-4>)    output_value = node_input.upper()
    [](<https://adk.dev/graphs/data-handling/#__codelineno-0-5>)    return Event(output=output_value) # "THE RESULT"
    
Use the **_return_** syntax when outputting **_Event_** data that does not require additional processing. When emitting data that requires additional processing, or if you are generating more than one data item, you can use more than one **_yield_** command. Each **_yield_** call adds to a list of data objects on the Event which is passed to the next node of a graph. A **_return_** or **_yield_** command without a parameter passes a `None` value to the next node.

**workflow package** : a `FunctionNode` simply returns a typed Go value. The framework automatically wraps the return value in a `session.Event` and sets `Event.Output`. The successor node receives this value as its typed `input` parameter — no manual event construction needed:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-1>)// newEventOutputPipeline demonstrates the primary data-passing mechanism for
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-2>)// workflow package nodes: a FunctionNode returns a typed Go value, and the
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-3>)// framework automatically sets event.Output to that value. The successor node
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-4>)// receives it as its typed `input` parameter.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-5>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-6>)// This mirrors the Python pattern exactly:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-7>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-8>)//  def my_function_node(node_input: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-9>)//      return Event(output=node_input.upper())
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-10>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-11>)// In Go, the function simply returns the value — no Event construction needed.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-12>)func newEventOutputPipeline() (agent.Agent, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-13>)    upperFn := func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-14>)        return strings.ToUpper(input), nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-15>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-16>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-17>)    suffixFn := func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-18>)        return input + " IS AWESOME!", nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-19>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-20>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-21>)    nodeA := workflow.NewFunctionNode("upper", upperFn, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-22>)    nodeB := workflow.NewFunctionNode("suffix", suffixFn, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-23>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-24>)    // workflow.Chain wires START → nodeA → nodeB. The output of nodeA is
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-25>)    // delivered as the typed input of nodeB via event.Output.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-26>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-27>)        Name:        "event_output_pipeline",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-28>)        Description: "Demonstrates Event.Output data flow between FunctionNodes.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-29>)        Edges:       workflow.Chain(workflow.Start, nodeA, nodeB),
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-30>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-1-31>)}
    
**Prebuilt workflow agents** : use `OutputKey` on `llmagent.Config` to save an agent's text response to session state, then reference it with `{key}` in downstream agents' `Instruction` templates:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-1>)// newOutputKeyPipeline demonstrates the OutputKey mechanism for the prebuilt
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-2>)// sequentialagent. When OutputKey is set on an llmagent.Config, the framework
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-3>)// automatically writes the agent's final text response to session state under
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-4>)// that key. Downstream agents read it by referencing {key} in their Instruction.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-5>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-6>)// This pattern applies to sequentialagent / parallelagent / loopagent.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-7>)// For the workflow package (FunctionNode / AgentNode), use Event.Output instead.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-8>)func newOutputKeyPipeline(ctx context.Context, geminiModel model.LLM) (agent.Agent, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-9>)    step1, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-10>)        Name:        "step_1",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-11>)        Model:       geminiModel,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-12>)        Description: "Transforms the user's text.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-13>)        Instruction: "Convert the user's message to uppercase. Output only the transformed text.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-14>)        OutputKey:   "upper_result",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-15>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-16>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-17>)        return nil, fmt.Errorf("step1: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-18>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-19>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-20>)    step2, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-21>)        Name:        "step_2",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-22>)        Model:       geminiModel,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-23>)        Description: "Reports the transformed text.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-24>)        Instruction: "The transformed text is: {upper_result}. Report it to the user.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-25>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-26>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-27>)        return nil, fmt.Errorf("step2: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-28>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-29>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-30>)    return sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-31>)        AgentConfig: agent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-32>)            Name:      "output_key_pipeline",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-33>)            SubAgents: []agent.Agent{step1, step2},
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-34>)        },
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-35>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-2-36>)}
    
### Node output: passing structured data[¶](<https://adk.dev/graphs/data-handling/#node-output-passing-structured-data> "Permanent link")

PythonGo

You can pass longer, structured data in a serializable format:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-3-1>)def my_function_node_3():
    [](<https://adk.dev/graphs/data-handling/#__codelineno-3-2>)    yield Event(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-3-3>)        output={
    [](<https://adk.dev/graphs/data-handling/#__codelineno-3-4>)            "city_name": "Paris",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-3-5>)            "city_time": "10:10 AM",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-3-6>)        },
    [](<https://adk.dev/graphs/data-handling/#__codelineno-3-7>)    )
    
Caution: Event.output limitation

Nodes are only allowed to emit a single **_Event.output_** data payload per execution. This limitation means that while you can use more than one **_yield_** in a node, having two or more **_yield_** commands with an **_Event.output_** results in a runtime error.

**workflow package** : a `FunctionNode` can return any JSON-serializable Go struct. The framework serializes it into `Event.Output` and deserializes it back into the successor node's typed `input` parameter. There is no single-payload restriction — each node has exactly one typed return value:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-1>)// newStructuredOutputPipeline shows how to pass a struct from one FunctionNode
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-2>)// to another. The framework serialises the return value into event.Output and
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-3>)// deserialises it back into the successor's typed input parameter.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-4>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-5>)// This is the Go equivalent of:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-6>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-7>)//  class CityTime(BaseModel):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-8>)//      time_info: str
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-9>)//      city: str
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-10>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-11>)//  def lookup_time_function(city: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-12>)//      return Event(output=CityTime(time_info="10:10 AM", city=city))
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-13>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-14>)//  def city_report(node_input: CityTime):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-15>)//      return Event(output=f"It is {node_input.time_info} in {node_input.city}.")
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-16>)type CityTime struct {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-17>)    TimeInfo string `json:"time_info"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-18>)    City     string `json:"city"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-19>)}
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-20>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-21>)func newStructuredOutputPipeline(ctx context.Context, geminiModel model.LLM) (agent.Agent, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-22>)    lookupTimeFn := func(_ agent.Context, city string) (CityTime, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-23>)        // Simulate looking up the current time in the city.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-24>)        return CityTime{TimeInfo: "10:10 AM", City: city}, nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-25>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-26>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-27>)    cityReportAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-28>)        Name:        "city_report_agent",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-29>)        Model:       geminiModel,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-30>)        Description: "Reports the city and current time from the previous node's output.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-31>)        // When wrapped as an AgentNode, the predecessor's event.Output
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-32>)        // is delivered as the agent's user content. The {key} template
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-33>)        // syntax is not required — the struct fields are provided inline.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-34>)        Instruction: "Report the city time information you received in a friendly sentence.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-35>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-36>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-37>)        return nil, fmt.Errorf("cityReportAgent: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-38>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-39>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-40>)    lookupTimeNode := workflow.NewFunctionNode("lookup_time", lookupTimeFn, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-41>)    cityReportNode, err := workflow.NewAgentNode(cityReportAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-42>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-43>)        return nil, fmt.Errorf("NewAgentNode: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-44>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-45>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-46>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-47>)        Name:      "city_time_pipeline",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-48>)        Edges:     workflow.Chain(workflow.Start, lookupTimeNode, cityReportNode),
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-49>)        SubAgents: []agent.Agent{cityReportAgent},
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-50>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-4-51>)}
    
**Prebuilt workflow agents** : use multiple `OutputKey` values, one per agent, to store individual fields in session state. Downstream agents read each field independently via `{key}` in their `Instruction`.

### Routing output[¶](<https://adk.dev/graphs/data-handling/#routing-output> "Permanent link")

PythonGo

Use the `route` parameter of an **_Event_** to drive conditional edge dispatch:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-5-1>)def router(node_input: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-5-2>)    return Event(route="BUG")
    
**workflow package** : an emitting `FunctionNode` constructs a `session.Event` directly, sets `Event.Routes` to the desired route keys, and sets `Event.Output` to forward the payload to the successor. The workflow engine reads `Event.Routes` at dispatch time to select the matching edge:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-1>)// classifyAndRoute shows how to set event.Routes alongside event.Output from
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-2>)// an emitting FunctionNode. The function constructs a session.Event directly,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-3>)// sets Routes to select the conditional edge, and sets Output to forward the
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-4>)// payload to the successor node.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-5>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-6>)// This mirrors the Python pattern:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-7>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-8>)//  def router(node_input: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-9>)//      return Event(route="BUG")
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-10>)func classifyAndRoute(ctx agent.Context, msg string, emit func(*session.Event) error) (any, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-11>)    category := classifyMessage(msg)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-12>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-13>)    ev := session.NewEvent(ctx, ctx.InvocationID())
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-14>)    ev.Routes = []string{category} // drives edge dispatch
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-15>)    ev.Output = msg                // forwarded as typed input to the successor
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-16>)    if err := emit(ev); err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-17>)        return nil, err
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-18>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-19>)    return nil, nil // nil suppresses the automatic terminal event
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-20>)}
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-21>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-22>)func classifyMessage(msg string) string {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-23>)    switch {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-24>)    case strings.Contains(strings.ToLower(msg), "bug"):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-25>)        return "BUG"
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-26>)    case strings.Contains(strings.ToLower(msg), "help"):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-27>)        return "CUSTOMER_SUPPORT"
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-28>)    default:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-29>)        return "LOGISTICS"
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-30>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-31>)}
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-32>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-33>)func newRoutingPipeline() (agent.Agent, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-34>)    classifyNode := workflow.NewEmittingFunctionNode("classify", classifyAndRoute, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-35>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-36>)    bugHandler := workflow.NewFunctionNode("bug_handler",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-37>)        func(_ agent.Context, msg string) (string, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-38>)            return "Handling bug: " + msg, nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-39>)        }, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-40>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-41>)    supportHandler := workflow.NewFunctionNode("support_handler",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-42>)        func(_ agent.Context, msg string) (string, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-43>)            return "Handling support: " + msg, nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-44>)        }, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-45>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-46>)    logisticsHandler := workflow.NewFunctionNode("logistics_handler",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-47>)        func(_ agent.Context, msg string) (string, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-48>)            return "Handling logistics: " + msg, nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-49>)        }, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-50>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-51>)    edges := workflow.Concat(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-52>)        workflow.Chain(workflow.Start, classifyNode),
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-53>)        []workflow.Edge{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-54>)            {From: classifyNode, To: bugHandler, Route: workflow.StringRoute("BUG")},
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-55>)            {From: classifyNode, To: supportHandler, Route: workflow.StringRoute("CUSTOMER_SUPPORT")},
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-56>)            {From: classifyNode, To: logisticsHandler, Route: workflow.StringRoute("LOGISTICS")},
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-57>)        },
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-58>)    )
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-59>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-60>)        Name:        "routing_pipeline",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-61>)        Description: "Classifies and routes a message using Event.Routes.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-62>)        Edges:       edges,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-63>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-6-64>)}
    
### User-facing messages[¶](<https://adk.dev/graphs/data-handling/#user-facing-messages> "Permanent link")

PythonGo

Use the **_message_** parameter of an **_Event_** to send a response to a user rather than pass data to the next node:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-7-1>)async def user_message(node_input: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-7-2>)  """Tell user research process is starting."""
    [](<https://adk.dev/graphs/data-handling/#__codelineno-7-3>)  yield Event(message="Beginning research process...")
    
**workflow package** : to emit a user-visible message without advancing the node's typed output, set `Event.Content` on an intermediate event emitted via the `emit` callback in an `EmittingFunctionNode`. The terminal return value (or `nil`) controls `Event.Output`.

**Prebuilt workflow agents** : any `llmagent` step automatically emits its model response as a user-facing event. For non-LLM steps, write a custom `Run` function on an `agent.Agent` that yields events whose `LLMResponse.Content` contains the text.

### Session state and state scopes[¶](<https://adk.dev/graphs/data-handling/#session-state-and-state-scopes> "Permanent link")

Session state persists data across turns within a session. It is the primary data-sharing mechanism for the prebuilt workflow agents, and is also available inside tools and callbacks regardless of which agent style you use.

PythonGo

Use the **_state_** parameter of an **_Event_** to maintain values across nodes. Nodes can modify state values, and the modified state values are available to downstream nodes:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-1>)async def init_state_node(attempts: int = 0):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-2>)  yield Event(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-3>)      state={
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-4>)          "attempts": attempts,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-5>)      },
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-6>)  )
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-7>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-8>)async def task_attempt_node(node_input: Content, attempts: int):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-9>)  yield Event(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-10>)      state={
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-11>)          "attempts": attempts + 1,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-12>)      },
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-13>)  )
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-14>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-15>)async def read_state_node(ctx: Context):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-16>)  print(f"attempts state: {ctx.state}") # attempts state: attempts: 1
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-17>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-18>)root_agent = Workflow(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-19>)    name="root_agent",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-20>)    edges=[("START", init_state_node, task_attempt_node, read_state_node)],
    [](<https://adk.dev/graphs/data-handling/#__codelineno-8-21>))
    
Caution: `state` property data limitations

The state parameter _should not be used to persist large amounts of data_ between nodes. Use artifacts or other data persistence mechanisms, such as database Tools, to persist large data resources during the life cycle of a Workflow.

State is written with `ctx.Session().State().Set(key, value)` and read with `.Get(key)`. The `session` package defines prefix constants that map to the same lifetime scopes as Python's state parameter. This pattern applies to prebuilt workflow agents and to tools and callbacks in any agent style:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-1>)// stateScopes shows how session-state key prefixes control the lifetime and
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-2>)// visibility of stored values. This pattern applies to the prebuilt workflow
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-3>)// agents (sequentialagent / parallelagent / loopagent) and to tools and
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-4>)// callbacks. For the workflow package (FunctionNode / AgentNode), prefer
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-5>)// returning values directly via Event.Output.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-6>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-7>)// Available prefixes:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-8>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-9>)//  session.KeyPrefixApp  ("app:")  – shared across all users and sessions
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-10>)//  session.KeyPrefixUser ("user:") – tied to the user, shared across sessions
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-11>)//  session.KeyPrefixTemp ("temp:") – discarded after the current invocation
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-12>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-13>)// Keys with no prefix persist for the lifetime of the session.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-14>)func stateScopes(ctx agent.Context) error {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-15>)    st := ctx.Session().State()
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-16>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-17>)    // Session-scoped (no prefix) — persists for the life of this session.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-18>)    if err := st.Set("attempts", 0); err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-19>)        return fmt.Errorf("state.Set attempts: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-20>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-21>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-22>)    // App-scoped — shared across all users and sessions for this app.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-23>)    if err := st.Set(session.KeyPrefixApp+"global_counter", 42); err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-24>)        return fmt.Errorf("state.Set app:global_counter: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-25>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-26>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-27>)    // User-scoped — shared across all sessions belonging to this user.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-28>)    if err := st.Set(session.KeyPrefixUser+"login_count", 1); err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-29>)        return fmt.Errorf("state.Set user:login_count: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-30>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-31>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-32>)    // Temp-scoped — discarded after this invocation ends.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-33>)    if err := st.Set(session.KeyPrefixTemp+"scratch", "ephemeral"); err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-34>)        return fmt.Errorf("state.Set temp:scratch: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-35>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-36>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-37>)    return nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-9-38>)}
    
Caution: state data limitations

Session state is a lightweight key-value store. Do not use it to persist large payloads such as file contents or binary data. Use ADK artifacts or external storage tools instead.

workflow package: prefer Event.Output over state

For the `workflow` package (`FunctionNode`, `AgentNode`, `DynamicNode`), pass data between nodes by returning typed values — the framework sets `Event.Output` automatically. Only use `State().Set` when you need to share values with tools, callbacks, or agent `Instruction` templates.

## Constrain node data with schemas[¶](<https://adk.dev/graphs/data-handling/#constrain-node-data-with-schemas> "Permanent link")

You can set input and output data schemas to constrain the data formats accepted and produced by any agent node.

PythonGo

Use `input_schema` and `output_schema` with a class that extends **_BaseModel_** to constrain any agent's input and output:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-1>)from google.adk import Agent
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-2>)from pydantic import BaseModel
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-3>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-4>)class FlightSearchInput(BaseModel):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-5>)    origin: str           # Airport code "SFO"
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-6>)    destination: str      # Airport code "CDG"
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-7>)    departure_date: date  # date(2026, 3, 15)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-8>)    passengers: int = 1   # Number of passengers
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-9>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-10>)class FlightSearchOutput(BaseModel):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-11>)    flights: list[Flight]
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-12>)    cheapest_price: float
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-13>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-14>)flight_searcher = Agent(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-15>)    name="flight_searcher",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-16>)    instruction="Search for available flights.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-17>)    input_schema=FlightSearchInput,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-18>)    output_schema=FlightSearchOutput,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-19>)    tools=[search_flights_api],
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-20>)    mode="single_turn",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-21>)    ...
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-22>))
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-23>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-24>)assistant = Agent(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-25>)    name="assistant",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-26>)    instruction="You help users plan trips.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-27>)    sub_agents=[flight_searcher],
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-28>)    ...
    [](<https://adk.dev/graphs/data-handling/#__codelineno-10-29>))
    
**workflow package** : use `workflow.NewAgentNodeTyped[Input, Output]` to attach schemas to an agent node. The generic type parameters are reflected into `*jsonschema.Schema` automatically — no hand-built schema construction needed. The node's `Event.Output` carries the structured result to the successor — no `OutputKey` or state write is needed:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-1>)// FlightSearchInput is the typed input schema for the flight-search agent node.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-2>)// workflow.NewAgentNodeTyped[FlightSearchInput, FlightSearchOutput] reflects
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-3>)// these structs into *jsonschema.Schema automatically — no hand-built schema
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-4>)// construction needed.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-5>)type FlightSearchInput struct {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-6>)    Origin        string `json:"origin"         jsonschema:"Departure airport code e.g. SFO"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-7>)    Destination   string `json:"destination"    jsonschema:"Arrival airport code e.g. CDG"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-8>)    DepartureDate string `json:"departure_date" jsonschema:"Travel date in YYYY-MM-DD format"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-9>)}
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-10>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-11>)// FlightSearchOutput is the typed output schema for the flight-search agent node.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-12>)type FlightSearchOutput struct {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-13>)    CheapestPrice string `json:"cheapest_price" jsonschema:"Cheapest available fare e.g. $450"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-14>)    FlightCount   string `json:"flight_count"   jsonschema:"Number of matching flights found"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-15>)}
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-16>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-17>)// newSchemaAgentPipeline demonstrates workflow.NewAgentNodeTyped, which infers
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-18>)// *jsonschema.Schema from the generic type parameters. This is the Go equivalent
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-19>)// of Python's:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-20>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-21>)//  flight_searcher = Agent(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-22>)//      input_schema=FlightSearchInput,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-23>)//      output_schema=FlightSearchOutput,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-24>)//      ...
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-25>)//  )
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-26>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-27>)// The node's event.Output carries the structured result to the successor —
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-28>)// no OutputKey or state write is needed.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-29>)func newSchemaAgentPipeline(ctx context.Context, geminiModel model.LLM) (agent.Agent, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-30>)    flightSearchAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-31>)        Name:        "flight_searcher",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-32>)        Model:       geminiModel,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-33>)        Description: "Searches for available flights and returns structured results.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-34>)        Instruction: `You are a flight-search assistant. Respond ONLY with a JSON object.`,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-35>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-36>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-37>)        return nil, fmt.Errorf("flightSearchAgent: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-38>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-39>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-40>)    synthAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-41>)        Name:        "trip_assistant",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-42>)        Model:       geminiModel,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-43>)        Description: "Summarises flight search results for the user.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-44>)        Instruction: `You help users plan trips. Summarise the flight result you received.`,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-45>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-46>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-47>)        return nil, fmt.Errorf("synthAgent: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-48>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-49>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-50>)    // NewAgentNodeTyped[In, Out] reflects FlightSearchInput and FlightSearchOutput
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-51>)    // into *jsonschema.Schema automatically. The node enforces the input schema
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-52>)    // and constrains the model reply to the output schema's shape.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-53>)    flightNode, err := workflow.NewAgentNodeTyped[FlightSearchInput, FlightSearchOutput](flightSearchAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-54>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-55>)        return nil, fmt.Errorf("flightNode: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-56>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-57>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-58>)    synthNode, err := workflow.NewAgentNode(synthAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-59>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-60>)        return nil, fmt.Errorf("synthNode: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-61>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-62>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-63>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-64>)        Name:      "flight_booking_pipeline",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-65>)        Edges:     workflow.Chain(workflow.Start, flightNode, synthNode),
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-66>)        SubAgents: []agent.Agent{flightSearchAgent, synthAgent},
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-67>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-11-68>)}
    
**Prebuilt workflow agents** : set `InputSchema` and `OutputSchema` on `llmagent.Config`. `OutputSchema` forces the model to reply with a JSON object matching the schema (the agent cannot use tools when `OutputSchema` is set). Use `OutputKey` to save the JSON string to state for downstream agents to reference via `{key}` in their `Instruction`.

## Access structured data in agents[¶](<https://adk.dev/graphs/data-handling/#access-structured-data-in-agents> "Permanent link")

PythonGo

Use the curly-brace `{ }` syntax to select properties from the input schema, or `< >` to select a property and also qualify it by the name of the source node:
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-1>)class CityTime(BaseModel):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-2>)    time_info: str  # time information
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-3>)    city: str       # city name
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-4>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-5>)def lookup_time_function(city: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-6>)    """Simulate returning the current time in the specified city."""
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-7>)    return Event(output=CityTime(time_info='10:10 AM', city=city))
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-8>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-9>)city_report_agent = Agent(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-10>)    name="city_report_agent",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-11>)    model="gemini-flash-latest",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-12>)    input_schema=CityTime,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-13>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-14>)    # data selection based on class and parameter
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-15>)    # instruction="""
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-16>)    #     Return a sentence in the following format:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-17>)    #     It is {CityTime.time_info} in {CityTime.city} right now.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-18>)    # """,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-19>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-20>)    # more restrictive data selection based on source node name
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-21>)    instruction="""
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-22>)        Return a sentence in the following format:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-23>)        It is <CityTime.time_info from lookup_time_function> in
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-24>)        <CityTime.city from lookup_time_function> right now.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-25>)    """,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-26>))
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-27>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-28>)root_agent = Workflow(
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-29>)    name="root_agent",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-30>)    edges=[
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-31>)        (START, city_generator_agent, lookup_time_function, city_report_agent)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-32>)    ],
    [](<https://adk.dev/graphs/data-handling/#__codelineno-12-33>))
    
In ADK Go v2.0.0, a `FunctionNode` returns a typed struct and the framework serializes it into `Event.Output`. The successor `AgentNode` receives the struct as its user content — the fields are available to the agent's `Instruction` without any `{key}` template syntax. This is the direct equivalent of Python's `input_schema=CityTime` with `{CityTime.time_info}` template placeholders: the struct fields are delivered as typed input rather than looked up by name from state.
    
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-1>)// newStructuredOutputPipeline shows how to pass a struct from one FunctionNode
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-2>)// to another. The framework serialises the return value into event.Output and
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-3>)// deserialises it back into the successor's typed input parameter.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-4>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-5>)// This is the Go equivalent of:
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-6>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-7>)//  class CityTime(BaseModel):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-8>)//      time_info: str
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-9>)//      city: str
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-10>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-11>)//  def lookup_time_function(city: str):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-12>)//      return Event(output=CityTime(time_info="10:10 AM", city=city))
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-13>)//
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-14>)//  def city_report(node_input: CityTime):
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-15>)//      return Event(output=f"It is {node_input.time_info} in {node_input.city}.")
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-16>)type CityTime struct {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-17>)    TimeInfo string `json:"time_info"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-18>)    City     string `json:"city"`
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-19>)}
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-20>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-21>)func newStructuredOutputPipeline(ctx context.Context, geminiModel model.LLM) (agent.Agent, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-22>)    lookupTimeFn := func(_ agent.Context, city string) (CityTime, error) {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-23>)        // Simulate looking up the current time in the city.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-24>)        return CityTime{TimeInfo: "10:10 AM", City: city}, nil
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-25>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-26>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-27>)    cityReportAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-28>)        Name:        "city_report_agent",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-29>)        Model:       geminiModel,
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-30>)        Description: "Reports the city and current time from the previous node's output.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-31>)        // When wrapped as an AgentNode, the predecessor's event.Output
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-32>)        // is delivered as the agent's user content. The {key} template
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-33>)        // syntax is not required — the struct fields are provided inline.
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-34>)        Instruction: "Report the city time information you received in a friendly sentence.",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-35>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-36>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-37>)        return nil, fmt.Errorf("cityReportAgent: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-38>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-39>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-40>)    lookupTimeNode := workflow.NewFunctionNode("lookup_time", lookupTimeFn, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-41>)    cityReportNode, err := workflow.NewAgentNode(cityReportAgent, workflow.NodeConfig{})
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-42>)    if err != nil {
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-43>)        return nil, fmt.Errorf("NewAgentNode: %w", err)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-44>)    }
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-45>)
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-46>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-47>)        Name:      "city_time_pipeline",
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-48>)        Edges:     workflow.Chain(workflow.Start, lookupTimeNode, cityReportNode),
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-49>)        SubAgents: []agent.Agent{cityReportAgent},
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-50>)    })
    [](<https://adk.dev/graphs/data-handling/#__codelineno-13-51>)}
    
For a complete example of this workflow, see [Graph-based agent workflows](<https://adk.dev/graphs/#get-started>).

Back to top 