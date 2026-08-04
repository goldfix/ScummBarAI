# MCP tools - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools-custom/mcp-tools/](https://adk.dev/tools-custom/mcp-tools/)

[ Skip to content ](<https://adk.dev/tools-custom/mcp-tools/#model-context-protocol-tools>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools-custom/mcp-tools.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools-custom/mcp-tools/index.md> "View this page as Markdown")

# Model Context Protocol Tools[¶](<https://adk.dev/tools-custom/mcp-tools/#model-context-protocol-tools> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0

This guide walks you through two ways of integrating Model Context Protocol (MCP) with ADK.

MCP tools for ADK

For a list of pre-built MCP tools for ADK, see [Tools and Integrations](<https://adk.dev/integrations/?topic=mcp>).

## What is Model Context Protocol (MCP)?[¶](<https://adk.dev/tools-custom/mcp-tools/#what-is-model-context-protocol-mcp> "Permanent link")

The Model Context Protocol (MCP) is an open standard designed to standardize how Large Language Models (LLMs) like Gemini and Claude communicate with external applications, data sources, and tools. Think of it as a universal connection mechanism that simplifies how LLMs obtain context, execute actions, and interact with various systems.

MCP follows a client-server architecture, defining how **data** (resources), **interactive templates** (prompts), and **actionable functions** (tools) are exposed by an **MCP server** and consumed by an **MCP client** (which could be an LLM host application or an AI agent).

This guide covers two primary integration patterns:

  1. **Using Existing MCP Servers within ADK:** An ADK agent acts as an MCP client, leveraging tools provided by external MCP servers.
  2. **Exposing ADK Tools via an MCP Server:** Building an MCP server that wraps ADK tools, making them accessible to any MCP client.

## Key considerations[¶](<https://adk.dev/tools-custom/mcp-tools/#key-considerations> "Permanent link")

When you start building with the Model Context Protocol (MCP) and ADK, these key architectural differences will help you design more stable and efficient agents:

  * **Protocol vs. Library:** MCP is a protocol specification, defining communication rules. ADK is a Python library/framework for building agents. McpToolset bridges these by implementing the client side of the MCP protocol within the ADK framework. Conversely, building an MCP server in Python requires using the model-context-protocol library.

  * **ADK Tools vs. MCP Tools:**

    * ADK Tools (BaseTool, FunctionTool, AgentTool, etc.) are Python objects designed for direct use within the ADK's LlmAgent and Runner.
    * MCP Tools are capabilities exposed by an MCP Server according to the protocol's schema. McpToolset makes these look like ADK tools to an LlmAgent.
  * **Asynchronous nature:** Both ADK and the MCP Python library are heavily based on the asyncio Python library. Tool implementations and server handlers should generally be async functions.

  * **Stateful sessions (MCP):** MCP establishes stateful, persistent connections between a client and server instance. This differs from typical stateless REST APIs.

    * **Deployment:** This statefulness can pose challenges for scaling and deployment, especially for remote servers handling many users. The original MCP design often assumed client and server were co-located. Managing these persistent connections requires careful infrastructure considerations (e.g., load balancing, session affinity).
    * **ADK McpToolset:** Manages this connection lifecycle. The exit_stack pattern shown in the examples is crucial for ensuring the connection (and potentially the server process) is properly terminated when the ADK agent finishes.
  * **Session persistence** : The `MCPToolset` supports object serialization via `getstate` and `setstate` methods. This feature helps your agent maintain its context when deployed to managed environments like Cloud Run or Google Kubernetes Engine (GKE).

!!! Note: While the agent preserves its session state during lifecycle events, active MCP connections are not automatically re-established upon restoration. The agent will re-initialize its connection to the MCP server as needed after the process is restored to ensure a reliable and up-to-date link.

## Prerequisites[¶](<https://adk.dev/tools-custom/mcp-tools/#prerequisites> "Permanent link")

Before you begin, ensure you have the following set up:

  * **Set up ADK:** Follow the standard ADK [setup instructions](<https://adk.dev/get-started/>) in the quickstart.
  * **Install/update Python/Java:** MCP requires Python version of 3.9 or higher for Python or Java 17 or higher.
  * **Setup Node.js and npx:** **(Python only)** Many community MCP servers are distributed as Node.js packages and run using `npx`. Install Node.js (which includes npx) if you haven't already. For details, see <https://nodejs.org/en>.
  * **Verify Installations:** **(Python only)** Confirm `adk` and `npx` are in your PATH within the activated virtual environment:

MacOS / Linux
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-0-1>)# Both commands should print the path to the executables.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-0-2>)which adk
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-0-3>)which npx
    
Windows
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-1-1>)# Both commands should print the path to the executables.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-1-2>)Get-Command adk
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-1-3>)Get-Command npx
    
## 1\. Using MCP servers with ADK agents (ADK as an MCP client) in `adk web`[¶](<https://adk.dev/tools-custom/mcp-tools/#1-using-mcp-servers-with-adk-agents-adk-as-an-mcp-client-in-adk-web> "Permanent link")

This section demonstrates how to integrate tools from external MCP (Model Context Protocol) servers into your ADK agents. This is the **most common** integration pattern when your ADK agent needs to use capabilities provided by an existing service that exposes an MCP interface. You will see how the `McpToolset` class can be directly added to your agent's `tools` list, enabling seamless connection to an MCP server, discovery of its tools, and making them available for your agent to use. These examples primarily focus on interactions within the `adk web` development environment.

### `McpToolset` class[¶](<https://adk.dev/tools-custom/mcp-tools/#mcptoolset-class> "Permanent link")

The `McpToolset` class is ADK's primary mechanism for integrating tools from an MCP server. When you include an `McpToolset` instance in your agent's `tools` list, it automatically handles the interaction with the specified MCP server. Here's how it works:

  1. **Connection Management:** On initialization, `McpToolset` establishes and manages the connection to the MCP server. This can be a local server process (using `StdioConnectionParams` for communication over standard input/output) or a remote server (using `SseConnectionParams` for Server-Sent Events). The toolset also handles the graceful shutdown of this connection when the agent or application terminates.
  2. **Tool Discovery & Adaptation:** Once connected, `McpToolset` queries the MCP server for its available tools (via the `list_tools` MCP method). It then converts the schemas of these discovered MCP tools into ADK-compatible `BaseTool` instances.
  3. **Exposure to Agent:** These adapted tools are then made available to your `LlmAgent` as if they were native ADK tools.
  4. **Proxying Tool Calls:** When your `LlmAgent` decides to use one of these tools, `McpToolset` transparently proxies the call (using the `call_tool` MCP method) to the MCP server, sends the necessary arguments, and returns the server's response back to the agent.
  5. **Filtering (Optional):** You can use the `tool_filter` parameter when creating an `McpToolset` to select a specific subset of tools from the MCP server, rather than exposing all of them to your agent.

The following examples demonstrate how to use `McpToolset` within the `adk web` development environment. For scenarios where you need more fine-grained control over the MCP connection lifecycle or are not using `adk web`, refer to the "Using MCP Tools in your own Agent out of `adk web`" section later in this page.

### Example 1: File System MCP Server[¶](<https://adk.dev/tools-custom/mcp-tools/#example-1-file-system-mcp-server> "Permanent link")

This Python example demonstrates connecting to a local MCP server that provides file system operations.

#### Step 1: Define your Agent with `McpToolset`[¶](<https://adk.dev/tools-custom/mcp-tools/#step-1-define-your-agent-with-mcptoolset> "Permanent link")

