# Environment Simulation - Agent Development Kit (ADK)

> Source: [https://adk.dev/evaluate/environment_simulation/](https://adk.dev/evaluate/environment_simulation/)

[ Skip to content ](<https://adk.dev/evaluate/environment_simulation/#environment-simulation-for-evaluations>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/evaluate/environment_simulation.md> "Edit this page on GitHub") [ ](<https://adk.dev/evaluate/environment_simulation/index.md> "View this page as Markdown")

# Environment simulation for evaluations[¶](<https://adk.dev/evaluate/environment_simulation/#environment-simulation-for-evaluations> "Permanent link")

Supported in ADKPython v1.24.0

When evaluating agents that rely on external dependencies — such as APIs, databases, or third-party services — running those tools live during testing can be slow, costly, or unreliable. The **Environment Simulator** lets you safely intercept these tool calls during agent execution and replace them with controlled, deterministic responses, without modifying the agent itself. This approach can fill a critical gap in the agent improvement loop, allowing you to create hermetic, offline test runs that isolate your agent logic for reliable scoring.

Overall, this feature lets you:

  * Test how an agent handles API errors or edge-case responses.
  * Run evaluations offline, without access to live backends.
  * Generate realistic mock responses automatically using an LLM.
  * Produce reproducible test runs by seeding probabilistic injections.

The Environment Simulation integrates with ADK's tool execution pipeline via the [`before_tool_callback`](<https://adk.dev/callbacks/types-of-callbacks/#tool-execution-callbacks>) hook or the [plugin system](<https://adk.dev/plugins/>), so no changes to your agent code are required.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-0-1>)The Environment Simulation is an experimental feature. Its API may change in future
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-0-2>)releases.
    
## How it works[¶](<https://adk.dev/evaluate/environment_simulation/#how-it-works> "Permanent link")

While [User Simulation](<https://adk.dev/evaluate/user-sim/>) drives the conversation forward, Environment Simulation provides the stable backend. At a high level, the Environment Simulator sits between your agent and its tools. When the agent calls a tool, the simulator intercepts the call and decides whether to return a synthetic response — either a predefined injection or an LLM-generated mock — or to let the real tool execute.

The decision logic follows this order for each configured tool:

  1. **Injection configs** are checked first, in order. If a matching injection is found (based on argument matching and probability), its error or response is returned immediately.
  2. **Mock strategy** is used as a fallback if no injection config applies. The simulator calls an LLM to generate a realistic response based on the tool's schema and any stateful context.
  3. **No-op** is returned (`None`) if the tool is not in the simulator config, allowing the real tool to execute normally.

## Integration[¶](<https://adk.dev/evaluate/environment_simulation/#integration> "Permanent link")

The `EnvironmentSimulationFactory` class provides two integration points:

  * `create_callback()` — Returns an async callable suitable for use as a `before_tool_callback` on any `LlmAgent`.
  * `create_plugin()` — Returns an `EnvironmentSimulationPlugin` instance that integrates with the ADK plugin system.

### Using as a callback[¶](<https://adk.dev/evaluate/environment_simulation/#using-as-a-callback> "Permanent link")

The following example shows how to create an environment simulation as one of the adk agent callbacks.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-2>)from google.adk.tools.environment_simulation import EnvironmentSimulationFactory
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-3>)from google.adk.tools.environment_simulation.environment_simulation_config import (
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-4>)    EnvironmentSimulationConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-5>)    InjectedError,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-6>)    InjectionConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-7>)    ToolSimulationConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-8>))
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-9>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-10>)config = EnvironmentSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-11>)    tool_simulation_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-12>)        ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-13>)            tool_name="get_user_profile",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-14>)            injection_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-15>)                InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-16>)                    injected_error=InjectedError(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-17>)                        injected_http_error_code=503,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-18>)                        error_message="Service temporarily unavailable.",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-19>)                    )
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-20>)                )
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-21>)            ],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-22>)        )
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-23>)    ]
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-24>))
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-25>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-26>)agent = LlmAgent(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-27>)    name="my_agent",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-28>)    model="gemini-flash-latest",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-29>)    tools=[get_user_profile],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-30>)    before_tool_callback=EnvironmentSimulationFactory.create_callback(config),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-1-31>))
    
### Using as a plugin[¶](<https://adk.dev/evaluate/environment_simulation/#using-as-a-plugin> "Permanent link")

