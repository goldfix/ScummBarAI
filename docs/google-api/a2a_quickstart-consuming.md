# Python - Agent Development Kit (ADK)

> Source: [https://adk.dev/a2a/quickstart-consuming/](https://adk.dev/a2a/quickstart-consuming/)

[ Skip to content ](<https://adk.dev/a2a/quickstart-consuming/#quickstart-consuming-a-remote-agent-via-a2a>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/a2a/quickstart-consuming.md> "Edit this page on GitHub") [ ](<https://adk.dev/a2a/quickstart-consuming/index.md> "View this page as Markdown")

# Quickstart: Consuming a remote agent via A2A[¶](<https://adk.dev/a2a/quickstart-consuming/#quickstart-consuming-a-remote-agent-via-a2a> "Permanent link")

Supported in ADKPythonExperimental

This quickstart covers the most common starting point for any developer: **"There is a remote agent, how do I let my ADK agent use it via A2A?"**. This is crucial for building complex multi-agent systems where different agents need to collaborate and interact.

A2A Python SDK version compatibility

ADK's A2A integration works with both major versions of the A2A SDK (`a2a-sdk` 0.3.x and 1.x.x). The installed A2A SDK version is detected automatically, so no changes to your ADK application code are needed.

Although `a2a-sdk` 0.3.x is supported in compatibility mode, new integrations should target 1.x.x. If your code references `a2a-sdk` types directly (for example, custom executors or hand-constructed `AgentCard` instances), see the [A2A SDK v1.0 migration guide](<https://github.com/a2aproject/a2a-python/tree/main/docs/migrations/v1_0>) when moving to 1.x.x.

## Overview[¶](<https://adk.dev/a2a/quickstart-consuming/#overview> "Permanent link")

This sample demonstrates the **Agent2Agent (A2A)** architecture in the Agent Development Kit (ADK), showcasing how multiple agents can work together to handle complex tasks. The sample implements an agent that can roll dice and check if numbers are prime.
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-0-1>)┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-0-2>)│   Root Agent    │───▶│   Roll Agent     │    │   Remote Prime     │
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-0-3>)│  (Local)        │    │   (Local)        │    │   Agent            │
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-0-4>)│                 │    │                  │    │  (localhost:8001)  │
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-0-5>)│                 │───▶│                  │◀───│                    │
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-0-6>)└─────────────────┘    └──────────────────┘    └────────────────────┘
    
The A2A Basic sample consists of:

  * **Root Agent** (`root_agent`): The main orchestrator that delegates tasks to specialized sub-agents
  * **Roll Agent** (`roll_agent`): A local sub-agent that handles dice rolling operations
  * **Prime Agent** (`prime_agent`): A remote A2A agent that checks if numbers are prime, this agent is running on a separate A2A server

## Exposing Your Agent with the ADK Server[¶](<https://adk.dev/a2a/quickstart-consuming/#exposing-your-agent-with-the-adk-server> "Permanent link")

The ADK comes with a built-in CLI command, `adk api_server --a2a` to expose your agent using the A2A protocol.

In the `a2a_basic` example, you will first need to expose the `check_prime_agent` via an A2A server, so that the local root agent can use it.

### 1\. Getting the Sample Code[¶](<https://adk.dev/a2a/quickstart-consuming/#getting-the-sample-code> "Permanent link")

First, make sure you have the necessary dependencies installed:
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-1-1>)pip install google-adk[a2a]
    
You can clone and navigate to the [**`a2a_basic`** sample](<https://github.com/google/adk-python/tree/main/contributing/samples/a2a/a2a_basic>) here:
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-2-1>)git clone https://github.com/google/adk-python.git
    
As you'll see, the folder structure is as follows:
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-1>)a2a_basic/
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-2>)├── remote_a2a/
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-3>)│   └── check_prime_agent/
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-4>)│       ├── __init__.py
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-5>)│       ├── agent.json
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-6>)│       └── agent.py
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-7>)├── README.md
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-8>)├── __init__.py
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-3-9>)└── agent.py # local root agent
    