Create an `agent.py` file (e.g., in `./adk_agent_samples/mcp_agent/agent.py`). The `McpToolset` is instantiated directly within the `tools` list of your `LlmAgent`.

  * **Important:** Replace `"/path/to/your/folder"` in the `args` list with the **absolute path** to an actual folder on your local system that the MCP server can access.
  * **Important:** Place the `.env` file in the parent directory of the `./adk_agent_samples` directory.

    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-1>)# ./adk_agent_samples/mcp_agent/agent.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-2>)import os # Required for path operations
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-3>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-4>)from google.adk.tools.mcp_tool import McpToolset
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-5>)from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-6>)from mcp import StdioServerParameters
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-7>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-8>)# It's good practice to define paths dynamically if possible,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-9>)# or ensure the user understands the need for an ABSOLUTE path.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-10>)# For this example, we'll construct a path relative to this file,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-11>)# assuming '/path/to/your/folder' is in the same directory as agent.py.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-12>)# REPLACE THIS with an actual absolute path if needed for your setup.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-13>)TARGET_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/path/to/your/folder")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-14>)# Ensure TARGET_FOLDER_PATH is an absolute path for the MCP server.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-15>)# If you created ./adk_agent_samples/mcp_agent/your_folder,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-16>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-17>)root_agent = LlmAgent(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-18>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-19>)    name='filesystem_assistant_agent',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-20>)    instruction='Help the user manage their files. You can list files, read files, etc.',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-21>)    tools=[
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-22>)        McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-23>)            connection_params=StdioConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-24>)                server_params = StdioServerParameters(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-25>)                    command='npx',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-26>)                    args=[
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-27>)                        "-y",  # Argument for npx to auto-confirm install
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-28>)                        "@modelcontextprotocol/server-filesystem",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-29>)                        # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-30>)                        # npx process can access.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-31>)                        # Replace with a valid absolute path on your system.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-32>)                        # For example: "/Users/youruser/accessible_mcp_files"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-33>)                        # or use a dynamically constructed absolute path:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-34>)                        os.path.abspath(TARGET_FOLDER_PATH),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-35>)                    ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-36>)                ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-37>)            ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-38>)            # Optional: Filter which tools from the MCP server are exposed
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-39>)            # tool_filter=['list_directory', 'read_file']
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-40>)        )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-41>)    ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-2-42>))
    
#### Step 2: Create an `__init__.py` file[¶](<https://adk.dev/tools-custom/mcp-tools/#step-2-create-an-__init__py-file> "Permanent link")

Ensure you have an `__init__.py` in the same directory as `agent.py` to make it a discoverable Python package for ADK.
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-3-1>)# ./adk_agent_samples/mcp_agent/__init__.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-3-2>)from . import agent
    
#### Step 3: Run `adk web` and Interact[¶](<https://adk.dev/tools-custom/mcp-tools/#step-3-run-adk-web-and-interact> "Permanent link")

Navigate to the parent directory of `mcp_agent` (e.g., `adk_agent_samples`) in your terminal and run:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-4-1>)cd ./adk_agent_samples # Or your equivalent parent directory
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-4-2>)adk web
    
Note for Windows users

When hitting the `_make_subprocess_transport NotImplementedError`, consider using `adk web --no-reload` instead.

Once the ADK Web UI loads in your browser:

  1. Select the `filesystem_assistant_agent` from the agent dropdown.
  2. Try prompts like:
     * "List files in the current directory."
     * "Can you read the file named sample.txt?" (assuming you created it in `TARGET_FOLDER_PATH`).
     * "What is the content of `another_file.md`?"

You should see the agent interacting with the MCP file system server, and the server's responses (file listings, file content) relayed through the agent. The `adk web` console (terminal where you ran the command) might also show logs from the `npx` process if it outputs to stderr.

![MCP with ADK Web - FileSystem Example](https://adk.dev/assets/adk-tool-mcp-filesystem-adk-web-demo.png)

For Java, refer to the following sample to define an agent that initializes the `McpToolset`:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-1>)package agents;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-2>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-4>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-5>)import com.google.adk.sessions.SessionKey;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-6>)import com.google.adk.tools.mcp.McpToolset;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-7>)import com.google.adk.tools.mcp.StdioServerParameters;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-8>)import com.google.genai.types.Content;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-9>)import com.google.genai.types.Part;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-10>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-11>)import java.util.List;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-12>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-13>)public class McpAgentCreator {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-14>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-15>)    /**
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-16>)     * Initializes an McpToolset, retrieves tools from an MCP server using stdio,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-17>)     * creates an LlmAgent with these tools, sends a prompt to the agent,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-18>)     * and ensures the toolset is closed.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-19>)     * @param args Command line arguments (not used).
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-20>)     */
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-21>)    public static void main(String[] args) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-22>)        //Note: you may have permissions issues if the folder is outside home
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-23>)        String yourFolderPath = "~/path/to/folder";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-24>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-25>)        StdioServerParameters serverParams = StdioServerParameters.builder()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-26>)                .command("npx")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-27>)                .args(List.of(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-28>)                        "-y",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-29>)                        "@modelcontextprotocol/server-filesystem",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-30>)                        yourFolderPath
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-31>)                ))
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-32>)                .build();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-33>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-34>)        try (McpToolset toolset = new McpToolset(serverParams.toServerParameters())) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-35>)            LlmAgent agent = LlmAgent.builder()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-36>)                    .model("gemini-flash-latest")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-37>)                    .name("enterprise_assistant")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-38>)                    .description("An agent to help users access their file systems")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-39>)                    .instruction(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-40>)                            "Help user accessing their file systems. You can list files in a directory."
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-41>)                    )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-42>)                    .tools(toolset)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-43>)                    .build();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-44>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-45>)            System.out.println("Agent created: " + agent.name());
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-46>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-47>)            InMemoryRunner runner = new InMemoryRunner(agent);
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-48>)            String userId = "user123";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-49>)            String sessionId = "1234";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-50>)            String promptText = "Which files are in this directory - " + yourFolderPath + "?";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-51>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-52>)            // Explicitly create the session first
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-53>)            SessionKey sessionKey = runner.sessionService().createSession(runner.appName(), userId, null, sessionId).blockingGet().sessionKey();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-54>)            System.out.println("Session created: " + sessionId + " for user: " + userId);
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-55>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-56>)            Content promptContent = Content.fromParts(Part.fromText(promptText));
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-57>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-58>)            System.out.println("\nSending prompt: \"" + promptText + "\" to agent...\n");
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-59>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-60>)            runner.runAsync(sessionKey, promptContent)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-61>)                    .blockingForEach(event -> {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-62>)                        System.out.println("Event received: " + event.toJson());
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-63>)                    });
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-64>)        } catch (Exception e) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-65>)            System.err.println("An error occurred: " + e.getMessage());
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-66>)            e.printStackTrace();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-67>)        }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-68>)    }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-5-69>)}
    