The following example shows how to create environment simulation as an ADK agent plugin.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-1>)from google.adk.apps import App
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-2>)from google.adk.tools.environment_simulation import EnvironmentSimulationFactory
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-3>)from google.adk.tools.environment_simulation.environment_simulation_config import (
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-4>)    EnvironmentSimulationConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-5>)    MockStrategy,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-6>)    ToolSimulationConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-7>))
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-8>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-9>)config = EnvironmentSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-10>)    tool_simulation_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-11>)        ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-12>)            tool_name="search_products",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-13>)            mock_strategy_type=MockStrategy.MOCK_STRATEGY_TOOL_SPEC,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-14>)        )
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-15>)    ]
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-16>))
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-17>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-18>)app = App(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-19>)    agent=my_agent,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-20>)    plugins=[EnvironmentSimulationFactory.create_plugin(config)],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-2-21>))
    
## Configuration reference[¶](<https://adk.dev/evaluate/environment_simulation/#configuration-reference> "Permanent link")

You can configure the Environment Simulator with a set of dataclasses. The following sections provide a detailed reference for each configuration object.

### `EnvironmentSimulationConfig`[¶](<https://adk.dev/evaluate/environment_simulation/#environmentsimulationconfig> "Permanent link")

The top-level configuration object.

Field | Type | Default | Description  
---|---|---|---  
`tool_simulation_configs` | `List[ToolSimulationConfig]` | required | One entry per tool to simulate. Must not be empty, and tool names must be unique.  
`simulation_model` | `str` | `"gemini-flash-latest"` | The LLM used for tool connection analysis and mock response generation.  
`simulation_model_configuration` | `GenerateContentConfig` | thinking enabled | LLM generation config for internal simulator calls.  
`environment_data` | `str \| None` | `None` | Optional environment context (e.g., a JSON database snapshot) passed to mock strategies to generate more realistic responses.  
`tracing` | `str \| None` | `None` | Tracing data (e.g., a prior agent run trace in JSON string format) to provide historical context.  
  
### `ToolSimulationConfig`[¶](<https://adk.dev/evaluate/environment_simulation/#toolsimulationconfig> "Permanent link")

Defines how a single named tool should be simulated.

Field | Type | Default | Description  
---|---|---|---  
`tool_name` | `str` | required | Must match the tool's registered name exactly.  
`injection_configs` | `List[InjectionConfig]` | `[]` | Zero or more injection configs, checked in order before the mock strategy.  
`mock_strategy_type` | `MockStrategy` | `MOCK_STRATEGY_UNSPECIFIED` | Fallback strategy when no injection is triggered.  
  
### `InjectionConfig`[¶](<https://adk.dev/evaluate/environment_simulation/#injectionconfig> "Permanent link")

Controls a single synthetic response that can be injected into a tool call. Exactly one of `injected_error` or `injected_response` must be set.

Field | Type | Default | Description  
---|---|---|---  
`injected_error` | `InjectedError \| None` | `None` | Error to return (mutually exclusive with `injected_response`).  
`injected_response` | `Dict[str, Any] \| None` | `None` | Fixed response dict to return (mutually exclusive with `injected_error`).  
`injection_probability` | `float` | `1.0` | Probability `[0.0, 1.0]` that this injection fires.  
`match_args` | `Dict[str, Any] \| None` | `None` | If set, the injection only fires when the tool's arguments contain all key-value pairs in `match_args`.  
`injected_latency_seconds` | `float` | `0.0` | Artificial delay (≤ 120 s) added before returning the injection result.  
`random_seed` | `int \| None` | `None` | Seed for the probability check, enabling deterministic injection behavior.  
  
### `InjectedError`[¶](<https://adk.dev/evaluate/environment_simulation/#injectederror> "Permanent link")

Defines an HTTP-style error response.

Field | Type | Description  
---|---|---  
`injected_http_error_code` | `int` | HTTP status code to surface as  
: : : `"error_code"` in the tool response. : |  |   
`error_message` | `str` | Human-readable message surfaced as  
: : : `"error_message"` in the tool response. : |  |   
  
### `MockStrategy`[¶](<https://adk.dev/evaluate/environment_simulation/#mockstrategy> "Permanent link")

Enum controlling how the simulator generates responses when no injection fires.

Value | Description  
---|---  
`MOCK_STRATEGY_TOOL_SPEC` | Uses the tool's schema and stateful context to  
: : prompt an LLM to generate a realistic response. : |   
`MOCK_STRATEGY_TRACING` | _(Deprecated)_ Please use  
: : `MOCK_STRATEGY_TOOL_SPEC` with tracing input. : |   
  
