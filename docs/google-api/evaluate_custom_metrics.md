# Custom Metrics - Agent Development Kit (ADK)

> Source: [https://adk.dev/evaluate/custom_metrics/](https://adk.dev/evaluate/custom_metrics/)

[ Skip to content ](<https://adk.dev/evaluate/custom_metrics/#custom-metrics-for-agent-evaluation>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/evaluate/custom_metrics.md> "Edit this page on GitHub") [ ](<https://adk.dev/evaluate/custom_metrics/index.md> "View this page as Markdown")

# Custom Metrics

## Custom Metrics for Agent Evaluation[¶](<https://adk.dev/evaluate/custom_metrics/#custom-metrics-for-agent-evaluation> "Permanent link")

Supported in ADKPython v1.18.0

If you require specialized metrics tailored to your specific use cases or domains that are not covered by built-in options, you can define your own custom metrics.

## Define a Custom Metric[¶](<https://adk.dev/evaluate/custom_metrics/#define-a-custom-metric> "Permanent link")

A custom metric is a Python function that evaluates an agent's performance on a given evaluation case and returns an [`EvaluationResult`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/evaluator.py>). The function receives the [`EvalMetric`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_metrics.py>), the list of [`Invocation`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_case.py>) objects produced by the agent during the evaluation run, and optionally, a list of expected invocations or a [`ConversationScenario`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_case.py>) as defined in the eval case.

Each `Invocation` object represents a single turn of interaction between the user and the agent, and contains information such as tool trajectory, intermediate responses, and final response for that turn.

Your custom metric function must have the following signature:
    
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-1>)from typing import Optional
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-2>)from google.adk.evaluation.eval_case import Invocation
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-3>)from google.adk.evaluation.eval_metrics import EvalMetric
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-4>)from google.adk.evaluation.conversation_scenarios import ConversationScenario
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-5>)from google.adk.evaluation.evaluator import EvaluationResult
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-6>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-7>)def my_custom_metric_function(
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-8>)    eval_metric: EvalMetric,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-9>)    actual_invocations: list[Invocation],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-10>)    expected_invocations: Optional[list[Invocation]],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-11>)    conversation_scenario: Optional[ConversationScenario],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-12>)) -> EvaluationResult:
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-0-13>)  ...
    
The function should return an `EvaluationResult` object with the `overall_score`, `overall_eval_status`, and `per_invocation_results` fields populated.

### Example[¶](<https://adk.dev/evaluate/custom_metrics/#example> "Permanent link")

Here is a simple example of a custom metric that checks if the agent's final response in each turn matches the expected final response exactly.
    
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-1>)import statistics
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-2>)from typing import Optional
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-3>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-4>)from google.adk.evaluation.conversation_scenarios import ConversationScenario
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-5>)from google.adk.evaluation.eval_case import Invocation
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-6>)from google.adk.evaluation.eval_metrics import EvalMetric
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-7>)from google.adk.evaluation.eval_metrics import EvalStatus
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-8>)from google.adk.evaluation.evaluator import EvaluationResult, PerInvocationResult
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-9>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-10>)def check_final_response_exact_match(
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-11>)    eval_metric: EvalMetric,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-12>)    actual_invocations: list[Invocation],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-13>)    expected_invocations: Optional[list[Invocation]],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-14>)    conversation_scenario: Optional[ConversationScenario],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-15>)) -> EvaluationResult:
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-16>)  """Checks if the final response of the first turn matches the expected
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-17>)  response."""
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-18>)  if not expected_invocations:
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-19>)    return EvaluationResult(overall_score=0.0, overall_eval_status=EvalStatus.NOT_EVALUATED)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-20>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-21>)  per_invocation_results = []
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-22>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-23>)  for actual, expected in zip(actual_invocations, expected_invocations):
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-24>)    actual_final_response = "".join([part.text for part in actual.final_response.parts])
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-25>)    expected_final_response = "".join([part.text for part in expected.final_response.parts])
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-26>)    score = 1.0 if actual_final_response == expected_final_response else 0.0
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-27>)    eval_status = EvalStatus.PASSED if score else EvalStatus.FAILED
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-28>)    invocation_result = PerInvocationResult(
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-29>)        actual_invocation=actual,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-30>)        expected_invocation=expected,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-31>)        score=score,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-32>)        eval_status=eval_status
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-33>)    )
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-34>)    per_invocation_results.append(invocation_result)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-35>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-36>)  average_score = statistics.mean(result.score for result in per_invocation_results)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-37>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-38>)  threshold = eval_metric.criterion.threshold
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-39>)  overall_eval_status = (
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-40>)    EvalStatus.PASSED if average_score >= threshold else EvalStatus.FAILED
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-41>)  )
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-42>)  return EvaluationResult(
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-43>)      overall_score=average_score,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-44>)      overall_eval_status=overall_eval_status,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-45>)      per_invocation_results=per_invocation_results,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-1-46>)  )
    
#### Async Metric[¶](<https://adk.dev/evaluate/custom_metrics/#async-metric> "Permanent link")

If your custom metric needs to make asynchronous calls, such as calling an API, you can define it as an `async` function.