Assuming a folder containing three files named `first`, `second` and `third`, successful response will look like this:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-6-1>)Event received: {"id":"163a449e-691a-48a2-9e38-8cadb6d1f136","invocationId":"e-c2458c56-e57a-45b2-97de-ae7292e505ef","author":"enterprise_assistant","content":{"parts":[{"functionCall":{"id":"adk-388b4ac2-d40e-4f6a-bda6-f051110c6498","args":{"path":"~/home-test"},"name":"list_directory"}}],"role":"model"},"actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"timestamp":1747377543788}
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-6-2>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-6-3>)Event received: {"id":"8728380b-bfad-4d14-8421-fa98d09364f1","invocationId":"e-c2458c56-e57a-45b2-97de-ae7292e505ef","author":"enterprise_assistant","content":{"parts":[{"functionResponse":{"id":"adk-388b4ac2-d40e-4f6a-bda6-f051110c6498","name":"list_directory","response":{"text_output":[{"text":"[FILE] first\n[FILE] second\n[FILE] third"}]}}}],"role":"user"},"actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"timestamp":1747377544679}
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-6-4>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-6-5>)Event received: {"id":"8fe7e594-3e47-4254-8b57-9106ad8463cb","invocationId":"e-c2458c56-e57a-45b2-97de-ae7292e505ef","author":"enterprise_assistant","content":{"parts":[{"text":"There are three files in the directory: first, second, and third."}],"role":"model"},"actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"timestamp":1747377544689}
    
For Typescript, you can define an agent that initializes the `MCPToolset` as follows:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-1>)import 'dotenv/config';
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-2>)import {LlmAgent, MCPToolset} from "@google/adk";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-3>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-4>)// REPLACE THIS with an actual absolute path for your setup.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-5>)const TARGET_FOLDER_PATH = "/path/to/your/folder";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-6>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-7>)export const rootAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-8>)    model: "gemini-flash-latest",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-9>)    name: "filesystem_assistant_agent",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-10>)    instruction: "Help the user manage their files. You can list files, read files, etc.",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-11>)    tools: [
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-12>)        // To filter tools, pass a list of tool names as the second argument
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-13>)        // to the MCPToolset constructor.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-14>)        // e.g., new MCPToolset(connectionParams, ['list_directory', 'read_file'])
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-15>)        new MCPToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-16>)            {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-17>)                type: "StdioConnectionParams",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-18>)                serverParams: {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-19>)                    command: "npx",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-20>)                    args: [
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-21>)                        "-y",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-22>)                        "@modelcontextprotocol/server-filesystem",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-23>)                        // IMPORTANT: This MUST be an ABSOLUTE path to a folder the
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-24>)                        // npx process can access.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-25>)                        // Replace with a valid absolute path on your system.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-26>)                        // For example: "/Users/youruser/accessible_mcp_files"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-27>)                        TARGET_FOLDER_PATH,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-28>)                    ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-29>)                },
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-30>)            }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-31>)        )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-32>)    ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-7-33>)});
    
### Example 2: Google Maps Grounding Lite MCP Server[¶](<https://adk.dev/tools-custom/mcp-tools/#example-2-google-maps-grounding-lite-mcp-server> "Permanent link")

[Google Maps Platform Grounding Lite](<https://developers.google.com/maps/ai/grounding-lite>) is a service with Model Context Protocol (MCP) support that makes it easy to ground your AI applications with trusted geospatial data from Google Maps. The MCP server provides tools that allow LLMs to access capabilities for places, weather, and routes. You can try out Grounding Lite by enabling it in any tool that supports MCP servers.

Grounding Lite provides tools that allow LLMs to access the following Google Maps capabilities:

  * **Search places:** Request information about places and get AI-generated place data summaries, as well as Place IDs, latitude and longitude coordinates, and Google Maps links for each of the places included in the summary. You can use the returned Place IDs and latitude and longitude coordinates with other Google Maps Platform APIs to show places on a map.
  * **Lookup weather:** Request information about weather and return current conditions, hourly forecasts, and daily forecasts.
  * **Compute routes:** Request information about driving or walking routes between two locations and return route distance and duration information.

#### Step 1: Enable the Maps Grounding Lite service on your Google Cloud project[¶](<https://adk.dev/tools-custom/mcp-tools/#step-1-enable-the-maps-grounding-lite-service-on-your-google-cloud-project> "Permanent link")

  1. [Set up your Google Cloud project](<https://developers.google.com/maps/get-started#create-project>) if you haven’t got one.
  2. In the [Google Cloud Console](<https://console.developers.google.com>), choose the project you want to use for Grounding Lite.
  3. Enable Grounding Lite in the [Google Cloud Console API Library](<https://console.developers.google.com/apis/library/mapstools.googleapis.com>).
  4. [Get a Google Maps Platform API Key](<https://developers.google.com/maps/get-started#api-key>)

#### Step 2: Define your Agent with `McpToolset` for Google Maps Grounding Lite[¶](<https://adk.dev/tools-custom/mcp-tools/#step-2-define-your-agent-with-mcptoolset-for-google-maps-grounding-lite> "Permanent link")

Modify your `agent.py` file (e.g., in `./adk_agent_samples/mcp_agent/agent.py`). Replace `YOUR_GOOGLE_MAPS_API_KEY` with the actual API key you obtained.
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-1>)# ./adk_agent_samples/mcp_agent/agent.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-2>)import os
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-3>)from google.adk.agents.llm_agent import Agent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-4>)from google.adk.tools.mcp_tool import McpToolset
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-5>)from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-6>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-7>)# Retrieve the API key from an environment variable or directly insert it.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-8>)# Using an environment variable is generally safer.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-9>)# Ensure this environment variable is set in the terminal where you run 'adk web'.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-10>)# Example: export GOOGLE_MAPS_API_KEY="YOUR_ACTUAL_KEY"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-11>)GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-12>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-13>)if not GOOGLE_MAPS_API_KEY:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-14>)    # Fallback or direct assignment for testing - NOT RECOMMENDED FOR PRODUCTION
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-15>)    GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY_HERE" # Replace if not using env var
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-16>)    if GOOGLE_MAPS_API_KEY == "YOUR_GOOGLE_MAPS_API_KEY_HERE":
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-17>)        print("WARNING: GOOGLE_MAPS_API_KEY is not set. Please set it as an environment variable or in the script.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-18>)        # You might want to raise an error or exit if the key is crucial and not found.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-19>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-20>)root_agent = Agent(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-21>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-22>)    name='travel_planner_agent',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-23>)    description='A helpful assistant for planning travel routes.',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-24>)    tools=[
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-25>)        McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-26>)            connection_params=StreamableHTTPConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-27>)                url="https://mapstools.googleapis.com/mcp",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-28>)                headers={
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-29>)                    "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-30>)                    "Content-Type": "application/json",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-31>)                    "Accept": "application/json, text/event-stream"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-32>)                }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-33>)            )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-34>)        )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-35>)    ]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-8-36>))
    
#### Step 3: Ensure `__init__.py` Exists[¶](<https://adk.dev/tools-custom/mcp-tools/#step-3-ensure-__init__py-exists> "Permanent link")

If you created this in Example 1, you can skip this. Otherwise, ensure you have an `__init__.py` in the `./adk_agent_samples/mcp_agent/` directory:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-9-1>)# ./adk_agent_samples/mcp_agent/__init__.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-9-2>)from . import agent
    
#### Step 4: Run `adk web` and Interact[¶](<https://adk.dev/tools-custom/mcp-tools/#step-4-run-adk-web-and-interact> "Permanent link")

  1. **Set Environment Variable (Recommended):** Before running `adk web`, it's best to set your Google Maps API key as an environment variable in your terminal: 
         
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-10-1>)export GOOGLE_MAPS_API_KEY="YOUR_ACTUAL_GOOGLE_MAPS_API_KEY"
         
Replace `YOUR_ACTUAL_GOOGLE_MAPS_API_KEY` with your key.

  2. **Run`adk web`**: Navigate to the parent directory of `mcp_agent` (e.g., `adk_agent_samples`) and run: 
         
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-11-1>)cd ./adk_agent_samples # Or your equivalent parent directory
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-11-2>)adk web
         
  3. **Interact in the UI** :

     * Select the `travel_planner_agent`.
     * Try prompts like:
       * "I will be in San Francisco tomorrow. What’s the weather like?"
       * "Find coffee shops near Golden Gate Park."
       * "Get directions from GooglePlex to SFO."

You should see the agent use the Google Maps Grounding Lite MCP tools to provide directions or location-based information.