## Injection mode[¶](<https://adk.dev/evaluate/environment_simulation/#injection-mode> "Permanent link")

Use injection configs to test specific failure or edge-case scenarios. Injections are evaluated in list order; the first one whose `match_args` criteria are met (and whose probability check passes) is applied.

### Injecting errors[¶](<https://adk.dev/evaluate/environment_simulation/#injecting-errors> "Permanent link")

The following example shows how to inject errors with specific error code and error message to the agent.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-1>)from google.adk.tools.environment_simulation.environment_simulation_config import (
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-2>)    InjectedError,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-3>)    InjectionConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-4>)    ToolSimulationConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-5>))
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-6>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-7>)ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-8>)    tool_name="charge_payment",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-9>)    injection_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-10>)        InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-11>)            injected_error=InjectedError(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-12>)                injected_http_error_code=402,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-13>)                error_message="Payment declined.",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-14>)            )
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-15>)        )
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-16>)    ],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-3-17>))
    
The agent will receive `{"error_code": 402, "error_message": "Payment declined."}` instead of a real tool result, allowing you to evaluate how the agent handles payment failures.

### Injecting fixed responses[¶](<https://adk.dev/evaluate/environment_simulation/#injecting-fixed-responses> "Permanent link")

Use the following InjectionConfig to specify a success response with fixed response payload. 
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-4-1>)InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-4-2>)    injected_response={"status": "ok", "order_id": "ORD-9999"}
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-4-3>))
    
### Conditional injection with argument matching[¶](<https://adk.dev/evaluate/environment_simulation/#conditional-injection-with-argument-matching> "Permanent link")

Use `match_args` to inject only when specific arguments are passed.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-5-1>)InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-5-2>)    match_args={"item_id": "ITEM-404"},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-5-3>)    injected_error=InjectedError(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-5-4>)        injected_http_error_code=404,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-5-5>)        error_message="Item not found.",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-5-6>)    ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-5-7>))
    
Here, the error is injected only when the tool is called with `item_id="ITEM-404"`. All other calls pass through to the next injection config or to the mock strategy.

### Probabilistic injection[¶](<https://adk.dev/evaluate/environment_simulation/#probabilistic-injection> "Permanent link")

Set `injection_probability` to a value between `0.0` and `1.0` to simulate flaky behavior. For reproducible test runs, pin the random outcome with `random_seed`.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-1>)InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-2>)    injection_probability=0.3,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-3>)    random_seed=42,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-4>)    injected_error=InjectedError(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-5>)        injected_http_error_code=500,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-6>)        error_message="Internal server error.",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-7>)    ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-6-8>))
    
### Injecting latency[¶](<https://adk.dev/evaluate/environment_simulation/#injecting-latency> "Permanent link")

Use `injected_latency_seconds` to simulate slow backend responses, useful for testing timeout handling or user experience under degraded conditions.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-7-1>)InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-7-2>)    injected_latency_seconds=5.0,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-7-3>)    injected_response={"result": "slow but successful"},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-7-4>))
    
### Combining multiple injection configs[¶](<https://adk.dev/evaluate/environment_simulation/#combining-multiple-injection-configs> "Permanent link")

Multiple injection configs on a single tool are checked in order. You can combine them to test multiple scenarios:
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-1>)ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-2>)    tool_name="get_inventory",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-3>)    injection_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-4>)        # Always fail for a specific out-of-stock item
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-5>)        InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-6>)            match_args={"sku": "OOS-001"},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-7>)            injected_response={"quantity": 0, "available": False},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-8>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-9>)        # Randomly fail 20% of the time for all other items
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-10>)        InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-11>)            injection_probability=0.2,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-12>)            random_seed=7,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-13>)            injected_error=InjectedError(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-14>)                injected_http_error_code=503,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-15>)                error_message="Inventory service unavailable.",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-16>)            ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-17>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-18>)    ],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-8-19>))
    
## Mock strategy mode[¶](<https://adk.dev/evaluate/environment_simulation/#mock-strategy-mode> "Permanent link")

When you want the simulator to generate plausible responses automatically — rather than returning hand-crafted values — use `MOCK_STRATEGY_TOOL_SPEC`.

