# Code with AI - Agent Development Kit (ADK)

> Source: [https://adk.dev/tutorials/coding-with-ai/](https://adk.dev/tutorials/coding-with-ai/)

[ Skip to content ](<https://adk.dev/tutorials/coding-with-ai/#coding-with-ai>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tutorials/coding-with-ai.md> "Edit this page on GitHub") [ ](<https://adk.dev/tutorials/coding-with-ai/index.md> "View this page as Markdown")

# Coding with AI[¶](<https://adk.dev/tutorials/coding-with-ai/#coding-with-ai> "Permanent link")

You can use AI coding assistants to build agents with Agent Development Kit (ADK). Give your coding agent ADK expertise by installing development skills into your project, or by connecting it to ADK documentation through an MCP server.

  * [**Agents CLI in Agent Platform**](<https://adk.dev/tutorials/coding-with-ai/#agents-cli>): Command-line tool and coding skills for ADK development.
  * [**ADK Docs MCP Server**](<https://adk.dev/tutorials/coding-with-ai/#adk-docs-mcp-server>): Connect your coding tool to ADK documentation through an MCP server.
  * [**ADK Docs Index**](<https://adk.dev/tutorials/coding-with-ai/#adk-docs-index>): Machine-readable documentation files following the `llms.txt` standard.

## Agents CLI[¶](<https://adk.dev/tutorials/coding-with-ai/#agents-cli> "Permanent link")

The [Agents CLI](<https://google.github.io/agents-cli/>) tool set lets you plug ADK agent expertise into your favorite AI-coding environments including Antigravity, Claude Code, Cursor, and other AI coding tools. Install Agents CLI into your current AI-powered development environment to scaffold, build, test, evaluate, and deploy ADK agents. Enable your development environment with these Agents CLI Skills:

  * Development lifecycle and coding guidelines
  * Project scaffolding
  * Evaluation methodology and scoring
  * Agent Runtime, Cloud Run, and GKE deployment
  * Gemini Enterprise agent publishing
  * Trace, logging, and integrations
  * Python API quick reference and docs index

To install Agents CLI and set up ADK development skills:
    
    [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-0-1>)uvx google-agents-cli setup
    
For more information on installing Agents CLI and using it in your development environment, see the [Agents CLI documentation](<https://google.github.io/agents-cli/>).

## ADK Docs MCP Server[¶](<https://adk.dev/tutorials/coding-with-ai/#adk-docs-mcp-server> "Permanent link")

You can configure your coding tool to search and read ADK documentation using an MCP server. Below are setup instructions for popular tools.

### Antigravity[¶](<https://adk.dev/tutorials/coding-with-ai/#antigravity> "Permanent link")

To add the ADK docs MCP server to [Antigravity](<https://antigravity.google/>) (requires [`uv`](<https://docs.astral.sh/uv/>)):

  1. Open the MCP store via the **...** (more) menu at the top of the editor's agent panel.
  2. Click on **Manage MCP Servers** then **View raw config**.
  3. Add the following to `mcp_config.json`:
         
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-1>){
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-2>)  "mcpServers": {
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-3>)    "adk-docs-mcp": {
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-4>)      "command": "uvx",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-5>)      "args": [
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-6>)        "--from",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-7>)        "mcpdoc",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-8>)        "mcpdoc",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-9>)        "--urls",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-10>)        "AgentDevelopmentKit:https://adk.dev/llms.txt",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-11>)        "--transport",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-12>)        "stdio"
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-13>)      ]
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-14>)    }
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-15>)  }
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-1-16>)}
         
### Claude Code[¶](<https://adk.dev/tutorials/coding-with-ai/#claude-code> "Permanent link")

To add the ADK docs MCP server to [Claude Code](<https://code.claude.com/docs/en/overview>):
    
    [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-2-1>)claude mcp add adk-docs --transport stdio -- uvx --from mcpdoc mcpdoc --urls AgentDevelopmentKit:https://adk.dev/llms.txt --transport stdio
    
### Cursor[¶](<https://adk.dev/tutorials/coding-with-ai/#cursor> "Permanent link")

To add the ADK docs MCP server to [Cursor](<https://cursor.com/>) (requires [`uv`](<https://docs.astral.sh/uv/>)):

  1. Open **Cursor Settings** and navigate to the **Tools & MCP** tab.
  2. Click on **New MCP Server** , which will open `mcp.json` for editing.
  3. Add the following to `mcp.json`:
         
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-1>){
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-2>)  "mcpServers": {
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-3>)    "adk-docs-mcp": {
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-4>)      "command": "uvx",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-5>)      "args": [
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-6>)        "--from",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-7>)        "mcpdoc",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-8>)        "mcpdoc",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-9>)        "--urls",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-10>)        "AgentDevelopmentKit:https://adk.dev/llms.txt",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-11>)        "--transport",
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-12>)        "stdio"
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-13>)      ]
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-14>)    }
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-15>)  }
         [](<https://adk.dev/tutorials/coding-with-ai/#__codelineno-3-16>)}
         
### Other Tools[¶](<https://adk.dev/tutorials/coding-with-ai/#other-tools> "Permanent link")

Any coding tool that supports MCP servers can use the same server configuration shown above. Adapt the JSON example from the Antigravity or Cursor sections for your tool's MCP settings.

## ADK Docs Index[¶](<https://adk.dev/tutorials/coding-with-ai/#adk-docs-index> "Permanent link")

The ADK documentation is available as machine-readable files following the [`llms.txt` standard](<https://llmstxt.org/>). These files are generated with every documentation update and are always up to date.

File | Description | URL  
---|---|---  
`llms.txt` | Documentation index with links | [`adk.dev/llms.txt`](<https://adk.dev/llms.txt>)  
`llms-full.txt` | Full documentation in a single file | [`adk.dev/llms-full.txt`](<https://adk.dev/llms-full.txt>)  
  
Back to top 