The following is an example of a custom metric function that uses a fake async profanity checker API to check if the agent response contains profanity.
    
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-1>)import asyncio
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-2>)import statistics
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-3>)from typing import Optional
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-4>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-5>)from google.adk.evaluation.conversation_scenarios import ConversationScenario
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-6>)from google.adk.evaluation.eval_case import Invocation
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-7>)from google.adk.evaluation.eval_metrics import EvalMetric
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-8>)from google.adk.evaluation.eval_metrics import EvalStatus
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-9>)from google.adk.evaluation.evaluator import EvaluationResult, PerInvocationResult
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-10>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-11>)class ProfanityChecker:
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-12>)  """A fake profanity checker that mimics an async API."""
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-13>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-14>)  async def check(self, text: str) -> bool:
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-15>)    """Returns True if profanity is detected, False otherwise."""
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-16>)    await asyncio.sleep(0.01)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-17>)    return "profanity" in text.lower()
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-18>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-19>)profanity_checker = ProfanityChecker()
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-20>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-21>)async def check_for_profanity(
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-22>)    eval_metric: EvalMetric,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-23>)    actual_invocations: list[Invocation],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-24>)    expected_invocations: Optional[list[Invocation]],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-25>)    conversation_scenario: Optional[ConversationScenario],
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-26>)) -> EvaluationResult:
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-27>)  """Checks if the agent response contains profanity using a fake async API."""
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-28>)  per_invocation_results = []
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-29>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-30>)  for invocation in actual_invocations:
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-31>)    agent_response = "".join(part.text for part in invocation.final_response.parts)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-32>)    has_profanity = await profanity_checker.check(agent_response)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-33>)    score = 0.0 if has_profanity else 1.0
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-34>)    eval_status = EvalStatus.FAILED if has_profanity else EvalStatus.PASSED
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-35>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-36>)    invocation_result = PerInvocationResult(
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-37>)        actual_invocation=invocation,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-38>)        score=score,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-39>)        eval_status=eval_status
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-40>)    )
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-41>)    per_invocation_results.append(invocation_result)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-42>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-43>)  scores = [
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-44>)      result.score
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-45>)      for result in per_invocation_results
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-46>)      if result.eval_status != EvalStatus.NOT_EVALUATED
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-47>)  ]
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-48>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-49>)  average_score = statistics.mean(scores)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-50>)
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-51>)  threshold = eval_metric.criterion.threshold
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-52>)  overall_eval_status = (
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-53>)      EvalStatus.PASSED if average_score >= threshold else EvalStatus.FAILED
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-54>)  )
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-55>)  return EvaluationResult(
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-56>)      overall_score=average_score,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-57>)      overall_eval_status=overall_eval_status,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-58>)      per_invocation_results=per_invocation_results,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-2-59>)  )
    
## Use a Custom Metric[¶](<https://adk.dev/evaluate/custom_metrics/#use-a-custom-metric> "Permanent link")

To use your custom metric in an evaluation run with `adk eval`, you need to specify it in your `EvalConfig` JSON file.

  1. Add your custom metric as one of the eval `criteria`. The key is your metric name, and the value is the passing threshold.
  2. Add a `custom_metrics` object to `EvalConfig`. Inside this object, add an entry for each custom metric, where the key is the metric name (matching the one in `criteria`) and the value is an object containing `code_config`.
  3. The `code_config` object should contain a `name` field with a string representing the Python import path to your custom metric function, in the format `my.module.my_function`.

### Example `EvalConfig`[¶](<https://adk.dev/evaluate/custom_metrics/#example-evalconfig> "Permanent link")

Assuming your `check_final_response_match` function is defined in `my_agent.metrics.py`, your `EvalConfig` might look like this:
    
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-1>){
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-2>)  "criteria": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-3>)    "my_check_final_response_exact_match": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-4>)      "threshold": 0.8
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-5>)    },
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-6>)    "tool_trajectory_avg_score": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-7>)      "threshold": 1.0
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-8>)    }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-9>)  },
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-10>)  "custom_metrics": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-11>)    "my_check_final_response_exact_match": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-12>)      "code_config": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-13>)        "name": "my_agent.metrics.check_final_response_exact_match"
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-14>)      }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-15>)    }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-16>)  }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-3-17>)}
    
With this configuration, when you run `adk eval --config_file_path=<path_to_this_config>`, ADK will execute `check_final_response_exact_match` for each eval case, and check if the returned score is >= 0.8 to mark the `response_match` criterion as passed or failed.

### Providing Metric Information[¶](<https://adk.dev/evaluate/custom_metrics/#providing-metric-information> "Permanent link")

You can optionally provide metadata about your custom metric, such as its description and value range, by adding a [`MetricInfo`](<https://github.com/google/adk-python/blob/main/src/google/adk/evaluation/eval_metrics.py#L369>) object within your custom metric definition in `EvalConfig`. If `metric_info` is not provided, ADK will use default values (`min_value`=0.0, `max_value`=1.0).

This information can be used by ADK tools for display and result aggregation purposes.

Here is an example of providing `metric_info` for a custom metric that returns a score between -1.0 and 1.0:
    
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-1>){
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-2>)  "criteria": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-3>)    "my_metric": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-4>)      "threshold": 0.5
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-5>)    }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-6>)  },
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-7>)  "custom_metrics": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-8>)    "my_metric": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-9>)      "code_config": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-10>)        "name": "my_agent.metrics.my_metric_function"
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-11>)      },
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-12>)      "metric_info": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-13>)        "metric_name": "my_metric",
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-14>)        "description": "This metric evaluates XYZ and returns a score between -1.0 and 1.0.",
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-15>)        "metric_value_info": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-16>)          "interval": {
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-17>)            "min_value": -1.0,
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-18>)            "max_value": 1.0
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-19>)          }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-20>)        }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-21>)      }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-22>)    }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-23>)  }
    [](<https://adk.dev/evaluate/custom_metrics/#__codelineno-4-24>)}
    
Back to top 