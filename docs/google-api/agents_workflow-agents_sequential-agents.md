# Sequential workflow - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/workflow-agents/sequential-agents/](https://adk.dev/agents/workflow-agents/sequential-agents/)

[ Skip to content ](<https://adk.dev/agents/workflow-agents/sequential-agents/#sequential-template-workflow-agent>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/workflow-agents/sequential-agents.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/workflow-agents/sequential-agents/index.md> "View this page as Markdown")

# Sequential template workflow agent[¶](<https://adk.dev/agents/workflow-agents/sequential-agents/#sequential-template-workflow-agent> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.2.0

The **_SequentialAgent_** class is a [template workflow](<https://adk.dev/agents/workflow-agents/>) agent that executes its sub-agents in the order they are specified in a list. Use **_SequentialAgent_** when you want execution to occur in a fixed, strict order. As with other templated workflows, the execution of a **_SequentialAgent_** object is not controlled by an AI model, and is deterministic in how it executes its sub-agents. The sub-agents specified in the sequential execution set may or may not utilize AI models, but the overall execution of those sub-agents is ultimately managed by the **_SequentialAgent_** object you define.

Alternative: graph-based workflows

Starting in ADK 2.0 for Python and Go, templated workflows have been superseded

by more flexible workflow structures, including [graph-based workflows](<https://adk.dev/graphs/>) and [dynamic workflows](<https://adk.dev/graphs/dynamic/>).

### Example scenario[¶](<https://adk.dev/agents/workflow-agents/sequential-agents/#example-scenario> "Permanent link")

You want to build an agent that can summarize any webpage, using two tools: **Get Page Contents** and **Summarize Page**. Since the agent must always call **Get Page Contents** before calling **Summarize Page** , you can build your agent using the **_SequentialAgent_** class.

### How it works[¶](<https://adk.dev/agents/workflow-agents/sequential-agents/#how-it-works> "Permanent link")

When the `SequentialAgent`'s `Run Async` method is called, it performs the following actions:

  1. **Iteration:** It iterates through the sub agents list in the order they were provided.
  2. **Sub-Agent Execution:** For each sub-agent in the list, it calls the sub-agent's `Run Async` method.

![Sequential Agent](https://adk.dev/assets/sequential-agent.png)

Shared Invocation Context

The `SequentialAgent` passes the same `InvocationContext` to each of its sub-agents. This means they all share the same session state, including the temporary (`temp:`) namespace, making it easy to pass data between steps within a single turn.

### Full Example: Code Development Pipeline[¶](<https://adk.dev/agents/workflow-agents/sequential-agents/#full-example-code-development-pipeline> "Permanent link")

Consider a simplified code development pipeline:

  * **Code Writer Agent:** An LLM Agent that generates initial code based on a specification.
  * **Code Reviewer Agent:** An LLM Agent that reviews the generated code for errors, style issues, and adherence to best practices. It receives the output of the Code Writer Agent.
  * **Code Refactorer Agent:** An LLM Agent that takes the reviewed code, and the reviewer's comments, and refactors it to improve quality and address issues.

Using a `SequentialAgent` makes it simple to define this exection flow, as shown in the following code snippet:
    
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-0-1>)SequentialAgent(sub_agents=[CodeWriterAgent, CodeReviewerAgent, CodeRefactorerAgent])
    
This ensures the code is written, _then_ reviewed, and _finally_ refactored, in a strict, dependable order. **The output from each sub-agent is passed to the next by storing them in state via[Output Key](<https://adk.dev/agents/llm-agents/##data-handling>)**.

Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-1>)from google.adk.agents.sequential_agent import SequentialAgent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-2>)from google.adk.agents.llm_agent import LlmAgent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-3>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-4>)# --- Constants ---
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-5>)GEMINI_MODEL = "gemini-2.5-flash"
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-6>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-7>)# --- 1. Define Sub-Agents for Each Pipeline Stage ---
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-8>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-9>)# Code Writer Agent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-10>)# Takes the initial specification (from user query) and writes code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-11>)code_writer_agent = LlmAgent(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-12>)    name="CodeWriterAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-13>)    model=GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-14>)    instruction="""
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-15>)    You are a Python Code Generator.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-16>)    Based *only* on the user's request, write Python code that fulfills the requirement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-17>)    Output *only* the complete Python code block, enclosed in triple backticks (```python ... ```).
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-18>)    Do not add any other text before or after the code block.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-19>)    """,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-20>)    description="Writes initial Python code based on a specification.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-21>)    output_key="generated_code"
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-22>))
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-23>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-24>)# Code Reviewer Agent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-25>)# Takes the code generated by the previous agent (read from state) and provides feedback.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-26>)code_reviewer_agent = LlmAgent(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-27>)    name="CodeReviewerAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-28>)    model=GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-29>)    instruction="""
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-30>)    You are an expert Python Code Reviewer.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-31>)    Your task is to provide constructive feedback on the provided code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-32>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-33>)    **Code to Review:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-34>)    ```python
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-35>)    {generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-36>)    ```
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-37>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-38>)    **Review Criteria:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-39>)    1.  **Correctness:** Does the code work as intended? Are there logic errors?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-40>)    2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-41>)    3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-42>)    4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-43>)    5.  **Best Practices:** Does the code follow common Python best practices?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-44>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-45>)    **Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-46>)    Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-47>)    If the code is excellent and requires no changes, simply state: "No major issues found."
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-48>)    Output *only* the review comments or the "No major issues" statement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-49>)    """,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-50>)    description="Reviews code and provides feedback.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-51>)    output_key="review_comments"
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-52>))
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-53>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-54>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-55>)# Code Refactorer Agent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-56>)# Takes the original code and the review comments (read from state) and refactors the code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-57>)code_refactorer_agent = LlmAgent(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-58>)    name="CodeRefactorerAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-59>)    model=GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-60>)    instruction="""
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-61>)    You are a Python Code Refactoring AI.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-62>)    Your goal is to improve the given Python code based on the provided review comments.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-63>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-64>)    **Original Code:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-65>)    ```python
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-66>)    {generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-67>)    ```
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-68>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-69>)    **Review Comments:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-70>)    {review_comments}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-71>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-72>)    **Task:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-73>)    Carefully apply the suggestions from the review comments to refactor the original code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-74>)    If the review comments state "No major issues found," return the original code unchanged.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-75>)    Ensure the final code is complete, functional, and includes necessary imports and docstrings.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-76>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-77>)    **Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-78>)    Output *only* the final, refactored Python code block, enclosed in triple backticks (```python ... ```).
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-79>)    Do not add any other text before or after the code block.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-80>)    """,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-81>)    description="Refactors code based on review comments.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-82>)    output_key="refactored_code"
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-83>))
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-84>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-85>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-86>)# --- 2. Create the SequentialAgent ---
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-87>)# This agent orchestrates the pipeline by running the sub_agents in order.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-88>)code_pipeline_agent = SequentialAgent(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-89>)    name="CodePipelineAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-90>)    sub_agents=[code_writer_agent, code_reviewer_agent, code_refactorer_agent],
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-91>)    description="Executes a sequence of code writing, reviewing, and refactoring.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-92>))
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-93>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-1-94>)root_agent = code_pipeline_agent
    
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-1>)// Part of agent.ts --> Follow https://adk.dev/get-started/ to learn the setup
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-2>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-3>)// --- 1. Define Sub-Agents for Each Pipeline Stage ---
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-4>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-5>)// Code Writer Agent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-6>)// Takes the initial specification (from user query) and writes code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-7>)const codeWriterAgent = new LlmAgent({
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-8>)    name: "CodeWriterAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-9>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-10>)    instruction: `You are a Python Code Generator.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-11>)Based *only* on the user's request, write Python code that fulfills the requirement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-12>)Output *only* the complete Python code block, enclosed in triple backticks (\`\`\`python ... \`\`\`).
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-13>)Do not add any other text before or after the code block.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-14>)`,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-15>)    description: "Writes initial Python code based on a specification.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-16>)    outputKey: "generated_code" // Stores output in state['generated_code']
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-17>)});
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-18>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-19>)// Code Reviewer Agent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-20>)// Takes the code generated by the previous agent (read from state) and provides feedback.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-21>)const codeReviewerAgent = new LlmAgent({
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-22>)    name: "CodeReviewerAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-23>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-24>)    instruction: `You are an expert Python Code Reviewer.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-25>)    Your task is to provide constructive feedback on the provided code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-26>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-27>)    **Code to Review:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-28>)    \`\`\`python
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-29>)    {generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-30>)    \`\`\`
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-31>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-32>)**Review Criteria:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-33>)1.  **Correctness:** Does the code work as intended? Are there logic errors?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-34>)2.  **Readability:** Is the code clear and easy to understand? Follows PEP 8 style guidelines?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-35>)3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-36>)4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-37>)5.  **Best Practices:** Does the code follow common Python best practices?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-38>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-39>)**Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-40>)Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-41>)If the code is excellent and requires no changes, simply state: "No major issues found."
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-42>)Output *only* the review comments or the "No major issues" statement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-43>)`,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-44>)    description: "Reviews code and provides feedback.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-45>)    outputKey: "review_comments", // Stores output in state['review_comments']
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-46>)});
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-47>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-48>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-49>)// Code Refactorer Agent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-50>)// Takes the original code and the review comments (read from state) and refactors the code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-51>)const codeRefactorerAgent = new LlmAgent({
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-52>)    name: "CodeRefactorerAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-53>)    model: GEMINI_MODEL,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-54>)    instruction: `You are a Python Code Refactoring AI.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-55>)Your goal is to improve the given Python code based on the provided review comments.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-56>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-57>)  **Original Code:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-58>)  \`\`\`python
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-59>)  {generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-60>)  \`\`\`
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-61>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-62>)  **Review Comments:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-63>)  {review_comments}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-64>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-65>)**Task:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-66>)Carefully apply the suggestions from the review comments to refactor the original code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-67>)If the review comments state "No major issues found," return the original code unchanged.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-68>)Ensure the final code is complete, functional, and includes necessary imports and docstrings.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-69>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-70>)**Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-71>)Output *only* the final, refactored Python code block, enclosed in triple backticks (\`\`\`python ... \`\`\`).
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-72>)Do not add any other text before or after the code block.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-73>)`,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-74>)    description: "Refactors code based on review comments.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-75>)    outputKey: "refactored_code", // Stores output in state['refactored_code']
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-76>)});
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-77>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-78>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-79>)// --- 2. Create the SequentialAgent ---
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-80>)// This agent orchestrates the pipeline by running the sub_agents in order.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-81>)const rootAgent = new SequentialAgent({
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-82>)    name: "CodePipelineAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-83>)    subAgents: [codeWriterAgent, codeReviewerAgent, codeRefactorerAgent],
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-84>)    description: "Executes a sequence of code writing, reviewing, and refactoring.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-85>)    // The agents will run in the order provided: Writer -> Reviewer -> Refactorer
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-2-86>)});
    
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-1>)    model, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-2>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-3>)        return fmt.Errorf("failed to create model: %v", err)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-4>)    }
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-5>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-6>)    codeWriterAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-7>)        Name:        "CodeWriterAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-8>)        Model:       model,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-9>)        Description: "Writes initial Go code based on a specification.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-10>)        Instruction: `You are a Go Code Generator.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-11>)Based *only* on the user's request, write Go code that fulfills the requirement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-12>)Output *only* the complete Go code block, enclosed in triple backticks ('''go ... ''').
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-13>)Do not add any other text before or after the code block.`,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-14>)        OutputKey: "generated_code",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-15>)    })
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-16>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-17>)        return fmt.Errorf("failed to create code writer agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-18>)    }
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-19>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-20>)    codeReviewerAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-21>)        Name:        "CodeReviewerAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-22>)        Model:       model,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-23>)        Description: "Reviews code and provides feedback.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-24>)        Instruction: `You are an expert Go Code Reviewer.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-25>)Your task is to provide constructive feedback on the provided code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-26>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-27>)**Code to Review:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-28>)'''go
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-29>){generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-30>)'''
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-31>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-32>)**Review Criteria:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-33>)1.  **Correctness:** Does the code work as intended? Are there logic errors?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-34>)2.  **Readability:** Is the code clear and easy to understand? Follows Go style guidelines?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-35>)3.  **Idiomatic Go:** Does the code use Go's features in a natural and standard way?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-36>)4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-37>)5.  **Best Practices:** Does the code follow common Go best practices?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-38>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-39>)**Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-40>)Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-41>)If the code is excellent and requires no changes, simply state: "No major issues found."
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-42>)Output *only* the review comments or the "No major issues" statement.`,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-43>)        OutputKey: "review_comments",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-44>)    })
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-45>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-46>)        return fmt.Errorf("failed to create code reviewer agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-47>)    }
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-48>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-49>)    codeRefactorerAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-50>)        Name:        "CodeRefactorerAgent",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-51>)        Model:       model,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-52>)        Description: "Refactors code based on review comments.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-53>)        Instruction: `You are a Go Code Refactoring AI.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-54>)Your goal is to improve the given Go code based on the provided review comments.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-55>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-56>)**Original Code:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-57>)'''go
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-58>){generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-59>)'''
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-60>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-61>)**Review Comments:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-62>){review_comments}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-63>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-64>)**Task:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-65>)Carefully apply the suggestions from the review comments to refactor the original code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-66>)If the review comments state "No major issues found," return the original code unchanged.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-67>)Ensure the final code is complete, functional, and includes necessary imports.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-68>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-69>)**Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-70>)Output *only* the final, refactored Go code block, enclosed in triple backticks ('''go ... ''').
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-71>)Do not add any other text before or after the code block.`,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-72>)        OutputKey: "refactored_code",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-73>)    })
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-74>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-75>)        return fmt.Errorf("failed to create code refactorer agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-76>)    }
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-77>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-78>)    codePipelineAgent, err := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-79>)        AgentConfig: agent.Config{
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-80>)            Name:        appName,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-81>)            Description: "Executes a sequence of code writing, reviewing, and refactoring.",
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-82>)            SubAgents: []agent.Agent{
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-83>)                codeWriterAgent,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-84>)                codeReviewerAgent,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-85>)                codeRefactorerAgent,
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-86>)            },
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-87>)        },
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-88>)    })
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-89>)    if err != nil {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-90>)        return fmt.Errorf("failed to create sequential agent: %v", err)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-3-91>)    }
    
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-2>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-4>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-5>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-6>)import com.google.genai.types.Content;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-7>)import com.google.genai.types.Part;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-8>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-9>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-10>)public class SequentialAgentExample {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-11>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-12>)  private static final String APP_NAME = "CodePipelineAgent";
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-13>)  private static final String USER_ID = "test_user_456";
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-14>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-15>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-16>)  public static void main(String[] args) {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-17>)    SequentialAgentExample sequentialAgentExample = new SequentialAgentExample();
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-18>)    sequentialAgentExample.runAgent(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-19>)        "Write a Java function to calculate the factorial of a number.");
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-20>)  }
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-21>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-22>)  public void runAgent(String prompt) {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-23>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-24>)    LlmAgent codeWriterAgent =
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-25>)        LlmAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-26>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-27>)            .name("CodeWriterAgent")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-28>)            .description("Writes initial Java code based on a specification.")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-29>)            .instruction(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-30>)                """
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-31>)                You are a Java Code Generator.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-32>)                Based *only* on the user's request, write Java code that fulfills the requirement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-33>)                Output *only* the complete Java code block, enclosed in triple backticks (```java ... ```).
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-34>)                Do not add any other text before or after the code block.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-35>)                """)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-36>)            .outputKey("generated_code")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-37>)            .build();
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-38>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-39>)    LlmAgent codeReviewerAgent =
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-40>)        LlmAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-41>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-42>)            .name("CodeReviewerAgent")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-43>)            .description("Reviews code and provides feedback.")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-44>)            .instruction(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-45>)                """
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-46>)                    You are an expert Java Code Reviewer.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-47>)                    Your task is to provide constructive feedback on the provided code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-48>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-49>)                    **Code to Review:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-50>)                    ```java
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-51>)                    {generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-52>)                    ```
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-53>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-54>)                    **Review Criteria:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-55>)                    1.  **Correctness:** Does the code work as intended? Are there logic errors?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-56>)                    2.  **Readability:** Is the code clear and easy to understand? Follows Java style guidelines?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-57>)                    3.  **Efficiency:** Is the code reasonably efficient? Any obvious performance bottlenecks?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-58>)                    4.  **Edge Cases:** Does the code handle potential edge cases or invalid inputs gracefully?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-59>)                    5.  **Best Practices:** Does the code follow common Java best practices?
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-60>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-61>)                    **Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-62>)                    Provide your feedback as a concise, bulleted list. Focus on the most important points for improvement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-63>)                    If the code is excellent and requires no changes, simply state: "No major issues found."
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-64>)                    Output *only* the review comments or the "No major issues" statement.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-65>)                """)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-66>)            .outputKey("review_comments")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-67>)            .build();
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-68>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-69>)    LlmAgent codeRefactorerAgent =
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-70>)        LlmAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-71>)            .model(MODEL_NAME)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-72>)            .name("CodeRefactorerAgent")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-73>)            .description("Refactors code based on review comments.")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-74>)            .instruction(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-75>)                """
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-76>)                You are a Java Code Refactoring AI.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-77>)                Your goal is to improve the given Java code based on the provided review comments.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-78>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-79>)                  **Original Code:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-80>)                  ```java
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-81>)                  {generated_code}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-82>)                  ```
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-83>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-84>)                  **Review Comments:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-85>)                  {review_comments}
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-86>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-87>)                **Task:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-88>)                Carefully apply the suggestions from the review comments to refactor the original code.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-89>)                If the review comments state "No major issues found," return the original code unchanged.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-90>)                Ensure the final code is complete, functional, and includes necessary imports and docstrings.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-91>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-92>)                **Output:**
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-93>)                Output *only* the final, refactored Java code block, enclosed in triple backticks (```java ... ```).
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-94>)                Do not add any other text before or after the code block.
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-95>)                """)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-96>)            .outputKey("refactored_code")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-97>)            .build();
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-98>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-99>)    SequentialAgent codePipelineAgent =
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-100>)        SequentialAgent.builder()
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-101>)            .name(APP_NAME)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-102>)            .description("Executes a sequence of code writing, reviewing, and refactoring.")
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-103>)            // The agents will run in the order provided: Writer -> Reviewer -> Refactorer
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-104>)            .subAgents(codeWriterAgent, codeReviewerAgent, codeRefactorerAgent)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-105>)            .build();
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-106>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-107>)    // Create an InMemoryRunner
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-108>)    InMemoryRunner runner = new InMemoryRunner(codePipelineAgent, APP_NAME);
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-109>)    // InMemoryRunner automatically creates a session service. Create a session using the service
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-110>)    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-111>)    Content userMessage = Content.fromParts(Part.fromText(prompt));
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-112>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-113>)    // Run the agent
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-114>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-115>)
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-116>)    // Stream event response
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-117>)    eventStream.blockingForEach(
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-118>)        event -> {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-119>)          if (event.finalResponse()) {
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-120>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-121>)          }
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-122>)        });
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-123>)  }
    [](<https://adk.dev/agents/workflow-agents/sequential-agents/#__codelineno-4-124>)}
    
Back to top 