![Google Maps Grounding Lite MCP with ADK Web Example](https://adk.dev/assets/adk-tool-maps-lite-mcp-adk-web-demo.png)

For Java, refer to the following sample to define an agent that initializes the `McpToolset`:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-1>)package agents;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-2>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-3>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-4>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-5>)import com.google.adk.sessions.SessionKey;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-6>)import com.google.adk.tools.mcp.McpToolset;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-7>)import com.google.adk.tools.mcp.StdioServerParameters;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-8>)import com.google.genai.types.Content;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-9>)import com.google.genai.types.Part;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-10>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-11>)import java.util.HashMap;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-12>)import java.util.Map;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-13>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-14>)public class MapsAgentCreator {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-15>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-16>)    /**
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-17>)     * Initializes an McpToolset for Google Maps Grounding Lite,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-18>)     * creates an LlmAgent, sends a map-related prompt, and closes the toolset.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-19>)     */
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-20>)    public static void main(String[] args) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-21>)        // Read from environment variables
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-22>)        String googleMapsApiKey = System.getenv("GOOGLE_MAPS_API_KEY");
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-23>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-24>)        if (googleMapsApiKey == null || googleMapsApiKey.trim().isEmpty()) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-25>)            // Fallback or direct assignment for testing - NOT RECOMMENDED FOR PRODUCTION
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-26>)            googleMapsApiKey = "YOUR_GOOGLE_MAPS_API_KEY_HERE"; // Replace if not using env var
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-27>)            if ("YOUR_GOOGLE_MAPS_API_KEY_HERE".equals(googleMapsApiKey)) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-28>)                System.out.println("WARNING: GOOGLE_MAPS_API_KEY is not set. Please set it as an environment variable or in the script.");
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-29>)            }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-30>)        }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-31>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-32>)        // Setup the headers for the remote MCP connection
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-33>)        Map<String, String> headers = new HashMap<>();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-34>)        headers.put("X-Goog-Api-Key", googleMapsApiKey);
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-35>)        headers.put("Content-Type", "application/json");
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-36>)        headers.put("Accept", "application/json, text/event-stream");
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-37>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-38>)        // Use StreamableHttpServerParameters for the remote HTTP MCP server connection
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-39>)        StreamableHttpServerParameters serverParams = StreamableHttpServerParameters.builder("https://mapstools.googleapis.com/mcp")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-40>)                .headers(headers)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-41>)                .build();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-42>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-43>)        try (McpToolset toolset = new McpToolset(serverParams)) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-44>)            // Build the Agent with the configured Toolset
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-45>)            LlmAgent agent = LlmAgent.builder()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-46>)                    .model("gemini-flash-latest")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-47>)                    .name("travel_planner_agent")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-48>)                    .description("A helpful assistant for planning travel routes.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-49>)                    .tools(toolset)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-50>)                    .build();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-51>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-52>)            System.out.println("Agent created: " + agent.name());
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-53>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-54>)            // Set up the runner and session
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-55>)            InMemoryRunner runner = new InMemoryRunner(agent);
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-56>)            String userId = "maps-user-" + System.currentTimeMillis();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-57>)            String sessionId = "maps-session-" + System.currentTimeMillis();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-58>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-59>)            String promptText = "Please give me directions to the nearest pharmacy to Madison Square Garden.";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-60>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-61>)            // Explicitly create the session first
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-62>)            SessionKey sessionKey = runner.sessionService().createSession(runner.appName(), userId, null, sessionId).blockingGet().sessionKey();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-63>)            System.out.println("Session created: " + sessionId + " for user: " + userId);
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-64>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-65>)            Content promptContent = Content.fromParts(Part.fromText(promptText));
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-66>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-67>)            System.out.println("\nSending prompt: \"" + promptText + "\" to agent...\n");
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-68>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-69>)            // Execute the prompt asynchronously and print the streamed events
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-70>)            runner.runAsync(sessionKey, promptContent)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-71>)                    .blockingForEach(event -> {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-72>)                        System.out.println("Event received: " + event.toJson());
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-73>)                    });
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-74>)        } catch (Exception e) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-75>)            System.err.println("An error occurred: " + e.getMessage());
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-76>)            e.printStackTrace();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-77>)        }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-78>)    }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-12-79>)}
    
For TypeScript, refer to the following sample to define an agent that initializes the `MCPToolset`:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-1>)import 'dotenv/config';
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-2>)import {LlmAgent, MCPToolset} from "@google/adk";
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-3>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-4>)// Retrieve the API key from an environment variable.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-5>)// Ensure this environment variable is set in the terminal where you run 'adk web'.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-6>)// Example: export GOOGLE_MAPS_API_KEY="YOUR_ACTUAL_KEY"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-7>)const googleMapsApiKey = process.env.GOOGLE_MAPS_API_KEY;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-8>)if (!googleMapsApiKey) {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-9>)    console.warn("WARNING: GOOGLE_MAPS_API_KEY is not set.");
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-10>)    // We throw an error here to prevent the agent from booting without its crucial grounding key
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-11>)    throw new Error('GOOGLE_MAPS_API_KEY is not provided, please run "export GOOGLE_MAPS_API_KEY=YOUR_ACTUAL_KEY" to add that.');
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-12>)}
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-13>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-14>)export const rootAgent = new LlmAgent({
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-15>)    model: "gemini-flash-latest",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-16>)    name: "travel_planner_agent",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-17>)    description: "A helpful assistant for planning travel.",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-18>)    tools: [
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-19>)        new MCPToolset({
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-20>)            // Using SseConnectionParams to connect to the remote Grounding Lite service,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-21>)            // mirroring Python's StreamableHTTPConnectionParams.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-22>)            type: "SseConnectionParams",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-23>)            url: "https://mapstools.googleapis.com/mcp",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-24>)            headers: {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-25>)                "X-Goog-Api-Key": googleMapsApiKey,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-26>)                "Content-Type": "application/json",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-27>)                "Accept": "application/json, text/event-stream"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-28>)            }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-29>)        })
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-30>)    ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-13-31>)});
    
## 2\. Build an MCP server with ADK tools (MCP server exposing ADK)[¶](<https://adk.dev/tools-custom/mcp-tools/#2-build-an-mcp-server-with-adk-tools-mcp-server-exposing-adk> "Permanent link")

This pattern allows you to wrap existing ADK tools and make them available to any standard MCP client application. The example in this section exposes the ADK `load_web_page` tool through a custom-built MCP server.

### Summary of steps[¶](<https://adk.dev/tools-custom/mcp-tools/#summary-of-steps> "Permanent link")

You will create a standard Python MCP server application using the `mcp` library. Within this server, you will:

  1. Instantiate the ADK tool(s) you want to expose (e.g., `FunctionTool(load_web_page)`).
  2. Implement the MCP server's `@app.list_tools()` handler to advertise the ADK tool(s). This involves converting the ADK tool definition to the MCP schema using the `adk_to_mcp_tool_type` utility from `google.adk.tools.mcp_tool.conversion_utils`.
  3. Implement the MCP server's `@app.call_tool()` handler. This handler will:
     * Receive tool call requests from MCP clients.
     * Identify if the request targets one of your wrapped ADK tools.
     * Execute the ADK tool's `.run_async()` method.
     * Format the ADK tool's result into an MCP-compliant response (e.g., `mcp.types.TextContent`).

### Prerequisites[¶](<https://adk.dev/tools-custom/mcp-tools/#prerequisites_1> "Permanent link")

Install the MCP server library in the same Python environment as your ADK installation:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-14-1>)pip install mcp
    
### Step 1: Create the MCP Server Script[¶](<https://adk.dev/tools-custom/mcp-tools/#step-1-create-the-mcp-server-script> "Permanent link")

Create a new Python file for your MCP server, for example, `my_adk_mcp_server.py`.

### Step 2: Implement the Server Logic[¶](<https://adk.dev/tools-custom/mcp-tools/#step-2-implement-the-server-logic> "Permanent link")

