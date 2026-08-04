# Custom Tools for ADK - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools-custom/](https://adk.dev/tools-custom/)

[ Skip to content ](<https://adk.dev/tools-custom/#custom-tools-for-adk>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools-custom/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools-custom/index.md> "View this page as Markdown")

# Custom Tools for ADK[¶](<https://adk.dev/tools-custom/#custom-tools-for-adk> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0

In an ADK agent workflow, Tools are programming functions with structured input and output that can be called by an ADK Agent to perform actions. ADK Tools function similarly to how you use a [Function Call](<https://ai.google.dev/gemini-api/docs/function-calling>) with Gemini or other generative AI models. You can perform various actions and programming functions with an ADK Tool, such as:

  * Querying databases
  * Making API requests: getting weather data, booking systems
  * Searching the web
  * Executing code snippets
  * Retrieving information from documents (RAG)
  * Interacting with other software or services

[ADK Tools and Integrations](<https://adk.dev/integrations/>)

Before building your own tools for ADK, check out the **[ADK Tools and Integrations](<https://adk.dev/integrations/>)** for pre-built tools and integrations you can use with ADK Agents.

## What is a Tool?[¶](<https://adk.dev/tools-custom/#what-is-a-tool> "Permanent link")

In the context of ADK, a Tool represents a specific capability provided to an AI agent, enabling it to perform actions and interact with the world beyond its core text generation and reasoning abilities. What distinguishes capable agents from basic language models is often their effective use of tools.

Technically, a tool is typically a modular code component—**like a Python, Java, or TypeScript function** , a class method, or even another specialized agent—designed to execute a distinct, predefined task. These tasks often involve interacting with external systems or data.

![Agent tool call](https://adk.dev/assets/agent-tool-call.png)

### Key Characteristics[¶](<https://adk.dev/tools-custom/#key-characteristics> "Permanent link")

**Action-Oriented:** Tools perform specific actions for an agent, such as searching for information, calling an API, or performing calculations.

**Extends Agent capabilities:** They empower agents to access real-time information, affect external systems, and overcome the knowledge limitations inherent in their training data.

**Execute predefined logic:** Crucially, tools execute specific, developer-defined logic. They do not possess their own independent reasoning capabilities like the agent's core Large Language Model (LLM). The LLM reasons about which tool to use, when, and with what inputs, but the tool itself just executes its designated function.

## How Agents Use Tools[¶](<https://adk.dev/tools-custom/#how-agents-use-tools> "Permanent link")

Agents leverage tools dynamically through mechanisms often involving function calling. The process generally follows these steps:

  1. **Reasoning:** The agent's LLM analyzes its system instruction, conversation history, and user request.
  2. **Selection:** Based on the analysis, the LLM decides on which tool, if any, to execute, based on the tools available to the agent and the docstrings that describes each tool.
  3. **Invocation:** The LLM generates the required arguments (inputs) for the selected tool and triggers its execution.
  4. **Observation:** The agent receives the output (result) returned by the tool.
  5. **Finalization:** The agent incorporates the tool's output into its ongoing reasoning process to formulate the next response, decide the subsequent step, or determine if the goal has been achieved.

Think of the tools as a specialized toolkit that the agent's intelligent core (the LLM) can access and utilize as needed to accomplish complex tasks.

## Tool Types in ADK[¶](<https://adk.dev/tools-custom/#tool-types-in-adk> "Permanent link")

ADK offers flexibility by supporting several types of tools:

  1. **[Function Tools](<https://adk.dev/tools-custom/function-tools/>):** Tools created by you, tailored to your specific application's needs.
     * **[Functions/Methods](<https://adk.dev/tools-custom/function-tools/#1-function-tool>):** Define standard synchronous functions or methods in your code (e.g., Python def).
     * **[Agents-as-Tools](<https://adk.dev/tools-custom/function-tools/#3-agent-as-a-tool>):** Use another, potentially specialized, agent as a tool for a parent agent.
     * **[Long Running Function Tools](<https://adk.dev/tools-custom/function-tools/#2-long-running-function-tool>):** Support for tools that perform asynchronous operations or take significant time to complete.
  2. **[Built-in Tools](<https://adk.dev/integrations/>):** Ready-to-use tools provided by the framework for common tasks. Examples: Google Search, Code Execution, Retrieval-Augmented Generation (RAG).
  3. **Third-Party Tools:** Integrate tools seamlessly from popular external libraries.

Navigate to the respective documentation pages linked above for detailed information and examples for each tool type.

## Referencing Tool in Agent’s Instructions[¶](<https://adk.dev/tools-custom/#referencing-tool-in-agents-instructions> "Permanent link")

Within an agent's instructions, you can directly reference a tool by using its **function name.** If the tool's **function name** and **docstring** are sufficiently descriptive, your instructions can primarily focus on **when the Large Language Model (LLM) should utilize the tool**. This promotes clarity and helps the model understand the intended use of each tool.

It is **crucial to clearly instruct the agent on how to handle different return values** that a tool might produce. For example, if a tool returns an error message, your instructions should specify whether the agent should retry the operation, give up on the task, or request additional information from the user.

Furthermore, ADK supports the sequential use of tools, where the output of one tool can serve as the input for another. When implementing such workflows, it's important to **describe the intended sequence of tool usage** within the agent's instructions to guide the model through the necessary steps.

### Example[¶](<https://adk.dev/tools-custom/#example> "Permanent link")

The following example showcases how an agent can use tools by **referencing their function names in its instructions**. It also demonstrates how to guide the agent to **handle different return values from tools** , such as success or error messages, and how to orchestrate the **sequential use of multiple tools** to accomplish a task.

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/#__codelineno-0-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-0-2>)#
    [](<https://adk.dev/tools-custom/#__codelineno-0-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-0-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-0-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-0-6>)#
    [](<https://adk.dev/tools-custom/#__codelineno-0-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-0-8>)#
    [](<https://adk.dev/tools-custom/#__codelineno-0-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-0-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-0-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-0-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-0-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-0-14>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-15>)import asyncio
    [](<https://adk.dev/tools-custom/#__codelineno-0-16>)from google.adk.agents import Agent
    [](<https://adk.dev/tools-custom/#__codelineno-0-17>)from google.adk.tools import FunctionTool
    [](<https://adk.dev/tools-custom/#__codelineno-0-18>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/#__codelineno-0-19>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/#__codelineno-0-20>)from google.genai import types
    [](<https://adk.dev/tools-custom/#__codelineno-0-21>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-22>)APP_NAME="weather_sentiment_agent"
    [](<https://adk.dev/tools-custom/#__codelineno-0-23>)USER_ID="user1234"
    [](<https://adk.dev/tools-custom/#__codelineno-0-24>)SESSION_ID="1234"
    [](<https://adk.dev/tools-custom/#__codelineno-0-25>)MODEL_ID="gemini-2.0-flash"
    [](<https://adk.dev/tools-custom/#__codelineno-0-26>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-27>)# Tool 1
    [](<https://adk.dev/tools-custom/#__codelineno-0-28>)def get_weather_report(city: str) -> dict:
    [](<https://adk.dev/tools-custom/#__codelineno-0-29>)    """Retrieves the current weather report for a specified city.
    [](<https://adk.dev/tools-custom/#__codelineno-0-30>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-31>)    Returns:
    [](<https://adk.dev/tools-custom/#__codelineno-0-32>)        dict: A dictionary containing the weather information with a 'status' key ('success' or 'error') and a 'report' key with the weather details if successful, or an 'error_message' if an error occurred.
    [](<https://adk.dev/tools-custom/#__codelineno-0-33>)    """
    [](<https://adk.dev/tools-custom/#__codelineno-0-34>)    if city.lower() == "london":
    [](<https://adk.dev/tools-custom/#__codelineno-0-35>)        return {"status": "success", "report": "The current weather in London is cloudy with a temperature of 18 degrees Celsius and a chance of rain."}
    [](<https://adk.dev/tools-custom/#__codelineno-0-36>)    elif city.lower() == "paris":
    [](<https://adk.dev/tools-custom/#__codelineno-0-37>)        return {"status": "success", "report": "The weather in Paris is sunny with a temperature of 25 degrees Celsius."}
    [](<https://adk.dev/tools-custom/#__codelineno-0-38>)    else:
    [](<https://adk.dev/tools-custom/#__codelineno-0-39>)        return {"status": "error", "error_message": f"Weather information for '{city}' is not available."}
    [](<https://adk.dev/tools-custom/#__codelineno-0-40>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-41>)weather_tool = FunctionTool(func=get_weather_report)
    [](<https://adk.dev/tools-custom/#__codelineno-0-42>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-43>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-44>)# Tool 2
    [](<https://adk.dev/tools-custom/#__codelineno-0-45>)def analyze_sentiment(text: str) -> dict:
    [](<https://adk.dev/tools-custom/#__codelineno-0-46>)    """Analyzes the sentiment of the given text.
    [](<https://adk.dev/tools-custom/#__codelineno-0-47>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-48>)    Returns:
    [](<https://adk.dev/tools-custom/#__codelineno-0-49>)        dict: A dictionary with 'sentiment' ('positive', 'negative', or 'neutral') and a 'confidence' score.
    [](<https://adk.dev/tools-custom/#__codelineno-0-50>)    """
    [](<https://adk.dev/tools-custom/#__codelineno-0-51>)    if "good" in text.lower() or "sunny" in text.lower():
    [](<https://adk.dev/tools-custom/#__codelineno-0-52>)        return {"sentiment": "positive", "confidence": 0.8}
    [](<https://adk.dev/tools-custom/#__codelineno-0-53>)    elif "rain" in text.lower() or "bad" in text.lower():
    [](<https://adk.dev/tools-custom/#__codelineno-0-54>)        return {"sentiment": "negative", "confidence": 0.7}
    [](<https://adk.dev/tools-custom/#__codelineno-0-55>)    else:
    [](<https://adk.dev/tools-custom/#__codelineno-0-56>)        return {"sentiment": "neutral", "confidence": 0.6}
    [](<https://adk.dev/tools-custom/#__codelineno-0-57>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-58>)sentiment_tool = FunctionTool(func=analyze_sentiment)
    [](<https://adk.dev/tools-custom/#__codelineno-0-59>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-60>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-61>)# Agent
    [](<https://adk.dev/tools-custom/#__codelineno-0-62>)weather_sentiment_agent = Agent(
    [](<https://adk.dev/tools-custom/#__codelineno-0-63>)    model=MODEL_ID,
    [](<https://adk.dev/tools-custom/#__codelineno-0-64>)    name='weather_sentiment_agent',
    [](<https://adk.dev/tools-custom/#__codelineno-0-65>)    instruction="""You are a helpful assistant that provides weather information and analyzes the sentiment of user feedback.
    [](<https://adk.dev/tools-custom/#__codelineno-0-66>)**If the user asks about the weather in a specific city, use the 'get_weather_report' tool to retrieve the weather details.**
    [](<https://adk.dev/tools-custom/#__codelineno-0-67>)**If the 'get_weather_report' tool returns a 'success' status, provide the weather report to the user.**
    [](<https://adk.dev/tools-custom/#__codelineno-0-68>)**If the 'get_weather_report' tool returns an 'error' status, inform the user that the weather information for the specified city is not available and ask if they have another city in mind.**
    [](<https://adk.dev/tools-custom/#__codelineno-0-69>)**After providing a weather report, if the user gives feedback on the weather (e.g., 'That's good' or 'I don't like rain'), use the 'analyze_sentiment' tool to understand their sentiment.** Then, briefly acknowledge their sentiment.
    [](<https://adk.dev/tools-custom/#__codelineno-0-70>)You can handle these tasks sequentially if needed.""",
    [](<https://adk.dev/tools-custom/#__codelineno-0-71>)    tools=[weather_tool, sentiment_tool]
    [](<https://adk.dev/tools-custom/#__codelineno-0-72>))
    [](<https://adk.dev/tools-custom/#__codelineno-0-73>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-74>)async def main():
    [](<https://adk.dev/tools-custom/#__codelineno-0-75>)    """Main function to run the agent asynchronously."""
    [](<https://adk.dev/tools-custom/#__codelineno-0-76>)    # Session and Runner Setup
    [](<https://adk.dev/tools-custom/#__codelineno-0-77>)    session_service = InMemorySessionService()
    [](<https://adk.dev/tools-custom/#__codelineno-0-78>)    # Use 'await' to correctly create the session
    [](<https://adk.dev/tools-custom/#__codelineno-0-79>)    await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/tools-custom/#__codelineno-0-80>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-81>)    runner = Runner(agent=weather_sentiment_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/tools-custom/#__codelineno-0-82>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-83>)    # Agent Interaction
    [](<https://adk.dev/tools-custom/#__codelineno-0-84>)    query = "weather in london?"
    [](<https://adk.dev/tools-custom/#__codelineno-0-85>)    print(f"User Query: {query}")
    [](<https://adk.dev/tools-custom/#__codelineno-0-86>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/#__codelineno-0-87>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-88>)    # The runner's run method handles the async loop internally
    [](<https://adk.dev/tools-custom/#__codelineno-0-89>)    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/tools-custom/#__codelineno-0-90>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-91>)    for event in events:
    [](<https://adk.dev/tools-custom/#__codelineno-0-92>)        if event.is_final_response():
    [](<https://adk.dev/tools-custom/#__codelineno-0-93>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/tools-custom/#__codelineno-0-94>)            print("Agent Response:", final_response)
    [](<https://adk.dev/tools-custom/#__codelineno-0-95>)
    [](<https://adk.dev/tools-custom/#__codelineno-0-96>)# Standard way to run the main async function
    [](<https://adk.dev/tools-custom/#__codelineno-0-97>)if __name__ == "__main__":
    [](<https://adk.dev/tools-custom/#__codelineno-0-98>)    asyncio.run(main())
    
    [](<https://adk.dev/tools-custom/#__codelineno-1-1>)/**
    [](<https://adk.dev/tools-custom/#__codelineno-1-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-1-3>) *
    [](<https://adk.dev/tools-custom/#__codelineno-1-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-1-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-1-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-1-7>) *
    [](<https://adk.dev/tools-custom/#__codelineno-1-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-1-9>) *
    [](<https://adk.dev/tools-custom/#__codelineno-1-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-1-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-1-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-1-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-1-14>) * limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-1-15>) */
    [](<https://adk.dev/tools-custom/#__codelineno-1-16>)import { LlmAgent, FunctionTool, InMemoryRunner, isFinalResponse, stringifyContent } from '@google/adk';
    [](<https://adk.dev/tools-custom/#__codelineno-1-17>)import { z } from "zod";
    [](<https://adk.dev/tools-custom/#__codelineno-1-18>)import { Content, createUserContent } from "@google/genai";
    [](<https://adk.dev/tools-custom/#__codelineno-1-19>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-20>)/**
    [](<https://adk.dev/tools-custom/#__codelineno-1-21>) * Retrieves the current weather report for a specified city.
    [](<https://adk.dev/tools-custom/#__codelineno-1-22>) */
    [](<https://adk.dev/tools-custom/#__codelineno-1-23>)function getWeatherReport(params: { city: string }): Record<string, any> {
    [](<https://adk.dev/tools-custom/#__codelineno-1-24>)    if (params.city.toLowerCase().includes("london")) {
    [](<https://adk.dev/tools-custom/#__codelineno-1-25>)        return {
    [](<https://adk.dev/tools-custom/#__codelineno-1-26>)            "status": "success",
    [](<https://adk.dev/tools-custom/#__codelineno-1-27>)            "report": "The current weather in London is cloudy with a " +
    [](<https://adk.dev/tools-custom/#__codelineno-1-28>)                "temperature of 18 degrees Celsius and a chance of rain.",
    [](<https://adk.dev/tools-custom/#__codelineno-1-29>)        };
    [](<https://adk.dev/tools-custom/#__codelineno-1-30>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-1-31>)    if (params.city.toLowerCase().includes("paris")) {
    [](<https://adk.dev/tools-custom/#__codelineno-1-32>)        return {
    [](<https://adk.dev/tools-custom/#__codelineno-1-33>)            "status": "success",
    [](<https://adk.dev/tools-custom/#__codelineno-1-34>)            "report": "The weather in Paris is sunny with a temperature of 25 " +
    [](<https://adk.dev/tools-custom/#__codelineno-1-35>)                "degrees Celsius.",
    [](<https://adk.dev/tools-custom/#__codelineno-1-36>)        };
    [](<https://adk.dev/tools-custom/#__codelineno-1-37>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-1-38>)    return {
    [](<https://adk.dev/tools-custom/#__codelineno-1-39>)        "status": "error",
    [](<https://adk.dev/tools-custom/#__codelineno-1-40>)        "error_message": `Weather information for '${params.city}' is not available.`,
    [](<https://adk.dev/tools-custom/#__codelineno-1-41>)    };
    [](<https://adk.dev/tools-custom/#__codelineno-1-42>)}
    [](<https://adk.dev/tools-custom/#__codelineno-1-43>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-44>)/**
    [](<https://adk.dev/tools-custom/#__codelineno-1-45>) * Analyzes the sentiment of a given text.
    [](<https://adk.dev/tools-custom/#__codelineno-1-46>) */
    [](<https://adk.dev/tools-custom/#__codelineno-1-47>)function analyzeSentiment(params: { text: string }): Record<string, any> {
    [](<https://adk.dev/tools-custom/#__codelineno-1-48>)    if (params.text.includes("cloudy") || params.text.includes("rain")) {
    [](<https://adk.dev/tools-custom/#__codelineno-1-49>)        return { "status": "success", "sentiment": "negative" };
    [](<https://adk.dev/tools-custom/#__codelineno-1-50>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-1-51>)    if (params.text.includes("sunny")) {
    [](<https://adk.dev/tools-custom/#__codelineno-1-52>)        return { "status": "success", "sentiment": "positive" };
    [](<https://adk.dev/tools-custom/#__codelineno-1-53>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-1-54>)    return { "status": "success", "sentiment": "neutral" };
    [](<https://adk.dev/tools-custom/#__codelineno-1-55>)}
    [](<https://adk.dev/tools-custom/#__codelineno-1-56>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-57>)const weatherTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/#__codelineno-1-58>)    name: "get_weather_report",
    [](<https://adk.dev/tools-custom/#__codelineno-1-59>)    description: "Retrieves the current weather report for a specified city.",
    [](<https://adk.dev/tools-custom/#__codelineno-1-60>)    parameters: z.object({
    [](<https://adk.dev/tools-custom/#__codelineno-1-61>)        city: z.string().describe("The city to get the weather for."),
    [](<https://adk.dev/tools-custom/#__codelineno-1-62>)    }),
    [](<https://adk.dev/tools-custom/#__codelineno-1-63>)    execute: getWeatherReport,
    [](<https://adk.dev/tools-custom/#__codelineno-1-64>)});
    [](<https://adk.dev/tools-custom/#__codelineno-1-65>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-66>)const sentimentTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/#__codelineno-1-67>)    name: "analyze_sentiment",
    [](<https://adk.dev/tools-custom/#__codelineno-1-68>)    description: "Analyzes the sentiment of a given text.",
    [](<https://adk.dev/tools-custom/#__codelineno-1-69>)    parameters: z.object({
    [](<https://adk.dev/tools-custom/#__codelineno-1-70>)        text: z.string().describe("The text to analyze the sentiment of."),
    [](<https://adk.dev/tools-custom/#__codelineno-1-71>)    }),
    [](<https://adk.dev/tools-custom/#__codelineno-1-72>)    execute: analyzeSentiment,
    [](<https://adk.dev/tools-custom/#__codelineno-1-73>)});
    [](<https://adk.dev/tools-custom/#__codelineno-1-74>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-75>)const instruction = `
    [](<https://adk.dev/tools-custom/#__codelineno-1-76>)    You are a helpful assistant that first checks the weather and then analyzes
    [](<https://adk.dev/tools-custom/#__codelineno-1-77>)    its sentiment.
    [](<https://adk.dev/tools-custom/#__codelineno-1-78>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-79>)    Follow these steps:
    [](<https://adk.dev/tools-custom/#__codelineno-1-80>)    1. Use the 'get_weather_report' tool to get the weather for the requested
    [](<https://adk.dev/tools-custom/#__codelineno-1-81>)       city.
    [](<https://adk.dev/tools-custom/#__codelineno-1-82>)    2. If the 'get_weather_report' tool returns an error, inform the user about
    [](<https://adk.dev/tools-custom/#__codelineno-1-83>)       the error and stop.
    [](<https://adk.dev/tools-custom/#__codelineno-1-84>)    3. If the weather report is available, use the 'analyze_sentiment' tool to
    [](<https://adk.dev/tools-custom/#__codelineno-1-85>)       determine the sentiment of the weather report.
    [](<https://adk.dev/tools-custom/#__codelineno-1-86>)    4. Finally, provide a summary to the user, including the weather report and
    [](<https://adk.dev/tools-custom/#__codelineno-1-87>)       its sentiment.
    [](<https://adk.dev/tools-custom/#__codelineno-1-88>)    `;
    [](<https://adk.dev/tools-custom/#__codelineno-1-89>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-90>)const agent = new LlmAgent({
    [](<https://adk.dev/tools-custom/#__codelineno-1-91>)    name: "weather_sentiment_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-1-92>)    instruction: instruction,
    [](<https://adk.dev/tools-custom/#__codelineno-1-93>)    tools: [weatherTool, sentimentTool],
    [](<https://adk.dev/tools-custom/#__codelineno-1-94>)    model: "gemini-2.5-flash"
    [](<https://adk.dev/tools-custom/#__codelineno-1-95>)});
    [](<https://adk.dev/tools-custom/#__codelineno-1-96>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-97>)async function main() {
    [](<https://adk.dev/tools-custom/#__codelineno-1-98>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-99>)    const runner = new InMemoryRunner({ agent: agent, appName: "weather_sentiment_app" });
    [](<https://adk.dev/tools-custom/#__codelineno-1-100>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-101>)    await runner.sessionService.createSession({
    [](<https://adk.dev/tools-custom/#__codelineno-1-102>)        appName: "weather_sentiment_app",
    [](<https://adk.dev/tools-custom/#__codelineno-1-103>)        userId: "user1",
    [](<https://adk.dev/tools-custom/#__codelineno-1-104>)        sessionId: "session1"
    [](<https://adk.dev/tools-custom/#__codelineno-1-105>)    });
    [](<https://adk.dev/tools-custom/#__codelineno-1-106>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-107>)    const newMessage: Content = createUserContent("What is the weather in London?");
    [](<https://adk.dev/tools-custom/#__codelineno-1-108>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-109>)    for await (const event of runner.runAsync({
    [](<https://adk.dev/tools-custom/#__codelineno-1-110>)        userId: "user1",
    [](<https://adk.dev/tools-custom/#__codelineno-1-111>)        sessionId: "session1",
    [](<https://adk.dev/tools-custom/#__codelineno-1-112>)        newMessage: newMessage,
    [](<https://adk.dev/tools-custom/#__codelineno-1-113>)    })) {
    [](<https://adk.dev/tools-custom/#__codelineno-1-114>)        if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/tools-custom/#__codelineno-1-115>)            const text = stringifyContent(event).trim();
    [](<https://adk.dev/tools-custom/#__codelineno-1-116>)            if (text) {
    [](<https://adk.dev/tools-custom/#__codelineno-1-117>)                console.log(text);
    [](<https://adk.dev/tools-custom/#__codelineno-1-118>)            }
    [](<https://adk.dev/tools-custom/#__codelineno-1-119>)        }
    [](<https://adk.dev/tools-custom/#__codelineno-1-120>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-1-121>)}
    [](<https://adk.dev/tools-custom/#__codelineno-1-122>)
    [](<https://adk.dev/tools-custom/#__codelineno-1-123>)main();
    
    [](<https://adk.dev/tools-custom/#__codelineno-2-1>)// Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-2-2>)//
    [](<https://adk.dev/tools-custom/#__codelineno-2-3>)// Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-2-4>)// you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-2-5>)// You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-2-6>)//
    [](<https://adk.dev/tools-custom/#__codelineno-2-7>)//     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-2-8>)//
    [](<https://adk.dev/tools-custom/#__codelineno-2-9>)// Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-2-10>)// distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-2-11>)// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-2-12>)// See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-2-13>)// limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-2-14>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-15>)package main
    [](<https://adk.dev/tools-custom/#__codelineno-2-16>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-17>)import (
    [](<https://adk.dev/tools-custom/#__codelineno-2-18>)    "context"
    [](<https://adk.dev/tools-custom/#__codelineno-2-19>)    "fmt"
    [](<https://adk.dev/tools-custom/#__codelineno-2-20>)    "log"
    [](<https://adk.dev/tools-custom/#__codelineno-2-21>)    "strings"
    [](<https://adk.dev/tools-custom/#__codelineno-2-22>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-23>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/#__codelineno-2-24>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/tools-custom/#__codelineno-2-25>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/tools-custom/#__codelineno-2-26>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/tools-custom/#__codelineno-2-27>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/tools-custom/#__codelineno-2-28>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/tools-custom/#__codelineno-2-29>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/tools-custom/#__codelineno-2-30>)    "google.golang.org/genai"
    [](<https://adk.dev/tools-custom/#__codelineno-2-31>))
    [](<https://adk.dev/tools-custom/#__codelineno-2-32>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-33>)type getWeatherReportArgs struct {
    [](<https://adk.dev/tools-custom/#__codelineno-2-34>)    City string `json:"city" jsonschema:"The city for which to get the weather report."`
    [](<https://adk.dev/tools-custom/#__codelineno-2-35>)}
    [](<https://adk.dev/tools-custom/#__codelineno-2-36>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-37>)type getWeatherReportResult struct {
    [](<https://adk.dev/tools-custom/#__codelineno-2-38>)    Status string `json:"status"`
    [](<https://adk.dev/tools-custom/#__codelineno-2-39>)    Report string `json:"report,omitempty"`
    [](<https://adk.dev/tools-custom/#__codelineno-2-40>)}
    [](<https://adk.dev/tools-custom/#__codelineno-2-41>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-42>)func getWeatherReport(ctx agent.Context, args getWeatherReportArgs) (getWeatherReportResult, error) {
    [](<https://adk.dev/tools-custom/#__codelineno-2-43>)    if strings.ToLower(args.City) == "london" {
    [](<https://adk.dev/tools-custom/#__codelineno-2-44>)        return getWeatherReportResult{Status: "success", Report: "The current weather in London is cloudy with a temperature of 18 degrees Celsius and a chance of rain."}, nil
    [](<https://adk.dev/tools-custom/#__codelineno-2-45>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-46>)    if strings.ToLower(args.City) == "paris" {
    [](<https://adk.dev/tools-custom/#__codelineno-2-47>)        return getWeatherReportResult{Status: "success", Report: "The weather in Paris is sunny with a temperature of 25 degrees Celsius."}, nil
    [](<https://adk.dev/tools-custom/#__codelineno-2-48>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-49>)    return getWeatherReportResult{}, fmt.Errorf("weather information for '%s' is not available.", args.City)
    [](<https://adk.dev/tools-custom/#__codelineno-2-50>)}
    [](<https://adk.dev/tools-custom/#__codelineno-2-51>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-52>)type analyzeSentimentArgs struct {
    [](<https://adk.dev/tools-custom/#__codelineno-2-53>)    Text string `json:"text" jsonschema:"The text to analyze for sentiment."`
    [](<https://adk.dev/tools-custom/#__codelineno-2-54>)}
    [](<https://adk.dev/tools-custom/#__codelineno-2-55>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-56>)type analyzeSentimentResult struct {
    [](<https://adk.dev/tools-custom/#__codelineno-2-57>)    Sentiment  string  `json:"sentiment"`
    [](<https://adk.dev/tools-custom/#__codelineno-2-58>)    Confidence float64 `json:"confidence"`
    [](<https://adk.dev/tools-custom/#__codelineno-2-59>)}
    [](<https://adk.dev/tools-custom/#__codelineno-2-60>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-61>)func analyzeSentiment(ctx agent.Context, args analyzeSentimentArgs) (analyzeSentimentResult, error) {
    [](<https://adk.dev/tools-custom/#__codelineno-2-62>)    if strings.Contains(strings.ToLower(args.Text), "good") || strings.Contains(strings.ToLower(args.Text), "sunny") {
    [](<https://adk.dev/tools-custom/#__codelineno-2-63>)        return analyzeSentimentResult{Sentiment: "positive", Confidence: 0.8}, nil
    [](<https://adk.dev/tools-custom/#__codelineno-2-64>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-65>)    if strings.Contains(strings.ToLower(args.Text), "rain") || strings.Contains(strings.ToLower(args.Text), "bad") {
    [](<https://adk.dev/tools-custom/#__codelineno-2-66>)        return analyzeSentimentResult{Sentiment: "negative", Confidence: 0.7}, nil
    [](<https://adk.dev/tools-custom/#__codelineno-2-67>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-68>)    return analyzeSentimentResult{Sentiment: "neutral", Confidence: 0.6}, nil
    [](<https://adk.dev/tools-custom/#__codelineno-2-69>)}
    [](<https://adk.dev/tools-custom/#__codelineno-2-70>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-71>)func main() {
    [](<https://adk.dev/tools-custom/#__codelineno-2-72>)    ctx := context.Background()
    [](<https://adk.dev/tools-custom/#__codelineno-2-73>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/#__codelineno-2-74>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-2-75>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-2-76>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-77>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-78>)    weatherTool, err := functiontool.New(
    [](<https://adk.dev/tools-custom/#__codelineno-2-79>)        functiontool.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-2-80>)            Name:        "get_weather_report",
    [](<https://adk.dev/tools-custom/#__codelineno-2-81>)            Description: "Retrieves the current weather report for a specified city.",
    [](<https://adk.dev/tools-custom/#__codelineno-2-82>)        },
    [](<https://adk.dev/tools-custom/#__codelineno-2-83>)        getWeatherReport,
    [](<https://adk.dev/tools-custom/#__codelineno-2-84>)    )
    [](<https://adk.dev/tools-custom/#__codelineno-2-85>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-2-86>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-2-87>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-88>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-89>)    sentimentTool, err := functiontool.New(
    [](<https://adk.dev/tools-custom/#__codelineno-2-90>)        functiontool.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-2-91>)            Name:        "analyze_sentiment",
    [](<https://adk.dev/tools-custom/#__codelineno-2-92>)            Description: "Analyzes the sentiment of the given text.",
    [](<https://adk.dev/tools-custom/#__codelineno-2-93>)        },
    [](<https://adk.dev/tools-custom/#__codelineno-2-94>)        analyzeSentiment,
    [](<https://adk.dev/tools-custom/#__codelineno-2-95>)    )
    [](<https://adk.dev/tools-custom/#__codelineno-2-96>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-2-97>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-2-98>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-99>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-100>)    weatherSentimentAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-2-101>)        Name:        "weather_sentiment_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-2-102>)        Model:       model,
    [](<https://adk.dev/tools-custom/#__codelineno-2-103>)        Instruction: "You are a helpful assistant that provides weather information and analyzes the sentiment of user feedback. **If the user asks about the weather in a specific city, use the 'get_weather_report' tool to retrieve the weather details.** **If the 'get_weather_report' tool returns a 'success' status, provide the weather report to the user.** **If the 'get_weather_report' tool returns an 'error' status, inform the user that the weather information for the specified city is not available and ask if they have another city in mind.** **After providing a weather report, if the user gives feedback on the weather (e.g., 'That's good' or 'I don't like rain'), use the 'analyze_sentiment' tool to understand their sentiment.** Then, briefly acknowledge their sentiment. You can handle these tasks sequentially if needed.",
    [](<https://adk.dev/tools-custom/#__codelineno-2-104>)        Tools:       []tool.Tool{weatherTool, sentimentTool},
    [](<https://adk.dev/tools-custom/#__codelineno-2-105>)    })
    [](<https://adk.dev/tools-custom/#__codelineno-2-106>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-2-107>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-2-108>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-109>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-110>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/tools-custom/#__codelineno-2-111>)    runner, err := runner.New(runner.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-2-112>)        AppName:        "weather_sentiment_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-2-113>)        Agent:          weatherSentimentAgent,
    [](<https://adk.dev/tools-custom/#__codelineno-2-114>)        SessionService: sessionService,
    [](<https://adk.dev/tools-custom/#__codelineno-2-115>)    })
    [](<https://adk.dev/tools-custom/#__codelineno-2-116>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-2-117>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-2-118>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-119>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-120>)    session, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/tools-custom/#__codelineno-2-121>)        AppName: "weather_sentiment_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-2-122>)        UserID:  "user1234",
    [](<https://adk.dev/tools-custom/#__codelineno-2-123>)    })
    [](<https://adk.dev/tools-custom/#__codelineno-2-124>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-2-125>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-2-126>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-127>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-128>)    run(ctx, runner, session.Session.ID(), "weather in london?")
    [](<https://adk.dev/tools-custom/#__codelineno-2-129>)    run(ctx, runner, session.Session.ID(), "I don't like rain.")
    [](<https://adk.dev/tools-custom/#__codelineno-2-130>)}
    [](<https://adk.dev/tools-custom/#__codelineno-2-131>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-132>)func run(ctx context.Context, r *runner.Runner, sessionID string, prompt string) {
    [](<https://adk.dev/tools-custom/#__codelineno-2-133>)    fmt.Printf("\n> %s\n", prompt)
    [](<https://adk.dev/tools-custom/#__codelineno-2-134>)    events := r.Run(
    [](<https://adk.dev/tools-custom/#__codelineno-2-135>)        ctx,
    [](<https://adk.dev/tools-custom/#__codelineno-2-136>)        "user1234",
    [](<https://adk.dev/tools-custom/#__codelineno-2-137>)        sessionID,
    [](<https://adk.dev/tools-custom/#__codelineno-2-138>)        genai.NewContentFromText(prompt, genai.RoleUser),
    [](<https://adk.dev/tools-custom/#__codelineno-2-139>)        agent.RunConfig{
    [](<https://adk.dev/tools-custom/#__codelineno-2-140>)            StreamingMode: agent.StreamingModeNone,
    [](<https://adk.dev/tools-custom/#__codelineno-2-141>)        },
    [](<https://adk.dev/tools-custom/#__codelineno-2-142>)    )
    [](<https://adk.dev/tools-custom/#__codelineno-2-143>)    for event, err := range events {
    [](<https://adk.dev/tools-custom/#__codelineno-2-144>)        if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-2-145>)            log.Fatalf("ERROR during agent execution: %v", err)
    [](<https://adk.dev/tools-custom/#__codelineno-2-146>)        }
    [](<https://adk.dev/tools-custom/#__codelineno-2-147>)
    [](<https://adk.dev/tools-custom/#__codelineno-2-148>)        if event.Content.Parts[0].Text != "" {
    [](<https://adk.dev/tools-custom/#__codelineno-2-149>)            fmt.Printf("Agent Response: %s\n", event.Content.Parts[0].Text)
    [](<https://adk.dev/tools-custom/#__codelineno-2-150>)        }
    [](<https://adk.dev/tools-custom/#__codelineno-2-151>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-2-152>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-3-1>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/tools-custom/#__codelineno-3-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/#__codelineno-3-3>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/tools-custom/#__codelineno-3-4>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/tools-custom/#__codelineno-3-5>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/tools-custom/#__codelineno-3-6>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/tools-custom/#__codelineno-3-7>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/tools-custom/#__codelineno-3-8>)import com.google.adk.tools.ToolContext; // Ensure this import is correct
    [](<https://adk.dev/tools-custom/#__codelineno-3-9>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/tools-custom/#__codelineno-3-10>)import com.google.genai.types.Content;
    [](<https://adk.dev/tools-custom/#__codelineno-3-11>)import com.google.genai.types.Part;
    [](<https://adk.dev/tools-custom/#__codelineno-3-12>)import java.util.HashMap;
    [](<https://adk.dev/tools-custom/#__codelineno-3-13>)import java.util.Locale;
    [](<https://adk.dev/tools-custom/#__codelineno-3-14>)import java.util.Map;
    [](<https://adk.dev/tools-custom/#__codelineno-3-15>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-16>)public class WeatherSentimentAgentApp {
    [](<https://adk.dev/tools-custom/#__codelineno-3-17>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-18>)  private static final String APP_NAME = "weather_sentiment_agent";
    [](<https://adk.dev/tools-custom/#__codelineno-3-19>)  private static final String USER_ID = "user1234";
    [](<https://adk.dev/tools-custom/#__codelineno-3-20>)  private static final String SESSION_ID = "1234";
    [](<https://adk.dev/tools-custom/#__codelineno-3-21>)  private static final String MODEL_ID = "gemini-2.0-flash";
    [](<https://adk.dev/tools-custom/#__codelineno-3-22>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-23>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-3-24>)   * Retrieves the current weather report for a specified city.
    [](<https://adk.dev/tools-custom/#__codelineno-3-25>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-3-26>)   * @param city The city for which to retrieve the weather report.
    [](<https://adk.dev/tools-custom/#__codelineno-3-27>)   * @param toolContext The context for the tool.
    [](<https://adk.dev/tools-custom/#__codelineno-3-28>)   * @return A dictionary containing the weather information.
    [](<https://adk.dev/tools-custom/#__codelineno-3-29>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-3-30>)  public static Map<String, Object> getWeatherReport(
    [](<https://adk.dev/tools-custom/#__codelineno-3-31>)      @Schema(name = "city")
    [](<https://adk.dev/tools-custom/#__codelineno-3-32>)      String city,
    [](<https://adk.dev/tools-custom/#__codelineno-3-33>)      @Schema(name = "toolContext")
    [](<https://adk.dev/tools-custom/#__codelineno-3-34>)      ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-35>)    Map<String, Object> response = new HashMap<>();
    [](<https://adk.dev/tools-custom/#__codelineno-3-36>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-37>)    if (city.toLowerCase(Locale.ROOT).equals("london")) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-38>)      response.put("status", "success");
    [](<https://adk.dev/tools-custom/#__codelineno-3-39>)      response.put(
    [](<https://adk.dev/tools-custom/#__codelineno-3-40>)          "report",
    [](<https://adk.dev/tools-custom/#__codelineno-3-41>)          "The current weather in London is cloudy with a temperature of 18 degrees Celsius and a"
    [](<https://adk.dev/tools-custom/#__codelineno-3-42>)              + " chance of rain.");
    [](<https://adk.dev/tools-custom/#__codelineno-3-43>)    } else if (city.toLowerCase(Locale.ROOT).equals("paris")) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-44>)      response.put("status", "success");
    [](<https://adk.dev/tools-custom/#__codelineno-3-45>)      response.put(
    [](<https://adk.dev/tools-custom/#__codelineno-3-46>)          "report", "The weather in Paris is sunny with a temperature of 25 degrees Celsius.");
    [](<https://adk.dev/tools-custom/#__codelineno-3-47>)    } else {
    [](<https://adk.dev/tools-custom/#__codelineno-3-48>)      response.put("status", "error");
    [](<https://adk.dev/tools-custom/#__codelineno-3-49>)      response.put(
    [](<https://adk.dev/tools-custom/#__codelineno-3-50>)          "error_message", String.format("Weather information for '%s' is not available.", city));
    [](<https://adk.dev/tools-custom/#__codelineno-3-51>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-3-52>)    return response;
    [](<https://adk.dev/tools-custom/#__codelineno-3-53>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-3-54>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-55>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-3-56>)   * Analyzes the sentiment of the given text.
    [](<https://adk.dev/tools-custom/#__codelineno-3-57>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-3-58>)   * @param text The text to analyze.
    [](<https://adk.dev/tools-custom/#__codelineno-3-59>)   * @param toolContext The context for the tool.
    [](<https://adk.dev/tools-custom/#__codelineno-3-60>)   * @return A dictionary with sentiment and confidence score.
    [](<https://adk.dev/tools-custom/#__codelineno-3-61>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-3-62>)  public static Map<String, Object> analyzeSentiment(
    [](<https://adk.dev/tools-custom/#__codelineno-3-63>)      @Schema(name = "text")
    [](<https://adk.dev/tools-custom/#__codelineno-3-64>)      String text,
    [](<https://adk.dev/tools-custom/#__codelineno-3-65>)      @Schema(name = "toolContext")
    [](<https://adk.dev/tools-custom/#__codelineno-3-66>)      ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-67>)    Map<String, Object> response = new HashMap<>();
    [](<https://adk.dev/tools-custom/#__codelineno-3-68>)    String lowerText = text.toLowerCase(Locale.ROOT);
    [](<https://adk.dev/tools-custom/#__codelineno-3-69>)    if (lowerText.contains("good") || lowerText.contains("sunny")) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-70>)      response.put("sentiment", "positive");
    [](<https://adk.dev/tools-custom/#__codelineno-3-71>)      response.put("confidence", 0.8);
    [](<https://adk.dev/tools-custom/#__codelineno-3-72>)    } else if (lowerText.contains("rain") || lowerText.contains("bad")) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-73>)      response.put("sentiment", "negative");
    [](<https://adk.dev/tools-custom/#__codelineno-3-74>)      response.put("confidence", 0.7);
    [](<https://adk.dev/tools-custom/#__codelineno-3-75>)    } else {
    [](<https://adk.dev/tools-custom/#__codelineno-3-76>)      response.put("sentiment", "neutral");
    [](<https://adk.dev/tools-custom/#__codelineno-3-77>)      response.put("confidence", 0.6);
    [](<https://adk.dev/tools-custom/#__codelineno-3-78>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-3-79>)    return response;
    [](<https://adk.dev/tools-custom/#__codelineno-3-80>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-3-81>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-82>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-3-83>)   * Calls the agent with the given query and prints the final response.
    [](<https://adk.dev/tools-custom/#__codelineno-3-84>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-3-85>)   * @param runner The runner to use.
    [](<https://adk.dev/tools-custom/#__codelineno-3-86>)   * @param query The query to send to the agent.
    [](<https://adk.dev/tools-custom/#__codelineno-3-87>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-3-88>)  public static void callAgent(Runner runner, String query) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-89>)    Content content = Content.fromParts(Part.fromText(query));
    [](<https://adk.dev/tools-custom/#__codelineno-3-90>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-91>)    InMemorySessionService sessionService = (InMemorySessionService) runner.sessionService();
    [](<https://adk.dev/tools-custom/#__codelineno-3-92>)    Session session =
    [](<https://adk.dev/tools-custom/#__codelineno-3-93>)        sessionService
    [](<https://adk.dev/tools-custom/#__codelineno-3-94>)            .createSession(APP_NAME, USER_ID, /* state= */ null, SESSION_ID)
    [](<https://adk.dev/tools-custom/#__codelineno-3-95>)            .blockingGet();
    [](<https://adk.dev/tools-custom/#__codelineno-3-96>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-97>)    runner
    [](<https://adk.dev/tools-custom/#__codelineno-3-98>)        .runAsync(session.userId(), session.id(), content)
    [](<https://adk.dev/tools-custom/#__codelineno-3-99>)        .forEach(
    [](<https://adk.dev/tools-custom/#__codelineno-3-100>)            event -> {
    [](<https://adk.dev/tools-custom/#__codelineno-3-101>)              if (event.finalResponse()
    [](<https://adk.dev/tools-custom/#__codelineno-3-102>)                  && event.content().isPresent()
    [](<https://adk.dev/tools-custom/#__codelineno-3-103>)                  && event.content().get().parts().isPresent()
    [](<https://adk.dev/tools-custom/#__codelineno-3-104>)                  && !event.content().get().parts().get().isEmpty()
    [](<https://adk.dev/tools-custom/#__codelineno-3-105>)                  && event.content().get().parts().get().get(0).text().isPresent()) {
    [](<https://adk.dev/tools-custom/#__codelineno-3-106>)                String finalResponse = event.content().get().parts().get().get(0).text().get();
    [](<https://adk.dev/tools-custom/#__codelineno-3-107>)                System.out.println("Agent Response: " + finalResponse);
    [](<https://adk.dev/tools-custom/#__codelineno-3-108>)              }
    [](<https://adk.dev/tools-custom/#__codelineno-3-109>)            });
    [](<https://adk.dev/tools-custom/#__codelineno-3-110>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-3-111>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-112>)  public static void main(String[] args) throws NoSuchMethodException {
    [](<https://adk.dev/tools-custom/#__codelineno-3-113>)    FunctionTool weatherTool =
    [](<https://adk.dev/tools-custom/#__codelineno-3-114>)        FunctionTool.create(
    [](<https://adk.dev/tools-custom/#__codelineno-3-115>)            WeatherSentimentAgentApp.class.getMethod(
    [](<https://adk.dev/tools-custom/#__codelineno-3-116>)                "getWeatherReport", String.class, ToolContext.class));
    [](<https://adk.dev/tools-custom/#__codelineno-3-117>)    FunctionTool sentimentTool =
    [](<https://adk.dev/tools-custom/#__codelineno-3-118>)        FunctionTool.create(
    [](<https://adk.dev/tools-custom/#__codelineno-3-119>)            WeatherSentimentAgentApp.class.getMethod(
    [](<https://adk.dev/tools-custom/#__codelineno-3-120>)                "analyzeSentiment", String.class, ToolContext.class));
    [](<https://adk.dev/tools-custom/#__codelineno-3-121>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-122>)    BaseAgent weatherSentimentAgent =
    [](<https://adk.dev/tools-custom/#__codelineno-3-123>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/#__codelineno-3-124>)            .model(MODEL_ID)
    [](<https://adk.dev/tools-custom/#__codelineno-3-125>)            .name("weather_sentiment_agent")
    [](<https://adk.dev/tools-custom/#__codelineno-3-126>)            .description("Weather Sentiment Agent")
    [](<https://adk.dev/tools-custom/#__codelineno-3-127>)            .instruction("""
    [](<https://adk.dev/tools-custom/#__codelineno-3-128>)                    You are a helpful assistant that provides weather information and analyzes the
    [](<https://adk.dev/tools-custom/#__codelineno-3-129>)                    sentiment of user feedback
    [](<https://adk.dev/tools-custom/#__codelineno-3-130>)                    **If the user asks about the weather in a specific city, use the
    [](<https://adk.dev/tools-custom/#__codelineno-3-131>)                    'get_weather_report' tool to retrieve the weather details.**
    [](<https://adk.dev/tools-custom/#__codelineno-3-132>)                    **If the 'get_weather_report' tool returns a 'success' status, provide the
    [](<https://adk.dev/tools-custom/#__codelineno-3-133>)                    weather report to the user.**
    [](<https://adk.dev/tools-custom/#__codelineno-3-134>)                    **If the 'get_weather_report' tool returns an 'error' status, inform the
    [](<https://adk.dev/tools-custom/#__codelineno-3-135>)                    user that the weather information for the specified city is not available
    [](<https://adk.dev/tools-custom/#__codelineno-3-136>)                    and ask if they have another city in mind.**
    [](<https://adk.dev/tools-custom/#__codelineno-3-137>)                    **After providing a weather report, if the user gives feedback on the
    [](<https://adk.dev/tools-custom/#__codelineno-3-138>)                    weather (e.g., 'That's good' or 'I don't like rain'), use the
    [](<https://adk.dev/tools-custom/#__codelineno-3-139>)                    'analyze_sentiment' tool to understand their sentiment.** Then, briefly
    [](<https://adk.dev/tools-custom/#__codelineno-3-140>)                    acknowledge their sentiment.
    [](<https://adk.dev/tools-custom/#__codelineno-3-141>)                    You can handle these tasks sequentially if needed.
    [](<https://adk.dev/tools-custom/#__codelineno-3-142>)                    """)
    [](<https://adk.dev/tools-custom/#__codelineno-3-143>)            .tools(ImmutableList.of(weatherTool, sentimentTool))
    [](<https://adk.dev/tools-custom/#__codelineno-3-144>)            .build();
    [](<https://adk.dev/tools-custom/#__codelineno-3-145>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-146>)    InMemorySessionService sessionService = new InMemorySessionService();
    [](<https://adk.dev/tools-custom/#__codelineno-3-147>)    Runner runner = new Runner(weatherSentimentAgent, APP_NAME, null, sessionService);
    [](<https://adk.dev/tools-custom/#__codelineno-3-148>)
    [](<https://adk.dev/tools-custom/#__codelineno-3-149>)    // Change the query to ensure the tool is called with a valid city that triggers a "success"
    [](<https://adk.dev/tools-custom/#__codelineno-3-150>)    // response from the tool, like "london" (without the question mark).
    [](<https://adk.dev/tools-custom/#__codelineno-3-151>)    callAgent(runner, "weather in paris");
    [](<https://adk.dev/tools-custom/#__codelineno-3-152>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-3-153>)}
    
## Tool Context[¶](<https://adk.dev/tools-custom/#tool-context> "Permanent link")

For more advanced scenarios, ADK allows you to access additional contextual information within your tool function by including the special parameter `tool_context: ToolContext`. By including this in the function signature, ADK will **automatically** provide an **instance of the ToolContext** class when your tool is called during agent execution.

The **ToolContext** provides access to several key pieces of information and control levers:

  * `state: State`: Read and modify the current session's state. Changes made here are tracked and persisted.

  * `actions: EventActions`: Influence the agent's subsequent actions after the tool runs (e.g., skip summarization, transfer to another agent).

  * `function_call_id: str`: The unique identifier assigned by the framework to this specific invocation of the tool. Useful for tracking and correlating with authentication responses. This can also be helpful when multiple tools are called within a single model response.

  * `function_call_event_id: str`: This attribute provides the unique identifier of the **event** that triggered the current tool call. This can be useful for tracking and logging purposes.

  * `auth_response: Any`: Contains the authentication response/credentials if an authentication flow was completed before this tool call.

  * Access to Services: Methods to interact with configured services like Artifacts and Memory.

Note that you shouldn't include the `tool_context` parameter in the tool function docstring. Since `ToolContext` is automatically injected by the ADK framework _after_ the LLM decides to call the tool function, it is not relevant for the LLM's decision-making and including it can confuse the LLM.

### **State Management**[¶](<https://adk.dev/tools-custom/#state-management> "Permanent link")

The `tool_context.state` attribute provides direct read and write access to the state associated with the current session. It behaves like a dictionary but ensures that any modifications are tracked as deltas and persisted by the session service. This enables tools to maintain and share information across different interactions and agent steps.

  * **Reading State** : Use standard dictionary access (`tool_context.state['my_key']`) or the `.get()` method (`tool_context.state.get('my_key', default_value)`).

  * **Writing State** : Assign values directly (`tool_context.state['new_key'] = 'new_value'`). These changes are recorded in the state_delta of the resulting event.

  * **State Prefixes** : Remember the standard state prefixes:

    * `app:*`: Shared across all users of the application.

    * `user:*`: Specific to the current user across all their sessions.

    * (No prefix): Specific to the current session.

    * `temp:*`: Temporary, not persisted across invocations (useful for passing data within a single run call but generally less useful inside a tool context which operates between LLM calls).

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/#__codelineno-4-1>)from google.adk.tools import ToolContext, FunctionTool
    [](<https://adk.dev/tools-custom/#__codelineno-4-2>)
    [](<https://adk.dev/tools-custom/#__codelineno-4-3>)def update_user_preference(preference: str, value: str, tool_context: ToolContext):
    [](<https://adk.dev/tools-custom/#__codelineno-4-4>)    """Updates a user-specific preference."""
    [](<https://adk.dev/tools-custom/#__codelineno-4-5>)    user_prefs_key = "user:preferences"
    [](<https://adk.dev/tools-custom/#__codelineno-4-6>)    # Get current preferences or initialize if none exist
    [](<https://adk.dev/tools-custom/#__codelineno-4-7>)    preferences = tool_context.state.get(user_prefs_key, {})
    [](<https://adk.dev/tools-custom/#__codelineno-4-8>)    preferences[preference] = value
    [](<https://adk.dev/tools-custom/#__codelineno-4-9>)    # Write the updated dictionary back to the state
    [](<https://adk.dev/tools-custom/#__codelineno-4-10>)    tool_context.state[user_prefs_key] = preferences
    [](<https://adk.dev/tools-custom/#__codelineno-4-11>)    print(f"Tool: Updated user preference '{preference}' to '{value}'")
    [](<https://adk.dev/tools-custom/#__codelineno-4-12>)    return {"status": "success", "updated_preference": preference}
    [](<https://adk.dev/tools-custom/#__codelineno-4-13>)
    [](<https://adk.dev/tools-custom/#__codelineno-4-14>)pref_tool = FunctionTool(func=update_user_preference)
    [](<https://adk.dev/tools-custom/#__codelineno-4-15>)
    [](<https://adk.dev/tools-custom/#__codelineno-4-16>)# In an Agent:
    [](<https://adk.dev/tools-custom/#__codelineno-4-17>)# my_agent = Agent(..., tools=[pref_tool])
    [](<https://adk.dev/tools-custom/#__codelineno-4-18>)
    [](<https://adk.dev/tools-custom/#__codelineno-4-19>)# When the LLM calls update_user_preference(preference='theme', value='dark', ...):
    [](<https://adk.dev/tools-custom/#__codelineno-4-20>)# The tool_context.state will be updated, and the change will be part of the
    [](<https://adk.dev/tools-custom/#__codelineno-4-21>)# resulting tool response event's actions.state_delta.
    
    [](<https://adk.dev/tools-custom/#__codelineno-5-1>)import { Context } from '@google/adk';
    [](<https://adk.dev/tools-custom/#__codelineno-5-2>)
    [](<https://adk.dev/tools-custom/#__codelineno-5-3>)// Updates a user-specific preference.
    [](<https://adk.dev/tools-custom/#__codelineno-5-4>)export function updateUserThemePreference(
    [](<https://adk.dev/tools-custom/#__codelineno-5-5>)  value: string,
    [](<https://adk.dev/tools-custom/#__codelineno-5-6>)  context: Context
    [](<https://adk.dev/tools-custom/#__codelineno-5-7>)): Record<string, any> {
    [](<https://adk.dev/tools-custom/#__codelineno-5-8>)  const userPrefsKey = "user:preferences";
    [](<https://adk.dev/tools-custom/#__codelineno-5-9>)
    [](<https://adk.dev/tools-custom/#__codelineno-5-10>)  // Get current preferences or initialize if none exist
    [](<https://adk.dev/tools-custom/#__codelineno-5-11>)  const preferences = context.state.get(userPrefsKey, {}) as Record<string, any>;
    [](<https://adk.dev/tools-custom/#__codelineno-5-12>)  preferences["theme"] = value;
    [](<https://adk.dev/tools-custom/#__codelineno-5-13>)
    [](<https://adk.dev/tools-custom/#__codelineno-5-14>)  // Write the updated dictionary back to the state
    [](<https://adk.dev/tools-custom/#__codelineno-5-15>)  context.state.set(userPrefsKey, preferences);
    [](<https://adk.dev/tools-custom/#__codelineno-5-16>)  console.log(
    [](<https://adk.dev/tools-custom/#__codelineno-5-17>)    `Tool: Updated user preference ${userPrefsKey} to ${JSON.stringify(context.state.get(userPrefsKey))}`
    [](<https://adk.dev/tools-custom/#__codelineno-5-18>)  );
    [](<https://adk.dev/tools-custom/#__codelineno-5-19>)
    [](<https://adk.dev/tools-custom/#__codelineno-5-20>)  return {
    [](<https://adk.dev/tools-custom/#__codelineno-5-21>)    status: "success",
    [](<https://adk.dev/tools-custom/#__codelineno-5-22>)    updated_preference: context.state.get(userPrefsKey),
    [](<https://adk.dev/tools-custom/#__codelineno-5-23>)  };
    [](<https://adk.dev/tools-custom/#__codelineno-5-24>)  // When the LLM calls updateUserThemePreference("dark"):
    [](<https://adk.dev/tools-custom/#__codelineno-5-25>)  // The context.state will be updated, and the change will be part of the
    [](<https://adk.dev/tools-custom/#__codelineno-5-26>)  // resulting tool response event's actions.stateDelta.
    [](<https://adk.dev/tools-custom/#__codelineno-5-27>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-6-1>)import (
    [](<https://adk.dev/tools-custom/#__codelineno-6-2>)    "fmt"
    [](<https://adk.dev/tools-custom/#__codelineno-6-3>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-4>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/#__codelineno-6-5>))
    [](<https://adk.dev/tools-custom/#__codelineno-6-6>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-7>)type updateUserPreferenceArgs struct {
    [](<https://adk.dev/tools-custom/#__codelineno-6-8>)    Preference string `json:"preference" jsonschema:"The name of the preference to set."`
    [](<https://adk.dev/tools-custom/#__codelineno-6-9>)    Value      string `json:"value" jsonschema:"The value to set for the preference."`
    [](<https://adk.dev/tools-custom/#__codelineno-6-10>)}
    [](<https://adk.dev/tools-custom/#__codelineno-6-11>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-12>)type updateUserPreferenceResult struct {
    [](<https://adk.dev/tools-custom/#__codelineno-6-13>)    UpdatedPreference string `json:"updated_preference"`
    [](<https://adk.dev/tools-custom/#__codelineno-6-14>)}
    [](<https://adk.dev/tools-custom/#__codelineno-6-15>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-16>)func updateUserPreference(ctx agent.Context, args updateUserPreferenceArgs) (*updateUserPreferenceResult, error) {
    [](<https://adk.dev/tools-custom/#__codelineno-6-17>)    userPrefsKey := "user:preferences"
    [](<https://adk.dev/tools-custom/#__codelineno-6-18>)    val, err := ctx.State().Get(userPrefsKey)
    [](<https://adk.dev/tools-custom/#__codelineno-6-19>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-6-20>)        val = make(map[string]any)
    [](<https://adk.dev/tools-custom/#__codelineno-6-21>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-6-22>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-23>)    preferencesMap, ok := val.(map[string]any)
    [](<https://adk.dev/tools-custom/#__codelineno-6-24>)    if !ok {
    [](<https://adk.dev/tools-custom/#__codelineno-6-25>)        preferencesMap = make(map[string]any)
    [](<https://adk.dev/tools-custom/#__codelineno-6-26>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-6-27>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-28>)    preferencesMap[args.Preference] = args.Value
    [](<https://adk.dev/tools-custom/#__codelineno-6-29>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-30>)    if err := ctx.State().Set(userPrefsKey, preferencesMap); err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-6-31>)        return nil, err
    [](<https://adk.dev/tools-custom/#__codelineno-6-32>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-6-33>)
    [](<https://adk.dev/tools-custom/#__codelineno-6-34>)    fmt.Printf("Tool: Updated user preference '%s' to '%s'\n", args.Preference, args.Value)
    [](<https://adk.dev/tools-custom/#__codelineno-6-35>)    return &updateUserPreferenceResult{
    [](<https://adk.dev/tools-custom/#__codelineno-6-36>)        UpdatedPreference: args.Preference,
    [](<https://adk.dev/tools-custom/#__codelineno-6-37>)    }, nil
    [](<https://adk.dev/tools-custom/#__codelineno-6-38>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-7-1>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/tools-custom/#__codelineno-7-2>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/tools-custom/#__codelineno-7-3>)
    [](<https://adk.dev/tools-custom/#__codelineno-7-4>)// Updates a user-specific preference.
    [](<https://adk.dev/tools-custom/#__codelineno-7-5>)public Map<String, String> updateUserThemePreference(String value, ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-7-6>)  String userPrefsKey = "user:preferences:theme";
    [](<https://adk.dev/tools-custom/#__codelineno-7-7>)
    [](<https://adk.dev/tools-custom/#__codelineno-7-8>)  // Get current preferences or initialize if none exist
    [](<https://adk.dev/tools-custom/#__codelineno-7-9>)  String preference = toolContext.state().getOrDefault(userPrefsKey, "").toString();
    [](<https://adk.dev/tools-custom/#__codelineno-7-10>)  if (preference.isEmpty()) {
    [](<https://adk.dev/tools-custom/#__codelineno-7-11>)    preference = value;
    [](<https://adk.dev/tools-custom/#__codelineno-7-12>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-7-13>)
    [](<https://adk.dev/tools-custom/#__codelineno-7-14>)  // Write the updated dictionary back to the state
    [](<https://adk.dev/tools-custom/#__codelineno-7-15>)  toolContext.state().put("user:preferences", preference);
    [](<https://adk.dev/tools-custom/#__codelineno-7-16>)  System.out.printf("Tool: Updated user preference %s to %s", userPrefsKey, preference);
    [](<https://adk.dev/tools-custom/#__codelineno-7-17>)
    [](<https://adk.dev/tools-custom/#__codelineno-7-18>)  return Map.of("status", "success", "updated_preference", toolContext.state().get(userPrefsKey).toString());
    [](<https://adk.dev/tools-custom/#__codelineno-7-19>)  // When the LLM calls updateUserThemePreference("dark"):
    [](<https://adk.dev/tools-custom/#__codelineno-7-20>)  // The toolContext.state will be updated, and the change will be part of the
    [](<https://adk.dev/tools-custom/#__codelineno-7-21>)  // resulting tool response event's actions.stateDelta.
    [](<https://adk.dev/tools-custom/#__codelineno-7-22>)}
    
### **Controlling Agent Flow**[¶](<https://adk.dev/tools-custom/#controlling-agent-flow> "Permanent link")

The `tool_context.actions` attribute in Python and TypeScript, `ToolContext.actions()` in Java, and `tool.Context.Actions()` in Go, holds an **EventActions** object. Modifying attributes on this object allows your tool to influence what the agent or framework does after the tool finishes execution.

  * **`skip_summarization: bool`** : (Default: False) If set to True, instructs the ADK to bypass the LLM call that typically summarizes the tool's output. This is useful if your tool's return value is already a user-ready message.

  * **`transfer_to_agent: str`** : Set this to the name of another agent. The framework will halt the current agent's execution and **transfer control of the conversation to the specified agent**. This allows tools to dynamically hand off tasks to more specialized agents.

  * **`escalate: bool`** : (Default: False) Setting this to True signals that the current agent cannot handle the request and should pass control up to its parent agent (if in a hierarchy). In a LoopAgent, setting **escalate=True** in a sub-agent's tool will terminate the loop.

#### Example[¶](<https://adk.dev/tools-custom/#example_1> "Permanent link")

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/#__codelineno-8-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-8-2>)#
    [](<https://adk.dev/tools-custom/#__codelineno-8-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-8-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-8-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-8-6>)#
    [](<https://adk.dev/tools-custom/#__codelineno-8-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-8-8>)#
    [](<https://adk.dev/tools-custom/#__codelineno-8-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-8-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-8-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-8-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-8-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-8-14>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-15>)from google.adk.agents import Agent
    [](<https://adk.dev/tools-custom/#__codelineno-8-16>)from google.adk.tools import FunctionTool
    [](<https://adk.dev/tools-custom/#__codelineno-8-17>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/#__codelineno-8-18>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/#__codelineno-8-19>)from google.adk.tools import ToolContext
    [](<https://adk.dev/tools-custom/#__codelineno-8-20>)from google.genai import types
    [](<https://adk.dev/tools-custom/#__codelineno-8-21>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-22>)APP_NAME="customer_support_agent"
    [](<https://adk.dev/tools-custom/#__codelineno-8-23>)USER_ID="user1234"
    [](<https://adk.dev/tools-custom/#__codelineno-8-24>)SESSION_ID="1234"
    [](<https://adk.dev/tools-custom/#__codelineno-8-25>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-26>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-27>)def check_and_transfer(query: str, tool_context: ToolContext) -> str:
    [](<https://adk.dev/tools-custom/#__codelineno-8-28>)    """Checks if the query requires escalation and transfers to another agent if needed."""
    [](<https://adk.dev/tools-custom/#__codelineno-8-29>)    if "urgent" in query.lower():
    [](<https://adk.dev/tools-custom/#__codelineno-8-30>)        print("Tool: Detected urgency, transferring to the support agent.")
    [](<https://adk.dev/tools-custom/#__codelineno-8-31>)        tool_context.actions.transfer_to_agent = "support_agent"
    [](<https://adk.dev/tools-custom/#__codelineno-8-32>)        return "Transferring to the support agent..."
    [](<https://adk.dev/tools-custom/#__codelineno-8-33>)    else:
    [](<https://adk.dev/tools-custom/#__codelineno-8-34>)        return f"Processed query: '{query}'. No further action needed."
    [](<https://adk.dev/tools-custom/#__codelineno-8-35>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-36>)escalation_tool = FunctionTool(func=check_and_transfer)
    [](<https://adk.dev/tools-custom/#__codelineno-8-37>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-38>)main_agent = Agent(
    [](<https://adk.dev/tools-custom/#__codelineno-8-39>)    model='gemini-2.0-flash',
    [](<https://adk.dev/tools-custom/#__codelineno-8-40>)    name='main_agent',
    [](<https://adk.dev/tools-custom/#__codelineno-8-41>)    instruction="""You are the first point of contact for customer support of an analytics tool. Answer general queries. If the user indicates urgency, use the 'escalation_tool' tool.""",
    [](<https://adk.dev/tools-custom/#__codelineno-8-42>)    tools=[escalation_tool]
    [](<https://adk.dev/tools-custom/#__codelineno-8-43>))
    [](<https://adk.dev/tools-custom/#__codelineno-8-44>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-45>)support_agent = Agent(
    [](<https://adk.dev/tools-custom/#__codelineno-8-46>)    model='gemini-2.0-flash',
    [](<https://adk.dev/tools-custom/#__codelineno-8-47>)    name='support_agent',
    [](<https://adk.dev/tools-custom/#__codelineno-8-48>)    instruction="""You are the dedicated support agent. Mentioned you are a support handler and please help the user with their urgent issue."""
    [](<https://adk.dev/tools-custom/#__codelineno-8-49>))
    [](<https://adk.dev/tools-custom/#__codelineno-8-50>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-51>)main_agent.sub_agents = [support_agent]
    [](<https://adk.dev/tools-custom/#__codelineno-8-52>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-53>)# Session and Runner
    [](<https://adk.dev/tools-custom/#__codelineno-8-54>)async def setup_session_and_runner():
    [](<https://adk.dev/tools-custom/#__codelineno-8-55>)    session_service = InMemorySessionService()
    [](<https://adk.dev/tools-custom/#__codelineno-8-56>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/tools-custom/#__codelineno-8-57>)    runner = Runner(agent=main_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/tools-custom/#__codelineno-8-58>)    return session, runner
    [](<https://adk.dev/tools-custom/#__codelineno-8-59>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-60>)# Agent Interaction
    [](<https://adk.dev/tools-custom/#__codelineno-8-61>)async def call_agent_async(query):
    [](<https://adk.dev/tools-custom/#__codelineno-8-62>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/#__codelineno-8-63>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/tools-custom/#__codelineno-8-64>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/tools-custom/#__codelineno-8-65>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-66>)    async for event in events:
    [](<https://adk.dev/tools-custom/#__codelineno-8-67>)        if event.is_final_response():
    [](<https://adk.dev/tools-custom/#__codelineno-8-68>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/tools-custom/#__codelineno-8-69>)            print("Agent Response: ", final_response)
    [](<https://adk.dev/tools-custom/#__codelineno-8-70>)
    [](<https://adk.dev/tools-custom/#__codelineno-8-71>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/tools-custom/#__codelineno-8-72>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/tools-custom/#__codelineno-8-73>)await call_agent_async("this is urgent, i cant login")
    
    [](<https://adk.dev/tools-custom/#__codelineno-9-1>)/**
    [](<https://adk.dev/tools-custom/#__codelineno-9-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-9-3>) *
    [](<https://adk.dev/tools-custom/#__codelineno-9-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-9-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-9-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-9-7>) *
    [](<https://adk.dev/tools-custom/#__codelineno-9-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-9-9>) *
    [](<https://adk.dev/tools-custom/#__codelineno-9-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-9-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-9-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-9-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-9-14>) * limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-9-15>) */
    [](<https://adk.dev/tools-custom/#__codelineno-9-16>)import { LlmAgent, FunctionTool, Context, InMemoryRunner, isFinalResponse, stringifyContent } from '@google/adk';
    [](<https://adk.dev/tools-custom/#__codelineno-9-17>)import { z } from "zod";
    [](<https://adk.dev/tools-custom/#__codelineno-9-18>)import { Content, createUserContent } from "@google/genai";
    [](<https://adk.dev/tools-custom/#__codelineno-9-19>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-20>)function checkAndTransfer(
    [](<https://adk.dev/tools-custom/#__codelineno-9-21>)  params: { query: string },
    [](<https://adk.dev/tools-custom/#__codelineno-9-22>)  context?: Context
    [](<https://adk.dev/tools-custom/#__codelineno-9-23>)): Record<string, any> {
    [](<https://adk.dev/tools-custom/#__codelineno-9-24>)  if (!context) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-25>)    // This should not happen in a normal ADK flow where the tool is called by an agent.
    [](<https://adk.dev/tools-custom/#__codelineno-9-26>)    throw new Error("Context is required to transfer agents.");
    [](<https://adk.dev/tools-custom/#__codelineno-9-27>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-9-28>)  if (params.query.toLowerCase().includes("urgent")) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-29>)    console.log("Tool: Urgent query detected, transferring to support_agent.");
    [](<https://adk.dev/tools-custom/#__codelineno-9-30>)    context.actions.transferToAgent = "support_agent";
    [](<https://adk.dev/tools-custom/#__codelineno-9-31>)    return { status: "success", message: "Transferring to support agent." };
    [](<https://adk.dev/tools-custom/#__codelineno-9-32>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-9-33>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-34>)  console.log("Tool: Query is not urgent, handling normally.");
    [](<https://adk.dev/tools-custom/#__codelineno-9-35>)  return { status: "success", message: "Query will be handled by the main agent." };
    [](<https://adk.dev/tools-custom/#__codelineno-9-36>)}
    [](<https://adk.dev/tools-custom/#__codelineno-9-37>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-38>)const transferTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/#__codelineno-9-39>)  name: "check_and_transfer",
    [](<https://adk.dev/tools-custom/#__codelineno-9-40>)  description: "Checks the user's query and transfers to a support agent if urgent.",
    [](<https://adk.dev/tools-custom/#__codelineno-9-41>)  parameters: z.object({
    [](<https://adk.dev/tools-custom/#__codelineno-9-42>)    query: z.string().describe("The user query to analyze."),
    [](<https://adk.dev/tools-custom/#__codelineno-9-43>)  }),
    [](<https://adk.dev/tools-custom/#__codelineno-9-44>)  execute: checkAndTransfer,
    [](<https://adk.dev/tools-custom/#__codelineno-9-45>)});
    [](<https://adk.dev/tools-custom/#__codelineno-9-46>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-47>)const supportAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/#__codelineno-9-48>)  name: "support_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-9-49>)  description: "Handles urgent user requests about accounts.",
    [](<https://adk.dev/tools-custom/#__codelineno-9-50>)  instruction: "You are the support agent. Handle the user's urgent request.",
    [](<https://adk.dev/tools-custom/#__codelineno-9-51>)  model: "gemini-2.5-flash"
    [](<https://adk.dev/tools-custom/#__codelineno-9-52>)});
    [](<https://adk.dev/tools-custom/#__codelineno-9-53>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-54>)const mainAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/#__codelineno-9-55>)  name: "main_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-9-56>)  description: "The main agent that routes non-urgent queries.",
    [](<https://adk.dev/tools-custom/#__codelineno-9-57>)  instruction: "You are the main agent. Use the check_and_transfer tool to analyze the user query. If the query is not urgent, handle it yourself.",
    [](<https://adk.dev/tools-custom/#__codelineno-9-58>)  tools: [transferTool],
    [](<https://adk.dev/tools-custom/#__codelineno-9-59>)  subAgents: [supportAgent],
    [](<https://adk.dev/tools-custom/#__codelineno-9-60>)  model: "gemini-2.5-flash"
    [](<https://adk.dev/tools-custom/#__codelineno-9-61>)});
    [](<https://adk.dev/tools-custom/#__codelineno-9-62>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-63>)async function main() {
    [](<https://adk.dev/tools-custom/#__codelineno-9-64>)  const runner = new InMemoryRunner({ agent: mainAgent, appName: "customer_support_app" });
    [](<https://adk.dev/tools-custom/#__codelineno-9-65>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-66>)  console.log("--- Running with a non-urgent query ---");
    [](<https://adk.dev/tools-custom/#__codelineno-9-67>)  await runner.sessionService.createSession({ appName: "customer_support_app", userId: "user1", sessionId: "session1" });
    [](<https://adk.dev/tools-custom/#__codelineno-9-68>)  const nonUrgentMessage: Content = createUserContent("I have a general question about my account.");
    [](<https://adk.dev/tools-custom/#__codelineno-9-69>)  for await (const event of runner.runAsync({ userId: "user1", sessionId: "session1", newMessage: nonUrgentMessage })) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-70>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-71>)      const text = stringifyContent(event).trim();
    [](<https://adk.dev/tools-custom/#__codelineno-9-72>)      if (text) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-73>)        console.log(`Final Response: ${text}`);
    [](<https://adk.dev/tools-custom/#__codelineno-9-74>)      }
    [](<https://adk.dev/tools-custom/#__codelineno-9-75>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-9-76>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-9-77>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-78>)  console.log("\n--- Running with an urgent query ---");
    [](<https://adk.dev/tools-custom/#__codelineno-9-79>)  await runner.sessionService.createSession({ appName: "customer_support_app", userId: "user1", sessionId: "session2" });
    [](<https://adk.dev/tools-custom/#__codelineno-9-80>)  const urgentMessage: Content = createUserContent("My account is locked and this is urgent!");
    [](<https://adk.dev/tools-custom/#__codelineno-9-81>)  for await (const event of runner.runAsync({ userId: "user1", sessionId: "session2", newMessage: urgentMessage })) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-82>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-83>)      const text = stringifyContent(event).trim();
    [](<https://adk.dev/tools-custom/#__codelineno-9-84>)      if (text) {
    [](<https://adk.dev/tools-custom/#__codelineno-9-85>)        console.log(`Final Response: ${text}`);
    [](<https://adk.dev/tools-custom/#__codelineno-9-86>)      }
    [](<https://adk.dev/tools-custom/#__codelineno-9-87>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-9-88>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-9-89>)}
    [](<https://adk.dev/tools-custom/#__codelineno-9-90>)
    [](<https://adk.dev/tools-custom/#__codelineno-9-91>)main();
    
    [](<https://adk.dev/tools-custom/#__codelineno-10-1>)// Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-10-2>)//
    [](<https://adk.dev/tools-custom/#__codelineno-10-3>)// Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-10-4>)// you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-10-5>)// You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-10-6>)//
    [](<https://adk.dev/tools-custom/#__codelineno-10-7>)//     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-10-8>)//
    [](<https://adk.dev/tools-custom/#__codelineno-10-9>)// Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-10-10>)// distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-10-11>)// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-10-12>)// See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-10-13>)// limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-10-14>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-15>)package main
    [](<https://adk.dev/tools-custom/#__codelineno-10-16>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-17>)import (
    [](<https://adk.dev/tools-custom/#__codelineno-10-18>)    "context"
    [](<https://adk.dev/tools-custom/#__codelineno-10-19>)    "fmt"
    [](<https://adk.dev/tools-custom/#__codelineno-10-20>)    "log"
    [](<https://adk.dev/tools-custom/#__codelineno-10-21>)    "strings"
    [](<https://adk.dev/tools-custom/#__codelineno-10-22>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-23>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/#__codelineno-10-24>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/tools-custom/#__codelineno-10-25>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/tools-custom/#__codelineno-10-26>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/tools-custom/#__codelineno-10-27>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/tools-custom/#__codelineno-10-28>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/tools-custom/#__codelineno-10-29>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/tools-custom/#__codelineno-10-30>)    "google.golang.org/genai"
    [](<https://adk.dev/tools-custom/#__codelineno-10-31>))
    [](<https://adk.dev/tools-custom/#__codelineno-10-32>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-33>)type checkAndTransferArgs struct {
    [](<https://adk.dev/tools-custom/#__codelineno-10-34>)    Query string `json:"query" jsonschema:"The user's query to check for urgency."`
    [](<https://adk.dev/tools-custom/#__codelineno-10-35>)}
    [](<https://adk.dev/tools-custom/#__codelineno-10-36>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-37>)type checkAndTransferResult struct {
    [](<https://adk.dev/tools-custom/#__codelineno-10-38>)    Status string `json:"status"`
    [](<https://adk.dev/tools-custom/#__codelineno-10-39>)}
    [](<https://adk.dev/tools-custom/#__codelineno-10-40>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-41>)func checkAndTransfer(ctx agent.Context, args checkAndTransferArgs) (checkAndTransferResult, error) {
    [](<https://adk.dev/tools-custom/#__codelineno-10-42>)    if strings.Contains(strings.ToLower(args.Query), "urgent") {
    [](<https://adk.dev/tools-custom/#__codelineno-10-43>)        fmt.Println("Tool: Detected urgency, transferring to the support agent.")
    [](<https://adk.dev/tools-custom/#__codelineno-10-44>)        ctx.Actions().TransferToAgent = "support_agent"
    [](<https://adk.dev/tools-custom/#__codelineno-10-45>)        return checkAndTransferResult{Status: "Transferring to the support agent..."}, nil
    [](<https://adk.dev/tools-custom/#__codelineno-10-46>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-47>)    return checkAndTransferResult{Status: fmt.Sprintf("Processed query: '%s'. No further action needed.", args.Query)}, nil
    [](<https://adk.dev/tools-custom/#__codelineno-10-48>)}
    [](<https://adk.dev/tools-custom/#__codelineno-10-49>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-50>)func main() {
    [](<https://adk.dev/tools-custom/#__codelineno-10-51>)    ctx := context.Background()
    [](<https://adk.dev/tools-custom/#__codelineno-10-52>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{})
    [](<https://adk.dev/tools-custom/#__codelineno-10-53>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-10-54>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-10-55>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-56>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-57>)    supportAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-10-58>)        Name:        "support_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-10-59>)        Model:       model,
    [](<https://adk.dev/tools-custom/#__codelineno-10-60>)        Instruction: "You are the dedicated support agent. Mentioned you are a support handler and please help the user with their urgent issue.",
    [](<https://adk.dev/tools-custom/#__codelineno-10-61>)    })
    [](<https://adk.dev/tools-custom/#__codelineno-10-62>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-10-63>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-10-64>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-65>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-66>)    checkAndTransferTool, err := functiontool.New(
    [](<https://adk.dev/tools-custom/#__codelineno-10-67>)        functiontool.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-10-68>)            Name:        "check_and_transfer",
    [](<https://adk.dev/tools-custom/#__codelineno-10-69>)            Description: "Checks if the query requires escalation and transfers to another agent if needed.",
    [](<https://adk.dev/tools-custom/#__codelineno-10-70>)        },
    [](<https://adk.dev/tools-custom/#__codelineno-10-71>)        checkAndTransfer,
    [](<https://adk.dev/tools-custom/#__codelineno-10-72>)    )
    [](<https://adk.dev/tools-custom/#__codelineno-10-73>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-10-74>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-10-75>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-76>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-77>)    mainAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-10-78>)        Name:        "main_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-10-79>)        Model:       model,
    [](<https://adk.dev/tools-custom/#__codelineno-10-80>)        Instruction: "You are the first point of contact for customer support of an analytics tool. Answer general queries. If the user indicates urgency, use the 'check_and_transfer' tool.",
    [](<https://adk.dev/tools-custom/#__codelineno-10-81>)        Tools:       []tool.Tool{checkAndTransferTool},
    [](<https://adk.dev/tools-custom/#__codelineno-10-82>)        SubAgents:   []agent.Agent{supportAgent},
    [](<https://adk.dev/tools-custom/#__codelineno-10-83>)    })
    [](<https://adk.dev/tools-custom/#__codelineno-10-84>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-10-85>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-10-86>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-87>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-88>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/tools-custom/#__codelineno-10-89>)    runner, err := runner.New(runner.Config{
    [](<https://adk.dev/tools-custom/#__codelineno-10-90>)        AppName:        "customer_support_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-10-91>)        Agent:          mainAgent,
    [](<https://adk.dev/tools-custom/#__codelineno-10-92>)        SessionService: sessionService,
    [](<https://adk.dev/tools-custom/#__codelineno-10-93>)    })
    [](<https://adk.dev/tools-custom/#__codelineno-10-94>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-10-95>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-10-96>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-97>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-98>)    session, err := sessionService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/tools-custom/#__codelineno-10-99>)        AppName: "customer_support_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-10-100>)        UserID:  "user1234",
    [](<https://adk.dev/tools-custom/#__codelineno-10-101>)    })
    [](<https://adk.dev/tools-custom/#__codelineno-10-102>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-10-103>)        log.Fatal(err)
    [](<https://adk.dev/tools-custom/#__codelineno-10-104>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-105>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-106>)    run(ctx, runner, session.Session.ID(), "this is urgent, i cant login")
    [](<https://adk.dev/tools-custom/#__codelineno-10-107>)}
    [](<https://adk.dev/tools-custom/#__codelineno-10-108>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-109>)func run(ctx context.Context, r *runner.Runner, sessionID string, prompt string) {
    [](<https://adk.dev/tools-custom/#__codelineno-10-110>)    fmt.Printf("\n> %s\n", prompt)
    [](<https://adk.dev/tools-custom/#__codelineno-10-111>)    events := r.Run(
    [](<https://adk.dev/tools-custom/#__codelineno-10-112>)        ctx,
    [](<https://adk.dev/tools-custom/#__codelineno-10-113>)        "user1234",
    [](<https://adk.dev/tools-custom/#__codelineno-10-114>)        sessionID,
    [](<https://adk.dev/tools-custom/#__codelineno-10-115>)        genai.NewContentFromText(prompt, genai.RoleUser),
    [](<https://adk.dev/tools-custom/#__codelineno-10-116>)        agent.RunConfig{
    [](<https://adk.dev/tools-custom/#__codelineno-10-117>)            StreamingMode: agent.StreamingModeNone,
    [](<https://adk.dev/tools-custom/#__codelineno-10-118>)        },
    [](<https://adk.dev/tools-custom/#__codelineno-10-119>)    )
    [](<https://adk.dev/tools-custom/#__codelineno-10-120>)    for event, err := range events {
    [](<https://adk.dev/tools-custom/#__codelineno-10-121>)        if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-10-122>)            log.Fatalf("ERROR during agent execution: %v", err)
    [](<https://adk.dev/tools-custom/#__codelineno-10-123>)        }
    [](<https://adk.dev/tools-custom/#__codelineno-10-124>)
    [](<https://adk.dev/tools-custom/#__codelineno-10-125>)        if event.Content.Parts[0].Text != "" {
    [](<https://adk.dev/tools-custom/#__codelineno-10-126>)            fmt.Printf("Agent Response: %s\n", event.Content.Parts[0].Text)
    [](<https://adk.dev/tools-custom/#__codelineno-10-127>)        }
    [](<https://adk.dev/tools-custom/#__codelineno-10-128>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-10-129>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-11-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/#__codelineno-11-2>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/tools-custom/#__codelineno-11-3>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/tools-custom/#__codelineno-11-4>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/tools-custom/#__codelineno-11-5>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/tools-custom/#__codelineno-11-6>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/tools-custom/#__codelineno-11-7>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/tools-custom/#__codelineno-11-8>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/tools-custom/#__codelineno-11-9>)import com.google.genai.types.Content;
    [](<https://adk.dev/tools-custom/#__codelineno-11-10>)import com.google.genai.types.Part;
    [](<https://adk.dev/tools-custom/#__codelineno-11-11>)import java.util.HashMap;
    [](<https://adk.dev/tools-custom/#__codelineno-11-12>)import java.util.Locale;
    [](<https://adk.dev/tools-custom/#__codelineno-11-13>)import java.util.Map;
    [](<https://adk.dev/tools-custom/#__codelineno-11-14>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-15>)public class CustomerSupportAgentApp {
    [](<https://adk.dev/tools-custom/#__codelineno-11-16>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-17>)  private static final String APP_NAME = "customer_support_agent";
    [](<https://adk.dev/tools-custom/#__codelineno-11-18>)  private static final String USER_ID = "user1234";
    [](<https://adk.dev/tools-custom/#__codelineno-11-19>)  private static final String SESSION_ID = "1234";
    [](<https://adk.dev/tools-custom/#__codelineno-11-20>)  private static final String MODEL_ID = "gemini-2.0-flash";
    [](<https://adk.dev/tools-custom/#__codelineno-11-21>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-22>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-11-23>)   * Checks if the query requires escalation and transfers to another agent if needed.
    [](<https://adk.dev/tools-custom/#__codelineno-11-24>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-11-25>)   * @param query The user's query.
    [](<https://adk.dev/tools-custom/#__codelineno-11-26>)   * @param toolContext The context for the tool.
    [](<https://adk.dev/tools-custom/#__codelineno-11-27>)   * @return A map indicating the result of the check and transfer.
    [](<https://adk.dev/tools-custom/#__codelineno-11-28>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-11-29>)  public static Map<String, Object> checkAndTransfer(
    [](<https://adk.dev/tools-custom/#__codelineno-11-30>)      @Schema(name = "query", description = "the user query")
    [](<https://adk.dev/tools-custom/#__codelineno-11-31>)      String query,
    [](<https://adk.dev/tools-custom/#__codelineno-11-32>)      @Schema(name = "toolContext", description = "the tool context")
    [](<https://adk.dev/tools-custom/#__codelineno-11-33>)      ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-11-34>)    Map<String, Object> response = new HashMap<>();
    [](<https://adk.dev/tools-custom/#__codelineno-11-35>)    if (query.toLowerCase(Locale.ROOT).contains("urgent")) {
    [](<https://adk.dev/tools-custom/#__codelineno-11-36>)      System.out.println("Tool: Detected urgency, transferring to the support agent.");
    [](<https://adk.dev/tools-custom/#__codelineno-11-37>)      toolContext.actions().setTransferToAgent("support_agent");
    [](<https://adk.dev/tools-custom/#__codelineno-11-38>)      response.put("status", "transferring");
    [](<https://adk.dev/tools-custom/#__codelineno-11-39>)      response.put("message", "Transferring to the support agent...");
    [](<https://adk.dev/tools-custom/#__codelineno-11-40>)    } else {
    [](<https://adk.dev/tools-custom/#__codelineno-11-41>)      response.put("status", "processed");
    [](<https://adk.dev/tools-custom/#__codelineno-11-42>)      response.put(
    [](<https://adk.dev/tools-custom/#__codelineno-11-43>)          "message", String.format("Processed query: '%s'. No further action needed.", query));
    [](<https://adk.dev/tools-custom/#__codelineno-11-44>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-11-45>)    return response;
    [](<https://adk.dev/tools-custom/#__codelineno-11-46>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-11-47>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-48>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-11-49>)   * Calls the agent with the given query and prints the final response.
    [](<https://adk.dev/tools-custom/#__codelineno-11-50>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-11-51>)   * @param runner The runner to use.
    [](<https://adk.dev/tools-custom/#__codelineno-11-52>)   * @param query The query to send to the agent.
    [](<https://adk.dev/tools-custom/#__codelineno-11-53>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-11-54>)  public static void callAgent(Runner runner, String query) {
    [](<https://adk.dev/tools-custom/#__codelineno-11-55>)    Content content =
    [](<https://adk.dev/tools-custom/#__codelineno-11-56>)        Content.fromParts(Part.fromText(query));
    [](<https://adk.dev/tools-custom/#__codelineno-11-57>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-58>)    InMemorySessionService sessionService = (InMemorySessionService) runner.sessionService();
    [](<https://adk.dev/tools-custom/#__codelineno-11-59>)    // Fixed: session ID does not need to be an optional.
    [](<https://adk.dev/tools-custom/#__codelineno-11-60>)    Session session =
    [](<https://adk.dev/tools-custom/#__codelineno-11-61>)        sessionService
    [](<https://adk.dev/tools-custom/#__codelineno-11-62>)            .createSession(APP_NAME, USER_ID, /* state= */ null, SESSION_ID)
    [](<https://adk.dev/tools-custom/#__codelineno-11-63>)            .blockingGet();
    [](<https://adk.dev/tools-custom/#__codelineno-11-64>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-65>)    runner
    [](<https://adk.dev/tools-custom/#__codelineno-11-66>)        .runAsync(session.userId(), session.id(), content)
    [](<https://adk.dev/tools-custom/#__codelineno-11-67>)        .forEach(
    [](<https://adk.dev/tools-custom/#__codelineno-11-68>)            event -> {
    [](<https://adk.dev/tools-custom/#__codelineno-11-69>)              if (event.finalResponse()
    [](<https://adk.dev/tools-custom/#__codelineno-11-70>)                  && event.content().isPresent()
    [](<https://adk.dev/tools-custom/#__codelineno-11-71>)                  && event.content().get().parts().isPresent()
    [](<https://adk.dev/tools-custom/#__codelineno-11-72>)                  && !event.content().get().parts().get().isEmpty()
    [](<https://adk.dev/tools-custom/#__codelineno-11-73>)                  && event.content().get().parts().get().get(0).text().isPresent()) {
    [](<https://adk.dev/tools-custom/#__codelineno-11-74>)                String finalResponse = event.content().get().parts().get().get(0).text().get();
    [](<https://adk.dev/tools-custom/#__codelineno-11-75>)                System.out.println("Agent Response: " + finalResponse);
    [](<https://adk.dev/tools-custom/#__codelineno-11-76>)              }
    [](<https://adk.dev/tools-custom/#__codelineno-11-77>)            });
    [](<https://adk.dev/tools-custom/#__codelineno-11-78>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-11-79>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-80>)  public static void main(String[] args) throws NoSuchMethodException {
    [](<https://adk.dev/tools-custom/#__codelineno-11-81>)    FunctionTool escalationTool =
    [](<https://adk.dev/tools-custom/#__codelineno-11-82>)        FunctionTool.create(
    [](<https://adk.dev/tools-custom/#__codelineno-11-83>)            CustomerSupportAgentApp.class.getMethod(
    [](<https://adk.dev/tools-custom/#__codelineno-11-84>)                "checkAndTransfer", String.class, ToolContext.class));
    [](<https://adk.dev/tools-custom/#__codelineno-11-85>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-86>)    LlmAgent supportAgent =
    [](<https://adk.dev/tools-custom/#__codelineno-11-87>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/#__codelineno-11-88>)            .model(MODEL_ID)
    [](<https://adk.dev/tools-custom/#__codelineno-11-89>)            .name("support_agent")
    [](<https://adk.dev/tools-custom/#__codelineno-11-90>)            .description("""
    [](<https://adk.dev/tools-custom/#__codelineno-11-91>)                The dedicated support agent.
    [](<https://adk.dev/tools-custom/#__codelineno-11-92>)                Mentions it is a support handler and helps the user with their urgent issue.
    [](<https://adk.dev/tools-custom/#__codelineno-11-93>)            """)
    [](<https://adk.dev/tools-custom/#__codelineno-11-94>)            .instruction("""
    [](<https://adk.dev/tools-custom/#__codelineno-11-95>)                You are the dedicated support agent.
    [](<https://adk.dev/tools-custom/#__codelineno-11-96>)                Mentioned you are a support handler and please help the user with their urgent issue.
    [](<https://adk.dev/tools-custom/#__codelineno-11-97>)            """)
    [](<https://adk.dev/tools-custom/#__codelineno-11-98>)            .build();
    [](<https://adk.dev/tools-custom/#__codelineno-11-99>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-100>)    LlmAgent mainAgent =
    [](<https://adk.dev/tools-custom/#__codelineno-11-101>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/#__codelineno-11-102>)            .model(MODEL_ID)
    [](<https://adk.dev/tools-custom/#__codelineno-11-103>)            .name("main_agent")
    [](<https://adk.dev/tools-custom/#__codelineno-11-104>)            .description("""
    [](<https://adk.dev/tools-custom/#__codelineno-11-105>)                The first point of contact for customer support of an analytics tool.
    [](<https://adk.dev/tools-custom/#__codelineno-11-106>)                Answers general queries.
    [](<https://adk.dev/tools-custom/#__codelineno-11-107>)                If the user indicates urgency, uses the 'check_and_transfer' tool.
    [](<https://adk.dev/tools-custom/#__codelineno-11-108>)                """)
    [](<https://adk.dev/tools-custom/#__codelineno-11-109>)            .instruction("""
    [](<https://adk.dev/tools-custom/#__codelineno-11-110>)                You are the first point of contact for customer support of an analytics tool.
    [](<https://adk.dev/tools-custom/#__codelineno-11-111>)                Answer general queries.
    [](<https://adk.dev/tools-custom/#__codelineno-11-112>)                If the user indicates urgency, use the 'check_and_transfer' tool.
    [](<https://adk.dev/tools-custom/#__codelineno-11-113>)                """)
    [](<https://adk.dev/tools-custom/#__codelineno-11-114>)            .tools(ImmutableList.of(escalationTool))
    [](<https://adk.dev/tools-custom/#__codelineno-11-115>)            .subAgents(supportAgent)
    [](<https://adk.dev/tools-custom/#__codelineno-11-116>)            .build();
    [](<https://adk.dev/tools-custom/#__codelineno-11-117>)    // Fixed: LlmAgent.subAgents() expects 0 arguments.
    [](<https://adk.dev/tools-custom/#__codelineno-11-118>)    // Sub-agents are now added to the main agent via its builder,
    [](<https://adk.dev/tools-custom/#__codelineno-11-119>)    // as `subAgents` is a property that should be set during agent construction
    [](<https://adk.dev/tools-custom/#__codelineno-11-120>)    // if it's not dynamically managed.
    [](<https://adk.dev/tools-custom/#__codelineno-11-121>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-122>)    InMemorySessionService sessionService = new InMemorySessionService();
    [](<https://adk.dev/tools-custom/#__codelineno-11-123>)    Runner runner = new Runner(mainAgent, APP_NAME, null, sessionService);
    [](<https://adk.dev/tools-custom/#__codelineno-11-124>)
    [](<https://adk.dev/tools-custom/#__codelineno-11-125>)    // Agent Interaction
    [](<https://adk.dev/tools-custom/#__codelineno-11-126>)    callAgent(runner, "this is urgent, i cant login");
    [](<https://adk.dev/tools-custom/#__codelineno-11-127>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-11-128>)}
    
##### Explanation[¶](<https://adk.dev/tools-custom/#explanation> "Permanent link")

  * We define two agents: `main_agent` and `support_agent`. The `main_agent` is designed to be the initial point of contact.
  * The `check_and_transfer` tool, when called by `main_agent`, examines the user's query.
  * If the query contains the word "urgent", the tool accesses the `tool_context`, specifically **`tool_context.actions`** , and sets the transfer_to_agent attribute to `support_agent`.
  * This action signals to the framework to **transfer the control of the conversation to the agent named`support_agent`**.
  * When the `main_agent` processes the urgent query, the `check_and_transfer` tool triggers the transfer. The subsequent response would ideally come from the `support_agent`.
  * For a normal query without urgency, the tool simply processes it without triggering a transfer.

This example illustrates how a tool, through EventActions in its ToolContext, can dynamically influence the flow of the conversation by transferring control to another specialized agent.

### **Authentication**[¶](<https://adk.dev/tools-custom/#authentication> "Permanent link")

ToolContext provides mechanisms for tools interacting with authenticated APIs. If your tool needs to handle authentication, you might use the following:

  * **`auth_response`** (in Python): Contains credentials (e.g., a token) if authentication was already handled by the framework before your tool was called (common with RestApiTool and OpenAPI security schemes). In TypeScript, this is retrieved via the getAuthResponse() method.

  * **`request_credential(auth_config: dict)`** (in Python) or **`requestCredential(authConfig: AuthConfig)`** (in TypeScript): Call this method if your tool determines authentication is needed but credentials aren't available. This signals the framework to start an authentication flow based on the provided auth_config.

  * **`get_auth_response()`** (in Python) or **`getAuthResponse(authConfig: AuthConfig)`** (in TypeScript): Call this in a subsequent invocation (after request_credential was successfully handled) to retrieve the credentials the user provided.

For detailed explanations of authentication flows, configuration, and examples, please refer to the dedicated Tool Authentication documentation page.

### **Context-Aware Data Access Methods**[¶](<https://adk.dev/tools-custom/#context-aware-data-access-methods> "Permanent link")

These methods provide convenient ways for your tool to interact with persistent data associated with the session or user, managed by configured services.

  * **`list_artifacts()`** (in Python) or **`listArtifacts()`** (in Java and TypeScript): Returns a list of filenames (or keys) for all artifacts currently stored for the session via the artifact_service. Artifacts are typically files (images, documents, etc.) uploaded by the user or generated by tools/agents.

  * **`load_artifact(filename: str)`** : Retrieves a specific artifact by its filename from the **artifact_service**. You can optionally specify a version; if omitted, the latest version is returned. Returns a `google.genai.types.Part` object containing the artifact data and mime type, or None if not found.

  * **`save_artifact(filename: str, artifact: types.Part)`** : Saves a new version of an artifact to the artifact_service. Returns the new version number (starting from 0).

  * **`search_memory(query: str)`** : (Support in ADK Python, Go and TypeScript) Queries the user's long-term memory using the configured `memory_service`. This is useful for retrieving relevant information from past interactions or stored knowledge. The structure of the **SearchMemoryResponse** depends on the specific memory service implementation but typically contains relevant text snippets or conversation excerpts.

#### Example[¶](<https://adk.dev/tools-custom/#example_2> "Permanent link")

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/#__codelineno-12-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-12-2>)#
    [](<https://adk.dev/tools-custom/#__codelineno-12-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-12-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-12-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-12-6>)#
    [](<https://adk.dev/tools-custom/#__codelineno-12-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-12-8>)#
    [](<https://adk.dev/tools-custom/#__codelineno-12-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-12-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-12-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-12-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-12-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-12-14>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-15>)from google.adk.tools import ToolContext, FunctionTool
    [](<https://adk.dev/tools-custom/#__codelineno-12-16>)from google.genai import types
    [](<https://adk.dev/tools-custom/#__codelineno-12-17>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-18>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-19>)def process_document(
    [](<https://adk.dev/tools-custom/#__codelineno-12-20>)    document_name: str, analysis_query: str, tool_context: ToolContext
    [](<https://adk.dev/tools-custom/#__codelineno-12-21>)) -> dict:
    [](<https://adk.dev/tools-custom/#__codelineno-12-22>)    """Analyzes a document using context from memory."""
    [](<https://adk.dev/tools-custom/#__codelineno-12-23>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-24>)    # 1. Load the artifact
    [](<https://adk.dev/tools-custom/#__codelineno-12-25>)    print(f"Tool: Attempting to load artifact: {document_name}")
    [](<https://adk.dev/tools-custom/#__codelineno-12-26>)    document_part = tool_context.load_artifact(document_name)
    [](<https://adk.dev/tools-custom/#__codelineno-12-27>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-28>)    if not document_part:
    [](<https://adk.dev/tools-custom/#__codelineno-12-29>)        return {"status": "error", "message": f"Document '{document_name}' not found."}
    [](<https://adk.dev/tools-custom/#__codelineno-12-30>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-31>)    document_text = document_part.text  # Assuming it's text for simplicity
    [](<https://adk.dev/tools-custom/#__codelineno-12-32>)    print(f"Tool: Loaded document '{document_name}' ({len(document_text)} chars).")
    [](<https://adk.dev/tools-custom/#__codelineno-12-33>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-34>)    # 2. Search memory for related context
    [](<https://adk.dev/tools-custom/#__codelineno-12-35>)    print(f"Tool: Searching memory for context related to: '{analysis_query}'")
    [](<https://adk.dev/tools-custom/#__codelineno-12-36>)    memory_response = tool_context.search_memory(
    [](<https://adk.dev/tools-custom/#__codelineno-12-37>)        f"Context for analyzing document about {analysis_query}"
    [](<https://adk.dev/tools-custom/#__codelineno-12-38>)    )
    [](<https://adk.dev/tools-custom/#__codelineno-12-39>)    memory_context = "\n".join(
    [](<https://adk.dev/tools-custom/#__codelineno-12-40>)        [
    [](<https://adk.dev/tools-custom/#__codelineno-12-41>)            m.events[0].content.parts[0].text
    [](<https://adk.dev/tools-custom/#__codelineno-12-42>)            for m in memory_response.memories
    [](<https://adk.dev/tools-custom/#__codelineno-12-43>)            if m.events and m.events[0].content
    [](<https://adk.dev/tools-custom/#__codelineno-12-44>)        ]
    [](<https://adk.dev/tools-custom/#__codelineno-12-45>)    )  # Simplified extraction
    [](<https://adk.dev/tools-custom/#__codelineno-12-46>)    print(f"Tool: Found memory context: {memory_context[:100]}...")
    [](<https://adk.dev/tools-custom/#__codelineno-12-47>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-48>)    # 3. Perform analysis (placeholder)
    [](<https://adk.dev/tools-custom/#__codelineno-12-49>)    analysis_result = f"Analysis of '{document_name}' regarding '{analysis_query}' using memory context: [Placeholder Analysis Result]"
    [](<https://adk.dev/tools-custom/#__codelineno-12-50>)    print("Tool: Performed analysis.")
    [](<https://adk.dev/tools-custom/#__codelineno-12-51>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-52>)    # 4. Save the analysis result as a new artifact
    [](<https://adk.dev/tools-custom/#__codelineno-12-53>)    analysis_part = types.Part.from_text(text=analysis_result)
    [](<https://adk.dev/tools-custom/#__codelineno-12-54>)    new_artifact_name = f"analysis_{document_name}"
    [](<https://adk.dev/tools-custom/#__codelineno-12-55>)    version = await tool_context.save_artifact(new_artifact_name, analysis_part)
    [](<https://adk.dev/tools-custom/#__codelineno-12-56>)    print(f"Tool: Saved analysis result as '{new_artifact_name}' version {version}.")
    [](<https://adk.dev/tools-custom/#__codelineno-12-57>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-58>)    return {
    [](<https://adk.dev/tools-custom/#__codelineno-12-59>)        "status": "success",
    [](<https://adk.dev/tools-custom/#__codelineno-12-60>)        "analysis_artifact": new_artifact_name,
    [](<https://adk.dev/tools-custom/#__codelineno-12-61>)        "version": version,
    [](<https://adk.dev/tools-custom/#__codelineno-12-62>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-12-63>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-64>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-65>)doc_analysis_tool = FunctionTool(func=process_document)
    [](<https://adk.dev/tools-custom/#__codelineno-12-66>)
    [](<https://adk.dev/tools-custom/#__codelineno-12-67>)# In an Agent:
    [](<https://adk.dev/tools-custom/#__codelineno-12-68>)# Assume artifact 'report.txt' was previously saved.
    [](<https://adk.dev/tools-custom/#__codelineno-12-69>)# Assume memory service is configured and has relevant past data.
    [](<https://adk.dev/tools-custom/#__codelineno-12-70>)# my_agent = Agent(..., tools=[doc_analysis_tool], artifact_service=..., memory_service=...)
    
    [](<https://adk.dev/tools-custom/#__codelineno-13-1>)import { Part } from "@google/genai";
    [](<https://adk.dev/tools-custom/#__codelineno-13-2>)import { Context } from '@google/adk';
    [](<https://adk.dev/tools-custom/#__codelineno-13-3>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-4>)// Analyzes a document using context from memory.
    [](<https://adk.dev/tools-custom/#__codelineno-13-5>)export async function processDocument(
    [](<https://adk.dev/tools-custom/#__codelineno-13-6>)  params: { documentName: string; analysisQuery: string },
    [](<https://adk.dev/tools-custom/#__codelineno-13-7>)  context?: Context
    [](<https://adk.dev/tools-custom/#__codelineno-13-8>)): Promise<Record<string, any>> {
    [](<https://adk.dev/tools-custom/#__codelineno-13-9>)  if (!context) {
    [](<https://adk.dev/tools-custom/#__codelineno-13-10>)    throw new Error("Context is required for this tool.");
    [](<https://adk.dev/tools-custom/#__codelineno-13-11>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-13-12>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-13>)  // 1. List all available artifacts
    [](<https://adk.dev/tools-custom/#__codelineno-13-14>)  const artifacts = await context.listArtifacts();
    [](<https://adk.dev/tools-custom/#__codelineno-13-15>)  console.log(`Listing all available artifacts: ${artifacts}`);
    [](<https://adk.dev/tools-custom/#__codelineno-13-16>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-17>)  // 2. Load an artifact
    [](<https://adk.dev/tools-custom/#__codelineno-13-18>)  console.log(`Tool: Attempting to load artifact: ${params.documentName}`);
    [](<https://adk.dev/tools-custom/#__codelineno-13-19>)  const documentPart = await context.loadArtifact(params.documentName);
    [](<https://adk.dev/tools-custom/#__codelineno-13-20>)  if (!documentPart) {
    [](<https://adk.dev/tools-custom/#__codelineno-13-21>)    console.log(`Tool: Document '${params.documentName}' not found.`);
    [](<https://adk.dev/tools-custom/#__codelineno-13-22>)    return {
    [](<https://adk.dev/tools-custom/#__codelineno-13-23>)      status: "error",
    [](<https://adk.dev/tools-custom/#__codelineno-13-24>)      message: `Document '${params.documentName}' not found.`, 
    [](<https://adk.dev/tools-custom/#__codelineno-13-25>)    };
    [](<https://adk.dev/tools-custom/#__codelineno-13-26>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-13-27>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-28>)  const documentText = documentPart.text ?? "";
    [](<https://adk.dev/tools-custom/#__codelineno-13-29>)  console.log(
    [](<https://adk.dev/tools-custom/#__codelineno-13-30>)    `Tool: Loaded document '${params.documentName}' (${documentText.length} chars).`
    [](<https://adk.dev/tools-custom/#__codelineno-13-31>)  );
    [](<https://adk.dev/tools-custom/#__codelineno-13-32>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-33>)  // 3. Search memory for related context
    [](<https://adk.dev/tools-custom/#__codelineno-13-34>)  console.log(`Tool: Searching memory for context related to '${params.analysisQuery}'`);
    [](<https://adk.dev/tools-custom/#__codelineno-13-35>)  const memory_results = await context.searchMemory(params.analysisQuery);
    [](<https://adk.dev/tools-custom/#__codelineno-13-36>)  console.log(`Tool: Found ${memory_results.memories.length} relevant memories.`);
    [](<https://adk.dev/tools-custom/#__codelineno-13-37>)  const context_from_memory = memory_results.memories
    [](<https://adk.dev/tools-custom/#__codelineno-13-38>)    .map((m) => m.content.parts[0].text)
    [](<https://adk.dev/tools-custom/#__codelineno-13-39>)    .join("\n");
    [](<https://adk.dev/tools-custom/#__codelineno-13-40>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-41>)  // 4. Perform analysis (placeholder)
    [](<https://adk.dev/tools-custom/#__codelineno-13-42>)  const analysisResult =
    [](<https://adk.dev/tools-custom/#__codelineno-13-43>)    `Analysis of '${params.documentName}' regarding '${params.analysisQuery}':\n` +
    [](<https://adk.dev/tools-custom/#__codelineno-13-44>)    `Context from Memory:\n${context_from_memory}\n` +
    [](<https://adk.dev/tools-custom/#__codelineno-13-45>)    `[Placeholder Analysis Result]`;
    [](<https://adk.dev/tools-custom/#__codelineno-13-46>)  console.log("Tool: Performed analysis.");
    [](<https://adk.dev/tools-custom/#__codelineno-13-47>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-48>)  // 5. Save the analysis result as a new artifact
    [](<https://adk.dev/tools-custom/#__codelineno-13-49>)  const analysisPart: Part = { text: analysisResult };
    [](<https://adk.dev/tools-custom/#__codelineno-13-50>)  const newArtifactName = `analysis_${params.documentName}`;
    [](<https://adk.dev/tools-custom/#__codelineno-13-51>)  await context.saveArtifact(newArtifactName, analysisPart);
    [](<https://adk.dev/tools-custom/#__codelineno-13-52>)  console.log(`Tool: Saved analysis result to '${newArtifactName}'.`);
    [](<https://adk.dev/tools-custom/#__codelineno-13-53>)
    [](<https://adk.dev/tools-custom/#__codelineno-13-54>)  return {
    [](<https://adk.dev/tools-custom/#__codelineno-13-55>)    status: "success",
    [](<https://adk.dev/tools-custom/#__codelineno-13-56>)    analysis_artifact: newArtifactName,
    [](<https://adk.dev/tools-custom/#__codelineno-13-57>)  };
    [](<https://adk.dev/tools-custom/#__codelineno-13-58>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-14-1>)// Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-14-2>)//
    [](<https://adk.dev/tools-custom/#__codelineno-14-3>)// Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-14-4>)// you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-14-5>)// You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-14-6>)//
    [](<https://adk.dev/tools-custom/#__codelineno-14-7>)//     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-14-8>)//
    [](<https://adk.dev/tools-custom/#__codelineno-14-9>)// Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-14-10>)// distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-14-11>)// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-14-12>)// See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-14-13>)// limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-14-14>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-15>)package main
    [](<https://adk.dev/tools-custom/#__codelineno-14-16>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-17>)import (
    [](<https://adk.dev/tools-custom/#__codelineno-14-18>)    "fmt"
    [](<https://adk.dev/tools-custom/#__codelineno-14-19>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-20>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/#__codelineno-14-21>)    "google.golang.org/genai"
    [](<https://adk.dev/tools-custom/#__codelineno-14-22>))
    [](<https://adk.dev/tools-custom/#__codelineno-14-23>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-24>)type processDocumentArgs struct {
    [](<https://adk.dev/tools-custom/#__codelineno-14-25>)    DocumentName  string `json:"document_name" jsonschema:"The name of the document to be processed."`
    [](<https://adk.dev/tools-custom/#__codelineno-14-26>)    AnalysisQuery string `json:"analysis_query" jsonschema:"The query for the analysis."`
    [](<https://adk.dev/tools-custom/#__codelineno-14-27>)}
    [](<https://adk.dev/tools-custom/#__codelineno-14-28>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-29>)type processDocumentResult struct {
    [](<https://adk.dev/tools-custom/#__codelineno-14-30>)    Status           string `json:"status"`
    [](<https://adk.dev/tools-custom/#__codelineno-14-31>)    AnalysisArtifact string `json:"analysis_artifact,omitempty"`
    [](<https://adk.dev/tools-custom/#__codelineno-14-32>)    Version          int64  `json:"version,omitempty"`
    [](<https://adk.dev/tools-custom/#__codelineno-14-33>)    Message          string `json:"message,omitempty"`
    [](<https://adk.dev/tools-custom/#__codelineno-14-34>)}
    [](<https://adk.dev/tools-custom/#__codelineno-14-35>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-36>)func processDocument(ctx agent.Context, args processDocumentArgs) (*processDocumentResult, error) {
    [](<https://adk.dev/tools-custom/#__codelineno-14-37>)    fmt.Printf("Tool: Attempting to load artifact: %s\n", args.DocumentName)
    [](<https://adk.dev/tools-custom/#__codelineno-14-38>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-39>)    // List all artifacts
    [](<https://adk.dev/tools-custom/#__codelineno-14-40>)    listResponse, err := ctx.Artifacts().List(ctx)
    [](<https://adk.dev/tools-custom/#__codelineno-14-41>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-14-42>)        return nil, fmt.Errorf("failed to list artifacts")
    [](<https://adk.dev/tools-custom/#__codelineno-14-43>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-14-44>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-45>)    fmt.Println("Tool: Available artifacts:")
    [](<https://adk.dev/tools-custom/#__codelineno-14-46>)    for _, file := range listResponse.FileNames {
    [](<https://adk.dev/tools-custom/#__codelineno-14-47>)        fmt.Printf(" - %s\n", file)
    [](<https://adk.dev/tools-custom/#__codelineno-14-48>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-14-49>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-50>)    documentPart, err := ctx.Artifacts().Load(ctx, args.DocumentName)
    [](<https://adk.dev/tools-custom/#__codelineno-14-51>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-14-52>)        return nil, fmt.Errorf("document '%s' not found", args.DocumentName)
    [](<https://adk.dev/tools-custom/#__codelineno-14-53>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-14-54>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-55>)    fmt.Printf("Tool: Loaded document '%s' of size %d bytes.\n", args.DocumentName, len(documentPart.Part.InlineData.Data))
    [](<https://adk.dev/tools-custom/#__codelineno-14-56>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-57>)    // 3. Search memory for related context
    [](<https://adk.dev/tools-custom/#__codelineno-14-58>)    fmt.Printf("Tool: Searching memory for context related to: '%s'\n", args.AnalysisQuery)
    [](<https://adk.dev/tools-custom/#__codelineno-14-59>)    memoryResp, err := ctx.SearchMemory(ctx, args.AnalysisQuery)
    [](<https://adk.dev/tools-custom/#__codelineno-14-60>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-14-61>)        fmt.Printf("Tool: Error searching memory: %v\n", err)
    [](<https://adk.dev/tools-custom/#__codelineno-14-62>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-14-63>)    memoryResultCount := 0
    [](<https://adk.dev/tools-custom/#__codelineno-14-64>)    if memoryResp != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-14-65>)        memoryResultCount = len(memoryResp.Memories)
    [](<https://adk.dev/tools-custom/#__codelineno-14-66>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-14-67>)    fmt.Printf("Tool: Found %d memory results.\n", memoryResultCount)
    [](<https://adk.dev/tools-custom/#__codelineno-14-68>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-69>)    analysisResult := fmt.Sprintf("Analysis of '%s' regarding '%s' using memory context: [Placeholder Analysis Result]", args.DocumentName, args.AnalysisQuery)
    [](<https://adk.dev/tools-custom/#__codelineno-14-70>)    fmt.Println("Tool: Performed analysis.")
    [](<https://adk.dev/tools-custom/#__codelineno-14-71>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-72>)    analysisPart := genai.NewPartFromText(analysisResult)
    [](<https://adk.dev/tools-custom/#__codelineno-14-73>)    newArtifactName := fmt.Sprintf("analysis_%s", args.DocumentName)
    [](<https://adk.dev/tools-custom/#__codelineno-14-74>)    version, err := ctx.Artifacts().Save(ctx, newArtifactName, analysisPart)
    [](<https://adk.dev/tools-custom/#__codelineno-14-75>)    if err != nil {
    [](<https://adk.dev/tools-custom/#__codelineno-14-76>)        return nil, fmt.Errorf("failed to save artifact")
    [](<https://adk.dev/tools-custom/#__codelineno-14-77>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-14-78>)    fmt.Printf("Tool: Saved analysis result as '%s' version %d.\n", newArtifactName, version.Version)
    [](<https://adk.dev/tools-custom/#__codelineno-14-79>)
    [](<https://adk.dev/tools-custom/#__codelineno-14-80>)    return &processDocumentResult{
    [](<https://adk.dev/tools-custom/#__codelineno-14-81>)        Status:           "success",
    [](<https://adk.dev/tools-custom/#__codelineno-14-82>)        AnalysisArtifact: newArtifactName,
    [](<https://adk.dev/tools-custom/#__codelineno-14-83>)        Version:          version.Version,
    [](<https://adk.dev/tools-custom/#__codelineno-14-84>)    }, nil
    [](<https://adk.dev/tools-custom/#__codelineno-14-85>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-15-1>)// Analyzes a document using context from memory.
    [](<https://adk.dev/tools-custom/#__codelineno-15-2>)// You can also list, load and save artifacts using Callback Context or LoadArtifacts tool.
    [](<https://adk.dev/tools-custom/#__codelineno-15-3>)public static @NonNull Maybe<ImmutableMap<String, Object>> processDocument(
    [](<https://adk.dev/tools-custom/#__codelineno-15-4>)    @Annotations.Schema(description = "The name of the document to analyze.") String documentName,
    [](<https://adk.dev/tools-custom/#__codelineno-15-5>)    @Annotations.Schema(description = "The query for the analysis.") String analysisQuery,
    [](<https://adk.dev/tools-custom/#__codelineno-15-6>)    ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-15-7>)
    [](<https://adk.dev/tools-custom/#__codelineno-15-8>)  // 1. List all available artifacts
    [](<https://adk.dev/tools-custom/#__codelineno-15-9>)  System.out.printf(
    [](<https://adk.dev/tools-custom/#__codelineno-15-10>)      "Listing all available artifacts %s:", toolContext.listArtifacts().blockingGet());
    [](<https://adk.dev/tools-custom/#__codelineno-15-11>)
    [](<https://adk.dev/tools-custom/#__codelineno-15-12>)  // 2. Load an artifact to memory
    [](<https://adk.dev/tools-custom/#__codelineno-15-13>)  System.out.println("Tool: Attempting to load artifact: " + documentName);
    [](<https://adk.dev/tools-custom/#__codelineno-15-14>)  Part documentPart = toolContext.loadArtifact(documentName, Optional.empty()).blockingGet();
    [](<https://adk.dev/tools-custom/#__codelineno-15-15>)  if (documentPart == null) {
    [](<https://adk.dev/tools-custom/#__codelineno-15-16>)    System.out.println("Tool: Document '" + documentName + "' not found.");
    [](<https://adk.dev/tools-custom/#__codelineno-15-17>)    return Maybe.just(
    [](<https://adk.dev/tools-custom/#__codelineno-15-18>)        ImmutableMap.<String, Object>of(
    [](<https://adk.dev/tools-custom/#__codelineno-15-19>)            "status", "error", "message", "Document '" + documentName + "' not found."));
    [](<https://adk.dev/tools-custom/#__codelineno-15-20>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-15-21>)  String documentText = documentPart.text().orElse("");
    [](<https://adk.dev/tools-custom/#__codelineno-15-22>)  System.out.println(
    [](<https://adk.dev/tools-custom/#__codelineno-15-23>)      "Tool: Loaded document '" + documentName + "' (" + documentText.length() + " chars).");
    [](<https://adk.dev/tools-custom/#__codelineno-15-24>)
    [](<https://adk.dev/tools-custom/#__codelineno-15-25>)  // 3. Perform analysis (placeholder)
    [](<https://adk.dev/tools-custom/#__codelineno-15-26>)  String analysisResult =
    [](<https://adk.dev/tools-custom/#__codelineno-15-27>)      "Analysis of '"
    [](<https://adk.dev/tools-custom/#__codelineno-15-28>)          + documentName
    [](<https://adk.dev/tools-custom/#__codelineno-15-29>)          + "' regarding '"
    [](<https://adk.dev/tools-custom/#__codelineno-15-30>)          + analysisQuery
    [](<https://adk.dev/tools-custom/#__codelineno-15-31>)          + " [Placeholder Analysis Result]";
    [](<https://adk.dev/tools-custom/#__codelineno-15-32>)  System.out.println("Tool: Performed analysis.");
    [](<https://adk.dev/tools-custom/#__codelineno-15-33>)
    [](<https://adk.dev/tools-custom/#__codelineno-15-34>)  // 4. Save the analysis result as a new artifact
    [](<https://adk.dev/tools-custom/#__codelineno-15-35>)  Part analysisPart = Part.fromText(analysisResult);
    [](<https://adk.dev/tools-custom/#__codelineno-15-36>)  String newArtifactName = "analysis_" + documentName;
    [](<https://adk.dev/tools-custom/#__codelineno-15-37>)
    [](<https://adk.dev/tools-custom/#__codelineno-15-38>)  toolContext.saveArtifact(newArtifactName, analysisPart);
    [](<https://adk.dev/tools-custom/#__codelineno-15-39>)
    [](<https://adk.dev/tools-custom/#__codelineno-15-40>)  return Maybe.just(
    [](<https://adk.dev/tools-custom/#__codelineno-15-41>)      ImmutableMap.<String, Object>builder()
    [](<https://adk.dev/tools-custom/#__codelineno-15-42>)          .put("status", "success")
    [](<https://adk.dev/tools-custom/#__codelineno-15-43>)          .put("analysis_artifact", newArtifactName)
    [](<https://adk.dev/tools-custom/#__codelineno-15-44>)          .build());
    [](<https://adk.dev/tools-custom/#__codelineno-15-45>)}
    [](<https://adk.dev/tools-custom/#__codelineno-15-46>)// FunctionTool processDocumentTool =
    [](<https://adk.dev/tools-custom/#__codelineno-15-47>)//      FunctionTool.create(ToolContextArtifactExample.class, "processDocument");
    [](<https://adk.dev/tools-custom/#__codelineno-15-48>)// In the Agent, include this function tool.
    [](<https://adk.dev/tools-custom/#__codelineno-15-49>)// LlmAgent agent = LlmAgent().builder().tools(processDocumentTool).build();
    
By leveraging the **ToolContext** , developers can create more sophisticated and context-aware custom tools that seamlessly integrate with ADK's architecture and enhance the overall capabilities of their agents.

## Defining Effective Tool Functions[¶](<https://adk.dev/tools-custom/#defining-effective-tool-functions> "Permanent link")

When using a method or function as an ADK Tool, how you define it significantly impacts the agent's ability to use it correctly. The agent's Large Language Model (LLM) relies heavily on the function's **name** , **parameters (arguments)** , **type hints** , and **docstring** / **source code comments** to understand its purpose and generate the correct call.

Here are key guidelines for defining effective tool functions:

  * **Function Name:**

    * Use descriptive, verb-noun based names that clearly indicate the action (e.g., `get_weather`, `searchDocuments`, `schedule_meeting`).
    * Avoid generic names like `run`, `process`, `handle_data`, or overly ambiguous names like `doStuff`. Even with a good description, a name like `do_stuff` might confuse the model about when to use the tool versus, for example, `cancelFlight`.
    * The LLM uses the function name as a primary identifier during tool selection.
  * **Parameters (Arguments):**

    * Your function can have any number of parameters.
    * Use clear and descriptive names (e.g., `city` instead of `c`, `search_query` instead of `q`).
    * **Provide type hints in Python** for all parameters (e.g., `city: str`, `user_id: int`, `items: list[str]`). This is essential for ADK to generate the correct schema for the LLM.
    * Ensure all parameter types are **JSON serializable**. All java primitives as well as standard Python types like `str`, `int`, `float`, `bool`, `list`, `dict`, and their combinations are generally safe. Avoid complex custom class instances as direct parameters unless they have a clear JSON representation.
    * **Avoid default values for information the model must provide.** E.g., avoid `def my_func(destination: str = "Paris")` if the destination should come from the user or conversation context. Default values can be appropriate for genuinely optional tuning parameters, but do not use them to hide required business inputs from the tool schema.
    * **`self` / `cls` Handled Automatically:** Implicit parameters like `self` (for instance methods) or `cls` (for class methods) are automatically handled by ADK and excluded from the schema shown to the LLM. You only need to define type hints and descriptions for the logical parameters your tool requires the LLM to provide.
  * **Return Type:**

    * The function's return value **must be a dictionary (`dict`)** in Python, a **Map** in Java, or a plain **object** in TypeScript.
    * If your function returns a non-dictionary type (e.g., a string, number, list), the ADK framework will automatically wrap it into a dictionary/Map like `{'result': your_original_return_value}` before passing the result back to the model.
    * Design the dictionary/Map keys and values to be **descriptive and easily understood _by the LLM_**. Remember, the model reads this output to decide its next step.
    * Include meaningful keys. For example, instead of returning just an error code like `500`, return `{'status': 'error', 'error_message': 'Database connection failed'}`.
    * It's a **highly recommended practice** to include a `status` key (e.g., `'success'`, `'error'`, `'pending'`, `'ambiguous'`) to clearly indicate the outcome of the tool execution for the model.
  * **Docstring / Source Code Comments:**

    * **This is critical.** The docstring is the primary source of descriptive information for the LLM.
    * **Clearly state what the tool _does_.** Be specific about its purpose and limitations.
    * **Explain _when_ the tool should be used.** Provide context or example scenarios to guide the LLM's decision-making.
    * **Describe _each parameter_ clearly.** Explain what information the LLM needs to provide for that argument.
    * Describe the **structure and meaning of the expected`dict` return value**, especially the different `status` values and associated data keys.
    * **Do not describe the injected ToolContext parameter**. Avoid mentioning the optional `tool_context: ToolContext` parameter within the docstring description since it is not a parameter the LLM needs to know about. ToolContext is injected by ADK, _after_ the LLM decides to call it.

**Example of a good definition:**

PythonTypeScriptGoJava
    
    [](<https://adk.dev/tools-custom/#__codelineno-16-1>)def lookup_order_status(order_id: str) -> dict:
    [](<https://adk.dev/tools-custom/#__codelineno-16-2>)  """Fetches the current status of a customer's order using its ID.
    [](<https://adk.dev/tools-custom/#__codelineno-16-3>)
    [](<https://adk.dev/tools-custom/#__codelineno-16-4>)  Use this tool ONLY when a user explicitly asks for the status of
    [](<https://adk.dev/tools-custom/#__codelineno-16-5>)  a specific order and provides the order ID. Do not use it for
    [](<https://adk.dev/tools-custom/#__codelineno-16-6>)  general inquiries.
    [](<https://adk.dev/tools-custom/#__codelineno-16-7>)
    [](<https://adk.dev/tools-custom/#__codelineno-16-8>)  Args:
    [](<https://adk.dev/tools-custom/#__codelineno-16-9>)      order_id: The unique identifier of the order to look up.
    [](<https://adk.dev/tools-custom/#__codelineno-16-10>)
    [](<https://adk.dev/tools-custom/#__codelineno-16-11>)  Returns:
    [](<https://adk.dev/tools-custom/#__codelineno-16-12>)      A dictionary indicating the outcome.
    [](<https://adk.dev/tools-custom/#__codelineno-16-13>)      On success, status is 'success' and includes an 'order' dictionary.
    [](<https://adk.dev/tools-custom/#__codelineno-16-14>)      On failure, status is 'error' and includes an 'error_message'.
    [](<https://adk.dev/tools-custom/#__codelineno-16-15>)      Example success: {'status': 'success', 'order': {'state': 'shipped', 'tracking_number': '1Z9...'}}
    [](<https://adk.dev/tools-custom/#__codelineno-16-16>)      Example error: {'status': 'error', 'error_message': 'Order ID not found.'}
    [](<https://adk.dev/tools-custom/#__codelineno-16-17>)  """
    [](<https://adk.dev/tools-custom/#__codelineno-16-18>)  # ... function implementation to fetch status ...
    [](<https://adk.dev/tools-custom/#__codelineno-16-19>)  if status_details := fetch_status_from_backend(order_id):
    [](<https://adk.dev/tools-custom/#__codelineno-16-20>)    return {
    [](<https://adk.dev/tools-custom/#__codelineno-16-21>)        "status": "success",
    [](<https://adk.dev/tools-custom/#__codelineno-16-22>)        "order": {
    [](<https://adk.dev/tools-custom/#__codelineno-16-23>)            "state": status_details.state,
    [](<https://adk.dev/tools-custom/#__codelineno-16-24>)            "tracking_number": status_details.tracking,
    [](<https://adk.dev/tools-custom/#__codelineno-16-25>)        },
    [](<https://adk.dev/tools-custom/#__codelineno-16-26>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-16-27>)  else:
    [](<https://adk.dev/tools-custom/#__codelineno-16-28>)    return {"status": "error", "error_message": f"Order ID {order_id} not found."}
    
    [](<https://adk.dev/tools-custom/#__codelineno-17-1>)/**
    [](<https://adk.dev/tools-custom/#__codelineno-17-2>) * Fetches the current status of a customer's order using its ID.
    [](<https://adk.dev/tools-custom/#__codelineno-17-3>) *
    [](<https://adk.dev/tools-custom/#__codelineno-17-4>) * Use this tool ONLY when a user explicitly asks for the status of
    [](<https://adk.dev/tools-custom/#__codelineno-17-5>) * a specific order and provides the order ID. Do not use it for
    [](<https://adk.dev/tools-custom/#__codelineno-17-6>) * general inquiries.
    [](<https://adk.dev/tools-custom/#__codelineno-17-7>) *
    [](<https://adk.dev/tools-custom/#__codelineno-17-8>) * @param params The parameters for the function.
    [](<https://adk.dev/tools-custom/#__codelineno-17-9>) * @param params.order_id The unique identifier of the order to look up.
    [](<https://adk.dev/tools-custom/#__codelineno-17-10>) * @returns A dictionary indicating the outcome.
    [](<https://adk.dev/tools-custom/#__codelineno-17-11>) *          On success, status is 'success' and includes an 'order' dictionary.
    [](<https://adk.dev/tools-custom/#__codelineno-17-12>) *          On failure, status is 'error' and includes an 'error_message'.
    [](<https://adk.dev/tools-custom/#__codelineno-17-13>) *          Example success: {'status': 'success', 'order': {'state': 'shipped', 'tracking_number': '1Z9...'}}
    [](<https://adk.dev/tools-custom/#__codelineno-17-14>) *          Example error: {'status': 'error', 'error_message': 'Order ID not found.'}
    [](<https://adk.dev/tools-custom/#__codelineno-17-15>) */
    [](<https://adk.dev/tools-custom/#__codelineno-17-16>)async function lookupOrderStatus(params: { order_id: string }): Promise<Record<string, any>> {
    [](<https://adk.dev/tools-custom/#__codelineno-17-17>)  // ... function implementation to fetch status from a backend ...
    [](<https://adk.dev/tools-custom/#__codelineno-17-18>)  const status_details = await fetchStatusFromBackend(params.order_id);
    [](<https://adk.dev/tools-custom/#__codelineno-17-19>)  if (status_details) {
    [](<https://adk.dev/tools-custom/#__codelineno-17-20>)    return {
    [](<https://adk.dev/tools-custom/#__codelineno-17-21>)      "status": "success",
    [](<https://adk.dev/tools-custom/#__codelineno-17-22>)      "order": {
    [](<https://adk.dev/tools-custom/#__codelineno-17-23>)        "state": status_details.state,
    [](<https://adk.dev/tools-custom/#__codelineno-17-24>)        "tracking_number": status_details.tracking,
    [](<https://adk.dev/tools-custom/#__codelineno-17-25>)      },
    [](<https://adk.dev/tools-custom/#__codelineno-17-26>)    };
    [](<https://adk.dev/tools-custom/#__codelineno-17-27>)  } else {
    [](<https://adk.dev/tools-custom/#__codelineno-17-28>)    return { "status": "error", "error_message": `Order ID ${params.order_id} not found.` };
    [](<https://adk.dev/tools-custom/#__codelineno-17-29>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-17-30>)}
    [](<https://adk.dev/tools-custom/#__codelineno-17-31>)
    [](<https://adk.dev/tools-custom/#__codelineno-17-32>)// Placeholder for a backend call
    [](<https://adk.dev/tools-custom/#__codelineno-17-33>)async function fetchStatusFromBackend(order_id: string): Promise<{state: string, tracking: string} | null> {
    [](<https://adk.dev/tools-custom/#__codelineno-17-34>)    if (order_id === "12345") {
    [](<https://adk.dev/tools-custom/#__codelineno-17-35>)        return { state: "shipped", tracking: "1Z9..." };
    [](<https://adk.dev/tools-custom/#__codelineno-17-36>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-17-37>)    return null;
    [](<https://adk.dev/tools-custom/#__codelineno-17-38>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-18-1>)import (
    [](<https://adk.dev/tools-custom/#__codelineno-18-2>)    "fmt"
    [](<https://adk.dev/tools-custom/#__codelineno-18-3>)
    [](<https://adk.dev/tools-custom/#__codelineno-18-4>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tools-custom/#__codelineno-18-5>))
    [](<https://adk.dev/tools-custom/#__codelineno-18-6>)
    [](<https://adk.dev/tools-custom/#__codelineno-18-7>)type lookupOrderStatusArgs struct {
    [](<https://adk.dev/tools-custom/#__codelineno-18-8>)    OrderID string `json:"order_id" jsonschema:"The ID of the order to look up."`
    [](<https://adk.dev/tools-custom/#__codelineno-18-9>)}
    [](<https://adk.dev/tools-custom/#__codelineno-18-10>)
    [](<https://adk.dev/tools-custom/#__codelineno-18-11>)type order struct {
    [](<https://adk.dev/tools-custom/#__codelineno-18-12>)    State          string `json:"state"`
    [](<https://adk.dev/tools-custom/#__codelineno-18-13>)    TrackingNumber string `json:"tracking_number"`
    [](<https://adk.dev/tools-custom/#__codelineno-18-14>)}
    [](<https://adk.dev/tools-custom/#__codelineno-18-15>)
    [](<https://adk.dev/tools-custom/#__codelineno-18-16>)type lookupOrderStatusResult struct {
    [](<https://adk.dev/tools-custom/#__codelineno-18-17>)    Status string `json:"status"`
    [](<https://adk.dev/tools-custom/#__codelineno-18-18>)    Order  order  `json:"order,omitempty"`
    [](<https://adk.dev/tools-custom/#__codelineno-18-19>)}
    [](<https://adk.dev/tools-custom/#__codelineno-18-20>)
    [](<https://adk.dev/tools-custom/#__codelineno-18-21>)func lookupOrderStatus(ctx agent.Context, args lookupOrderStatusArgs) (*lookupOrderStatusResult, error) {
    [](<https://adk.dev/tools-custom/#__codelineno-18-22>)    // ... function implementation to fetch status ...
    [](<https://adk.dev/tools-custom/#__codelineno-18-23>)    statusDetails, ok := fetchStatusFromBackend(args.OrderID)
    [](<https://adk.dev/tools-custom/#__codelineno-18-24>)    if !ok {
    [](<https://adk.dev/tools-custom/#__codelineno-18-25>)        return nil, fmt.Errorf("order ID %s not found", args.OrderID)
    [](<https://adk.dev/tools-custom/#__codelineno-18-26>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-18-27>)    return &lookupOrderStatusResult{
    [](<https://adk.dev/tools-custom/#__codelineno-18-28>)        Status: "success",
    [](<https://adk.dev/tools-custom/#__codelineno-18-29>)        Order: order{
    [](<https://adk.dev/tools-custom/#__codelineno-18-30>)            State:          statusDetails.State,
    [](<https://adk.dev/tools-custom/#__codelineno-18-31>)            TrackingNumber: statusDetails.Tracking,
    [](<https://adk.dev/tools-custom/#__codelineno-18-32>)        },
    [](<https://adk.dev/tools-custom/#__codelineno-18-33>)    }, nil
    [](<https://adk.dev/tools-custom/#__codelineno-18-34>)}
    
    [](<https://adk.dev/tools-custom/#__codelineno-19-1>)/**
    [](<https://adk.dev/tools-custom/#__codelineno-19-2>) * Retrieves the current weather report for a specified city.
    [](<https://adk.dev/tools-custom/#__codelineno-19-3>) *
    [](<https://adk.dev/tools-custom/#__codelineno-19-4>) * @param city The city for which to retrieve the weather report.
    [](<https://adk.dev/tools-custom/#__codelineno-19-5>) * @param toolContext The context for the tool.
    [](<https://adk.dev/tools-custom/#__codelineno-19-6>) * @return A dictionary containing the weather information.
    [](<https://adk.dev/tools-custom/#__codelineno-19-7>) */
    [](<https://adk.dev/tools-custom/#__codelineno-19-8>)public static Map<String, Object> getWeatherReport(String city, ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-19-9>)    Map<String, Object> response = new HashMap<>();
    [](<https://adk.dev/tools-custom/#__codelineno-19-10>)    if (city.toLowerCase(Locale.ROOT).equals("london")) {
    [](<https://adk.dev/tools-custom/#__codelineno-19-11>)        response.put("status", "success");
    [](<https://adk.dev/tools-custom/#__codelineno-19-12>)        response.put(
    [](<https://adk.dev/tools-custom/#__codelineno-19-13>)                "report",
    [](<https://adk.dev/tools-custom/#__codelineno-19-14>)                "The current weather in London is cloudy with a temperature of 18 degrees Celsius and a"
    [](<https://adk.dev/tools-custom/#__codelineno-19-15>)                        + " chance of rain.");
    [](<https://adk.dev/tools-custom/#__codelineno-19-16>)    } else if (city.toLowerCase(Locale.ROOT).equals("paris")) {
    [](<https://adk.dev/tools-custom/#__codelineno-19-17>)        response.put("status", "success");
    [](<https://adk.dev/tools-custom/#__codelineno-19-18>)        response.put("report", "The weather in Paris is sunny with a temperature of 25 degrees Celsius.");
    [](<https://adk.dev/tools-custom/#__codelineno-19-19>)    } else {
    [](<https://adk.dev/tools-custom/#__codelineno-19-20>)        response.put("status", "error");
    [](<https://adk.dev/tools-custom/#__codelineno-19-21>)        response.put("error_message", String.format("Weather information for '%s' is not available.", city));
    [](<https://adk.dev/tools-custom/#__codelineno-19-22>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-19-23>)    return response;
    [](<https://adk.dev/tools-custom/#__codelineno-19-24>)}
    
  * **Simplicity and Focus:**
    * **Keep Tools Focused:** Each tool should ideally perform one well-defined task.
    * **Fewer Parameters are Better:** Models generally handle tools with fewer, clearly defined parameters more reliably than those with many optional or complex ones.
    * **Use Simple Data Types:** Prefer basic types (`str`, `int`, `bool`, `float`, `List[str]`, in **Python** ; `int`, `byte`, `short`, `long`, `float`, `double`, `boolean` and `char` in **Java** ; or `string`, `number`, `boolean`, and arrays like `string[]` in **TypeScript**) over complex custom classes or deeply nested structures as parameters when possible.
    * **Decompose Complex Tasks:** Break down functions that perform multiple distinct logical steps into smaller, more focused tools. For instance, instead of a single `update_user_profile(profile: ProfileObject)` tool, consider separate tools like `update_user_name(name: str)`, `update_user_address(address: str)`, `update_user_preferences(preferences: list[str])`, etc. This makes it easier for the LLM to select and use the correct capability.

By adhering to these guidelines, you provide the LLM with the clarity and structure it needs to effectively utilize your custom function tools, leading to more capable and reliable agent behavior.

## Toolsets: Grouping and Dynamically Providing Tools[¶](<https://adk.dev/tools-custom/#toolsets-grouping-and-dynamically-providing-tools> "Permanent link")

Supported in ADKPython v0.5.0Typescript v0.2.0

Beyond individual tools, ADK introduces the concept of a **Toolset** via the `BaseToolset` interface (defined in `google.adk.tools.base_toolset`). A toolset allows you to manage and provide a collection of `BaseTool` instances, often dynamically, to an agent.

This approach is beneficial for:

  * **Organizing Related Tools:** Grouping tools that serve a common purpose (e.g., all tools for mathematical operations, or all tools interacting with a specific API).
  * **Dynamic Tool Availability:** Enabling an agent to have different tools available based on the current context (e.g., user permissions, session state, or other runtime conditions). The `get_tools` method of a toolset can decide which tools to expose.
  * **Integrating External Tool Providers:** Toolsets can act as adapters for tools coming from external systems, like an OpenAPI specification or an MCP server, converting them into ADK-compatible `BaseTool` objects.

### The `BaseToolset` Interface[¶](<https://adk.dev/tools-custom/#the-basetoolset-interface> "Permanent link")

Any class acting as a toolset in ADK should implement the `BaseToolset` abstract base class. This interface primarily defines two methods:

  * **`async def get_tools(...) -> list[BaseTool]:`** This is the core method of a toolset. When an ADK agent needs to know its available tools, it will call `get_tools()` on each `BaseToolset` instance provided in its `tools` list.

    * It receives an optional `readonly_context` (an instance of `ReadonlyContext`). This context provides read-only access to information like the current session state (`readonly_context.state`), agent name, and invocation ID. The toolset can use this context to dynamically decide which tools to return.
    * It **must** return a `list` of `BaseTool` instances (e.g., `FunctionTool`, `RestApiTool`).
  * **`async def close(self) -> None:`** This asynchronous method is called by the ADK framework when the toolset is no longer needed, for example, when an agent server is shutting down or the `Runner` is being closed. Implement this method to perform any necessary cleanup, such as closing network connections, releasing file handles, or cleaning up other resources managed by the toolset.

### Using Toolsets with Agents[¶](<https://adk.dev/tools-custom/#using-toolsets-with-agents> "Permanent link")

You can include instances of your `BaseToolset` implementations directly in an `LlmAgent`'s `tools` list, alongside individual `BaseTool` instances.

When the agent initializes or needs to determine its available capabilities, the ADK framework will iterate through the `tools` list:

  * If an item is a `BaseTool` instance, it's used directly.
  * If an item is a `BaseToolset` instance, its `get_tools()` method is called (with the current `ReadonlyContext`), and the returned list of `BaseTool`s is added to the agent's available tools.

### Example: A Simple Math Toolset[¶](<https://adk.dev/tools-custom/#example-a-simple-math-toolset> "Permanent link")

Let's create a basic example of a toolset that provides simple arithmetic operations.

PythonTypeScriptJava
    
    [](<https://adk.dev/tools-custom/#__codelineno-20-1>)import asyncio
    [](<https://adk.dev/tools-custom/#__codelineno-20-2>)from typing import Optional, List, Dict, Any
    [](<https://adk.dev/tools-custom/#__codelineno-20-3>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-4>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/tools-custom/#__codelineno-20-5>)from google.adk.agents.readonly_context import ReadonlyContext
    [](<https://adk.dev/tools-custom/#__codelineno-20-6>)from google.adk.tools import BaseTool, FunctionTool
    [](<https://adk.dev/tools-custom/#__codelineno-20-7>)from google.adk.tools.base_toolset import BaseToolset
    [](<https://adk.dev/tools-custom/#__codelineno-20-8>)from google.adk.tools.tool_context import ToolContext
    [](<https://adk.dev/tools-custom/#__codelineno-20-9>)from google.adk.runners import InMemoryRunner
    [](<https://adk.dev/tools-custom/#__codelineno-20-10>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-11>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-12>)# 1. Define the individual tool functions
    [](<https://adk.dev/tools-custom/#__codelineno-20-13>)def add_numbers(a: int, b: int, tool_context: ToolContext) -> Dict[str, Any]:
    [](<https://adk.dev/tools-custom/#__codelineno-20-14>)    """Adds two integer numbers.
    [](<https://adk.dev/tools-custom/#__codelineno-20-15>)    Args:
    [](<https://adk.dev/tools-custom/#__codelineno-20-16>)        a: The first number.
    [](<https://adk.dev/tools-custom/#__codelineno-20-17>)        b: The second number.
    [](<https://adk.dev/tools-custom/#__codelineno-20-18>)    Returns:
    [](<https://adk.dev/tools-custom/#__codelineno-20-19>)        A dictionary with the sum, e.g., {'status': 'success', 'result': 5}
    [](<https://adk.dev/tools-custom/#__codelineno-20-20>)    """
    [](<https://adk.dev/tools-custom/#__codelineno-20-21>)    print(f"Tool: add_numbers called with a={a}, b={b}")
    [](<https://adk.dev/tools-custom/#__codelineno-20-22>)    result = a + b
    [](<https://adk.dev/tools-custom/#__codelineno-20-23>)    # Example: Storing something in tool_context state
    [](<https://adk.dev/tools-custom/#__codelineno-20-24>)    tool_context.state["last_math_operation"] = "addition"
    [](<https://adk.dev/tools-custom/#__codelineno-20-25>)    return {"status": "success", "result": result}
    [](<https://adk.dev/tools-custom/#__codelineno-20-26>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-27>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-28>)def subtract_numbers(a: int, b: int) -> Dict[str, Any]:
    [](<https://adk.dev/tools-custom/#__codelineno-20-29>)    """Subtracts the second number from the first.
    [](<https://adk.dev/tools-custom/#__codelineno-20-30>)    Args:
    [](<https://adk.dev/tools-custom/#__codelineno-20-31>)        a: The first number.
    [](<https://adk.dev/tools-custom/#__codelineno-20-32>)        b: The second number.
    [](<https://adk.dev/tools-custom/#__codelineno-20-33>)    Returns:
    [](<https://adk.dev/tools-custom/#__codelineno-20-34>)        A dictionary with the difference, e.g., {'status': 'success', 'result': 1}
    [](<https://adk.dev/tools-custom/#__codelineno-20-35>)    """
    [](<https://adk.dev/tools-custom/#__codelineno-20-36>)    print(f"Tool: subtract_numbers called with a={a}, b={b}")
    [](<https://adk.dev/tools-custom/#__codelineno-20-37>)    return {"status": "success", "result": a - b}
    [](<https://adk.dev/tools-custom/#__codelineno-20-38>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-39>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-40>)# 2. Create the Toolset by implementing BaseToolset
    [](<https://adk.dev/tools-custom/#__codelineno-20-41>)class SimpleMathToolset(BaseToolset):
    [](<https://adk.dev/tools-custom/#__codelineno-20-42>)    def __init__(self, prefix: str = "math"):
    [](<https://adk.dev/tools-custom/#__codelineno-20-43>)        self.prefix = prefix
    [](<https://adk.dev/tools-custom/#__codelineno-20-44>)        super().__init__(tool_name_prefix=self.prefix) # Toolset can customize names by passing a prefix
    [](<https://adk.dev/tools-custom/#__codelineno-20-45>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-46>)        # Create FunctionTool instances once
    [](<https://adk.dev/tools-custom/#__codelineno-20-47>)        self._add_tool = FunctionTool(
    [](<https://adk.dev/tools-custom/#__codelineno-20-48>)            func=add_numbers,
    [](<https://adk.dev/tools-custom/#__codelineno-20-49>)        )
    [](<https://adk.dev/tools-custom/#__codelineno-20-50>)        self._subtract_tool = FunctionTool(
    [](<https://adk.dev/tools-custom/#__codelineno-20-51>)            func=subtract_numbers,
    [](<https://adk.dev/tools-custom/#__codelineno-20-52>)        )
    [](<https://adk.dev/tools-custom/#__codelineno-20-53>)        print(f"SimpleMathToolset initialized with prefix '{self.prefix}'")
    [](<https://adk.dev/tools-custom/#__codelineno-20-54>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-55>)    async def get_tools(
    [](<https://adk.dev/tools-custom/#__codelineno-20-56>)        self, readonly_context: Optional[ReadonlyContext] = None
    [](<https://adk.dev/tools-custom/#__codelineno-20-57>)    ) -> List[BaseTool]:
    [](<https://adk.dev/tools-custom/#__codelineno-20-58>)        print("SimpleMathToolset.get_tools() called.")
    [](<https://adk.dev/tools-custom/#__codelineno-20-59>)        # Example of dynamic behavior:
    [](<https://adk.dev/tools-custom/#__codelineno-20-60>)        # Could use readonly_context.state to decide which tools to return
    [](<https://adk.dev/tools-custom/#__codelineno-20-61>)        # For instance, if readonly_context.state.get("enable_advanced_math"):
    [](<https://adk.dev/tools-custom/#__codelineno-20-62>)        #    return [self._add_tool, self._subtract_tool, self._multiply_tool]
    [](<https://adk.dev/tools-custom/#__codelineno-20-63>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-64>)        # For this simple example, always return both tools
    [](<https://adk.dev/tools-custom/#__codelineno-20-65>)        tools_to_return = [self._add_tool, self._subtract_tool]
    [](<https://adk.dev/tools-custom/#__codelineno-20-66>)        print(f"SimpleMathToolset providing tools: {[t.name for t in tools_to_return]}")
    [](<https://adk.dev/tools-custom/#__codelineno-20-67>)        return tools_to_return
    [](<https://adk.dev/tools-custom/#__codelineno-20-68>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-69>)    async def close(self) -> None:
    [](<https://adk.dev/tools-custom/#__codelineno-20-70>)        # No resources to clean up in this simple example
    [](<https://adk.dev/tools-custom/#__codelineno-20-71>)        print(f"SimpleMathToolset.close() called for prefix '{self.prefix}'.")
    [](<https://adk.dev/tools-custom/#__codelineno-20-72>)        await asyncio.sleep(0)  # Placeholder for async cleanup if needed
    [](<https://adk.dev/tools-custom/#__codelineno-20-73>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-74>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-75>)# 3. Define an individual tool (not part of the toolset)
    [](<https://adk.dev/tools-custom/#__codelineno-20-76>)def greet_user(name: str = "User") -> Dict[str, str]:
    [](<https://adk.dev/tools-custom/#__codelineno-20-77>)    """Greets the user."""
    [](<https://adk.dev/tools-custom/#__codelineno-20-78>)    print(f"Tool: greet_user called with name={name}")
    [](<https://adk.dev/tools-custom/#__codelineno-20-79>)    return {"greeting": f"Hello, {name}!"}
    [](<https://adk.dev/tools-custom/#__codelineno-20-80>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-81>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-82>)greet_tool = FunctionTool(func=greet_user)
    [](<https://adk.dev/tools-custom/#__codelineno-20-83>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-84>)# 4. Instantiate the toolset
    [](<https://adk.dev/tools-custom/#__codelineno-20-85>)math_toolset_instance = SimpleMathToolset(prefix="calculator")
    [](<https://adk.dev/tools-custom/#__codelineno-20-86>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-87>)# 5. Define an agent that uses both the individual tool and the toolset
    [](<https://adk.dev/tools-custom/#__codelineno-20-88>)calculator_agent = LlmAgent(
    [](<https://adk.dev/tools-custom/#__codelineno-20-89>)    name="CalculatorAgent",
    [](<https://adk.dev/tools-custom/#__codelineno-20-90>)    model="gemini-flash-latest",  # Replace with your desired model
    [](<https://adk.dev/tools-custom/#__codelineno-20-91>)    instruction="You are a helpful calculator and greeter. "
    [](<https://adk.dev/tools-custom/#__codelineno-20-92>)    "Use 'greet_user' for greetings. "
    [](<https://adk.dev/tools-custom/#__codelineno-20-93>)    "Use 'calculator_add_numbers' to add and 'calculator_subtract_numbers' to subtract. "
    [](<https://adk.dev/tools-custom/#__codelineno-20-94>)    "Announce the state of 'last_math_operation' if it's set.",
    [](<https://adk.dev/tools-custom/#__codelineno-20-95>)    tools=[greet_tool, math_toolset_instance],  # Individual tool  # Toolset instance
    [](<https://adk.dev/tools-custom/#__codelineno-20-96>))
    [](<https://adk.dev/tools-custom/#__codelineno-20-97>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-98>)# 6. Run the agent
    [](<https://adk.dev/tools-custom/#__codelineno-20-99>)runner = InMemoryRunner(agent=calculator_agent, app_name="toolset_example_app")
    [](<https://adk.dev/tools-custom/#__codelineno-20-100>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-101>)async def main():
    [](<https://adk.dev/tools-custom/#__codelineno-20-102>)    print("\n--- Query 1: Greeting ---")
    [](<https://adk.dev/tools-custom/#__codelineno-20-103>)    await runner.run_debug("Hi there!")
    [](<https://adk.dev/tools-custom/#__codelineno-20-104>)    print("\n--- Query 2: Addition ---")
    [](<https://adk.dev/tools-custom/#__codelineno-20-105>)    await runner.run_debug("What is 5 plus 3?")
    [](<https://adk.dev/tools-custom/#__codelineno-20-106>)    await math_toolset_instance.close()
    [](<https://adk.dev/tools-custom/#__codelineno-20-107>)
    [](<https://adk.dev/tools-custom/#__codelineno-20-108>)if __name__ == "__main__":
    [](<https://adk.dev/tools-custom/#__codelineno-20-109>)    asyncio.run(main())
    
    [](<https://adk.dev/tools-custom/#__codelineno-21-1>)/**
    [](<https://adk.dev/tools-custom/#__codelineno-21-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/#__codelineno-21-3>) *
    [](<https://adk.dev/tools-custom/#__codelineno-21-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/#__codelineno-21-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/#__codelineno-21-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/#__codelineno-21-7>) *
    [](<https://adk.dev/tools-custom/#__codelineno-21-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/#__codelineno-21-9>) *
    [](<https://adk.dev/tools-custom/#__codelineno-21-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/#__codelineno-21-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/#__codelineno-21-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/#__codelineno-21-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/#__codelineno-21-14>) * limitations under the License.
    [](<https://adk.dev/tools-custom/#__codelineno-21-15>) */
    [](<https://adk.dev/tools-custom/#__codelineno-21-16>)import { LlmAgent, FunctionTool, Context, BaseToolset, InMemoryRunner, isFinalResponse, BaseTool, stringifyContent } from '@google/adk';
    [](<https://adk.dev/tools-custom/#__codelineno-21-17>)import { z } from "zod";
    [](<https://adk.dev/tools-custom/#__codelineno-21-18>)import { Content, createUserContent } from "@google/genai";
    [](<https://adk.dev/tools-custom/#__codelineno-21-19>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-20>)function addNumbers(params: { a: number; b: number }, context?: Context): Record<string, any> {
    [](<https://adk.dev/tools-custom/#__codelineno-21-21>)  if (!context) {
    [](<https://adk.dev/tools-custom/#__codelineno-21-22>)    throw new Error("Context is required for this tool.");
    [](<https://adk.dev/tools-custom/#__codelineno-21-23>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-21-24>)  const result = params.a + params.b;
    [](<https://adk.dev/tools-custom/#__codelineno-21-25>)  context.state.set("last_math_result", result);
    [](<https://adk.dev/tools-custom/#__codelineno-21-26>)  return { result: result };
    [](<https://adk.dev/tools-custom/#__codelineno-21-27>)}
    [](<https://adk.dev/tools-custom/#__codelineno-21-28>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-29>)function subtractNumbers(params: { a: number; b: number }): Record<string, any> {
    [](<https://adk.dev/tools-custom/#__codelineno-21-30>)  return { result: params.a - params.b };
    [](<https://adk.dev/tools-custom/#__codelineno-21-31>)}
    [](<https://adk.dev/tools-custom/#__codelineno-21-32>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-33>)function greetUser(params: { name: string }): Record<string, any> {
    [](<https://adk.dev/tools-custom/#__codelineno-21-34>)  return { greeting: `Hello, ${params.name}!` };
    [](<https://adk.dev/tools-custom/#__codelineno-21-35>)}
    [](<https://adk.dev/tools-custom/#__codelineno-21-36>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-37>)class SimpleMathToolset extends BaseToolset {
    [](<https://adk.dev/tools-custom/#__codelineno-21-38>)  private readonly tools: BaseTool[];
    [](<https://adk.dev/tools-custom/#__codelineno-21-39>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-40>)  constructor(prefix = "") {
    [](<https://adk.dev/tools-custom/#__codelineno-21-41>)    super([]); // No filter
    [](<https://adk.dev/tools-custom/#__codelineno-21-42>)    this.tools = [
    [](<https://adk.dev/tools-custom/#__codelineno-21-43>)      new FunctionTool({
    [](<https://adk.dev/tools-custom/#__codelineno-21-44>)        name: `${prefix}add_numbers`,
    [](<https://adk.dev/tools-custom/#__codelineno-21-45>)        description: "Adds two numbers and stores the result in the session state.",
    [](<https://adk.dev/tools-custom/#__codelineno-21-46>)        parameters: z.object({ a: z.number(), b: z.number() }),
    [](<https://adk.dev/tools-custom/#__codelineno-21-47>)        execute: addNumbers,
    [](<https://adk.dev/tools-custom/#__codelineno-21-48>)      }),
    [](<https://adk.dev/tools-custom/#__codelineno-21-49>)      new FunctionTool({
    [](<https://adk.dev/tools-custom/#__codelineno-21-50>)        name: `${prefix}subtract_numbers`,
    [](<https://adk.dev/tools-custom/#__codelineno-21-51>)        description: "Subtracts the second number from the first.",
    [](<https://adk.dev/tools-custom/#__codelineno-21-52>)        parameters: z.object({ a: z.number(), b: z.number() }),
    [](<https://adk.dev/tools-custom/#__codelineno-21-53>)        execute: subtractNumbers,
    [](<https://adk.dev/tools-custom/#__codelineno-21-54>)      }),
    [](<https://adk.dev/tools-custom/#__codelineno-21-55>)    ];
    [](<https://adk.dev/tools-custom/#__codelineno-21-56>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-21-57>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-58>)  async getTools(): Promise<BaseTool[]> {
    [](<https://adk.dev/tools-custom/#__codelineno-21-59>)    return this.tools;
    [](<https://adk.dev/tools-custom/#__codelineno-21-60>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-21-61>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-62>)  async close(): Promise<void> {
    [](<https://adk.dev/tools-custom/#__codelineno-21-63>)    console.log("SimpleMathToolset closed.");
    [](<https://adk.dev/tools-custom/#__codelineno-21-64>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-21-65>)}
    [](<https://adk.dev/tools-custom/#__codelineno-21-66>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-67>)async function main() {
    [](<https://adk.dev/tools-custom/#__codelineno-21-68>)  const mathToolset = new SimpleMathToolset("calculator_");
    [](<https://adk.dev/tools-custom/#__codelineno-21-69>)  const greetTool = new FunctionTool({
    [](<https://adk.dev/tools-custom/#__codelineno-21-70>)    name: "greet_user",
    [](<https://adk.dev/tools-custom/#__codelineno-21-71>)    description: "Greets the user.",
    [](<https://adk.dev/tools-custom/#__codelineno-21-72>)    parameters: z.object({ name: z.string() }),
    [](<https://adk.dev/tools-custom/#__codelineno-21-73>)    execute: greetUser,
    [](<https://adk.dev/tools-custom/#__codelineno-21-74>)  });
    [](<https://adk.dev/tools-custom/#__codelineno-21-75>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-76>)  const instruction =
    [](<https://adk.dev/tools-custom/#__codelineno-21-77>)    `You are a calculator and a greeter.
    [](<https://adk.dev/tools-custom/#__codelineno-21-78>)    If the user asks for a math operation, use the calculator tools.
    [](<https://adk.dev/tools-custom/#__codelineno-21-79>)    If the user asks for a greeting, use the greet_user tool.
    [](<https://adk.dev/tools-custom/#__codelineno-21-80>)    The result of the last math operation is stored in the 'last_math_result' state variable.`;
    [](<https://adk.dev/tools-custom/#__codelineno-21-81>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-82>)  const calculatorAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/#__codelineno-21-83>)    name: "calculator_agent",
    [](<https://adk.dev/tools-custom/#__codelineno-21-84>)    instruction: instruction,
    [](<https://adk.dev/tools-custom/#__codelineno-21-85>)    tools: [greetTool, mathToolset],
    [](<https://adk.dev/tools-custom/#__codelineno-21-86>)    model: "gemini-2.5-flash",
    [](<https://adk.dev/tools-custom/#__codelineno-21-87>)  });
    [](<https://adk.dev/tools-custom/#__codelineno-21-88>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-89>)  const runner = new InMemoryRunner({ agent: calculatorAgent, appName: "toolset_app" });
    [](<https://adk.dev/tools-custom/#__codelineno-21-90>)  await runner.sessionService.createSession({ appName: "toolset_app", userId: "user1", sessionId: "session1" });
    [](<https://adk.dev/tools-custom/#__codelineno-21-91>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-92>)  const message: Content = createUserContent("What is 5 + 3?");
    [](<https://adk.dev/tools-custom/#__codelineno-21-93>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-94>)  for await (const event of runner.runAsync({ userId: "user1", sessionId: "session1", newMessage: message })) {
    [](<https://adk.dev/tools-custom/#__codelineno-21-95>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/tools-custom/#__codelineno-21-96>)      const text = stringifyContent(event).trim();
    [](<https://adk.dev/tools-custom/#__codelineno-21-97>)      if (text) {
    [](<https://adk.dev/tools-custom/#__codelineno-21-98>)        console.log(`Response from agent: ${text}`);
    [](<https://adk.dev/tools-custom/#__codelineno-21-99>)      }
    [](<https://adk.dev/tools-custom/#__codelineno-21-100>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-21-101>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-21-102>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-103>)  await mathToolset.close();
    [](<https://adk.dev/tools-custom/#__codelineno-21-104>)}
    [](<https://adk.dev/tools-custom/#__codelineno-21-105>)
    [](<https://adk.dev/tools-custom/#__codelineno-21-106>)main();
    
    [](<https://adk.dev/tools-custom/#__codelineno-22-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/#__codelineno-22-2>)import com.google.adk.agents.ReadonlyContext;
    [](<https://adk.dev/tools-custom/#__codelineno-22-3>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/tools-custom/#__codelineno-22-4>)import com.google.adk.tools.BaseTool;
    [](<https://adk.dev/tools-custom/#__codelineno-22-5>)import com.google.adk.tools.BaseToolset;
    [](<https://adk.dev/tools-custom/#__codelineno-22-6>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/tools-custom/#__codelineno-22-7>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/tools-custom/#__codelineno-22-8>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/tools-custom/#__codelineno-22-9>)import java.util.HashMap;
    [](<https://adk.dev/tools-custom/#__codelineno-22-10>)import java.util.Map;
    [](<https://adk.dev/tools-custom/#__codelineno-22-11>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-12>)public class SimpleMathToolsetApp {
    [](<https://adk.dev/tools-custom/#__codelineno-22-13>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-14>)  // 1. Define the individual tool functions
    [](<https://adk.dev/tools-custom/#__codelineno-22-15>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-16>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-22-17>)   * Adds two integer numbers.
    [](<https://adk.dev/tools-custom/#__codelineno-22-18>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-22-19>)   * @param a The first number.
    [](<https://adk.dev/tools-custom/#__codelineno-22-20>)   * @param b The second number.
    [](<https://adk.dev/tools-custom/#__codelineno-22-21>)   * @param toolContext The tool context.
    [](<https://adk.dev/tools-custom/#__codelineno-22-22>)   * @return A map with the sum.
    [](<https://adk.dev/tools-custom/#__codelineno-22-23>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-22-24>)  public static Map<String, Object> addNumbers(
    [](<https://adk.dev/tools-custom/#__codelineno-22-25>)      @Schema(name = "a", description = "The first number") int a,
    [](<https://adk.dev/tools-custom/#__codelineno-22-26>)      @Schema(name = "b", description = "The second number") int b,
    [](<https://adk.dev/tools-custom/#__codelineno-22-27>)      ToolContext toolContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-22-28>)    System.out.println("Tool: add_numbers called with a=" + a + ", b=" + b);
    [](<https://adk.dev/tools-custom/#__codelineno-22-29>)    int result = a + b;
    [](<https://adk.dev/tools-custom/#__codelineno-22-30>)    // Example: Storing something in tool_context state
    [](<https://adk.dev/tools-custom/#__codelineno-22-31>)    toolContext.state().put("last_math_operation", "addition");
    [](<https://adk.dev/tools-custom/#__codelineno-22-32>)    Map<String, Object> response = new HashMap<>();
    [](<https://adk.dev/tools-custom/#__codelineno-22-33>)    response.put("status", "success");
    [](<https://adk.dev/tools-custom/#__codelineno-22-34>)    response.put("result", result);
    [](<https://adk.dev/tools-custom/#__codelineno-22-35>)    return response;
    [](<https://adk.dev/tools-custom/#__codelineno-22-36>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-22-37>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-38>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-22-39>)   * Subtracts the second number from the first.
    [](<https://adk.dev/tools-custom/#__codelineno-22-40>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-22-41>)   * @param a The first number.
    [](<https://adk.dev/tools-custom/#__codelineno-22-42>)   * @param b The second number.
    [](<https://adk.dev/tools-custom/#__codelineno-22-43>)   * @return A map with the difference.
    [](<https://adk.dev/tools-custom/#__codelineno-22-44>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-22-45>)  public static Map<String, Object> subtractNumbers(
    [](<https://adk.dev/tools-custom/#__codelineno-22-46>)      @Schema(name = "a", description = "The first number") int a,
    [](<https://adk.dev/tools-custom/#__codelineno-22-47>)      @Schema(name = "b", description = "The second number") int b) {
    [](<https://adk.dev/tools-custom/#__codelineno-22-48>)    System.out.println("Tool: subtract_numbers called with a=" + a + ", b=" + b);
    [](<https://adk.dev/tools-custom/#__codelineno-22-49>)    Map<String, Object> response = new HashMap<>();
    [](<https://adk.dev/tools-custom/#__codelineno-22-50>)    response.put("status", "success");
    [](<https://adk.dev/tools-custom/#__codelineno-22-51>)    response.put("result", a - b);
    [](<https://adk.dev/tools-custom/#__codelineno-22-52>)    return response;
    [](<https://adk.dev/tools-custom/#__codelineno-22-53>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-22-54>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-55>)  // 2. Create the Toolset by implementing BaseToolset
    [](<https://adk.dev/tools-custom/#__codelineno-22-56>)  public static class SimpleMathToolset implements BaseToolset {
    [](<https://adk.dev/tools-custom/#__codelineno-22-57>)    private final BaseTool addTool;
    [](<https://adk.dev/tools-custom/#__codelineno-22-58>)    private final BaseTool subtractTool;
    [](<https://adk.dev/tools-custom/#__codelineno-22-59>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-60>)    public SimpleMathToolset() throws NoSuchMethodException {
    [](<https://adk.dev/tools-custom/#__codelineno-22-61>)      // Create FunctionTool instances once
    [](<https://adk.dev/tools-custom/#__codelineno-22-62>)      this.addTool =
    [](<https://adk.dev/tools-custom/#__codelineno-22-63>)          FunctionTool.create(
    [](<https://adk.dev/tools-custom/#__codelineno-22-64>)              SimpleMathToolsetApp.class.getMethod(
    [](<https://adk.dev/tools-custom/#__codelineno-22-65>)                  "addNumbers", int.class, int.class, ToolContext.class));
    [](<https://adk.dev/tools-custom/#__codelineno-22-66>)      this.subtractTool =
    [](<https://adk.dev/tools-custom/#__codelineno-22-67>)          FunctionTool.create(
    [](<https://adk.dev/tools-custom/#__codelineno-22-68>)              SimpleMathToolsetApp.class.getMethod("subtractNumbers", int.class, int.class));
    [](<https://adk.dev/tools-custom/#__codelineno-22-69>)      System.out.println("SimpleMathToolset initialized");
    [](<https://adk.dev/tools-custom/#__codelineno-22-70>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-22-71>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-72>)    @Override
    [](<https://adk.dev/tools-custom/#__codelineno-22-73>)    public Flowable<BaseTool> getTools(ReadonlyContext readonlyContext) {
    [](<https://adk.dev/tools-custom/#__codelineno-22-74>)      System.out.println("SimpleMathToolset.getTools() called.");
    [](<https://adk.dev/tools-custom/#__codelineno-22-75>)      // Example of dynamic behavior:
    [](<https://adk.dev/tools-custom/#__codelineno-22-76>)      // Could use readonlyContext to access state and conditionally return tools.
    [](<https://adk.dev/tools-custom/#__codelineno-22-77>)      // For this simple example, always return both tools:
    [](<https://adk.dev/tools-custom/#__codelineno-22-78>)      return Flowable.just(addTool, subtractTool);
    [](<https://adk.dev/tools-custom/#__codelineno-22-79>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-22-80>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-81>)    @Override
    [](<https://adk.dev/tools-custom/#__codelineno-22-82>)    public void close() throws Exception {
    [](<https://adk.dev/tools-custom/#__codelineno-22-83>)      // No resources to clean up in this simple example
    [](<https://adk.dev/tools-custom/#__codelineno-22-84>)      System.out.println("SimpleMathToolset.close() called.");
    [](<https://adk.dev/tools-custom/#__codelineno-22-85>)    }
    [](<https://adk.dev/tools-custom/#__codelineno-22-86>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-22-87>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-88>)  // 3. Define an individual tool (not part of the toolset)
    [](<https://adk.dev/tools-custom/#__codelineno-22-89>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-90>)  /**
    [](<https://adk.dev/tools-custom/#__codelineno-22-91>)   * Greets the user.
    [](<https://adk.dev/tools-custom/#__codelineno-22-92>)   *
    [](<https://adk.dev/tools-custom/#__codelineno-22-93>)   * @param name The name of the user.
    [](<https://adk.dev/tools-custom/#__codelineno-22-94>)   * @return A map with the greeting.
    [](<https://adk.dev/tools-custom/#__codelineno-22-95>)   */
    [](<https://adk.dev/tools-custom/#__codelineno-22-96>)  public static Map<String, Object> greetUser(
    [](<https://adk.dev/tools-custom/#__codelineno-22-97>)      @Schema(name = "name", description = "The name of the user") String name) {
    [](<https://adk.dev/tools-custom/#__codelineno-22-98>)    System.out.println("Tool: greetUser called with name=" + name);
    [](<https://adk.dev/tools-custom/#__codelineno-22-99>)    Map<String, Object> response = new HashMap<>();
    [](<https://adk.dev/tools-custom/#__codelineno-22-100>)    response.put("greeting", "Hello, " + name + "!");
    [](<https://adk.dev/tools-custom/#__codelineno-22-101>)    return response;
    [](<https://adk.dev/tools-custom/#__codelineno-22-102>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-22-103>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-104>)  public static void main(String[] args) throws Exception {
    [](<https://adk.dev/tools-custom/#__codelineno-22-105>)    BaseTool greetTool =
    [](<https://adk.dev/tools-custom/#__codelineno-22-106>)        FunctionTool.create(SimpleMathToolsetApp.class.getMethod("greetUser", String.class));
    [](<https://adk.dev/tools-custom/#__codelineno-22-107>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-108>)    // 4. Instantiate the toolset
    [](<https://adk.dev/tools-custom/#__codelineno-22-109>)    BaseToolset mathToolsetInstance = new SimpleMathToolset();
    [](<https://adk.dev/tools-custom/#__codelineno-22-110>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-111>)    // 5. Define an agent that uses both the individual tool and the toolset
    [](<https://adk.dev/tools-custom/#__codelineno-22-112>)    LlmAgent calculatorAgent =
    [](<https://adk.dev/tools-custom/#__codelineno-22-113>)        LlmAgent.builder()
    [](<https://adk.dev/tools-custom/#__codelineno-22-114>)            .name("CalculatorAgent")
    [](<https://adk.dev/tools-custom/#__codelineno-22-115>)            .model("gemini-2.5-flash") // Replace with your desired model
    [](<https://adk.dev/tools-custom/#__codelineno-22-116>)            .instruction(
    [](<https://adk.dev/tools-custom/#__codelineno-22-117>)                "You are a helpful calculator and greeter. "
    [](<https://adk.dev/tools-custom/#__codelineno-22-118>)                    + "Use 'greetUser' for greetings. "
    [](<https://adk.dev/tools-custom/#__codelineno-22-119>)                    + "Use 'addNumbers' to add and 'subtractNumbers' to subtract. "
    [](<https://adk.dev/tools-custom/#__codelineno-22-120>)                    + "Announce the state of 'last_math_operation' if it's set.")
    [](<https://adk.dev/tools-custom/#__codelineno-22-121>)            .tools(greetTool, mathToolsetInstance) // Individual tool and Toolset instance
    [](<https://adk.dev/tools-custom/#__codelineno-22-122>)            .build();
    [](<https://adk.dev/tools-custom/#__codelineno-22-123>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-124>)    // System.out.println("Agent '" + calculatorAgent.name() + "' created.");
    [](<https://adk.dev/tools-custom/#__codelineno-22-125>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-126>)    // Runner runner = new Runner(calculatorAgent, ...);
    [](<https://adk.dev/tools-custom/#__codelineno-22-127>)    // ... setup and usage ...
    [](<https://adk.dev/tools-custom/#__codelineno-22-128>)
    [](<https://adk.dev/tools-custom/#__codelineno-22-129>)    // Important: Clean up the toolset if it manages resources
    [](<https://adk.dev/tools-custom/#__codelineno-22-130>)    mathToolsetInstance.close();
    [](<https://adk.dev/tools-custom/#__codelineno-22-131>)  }
    [](<https://adk.dev/tools-custom/#__codelineno-22-132>)}
    
In this example:

  * `SimpleMathToolset` implements `BaseToolset` and its `get_tools()` method returns `FunctionTool` instances for `add_numbers` and `subtract_numbers`. It also customizes their names using a prefix.
  * The `calculator_agent` is configured with both an individual `greet_tool` and an instance of `SimpleMathToolset`.
  * When `calculator_agent` is run, ADK will call `math_toolset_instance.get_tools()`. The agent's LLM will then have access to `greet_user`, `calculator_add_numbers`, and `calculator_subtract_numbers` to handle user requests.
  * The `add_numbers` tool demonstrates writing to `tool_context.state`, and the agent's instruction mentions reading this state.
  * The `close()` method is called to ensure any resources held by the toolset are released.

Toolsets offer a powerful way to organize, manage, and dynamically provide collections of tools to your ADK agents, leading to more modular, maintainable, and adaptable agentic applications.

Back to top 