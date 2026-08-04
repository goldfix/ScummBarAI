# Collaborative workflows - Agent Development Kit (ADK)

> Source: [https://adk.dev/workflows/collaboration/](https://adk.dev/workflows/collaboration/)

[ Skip to content ](<https://adk.dev/workflows/collaboration/#build-collaborative-agent-teams>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/workflows/collaboration.md> "Edit this page on GitHub") [ ](<https://adk.dev/workflows/collaboration/index.md> "View this page as Markdown")

# Build collaborative agent teams[¶](<https://adk.dev/workflows/collaboration/#build-collaborative-agent-teams> "Permanent link")

Supported in ADKPython v2.0.0Go v2.0.0

Some complex tasks may require multiple agents with specific responsibilities and benefit from less structured procedures, particularly for iterative processes with several, substantial sub-tasks. In a collaborative agent team in ADK, a coordinator agent handles delegation of tasks to one or more subagents. This approach makes it easier to build complex, self-managing agent systems, with subagents defined to handle specific tasks, and automatic return to the parent after completing a task.

When using this self-managed agent team approach, the subagents are assigned an operating **_mode_** to manage their behavior and limit their scope of work. These **_modes_** set general behavior guidelines for subagents and create more predictable and reliable mulit-agent workflows. The following settings are available for collaboration modes:

  * **_Chat_** : Full user interaction, manual return to parent agent (default, current behavior)
  * **_Task_** : User interaction for clarifications with automatic return to parent agent
  * **_Single-turn:_** No user interaction with automatic return and can be run in parallel

This guide covers how to use modes for your subagents and how these modes impact agent behavior.

Disabled: Task mode in graph-based workflows

The collaborative mode `task` behavior is disabled for use in graph-based workflows in ADK Python v2.0.0. This feature is expected to be re-enabled in a future release.

## Get started[¶](<https://adk.dev/workflows/collaboration/#get-started> "Permanent link")

The following code example shows how to set operating modes for a small team of subagents and assign them to a coordinator agent:

PythonGo
    
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-1>)from google.adk import Agent
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-2>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-3>)weather_agent = Agent(
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-4>)    name="weather_checker",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-5>)    mode="single_turn",         # no user interaction
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-6>)    tools=[get_weather, user_info, geocode_address],
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-7>))
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-8>)flight_agent = Agent(
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-9>)    name="flight_booker",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-10>)    mode="task",                # can ask user questions
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-11>)    input_schema=FlightInput,
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-12>)    output_schema=FlightResult,
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-13>)    tools=[search_flights, book_flight],
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-14>))
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-15>)root = Agent(
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-16>)    name="travel_planner",      # coordinator agent
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-17>)    sub_agents=[weather_agent, flight_agent],
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-18>)    # Auto-injects delegation tools named after each subagent:
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-19>)    # weather_checker, flight_booker
    [](<https://adk.dev/workflows/collaboration/#__codelineno-0-20>))
    
In ADK Go v2.0.0, the `Mode` field on `llmagent.Config` accepts the same mode strings as Python: `"chat"`, `"task"`, and `"single_turn"`. Declaring `SubAgents` on the coordinator agent causes ADK to automatically generate a delegation tool for each subagent, named after the subagent itself, exactly as in Python.
    
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-1>)// Stub tool functions — in a real agent these call external services.
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-2>)func getWeather(_ agent.Context, _ struct{ City string }) (string, error) {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-3>)    return "Sunny, 22°C", nil
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-4>)}
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-5>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-6>)func searchFlights(_ agent.Context, _ struct{ Origin, Destination string }) (string, error) {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-7>)    return "3 flights found", nil
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-8>)}
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-9>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-10>)func bookFlight(_ agent.Context, _ struct{ FlightID string }) (string, error) {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-11>)    return "Flight booked", nil
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-12>)}
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-13>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-14>)// newCollaborativeTeam builds a coordinator agent with two subagents, each
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-15>)// configured with a different collaboration mode. This is the Go equivalent of:
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-16>)//
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-17>)//  weather_agent = Agent(name="weather_checker", mode="single_turn", ...)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-18>)//  flight_agent  = Agent(name="flight_booker",   mode="task",        ...)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-19>)//  root = Agent(name="travel_planner", sub_agents=[weather_agent, flight_agent])
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-20>)func newCollaborativeTeam(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-21>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-22>)    if err != nil {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-23>)        return nil, err
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-24>)    }
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-25>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-26>)    getWeatherTool, err := functiontool.New(functiontool.Config{
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-27>)        Name:        "get_weather",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-28>)        Description: "Returns the current weather for a city.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-29>)    }, getWeather)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-30>)    if err != nil {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-31>)        return nil, err
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-32>)    }
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-33>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-34>)    searchFlightsTool, err := functiontool.New(functiontool.Config{
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-35>)        Name:        "search_flights",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-36>)        Description: "Searches for available flights between two airports.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-37>)    }, searchFlights)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-38>)    if err != nil {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-39>)        return nil, err
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-40>)    }
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-41>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-42>)    bookFlightTool, err := functiontool.New(functiontool.Config{
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-43>)        Name:        "book_flight",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-44>)        Description: "Books a specific flight by ID.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-45>)    }, bookFlight)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-46>)    if err != nil {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-47>)        return nil, err
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-48>)    }
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-49>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-50>)    // weatherAgent runs in ModeSingleTurn: no user interaction, executes one
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-51>)    // turn and returns automatically. Equivalent to mode="single_turn" in Python.
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-52>)    weatherAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-53>)        Name:        "weather_checker",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-54>)        Model:       model,
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-55>)        Mode:        llmagent.ModeSingleTurn,
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-56>)        Description: "Checks the current weather for a given city.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-57>)        Instruction: "Use the get_weather tool to look up the current weather.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-58>)        Tools:       []tool.Tool{getWeatherTool},
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-59>)    })
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-60>)    if err != nil {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-61>)        return nil, err
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-62>)    }
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-63>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-64>)    // flightAgent runs in ModeTask: may ask the user clarifying questions and
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-65>)    // automatically returns control to the coordinator when done. Equivalent to
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-66>)    // mode="task" in Python.
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-67>)    flightAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-68>)        Name:        "flight_booker",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-69>)        Model:       model,
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-70>)        Mode:        llmagent.ModeTask,
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-71>)        Description: "Searches for and books flights.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-72>)        Instruction: "Help the user find and book a flight using the available tools.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-73>)        Tools:       []tool.Tool{searchFlightsTool, bookFlightTool},
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-74>)    })
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-75>)    if err != nil {
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-76>)        return nil, err
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-77>)    }
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-78>)
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-79>)    // The coordinator agent declares SubAgents. ADK automatically generates
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-80>)    // weather_checker and flight_booker delegation tools, named after each
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-81>)    // subagent, so the coordinator can delegate work to each one.
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-82>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-83>)        Name:        "travel_planner",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-84>)        Model:       model,
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-85>)        Description: "Coordinator agent that delegates to weather and flight subagents.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-86>)        Instruction: "Help the user plan their trip. Use the weather checker and flight booker as needed.",
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-87>)        SubAgents:   []agent.Agent{weatherAgent, flightAgent},
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-88>)    })
    [](<https://adk.dev/workflows/collaboration/#__codelineno-1-89>)}
    
When you run this workflow, the `travel_planner` coordinator agent automatically identifies and assigns tasks to the subagents. When a subagent completes a task, it automatically returns to the coordinator agent. For more information about structuring data using **_input_schema_** and **_output_schema_** with agents, subagents, and workflow nodes, see [Data handling for agent workflows](<https://adk.dev/graphs/data-handling/>).

## Mode configuration and behaviors[¶](<https://adk.dev/workflows/collaboration/#mode-configuration-and-behaviors> "Permanent link")

Each collaboration mode has specific behaviors and limitations associated with it. The following table compares the attributes of a subagent configured with each mode:

Caution: Mode only for subagents

The **_mode_** setting is intended specifically for use with subagents invoked by a coordinator parent agent. Do not configure a root agent with the mode setting.

**Topic \ Mode** | `chat` (default) | `task` | `single_turn`  
---|---|---|---  
**Human in the Loop** | Full interaction | For clarification only | Disallowed  
**User interaction** | User chats freely with agent | Agent asks questions as needed | No user interaction  
**Control flow** | Agent controls until manual handoff | Agent controls until task complete | Returns immediately after task  
**Parallel execution** | Not supported | Not supported | Multiple tasks can run in parallel  
**Return to parent** | Manual (via transfer) | Automatic (via `finish_task`) | Automatic (with result)  
  
**Table 1.** Comparison of ADK Collaboration agent **_mode_** behavior and limitations.

## Operating considerations[¶](<https://adk.dev/workflows/collaboration/#operating-considerations> "Permanent link")

When using collaboration agent modes, there are a few control transfer and context management considerations to consider, as described in the following sections.

### Workflow Node and Agent transfers[¶](<https://adk.dev/workflows/collaboration/#workflow-node-and-agent-transfers> "Permanent link")

Agents configured with **_task_** or **_single-turn_** modes can be used as Workflow Agent graph nodes, and with **_LlmAgent_** instances. However the execution transfer behavior is different depending on the calling, or parent, agent:

**As a workflow graph node:** When a task or single-turn agent is placed within a workflow graph — such as a **_SequentialAgent_** or **_ParallelAgent_** (Python and Go prebuilt agents), or wrapped with `workflow.NewAgentNode` in the ADK Go v2.0.0 graph engine — the agent executes its task. Upon completion, control automatically advances to the next node based on the logic of the workflow agent's graph.

**As a transferee from an LlmAgent:** When a parent **_LlmAgent_** transfers control to a task agent via the delegation tool named after that subagent, the task agent executes until it calls `finish_task`. At that point, control automatically returns to the originating agent that initiated the transfer. This behavior differs from default, chat **_mode_** agents, which require explicit `transfer_to_agent` calls to hand back control.

**Invocation Context** | **After Task Completion**  
---|---  
Workflow node | Advances to next node in the graph  
Transfer from LlmAgent | Returns control to the originating agent  
  
This distinction allows the same task agent to be reused in both contexts without modification. The runtime determines the appropriate control flow based on how the agent was invoked.

### Agent context isolation[¶](<https://adk.dev/workflows/collaboration/#agent-context-isolation> "Permanent link")

Each **_task_** or **_single-turn_** mode agent operates in its own isolated session branch. When these agents operate in parallel, each agent only sees events from its own branch when building context for AI model calls, and cannot see what its peer agents are doing. Once all parallel branches complete, the parent agent receives the collected results and can proceed.

## Known limitations[¶](<https://adk.dev/workflows/collaboration/#known-limitations> "Permanent link")

There are some known limitations with agent collaboration modes:

  * **_Task_ mode agents** must be leaf agents and cannot have subagents.

Back to top 