Add the following code to `my_adk_mcp_server.py`. This script sets up an MCP server that exposes the ADK `load_web_page` tool.
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-1>)# my_adk_mcp_server.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-2>)import asyncio
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-3>)import json
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-4>)import os
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-5>)from dotenv import load_dotenv
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-6>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-7>)# MCP Server Imports
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-8>)from mcp import types as mcp_types # Use alias to avoid conflict
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-9>)from mcp.server.lowlevel import Server, NotificationOptions
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-10>)from mcp.server.models import InitializationOptions
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-11>)import mcp.server.stdio # For running as a stdio server
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-12>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-13>)# ADK Tool Imports
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-14>)from google.adk.tools.function_tool import FunctionTool
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-15>)from google.adk.tools.load_web_page import load_web_page # Example ADK tool
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-16>)# ADK <-> MCP Conversion Utility
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-17>)from google.adk.tools.mcp_tool.conversion_utils import adk_to_mcp_tool_type
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-18>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-19>)# --- Load Environment Variables (If ADK tools need them, e.g., API keys) ---
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-20>)load_dotenv() # Create a .env file in the same directory if needed
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-21>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-22>)# --- Prepare the ADK Tool ---
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-23>)# Instantiate the ADK tool you want to expose.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-24>)# This tool will be wrapped and called by the MCP server.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-25>)print("Initializing ADK load_web_page tool...")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-26>)adk_tool_to_expose = FunctionTool(load_web_page)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-27>)print(f"ADK tool '{adk_tool_to_expose.name}' initialized and ready to be exposed via MCP.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-28>)# --- End ADK Tool Prep ---
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-29>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-30>)# --- MCP Server Setup ---
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-31>)print("Creating MCP Server instance...")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-32>)# Create a named MCP Server instance using the mcp.server library
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-33>)app = Server("adk-tool-exposing-mcp-server")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-34>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-35>)# Implement the MCP server's handler to list available tools
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-36>)@app.list_tools()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-37>)async def list_mcp_tools() -> list[mcp_types.Tool]:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-38>)    """MCP handler to list tools this server exposes."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-39>)    print("MCP Server: Received list_tools request.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-40>)    # Convert the ADK tool's definition to the MCP Tool schema format
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-41>)    mcp_tool_schema = adk_to_mcp_tool_type(adk_tool_to_expose)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-42>)    print(f"MCP Server: Advertising tool: {mcp_tool_schema.name}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-43>)    return [mcp_tool_schema]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-44>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-45>)# Implement the MCP server's handler to execute a tool call
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-46>)@app.call_tool()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-47>)async def call_mcp_tool(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-48>)    name: str, arguments: dict
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-49>)) -> list[mcp_types.Content]: # MCP uses mcp_types.Content
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-50>)    """MCP handler to execute a tool call requested by an MCP client."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-51>)    print(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-52>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-53>)    # Check if the requested tool name matches our wrapped ADK tool
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-54>)    if name == adk_tool_to_expose.name:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-55>)        try:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-56>)            # Execute the ADK tool's run_async method.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-57>)            # Note: tool_context is None here because this MCP server is
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-58>)            # running the ADK tool outside of a full ADK Runner invocation.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-59>)            # If the ADK tool requires ToolContext features (like state or auth),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-60>)            # this direct invocation might need more sophisticated handling.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-61>)            adk_tool_response = await adk_tool_to_expose.run_async(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-62>)                args=arguments,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-63>)                tool_context=None,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-64>)            )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-65>)            print(f"MCP Server: ADK tool '{name}' executed. Response: {adk_tool_response}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-66>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-67>)            # Format the ADK tool's response (often a dict) into an MCP-compliant format.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-68>)            # Here, we serialize the response dictionary as a JSON string within TextContent.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-69>)            # Adjust formatting based on the ADK tool's output and client needs.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-70>)            response_text = json.dumps(adk_tool_response, indent=2)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-71>)            # MCP expects a list of mcp_types.Content parts
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-72>)            return [mcp_types.TextContent(type="text", text=response_text)]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-73>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-74>)        except Exception as e:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-75>)            print(f"MCP Server: Error executing ADK tool '{name}': {e}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-76>)            # Return an error message in MCP format
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-77>)            error_text = json.dumps({"error": f"Failed to execute tool '{name}': {str(e)}"})
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-78>)            return [mcp_types.TextContent(type="text", text=error_text)]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-79>)    else:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-80>)        # Handle calls to unknown tools
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-81>)        print(f"MCP Server: Tool '{name}' not found/exposed by this server.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-82>)        error_text = json.dumps({"error": f"Tool '{name}' not implemented by this server."})
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-83>)        return [mcp_types.TextContent(type="text", text=error_text)]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-84>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-85>)# --- MCP Server Runner ---
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-86>)async def run_mcp_stdio_server():
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-87>)    """Runs the MCP server, listening for connections over standard input/output."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-88>)    # Use the stdio_server context manager from the mcp.server.stdio library
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-89>)    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-90>)        print("MCP Stdio Server: Starting handshake with client...")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-91>)        await app.run(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-92>)            read_stream,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-93>)            write_stream,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-94>)            InitializationOptions(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-95>)                server_name=app.name, # Use the server name defined above
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-96>)                server_version="0.1.0",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-97>)                capabilities=app.get_capabilities(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-98>)                    # Define server capabilities - consult MCP docs for options
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-99>)                    notification_options=NotificationOptions(),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-100>)                    experimental_capabilities={},
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-101>)                ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-102>)            ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-103>)        )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-104>)        print("MCP Stdio Server: Run loop finished or client disconnected.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-105>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-106>)if __name__ == "__main__":
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-107>)    print("Launching MCP Server to expose ADK tools via stdio...")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-108>)    try:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-109>)        asyncio.run(run_mcp_stdio_server())
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-110>)    except KeyboardInterrupt:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-111>)        print("\nMCP Server (stdio) stopped by user.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-112>)    except Exception as e:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-113>)        print(f"MCP Server (stdio) encountered an error: {e}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-114>)    finally:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-115>)        print("MCP Server (stdio) process exiting.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-15-116>)# --- End MCP Server ---
    
### Step 3: Test your Custom MCP Server with an ADK Agent[¶](<https://adk.dev/tools-custom/mcp-tools/#step-3-test-your-custom-mcp-server-with-an-adk-agent> "Permanent link")

Now, create an ADK agent that will act as a client to the MCP server you just built. This ADK agent will use `McpToolset` to connect to your `my_adk_mcp_server.py` script.

Create an `agent.py` (e.g., in `./adk_agent_samples/mcp_client_agent/agent.py`):
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-1>)# ./adk_agent_samples/mcp_client_agent/agent.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-2>)import os
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-3>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-4>)from google.adk.tools.mcp_tool import McpToolset
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-5>)from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-6>)from mcp import StdioServerParameters
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-7>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-8>)# IMPORTANT: Replace this with the ABSOLUTE path to your my_adk_mcp_server.py script
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-9>)PATH_TO_YOUR_MCP_SERVER_SCRIPT = "/path/to/your/my_adk_mcp_server.py" # <<< REPLACE
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-10>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-11>)if PATH_TO_YOUR_MCP_SERVER_SCRIPT == "/path/to/your/my_adk_mcp_server.py":
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-12>)    print("WARNING: PATH_TO_YOUR_MCP_SERVER_SCRIPT is not set. Please update it in agent.py.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-13>)    # Optionally, raise an error if the path is critical
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-14>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-15>)root_agent = LlmAgent(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-16>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-17>)    name='web_reader_mcp_client_agent',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-18>)    instruction="Use the 'load_web_page' tool to fetch content from a URL provided by the user.",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-19>)    tools=[
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-20>)        McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-21>)            connection_params=StdioConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-22>)                server_params = StdioServerParameters(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-23>)                    command='python3', # Command to run your MCP server script
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-24>)                    args=[PATH_TO_YOUR_MCP_SERVER_SCRIPT], # Argument is the path to the script
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-25>)                )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-26>)            )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-27>)            # tool_filter=['load_web_page'] # Optional: ensure only specific tools are loaded
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-28>)        )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-29>)    ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-16-30>))
    
And an `__init__.py` in the same directory: 
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-17-1>)# ./adk_agent_samples/mcp_client_agent/__init__.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-17-2>)from . import agent
    
**To run the test:**

  1. **Start your custom MCP server (optional, for separate observation):** You can run your `my_adk_mcp_server.py` directly in one terminal to see its logs: 
         
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-18-1>)python3 /path/to/your/my_adk_mcp_server.py
         
It will print "Launching MCP Server..." and wait. The ADK agent (run via `adk web`) will then connect to this process if the `command` in `StdioConnectionParams` is set up to execute it. _(Alternatively,`McpToolset` will start this server script as a subprocess automatically when the agent initializes)._

  2. **Run`adk web` for the client agent:** Navigate to the parent directory of `mcp_client_agent` (e.g., `adk_agent_samples`) and run: 
         
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-19-1>)cd ./adk_agent_samples # Or your equivalent parent directory
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-19-2>)adk web
         
  3. **Interact in the ADK Web UI:**

     * Select the `web_reader_mcp_client_agent`.
     * Try a prompt like: "Load the content from https://example.com"

The ADK agent (`web_reader_mcp_client_agent`) will use `McpToolset` to start and connect to your `my_adk_mcp_server.py`. Your MCP server will receive the `call_tool` request, execute the ADK `load_web_page` tool, and return the result. The ADK agent will then relay this information. You should see logs from both the ADK Web UI (and its terminal) and potentially from your `my_adk_mcp_server.py` terminal if you ran it separately.

This example demonstrates how ADK tools can be encapsulated within an MCP server, making them accessible to a broader range of MCP-compliant clients, not just ADK agents.

Refer to the [documentation](<https://modelcontextprotocol.io/quickstart/server#core-mcp-concepts>), to try it out with Claude Desktop.

## Advanced use cases[¶](<https://adk.dev/tools-custom/mcp-tools/#advanced-use-cases> "Permanent link")

The following sections describe how to handle more advanced use cases with MCP Tools in agents.

### Use MCP Tools without `adk web`[¶](<https://adk.dev/tools-custom/mcp-tools/#use-mcp-tools-without-adk-web> "Permanent link")

This section is relevant to you if:

  * You are developing your own Agent using ADK
  * And, you are **NOT** using `adk web`,
  * And, you are exposing the agent via your own UI

Using MCP Tools requires a different setup than using regular tools, due to the fact that specs for MCP Tools are fetched asynchronously from the MCP Server running remotely, or in another process.

The following example is modified from the "Example 1: File System MCP Server" example above. The main differences are:

  1. Your tool and agent are created asynchronously
  2. You need to properly manage the exit stack, so that your agents and tools are destructed properly when the connection to MCP Server is closed.

    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-1>)# agent.py (modify get_tools_async and other parts as needed)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-2>)# ./adk_agent_samples/mcp_agent/agent.py
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-3>)import os
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-4>)import asyncio
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-5>)from dotenv import load_dotenv
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-6>)from google.genai import types
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-7>)from google.adk.agents.llm_agent import LlmAgent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-8>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-9>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-10>)from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-11>)from google.adk.tools.mcp_tool import McpToolset
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-12>)from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-13>)from mcp import StdioServerParameters
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-14>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-15>)# Load environment variables from .env file in the parent directory
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-16>)# Place this near the top, before using env vars like API keys
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-17>)load_dotenv('../.env')
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-18>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-19>)# Ensure TARGET_FOLDER_PATH is an absolute path for the MCP server.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-20>)TARGET_FOLDER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "/path/to/your/folder")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-21>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-22>)# --- Step 1: Agent Definition ---
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-23>)async def get_agent_async():
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-24>)  """Creates an ADK Agent equipped with tools from the MCP Server."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-25>)  toolset = McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-26>)      # Use StdioConnectionParams for local process communication
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-27>)      connection_params=StdioConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-28>)          server_params = StdioServerParameters(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-29>)            command='npx', # Command to run the server
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-30>)            args=["-y",    # Arguments for the command
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-31>)                "@modelcontextprotocol/server-filesystem",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-32>)                TARGET_FOLDER_PATH],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-33>)          ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-34>)      ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-35>)      tool_filter=['read_file', 'list_directory'] # Optional: filter specific tools
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-36>)      # For remote servers, you would use SseConnectionParams instead:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-37>)      # connection_params=SseConnectionParams(url="http://remote-server:port/path", headers={...})
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-38>)  )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-39>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-40>)  # Use in an agent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-41>)  root_agent = LlmAgent(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-42>)      model='gemini-flash-latest', # Adjust model name if needed based on availability
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-43>)      name='enterprise_assistant',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-44>)      instruction='Help user accessing their file systems',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-45>)      tools=[toolset], # Provide the MCP tools to the ADK agent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-46>)  )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-47>)  return root_agent, toolset
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-48>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-49>)# --- Step 2: Main Execution Logic ---
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-50>)async def async_main():
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-51>)  session_service = InMemorySessionService()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-52>)  # Artifact service might not be needed for this example
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-53>)  artifacts_service = InMemoryArtifactService()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-54>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-55>)  session = await session_service.create_session(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-56>)      state={}, app_name='mcp_filesystem_app', user_id='user_fs'
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-57>)  )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-58>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-59>)  # TODO: Change the query to be relevant to YOUR specified folder.
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-60>)  # e.g., "list files in the 'documents' subfolder" or "read the file 'notes.txt'"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-61>)  query = "list files in the tests folder"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-62>)  print(f"User Query: '{query}'")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-63>)  content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-64>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-65>)  root_agent, toolset = await get_agent_async()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-66>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-67>)  runner = Runner(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-68>)      app_name='mcp_filesystem_app',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-69>)      agent=root_agent,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-70>)      artifact_service=artifacts_service, # Optional
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-71>)      session_service=session_service,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-72>)  )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-73>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-74>)  print("Running agent...")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-75>)  events_async = runner.run_async(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-76>)      session_id=session.id, user_id=session.user_id, new_message=content
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-77>)  )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-78>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-79>)  async for event in events_async:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-80>)    print(f"Event received: {event}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-81>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-82>)  # Cleanup is handled automatically by the agent framework
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-83>)  # But you can also manually close if needed:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-84>)  print("Closing MCP server connection...")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-85>)  await toolset.close()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-86>)  print("Cleanup complete.")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-87>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-88>)if __name__ == '__main__':
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-89>)  try:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-90>)    asyncio.run(async_main())
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-91>)  except Exception as e:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-20-92>)    print(f"An error occurred: {e}")
    
