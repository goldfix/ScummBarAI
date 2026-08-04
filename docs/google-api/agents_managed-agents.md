# Managed agents - Agent Development Kit (ADK)

> Source: [https://adk.dev/agents/managed-agents/](https://adk.dev/agents/managed-agents/)

[ Skip to content ](<https://adk.dev/agents/managed-agents/#managed-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/agents/managed-agents.md> "Edit this page on GitHub") [ ](<https://adk.dev/agents/managed-agents/index.md> "View this page as Markdown")

# Managed agents[¶](<https://adk.dev/agents/managed-agents/#managed-agents> "Permanent link")

Supported in ADKPython v2.4.0Preview

Managed agents let you use Google's first-party, out-of-the-box agents, backed by the Managed Agents API, from within your ADK flows. Managed agents are available through the [Gemini API](<https://ai.google.dev/gemini-api/docs/agents>) and [Agent Platform](<https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents>). The `ManagedAgent` class connects to a managed agent (such as the Antigravity agent) that runs in a specialized, server-side execution environment, so you get powerful built-in capabilities without managing sandboxes or writing client-side function declarations.

`ManagedAgent` implements the same `BaseAgent` contract as other ADK agents, so you can use it standalone or drop it directly into an ADK flow. It is a good fit when you want a robust, server-hosted agent with specialized built-in tools rather than building and operating that environment yourself.

## What are managed agents?[¶](<https://adk.dev/agents/managed-agents/#what-are-managed-agents> "Permanent link")

A _managed agent_ is an agent whose reasoning, tools, and execution environment are hosted and operated by Google through the Managed Agents API, rather than run by your own ADK process. Instead of issuing standard `generate_content` calls, `ManagedAgent` creates server-side _interactions_ and streams the results back into your ADK flow. Managed agents provide several built-in advantages:

  * **First-party, out-of-the-box agents:** Connect to ready-made agents (for example, the Antigravity agent) by referencing their `agent_id`.
  * **Built-in, server-side execution:** Capabilities such as web search and code execution run in a managed sandbox on the server, with no local sandbox to provision or secure.
  * **No client-side function declarations:** Server-side tools are configured on the managed agent, so you don't declare or execute them locally.

## When to use managed agents vs. building your own[¶](<https://adk.dev/agents/managed-agents/#when-to-use-managed-agents-vs-building-your-own> "Permanent link")

Managed agents and ADK agents solve different problems. Choosing between them is mostly a trade-off between out-of-the-box power and fine-grained control.

  * **Managed agents** give you a powerful agent out of the box, but with limited flexibility. The toolset is predefined and server-side, the agent runs only in the managed environment, and client-side or MCP tools are not supported.
  * **ADK agents** (such as [`LlmAgent`](<https://adk.dev/agents/llm-agents/>)) give you fine-grained control over the model, instructions, tools (including custom function tools and MCP tools), and where execution happens.

## Prerequisites[¶](<https://adk.dev/agents/managed-agents/#prerequisites> "Permanent link")

`ManagedAgent` supports two backends. Complete the prerequisites for the backend you plan to use: obtain credentials and an `agent_id`.

### Gemini API backend[¶](<https://adk.dev/agents/managed-agents/#gemini-api-backend> "Permanent link")

  * **Authentication:** Obtain a Gemini API key and set it as the `GEMINI_API_KEY` environment variable.
  * **Agent ID:** You need an `agent_id` to connect to. You can either:
    * Create a new agent by following the [Gemini API Agents documentation](<https://ai.google.dev/gemini-api/docs/agents>).
    * Use an out-of-the-box agent ID, such as `antigravity-preview-05-2026`, which is used in the examples below.

### Agent Platform backend[¶](<https://adk.dev/agents/managed-agents/#agent-platform-backend> "Permanent link")

  * **Authentication:** Agent Platform requires Google Cloud credentials. Follow the [Agent Platform setup instructions](<https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents/create-manage#before-you-begin>) to authenticate your local environment (for example, with `gcloud auth application-default login`).
  * **Location:** The Managed Agents API is served only from the `global` location. `ManagedAgent` enforces a connection to `global` on the Agent Platform backend.
  * **Agent ID:** As with the Gemini API, you need an `agent_id`. Create one using the [Create and manage agents guide](<https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents/create-manage>), or use an out-of-the-box agent ID available to your project.

## Get started[¶](<https://adk.dev/agents/managed-agents/#get-started> "Permanent link")

The following example creates two managed agents: one that answers questions using web search, and one that solves computational questions by running code server-side. Both run their tools in the managed environment (`environment={'type': 'remote'}`).

Python
    
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-1>)import os
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-2>)from google.adk.agents import ManagedAgent
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-3>)from google.adk.tools import google_search
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-4>)from google.genai import types
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-5>)
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-6>)# Ensure you have the MANAGED_AGENT_ID and the proper environment config
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-7>)_AGENT_ID = os.environ.get('MANAGED_AGENT_ID', 'antigravity-preview-05-2026')
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-8>)
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-9>)managed_search_agent = ManagedAgent(
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-10>)    name='managed_search_agent',
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-11>)    description='Answers questions that need fresh, grounded information from the web.',
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-12>)    agent_id=_AGENT_ID,
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-13>)    environment={'type': 'remote'},
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-14>)    tools=[google_search],
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-15>))
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-16>)
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-17>)# A managed code execution agent using raw types.Tool
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-18>)managed_code_execution_agent = ManagedAgent(
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-19>)    name='managed_code_execution_agent',
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-20>)    description='Solves computational questions by running code server-side.',
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-21>)    agent_id=_AGENT_ID,
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-22>)    environment={'type': 'remote'},
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-23>)    tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    [](<https://adk.dev/agents/managed-agents/#__codelineno-0-24>))
    
## How it works[¶](<https://adk.dev/agents/managed-agents/#how-it-works> "Permanent link")

When you invoke a `ManagedAgent`, ADK sends your request to the managed agent via the [Interactions API](<https://ai.google.dev/gemini-api/docs/interactions-overview>) and streams the results, both partial and final, back into your ADK flow in real time. The reasoning, tools, and execution all run in Google's managed environment rather than in your ADK process.

How `ManagedAgent` maps to the Managed Agents API

An ADK `ManagedAgent` does not create or register a new managed agent resource. It connects to an agent that already exists on the backend (the one named by `agent_id`) and applies its configuration (such as `tools` and `environment`) as per-interaction overrides at runtime. In Managed Agents API terms, ADK works entirely on the _data plane_ (the Interactions API) and leaves the _control plane_ (the Agents API, which creates and manages agent resources) untouched. For how these two planes differ, see the [Managed Agents API system architecture](<https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents>).

### Local session vs. remote state[¶](<https://adk.dev/agents/managed-agents/#local-session-vs-remote-state> "Permanent link")

`ManagedAgent` keeps almost no state locally. The ADK session persists only two values on the events it emits: the `previous_interaction_id` and the sandbox `environment_id`. On each new turn the agent recovers both by scanning prior session events, then reuses them so the conversation and its sandbox continue.

Everything else lives server-side. The Managed Agents API owns the sandbox environment and the full interaction history, and that remote interaction, not the local session, is the source of truth for continuing a conversation. Response text appears in both the local ADK events and the remote interaction history, but ADK stores only the IDs it needs to recover and reuse the remote state; it never re-sends prior turns.

## Limitations[¶](<https://adk.dev/agents/managed-agents/#limitations> "Permanent link")

  * **Location pinned (Agent Platform only):** For the Agent Platform backend, the Managed Agents API is currently served only from the `global` location. Regional endpoints raise an error.
  * **Server-side tools only:** Client-executed tools (Python functions, callables) and MCP tools are not supported and raise a `NotImplementedError`.
  * **Streaming only:** The agent uses streaming interactions (`stream=True`). Background-polling execution and strictly non-streaming connections are not yet fully supported.
  * **Backend differences:** The Gemini API and Agent Platform backends currently exhibit slightly different behavioral patterns. Test against the specific backend you intend to use.

## Next steps[¶](<https://adk.dev/agents/managed-agents/#next-steps> "Permanent link")

  * **Samples:** [Managed Agent Basic](<https://github.com/google/adk-python/tree/main/contributing/samples/managed_agent/basic>) and [Managed Agent Code Execution](<https://github.com/google/adk-python/tree/main/contributing/samples/managed_agent/code_execution>).
  * **Backend documentation:** [Gemini API Agents](<https://ai.google.dev/gemini-api/docs/agents>) and [Agent Platform Managed Agents](<https://docs.cloud.google.com/gemini-enterprise-agent-platform/build/managed-agents>).
  * **Related ADK topics:** [Models for agents](<https://adk.dev/agents/models/>), [Multi-agent workflows](<https://adk.dev/workflows/>), and [Custom tools](<https://adk.dev/tools-custom/>).

Back to top 