#### Main Agent (`a2a_basic/agent.py`)[¶](<https://adk.dev/a2a/quickstart-consuming/#main-agent-a2a_basicagentpy> "Permanent link")

  * **`roll_die(sides: int)`** : Function tool for rolling dice
  * **`roll_agent`** : Local agent specialized in dice rolling
  * **`prime_agent`** : Remote A2A agent configuration
  * **`root_agent`** : Main orchestrator with delegation logic

#### Remote Prime Agent (`a2a_basic/remote_a2a/check_prime_agent/`)[¶](<https://adk.dev/a2a/quickstart-consuming/#remote-prime-agent-a2a_basicremote_a2acheck_prime_agent> "Permanent link")

  * **`agent.py`** : Implementation of the prime checking service
  * **`agent.json`** : Agent card of the A2A agent
  * **`check_prime(nums: list[int])`** : Prime number checking algorithm

### 2\. Start the Remote Prime Agent server[¶](<https://adk.dev/a2a/quickstart-consuming/#start-the-remote-prime-agent-server> "Permanent link")

To show how your ADK agent can consume a remote agent via A2A, you'll first need to start a remote agent server, which will host the prime agent (under `check_prime_agent`).
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-4-1>)# Start the remote a2a server that serves the check_prime_agent on port 8001
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-4-2>)adk api_server --a2a --port 8001 contributing/samples/a2a/a2a_basic/remote_a2a
    
Adding logging for debugging with `--log_level debug`

To enable debug-level logging, you can add `--log_level debug` to your `adk api_server`, as in: 
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-5-1>)adk api_server --a2a --port 8001 contributing/samples/a2a/a2a_basic/remote_a2a --log_level debug
    
This will give richer logs for you to inspect when testing your agents.

Why use port 8001?

In this quickstart, when testing locally, your agents will be using localhost, so the `port` for the A2A server for the exposed agent (the remote, prime agent) must be different from the consuming agent's port. The default port for `adk web` where you will interact with the consuming agent is `8000`, which is why the A2A server is created using a separate port, `8001`.

Once executed, you should see something like:
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-6-1>)INFO:     Started server process [56558]
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-6-2>)INFO:     Waiting for application startup.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-6-3>)INFO:     Application startup complete.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-6-4>)INFO:     Uvicorn running on http://127.0.0.1:8001 (Press CTRL+C to quit)
    
### 3\. Look out for the required agent card (`agent-card.json`) of the remote agent[¶](<https://adk.dev/a2a/quickstart-consuming/#look-out-for-the-required-agent-card-agent-json-of-the-remote-agent> "Permanent link")

A2A Protocol requires that each agent must have an agent card that describes what it does.

If someone else has already built the remote A2A agent that you are looking to consume in your agent, then you should confirm that they have an agent card (`agent-card.json`).

In the sample, the `check_prime_agent` already has an agent card provided:

a2a_basic/remote_a2a/check_prime_agent/agent-card.json
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-1>){
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-2>)  "capabilities": {},
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-3>)  "defaultInputModes": ["text/plain"],
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-4>)  "defaultOutputModes": ["application/json"],
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-5>)  "description": "An agent specialized in checking whether numbers are prime. It can efficiently determine the primality of individual numbers or lists of numbers.",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-6>)  "name": "check_prime_agent",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-7>)  "skills": [
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-8>)    {
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-9>)      "id": "prime_checking",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-10>)      "name": "Prime Number Checking",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-11>)      "description": "Check if numbers in a list are prime using efficient mathematical algorithms",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-12>)      "tags": ["mathematical", "computation", "prime", "numbers"]
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-13>)    }
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-14>)  ],
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-15>)  "url": "http://localhost:8001/a2a/check_prime_agent",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-16>)  "version": "1.0.0"
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-7-17>)}
    
More info on agent cards in ADK

