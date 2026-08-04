# Workflow patterns - Agent Development Kit (ADK)

> Source: [https://adk.dev/workflows/patterns/](https://adk.dev/workflows/patterns/)

[ Skip to content ](<https://adk.dev/workflows/patterns/#multi-agent-workflow-patterns>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/workflows/patterns.md> "Edit this page on GitHub") [ ](<https://adk.dev/workflows/patterns/index.md> "View this page as Markdown")

# Multi-agent workflow patterns[¶](<https://adk.dev/workflows/patterns/#multi-agent-workflow-patterns> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

This guide provides a number of agent patterns which you can implement with Agent Development Kit (ADK), including code examples. These patterns are useful across a broad set of applications and you should evaluate and test them against your project requirements before committing to a full implementation.

## Coordinator and dispatcher[¶](<https://adk.dev/workflows/patterns/#coordinator-and-dispatcher> "Permanent link")

  * **Structure:** A central [`LlmAgent`](<https://adk.dev/agents/llm-agents/>) (Coordinator) manages several specialized `sub_agents`.
  * **Goal:** Route incoming requests to the appropriate specialist agent.
  * **ADK Primitives Used:**
    * **Hierarchy:** Coordinator has specialists listed in `sub_agents`.
    * **Interaction:** Primarily uses **LLM-Driven Delegation** (requires clear `description`s on sub-agents and appropriate `instruction` on Coordinator) or **Explicit Invocation (`AgentTool`)** (Coordinator includes `AgentTool`-wrapped specialists in its `tools`).

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-1>)# Conceptual Code: Coordinator using LLM Transfer
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-2>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-5>)billing_agent = LlmAgent(name="Billing", description="Handles billing inquiries.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-6>)support_agent = LlmAgent(name="Support", description="Handles technical support requests.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-8>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-9>)coordinator = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-10>)    name="HelpDeskCoordinator",
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-11>)    model="gemini-flash-latest",
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-12>)    instruction="Route user requests: Use Billing agent for payment issues, Support agent for technical problems.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-13>)    description="Main help desk router.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-14>)    # allow_transfer=True is often implicit with sub_agents in AutoFlow
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-15>)    sub_agents=[billing_agent, support_agent]
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-16>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-17>)# User asks "My payment failed" -> Coordinator's LLM should call transfer_to_agent(agent_name='Billing')
    [](<https://adk.dev/workflows/patterns/#__codelineno-0-18>)# User asks "I can't log in" -> Coordinator's LLM should call transfer_to_agent(agent_name='Support')
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-1>)// Conceptual Code: Coordinator using LLM Transfer
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-2>)import { LlmAgent } from '@google/adk';
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-4>)const billingAgent = new LlmAgent({name: 'Billing', description: 'Handles billing inquiries.'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-5>)const supportAgent = new LlmAgent({name: 'Support', description: 'Handles technical support requests.'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-6>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-7>)const coordinator = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-8>)    name: 'HelpDeskCoordinator',
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-9>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-10>)    instruction: 'Route user requests: Use Billing agent for payment issues, Support agent for technical problems.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-11>)    description: 'Main help desk router.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-12>)    // allowTransfer=true is often implicit with subAgents in AutoFlow
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-13>)    subAgents: [billingAgent, supportAgent]
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-14>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-15>)// User asks "My payment failed" -> Coordinator's LLM should call {functionCall: {name: 'transfer_to_agent', args: {agent_name: 'Billing'}}}
    [](<https://adk.dev/workflows/patterns/#__codelineno-1-16>)// User asks "I can't log in" -> Coordinator's LLM should call {functionCall: {name: 'transfer_to_agent', args: {agent_name: 'Support'}}}
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-1>)import (
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-4>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-5>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-6>)// Conceptual Code: Coordinator using LLM Transfer
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-7>)billingAgent, _ := llmagent.New(llmagent.Config{Name: "Billing", Description: "Handles billing inquiries.", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-8>)supportAgent, _ := llmagent.New(llmagent.Config{Name: "Support", Description: "Handles technical support requests.", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-9>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-10>)coordinator, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-11>)    Name:        "HelpDeskCoordinator",
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-12>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-13>)    Instruction: "Route user requests: Use Billing agent for payment issues, Support agent for technical problems.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-14>)    Description: "Main help desk router.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-15>)    SubAgents:   []agent.Agent{billingAgent, supportAgent},
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-16>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-17>)// User asks "My payment failed" -> Coordinator's LLM should call transfer_to_agent(agent_name='Billing')
    [](<https://adk.dev/workflows/patterns/#__codelineno-2-18>)// User asks "I can't log in" -> Coordinator's LLM should call transfer_to_agent(agent_name='Support')
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-1>)// Conceptual Code: Coordinator using LLM Transfer
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-4>)LlmAgent billingAgent = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-5>)    .name("Billing")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-6>)    .description("Handles billing inquiries and payment issues.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-7>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-8>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-9>)LlmAgent supportAgent = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-10>)    .name("Support")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-11>)    .description("Handles technical support requests and login problems.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-12>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-13>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-14>)LlmAgent coordinator = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-15>)    .name("HelpDeskCoordinator")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-16>)    .model("gemini-flash-latest")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-17>)    .instruction("Route user requests: Use Billing agent for payment issues, Support agent for technical problems.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-18>)    .description("Main help desk router.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-19>)    .subAgents(billingAgent, supportAgent)
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-20>)    // Agent transfer is implicit with sub agents in the Autoflow, unless specified
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-21>)    // using .disallowTransferToParent or disallowTransferToPeers
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-22>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-23>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-24>)// User asks "My payment failed" -> Coordinator's LLM should call
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-25>)// transferToAgent(agentName='Billing')
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-26>)// User asks "I can't log in" -> Coordinator's LLM should call
    [](<https://adk.dev/workflows/patterns/#__codelineno-3-27>)// transferToAgent(agentName='Support')
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-1>)val billingAgent =
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-2>)    LlmAgent(name = "Billing", model = model, description = "Handles billing inquiries.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-3>)val supportAgent =
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-4>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-5>)        name = "Support",
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-6>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-7>)        description = "Handles technical support requests.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-8>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-9>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-10>)val helpDesk =
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-11>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-12>)        name = "HelpDeskCoordinator",
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-13>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-14>)        instruction =
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-15>)            Instruction(
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-16>)                "Route user requests: Use Billing agent for payment issues, Support agent for technical problems.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-17>)            ),
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-18>)        description = "Main help desk router.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-19>)        subAgents = listOf(billingAgent, supportAgent),
    [](<https://adk.dev/workflows/patterns/#__codelineno-4-20>)    )
    
## Sequential pipeline[¶](<https://adk.dev/workflows/patterns/#sequential-pipeline> "Permanent link")

  * **Structure:** A [`SequentialAgent`](<https://adk.dev/agents/workflow-agents/sequential-agents/>) contains `sub_agents` executed in a fixed order.
  * **Goal:** Implement a multistep process where the output of one-step feeds into the next.
  * **ADK Primitives Used:**
    * **Workflow:** `SequentialAgent` defines the order.
    * **Communication:** Primarily uses **Shared Session State**. Earlier agents write results (often via `output_key`), later agents read those results from `context.state`.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-1>)# Conceptual Code: Sequential Data Pipeline
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-2>)from google.adk.agents import SequentialAgent, LlmAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-5>)validator = LlmAgent(name="ValidateInput", instruction="Validate the input.", output_key="validation_status")
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-6>)processor = LlmAgent(name="ProcessData", instruction="Process data if {validation_status} is 'valid'.", output_key="result")
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-7>)reporter = LlmAgent(name="ReportResult", instruction="Report the result from {result}.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-8>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-9>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-10>)data_pipeline = SequentialAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-11>)    name="DataPipeline",
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-12>)    sub_agents=[validator, processor, reporter]
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-13>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-14>)# validator runs -> saves to state['validation_status']
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-15>)# processor runs -> reads state['validation_status'], saves to state['result']
    [](<https://adk.dev/workflows/patterns/#__codelineno-5-16>)# reporter runs -> reads state['result']
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-1>)// Conceptual Code: Sequential Data Pipeline
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-2>)import { SequentialAgent, LlmAgent } from '@google/adk';
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-4>)const validator = new LlmAgent({name: 'ValidateInput', instruction: 'Validate the input.', outputKey: 'validation_status'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-5>)const processor = new LlmAgent({name: 'ProcessData', instruction: 'Process data if {validation_status} is "valid".', outputKey: 'result'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-6>)const reporter = new LlmAgent({name: 'ReportResult', instruction: 'Report the result from {result}.'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-8>)const dataPipeline = new SequentialAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-9>)    name: 'DataPipeline',
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-10>)    subAgents: [validator, processor, reporter]
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-11>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-12>)// validator runs -> saves to state['validation_status']
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-13>)// processor runs -> reads state['validation_status'], saves to state['result']
    [](<https://adk.dev/workflows/patterns/#__codelineno-6-14>)// reporter runs -> reads state['result']
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-1>)import (
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-4>)    "google.golang.org/adk/v2/agent/workflowagents/sequentialagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-5>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-6>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-7>)// Conceptual Code: Sequential Data Pipeline
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-8>)validator, _ := llmagent.New(llmagent.Config{Name: "ValidateInput", Instruction: "Validate the input.", OutputKey: "validation_status", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-9>)processor, _ := llmagent.New(llmagent.Config{Name: "ProcessData", Instruction: "Process data if {validation_status} is 'valid'.", OutputKey: "result", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-10>)reporter, _ := llmagent.New(llmagent.Config{Name: "ReportResult", Instruction: "Report the result from {result}.", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-12>)dataPipeline, _ := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-13>)    AgentConfig: agent.Config{Name: "DataPipeline", SubAgents: []agent.Agent{validator, processor, reporter}},
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-14>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-15>)// validator runs -> saves to state["validation_status"]
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-16>)// processor runs -> reads state["validation_status"], saves to state["result"]
    [](<https://adk.dev/workflows/patterns/#__codelineno-7-17>)// reporter runs -> reads state["result"]
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-1>)// Conceptual Code: Sequential Data Pipeline
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-2>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-5>)LlmAgent validator = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-6>)    .name("ValidateInput")
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-7>)    .instruction("Validate the input")
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-8>)    .outputKey("validation_status") // Saves its main text output to session.state["validation_status"]
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-9>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-10>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-12>)LlmAgent processor = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-13>)    .name("ProcessData")
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-14>)    .instruction("Process data if {validation_status} is 'valid'")
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-15>)    .outputKey("result") // Saves its main text output to session.state["result"]
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-16>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-17>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-18>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-19>)LlmAgent reporter = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-20>)    .name("ReportResult")
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-21>)    .instruction("Report the result from {result}")
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-22>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-23>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-24>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-25>)SequentialAgent dataPipeline = SequentialAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-26>)    .name("DataPipeline")
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-27>)    .subAgents(validator, processor, reporter)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-28>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-29>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-30>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-31>)// validator runs -> saves to state['validation_status']
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-32>)// processor runs -> reads state['validation_status'], saves to state['result']
    [](<https://adk.dev/workflows/patterns/#__codelineno-8-33>)// reporter runs -> reads state['result']
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-1>)val validator =
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-2>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-3>)        name = "ValidateInput",
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-4>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-5>)        instruction = Instruction("Validate the input."),
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-6>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-7>)val processor =
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-8>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-9>)        name = "ProcessData",
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-10>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-11>)        instruction = Instruction("Process data if validation is successful."),
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-12>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-13>)val reporter =
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-14>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-15>)        name = "ReportResult",
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-16>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-17>)        instruction = Instruction("Report the result."),
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-18>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-19>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-20>)val dataPipeline =
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-21>)    SequentialAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-22>)        name = "DataPipeline",
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-23>)        subAgents = listOf(validator, processor, reporter),
    [](<https://adk.dev/workflows/patterns/#__codelineno-9-24>)    )
    
## Parallel fan-out and gather[¶](<https://adk.dev/workflows/patterns/#parallel-fan-out-and-gather> "Permanent link")

  * **Structure:** A [`ParallelAgent`](<https://adk.dev/agents/workflow-agents/parallel-agents/>) runs multiple `sub_agents` concurrently, often followed by a later agent (in a `SequentialAgent`) that aggregates results.
  * **Goal:** Execute independent tasks simultaneously to reduce latency, then combine their outputs.
  * **ADK Primitives Used:**
    * **Workflow:** `ParallelAgent` for concurrent execution (Fan-Out). Often nested within a `SequentialAgent` to handle the subsequent aggregation step (Gather).
    * **Communication:** Sub-agents write results to distinct keys in **Shared Session State**. The subsequent "Gather" agent reads multiple state keys.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-1>)# Conceptual Code: Parallel Information Gathering
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-2>)from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-5>)fetch_api1 = LlmAgent(name="API1Fetcher", instruction="Fetch data from API 1.", output_key="api1_data")
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-6>)fetch_api2 = LlmAgent(name="API2Fetcher", instruction="Fetch data from API 2.", output_key="api2_data")
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-8>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-9>)gather_concurrently = ParallelAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-10>)    name="ConcurrentFetch",
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-11>)    sub_agents=[fetch_api1, fetch_api2]
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-12>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-13>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-14>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-15>)synthesizer = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-16>)    name="Synthesizer",
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-17>)    instruction="Combine results from {api1_data} and {api2_data}."
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-18>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-19>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-20>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-21>)overall_workflow = SequentialAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-22>)    name="FetchAndSynthesize",
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-23>)    sub_agents=[gather_concurrently, synthesizer] # Run parallel fetch, then synthesize
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-24>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-25>)# fetch_api1 and fetch_api2 run concurrently, saving to state.
    [](<https://adk.dev/workflows/patterns/#__codelineno-10-26>)# synthesizer runs afterwards, reading state['api1_data'] and state['api2_data'].
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-1>)// Conceptual Code: Parallel Information Gathering
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-2>)import { SequentialAgent, ParallelAgent, LlmAgent } from '@google/adk';
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-4>)const fetchApi1 = new LlmAgent({name: 'API1Fetcher', instruction: 'Fetch data from API 1.', outputKey: 'api1_data'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-5>)const fetchApi2 = new LlmAgent({name: 'API2Fetcher', instruction: 'Fetch data from API 2.', outputKey: 'api2_data'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-6>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-7>)const gatherConcurrently = new ParallelAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-8>)    name: 'ConcurrentFetch',
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-9>)    subAgents: [fetchApi1, fetchApi2]
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-10>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-12>)const synthesizer = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-13>)    name: 'Synthesizer',
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-14>)    instruction: 'Combine results from {api1_data} and {api2_data}.'
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-15>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-16>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-17>)const overallWorkflow = new SequentialAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-18>)    name: 'FetchAndSynthesize',
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-19>)    subAgents: [gatherConcurrently, synthesizer] // Run parallel fetch, then synthesize
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-20>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-21>)// fetchApi1 and fetchApi2 run concurrently, saving to state.
    [](<https://adk.dev/workflows/patterns/#__codelineno-11-22>)// synthesizer runs afterwards, reading state['api1_data'] and state['api2_data'].
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-1>)import (
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-4>)    "google.golang.org/adk/v2/agent/workflowagents/parallelagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-5>)    "google.golang.org/adk/v2/agent/workflowagents/sequentialagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-6>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-8>)// Conceptual Code: Parallel Information Gathering
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-9>)fetchAPI1, _ := llmagent.New(llmagent.Config{Name: "API1Fetcher", Instruction: "Fetch data from API 1.", OutputKey: "api1_data", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-10>)fetchAPI2, _ := llmagent.New(llmagent.Config{Name: "API2Fetcher", Instruction: "Fetch data from API 2.", OutputKey: "api2_data", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-12>)gatherConcurrently, _ := parallelagent.New(parallelagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-13>)    AgentConfig: agent.Config{Name: "ConcurrentFetch", SubAgents: []agent.Agent{fetchAPI1, fetchAPI2}},
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-14>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-15>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-16>)synthesizer, _ := llmagent.New(llmagent.Config{Name: "Synthesizer", Instruction: "Combine results from {api1_data} and {api2_data}.", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-17>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-18>)overallWorkflow, _ := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-19>)    AgentConfig: agent.Config{Name: "FetchAndSynthesize", SubAgents: []agent.Agent{gatherConcurrently, synthesizer}},
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-20>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-21>)// fetch_api1 and fetch_api2 run concurrently, saving to state.
    [](<https://adk.dev/workflows/patterns/#__codelineno-12-22>)// synthesizer runs afterwards, reading state["api1_data"] and state["api2_data"].
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-1>)// Conceptual Code: Parallel Information Gathering
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-3>)import com.google.adk.agents.ParallelAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-4>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-5>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-6>)LlmAgent fetchApi1 = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-7>)    .name("API1Fetcher")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-8>)    .instruction("Fetch data from API 1.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-9>)    .outputKey("api1_data")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-10>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-12>)LlmAgent fetchApi2 = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-13>)    .name("API2Fetcher")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-14>)    .instruction("Fetch data from API 2.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-15>)    .outputKey("api2_data")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-16>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-17>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-18>)ParallelAgent gatherConcurrently = ParallelAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-19>)    .name("ConcurrentFetcher")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-20>)    .subAgents(fetchApi2, fetchApi1)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-21>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-22>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-23>)LlmAgent synthesizer = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-24>)    .name("Synthesizer")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-25>)    .instruction("Combine results from {api1_data} and {api2_data}.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-26>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-27>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-28>)SequentialAgent overallWorfklow = SequentialAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-29>)    .name("FetchAndSynthesize") // Run parallel fetch, then synthesize
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-30>)    .subAgents(gatherConcurrently, synthesizer)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-31>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-32>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-33>)// fetch_api1 and fetch_api2 run concurrently, saving to state.
    [](<https://adk.dev/workflows/patterns/#__codelineno-13-34>)// synthesizer runs afterwards, reading state['api1_data'] and state['api2_data'].
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-1>)val fetchApi1 =
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-2>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-3>)        name = "API1Fetcher",
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-4>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-5>)        instruction = Instruction("Fetch data from API 1."),
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-6>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-7>)val fetchApi2 =
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-8>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-9>)        name = "API2Fetcher",
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-10>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-11>)        instruction = Instruction("Fetch data from API 2."),
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-12>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-13>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-14>)val gatherConcurrently =
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-15>)    ParallelAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-16>)        name = "ConcurrentFetch",
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-17>)        subAgents = listOf(fetchApi1, fetchApi2),
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-18>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-19>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-20>)val synthesizer =
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-21>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-22>)        name = "Synthesizer",
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-23>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-24>)        instruction = Instruction("Combine results from state."),
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-25>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-26>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-27>)val overallWorkflow =
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-28>)    SequentialAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-29>)        name = "FetchAndSynthesize",
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-30>)        subAgents = listOf(gatherConcurrently, synthesizer),
    [](<https://adk.dev/workflows/patterns/#__codelineno-14-31>)    )
    
## Hierarchical task decomposition[¶](<https://adk.dev/workflows/patterns/#hierarchical-task-decomposition> "Permanent link")

  * **Structure:** A multi-level tree of agents where higher-level agents break down complex goals and delegate sub-tasks to lower-level agents.
  * **Goal:** Solve complex problems by recursively breaking them down into simpler, executable steps.
  * **ADK Primitives Used:**
    * **Hierarchy:** Multi-level `parent_agent`/`sub_agents` structure.
    * **Interaction:** Primarily **LLM-Driven Delegation** or **Explicit Invocation (`AgentTool`)** used by parent agents to assign tasks to subagents. Results are returned up the hierarchy (via tool responses or state).

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-1>)# Conceptual Code: Hierarchical Research Task
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-2>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-3>)from google.adk.tools import agent_tool
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-5>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-6>)# Low-level tool-like agents
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-7>)web_searcher = LlmAgent(name="WebSearch", description="Performs web searches for facts.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-8>)summarizer = LlmAgent(name="Summarizer", description="Summarizes text.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-9>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-10>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-11>)# Mid-level agent combining tools
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-12>)research_assistant = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-13>)    name="ResearchAssistant",
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-14>)    model="gemini-flash-latest",
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-15>)    description="Finds and summarizes information on a topic.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-16>)    tools=[agent_tool.AgentTool(agent=web_searcher), agent_tool.AgentTool(agent=summarizer)]
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-17>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-18>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-19>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-20>)# High-level agent delegating research
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-21>)report_writer = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-22>)    name="ReportWriter",
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-23>)    model="gemini-flash-latest",
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-24>)    instruction="Write a report on topic X. Use the ResearchAssistant to gather information.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-25>)    tools=[agent_tool.AgentTool(agent=research_assistant)]
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-26>)    # Alternatively, could use LLM Transfer if research_assistant is a sub_agent
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-27>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-28>)# User interacts with ReportWriter.
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-29>)# ReportWriter calls ResearchAssistant tool.
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-30>)# ResearchAssistant calls WebSearch and Summarizer tools.
    [](<https://adk.dev/workflows/patterns/#__codelineno-15-31>)# Results flow back up.
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-1>)// Conceptual Code: Hierarchical Research Task
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-2>)import { LlmAgent, AgentTool } from '@google/adk';
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-4>)// Low-level tool-like agents
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-5>)const webSearcher = new LlmAgent({name: 'WebSearch', description: 'Performs web searches for facts.'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-6>)const summarizer = new LlmAgent({name: 'Summarizer', description: 'Summarizes text.'});
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-8>)// Mid-level agent combining tools
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-9>)const researchAssistant = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-10>)    name: 'ResearchAssistant',
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-11>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-12>)    description: 'Finds and summarizes information on a topic.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-13>)    tools: [new AgentTool({agent: webSearcher}), new AgentTool({agent: summarizer})]
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-14>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-15>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-16>)// High-level agent delegating research
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-17>)const reportWriter = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-18>)    name: 'ReportWriter',
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-19>)    model: 'gemini-flash-latest',
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-20>)    instruction: 'Write a report on topic X. Use the ResearchAssistant to gather information.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-21>)    tools: [new AgentTool({agent: researchAssistant})]
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-22>)    // Alternatively, could use LLM Transfer if researchAssistant is a subAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-23>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-24>)// User interacts with ReportWriter.
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-25>)// ReportWriter calls ResearchAssistant tool.
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-26>)// ResearchAssistant calls WebSearch and Summarizer tools.
    [](<https://adk.dev/workflows/patterns/#__codelineno-16-27>)// Results flow back up.
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-1>)import (
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-2>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-3>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-4>)    "google.golang.org/adk/v2/tool/agenttool"
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-5>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-6>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-7>)// Conceptual Code: Hierarchical Research Task
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-8>)// Low-level tool-like agents
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-9>)webSearcher, _ := llmagent.New(llmagent.Config{Name: "WebSearch", Description: "Performs web searches for facts.", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-10>)summarizer, _ := llmagent.New(llmagent.Config{Name: "Summarizer", Description: "Summarizes text.", Model: m})
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-12>)// Mid-level agent combining tools
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-13>)webSearcherTool := agenttool.New(webSearcher, nil)
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-14>)summarizerTool := agenttool.New(summarizer, nil)
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-15>)researchAssistant, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-16>)    Name:        "ResearchAssistant",
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-17>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-18>)    Description: "Finds and summarizes information on a topic.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-19>)    Tools:       []tool.Tool{webSearcherTool, summarizerTool},
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-20>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-21>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-22>)// High-level agent delegating research
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-23>)researchAssistantTool := agenttool.New(researchAssistant, nil)
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-24>)reportWriter, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-25>)    Name:        "ReportWriter",
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-26>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-27>)    Instruction: "Write a report on topic X. Use the ResearchAssistant to gather information.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-28>)    Tools:       []tool.Tool{researchAssistantTool},
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-29>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-30>)// User interacts with ReportWriter.
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-31>)// ReportWriter calls ResearchAssistant tool.
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-32>)// ResearchAssistant calls WebSearch and Summarizer tools.
    [](<https://adk.dev/workflows/patterns/#__codelineno-17-33>)// Results flow back up.
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-1>)// Conceptual Code: Hierarchical Research Task
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-3>)import com.google.adk.tools.AgentTool;
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-5>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-6>)// Low-level tool-like agents
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-7>)LlmAgent webSearcher = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-8>)    .name("WebSearch")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-9>)    .description("Performs web searches for facts.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-10>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-12>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-13>)LlmAgent summarizer = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-14>)    .name("Summarizer")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-15>)    .description("Summarizes text.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-16>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-17>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-18>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-19>)// Mid-level agent combining tools
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-20>)LlmAgent researchAssistant = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-21>)    .name("ResearchAssistant")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-22>)    .model("gemini-flash-latest")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-23>)    .description("Finds and summarizes information on a topic.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-24>)    .tools(AgentTool.create(webSearcher), AgentTool.create(summarizer))
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-25>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-26>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-27>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-28>)// High-level agent delegating research
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-29>)LlmAgent reportWriter = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-30>)    .name("ReportWriter")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-31>)    .model("gemini-flash-latest")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-32>)    .instruction("Write a report on topic X. Use the ResearchAssistant to gather information.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-33>)    .tools(AgentTool.create(researchAssistant))
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-34>)    // Alternatively, could use LLM Transfer if research_assistant is a subAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-35>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-36>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-37>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-38>)// User interacts with ReportWriter.
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-39>)// ReportWriter calls ResearchAssistant tool.
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-40>)// ResearchAssistant calls WebSearch and Summarizer tools.
    [](<https://adk.dev/workflows/patterns/#__codelineno-18-41>)// Results flow back up.
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-1>)val webSearcher =
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-2>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-3>)        name = "WebSearch",
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-4>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-5>)        description = "Performs web searches for facts.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-6>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-7>)val summarizer = LlmAgent(name = "Summarizer", model = model, description = "Summarizes text.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-8>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-9>)val researchAssistant =
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-10>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-11>)        name = "ResearchAssistant",
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-12>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-13>)        description = "Finds and summarizes information on a topic.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-14>)        subAgents = listOf(webSearcher, summarizer),
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-15>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-16>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-17>)val reportWriter =
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-18>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-19>)        name = "ReportWriter",
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-20>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-21>)        instruction =
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-22>)            Instruction(
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-23>)                "Write a report on topic X. Use the ResearchAssistant to gather information.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-24>)            ),
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-25>)        subAgents = listOf(researchAssistant),
    [](<https://adk.dev/workflows/patterns/#__codelineno-19-26>)    )
    
## Generate and review pattern[¶](<https://adk.dev/workflows/patterns/#generate-and-review-pattern> "Permanent link")

  * **Structure:** Typically involves two agents within a [`SequentialAgent`](<https://adk.dev/agents/workflow-agents/sequential-agents/>): a generator agent and a critic reviewer agent.
  * **Goal:** Improve the quality or validity of generated output by having a dedicated agent review it.
  * **ADK Primitives Used:**
    * **Workflow:** `SequentialAgent` ensures generation happens before review.
    * **Communication:** **Shared Session State** (Generator uses `output_key` to save output; Reviewer reads that state key). The Reviewer might save its feedback to another state key for subsequent steps.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-1>)# Conceptual Code: Generator-Critic
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-2>)from google.adk.agents import SequentialAgent, LlmAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-5>)generator = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-6>)    name="DraftWriter",
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-7>)    instruction="Write a short paragraph about subject X.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-8>)    output_key="draft_text"
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-9>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-10>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-12>)reviewer = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-13>)    name="FactChecker",
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-14>)    instruction="Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-15>)    output_key="review_status"
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-16>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-17>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-18>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-19>)# Optional: Further steps based on review_status
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-20>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-21>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-22>)review_pipeline = SequentialAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-23>)    name="WriteAndReview",
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-24>)    sub_agents=[generator, reviewer]
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-25>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-26>)# generator runs -> saves draft to state['draft_text']
    [](<https://adk.dev/workflows/patterns/#__codelineno-20-27>)# reviewer runs -> reads state['draft_text'], saves status to state['review_status']
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-1>)// Conceptual Code: Generator-Critic
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-2>)import { SequentialAgent, LlmAgent } from '@google/adk';
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-3>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-4>)const generator = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-5>)    name: 'DraftWriter',
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-6>)    instruction: 'Write a short paragraph about subject X.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-7>)    outputKey: 'draft_text'
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-8>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-9>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-10>)const reviewer = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-11>)    name: 'FactChecker',
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-12>)    instruction: 'Review the text in {draft_text} for factual accuracy. Output "valid" or "invalid" with reasons.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-13>)    outputKey: 'review_status'
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-14>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-15>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-16>)// Optional: Further steps based on review_status
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-17>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-18>)const reviewPipeline = new SequentialAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-19>)    name: 'WriteAndReview',
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-20>)    subAgents: [generator, reviewer]
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-21>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-22>)// generator runs -> saves draft to state['draft_text']
    [](<https://adk.dev/workflows/patterns/#__codelineno-21-23>)// reviewer runs -> reads state['draft_text'], saves status to state['review_status']
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-1>)import (
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-4>)    "google.golang.org/adk/v2/agent/workflowagents/sequentialagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-5>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-6>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-7>)// Conceptual Code: Generator-Critic
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-8>)generator, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-9>)    Name:        "DraftWriter",
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-10>)    Instruction: "Write a short paragraph about subject X.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-11>)    OutputKey:   "draft_text",
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-12>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-13>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-14>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-15>)reviewer, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-16>)    Name:        "FactChecker",
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-17>)    Instruction: "Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-18>)    OutputKey:   "review_status",
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-19>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-20>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-21>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-22>)reviewPipeline, _ := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-23>)    AgentConfig: agent.Config{Name: "WriteAndReview", SubAgents: []agent.Agent{generator, reviewer}},
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-24>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-25>)// generator runs -> saves draft to state["draft_text"]
    [](<https://adk.dev/workflows/patterns/#__codelineno-22-26>)// reviewer runs -> reads state["draft_text"], saves status to state["review_status"]
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-1>)// Conceptual Code: Generator-Critic
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-3>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-5>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-6>)LlmAgent generator = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-7>)    .name("DraftWriter")
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-8>)    .instruction("Write a short paragraph about subject X.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-9>)    .outputKey("draft_text")
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-10>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-12>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-13>)LlmAgent reviewer = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-14>)    .name("FactChecker")
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-15>)    .instruction("Review the text in {draft_text} for factual accuracy. Output 'valid' or 'invalid' with reasons.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-16>)    .outputKey("review_status")
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-17>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-18>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-19>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-20>)// Optional: Further steps based on review_status
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-21>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-22>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-23>)SequentialAgent reviewPipeline = SequentialAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-24>)    .name("WriteAndReview")
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-25>)    .subAgents(generator, reviewer)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-26>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-27>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-28>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-29>)// generator runs -> saves draft to state['draft_text']
    [](<https://adk.dev/workflows/patterns/#__codelineno-23-30>)// reviewer runs -> reads state['draft_text'], saves status to state['review_status']
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-1>)val generator =
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-2>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-3>)        name = "DraftWriter",
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-4>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-5>)        instruction = Instruction("Write a short paragraph about subject X."),
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-6>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-8>)val reviewer =
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-9>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-10>)        name = "FactChecker",
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-11>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-12>)        instruction =
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-13>)            Instruction(
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-14>)                "Review the generated text for factual accuracy. Output 'valid' or 'invalid' with reasons.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-15>)            ),
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-16>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-17>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-18>)val reviewPipeline =
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-19>)    SequentialAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-20>)        name = "WriteAndReview",
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-21>)        subAgents = listOf(generator, reviewer),
    [](<https://adk.dev/workflows/patterns/#__codelineno-24-22>)    )
    
## Iterative refinement[¶](<https://adk.dev/workflows/patterns/#iterative-refinement> "Permanent link")

  * **Structure:** Uses a [`LoopAgent`](<https://adk.dev/agents/workflow-agents/loop-agents/>) containing one or more agents that work on a task over multiple iterations.
  * **Goal:** Progressively improve a result (e.g., code, text, plan) stored in the session state until a quality threshold is met or a maximum number of iterations is reached.
  * **ADK Primitives Used:**
    * **Workflow:** `LoopAgent` manages the repetition.
    * **Communication:** **Shared Session State** is essential for agents to read the previous iteration's output and save the refined version.
    * **Termination:** The loop typically ends based on `max_iterations` or a dedicated checking agent setting `escalate=True` in the `Event Actions` when the result is satisfactory.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-1>)# Conceptual Code: Iterative Code Refinement
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-2>)from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-3>)from google.adk.events import Event, EventActions
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-4>)from google.adk.agents.invocation_context import InvocationContext
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-5>)from typing import AsyncGenerator
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-6>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-8>)# Agent to generate/refine code based on state['current_code'] and state['requirements']
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-9>)code_refiner = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-10>)    name="CodeRefiner",
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-11>)    instruction="Read state['current_code'] (if exists) and state['requirements']. Generate/refine Python code to meet requirements. Save to state['current_code'].",
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-12>)    output_key="current_code" # Overwrites previous code in state
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-13>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-14>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-15>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-16>)# Agent to check if the code meets quality standards
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-17>)quality_checker = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-18>)    name="QualityChecker",
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-19>)    instruction="Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-20>)    output_key="quality_status"
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-21>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-22>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-23>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-24>)# Custom agent to check the status and escalate if 'pass'
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-25>)class CheckStatusAndEscalate(BaseAgent):
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-26>)    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-27>)        status = ctx.session.state.get("quality_status", "fail")
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-28>)        should_stop = (status == "pass")
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-29>)        yield Event(author=self.name, actions=EventActions(escalate=should_stop))
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-30>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-31>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-32>)refinement_loop = LoopAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-33>)    name="CodeRefinementLoop",
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-34>)    max_iterations=5,
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-35>)    sub_agents=[code_refiner, quality_checker, CheckStatusAndEscalate(name="StopChecker")]
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-36>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-37>)# Loop runs: Refiner -> Checker -> StopChecker
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-38>)# State['current_code'] is updated each iteration.
    [](<https://adk.dev/workflows/patterns/#__codelineno-25-39>)# Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-1>)// Conceptual Code: Iterative Code Refinement
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-2>)import { LoopAgent, LlmAgent, BaseAgent, InvocationContext } from '@google/adk';
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-3>)import type { Event, createEvent, createEventActions } from '@google/genai';
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-5>)// Agent to generate/refine code based on state['current_code'] and state['requirements']
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-6>)const codeRefiner = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-7>)    name: 'CodeRefiner',
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-8>)    instruction: 'Read state["current_code"] (if exists) and state["requirements"]. Generate/refine Typescript code to meet requirements. Save to state["current_code"].',
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-9>)    outputKey: 'current_code' // Overwrites previous code in state
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-10>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-12>)// Agent to check if the code meets quality standards
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-13>)const qualityChecker = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-14>)    name: 'QualityChecker',
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-15>)    instruction: 'Evaluate the code in state["current_code"] against state["requirements"]. Output "pass" or "fail".',
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-16>)    outputKey: 'quality_status'
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-17>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-18>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-19>)// Custom agent to check the status and escalate if 'pass'
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-20>)class CheckStatusAndEscalate extends BaseAgent {
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-21>)    async *runAsyncImpl(ctx: InvocationContext): AsyncGenerator<Event> {
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-22>)        const status = ctx.session.state.quality_status;
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-23>)        const shouldStop = status === 'pass';
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-24>)        if (shouldStop) {
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-25>)            yield createEvent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-26>)                author: 'StopChecker',
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-27>)                actions: createEventActions(),
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-28>)            });
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-29>)        }
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-30>)    }
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-31>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-32>)    async *runLiveImpl(ctx: InvocationContext): AsyncGenerator<Event> {
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-33>)        // This agent doesn't have a live implementation
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-34>)        yield createEvent({ author: 'StopChecker' });
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-35>)    }
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-36>)}
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-37>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-38>)// Loop runs: Refiner -> Checker -> StopChecker
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-39>)// State['current_code'] is updated each iteration.
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-40>)// Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-41>)const refinementLoop = new LoopAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-42>)    name: 'CodeRefinementLoop',
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-43>)    maxIterations: 5,
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-44>)    subAgents: [codeRefiner, qualityChecker, new CheckStatusAndEscalate({name: 'StopChecker'})]
    [](<https://adk.dev/workflows/patterns/#__codelineno-26-45>)});
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-1>)import (
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-2>)    "iter"
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-3>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-4>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-5>)    "google.golang.org/adk/v2/agent/workflowagents/loopagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-6>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-7>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-8>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-9>)// Conceptual Code: Iterative Code Refinement
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-10>)codeRefiner, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-11>)    Name:        "CodeRefiner",
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-12>)    Instruction: "Read state['current_code'] (if exists) and state['requirements']. Generate/refine Python code to meet requirements. Save to state['current_code'].",
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-13>)    OutputKey:   "current_code",
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-14>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-15>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-16>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-17>)qualityChecker, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-18>)    Name:        "QualityChecker",
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-19>)    Instruction: "Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-20>)    OutputKey:   "quality_status",
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-21>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-22>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-23>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-24>)checkStatusAndEscalate, _ := agent.New(agent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-25>)    Name: "StopChecker",
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-26>)    Run: func(ctx agent.InvocationContext) iter.Seq2[*session.Event, error] {
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-27>)        return func(yield func(*session.Event, error) bool) {
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-28>)            status, _ := ctx.Session().State().Get("quality_status")
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-29>)            shouldStop := status == "pass"
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-30>)            yield(&session.Event{Author: "StopChecker", Actions: session.EventActions{Escalate: shouldStop}}, nil)
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-31>)        }
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-32>)    },
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-33>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-34>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-35>)refinementLoop, _ := loopagent.New(loopagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-36>)    MaxIterations: 5,
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-37>)    AgentConfig:   agent.Config{Name: "CodeRefinementLoop", SubAgents: []agent.Agent{codeRefiner, qualityChecker, checkStatusAndEscalate}},
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-38>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-39>)// Loop runs: Refiner -> Checker -> StopChecker
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-40>)// State["current_code"] is updated each iteration.
    [](<https://adk.dev/workflows/patterns/#__codelineno-27-41>)// Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5 iterations.
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-1>)// Conceptual Code: Iterative Code Refinement
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-2>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-4>)import com.google.adk.agents.LoopAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-5>)import com.google.adk.events.Event;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-6>)import com.google.adk.events.EventActions;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-7>)import com.google.adk.agents.InvocationContext;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-8>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-9>)import java.util.List;
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-10>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-11>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-12>)// Agent to generate/refine code based on state['current_code'] and state['requirements']
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-13>)LlmAgent codeRefiner = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-14>)    .name("CodeRefiner")
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-15>)    .instruction("Read state['current_code'] (if exists) and state['requirements']. Generate/refine Java code to meet requirements. Save to state['current_code'].")
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-16>)    .outputKey("current_code") // Overwrites previous code in state
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-17>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-18>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-19>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-20>)// Agent to check if the code meets quality standards
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-21>)LlmAgent qualityChecker = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-22>)    .name("QualityChecker")
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-23>)    .instruction("Evaluate the code in state['current_code'] against state['requirements']. Output 'pass' or 'fail'.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-24>)    .outputKey("quality_status")
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-25>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-26>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-27>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-28>)BaseAgent checkStatusAndEscalate = new BaseAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-29>)    "StopChecker","Checks quality_status and escalates if 'pass'.", List.of(), null, null) {
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-30>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-31>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-32>)  @Override
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-33>)  protected Flowable<Event> runAsyncImpl(InvocationContext invocationContext) {
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-34>)    String status = (String) invocationContext.session().state().getOrDefault("quality_status", "fail");
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-35>)    boolean shouldStop = "pass".equals(status);
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-36>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-37>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-38>)    EventActions actions = EventActions.builder().escalate(shouldStop).build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-39>)    Event event = Event.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-40>)        .author(this.name())
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-41>)        .actions(actions)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-42>)        .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-43>)    return Flowable.just(event);
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-44>)  }
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-45>)};
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-46>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-47>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-48>)LoopAgent refinementLoop = LoopAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-49>)    .name("CodeRefinementLoop")
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-50>)    .maxIterations(5)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-51>)    .subAgents(codeRefiner, qualityChecker, checkStatusAndEscalate)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-52>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-53>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-54>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-55>)// Loop runs: Refiner -> Checker -> StopChecker
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-56>)// State['current_code'] is updated each iteration.
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-57>)// Loop stops if QualityChecker outputs 'pass' (leading to StopChecker escalating) or after 5
    [](<https://adk.dev/workflows/patterns/#__codelineno-28-58>)// iterations.
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-1>)val codeRefiner =
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-2>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-3>)        name = "CodeRefiner",
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-4>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-5>)        instruction =
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-6>)            Instruction(
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-7>)                "Read current code (if exists) and requirements from state. Generate/refine Kotlin code to meet requirements.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-8>)            ),
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-9>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-10>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-11>)val qualityChecker =
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-12>)    LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-13>)        name = "QualityChecker",
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-14>)        model = model,
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-15>)        instruction =
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-16>)            Instruction(
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-17>)                "Evaluate the code in state against requirements. Output 'pass' or 'fail'.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-18>)            ),
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-19>)    )
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-20>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-21>)val stopChecker = CheckConditionAgent(name = "StopChecker") // Checks quality_status
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-22>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-23>)val refinementLoop =
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-24>)    LoopAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-25>)        name = "CodeRefinementLoop",
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-26>)        maxIterations = 5,
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-27>)        subAgents = listOf(codeRefiner, qualityChecker, stopChecker),
    [](<https://adk.dev/workflows/patterns/#__codelineno-29-28>)    )
    
## Human-in-the-loop[¶](<https://adk.dev/workflows/patterns/#human-in-the-loop> "Permanent link")

  * **Structure:** Integrates human intervention points within an agent workflow.
  * **Goal:** Allow for human oversight, approval, correction, or tasks that AI cannot perform.
  * **ADK Primitives Used (Conceptual):**
    * **Interaction:** Can be implemented using a custom **Tool** that pauses execution and sends a request to an external system (e.g., a UI, ticketing system) waiting for human input. The tool then returns the human's response to the agent.
    * **Workflow:** Could use **LLM-Driven Delegation** (`transfer_to_agent`) targeting a conceptual "Human Agent" that triggers the external workflow, or use the custom tool within an `LlmAgent`.
    * **State/Callbacks:** State can hold task details for the human; callbacks can manage the interaction flow.
    * **Note:** ADK doesn't have a built-in "Human Agent" type, so this requires custom integration.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-1>)# Conceptual Code: Using a Tool for Human Approval
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-2>)from google.adk.agents import LlmAgent, SequentialAgent
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-3>)from google.adk.tools import FunctionTool
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-5>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-6>)# --- Assume external_approval_tool exists ---
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-7>)# This tool would:
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-8>)# 1. Take details (e.g., request_id, amount, reason).
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-9>)# 2. Send these details to a human review system (e.g., via API).
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-10>)# 3. Poll or wait for the human response (approved/rejected).
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-11>)# 4. Return the human's decision.
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-12>)# async def external_approval_tool(amount: float, reason: str) -> str: ...
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-13>)approval_tool = FunctionTool(func=external_approval_tool)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-14>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-15>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-16>)# Agent that prepares the request
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-17>)prepare_request = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-18>)    name="PrepareApproval",
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-19>)    instruction="Prepare the approval request details based on user input. Store amount and reason in state.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-20>)    # ... likely sets state['approval_amount'] and state['approval_reason'] ...
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-21>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-22>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-23>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-24>)# Agent that calls the human approval tool
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-25>)request_approval = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-26>)    name="RequestHumanApproval",
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-27>)    instruction="Use the external_approval_tool with amount from state['approval_amount'] and reason from state['approval_reason'].",
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-28>)    tools=[approval_tool],
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-29>)    output_key="human_decision"
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-30>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-31>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-32>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-33>)# Agent that proceeds based on human decision
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-34>)process_decision = LlmAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-35>)    name="ProcessDecision",
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-36>)    instruction="Check {human_decision}. If 'approved', proceed. If 'rejected', inform user."
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-37>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-38>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-39>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-40>)approval_workflow = SequentialAgent(
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-41>)    name="HumanApprovalWorkflow",
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-42>)    sub_agents=[prepare_request, request_approval, process_decision]
    [](<https://adk.dev/workflows/patterns/#__codelineno-30-43>))
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-1>)// Conceptual Code: Using a Tool for Human Approval
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-2>)import { LlmAgent, SequentialAgent, FunctionTool } from '@google/adk';
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-3>)import { z } from 'zod';
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-4>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-5>)// --- Assume externalApprovalTool exists ---
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-6>)// This tool would:
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-7>)// 1. Take details (e.g., request_id, amount, reason).
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-8>)// 2. Send these details to a human review system (e.g., via API).
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-9>)// 3. Poll or wait for the human response (approved/rejected).
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-10>)// 4. Return the human's decision.
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-11>)async function externalApprovalTool(params: {amount: number, reason: string}): Promise<{decision: string}> {
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-12>)  // ... implementation to call external system
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-13>)  return {decision: 'approved'}; // or 'rejected'
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-14>)}
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-15>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-16>)const approvalTool = new FunctionTool({
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-17>)  name: 'external_approval_tool',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-18>)  description: 'Sends a request for human approval.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-19>)  parameters: z.object({
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-20>)    amount: z.number(),
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-21>)    reason: z.string(),
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-22>)  }),
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-23>)  execute: externalApprovalTool,
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-24>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-25>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-26>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-27>)// Agent that prepares the request
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-28>)const prepareRequest = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-29>)    name: 'PrepareApproval',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-30>)    instruction: 'Prepare the approval request details based on user input. Store amount and reason in state.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-31>)    // ... likely sets state['approval_amount'] and state['approval_reason'] ...
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-32>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-33>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-34>)// Agent that calls the human approval tool
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-35>)const requestApproval = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-36>)    name: 'RequestHumanApproval',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-37>)    instruction: 'Use the external_approval_tool with amount from state["approval_amount"] and reason from state["approval_reason"].',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-38>)    tools: [approvalTool],
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-39>)    outputKey: 'human_decision'
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-40>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-41>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-42>)// Agent that proceeds based on human decision
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-43>)const processDecision = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-44>)    name: 'ProcessDecision',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-45>)    instruction: 'Check {human_decision}. If "approved", proceed. If "rejected", inform user.'
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-46>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-47>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-48>)const approvalWorkflow = new SequentialAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-49>)    name: 'HumanApprovalWorkflow',
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-50>)    subAgents: [prepareRequest, requestApproval, processDecision]
    [](<https://adk.dev/workflows/patterns/#__codelineno-31-51>)});
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-1>)import (
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-2>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-3>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-4>)    "google.golang.org/adk/v2/agent/workflowagents/sequentialagent"
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-5>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-6>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-7>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-8>)// Conceptual Code: Using a Tool for Human Approval
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-9>)// --- Assume externalApprovalTool exists ---
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-10>)// func externalApprovalTool(amount float64, reason string) (string, error) { ... }
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-11>)type externalApprovalToolArgs struct {
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-12>)    Amount float64 `json:"amount" jsonschema:"The amount for which approval is requested."`
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-13>)    Reason string  `json:"reason" jsonschema:"The reason for the approval request."`
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-14>)}
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-15>)var externalApprovalTool func(agent.Context, externalApprovalToolArgs) (string, error)
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-16>)approvalTool, _ := functiontool.New(
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-17>)    functiontool.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-18>)        Name:        "external_approval_tool",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-19>)        Description: "Sends a request for human approval.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-20>)    },
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-21>)    externalApprovalTool,
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-22>))
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-23>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-24>)prepareRequest, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-25>)    Name:        "PrepareApproval",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-26>)    Instruction: "Prepare the approval request details based on user input. Store amount and reason in state.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-27>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-28>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-29>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-30>)requestApproval, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-31>)    Name:        "RequestHumanApproval",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-32>)    Instruction: "Use the external_approval_tool with amount from state['approval_amount'] and reason from state['approval_reason'].",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-33>)    Tools:       []tool.Tool{approvalTool},
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-34>)    OutputKey:   "human_decision",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-35>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-36>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-37>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-38>)processDecision, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-39>)    Name:        "ProcessDecision",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-40>)    Instruction: "Check {human_decision}. If 'approved', proceed. If 'rejected', inform user.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-41>)    Model:       m,
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-42>)})
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-43>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-44>)approvalWorkflow, _ := sequentialagent.New(sequentialagent.Config{
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-45>)    AgentConfig: agent.Config{Name: "HumanApprovalWorkflow", SubAgents: []agent.Agent{prepareRequest, requestApproval, processDecision}},
    [](<https://adk.dev/workflows/patterns/#__codelineno-32-46>)})
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-1>)// Conceptual Code: Using a Tool for Human Approval
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-2>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-3>)import com.google.adk.agents.SequentialAgent;
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-4>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-5>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-6>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-7>)// --- Assume external_approval_tool exists ---
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-8>)// This tool would:
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-9>)// 1. Take details (e.g., request_id, amount, reason).
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-10>)// 2. Send these details to a human review system (e.g., via API).
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-11>)// 3. Poll or wait for the human response (approved/rejected).
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-12>)// 4. Return the human's decision.
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-13>)// public boolean externalApprovalTool(float amount, String reason) { ... }
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-14>)FunctionTool approvalTool = FunctionTool.create(externalApprovalTool);
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-15>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-16>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-17>)// Agent that prepares the request
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-18>)LlmAgent prepareRequest = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-19>)    .name("PrepareApproval")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-20>)    .instruction("Prepare the approval request details based on user input. Store amount and reason in state.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-21>)    // ... likely sets state['approval_amount'] and state['approval_reason'] ...
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-22>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-23>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-24>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-25>)// Agent that calls the human approval tool
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-26>)LlmAgent requestApproval = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-27>)    .name("RequestHumanApproval")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-28>)    .instruction("Use the external_approval_tool with amount from state['approval_amount'] and reason from state['approval_reason'].")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-29>)    .tools(approvalTool)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-30>)    .outputKey("human_decision")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-31>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-32>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-33>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-34>)// Agent that proceeds based on human decision
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-35>)LlmAgent processDecision = LlmAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-36>)    .name("ProcessDecision")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-37>)    .instruction("Check {human_decision}. If 'approved', proceed. If 'rejected', inform user.")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-38>)    .build();
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-39>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-40>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-41>)SequentialAgent approvalWorkflow = SequentialAgent.builder()
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-42>)    .name("HumanApprovalWorkflow")
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-43>)    .subAgents(prepareRequest, requestApproval, processDecision)
    [](<https://adk.dev/workflows/patterns/#__codelineno-33-44>)    .build();
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-1>)class ExternalApprovalTool : BaseTool(
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-2>)    "external_approval_tool",
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-3>)    "Sends a request for human approval.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-4>)) {
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-5>)    override fun declaration(): FunctionDeclaration =
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-6>)        FunctionDeclaration(
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-7>)            "external_approval_tool",
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-8>)            "Sends a request for human approval.",
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-9>)        )
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-10>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-11>)    override suspend fun run(
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-12>)        context: ToolContext,
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-13>)        args: Map<String, Any>,
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-14>)    ): Any {
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-15>)        // Simulate calling external system (e.g., UI, ticketing system)
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-16>)        // In a real app, this might poll for a result or wait for a webhook.
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-17>)        return mapOf("decision" to "approved")
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-18>)    }
    [](<https://adk.dev/workflows/patterns/#__codelineno-34-19>)}
    
### Human in the loop with Policy[¶](<https://adk.dev/workflows/patterns/#human-in-the-loop-with-policy> "Permanent link")

A more advanced and structured way to implement Human-in-the-Loop is by using a `PolicyEngine`. This approach allows you to define policies that can trigger a confirmation step from a user before a tool is executed. The `SecurityPlugin` intercepts a tool call, consults the `PolicyEngine`, and if the policy dictates, it will automatically request user confirmation. This pattern is more robust for enforcing governance and security rules.

Here's how it works:

  1. **`SecurityPlugin`** : You add this plugin to your `Runner`. It acts as an interceptor for all tool calls.
  2. **`BasePolicyEngine`** : You create a custom class that implements this interface. Its `evaluate()` method contains your logic to decide if a tool call needs confirmation.
  3. **`PolicyOutcome.CONFIRM`** : When your `evaluate()` method returns this outcome, the `SecurityPlugin` pauses the tool execution and generates a special `FunctionCall` using `getAskUserConfirmationFunctionCalls`.
  4. **Application Handling** : Your application code receives this special function call and presents the confirmation request to the user.
  5. **User Confirmation** : Once the user confirms, your application sends a `FunctionResponse` back to the agent, which allows the `SecurityPlugin` to proceed with the original tool execution.

TypeScript Recommended Pattern

The Policy-based pattern is the recommended approach for implementing Human-in-the-Loop workflows in TypeScript. Support in other ADK languages is planned for future releases.

A conceptual example of using a `CustomPolicyEngine` to require user confirmation before executing any tool is shown below.

TypeScript
    
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-1>)const rootAgent = new LlmAgent({
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-2>)  name: 'weather_time_agent',
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-3>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-4>)  description:
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-5>)      'Agent to answer questions about the time and weather in a city.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-6>)  instruction:
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-7>)      'You are a helpful agent who can answer user questions about the time and weather in a city.',
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-8>)  tools: [getWeatherTool],
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-9>)});
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-10>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-11>)class CustomPolicyEngine implements BasePolicyEngine {
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-12>)  async evaluate(_context: ToolCallPolicyContext): Promise<PolicyCheckResult> {
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-13>)    // Default permissive implementation
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-14>)    return Promise.resolve({
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-15>)      outcome: PolicyOutcome.CONFIRM,
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-16>)      reason: 'Needs confirmation for tool call',
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-17>)    });
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-18>)  }
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-19>)}
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-20>)
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-21>)const runner = new InMemoryRunner({
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-22>)    agent: rootAgent,
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-23>)    appName,
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-24>)    plugins: [new SecurityPlugin({policyEngine: new CustomPolicyEngine()})]
    [](<https://adk.dev/workflows/patterns/#__codelineno-35-25>)});
    
You can find the full code sample [here](<https://github.com/google/adk-docs/blob/main/examples/typescript/snippets/agents/workflow-agents/hitl_confirmation_agent.ts>).

Back to top 