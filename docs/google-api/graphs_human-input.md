# Human input - Agent Development Kit (ADK)

> Source: [https://adk.dev/graphs/human-input/](https://adk.dev/graphs/human-input/)

[ Skip to content ](<https://adk.dev/graphs/human-input/#human-input-for-agent-workflows>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/graphs/human-input.md> "Edit this page on GitHub") [ ](<https://adk.dev/graphs/human-input/index.md> "View this page as Markdown")

# Human input for agent workflows[¶](<https://adk.dev/graphs/human-input/#human-input-for-agent-workflows> "Permanent link")

Supported in ADKPython v2.0.0Go v2.0.0

Being able to request human input for data input, decision verification, or action permission is an important part of many agent-powered workflows. Graph-based workflows in ADK can include human in the loop (HITL) nodes specifically built for obtaining input from humans as part of a workflow. These nodes do not require artificial intelligence (AI) models to run, which can make the input process more predictable and reliable.

## Get started[¶](<https://adk.dev/graphs/human-input/#get-started> "Permanent link")

PythonGo

You can implement a human input node in a graph using the **_RequestInput_** class and a text prompt for the user. The following code example shows how to add a human input node to a Workflow graph:
    
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-1>)from google.adk.events import RequestInput
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-2>)from google.adk import Workflow
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-3>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-4>)def step1(): # Human input step
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-5>)  yield RequestInput(message="Enter a number:")
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-6>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-7>)def step2(node_input):
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-8>)  return node_input * 2
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-9>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-10>)root_agent = Workflow(
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-11>)    name="root_agent",
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-12>)    edges=[('START', step1, step2)],
    [](<https://adk.dev/graphs/human-input/#__codelineno-0-13>))
    
In this code example, `step1` pauses the execution of the agent until the system receives an input from a user. Once the system receives input from the user, that input is passed to the next node.

In ADK Go v2.0.0, a HITL graph node is built with `workflow.NewEmittingFunctionNode` and `workflow.ResumeOrRequestInput`. This is the direct equivalent of Python's `RequestInput` node:

  * On the **first pass** , `workflow.ResumeOrRequestInput` emits a `session.RequestInput` event (surfaced as `Event.RequestedInput`) and returns `ErrNodeInterrupted`, pausing the workflow.
  * After the human replies, the node is **re-invoked from the top** (`RerunOnResume: &true`) and `ResumeOrRequestInput` returns the reply payload, which flows as typed input to the next node via `event.Output`.

    [](<https://adk.dev/graphs/human-input/#__codelineno-1-1>)// newGraphHITLWorkflow demonstrates a graph HITL node using
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-2>)// workflow.NewEmittingFunctionNode and workflow.ResumeOrRequestInput.
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-3>)//
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-4>)// This is the Go equivalent of the Python RequestInput node:
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-5>)//
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-6>)//  def step1():  # Human input step
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-7>)//      yield RequestInput(message="Enter a number:")
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-8>)//
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-9>)//  def step2(node_input):
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-10>)//      return node_input * 2
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-11>)//
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-12>)//  root_agent = Workflow(
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-13>)//      name="root_agent",
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-14>)//      edges=[('START', step1, step2)],
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-15>)//  )
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-16>)//
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-17>)// On the first pass, step1Node emits a RequestInput event and pauses the
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-18>)// workflow (ErrNodeInterrupted). After the human replies, the node is re-run
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-19>)// and ResumeOrRequestInput returns the reply, which flows as typed input to
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-20>)// step2Node via event.Output.
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-21>)func newGraphHITLWorkflow() (agent.Agent, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-22>)    rerun := true
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-23>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-24>)    // step1Node: pauses for human input on the first pass, returns the
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-25>)    // human's reply on resume. workflow.ResumeOrRequestInput handles both
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-26>)    // phases — no manual re-entry bookkeeping needed.
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-27>)    step1Node := workflow.NewEmittingFunctionNode[any, string]("step1",
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-28>)        func(ctx agent.Context, _ any, emit func(*session.Event) error) (string, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-29>)            reply, err := workflow.ResumeOrRequestInput(ctx, emit, session.RequestInput{
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-30>)                InterruptID: "enter_number",
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-31>)                Message:     "Enter a number:",
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-32>)            })
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-33>)            if err != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-34>)                // ErrNodeInterrupted on first pass — workflow pauses here.
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-35>)                return "", err
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-36>)            }
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-37>)            // On resume, reply is the human's text response.
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-38>)            number, _ := reply.(string)
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-39>)            return number, nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-40>)        },
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-41>)        workflow.NodeConfig{RerunOnResume: &rerun},
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-42>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-43>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-44>)    // step2Node: receives the human's input as its typed string input via
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-45>)    // event.Output and doubles the number.
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-46>)    step2Node := workflow.NewFunctionNode("step2",
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-47>)        func(_ agent.Context, input string) (string, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-48>)            return fmt.Sprintf("You entered: %s (doubled: %s%s)", input, input, input), nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-49>)        },
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-50>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-51>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-52>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-53>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-54>)        Name:        "root_agent",
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-55>)        Description: "Pauses for a number from the user, then doubles it.",
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-56>)        Edges:       workflow.Chain(workflow.Start, step1Node, step2Node),
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-57>)    })
    [](<https://adk.dev/graphs/human-input/#__codelineno-1-58>)}
    
## Configuration options[¶](<https://adk.dev/graphs/human-input/#configuration-options> "Permanent link")

PythonGo

Human input nodes can use the **_RequestInput_** class with the following configuration options:

  * **`message`:** Text provided to the user to explain the human input request.
  * **`payload`:** Structured data to be used as part of the human input request.
  * **`response_schema`:** A data structure the human response must conform to.

Note: Response schema input limitations

For the **response_schema** setting, the **_RequestInput_** class does not automatically reformat human responses to fit a specified data structure. The human response must be provided in the specified format. For a better user experience, consider providing a user interface to collect structured data or use an Agent node to conform unstructured data to the format required.

`session.RequestInput` carries the following fields, which map directly to Python's `RequestInput` parameters:

  * **`InterruptID`** (`string`): A unique identifier for this pause point. Use a stable prefix plus a UUID to avoid collision across workflow runs. Equivalent to the implicit interrupt ID in Python.
  * **`Message`** (`string`): Human-readable prompt displayed to the user. Equivalent to Python's `message` parameter.
  * **`Payload`** (`any`): Optional structured data sent alongside the prompt so the client can render additional context. Equivalent to Python's `payload` parameter.

`workflow.NodeConfig.RerunOnResume` controls what happens on resume:

  * **`&true`**: the node body is re-run from the top; `ResumeOrRequestInput` returns the human's reply on the second pass. Required for nodes that use `ResumeOrRequestInput`.
  * **`&false`** or **`nil`** (leaf default): the reply is routed to the node's successor as input, bypassing the interrupted node.

Note: Structured response from the client

ADK Go does not automatically parse or validate the structure of the human's reply payload. If your workflow needs structured feedback, include a UI or a downstream agent node to validate the response before acting on it.

## Human input examples[¶](<https://adk.dev/graphs/human-input/#human-input-examples> "Permanent link")

The following code examples demonstrate more detailed human input requests.

### Request input with a message and payload[¶](<https://adk.dev/graphs/human-input/#request-input-with-a-message-and-payload> "Permanent link")

PythonGo

The following code sample shows how to construct a **_RequestInput_** object in a workflow node, including a **_payload_** and **_response schema_**. In this example, the `ActivitiesList` is expected to be completed by an agent node that composes a list of activities, and the `get_user_feedback()` node requests feedback from the user.
    
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-1>)class ActivitiesList(BaseModel):
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-2>)   """Itinerary should be a list of dictionaries for each activity. Each
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-3>)   activity has a name and a description"""
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-4>)   itinerary: List[Dict[str, str]]
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-5>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-6>)class UserFeedback(BaseModel):
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-7>)   """Expected response structure from the user."""
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-8>)   user_response: str
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-9>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-10>)async def get_user_feedback(node_input: ActivitiesList):
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-11>)   """
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-12>)   Retrieves the user's thoughts on the agents initial itinerary in order to
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-13>)   either expand on, change the list, or exit the loop
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-14>)   """
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-15>)   message = (
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-16>)       f"""
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-17>)       Here is your recommended base itinerary:\n{node_input}\n\n
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-18>)       Which of these items appeal to you (if any)?
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-19>)       """
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-20>)   )
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-21>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-22>)   yield RequestInput(
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-23>)       message=message,
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-24>)       payload=node_input,
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-25>)        response_schema=UserFeedback,
    [](<https://adk.dev/graphs/human-input/#__codelineno-2-26>)   )
    
The following code sample shows a three-node graph: a builder node generates a structured itinerary, a HITL node sends it as `Payload` alongside the prompt, and a final node acts on the user's feedback. The `Payload` field lets the client render the full itinerary for the user before they respond:
    
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-1>)// ItineraryItem represents a single activity in a travel plan.
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-2>)type ItineraryItem struct {
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-3>)    Name        string `json:"name"`
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-4>)    Description string `json:"description"`
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-5>)}
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-6>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-7>)// newItineraryReviewWorkflow demonstrates a graph HITL node that sends a
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-8>)// structured payload alongside the input prompt so the client can render
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-9>)// additional context for the user. This mirrors Python's:
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-10>)//
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-11>)//  async def get_user_feedback(node_input: ActivitiesList):
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-12>)//      yield RequestInput(
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-13>)//          message="Which items appeal to you?",
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-14>)//          payload=node_input,
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-15>)//          response_schema=UserFeedback,
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-16>)//      )
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-17>)func newItineraryReviewWorkflow() (agent.Agent, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-18>)    rerun := true
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-19>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-20>)    // buildItineraryNode: generates an itinerary and passes it to the HITL
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-21>)    // node as its typed output via event.Output.
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-22>)    buildItineraryNode := workflow.NewFunctionNode("build_itinerary",
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-23>)        func(_ agent.Context, _ any) ([]ItineraryItem, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-24>)            return []ItineraryItem{
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-25>)                {Name: "Eiffel Tower", Description: "Iconic iron lattice tower."},
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-26>)                {Name: "Louvre Museum", Description: "World's largest art museum."},
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-27>)                {Name: "Seine River Cruise", Description: "Scenic boat tour of Paris."},
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-28>)            }, nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-29>)        },
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-30>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-31>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-32>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-33>)    // reviewNode: sends the itinerary as payload alongside the prompt so the
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-34>)    // client can display it. On resume, the human's selection is returned.
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-35>)    reviewNode := workflow.NewEmittingFunctionNode[[]ItineraryItem, string]("get_user_feedback",
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-36>)        func(ctx agent.Context, itinerary []ItineraryItem, emit func(*session.Event) error) (string, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-37>)            reply, err := workflow.ResumeOrRequestInput(ctx, emit, session.RequestInput{
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-38>)                InterruptID: "itinerary_review",
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-39>)                Message:     fmt.Sprintf("Here is your recommended itinerary (%d activities). Which items appeal to you?", len(itinerary)),
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-40>)                Payload:     itinerary, // structured payload rendered by the client
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-41>)            })
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-42>)            if err != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-43>)                // ErrNodeInterrupted on first pass — workflow pauses here.
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-44>)                return "", err
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-45>)            }
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-46>)            feedback, _ := reply.(string)
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-47>)            return feedback, nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-48>)        },
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-49>)        workflow.NodeConfig{RerunOnResume: &rerun},
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-50>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-51>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-52>)    // finalNode: receives the user's feedback and produces a confirmation.
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-53>)    finalNode := workflow.NewFunctionNode("finalize",
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-54>)        func(_ agent.Context, feedback string) (string, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-55>)            return fmt.Sprintf("Itinerary finalised with your feedback: %q", feedback), nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-56>)        },
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-57>)        workflow.NodeConfig{},
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-58>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-59>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-60>)    return workflowagent.New(workflowagent.Config{
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-61>)        Name:        "concierge_workflow",
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-62>)        Description: "Builds an itinerary, asks the user for feedback, then finalises.",
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-63>)        Edges:       workflow.Chain(workflow.Start, buildItineraryNode, reviewNode, finalNode),
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-64>)    })
    [](<https://adk.dev/graphs/human-input/#__codelineno-3-65>)}
    
## Tool-confirmation: approval prompts in LLM agents[¶](<https://adk.dev/graphs/human-input/#tool-confirmation-approval-prompts-in-llm-agents> "Permanent link")

Tool-confirmation is a separate, LLM-agent–level mechanism for yes/no approval prompts. Unlike graph HITL nodes, tool-confirmation works inside an `llmagent` tool function rather than as a standalone graph node. It is useful when you want an LLM agent to pause and ask for approval before executing a specific tool call.

PythonGo

The following code sample shows how to construct a **_RequestInput_** object in a workflow node, including a **_response schema_** :
    
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-1>)async def initial_prompt(ctx: Context):
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-2>)   """Ask the user for itinerary information"""
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-3>)   input_message = """
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-4>)       This is an interactive concierge workflow tasked with making you a great
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-5>)       itinerary for you in your city of choice. If you give some details about
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-6>)       yourself or what you are generally looking for I can better personalize
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-7>)       your itinerary.
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-8>)       For example, input your:
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-9>)           City (Required),
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-10>)           Age,
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-11>)           Hobby,
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-12>)           Example of attraction you liked
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-13>)   """
    [](<https://adk.dev/graphs/human-input/#__codelineno-4-14>)   yield RequestInput(message=input_message, response_schema=str)
    
Set `RequireConfirmation: true` in `functiontool.Config` for a static yes/no approval before a tool executes, or call `ctx.RequestConfirmation` from inside the tool for a custom hint message:
    
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-1>)// DoubleNumberArgs holds the input for the doubleNumber tool.
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-2>)type DoubleNumberArgs struct {
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-3>)    Number int `json:"number" jsonschema:"The number to double."`
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-4>)}
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-5>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-6>)// DoubleNumberResults holds the output of the doubleNumber tool.
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-7>)type DoubleNumberResults struct {
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-8>)    Result int `json:"result"`
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-9>)}
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-10>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-11>)// doubleNumber is a tool that doubles the given number.
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-12>)// Because RequireConfirmation is true, the framework automatically pauses
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-13>)// execution and emits an "adk_request_confirmation" event to the client before
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-14>)// running the tool. The client must reply with a FunctionResponse confirming
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-15>)// or denying the action.
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-16>)func doubleNumber(_ agent.Context, args DoubleNumberArgs) (DoubleNumberResults, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-17>)    return DoubleNumberResults{Result: args.Number * 2}, nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-18>)}
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-19>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-20>)// newSimpleHITLAgent creates an LLM agent with a tool that always requires
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-21>)// user confirmation before it executes (tool-confirmation pattern).
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-22>)func newSimpleHITLAgent(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-23>)    model, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-24>)    if err != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-25>)        return nil, fmt.Errorf("failed to create model: %w", err)
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-26>)    }
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-27>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-28>)    doubleNumberTool, err := functiontool.New(
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-29>)        functiontool.Config{
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-30>)            Name:                "double_number",
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-31>)            Description:         "Doubles the given number. Requires user approval before running.",
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-32>)            RequireConfirmation: true,
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-33>)        },
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-34>)        doubleNumber,
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-35>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-36>)    if err != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-37>)        return nil, fmt.Errorf("failed to create tool: %w", err)
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-38>)    }
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-39>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-40>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-41>)        Name:        "double_number_agent",
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-42>)        Model:       model,
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-43>)        Instruction: "You are a helpful assistant. When asked to double a number, use the double_number tool.",
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-44>)        Tools:       []tool.Tool{doubleNumberTool},
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-45>)    })
    [](<https://adk.dev/graphs/human-input/#__codelineno-5-46>)}
    
For a custom hint with manual re-entry handling:
    
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-1>)// BookFlightArgs holds the input for the bookFlight tool.
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-2>)type BookFlightArgs struct {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-3>)    Origin      string `json:"origin"      jsonschema:"Departure airport code."`
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-4>)    Destination string `json:"destination" jsonschema:"Arrival airport code."`
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-5>)    Date        string `json:"date"        jsonschema:"Travel date in YYYY-MM-DD format."`
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-6>)}
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-7>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-8>)// BookFlightResults holds the outcome of the bookFlight tool.
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-9>)type BookFlightResults struct {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-10>)    Status        string `json:"status"`
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-11>)    ConfirmNumber string `json:"confirm_number,omitempty"`
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-12>)}
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-13>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-14>)// bookFlight is a tool that pauses for human approval before completing a
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-15>)// booking (tool-confirmation pattern with a custom hint message).
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-16>)func bookFlight(ctx agent.Context, args BookFlightArgs) (BookFlightResults, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-17>)    if confirmation := ctx.ToolConfirmation(); confirmation != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-18>)        if !confirmation.Confirmed {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-19>)            return BookFlightResults{Status: "Booking cancelled by user."}, nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-20>)        }
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-21>)        return BookFlightResults{
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-22>)            Status:        "Booking confirmed.",
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-23>)            ConfirmNumber: "FLT-20251031",
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-24>)        }, nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-25>)    }
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-26>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-27>)    hint := fmt.Sprintf(
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-28>)        "The agent wants to book a flight from %s to %s on %s. Do you approve?",
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-29>)        args.Origin, args.Destination, args.Date,
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-30>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-31>)    if err := ctx.RequestConfirmation(hint, nil); err != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-32>)        return BookFlightResults{}, fmt.Errorf("failed to request confirmation: %w", err)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-33>)    }
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-34>)    return BookFlightResults{Status: "Awaiting user approval."}, nil
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-35>)}
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-36>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-37>)// newHITLWithHintAgent creates an LLM agent whose bookFlight tool manually
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-38>)// requests confirmation with a descriptive hint (tool-confirmation pattern).
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-39>)func newHITLWithHintAgent(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-40>)    model, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-41>)    if err != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-42>)        return nil, fmt.Errorf("failed to create model: %w", err)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-43>)    }
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-44>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-45>)    bookFlightTool, err := functiontool.New(
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-46>)        functiontool.Config{
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-47>)            Name:        "book_flight",
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-48>)            Description: "Books a flight between two airports on a given date.",
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-49>)        },
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-50>)        bookFlight,
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-51>)    )
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-52>)    if err != nil {
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-53>)        return nil, fmt.Errorf("failed to create tool: %w", err)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-54>)    }
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-55>)
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-56>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-57>)        Name:        "flight_booking_agent",
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-58>)        Model:       model,
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-59>)        Instruction: "You are a flight booking assistant. Help the user book flights.",
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-60>)        Tools:       []tool.Tool{bookFlightTool},
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-61>)    })
    [](<https://adk.dev/graphs/human-input/#__codelineno-6-62>)}
    
Back to top 