# Simple agents - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/llm-agents/](https://adk.dev/agents/llm-agents/)

[ Skip to content ](<https://adk.dev/agents/llm-agents/#simple-agents-with-llmagent>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/llm-agents.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/llm-agents/index.md> "View this page as Markdown")

# Simple agents with LlmAgent[¶](<https://adk.dev/agents/llm-agents/#simple-agents-with-llmagent> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

The `LlmAgent` class, often aliased simply as `Agent`, is a core component in ADK, acting as the core part of your agent application. It leverages the power of a Large Language Model (LLM) or generative AI model for reasoning, understanding natural language, making decisions, generating responses, and interacting with tools. Since this type of agent uses an AI model to interpret instructions and context, the AI model dynamically decides how to proceed, which tools to use (if any), and what output to provide. As such, the behavior of this type of agent is non-deterministic and must be built and evaluated with this behavior in mind.

Building an effective `LlmAgent` involves defining its identity, clearly guiding its behavior through instructions, and equipping it with the necessary tools and capabilities.

## Define agent identity and purpose[¶](<https://adk.dev/agents/llm-agents/#define-agent-identity-and-purpose> "Permanent link")

First, you need to establish what the agent _is_ and what it's _for_.

  * **`name` (Required):** Every agent needs a unique string identifier. This `name` is crucial for internal operations, especially in multi-agent systems where agents need to refer to or delegate tasks to each other. Choose a descriptive name that reflects the agent's function (e.g., `customer_support_router`, `billing_inquiry_agent`). Avoid reserved names like `user`.

  * **`description` (Optional, Recommended for Multi-Agent):** Provide a concise summary of the agent's capabilities. This description is primarily used by _other_ LLM agents to determine if they should route a task to this agent. Make it specific enough to differentiate it from peers (e.g., "Handles inquiries about current billing statements," not just "Billing agent").

  * **`model` (Required):** Specify the underlying LLM that will power this agent's reasoning. This is a string identifier like `"gemini-flash-latest"`. The choice of model impacts the agent's capabilities, cost, and performance. See the [Models](<https://adk.dev/agents/models/>) page for available options and considerations.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-0-1>)# Example: Defining the basic identity
    [](<https://adk.dev/agents/llm-agents/#__codelineno-0-2>)capital_agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-0-3>)    model="gemini-flash-latest",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-0-4>)    name="capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-0-5>)    description="Answers user questions about the capital city of a given country."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-0-6>)    # instruction and tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-0-7>))
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-1-1>)// Example: Defining the basic identity
    [](<https://adk.dev/agents/llm-agents/#__codelineno-1-2>)const capitalAgent = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-1-3>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-1-4>)    name: 'capital_agent',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-1-5>)    description: 'Answers user questions about the capital city of a given country.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-1-6>)    // instruction and tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-1-7>)});
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-2-1>)// Example: Defining the basic identity
    [](<https://adk.dev/agents/llm-agents/#__codelineno-2-2>)agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-2-3>)    Name:        "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-2-4>)    Model:       model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-2-5>)    Description: "Answers user questions about the capital city of a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-2-6>)    // instruction and tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-2-7>)})
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-1>)// Example: Defining the basic identity
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-2>)LlmAgent capitalAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-3>)    LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-4>)        .model("gemini-flash-latest")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-5>)        .name("capital_agent")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-6>)        .description("Answers user questions about the capital city of a given country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-7>)        // instruction and tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-3-8>)        .build();
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-4-1>)val capitalAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-4-2>)    LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-4-3>)        name = "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-4-4>)        model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-4-5>)        description = "Answers user questions about the capital city of a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-4-6>)    )
    
## Guide the agent with instructions[¶](<https://adk.dev/agents/llm-agents/#guide-the-agent-with-instructions> "Permanent link")

The `instruction` parameter is arguably the most critical for shaping an `LlmAgent`'s behavior. It's a string (or a function returning a string) that tells the agent:

  * Its core task or goal.
  * Its personality or persona (e.g., "You are a helpful assistant," "You are a witty pirate").
  * Constraints on its behavior (e.g., "Only answer questions about X," "Never reveal Y").
  * How and when to use its `tools`. You should explain the purpose of each tool and the circumstances under which it should be called, supplementing any descriptions within the tool itself.
  * The desired format for its output (e.g., "Respond in JSON," "Provide a bulleted list").

**Tips for effective instructions:**

  * **Be Clear and Specific:** Avoid ambiguity. Clearly state the desired actions and outcomes.
  * **Use Markdown:** Improve readability for complex instructions using headings, lists, etc.
  * **Provide Examples (Few-Shot):** For complex tasks or specific output formats, include examples directly in the instruction.
  * **Guide Tool Use:** Don't just list tools; explain _when_ and _why_ the agent should use them.

**Use dynamic state variables:**

  * The instruction is a string template, you can use the `{var}` syntax to insert dynamic values into the instruction.
  * `{var}` is used to insert the value of the state variable named var.
  * `{artifact.var}` is used to insert the text content of the artifact named var.
  * If the state variable or artifact does not exist, the agent will raise an error. If you want to ignore the error, you can append a `?` to the variable name as in `{var?}`.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-1>)# Example: Adding instructions
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-2>)capital_agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-3>)    model="gemini-flash-latest",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-4>)    name="capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-5>)    description="Answers user questions about the capital city of a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-6>)    instruction="""You are an agent that provides the capital city of a country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-7>)When a user asks for the capital of a country:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-8>)1. Identify the country name from the user's query.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-9>)2. Use the `get_capital_city` tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-10>)3. Respond clearly to the user, stating the capital city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-11>)Example Query: "What's the capital of {country}?"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-12>)Example Response: "The capital of France is Paris."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-13>)""",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-14>)    # tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-5-15>))
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-1>)// Example: Adding instructions
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-2>)const capitalAgent = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-3>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-4>)    name: 'capital_agent',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-5>)    description: 'Answers user questions about the capital city of a given country.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-6>)    instruction: `You are an agent that provides the capital city of a country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-7>)        When a user asks for the capital of a country:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-8>)        1. Identify the country name from the user's query.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-9>)        2. Use the \`getCapitalCity\` tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-10>)        3. Respond clearly to the user, stating the capital city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-11>)        Example Query: "What's the capital of {country}?"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-12>)        Example Response: "The capital of France is Paris."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-13>)        `,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-14>)    // tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-6-15>)});
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-1>)    // Example: Adding instructions
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-2>)    agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-3>)        Name:        "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-4>)        Model:       model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-5>)        Description: "Answers user questions about the capital city of a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-6>)        Instruction: `You are an agent that provides the capital city of a country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-7>)When a user asks for the capital of a country:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-8>)1. Identify the country name from the user's query.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-9>)2. Use the 'get_capital_city' tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-10>)3. Respond clearly to the user, stating the capital city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-11>)Example Query: "What's the capital of {country}?"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-12>)Example Response: "The capital of France is Paris."`,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-13>)        // tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-7-14>)    })
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-1>)// Example: Adding instructions
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-2>)LlmAgent capitalAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-3>)    LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-4>)        .model("gemini-flash-latest")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-5>)        .name("capital_agent")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-6>)        .description("Answers user questions about the capital city of a given country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-7>)        .instruction(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-8>)            """
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-9>)            You are an agent that provides the capital city of a country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-10>)            When a user asks for the capital of a country:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-11>)            1. Identify the country name from the user's query.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-12>)            2. Use the `get_capital_city` tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-13>)            3. Respond clearly to the user, stating the capital city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-14>)            Example Query: "What's the capital of {country}?"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-15>)            Example Response: "The capital of France is Paris."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-16>)            """)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-17>)        // tools will be added next
    [](<https://adk.dev/agents/llm-agents/#__codelineno-8-18>)        .build();
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-1>)val instructedAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-2>)    LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-3>)        name = "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-4>)        model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-5>)        instruction =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-6>)            Instruction(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-7>)                """
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-8>)                You are an agent that provides the capital city of a country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-9>)                When a user asks for the capital of a country:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-10>)                1. Identify the country name from the user's query.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-11>)                2. Use the `getCapitalCity` tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-12>)                3. Respond clearly to the user, stating the capital city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-13>)                Example Query: "What's the capital of {country}?"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-14>)                Example Response: "The capital of France is Paris."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-15>)                """.trimIndent(),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-16>)            ),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-9-17>)    )
    
**Note:** For instructions that apply to _all_ agents in a system, consider using `global_instruction` on the root agent.

## Equip the agent with tools[¶](<https://adk.dev/agents/llm-agents/#equip-the-agent-with-tools> "Permanent link")

