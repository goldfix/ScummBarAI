# Loop workflow - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/workflow-agents/loop-agents/](https://adk.dev/agents/workflow-agents/loop-agents/)

[ Skip to content ](<https://adk.dev/agents/workflow-agents/loop-agents/#loop-template-workflow-agent>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/workflow-agents/loop-agents.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/workflow-agents/loop-agents/index.md> "View this page as Markdown")

# Loop template workflow agent[¶](<https://adk.dev/agents/workflow-agents/loop-agents/#loop-template-workflow-agent> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.2.0

The **_LoopAgent_** class is a [template workflow](<https://adk.dev/agents/workflow-agents/>) agent that executes its sub-agents in a loop for a specified number of iterations or until a termination condition is met. Use the **_LoopAgent_** when your workflow involves repetition or iterative refinement, such as revising code or a document. As with other templated workflows, the execution of a **_LoopAgent_** object is not controlled by an AI model, and is deterministic in how it executes its sub-agents. The sub-agents within the defined loop may or may not utilize AI models, but the overall execution of those sub-agents is ultimately managed by the **_LoopAgent_** object you define.

Alternative: graph-based workflows

Starting in ADK 2.0 for Python and Go, templated workflows have been superseded

by more flexible workflow structures, including [graph-based workflows](<https://adk.dev/graphs/>) and [dynamic workflows](<https://adk.dev/graphs/dynamic/>).

### Example scenario[¶](<https://adk.dev/agents/workflow-agents/loop-agents/#example-scenario> "Permanent link")

You want to build an agent that can generate images of food, but sometimes when you want to generate a specific number of items, such as bananas, the agent generates a different number of those items in the image, such as an image of 7 bananas. You have two tools: `Generate Image`, `Count Food Items`. If your goal is to keep generating images until it either correctly generates the specified number of items, or after a certain number of iterations, you can build your agent using a **_LoopAgent_** workflow.

### How it Works[¶](<https://adk.dev/agents/workflow-agents/loop-agents/#how-it-works> "Permanent link")

When the `LoopAgent`'s `Run Async` method is called, it performs the following actions:

  1. **Sub-Agent Execution:** It iterates through the Sub Agents list _in order_. For _each_ sub-agent, it calls the agent's `Run Async` method.
  2. **Termination Check:**

_Crucially_ , the `LoopAgent` itself does _not_ inherently decide when to stop looping. You _must_ implement a termination mechanism to prevent infinite loops. Common strategies include:

     * **Max Iterations** : Set a maximum number of iterations in the `LoopAgent`. **The loop will terminate after that many iterations**.
     * **Escalation from sub-agent** : Design one or more sub-agents to evaluate a condition (e.g., "Is the document quality good enough?", "Has a consensus been reached?"). If the condition is met, the sub-agent can signal termination (e.g., by raising a custom event, setting a flag in a shared context, or returning a specific value).

![Loop Agent](https://adk.dev/assets/loop-agent.png)

### Full Example: Iterative Document Improvement[¶](<https://adk.dev/agents/workflow-agents/loop-agents/#full-example-iterative-document-improvement> "Permanent link")

Imagine a scenario where you want to iteratively improve a document:

  * **Writer Agent:** An `LlmAgent` that generates or refines a draft on a topic.
  * **Critic Agent:** An `LlmAgent` that critiques the draft, identifying areas for improvement.
        
        [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-0-1>)LoopAgent(sub_agents=[WriterAgent, CriticAgent], max_iterations=5)
        
In this setup, the `LoopAgent` would manage the iterative process. The `CriticAgent` could be **designed to return a "STOP" signal when the document reaches a satisfactory quality level** , preventing further iterations. Alternatively, the `max iterations` parameter could be used to limit the process to a fixed number of cycles, or external logic could be implemented to make stop decisions. The **loop would run at most five times** , ensuring the iterative refinement doesn't continue indefinitely.

Full Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-1>)from google.adk.agents import LoopAgent, LlmAgent, SequentialAgent
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-2>)from google.adk.tools.tool_context import ToolContext
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-3>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-4>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-5>)# --- Constants ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-6>)GEMINI_MODEL = "gemini-2.5-flash"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-7>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-8>)# --- State Keys ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-9>)STATE_CURRENT_DOC = "current_document"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-10>)STATE_CRITICISM = "criticism"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-11>)# Define the exact phrase the Critic should use to signal completion
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-12>)COMPLETION_PHRASE = "No major issues found."
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-13>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-14>)# --- Tool Definition ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-15>)def exit_loop(tool_context: ToolContext):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-16>)    """Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end."""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-17>)    print(f"  [Tool Call] exit_loop triggered by {tool_context.agent_name}")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-18>)    tool_context.actions.escalate = True
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-19>)    tool_context.actions.skip_summarization = True
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-20>)    # Return empty dict as tools should typically return JSON-serializable output
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-21>)    return {}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-22>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-23>)# --- Before Agent Callback ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-24>)def update_initial_topic_state(callback_context: CallbackContext):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-25>)    """Ensure 'initial_topic' is set in state before pipeline starts."""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-26>)    callback_context.state['initial_topic'] = callback_context.state.get('initial_topic', 'a robot developing unexpected emotions')
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-27>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-28>)# --- Agent Definitions ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-29>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-30>)# STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-31>)initial_writer_agent = LlmAgent(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-32>)    name="InitialWriterAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-33>)    model=GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-34>)    include_contents='none',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-35>)    instruction=f"""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-36>)    You are a Creative Writing Assistant tasked with starting a story.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-37>)    Write a *very basic* first draft of a short story (just 1-2 simple sentences).
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-38>)    Keep it plain and minimal - do NOT add descriptive language yet.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-39>)    Topic: {{initial_topic}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-40>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-41>)    Output *only* the story/document text. Do not add introductions or explanations.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-42>)    """,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-43>)    description="Writes the initial document draft based on the topic, aiming for some initial substance.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-44>)    output_key=STATE_CURRENT_DOC
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-45>))
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-46>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-47>)# STEP 2a: Critic Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-48>)critic_agent_in_loop = LlmAgent(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-49>)    name="CriticAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-50>)    model=GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-51>)    include_contents='none',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-52>)    instruction=f"""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-53>)    You are a Constructive Critic AI reviewing a short story draft.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-54>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-55>)    **Document to Review:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-56>)    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-57>)    {{current_document}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-58>)    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-59>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-60>)    **Completion Criteria (ALL must be met):**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-61>)    1. At least 4 sentences long
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-62>)    2. Has a clear beginning, middle, and end
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-63>)    3. Includes at least one descriptive detail (sensory or emotional)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-64>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-65>)    **Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-66>)    Check the document against the criteria above.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-67>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-68>)    IF any criteria is NOT met, provide specific feedback on what to add or improve.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-69>)    Output *only* the critique text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-70>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-71>)    IF ALL criteria are met, respond *exactly* with: "{COMPLETION_PHRASE}"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-72>)    """,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-73>)    description="Reviews the current draft, providing critique if clear improvements are needed, otherwise signals completion.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-74>)    output_key=STATE_CRITICISM
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-75>))
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-76>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-77>)# STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-78>)refiner_agent_in_loop = LlmAgent(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-79>)    name="RefinerAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-80>)    model=GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-81>)    # Relies solely on state via placeholders
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-82>)    include_contents='none',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-83>)    instruction=f"""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-84>)    You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-85>)    **Current Document:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-86>)    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-87>)    {{current_document}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-88>)    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-89>)    **Critique/Suggestions:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-90>)    {{criticism}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-91>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-92>)    **Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-93>)    Analyze the 'Critique/Suggestions'.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-94>)    IF the critique is *exactly* "{COMPLETION_PHRASE}":
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-95>)    You MUST call the 'exit_loop' function. Do not output any text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-96>)    ELSE (the critique contains actionable feedback):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-97>)    Carefully apply the suggestions to improve the 'Current Document'. Output *only* the refined document text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-98>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-99>)    Do not add explanations. Either output the refined document OR call the exit_loop function.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-100>)    """,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-101>)    description="Refines the document based on critique, or calls exit_loop if critique indicates completion.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-102>)    tools=[exit_loop], # Provide the exit_loop tool
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-103>)    output_key=STATE_CURRENT_DOC # Overwrites state['current_document'] with the refined version
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-104>))
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-105>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-106>)# STEP 2: Refinement Loop Agent
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-107>)refinement_loop = LoopAgent(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-108>)    name="RefinementLoop",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-109>)    # Agent order is crucial: Critique first, then Refine/Exit
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-110>)    sub_agents=[
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-111>)        critic_agent_in_loop,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-112>)        refiner_agent_in_loop,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-113>)    ],
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-114>)    max_iterations=5 # Limit loops
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-115>))
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-116>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-117>)# STEP 3: Overall Sequential Pipeline
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-118>)# For ADK tools compatibility, the root agent must be named `root_agent`
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-119>)root_agent = SequentialAgent(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-120>)    name="IterativeWritingPipeline",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-121>)    sub_agents=[
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-122>)        initial_writer_agent, # Run first to create initial doc
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-123>)        refinement_loop       # Then run the critique/refine loop
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-124>)    ],
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-125>)    before_agent_callback=update_initial_topic_state, # set initial topic in state
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-126>)    description="Writes an initial document and then iteratively refines it with critique using an exit tool."
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-1-127>))
    
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-1>)// Part of agent.ts --> Follow https://adk.dev/get-started/ to learn the setup
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-2>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-3>)import { LoopAgent, LlmAgent, SequentialAgent, FunctionTool } from '@google/adk';
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-4>)import { z } from 'zod';
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-5>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-6>)// --- Constants ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-7>)const GEMINI_MODEL = "gemini-2.5-flash";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-8>)const STATE_INITIAL_TOPIC = "initial_topic";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-9>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-10>)// --- State Keys ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-11>)const STATE_CURRENT_DOC = "current_document";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-12>)const STATE_CRITICISM = "criticism";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-13>)// Define the exact phrase the Critic should use to signal completion
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-14>)const COMPLETION_PHRASE = "No major issues found.";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-15>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-16>)// --- Tool Definition ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-17>)const exitLoopTool = new FunctionTool({
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-18>)    name: 'exit_loop',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-19>)    description: 'Call this function ONLY when the critique indicates no further changes are needed, signaling the iterative process should end.',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-20>)    parameters: z.object({}),
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-21>)    execute: (input, context) => {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-22>)        if (context) {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-23>)            console.log(`  [Tool Call] exit_loop triggered by ${context.agentName} with input: ${input}`);
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-24>)            context.actions.escalate = true;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-25>)        }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-26>)        return {};
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-27>)    },
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-28>)});
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-29>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-30>)// --- Agent Definitions ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-31>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-32>)// STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-33>)const initialWriterAgent = new LlmAgent({
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-34>)    name: "InitialWriterAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-35>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-36>)    includeContents: 'none',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-37>)    // MODIFIED Instruction: Ask for a slightly more developed start
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-38>)    instruction: `You are a Creative Writing Assistant tasked with starting a story.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-39>)    Write the *first draft* of a short story (aim for 2-4 sentences).
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-40>)    Base the content *only* on the topic provided below. Try to introduce a specific element (like a character, a setting detail, or a starting action) to make it engaging.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-41>)    Topic: {{${STATE_INITIAL_TOPIC}}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-42>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-43>)    Output *only* the story/document text. Do not add introductions or explanations.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-44>)    `,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-45>)    description: "Writes the initial document draft based on the topic, aiming for some initial substance.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-46>)    outputKey: STATE_CURRENT_DOC
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-47>)});
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-48>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-49>)// STEP 2a: Critic Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-50>)const criticAgentInLoop = new LlmAgent({
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-51>)    name: "CriticAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-52>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-53>)    includeContents: 'none',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-54>)    // MODIFIED Instruction: More nuanced completion criteria, look for clear improvement paths.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-55>)    instruction: `You are a Constructive Critic AI reviewing a short document draft (typically 2-6 sentences). Your goal is balanced feedback.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-56>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-57>)    **Document to Review:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-58>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-59>)    {{current_document}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-60>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-61>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-62>)    **Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-63>)    Review the document for clarity, engagement, and basic coherence according to the initial topic (if known).
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-64>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-65>)    IF you identify 1-2 *clear and actionable* ways the document could be improved to better capture the topic or enhance reader engagement (e.g., "Needs a stronger opening sentence", "Clarify the character's goal"):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-66>)    Provide these specific suggestions concisely. Output *only* the critique text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-67>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-68>)    ELSE IF the document is coherent, addresses the topic adequately for its length, and has no glaring errors or obvious omissions:
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-69>)    Respond *exactly* with the phrase "${COMPLETION_PHRASE}" and nothing else. It doesn't need to be perfect, just functionally complete for this stage. Avoid suggesting purely subjective stylistic preferences if the core is sound.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-70>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-71>)    Do not add explanations. Output only the critique OR the exact completion.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-72>)`,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-73>)    description: "Reviews the current draft, providing critique if clear improvements are needed, otherwise signals completion.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-74>)    outputKey: STATE_CRITICISM
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-75>)});
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-76>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-77>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-78>)// STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-79>)const refinerAgentInLoop = new LlmAgent({
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-80>)    name: "RefinerAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-81>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-82>)    // Relies solely on state via placeholders
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-83>)    includeContents: 'none',
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-84>)    instruction: `You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-85>)    **Current Document:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-86>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-87>)    {{current_document}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-88>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-89>)    **Critique/Suggestions:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-90>)    {{criticism}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-91>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-92>)    **Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-93>)    Analyze the 'Critique/Suggestions'.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-94>)    IF the critique is *exactly* "${COMPLETION_PHRASE}":
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-95>)    You MUST call the 'exit_loop' function. Do not output any text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-96>)    ELSE (the critique contains actionable feedback):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-97>)    Carefully apply the suggestions to improve the 'Current Document'. Output *only* the refined document text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-98>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-99>)    Do not add explanations. Either output the refined document OR call the exit_loop function.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-100>)`,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-101>)    tools: [exitLoopTool],
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-102>)    description: "Refines the document based on critique, or calls exit_loop if critique indicates completion.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-103>)    outputKey: STATE_CURRENT_DOC
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-104>)});
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-105>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-106>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-107>)// STEP 2: Refinement Loop Agent
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-108>)const refinementLoop = new LoopAgent({
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-109>)    name: "RefinementLoop",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-110>)    // Agent order is crucial: Critique first, then Refine/Exit
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-111>)    subAgents: [
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-112>)        criticAgentInLoop,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-113>)        refinerAgentInLoop,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-114>)    ],
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-115>)    maxIterations: 5 // Limit loops
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-116>)});
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-117>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-118>)// STEP 3: Overall Sequential Pipeline
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-119>)// For ADK tools compatibility, the root agent must be named `root_agent`
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-120>)export const rootAgent = new SequentialAgent({
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-121>)    name: "IterativeWritingPipeline",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-122>)    subAgents: [
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-123>)        initialWriterAgent, // Run first to create initial doc
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-124>)        refinementLoop       // Then run the critique/refine loop
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-125>)    ],
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-126>)    description: "Writes an initial document and then iteratively refines it with critique using an exit tool."
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-2-127>)});
    
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-1>)// ExitLoopArgs defines the (empty) arguments for the ExitLoop tool.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-2>)type ExitLoopArgs struct{}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-3>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-4>)// ExitLoopResults defines the output of the ExitLoop tool.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-5>)type ExitLoopResults struct{}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-6>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-7>)// ExitLoop is a tool that signals the loop to terminate by setting Escalate to true.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-8>)func ExitLoop(ctx agent.Context, input ExitLoopArgs) (ExitLoopResults, error) {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-9>)    fmt.Printf("[Tool Call] exitLoop triggered by %s \n", ctx.AgentName())
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-10>)    ctx.Actions().Escalate = true
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-11>)    return ExitLoopResults{}, nil
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-12>)}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-13>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-14>)func main() {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-15>)    ctx := context.Background()
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-16>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-17>)    if err := runAgent(ctx, "Write a document about a cat"); err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-18>)        log.Fatalf("Agent execution failed: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-19>)    }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-20>)}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-21>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-22>)func runAgent(ctx context.Context, prompt string) error {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-23>)    model, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-24>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-25>)        return fmt.Errorf("failed to create model: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-26>)    }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-27>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-28>)    // STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-29>)    initialWriterAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-30>)        Name:        "InitialWriterAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-31>)        Model:       model,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-32>)        Description: "Writes the initial document draft based on the topic.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-33>)        Instruction: `You are a Creative Writing Assistant tasked with starting a story.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-34>)Write the *first draft* of a short story (aim for 2-4 sentences).
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-35>)Base the content *only* on the topic provided in the user's prompt.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-36>)Output *only* the story/document text. Do not add introductions or explanations.`,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-37>)        OutputKey: stateDoc,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-38>)    })
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-39>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-40>)        return fmt.Errorf("failed to create initial writer agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-41>)    }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-42>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-43>)    // STEP 2a: Critic Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-44>)    criticAgentInLoop, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-45>)        Name:        "CriticAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-46>)        Model:       model,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-47>)        Description: "Reviews the current draft, providing critique or signaling completion.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-48>)        Instruction: fmt.Sprintf(`You are a Constructive Critic AI reviewing a short document draft.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-49>)**Document to Review:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-50>)"""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-51>){%s}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-52>)"""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-53>)**Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-54>)Review the document.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-55>)IF you identify 1-2 *clear and actionable* ways it could be improved:
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-56>)Provide these specific suggestions concisely. Output *only* the critique text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-57>)ELSE IF the document is coherent and addresses the topic adequately:
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-58>)Respond *exactly* with the phrase "%s" and nothing else.`, stateDoc, donePhrase),
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-59>)        OutputKey: stateCrit,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-60>)    })
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-61>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-62>)        return fmt.Errorf("failed to create critic agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-63>)    }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-64>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-65>)    exitLoopTool, err := functiontool.New(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-66>)        functiontool.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-67>)            Name:        "exitLoop",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-68>)            Description: "Call this function ONLY when the critique indicates no further changes are needed.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-69>)        },
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-70>)        ExitLoop,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-71>)    )
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-72>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-73>)        return fmt.Errorf("failed to create exit loop tool: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-74>)    }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-75>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-76>)    // STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-77>)    refinerAgentInLoop, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-78>)        Name:  "RefinerAgent",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-79>)        Model: model,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-80>)        Instruction: fmt.Sprintf(`You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-81>)**Current Document:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-82>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-83>)"""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-84>){%s}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-85>)"""
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-86>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-87>)**Critique/Suggestions:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-88>){%s}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-89>)**Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-90>)Analyze the 'Critique/Suggestions'.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-91>)IF the critique is *exactly* "%s":
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-92>)You MUST call the 'exitLoop' function. Do not output any text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-93>)ELSE (the critique contains actionable feedback):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-94>)Carefully apply the suggestions to improve the 'Current Document'. Output *only* the refined document text.`, stateDoc, stateCrit, donePhrase),
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-95>)        Description: "Refines the document based on critique, or calls exitLoop if critique indicates completion.",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-96>)        Tools:       []tool.Tool{exitLoopTool},
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-97>)        OutputKey:   stateDoc,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-98>)    })
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-99>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-100>)        return fmt.Errorf("failed to create refiner agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-101>)    }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-102>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-103>)    // STEP 2: Refinement Loop Agent
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-104>)    refinementLoop, err := loopagent.New(loopagent.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-105>)        AgentConfig: agent.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-106>)            Name:      "RefinementLoop",
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-107>)            SubAgents: []agent.Agent{criticAgentInLoop, refinerAgentInLoop},
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-108>)        },
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-109>)        MaxIterations: 5,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-110>)    })
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-111>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-112>)        return fmt.Errorf("failed to create loop agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-113>)    }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-114>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-115>)    // STEP 3: Overall Sequential Pipeline
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-116>)    iterativeWriterAgent, err := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-117>)        AgentConfig: agent.Config{
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-118>)            Name:      appName,
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-119>)            SubAgents: []agent.Agent{initialWriterAgent, refinementLoop},
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-120>)        },
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-121>)    })
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-122>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-123>)        return fmt.Errorf("failed to create sequential agent pipeline: %v", err)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-3-124>)    }
    
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-1>)import static com.google.adk.agents.LlmAgent.IncludeContents.NONE;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-2>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-4>)import com.google.adk.agents.LoopAgent;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-5>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-6>)import com.google.adk.events.Event;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-7>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-8>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-9>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-10>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-11>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-12>)import com.google.genai.types.Content;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-13>)import com.google.genai.types.Part;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-14>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-15>)import java.util.Map;
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-16>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-17>)public class LoopAgentExample {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-18>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-19>)  // --- Constants ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-20>)  private static final String APP_NAME = "IterativeWritingPipeline";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-21>)  private static final String USER_ID = "test_user_456";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-22>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-23>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-24>)  // --- State Keys ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-25>)  private static final String STATE_CURRENT_DOC = "current_document";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-26>)  private static final String STATE_CRITICISM = "criticism";
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-27>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-28>)  public static void main(String[] args) {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-29>)    LoopAgentExample loopAgentExample = new LoopAgentExample();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-30>)    loopAgentExample.runAgent("Write a document about a cat");
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-31>)  }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-32>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-33>)  // --- Tool Definition ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-34>)  @Schema(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-35>)      description =
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-36>)          "Call this function ONLY when the critique indicates no further changes are needed,"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-37>)              + " signaling the iterative process should end.")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-38>)  public static Map<String, Object> exitLoop(@Schema(name = "toolContext") ToolContext toolContext) {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-39>)    System.out.printf("[Tool Call] exitLoop triggered by %s \n", toolContext.agentName());
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-40>)    toolContext.actions().setEscalate(true);
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-41>)    //  Return empty dict as tools should typically return JSON-serializable output
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-42>)    return Map.of();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-43>)  }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-44>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-45>)  // --- Agent Definitions ---
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-46>)  public void runAgent(String prompt) {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-47>)    // STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-48>)    LlmAgent initialWriterAgent =
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-49>)        LlmAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-50>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-51>)            .name("InitialWriterAgent")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-52>)            .description(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-53>)                "Writes the initial document draft based on the topic, aiming for some initial"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-54>)                    + " substance.")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-55>)            .instruction(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-56>)                """
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-57>)                    You are a Creative Writing Assistant tasked with starting a story.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-58>)                    Write the *first draft* of a short story (aim for 2-4 sentences).
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-59>)                    Base the content *only* on the topic provided below. Try to introduce a specific element (like a character, a setting detail, or a starting action) to make it engaging.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-60>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-61>)                    Output *only* the story/document text. Do not add introductions or explanations.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-62>)                """)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-63>)            .outputKey(STATE_CURRENT_DOC)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-64>)            .includeContents(NONE)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-65>)            .build();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-66>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-67>)    // STEP 2a: Critic Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-68>)    LlmAgent criticAgentInLoop =
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-69>)        LlmAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-70>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-71>)            .name("CriticAgent")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-72>)            .description(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-73>)                "Reviews the current draft, providing critique if clear improvements are needed,"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-74>)                    + " otherwise signals completion.")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-75>)            .instruction(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-76>)                """
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-77>)                    You are a Constructive Critic AI reviewing a short document draft (typically 2-6 sentences). Your goal is balanced feedback.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-78>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-79>)                    **Document to Review:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-80>)                    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-81>)                    {{current_document}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-82>)                    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-83>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-84>)                    **Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-85>)                    Review the document for clarity, engagement, and basic coherence according to the initial topic (if known).
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-86>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-87>)                    IF you identify 1-2 *clear and actionable* ways the document could be improved to better capture the topic or enhance reader engagement (e.g., "Needs a stronger opening sentence", "Clarify the character's goal"):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-88>)                    Provide these specific suggestions concisely. Output *only* the critique text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-89>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-90>)                    ELSE IF the document is coherent, addresses the topic adequately for its length, and has no glaring errors or obvious omissions:
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-91>)                    Respond *exactly* with the phrase "No major issues found." and nothing else. It doesn't need to be perfect, just functionally complete for this stage. Avoid suggesting purely subjective stylistic preferences if the core is sound.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-92>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-93>)                    Do not add explanations. Output only the critique OR the exact completion phrase.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-94>)                    """)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-95>)            .outputKey(STATE_CRITICISM)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-96>)            .includeContents(NONE)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-97>)            .build();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-98>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-99>)    // STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-100>)    LlmAgent refinerAgentInLoop =
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-101>)        LlmAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-102>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-103>)            .name("RefinerAgent")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-104>)            .description(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-105>)                "Refines the document based on critique, or calls exitLoop if critique indicates"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-106>)                    + " completion.")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-107>)            .instruction(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-108>)                """
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-109>)                    You are a Creative Writing Assistant refining a document based on feedback OR exiting the process.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-110>)                    **Current Document:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-111>)                    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-112>)                    {{current_document}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-113>)                    ```
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-114>)                    **Critique/Suggestions:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-115>)                    {{criticism}}
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-116>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-117>)                    **Task:**
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-118>)                    Analyze the 'Critique/Suggestions'.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-119>)                    IF the critique is *exactly* "No major issues found.":
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-120>)                    You MUST call the 'exitLoop' function. Do not output any text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-121>)                    ELSE (the critique contains actionable feedback):
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-122>)                    Carefully apply the suggestions to improve the 'Current Document'. Output *only* the refined document text.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-123>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-124>)                    Do not add explanations. Either output the refined document OR call the exitLoop function.
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-125>)                """)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-126>)            .outputKey(STATE_CURRENT_DOC)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-127>)            .includeContents(NONE)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-128>)            .tools(FunctionTool.create(LoopAgentExample.class, "exitLoop"))
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-129>)            .build();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-130>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-131>)    // STEP 2: Refinement Loop Agent
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-132>)    LoopAgent refinementLoop =
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-133>)        LoopAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-134>)            .name("RefinementLoop")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-135>)            .description("Repeatedly refines the document with critique and then exits.")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-136>)            .subAgents(criticAgentInLoop, refinerAgentInLoop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-137>)            .maxIterations(5)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-138>)            .build();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-139>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-140>)    // STEP 3: Overall Sequential Pipeline
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-141>)    SequentialAgent iterativeWriterAgent =
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-142>)        SequentialAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-143>)            .name(APP_NAME)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-144>)            .description(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-145>)                "Writes an initial document and then iteratively refines it with critique using an"
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-146>)                    + " exit tool.")
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-147>)            .subAgents(initialWriterAgent, refinementLoop)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-148>)            .build();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-149>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-150>)    // Create an InMemoryRunner
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-151>)    InMemoryRunner runner = new InMemoryRunner(iterativeWriterAgent, APP_NAME);
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-152>)    // InMemoryRunner automatically creates a session service. Create a session using the service
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-153>)    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-154>)    Content userMessage = Content.fromParts(Part.fromText(prompt));
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-155>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-156>)    // Run the agent
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-157>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-158>)
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-159>)    // Stream event response
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-160>)    eventStream.blockingForEach(
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-161>)        event -> {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-162>)          if (event.finalResponse()) {
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-163>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-164>)          }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-165>)        });
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-166>)  }
    [](<https://adk.dev/agents/workflow-agents/loop-agents/#__codelineno-4-167>)}
    
Back to top 