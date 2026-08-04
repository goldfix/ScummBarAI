# User Simulation - Agent Development Kit (ADK)

> Source: [https://adk.dev/evaluate/user-sim/](https://adk.dev/evaluate/user-sim/)

[ Skip to content ](<https://adk.dev/evaluate/user-sim/#user-simulation>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/evaluate/user-sim.md> "Edit this page on GitHub") [ ](<https://adk.dev/evaluate/user-sim/index.md> "View this page as Markdown")

# User simulation[¶](<https://adk.dev/evaluate/user-sim/#user-simulation> "Permanent link")

Supported in ADKPython v1.18.0

When evaluating conversational agents, it is not always practical to use a fixed set of user prompts, as the conversation can proceed in unexpected ways. For example, if the agent needs the user to supply two values to perform a task, it may ask for those values one at a time or both at once. To resolve this issue, ADK can dynamically generate user prompts using a generative AI model.

To use this feature, you must specify a [`ConversationScenario`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/conversation_scenarios.py>) which dictates the user's goals in their conversation with the agent. You may also specify a user persona that you expect the user to adhere to.

A `ConversationScenario` consists of the following components:

  * `starting_prompt`: A fixed initial prompt that the user should use to start the conversation with the agent.
  * `conversation_plan`: A high-level guideline for the goals the user must achieve.
  * `user_persona`: A definition of the user's traits, such as technical expertise or linguistic style.

A sample conversation scenario for the [`hello_world`](<https://github.com/google/adk-python/tree/main/contributing/samples/core/hello_world>) agent is shown below:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-0-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-0-2>)  "starting_prompt": "What can you do for me?",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-0-3>)  "conversation_plan": "Ask the agent to roll a 20-sided die. After you get the result, ask the agent to check if it is prime."
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-0-4>)}
    
The LLM uses the `conversation_plan`, along with the conversation history, to dynamically generate user prompts.

You can also specify a pre-built `user_persona` in the following manner:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-1-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-1-2>)  "starting_prompt": "What can you do for me?",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-1-3>)  "conversation_plan": "Ask the agent to roll a 20-sided die. After you get the result, ask the agent to check if it is prime.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-1-4>)  "user_persona": "NOVICE"
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-1-5>)}
    
While the conversation plan dictates what must be accomplished, the persona dictates how the model phrases its queries and reacts to the agent's responses.

## User personas[¶](<https://adk.dev/evaluate/user-sim/#user-personas> "Permanent link")

Supported in ADKPython v1.26.0

A User Persona is a role that the simulated user adopts during the conversation. It is defined by a set of **behaviors** that dictate how the user interacts with the agent, such as their communication style, how they provide information, and how they react to errors.

A `UserPersona` consists of the following fields:

  * `id`: A unique identifier for the persona.
  * `description`: A high-level description of who the user is and how they interact with the agent.
  * `behaviors`: A list of `UserBehavior` objects that define specific traits.

Each `UserBehavior` includes:

  * `name`: The name of the behavior.
  * `description`: A summary of the expected behavior.
  * `behavior_instructions`: Specific instructions given to the simulated user (LLM) on how to act.
  * `violation_rubrics`: Used by evaluators to determine whether the user is following this behavior. If **any** of these rubrics are **satisfied** , the evaluator should determine the behavior was **not** followed.

## Pre-built Personas[¶](<https://adk.dev/evaluate/user-sim/#pre-built-personas> "Permanent link")

ADK provides a set of pre-built personas composed of common behaviors. The table below summarizes the behaviors for each persona:

Behavior | **EXPERT** persona | **NOVICE** persona | **EVALUATOR** persona  
---|---|---|---  
**Advance** | Detail oriented (proactively provides details) | Goal oriented (waits to be asked for details) | Detail oriented  
**Answer** | Relevant questions only | Answer all questions | Relevant questions only  
**Correct Agent Inaccuracies** | Yes | No | No  
**Troubleshoot Agent Errors** | Once | Never | Never  
**Tone** | Professional | Conversational | Conversational  
  
