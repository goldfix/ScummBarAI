# Template agent workflows - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/workflow-agents/](https://adk.dev/agents/workflow-agents/)

[ Skip to content ](<https://adk.dev/agents/workflow-agents/#template-agent-workflows>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/workflow-agents/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/workflow-agents/index.md> "View this page as Markdown")

# Template agent workflows[¶](<https://adk.dev/agents/workflow-agents/#template-agent-workflows> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0

This section introduces _template workflows_ , also known as _workflow agents_ , which are specialized agents that control the execution flow of one or more sub-agents. Template workflow agents are specialized components designed for orchestrating the execution flow of sub-agents. Their primary role is to manage how and when other agents run, defining the control flow of a process.

Alternative: graph-based workflows

Starting in ADK 2.0 for Python and Go, template workflows have been superseded

by more flexible workflow structures, including [graph-based workflows](<https://adk.dev/graphs/>) and [dynamic workflows](<https://adk.dev/graphs/dynamic/>). These workflow architectures provide more control, flexibility and capability to evolve your agent workflows over time.

![Template agent workflows in ADK](https://adk.dev/assets/template_workflows.svg)

**Figure 1.** Execution patterns of template workflows in ADK

Template workflow agents operate based on predefined logic. They determine the execution sequence according to their type, such as sequential, parallel, or loop, without consulting an AI model for assistance with the orchestration. This approach results in deterministic and predictable execution patterns. Template workflows include the following task execution structures, which each implement a distinct task completion pattern:

  * **Sequential Agent workflow**

* * *

Executes sub-agents one after another, in sequence.

[ Learn more](<https://adk.dev/agents/workflow-agents/sequential-agents/>)

  * **Loop Agent workflow**

* * *

Repeatedly executes its sub-agents until a specific termination condition is met.

[ Learn more](<https://adk.dev/agents/workflow-agents/loop-agents/>)

  * **Parallel Agent workflow**

* * *

Executes multiple sub-agents in parallel.

[ Learn more](<https://adk.dev/agents/workflow-agents/parallel-agents/>)

Back to top 