In ADK, you can use a `to_a2a(root_agent)` wrapper which automatically generates an agent card for you. If you're interested in learning more about how to expose your existing agent so others can use it, then please look at the [A2A Quickstart (Exposing)](<https://adk.dev/a2a/quickstart-exposing/>) tutorial.

### 4\. Run the Main (Consuming) Agent[¶](<https://adk.dev/a2a/quickstart-consuming/#run-the-main-consuming-agent> "Permanent link")
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-8-1>)# In a separate terminal, run the adk web server
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-8-2>)adk web contributing/samples/
    
#### How it works[¶](<https://adk.dev/a2a/quickstart-consuming/#how-it-works> "Permanent link")

The main agent uses the `RemoteA2aAgent()` function to consume the remote agent (`prime_agent` in our example). As you can see below, `RemoteA2aAgent()` requires the `name`, `description`, and the URL of the `agent_card`.

a2a_basic/agent.py
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-1>)<...code truncated...>
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-2>)
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-3>)from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-4>)from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-5>)
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-6>)prime_agent = RemoteA2aAgent(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-7>)    name="prime_agent",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-8>)    description="Agent that handles checking if numbers are prime.",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-9>)    agent_card=(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-10>)        f"http://localhost:8001/a2a/check_prime_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-11>)    ),
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-12>)    use_legacy=False,
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-13>))
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-14>)
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-9-15>)<...code truncated>
    
Using the new A2A integration

By setting `use_legacy=False`, the agent will use the new ADK-A2A integration, as it will send the [A2A extension](<https://adk.dev/a2a/a2a-extension/>) to the remote agent.

Then, you can simply use the `RemoteA2aAgent` in your agent. In this case, `prime_agent` is used as one of the sub-agents in the `root_agent` below:

a2a_basic/agent.py
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-1>)from google.adk.agents.llm_agent import Agent
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-2>)from google.genai import types
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-3>)
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-4>)root_agent = Agent(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-5>)    model="gemini-flash-latest",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-6>)    name="root_agent",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-7>)    instruction="""
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-8>)      <You are a helpful assistant that can roll dice and check if numbers are prime.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-9>)      You delegate rolling dice tasks to the roll_agent and prime checking tasks to the prime_agent.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-10>)      Follow these steps:
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-11>)      1. If the user asks to roll a die, delegate to the roll_agent.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-12>)      2. If the user asks to check primes, delegate to the prime_agent.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-13>)      3. If the user asks to roll a die and then check if the result is prime, call roll_agent first, then pass the result to prime_agent.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-14>)      Always clarify the results before proceeding.>
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-15>)    """,
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-16>)    global_instruction=(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-17>)        "You are DicePrimeBot, ready to roll dice and check prime numbers."
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-18>)    ),
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-19>)    sub_agents=[roll_agent, prime_agent],
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-20>)    tools=[example_tool],
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-21>)    generate_content_config=types.GenerateContentConfig(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-22>)        safety_settings=[
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-23>)            types.SafetySetting(  # avoid false alarm about rolling dice.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-24>)                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-25>)                threshold=types.HarmBlockThreshold.OFF,
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-26>)            ),
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-27>)        ]
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-28>)    ),
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-10-29>))
    
### Advanced Configuration: Custom Converters and Interceptors[¶](<https://adk.dev/a2a/quickstart-consuming/#advanced-configuration-custom-converters-and-interceptors> "Permanent link")

Internally, the `RemoteA2aAgent` translates between the A2A protocol format and the ADK's native `Event` system. You can customize this behaviour by passing an [`A2aRemoteAgentConfig`](<https://github.com/google/adk-python/blob/main/src/google/adk/a2a/agent/config.py>) object via the `config` parameter to `RemoteA2aAgent`.

This allows you to define custom type mappings, inject request parameters, and intercept requests or responses.

#### Converters[¶](<https://adk.dev/a2a/quickstart-consuming/#converters> "Permanent link")