### Handling progress updates[¶](<https://adk.dev/tools-custom/mcp-tools/#handling-progress-updates> "Permanent link")

For long-running tools, `McpToolset` supports a `progress_callback`. This approach allows you to receive real-time updates from the MCP server. You can provide a simple callback function or a factory that creates callbacks with access to the runtime context, such as updating session state.
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-21-1>)async def my_progress_callback(progress: float, total: float, message: str):
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-21-2>)    print(f"Progress: {progress}/{total} - {message}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-21-3>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-21-4>)toolset = McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-21-5>)    connection_params=...,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-21-6>)    progress_callback=my_progress_callback
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-21-7>))
    
## Deploy Agents with MCP Tools[¶](<https://adk.dev/tools-custom/mcp-tools/#deploy-agents-with-mcp-tools> "Permanent link")

When deploying ADK agents that use MCP tools to production environments like Cloud Run, GKE, or Agent Runtime, you need to consider how MCP connections will work in containerized and distributed environments.

### Critical Deployment Requirement: Synchronous Agent Definition[¶](<https://adk.dev/tools-custom/mcp-tools/#critical-deployment-requirement-synchronous-agent-definition> "Permanent link")

**⚠️ Important:** When deploying agents with MCP tools, the agent and its McpToolset must be defined **synchronously** in your `agent.py` file. While `adk web` allows for asynchronous agent creation, deployment environments require synchronous instantiation.
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-1>)# ✅ CORRECT: Synchronous agent definition for deployment
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-2>)import os
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-3>)from google.adk.agents.llm_agent import LlmAgent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-4>)from google.adk.tools.mcp_tool import McpToolset
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-5>)from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-6>)from mcp import StdioServerParameters
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-7>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-8>)_allowed_path = os.path.dirname(os.path.abspath(__file__))
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-9>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-10>)root_agent = LlmAgent(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-11>)    model='gemini-flash-latest',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-12>)    name='enterprise_assistant',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-13>)    instruction=f'Help user accessing their file systems. Allowed directory: {_allowed_path}',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-14>)    tools=[
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-15>)        McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-16>)            connection_params=StdioConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-17>)                server_params=StdioServerParameters(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-18>)                    command='npx',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-19>)                    args=['-y', '@modelcontextprotocol/server-filesystem', _allowed_path],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-20>)                ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-21>)                timeout=5,  # Configure appropriate timeouts
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-22>)            ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-23>)            # Filter tools for security in production
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-24>)            tool_filter=[
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-25>)                'read_file', 'read_multiple_files', 'list_directory',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-26>)                'directory_tree', 'search_files', 'get_file_info',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-27>)                'list_allowed_directories',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-28>)            ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-29>)        )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-30>)    ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-22-31>))
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-23-1>)# ❌ WRONG: Asynchronous patterns don't work in deployment
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-23-2>)async def get_agent():  # This won't work for deployment
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-23-3>)    toolset = await create_mcp_toolset_async()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-23-4>)    return LlmAgent(tools=[toolset])
    
