# Types of callbacks - Agent Development Kit (ADK)

> Source: [https://adk.dev/callbacks/types-of-callbacks/](https://adk.dev/callbacks/types-of-callbacks/)

[ Skip to content ](<https://adk.dev/callbacks/types-of-callbacks/#types-of-callbacks>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/callbacks/types-of-callbacks.md> "Edit this page on GitHub") [ ](<https://adk.dev/callbacks/types-of-callbacks/index.md> "View this page as Markdown")

# Types of Callbacks[¶](<https://adk.dev/callbacks/types-of-callbacks/#types-of-callbacks> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0

The framework provides different types of callbacks that trigger at various stages of an agent's execution. Understanding when each callback fires and what context it receives is key to using them effectively.

## Agent Lifecycle Callbacks[¶](<https://adk.dev/callbacks/types-of-callbacks/#agent-lifecycle-callbacks> "Permanent link")

These callbacks are available on _any_ agent that inherits from `BaseAgent` (including `LlmAgent`, `SequentialAgent`, `ParallelAgent`, `LoopAgent`, etc).

Note

The specific method names or return types may vary slightly by SDK language (e.g., return `None` in Python, return `Optional.empty()` or `Maybe.empty()` in Java). Refer to the language-specific API documentation for details.

Python: Use the documented callback parameter names

In Python, callback function parameter names must match the documented names exactly because ADK passes callback arguments by keyword. For example, use `callback_context` for agent and model callbacks, and `tool_context` for tool callbacks. Renaming these parameters to aliases such as `ctx` will cause runtime `TypeError` failures.
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-0-1>)# Correct
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-0-2>)def before_agent_callback(callback_context):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-0-3>)    ...
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-0-4>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-0-5>)# Incorrect
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-0-6>)def before_agent_callback(ctx):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-0-7>)    ...
    
Callback | Required parameter names  
---|---  
`before_agent_callback` | `callback_context`  
`after_agent_callback` | `callback_context`  
`before_model_callback` | `callback_context`, `llm_request`  
`after_model_callback` | `callback_context`, `llm_response`  
`before_tool_callback` | `tool`, `args`, `tool_context`  
`after_tool_callback` | `tool`, `args`, `tool_context`, `tool_response`  
  
### Before Agent Callback[¶](<https://adk.dev/callbacks/types-of-callbacks/#before-agent-callback> "Permanent link")

**When:** Called _immediately before_ the agent's `_run_async_impl` (or `_run_live_impl`) method is executed. It runs after the agent's `InvocationContext` is created but _before_ its core logic begins.

**Purpose:** Ideal for setting up resources or state needed only for this specific agent's run, performing validation checks on the session state (callback_context.state) before execution starts, logging the entry point of the agent's activity, or potentially modifying the invocation context before the core logic uses it.

Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-2>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-6>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-8>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-13>)# limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-15>)# # --- Setup Instructions ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-16>)# # 1. Install the ADK package:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-17>)# !pip install google-adk
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-18>)# # Make sure to restart kernel if using colab/jupyter notebooks
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-20>)# # 2. Set up your Gemini API Key:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-21>)# #    - Get a key from Google AI Studio: https://aistudio.google.com/app/apikey
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-22>)# #    - Set it as an environment variable:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-23>)# import os
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-24>)# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE" # <--- REPLACE with your actual key
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-25>)# # Or learn about other authentication methods (like Agent Platform):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-26>)# # https://adk.dev/agents/models/
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-27>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-28>)# ADK Imports
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-29>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-30>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-31>)from google.adk.runners import InMemoryRunner  # Use InMemoryRunner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-32>)from google.genai import types  # For types.Content
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-33>)from typing import Optional
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-34>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-35>)# Define the model - Use the specific model name requested
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-36>)GEMINI_2_FLASH = "gemini-2.0-flash"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-37>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-38>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-39>)# --- 1. Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-40>)def check_if_agent_should_run(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-41>)    callback_context: CallbackContext,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-42>)) -> Optional[types.Content]:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-43>)    """
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-44>)    Logs entry and checks 'skip_llm_agent' in session state.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-45>)    If True, returns Content to skip the agent's execution.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-46>)    If False or not present, returns None to allow execution.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-47>)    """
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-48>)    agent_name = callback_context.agent_name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-49>)    invocation_id = callback_context.invocation_id
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-50>)    current_state = callback_context.state.to_dict()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-51>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-52>)    print(f"\n[Callback] Entering agent: {agent_name} (Inv: {invocation_id})")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-53>)    print(f"[Callback] Current State: {current_state}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-54>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-55>)    # Check the condition in session state dictionary
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-56>)    if current_state.get("skip_llm_agent", False):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-57>)        print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-58>)            f"[Callback] State condition 'skip_llm_agent=True' met: Skipping agent {agent_name}."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-59>)        )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-60>)        # Return Content to skip the agent's run
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-61>)        return types.Content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-62>)            parts=[
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-63>)                types.Part(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-64>)                    text=f"Agent {agent_name} skipped by before_agent_callback due to state."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-65>)                )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-66>)            ],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-67>)            role="model",  # Assign model role to the overriding response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-68>)        )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-69>)    else:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-70>)        print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-71>)            f"[Callback] State condition not met: Proceeding with agent {agent_name}."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-72>)        )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-73>)        # Return None to allow the LlmAgent's normal execution
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-74>)        return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-75>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-76>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-77>)# --- 2. Setup Agent with Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-78>)llm_agent_with_before_cb = LlmAgent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-79>)    name="MyControlledAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-80>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-81>)    instruction="You are a concise assistant.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-82>)    description="An LLM agent demonstrating stateful before_agent_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-83>)    before_agent_callback=check_if_agent_should_run,  # Assign the callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-84>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-85>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-86>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-87>)# --- 3. Setup Runner and Sessions using InMemoryRunner ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-88>)async def main():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-89>)    app_name = "before_agent_demo"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-90>)    user_id = "test_user"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-91>)    session_id_run = "session_will_run"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-92>)    session_id_skip = "session_will_skip"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-93>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-94>)    # Use InMemoryRunner - it includes InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-95>)    runner = InMemoryRunner(agent=llm_agent_with_before_cb, app_name=app_name)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-96>)    # Get the bundled session service to create sessions
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-97>)    session_service = runner.session_service
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-98>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-99>)    # Create session 1: Agent will run (default empty state)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-100>)    await session_service.create_session(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-101>)        app_name=app_name,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-102>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-103>)        session_id=session_id_run,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-104>)        # No initial state means 'skip_llm_agent' will be False in the callback check
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-105>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-106>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-107>)    # Create session 2: Agent will be skipped (state has skip_llm_agent=True)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-108>)    await session_service.create_session(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-109>)        app_name=app_name,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-110>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-111>)        session_id=session_id_skip,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-112>)        state={"skip_llm_agent": True},  # Set the state flag here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-113>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-114>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-115>)    # --- Scenario 1: Run where callback allows agent execution ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-116>)    print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-117>)        "\n"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-118>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-119>)        + f" SCENARIO 1: Running Agent on Session '{session_id_run}' (Should Proceed) "
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-120>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-121>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-122>)    async for event in runner.run_async(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-123>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-124>)        session_id=session_id_run,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-125>)        new_message=types.Content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-126>)            role="user", parts=[types.Part(text="Hello, please respond.")]
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-127>)        ),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-128>)    ):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-129>)        # Print final output (either from LLM or callback override)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-130>)        if event.is_final_response() and event.content:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-131>)            print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-132>)                f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-133>)            )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-134>)        elif event.is_error():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-135>)            print(f"Error Event: {event.error_details}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-136>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-137>)    # --- Scenario 2: Run where callback intercepts and skips agent ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-138>)    print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-139>)        "\n"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-140>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-141>)        + f" SCENARIO 2: Running Agent on Session '{session_id_skip}' (Should Skip) "
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-142>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-143>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-144>)    async for event in runner.run_async(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-145>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-146>)        session_id=session_id_skip,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-147>)        new_message=types.Content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-148>)            role="user", parts=[types.Part(text="This message won't reach the LLM.")]
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-149>)        ),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-150>)    ):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-151>)        # Print final output (either from LLM or callback override)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-152>)        if event.is_final_response() and event.content:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-153>)            print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-154>)                f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-155>)            )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-156>)        elif event.is_error():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-157>)            print(f"Error Event: {event.error_details}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-158>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-159>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-160>)# --- 4. Execute ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-161>)# In a Python script:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-162>)# import asyncio
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-163>)# if __name__ == "__main__":
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-164>)#     # Make sure GOOGLE_API_KEY environment variable is set if not using Agent Platform auth
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-165>)#     # Or ensure Application Default Credentials (ADC) are configured for Agent Platform
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-166>)#     asyncio.run(main())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-167>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-168>)# In a Jupyter Notebook or similar environment:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-1-169>)await main()
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-1>)/**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-3>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-7>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-9>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-14>) * limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-15>) */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-16>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-17>)import { LlmAgent, InMemoryRunner, Context, isFinalResponse } from '@google/adk';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-18>)import { Content, createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-20>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-21>)const APP_NAME = "before_agent_callback_app";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-22>)const USER_ID = "test_user_before_agent";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-23>)const SESSION_ID_RUN = "session_will_run";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-24>)const SESSION_ID_SKIP = "session_will_skip";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-26>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-27>)// --- 1. Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-28>)function checkIfAgentShouldRun(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-29>)  context: Context
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-30>)): Content | undefined {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-31>)  /**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-32>)   * Logs entry and checks 'skip_llm_agent' in session state.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-33>)   * If True, returns Content to skip the agent's execution.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-34>)   * If False or not present, returns undefined to allow execution.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-35>)   */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-36>)  const agentName = context.agentName;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-37>)  const invocationId = context.invocationId;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-38>)  const currentState = context.state;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-39>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-40>)  console.log(`\n[Callback] Entering agent: ${agentName} (Inv: ${invocationId})`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-41>)  console.log(`[Callback] Current State:`, currentState);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-42>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-43>)  // Check the condition in session state
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-44>)  if (currentState.get("skip_llm_agent") === true) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-45>)    console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-46>)      `[Callback] State condition 'skip_llm_agent=True' met: Skipping agent ${agentName}.`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-47>)    );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-48>)    // Return Content to skip the agent's run
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-49>)    return {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-50>)      parts: [
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-51>)        {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-52>)          text: `Agent ${agentName} skipped by before_agent_callback due to state.`,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-53>)        },
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-54>)      ],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-55>)      role: "model", // Assign model role to the overriding response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-56>)    };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-57>)  } else {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-58>)    console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-59>)      `[Callback] State condition not met: Proceeding with agent ${agentName}.`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-60>)    );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-61>)    // Return undefined to allow the LlmAgent's normal execution
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-62>)    return undefined;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-63>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-64>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-65>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-66>)// --- 2. Setup Agent with Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-67>)const llmAgentWithBeforeCb = new LlmAgent({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-68>)  name: "MyControlledAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-69>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-70>)  instruction: "You are a concise assistant.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-71>)  description: "An LLM agent demonstrating stateful before_agent_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-72>)  beforeAgentCallback: checkIfAgentShouldRun, // Assign the callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-73>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-74>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-75>)// --- 3. Setup Runner and Sessions using InMemoryRunner ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-76>)async function main() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-77>)  // Use InMemoryRunner - it includes InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-78>)  const runner = new InMemoryRunner({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-79>)    agent: llmAgentWithBeforeCb,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-80>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-81>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-82>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-83>)  // Create session 1: Agent will run (default empty state)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-84>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-85>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-86>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-87>)    sessionId: SESSION_ID_RUN,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-88>)    // No initial state means 'skip_llm_agent' will be False in the callback check
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-89>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-90>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-91>)  // Create session 2: Agent will be skipped (state has skip_llm_agent=True)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-92>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-93>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-94>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-95>)    sessionId: SESSION_ID_SKIP,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-96>)    state: { skip_llm_agent: true }, // Set the state flag here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-97>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-98>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-99>)  // --- Scenario 1: Run where callback allows agent execution ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-100>)  console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-101>)    `\n==================== SCENARIO 1: Running Agent on Session "${SESSION_ID_RUN}" (Should Proceed) ====================`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-102>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-103>)  const eventsRun = runner.runAsync({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-104>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-105>)    sessionId: SESSION_ID_RUN,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-106>)    newMessage: createUserContent("Hello, please respond."),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-107>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-108>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-109>)  for await (const event of eventsRun) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-110>)    // Print final output (either from LLM or callback override)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-111>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-112>)      const finalResponse = event.content.parts
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-113>)        .map((part: any) => part.text ?? "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-114>)        .join("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-115>)      console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-116>)        `Final Output: [${event.author}] ${finalResponse.trim()}`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-117>)      );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-118>)    } else if (event.errorMessage) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-119>)      console.log(`Error Event: ${event.errorMessage}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-120>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-121>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-122>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-123>)  // --- Scenario 2: Run where callback intercepts and skips agent ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-124>)  console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-125>)    `\n==================== SCENARIO 2: Running Agent on Session "${SESSION_ID_SKIP}" (Should Skip) ====================`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-126>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-127>)  const eventsSkip = runner.runAsync({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-128>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-129>)    sessionId: SESSION_ID_SKIP,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-130>)    newMessage: createUserContent("This message won't reach the LLM."),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-131>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-132>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-133>)  for await (const event of eventsSkip) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-134>)    // Print final output (either from LLM or callback override)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-135>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-136>)      const finalResponse = event.content.parts
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-137>)        .map((part: any) => part.text ?? "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-138>)        .join("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-139>)      console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-140>)        `Final Output: [${event.author}] ${finalResponse.trim()}`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-141>)      );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-142>)    } else if (event.errorMessage) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-143>)      console.log(`Error Event: ${event.errorMessage}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-144>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-145>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-146>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-147>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-148>)// --- 4. Execute ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-2-149>)main();
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-1>)package main
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-2>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-3>)import (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-4>)    "context"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-5>)    "fmt"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-6>)    "log"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-7>)    "regexp"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-8>)    "strings"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-9>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-10>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-11>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-12>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-13>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-14>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-15>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-16>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-17>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-18>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-19>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-20>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-21>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-22>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-23>)// 1. Define the Callback Function
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-24>)func onBeforeAgent(ctx agent.Context) (*genai.Content, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-25>)    agentName := ctx.AgentName()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-26>)    log.Printf("[Callback] Entering agent: %s", agentName)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-27>)    if skip, _ := ctx.State().Get("skip_llm_agent"); skip == true {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-28>)        log.Printf("[Callback] State condition met: Skipping agent %s", agentName)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-29>)        return genai.NewContentFromText(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-30>)                fmt.Sprintf("Agent %s skipped by before_agent_callback.", agentName),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-31>)                genai.RoleModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-32>)            ),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-33>)            nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-34>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-35>)    log.Printf("[Callback] State condition not met: Running agent %s", agentName)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-36>)    return nil, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-37>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-38>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-39>)// 2. Define a function to set up and run the agent with the callback.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-40>)func runBeforeAgentExample() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-41>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-42>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-43>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-44>)        log.Fatalf("FATAL: Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-45>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-46>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-47>)    // 3. Register the callback in the agent configuration.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-48>)    llmCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-49>)        Name:                 "AgentWithBeforeAgentCallback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-50>)        BeforeAgentCallbacks: []agent.BeforeAgentCallback{onBeforeAgent},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-51>)        Model:                geminiModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-52>)        Instruction:          "You are a concise assistant.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-53>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-54>)    testAgent, err := llmagent.New(llmCfg)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-55>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-56>)        log.Fatalf("FATAL: Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-57>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-58>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-59>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-60>)    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-61>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-62>)        log.Fatalf("FATAL: Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-63>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-64>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-65>)    // 4. Run scenarios to demonstrate the callback's behavior.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-66>)    log.Println("--- SCENARIO 1: Agent should run normally ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-67>)    runScenario(ctx, r, sessionService, appName, "session_normal", nil, "Hello, world!")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-68>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-69>)    log.Println("\n--- SCENARIO 2: Agent should be skipped ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-70>)    runScenario(ctx, r, sessionService, appName, "session_skip", map[string]any{"skip_llm_agent": true}, "This should be skipped.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-3-71>)}
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-2>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-3>)import com.google.adk.agents.CallbackContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-4>)import com.google.adk.events.Event;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-5>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-6>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-7>)import com.google.adk.sessions.State;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-8>)import com.google.genai.types.Content;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-9>)import com.google.genai.types.Part;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-10>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-11>)import io.reactivex.rxjava3.core.Maybe;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-12>)import java.util.Map;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-13>)import java.util.concurrent.ConcurrentHashMap;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-15>)public class BeforeAgentCallbackExample {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-16>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-17>)  private static final String APP_NAME = "AgentWithBeforeAgentCallback";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-18>)  private static final String USER_ID = "test_user_456";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-19>)  private static final String SESSION_ID = "session_id_123";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-20>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-21>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-22>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-23>)    BeforeAgentCallbackExample callbackAgent = new BeforeAgentCallbackExample();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-24>)    callbackAgent.defineAgent("Write a document about a cat");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-25>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-26>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-27>)  // --- 1. Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-28>)  /**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-29>)   * Logs entry and checks 'skip_llm_agent' in session state. If True, returns Content to skip the
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-30>)   * agent's execution. If False or not present, returns None to allow execution.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-31>)   */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-32>)  public Maybe<Content> checkIfAgentShouldRun(CallbackContext callbackContext) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-33>)    String agentName = callbackContext.agentName();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-34>)    String invocationId = callbackContext.invocationId();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-35>)    State currentState = callbackContext.state();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-36>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-37>)    System.out.printf("%n[Callback] Entering agent: %s (Inv: %s)%n", agentName, invocationId);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-38>)    System.out.printf("[Callback] Current State: %s%n", currentState.entrySet());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-39>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-40>)    // Check the condition in session state dictionary
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-41>)    if (Boolean.TRUE.equals(currentState.get("skip_llm_agent"))) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-42>)      System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-43>)          "[Callback] State condition 'skip_llm_agent=True' met: Skipping agent %s", agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-44>)      // Return Content to skip the agent's run
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-45>)      return Maybe.just(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-46>)          Content.fromParts(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-47>)              Part.fromText(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-48>)                  String.format(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-49>)                      "Agent %s skipped by before_agent_callback due to state.", agentName))));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-50>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-51>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-52>)    System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-53>)        "[Callback] State condition 'skip_llm_agent=True' NOT met: Running agent %s \n", agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-54>)    // Return empty response to allow the LlmAgent's normal execution
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-55>)    return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-56>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-57>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-58>)  public void defineAgent(String prompt) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-59>)    // --- 2. Setup Agent with Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-60>)    BaseAgent llmAgentWithBeforeCallback =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-61>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-62>)            .model(MODEL_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-63>)            .name(APP_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-64>)            .instruction("You are a concise assistant.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-65>)            .description("An LLM agent demonstrating stateful before_agent_callback")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-66>)            // You can also use a sync version of this callback "beforeAgentCallbackSync"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-67>)            .beforeAgentCallback(this::checkIfAgentShouldRun)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-68>)            .build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-69>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-70>)    // --- 3. Setup Runner and Sessions using InMemoryRunner ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-71>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-72>)    // Use InMemoryRunner - it includes InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-73>)    InMemoryRunner runner = new InMemoryRunner(llmAgentWithBeforeCallback, APP_NAME);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-74>)    // Scenario 1: Initial state is null, which means 'skip_llm_agent' will be false in the callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-75>)    // check
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-76>)    runAgent(runner, null, prompt);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-77>)    // Scenario 2: Agent will be skipped (state has skip_llm_agent=true)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-78>)    runAgent(runner, new ConcurrentHashMap<>(Map.of("skip_llm_agent", true)), prompt);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-79>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-80>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-81>)  public void runAgent(InMemoryRunner runner, ConcurrentHashMap<String, Object> initialState, String prompt) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-82>)    // InMemoryRunner automatically creates a session service. Create a session using the service.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-83>)    Session session =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-84>)        runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-85>)            .sessionService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-86>)            .createSession(APP_NAME, USER_ID, initialState, SESSION_ID)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-87>)            .blockingGet();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-88>)    Content userMessage = Content.fromParts(Part.fromText(prompt));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-89>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-90>)    // Run the agent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-91>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-92>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-93>)    // Print final output (either from LLM or callback override)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-94>)    eventStream.blockingForEach(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-95>)        event -> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-96>)          if (event.finalResponse()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-97>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-98>)          }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-99>)        });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-100>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-4-101>)}
    