## Example: Evaluate the [`hello_world`](<https://github.com/google/adk-python/tree/main/contributing/samples/core/hello_world>) agent with conversation scenarios[¶](<https://adk.dev/evaluate/user-sim/#example-evaluate-the-hello_world-agent-with-conversation-scenarios> "Permanent link")

To add evaluation cases containing conversation scenarios to a new or existing [`EvalSet`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py>), you need to first create a list of conversation scenarios to test the agent in.

Try saving the following to `contributing/samples/core/hello_world/conversation_scenarios.json`:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-2>)  "scenarios": [
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-3>)    {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-4>)      "starting_prompt": "What can you do for me?",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-5>)      "conversation_plan": "Ask the agent to roll a 20-sided die. After you get the result, ask the agent to check if it is prime.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-6>)      "user_persona": "NOVICE"
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-7>)    },
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-8>)    {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-9>)      "starting_prompt": "Hi, I'm running a tabletop RPG in which prime numbers are bad!",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-10>)      "conversation_plan": "Say that you don't care about the value; you just want the agent to tell you if a roll is good or bad. Once the agent agrees, ask it to roll a 6-sided die. Finally, ask the agent to do the same with 2 20-sided dice.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-11>)      "user_persona": "EXPERT"
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-12>)    }
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-13>)  ]
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-2-14>)}
    
You will also need a session input file containing information used during evaluation. Try saving the following to `contributing/samples/core/hello_world/session_input.json`:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-3-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-3-2>)  "app_name": "hello_world",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-3-3>)  "user_id": "user"
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-3-4>)}
    
Then, you can add the conversation scenarios to an `EvalSet`:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-1>)# (optional) create a new EvalSet
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-2>)adk eval_set create \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-3>)  contributing/samples/core/hello_world \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-4>)  eval_set_with_scenarios
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-5>)
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-6>)# add conversation scenarios to the EvalSet as new eval cases
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-7>)adk eval_set add_eval_case \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-8>)  contributing/samples/core/hello_world \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-9>)  eval_set_with_scenarios \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-10>)  --scenarios_file contributing/samples/core/hello_world/conversation_scenarios.json \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-4-11>)  --session_input_file contributing/samples/core/hello_world/session_input.json
    
By default, ADK runs evaluations with metrics that require the agent's expected response to be specified. Since that is not the case for a dynamic conversation scenario, we will use an [`EvalConfig`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_config.py>) with some alternate supported metrics.

Try saving the following to `contributing/samples/core/hello_world/eval_config.json`:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-2>)  "criteria": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-3>)    "hallucinations_v1": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-4>)      "threshold": 0.5,
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-5>)      "evaluate_intermediate_nl_responses": true
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-6>)    },
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-7>)    "safety_v1": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-8>)      "threshold": 0.8
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-9>)    }
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-10>)  }
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-5-11>)}
    
Finally, you can use the `adk eval` command to run the evaluation:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-6-1>)adk eval \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-6-2>)    contributing/samples/core/hello_world \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-6-3>)    --config_file_path contributing/samples/core/hello_world/eval_config.json \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-6-4>)    eval_set_with_scenarios \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-6-5>)    --print_detailed_results
    
## User simulator configuration[¶](<https://adk.dev/evaluate/user-sim/#user-simulator-configuration> "Permanent link")