Converters handle the translation of incoming A2A responses into native ADK objects. You can provide your own mapping functions for the following hooks:

  * **`a2a_message_converter`** : Converts standard A2A Messages into ADK `Event` objects.
  * **`a2a_task_converter`** : Converts an A2A Task into an ADK `Event`.
  * **`a2a_status_update_converter`** : Converts A2A `TaskStatusUpdateEvent`s into ADK `Event` objects.
  * **`a2a_artifact_update_converter`** : Converts A2A `TaskArtifactUpdateEvent`s into ADK `Event` objects.
  * **`a2a_part_converter`** : A foundational low-level hook utilized internally by other converters to convert individual A2A Message Parts into GenAI `Part` objects.

Note

These custom client converters are used only when the response is coming from the new implementation of the [agent executor](<https://github.com/google/adk-python/blob/main/src/google/adk/a2a/executor/a2a_agent_executor_impl.py>). For more details, see the [A2A extension](<https://adk.dev/a2a/a2a-extension/>).

#### Request Interceptors[¶](<https://adk.dev/a2a/quickstart-consuming/#request-interceptors> "Permanent link")

You can inject a list of `request_interceptors` to add middleware logic to A2A requests:

  * **`before_request`** : Executed before the agent starts processing. You can modify the `A2AMessage`, or return an ADK `Event` to immediately abort the request and return that event to the caller.
  * **`after_request`** : Executed after the agent has processed the request. You can modify the resulting ADK `Event`, or return `None` to filter out and drop the event entirely.

#### Request Parameters Configuration[¶](<https://adk.dev/a2a/quickstart-consuming/#request-parameters-configuration> "Permanent link")

Through interceptors, you can also modify the `ParametersConfig` for the A2A request to inject:

  * **`request_metadata`** : Pass custom metadata dictionaries into the request headers.
  * **`client_call_context`** : Inject specific client call contexts for the underlying transport.

    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-1>)<...code truncated...>
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-2>)
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-3>)from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-4>)from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-5>)
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-6>)prime_agent = RemoteA2aAgent(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-7>)    name="prime_agent",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-8>)    description="Agent that handles checking if numbers are prime.",
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-9>)    agent_card=(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-10>)        f"http://localhost:8001/a2a/check_prime_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-11>)    ),
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-12>)    use_legacy=False,
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-13>)    config=A2aRemoteAgentConfig(
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-14>)        a2a_message_converter=my_a2a_message_converter,
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-15>)        request_interceptors=[my_request_interceptor],
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-16>)    ),
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-17>))
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-18>)
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-11-19>)<...code truncated>
    
## Example Interactions[¶](<https://adk.dev/a2a/quickstart-consuming/#example-interactions> "Permanent link")

Once both your main and remote agents are running, you can interact with the root agent to see how it calls the remote agent via A2A:

**Simple Dice Rolling:** This interaction uses a local agent, the Roll Agent:
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-12-1>)User: Roll a 6-sided die
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-12-2>)Bot: I rolled a 4 for you.
    
**Prime Number Checking:**

This interaction uses a remote agent via A2A, the Prime Agent:
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-13-1>)User: Is 7 a prime number?
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-13-2>)Bot: Yes, 7 is a prime number.
    
**Combined Operations:**

This interaction uses both the local Roll Agent and the remote Prime Agent:
    
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-14-1>)User: Roll a 10-sided die and check if it's prime
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-14-2>)Bot: I rolled an 8 for you.
    [](<https://adk.dev/a2a/quickstart-consuming/#__codelineno-14-3>)Bot: 8 is not a prime number.
    
## Next Steps[¶](<https://adk.dev/a2a/quickstart-consuming/#next-steps> "Permanent link")

Now that you have created an agent that's using a remote agent via an A2A server, the next step is to learn how to connect to it from another agent.

  * [**A2A Quickstart (Exposing)**](<https://adk.dev/a2a/quickstart-exposing/>): Learn how to expose your existing agent so that other agents can use it via the A2A Protocol.

Back to top 