Tools give your `LlmAgent` capabilities beyond the LLM's built-in knowledge or reasoning. They allow the agent to interact with the outside world, perform calculations, fetch real-time data, or execute specific actions.

  * **`tools` (Optional):** Provide a list of tools the agent can use. Each item in the list can be:
    * A native function or method (wrapped as a `FunctionTool`). Python ADK automatically wraps the native function into a `FunctionTool` whereas, you must explicitly wrap your Java methods using `FunctionTool.create(...)`. In Kotlin, you can use the `@Tool` annotation to automatically generate a `FunctionTool` at compile-time.
    * An instance of a class inheriting from `BaseTool`.
    * An instance of another agent (`AgentTool`, enabling agent-to-agent delegation - see [Custom agent workflows](<https://adk.dev/agents/custom-agents/#delegation>)).

The LLM uses the function/tool names, descriptions (from docstrings or the `description` field), and parameter schemas to decide which tool to call based on the conversation and its instructions.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-1>)# Define a tool function
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-2>)def get_capital_city(country: str) -> str:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-3>)  """Retrieves the capital city for a given country."""
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-4>)  # Replace with actual logic (e.g., API call, database lookup)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-5>)  capitals = {"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-6>)  return capitals.get(country.lower(), f"Sorry, I don't know the capital of {country}.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-7>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-8>)# Add the tool to the agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-9>)capital_agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-10>)    model="gemini-flash-latest",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-11>)    name="capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-12>)    description="Answers user questions about the capital city of a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-13>)    instruction="""You are an agent that provides the capital city of a country... (previous instruction text)""",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-14>)    tools=[get_capital_city] # Provide the function directly
    [](<https://adk.dev/agents/llm-agents/#__codelineno-10-15>))
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-1>)import {z} from 'zod';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-2>)import { LlmAgent, FunctionTool } from '@google/adk';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-3>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-4>)// Define the schema for the tool's input parameters
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-5>)const getCapitalCityParamsSchema = z.object({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-6>)    country: z.string().describe('The country to get capital for.'),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-7>)});
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-8>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-9>)// Define the tool function itself
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-10>)async function getCapitalCity(params: z.infer<typeof getCapitalCityParamsSchema>): Promise<{ capitalCity: string }> {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-11>)const capitals: Record<string, string> = {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-12>)    'france': 'Paris',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-13>)    'japan': 'Tokyo',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-14>)    'canada': 'Ottawa',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-15>)};
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-16>)const result = capitals[params.country.toLowerCase()] ??
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-17>)    `Sorry, I don't know the capital of ${params.country}.`;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-18>)return {capitalCity: result}; // Tools must return an object
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-19>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-20>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-21>)// Create an instance of the FunctionTool
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-22>)const getCapitalCityTool = new FunctionTool({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-23>)    name: 'getCapitalCity',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-24>)    description: 'Retrieves the capital city for a given country.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-25>)    parameters: getCapitalCityParamsSchema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-26>)    execute: getCapitalCity,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-27>)});
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-28>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-29>)// Add the tool to the agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-30>)const capitalAgent = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-31>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-32>)    name: 'capitalAgent',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-33>)    description: 'Answers user questions about the capital city of a given country.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-34>)    instruction: 'You are an agent that provides the capital city of a country...', // Note: the full instruction is omitted for brevity
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-35>)    tools: [getCapitalCityTool], // Provide the FunctionTool instance in an array
    [](<https://adk.dev/agents/llm-agents/#__codelineno-11-36>)});
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-1>)// Define a tool function
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-2>)type getCapitalCityArgs struct {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-3>)    Country string `json:"country" jsonschema:"The country to get the capital of."`
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-4>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-5>)getCapitalCity := func(ctx agent.Context, args getCapitalCityArgs) (map[string]any, error) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-6>)    // Replace with actual logic (e.g., API call, database lookup)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-7>)    capitals := map[string]string{"france": "Paris", "japan": "Tokyo", "canada": "Ottawa"}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-8>)    capital, ok := capitals[strings.ToLower(args.Country)]
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-9>)    if !ok {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-10>)        return nil, fmt.Errorf("Sorry, I don't know the capital of %s.", args.Country)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-11>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-12>)    return map[string]any{"result": capital}, nil
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-13>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-14>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-15>)// Add the tool to the agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-16>)capitalTool, err := functiontool.New(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-17>)    functiontool.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-18>)        Name:        "get_capital_city",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-19>)        Description: "Retrieves the capital city for a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-20>)    },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-21>)    getCapitalCity,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-22>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-23>)if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-24>)    log.Fatal(err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-25>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-26>)agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-27>)    Name:        "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-28>)    Model:       model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-29>)    Description: "Answers user questions about the capital city of a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-30>)    Instruction: "You are an agent that provides the capital city of a country... (previous instruction text)",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-31>)    Tools:       []tool.Tool{capitalTool},
    [](<https://adk.dev/agents/llm-agents/#__codelineno-12-32>)})
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-1>)// Define a tool function
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-2>)// Retrieves the capital city of a given country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-3>)public static Map<String, Object> getCapitalCity(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-4>)        @Schema(name = "country", description = "The country to get capital for")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-5>)        String country) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-6>)  // Replace with actual logic (e.g., API call, database lookup)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-7>)  Map<String, String> countryCapitals = new HashMap<>();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-8>)  countryCapitals.put("canada", "Ottawa");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-9>)  countryCapitals.put("france", "Paris");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-10>)  countryCapitals.put("japan", "Tokyo");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-11>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-12>)  String result =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-13>)          countryCapitals.getOrDefault(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-14>)                  country.toLowerCase(), "Sorry, I couldn't find the capital for " + country + ".");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-15>)  return Map.of("result", result); // Tools must return a Map
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-16>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-17>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-18>)// Add the tool to the agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-19>)FunctionTool capitalTool = FunctionTool.create(experiment.getClass(), "getCapitalCity");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-20>)LlmAgent capitalAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-21>)    LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-22>)        .model("gemini-flash-latest")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-23>)        .name("capital_agent")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-24>)        .description("Answers user questions about the capital city of a given country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-25>)        .instruction("You are an agent that provides the capital city of a country... (previous instruction text)")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-26>)        .tools(capitalTool) // Provide the function wrapped as a FunctionTool
    [](<https://adk.dev/agents/llm-agents/#__codelineno-13-27>)        .build();
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-1>)class CapitalService {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-2>)    @Tool(description = "Retrieves the capital city for a given country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-3>)    fun getCapitalCity(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-4>)        @Param("The country to get capital for.") country: String,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-5>)    ): String {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-6>)        val capitals = mapOf("france" to "Paris", "japan" to "Tokyo", "canada" to "Ottawa")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-7>)        return capitals[country.lowercase()] ?: "Sorry, I don't know the capital of $country."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-8>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-9>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-10>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-11>)// Add the tool to the agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-12>)// Note: generatedTools() is generated by KSP for classes containing @Tool annotated functions.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-13>)// In a real project, you would need to set up the ADK KSP processor.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-14>)// val agentWithTools = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-15>)//     name = "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-16>)//     model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-17>)//     tools = capitalService.generatedTools()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-14-18>)// )
    
Learn more about Tools in [Custom Tools](<https://adk.dev/tools-custom/>).

## Advanced configuration and control[¶](<https://adk.dev/agents/llm-agents/#advanced-configuration-and-control> "Permanent link")

Beyond the core parameters, `LlmAgent` offers several options for finer control:

### Fine-tune AI model operation[¶](<https://adk.dev/agents/llm-agents/#fine-tune-ai-model-operation> "Permanent link")

You can adjust how the underlying AI model generates responses using `generate_content_config`.

  * **`generate_content_config` (Optional):** Pass an instance of [`google.genai.types.GenerateContentConfig`](<https://googleapis.github.io/python-genai/genai.html#genai.types.GenerateContentConfig>) to control parameters like `temperature` (randomness), `max_output_tokens` (response length), `top_p`, `top_k`, and safety settings.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-1>)from google.genai import types
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-3>)agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-4>)    # ... other params
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-5>)    generate_content_config=types.GenerateContentConfig(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-6>)        temperature=0.2, # More deterministic output
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-7>)        max_output_tokens=250,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-8>)        safety_settings=[
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-9>)            types.SafetySetting(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-10>)                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-11>)                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-12>)            )
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-13>)        ]
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-14>)    )
    [](<https://adk.dev/agents/llm-agents/#__codelineno-15-15>))
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-1>)import { GenerateContentConfig } from '@google/genai';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-3>)const generateContentConfig: GenerateContentConfig = {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-4>)    temperature: 0.2, // More deterministic output
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-5>)    maxOutputTokens: 250,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-6>)};
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-7>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-8>)const agent = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-9>)    // ... other params
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-10>)    generateContentConfig,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-16-11>)});
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-1>)import "google.golang.org/genai"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-3>)temperature := float32(0.2)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-4>)agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-5>)    Name:  "gen_config_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-6>)    Model: model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-7>)    GenerateContentConfig: &genai.GenerateContentConfig{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-8>)        Temperature:     &temperature,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-9>)        MaxOutputTokens: 250,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-10>)    },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-17-11>)})
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-1>)import com.google.genai.types.GenerateContentConfig;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-3>)LlmAgent agent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-4>)    LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-5>)        // ... other params
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-6>)        .generateContentConfig(GenerateContentConfig.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-7>)            .temperature(0.2F) // More deterministic output
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-8>)            .maxOutputTokens(250)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-9>)            .build())
    [](<https://adk.dev/agents/llm-agents/#__codelineno-18-10>)        .build();
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-1>)val agentWithConfig =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-2>)    LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-3>)        name = "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-4>)        model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-5>)        generateContentConfig =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-6>)            GenerateContentConfig(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-7>)                temperature = 0.2f,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-8>)                maxOutputTokens = 250,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-9>)            ),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-19-10>)    )
    
### Configure a default model[¶](<https://adk.dev/agents/llm-agents/#configure-a-default-model> "Permanent link")

Supported in ADKPython v1.22.0

You can set a system-wide default model for all `LlmAgent` instances using the `set_default_model` class method. If you do not specify a model when creating an agent, it falls back to ADK's built-in default model. This setting helps you avoid redundant model specifications and easily change the model for all agents at once.

Python
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-3>)# Set a new default model for all agents
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-4>)LlmAgent.set_default_model("gemini-flash-latest")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-5>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-6>)# This agent will now use "gemini-flash-latest" by default
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-7>)agent_with_default_model = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-8>)    name="default_model_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-9>)    instruction="You are a helpful assistant."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-10>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-11>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-12>)# You can still override the default for specific agents
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-13>)specific_agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-14>)    name="specific_model_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-15>)    model="gemini-pro-latest",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-16>)    instruction="You are a creative writer."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-20-17>))
    
### Structure data input and output[¶](<https://adk.dev/agents/llm-agents/#data-handling> "Permanent link")

