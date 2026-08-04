# Resume Agents - Agent Development Kit (ADK)

> Source: [https://adk.dev/runtime/resume/](https://adk.dev/runtime/resume/)

[ Skip to content ](<https://adk.dev/runtime/resume/#resume-stopped-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/runtime/resume.md> "Edit this page on GitHub") [ ](<https://adk.dev/runtime/resume/index.md> "View this page as Markdown")

# Resume stopped agents[¶](<https://adk.dev/runtime/resume/#resume-stopped-agents> "Permanent link")

Supported in ADKPython v1.14.0Kotlin v0.1.0

An ADK agent's execution can be interrupted by various factors including dropped network connections, power failure, or a required external system going offline. The Resume feature of ADK allows an agent workflow to pick up where it left off, avoiding the need to restart the entire workflow. In ADK Python 1.16 and higher, you can configure an ADK workflow to be resumable, so that it tracks the execution of workflow and then allows you to resume it after an unexpected interruption.

This guide explains how to configure your ADK agent workflow to be resumable. If you use Custom Agents, you can update them to be resumable. For more information, see [Add resume to custom Agents](<https://adk.dev/runtime/resume/#custom-agents>).

## Add resumable configuration[¶](<https://adk.dev/runtime/resume/#add-resumable-configuration> "Permanent link")

Enable the Resume function for an agent workflow by applying a Resumability configuration to the App object of your ADK workflow, as shown in the following code example:

PythonKotlin
    
    [](<https://adk.dev/runtime/resume/#__codelineno-0-1>)app = App(
    [](<https://adk.dev/runtime/resume/#__codelineno-0-2>)    name='my_resumable_agent',
    [](<https://adk.dev/runtime/resume/#__codelineno-0-3>)    root_agent=root_agent,
    [](<https://adk.dev/runtime/resume/#__codelineno-0-4>)    # Set the resumability config to enable resumability.
    [](<https://adk.dev/runtime/resume/#__codelineno-0-5>)    resumability_config=ResumabilityConfig(
    [](<https://adk.dev/runtime/resume/#__codelineno-0-6>)        is_resumable=True,
    [](<https://adk.dev/runtime/resume/#__codelineno-0-7>)    ),
    [](<https://adk.dev/runtime/resume/#__codelineno-0-8>))
    
    [](<https://adk.dev/runtime/resume/#__codelineno-1-1>)@OptIn(ExperimentalResumabilityFeature::class)
    [](<https://adk.dev/runtime/resume/#__codelineno-1-2>)val runner =
    [](<https://adk.dev/runtime/resume/#__codelineno-1-3>)    InMemoryRunner(
    [](<https://adk.dev/runtime/resume/#__codelineno-1-4>)        app =
    [](<https://adk.dev/runtime/resume/#__codelineno-1-5>)            App(
    [](<https://adk.dev/runtime/resume/#__codelineno-1-6>)                appName = "my_resumable_agent",
    [](<https://adk.dev/runtime/resume/#__codelineno-1-7>)                rootAgent = rootAgent,
    [](<https://adk.dev/runtime/resume/#__codelineno-1-8>)                resumabilityConfig = ResumabilityConfig(isResumable = true),
    [](<https://adk.dev/runtime/resume/#__codelineno-1-9>)            ),
    [](<https://adk.dev/runtime/resume/#__codelineno-1-10>)        sessionService = InMemorySessionService(),
    [](<https://adk.dev/runtime/resume/#__codelineno-1-11>)    )
    
Caution: Long Running Functions, Confirmations, Authentication

For agents that use [Long Running Functions](<https://adk.dev/tools-custom/function-tools/#long-run-tool>), [Confirmations](<https://adk.dev/tools-custom/confirmation/>), or [Authentication](<https://adk.dev/tools-custom/authentication/>) requiring user input, adding a resumable confirmation changes how these features operate. For more information, see the documentation for those features.

Note: Custom Agents

Resume is not supported by default for Custom Agents. You must update the agent code for a Custom Agent to support the Resume feature. For information on modifying Custom Agents to support incremental resume functionality, see [Add resume to custom Agents](<https://adk.dev/runtime/resume/#custom-agents>).

## Resume a stopped workflow[¶](<https://adk.dev/runtime/resume/#resume-a-stopped-workflow> "Permanent link")

When an ADK workflow stops execution you can resume the workflow using a command containing the Invocation ID for the workflow instance, which can be found in the [Event](<https://adk.dev/events/#understanding-and-using-events>) history of the workflow. Make sure the ADK API server is running, in case it was interrupted or powered off, and then run the following command to resume the workflow, as shown in the following API request example.
    
    [](<https://adk.dev/runtime/resume/#__codelineno-2-1>)# restart the API server if needed:
    [](<https://adk.dev/runtime/resume/#__codelineno-2-2>)adk api_server my_resumable_agent/
    [](<https://adk.dev/runtime/resume/#__codelineno-2-3>)
    [](<https://adk.dev/runtime/resume/#__codelineno-2-4>)# resume the agent:
    [](<https://adk.dev/runtime/resume/#__codelineno-2-5>)curl -X POST http://localhost:8000/run_sse \
    [](<https://adk.dev/runtime/resume/#__codelineno-2-6>) -H "Content-Type: application/json" \
    [](<https://adk.dev/runtime/resume/#__codelineno-2-7>) -d '{
    [](<https://adk.dev/runtime/resume/#__codelineno-2-8>)   "app_name": "my_resumable_agent",
    [](<https://adk.dev/runtime/resume/#__codelineno-2-9>)   "user_id": "u_123",
    [](<https://adk.dev/runtime/resume/#__codelineno-2-10>)   "session_id": "s_abc",
    [](<https://adk.dev/runtime/resume/#__codelineno-2-11>)   "invocation_id": "invocation-123",
    [](<https://adk.dev/runtime/resume/#__codelineno-2-12>) }'
    
You can also resume a workflow using the Runner object Run Async method, as shown below:

PythonKotlin
    
    [](<https://adk.dev/runtime/resume/#__codelineno-3-1>)runner.run_async(user_id='u_123', session_id='s_abc',
    [](<https://adk.dev/runtime/resume/#__codelineno-3-2>)    invocation_id='invocation-123')
    [](<https://adk.dev/runtime/resume/#__codelineno-3-3>)
    [](<https://adk.dev/runtime/resume/#__codelineno-3-4>)# When new_message is set to a function response,
    [](<https://adk.dev/runtime/resume/#__codelineno-3-5>)# we are trying to resume a long running function.
    
    [](<https://adk.dev/runtime/resume/#__codelineno-4-1>)fun resumeAgent(runner: InMemoryRunner) =
    [](<https://adk.dev/runtime/resume/#__codelineno-4-2>)    runBlocking {
    [](<https://adk.dev/runtime/resume/#__codelineno-4-3>)        runner
    [](<https://adk.dev/runtime/resume/#__codelineno-4-4>)            .runAsync(
    [](<https://adk.dev/runtime/resume/#__codelineno-4-5>)                userId = "user123",
    [](<https://adk.dev/runtime/resume/#__codelineno-4-6>)                sessionId = "session456",
    [](<https://adk.dev/runtime/resume/#__codelineno-4-7>)                invocationId = "previous-invocation-id",
    [](<https://adk.dev/runtime/resume/#__codelineno-4-8>)            ).collect { event ->
    [](<https://adk.dev/runtime/resume/#__codelineno-4-9>)                // resume execution from previous state
    [](<https://adk.dev/runtime/resume/#__codelineno-4-10>)            }
    [](<https://adk.dev/runtime/resume/#__codelineno-4-11>)    }
    
Note

Resuming a workflow from the ADK Web user interface or using the ADK command line (CLI) tool is not currently supported.

## How it works[¶](<https://adk.dev/runtime/resume/#how-it-works> "Permanent link")

The Resume feature works by logging completed Agent workflow tasks, including incremental steps using [Events](<https://adk.dev/events/>) and [Event Actions](<https://adk.dev/events/#detecting-actions-and-side-effects>). tracking completion of agent tasks within a resumable workflow. If a workflow is interrupted and then later restarted, the system resumes the workflow by setting the completion state of each agent. If an agent did not complete, the workflow system reinstates any completed Events for that agent, and restarts the workflow from the partially completed state. For multi-agent workflows, the specific resume behavior varies, based on the multi-agent classes in your workflow, as described below:

  * **Sequential Agent** : Reads the current_sub_agent from its saved state to find the next sub-agent to run in the sequence.
  * **Loop Agent** : Uses the current_sub_agent and times_looped values to continue the loop from the last completed iteration and sub-agent.
  * **Parallel Agent** : Determines which sub-agents have already completed and only runs those that have not finished.

Event logging includes results from Tools which successfully returned a result. So if an agent successfully executed Function Tools A and B, and then failed during execution of tool C, the system reinstates the results from the tools A and B, and resumes the workflow by re-running the tool C request.

Caution: Tool execution behavior

When resuming a workflow with Tools, the Resume feature ensures that the Tools in an agent are run **_at least once_** , and may run more than once when resuming a workflow. If your agent uses Tools where duplicate runs would have a negative impact, such as purchases, you should modify the Tool to check for and prevent duplicate runs.

Note: Workflow modification with Resume not supported

Do not modify a stopped agent workflow before resuming it. For example adding or removing agents from workflow that has stopped and then resuming that workflow is not supported.

## Add resume to custom Agents[¶](<https://adk.dev/runtime/resume/#custom-agents> "Permanent link")

Custom agents have specific implementation requirements in order to support resumability. You must decide on and define workflow steps within your custom agent which produce a result which can be preserved before handing off to the next step of processing. The following steps outline how to modify a Custom Agent to support a workflow Resume.

  * **Create CustomAgentState class** : Extend the BaseAgentState to create an object that preserves the state of your agent.
    * **Optionally, create WorkFlowStep class** : If your custom agent has sequential steps, consider creating a WorkFlowStep list object that defines the discrete, savable steps of the agent.
  * **Add initial agent state:** Modify your agent's async run function to set the initial state of your agent.
  * **Add agent state checkpoints** : Modify your agent's async run function to generate and save the agent state for each completed step of the agent's overall task.
  * **Add end of agent status to track agent state:** Modify your agent's async run function to include an `end_of_agent=True` status upon successful completion of the agent's full task.

The following example shows the required code modifications to the example StoryFlowAgent class shown in the [Custom Agents](<https://adk.dev/agents/custom-agents/#full-code-example>) guide:
    
    [](<https://adk.dev/runtime/resume/#__codelineno-5-1>)class WorkflowStep(int, Enum):
    [](<https://adk.dev/runtime/resume/#__codelineno-5-2>) INITIAL_STORY_GENERATION = 1
    [](<https://adk.dev/runtime/resume/#__codelineno-5-3>) CRITIC_REVISER_LOOP = 2
    [](<https://adk.dev/runtime/resume/#__codelineno-5-4>) POST_PROCESSING = 3
    [](<https://adk.dev/runtime/resume/#__codelineno-5-5>) CONDITIONAL_REGENERATION = 4
    [](<https://adk.dev/runtime/resume/#__codelineno-5-6>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-7>)# Extend BaseAgentState
    [](<https://adk.dev/runtime/resume/#__codelineno-5-8>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-9>)### class StoryFlowAgentState(BaseAgentState):
    [](<https://adk.dev/runtime/resume/#__codelineno-5-10>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-11>)###   step = WorkflowStep
    [](<https://adk.dev/runtime/resume/#__codelineno-5-12>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-13>)@override
    [](<https://adk.dev/runtime/resume/#__codelineno-5-14>)async def _run_async_impl(
    [](<https://adk.dev/runtime/resume/#__codelineno-5-15>)    self, ctx: InvocationContext
    [](<https://adk.dev/runtime/resume/#__codelineno-5-16>)) -> AsyncGenerator[Event, None]:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-17>)    """
    [](<https://adk.dev/runtime/resume/#__codelineno-5-18>)    Implements the custom orchestration logic for the story workflow.
    [](<https://adk.dev/runtime/resume/#__codelineno-5-19>)    Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
    [](<https://adk.dev/runtime/resume/#__codelineno-5-20>)    """
    [](<https://adk.dev/runtime/resume/#__codelineno-5-21>)    agent_state = self._load_agent_state(ctx, WorkflowStep)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-22>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-23>)    if agent_state is None:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-24>)      # Record the start of the agent
    [](<https://adk.dev/runtime/resume/#__codelineno-5-25>)      agent_state = StoryFlowAgentState(step=WorkflowStep.INITIAL_STORY_GENERATION)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-26>)      yield self._create_agent_state_event(ctx, agent_state)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-27>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-28>)    next_step = agent_state.step
    [](<https://adk.dev/runtime/resume/#__codelineno-5-29>)    logger.info(f"[{self.name}] Starting story generation workflow.")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-30>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-31>)    # Step 1. Initial Story Generation
    [](<https://adk.dev/runtime/resume/#__codelineno-5-32>)    if next_step <= WorkflowStep.INITIAL_STORY_GENERATION:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-33>)      logger.info(f"[{self.name}] Running StoryGenerator...")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-34>)      async for event in self.story_generator.run_async(ctx):
    [](<https://adk.dev/runtime/resume/#__codelineno-5-35>)          yield event
    [](<https://adk.dev/runtime/resume/#__codelineno-5-36>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-37>)      # Check if story was generated before proceeding
    [](<https://adk.dev/runtime/resume/#__codelineno-5-38>)      if "current_story" not in ctx.session.state or not ctx.session.state[
    [](<https://adk.dev/runtime/resume/#__codelineno-5-39>)          "current_story"
    [](<https://adk.dev/runtime/resume/#__codelineno-5-40>)      ]:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-41>)          return  # Stop processing if initial story failed
    [](<https://adk.dev/runtime/resume/#__codelineno-5-42>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-43>)    agent_state = StoryFlowAgentState(step=WorkflowStep.CRITIC_REVISER_LOOP)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-44>)    yield self._create_agent_state_event(ctx, agent_state)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-45>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-46>)    # Step 2. Critic-Reviser Loop
    [](<https://adk.dev/runtime/resume/#__codelineno-5-47>)    if next_step <= WorkflowStep.CRITIC_REVISER_LOOP:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-48>)      logger.info(f"[{self.name}] Running CriticReviserLoop...")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-49>)      async for event in self.loop_agent.run_async(ctx):
    [](<https://adk.dev/runtime/resume/#__codelineno-5-50>)          logger.info(
    [](<https://adk.dev/runtime/resume/#__codelineno-5-51>)              f"[{self.name}] Event from CriticReviserLoop: "
    [](<https://adk.dev/runtime/resume/#__codelineno-5-52>)              f"{event.model_dump_json(indent=2, exclude_none=True)}"
    [](<https://adk.dev/runtime/resume/#__codelineno-5-53>)          )
    [](<https://adk.dev/runtime/resume/#__codelineno-5-54>)          yield event
    [](<https://adk.dev/runtime/resume/#__codelineno-5-55>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-56>)    agent_state = StoryFlowAgentState(step=WorkflowStep.POST_PROCESSING)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-57>)    yield self._create_agent_state_event(ctx, agent_state)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-58>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-59>)    # Step 3. Sequential Post-Processing (Grammar and Tone Check)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-60>)    if next_step <= WorkflowStep.POST_PROCESSING:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-61>)      logger.info(f"[{self.name}] Running PostProcessing...")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-62>)      async for event in self.sequential_agent.run_async(ctx):
    [](<https://adk.dev/runtime/resume/#__codelineno-5-63>)          logger.info(
    [](<https://adk.dev/runtime/resume/#__codelineno-5-64>)              f"[{self.name}] Event from PostProcessing: "
    [](<https://adk.dev/runtime/resume/#__codelineno-5-65>)              f"{event.model_dump_json(indent=2, exclude_none=True)}"
    [](<https://adk.dev/runtime/resume/#__codelineno-5-66>)          )
    [](<https://adk.dev/runtime/resume/#__codelineno-5-67>)          yield event
    [](<https://adk.dev/runtime/resume/#__codelineno-5-68>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-69>)    agent_state = StoryFlowAgentState(step=WorkflowStep.CONDITIONAL_REGENERATION)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-70>)    yield self._create_agent_state_event(ctx, agent_state)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-71>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-72>)    # Step 4. Tone-Based Conditional Logic
    [](<https://adk.dev/runtime/resume/#__codelineno-5-73>)    if next_step <= WorkflowStep.CONDITIONAL_REGENERATION:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-74>)      tone_check_result = ctx.session.state.get("tone_check_result")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-75>)      if tone_check_result == "negative":
    [](<https://adk.dev/runtime/resume/#__codelineno-5-76>)          logger.info(f"[{self.name}] Tone is negative. Regenerating story...")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-77>)          async for event in self.story_generator.run_async(ctx):
    [](<https://adk.dev/runtime/resume/#__codelineno-5-78>)              logger.info(
    [](<https://adk.dev/runtime/resume/#__codelineno-5-79>)                  f"[{self.name}] Event from StoryGenerator (Regen): "
    [](<https://adk.dev/runtime/resume/#__codelineno-5-80>)                  f"{event.model_dump_json(indent=2, exclude_none=True)}"
    [](<https://adk.dev/runtime/resume/#__codelineno-5-81>)              )
    [](<https://adk.dev/runtime/resume/#__codelineno-5-82>)              yield event
    [](<https://adk.dev/runtime/resume/#__codelineno-5-83>)      else:
    [](<https://adk.dev/runtime/resume/#__codelineno-5-84>)          logger.info(f"[{self.name}] Tone is not negative. Keeping current story.")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-85>)
    [](<https://adk.dev/runtime/resume/#__codelineno-5-86>)    logger.info(f"[{self.name}] Workflow finished.")
    [](<https://adk.dev/runtime/resume/#__codelineno-5-87>)    yield self._create_agent_state_event(ctx, end_of_agent=True)
    
Back to top 