The simulator uses an LLM to:

  1. Analyze the schemas of all tools the agent has access to, and identify _stateful dependencies_ between them (e.g., a `create_order` tool produces an `order_id` that `get_order` consumes).
  2. Track a **state store** of IDs and resources created during the session.
  3. Generate a response that is consistent with the tool's schema and the current state — returning a 404-style error if a consuming tool requests a resource that was never created.

    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-1>)from google.adk.tools.environment_simulation.environment_simulation_config import (
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-2>)    EnvironmentSimulationConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-3>)    MockStrategy,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-4>)    ToolSimulationConfig,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-5>))
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-6>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-7>)config = EnvironmentSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-8>)    tool_simulation_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-9>)        ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-10>)            tool_name="create_order",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-11>)            mock_strategy_type=MockStrategy.MOCK_STRATEGY_TOOL_SPEC,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-12>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-13>)        ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-14>)            tool_name="get_order",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-15>)            mock_strategy_type=MockStrategy.MOCK_STRATEGY_TOOL_SPEC,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-16>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-17>)        ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-18>)            tool_name="cancel_order",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-19>)            mock_strategy_type=MockStrategy.MOCK_STRATEGY_TOOL_SPEC,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-20>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-21>)    ]
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-9-22>))
    
With this config, the simulator will automatically generate an `order_id` when `create_order` is mocked, and use it to return consistent results (or a not-found error) when `get_order` or `cancel_order` are subsequently called.

### Providing environment data[¶](<https://adk.dev/evaluate/environment_simulation/#providing-environment-data> "Permanent link")

Pass domain-specific context through `environment_data` to make mock responses more realistic. This can be a JSON string representing a snapshot of your database or any structured context the LLM should use when generating responses.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-1>)import json
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-2>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-3>)db_snapshot = {
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-4>)    "products": [
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-5>)        {"id": "P-001", "name": "Wireless Headphones", "price": 79.99, "stock": 12},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-6>)        {"id": "P-002", "name": "USB-C Hub", "price": 34.99, "stock": 0},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-7>)    ],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-8>)    "warehouse_location": "US-WEST-2",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-9>)}
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-10>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-11>)config = EnvironmentSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-12>)    tool_simulation_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-13>)        ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-14>)            tool_name="search_products",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-15>)            mock_strategy_type=MockStrategy.MOCK_STRATEGY_TOOL_SPEC,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-16>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-17>)    ],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-18>)    environment_data=json.dumps(db_snapshot),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-10-19>))
    
The LLM will use this data to return product names, prices, and stock levels that match your domain, rather than generating arbitrary placeholder values.

### Providing tracing data[¶](<https://adk.dev/evaluate/environment_simulation/#providing-tracing-data> "Permanent link")

Feed traces generated in the agent to be mocked through `tracing` to make mock responses more realistic.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-1>)import json
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-2>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-3>)agent_traces = [
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-4>)    {
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-5>)        "invocation_id": "inv-001",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-6>)        "user_content": {"role": "user", "parts": [{"text": "Search for high-end headphones"}]},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-7>)        "intermediate_data": {
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-8>)            "tool_uses": [
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-9>)                {
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-10>)                    "name": "search_products",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-11>)                    "args": {"query": "high-end headphones"},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-12>)                    "response": {"products": [{"id": "P-123", "name": "Premium Wireless ANC Headphones"}]}
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-13>)                }
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-14>)            ]
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-15>)        }
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-16>)    }
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-17>)]
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-18>)
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-19>)config = EnvironmentSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-20>)    tool_simulation_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-21>)        ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-22>)            tool_name="search_products",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-23>)            mock_strategy_type=MockStrategy.MOCK_STRATEGY_TOOL_SPEC,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-24>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-25>)    ],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-26>)    tracing=json.dumps(agent_traces),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-11-27>))
    
The LLM will use this data to return product names, prices, and stock levels that match your domain, rather than generating arbitrary placeholder values.

## Mixing injections and mock strategy[¶](<https://adk.dev/evaluate/environment_simulation/#mixing-injections-and-mock-strategy> "Permanent link")

Injection configs and a mock strategy can be combined on the same tool. Injections are always checked first; the mock strategy fires only when no injection applies.
    
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-1>)ToolSimulationConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-2>)    tool_name="send_notification",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-3>)    injection_configs=[
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-4>)        # Always fail for a known-bad recipient
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-5>)        InjectionConfig(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-6>)            match_args={"recipient_id": "INVALID"},
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-7>)            injected_error=InjectedError(
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-8>)                injected_http_error_code=400,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-9>)                error_message="Invalid recipient.",
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-10>)            ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-11>)        ),
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-12>)    ],
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-13>)    # For all other recipients, generate a plausible success response
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-14>)    mock_strategy_type=MockStrategy.MOCK_STRATEGY_TOOL_SPEC,
    [](<https://adk.dev/evaluate/environment_simulation/#__codelineno-12-15>))
    
Back to top 