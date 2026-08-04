# Visual Builder - Agent Development Kit (ADK)

> Source: [https://adk.dev/visual-builder/](https://adk.dev/visual-builder/)

[ Skip to content ](<https://adk.dev/visual-builder/#use-the-visual-builder>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/visual-builder/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/visual-builder/index.md> "View this page as Markdown")

# Use the Visual Builder[¶](<https://adk.dev/visual-builder/#use-the-visual-builder> "Permanent link")

Supported in ADKPython v1.18.0Experimental

The ADK Visual Builder is a feature of the ADK web interface that provides a visual workflow design environment for creating and managing agents. The Visual Builder allows you to design, build, and test agents in a beginner-friendly graphical interface, and includes an AI-powered assistant to help you build agents.

![Visual Agent Builder](https://adk.dev/assets/visual-builder.png)

Experimental

The Visual Builder feature is an experimental release. We welcome your [feedback](<https://github.com/google/adk-python/issues/new?template=feature_request.md>)!

## Create an agent[¶](<https://adk.dev/visual-builder/#create-an-agent> "Permanent link")

To use the Visual Builder, start the ADK web interface:
    
    [](<https://adk.dev/visual-builder/#__codelineno-0-1>)adk web
    
Then follow the steps below to create an agent.

Tip: Run from a code development directory

The Visual Builder tool writes project files to new subdirectories located in the directory where you run ADK Web. Make sure you run this command from a developer directory location where you have write access.

![Visual Agent Builder start](https://adk.dev/assets/visual-builder-start.png) **Figure 1:** ADK Web controls to start the Visual Builder tool.

To create an agent with Visual Builder:

  1. In the top left of the web UI, select the **+** (plus sign), as shown in _Figure 1_ , to start creating an agent.
  2. Type a name for your agent application and select **Create**.
  3. Edit your agent by doing any of the following:
     * In the left panel, edit agent component values.
     * In the central panel, add new agent components.
     * In the right panel, use prompts to modify the agent or get help.
  4. In the bottom left corner, select **Save** to save your agent.
  5. Interact with your new agent to test it.
  6. In the top left of the web UI, select the pencil icon, as shown in _Figure 1_ , to continue editing your agent.

Here are a few things to note when using Visual Builder:

  * **Create agent and save:** When creating an agent, make sure you select **Save** before exiting the editing interface, otherwise your new agent may not be editable.
  * **Agent editing:** Edit (pencil icon) for agents is _only_ available for agents created with Visual Builder.
  * **Add tools:** When adding existing custom Tools to a Visual Builder agent, specify a fully-qualified Python function name.

Try this prompt with the Visual Builder assistant
    
    [](<https://adk.dev/visual-builder/#__codelineno-1-1>)Help me add a dice roll tool to my current agent.
    [](<https://adk.dev/visual-builder/#__codelineno-1-2>)Use the default model if you need to configure that.
    
## Supported components[¶](<https://adk.dev/visual-builder/#supported-components> "Permanent link")

The Visual Builder tool provides a drag-and-drop user interface for constructing agents, as well as an AI-powered development Assistant that can answer questions and edit your agent workflow. The tool supports all the essential components for building an ADK agent workflow, including:

  * **Agents**
    * **Root Agent** : The primary controlling agent for a workflow. All other agents in an ADK agent workflow are considered Sub Agents.
    * [**LLM Agent:**](<https://adk.dev/agents/llm-agents/>) An agent powered by a generative AI model.
    * [**Sequential Agent:**](<https://adk.dev/agents/workflow-agents/sequential-agents/>) A workflow agent that executes a series of sub-agents in a sequence.
    * [**Loop Agent:**](<https://adk.dev/agents/workflow-agents/loop-agents/>) A workflow agent that repeatedly executes a sub-agent until a certain condition is met.
    * [**Parallel Agent:**](<https://adk.dev/agents/workflow-agents/parallel-agents/>) A workflow agent that executes multiple sub-agents concurrently.
  * **Tools**
    * [**Prebuilt tools:**](<https://adk.dev/integrations/>) A limited set of ADK-provided tools can be added to agents.
    * [**Custom tools:**](<https://adk.dev/tools-custom/>) You can build and add custom tools to your workflow.
  * **Components**
    * [**Callbacks**](<https://adk.dev/callbacks/>) A flow control component that lets you modify the behavior of agents at the start and end of agent workflow events.

Some advanced ADK features are not supported by Visual Builder due to limitations of the Agent Config feature. For more information, see the Agent Config [Known limitations](<https://adk.dev/agents/config/#known-limitations>).

## Generated project structure[¶](<https://adk.dev/visual-builder/#generated-project-structure> "Permanent link")

The Visual Builder tool generates code in the [Agent Config](<https://adk.dev/agents/config/>) format, using `.yaml` configuration files for agents and Python code for custom tools. These files are generated in a subfolder of the directory where you ran the ADK web interface. The following listing shows an example layout for a DiceAgent project:
    
    [](<https://adk.dev/visual-builder/#__codelineno-2-1>)DiceAgent/
    [](<https://adk.dev/visual-builder/#__codelineno-2-2>)    root_agent.yaml    # main agent code
    [](<https://adk.dev/visual-builder/#__codelineno-2-3>)    sub_agent_1.yaml   # sub agents (if any)
    [](<https://adk.dev/visual-builder/#__codelineno-2-4>)    tools/             # tools directory
    [](<https://adk.dev/visual-builder/#__codelineno-2-5>)        __init__.py
    [](<https://adk.dev/visual-builder/#__codelineno-2-6>)        dice_tool.py   # tool code
    
Editing generated agents

You can edit the generated files in your development environment. However, some changes may not be compatible with Visual Builder.

For more information on the Agent Config code format used by Visual Builder, see [Agent Config](<https://adk.dev/agents/config/>) and [Agent Config YAML schema](<https://adk.dev/api-reference/agentconfig/>).

## Security and deployment[¶](<https://adk.dev/visual-builder/#security-and-deployment> "Permanent link")

The Visual Builder saves agent configuration files to your project directory through local API endpoints. For security reasons, these endpoints are available only when the web UI is served (for example, `adk web`). In headless or API-only deployments, such as the default `adk deploy cloud_run`, they are not registered, which prevents unauthorized file writes.

File upload restrictions

To prevent arbitrary file writes, file uploads through the Visual Builder accept only files with `.yaml` and `.yml` extensions. The server automatically rejects absolute paths, path traversal sequences (`..`), and YAML files containing blocked keys (such as `args`) that can execute arbitrary code.

Back to top 