# Overview - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools-custom/function-tools/](https://adk.dev/tools-custom/function-tools/)

[ Skip to content ](<https://adk.dev/tools-custom/function-tools/#function-tools>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools-custom/function-tools.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools-custom/function-tools/index.md> "View this page as Markdown")

# Function tools[¶](<https://adk.dev/tools-custom/function-tools/#function-tools> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

When pre-built ADK tools don't meet your requirements, you can create custom _function tools_. Building function tools allows you to create tailored functionality, such as connecting to proprietary databases or implementing unique algorithms. For example, a function tool, `myfinancetool`, might be a function that calculates a specific financial metric. ADK also supports long-running functions, so if that calculation takes a while, the agent can continue working on other tasks.

ADK offers several ways to create functions tools, each suited to different levels of complexity and control:

  * [Function tools](<https://adk.dev/tools-custom/function-tools/#function-tool>)
  * [Long running function tools](<https://adk.dev/tools-custom/function-tools/#long-run-tool>)
  * [Agent-as-a-Tool](<https://adk.dev/tools-custom/function-tools/#agent-tool>)

## Function tools[¶](<https://adk.dev/tools-custom/function-tools/#function-tool> "Permanent link")

Transforming a Python function into a tool is a straightforward way to integrate custom logic into your agents. When you assign a function to an agent’s `tools` list, the framework automatically wraps it as a `FunctionTool`.

### How it works[¶](<https://adk.dev/tools-custom/function-tools/#how-it-works> "Permanent link")

The ADK framework automatically inspects your Python function's signature—including its name, docstring, parameters, type hints, and default values—to generate a schema. This schema is what the LLM uses to understand the tool's purpose, when to use it, and what arguments it requires.

### Define function signatures[¶](<https://adk.dev/tools-custom/function-tools/#define-function-signatures> "Permanent link")

A well-defined function signature is crucial for the LLM to use your tool correctly.

#### Parameters[¶](<https://adk.dev/tools-custom/function-tools/#parameters> "Permanent link")

##### Required parameters[¶](<https://adk.dev/tools-custom/function-tools/#required-parameters> "Permanent link")

PythonGoJavaKotlin

A parameter is considered **required** if it has a type hint but **no default value**. The LLM must provide a value for this argument when it calls the tool. The parameter's description is taken from the function's docstring.

Example: Required Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-1>)def get_weather(city: str, unit: str):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-2>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-3>)    Retrieves the weather for a city in the specified unit.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-4>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-5>)    Args:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-6>)        city (str): The city name.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-7>)        unit (str): The temperature unit, either 'Celsius' or 'Fahrenheit'.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-8>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-9>)    # ... function logic ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-0-10>)    return {"status": "success", "report": f"Weather for {city} is sunny."}
    
In this example, both `city` and `unit` are mandatory. If the LLM tries to call `get_weather` without one of them, the ADK will return an error to the LLM, prompting it to correct the call.

In Go, you use struct tags to control the JSON schema. The two primary tags are `json` and `jsonschema`.

A parameter is considered **required** if its struct field does **not** have the `omitempty` or `omitzero` option in its `json` tag.

The `jsonschema` tag is used to provide the argument's description. This is crucial for the LLM to understand what the argument is for.

Example: Required Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-1>)// GetWeatherParams defines the arguments for the getWeather tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-2>)type GetWeatherParams struct {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-3>)    // This field is REQUIRED (no "omitempty").
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-4>)    // The jsonschema tag provides the description.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-5>)    Location string `json:"location" jsonschema:"The city and state, e.g., San Francisco, CA"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-6>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-7>)    // This field is also REQUIRED.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-8>)    Unit     string `json:"unit" jsonschema:"The temperature unit, either 'celsius' or 'fahrenheit'"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-1-9>)}
    
In this example, both `location` and `unit` are mandatory.

In Java, primitive types (e.g., `int`, `double`, `boolean`) are inherently **required** because they cannot be null. For object types (like `String` or `Integer`), they are typically considered required unless explicitly marked as optional.

The `@Schema` annotation is used to provide the argument's description and can explicitly define parameter properties. This is crucial for the LLM to understand what the argument is for.

Example: Required Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-1>)// The @Schema annotation on the parameter provides the description.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-2>)public static Map<String, Object> getWeather(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-3>)    @Schema(description = "The city and state, e.g., San Francisco, CA", name = "location")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-4>)    String location,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-5>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-6>)    @Schema(description = "The temperature unit, either 'Celsius' or 'Fahrenheit'", name = "unit")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-7>)    String unit) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-8>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-9>)    // ... function logic ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-10>)    return Map.of("status", "success", "report", "Weather for " + location + " is sunny.");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-2-11>)}
    
In this example, both `location` and `unit` are mandatory.

In Kotlin, parameters are considered **required** by default if they are of a non-nullable type and have no default value. The LLM must provide a value for these arguments.

The `@Param` annotation is used to provide the argument's description. This is crucial for the LLM to understand what the argument is for.

Example: Required Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-1>)class WeatherService {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-2>)    /**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-3>)     * Retrieves the weather for a city in the specified unit.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-4>)     */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-5>)    @Tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-6>)    fun getWeather(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-7>)        @Param("The city and state, e.g., San Francisco, CA") location: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-8>)        @Param("The temperature unit, either 'Celsius' or 'Fahrenheit'") unit: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-9>)    ): String {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-10>)        // ... function logic ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-11>)        return "Weather for $location is sunny in $unit."
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-12>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-3-13>)}
    
In this example, both `location` and `unit` are mandatory.

##### Optional parameters[¶](<https://adk.dev/tools-custom/function-tools/#optional-parameters> "Permanent link")

PythonGoJavaKotlin

A parameter is considered **optional** if you provide a **default value**. This is the standard Python way to define optional arguments. You can also mark a parameter as optional using `typing.Optional[SomeType]` or the `| None` syntax (Python 3.10+).

Use defaults only for values that are truly optional. Do not add defaults for information the model should derive from the user request or ask the user to provide.

Example: Optional Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-1>)def search_flights(destination: str, departure_date: str, flexible_days: int = 0):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-2>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-3>)    Searches for flights.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-4>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-5>)    Args:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-6>)        destination (str): The destination city.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-7>)        departure_date (str): The desired departure date.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-8>)        flexible_days (int, optional): Number of flexible days for the search. Defaults to 0.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-9>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-10>)    # ... function logic ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-11>)    if flexible_days > 0:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-12>)        return {"status": "success", "report": f"Found flexible flights to {destination}."}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-4-13>)    return {"status": "success", "report": f"Found flights to {destination} on {departure_date}."}
    
Here, `flexible_days` is optional. The LLM can choose to provide it, but it's not required.

A parameter is considered **optional** if its struct field has the `omitempty` or `omitzero` option in its `json` tag.

Example: Optional Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-1>)// GetWeatherParams defines the arguments for the getWeather tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-2>)type GetWeatherParams struct {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-3>)    // Location is required.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-4>)    Location string `json:"location" jsonschema:"The city and state, e.g., San Francisco, CA"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-5>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-6>)    // Unit is optional.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-7>)    Unit string `json:"unit,omitempty" jsonschema:"The temperature unit, either 'celsius' or 'fahrenheit'"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-8>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-9>)    // Days is optional.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-10>)    Days int `json:"days,omitzero" jsonschema:"The number of forecast days to return (defaults to 1)"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-5-11>)}
    
Here, `unit` and `days` are optional. The LLM can choose to provide them, but they are not required.

A parameter can be considered **optional** in Java by using object types that allow `null` values (such as `Integer` instead of `int`), or by explicitly defining it as optional using `java.util.Optional`.

Example: Optional Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-1>)import java.util.Map;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-2>)import java.util.Optional;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-3>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-4>)public static Map<String, Object> searchFlights(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-5>)    @Schema(description = "The destination city.", name = "destination")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-6>)    String destination,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-7>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-8>)    @Schema(description = "The desired departure date.", name = "departureDate")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-9>)    String departureDate,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-10>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-11>)    @Schema(description = "Number of flexible days for the search. Defaults to 0.", name = "flexibleDays")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-12>)    Optional<Integer> flexibleDays) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-13>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-14>)    // ... function logic ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-15>)    int days = flexibleDays.orElse(0);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-16>)    if (days > 0) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-17>)        return Map.of("status", "success", "report", "Found flexible flights to " + destination + ".");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-18>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-19>)    return Map.of("status", "success", "report", "Found flights to " + destination + " on " + departureDate + ".");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-6-20>)}
    
Here, `flexibleDays` is optional. The LLM can choose to provide it, but it's not required.

In Kotlin, a parameter is considered **optional** if it is of a **nullable type** or if it has a **default value**.

Example: Optional Parameters
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-1>)class FlightService {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-2>)    /**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-3>)     * Searches for flights.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-4>)     */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-5>)    @Tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-6>)    fun searchFlights(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-7>)        @Param("The destination city.") destination: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-8>)        @Param("The desired departure date.") departureDate: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-9>)        @Param("Number of flexible days for the search. Defaults to 0.") flexibleDays: Int? = 0,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-10>)    ): String {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-11>)        // ... function logic ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-12>)        val days = flexibleDays ?: 0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-13>)        if (days > 0) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-14>)            return "Found flexible flights to $destination."
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-15>)        }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-16>)        return "Found flights to $destination on $departureDate."
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-17>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-7-18>)}
    
Here, `flexibleDays` is optional. The LLM can choose to provide it, but it's not required.

##### Optional parameters with `typing.Optional`[¶](<https://adk.dev/tools-custom/function-tools/#optional-parameters-with-typingoptional> "Permanent link")

You can also mark a parameter as optional using `typing.Optional[SomeType]` or the `| None` syntax (Python 3.10+). This signals that the parameter can be `None`. When combined with a default value of `None`, it behaves as a standard optional parameter.

Example: `typing.Optional`

Python
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-1>)from typing import Optional
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-2>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-3>)def create_user_profile(username: str, bio: Optional[str] = None):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-4>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-5>)    Creates a new user profile.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-6>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-7>)    Args:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-8>)        username (str): The user's unique username.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-9>)        bio (str, optional): A short biography for the user. Defaults to None.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-10>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-11>)    # ... function logic ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-12>)    if bio:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-13>)        return {"status": "success", "message": f"Profile for {username} created with a bio."}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-8-14>)    return {"status": "success", "message": f"Profile for {username} created."}
    
##### Variadic parameters (`*args` and `**kwargs`)[¶](<https://adk.dev/tools-custom/function-tools/#variadic-parameters-args-and-kwargs> "Permanent link")

While you can include `*args` (variable positional arguments) and `**kwargs` (variable keyword arguments) in your function signature for other purposes, they are **ignored by the ADK framework** when generating the tool schema for the LLM. The LLM will not be aware of them and cannot pass arguments to them. It's best to rely on explicitly defined parameters for all data you expect from the LLM.

#### Context injection[¶](<https://adk.dev/tools-custom/function-tools/#context-injection> "Permanent link")

Context injection allows your custom functions to access the agent's environment, such as session state or available actions. To enable, add a parameter typed as `ToolContext` to your function. ADK automatically injects the context data before your function runs and ensures this parameter is not visible to the LLM.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-9-1>)from google.adk.tools import ToolContext
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-9-2>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-9-3>)def my_tool(arg1: str, tool_context: ToolContext):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-9-4>)    # Example: Accessing session state
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-9-5>)    user_id = tool_context.state.get("user_id")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-9-6>)    # Example: Triggering an action
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-9-7>)    # tool_context.actions.transfer_to_agent = "secondary_agent"
    
`ToolContext` provides access to:

  * **`state`:** A dictionary-like object for session-scoped data.
  * **`actions`:** Controls for agent behavior, for example `transfer_to_agent`.
  * **Methods** : To handle artifacts, such as `load_artifact` or `save_artifact`.

##### Customize the parameter name[¶](<https://adk.dev/tools-custom/function-tools/#customize-the-parameter-name> "Permanent link")