You can override the default user simulator configuration to change the model, internal model behavior, and the maximum number of user-agent interactions. The below `EvalConfig` shows the default user simulator configuration:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-2>)  "criteria": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-3>)    # same as before
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-4>)  },
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-5>)  "user_simulator_config": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-6>)    "model": "gemini-flash-latest",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-7>)    "model_configuration": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-8>)      "thinking_config": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-9>)        "include_thoughts": true,
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-10>)        "thinking_budget": 10240
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-11>)      }
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-12>)    },
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-13>)    "max_allowed_invocations": 20
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-14>)  }
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-7-15>)}
    
  * `model`: The model backing the user simulator.
  * `model_configuration`: A [`GenerateContentConfig`](<https://github.com/googleapis/python-genai/blob/6196b1b4251007e33661bb5d7dc27bafee3feefe/google/genai/types.py#L4295>) which controls the model behavior.
  * `max_allowed_invocations`: The maximum user-agent interactions allowed before the conversation is forcefully terminated. This should be set to be greater than the longest reasonable user-agent interaction in your `EvalSet`.
  * `custom_instructions`: Optional. Overrides the default instructions for the user simulator. The instruction string must contain the following formatting placeholders using [Jinja](<https://jinja.palletsprojects.com/en/stable/templates/>) syntax (_do not substitute values in advance!_):
    * `{{ stop_signal }}` : text to be generated when the user simulator decides that the conversation is over.
    * `{{ conversation_plan }}` : the overall plan for the conversation that the user simulator must follow.
    * `{{ conversation_history }}` : the conversation between the user and the agent so far.
    * You can also access the `UserPersona` object through the `{{ persona }}` placeholder.

## Custom personas[¶](<https://adk.dev/evaluate/user-sim/#custom-personas> "Permanent link")

You can define your own custom persona by providing a `UserPersona` object in the `ConversationScenario`.

Example of a custom persona definition:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-2>)  "starting_prompt": "I need help with my account.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-3>)  "conversation_plan": "Ask the agent to reset your password.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-4>)  "user_persona": {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-5>)    "id": "IMPATIENT_USER",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-6>)    "description": "A user who is in a rush and gets easily frustrated.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-7>)    "behaviors": [
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-8>)      {
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-9>)        "name": "Short responses",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-10>)        "description": "The user should provide very short, sometimes incomplete responses.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-11>)        "behavior_instructions": [
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-12>)            "Keep your responses under 10 words.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-13>)            "Omit polite phrases."
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-14>)        ],
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-15>)        "violation_rubrics": [
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-16>)            "The user response is over 10 words.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-17>)            "The user response is overly polite."
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-18>)        ]
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-19>)      }
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-20>)    ]
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-21>)  }
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-8-22>)}
    
## Generate evaluation cases via user simulation[¶](<https://adk.dev/evaluate/user-sim/#generate-evaluation-cases-via-user-simulation> "Permanent link")

Writing evaluation cases manually can be time-consuming and may not cover all potential failure modes. ADK provides a command to automatically generate diverse and realistic conversation scenarios based on your agent's definition using the Agent Platform Eval SDK.

Prerequisites: Agent Platform Credentials

Generating evaluation cases uses the [Vertex Gen AI Evaluation Service API](<https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/evaluation-overview>). You must have a Google Cloud project with the Agent Platform API enabled and valid Application Default Credentials (ADC) configured in your environment.

### Command Syntax[¶](<https://adk.dev/evaluate/user-sim/#command-syntax> "Permanent link")
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-9-1>)adk eval_set generate_eval_cases \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-9-2>)    <AGENT_MODULE_FILE_PATH> \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-9-3>)    <EVAL_SET_ID> \
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-9-4>)    --user_simulation_config_file=<PATH_TO_CONFIG_FILE>
    
### Configuration File Format[¶](<https://adk.dev/evaluate/user-sim/#configuration-file-format> "Permanent link")

The `--user_simulation_config_file` expects a JSON file matching the `ConversationGenerationConfig` schema:
    
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-10-1>){
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-10-2>)  "count": 5,
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-10-3>)  "generation_instruction": "Generate scenarios where the user asks to control home devices under different conditions.",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-10-4>)  "environment_context": "Available devices: device_1 (Light), device_2 (Thermostat).",
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-10-5>)  "model_name": "gemini-flash-latest"
    [](<https://adk.dev/evaluate/user-sim/#__codelineno-10-6>)}
    
### Configuration Fields[¶](<https://adk.dev/evaluate/user-sim/#configuration-fields> "Permanent link")

  * **`count`** (required): The number of conversation scenarios to generate.
  * **`generation_instruction`** (optional): A natural language prompt guiding the specific types of scenarios or goals you want to test.
  * **`environment_context`** (optional): Context describing the backend data or state accessible to the agent's tools. This helps the generator create queries that are grounded in realistic data (e.g., valid device IDs).
  * **`model_name`** (required): The Gemini model used for generation (e.g., `gemini-flash-latest`).

Back to top 