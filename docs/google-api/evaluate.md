# Why evaluate agents - Agent Development Kit (ADK)

> Source: [https://adk.dev/evaluate/](https://adk.dev/evaluate/)

[ Skip to content ](<https://adk.dev/evaluate/#why-evaluate-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/evaluate/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/evaluate/index.md> "View this page as Markdown")

# Why evaluate agents[¶](<https://adk.dev/evaluate/#why-evaluate-agents> "Permanent link")

Supported in ADKPython

In traditional software development, unit tests and integration tests provide confidence that code functions as expected and remains stable through changes. These tests provide a clear "pass/fail" signal, guiding further development. However, LLM agents introduce a level of variability that makes traditional testing approaches insufficient.

Due to the probabilistic nature of models, deterministic "pass/fail" assertions are often unsuitable for evaluating agent performance. Instead, we need qualitative evaluations of both the final output and the agent's trajectory - the sequence of steps taken to reach the solution. This involves assessing the quality of the agent's decisions, its reasoning process, and the final result.

This may seem like a lot of extra work to set up, but the investment of automating evaluations pays off quickly. If you intend to progress beyond prototype, this is a highly recommended best practice.

![intro_components.png](https://adk.dev/assets/evaluate_agent.png)

## Prepare for agent evaluations[¶](<https://adk.dev/evaluate/#prepare-for-agent-evaluations> "Permanent link")

Before automating agent evaluations, define clear objectives and success criteria:

  * **Define Success:** What constitutes a successful outcome for your agent?
  * **Identify Critical Tasks:** What are the essential tasks your agent must accomplish?
  * **Choose Relevant Metrics:** What metrics will you track to measure performance?

These considerations will guide the creation of evaluation scenarios and enable effective monitoring of agent behavior in real-world deployments.

## What to evaluate?[¶](<https://adk.dev/evaluate/#what-to-evaluate> "Permanent link")

To bridge the gap between a proof-of-concept and a production-ready AI agent, a robust and automated evaluation framework is essential. Unlike evaluating generative models, where the focus is primarily on the final output, agent evaluation requires a deeper understanding of the decision-making process. Agent evaluation can be broken down into two components:

  1. **Evaluate Trajectory and Tool Use:** Analyzing the steps an agent takes to reach a solution, including its choice of tools, strategies, and the efficiency of its approach.
  2. **Evaluate the Final Response:** Assessing the quality, relevance, and correctness of the agent's final output.

The trajectory is just a list of steps the agent took before it returned to the user. We can compare that against the list of steps we expect the agent to have taken.

### Evaluate trajectory and tool use[¶](<https://adk.dev/evaluate/#evaluate-trajectory-and-tool-use> "Permanent link")

Before responding to a user, an agent typically performs a series of actions, which we refer to as a 'trajectory.' It might compare the user input with session history to disambiguate a term, or lookup a policy document, search a knowledge base or invoke an API to save a ticket. We call this a ‘trajectory’ of actions. Evaluating an agent's performance requires comparing its actual trajectory to an expected, or ideal, one. This comparison can reveal errors and inefficiencies in the agent's process. The expected trajectory represents the ground truth -- the list of steps we anticipate the agent should take.

For example:
    
    [](<https://adk.dev/evaluate/#__codelineno-0-1>)# Trajectory evaluation will compare
    [](<https://adk.dev/evaluate/#__codelineno-0-2>)expected_steps = ["determine_intent", "use_tool", "review_results", "report_generation"]
    [](<https://adk.dev/evaluate/#__codelineno-0-3>)actual_steps = ["determine_intent", "use_tool", "review_results", "report_generation"]
    
ADK provides both groundtruth based and rubric based tool use evaluation metrics. To select the appropriate metric for your agent's specific requirements and goals, please refer to our [recommendations](<https://adk.dev/evaluate/#recommendations-on-criteria>).

## How evaluation works with ADK[¶](<https://adk.dev/evaluate/#how-evaluation-works-with-adk> "Permanent link")

ADK offers two methods for evaluating agent performance against predefined datasets and evaluation criteria. While conceptually similar, they differ in the amount of data they can process, which typically dictates the appropriate use case for each.

### Evaluate with test files[¶](<https://adk.dev/evaluate/#evaluate-with-test-files> "Permanent link")

This approach involves creating individual test files, each representing a single, simple agent-model interaction (a session). It's most effective during active agent development, serving as a form of unit testing. These tests are designed for rapid execution and should focus on simple session complexity. Each test file contains a single session, which may consist of multiple turns. A turn represents a single interaction between the user and the agent. Each turn includes

  * `User Content`: The user issued query.
  * `Expected Intermediate Tool Use Trajectory`: The tool calls we expect the agent to make in order to respond correctly to the user query.
  * `Expected Intermediate Agent Responses`: These are the natural language responses that the agent (or sub-agents) generates as it moves towards generating a final answer. These natural language responses are usually an artifact of an multi-agent system, where your root agent depends on sub-agents to achieve a goal. These intermediate responses, may or may not be of interest to the end user, but for a developer/owner of the system, are of critical importance, as they give you the confidence that the agent went through the right path to generate final response.
  * `Final Response`: The expected final response from the agent.

You can give the file any name for example `evaluation.test.json`. The framework only checks for the `.test.json` suffix, and the preceding part of the filename is not constrained. The test files are backed by a formal Pydantic data model. The two key schema files are [Eval Set](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py>) and [Eval Case](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_case.py>). Here is a test file with a few examples:

Note

Comments are included for explanatory purposes and should be removed for the JSON to be valid.
    
    [](<https://adk.dev/evaluate/#__codelineno-1-1>)# Do note that some fields are removed for sake of making this doc readable.
    [](<https://adk.dev/evaluate/#__codelineno-1-2>){
    [](<https://adk.dev/evaluate/#__codelineno-1-3>)  "eval_set_id": "home_automation_agent_light_on_off_set",
    [](<https://adk.dev/evaluate/#__codelineno-1-4>)  "name": "",
    [](<https://adk.dev/evaluate/#__codelineno-1-5>)  "description": "This is an eval set that is used for unit testing `x` behavior of the Agent",
    [](<https://adk.dev/evaluate/#__codelineno-1-6>)  "eval_cases": [
    [](<https://adk.dev/evaluate/#__codelineno-1-7>)    {
    [](<https://adk.dev/evaluate/#__codelineno-1-8>)      "eval_id": "eval_case_id",
    [](<https://adk.dev/evaluate/#__codelineno-1-9>)      "conversation": [
    [](<https://adk.dev/evaluate/#__codelineno-1-10>)        {
    [](<https://adk.dev/evaluate/#__codelineno-1-11>)          "invocation_id": "b7982664-0ab6-47cc-ab13-326656afdf75", # Unique identifier for the invocation.
    [](<https://adk.dev/evaluate/#__codelineno-1-12>)          "user_content": { # Content provided by the user in this invocation. This is the query.
    [](<https://adk.dev/evaluate/#__codelineno-1-13>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-1-14>)              {
    [](<https://adk.dev/evaluate/#__codelineno-1-15>)                "text": "Turn off device_2 in the Bedroom."
    [](<https://adk.dev/evaluate/#__codelineno-1-16>)              }
    [](<https://adk.dev/evaluate/#__codelineno-1-17>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-1-18>)            "role": "user"
    [](<https://adk.dev/evaluate/#__codelineno-1-19>)          },
    [](<https://adk.dev/evaluate/#__codelineno-1-20>)          "final_response": { # Final response from the agent that acts as a reference of benchmark.
    [](<https://adk.dev/evaluate/#__codelineno-1-21>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-1-22>)              {
    [](<https://adk.dev/evaluate/#__codelineno-1-23>)                "text": "I have set the device_2 status to off."
    [](<https://adk.dev/evaluate/#__codelineno-1-24>)              }
    [](<https://adk.dev/evaluate/#__codelineno-1-25>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-1-26>)            "role": "model"
    [](<https://adk.dev/evaluate/#__codelineno-1-27>)          },
    [](<https://adk.dev/evaluate/#__codelineno-1-28>)          "intermediate_data": {
    [](<https://adk.dev/evaluate/#__codelineno-1-29>)            "tool_uses": [ # Tool use trajectory in chronological order.
    [](<https://adk.dev/evaluate/#__codelineno-1-30>)              {
    [](<https://adk.dev/evaluate/#__codelineno-1-31>)                "args": {
    [](<https://adk.dev/evaluate/#__codelineno-1-32>)                  "location": "Bedroom",
    [](<https://adk.dev/evaluate/#__codelineno-1-33>)                  "device_id": "device_2",
    [](<https://adk.dev/evaluate/#__codelineno-1-34>)                  "status": "OFF"
    [](<https://adk.dev/evaluate/#__codelineno-1-35>)                },
    [](<https://adk.dev/evaluate/#__codelineno-1-36>)                "name": "set_device_info"
    [](<https://adk.dev/evaluate/#__codelineno-1-37>)              }
    [](<https://adk.dev/evaluate/#__codelineno-1-38>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-1-39>)            "intermediate_responses": [] # Any intermediate sub-agent responses.
    [](<https://adk.dev/evaluate/#__codelineno-1-40>)          }
    [](<https://adk.dev/evaluate/#__codelineno-1-41>)        }
    [](<https://adk.dev/evaluate/#__codelineno-1-42>)      ],
    [](<https://adk.dev/evaluate/#__codelineno-1-43>)      "session_input": { # Initial session input.
    [](<https://adk.dev/evaluate/#__codelineno-1-44>)        "app_name": "home_automation_agent",
    [](<https://adk.dev/evaluate/#__codelineno-1-45>)        "user_id": "test_user",
    [](<https://adk.dev/evaluate/#__codelineno-1-46>)        "state": {}
    [](<https://adk.dev/evaluate/#__codelineno-1-47>)      }
    [](<https://adk.dev/evaluate/#__codelineno-1-48>)    }
    [](<https://adk.dev/evaluate/#__codelineno-1-49>)  ]
    [](<https://adk.dev/evaluate/#__codelineno-1-50>)}
    
Test files can be organized into folders. Optionally, a folder can also include a `test_config.json` file that specifies the evaluation criteria.

#### How to migrate test files not backed by the Pydantic schema?[¶](<https://adk.dev/evaluate/#how-to-migrate-test-files-not-backed-by-the-pydantic-schema> "Permanent link")

Note

If your test files don't adhere to [EvalSet](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py>) schema file, then this section is relevant to you.

Please use `AgentEvaluator.migrate_eval_data_to_new_schema` to migrate your existing `*.test.json` files to the Pydantic backed schema.

The utility takes your current test data file and an optional initial session file, and generates a single output json file with data serialized in the new format. Given that the new schema is more cohesive, both the old test data file and initial session file can be ignored (or removed.)

### Evaluate with an Evalset File[¶](<https://adk.dev/evaluate/#evaluate-with-an-evalset-file> "Permanent link")

The evalset approach utilizes a dedicated dataset called an "evalset" for evaluating agent-model interactions. Similar to a test file, the evalset contains example interactions. However, an evalset can contain multiple, potentially lengthy sessions, making it ideal for simulating complex, multi-turn conversations. Due to its ability to represent complex sessions, the evalset is well-suited for integration tests. These tests are typically run less frequently than unit tests due to their more extensive nature.

An evalset file contains multiple "evals," each representing a distinct session. Each eval consists of one or more "turns," which include the user query, expected tool use, expected intermediate agent responses, and a reference response. These fields have the same meaning as they do in the test file approach. Alternatively, an eval can define a _conversation scenario_ which is used to [dynamically simulate](<https://adk.dev/evaluate/user-sim/>) a user interaction with the agent. Each eval is identified by a unique name. Furthermore, each eval includes an associated initial session state.

Creating evalsets manually can be complex, therefore UI tools are provided to help capture relevant sessions and easily convert them into evals within your evalset. Learn more about using the web UI for evaluation below. Here is an example evalset containing two sessions. The eval set files are backed by a formal Pydantic data model. The two key schema files are [Eval Set](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py>) and [Eval Case](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_case.py>).

Note

Comments are included for explanatory purposes and should be removed for the JSON to be valid.
    
    [](<https://adk.dev/evaluate/#__codelineno-2-1>)# Do note that some fields are removed for sake of making this doc readable.
    [](<https://adk.dev/evaluate/#__codelineno-2-2>){
    [](<https://adk.dev/evaluate/#__codelineno-2-3>)  "eval_set_id": "eval_set_example_with_multiple_sessions",
    [](<https://adk.dev/evaluate/#__codelineno-2-4>)  "name": "Eval set with multiple sessions",
    [](<https://adk.dev/evaluate/#__codelineno-2-5>)  "description": "This eval set is an example that shows that an eval set can have more than one session.",
    [](<https://adk.dev/evaluate/#__codelineno-2-6>)  "eval_cases": [
    [](<https://adk.dev/evaluate/#__codelineno-2-7>)    {
    [](<https://adk.dev/evaluate/#__codelineno-2-8>)      "eval_id": "session_01",
    [](<https://adk.dev/evaluate/#__codelineno-2-9>)      "conversation": [
    [](<https://adk.dev/evaluate/#__codelineno-2-10>)        {
    [](<https://adk.dev/evaluate/#__codelineno-2-11>)          "invocation_id": "e-0067f6c4-ac27-4f24-81d7-3ab994c28768",
    [](<https://adk.dev/evaluate/#__codelineno-2-12>)          "user_content": {
    [](<https://adk.dev/evaluate/#__codelineno-2-13>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-2-14>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-15>)                "text": "What can you do?"
    [](<https://adk.dev/evaluate/#__codelineno-2-16>)              }
    [](<https://adk.dev/evaluate/#__codelineno-2-17>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-2-18>)            "role": "user"
    [](<https://adk.dev/evaluate/#__codelineno-2-19>)          },
    [](<https://adk.dev/evaluate/#__codelineno-2-20>)          "final_response": {
    [](<https://adk.dev/evaluate/#__codelineno-2-21>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-2-22>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-23>)
    [](<https://adk.dev/evaluate/#__codelineno-2-24>)                "text": "I can roll dice of different sizes and check if numbers are prime."
    [](<https://adk.dev/evaluate/#__codelineno-2-25>)              }
    [](<https://adk.dev/evaluate/#__codelineno-2-26>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-2-27>)            "role": null
    [](<https://adk.dev/evaluate/#__codelineno-2-28>)          },
    [](<https://adk.dev/evaluate/#__codelineno-2-29>)          "intermediate_data": {
    [](<https://adk.dev/evaluate/#__codelineno-2-30>)            "tool_uses": [],
    [](<https://adk.dev/evaluate/#__codelineno-2-31>)            "intermediate_responses": []
    [](<https://adk.dev/evaluate/#__codelineno-2-32>)          }
    [](<https://adk.dev/evaluate/#__codelineno-2-33>)        }
    [](<https://adk.dev/evaluate/#__codelineno-2-34>)      ],
    [](<https://adk.dev/evaluate/#__codelineno-2-35>)      "session_input": {
    [](<https://adk.dev/evaluate/#__codelineno-2-36>)        "app_name": "hello_world",
    [](<https://adk.dev/evaluate/#__codelineno-2-37>)        "user_id": "user",
    [](<https://adk.dev/evaluate/#__codelineno-2-38>)        "state": {}
    [](<https://adk.dev/evaluate/#__codelineno-2-39>)      }
    [](<https://adk.dev/evaluate/#__codelineno-2-40>)    },
    [](<https://adk.dev/evaluate/#__codelineno-2-41>)    {
    [](<https://adk.dev/evaluate/#__codelineno-2-42>)      "eval_id": "session_02",
    [](<https://adk.dev/evaluate/#__codelineno-2-43>)      "conversation": [
    [](<https://adk.dev/evaluate/#__codelineno-2-44>)        {
    [](<https://adk.dev/evaluate/#__codelineno-2-45>)          "invocation_id": "e-92d34c6d-0a1b-452a-ba90-33af2838647a",
    [](<https://adk.dev/evaluate/#__codelineno-2-46>)          "user_content": {
    [](<https://adk.dev/evaluate/#__codelineno-2-47>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-2-48>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-49>)                "text": "Roll a 19 sided dice"
    [](<https://adk.dev/evaluate/#__codelineno-2-50>)              }
    [](<https://adk.dev/evaluate/#__codelineno-2-51>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-2-52>)            "role": "user"
    [](<https://adk.dev/evaluate/#__codelineno-2-53>)          },
    [](<https://adk.dev/evaluate/#__codelineno-2-54>)          "final_response": {
    [](<https://adk.dev/evaluate/#__codelineno-2-55>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-2-56>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-57>)                "text": "I rolled a 17."
    [](<https://adk.dev/evaluate/#__codelineno-2-58>)              }
    [](<https://adk.dev/evaluate/#__codelineno-2-59>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-2-60>)            "role": null
    [](<https://adk.dev/evaluate/#__codelineno-2-61>)          },
    [](<https://adk.dev/evaluate/#__codelineno-2-62>)          "intermediate_data": {
    [](<https://adk.dev/evaluate/#__codelineno-2-63>)            "tool_uses": [],
    [](<https://adk.dev/evaluate/#__codelineno-2-64>)            "intermediate_responses": []
    [](<https://adk.dev/evaluate/#__codelineno-2-65>)          }
    [](<https://adk.dev/evaluate/#__codelineno-2-66>)        },
    [](<https://adk.dev/evaluate/#__codelineno-2-67>)        {
    [](<https://adk.dev/evaluate/#__codelineno-2-68>)          "invocation_id": "e-bf8549a1-2a61-4ecc-a4ee-4efbbf25a8ea",
    [](<https://adk.dev/evaluate/#__codelineno-2-69>)          "user_content": {
    [](<https://adk.dev/evaluate/#__codelineno-2-70>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-2-71>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-72>)                "text": "Roll a 10 sided dice twice and then check if 9 is a prime or not"
    [](<https://adk.dev/evaluate/#__codelineno-2-73>)              }
    [](<https://adk.dev/evaluate/#__codelineno-2-74>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-2-75>)            "role": "user"
    [](<https://adk.dev/evaluate/#__codelineno-2-76>)          },
    [](<https://adk.dev/evaluate/#__codelineno-2-77>)          "final_response": {
    [](<https://adk.dev/evaluate/#__codelineno-2-78>)            "parts": [
    [](<https://adk.dev/evaluate/#__codelineno-2-79>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-80>)                "text": "I got 4 and 7 from the dice roll, and 9 is not a prime number.\n"
    [](<https://adk.dev/evaluate/#__codelineno-2-81>)              }
    [](<https://adk.dev/evaluate/#__codelineno-2-82>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-2-83>)            "role": null
    [](<https://adk.dev/evaluate/#__codelineno-2-84>)          },
    [](<https://adk.dev/evaluate/#__codelineno-2-85>)          "intermediate_data": {
    [](<https://adk.dev/evaluate/#__codelineno-2-86>)            "tool_uses": [
    [](<https://adk.dev/evaluate/#__codelineno-2-87>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-88>)                "id": "adk-1a3f5a01-1782-4530-949f-07cf53fc6f05",
    [](<https://adk.dev/evaluate/#__codelineno-2-89>)                "args": {
    [](<https://adk.dev/evaluate/#__codelineno-2-90>)                  "sides": 10
    [](<https://adk.dev/evaluate/#__codelineno-2-91>)                },
    [](<https://adk.dev/evaluate/#__codelineno-2-92>)                "name": "roll_die"
    [](<https://adk.dev/evaluate/#__codelineno-2-93>)              },
    [](<https://adk.dev/evaluate/#__codelineno-2-94>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-95>)                "id": "adk-52fc3269-caaf-41c3-833d-511e454c7058",
    [](<https://adk.dev/evaluate/#__codelineno-2-96>)                "args": {
    [](<https://adk.dev/evaluate/#__codelineno-2-97>)                  "sides": 10
    [](<https://adk.dev/evaluate/#__codelineno-2-98>)                },
    [](<https://adk.dev/evaluate/#__codelineno-2-99>)                "name": "roll_die"
    [](<https://adk.dev/evaluate/#__codelineno-2-100>)              },
    [](<https://adk.dev/evaluate/#__codelineno-2-101>)              {
    [](<https://adk.dev/evaluate/#__codelineno-2-102>)                "id": "adk-5274768e-9ec5-4915-b6cf-f5d7f0387056",
    [](<https://adk.dev/evaluate/#__codelineno-2-103>)                "args": {
    [](<https://adk.dev/evaluate/#__codelineno-2-104>)                  "nums": [
    [](<https://adk.dev/evaluate/#__codelineno-2-105>)                    9
    [](<https://adk.dev/evaluate/#__codelineno-2-106>)                  ]
    [](<https://adk.dev/evaluate/#__codelineno-2-107>)                },
    [](<https://adk.dev/evaluate/#__codelineno-2-108>)                "name": "check_prime"
    [](<https://adk.dev/evaluate/#__codelineno-2-109>)              }
    [](<https://adk.dev/evaluate/#__codelineno-2-110>)            ],
    [](<https://adk.dev/evaluate/#__codelineno-2-111>)            "intermediate_responses": [
    [](<https://adk.dev/evaluate/#__codelineno-2-112>)              [
    [](<https://adk.dev/evaluate/#__codelineno-2-113>)                "data_processing_agent",
    [](<https://adk.dev/evaluate/#__codelineno-2-114>)                [
    [](<https://adk.dev/evaluate/#__codelineno-2-115>)                  {
    [](<https://adk.dev/evaluate/#__codelineno-2-116>)                    "text": "I have rolled a 10 sided die twice. The first roll is 5 and the second roll is 3.\n"
    [](<https://adk.dev/evaluate/#__codelineno-2-117>)                  }
    [](<https://adk.dev/evaluate/#__codelineno-2-118>)                ]
    [](<https://adk.dev/evaluate/#__codelineno-2-119>)              ]
    [](<https://adk.dev/evaluate/#__codelineno-2-120>)            ]
    [](<https://adk.dev/evaluate/#__codelineno-2-121>)          }
    [](<https://adk.dev/evaluate/#__codelineno-2-122>)        }
    [](<https://adk.dev/evaluate/#__codelineno-2-123>)      ],
    [](<https://adk.dev/evaluate/#__codelineno-2-124>)      "session_input": {
    [](<https://adk.dev/evaluate/#__codelineno-2-125>)        "app_name": "hello_world",
    [](<https://adk.dev/evaluate/#__codelineno-2-126>)        "user_id": "user",
    [](<https://adk.dev/evaluate/#__codelineno-2-127>)        "state": {}
    [](<https://adk.dev/evaluate/#__codelineno-2-128>)      }
    [](<https://adk.dev/evaluate/#__codelineno-2-129>)    }
    [](<https://adk.dev/evaluate/#__codelineno-2-130>)  ]
    [](<https://adk.dev/evaluate/#__codelineno-2-131>)}
    
#### How to migrate eval set files not backed by the Pydantic schema?[¶](<https://adk.dev/evaluate/#how-to-migrate-eval-set-files-not-backed-by-the-pydantic-schema> "Permanent link")

Note

If your eval set files don't adhere to [EvalSet](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_set.py>) schema file, then this section is relevant to you.

Based on who is maintaining the eval set data, there are two routes:

  1. **Eval set data maintained by ADK UI** If you use ADK UI to maintain your Eval set data then _no action is needed_ from you.

  2. **Eval set data is developed and maintained manually and used in ADK eval CLI** A migration tool is in the works, until then the ADK eval CLI command will continue to support data in the old format.

### Evaluate with conformance testing[¶](<https://adk.dev/evaluate/#evaluate-with-conformance-testing> "Permanent link")

`adk conformance test` command verifies that your AI agents behave consistently over time. It ensures that updates to your codebase or models don't introduce regressions by validating current agent outputs against baseline data.

#### Prerequisites and setup[¶](<https://adk.dev/evaluate/#prerequisites-and-setup> "Permanent link")

Before the `adk conformance` command can execute meaningful regression testing, you must establish an optimal "golden baseline." Conformance testing operates by comparing live agent behavior against these previously recorded, verified interactions.

Follow this workflow to prepare your environment:

##### Create the Test Directory Hierarchy[¶](<https://adk.dev/evaluate/#create-the-test-directory-hierarchy> "Permanent link")

Conformance tests rely on a strict file layout to automatically discover and map test cases. Initialize your testing directory using the following structure:
    
    [](<https://adk.dev/evaluate/#__codelineno-3-1>)tests
    [](<https://adk.dev/evaluate/#__codelineno-3-2>)└── category_name/
    [](<https://adk.dev/evaluate/#__codelineno-3-3>)    └── test_case_name/
    [](<https://adk.dev/evaluate/#__codelineno-3-4>)        ├── spec.yaml                  # Test case specification
    [](<https://adk.dev/evaluate/#__codelineno-3-5>)        ├── generated-recordings.yaml   # Baseline recorded interactions
    [](<https://adk.dev/evaluate/#__codelineno-3-6>)        └── generated-session.yaml      # Baseline session data
    
Note

If your agent uses Server-Sent Events (SSE), the testing framework will additionally look for `generated-recordings-sse.yaml` and `generated-session-sse.yaml` within the same folder.

##### Define the test specification (spec.yaml)[¶](<https://adk.dev/evaluate/#define-the-test-specification-specyaml> "Permanent link")

In your target test folder, create a `spec.yaml` file. This file outlines the initial conditions, configurations, and user prompts that the agent will execute during the baseline recording and subsequent conformance runs. Ensure your file matches the following basic schema, this is an example only:
    
    [](<https://adk.dev/evaluate/#__codelineno-4-1>)# Example spec.yaml for a Weather Agent name: "current_weather_check" description:
    [](<https://adk.dev/evaluate/#__codelineno-4-2>)"Verifies the agent correctly identifies location and calls the weather tool."
    [](<https://adk.dev/evaluate/#__codelineno-4-3>)user_prompts: - "What's the temperature in San Francisco right now?" expected_tools:
    [](<https://adk.dev/evaluate/#__codelineno-4-4>) - "get_weather_api"
    
#### Automate the baseline[¶](<https://adk.dev/evaluate/#automate-the-baseline> "Permanent link")

Because the background data (like LLM requests and tool calls) is complex, you shouldn't try to write or save the baseline files manually. Instead, let ADK generate them for you.

  1. Start your ADK web server with the recording plugin turned on:

    [](<https://adk.dev/evaluate/#__codelineno-5-1>)adk web -v --extra_plugins=google.adk.cli.plugins.recordings_plugin.RecordingsPlugin /path/to/agents
    
  1. Next, open a new terminal window and tell ADK to create the baseline files based on your spec.yaml:

    [](<https://adk.dev/evaluate/#__codelineno-6-1>)adk conformance create tests/category/test_name
    
This automatically runs the scenario, records all the interactions, and saves the generated-recordings.yaml and generated-session.yaml files exactly where they need to be.

Once these baseline files are locked in, your setup is complete, and the directory is ready to be targeted by `adk conformance` in either **Replay** or **Live** mode.

#### How it works[¶](<https://adk.dev/evaluate/#how-it-works> "Permanent link")

  * **Replay Mode (Default):** The tool runs your agent and compares its live LLM requests, responses, and tool calls directly against your previously recorded interactions to catch unexpected deviations.
  * **Live Mode:** Runs evaluation-based verification against active environments _(Note: This mode is a work in progress)_.

### Evaluation criteria[¶](<https://adk.dev/evaluate/#evaluation-criteria> "Permanent link")

ADK provides several built-in criteria for evaluating agent performance, ranging from tool trajectory matching to LLM-based response quality assessment. For a detailed list of available criteria and guidance on when to use them, please see [Evaluation Criteria](<https://adk.dev/evaluate/criteria/>).

Here is a summary of all the available criteria:

  * **tool_trajectory_avg_score** : Exact match of tool call trajectory.
  * **response_match_score** : ROUGE-1 similarity to reference response.
  * **final_response_match_v2** : LLM-judged semantic match to a reference response.
  * **rubric_based_final_response_quality_v1** : LLM-judged final response quality based on custom rubrics.
  * **rubric_based_tool_use_quality_v1** : LLM-judged tool usage quality based on custom rubrics.
  * **hallucinations_v1** : LLM-judged groundedness of agent response against context.
  * **safety_v1** : Safety/harmlessness of agent response.
  * **per_turn_user_simulator_quality_v1** : LLM-judged user simulator quality.
  * **multi_turn_task_success_v1** : Evaluates if agent achieves goal(s) of conversation.
  * **multi_turn_trajectory_quality_v1** : Evaluates the overall trajectory of the conversation.
  * **multi_turn_tool_use_quality_v1** : Evaluates function calls made during a conversation.

Note

Some criteria (such as response quality, safety, and multi-turn quality) require the [Vertex Gen AI Evaluation Service API](<https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/evaluation>). To use them, authenticate by setting a `GOOGLE_API_KEY` environment variable, or by using Google Cloud project credentials (`GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` with Application Default Credentials).

If no evaluation criteria are provided, the following default configuration is used:

  * `tool_trajectory_avg_score`: Defaults to 1.0, requiring a 100% match in the tool usage trajectory.
  * `response_match_score`: Defaults to 0.8, allowing for a small margin of error in the agent's natural language responses.

Here is an example of a `test_config.json` file specifying custom evaluation criteria:
    
    [](<https://adk.dev/evaluate/#__codelineno-7-1>){
    [](<https://adk.dev/evaluate/#__codelineno-7-2>)  "criteria": {
    [](<https://adk.dev/evaluate/#__codelineno-7-3>)    "tool_trajectory_avg_score": 1.0,
    [](<https://adk.dev/evaluate/#__codelineno-7-4>)    "response_match_score": 0.8
    [](<https://adk.dev/evaluate/#__codelineno-7-5>)  }
    [](<https://adk.dev/evaluate/#__codelineno-7-6>)}
    
#### Recommendations on criteria[¶](<https://adk.dev/evaluate/#recommendations-on-criteria> "Permanent link")

Choose criteria based on your evaluation goals:

  * **Enable tests in CI/CD pipelines or regression testing:** Use `tool_trajectory_avg_score` and `response_match_score`. These criteria are fast, predictable, and suitable for frequent automated checks.
  * **Evaluate trusted reference responses:** Use `final_response_match_v2` to evaluate semantic equivalence. This LLM-based check is more flexible than exact matching and better captures whether the agent's response means the same thing as the reference response.
  * **Evaluate response quality without a reference response:** Use `rubric_based_final_response_quality_v1`. This is useful when you don't have a trusted reference, but you can define attributes of a good response (e.g., "The response is concise," "The response has a helpful tone").
  * **Evaluate the correctness of tool usage:** Use `rubric_based_tool_use_quality_v1`. This allows you to validate the agent's reasoning process by checking, for example, that a specific tool was called or that tools were called in the correct order (e.g., "Tool A must be called before Tool B").
  * **Check if responses are grounded in context:** Use `hallucinations_v1` to detect if the agent makes claims that are unsupported by or contradictory to the information available to it (e.g., tool outputs).
  * **Check for harmful content:** Use `safety_v1` to ensure that agent responses are safe and do not violate safety policies.
  * **Evaluate multi-turn goal completion:** Use `multi_turn_task_success_v1` to measure the overall success of a multi-turn conversation in achieving its intended objectives.
  * **Evaluate overall conversation trajectory:** Use `multi_turn_trajectory_quality_v1` to assess the efficiency, effectiveness, and logic of the steps taken during the conversation.
  * **Evaluate tool usage in multi-turn workflows:** Use `multi_turn_tool_use_quality_v1` to assess the quality, relevance, and correctness of tool or function calls made across multiple turns.

In addition, criteria which require information on expected agent tool use and/or responses are not supported in combination with [User Simulation](<https://adk.dev/evaluate/user-sim/>). Currently, only the `hallucinations_v1` and `safety_v1` criteria support such evals.

### User simulation[¶](<https://adk.dev/evaluate/#user-simulation> "Permanent link")

When evaluating conversational agents, it is not always practical to use a fixed set of user prompts, as the conversation can proceed in unexpected ways. For example, if the agent needs the user to supply two values to perform a task, it may ask for those values one at a time or both at once. To resolve this issue, ADK allows you test the behavior of the agent in a specific _conversation scenario_ with user prompts that are dynamically generated by an AI model. For details on how to set up an eval with user simulation, see [User Simulation](<https://adk.dev/evaluate/user-sim/>).

## How to run evaluation with ADK[¶](<https://adk.dev/evaluate/#how-to-run-evaluation-with-adk> "Permanent link")

As a developer, you can evaluate your agents using the ADK in the following ways:

  * **Web-based UI (**`adk web`**):** Evaluate agents interactively through a web-based interface.
  * **Programmatically (**`pytest`**)** : Integrate evaluation into your testing pipeline using `pytest` and test files.
  * **Command Line Interface (**`adk eval`**):** Run evaluations on an existing evaluation set file directly from the command line.
  * **Conformance Testing** (**`adk conformance`**):** Execute automated tests against your baseline files to detect unexpected deviations or regressions.

### Run evaluations via the web UI[¶](<https://adk.dev/evaluate/#run-evaluations-via-the-web-ui> "Permanent link")

The web UI provides an interactive way to evaluate agents, generate evaluation datasets, and inspect agent behavior in detail.

#### Step 1: Create and save a test case[¶](<https://adk.dev/evaluate/#step-1-create-and-save-a-test-case> "Permanent link")

  1. Start the web server by running: `adk web <path_to_your_agents_folder>`
  2. In the web interface, select an agent and interact with it to create a session.
  3. Navigate to the **Eval** tab on the right side of the interface.
  4. Create a new eval set or select an existing one.
  5. Click **"Add current session"** to save the conversation as a new evaluation case.

#### Step 2: View and edit your test case[¶](<https://adk.dev/evaluate/#step-2-view-and-edit-your-test-case> "Permanent link")

Once a case is saved, you can click its ID in the list to inspect it. To make changes, click the **Edit current eval case** icon (pencil). This interactive view allows you to:

  * **Modify** agent text responses to refine test scenarios.
  * **Delete** individual agent messages from the conversation.
  * **Delete** the entire evaluation case if it's no longer needed.

![adk-eval-case.gif](https://adk.dev/assets/adk-eval-case.gif)

#### Step 3: Run the evaluation with custom metrics[¶](<https://adk.dev/evaluate/#step-3-run-the-evaluation-with-custom-metrics> "Permanent link")

  1. Select one or more test cases from your evalset.
  2. Click **Run Evaluation**. An **EVALUATION METRIC** dialog will appear.
  3. In the dialog, use the sliders to configure the thresholds for:
     * **Tool trajectory avg score**
     * **Response match score**
  4. Click **Start** to run the evaluation using your custom criteria. The evaluation history will record the metrics used for each run.

![adk-eval-config.gif](https://adk.dev/assets/adk-eval-config.gif)

#### Step 4: Analyze results[¶](<https://adk.dev/evaluate/#step-4-analyze-results> "Permanent link")

After the run completes, you can analyze the results:

  * **Analyze Run Failures** : Click on any **Pass** or **Fail** result. For failures, you can hover over the `Fail` label to see a side-by-side comparison of the **Actual vs. Expected Output** and the scores that caused the failure.

### Debugging with the Trace View[¶](<https://adk.dev/evaluate/#debugging-with-the-trace-view> "Permanent link")

ADK web UI includes a powerful **Trace** tab for debugging agent behavior. This feature is available for any agent session, not just during evaluation.

The **Trace** tab provides a detailed and interactive way to inspect your agent's execution flow. Traces are automatically grouped by user message, making it easy to follow the chain of events.

Each trace row is interactive:

  * **Hovering** over a trace row highlights the corresponding message in the chat window.
  * **Clicking** on a trace row opens a detailed inspection panel with four tabs:
    * **Event** : The raw event data.
    * **Request** : The request sent to the model.
    * **Response** : The response received from the model.
    * **Graph** : A visual representation of the tool calls and agent logic flow.

![adk-trace1.gif](https://adk.dev/assets/adk-trace1.gif) ![adk-trace2.gif](https://adk.dev/assets/adk-trace2.gif)

Blue rows in the trace view indicate that an event was generated from that interaction. Clicking on these blue rows will open the bottom event detail panel, providing deeper insights into the agent's execution flow.

### Run tests programmatically[¶](<https://adk.dev/evaluate/#run-tests-programmatically> "Permanent link")

You can also use **`pytest`** to run test files as part of your integration tests.

#### Example command[¶](<https://adk.dev/evaluate/#example-command> "Permanent link")
    
    [](<https://adk.dev/evaluate/#__codelineno-8-1>)pytest tests/integration/
    
#### Example test code[¶](<https://adk.dev/evaluate/#example-test-code> "Permanent link")

Here is an example of a `pytest` test case that runs a single test file:
    
    [](<https://adk.dev/evaluate/#__codelineno-9-1>)from google.adk.evaluation.agent_evaluator import AgentEvaluator
    [](<https://adk.dev/evaluate/#__codelineno-9-2>)import pytest
    [](<https://adk.dev/evaluate/#__codelineno-9-3>)
    [](<https://adk.dev/evaluate/#__codelineno-9-4>)@pytest.mark.asyncio
    [](<https://adk.dev/evaluate/#__codelineno-9-5>)async def test_with_single_test_file():
    [](<https://adk.dev/evaluate/#__codelineno-9-6>)    """Test the agent's basic ability via a session file."""
    [](<https://adk.dev/evaluate/#__codelineno-9-7>)    await AgentEvaluator.evaluate(
    [](<https://adk.dev/evaluate/#__codelineno-9-8>)        agent_module="home_automation_agent",
    [](<https://adk.dev/evaluate/#__codelineno-9-9>)        eval_dataset_file_path_or_dir="tests/integration/fixture/home_automation_agent/simple_test.test.json",
    [](<https://adk.dev/evaluate/#__codelineno-9-10>)    )
    
This approach allows you to integrate agent evaluations into your CI/CD pipelines or larger test suites. If you want to specify the initial session state for your tests, you can do that by storing the session details in a file and passing that to `AgentEvaluator.evaluate` method.

### Run evaluations via the CLI[¶](<https://adk.dev/evaluate/#run-evaluations-via-the-cli> "Permanent link")

You can also run evaluation of an eval set file through the command line interface (CLI). This runs the same evaluation that runs on the UI, but it helps with automation, i.e. you can add this command as a part of your regular build generation and verification process.

Here is the command:
    
    [](<https://adk.dev/evaluate/#__codelineno-10-1>)adk eval \
    [](<https://adk.dev/evaluate/#__codelineno-10-2>)    <AGENT_MODULE_FILE_PATH> \
    [](<https://adk.dev/evaluate/#__codelineno-10-3>)    <EVAL_SET_FILE_PATH> \
    [](<https://adk.dev/evaluate/#__codelineno-10-4>)    [--config_file_path=<PATH_TO_TEST_JSON_CONFIG_FILE>] \
    [](<https://adk.dev/evaluate/#__codelineno-10-5>)    [--print_detailed_results]
    
For example:
    
    [](<https://adk.dev/evaluate/#__codelineno-11-1>)adk eval \
    [](<https://adk.dev/evaluate/#__codelineno-11-2>)    samples_for_testing/hello_world \
    [](<https://adk.dev/evaluate/#__codelineno-11-3>)    samples_for_testing/hello_world/hello_world_eval_set_001.evalset.json
    
Here are the details for each command line argument:

  * `AGENT_MODULE_FILE_PATH`: The path to the `__init__.py` file that contains a module by the name "agent". "agent" module contains a `root_agent`.
  * `EVAL_SET_FILE_PATH`: The path to evaluations file(s). You can specify one or more eval set file paths. For each file, all evals will be run by default. If you want to run only specific evals from a eval set, first create a comma separated list of eval names and then add that as a suffix to the eval set file name, demarcated by a colon `:` .
  * For example: `sample_eval_set_file.json:eval_1,eval_2,eval_3` `This will only run eval_1, eval_2 and eval_3 from sample_eval_set_file.json`
  * `CONFIG_FILE_PATH`: The path to the config file.
  * `PRINT_DETAILED_RESULTS`: Prints detailed results on the console.

### Run conformance tests[¶](<https://adk.dev/evaluate/#run-conformance-tests> "Permanent link")

You can run all your tests at once, run specific ones, or create a summary report.

#### Run all tests[¶](<https://adk.dev/evaluate/#run-all-tests> "Permanent link")

If you don't type a specific folder path, the tool automatically looks for a tests/ folder in your workspace and runs everything inside it:
    
    [](<https://adk.dev/evaluate/#__codelineno-12-1>)adk conformance test
    
#### Run specific test groups or individual cases[¶](<https://adk.dev/evaluate/#run-specific-test-groups-or-individual-cases> "Permanent link")

Pass one or more folder paths to narrow down which tests execute:
    
    [](<https://adk.dev/evaluate/#__codelineno-13-1>)# Test an entire category of tests
    [](<https://adk.dev/evaluate/#__codelineno-13-2>)adk conformance test tests/core
    [](<https://adk.dev/evaluate/#__codelineno-13-3>)
    [](<https://adk.dev/evaluate/#__codelineno-13-4>)# Test one specific case
    [](<https://adk.dev/evaluate/#__codelineno-13-5>)adk conformance test tests/core/description_001
    
#### Generate Markdown test reports[¶](<https://adk.dev/evaluate/#generate-markdown-test-reports> "Permanent link")

Add the `--generate_report` flag to produce a clean test summary report. You can optionally specify where to save it using the `--report_dir parameter`:
    
    [](<https://adk.dev/evaluate/#__codelineno-14-1>)# Save the report in a specific folder
    [](<https://adk.dev/evaluate/#__codelineno-14-2>)adk conformance test --generate_report --report_dir=reports
    
#### Automate with CI/CD[¶](<https://adk.dev/evaluate/#automate-with-cicd> "Permanent link")

Because adk conformance test is a command-line tool that fails if things don't match, it is highly useful for CI/CD pipelines. You can set it up to run automatically whenever someone opens a pull request, blocking any code from merging if it changes the agent's expected behavior.

Back to top 