**Note on the`before_agent_callback` Example:**

  * **What it Shows:** This example demonstrates the `before_agent_callback`. This callback runs _right before_ the agent's main processing logic starts for a given request.
  * **How it Works:** The callback function (`check_if_agent_should_run`) looks at a flag (`skip_llm_agent`) in the session's state.
    * If the flag is `True`, the callback returns a `types.Content` object. This tells the ADK framework to **skip** the agent's main execution entirely and use the callback's returned content as the final response.
    * If the flag is `False` (or not set), the callback returns `None` or an empty object. This tells the ADK framework to **proceed** with the agent's normal execution (calling the LLM in this case).
  * **Expected Outcome:** You'll see two scenarios:
    1. In the session _with_ the `skip_llm_agent: True` state, the agent's LLM call is bypassed, and the output comes directly from the callback ("Agent... skipped...").
    2. In the session _without_ that state flag, the callback allows the agent to run, and you see the actual response from the LLM (e.g., "Hello!").
  * **Understanding Callbacks:** This highlights how `before_` callbacks act as **gatekeepers** , allowing you to intercept execution _before_ a major step and potentially prevent it based on checks (like state, input validation, permissions).

### After Agent Callback[¶](<https://adk.dev/callbacks/types-of-callbacks/#after-agent-callback> "Permanent link")

**When:** Called _immediately after_ the agent's `_run_async_impl` (or `_run_live_impl`) method successfully completes. It does _not_ run if the agent was skipped due to `before_agent_callback` returning content or if `end_invocation` was set during the agent's run.

**Purpose:** Useful for cleanup tasks, post-execution validation, logging the completion of an agent's activity, or modifying final state.

After Agent Callback output modification limitations