By default, the injected parameter is called `tool_context`, but you can name the parameter anything you want. ADK detects it by its `ToolContext` type annotation rather than by name. For example, to use the name `ctx`:
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-10-1>)from google.adk.tools import ToolContext
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-10-2>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-10-3>)def my_tool(arg1: str, ctx: ToolContext):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-10-4>)    # 'ctx' receives the ToolContext because of its type annotation
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-10-5>)    user_id = ctx.state.get("user_id")
    
#### Return type[¶](<https://adk.dev/tools-custom/function-tools/#return-type> "Permanent link")

The preferred return type for a Function Tool is a **dictionary** in Python, a **Map** or custom **Record or POJO** in Java, an **object** in TypeScript, or a **Map** or **Data Class** in Kotlin. This allows you to structure the response with key-value pairs, providing context and clarity to the LLM. If your function returns a type other than a dictionary or map, the framework automatically wraps it into a dictionary with a single key named **"result"**.

Strive to make your return values as descriptive as possible. _For example,_ instead of returning a numeric error code, return a dictionary with an "error_message" key containing a human-readable explanation. **Remember that the LLM** , not a piece of code, needs to understand the result. As a best practice, include a "status" key in your return dictionary to indicate the overall outcome (e.g., "success", "error", "pending"), providing the LLM with a clear signal about the operation's state.

#### Docstrings[¶](<https://adk.dev/tools-custom/function-tools/#docstrings> "Permanent link")

The docstring of your function serves as the tool's **description** and is sent to the LLM. Therefore, a well-written and comprehensive docstring is crucial for the LLM to understand how to use the tool effectively. Clearly explain the purpose of the function, the meaning of its parameters, and the expected return values. In Java, you can use Javadoc comments or the `@Schema(description="...")` annotation on your method to serve as this description. In Kotlin, you can use KDoc comments or the `@Tool(description="...")` and `@Param(description="...")` annotations to provide these descriptions.

### Pass data between tools[¶](<https://adk.dev/tools-custom/function-tools/#pass-data-between-tools> "Permanent link")

When an agent calls multiple tools in a sequence, you might need to pass data from one tool to another. The recommended way to do this is by using the `temp:` prefix in the session state.

A tool can write data to a `temp:` variable, and a subsequent tool can read it. This data is only available for the current invocation and is discarded afterwards.

Shared Invocation Context

All tool calls within a single agent turn share the same `InvocationContext`. This means they also share the same temporary (`temp:`) state, which is how data can be passed between them.

### Example[¶](<https://adk.dev/tools-custom/function-tools/#example> "Permanent link")

Example

PythonTypescriptGoJavaKotlin

This tool is a python function which obtains the Stock price of a given Stock ticker/ symbol.