### Quick Deployment Commands[¶](<https://adk.dev/tools-custom/mcp-tools/#quick-deployment-commands> "Permanent link")

#### Agent Runtime[¶](<https://adk.dev/tools-custom/mcp-tools/#agent-runtime> "Permanent link")
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-24-1>)uv run adk deploy agent_engine \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-24-2>)  --project=<your-gcp-project-id> \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-24-3>)  --region=<your-gcp-region> \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-24-4>)  --staging_bucket="gs://<your-gcs-bucket>" \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-24-5>)  --display_name="My MCP Agent" \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-24-6>)  ./path/to/your/agent_directory
    
#### Cloud Run[¶](<https://adk.dev/tools-custom/mcp-tools/#cloud-run> "Permanent link")
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-25-1>)uv run adk deploy cloud_run \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-25-2>)  --project=<your-gcp-project-id> \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-25-3>)  --region=<your-gcp-region> \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-25-4>)  --service_name=<your-service-name> \
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-25-5>)  ./path/to/your/agent_directory
    
### Deployment Patterns[¶](<https://adk.dev/tools-custom/mcp-tools/#deployment-patterns> "Permanent link")

#### Pattern 1: Self-Contained Stdio MCP Servers[¶](<https://adk.dev/tools-custom/mcp-tools/#pattern-1-self-contained-stdio-mcp-servers> "Permanent link")

For MCP servers that can be packaged as npm packages or Python modules (like `@modelcontextprotocol/server-filesystem`), you can include them directly in your agent container:

**Container Requirements:**
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-1>)# Example for npm-based MCP servers
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-2>)FROM python:3.13-slim
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-3>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-4>)# Install Node.js and npm for MCP servers
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-5>)RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-6>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-7>)# Install your Python dependencies
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-8>)COPY requirements.txt .
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-9>)RUN pip install -r requirements.txt
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-10>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-11>)# Copy your agent code
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-12>)COPY . .
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-13>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-14>)# Your agent can now use StdioConnectionParams with 'npx' commands
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-26-15>)CMD ["python", "main.py"]
    
**Agent Configuration:**
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-1>)# This works in containers because npx and the MCP server run in the same environment
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-2>)McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-3>)    connection_params=StdioConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-4>)        server_params=StdioServerParameters(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-5>)            command='npx',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-6>)            args=["-y", "@modelcontextprotocol/server-filesystem", "/app/data"],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-7>)        ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-8>)    ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-27-9>))
    
#### Pattern 2: Remote MCP Servers (Streamable HTTP)[¶](<https://adk.dev/tools-custom/mcp-tools/#pattern-2-remote-mcp-servers-streamable-http> "Permanent link")

For production deployments requiring scalability, deploy MCP servers as separate services and connect via Streamable HTTP:

**MCP Server Deployment (Cloud Run):**
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-1>)# deploy_mcp_server.py - Separate Cloud Run service using Streamable HTTP
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-2>)import contextlib
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-3>)import logging
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-4>)from collections.abc import AsyncIterator
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-5>)from typing import Any
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-6>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-7>)import anyio
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-8>)import click
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-9>)import mcp.types as types
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-10>)from mcp.server.lowlevel import Server
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-11>)from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-12>)from starlette.applications import Starlette
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-13>)from starlette.routing import Mount
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-14>)from starlette.types import Receive, Scope, Send
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-15>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-16>)logger = logging.getLogger(__name__)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-17>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-18>)def create_mcp_server():
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-19>)    """Create and configure the MCP server."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-20>)    app = Server("adk-mcp-streamable-server")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-21>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-22>)    @app.call_tool()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-23>)    async def call_tool(name: str, arguments: dict[str, Any]) -> list[types.ContentBlock]:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-24>)        """Handle tool calls from MCP clients."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-25>)        # Example tool implementation - replace with your actual ADK tools
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-26>)        if name == "example_tool":
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-27>)            result = arguments.get("input", "No input provided")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-28>)            return [
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-29>)                types.TextContent(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-30>)                    type="text",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-31>)                    text=f"Processed: {result}"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-32>)                )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-33>)            ]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-34>)        else:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-35>)            raise ValueError(f"Unknown tool: {name}")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-36>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-37>)    @app.list_tools()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-38>)    async def list_tools() -> list[types.Tool]:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-39>)        """List available tools."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-40>)        return [
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-41>)            types.Tool(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-42>)                name="example_tool",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-43>)                description="Example tool for demonstration",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-44>)                inputSchema={
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-45>)                    "type": "object",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-46>)                    "properties": {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-47>)                        "input": {
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-48>)                            "type": "string",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-49>)                            "description": "Input text to process"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-50>)                        }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-51>)                    },
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-52>)                    "required": ["input"]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-53>)                }
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-54>)            )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-55>)        ]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-56>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-57>)    return app
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-58>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-59>)def main(port: int = 8080, json_response: bool = False):
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-60>)    """Main server function."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-61>)    logging.basicConfig(level=logging.INFO)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-62>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-63>)    app = create_mcp_server()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-64>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-65>)    # Create session manager with stateless mode for scalability
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-66>)    session_manager = StreamableHTTPSessionManager(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-67>)        app=app,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-68>)        event_store=None,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-69>)        json_response=json_response,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-70>)        stateless=True,  # Important for Cloud Run scalability
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-71>)    )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-72>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-73>)    async def handle_streamable_http(scope: Scope, receive: Receive, send: Send) -> None:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-74>)        await session_manager.handle_request(scope, receive, send)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-75>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-76>)    @contextlib.asynccontextmanager
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-77>)    async def lifespan(app: Starlette) -> AsyncIterator[None]:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-78>)        """Manage session manager lifecycle."""
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-79>)        async with session_manager.run():
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-80>)            logger.info("MCP Streamable HTTP server started!")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-81>)            try:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-82>)                yield
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-83>)            finally:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-84>)                logger.info("MCP server shutting down...")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-85>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-86>)    # Create ASGI application
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-87>)    starlette_app = Starlette(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-88>)        debug=False,  # Set to False for production
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-89>)        routes=[
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-90>)            Mount("/mcp", app=handle_streamable_http),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-91>)        ],
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-92>)        lifespan=lifespan,
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-93>)    )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-94>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-95>)    import uvicorn
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-96>)    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-97>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-98>)if __name__ == "__main__":
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-28-99>)    main()
    
**Agent Configuration for Remote MCP:**