The `after_agent_callback` can not fully alter the response output because the agent may have called AI models multiple times and omitted multiple events. So modifying the output is not allowed, although you can _append_ additional content. If you want to change an AI model response, consider `after_model_callback`.

Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-2>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-6>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-8>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-13>)# limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-15>)# # --- Setup Instructions ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-16>)# # 1. Install the ADK package:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-17>)# !pip install google-adk
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-18>)# # Make sure to restart kernel if using colab/jupyter notebooks
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-20>)# # 2. Set up your Gemini API Key:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-21>)# #    - Get a key from Google AI Studio: https://aistudio.google.com/app/apikey
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-22>)# #    - Set it as an environment variable:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-23>)# import os
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-24>)# os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY_HERE" # <--- REPLACE with your actual key
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-25>)# # Or learn about other authentication methods (like Agent Platform):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-26>)# # https://adk.dev/agents/models/
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-27>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-28>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-29>)# ADK Imports
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-30>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-31>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-32>)from google.adk.runners import InMemoryRunner  # Use InMemoryRunner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-33>)from google.genai import types  # For types.Content
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-34>)from typing import Optional
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-35>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-36>)# Define the model - Use the specific model name requested
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-37>)GEMINI_2_FLASH = "gemini-2.0-flash"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-38>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-39>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-40>)# --- 1. Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-41>)def modify_output_after_agent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-42>)    callback_context: CallbackContext,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-43>)) -> Optional[types.Content]:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-44>)    """
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-45>)    Logs exit from an agent and checks 'add_concluding_note' in session state.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-46>)    If True, returns new Content to *replace* the agent's original output.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-47>)    If False or not present, returns None, allowing the agent's original output to be used.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-48>)    """
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-49>)    agent_name = callback_context.agent_name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-50>)    invocation_id = callback_context.invocation_id
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-51>)    current_state = callback_context.state.to_dict()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-52>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-53>)    print(f"\n[Callback] Exiting agent: {agent_name} (Inv: {invocation_id})")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-54>)    print(f"[Callback] Current State: {current_state}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-55>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-56>)    # Example: Check state to decide whether to modify the final output
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-57>)    if current_state.get("add_concluding_note", False):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-58>)        print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-59>)            f"[Callback] State condition 'add_concluding_note=True' met: Replacing agent {agent_name}'s output."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-60>)        )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-61>)        # Return Content to *replace* the agent's own output
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-62>)        return types.Content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-63>)            parts=[
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-64>)                types.Part(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-65>)                    text=f"Concluding note added by after_agent_callback, replacing original output."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-66>)                )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-67>)            ],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-68>)            role="model",  # Assign model role to the overriding response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-69>)        )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-70>)    else:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-71>)        print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-72>)            f"[Callback] State condition not met: Using agent {agent_name}'s original output."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-73>)        )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-74>)        # Return None - the agent's output produced just before this callback will be used.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-75>)        return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-76>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-77>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-78>)# --- 2. Setup Agent with Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-79>)llm_agent_with_after_cb = LlmAgent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-80>)    name="MySimpleAgentWithAfter",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-81>)    model=GEMINI_2_FLASH,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-82>)    instruction="You are a simple agent. Just say 'Processing complete!'",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-83>)    description="An LLM agent demonstrating after_agent_callback for output modification",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-84>)    after_agent_callback=modify_output_after_agent,  # Assign the callback here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-85>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-86>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-87>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-88>)# --- 3. Setup Runner and Sessions using InMemoryRunner ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-89>)async def main():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-90>)    app_name = "after_agent_demo"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-91>)    user_id = "test_user_after"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-92>)    session_id_normal = "session_run_normally"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-93>)    session_id_modify = "session_modify_output"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-94>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-95>)    # Use InMemoryRunner - it includes InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-96>)    runner = InMemoryRunner(agent=llm_agent_with_after_cb, app_name=app_name)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-97>)    # Get the bundled session service to create sessions
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-98>)    session_service = runner.session_service
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-99>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-100>)    # Create session 1: Agent output will be used as is (default empty state)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-101>)    await session_service.create_session(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-102>)        app_name=app_name,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-103>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-104>)        session_id=session_id_normal,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-105>)        # No initial state means 'add_concluding_note' will be False in the callback check
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-106>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-107>)    # print(f"Session '{session_id_normal}' created with default state.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-108>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-109>)    # Create session 2: Agent output will be replaced by the callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-110>)    await session_service.create_session(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-111>)        app_name=app_name,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-112>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-113>)        session_id=session_id_modify,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-114>)        state={"add_concluding_note": True},  # Set the state flag here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-115>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-116>)    # print(f"Session '{session_id_modify}' created with state={{'add_concluding_note': True}}.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-117>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-118>)    # --- Scenario 1: Run where callback allows agent's original output ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-119>)    print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-120>)        "\n"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-121>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-122>)        + f" SCENARIO 1: Running Agent on Session '{session_id_normal}' (Should Use Original Output) "
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-123>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-124>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-125>)    async for event in runner.run_async(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-126>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-127>)        session_id=session_id_normal,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-128>)        new_message=types.Content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-129>)            role="user", parts=[types.Part(text="Process this please.")]
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-130>)        ),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-131>)    ):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-132>)        # Print final output (either from LLM or callback override)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-133>)        if event.is_final_response() and event.content:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-134>)            print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-135>)                f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-136>)            )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-137>)        elif event.is_error():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-138>)            print(f"Error Event: {event.error_details}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-139>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-140>)    # --- Scenario 2: Run where callback replaces the agent's output ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-141>)    print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-142>)        "\n"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-143>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-144>)        + f" SCENARIO 2: Running Agent on Session '{session_id_modify}' (Should Replace Output) "
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-145>)        + "=" * 20
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-146>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-147>)    async for event in runner.run_async(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-148>)        user_id=user_id,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-149>)        session_id=session_id_modify,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-150>)        new_message=types.Content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-151>)            role="user", parts=[types.Part(text="Process this and add note.")]
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-152>)        ),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-153>)    ):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-154>)        # Print final output (either from LLM or callback override)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-155>)        if event.is_final_response() and event.content:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-156>)            print(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-157>)                f"Final Output: [{event.author}] {event.content.parts[0].text.strip()}"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-158>)            )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-159>)        elif event.is_error():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-160>)            print(f"Error Event: {event.error_details}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-161>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-162>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-163>)# --- 4. Execute ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-164>)# In a Python script:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-165>)# import asyncio
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-166>)# if __name__ == "__main__":
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-167>)#     # Make sure GOOGLE_API_KEY environment variable is set if not using Agent Platform auth
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-168>)#     # Or ensure Application Default Credentials (ADC) are configured for Agent Platform
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-169>)#     asyncio.run(main())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-170>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-171>)# In a Jupyter Notebook or similar environment:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-5-172>)await main()
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-1>)/**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-3>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-7>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-9>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-14>) * limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-15>) */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-16>)import { LlmAgent, Context, isFinalResponse, InMemoryRunner } from '@google/adk';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-17>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-18>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-19>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-20>)const APP_NAME = "after_agent_callback_app";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-21>)const USER_ID = "test_user_after_agent";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-22>)const SESSION_NORMAL_ID = "session_run_normally_ts";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-23>)const SESSION_MODIFY_ID = "session_modify_output_ts";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-24>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-25>)// --- 1. Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-26>)/**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-27>) * Logs exit from an agent and checks "add_concluding_note" in session state.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-28>) * If True, returns new Content to *replace* the agent's original output.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-29>) * If False or not present, returns void, allowing the agent's original output to be used.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-30>) */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-31>)function modifyOutputAfterAgent(context: Context): any {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-32>)  const agentName = context.agentName;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-33>)  const invocationId = context.invocationId;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-34>)  const currentState = context.state;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-35>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-36>)  console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-37>)    `
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-38>)[Callback] Exiting agent: ${agentName} (Inv: ${invocationId})`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-39>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-40>)  console.log(`[Callback] Current State:`, currentState);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-41>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-42>)  // Example: Check state to decide whether to modify the final output
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-43>)  if (currentState.get("add_concluding_note") === true) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-44>)    console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-45>)      `[Callback] State condition "add_concluding_note=true" met: Replacing agent ${agentName}'s output.`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-46>)    );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-47>)    // Return Content to *replace* the agent's own output
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-48>)    return createUserContent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-49>)      "Concluding note added by after_agent_callback, replacing original output."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-50>)    );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-51>)  } else {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-52>)    console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-53>)      `[Callback] State condition not met: Using agent ${agentName}'s original output.`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-54>)    );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-55>)    // Return void/undefined - the agent's output will be used.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-56>)    return;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-57>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-58>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-59>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-60>)// --- 2. Setup Agent with Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-61>)const llmAgentWithAfterCb = new LlmAgent({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-62>)  name: "MySimpleAgentWithAfter",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-63>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-64>)  instruction: "You are a simple agent. Just say \"Processing complete!\"",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-65>)  description:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-66>)    "An LLM agent demonstrating after_agent_callback for output modification",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-67>)  afterAgentCallback: modifyOutputAfterAgent, // Assign the callback here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-68>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-69>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-70>)// --- 3. Run the Agent ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-71>)async function main() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-72>)  const runner = new InMemoryRunner({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-73>)    agent: llmAgentWithAfterCb,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-74>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-75>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-76>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-77>)  // Create session 1: Agent output will be used as is (default empty state)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-78>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-79>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-80>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-81>)    sessionId: SESSION_NORMAL_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-82>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-83>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-84>)  // Create session 2: Agent output will be replaced by the callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-85>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-86>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-87>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-88>)    sessionId: SESSION_MODIFY_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-89>)    state: { add_concluding_note: true }, // Set the state flag here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-90>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-91>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-92>)  // --- Scenario 1: Run where callback allows agent's original output ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-93>)  console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-94>)    `
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-95>)==================== SCENARIO 1: Running Agent on Session "${SESSION_NORMAL_ID}" (Should Use Original Output) ====================
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-96>)`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-97>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-98>)  const eventsNormal = runner.runAsync({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-99>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-100>)    sessionId: SESSION_NORMAL_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-101>)    newMessage: createUserContent("Process this please."),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-102>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-103>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-104>)  for await (const event of eventsNormal) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-105>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-106>)      const finalResponse = event.content.parts
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-107>)        .map((part: any) => part.text ?? "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-108>)        .join("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-109>)      console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-110>)        `Final Output: [${event.author}] ${finalResponse.trim()}`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-111>)      );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-112>)    } else if (event.errorMessage) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-113>)      console.log(`Error Event: ${event.errorMessage}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-114>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-115>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-116>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-117>)  // --- Scenario 2: Run where callback replaces the agent's output ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-118>)  console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-119>)    `
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-120>)==================== SCENARIO 2: Running Agent on Session "${SESSION_MODIFY_ID}" (Should Replace Output) ====================
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-121>)`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-122>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-123>)  const eventsModify = runner.runAsync({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-124>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-125>)    sessionId: SESSION_MODIFY_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-126>)    newMessage: createUserContent("Process this and add note."),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-127>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-128>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-129>)  for await (const event of eventsModify) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-130>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-131>)      const finalResponse = event.content.parts
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-132>)        .map((part: any) => part.text ?? "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-133>)        .join("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-134>)      console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-135>)        `Final Output: [${event.author}] ${finalResponse.trim()}`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-136>)      );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-137>)    } else if (event.errorMessage) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-138>)      console.log(`Error Event: ${event.errorMessage}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-139>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-140>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-141>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-142>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-6-143>)main();
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-1>)package main
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-2>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-3>)import (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-4>)    "context"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-5>)    "fmt"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-6>)    "log"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-7>)    "regexp"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-8>)    "strings"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-9>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-10>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-11>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-12>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-13>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-14>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-15>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-16>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-17>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-18>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-19>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-20>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-21>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-22>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-23>)func onAfterAgent(ctx agent.Context) (*genai.Content, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-24>)    agentName := ctx.AgentName()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-25>)    invocationID := ctx.InvocationID()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-26>)    state := ctx.State()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-27>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-28>)    log.Printf("\n[Callback] Exiting agent: %s (Inv: %s)", agentName, invocationID)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-29>)    log.Printf("[Callback] Current State: %v", state)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-30>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-31>)    if addNote, _ := state.Get("add_concluding_note"); addNote == true {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-32>)        log.Printf("[Callback] State condition 'add_concluding_note=True' met: Replacing agent %s's output.", agentName)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-33>)        return genai.NewContentFromText(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-34>)            "Concluding note added by after_agent_callback, replacing original output.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-35>)            genai.RoleModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-36>)        ), nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-37>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-38>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-39>)    log.Printf("[Callback] State condition not met: Using agent %s's original output.", agentName)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-40>)    return nil, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-41>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-42>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-43>)func runAfterAgentExample() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-44>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-45>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-46>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-47>)        log.Fatalf("FATAL: Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-48>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-49>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-50>)    llmCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-51>)        Name:                "AgentWithAfterAgentCallback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-52>)        AfterAgentCallbacks: []agent.AfterAgentCallback{onAfterAgent},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-53>)        Model:               geminiModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-54>)        Instruction:         "You are a simple agent. Just say 'Processing complete!'",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-55>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-56>)    testAgent, err := llmagent.New(llmCfg)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-57>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-58>)        log.Fatalf("FATAL: Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-59>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-60>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-61>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-62>)    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-63>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-64>)        log.Fatalf("FATAL: Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-65>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-66>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-67>)    log.Println("--- SCENARIO 1: Should use original output ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-68>)    runScenario(ctx, r, sessionService, appName, "session_normal", nil, "Process this.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-69>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-70>)    log.Println("\n--- SCENARIO 2: Should replace output ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-71>)    runScenario(ctx, r, sessionService, appName, "session_modify", map[string]any{"add_concluding_note": true}, "Process and add note.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-7-72>)}
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-2>)import com.google.adk.agents.CallbackContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-4>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-5>)import com.google.adk.sessions.State;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-6>)import com.google.genai.types.Content;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-7>)import com.google.genai.types.Part;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-8>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-9>)import io.reactivex.rxjava3.core.Maybe;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-10>)import java.util.HashMap;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-11>)import java.util.List;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-12>)import java.util.Map;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-13>)import java.util.concurrent.ConcurrentHashMap;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-15>)public class AfterAgentCallbackExample {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-16>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-17>)  // --- Constants ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-18>)  private static final String APP_NAME = "after_agent_demo";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-19>)  private static final String USER_ID = "test_user_after";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-20>)  private static final String SESSION_ID_NORMAL = "session_run_normally";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-21>)  private static final String SESSION_ID_MODIFY = "session_modify_output";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-22>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-23>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-24>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-25>)    AfterAgentCallbackExample demo = new AfterAgentCallbackExample();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-26>)    demo.defineAgentAndRunScenarios();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-27>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-28>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-29>)  // --- 1. Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-30>)  /**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-31>)   * Log exit from an agent and checks 'add_concluding_note' in session state. If True, returns new
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-32>)   * Content to *replace* the agent's original output. If False or not present, returns
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-33>)   * Maybe.empty(), allowing the agent's original output to be used.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-34>)   */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-35>)  public Maybe<Content> modifyOutputAfterAgent(CallbackContext callbackContext) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-36>)    String agentName = callbackContext.agentName();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-37>)    String invocationId = callbackContext.invocationId();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-38>)    State currentState = callbackContext.state();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-39>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-40>)    System.out.printf("%n[Callback] Exiting agent: %s (Inv: %s)%n", agentName, invocationId);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-41>)    System.out.printf("[Callback] Current State: %s%n", currentState.entrySet());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-42>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-43>)    Object addNoteFlag = currentState.get("add_concluding_note");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-44>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-45>)    // Example: Check state to decide whether to modify the final output
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-46>)    if (Boolean.TRUE.equals(addNoteFlag)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-47>)      System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-48>)          "[Callback] State condition 'add_concluding_note=True' met: Replacing agent %s's"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-49>)              + " output.%n",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-50>)          agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-51>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-52>)      // Return Content to *replace* the agent's own output
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-53>)      return Maybe.just(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-54>)          Content.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-55>)              .parts(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-56>)                  List.of(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-57>)                      Part.fromText(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-58>)                          "Concluding note added by after_agent_callback, replacing original output.")))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-59>)              .role("model") // Assign model role to the overriding response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-60>)              .build());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-61>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-62>)    } else {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-63>)      System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-64>)          "[Callback] State condition not met: Using agent %s's original output.%n", agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-65>)      // Return None - the agent's output produced just before this callback will be used.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-66>)      return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-67>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-68>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-69>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-70>)  // --- 2. Setup Agent with Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-71>)  public void defineAgentAndRunScenarios() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-72>)    LlmAgent llmAgentWithAfterCb =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-73>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-74>)            .name(APP_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-75>)            .model(MODEL_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-76>)            .description("An LLM agent demonstrating after_agent_callback for output modification")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-77>)            .instruction("You are a simple agent. Just say 'Processing complete!'")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-78>)            .afterAgentCallback(this::modifyOutputAfterAgent) // Assign the callback here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-79>)            .build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-80>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-81>)    // --- 3. Setup Runner and Sessions using InMemoryRunner ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-82>)    // Use InMemoryRunner - it includes InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-83>)    InMemoryRunner runner = new InMemoryRunner(llmAgentWithAfterCb, APP_NAME);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-84>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-85>)    // --- Scenario 1: Run where callback allows agent's original output ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-86>)    System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-87>)        "%n%s SCENARIO 1: Running Agent (Should Use Original Output) %s%n",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-88>)        "=".repeat(20), "=".repeat(20));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-89>)    // No initial state means 'add_concluding_note' will be false in the callback check
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-90>)    runScenario(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-91>)        runner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-92>)        llmAgentWithAfterCb.name(), // Use agent name for runner's appName consistency
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-93>)        SESSION_ID_NORMAL,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-94>)        null,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-95>)        "Process this please.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-96>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-97>)    // --- Scenario 2: Run where callback replaces the agent's output ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-98>)    System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-99>)        "%n%s SCENARIO 2: Running Agent (Should Replace Output) %s%n",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-100>)        "=".repeat(20), "=".repeat(20));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-101>)    Map<String, Object> modifyState = new HashMap<>();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-102>)    modifyState.put("add_concluding_note", true); // Set the state flag here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-103>)    runScenario(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-104>)        runner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-105>)        llmAgentWithAfterCb.name(), // Use agent name for runner's appName consistency
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-106>)        SESSION_ID_MODIFY,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-107>)        new ConcurrentHashMap<>(modifyState),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-108>)        "Process this and add note.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-109>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-110>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-111>)  // --- 3. Method to Run a Single Scenario ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-112>)  public void runScenario(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-113>)      InMemoryRunner runner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-114>)      String appName,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-115>)      String sessionId,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-116>)      ConcurrentHashMap<String, Object> initialState,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-117>)      String userQuery) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-118>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-119>)    // Create session using the runner's bundled session service
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-120>)    runner.sessionService().createSession(appName, USER_ID, initialState, sessionId).blockingGet();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-121>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-122>)    System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-123>)        "Running scenario for session: %s, initial state: %s%n", sessionId, initialState);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-124>)    Content userMessage =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-125>)        Content.builder().role("user").parts(List.of(Part.fromText(userQuery))).build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-126>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-127>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, sessionId, userMessage);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-128>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-129>)    // Print final output
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-130>)    eventStream.blockingForEach(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-131>)        event -> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-132>)          if (event.finalResponse() && event.content().isPresent()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-133>)            String author = event.author() != null ? event.author() : "UNKNOWN";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-134>)            String text =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-135>)                event
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-136>)                    .content()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-137>)                    .flatMap(Content::parts)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-138>)                    .filter(parts -> !parts.isEmpty())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-139>)                    .map(parts -> parts.get(0).text().orElse("").trim())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-140>)                    .orElse("[No text in final response]");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-141>)            System.out.printf("Final Output for %s: [%s] %s%n", sessionId, author, text);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-142>)          } else if (event.errorCode().isPresent()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-143>)            System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-144>)                "Error Event for %s: %s%n",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-145>)                sessionId, event.errorMessage().orElse("Unknown error"));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-146>)          }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-147>)        });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-148>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-8-149>)}
    
**Note on the`after_agent_callback` Example:**

  * **What it Shows:** This example demonstrates the `after_agent_callback`. This callback runs _right after_ the agent's main processing logic has finished and produced its result, but _before_ that result is finalized and returned.
  * **How it Works:** The callback function (`modify_output_after_agent`) checks a flag (`add_concluding_note`) in the session's state.
    * If the flag is `True`, the callback returns a _new_ `types.Content` object. This tells the ADK framework to **append** the agent's original output with the content returned by the callback.
    * If the flag is `False` (or not set), the callback returns `None` or an empty object. This tells the ADK framework to **use** the original output generated by the agent.
  * **Expected Outcome:** You'll see two scenarios:
    1. In the session _without_ the `add_concluding_note: True` state, the callback allows the agent's original output ("Processing complete!") to be used.
    2. In the session _with_ that state flag, the callback intercepts the agent's original output and appends it with its own message ("Concluding note added...").
  * **Understanding Callbacks:** This highlights how `after_` callbacks allow **post-processing** or **modification**. You can inspect the result of a step (the agent's run) and decide whether to let it pass through, change it, or completely replace it based on your logic.

## LLM Interaction Callbacks[¶](<https://adk.dev/callbacks/types-of-callbacks/#llm-interaction-callbacks> "Permanent link")

These callbacks are specific to `LlmAgent` and provide hooks around the interaction with the Large Language Model.

### Before Model Callback[¶](<https://adk.dev/callbacks/types-of-callbacks/#before-model-callback> "Permanent link")

**When:** Called just before the `generate_content_async` (or equivalent) request is sent to the LLM within an `LlmAgent`'s flow.

**Purpose:** Allows inspection and modification of the request going to the LLM. Use cases include adding dynamic instructions, injecting few-shot examples based on state, modifying model config, implementing guardrails (like profanity filters), or implementing request-level caching.

**Return Value Effect:** If the callback returns `None` (or a `Maybe.empty()` object in Java), the LLM continues its normal workflow. If the callback returns an `LlmResponse` object, then the call to the LLM is **skipped**. The returned `LlmResponse` is used directly as if it came from the model. This is powerful for implementing guardrails or caching.

Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-2>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-6>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-8>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-13>)# limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-15>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-16>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-17>)from google.adk.models import LlmResponse, LlmRequest
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-18>)from google.adk.runners import Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-19>)from typing import Optional
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-20>)from google.genai import types 
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-21>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-22>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-23>)GEMINI_2_FLASH="gemini-2.0-flash"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-24>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-25>)# --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-26>)def simple_before_model_modifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-27>)    callback_context: CallbackContext, llm_request: LlmRequest
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-28>)) -> Optional[LlmResponse]:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-29>)    """Inspects/modifies the LLM request or skips the call."""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-30>)    agent_name = callback_context.agent_name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-31>)    print(f"[Callback] Before model call for agent: {agent_name}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-32>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-33>)    # Inspect the last user message in the request contents
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-34>)    last_user_message = ""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-35>)    if llm_request.contents and llm_request.contents[-1].role == 'user':
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-36>)         if llm_request.contents[-1].parts:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-37>)            last_user_message = llm_request.contents[-1].parts[0].text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-38>)    print(f"[Callback] Inspecting last user message: '{last_user_message}'")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-39>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-40>)    # --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-41>)    # Add a prefix to the system instruction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-42>)    original_instruction = llm_request.config.system_instruction or types.Content(role="system", parts=[])
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-43>)    prefix = "[Modified by Callback] "
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-44>)    # Ensure system_instruction is Content and parts list exists
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-45>)    if not isinstance(original_instruction, types.Content):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-46>)         # Handle case where it might be a string (though config expects Content)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-47>)         original_instruction = types.Content(role="system", parts=[types.Part(text=str(original_instruction))])
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-48>)    if not original_instruction.parts:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-49>)        original_instruction.parts.append(types.Part(text="")) # Add an empty part if none exist
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-50>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-51>)    # Modify the text of the first part
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-52>)    modified_text = prefix + (original_instruction.parts[0].text or "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-53>)    original_instruction.parts[0].text = modified_text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-54>)    llm_request.config.system_instruction = original_instruction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-55>)    print(f"[Callback] Modified system instruction to: '{modified_text}'")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-56>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-57>)    # --- Skip Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-58>)    # Check if the last user message contains "BLOCK"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-59>)    if "BLOCK" in last_user_message.upper():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-60>)        print("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-61>)        # Return an LlmResponse to skip the actual LLM call
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-62>)        return LlmResponse(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-63>)            content=types.Content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-64>)                role="model",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-65>)                parts=[types.Part(text="LLM call was blocked by before_model_callback.")],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-66>)            )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-67>)        )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-68>)    else:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-69>)        print("[Callback] Proceeding with LLM call.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-70>)        # Return None to allow the (modified) request to go to the LLM
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-71>)        return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-72>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-73>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-74>)# Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-75>)my_llm_agent = LlmAgent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-76>)        name="ModelCallbackAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-77>)        model=GEMINI_2_FLASH,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-78>)        instruction="You are a helpful assistant.", # Base instruction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-79>)        description="An LLM agent demonstrating before_model_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-80>)        before_model_callback=simple_before_model_modifier # Assign the function here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-81>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-82>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-83>)APP_NAME = "guardrail_app"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-84>)USER_ID = "user_1"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-85>)SESSION_ID = "session_001"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-86>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-87>)# Session and Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-88>)async def setup_session_and_runner():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-89>)    session_service = InMemorySessionService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-90>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-91>)    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-92>)    return session, runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-93>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-94>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-95>)# Agent Interaction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-96>)async def call_agent_async(query):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-97>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-98>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-99>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-100>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-101>)    async for event in events:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-102>)        if event.is_final_response():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-103>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-104>)            print("Agent Response: ", final_response)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-105>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-106>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-107>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-9-108>)await call_agent_async("write a joke on BLOCK")
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-1>)/**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-3>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-7>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-9>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-14>) * limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-15>) */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-16>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-17>)import { LlmAgent, InMemoryRunner, Context, isFinalResponse } from '@google/adk';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-18>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-20>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-21>)const APP_NAME = "before_model_callback_app";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-22>)const USER_ID = "test_user_before_model";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-23>)const SESSION_ID_BLOCK = "session_block_model_call";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-24>)const SESSION_ID_NORMAL = "session_normal_model_call";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-26>)// --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-27>)function simpleBeforeModelModifier({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-28>)  context,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-29>)  request,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-30>)}: {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-31>)  context: Context;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-32>)  request: any;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-33>)}): any | undefined {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-34>)  console.log(`[Callback] Before model call for agent: ${context.agentName}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-35>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-36>)  // Inspect the last user message in the request contents
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-37>)  const lastUserMessage = request.contents?.at(-1)?.parts?.[0]?.text ?? "";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-38>)  console.log(`[Callback] Inspecting last user message: '${lastUserMessage}'`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-39>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-40>)  // --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-41>)  // Add a prefix to the system instruction.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-42>)  // We create a deep copy to avoid modifying the original agent's config object.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-43>)  const modifiedConfig = JSON.parse(JSON.stringify(request.config));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-44>)  const originalInstructionText =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-45>)    modifiedConfig.systemInstruction?.parts?.[0]?.text ?? "";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-46>)  const prefix = "[Modified by Callback] ";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-47>)  modifiedConfig.systemInstruction = {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-48>)    role: "system",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-49>)    parts: [{ text: prefix + originalInstructionText }],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-50>)  };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-51>)  request.config = modifiedConfig; // Assign the modified config back to the request
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-52>)  console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-53>)    `[Callback] Modified system instruction to: '${modifiedConfig.systemInstruction.parts[0].text}'`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-54>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-55>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-56>)  // --- Skip Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-57>)  // Check if the last user message contains "BLOCK"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-58>)  if (lastUserMessage.toUpperCase().includes("BLOCK")) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-59>)    console.log("[Callback] 'BLOCK' keyword found. Skipping LLM call.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-60>)    // Return an LlmResponse to skip the actual LLM call
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-61>)    return {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-62>)      content: {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-63>)        role: "model",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-64>)        parts: [
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-65>)          { text: "LLM call was blocked by the before_model_callback." },
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-66>)        ],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-67>)      },
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-68>)    };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-69>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-70>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-71>)  console.log("[Callback] Proceeding with LLM call.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-72>)  // Return undefined to allow the (modified) request to go to the LLM
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-73>)  return undefined;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-74>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-75>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-76>)// --- Create LlmAgent and Assign Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-77>)const myLlmAgent = new LlmAgent({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-78>)  name: "ModelCallbackAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-79>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-80>)  instruction: "You are a helpful assistant.", // Base instruction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-81>)  description: "An LLM agent demonstrating before_model_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-82>)  beforeModelCallback: simpleBeforeModelModifier, // Assign the function here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-83>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-84>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-85>)// --- Agent Interaction Logic ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-86>)async function callAgentAndPrint(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-87>)  runner: InMemoryRunner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-88>)  query: string,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-89>)  sessionId: string
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-90>)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-91>)  console.log(`\n>>> Calling Agent with query: "${query}"`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-92>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-93>)  let finalResponseContent = "No final response received.";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-94>)  const events = runner.runAsync({ userId: USER_ID, sessionId, newMessage: createUserContent(query) });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-95>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-96>)  for await (const event of events) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-97>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-98>)      finalResponseContent = event.content.parts
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-99>)        .map((part: { text?: string }) => part.text ?? "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-100>)        .join("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-101>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-102>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-103>)  console.log("<<< Agent Response: ", finalResponseContent);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-104>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-105>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-106>)// --- Run Interactions ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-107>)async function main() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-108>)  const runner = new InMemoryRunner({ agent: myLlmAgent, appName: APP_NAME });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-109>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-110>)  // Scenario 1: The callback will find "BLOCK" and skip the model call
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-111>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-112>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-113>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-114>)    sessionId: SESSION_ID_BLOCK,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-115>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-116>)  await callAgentAndPrint(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-117>)    runner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-118>)    "write a joke about BLOCK",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-119>)    SESSION_ID_BLOCK
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-120>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-121>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-122>)  // Scenario 2: The callback will modify the instruction and proceed
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-123>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-124>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-125>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-126>)    sessionId: SESSION_ID_NORMAL,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-127>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-128>)  await callAgentAndPrint(runner, "write a short poem", SESSION_ID_NORMAL);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-129>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-130>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-10-131>)main();
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-1>)package main
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-2>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-3>)import (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-4>)    "context"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-5>)    "fmt"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-6>)    "log"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-7>)    "regexp"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-8>)    "strings"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-9>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-10>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-11>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-12>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-13>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-14>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-15>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-16>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-17>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-18>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-19>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-20>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-21>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-22>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-23>)func onBeforeModel(ctx agent.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-24>)    log.Printf("[Callback] BeforeModel triggered for agent %q.", ctx.AgentName())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-26>)    // Modification Example: Add a prefix to the system instruction.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-27>)    if req.Config.SystemInstruction != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-28>)        prefix := "[Modified by Callback] "
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-29>)        // This is a simplified example; production code might need deeper checks.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-30>)        if len(req.Config.SystemInstruction.Parts) > 0 {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-31>)            req.Config.SystemInstruction.Parts[0].Text = prefix + req.Config.SystemInstruction.Parts[0].Text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-32>)        } else {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-33>)            req.Config.SystemInstruction.Parts = append(req.Config.SystemInstruction.Parts, &genai.Part{Text: prefix})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-34>)        }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-35>)        log.Printf("[Callback] Modified system instruction.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-36>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-37>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-38>)    // Skip Example: Check for "BLOCK" in the user's prompt.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-39>)    for _, content := range req.Contents {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-40>)        for _, part := range content.Parts {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-41>)            if strings.Contains(strings.ToUpper(part.Text), "BLOCK") {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-42>)                log.Println("[Callback] 'BLOCK' keyword found. Skipping LLM call.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-43>)                return &model.LLMResponse{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-44>)                    Content: &genai.Content{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-45>)                        Parts: []*genai.Part{{Text: "LLM call was blocked by before_model_callback."}},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-46>)                        Role:  "model",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-47>)                    },
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-48>)                }, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-49>)            }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-50>)        }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-51>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-52>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-53>)    log.Println("[Callback] Proceeding with LLM call.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-54>)    return nil, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-55>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-56>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-57>)func runBeforeModelExample() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-58>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-59>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-60>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-61>)        log.Fatalf("FATAL: Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-62>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-63>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-64>)    llmCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-65>)        Name:                 "AgentWithBeforeModelCallback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-66>)        Model:                geminiModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-67>)        BeforeModelCallbacks: []llmagent.BeforeModelCallback{onBeforeModel},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-68>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-69>)    testAgent, err := llmagent.New(llmCfg)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-70>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-71>)        log.Fatalf("FATAL: Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-72>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-73>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-74>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-75>)    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-76>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-77>)        log.Fatalf("FATAL: Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-78>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-79>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-80>)    log.Println("--- SCENARIO 1: Should proceed to LLM ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-81>)    runScenario(ctx, r, sessionService, appName, "session_normal", nil, "Tell me a fun fact.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-82>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-83>)    log.Println("\n--- SCENARIO 2: Should be blocked by callback ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-84>)    runScenario(ctx, r, sessionService, appName, "session_blocked", nil, "write a joke on BLOCK")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-11-85>)}
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-2>)import com.google.adk.agents.CallbackContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-4>)import com.google.adk.models.LlmRequest;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-5>)import com.google.adk.models.LlmResponse;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-6>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-7>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-8>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-9>)import com.google.common.collect.Iterables;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-10>)import com.google.genai.types.Content;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-11>)import com.google.genai.types.GenerateContentConfig;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-12>)import com.google.genai.types.Part;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-13>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-14>)import io.reactivex.rxjava3.core.Maybe;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-15>)import java.util.ArrayList;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-16>)import java.util.List;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-17>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-18>)public class BeforeModelCallbackExample {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-20>)  // --- Define Constants ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-21>)  private static final String AGENT_NAME = "ModelCallbackAgent";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-22>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-23>)  private static final String AGENT_INSTRUCTION = "You are a helpful assistant.";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-24>)  private static final String AGENT_DESCRIPTION =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-25>)      "An LLM agent demonstrating before_model_callback";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-26>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-27>)  // For session and runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-28>)  private static final String APP_NAME = "guardrail_app_java";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-29>)  private static final String USER_ID = "user_1_java";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-30>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-31>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-32>)    BeforeModelCallbackExample demo = new BeforeModelCallbackExample();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-33>)    demo.defineAgentAndRun();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-34>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-35>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-36>)  // --- 1. Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-37>)  // Inspects/modifies the LLM request or skips the actual LLM call.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-38>)  public Maybe<LlmResponse> simpleBeforeModelModifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-39>)      CallbackContext callbackContext, LlmRequest llmRequest) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-40>)    String agentName = callbackContext.agentName();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-41>)    System.out.printf("%n[Callback] Before model call for agent: %s%n", agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-42>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-43>)    String lastUserMessage = "";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-44>)    if (llmRequest.contents() != null && !llmRequest.contents().isEmpty()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-45>)      Content lastContentItem = Iterables.getLast(llmRequest.contents());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-46>)      if ("user".equals(lastContentItem.role().orElse(null))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-47>)          && lastContentItem.parts().isPresent()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-48>)          && !lastContentItem.parts().get().isEmpty()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-49>)        lastUserMessage = lastContentItem.parts().get().get(0).text().orElse("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-50>)      }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-51>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-52>)    System.out.printf("[Callback] Inspecting last user message: '%s'%n", lastUserMessage);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-53>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-54>)    // --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-55>)    // Add a prefix to the system instruction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-56>)    Content systemInstructionFromRequest = Content.builder().parts(ImmutableList.of()).build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-57>)    // Ensure system_instruction is Content and parts list exists
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-58>)    if (llmRequest.config().isPresent()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-59>)      systemInstructionFromRequest =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-60>)          llmRequest
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-61>)              .config()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-62>)              .get()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-63>)              .systemInstruction()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-64>)              .orElseGet(() -> Content.builder().role("system").parts(ImmutableList.of()).build());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-65>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-66>)    List<Part> currentSystemParts =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-67>)        new ArrayList<>(systemInstructionFromRequest.parts().orElse(ImmutableList.of()));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-68>)    // Ensure a part exists for modification
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-69>)    if (currentSystemParts.isEmpty()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-70>)      currentSystemParts.add(Part.fromText(""));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-71>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-72>)    // Modify the text of the first part
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-73>)    String prefix = "[Modified by Callback] ";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-74>)    String conceptuallyModifiedText = prefix + currentSystemParts.get(0).text().orElse("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-75>)    llmRequest =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-76>)        llmRequest.toBuilder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-77>)            .config(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-78>)                GenerateContentConfig.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-79>)                    .systemInstruction(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-80>)                        Content.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-81>)                            .parts(List.of(Part.fromText(conceptuallyModifiedText)))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-82>)                            .build())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-83>)                    .build())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-84>)            .build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-85>)    System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-86>)        "Modified System Instruction %s", llmRequest.config().get().systemInstruction());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-87>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-88>)    // --- Skip Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-89>)    // Check if the last user message contains "BLOCK"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-90>)    if (lastUserMessage.toUpperCase().contains("BLOCK")) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-91>)      System.out.println("[Callback] 'BLOCK' keyword found. Skipping LLM call.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-92>)      // Return an LlmResponse to skip the actual LLM call
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-93>)      return Maybe.just(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-94>)          LlmResponse.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-95>)              .content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-96>)                  Content.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-97>)                      .role("model")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-98>)                      .parts(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-99>)                          ImmutableList.of(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-100>)                              Part.fromText("LLM call was blocked by before_model_callback.")))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-101>)                      .build())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-102>)              .build());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-103>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-104>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-105>)    // Return Empty response to allow the (modified) request to go to the LLM
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-106>)    System.out.println("[Callback] Proceeding with LLM call (using the original LlmRequest).");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-107>)    return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-108>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-109>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-110>)  // --- 2. Define Agent and Run Scenarios ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-111>)  public void defineAgentAndRun() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-112>)    // Setup Agent with Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-113>)    LlmAgent myLlmAgent =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-114>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-115>)            .name(AGENT_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-116>)            .model(MODEL_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-117>)            .instruction(AGENT_INSTRUCTION)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-118>)            .description(AGENT_DESCRIPTION)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-119>)            .beforeModelCallback(this::simpleBeforeModelModifier)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-120>)            .build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-121>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-122>)    // Create an InMemoryRunner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-123>)    InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-124>)    // InMemoryRunner automatically creates a session service. Create a session using the service
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-125>)    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-126>)    Content userMessage =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-127>)        Content.fromParts(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-128>)            Part.fromText("Tell me about quantum computing. This is a test. So BLOCK."));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-129>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-130>)    // Run the agent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-131>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-132>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-133>)    // Stream event response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-134>)    eventStream.blockingForEach(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-135>)        event -> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-136>)          if (event.finalResponse()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-137>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-138>)          }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-139>)        });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-140>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-12-141>)}
    
### After Model Callback[¶](<https://adk.dev/callbacks/types-of-callbacks/#after-model-callback> "Permanent link")

**When:** Called just after a response (`LlmResponse`) is received from the LLM, before it's processed further by the invoking agent.

**Purpose:** Allows inspection or modification of the raw LLM response. Use cases include

  * logging model outputs,
  * reformatting responses,
  * censoring sensitive information generated by the model,
  * parsing structured data from the LLM response and storing it in `callback_context.state`
  * or handling specific error codes.

Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-2>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-6>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-8>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-13>)# limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-15>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-16>)from google.adk.agents.callback_context import CallbackContext
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-17>)from google.adk.runners import Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-18>)from typing import Optional
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-19>)from google.genai import types 
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-20>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-21>)from google.adk.models import LlmResponse
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-22>)from copy import deepcopy
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-23>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-24>)GEMINI_2_FLASH="gemini-2.0-flash"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-26>)# --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-27>)def simple_after_model_modifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-28>)    callback_context: CallbackContext, llm_response: LlmResponse
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-29>)) -> Optional[LlmResponse]:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-30>)    """Inspects/modifies the LLM response after it's received."""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-31>)    agent_name = callback_context.agent_name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-32>)    print(f"[Callback] After model call for agent: {agent_name}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-33>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-34>)    # --- Inspection ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-35>)    original_text = ""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-36>)    if llm_response.content and llm_response.content.parts:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-37>)        # Assuming simple text response for this example
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-38>)        if llm_response.content.parts[0].text:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-39>)            original_text = llm_response.content.parts[0].text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-40>)            print(f"[Callback] Inspected original response text: '{original_text[:100]}...'") # Log snippet
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-41>)        elif llm_response.content.parts[0].function_call:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-42>)             print(f"[Callback] Inspected response: Contains function call '{llm_response.content.parts[0].function_call.name}'. No text modification.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-43>)             return None # Don't modify tool calls in this example
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-44>)        else:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-45>)             print("[Callback] Inspected response: No text content found.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-46>)             return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-47>)    elif llm_response.error_message:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-48>)        print(f"[Callback] Inspected response: Contains error '{llm_response.error_message}'. No modification.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-49>)        return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-50>)    else:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-51>)        print("[Callback] Inspected response: Empty LlmResponse.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-52>)        return None # Nothing to modify
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-53>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-54>)    # --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-55>)    # Replace "joke" with "funny story" (case-insensitive)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-56>)    search_term = "joke"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-57>)    replace_term = "funny story"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-58>)    if search_term in original_text.lower():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-59>)        print(f"[Callback] Found '{search_term}'. Modifying response.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-60>)        modified_text = original_text.replace(search_term, replace_term)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-61>)        modified_text = modified_text.replace(search_term.capitalize(), replace_term.capitalize()) # Handle capitalization
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-62>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-63>)        # Create a NEW LlmResponse with the modified content
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-64>)        # Deep copy parts to avoid modifying original if other callbacks exist
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-65>)        modified_parts = [deepcopy(part) for part in llm_response.content.parts]
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-66>)        modified_parts[0].text = modified_text # Update the text in the copied part
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-67>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-68>)        new_response = LlmResponse(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-69>)             content=types.Content(role="model", parts=modified_parts),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-70>)             # Copy other relevant fields if necessary, e.g., grounding_metadata
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-71>)             grounding_metadata=llm_response.grounding_metadata
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-72>)             )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-73>)        print(f"[Callback] Returning modified response.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-74>)        return new_response # Return the modified response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-75>)    else:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-76>)        print(f"[Callback] '{search_term}' not found. Passing original response through.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-77>)        # Return None to use the original llm_response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-78>)        return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-79>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-80>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-81>)# Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-82>)my_llm_agent = LlmAgent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-83>)        name="AfterModelCallbackAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-84>)        model=GEMINI_2_FLASH,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-85>)        instruction="You are a helpful assistant.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-86>)        description="An LLM agent demonstrating after_model_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-87>)        after_model_callback=simple_after_model_modifier # Assign the function here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-88>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-89>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-90>)APP_NAME = "guardrail_app"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-91>)USER_ID = "user_1"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-92>)SESSION_ID = "session_001"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-93>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-94>)# Session and Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-95>)async def setup_session_and_runner():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-96>)    session_service = InMemorySessionService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-97>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-98>)    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-99>)    return session, runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-100>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-101>)# Agent Interaction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-102>)async def call_agent_async(query):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-103>)  session, runner = await setup_session_and_runner()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-104>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-105>)  content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-106>)  events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-107>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-108>)  async for event in events:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-109>)      if event.is_final_response():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-110>)          final_response = event.content.parts[0].text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-111>)          print("Agent Response: ", final_response)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-112>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-113>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-114>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-13-115>)await call_agent_async("""write multiple time the word "joke" """)
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-1>)/**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-3>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-7>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-9>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-14>) * limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-15>) */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-16>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-17>)import { LlmAgent, InMemoryRunner, Context, isFinalResponse } from '@google/adk';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-18>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-20>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-21>)const APP_NAME = "after_model_callback_app";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-22>)const USER_ID = "test_user_after_model";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-23>)const SESSION_ID_JOKE = "session_modify_model_call";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-24>)const SESSION_ID_POEM = "session_normal_model_call";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-26>)// --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-27>)function simpleAfterModelModifier({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-28>)  context,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-29>)  response,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-30>)}: {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-31>)  context: Context;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-32>)  response: any;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-33>)}): any | undefined {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-34>)  console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-35>)    `[Callback] After model call for agent: ${context.agentName}`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-36>)  );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-37>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-38>)  const modelResponseText = response.content?.parts?.[0]?.text ?? "";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-39>)  console.log(`[Callback] Inspecting model response: "${modelResponseText.substring(0, 50)}..."`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-40>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-41>)  // --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-42>)  // Replace "joke" with "funny story" (case-insensitive)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-43>)  const searchTerm = "joke";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-44>)  const replaceTerm = "funny story";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-45>)  if (modelResponseText.toLowerCase().includes(searchTerm)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-46>)    console.log(`[Callback] Found '${searchTerm}'. Modifying response.`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-47>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-48>)    // Create a deep copy to avoid mutating the original response object
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-49>)    const modifiedResponse = JSON.parse(JSON.stringify(response));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-50>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-51>)    // Safely modify the text of the first part
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-52>)    if (modifiedResponse.content?.parts?.[0]) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-53>)      // Use a regular expression for case-insensitive replacement
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-54>)      const regex = new RegExp(searchTerm, "gi");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-55>)      modifiedResponse.content.parts[0].text = modelResponseText.replace(regex, replaceTerm);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-56>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-57>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-58>)    console.log(`[Callback] Returning modified response.`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-59>)    return modifiedResponse;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-60>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-61>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-62>)  console.log("[Callback] Proceeding with original LLM response.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-63>)  // Return undefined to proceed without any modifications
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-64>)  return undefined;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-65>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-66>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-67>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-68>)// --- Create LlmAgent and Assign Callback ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-69>)const myLlmAgent = new LlmAgent({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-70>)  name: "AfterModelCallbackAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-71>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-72>)  instruction: "You are a helpful assistant who tells jokes.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-73>)  description: "An LLM agent demonstrating after_model_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-74>)  afterModelCallback: simpleAfterModelModifier, // Assign the function here
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-75>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-76>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-77>)// --- Agent Interaction Logic ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-78>)async function callAgentAndPrint({runner, query, sessionId,}: {  runner: InMemoryRunner;  query: string;  sessionId: string;}) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-79>)  console.log(`\n>>> Calling Agent with query: "${query}"`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-80>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-81>)  let finalResponseContent = "No final response received.";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-82>)  const events = runner.runAsync({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-83>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-84>)    sessionId: sessionId,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-85>)    newMessage: createUserContent(query),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-86>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-87>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-88>)  for await (const event of events) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-89>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-90>)      finalResponseContent = event.content.parts
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-91>)        .map((part: { text?: string }) => part.text ?? "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-92>)        .join("");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-93>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-94>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-95>)  console.log("<<< Agent Response: ", finalResponseContent);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-96>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-97>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-98>)// --- Run Interactions ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-99>)async function main() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-100>)  const runner = new InMemoryRunner({ agent: myLlmAgent, appName: APP_NAME });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-101>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-102>)  // Scenario 1: The callback will find "joke" and modify the response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-103>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-104>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-105>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-106>)    sessionId: SESSION_ID_JOKE,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-107>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-108>)  await callAgentAndPrint({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-109>)    runner: runner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-110>)    query: 'write a short joke about computers',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-111>)    sessionId: SESSION_ID_JOKE,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-112>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-113>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-114>)  // Scenario 2: The callback will not find "joke" and will pass the response through unmodified
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-115>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-116>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-117>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-118>)    sessionId: SESSION_ID_POEM,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-119>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-120>)  await callAgentAndPrint({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-121>)    runner: runner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-122>)    query: 'write a short poem about coding',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-123>)    sessionId: SESSION_ID_POEM,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-124>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-125>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-126>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-14-127>)main();
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-1>)package main
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-2>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-3>)import (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-4>)    "context"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-5>)    "fmt"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-6>)    "log"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-7>)    "regexp"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-8>)    "strings"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-9>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-10>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-11>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-12>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-13>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-14>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-15>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-16>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-17>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-18>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-19>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-20>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-21>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-22>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-23>)func onAfterModel(ctx agent.Context, resp *model.LLMResponse, respErr error) (*model.LLMResponse, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-24>)    log.Printf("[Callback] AfterModel triggered for agent %q.", ctx.AgentName())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-25>)    if respErr != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-26>)        log.Printf("[Callback] Model returned an error: %v. Passing it through.", respErr)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-27>)        return nil, respErr
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-28>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-29>)    if resp == nil || resp.Content == nil || len(resp.Content.Parts) == 0 {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-30>)        log.Println("[Callback] Response is nil or has no parts, nothing to process.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-31>)        return nil, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-32>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-33>)    // Check for function calls and pass them through without modification.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-34>)    if resp.Content.Parts[0].FunctionCall != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-35>)        log.Println("[Callback] Response is a function call. No modification.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-36>)        return nil, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-37>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-38>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-39>)    originalText := resp.Content.Parts[0].Text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-40>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-41>)    // Use a case-insensitive regex with word boundaries to find "joke".
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-42>)    re := regexp.MustCompile(`(?i)\bjoke\b`)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-43>)    if !re.MatchString(originalText) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-44>)        log.Println("[Callback] 'joke' not found. Passing original response through.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-45>)        return nil, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-46>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-47>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-48>)    log.Println("[Callback] 'joke' found. Modifying response.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-49>)    // Use a replacer function to handle capitalization.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-50>)    modifiedText := re.ReplaceAllStringFunc(originalText, func(s string) string {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-51>)        if strings.ToUpper(s) == "JOKE" {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-52>)            if s == "Joke" {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-53>)                return "Funny story"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-54>)            }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-55>)            return "funny story"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-56>)        }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-57>)        return s // Should not be reached with this regex, but it's safe.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-58>)    })
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-59>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-60>)    resp.Content.Parts[0].Text = modifiedText
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-61>)    return resp, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-62>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-63>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-64>)func runAfterModelExample() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-65>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-66>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-67>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-68>)        log.Fatalf("FATAL: Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-69>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-70>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-71>)    llmCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-72>)        Name:                "AgentWithAfterModelCallback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-73>)        Model:               geminiModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-74>)        AfterModelCallbacks: []llmagent.AfterModelCallback{onAfterModel},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-75>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-76>)    testAgent, err := llmagent.New(llmCfg)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-77>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-78>)        log.Fatalf("FATAL: Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-79>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-80>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-81>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-82>)    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-83>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-84>)        log.Fatalf("FATAL: Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-85>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-86>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-87>)    log.Println("--- SCENARIO 1: Response should be modified ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-88>)    runScenario(ctx, r, sessionService, appName, "session_modify", nil, `Give me a paragraph about different styles of jokes.`)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-15-89>)}
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-2>)import com.google.adk.agents.CallbackContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-4>)import com.google.adk.models.LlmResponse;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-5>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-6>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-7>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-8>)import com.google.genai.types.Content;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-9>)import com.google.genai.types.Part;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-10>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-11>)import io.reactivex.rxjava3.core.Maybe;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-12>)import java.util.ArrayList;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-13>)import java.util.List;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-14>)import java.util.Optional;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-15>)import java.util.regex.Matcher;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-16>)import java.util.regex.Pattern;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-17>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-18>)public class AfterModelCallbackExample {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-20>)  // --- Define Constants ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-21>)  private static final String AGENT_NAME = "AfterModelCallbackAgent";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-22>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-23>)  private static final String AGENT_INSTRUCTION = "You are a helpful assistant.";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-24>)  private static final String AGENT_DESCRIPTION = "An LLM agent demonstrating after_model_callback";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-26>)  // For session and runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-27>)  private static final String APP_NAME = "AfterModelCallbackAgentApp";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-28>)  private static final String USER_ID = "user_1";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-29>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-30>)  // For text replacement
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-31>)  private static final String SEARCH_TERM = "joke";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-32>)  private static final String REPLACE_TERM = "funny story";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-33>)  private static final Pattern SEARCH_PATTERN =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-34>)      Pattern.compile("\\b" + Pattern.quote(SEARCH_TERM) + "\\b", Pattern.CASE_INSENSITIVE);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-35>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-36>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-37>)    AfterModelCallbackExample example = new AfterModelCallbackExample();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-38>)    example.defineAgentAndRun();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-39>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-40>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-41>)  // --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-42>)  // Inspects/modifies the LLM response after it's received.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-43>)  public Maybe<LlmResponse> simpleAfterModelModifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-44>)      CallbackContext callbackContext, LlmResponse llmResponse) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-45>)    String agentName = callbackContext.agentName();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-46>)    System.out.printf("%n[Callback] After model call for agent: %s%n", agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-47>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-48>)    // --- Inspection Phase ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-49>)    if (llmResponse.errorMessage().isPresent()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-50>)      System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-51>)          "[Callback] Response has error: '%s'. No modification.%n",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-52>)          llmResponse.errorMessage().get());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-53>)      return Maybe.empty(); // Pass through errors
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-54>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-55>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-56>)    Optional<Part> firstTextPartOpt =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-57>)        llmResponse
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-58>)            .content()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-59>)            .flatMap(Content::parts)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-60>)            .filter(parts -> !parts.isEmpty() && parts.get(0).text().isPresent())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-61>)            .map(parts -> parts.get(0));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-62>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-63>)    if (!firstTextPartOpt.isPresent()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-64>)      // Could be a function call, empty content, or no text in the first part
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-65>)      llmResponse
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-66>)          .content()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-67>)          .flatMap(Content::parts)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-68>)          .filter(parts -> !parts.isEmpty() && parts.get(0).functionCall().isPresent())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-69>)          .ifPresent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-70>)              parts ->
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-71>)                  System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-72>)                      "[Callback] Response is a function call ('%s'). No text modification.%n",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-73>)                      parts.get(0).functionCall().get().name().orElse("N/A")));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-74>)      if (!llmResponse.content().isPresent()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-75>)          || !llmResponse.content().flatMap(Content::parts).isPresent()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-76>)          || llmResponse.content().flatMap(Content::parts).get().isEmpty()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-77>)        System.out.println(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-78>)            "[Callback] Response content is empty or has no parts. No modification.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-79>)      } else if (!firstTextPartOpt.isPresent()) { // Already checked for function call
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-80>)        System.out.println("[Callback] First part has no text content. No modification.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-81>)      }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-82>)      return Maybe.empty(); // Pass through non-text or unsuitable responses
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-83>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-84>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-85>)    String originalText = firstTextPartOpt.get().text().get();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-86>)    System.out.printf("[Callback] Inspected original text: '%.100s...'%n", originalText);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-87>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-88>)    // --- Modification Phase ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-89>)    Matcher matcher = SEARCH_PATTERN.matcher(originalText);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-90>)    if (!matcher.find()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-91>)      System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-92>)          "[Callback] '%s' not found. Passing original response through.%n", SEARCH_TERM);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-93>)      return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-94>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-95>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-96>)    System.out.printf("[Callback] Found '%s'. Modifying response.%n", SEARCH_TERM);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-97>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-98>)    // Perform the replacement, respecting original capitalization of the found term's first letter
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-99>)    String foundTerm = matcher.group(0); // The actual term found (e.g., "joke" or "Joke")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-100>)    String actualReplaceTerm = REPLACE_TERM;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-101>)    if (Character.isUpperCase(foundTerm.charAt(0)) && REPLACE_TERM.length() > 0) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-102>)      actualReplaceTerm = Character.toUpperCase(REPLACE_TERM.charAt(0)) + REPLACE_TERM.substring(1);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-103>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-104>)    String modifiedText = matcher.replaceFirst(Matcher.quoteReplacement(actualReplaceTerm));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-105>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-106>)    // Create a new LlmResponse with the modified content
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-107>)    Content originalContent = llmResponse.content().get();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-108>)    List<Part> originalParts = originalContent.parts().orElse(ImmutableList.of());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-109>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-110>)    List<Part> modifiedPartsList = new ArrayList<>(originalParts.size());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-111>)    if (!originalParts.isEmpty()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-112>)      modifiedPartsList.add(Part.fromText(modifiedText)); // Replace first part's text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-113>)      // Add remaining parts as they were (shallow copy)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-114>)      for (int i = 1; i < originalParts.size(); i++) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-115>)        modifiedPartsList.add(originalParts.get(i));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-116>)      }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-117>)    } else { // Should not happen if firstTextPartOpt was present
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-118>)      modifiedPartsList.add(Part.fromText(modifiedText));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-119>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-120>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-121>)    LlmResponse.Builder newResponseBuilder =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-122>)        LlmResponse.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-123>)            .content(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-124>)                originalContent.toBuilder().parts(ImmutableList.copyOf(modifiedPartsList)).build())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-125>)            .groundingMetadata(llmResponse.groundingMetadata());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-126>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-127>)    System.out.println("[Callback] Returning modified response.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-128>)    return Maybe.just(newResponseBuilder.build());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-129>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-130>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-131>)  // --- 2. Define Agent and Run Scenarios ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-132>)  public void defineAgentAndRun() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-133>)    // Setup Agent with Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-134>)    LlmAgent myLlmAgent =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-135>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-136>)            .name(AGENT_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-137>)            .model(MODEL_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-138>)            .instruction(AGENT_INSTRUCTION)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-139>)            .description(AGENT_DESCRIPTION)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-140>)            .afterModelCallback(this::simpleAfterModelModifier)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-141>)            .build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-142>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-143>)    // Create an InMemoryRunner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-144>)    InMemoryRunner runner = new InMemoryRunner(myLlmAgent, APP_NAME);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-145>)    // InMemoryRunner automatically creates a session service. Create a session using the service
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-146>)    Session session = runner.sessionService().createSession(APP_NAME, USER_ID).blockingGet();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-147>)    Content userMessage =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-148>)        Content.fromParts(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-149>)            Part.fromText(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-150>)                "Tell me a joke about quantum computing. Include the word 'joke' in your response"));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-151>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-152>)    // Run the agent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-153>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-154>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-155>)    // Stream event response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-156>)    eventStream.blockingForEach(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-157>)        event -> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-158>)          if (event.finalResponse()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-159>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-160>)          }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-161>)        });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-162>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-16-163>)}
    