For scenarios requiring structured data exchange with an `LLM Agent`, the ADK provides mechanisms to define expected input and desired output formats using schema definitions.

  * **`input_schema` (Optional):** Define a schema representing the expected input structure. If set, the user message content passed to this agent _must_ be a JSON string conforming to this schema. Your instructions should guide the user or preceding agent accordingly.

  * **`output_schema` (Optional):** Define a schema representing the desired output structure. If set, the agent's final response _must_ be a JSON string conforming to this schema.

Warning: Using `output_schema` with `tools`

Using `output_schema` with `tools` in the same LLM request is only supported by specific models, including [Gemini 3.0](<https://ai.google.dev/gemini-api/docs/function-calling?example=meeting#structured-output>). For other models, workarounds using [function tools](<https://github.com/google/adk-python/blob/main/src/google/adk/flows/llm_flows/_output_schema_processor.py>)) in ADK may not work reliably. In such cases, consider using sub-agents that handle output formatting separately.

  * **`output_key` (Optional):** Provide a string key. If set, the text content of the agent's _final_ response will be automatically saved to the session's state dictionary under this key. This is useful for passing results between agents or steps in a workflow.
    * In Python, this might look like: `session.state[output_key] = agent_response_text`
    * In Java: `session.state().put(outputKey, agentResponseText)`
    * In Golang, within a callback handler: `ctx.State().Set(output_key, agentResponseText)`

PythonTypescriptGoJava

The input and output schema is typically a `Pydantic` BaseModel.
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-1>)from pydantic import BaseModel, Field
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-3>)class CapitalOutput(BaseModel):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-4>)    capital: str = Field(description="The capital of the country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-5>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-6>)structured_capital_agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-7>)    # ... name, model, description
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-8>)    instruction="""You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {"capital": "capital_name"}""",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-9>)    output_schema=CapitalOutput, # Enforce JSON output
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-10>)    output_key="found_capital"  # Store result in state['found_capital']
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-11>)    # Cannot use tools=[get_capital_city] effectively here
    [](<https://adk.dev/agents/llm-agents/#__codelineno-21-12>))
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-1>)import {z} from 'zod';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-2>)import { Schema, Type } from '@google/genai';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-3>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-4>)// Define the schema for the output
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-5>)const CapitalOutputSchema: Schema = {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-6>)    type: Type.OBJECT,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-7>)    properties: {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-8>)        capital: {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-9>)            type: Type.STRING,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-10>)            description: 'The capital of the country.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-11>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-12>)    },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-13>)    required: ['capital'],
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-14>)};
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-15>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-16>)// Create the LlmAgent instance
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-17>)const structuredCapitalAgent = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-18>)    // ... name, model, description
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-19>)    instruction: `You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {"capital": "capital_name"}`,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-20>)    outputSchema: CapitalOutputSchema, // Enforce JSON output
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-21>)    outputKey: 'found_capital', // Store result in state['found_capital']
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-22>)    // Cannot use tools effectively here
    [](<https://adk.dev/agents/llm-agents/#__codelineno-22-23>)});
    
The input and output schema is a `google.genai.types.Schema` object.
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-1>)capitalOutput := &genai.Schema{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-2>)    Type:        genai.TypeObject,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-3>)    Description: "Schema for capital city information.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-4>)    Properties: map[string]*genai.Schema{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-5>)        "capital": {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-6>)            Type:        genai.TypeString,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-7>)            Description: "The capital city of the country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-8>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-9>)    },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-10>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-11>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-12>)agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-13>)    Name:         "structured_capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-14>)    Model:        model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-15>)    Description:  "Provides capital information in a structured format.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-16>)    Instruction:  `You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {"capital": "capital_name"}`,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-17>)    OutputSchema: capitalOutput,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-18>)    OutputKey:    "found_capital",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-19>)    // Cannot use the capitalTool tool effectively here
    [](<https://adk.dev/agents/llm-agents/#__codelineno-23-20>)})
    
The input and output schema is a `google.genai.types.Schema` object.
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-1>)private static final Schema CAPITAL_OUTPUT =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-2>)    Schema.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-3>)        .type("OBJECT")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-4>)        .description("Schema for capital city information.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-5>)        .properties(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-6>)            Map.of(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-7>)                "capital",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-8>)                Schema.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-9>)                    .type("STRING")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-10>)                    .description("The capital city of the country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-11>)                    .build()))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-12>)        .build();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-13>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-14>)LlmAgent structuredCapitalAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-15>)    LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-16>)        // ... name, model, description
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-17>)        .instruction(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-18>)                "You are a Capital Information Agent. Given a country, respond ONLY with a JSON object containing the capital. Format: {\"capital\": \"capital_name\"}")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-19>)        .outputSchema(CAPITAL_OUTPUT) // Enforce JSON output
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-20>)        .outputKey("found_capital") // Store result in state.get("found_capital")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-21>)        // Cannot use tools(getCapitalCity) effectively here
    [](<https://adk.dev/agents/llm-agents/#__codelineno-24-22>)        .build();
    
### Manage agent context[¶](<https://adk.dev/agents/llm-agents/#manage-agent-context> "Permanent link")

Control whether the agent receives the prior conversation history.

  * **`include_contents` (Optional, Default: `'default'`):** Determines if the `contents` (history) are sent to the LLM.
    * `'default'`: The agent receives the relevant conversation history.
    * `'none'`: The agent receives no prior `contents`. It operates based solely on its current instruction and any input provided in the _current_ turn (useful for stateless tasks or enforcing specific contexts).

PythonTypescriptGoJava
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-25-1>)stateless_agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-25-2>)    # ... other params
    [](<https://adk.dev/agents/llm-agents/#__codelineno-25-3>)    include_contents='none'
    [](<https://adk.dev/agents/llm-agents/#__codelineno-25-4>))
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-26-1>)const statelessAgent = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-26-2>)    // ... other params
    [](<https://adk.dev/agents/llm-agents/#__codelineno-26-3>)    includeContents: 'none',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-26-4>)});
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-27-1>)import "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-27-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-27-3>)agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-27-4>)    Name:            "stateless_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-27-5>)    Model:           model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-27-6>)    IncludeContents: llmagent.IncludeContentsNone,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-27-7>)})
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-28-1>)import com.google.adk.agents.LlmAgent.IncludeContents;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-28-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-28-3>)LlmAgent statelessAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-28-4>)    LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-28-5>)        // ... other params
    [](<https://adk.dev/agents/llm-agents/#__codelineno-28-6>)        .includeContents(IncludeContents.NONE)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-28-7>)        .build();
    
Go v2.0.0: agent execution modes

ADK Go v2.0.0 introduces an explicit `Mode` field on `llmagent.Config` that controls how the agent runs when used inside a graph-based or dynamic workflow. Three modes are available:

  * **`ModeChat`** (default for an agent used as a sub-agent): The agent participates in a multi-turn conversation with the user and is reachable from peer agents via `transfer_to_agent`.
  * **`ModeSingleTurn`** (default for an agent used as a node in a workflow): The agent completes its task in a single turn without chatting with the user.
  * **`ModeTask`** : A task agent that chats with the user to accomplish a task — in contrast to `ModeSingleTurn`, it can interact with the user across turns to complete the work.

When you wrap an `llmagent` with `workflow.NewAgentNode`, the workflow engine automatically sets the mode to `ModeSingleTurn` if no mode is specified — equivalent to Python's `mode="single_turn"` on an agent used as a workflow node. For more information on composing agents in graph-based workflows, see [Graph-based agent workflows](<https://adk.dev/graphs/>).

### Configure a planner[¶](<https://adk.dev/agents/llm-agents/#configure-a-planner> "Permanent link")

Supported in ADKPython v0.1.0

**`planner` (Optional):** Assign a `BasePlanner` instance to enable multi-step reasoning and planning before execution. There are two main planners:

  * **`BuiltInPlanner`:** Leverages the model's built-in planning capabilities (e.g., Gemini's thinking feature). See [Gemini Thinking](<https://ai.google.dev/gemini-api/docs/thinking>) for details and examples.

Here, the `thinking_budget` parameter guides the model on the number of thinking tokens to use when generating a response. The `include_thoughts` parameter controls whether the model should include its raw thoughts and internal reasoning process in the response.
        
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-1>)from google.adk import Agent
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-2>)from google.adk.planners import BuiltInPlanner
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-3>)from google.genai import types
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-4>)
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-5>)my_agent = Agent(
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-6>)    model="gemini-flash-latest",
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-7>)    planner=BuiltInPlanner(
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-8>)        thinking_config=types.ThinkingConfig(
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-9>)            include_thoughts=True,
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-10>)            thinking_budget=1024,
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-11>)        )
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-12>)    ),
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-13>)    # ... your tools here
        [](<https://adk.dev/agents/llm-agents/#__codelineno-29-14>))
        
  * **`PlanReActPlanner`:** This planner instructs the model to follow a specific structure in its output: first create a plan, then execute actions (like calling tools), and provide reasoning for its steps. _It's particularly useful for models that don't have a built-in "thinking" feature_.
        
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-1>)from google.adk import Agent
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-2>)from google.adk.planners import PlanReActPlanner
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-3>)
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-4>)my_agent = Agent(
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-5>)    model="gemini-flash-latest",
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-6>)    planner=PlanReActPlanner(),
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-7>)    # ... your tools here
        [](<https://adk.dev/agents/llm-agents/#__codelineno-30-8>))
        
The agent's response will follow a structured format:
        
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-1>)[user]: ai news
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-2>)[google_search_agent]: /*PLANNING*/
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-3>)1. Perform a Google search for "latest AI news" to get current updates and headlines related to artificial intelligence.
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-4>)2. Synthesize the information from the search results to provide a summary of recent AI news.
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-5>)
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-6>)/*ACTION*/
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-7>)/*REASONING*/
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-8>)The search results provide a comprehensive overview of recent AI news, covering various aspects like company developments, research breakthroughs, and applications. I have enough information to answer the user's request.
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-9>)
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-10>)/*FINAL_ANSWER*/
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-11>)Here's a summary of recent AI news:
        [](<https://adk.dev/agents/llm-agents/#__codelineno-31-12>)....
        
Example for using built-in-planner:
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-1>)from dotenv import load_dotenv
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-3>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-4>)import asyncio
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-5>)import os
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-6>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-7>)from google.genai import types
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-8>)from google.adk.agents.llm_agent import LlmAgent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-9>)from google.adk.runners import Runner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-10>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-11>)from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-12>)from google.adk.planners import BasePlanner, BuiltInPlanner, PlanReActPlanner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-13>)from google.adk.models import LlmRequest
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-14>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-15>)from google.genai.types import ThinkingConfig
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-16>)from google.genai.types import GenerateContentConfig
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-17>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-18>)import datetime
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-19>)from zoneinfo import ZoneInfo
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-20>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-21>)APP_NAME = "weather_app"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-22>)USER_ID = "1234"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-23>)SESSION_ID = "session1234"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-24>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-25>)def get_weather(city: str) -> dict:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-26>)    """Retrieves the current weather report for a specified city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-27>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-28>)    Args:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-29>)        city (str): The name of the city for which to retrieve the weather report.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-30>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-31>)    Returns:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-32>)        dict: status and result or error msg.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-33>)    """
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-34>)    if city.lower() == "new york":
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-35>)        return {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-36>)            "status": "success",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-37>)            "report": (
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-38>)                "The weather in New York is sunny with a temperature of 25 degrees"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-39>)                " Celsius (77 degrees Fahrenheit)."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-40>)            ),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-41>)        }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-42>)    else:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-43>)        return {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-44>)            "status": "error",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-45>)            "error_message": f"Weather information for '{city}' is not available.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-46>)        }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-47>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-48>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-49>)def get_current_time(city: str) -> dict:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-50>)    """Returns the current time in a specified city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-51>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-52>)    Args:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-53>)        city (str): The name of the city for which to retrieve the current time.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-54>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-55>)    Returns:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-56>)        dict: status and result or error msg.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-57>)    """
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-58>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-59>)    if city.lower() == "new york":
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-60>)        tz_identifier = "America/New_York"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-61>)    else:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-62>)        return {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-63>)            "status": "error",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-64>)            "error_message": (
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-65>)                f"Sorry, I don't have timezone information for {city}."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-66>)            ),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-67>)        }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-68>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-69>)    tz = ZoneInfo(tz_identifier)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-70>)    now = datetime.datetime.now(tz)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-71>)    report = (
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-72>)        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-73>)    )
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-74>)    return {"status": "success", "report": report}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-75>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-76>)# Step 1: Create a ThinkingConfig
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-77>)thinking_config = ThinkingConfig(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-78>)    include_thoughts=True,   # Ask the model to include its thoughts in the response
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-79>)    thinking_budget=256      # Limit the 'thinking' to 256 tokens (adjust as needed)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-80>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-81>)print("ThinkingConfig:", thinking_config)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-82>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-83>)# Step 2: Instantiate BuiltInPlanner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-84>)planner = BuiltInPlanner(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-85>)    thinking_config=thinking_config
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-86>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-87>)print("BuiltInPlanner created.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-88>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-89>)# Step 3: Wrap the planner in an LlmAgent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-90>)agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-91>)    model="gemini-flash-latest",  # Set your model name
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-92>)    name="weather_and_time_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-93>)    instruction="You are an agent that returns time and weather",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-94>)    planner=planner,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-95>)    tools=[get_weather, get_current_time]
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-96>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-97>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-98>)# Session and Runner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-99>)session_service = InMemorySessionService()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-100>)session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-101>)runner = Runner(agent=agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-102>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-103>)# Agent Interaction
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-104>)def call_agent(query):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-105>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-106>)    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-107>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-108>)    for event in events:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-109>)        print(f"\nDEBUG EVENT: {event}\n")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-110>)        if event.is_final_response() and event.content:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-111>)            final_answer = event.content.parts[0].text.strip()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-112>)            print("\n🟢 FINAL ANSWER\n", final_answer, "\n")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-113>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-32-114>)call_agent("If it's raining in New York right now, what is the current temperature?")
    
### Code execution[¶](<https://adk.dev/agents/llm-agents/#code-execution> "Permanent link")

Supported in ADKPython v0.1.0Java v0.1.0

  * **`code_executor` (Optional):** Provide a `BaseCodeExecutor` instance to allow the agent to execute code blocks found in the LLM's response. For more information, see [Code Execution with Gemini API](<https://adk.dev/integrations/code-execution/>).

PythonJava
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-2>)#
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-6>)#
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-8>)#
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-13>)# limitations under the License.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-14>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-15>)import asyncio
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-16>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-17>)from google.adk.runners import Runner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-18>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-19>)from google.adk.code_executors import BuiltInCodeExecutor
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-20>)from google.genai import types
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-21>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-22>)AGENT_NAME = "calculator_agent"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-23>)APP_NAME = "calculator"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-24>)USER_ID = "user1234"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-25>)SESSION_ID = "session_code_exec_async"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-26>)GEMINI_MODEL = "gemini-2.0-flash"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-27>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-28>)# Agent Definition
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-29>)code_agent = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-30>)    name=AGENT_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-31>)    model=GEMINI_MODEL,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-32>)    code_executor=BuiltInCodeExecutor(),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-33>)    instruction="""You are a calculator agent.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-34>)    When given a mathematical expression, write and execute Python code to calculate the result.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-35>)    Return only the final numerical result as plain text, without markdown or code blocks.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-36>)    """,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-37>)    description="Executes Python code to perform calculations.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-38>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-39>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-40>)# Session and Runner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-41>)session_service = InMemorySessionService()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-42>)session = asyncio.run(session_service.create_session(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-43>)    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-44>)))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-45>)runner = Runner(agent=code_agent, app_name=APP_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-46>)                session_service=session_service)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-47>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-48>)# Agent Interaction (Async)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-49>)async def call_agent_async(query):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-50>)    content = types.Content(role="user", parts=[types.Part(text=query)])
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-51>)    print(f"\n--- Running Query: {query} ---")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-52>)    final_response_text = "No final text response captured."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-53>)    try:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-54>)        # Use run_async
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-55>)        async for event in runner.run_async(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-56>)            user_id=USER_ID, session_id=SESSION_ID, new_message=content
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-57>)        ):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-58>)            print(f"Event ID: {event.id}, Author: {event.author}")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-59>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-60>)            # --- Check for specific parts FIRST ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-61>)            has_specific_part = False
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-62>)            if event.content and event.content.parts:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-63>)                for part in event.content.parts:  # Iterate through all parts
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-64>)                    if part.executable_code:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-65>)                        # Access the actual code string via .code
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-66>)                        print(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-67>)                            f"  Debug: Agent generated code:\n```python\n{part.executable_code.code}\n```"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-68>)                        )
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-69>)                        has_specific_part = True
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-70>)                    elif part.code_execution_result:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-71>)                        # Access outcome and output correctly
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-72>)                        print(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-73>)                            f"  Debug: Code Execution Result: {part.code_execution_result.outcome} - Output:\n{part.code_execution_result.output}"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-74>)                        )
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-75>)                        has_specific_part = True
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-76>)                    # Also print any text parts found in any event for debugging
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-77>)                    elif part.text and not part.text.isspace():
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-78>)                        print(f"  Text: '{part.text.strip()}'")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-79>)                        # Do not set has_specific_part=True here, as we want the final response logic below
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-80>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-81>)            # --- Check for final response AFTER specific parts ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-82>)            # Only consider it final if it doesn't have the specific code parts we just handled
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-83>)            if not has_specific_part and event.is_final_response():
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-84>)                if (
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-85>)                    event.content
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-86>)                    and event.content.parts
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-87>)                    and event.content.parts[0].text
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-88>)                ):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-89>)                    final_response_text = event.content.parts[0].text.strip()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-90>)                    print(f"==> Final Agent Response: {final_response_text}")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-91>)                else:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-92>)                    print(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-93>)                        "==> Final Agent Response: [No text content in final event]")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-94>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-95>)    except Exception as e:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-96>)        print(f"ERROR during agent run: {e}")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-97>)    print("-" * 30)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-98>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-99>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-100>)# Main async function to run the examples
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-101>)async def main():
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-102>)    await call_agent_async("Calculate the value of (5 + 7) * 3")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-103>)    await call_agent_async("What is 10 factorial?")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-104>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-105>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-106>)# Execute the main async function
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-107>)try:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-108>)    asyncio.run(main())
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-109>)except RuntimeError as e:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-110>)    # Handle specific error when running asyncio.run in an already running loop (like Jupyter/Colab)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-111>)    if "cannot be called from a running event loop" in str(e):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-112>)        print("\nRunning in an existing event loop (like Colab/Jupyter).")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-113>)        print("Please run `await main()` in a notebook cell instead.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-114>)        # If in an interactive environment like a notebook, you might need to run:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-115>)        # await main()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-116>)    else:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-33-117>)        raise e  # Re-raise other runtime errors
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-1>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-3>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-4>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-5>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-6>)import com.google.adk.tools.BuiltInCodeExecutionTool;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-7>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-8>)import com.google.genai.types.Content;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-9>)import com.google.genai.types.Part;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-10>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-11>)public class CodeExecutionAgentApp {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-12>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-13>)  private static final String AGENT_NAME = "calculator_agent";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-14>)  private static final String APP_NAME = "calculator";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-15>)  private static final String USER_ID = "user1234";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-16>)  private static final String SESSION_ID = "session_code_exec_sync";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-17>)  private static final String GEMINI_MODEL = "gemini-2.0-flash";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-18>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-19>)  /**
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-20>)   * Calls the agent with a query and prints the interaction events and final response.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-21>)   *
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-22>)   * @param runner The runner instance for the agent.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-23>)   * @param query The query to send to the agent.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-24>)   */
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-25>)  public static void callAgent(Runner runner, String query) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-26>)    Content content =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-27>)        Content.builder().role("user").parts(ImmutableList.of(Part.fromText(query))).build();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-28>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-29>)    InMemorySessionService sessionService = (InMemorySessionService) runner.sessionService();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-30>)    Session session =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-31>)        sessionService
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-32>)            .createSession(APP_NAME, USER_ID, /* state= */ null, SESSION_ID)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-33>)            .blockingGet();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-34>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-35>)    System.out.println("\n--- Running Query: " + query + " ---");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-36>)    final String[] finalResponseText = {"No final text response captured."};
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-37>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-38>)    try {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-39>)      runner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-40>)          .runAsync(session.userId(), session.id(), content)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-41>)          .forEach(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-42>)              event -> {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-43>)                System.out.println("Event ID: " + event.id() + ", Author: " + event.author());
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-44>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-45>)                boolean hasSpecificPart = false;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-46>)                if (event.content().isPresent() && event.content().get().parts().isPresent()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-47>)                  for (Part part : event.content().get().parts().get()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-48>)                    if (part.executableCode().isPresent()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-49>)                      System.out.println(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-50>)                          "  Debug: Agent generated code:\n```python\n"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-51>)                              + part.executableCode().get().code()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-52>)                              + "\n```");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-53>)                      hasSpecificPart = true;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-54>)                    } else if (part.codeExecutionResult().isPresent()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-55>)                      System.out.println(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-56>)                          "  Debug: Code Execution Result: "
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-57>)                              + part.codeExecutionResult().get().outcome()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-58>)                              + " - Output:\n"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-59>)                              + part.codeExecutionResult().get().output());
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-60>)                      hasSpecificPart = true;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-61>)                    } else if (part.text().isPresent() && !part.text().get().trim().isEmpty()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-62>)                      System.out.println("  Text: '" + part.text().get().trim() + "'");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-63>)                    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-64>)                  }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-65>)                }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-66>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-67>)                if (!hasSpecificPart && event.finalResponse()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-68>)                  if (event.content().isPresent()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-69>)                      && event.content().get().parts().isPresent()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-70>)                      && !event.content().get().parts().get().isEmpty()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-71>)                      && event.content().get().parts().get().get(0).text().isPresent()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-72>)                    finalResponseText[0] =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-73>)                        event.content().get().parts().get().get(0).text().get().trim();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-74>)                    System.out.println("==> Final Agent Response: " + finalResponseText[0]);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-75>)                  } else {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-76>)                    System.out.println(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-77>)                        "==> Final Agent Response: [No text content in final event]");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-78>)                  }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-79>)                }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-80>)              });
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-81>)    } catch (Exception e) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-82>)      System.err.println("ERROR during agent run: " + e.getMessage());
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-83>)      e.printStackTrace();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-84>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-85>)    System.out.println("------------------------------");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-86>)  }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-87>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-88>)  public static void main(String[] args) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-89>)    BuiltInCodeExecutionTool codeExecutionTool = new BuiltInCodeExecutionTool();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-90>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-91>)    BaseAgent codeAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-92>)        LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-93>)            .name(AGENT_NAME)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-94>)            .model(GEMINI_MODEL)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-95>)            .tools(ImmutableList.of(codeExecutionTool))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-96>)            .instruction(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-97>)                """
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-98>)                                You are a calculator agent.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-99>)                                When given a mathematical expression, write and execute Python code to calculate the result.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-100>)                                Return only the final numerical result as plain text, without markdown or code blocks.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-101>)                                """)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-102>)            .description("Executes Python code to perform calculations.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-103>)            .build();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-104>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-105>)    InMemorySessionService sessionService = new InMemorySessionService();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-106>)    Runner runner = new Runner(codeAgent, APP_NAME, null, sessionService);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-107>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-108>)    callAgent(runner, "Calculate the value of (5 + 7) * 3");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-109>)    callAgent(runner, "What is 10 factorial?");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-110>)  }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-34-111>)}
    
## Code example[¶](<https://adk.dev/agents/llm-agents/#code-example> "Permanent link")

This following example demonstrates the core concepts discussed in this page. More complex agents might incorporate schemas, context control, and planning.

Code

Here's the complete basic `capital_agent`:

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-2>)#
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-6>)#
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-8>)#
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-13>)# limitations under the License.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-14>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-15>)# --- Full example code demonstrating LlmAgent with Tools vs. Output Schema ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-16>)import json # Needed for pretty printing dicts
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-17>)import asyncio 
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-18>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-19>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-20>)from google.adk.runners import Runner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-21>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-22>)from google.genai import types
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-23>)from pydantic import BaseModel, Field
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-24>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-25>)# --- 1. Define Constants ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-26>)APP_NAME = "agent_comparison_app"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-27>)USER_ID = "test_user_456"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-28>)SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-29>)SESSION_ID_SCHEMA_AGENT = "session_schema_agent_xyz"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-30>)MODEL_NAME = "gemini-2.0-flash"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-31>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-32>)# --- 2. Define Schemas ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-33>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-34>)# Input schema used by both agents
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-35>)class CountryInput(BaseModel):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-36>)    country: str = Field(description="The country to get information about.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-37>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-38>)# Output schema ONLY for the second agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-39>)class CapitalInfoOutput(BaseModel):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-40>)    capital: str = Field(description="The capital city of the country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-41>)    # Note: Population is illustrative; the LLM will infer or estimate this
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-42>)    # as it cannot use tools when output_schema is set.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-43>)    population_estimate: str = Field(description="An estimated population of the capital city.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-44>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-45>)# --- 3. Define the Tool (Only for the first agent) ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-46>)def get_capital_city(country: str) -> str:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-47>)    """Retrieves the capital city of a given country."""
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-48>)    print(f"\n-- Tool Call: get_capital_city(country='{country}') --")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-49>)    country_capitals = {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-50>)        "united states": "Washington, D.C.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-51>)        "canada": "Ottawa",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-52>)        "france": "Paris",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-53>)        "japan": "Tokyo",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-54>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-55>)    result = country_capitals.get(country.lower(), f"Sorry, I couldn't find the capital for {country}.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-56>)    print(f"-- Tool Result: '{result}' --")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-57>)    return result
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-58>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-59>)# --- 4. Configure Agents ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-60>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-61>)# Agent 1: Uses a tool and output_key
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-62>)capital_agent_with_tool = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-63>)    model=MODEL_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-64>)    name="capital_agent_tool",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-65>)    description="Retrieves the capital city using a specific tool.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-66>)    instruction="""You are a helpful agent that provides the capital city of a country using a tool.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-67>)The user will provide the country name in a JSON format like {"country": "country_name"}.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-68>)1. Extract the country name.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-69>)2. Use the `get_capital_city` tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-70>)3. Respond clearly to the user, stating the capital city found by the tool.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-71>)""",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-72>)    tools=[get_capital_city],
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-73>)    input_schema=CountryInput,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-74>)    output_key="capital_tool_result", # Store final text response
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-75>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-76>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-77>)# Agent 2: Uses output_schema (NO tools possible)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-78>)structured_info_agent_schema = LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-79>)    model=MODEL_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-80>)    name="structured_info_agent_schema",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-81>)    description="Provides capital and estimated population in a specific JSON format.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-82>)    instruction=f"""You are an agent that provides country information.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-83>)The user will provide the country name in a JSON format like {{"country": "country_name"}}.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-84>)Respond ONLY with a JSON object matching this exact schema:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-85>){json.dumps(CapitalInfoOutput.model_json_schema(), indent=2)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-86>)Use your knowledge to determine the capital and estimate the population. Do not use any tools.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-87>)""",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-88>)    # *** NO tools parameter here - using output_schema prevents tool use ***
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-89>)    input_schema=CountryInput,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-90>)    output_schema=CapitalInfoOutput, # Enforce JSON output structure
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-91>)    output_key="structured_info_result", # Store final JSON response
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-92>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-93>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-94>)# --- 5. Set up Session Management and Runners ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-95>)session_service = InMemorySessionService()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-96>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-97>)# Create a runner for EACH agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-98>)capital_runner = Runner(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-99>)    agent=capital_agent_with_tool,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-100>)    app_name=APP_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-101>)    session_service=session_service
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-102>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-103>)structured_runner = Runner(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-104>)    agent=structured_info_agent_schema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-105>)    app_name=APP_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-106>)    session_service=session_service
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-107>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-108>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-109>)# --- 6. Define Agent Interaction Logic ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-110>)async def call_agent_and_print(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-111>)    runner_instance: Runner,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-112>)    agent_instance: LlmAgent,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-113>)    session_id: str,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-114>)    query_json: str
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-115>)):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-116>)    """Sends a query to the specified agent/runner and prints results."""
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-117>)    print(f"\n>>> Calling Agent: '{agent_instance.name}' | Query: {query_json}")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-118>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-119>)    user_content = types.Content(role='user', parts=[types.Part(text=query_json)])
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-120>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-121>)    final_response_content = "No final response received."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-122>)    async for event in runner_instance.run_async(user_id=USER_ID, session_id=session_id, new_message=user_content):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-123>)        # print(f"Event: {event.type}, Author: {event.author}") # Uncomment for detailed logging
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-124>)        if event.is_final_response() and event.content and event.content.parts:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-125>)            # For output_schema, the content is the JSON string itself
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-126>)            final_response_content = event.content.parts[0].text
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-127>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-128>)    print(f"<<< Agent '{agent_instance.name}' Response: {final_response_content}")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-129>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-130>)    current_session = await session_service.get_session(app_name=APP_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-131>)                                                  user_id=USER_ID,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-132>)                                                  session_id=session_id)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-133>)    stored_output = current_session.state.get(agent_instance.output_key)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-134>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-135>)    # Pretty print if the stored output looks like JSON (likely from output_schema)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-136>)    print(f"--- Session State ['{agent_instance.output_key}']: ", end="")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-137>)    try:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-138>)        # Attempt to parse and pretty print if it's JSON
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-139>)        parsed_output = json.loads(stored_output)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-140>)        print(json.dumps(parsed_output, indent=2))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-141>)    except (json.JSONDecodeError, TypeError):
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-142>)         # Otherwise, print as string
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-143>)        print(stored_output)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-144>)    print("-" * 30)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-145>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-146>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-147>)# --- 7. Run Interactions ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-148>)async def main():
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-149>)    # Create separate sessions for clarity, though not strictly necessary if context is managed
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-150>)    print("--- Creating Sessions ---")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-151>)    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_TOOL_AGENT)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-152>)    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID_SCHEMA_AGENT)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-153>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-154>)    print("--- Testing Agent with Tool ---")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-155>)    await call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "France"}')
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-156>)    await call_agent_and_print(capital_runner, capital_agent_with_tool, SESSION_ID_TOOL_AGENT, '{"country": "Canada"}')
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-157>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-158>)    print("\n\n--- Testing Agent with Output Schema (No Tool Use) ---")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-159>)    await call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "France"}')
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-160>)    await call_agent_and_print(structured_runner, structured_info_agent_schema, SESSION_ID_SCHEMA_AGENT, '{"country": "Japan"}')
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-161>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-162>)# --- Run the Agent ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-163>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-164>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-165>)if __name__ == "__main__":
    [](<https://adk.dev/agents/llm-agents/#__codelineno-35-166>)    asyncio.run(main())    
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-1>)// Copyright 2025 Google LLC
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-2>)//
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-3>)// Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-4>)// you may not use this file except in compliance with the License.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-5>)// You may obtain a copy of the License at
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-6>)//
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-7>)//     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-8>)//
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-9>)// Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-10>)// distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-11>)// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-12>)// See the License for the specific language governing permissions and
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-13>)// limitations under the License.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-14>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-15>)import { LlmAgent, FunctionTool, InMemoryRunner, isFinalResponse } from '@google/adk';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-16>)import { createUserContent, Schema, Type } from '@google/genai';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-17>)import type { Part } from '@google/genai';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-18>) import { z } from 'zod';
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-19>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-20>)// --- 1. Define Constants ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-21>)const APP_NAME = "capital_app_ts";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-22>)const USER_ID = "test_user_789";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-23>)const SESSION_ID_TOOL_AGENT = "session_tool_agent_ts";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-24>)const SESSION_ID_SCHEMA_AGENT = "session_schema_agent_ts";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-25>)const MODEL_NAME = "gemini-2.5-flash"; // Using flash for speed
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-26>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-27>)// --- 2. Define Schemas ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-28>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-29>)// A. Schema for the Tool's parameters (using Zod)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-30>)const CountryInput = z.object({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-31>)    country: z.string().describe('The country to get the capital for.'),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-32>)});
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-33>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-34>)// B. Output schema ONLY for the second agent (using ADK's Schema type)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-35>)const CapitalInfoOutputSchema: Schema = {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-36>)    type: Type.OBJECT,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-37>)    description: "Schema for capital city information.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-38>)    properties: {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-39>)        capital: {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-40>)            type: Type.STRING,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-41>)            description: "The capital city of the country."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-42>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-43>)        population_estimate: {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-44>)            type: Type.STRING,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-45>)            description: "An estimated population of the capital city."
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-46>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-47>)    },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-48>)    required: ["capital", "population_estimate"],
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-49>)};
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-50>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-51>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-52>)// --- 3. Define the Tool (Only for the first agent) ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-53>)async function getCapitalCity(params: z.infer<typeof CountryInput>): Promise<{ result: string }> {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-54>)    console.log(`\n-- Tool Call: getCapitalCity(country='${params.country}') --`);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-55>)    const capitals: Record<string, string> = {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-56>)        'united states': 'Washington, D.C.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-57>)        'canada': 'Ottawa',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-58>)        'france': 'Paris',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-59>)        'japan': 'Tokyo',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-60>)    };
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-61>)    const result = capitals[params.country.toLowerCase()] ??
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-62>)        `Sorry, I couldn't find the capital for ${params.country}.`;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-63>)    console.log(`-- Tool Result: '${result}' --`);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-64>)    return { result: result }; // Tools must return an object
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-65>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-66>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-67>)// --- 4. Configure Agents ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-68>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-69>)// Agent 1: Uses a tool and outputKey
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-70>)const getCapitalCityTool = new FunctionTool({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-71>)    name: 'get_capital_city',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-72>)    description: 'Retrieves the capital city for a given country',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-73>)    parameters: CountryInput,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-74>)    execute: getCapitalCity,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-75>)});
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-76>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-77>)const capitalAgentWithTool = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-78>)    model: MODEL_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-79>)    name: 'capital_agent_tool',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-80>)    description: 'Retrieves the capital city using a specific tool.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-81>)    instruction: `You are a helpful agent that provides the capital city of a country using a tool.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-82>)The user will provide the country name in a JSON format like {"country": "country_name"}.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-83>)1. Extract the country name.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-84>)2. Use the \`get_capital_city\` tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-85>)3. Respond with a JSON object with the key 'capital' and the value as the capital city.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-86>)`,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-87>)    tools: [getCapitalCityTool],
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-88>)    outputKey: "capital_tool_result", // Store final text response
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-89>)});
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-90>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-91>)// Agent 2: Uses outputSchema (NO tools possible)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-92>)const structuredInfoAgentSchema = new LlmAgent({
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-93>)    model: MODEL_NAME,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-94>)    name: 'structured_info_agent_schema',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-95>)    description: 'Provides capital and estimated population in a specific JSON format.',
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-96>)    instruction: `You are an agent that provides country information.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-97>)The user will provide the country name in a JSON format like {"country": "country_name"}.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-98>)Respond ONLY with a JSON object matching this exact schema:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-99>)${JSON.stringify(CapitalInfoOutputSchema, null, 2)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-100>)Use your knowledge to determine the capital and estimate the population. Do not use any tools.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-101>)`,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-102>)    // *** NO tools parameter here - using outputSchema prevents tool use ***
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-103>)    outputSchema: CapitalInfoOutputSchema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-104>)    outputKey: "structured_info_result",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-105>)});
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-106>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-107>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-108>)// --- 5. Define Agent Interaction Logic ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-109>)async function callAgentAndPrint(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-110>)    runner: InMemoryRunner,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-111>)    agent: LlmAgent,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-112>)    sessionId: string,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-113>)    queryJson: string
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-114>)) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-115>)    console.log(`\n>>> Calling Agent: '${agent.name}' | Query: ${queryJson}`);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-116>)    const message = createUserContent(queryJson);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-117>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-118>)    let finalResponseContent = "No final response received.";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-119>)    for await (const event of runner.runAsync({ userId: USER_ID, sessionId: sessionId, newMessage: message })) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-120>)        if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-121>)            finalResponseContent = event.content.parts.map((part: Part) => part.text ?? '').join('');
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-122>)        }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-123>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-124>)    console.log(`<<< Agent '${agent.name}' Response: ${finalResponseContent}`);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-125>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-126>)    // Check the session state
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-127>)    const currentSession = await runner.sessionService.getSession({ appName: APP_NAME, userId: USER_ID, sessionId: sessionId });
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-128>)    if (!currentSession) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-129>)        console.log(`--- Session not found: ${sessionId} ---`);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-130>)        return;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-131>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-132>)    const storedOutput = currentSession.state[agent.outputKey!];
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-133>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-134>)    console.log(`--- Session State ['${agent.outputKey}']: `);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-135>)    try {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-136>)        // Attempt to parse and pretty print if it's JSON
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-137>)        const parsedOutput = JSON.parse(storedOutput as string);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-138>)        console.log(JSON.stringify(parsedOutput, null, 2));
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-139>)    } catch (e) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-140>)        // Otherwise, print as a string
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-141>)        console.log(storedOutput);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-142>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-143>)    console.log("-".repeat(30));
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-144>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-145>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-146>)// --- 6. Run Interactions ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-147>)async function main() {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-148>)    // Set up runners for each agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-149>)    const capitalRunner = new InMemoryRunner({ appName: APP_NAME, agent: capitalAgentWithTool });
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-150>)    const structuredRunner = new InMemoryRunner({ appName: APP_NAME, agent: structuredInfoAgentSchema });
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-151>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-152>)    // Create sessions
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-153>)    console.log("--- Creating Sessions ---");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-154>)    await capitalRunner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_TOOL_AGENT });
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-155>)    await structuredRunner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: SESSION_ID_SCHEMA_AGENT });
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-156>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-157>)    console.log("\n--- Testing Agent with Tool ---");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-158>)    await callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, '{"country": "France"}');
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-159>)    await callAgentAndPrint(capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, '{"country": "Canada"}');
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-160>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-161>)    console.log("\n\n--- Testing Agent with Output Schema (No Tool Use) ---");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-162>)    await callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, '{"country": "France"}');
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-163>)    await callAgentAndPrint(structuredRunner, structuredInfoAgentSchema, SESSION_ID_SCHEMA_AGENT, '{"country": "Japan"}');
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-164>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-165>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-36-166>)main();
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-1>)package main
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-3>)import (
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-4>)    "context"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-5>)    "encoding/json"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-6>)    "errors"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-7>)    "fmt"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-8>)    "log"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-9>)    "strings"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-10>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-11>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-12>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-13>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-14>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-15>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-16>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-17>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-18>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-19>)    "google.golang.org/genai"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-20>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-21>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-22>)// --- Main Runnable Example ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-23>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-24>)const (
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-25>)    modelName = "gemini-flash-latest"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-26>)    appName   = "agent_comparison_app"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-27>)    userID    = "test_user_456"
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-28>))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-29>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-30>)type getCapitalCityArgs struct {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-31>)    Country string `json:"country" jsonschema:"The country to get the capital of."`
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-32>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-33>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-34>)// getCapitalCity retrieves the capital city of a given country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-35>)func getCapitalCity(ctx agent.Context, args getCapitalCityArgs) (map[string]any, error) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-36>)    fmt.Printf("\n-- Tool Call: getCapitalCity(country='%s') --\n", args.Country)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-37>)    capitals := map[string]string{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-38>)        "united states": "Washington, D.C.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-39>)        "canada":        "Ottawa",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-40>)        "france":        "Paris",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-41>)        "japan":         "Tokyo",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-42>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-43>)    capital, ok := capitals[strings.ToLower(args.Country)]
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-44>)    if !ok {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-45>)        result := fmt.Sprintf("Sorry, I couldn't find the capital for %s.", args.Country)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-46>)        fmt.Printf("-- Tool Result: '%s' --\n", result)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-47>)        return nil, errors.New(result)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-48>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-49>)    fmt.Printf("-- Tool Result: '%s' --\n", capital)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-50>)    return map[string]any{"result": capital}, nil
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-51>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-52>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-53>)// callAgent is a helper function to execute an agent with a given prompt and handle its output.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-54>)func callAgent(ctx context.Context, a agent.Agent, outputKey string, prompt string) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-55>)    fmt.Printf("\n>>> Calling Agent: '%s' | Query: %s\n", a.Name(), prompt)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-56>)    // Create an in-memory session service to manage agent state.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-57>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-58>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-59>)    // Create a new session for the agent interaction.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-60>)    sessionCreateResponse, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-61>)        AppName: appName,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-62>)        UserID:  userID,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-63>)    })
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-64>)    if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-65>)        log.Fatalf("Failed to create the session service: %v", err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-66>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-67>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-68>)    session := sessionCreateResponse.Session
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-69>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-70>)    // Configure the runner with the application name, agent, and session service.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-71>)    config := runner.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-72>)        AppName:        appName,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-73>)        Agent:          a,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-74>)        SessionService: sessionService,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-75>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-76>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-77>)    // Create a new runner instance.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-78>)    r, err := runner.New(config)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-79>)    if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-80>)        log.Fatalf("Failed to create the runner: %v", err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-81>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-82>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-83>)    // Prepare the user's message to send to the agent.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-84>)    sessionID := session.ID()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-85>)    userMsg := &genai.Content{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-86>)        Parts: []*genai.Part{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-87>)            genai.NewPartFromText(prompt),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-88>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-89>)        Role: string(genai.RoleUser),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-90>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-91>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-92>)    // Run the agent and process the streaming events.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-93>)    for event, err := range r.Run(ctx, userID, sessionID, userMsg, agent.RunConfig{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-94>)        StreamingMode: agent.StreamingModeSSE,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-95>)    }) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-96>)        if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-97>)            fmt.Printf("\nAGENT_ERROR: %v\n", err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-98>)        } else if event.Partial {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-99>)            // Print partial responses as they are received.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-100>)            for _, p := range event.Content.Parts {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-101>)                fmt.Print(p.Text)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-102>)            }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-103>)        }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-104>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-105>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-106>)    // After the run, check if there's an expected output key in the session state.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-107>)    if outputKey != "" {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-108>)        storedOutput, error := session.State().Get(outputKey)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-109>)        if error == nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-110>)            // Pretty-print the stored output if it's a JSON string.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-111>)            fmt.Printf("\n--- Session State ['%s']: ", outputKey)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-112>)            storedString, isString := storedOutput.(string)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-113>)            if isString {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-114>)                var prettyJSON map[string]interface{}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-115>)                if err := json.Unmarshal([]byte(storedString), &prettyJSON); err == nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-116>)                    indentedJSON, err := json.MarshalIndent(prettyJSON, "", "  ")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-117>)                    if err == nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-118>)                        fmt.Println(string(indentedJSON))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-119>)                    } else {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-120>)                        fmt.Println(storedString)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-121>)                    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-122>)                } else {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-123>)                    fmt.Println(storedString)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-124>)                }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-125>)            } else {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-126>)                fmt.Println(storedOutput)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-127>)            }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-128>)            fmt.Println(strings.Repeat("-", 30))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-129>)        }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-130>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-131>)}
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-132>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-133>)func main() {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-134>)    ctx := context.Background()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-135>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-136>)    model, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-137>)    if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-138>)        log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-139>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-140>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-141>)    capitalTool, err := functiontool.New(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-142>)        functiontool.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-143>)            Name:        "get_capital_city",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-144>)            Description: "Retrieves the capital city for a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-145>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-146>)        getCapitalCity,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-147>)    )
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-148>)    if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-149>)        log.Fatalf("Failed to create function tool: %v", err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-150>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-151>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-152>)    countryInputSchema := &genai.Schema{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-153>)        Type:        genai.TypeObject,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-154>)        Description: "Input for specifying a country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-155>)        Properties: map[string]*genai.Schema{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-156>)            "country": {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-157>)                Type:        genai.TypeString,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-158>)                Description: "The country to get information about.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-159>)            },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-160>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-161>)        Required: []string{"country"},
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-162>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-163>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-164>)    capitalAgentWithTool, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-165>)        Name:        "capital_agent_tool",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-166>)        Model:       model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-167>)        Description: "Retrieves the capital city using a specific tool.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-168>)        Instruction: `You are a helpful agent that provides the capital city of a country using a tool.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-169>)The user will provide the country name in a JSON format like {"country": "country_name"}.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-170>)1. Extract the country name.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-171>)2. Use the 'get_capital_city' tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-172>)3. Respond clearly to the user, stating the capital city found by the tool.`,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-173>)        Tools:       []tool.Tool{capitalTool},
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-174>)        InputSchema: countryInputSchema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-175>)        OutputKey:   "capital_tool_result",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-176>)    })
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-177>)    if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-178>)        log.Fatalf("Failed to create capital agent with tool: %v", err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-179>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-180>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-181>)    capitalInfoOutputSchema := &genai.Schema{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-182>)        Type:        genai.TypeObject,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-183>)        Description: "Schema for capital city information.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-184>)        Properties: map[string]*genai.Schema{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-185>)            "capital": {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-186>)                Type:        genai.TypeString,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-187>)                Description: "The capital city of the country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-188>)            },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-189>)            "population_estimate": {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-190>)                Type:        genai.TypeString,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-191>)                Description: "An estimated population of the capital city.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-192>)            },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-193>)        },
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-194>)        Required: []string{"capital", "population_estimate"},
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-195>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-196>)    schemaJSON, _ := json.Marshal(capitalInfoOutputSchema)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-197>)    structuredInfoAgentSchema, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-198>)        Name:        "structured_info_agent_schema",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-199>)        Model:       model,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-200>)        Description: "Provides capital and estimated population in a specific JSON format.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-201>)        Instruction: fmt.Sprintf(`You are an agent that provides country information.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-202>)The user will provide the country name in a JSON format like {"country": "country_name"}.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-203>)Respond ONLY with a JSON object matching this exact schema:
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-204>)%s
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-205>)Use your knowledge to determine the capital and estimate the population. Do not use any tools.`, string(schemaJSON)),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-206>)        InputSchema:  countryInputSchema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-207>)        OutputSchema: capitalInfoOutputSchema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-208>)        OutputKey:    "structured_info_result",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-209>)    })
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-210>)    if err != nil {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-211>)        log.Fatalf("Failed to create structured info agent: %v", err)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-212>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-213>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-214>)    fmt.Println("--- Testing Agent with Tool ---")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-215>)    callAgent(ctx, capitalAgentWithTool, "capital_tool_result", `{"country": "France"}`)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-216>)    callAgent(ctx, capitalAgentWithTool, "capital_tool_result", `{"country": "Canada"}`)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-217>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-218>)    fmt.Println("\n\n--- Testing Agent with Output Schema (No Tool Use) ---")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-219>)    callAgent(ctx, structuredInfoAgentSchema, "structured_info_result", `{"country": "France"}`)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-220>)    callAgent(ctx, structuredInfoAgentSchema, "structured_info_result", `{"country": "Japan"}`)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-37-221>)}
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-1>)// --- Full example code demonstrating LlmAgent with Tools vs. Output Schema ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-2>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-4>)import com.google.adk.events.Event;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-5>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-6>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-7>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-8>)import com.google.adk.tools.Annotations;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-9>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-10>)import com.google.genai.types.Content;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-11>)import com.google.genai.types.Part;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-12>)import com.google.genai.types.Schema;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-13>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-14>)import java.util.HashMap;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-15>)import java.util.List;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-16>)import java.util.Map;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-17>)import java.util.Optional;
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-18>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-19>)public class LlmAgentExample {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-20>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-21>)  // --- 1. Define Constants ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-22>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-23>)  private static final String APP_NAME = "capital_agent_tool";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-24>)  private static final String USER_ID = "test_user_456";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-25>)  private static final String SESSION_ID_TOOL_AGENT = "session_tool_agent_xyz";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-26>)  private static final String SESSION_ID_SCHEMA_AGENT = "session_schema_agent_xyz";
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-27>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-28>)  // --- 2. Define Schemas ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-29>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-30>)  // Input schema used by both agents
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-31>)  private static final Schema COUNTRY_INPUT_SCHEMA =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-32>)      Schema.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-33>)          .type("OBJECT")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-34>)          .description("Input for specifying a country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-35>)          .properties(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-36>)              Map.of(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-37>)                  "country",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-38>)                  Schema.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-39>)                      .type("STRING")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-40>)                      .description("The country to get information about.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-41>)                      .build()))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-42>)          .required(List.of("country"))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-43>)          .build();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-44>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-45>)  // Output schema ONLY for the second agent
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-46>)  private static final Schema CAPITAL_INFO_OUTPUT_SCHEMA =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-47>)      Schema.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-48>)          .type("OBJECT")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-49>)          .description("Schema for capital city information.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-50>)          .properties(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-51>)              Map.of(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-52>)                  "capital",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-53>)                  Schema.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-54>)                      .type("STRING")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-55>)                      .description("The capital city of the country.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-56>)                      .build(),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-57>)                  "population_estimate",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-58>)                  Schema.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-59>)                      .type("STRING")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-60>)                      .description("An estimated population of the capital city.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-61>)                      .build()))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-62>)          .required(List.of("capital", "population_estimate"))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-63>)          .build();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-64>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-65>)  // --- 3. Define the Tool (Only for the first agent) ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-66>)  // Retrieves the capital city of a given country.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-67>)  public static Map<String, Object> getCapitalCity(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-68>)      @Annotations.Schema(name = "country", description = "The country to get capital for")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-69>)      String country) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-70>)    System.out.printf("%n-- Tool Call: getCapitalCity(country='%s') --%n", country);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-71>)    Map<String, String> countryCapitals = new HashMap<>();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-72>)    countryCapitals.put("united states", "Washington, D.C.");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-73>)    countryCapitals.put("canada", "Ottawa");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-74>)    countryCapitals.put("france", "Paris");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-75>)    countryCapitals.put("japan", "Tokyo");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-76>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-77>)    String result =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-78>)        countryCapitals.getOrDefault(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-79>)            country.toLowerCase(), "Sorry, I couldn't find the capital for " + country + ".");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-80>)    System.out.printf("-- Tool Result: '%s' --%n", result);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-81>)    return Map.of("result", result); // Tools must return a Map
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-82>)  }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-83>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-84>)  public static void main(String[] args){
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-85>)    LlmAgentExample agentExample = new LlmAgentExample();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-86>)    FunctionTool capitalTool = FunctionTool.create(agentExample.getClass(), "getCapitalCity");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-87>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-88>)    // --- 4. Configure Agents ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-89>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-90>)    // Agent 1: Uses a tool and output_key
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-91>)    LlmAgent capitalAgentWithTool =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-92>)        LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-93>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-94>)            .name("capital_agent_tool")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-95>)            .description("Retrieves the capital city using a specific tool.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-96>)            .instruction(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-97>)              """
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-98>)              You are a helpful agent that provides the capital city of a country using a tool.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-99>)              1. Extract the country name.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-100>)              2. Use the `get_capital_city` tool to find the capital.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-101>)              3. Respond clearly to the user, stating the capital city found by the tool.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-102>)              """)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-103>)            .tools(capitalTool)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-104>)            .inputSchema(COUNTRY_INPUT_SCHEMA)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-105>)            .outputKey("capital_tool_result") // Store final text response
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-106>)            .build();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-107>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-108>)    // Agent 2: Uses an output schema
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-109>)    LlmAgent structuredInfoAgentSchema =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-110>)        LlmAgent.builder()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-111>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-112>)            .name("structured_info_agent_schema")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-113>)            .description("Provides capital and estimated population in a specific JSON format.")
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-114>)            .instruction(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-115>)                String.format("""
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-116>)                You are an agent that provides country information.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-117>)                Respond ONLY with a JSON object matching this exact schema: %s
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-118>)                Use your knowledge to determine the capital and estimate the population. Do not use any tools.
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-119>)                """, CAPITAL_INFO_OUTPUT_SCHEMA.toJson()))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-120>)            // *** NO tools parameter here - using output_schema prevents tool use ***
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-121>)            .inputSchema(COUNTRY_INPUT_SCHEMA)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-122>)            .outputSchema(CAPITAL_INFO_OUTPUT_SCHEMA) // Enforce JSON output structure
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-123>)            .outputKey("structured_info_result") // Store final JSON response
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-124>)            .build();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-125>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-126>)    // --- 5. Set up Session Management and Runners ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-127>)    InMemorySessionService sessionService = new InMemorySessionService();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-128>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-129>)    sessionService.createSession(APP_NAME, USER_ID, null, SESSION_ID_TOOL_AGENT).blockingGet();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-130>)    sessionService.createSession(APP_NAME, USER_ID, null, SESSION_ID_SCHEMA_AGENT).blockingGet();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-131>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-132>)    Runner capitalRunner = new Runner(capitalAgentWithTool, APP_NAME, null, sessionService);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-133>)    Runner structuredRunner = new Runner(structuredInfoAgentSchema, APP_NAME, null, sessionService);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-134>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-135>)    // --- 6. Run Interactions ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-136>)    System.out.println("--- Testing Agent with Tool ---");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-137>)    agentExample.callAgentAndPrint(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-138>)        capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, "{\"country\": \"France\"}");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-139>)    agentExample.callAgentAndPrint(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-140>)        capitalRunner, capitalAgentWithTool, SESSION_ID_TOOL_AGENT, "{\"country\": \"Canada\"}");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-141>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-142>)    System.out.println("\n\n--- Testing Agent with Output Schema (No Tool Use) ---");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-143>)    agentExample.callAgentAndPrint(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-144>)        structuredRunner,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-145>)        structuredInfoAgentSchema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-146>)        SESSION_ID_SCHEMA_AGENT,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-147>)        "{\"country\": \"France\"}");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-148>)    agentExample.callAgentAndPrint(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-149>)        structuredRunner,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-150>)        structuredInfoAgentSchema,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-151>)        SESSION_ID_SCHEMA_AGENT,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-152>)        "{\"country\": \"Japan\"}");
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-153>)  }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-154>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-155>)  // --- 7. Define Agent Interaction Logic ---
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-156>)  public void callAgentAndPrint(Runner runner, LlmAgent agent, String sessionId, String queryJson) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-157>)    System.out.printf(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-158>)        "%n>>> Calling Agent: '%s' | Session: '%s' | Query: %s%n",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-159>)        agent.name(), sessionId, queryJson);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-160>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-161>)    Content userContent = Content.fromParts(Part.fromText(queryJson));
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-162>)    final String[] finalResponseContent = {"No final response received."};
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-163>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, sessionId, userContent);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-164>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-165>)    // Stream event response
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-166>)    eventStream.blockingForEach(event -> {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-167>)          if (event.finalResponse() && event.content().isPresent()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-168>)            event
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-169>)                .content()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-170>)                .get()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-171>)                .parts()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-172>)                .flatMap(parts -> parts.isEmpty() ? Optional.empty() : Optional.of(parts.get(0)))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-173>)                .flatMap(Part::text)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-174>)                .ifPresent(text -> finalResponseContent[0] = text);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-175>)          }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-176>)        });
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-177>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-178>)    System.out.printf("<<< Agent '%s' Response: %s%n", agent.name(), finalResponseContent[0]);
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-179>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-180>)    // Retrieve the session again to get the updated state
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-181>)    Session updatedSession =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-182>)        runner
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-183>)            .sessionService()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-184>)            .getSession(APP_NAME, USER_ID, sessionId, Optional.empty())
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-185>)            .blockingGet();
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-186>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-187>)    if (updatedSession != null && agent.outputKey().isPresent()) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-188>)      // Print to verify if the stored output looks like JSON (likely from output_schema)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-189>)      System.out.printf("--- Session State ['%s']: ", agent.outputKey().get());
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-190>)      }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-191>)  }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-38-192>)}
    
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-1>)val finalAgent =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-2>)    LlmAgent(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-3>)        name = "capital_agent",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-4>)        model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-5>)        description = "Answers user questions about the capital city of a given country.",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-6>)        instruction =
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-7>)            Instruction(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-8>)                "You are an agent that provides the capital city of a country...",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-9>)            ),
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-10>)        // tools = capitalService.generatedTools() // Assuming tools are added
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-11>)    )
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-12>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-13>)val sessionService = InMemorySessionService()
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-14>)val runner = InMemoryRunner(finalAgent, "capital_app", sessionService)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-15>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-16>)val userMessage = Content(parts = listOf(Part(text = "What is the capital of France?")))
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-17>)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-18>)// Use runAsync to get a Flow of events
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-19>)runner.runAsync(
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-20>)    userId = "user123",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-21>)    sessionId = "session456",
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-22>)    newMessage = userMessage,
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-23>)).collect {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-24>)        event ->
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-25>)    if (event.isFinalResponse) {
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-26>)        val finalResponse = event.content?.parts?.firstOrNull()?.text
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-27>)        println(finalResponse)
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-28>)    }
    [](<https://adk.dev/agents/llm-agents/#__codelineno-39-29>)}
    
## Additional features[¶](<https://adk.dev/agents/llm-agents/#additional-features> "Permanent link")

ADK provides additional features for agents not covered in this guide, including the following:

  * **Callbacks:** Add more controls by intercepting agent execution points, including before and after model calls, and before and after tool calls with [Callbacks](<https://adk.dev/callbacks/types-of-callbacks/>).
  * **Graph-based workflows:** Compose LLM agents as steps in deterministic, graph-based pipelines using [Graph-based agent workflows](<https://adk.dev/graphs/>). In Go v2.0.0, use `workflow.NewAgentNode` to wrap any LLM agent as a workflow node.
  * **Multi-agent systems:** Advanced strategies for agent interaction, including agent transfer (`disallow_transfer_to_parent`, `disallow_transfer_to_peers`) and shared instructions (`global_instruction`). See [Multi-agent workflows](<https://adk.dev/workflows/>) and [collaborative agent teams](<https://adk.dev/workflows/collaboration/>).

Back to top 