PythonJava
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-29-1>)# Your ADK agent connects to the remote MCP service via Streamable HTTP
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-29-2>)McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-29-3>)    connection_params=StreamableHTTPConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-29-4>)        url="https://your-mcp-server-url.run.app/mcp",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-29-5>)        headers={"Authorization": "Bearer your-auth-token"}
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-29-6>)    ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-29-7>))
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-1>)import java.util.Map;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-2>)import com.google.adk.tools.mcp.StreamableHttpServerParameters;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-3>)import com.google.adk.tools.mcp.McpToolset;
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-4>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-5>)// Your ADK agent connects to the remote MCP service via Streamable HTTP
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-6>)StreamableHttpServerParameters streamableParams = StreamableHttpServerParameters.builder()
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-7>)        .url("https://your-mcp-server-url.run.app/mcp")
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-8>)        .headers(Map.of("Authorization", "Bearer your-auth-token"))
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-9>)        .build();
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-10>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-30-11>)McpToolset toolset = new McpToolset(streamableParams);
    
#### Pattern 3: Sidecar MCP Servers (GKE)[¶](<https://adk.dev/tools-custom/mcp-tools/#pattern-3-sidecar-mcp-servers-gke> "Permanent link")

In Kubernetes environments, you can deploy MCP servers as sidecar containers:
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-1>)# deployment.yaml - GKE with MCP sidecar
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-2>)apiVersion: apps/v1
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-3>)kind: Deployment
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-4>)metadata:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-5>)  name: adk-agent-with-mcp
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-6>)spec:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-7>)  template:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-8>)    spec:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-9>)      containers:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-10>)      # Main ADK agent container
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-11>)      - name: adk-agent
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-12>)        image: your-adk-agent:latest
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-13>)        ports:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-14>)        - containerPort: 8080
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-15>)        env:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-16>)        - name: MCP_SERVER_URL
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-17>)          value: "http://localhost:8081"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-18>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-19>)      # MCP server sidecar
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-20>)      - name: mcp-server
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-21>)        image: your-mcp-server:latest
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-22>)        ports:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-31-23>)        - containerPort: 8081
    
### Connection Management Considerations[¶](<https://adk.dev/tools-custom/mcp-tools/#connection-management-considerations> "Permanent link")

#### Stdio Connections[¶](<https://adk.dev/tools-custom/mcp-tools/#stdio-connections> "Permanent link")

  * **Pros:** Simple setup, process isolation, works well in containers
  * **Cons:** Process overhead, not suitable for high-scale deployments
  * **Best for:** Development, single-tenant deployments, simple MCP servers

#### SSE/HTTP Connections[¶](<https://adk.dev/tools-custom/mcp-tools/#ssehttp-connections> "Permanent link")

  * **Pros:** Network-based, scalable, can handle multiple clients
  * **Cons:** Requires network infrastructure, authentication complexity
  * **Best for:** Production deployments, multi-tenant systems, external MCP services

### Production Deployment Checklist[¶](<https://adk.dev/tools-custom/mcp-tools/#production-deployment-checklist> "Permanent link")

When deploying agents with MCP tools to production:

**✅ Connection Lifecycle** \- Ensure proper cleanup of MCP connections using exit_stack patterns \- Configure appropriate timeouts for connection establishment and requests \- Implement retry logic for transient connection failures

**✅ Resource Management** \- Monitor memory usage for stdio MCP servers (each spawns a process) \- Configure appropriate CPU/memory limits for MCP server processes \- Consider connection pooling for remote MCP servers

**✅ Security** \- Use authentication headers for remote MCP connections \- Restrict network access between ADK agents and MCP servers \- **Filter MCP tools using`tool_filter` to limit exposed functionality** \- Validate MCP tool inputs to prevent injection attacks \- Use restrictive file paths for filesystem MCP servers (e.g., `os.path.dirname(os.path.abspath(__file__))`) \- Consider read-only tool filters for production environments

**✅ Monitoring & Observability** \- Log MCP connection establishment and teardown events \- Monitor MCP tool execution times and success rates \- Set up alerts for MCP connection failures

**✅ Scalability** \- For high-volume deployments, prefer remote MCP servers over stdio \- Configure session affinity if using stateful MCP servers \- Consider MCP server connection limits and implement circuit breakers

### Environment-Specific Configurations[¶](<https://adk.dev/tools-custom/mcp-tools/#environment-specific-configurations> "Permanent link")

#### Cloud Run[¶](<https://adk.dev/tools-custom/mcp-tools/#cloud-run_1> "Permanent link")
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-1>)# Cloud Run environment variables for MCP configuration
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-2>)import os
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-3>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-4>)# Detect Cloud Run environment
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-5>)if os.getenv('K_SERVICE'):
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-6>)    # Use remote MCP servers in Cloud Run
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-7>)    mcp_connection = SseConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-8>)        url=os.getenv('MCP_SERVER_URL'),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-9>)        headers={'Authorization': f"Bearer {os.getenv('MCP_AUTH_TOKEN')}"}
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-10>)    )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-11>)else:
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-12>)    # Use stdio for local development
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-13>)    mcp_connection = StdioConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-14>)        server_params=StdioServerParameters(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-15>)            command='npx',
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-16>)            args=["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-17>)        )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-18>)    )
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-19>)
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-32-20>)McpToolset(connection_params=mcp_connection)
    
#### GKE[¶](<https://adk.dev/tools-custom/mcp-tools/#gke> "Permanent link")
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-33-1>)# GKE-specific MCP configuration
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-33-2>)# Use service discovery for MCP servers within the cluster
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-33-3>)McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-33-4>)    connection_params=SseConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-33-5>)        url="http://mcp-service.default.svc.cluster.local:8080/sse"
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-33-6>)    ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-33-7>))
    
#### Agent Runtime[¶](<https://adk.dev/tools-custom/mcp-tools/#agent-runtime_1> "Permanent link")
    
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-1>)# Agent Runtime managed deployment
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-2>)# Prefer lightweight, self-contained MCP servers or external services
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-3>)McpToolset(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-4>)    connection_params=SseConnectionParams(
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-5>)        url="https://your-managed-mcp-service.googleapis.com/sse",
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-6>)        headers={'Authorization': 'Bearer $(gcloud auth print-access-token)'}
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-7>)    ),
    [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-34-8>))
    
### Troubleshooting Deployment Issues[¶](<https://adk.dev/tools-custom/mcp-tools/#troubleshooting-deployment-issues> "Permanent link")

**Common MCP Deployment Problems:**

  1. **Stdio Process Startup Failures**
         
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-1>)# Debug stdio connection issues
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-2>)McpToolset(
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-3>)    connection_params=StdioConnectionParams(
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-4>)        server_params=StdioServerParameters(
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-5>)            command='npx',
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-6>)            args=["-y", "@modelcontextprotocol/server-filesystem", "/app/data"],
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-7>)            # Add environment debugging
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-8>)            env={'DEBUG': '1'}
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-9>)        ),
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-10>)    ),
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-35-11>))
         
  2. **Network Connectivity Issues**
         
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-36-1>)# Test remote MCP connectivity
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-36-2>)import aiohttp
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-36-3>)
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-36-4>)async def test_mcp_connection():
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-36-5>)    async with aiohttp.ClientSession() as session:
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-36-6>)        async with session.get('https://your-mcp-server.com/health') as resp:
         [](<https://adk.dev/tools-custom/mcp-tools/#__codelineno-36-7>)            print(f"MCP Server Health: {resp.status}")
         
  3. **Resource Exhaustion**

  4. Monitor container memory usage when using stdio MCP servers
  5. Set appropriate limits in Kubernetes deployments
  6. Use remote MCP servers for resource-intensive operations

## Further Resources[¶](<https://adk.dev/tools-custom/mcp-tools/#further-resources> "Permanent link")

  * [Model Context Protocol Documentation](<https://modelcontextprotocol.io/>)
  * [MCP Specification](<https://modelcontextprotocol.io/specification/>)
  * [MCP Python SDK & Examples](<https://github.com/modelcontextprotocol/>)

Back to top 