## Tool Execution Callbacks[¶](<https://adk.dev/callbacks/types-of-callbacks/#tool-execution-callbacks> "Permanent link")

These callbacks are also specific to `LlmAgent` and trigger around the execution of tools (including `FunctionTool`, `AgentTool`, etc.) that the LLM might request.

### Before Tool Callback[¶](<https://adk.dev/callbacks/types-of-callbacks/#before-tool-callback> "Permanent link")

**When:** Called just before a specific tool's `run_async` method is invoked, after the LLM has generated a function call for it.

**Purpose:** Allows inspection and modification of tool arguments, performing authorization checks before execution, logging tool usage attempts, or implementing tool-level caching.

**Return Value Effect:**

  1. If the callback returns `None` (or a `Maybe.empty()` object in Java), the tool's `run_async` method is executed with the (potentially modified) `args`.
  2. If a dictionary (or `Map` in Java) is returned, the tool's `run_async` method is **skipped**. The returned dictionary is used directly as the result of the tool call. This is useful for caching or overriding tool behavior.

Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-2>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-6>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-8>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-13>)# limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-15>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-16>)from google.adk.runners import Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-17>)from typing import Optional
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-18>)from google.genai import types 
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-19>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-20>)from google.adk.tools import FunctionTool
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-21>)from google.adk.tools.tool_context import ToolContext
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-22>)from google.adk.tools.base_tool import BaseTool
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-23>)from typing import Dict, Any
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-24>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-26>)GEMINI_2_FLASH="gemini-2.0-flash"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-27>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-28>)def get_capital_city(country: str) -> str:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-29>)    """Retrieves the capital city of a given country."""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-30>)    print(f"--- Tool 'get_capital_city' executing with country: {country} ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-31>)    country_capitals = {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-32>)        "united states": "Washington, D.C.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-33>)        "canada": "Ottawa",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-34>)        "france": "Paris",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-35>)        "germany": "Berlin",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-36>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-37>)    return country_capitals.get(country.lower(), f"Capital not found for {country}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-38>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-39>)capital_tool = FunctionTool(func=get_capital_city)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-40>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-41>)def simple_before_tool_modifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-42>)    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-43>)) -> Optional[Dict]:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-44>)    """Inspects/modifies tool args or skips the tool call."""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-45>)    agent_name = tool_context.agent_name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-46>)    tool_name = tool.name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-47>)    print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-48>)    print(f"[Callback] Original args: {args}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-49>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-50>)    if tool_name == 'get_capital_city' and args.get('country', '').lower() == 'canada':
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-51>)        print("[Callback] Detected 'Canada'. Modifying args to 'France'.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-52>)        args['country'] = 'France'
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-53>)        print(f"[Callback] Modified args: {args}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-54>)        return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-55>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-56>)    # If the tool is 'get_capital_city' and country is 'BLOCK'
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-57>)    if tool_name == 'get_capital_city' and args.get('country', '').upper() == 'BLOCK':
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-58>)        print("[Callback] Detected 'BLOCK'. Skipping tool execution.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-59>)        return {"result": "Tool execution was blocked by before_tool_callback."}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-60>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-61>)    print("[Callback] Proceeding with original or previously modified args.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-62>)    return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-63>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-64>)my_llm_agent = LlmAgent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-65>)        name="ToolCallbackAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-66>)        model=GEMINI_2_FLASH,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-67>)        instruction="You are an agent that can find capital cities. Use the get_capital_city tool.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-68>)        description="An LLM agent demonstrating before_tool_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-69>)        tools=[capital_tool],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-70>)        before_tool_callback=simple_before_tool_modifier
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-71>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-72>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-73>)APP_NAME = "guardrail_app"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-74>)USER_ID = "user_1"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-75>)SESSION_ID = "session_001"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-76>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-77>)# Session and Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-78>)async def setup_session_and_runner():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-79>)    session_service = InMemorySessionService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-80>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-81>)    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-82>)    return session, runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-83>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-84>)# Agent Interaction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-85>)async def call_agent_async(query):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-86>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-87>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-88>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-89>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-90>)    async for event in events:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-91>)        if event.is_final_response():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-92>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-93>)            print("Agent Response: ", final_response)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-94>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-95>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-96>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-17-97>)await call_agent_async("Canada")
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-1>)/**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-3>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-7>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-9>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-14>) * limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-15>) */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-16>)import { LlmAgent, InMemoryRunner, FunctionTool, Context, isFinalResponse, BaseTool } from '@google/adk';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-17>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-18>)import { z } from 'zod';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-20>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-21>)const APP_NAME = "before_tool_callback_app";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-22>)const USER_ID = "test_user_before_tool";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-23>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-24>)// --- Define a Simple Tool Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-25>)const CountryInput = z.object({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-26>)  country: z.string().describe('The country to get the capital for.'),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-27>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-28>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-29>)async function getCapitalCity(params: z.infer<typeof CountryInput>): Promise<{ result: string }> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-30>)    console.log(`\n-- Tool Call: getCapitalCity(country='${params.country}') --`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-31>)    const capitals: Record<string, string> = {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-32>)        'united states': 'Washington, D.C.',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-33>)        'canada': 'Ottawa',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-34>)        'france': 'Paris',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-35>)        'japan': 'Tokyo',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-36>)    };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-37>)    const result = capitals[params.country.toLowerCase()] ??
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-38>)        `Sorry, I couldn't find the capital for ${params.country}.`;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-39>)    console.log(`-- Tool Result: '${result}' --`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-40>)    return { result };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-41>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-42>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-43>)const getCapitalCityTool = new FunctionTool({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-44>)    name: 'get_capital_city',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-45>)    description: 'Retrieves the capital city for a given country',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-46>)    parameters: CountryInput,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-47>)    execute: getCapitalCity,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-48>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-49>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-50>)// --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-51>)function simpleBeforeToolModifier({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-52>)  tool,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-53>)  args,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-54>)  context,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-55>)}: {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-56>)  tool: BaseTool;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-57>)  args: Record<string, any>;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-58>)  context: Context;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-59>)}) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-60>)  const agentName = context.agentName;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-61>)  const toolName = tool.name;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-62>)  console.log(`[Callback] Before tool call for tool '${toolName}' in agent '${agentName}'`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-63>)  console.log(`[Callback] Original args: ${JSON.stringify(args)}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-64>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-65>)  if (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-66>)    toolName === "get_capital_city" &&
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-67>)    args["country"]?.toLowerCase() === "canada"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-68>)  ) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-69>)    console.log("[Callback] Detected 'Canada'. Modifying args to 'France'.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-70>)    args["country"] = "France";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-71>)    console.log(`[Callback] Modified args: ${JSON.stringify(args)}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-72>)    return undefined;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-73>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-74>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-75>)  if (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-76>)    toolName === "get_capital_city" &&
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-77>)    args["country"]?.toUpperCase() === "BLOCK"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-78>)  ) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-79>)    console.log("[Callback] Detected 'BLOCK'. Skipping tool execution.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-80>)    return { result: "Tool execution was blocked by before_tool_callback." };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-81>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-82>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-83>)  console.log("[Callback] Proceeding with original or previously modified args.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-84>)  return;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-85>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-86>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-87>)// Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-88>)const myLlmAgent = new LlmAgent({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-89>)  name: 'ToolCallbackAgent',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-90>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-91>)  instruction: 'You are an agent that can find capital cities. Use the get_capital_city tool.',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-92>)  description: 'An LLM agent demonstrating before_tool_callback',
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-93>)  tools: [getCapitalCityTool],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-94>)  beforeToolCallback: simpleBeforeToolModifier,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-95>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-96>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-97>)// Agent Interaction Logic
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-98>)async function callAgentAndPrint(runner: InMemoryRunner, query: string, sessionId: string) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-99>)  console.log(`\n>>> Calling Agent for session '${sessionId}' | Query: "${query}"`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-100>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-101>)  for await (const event of runner.runAsync({ userId: USER_ID, sessionId, newMessage: createUserContent(query) })) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-102>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-103>)      const finalResponseContent = event.content.parts.map(part => part.text ?? '').join('');
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-104>)      console.log(`<<< Final Output: ${finalResponseContent}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-105>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-106>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-107>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-108>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-109>)// Run Interactions
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-110>)async function main() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-111>)  const runner = new InMemoryRunner({ agent: myLlmAgent, appName: APP_NAME });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-112>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-113>)  // Scenario 1: Callback modifies the arguments from "Canada" to "France"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-114>)  const canadaSessionId = 'session_canada_test';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-115>)  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: canadaSessionId });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-116>)  await callAgentAndPrint(runner, 'What is the capital of Canada?', canadaSessionId);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-117>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-118>)  // Scenario 2: Callback skips the tool call
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-119>)  const blockSessionId = 'session_block_test';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-120>)  await runner.sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: blockSessionId });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-121>)  await callAgentAndPrint(runner, 'What is the capital of BLOCK?', blockSessionId);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-122>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-123>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-18-124>)main();
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-1>)package main
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-2>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-3>)import (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-4>)    "context"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-5>)    "fmt"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-6>)    "log"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-7>)    "regexp"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-8>)    "strings"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-9>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-10>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-11>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-12>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-13>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-14>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-15>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-16>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-17>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-18>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-19>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-20>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-21>)// GetCapitalCityArgs defines the arguments for the getCapitalCity tool.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-22>)type GetCapitalCityArgs struct {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-23>)    Country string `json:"country" jsonschema:"The country to get the capital of."`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-24>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-26>)// getCapitalCity is a tool that returns the capital of a given country.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-27>)func getCapitalCity(ctx agent.Context, args *GetCapitalCityArgs) (string, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-28>)    capitals := map[string]string{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-29>)        "canada":        "Ottawa",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-30>)        "france":        "Paris",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-31>)        "germany":       "Berlin",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-32>)        "united states": "Washington, D.C.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-33>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-34>)    capital, ok := capitals[strings.ToLower(args.Country)]
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-35>)    if !ok {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-36>)        return "", fmt.Errorf("unknown country: %s", args.Country)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-37>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-38>)    return capital, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-39>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-40>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-41>)func onBeforeTool(ctx agent.Context, t tool.Tool, args map[string]any) (map[string]any, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-42>)    log.Printf("[Callback] BeforeTool triggered for tool %q in agent %q.", t.Name(), ctx.AgentName())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-43>)    log.Printf("[Callback] Original args: %v", args)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-44>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-45>)    if t.Name() == "getCapitalCity" {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-46>)        if country, ok := args["country"].(string); ok {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-47>)            if strings.ToLower(country) == "canada" {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-48>)                log.Println("[Callback] Detected 'Canada'. Modifying args to 'France'.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-49>)                args["country"] = "France"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-50>)                return args, nil // Proceed with modified args
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-51>)            } else if strings.ToUpper(country) == "BLOCK" {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-52>)                log.Println("[Callback] Detected 'BLOCK'. Skipping tool execution.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-53>)                // Skip tool and return a custom result.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-54>)                return map[string]any{"result": "Tool execution was blocked by before_tool_callback."}, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-55>)            }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-56>)        }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-57>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-58>)    log.Println("[Callback] Proceeding with original or previously modified args.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-59>)    return nil, nil // Proceed with original args
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-60>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-61>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-62>)func runBeforeToolExample() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-63>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-64>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-65>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-66>)        log.Fatalf("FATAL: Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-67>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-68>)    capitalTool, err := functiontool.New(functiontool.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-69>)        Name:        "getCapitalCity",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-70>)        Description: "Retrieves the capital city of a given country.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-71>)    }, getCapitalCity)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-72>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-73>)        log.Fatalf("FATAL: Failed to create function tool: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-74>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-75>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-76>)    llmCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-77>)        Name:                "AgentWithBeforeToolCallback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-78>)        Model:               geminiModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-79>)        Tools:               []tool.Tool{capitalTool},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-80>)        BeforeToolCallbacks: []llmagent.BeforeToolCallback{onBeforeTool},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-81>)        Instruction:         "You are an agent that can find capital cities. Use the getCapitalCity tool.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-82>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-83>)    testAgent, err := llmagent.New(llmCfg)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-84>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-85>)        log.Fatalf("FATAL: Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-86>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-87>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-88>)    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-89>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-90>)        log.Fatalf("FATAL: Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-91>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-92>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-93>)    log.Println("--- SCENARIO 1: Args should be modified ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-94>)    runScenario(ctx, r, sessionService, appName, "session_tool_modify", nil, "What is the capital of Canada?")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-95>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-96>)    log.Println("--- SCENARIO 2: Tool call should be blocked ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-97>)    runScenario(ctx, r, sessionService, appName, "session_tool_block", nil, "capital of BLOCK")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-19-98>)}
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-2>)import com.google.adk.agents.InvocationContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-4>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-5>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-6>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-7>)import com.google.adk.tools.BaseTool;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-8>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-9>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-10>)import com.google.common.collect.ImmutableMap;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-11>)import com.google.genai.types.Content;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-12>)import com.google.genai.types.Part;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-13>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-14>)import io.reactivex.rxjava3.core.Maybe;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-15>)import java.util.HashMap;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-16>)import java.util.Map;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-17>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-18>)public class BeforeToolCallbackExample {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-20>)  private static final String APP_NAME = "ToolCallbackAgentApp";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-21>)  private static final String USER_ID = "user_1";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-22>)  private static final String SESSION_ID = "session_001";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-23>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-24>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-25>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-26>)    BeforeToolCallbackExample example = new BeforeToolCallbackExample();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-27>)    example.runAgent("capital of canada");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-28>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-29>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-30>)  // --- Define a Simple Tool Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-31>)  // The Schema is important for the callback "args" to correctly identify the input.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-32>)  public static Map<String, Object> getCapitalCity(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-33>)      @Schema(name = "country", description = "The country to find the capital of.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-34>)          String country) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-35>)    System.out.printf("--- Tool 'getCapitalCity' executing with country: %s ---%n", country);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-36>)    Map<String, String> countryCapitals = new HashMap<>();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-37>)    countryCapitals.put("united states", "Washington, D.C.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-38>)    countryCapitals.put("canada", "Ottawa");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-39>)    countryCapitals.put("france", "Paris");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-40>)    countryCapitals.put("germany", "Berlin");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-41>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-42>)    String capital =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-43>)        countryCapitals.getOrDefault(country.toLowerCase(), "Capital not found for " + country);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-44>)    // FunctionTool expects a Map<String, Object> as the return type for the method it wraps.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-45>)    return ImmutableMap.of("capital", capital);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-46>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-47>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-48>)  // Define the Callback function
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-49>)  // The Tool callback provides all these parameters by default.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-50>)  public Maybe<Map<String, Object>> simpleBeforeToolModifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-51>)      InvocationContext invocationContext,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-52>)      BaseTool tool,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-53>)      Map<String, Object> args,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-54>)      ToolContext toolContext) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-55>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-56>)    String agentName = invocationContext.agent().name();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-57>)    String toolName = tool.name();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-58>)    System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-59>)        "[Callback] Before tool call for tool '%s' in agent '%s'%n", toolName, agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-60>)    System.out.printf("[Callback] Original args: %s%n", args);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-61>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-62>)    if ("getCapitalCity".equals(toolName)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-63>)      String countryArg = (String) args.get("country");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-64>)      if (countryArg != null) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-65>)        if ("canada".equalsIgnoreCase(countryArg)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-66>)          System.out.println("[Callback] Detected 'Canada'. Modifying args to 'France'.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-67>)          args.put("country", "France");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-68>)          System.out.printf("[Callback] Modified args: %s%n", args);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-69>)          // Proceed with modified args
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-70>)          return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-71>)        } else if ("BLOCK".equalsIgnoreCase(countryArg)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-72>)          System.out.println("[Callback] Detected 'BLOCK'. Skipping tool execution.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-73>)          // Return a map to skip the tool call and use this as the result
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-74>)          return Maybe.just(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-75>)              ImmutableMap.of("result", "Tool execution was blocked by before_tool_callback."));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-76>)        }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-77>)      }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-78>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-79>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-80>)    System.out.println("[Callback] Proceeding with original or previously modified args.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-81>)    return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-82>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-83>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-84>)  public void runAgent(String query) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-85>)    // --- Wrap the function into a Tool ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-86>)    FunctionTool capitalTool = FunctionTool.create(this.getClass(), "getCapitalCity");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-87>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-88>)    // Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-89>)    LlmAgent myLlmAgent =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-90>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-91>)            .name(APP_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-92>)            .model(MODEL_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-93>)            .instruction(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-94>)                "You are an agent that can find capital cities. Use the getCapitalCity tool.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-95>)            .description("An LLM agent demonstrating before_tool_callback")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-96>)            .tools(capitalTool)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-97>)            .beforeToolCallback(this::simpleBeforeToolModifier)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-98>)            .build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-99>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-100>)    // Session and Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-101>)    InMemoryRunner runner = new InMemoryRunner(myLlmAgent);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-102>)    Session session =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-103>)        runner.sessionService().createSession(APP_NAME, USER_ID, null, SESSION_ID).blockingGet();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-104>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-105>)    Content userMessage = Content.fromParts(Part.fromText(query));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-106>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-107>)    System.out.printf("%n--- Calling agent with query: \"%s\" ---%n", query);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-108>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-109>)    // Stream event response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-110>)    eventStream.blockingForEach(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-111>)        event -> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-112>)          if (event.finalResponse()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-113>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-114>)          }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-115>)        });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-116>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-20-117>)}
    
### After Tool Callback[¶](<https://adk.dev/callbacks/types-of-callbacks/#after-tool-callback> "Permanent link")

**When:** Called just after the tool's `run_async` method completes successfully.

**Purpose:** Allows inspection and modification of the tool's result before it's sent back to the LLM (potentially after summarization). Useful for logging tool results, post-processing or formatting results, or saving specific parts of the result to the session state.

**Return Value Effect:**

  1. If the callback returns `None` (or a `Maybe.empty()` object in Java), the original `tool_response` is used.
  2. If a new dictionary is returned, it **replaces** the original `tool_response`. This allows modifying or filtering the result seen by the LLM.

Code

PythonTypescriptGoJava
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-2>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-6>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-8>)#
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-13>)# limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-14>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-15>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-16>)from google.adk.runners import Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-17>)from typing import Optional
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-18>)from google.genai import types 
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-19>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-20>)from google.adk.tools import FunctionTool
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-21>)from google.adk.tools.tool_context import ToolContext
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-22>)from google.adk.tools.base_tool import BaseTool
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-23>)from typing import Dict, Any
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-24>)from copy import deepcopy
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-26>)GEMINI_2_FLASH="gemini-2.0-flash"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-27>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-28>)# --- Define a Simple Tool Function (Same as before) ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-29>)def get_capital_city(country: str) -> str:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-30>)    """Retrieves the capital city of a given country."""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-31>)    print(f"--- Tool 'get_capital_city' executing with country: {country} ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-32>)    country_capitals = {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-33>)        "united states": "Washington, D.C.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-34>)        "canada": "Ottawa",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-35>)        "france": "Paris",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-36>)        "germany": "Berlin",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-37>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-38>)    return {"result": country_capitals.get(country.lower(), f"Capital not found for {country}")}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-39>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-40>)# --- Wrap the function into a Tool ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-41>)capital_tool = FunctionTool(func=get_capital_city)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-42>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-43>)# --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-44>)def simple_after_tool_modifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-45>)    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext, tool_response: Dict
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-46>)) -> Optional[Dict]:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-47>)    """Inspects/modifies the tool result after execution."""
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-48>)    agent_name = tool_context.agent_name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-49>)    tool_name = tool.name
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-50>)    print(f"[Callback] After tool call for tool '{tool_name}' in agent '{agent_name}'")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-51>)    print(f"[Callback] Args used: {args}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-52>)    print(f"[Callback] Original tool_response: {tool_response}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-53>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-54>)    # Default structure for function tool results is {"result": <return_value>}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-55>)    original_result_value = tool_response.get("result", "")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-56>)    # original_result_value = tool_response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-57>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-58>)    # --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-59>)    # If the tool was 'get_capital_city' and result is 'Washington, D.C.'
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-60>)    if tool_name == 'get_capital_city' and original_result_value == "Washington, D.C.":
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-61>)        print("[Callback] Detected 'Washington, D.C.'. Modifying tool response.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-62>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-63>)        # IMPORTANT: Create a new dictionary or modify a copy
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-64>)        modified_response = deepcopy(tool_response)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-65>)        modified_response["result"] = f"{original_result_value} (Note: This is the capital of the USA)."
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-66>)        modified_response["note_added_by_callback"] = True # Add extra info if needed
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-67>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-68>)        print(f"[Callback] Modified tool_response: {modified_response}")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-69>)        return modified_response # Return the modified dictionary
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-70>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-71>)    print("[Callback] Passing original tool response through.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-72>)    # Return None to use the original tool_response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-73>)    return None
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-74>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-75>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-76>)# Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-77>)my_llm_agent = LlmAgent(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-78>)        name="AfterToolCallbackAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-79>)        model=GEMINI_2_FLASH,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-80>)        instruction="You are an agent that finds capital cities using the get_capital_city tool. Report the result clearly.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-81>)        description="An LLM agent demonstrating after_tool_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-82>)        tools=[capital_tool], # Add the tool
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-83>)        after_tool_callback=simple_after_tool_modifier # Assign the callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-84>)    )
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-85>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-86>)APP_NAME = "guardrail_app"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-87>)USER_ID = "user_1"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-88>)SESSION_ID = "session_001"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-89>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-90>)# Session and Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-91>)async def setup_session_and_runner():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-92>)    session_service = InMemorySessionService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-93>)    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-94>)    runner = Runner(agent=my_llm_agent, app_name=APP_NAME, session_service=session_service)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-95>)    return session, runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-96>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-97>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-98>)# Agent Interaction
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-99>)async def call_agent_async(query):
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-100>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-101>)    session, runner = await setup_session_and_runner()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-102>)    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-103>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-104>)    async for event in events:
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-105>)        if event.is_final_response():
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-106>)            final_response = event.content.parts[0].text
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-107>)            print("Agent Response: ", final_response)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-108>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-109>)# Note: In Colab, you can directly use 'await' at the top level.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-110>)# If running this code as a standalone Python script, you'll need to use asyncio.run() or manage the event loop.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-21-111>)await call_agent_async("united states")
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-1>)/**
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-2>) * Copyright 2025 Google LLC
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-3>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-4>) * Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-5>) * you may not use this file except in compliance with the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-6>) * You may obtain a copy of the License at
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-7>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-8>) *     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-9>) *
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-10>) * Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-11>) * distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-12>) * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-13>) * See the License for the specific language governing permissions and
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-14>) * limitations under the License.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-15>) */
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-16>)import { LlmAgent, InMemoryRunner, FunctionTool, isFinalResponse, Context, BaseTool } from '@google/adk';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-17>)import { createUserContent } from "@google/genai";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-18>)import { z } from "zod";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-20>)const MODEL_NAME = "gemini-2.5-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-21>)const APP_NAME = "after_tool_callback_app";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-22>)const USER_ID = "test_user_after_tool";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-23>)const SESSION_ID = "session_001";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-24>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-25>)// --- Define a Simple Tool Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-26>)const CountryInput = z.object({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-27>)  country: z.string().describe("The country to get the capital for."),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-28>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-29>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-30>)async function getCapitalCity(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-31>)  params: z.infer<typeof CountryInput>,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-32>)): Promise<{ result: string }> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-33>)  console.log(`--- Tool 'get_capital_city' executing with country: ${params.country} ---`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-34>)  const countryCapitals: Record<string, string> = {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-35>)    "united states": "Washington, D.C.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-36>)    "canada": "Ottawa",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-37>)    "france": "Paris",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-38>)    "germany": "Berlin",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-39>)  };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-40>)  const result = countryCapitals[params.country.toLowerCase()] ?? `Capital not found for ${params.country}`;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-41>)  return { result };
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-42>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-43>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-44>)// --- Wrap the function into a Tool ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-45>)const capitalTool = new FunctionTool({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-46>)  name: "get_capital_city",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-47>)  description: "Retrieves the capital city for a given country",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-48>)  parameters: CountryInput,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-49>)  execute: getCapitalCity,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-50>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-51>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-52>)// --- Define the Callback Function ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-53>)function simpleAfterToolModifier({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-54>)  tool,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-55>)  args,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-56>)  context,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-57>)  response,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-58>)}: {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-59>)  tool: BaseTool;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-60>)  args: Record<string, any>;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-61>)  context: Context;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-62>)  response: Record<string, any>;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-63>)}) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-64>)  const agentName = context.agentName;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-65>)  const toolName = tool.name;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-66>)  console.log(`[Callback] After tool call for tool '${toolName}' in agent '${agentName}'`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-67>)  console.log(`[Callback] Original args: ${args}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-68>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-69>)  const originalResultValue = response?.result || "";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-70>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-71>)  // --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-72>)  if (toolName === "get_capital_city" && originalResultValue === "Washington, D.C.") {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-73>)    const modifiedResponse = JSON.parse(JSON.stringify(response));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-74>)    modifiedResponse.result = `${originalResultValue} (Note: This is the capital of the USA).`;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-75>)    modifiedResponse["note_added_by_callback"] = true;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-76>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-77>)    console.log(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-78>)      `[Callback] Modified response: ${JSON.stringify(modifiedResponse)}`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-79>)    );
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-80>)    return modifiedResponse;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-81>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-82>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-83>)  console.log('[Callback] Passing original tool response through.');
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-84>)  return undefined;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-85>)};
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-86>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-87>)// Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-88>)const myLlmAgent = new LlmAgent({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-89>)  name: "AfterToolCallbackAgent",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-90>)  model: MODEL_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-91>)  instruction: "You are an agent that finds capital cities using the get_capital_city tool. Report the result clearly.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-92>)  description: "An LLM agent demonstrating after_tool_callback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-93>)  tools: [capitalTool],
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-94>)  afterToolCallback: simpleAfterToolModifier,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-95>)});
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-96>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-97>)// Agent Interaction Logic
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-98>)async function callAgentAndPrint(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-99>)  runner: InMemoryRunner,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-100>)  agent: LlmAgent,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-101>)  sessionId: string,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-102>)  query: string,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-103>)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-104>)  console.log(`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-105>)>>> Calling Agent: '${agent.name}' | Query: ${query}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-106>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-107>)  let finalResponseContent = "";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-108>)  for await (const event of runner.runAsync({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-109>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-110>)    sessionId: sessionId,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-111>)    newMessage: createUserContent(query),
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-112>)  })) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-113>)    const authorName = event.author || "System";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-114>)    if (isFinalResponse(event) && event.content?.parts?.length) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-115>)      finalResponseContent = 'The capital of the united states is Washington, D.C. (Note: This is the capital of the USA).';
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-116>)      console.log(`--- Output from: ${authorName} ---`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-117>)    } else if (event.errorMessage) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-118>)      console.log(`  -> Error from ${authorName}: ${event.errorMessage}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-119>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-120>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-121>)  console.log(`<<< Agent '${agent.name}' Response: ${finalResponseContent}`);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-122>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-123>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-124>)// Run Interactions
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-125>)async function main() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-126>)  const runner = new InMemoryRunner({ appName: APP_NAME, agent: myLlmAgent });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-127>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-128>)  await runner.sessionService.createSession({
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-129>)    appName: APP_NAME,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-130>)    userId: USER_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-131>)    sessionId: SESSION_ID,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-132>)  });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-133>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-134>)  await callAgentAndPrint(runner, myLlmAgent, SESSION_ID, "united states");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-135>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-136>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-22-137>)main();
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-1>)package main
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-2>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-3>)import (
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-4>)    "context"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-5>)    "fmt"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-6>)    "log"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-7>)    "regexp"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-8>)    "strings"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-9>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-10>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-11>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-12>)    "google.golang.org/adk/v2/model"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-13>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-14>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-15>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-16>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-17>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-18>)    "google.golang.org/genai"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-19>))
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-20>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-21>)// GetCapitalCityArgs defines the arguments for the getCapitalCity tool.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-22>)type GetCapitalCityArgs struct {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-23>)    Country string `json:"country" jsonschema:"The country to get the capital of."`
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-24>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-25>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-26>)// getCapitalCity is a tool that returns the capital of a given country.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-27>)func getCapitalCity(ctx agent.Context, args *GetCapitalCityArgs) (string, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-28>)    capitals := map[string]string{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-29>)        "canada":        "Ottawa",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-30>)        "france":        "Paris",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-31>)        "germany":       "Berlin",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-32>)        "united states": "Washington, D.C.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-33>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-34>)    capital, ok := capitals[strings.ToLower(args.Country)]
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-35>)    if !ok {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-36>)        return "", fmt.Errorf("unknown country: %s", args.Country)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-37>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-38>)    return capital, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-39>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-40>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-41>)func onAfterTool(ctx agent.Context, t tool.Tool, args map[string]any, result map[string]any, err error) (map[string]any, error) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-42>)    log.Printf("[Callback] AfterTool triggered for tool %q in agent %q.", t.Name(), ctx.AgentName())
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-43>)    log.Printf("[Callback] Original result: %v", result)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-44>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-45>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-46>)        log.Printf("[Callback] Tool run produced an error: %v. Passing through.", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-47>)        return nil, err
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-48>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-49>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-50>)    if t.Name() == "getCapitalCity" {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-51>)        if originalResult, ok := result["result"].(string); ok && originalResult == "Washington, D.C." {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-52>)            log.Println("[Callback] Detected 'Washington, D.C.'. Modifying tool response.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-53>)            modifiedResult := make(map[string]any)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-54>)            for k, v := range result {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-55>)                modifiedResult[k] = v
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-56>)            }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-57>)            modifiedResult["result"] = fmt.Sprintf("%s (Note: This is the capital of the USA).", originalResult)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-58>)            modifiedResult["note_added_by_callback"] = true
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-59>)            return modifiedResult, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-60>)        }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-61>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-62>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-63>)    log.Println("[Callback] Passing original tool response through.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-64>)    return nil, nil
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-65>)}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-66>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-67>)func runAfterToolExample() {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-68>)    ctx := context.Background()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-69>)    geminiModel, err := gemini.NewModel(ctx, modelName, &genai.ClientConfig{})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-70>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-71>)        log.Fatalf("FATAL: Failed to create model: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-72>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-73>)    capitalTool, err := functiontool.New(functiontool.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-74>)        Name:        "getCapitalCity",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-75>)        Description: "Retrieves the capital city of a given country.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-76>)    }, getCapitalCity)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-77>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-78>)        log.Fatalf("FATAL: Failed to create function tool: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-79>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-80>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-81>)    llmCfg := llmagent.Config{
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-82>)        Name:               "AgentWithAfterToolCallback",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-83>)        Model:              geminiModel,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-84>)        Tools:              []tool.Tool{capitalTool},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-85>)        AfterToolCallbacks: []llmagent.AfterToolCallback{onAfterTool},
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-86>)        Instruction:        "You are an agent that finds capital cities. Use the getCapitalCity tool.",
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-87>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-88>)    testAgent, err := llmagent.New(llmCfg)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-89>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-90>)        log.Fatalf("FATAL: Failed to create agent: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-91>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-92>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-93>)    r, err := runner.New(runner.Config{AppName: appName, Agent: testAgent, SessionService: sessionService})
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-94>)    if err != nil {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-95>)        log.Fatalf("FATAL: Failed to create runner: %v", err)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-96>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-97>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-98>)    log.Println("--- SCENARIO 1: Result should be modified ---")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-99>)    runScenario(ctx, r, sessionService, appName, "session_tool_after_modify", nil, "capital of united states")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-23-100>)}
    
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-2>)import com.google.adk.agents.InvocationContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-4>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-5>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-6>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-7>)import com.google.adk.tools.BaseTool;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-8>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-9>)import com.google.adk.tools.ToolContext;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-10>)import com.google.common.collect.ImmutableMap;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-11>)import com.google.genai.types.Content;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-12>)import com.google.genai.types.Part;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-13>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-14>)import io.reactivex.rxjava3.core.Maybe;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-15>)import java.util.HashMap;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-16>)import java.util.Map;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-17>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-18>)public class AfterToolCallbackExample {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-19>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-20>)  private static final String APP_NAME = "AfterToolCallbackAgentApp";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-21>)  private static final String USER_ID = "user_1";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-22>)  private static final String SESSION_ID = "session_001";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-23>)  private static final String MODEL_NAME = "gemini-2.0-flash";
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-24>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-25>)  public static void main(String[] args) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-26>)    AfterToolCallbackExample example = new AfterToolCallbackExample();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-27>)    example.runAgent("What is the capital of the United States?");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-28>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-29>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-30>)  // --- Define a Simple Tool Function (Same as before) ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-31>)  @Schema(description = "Retrieves the capital city of a given country.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-32>)  public static Map<String, Object> getCapitalCity(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-33>)      @Schema(description = "The country to find the capital of.") String country) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-34>)    System.out.printf("--- Tool 'getCapitalCity' executing with country: %s ---%n", country);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-35>)    Map<String, String> countryCapitals = new HashMap<>();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-36>)    countryCapitals.put("united states", "Washington, D.C.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-37>)    countryCapitals.put("canada", "Ottawa");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-38>)    countryCapitals.put("france", "Paris");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-39>)    countryCapitals.put("germany", "Berlin");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-40>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-41>)    String capital =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-42>)        countryCapitals.getOrDefault(country.toLowerCase(), "Capital not found for " + country);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-43>)    return ImmutableMap.of("result", capital);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-44>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-45>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-46>)  // Define the Callback function.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-47>)  public Maybe<Map<String, Object>> simpleAfterToolModifier(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-48>)      InvocationContext invocationContext,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-49>)      BaseTool tool,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-50>)      Map<String, Object> args,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-51>)      ToolContext toolContext,
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-52>)      Object toolResponse) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-53>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-54>)    // Inspects/modifies the tool result after execution.
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-55>)    String agentName = invocationContext.agent().name();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-56>)    String toolName = tool.name();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-57>)    System.out.printf(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-58>)        "[Callback] After tool call for tool '%s' in agent '%s'%n", toolName, agentName);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-59>)    System.out.printf("[Callback] Args used: %s%n", args);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-60>)    System.out.printf("[Callback] Original tool_response: %s%n", toolResponse);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-61>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-62>)    if (!(toolResponse instanceof Map)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-63>)      System.out.println("[Callback] toolResponse is not a Map, cannot process further.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-64>)      // Pass through if not a map
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-65>)      return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-66>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-67>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-68>)    // Default structure for function tool results is {"result": <return_value>}
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-69>)    @SuppressWarnings("unchecked")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-70>)    Map<String, Object> responseMap = (Map<String, Object>) toolResponse;
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-71>)    Object originalResultValue = responseMap.get("result");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-72>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-73>)    // --- Modification Example ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-74>)    // If the tool was 'get_capital_city' and result is 'Washington, D.C.'
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-75>)    if ("getCapitalCity".equals(toolName) && "Washington, D.C.".equals(originalResultValue)) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-76>)      System.out.println("[Callback] Detected 'Washington, D.C.'. Modifying tool response.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-77>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-78>)      // IMPORTANT: Create a new mutable map or modify a copy
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-79>)      Map<String, Object> modifiedResponse = new HashMap<>(responseMap);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-80>)      modifiedResponse.put(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-81>)          "result", originalResultValue + " (Note: This is the capital of the USA).");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-82>)      modifiedResponse.put("note_added_by_callback", true); // Add extra info if needed
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-83>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-84>)      System.out.printf("[Callback] Modified tool_response: %s%n", modifiedResponse);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-85>)      return Maybe.just(modifiedResponse);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-86>)    }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-87>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-88>)    System.out.println("[Callback] Passing original tool response through.");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-89>)    // Return Maybe.empty() to use the original tool_response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-90>)    return Maybe.empty();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-91>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-92>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-93>)  public void runAgent(String query) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-94>)    // --- Wrap the function into a Tool ---
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-95>)    FunctionTool capitalTool = FunctionTool.create(this.getClass(), "getCapitalCity");
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-96>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-97>)    // Create LlmAgent and Assign Callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-98>)    LlmAgent myLlmAgent =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-99>)        LlmAgent.builder()
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-100>)            .name(APP_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-101>)            .model(MODEL_NAME)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-102>)            .instruction(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-103>)                "You are an agent that finds capital cities using the getCapitalCity tool. Report"
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-104>)                    + " the result clearly.")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-105>)            .description("An LLM agent demonstrating after_tool_callback")
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-106>)            .tools(capitalTool) // Add the tool
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-107>)            .afterToolCallback(this::simpleAfterToolModifier) // Assign the callback
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-108>)            .build();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-109>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-110>)    InMemoryRunner runner = new InMemoryRunner(myLlmAgent);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-111>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-112>)    // Session and Runner
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-113>)    Session session =
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-114>)        runner.sessionService().createSession(APP_NAME, USER_ID, null, SESSION_ID).blockingGet();
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-115>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-116>)    Content userMessage = Content.fromParts(Part.fromText(query));
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-117>)
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-118>)    System.out.printf("%n--- Calling agent with query: \"%s\" ---%n", query);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-119>)    Flowable<Event> eventStream = runner.runAsync(USER_ID, session.id(), userMessage);
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-120>)    // Stream event response
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-121>)    eventStream.blockingForEach(
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-122>)        event -> {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-123>)          if (event.finalResponse()) {
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-124>)            System.out.println(event.stringifyContent());
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-125>)          }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-126>)        });
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-127>)  }
    [](<https://adk.dev/callbacks/types-of-callbacks/#__codelineno-24-128>)}
    
Back to top 