_Note_ : You need to `pip install yfinance` library before using this tool.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-2>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-6>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-8>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-15>)from google.adk.agents import Agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-16>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-17>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-18>)from google.genai import types
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-19>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-20>)import yfinance as yf
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-21>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-22>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-23>)APP_NAME = "stock_app"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-24>)USER_ID = "1234"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-25>)SESSION_ID = "session1234"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-26>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-27>)def get_stock_price(symbol: str):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-28>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-29>)    Retrieves the current stock price for a given symbol.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-30>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-31>)    Args:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-32>)        symbol (str): The stock symbol (e.g., "AAPL", "GOOG").
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-33>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-34>)    Returns:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-35>)        float: The current stock price, or None if an error occurs.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-36>)    """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-37>)    try:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-38>)        stock = yf.Ticker(symbol)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-39>)        historical_data = stock.history(period="1d")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-40>)        if not historical_data.empty:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-41>)            current_price = historical_data['Close'].iloc[-1]
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-42>)            return current_price
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-43>)        else:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-44>)            return None
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-45>)    except Exception as e:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-46>)        print(f"Error retrieving stock price for {symbol}: {e}")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-47>)        return None
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-48>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-49>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-50>)stock_price_agent = Agent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-51>)    model='gemini-2.0-flash',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-52>)    name='stock_agent',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-53>)    instruction= 'You are an agent who retrieves stock prices. If a ticker symbol is provided, fetch the current price. If only a company name is given, first perform a Google search to find the correct ticker symbol before retrieving the stock price. If the provided ticker symbol is invalid or data cannot be retrieved, inform the user that the stock price could not be found.',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-54>)    description='This agent specializes in retrieving real-time stock prices. Given a stock ticker symbol (e.g., AAPL, GOOG, MSFT) or the stock name, use the tools and reliable data sources to provide the most up-to-date price.',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-55>)    tools=[get_stock_price], # You can add Python functions directly to the tools list; they will be automatically wrapped as FunctionTools.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-56>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-57>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-58>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-59>)# Session and Runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-60>)async def setup_session_and_runner():
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-61>)    session_service = InMemorySessionService()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-62>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-63>)    runner = Runner(agent=stock_price_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-64>)    return session, runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-65>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-66>)# Agent Interaction
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-67>)async def call_agent_async(query):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-68>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-69>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-70>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-71>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-72>)    async for event in events:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-73>)        if event.is_final_response():
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-74>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-75>)            print("Agent Response: ", final_response)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-76>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-77>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-78>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-79>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-11-80>)await call_agent_async("stock price of GOOG")
    
The return value from this tool will be wrapped into a dictionary.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-12-1>){"result": "$123"}
    
This tool retrieves the mocked value of a stock price.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-1>)/**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-3>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-7>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-9>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-14>) * limitations under the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-15>) */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-16>)import {Content, Part, createUserContent} from '@google/genai';
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-17>)import { stringifyContent, FunctionTool, InMemoryRunner, LlmAgent } from '@google/adk';
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-18>)import {z} from 'zod';
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-19>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-20>)// Define the function to get the stock price
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-21>)async function getStockPrice({ticker}: {ticker: string}): Promise<Record<string, unknown>> {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-22>)  console.log(`Getting stock price for ${ticker}`);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-23>)  // In a real-world scenario, you would fetch the stock price from an API
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-24>)  const price = (Math.random() * 1000).toFixed(2);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-25>)  return {price: `$${price}`};
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-26>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-27>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-28>)async function main() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-29>)  // Define the schema for the tool's parameters using Zod
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-30>)  const getStockPriceSchema = z.object({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-31>)    ticker: z.string().describe('The stock ticker symbol to look up.'),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-32>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-33>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-34>)  // Create a FunctionTool from the function and schema
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-35>)  const stockPriceTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-36>)    name: 'getStockPrice',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-37>)    description: 'Gets the current price of a stock.',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-38>)    parameters: getStockPriceSchema,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-39>)    execute: getStockPrice,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-40>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-41>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-42>)  // Define the agent that will use the tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-43>)  const stockAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-44>)    name: 'stock_agent',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-45>)    model: 'gemini-2.5-flash',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-46>)    instruction: 'You can get the stock price of a company.',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-47>)    tools: [stockPriceTool],
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-48>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-49>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-50>)  // Create a runner for the agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-51>)  const runner = new InMemoryRunner({agent: stockAgent});
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-52>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-53>)  // Create a new session
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-54>)  const session = await runner.sessionService.createSession({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-55>)    appName: runner.appName,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-56>)    userId: 'test-user',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-57>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-58>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-59>)  const userContent: Content = createUserContent('What is the stock price of GOOG?');
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-60>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-61>)  // Run the agent and get the response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-62>)  const response = [];
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-63>)  for await (const event of runner.runAsync({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-64>)    userId: session.userId,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-65>)    sessionId: session.id,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-66>)    newMessage: userContent,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-67>)  })) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-68>)    response.push(event);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-69>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-70>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-71>)  // Print the final response from the agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-72>)  const finalResponse = response[response.length - 1];
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-73>)  if (finalResponse?.content?.parts?.length) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-74>)    console.log(stringifyContent(finalResponse));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-75>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-76>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-77>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-13-78>)main();
    
The return value from this tool will be an object.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-14-1>)For input `GOOG`: {"price": 2800.0, "currency": "USD"}
    
This tool retrieves the mocked value of a stock price.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-1>)import (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-4>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-5>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-6>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-7>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-8>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-9>)    "google.golang.org/genai"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-10>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-11>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-12>)// Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-13>)//
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-14>)// Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-15>)// you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-16>)// You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-17>)//
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-18>)//     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-19>)//
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-20>)// Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-21>)// distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-22>)// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-23>)// See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-24>)// limitations under the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-25>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-26>)package main
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-27>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-28>)import (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-29>)    "context"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-30>)    "fmt"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-31>)    "log"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-32>)    "strings"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-33>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-34>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-35>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-36>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-37>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-38>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-39>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-40>)    "google.golang.org/adk/v2/tool/agenttool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-41>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-42>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-43>)    "google.golang.org/genai"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-44>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-45>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-46>)// mockStockPrices provides a simple in-memory database of stock prices
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-47>)// to simulate a real-world stock data API. This allows the example to
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-48>)// demonstrate tool functionality without making external network calls.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-49>)var mockStockPrices = map[string]float64{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-50>)    "GOOG": 300.6,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-51>)    "AAPL": 123.4,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-52>)    "MSFT": 234.5,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-53>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-54>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-55>)// getStockPriceArgs defines the schema for the arguments passed to the getStockPrice tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-56>)// Using a struct is the recommended approach in the Go ADK as it provides strong
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-57>)// typing and clear validation for the expected inputs.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-58>)type getStockPriceArgs struct {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-59>)    Symbol string `json:"symbol" jsonschema:"The stock ticker symbol, e.g., GOOG"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-60>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-61>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-62>)// getStockPriceResults defines the output schema for the getStockPrice tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-63>)type getStockPriceResults struct {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-64>)    Symbol string  `json:"symbol"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-65>)    Price  float64 `json:"price,omitempty"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-66>)    Error  string  `json:"error,omitempty"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-67>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-68>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-69>)// getStockPrice is a tool that retrieves the stock price for a given ticker symbol
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-70>)// from the mockStockPrices map. It demonstrates how a function can be used as a
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-71>)// tool by an agent. If the symbol is found, it returns a struct containing the
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-72>)// symbol and its price. Otherwise, it returns a struct with an error message.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-73>)func getStockPrice(ctx agent.Context, input getStockPriceArgs) (getStockPriceResults, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-74>)    symbolUpper := strings.ToUpper(input.Symbol)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-75>)    if price, ok := mockStockPrices[symbolUpper]; ok {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-76>)        fmt.Printf("Tool: Found price for %s: %f\n", input.Symbol, price)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-77>)        return getStockPriceResults{Symbol: input.Symbol, Price: price}, nil
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-78>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-79>)    return getStockPriceResults{}, fmt.Errorf("no data found for symbol")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-80>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-81>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-82>)// createStockAgent initializes and configures an LlmAgent.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-83>)// This agent is equipped with the getStockPrice tool and is instructed
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-84>)// on how to respond to user queries about stock prices. It uses the
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-85>)// Gemini model to understand user intent and decide when to use its tools.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-86>)func createStockAgent(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-87>)    stockPriceTool, err := functiontool.New(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-88>)        functiontool.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-89>)            Name:        "get_stock_price",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-90>)            Description: "Retrieves the current stock price for a given symbol.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-91>)        },
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-92>)        getStockPrice)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-93>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-94>)        return nil, err
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-95>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-96>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-97>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-98>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-99>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-100>)        log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-101>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-102>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-103>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-104>)        Name:        "stock_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-105>)        Model:       model,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-106>)        Instruction: "You are an agent who retrieves stock prices. If a ticker symbol is provided, fetch the current price. If only a company name is given, first perform a Google search to find the correct ticker symbol before retrieving the stock price. If the provided ticker symbol is invalid or data cannot be retrieved, inform the user that the stock price could not be found.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-107>)        Description: "This agent specializes in retrieving real-time stock prices. Given a stock ticker symbol (e.g., AAPL, GOOG, MSFT) or the stock name, use the tools and reliable data sources to provide the most up-to-date price.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-108>)        Tools: []tool.Tool{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-109>)            stockPriceTool,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-110>)        },
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-111>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-112>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-113>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-114>)// userID and appName are constants used to identify the user and application
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-115>)// throughout the session. These values are important for logging, tracking,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-116>)// and managing state across different agent interactions.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-117>)const (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-118>)    userID  = "example_user_id"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-119>)    appName = "example_app"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-120>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-121>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-122>)// callAgent orchestrates the execution of the agent for a given prompt.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-123>)// It sets up the necessary services, creates a session, and uses a runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-124>)// to manage the agent's lifecycle. It streams the agent's responses and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-125>)// prints them to the console, handling any potential errors during the run.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-126>)func callAgent(ctx context.Context, a agent.Agent, prompt string) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-127>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-128>)    // Create a new session for the agent interactions.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-129>)    session, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-130>)        AppName: appName,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-131>)        UserID:  userID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-132>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-133>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-134>)        log.Fatalf("Failed to create the session service: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-135>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-136>)    config := runner.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-137>)        AppName:        appName,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-138>)        Agent:          a,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-139>)        SessionService: sessionService,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-140>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-141>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-142>)    // Create the runner to manage the agent execution.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-143>)    r, err := runner.New(config)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-144>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-145>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-146>)        log.Fatalf("Failed to create the runner: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-147>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-148>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-149>)    sessionID := session.Session.ID()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-150>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-151>)    userMsg := &genai.Content{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-152>)        Parts: []*genai.Part{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-153>)            genai.NewPartFromText(prompt),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-154>)        },
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-155>)        Role: string(genai.RoleUser),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-156>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-157>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-158>)    for event, err := range r.Run(ctx, userID, sessionID, userMsg, agent.RunConfig{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-159>)        StreamingMode: agent.StreamingModeNone,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-160>)    }) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-161>)        if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-162>)            fmt.Printf("\nAGENT_ERROR: %v\n", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-163>)        } else {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-164>)            for _, p := range event.Content.Parts {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-165>)                fmt.Print(p.Text)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-166>)            }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-167>)        }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-168>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-169>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-170>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-171>)// RunAgentSimulation serves as the entry point for this example.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-172>)// It creates the stock agent and then simulates a series of user interactions
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-173>)// by sending different prompts to the agent. This function showcases how the
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-174>)// agent responds to various queries, including both successful and unsuccessful
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-175>)// attempts to retrieve stock prices.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-176>)func RunAgentSimulation() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-177>)    // Create the stock agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-178>)    agent, err := createStockAgent(context.Background())
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-179>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-180>)        panic(err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-181>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-182>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-183>)    fmt.Println("Agent created:", agent.Name())
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-184>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-185>)    prompts := []string{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-186>)        "stock price of GOOG",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-187>)        "What's the price of MSFT?",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-188>)        "Can you find the stock price for an unknown company XYZ?",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-189>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-190>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-191>)    // Simulate running the agent with different prompts
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-192>)    for _, prompt := range prompts {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-193>)        fmt.Printf("\nPrompt: %s\nResponse: ", prompt)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-194>)        callAgent(context.Background(), agent, prompt)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-195>)        fmt.Println("\n---")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-196>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-197>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-198>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-199>)// createSummarizerAgent creates an agent whose sole purpose is to summarize text.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-200>)func createSummarizerAgent(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-201>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-202>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-203>)        return nil, err
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-204>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-205>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-206>)        Name:        "SummarizerAgent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-207>)        Model:       model,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-208>)        Instruction: "You are an expert at summarizing text. Take the user's input and provide a concise summary.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-209>)        Description: "An agent that summarizes text.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-210>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-211>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-212>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-213>)// createMainAgent creates the primary agent that will use the summarizer agent as a tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-214>)func createMainAgent(ctx context.Context, tools ...tool.Tool) (agent.Agent, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-215>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-216>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-217>)        return nil, err
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-218>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-219>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-220>)        Name:  "MainAgent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-221>)        Model: model,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-222>)        Instruction: "You are a helpful assistant. If you are asked to summarize a long text, use the 'summarize' tool. " +
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-223>)            "After getting the summary, present it to the user by saying 'Here is a summary of the text:'.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-224>)        Description: "The main agent that can delegate tasks.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-225>)        Tools:       tools,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-226>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-227>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-228>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-229>)func RunAgentAsToolSimulation() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-230>)    ctx := context.Background()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-231>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-232>)    // 1. Create the Tool Agent (Summarizer)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-233>)    summarizerAgent, err := createSummarizerAgent(ctx)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-234>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-235>)        log.Fatalf("Failed to create summarizer agent: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-236>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-237>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-238>)    // 2. Wrap the Tool Agent in an AgentTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-239>)    summarizeTool := agenttool.New(summarizerAgent, &agenttool.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-240>)        SkipSummarization: true,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-241>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-242>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-243>)    // 3. Create the Main Agent and provide it with the AgentTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-244>)    mainAgent, err := createMainAgent(ctx, summarizeTool)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-245>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-246>)        log.Fatalf("Failed to create main agent: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-247>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-248>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-249>)    // 4. Run the main agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-250>)    prompt := `
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-251>)        Please summarize this text for me:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-252>)        Quantum computing represents a fundamentally different approach to computation,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-253>)        leveraging the bizarre principles of quantum mechanics to process information. Unlike classical computers
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-254>)        that rely on bits representing either 0 or 1, quantum computers use qubits which can exist in a state of superposition - effectively
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-255>)        being 0, 1, or a combination of both simultaneously. Furthermore, qubits can become entangled,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-256>)        meaning their fates are intertwined regardless of distance, allowing for complex correlations. This parallelism and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-257>)        interconnectedness grant quantum computers the potential to solve specific types of incredibly complex problems - such
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-258>)        as drug discovery, materials science, complex system optimization, and breaking certain types of cryptography - far
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-259>)        faster than even the most powerful classical supercomputers could ever achieve, although the technology is still largely in its developmental stages.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-260>)    `
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-261>)    fmt.Printf("\nPrompt: %s\nResponse: ", prompt)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-262>)    callAgent(context.Background(), mainAgent, prompt)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-263>)    fmt.Println("\n---")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-264>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-265>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-266>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-267>)func main() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-268>)    fmt.Println("Attempting to run the agent simulation...")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-269>)    RunAgentSimulation()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-270>)    fmt.Println("\nAttempting to run the agent-as-a-tool simulation...")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-271>)    RunAgentAsToolSimulation()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-15-272>)}
    
The return value from this tool will be a `getStockPriceResults` instance.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-16-1>)For input `{"symbol": "GOOG"}`: {"price":300.6,"symbol":"GOOG"}
    
This tool retrieves the mocked value of a stock price.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-2>)import com.google.adk.events.Event;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-3>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-4>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-5>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-6>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-7>)import com.google.genai.types.Content;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-8>)import com.google.genai.types.Part;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-9>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-10>)import java.util.Map;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-11>)import yahoofinance.Stock;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-12>)import yahoofinance.YahooFinance;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-13>)import java.math.BigDecimal;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-15>)public class StockPriceAgent {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-16>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-17>)  private static final String APP_NAME = "stock_agent";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-18>)  private static final String USER_ID = "user1234";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-19>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-20>)  // No longer using mock stock data - we fetch it live!
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-21>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-22>)  @Schema(description = "Retrieves the current stock price for a given symbol.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-23>)  public static Map<String, Object> getStockPrice(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-24>)      @Schema(description = "The stock symbol (e.g., \"AAPL\", \"GOOG\")",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-25>)        name = "symbol")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-26>)      String symbol) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-27>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-28>)    try {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-29>)      Stock stock = YahooFinance.get(symbol.toUpperCase());
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-30>)      if (stock != null && stock.getQuote().getPrice() != null) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-31>)        BigDecimal currentPrice = stock.getQuote().getPrice();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-32>)        System.out.println("Tool: Found live price for " + symbol + ": " + currentPrice);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-33>)        return Map.of("symbol", symbol, "price", currentPrice.doubleValue());
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-34>)      } else {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-35>)        return Map.of("symbol", symbol, "error", "No data found for symbol");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-36>)      }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-37>)    } catch (Exception e) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-38>)      return Map.of("symbol", symbol, "error", e.getMessage());
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-39>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-40>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-41>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-42>)  public static void callAgent(String prompt) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-43>)    // Create the FunctionTool from the Java method
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-44>)    FunctionTool getStockPriceTool = FunctionTool.create(StockPriceAgent.class, "getStockPrice");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-45>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-46>)    LlmAgent stockPriceAgent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-47>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-48>)            .model("gemini-2.0-flash")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-49>)            .name("stock_agent")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-50>)            .instruction(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-51>)                "You are an agent who retrieves stock prices. If a ticker symbol is provided, fetch the current price. If only a company name is given, first perform a Google search to find the correct ticker symbol before retrieving the stock price. If the provided ticker symbol is invalid or data cannot be retrieved, inform the user that the stock price could not be found.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-52>)            .description(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-53>)                "This agent specializes in retrieving real-time stock prices. Given a stock ticker symbol (e.g., AAPL, GOOG, MSFT) or the stock name, use the tools and reliable data sources to provide the most up-to-date price.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-54>)            .tools(getStockPriceTool) // Add the Java FunctionTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-55>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-56>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-57>)    // Create an InMemoryRunner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-58>)    InMemoryRunner runner = new InMemoryRunner(stockPriceAgent, APP_NAME);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-59>)    // InMemoryRunner automatically creates a session service. Create a session using the service
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-60>)    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-61>)    Content userMessage = Content.fromParts(Part.fromText(prompt));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-62>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-63>)    // Run the agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-64>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-65>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-66>)    // Stream event response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-67>)    eventStream.blockingForEach(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-68>)        event -> {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-69>)          if (event.finalResponse()) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-70>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-71>)          }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-72>)        });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-73>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-74>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-75>)  public static void main(String[] args) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-76>)    callAgent("stock price of GOOG");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-77>)    callAgent("What's the price of MSFT?");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-78>)    callAgent("Can you find the stock price for an unknown company XYZ?");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-79>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-17-80>)}
    
The return value from this tool will be wrapped into a Map.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-18-1>)For input `GOOG`: {"symbol": "GOOG", "price": "1.0"}
    
This tool retrieves the mocked value of a stock price.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-1>)data class StockPrice(val symbol: String, val price: Double)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-2>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-3>)class StockService {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-4>)    /**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-5>)     * Retrieves the stock price for a given symbol.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-6>)     */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-7>)    @Tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-8>)    fun getStockPrice(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-9>)        @Param("The stock symbol, e.g. GOOG") symbol: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-10>)    ): StockPrice {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-11>)        // In a real app, you would call a stock price API here.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-12>)        return StockPrice(symbol = symbol, price = 123.45)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-13>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-14>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-15>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-16>)fun main() =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-17>)    runBlocking {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-18>)        val stockService = StockService()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-19>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-20>)        val agent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-21>)            LlmAgent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-22>)                name = "stock_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-23>)                model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-24>)                instruction = Instruction("You are a helpful stock assistant."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-25>)                // .generatedTools() is used to get the tools from the annotated class.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-26>)                tools = stockService.generatedTools(),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-27>)            )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-28>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-29>)        // ... use the agent ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-19-30>)    }
    
The return value from this tool will be a Map.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-20-1>)For input `GOOG`: {"symbol": "GOOG", "price": 123.45}
    
### Best practices[¶](<https://adk.dev/tools-custom/function-tools/#best-practices> "Permanent link")

While you have considerable flexibility in defining your function, remember that simplicity enhances usability for the LLM. Consider these guidelines:

  * **Fewer Parameters are Better:** Minimize the number of parameters to reduce complexity.
  * **Simple Data Types:** Favor primitive data types like `str` and `int` over custom classes whenever possible.
  * **Meaningful Names:** The function's name and parameter names significantly influence how the LLM interprets and utilizes the tool. Choose names that clearly reflect the function's purpose and the meaning of its inputs. Avoid generic names like `do_stuff()` or `beAgent()`.
  * **Build for Parallel Execution:** Improve function calling performance when multiple tools are run by building for asynchronous operation. For information on enabling parallel execution for tools, see [Increase tool performance with parallel execution](<https://adk.dev/tools-custom/performance/>).

## Long running function tools[¶](<https://adk.dev/tools-custom/function-tools/#long-run-tool> "Permanent link")

This tool is designed to help you start and manage tasks that are handled outside the operation of your agent workflow, and require a significant amount of processing time, without blocking the agent's execution. This tool is a subclass of `FunctionTool`.

When using a `LongRunningFunctionTool`, your function can initiate the long-running operation and optionally return an **initial result** , such as a long-running operation id. Once a long running function tool is invoked the agent runner pauses the agent run and lets the agent client to decide whether to continue or wait until the long-running operation finishes. The agent client can query the progress of the long-running operation and send back an intermediate or final response. The agent can then continue with other tasks. An example is the human-in-the-loop scenario where the agent needs human approval before proceeding with a task.

Warning: Execution handling

Long Running Function Tools are designed to help you start and _manage_ long running tasks as part of your agent workflow, but **_not perform_** the actual, long task. For tasks that require significant time to complete, you should implement a separate server to do the task.

Tip: Parallel execution

Depending on the type of tool you are building, designing for asynchronous operation may be a better solution than creating a long running tool. For more information, see [Increase tool performance with parallel execution](<https://adk.dev/tools-custom/performance/>).

### How it works[¶](<https://adk.dev/tools-custom/function-tools/#how-it-works_1> "Permanent link")

In Python, you wrap a function with `LongRunningFunctionTool`. In Java, you pass a Method name to `LongRunningFunctionTool.create()`. In TypeScript, you instantiate the `LongRunningFunctionTool` class.

  1. **Initiation:** When the LLM calls the tool, your function starts the long-running operation.
  2. **Initial Updates:** Your function should optionally return an initial result (e.g. the long-running operation id). The ADK framework takes the result and sends it back to the LLM packaged within a `FunctionResponse`. This allows the LLM to inform the user (e.g., status, percentage complete, messages). And then the agent run is ended / paused.
  3. **Continue or Wait:** After each agent run is completed. Agent client can query the progress of the long-running operation and decide whether to continue the agent run with an intermediate response (to update the progress) or wait until a final response is retrieved. Agent client should send the intermediate or final response back to the agent for the next run.
  4. **Framework Handling:** The ADK framework manages the execution. It sends the intermediate or final `FunctionResponse` sent by agent client to the LLM to generate a user friendly message.

### Create the tool[¶](<https://adk.dev/tools-custom/function-tools/#create-the-tool> "Permanent link")

Define your tool function and wrap it using the `LongRunningFunctionTool` class:

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-1>)from typing import Any
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-2>)from google.adk.tools import LongRunningFunctionTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-3>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-4>)# 1. Define the long running function
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-5>)def ask_for_approval(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-6>)    purpose: str, amount: float
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-7>)) -> dict[str, Any]:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-8>)    """Ask for approval for the reimbursement."""
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-9>)    # create a ticket for the approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-10>)    # Send a notification to the approver with the link of the ticket
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-11>)    return {'status': 'pending', 'approver': 'Sean Zhou', 'purpose' : purpose, 'amount': amount, 'ticket-id': 'approval-ticket-1'}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-12>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-13>)def reimburse(purpose: str, amount: float) -> dict[str, Any]:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-14>)    """Reimburse the amount of money to the employee."""
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-15>)    # send the reimbrusement request to payment vendor
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-16>)    return {'status': 'ok'}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-17>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-18>)# 2. Wrap the function with LongRunningFunctionTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-21-19>)long_running_tool = LongRunningFunctionTool(func=ask_for_approval)
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-1>)// 1. Define the long-running function
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-2>)function askForApproval(args: {purpose: string; amount: number}) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-3>)  /**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-4>)   * Ask for approval for the reimbursement.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-5>)   */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-6>)  // create a ticket for the approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-7>)  // Send a notification to the approver with the link of the ticket
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-8>)  return {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-9>)    "status": "pending",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-10>)    "approver": "Sean Zhou",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-11>)    "purpose": args.purpose,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-12>)    "amount": args.amount,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-13>)    "ticket-id": "approval-ticket-1",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-14>)  };
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-15>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-16>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-17>)// 2. Instantiate the LongRunningFunctionTool class with the long-running function
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-18>)const longRunningTool = new LongRunningFunctionTool({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-19>)  name: "ask_for_approval",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-20>)  description: "Ask for approval for the reimbursement.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-21>)  parameters: z.object({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-22>)    purpose: z.string().describe("The purpose of the reimbursement."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-23>)    amount: z.number().describe("The amount to reimburse."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-24>)  }),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-25>)  execute: askForApproval,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-22-26>)});
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-1>)import (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-4>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-5>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-6>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-7>)    "google.golang.org/genai"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-8>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-9>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-10>)// CreateTicketArgs defines the arguments for our long-running tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-11>)type CreateTicketArgs struct {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-12>)    Urgency string `json:"urgency" jsonschema:"The urgency level of the ticket."`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-13>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-15>)// CreateTicketResults defines the *initial* output of our long-running tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-16>)type CreateTicketResults struct {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-17>)    Status   string `json:"status"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-18>)    TicketId string `json:"ticket_id"`
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-19>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-20>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-21>)// createTicketAsync simulates the *initiation* of a long-running ticket creation task.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-22>)func createTicketAsync(ctx agent.Context, args CreateTicketArgs) (CreateTicketResults, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-23>)    log.Printf("TOOL_EXEC: 'create_ticket_long_running' called with urgency: %s (Call ID: %s)\n", args.Urgency, ctx.FunctionCallID())
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-24>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-25>)    // "Generate" a ticket ID and return it in the initial response.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-26>)    ticketID := "TICKET-ABC-123"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-27>)    log.Printf("ACTION: Generated Ticket ID: %s for Call ID: %s\n", ticketID, ctx.FunctionCallID())
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-28>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-29>)    // In a real application, you would save the association between the
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-30>)    // FunctionCallID and the ticketID to handle the async response later.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-31>)    return CreateTicketResults{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-32>)        Status:   "started",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-33>)        TicketId: ticketID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-34>)    }, nil
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-35>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-36>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-37>)func createTicketAgent(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-38>)    ticketTool, err := functiontool.New(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-39>)        functiontool.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-40>)            Name:        "create_ticket_long_running",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-41>)            Description: "Creates a new support ticket with a specified urgency level.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-42>)        },
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-43>)        createTicketAsync,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-44>)    )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-45>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-46>)        return nil, fmt.Errorf("failed to create long running tool: %w", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-47>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-48>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-49>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-50>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-51>)        return nil, fmt.Errorf("failed to create model: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-52>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-53>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-54>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-55>)        Name:        "ticket_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-56>)        Model:       model,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-57>)        Instruction: "You are a helpful assistant for creating support tickets. Provide the status of the ticket at each interaction.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-58>)        Tools:       []tool.Tool{ticketTool},
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-59>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-23-60>)}
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-2>)import com.google.adk.tools.LongRunningFunctionTool;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-3>)import java.util.HashMap;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-4>)import java.util.Map;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-5>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-6>)public class ExampleLongRunningFunction {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-7>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-8>)  // Define your Long Running function.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-9>)  // Ask for approval for the reimbursement.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-10>)  public static Map<String, Object> askForApproval(String purpose, double amount) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-11>)    // Simulate creating a ticket and sending a notification
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-12>)    System.out.println(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-13>)        "Simulating ticket creation for purpose: " + purpose + ", amount: " + amount);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-15>)    // Send a notification to the approver with the link of the ticket
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-16>)    Map<String, Object> result = new HashMap<>();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-17>)    result.put("status", "pending");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-18>)    result.put("approver", "Sean Zhou");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-19>)    result.put("purpose", purpose);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-20>)    result.put("amount", amount);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-21>)    result.put("ticket-id", "approval-ticket-1");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-22>)    return result;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-23>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-24>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-25>)  public static void main(String[] args) throws NoSuchMethodException {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-26>)    // Pass the method to LongRunningFunctionTool.create
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-27>)    LongRunningFunctionTool approveTool =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-28>)        LongRunningFunctionTool.create(ExampleLongRunningFunction.class, "askForApproval");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-29>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-30>)    // Include the tool in the agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-31>)    LlmAgent approverAgent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-32>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-33>)            // ...
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-34>)            .tools(approveTool)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-35>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-36>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-24-37>)}
    
In Kotlin, you can create a long-running function tool by setting the `isLongRunning` property to `true` in the `@Tool` annotation.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-1>)data class ReimbursementApproval(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-2>)    val status: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-3>)    val approver: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-4>)    val purpose: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-5>)    val amount: Double,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-6>)    val ticketId: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-7>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-8>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-9>)class ReimbursementService {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-10>)    /**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-11>)     * Asks for approval for the reimbursement.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-12>)     */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-13>)    @Tool(isLongRunning = true)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-14>)    fun askForApproval(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-15>)        @Param("The purpose of the reimbursement.") purpose: String,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-16>)        @Param("The amount to be reimbursed.") amount: Double,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-17>)    ): ReimbursementApproval {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-18>)        // Simulate creating a ticket and sending a notification.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-19>)        // This tool returns the initial result and then the agent pauses.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-20>)        return ReimbursementApproval(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-21>)            status = "pending",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-22>)            approver = "Sean Zhou",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-23>)            purpose = purpose,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-24>)            amount = amount,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-25>)            ticketId = "approval-ticket-1",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-26>)        )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-27>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-28>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-29>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-30>)fun main() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-31>)    val service = ReimbursementService()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-32>)    val agent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-33>)        LlmAgent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-34>)            name = "approver_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-35>)            model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-36>)            instruction = Instruction("You are a helpful reimbursement assistant."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-37>)            tools = service.generatedTools(),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-38>)        )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-25-39>)}
    
### Intermediate / final result updates[¶](<https://adk.dev/tools-custom/function-tools/#intermediate-final-result-updates> "Permanent link")

Agent client received an event with long running function calls and check the status of the ticket. Then Agent client can send the intermediate or final response back to update the progress. The framework packages this value (even if it's None) into the content of the `FunctionResponse` sent back to the LLM.

Note: Long running function response with Resume feature

If your ADK agent workflow is configured with the [Resume](<https://adk.dev/runtime/resume/>) feature, you also must include the Invocation ID (`invocation_id`) parameter with the long running function response. The Invocation ID you provide must be the same invocation that generated the long running function request, otherwise the system starts a new invocation with the response. If your agent uses the Resume feature, consider including the Invocation ID as a parameter with your long running function request, so it can be included with the response. For more details on using the Resume feature, see [Resume stopped agents](<https://adk.dev/runtime/resume/>).

Applies to only Java ADK

When passing `ToolContext` with Function Tools, ensure that one of the following is true:

  * The Schema is passed with the ToolContext parameter in the function signature, like:

    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-26-1>)@com.google.adk.tools.Annotations.Schema(name = "toolContext") ToolContext toolContext
    
OR

  * The following `-parameters` flag is set to the mvn compiler plugin

    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-1>)<build>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-2>)    <plugins>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-3>)        <plugin>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-4>)            <groupId>org.apache.maven.plugins</groupId>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-5>)            <artifactId>maven-compiler-plugin</artifactId>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-6>)            <version>3.14.0</version> <!-- or newer -->
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-7>)            <configuration>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-8>)                <compilerArgs>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-9>)                    <arg>-parameters</arg>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-10>)                </compilerArgs>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-11>)            </configuration>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-12>)        </plugin>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-13>)    </plugins>
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-27-14>)</build>
    
PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-1>)# Agent Interaction
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-2>)async def call_agent_async(query):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-3>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-4>)    def get_long_running_function_call(event: Event) -> types.FunctionCall:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-5>)        # Get the long running function call from the event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-6>)        if not event.long_running_tool_ids or not event.content or not event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-7>)            return
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-8>)        for part in event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-9>)            if (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-10>)                part
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-11>)                and part.function_call
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-12>)                and event.long_running_tool_ids
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-13>)                and part.function_call.id in event.long_running_tool_ids
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-14>)            ):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-15>)                return part.function_call
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-16>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-17>)    def get_function_response(event: Event, function_call_id: str) -> types.FunctionResponse:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-18>)        # Get the function response for the fuction call with specified id.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-19>)        if not event.content or not event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-20>)            return
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-21>)        for part in event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-22>)            if (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-23>)                part
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-24>)                and part.function_response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-25>)                and part.function_response.id == function_call_id
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-26>)            ):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-27>)                return part.function_response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-28>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-29>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-30>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-31>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-32>)    print("\nRunning agent...")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-33>)    events_async = runner.run_async(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-34>)        session_id=session.id, user_id=USER_ID, new_message=content
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-35>)    )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-36>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-37>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-38>)    long_running_function_call, long_running_function_response, ticket_id = None, None, None
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-39>)    async for event in events_async:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-40>)        # Use helper to check for the specific auth request event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-41>)        if not long_running_function_call:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-42>)            long_running_function_call = get_long_running_function_call(event)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-43>)        else:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-44>)            _potential_response = get_function_response(event, long_running_function_call.id)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-45>)            if _potential_response: # Only update if we get a non-None response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-46>)                long_running_function_response = _potential_response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-47>)                ticket_id = long_running_function_response.response['ticket-id']
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-48>)        if event.content and event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-49>)            if text := ''.join(part.text or '' for part in event.content.parts):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-50>)                print(f'[{event.author}]: {text}')
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-51>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-52>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-53>)    if long_running_function_response:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-54>)        # query the status of the correpsonding ticket via tciket_id
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-55>)        # send back an intermediate / final response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-56>)        updated_response = long_running_function_response.model_copy(deep=True)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-57>)        updated_response.response = {'status': 'approved'}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-58>)        async for event in runner.run_async(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-59>)          session_id=session.id, user_id=USER_ID, new_message=types.Content(parts=[types.Part(function_response = updated_response)], role='user')
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-60>)        ):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-61>)            if event.content and event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-62>)                if text := ''.join(part.text or '' for part in event.content.parts):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-28-63>)                    print(f'[{event.author}]: {text}')
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-1>)/**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-3>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-7>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-9>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-14>) * limitations under the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-15>) */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-16>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-17>)import { LlmAgent, Runner, FunctionTool, LongRunningFunctionTool, InMemorySessionService, Event, stringifyContent } from '@google/adk';
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-18>)import {z} from "zod";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-19>)import {Content, FunctionCall, FunctionResponse, createUserContent} from "@google/genai";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-20>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-21>)// 1. Define the long-running function
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-22>)function askForApproval(args: {purpose: string; amount: number}) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-23>)  /**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-24>)   * Ask for approval for the reimbursement.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-25>)   */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-26>)  // create a ticket for the approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-27>)  // Send a notification to the approver with the link of the ticket
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-28>)  return {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-29>)    "status": "pending",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-30>)    "approver": "Sean Zhou",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-31>)    "purpose": args.purpose,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-32>)    "amount": args.amount,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-33>)    "ticket-id": "approval-ticket-1",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-34>)  };
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-35>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-36>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-37>)// 2. Instantiate the LongRunningFunctionTool class with the long-running function
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-38>)const longRunningTool = new LongRunningFunctionTool({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-39>)  name: "ask_for_approval",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-40>)  description: "Ask for approval for the reimbursement.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-41>)  parameters: z.object({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-42>)    purpose: z.string().describe("The purpose of the reimbursement."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-43>)    amount: z.number().describe("The amount to reimburse."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-44>)  }),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-45>)  execute: askForApproval,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-46>)});
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-47>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-48>)function reimburse(args: {purpose: string; amount: number}) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-49>)  /**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-50>)   * Reimburse the amount of money to the employee.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-51>)   */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-52>)  // send the reimbursement request to payment vendor
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-53>)  return {status: "ok"};
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-54>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-55>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-56>)const reimburseTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-57>)  name: "reimburse",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-58>)  description: "Reimburse the amount of money to the employee.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-59>)  parameters: z.object({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-60>)    purpose: z.string().describe("The purpose of the reimbursement."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-61>)    amount: z.number().describe("The amount to reimburse."),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-62>)  }),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-63>)  execute: reimburse,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-64>)});
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-65>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-66>)// 3. Use the tool in an Agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-67>)const reimbursementAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-68>)  model: "gemini-2.5-flash",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-69>)  name: "reimbursement_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-70>)  instruction: `
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-71>)      You are an agent whose job is to handle the reimbursement process for
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-72>)      the employees. If the amount is less than $100, you will automatically
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-73>)      approve the reimbursement.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-74>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-75>)      If the amount is greater than $100, you will
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-76>)      ask for approval from the manager. If the manager approves, you will
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-77>)      call reimburse() to reimburse the amount to the employee. If the manager
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-78>)      rejects, you will inform the employee of the rejection.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-79>)    `,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-80>)  tools: [reimburseTool, longRunningTool],
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-81>)});
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-82>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-83>)const APP_NAME = "human_in_the_loop";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-84>)const USER_ID = "1234";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-85>)const SESSION_ID = "session1234";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-86>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-87>)// Session and Runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-88>)async function setupSessionAndRunner() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-89>)  const sessionService = new InMemorySessionService();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-90>)  const session = await sessionService.createSession({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-91>)    appName: APP_NAME,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-92>)    userId: USER_ID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-93>)    sessionId: SESSION_ID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-94>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-95>)  const runner = new Runner({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-96>)    agent: reimbursementAgent,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-97>)    appName: APP_NAME,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-98>)    sessionService: sessionService,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-99>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-100>)  return {session, runner};
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-101>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-102>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-103>)function getLongRunningFunctionCall(event: Event): FunctionCall | undefined {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-104>)  // Get the long-running function call from the event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-105>)  if (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-106>)    !event.longRunningToolIds ||
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-107>)    !event.content ||
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-108>)    !event.content.parts?.length
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-109>)  ) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-110>)    return;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-111>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-112>)  for (const part of event.content.parts) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-113>)    if (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-114>)      part &&
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-115>)      part.functionCall &&
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-116>)      event.longRunningToolIds &&
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-117>)      part.functionCall.id &&
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-118>)      event.longRunningToolIds.includes(part.functionCall.id)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-119>)    ) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-120>)      return part.functionCall;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-121>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-122>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-123>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-124>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-125>)function getFunctionResponse(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-126>)  event: Event,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-127>)  functionCallId: string
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-128>)): FunctionResponse | undefined {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-129>)  // Get the function response for the function call with specified id.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-130>)  if (!event.content || !event.content.parts?.length) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-131>)    return;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-132>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-133>)  for (const part of event.content.parts) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-134>)    if (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-135>)      part &&
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-136>)      part.functionResponse &&
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-137>)      part.functionResponse.id === functionCallId
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-138>)    ) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-139>)      return part.functionResponse;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-140>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-141>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-142>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-143>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-144>)// Agent Interaction
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-145>)async function callAgentAsync(query: string) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-146>)  let longRunningFunctionCall: FunctionCall | undefined;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-147>)  let longRunningFunctionResponse: FunctionResponse | undefined;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-148>)  let ticketId: string | undefined;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-149>)  const content: Content = createUserContent(query);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-150>)  const {session, runner} = await setupSessionAndRunner();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-151>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-152>)  console.log("\nRunning agent...");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-153>)  const events = runner.runAsync({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-154>)    sessionId: session.id,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-155>)    userId: USER_ID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-156>)    newMessage: content,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-157>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-158>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-159>)  for await (const event of events) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-160>)    // Use helper to check for the specific auth request event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-161>)    if (!longRunningFunctionCall) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-162>)      longRunningFunctionCall = getLongRunningFunctionCall(event);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-163>)    } else {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-164>)      const _potentialResponse = getFunctionResponse(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-165>)        event,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-166>)        longRunningFunctionCall.id!
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-167>)      );
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-168>)      if (_potentialResponse) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-169>)        // Only update if we get a non-None response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-170>)        longRunningFunctionResponse = _potentialResponse;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-171>)        ticketId = (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-172>)          longRunningFunctionResponse.response as {[key: string]: any}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-173>)        )[`ticket-id`];
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-174>)      }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-175>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-176>)    const text = stringifyContent(event);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-177>)    if (text) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-178>)      console.log(`[${event.author}]: ${text}`);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-179>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-180>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-181>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-182>)  if (longRunningFunctionResponse) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-183>)    // query the status of the corresponding ticket via ticket_id
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-184>)    // send back an intermediate / final response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-185>)    const updatedResponse = JSON.parse(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-186>)      JSON.stringify(longRunningFunctionResponse)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-187>)    );
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-188>)    updatedResponse.response = {status: "approved"};
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-189>)    for await (const event of runner.runAsync({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-190>)      sessionId: session.id,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-191>)      userId: USER_ID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-192>)      newMessage: createUserContent(JSON.stringify({functionResponse: updatedResponse})),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-193>)    })) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-194>)      const text = stringifyContent(event);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-195>)      if (text) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-196>)        console.log(`[${event.author}]: ${text}`);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-197>)      }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-198>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-199>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-200>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-201>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-202>)async function main() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-203>)  // reimbursement that doesn't require approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-204>)  await callAgentAsync("Please reimburse 50$ for meals");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-205>)  // reimbursement that requires approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-206>)  await callAgentAsync("Please reimburse 200$ for meals");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-207>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-208>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-29-209>)main();
    
The following example demonstrates a multi-turn workflow. First, the user asks the agent to create a ticket. The agent calls the long-running tool and the client captures the `FunctionCall` ID. The client then simulates the asynchronous work completing by sending subsequent `FunctionResponse` messages back to the agent to provide the ticket ID and final status.
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-1>)// runTurn executes a single turn with the agent and returns the captured function call ID.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-2>)func runTurn(ctx context.Context, r *runner.Runner, sessionID, turnLabel string, content *genai.Content) string {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-3>)    var funcCallID atomic.Value // Safely store the found ID.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-4>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-5>)    fmt.Printf("\n--- %s ---\n", turnLabel)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-6>)    for event, err := range r.Run(ctx, userID, sessionID, content, agent.RunConfig{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-7>)        StreamingMode: agent.StreamingModeNone,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-8>)    }) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-9>)        if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-10>)            fmt.Printf("\nAGENT_ERROR: %v\n", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-11>)            continue
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-12>)        }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-13>)        // Print a summary of the event for clarity.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-14>)        printEventSummary(event, turnLabel)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-15>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-16>)        // Capture the function call ID from the event.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-17>)        for _, part := range event.Content.Parts {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-18>)            if fc := part.FunctionCall; fc != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-19>)                if fc.Name == "create_ticket_long_running" {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-20>)                    funcCallID.Store(fc.ID)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-21>)                }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-22>)            }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-23>)        }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-24>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-25>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-26>)    if id, ok := funcCallID.Load().(string); ok {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-27>)        return id
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-28>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-29>)    return ""
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-30>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-31>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-32>)func main() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-33>)    ctx := context.Background()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-34>)    ticketAgent, err := createTicketAgent(ctx)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-35>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-36>)        log.Fatalf("Failed to create agent: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-37>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-38>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-39>)    // Setup the runner and session.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-40>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-41>)    session, err := sessionService.Create(ctx, &session.CreateRequest{AppName: appName, UserID: userID})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-42>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-43>)        log.Fatalf("Failed to create session: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-44>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-45>)    r, err := runner.New(runner.Config{AppName: appName, Agent: ticketAgent, SessionService: sessionService})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-46>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-47>)        log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-48>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-49>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-50>)    // --- Turn 1: User requests to create a ticket. ---
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-51>)    initialUserMessage := genai.NewContentFromText("Create a high urgency ticket for me.", genai.RoleUser)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-52>)    funcCallID := runTurn(ctx, r, session.Session.ID(), "Turn 1: User Request", initialUserMessage)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-53>)    if funcCallID == "" {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-54>)        log.Fatal("ERROR: Tool 'create_ticket_long_running' not called in Turn 1.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-55>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-56>)    fmt.Printf("ACTION: Captured FunctionCall ID: %s\n", funcCallID)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-57>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-58>)    // --- Turn 2: App provides the final status of the ticket. ---
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-59>)    // In a real application, the ticketID would be retrieved from a database
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-60>)    // using the funcCallID. For this example, we'll use the same ID.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-61>)    ticketID := "TICKET-ABC-123"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-62>)    willContinue := false // Signal that this is the final response.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-63>)    ticketStatusResponse := &genai.FunctionResponse{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-64>)        Name: "create_ticket_long_running",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-65>)        ID:   funcCallID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-66>)        Response: map[string]any{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-67>)            "status":    "approved",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-68>)            "ticket_id": ticketID,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-69>)        },
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-70>)        WillContinue: &willContinue,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-71>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-72>)    appResponseWithStatus := &genai.Content{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-73>)        Role:  string(genai.RoleUser),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-74>)        Parts: []*genai.Part{{FunctionResponse: ticketStatusResponse}},
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-75>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-76>)    runTurn(ctx, r, session.Session.ID(), "Turn 2: App provides ticket status", appResponseWithStatus)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-77>)    fmt.Println("Long running function completed successfully.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-78>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-79>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-80>)// printEventSummary provides a readable log of agent and LLM interactions.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-81>)func printEventSummary(event *session.Event, turnLabel string) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-82>)    for _, part := range event.Content.Parts {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-83>)        // Check for a text part.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-84>)        if part.Text != "" {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-85>)            fmt.Printf("[%s][%s_TEXT]: %s\n", turnLabel, event.Author, part.Text)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-86>)        }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-87>)        // Check for a function call part.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-88>)        if fc := part.FunctionCall; fc != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-89>)            fmt.Printf("[%s][%s_CALL]: %s(%v) ID: %s\n", turnLabel, event.Author, fc.Name, fc.Args, fc.ID)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-90>)        }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-91>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-30-92>)}
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-2>)import com.google.adk.events.Event;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-3>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-4>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-5>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-6>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-7>)import com.google.adk.tools.LongRunningFunctionTool;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-8>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-9>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-10>)import com.google.common.collect.ImmutableMap;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-11>)import com.google.genai.types.Content;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-12>)import com.google.genai.types.FunctionCall;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-13>)import com.google.genai.types.FunctionResponse;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-14>)import com.google.genai.types.Part;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-15>)import java.util.Optional;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-16>)import java.util.UUID;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-17>)import java.util.concurrent.atomic.AtomicReference;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-18>)import java.util.stream.Collectors;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-19>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-20>)public class LongRunningFunctionExample {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-21>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-22>)  private static String USER_ID = "user123";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-23>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-24>)  @Schema(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-25>)      name = "create_ticket_long_running",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-26>)      description = """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-27>)          Creates a new support ticket with a specified urgency level.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-28>)          Examples of urgency are 'high', 'medium', or 'low'.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-29>)          The ticket creation is a long-running process, and its ID will be provided when ready.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-30>)      """)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-31>)  public static void createTicketAsync(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-32>)      @Schema(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-33>)              name = "urgency",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-34>)              description =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-35>)                  "The urgency level for the new ticket, such as 'high', 'medium', or 'low'.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-36>)          String urgency,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-37>)      @Schema(name = "toolContext") // Ensures ADK injection
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-38>)          ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-39>)    System.out.printf(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-40>)        "TOOL_EXEC: 'create_ticket_long_running' called with urgency: %s (Call ID: %s)%n",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-41>)        urgency, toolContext.functionCallId().orElse("N/A"));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-42>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-43>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-44>)  public static void main(String[] args) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-45>)    LlmAgent agent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-46>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-47>)            .name("ticket_agent")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-48>)            .description("Agent for creating tickets via a long-running task.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-49>)            .model("gemini-2.0-flash")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-50>)            .tools(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-51>)                ImmutableList.of(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-52>)                    LongRunningFunctionTool.create(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-53>)                        LongRunningFunctionExample.class, "createTicketAsync")))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-54>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-55>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-56>)    Runner runner = new InMemoryRunner(agent);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-57>)    Session session =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-58>)        runner.sessionService().createSession(agent.name(), USER_ID, null, null).blockingGet();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-59>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-60>)    // --- Turn 1: User requests ticket ---
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-61>)    System.out.println("\n--- Turn 1: User Request ---");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-62>)    Content initialUserMessage =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-63>)        Content.fromParts(Part.fromText("Create a high urgency ticket for me."));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-64>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-65>)    AtomicReference<String> funcCallIdRef = new AtomicReference<>();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-66>)    runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-67>)        .runAsync(USER_ID, session.id(), initialUserMessage)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-68>)        .blockingForEach(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-69>)            event -> {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-70>)              printEventSummary(event, "T1");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-71>)              if (funcCallIdRef.get() == null) { // Capture the first relevant function call ID
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-72>)                event.content().flatMap(Content::parts).orElse(ImmutableList.of()).stream()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-73>)                    .map(Part::functionCall)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-74>)                    .flatMap(Optional::stream)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-75>)                    .filter(fc -> "create_ticket_long_running".equals(fc.name().orElse("")))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-76>)                    .findFirst()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-77>)                    .flatMap(FunctionCall::id)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-78>)                    .ifPresent(funcCallIdRef::set);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-79>)              }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-80>)            });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-81>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-82>)    if (funcCallIdRef.get() == null) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-83>)      System.out.println("ERROR: Tool 'create_ticket_long_running' not called in Turn 1.");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-84>)      return;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-85>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-86>)    System.out.println("ACTION: Captured FunctionCall ID: " + funcCallIdRef.get());
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-87>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-88>)    // --- Turn 2: App provides initial ticket_id (simulating async tool completion) ---
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-89>)    System.out.println("\n--- Turn 2: App provides ticket_id ---");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-90>)    String ticketId = "TICKET-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-91>)    FunctionResponse ticketCreatedFuncResponse =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-92>)        FunctionResponse.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-93>)            .name("create_ticket_long_running")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-94>)            .id(funcCallIdRef.get())
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-95>)            .response(ImmutableMap.of("ticket_id", ticketId))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-96>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-97>)    Content appResponseWithTicketId =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-98>)        Content.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-99>)            .parts(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-100>)                ImmutableList.of(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-101>)                    Part.builder().functionResponse(ticketCreatedFuncResponse).build()))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-102>)            .role("user")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-103>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-104>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-105>)    runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-106>)        .runAsync(USER_ID, session.id(), appResponseWithTicketId)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-107>)        .blockingForEach(event -> printEventSummary(event, "T2"));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-108>)    System.out.println("ACTION: Sent ticket_id " + ticketId + " to agent.");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-109>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-110>)    // --- Turn 3: App provides ticket status update ---
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-111>)    System.out.println("\n--- Turn 3: App provides ticket status ---");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-112>)    FunctionResponse ticketStatusFuncResponse =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-113>)        FunctionResponse.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-114>)            .name("create_ticket_long_running")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-115>)            .id(funcCallIdRef.get())
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-116>)            .response(ImmutableMap.of("status", "approved", "ticket_id", ticketId))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-117>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-118>)    Content appResponseWithStatus =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-119>)        Content.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-120>)            .parts(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-121>)                ImmutableList.of(Part.builder().functionResponse(ticketStatusFuncResponse).build()))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-122>)            .role("user")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-123>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-124>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-125>)    runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-126>)        .runAsync(USER_ID, session.id(), appResponseWithStatus)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-127>)        .blockingForEach(event -> printEventSummary(event, "T3_FINAL"));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-128>)    System.out.println("Long running function completed successfully.");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-129>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-130>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-131>)  private static void printEventSummary(Event event, String turnLabel) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-132>)    event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-133>)        .content()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-134>)        .ifPresent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-135>)            content -> {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-136>)              String text =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-137>)                  content.parts().orElse(ImmutableList.of()).stream()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-138>)                      .map(part -> part.text().orElse(""))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-139>)                      .filter(s -> !s.isEmpty())
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-140>)                      .collect(Collectors.joining(" "));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-141>)              if (!text.isEmpty()) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-142>)                System.out.printf("[%s][%s_TEXT]: %s%n", turnLabel, event.author(), text);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-143>)              }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-144>)              content.parts().orElse(ImmutableList.of()).stream()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-145>)                  .map(Part::functionCall)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-146>)                  .flatMap(Optional::stream)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-147>)                  .findFirst() // Assuming one function call per relevant event for simplicity
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-148>)                  .ifPresent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-149>)                      fc ->
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-150>)                          System.out.printf(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-151>)                              "[%s][%s_CALL]: %s(%s) ID: %s%n",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-152>)                              turnLabel,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-153>)                              event.author(),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-154>)                              fc.name().orElse("N/A"),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-155>)                              fc.args().orElse(ImmutableMap.of()),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-156>)                              fc.id().orElse("N/A")));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-157>)            });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-158>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-31-159>)}
    
Python complete example: File Processing Simulation
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-2>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-6>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-8>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-15>)import asyncio
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-16>)from google.adk.agents import Agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-17>)from google.adk.events import Event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-18>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-19>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-20>)from google.genai import types
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-21>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-22>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-23>)from typing import Any
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-24>)from google.adk.tools import LongRunningFunctionTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-25>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-26>)# 1. Define the long running function
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-27>)def ask_for_approval(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-28>)    purpose: str, amount: float
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-29>)) -> dict[str, Any]:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-30>)    """Ask for approval for the reimbursement."""
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-31>)    # create a ticket for the approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-32>)    # Send a notification to the approver with the link of the ticket
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-33>)    return {'status': 'pending', 'approver': 'Sean Zhou', 'purpose' : purpose, 'amount': amount, 'ticket-id': 'approval-ticket-1'}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-34>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-35>)def reimburse(purpose: str, amount: float) -> dict[str, Any]:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-36>)    """Reimburse the amount of money to the employee."""
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-37>)    # send the reimbrusement request to payment vendor
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-38>)    return {'status': 'ok'}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-39>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-40>)# 2. Wrap the function with LongRunningFunctionTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-41>)long_running_tool = LongRunningFunctionTool(func=ask_for_approval)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-42>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-43>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-44>)# 3. Use the tool in an Agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-45>)file_processor_agent = Agent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-46>)    # Use a model compatible with function calling
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-47>)    model="gemini-2.0-flash",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-48>)    name='reimbursement_agent',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-49>)    instruction="""
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-50>)      You are an agent whose job is to handle the reimbursement process for
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-51>)      the employees. If the amount is less than $100, you will automatically
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-52>)      approve the reimbursement.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-53>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-54>)      If the amount is greater than $100, you will
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-55>)      ask for approval from the manager. If the manager approves, you will
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-56>)      call reimburse() to reimburse the amount to the employee. If the manager
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-57>)      rejects, you will inform the employee of the rejection.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-58>)    """,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-59>)    tools=[reimburse, long_running_tool]
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-60>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-61>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-62>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-63>)APP_NAME = "human_in_the_loop"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-64>)USER_ID = "1234"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-65>)SESSION_ID = "session1234"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-66>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-67>)# Session and Runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-68>)async def setup_session_and_runner():
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-69>)    session_service = InMemorySessionService()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-70>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-71>)    runner = Runner(agent=file_processor_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-72>)    return session, runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-73>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-74>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-75>)# Agent Interaction
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-76>)async def call_agent_async(query):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-77>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-78>)    def get_long_running_function_call(event: Event) -> types.FunctionCall:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-79>)        # Get the long running function call from the event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-80>)        if not event.long_running_tool_ids or not event.content or not event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-81>)            return
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-82>)        for part in event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-83>)            if (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-84>)                part
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-85>)                and part.function_call
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-86>)                and event.long_running_tool_ids
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-87>)                and part.function_call.id in event.long_running_tool_ids
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-88>)            ):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-89>)                return part.function_call
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-90>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-91>)    def get_function_response(event: Event, function_call_id: str) -> types.FunctionResponse:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-92>)        # Get the function response for the fuction call with specified id.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-93>)        if not event.content or not event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-94>)            return
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-95>)        for part in event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-96>)            if (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-97>)                part
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-98>)                and part.function_response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-99>)                and part.function_response.id == function_call_id
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-100>)            ):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-101>)                return part.function_response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-102>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-103>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-104>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-105>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-106>)    print("\nRunning agent...")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-107>)    events_async = runner.run_async(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-108>)        session_id=session.id, user_id=USER_ID, new_message=content
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-109>)    )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-110>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-111>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-112>)    long_running_function_call, long_running_function_response, ticket_id = None, None, None
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-113>)    async for event in events_async:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-114>)        # Use helper to check for the specific auth request event
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-115>)        if not long_running_function_call:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-116>)            long_running_function_call = get_long_running_function_call(event)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-117>)        else:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-118>)            _potential_response = get_function_response(event, long_running_function_call.id)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-119>)            if _potential_response: # Only update if we get a non-None response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-120>)                long_running_function_response = _potential_response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-121>)                ticket_id = long_running_function_response.response['ticket-id']
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-122>)        if event.content and event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-123>)            if text := ''.join(part.text or '' for part in event.content.parts):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-124>)                print(f'[{event.author}]: {text}')
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-125>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-126>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-127>)    if long_running_function_response:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-128>)        # query the status of the correpsonding ticket via tciket_id
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-129>)        # send back an intermediate / final response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-130>)        updated_response = long_running_function_response.model_copy(deep=True)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-131>)        updated_response.response = {'status': 'approved'}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-132>)        async for event in runner.run_async(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-133>)          session_id=session.id, user_id=USER_ID, new_message=types.Content(parts=[types.Part(function_response = updated_response)], role='user')
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-134>)        ):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-135>)            if event.content and event.content.parts:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-136>)                if text := ''.join(part.text or '' for part in event.content.parts):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-137>)                    print(f'[{event.author}]: {text}')
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-138>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-139>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-140>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-141>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-142>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-143>)# reimbursement that doesn't require approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-144>)# asyncio.run(call_agent_async("Please reimburse 50$ for meals"))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-145>)await call_agent_async("Please reimburse 50$ for meals") # For Notebooks, uncomment this line and comment the above line
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-146>)# reimbursement that requires approval
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-147>)# asyncio.run(call_agent_async("Please reimburse 200$ for meals"))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-32-148>)await call_agent_async("Please reimburse 200$ for meals") # For Notebooks, uncomment this line and comment the above line
    
#### Key aspects of this example[¶](<https://adk.dev/tools-custom/function-tools/#key-aspects-of-this-example> "Permanent link")

  * **`LongRunningFunctionTool`** : Wraps the supplied method/function; the framework handles sending yielded updates and the final return value as sequential FunctionResponses.
  * **Agent instruction** : Directs the LLM to use the tool and understand the incoming FunctionResponse stream (progress vs. completion) for user updates.
  * **Final return** : The function returns the final result dictionary, which is sent in the concluding FunctionResponse to indicate completion.

## Agent-as-a-Tool[¶](<https://adk.dev/tools-custom/function-tools/#agent-tool> "Permanent link")

This feature allows you to leverage the capabilities of other agents within your system by calling them as tools. The Agent-as-a-Tool enables you to invoke another agent to perform a specific task, effectively **delegating responsibility**. This is conceptually similar to creating a Python function that calls another agent and uses the agent's response as the function's return value.

### Key difference from sub-agents[¶](<https://adk.dev/tools-custom/function-tools/#key-difference-from-sub-agents> "Permanent link")

It's important to distinguish an Agent-as-a-Tool from a sub-agent.

  * **Agent-as-a-Tool:** When Agent A calls Agent B as a tool (using Agent-as-a-Tool), Agent B's answer is **passed back** to Agent A, which then summarizes the answer and generates a response to the user. Agent A retains control and continues to handle future user input.
  * **Sub-agent:** When Agent A calls Agent B as a sub-agent, the responsibility of answering the user is completely **transferred to Agent B**. Agent A is effectively out of the loop. All subsequent user input will be answered by Agent B.

### Use `AgentTool`[¶](<https://adk.dev/tools-custom/function-tools/#use-agenttool> "Permanent link")

To use an agent as a tool, wrap the agent with the `AgentTool` class.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-33-1>)tools=[AgentTool(agent=agent_b)]
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-34-1>)tools: [new AgentTool({agent: agentB})]
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-35-1>)agenttool.New(agent, &agenttool.Config{...})
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-36-1>)AgentTool.create(agent)
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-37-1>)AgentTool(agent = agentB)
    
### Customize your agent tool[¶](<https://adk.dev/tools-custom/function-tools/#customize-your-agent-tool> "Permanent link")

The `AgentTool` class provides the following attributes for customizing its behavior.

#### Skip summarization[¶](<https://adk.dev/tools-custom/function-tools/#skip-summarization> "Permanent link")

**`skip_summarization`** (boolean) If set to `True`, this customization instructs the framework to bypass the LLM-based summarization of the tool agent's response. This feature is best used when the tool's output is already well-formatted and requires no further processing.

  * **Use:** Python/TypeScript (`skip_summarization`); Kotlin/Java (`skipSummarization`).

Example

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-2>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-6>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-8>)#
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-15>)from google.adk.agents import Agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-16>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-17>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-18>)from google.adk.tools.agent_tool import AgentTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-19>)from google.genai import types
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-20>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-21>)APP_NAME="summary_agent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-22>)USER_ID="user1234"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-23>)SESSION_ID="1234"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-24>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-25>)summary_agent = Agent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-26>)    model="gemini-2.0-flash",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-27>)    name="summary_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-28>)    instruction="""You are an expert summarizer. Please read the following text and provide a concise summary.""",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-29>)    description="Agent to summarize text",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-30>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-31>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-32>)root_agent = Agent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-33>)    model='gemini-2.0-flash',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-34>)    name='root_agent',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-35>)    instruction="""You are a helpful assistant. When the user provides a text, use the 'summarize' tool to generate a summary. Always forward the user's message exactly as received to the 'summarize' tool, without modifying or summarizing it yourself. Present the response from the tool to the user.""",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-36>)    tools=[AgentTool(agent=summary_agent, skip_summarization=True)]
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-37>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-38>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-39>)# Session and Runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-40>)async def setup_session_and_runner():
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-41>)    session_service = InMemorySessionService()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-42>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-43>)    runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-44>)    return session, runner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-45>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-46>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-47>)# Agent Interaction
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-48>)async def call_agent_async(query):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-49>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-50>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-51>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-52>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-53>)    async for event in events:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-54>)        if event.is_final_response():
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-55>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-56>)            print("Agent Response: ", final_response)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-57>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-58>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-59>)long_text = """Quantum computing represents a fundamentally different approach to computation, 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-60>)leveraging the bizarre principles of quantum mechanics to process information. Unlike classical computers 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-61>)that rely on bits representing either 0 or 1, quantum computers use qubits which can exist in a state of superposition - effectively 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-62>)being 0, 1, or a combination of both simultaneously. Furthermore, qubits can become entangled, 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-63>)meaning their fates are intertwined regardless of distance, allowing for complex correlations. This parallelism and 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-64>)interconnectedness grant quantum computers the potential to solve specific types of incredibly complex problems - such 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-65>)as drug discovery, materials science, complex system optimization, and breaking certain types of cryptography - far 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-66>)faster than even the most powerful classical supercomputers could ever achieve, although the technology is still largely in its developmental stages."""
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-67>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-68>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-69>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-70>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-38-71>)await call_agent_async(long_text)
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-1>)/**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-3>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-7>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-9>) *
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-14>) * limitations under the License.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-15>) */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-16>)import { AgentTool, InMemoryRunner, LlmAgent } from '@google/adk';
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-17>)import {Part, createUserContent} from '@google/genai';
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-18>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-19>)/**
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-20>) * This example demonstrates how to use an agent as a tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-21>) */
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-22>)async function main() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-23>)  // Define the summarization agent that will be used as a tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-24>)  const summaryAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-25>)    name: 'summary_agent',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-26>)    model: 'gemini-2.5-flash',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-27>)    description: 'Agent to summarize text',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-28>)    instruction:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-29>)      'You are an expert summarizer. Please read the following text and provide a concise summary.',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-30>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-31>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-32>)  // Define the main agent that uses the summarization agent as a tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-33>)  // skipSummarization is set to true, so the main_agent will directly output
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-34>)  // the result from the summary_agent without further processing.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-35>)  const mainAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-36>)    name: 'main_agent',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-37>)    model: 'gemini-2.5-flash',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-38>)    instruction:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-39>)      "You are a helpful assistant. When the user provides a text, use the 'summary_agent' tool to generate a summary. Always forward the user's message exactly as received to the 'summary_agent' tool, without modifying or summarizing it yourself. Present the response from the tool to the user.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-40>)    tools: [new AgentTool({agent: summaryAgent, skipSummarization: true})],
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-41>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-42>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-43>)  const appName = 'agent-as-a-tool-app';
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-44>)  const runner = new InMemoryRunner({agent: mainAgent, appName});
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-45>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-46>)  const longText = `Quantum computing represents a fundamentally different approach to computation, 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-47>)leveraging the bizarre principles of quantum mechanics to process information. Unlike classical computers 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-48>)that rely on bits representing either 0 or 1, quantum computers use qubits which can exist in a state of superposition - effectively 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-49>)being 0, 1, or a combination of both simultaneously. Furthermore, qubits can become entangled, 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-50>)meaning their fates are intertwined regardless of distance, allowing for complex correlations. This parallelism and 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-51>)interconnectedness grant quantum computers the potential to solve specific types of incredibly complex problems - such 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-52>)as drug discovery, materials science, complex system optimization, and breaking certain types of cryptography - far 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-53>)faster than even the most powerful classical supercomputers could ever achieve, although the technology is still largely in its developmental stages.`;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-54>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-55>)  // Create the session before running the agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-56>)  await runner.sessionService.createSession({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-57>)    appName,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-58>)    userId: 'user1',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-59>)    sessionId: 'session1',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-60>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-61>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-62>)  // Run the agent with the long text to summarize
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-63>)  const events = runner.runAsync({
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-64>)    userId: 'user1',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-65>)    sessionId: 'session1',
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-66>)    newMessage: createUserContent(longText),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-67>)  });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-68>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-69>)  // Print the final response from the agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-70>)  console.log('Agent Response:');
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-71>)  for await (const event of events) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-72>)    if (event.content?.parts?.length) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-73>)      const responsePart = event.content.parts.find((p: Part) => p.functionResponse);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-74>)      if (responsePart && responsePart.functionResponse) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-75>)        console.log(responsePart.functionResponse.response);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-76>)      }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-77>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-78>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-79>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-80>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-39-81>)main();
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-1>)import (
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-4>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-5>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-6>)    "google.golang.org/adk/v2/tool/agenttool"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-7>)    "google.golang.org/genai"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-8>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-9>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-10>)// createSummarizerAgent creates an agent whose sole purpose is to summarize text.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-11>)func createSummarizerAgent(ctx context.Context) (agent.Agent, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-12>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-13>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-14>)        return nil, err
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-15>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-16>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-17>)        Name:        "SummarizerAgent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-18>)        Model:       model,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-19>)        Instruction: "You are an expert at summarizing text. Take the user's input and provide a concise summary.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-20>)        Description: "An agent that summarizes text.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-21>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-22>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-23>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-24>)// createMainAgent creates the primary agent that will use the summarizer agent as a tool.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-25>)func createMainAgent(ctx context.Context, tools ...tool.Tool) (agent.Agent, error) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-26>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-27>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-28>)        return nil, err
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-29>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-30>)    return llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-31>)        Name:  "MainAgent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-32>)        Model: model,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-33>)        Instruction: "You are a helpful assistant. If you are asked to summarize a long text, use the 'summarize' tool. " +
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-34>)            "After getting the summary, present it to the user by saying 'Here is a summary of the text:'.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-35>)        Description: "The main agent that can delegate tasks.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-36>)        Tools:       tools,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-37>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-38>)}
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-39>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-40>)func RunAgentAsToolSimulation() {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-41>)    ctx := context.Background()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-42>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-43>)    // 1. Create the Tool Agent (Summarizer)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-44>)    summarizerAgent, err := createSummarizerAgent(ctx)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-45>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-46>)        log.Fatalf("Failed to create summarizer agent: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-47>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-48>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-49>)    // 2. Wrap the Tool Agent in an AgentTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-50>)    summarizeTool := agenttool.New(summarizerAgent, &agenttool.Config{
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-51>)        SkipSummarization: true,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-52>)    })
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-53>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-54>)    // 3. Create the Main Agent and provide it with the AgentTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-55>)    mainAgent, err := createMainAgent(ctx, summarizeTool)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-56>)    if err != nil {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-57>)        log.Fatalf("Failed to create main agent: %v", err)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-58>)    }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-59>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-60>)    // 4. Run the main agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-61>)    prompt := `
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-62>)        Please summarize this text for me:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-63>)        Quantum computing represents a fundamentally different approach to computation,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-64>)        leveraging the bizarre principles of quantum mechanics to process information. Unlike classical computers
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-65>)        that rely on bits representing either 0 or 1, quantum computers use qubits which can exist in a state of superposition - effectively
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-66>)        being 0, 1, or a combination of both simultaneously. Furthermore, qubits can become entangled,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-67>)        meaning their fates are intertwined regardless of distance, allowing for complex correlations. This parallelism and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-68>)        interconnectedness grant quantum computers the potential to solve specific types of incredibly complex problems - such
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-69>)        as drug discovery, materials science, complex system optimization, and breaking certain types of cryptography - far
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-70>)        faster than even the most powerful classical supercomputers could ever achieve, although the technology is still largely in its developmental stages.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-71>)    `
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-72>)    fmt.Printf("\nPrompt: %s\nResponse: ", prompt)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-73>)    callAgent(context.Background(), mainAgent, prompt)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-74>)    fmt.Println("\n---")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-40-75>)}
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-2>)import com.google.adk.events.Event;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-3>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-4>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-5>)import com.google.adk.tools.AgentTool;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-6>)import com.google.genai.types.Content;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-7>)import com.google.genai.types.Part;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-8>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-9>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-10>)public class AgentToolCustomization {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-11>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-12>)  private static final String APP_NAME = "summary_agent";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-13>)  private static final String USER_ID = "user1234";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-15>)  public static void initAgentAndRun(String prompt) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-16>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-17>)    LlmAgent summaryAgent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-18>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-19>)            .model("gemini-2.0-flash")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-20>)            .name("summaryAgent")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-21>)            .instruction(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-22>)                "You are an expert summarizer. Please read the following text and provide a concise summary.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-23>)            .description("Agent to summarize text")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-24>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-25>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-26>)    // Define root_agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-27>)    LlmAgent rootAgent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-28>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-29>)            .model("gemini-2.0-flash")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-30>)            .name("rootAgent")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-31>)            .instruction(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-32>)                "You are a helpful assistant. When the user provides a text, always use the 'summaryAgent' tool to generate a summary. Always forward the user's message exactly as received to the 'summaryAgent' tool, without modifying or summarizing it yourself. Present the response from the tool to the user.")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-33>)            .description("Assistant agent")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-34>)            .tools(AgentTool.create(summaryAgent, true)) // Set skipSummarization to true
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-35>)            .build();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-36>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-37>)    // Create an InMemoryRunner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-38>)    InMemoryRunner runner = new InMemoryRunner(rootAgent, APP_NAME);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-39>)    // InMemoryRunner automatically creates a session service. Create a session using the service
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-40>)    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-41>)    Content userMessage = Content.fromParts(Part.fromText(prompt));
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-42>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-43>)    // Run the agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-44>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-45>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-46>)    // Stream event response
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-47>)    eventStream.blockingForEach(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-48>)        event -> {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-49>)          if (event.finalResponse()) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-50>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-51>)          }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-52>)        });
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-53>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-54>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-55>)  public static void main(String[] args) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-56>)    String longText =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-57>)        """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-58>)            Quantum computing represents a fundamentally different approach to computation,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-59>)            leveraging the bizarre principles of quantum mechanics to process information. Unlike classical computers
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-60>)            that rely on bits representing either 0 or 1, quantum computers use qubits which can exist in a state of superposition - effectively
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-61>)            being 0, 1, or a combination of both simultaneously. Furthermore, qubits can become entangled,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-62>)            meaning their fates are intertwined regardless of distance, allowing for complex correlations. This parallelism and
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-63>)            interconnectedness grant quantum computers the potential to solve specific types of incredibly complex problems - such
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-64>)            as drug discovery, materials science, complex system optimization, and breaking certain types of cryptography - far
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-65>)            faster than even the most powerful classical supercomputers could ever achieve, although the technology is still largely in its developmental stages.""";
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-66>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-67>)    initAgentAndRun(longText);
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-68>)  }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-41-69>)}
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-1>)import com.google.adk.kt.agents.Instruction
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-2>)import com.google.adk.kt.agents.LlmAgent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-3>)import com.google.adk.kt.models.Gemini
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-4>)import com.google.adk.kt.runners.InMemoryRunner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-5>)import com.google.adk.kt.tools.AgentTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-6>)import com.google.adk.kt.types.Content
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-7>)import com.google.adk.kt.types.Part
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-8>)import kotlinx.coroutines.runBlocking
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-9>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-10>)fun main() =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-11>)    runBlocking {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-12>)        val appName = "summary_agent"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-13>)        val userId = "user1234"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-15>)        // Define a specialized agent to be used as a tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-16>)        val summaryAgent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-17>)            LlmAgent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-18>)                name = "summary_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-19>)                model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-20>)                description = "Agent to summarize text",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-21>)                instruction =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-22>)                    Instruction(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-23>)                        "You are an expert summarizer. Please read the following text and provide a concise summary.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-24>)                    ),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-25>)            )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-26>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-27>)        // Wrap the agent in an AgentTool with skipSummarization = true
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-28>)        val summaryTool =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-29>)            AgentTool(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-30>)                agent = summaryAgent,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-31>)                skipSummarization = true,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-32>)            )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-33>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-34>)        // Define the root agent that uses the summary tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-35>)        val rootAgent =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-36>)            LlmAgent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-37>)                name = "root_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-38>)                model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-39>)                instruction =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-40>)                    Instruction(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-41>)                        "You are a helpful assistant. When the user provides a text, use the 'summary_agent' tool to generate a summary. Always forward the user's message exactly as received to the 'summary_agent' tool. Present the response from the tool to the user.",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-42>)                    ),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-43>)                tools = listOf(summaryTool),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-44>)            )
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-45>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-46>)        // Create an InMemoryRunner
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-47>)        val runner = InMemoryRunner(agent = rootAgent, appName = appName)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-48>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-49>)        val sessionId = "session_001"
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-50>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-51>)        val longText =
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-52>)            """
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-53>)            Quantum computing represents a fundamentally different approach to computation, 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-54>)            leveraging the bizarre principles of quantum mechanics to process information. Unlike classical computers 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-55>)            that rely on bits representing either 0 or 1, quantum computers use qubits which can exist in a state of superposition - effectively 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-56>)            being 0, 1, or a combination of both simultaneously. Furthermore, qubits can become entangled, 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-57>)            meaning their fates are intertwined regardless of distance, allowing for complex correlations. This parallelism and 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-58>)            interconnectedness grant quantum computers the potential to solve specific types of incredibly complex problems - such 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-59>)            as drug discovery, materials science, complex system optimization, and breaking certain types of cryptography - far 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-60>)            faster than even the most powerful classical supercomputers could ever achieve, although the technology is still largely in its developmental stages.
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-61>)            """.trimIndent()
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-62>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-63>)        val userMessage = Content(parts = listOf(Part(text = longText)))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-64>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-65>)        // Run the agent and collect events
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-66>)        runner.runAsync(userId = userId, sessionId = sessionId, newMessage = userMessage).collect {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-67>)                event ->
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-68>)            if (event.isFinalResponse) {
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-69>)                val finalResponse = event.content?.parts?.firstOrNull()?.text
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-70>)                println("Agent Response: $finalResponse")
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-71>)            }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-72>)        }
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-42-73>)    }
    
##### How it works[¶](<https://adk.dev/tools-custom/function-tools/#how-it-works_2> "Permanent link")

  1. When the `root_agent` receives the long text, its instruction tells it to use the 'summarize' tool for long texts.
  2. The framework recognizes 'summarize' as an `AgentTool` that wraps the `summary_agent`.
  3. Behind the scenes, the `root_agent` will call the `summary_agent` with the long text as input.
  4. The `summary_agent` will process the text according to its instruction and generate a summary.
  5. **The response from the`summary_agent` is then passed back to the `root_agent`.**
  6. The `root_agent` can then take the summary and formulate its final response to the user (e.g., "Here's a summary of the text: ...")

#### Propagate grounding metadata[¶](<https://adk.dev/tools-custom/function-tools/#propagate-grounding-metadata> "Permanent link")

**`propagate_grounding_metadata`** (boolean, default: `False`) If set to `True`, the tool automatically forwards any grounding metadata, such as Google Search citations, generated by the sub-agent up to the parent agent's session state. This customization ensures that citations are preserved when using specialized search agents as tools.

Python
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-1>)from google.adk.agents import Agent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-2>)from google.adk.tools import AgentTool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-3>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-4>)search_specialist_agent = Agent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-5>)    # Specify your generative model
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-6>)    model="gemini-flash-latest",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-7>)    name="search_specialist_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-8>)    instruction=(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-9>)        "You are a search expert. Find and "
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-10>)        "compile citations on requested topics."
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-11>)    ),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-12>)    # Add any search tools here
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-13>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-14>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-15>)search_agent_tool = AgentTool(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-16>)    agent=search_specialist_agent,
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-17>)    # Keeps citations intact back to the root
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-18>)    propagate_grounding_metadata=True
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-19>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-20>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-21>)root_agent = Agent(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-22>)    model="gemini-flash-latest",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-23>)    name="root_agent",
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-24>)    description=(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-25>)        "A central coordinator that delegates "
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-26>)        "to specialist agents."
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-27>)    ),
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-28>)    tools=[search_agent_tool]
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-43-29>))
    
#### Control plugin inheritance[¶](<https://adk.dev/tools-custom/function-tools/#control-plugin-inheritance> "Permanent link")

When you wrap an agent with `AgentTool`, you can control whether it inherits plugins from the parent runner using the `include_plugins` parameter.

  * **`include_plugins=True` (default):** The child agent inherits all plugins from the parent, preserving trace spans and event streaming.
  * **`include_plugins=False`:** The child agent runs in an isolated environment without inheriting any plugins from the parent. Use this setting to ensure an agent's execution is self-contained and unaffected by the parent's plugin environment.

Python
    
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-1>)from google.adk.tools import agent_tool
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-2>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-3>)# Placeholder definition for MyImageAgent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-4>)class MyImageAgent:
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-5>)    def __init__(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-6>)        self, name="My Agent", description="A simple image agent."
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-7>)    ):
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-8>)        self.name = name
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-9>)        # Added description attribute
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-10>)        self.description = description 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-11>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-12>)# Example 1: Isolate MyImageAgent from parent plugins 
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-13>)my_isolated_tool = agent_tool.AgentTool(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-14>)    agent=MyImageAgent(), # Instantiate MyImageAgent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-15>)    include_plugins=False
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-16>))
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-17>)
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-18>)# Example 2: Inherit plugins
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-19>)my_observable_tool = agent_tool.AgentTool(
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-20>)    agent=MyImageAgent(), # Instantiate MyImageAgent
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-21>)    include_plugins=True
    [](<https://adk.dev/tools-custom/function-tools/#__codelineno-44-22>))
    
Back to top 