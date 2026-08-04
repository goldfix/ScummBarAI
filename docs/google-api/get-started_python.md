# Python - Agent Development Kit (ADK)

> Source: [https://adk.dev/get-started/python/](https://adk.dev/get-started/python/)

[ Skip to content ](<https://adk.dev/get-started/python/#python-quickstart-for-adk>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/get-started/python.md> "Edit this page on GitHub") [ ](<https://adk.dev/get-started/python/index.md> "View this page as Markdown")

# Python Quickstart for ADK[¶](<https://adk.dev/get-started/python/#python-quickstart-for-adk> "Permanent link")

This guide shows you how to get up and running with Agent Development Kit (ADK) for Python. Before you start, make sure you have the following installed:

  * Python 3.10 or later
  * `pip` for installing packages

## Installation[¶](<https://adk.dev/get-started/python/#installation> "Permanent link")

Install ADK by running the following command:
    
    [](<https://adk.dev/get-started/python/#__codelineno-0-1>)pip install google-adk
    
Recommended: create and activate a Python virtual environment

Create a Python virtual environment:
    
    [](<https://adk.dev/get-started/python/#__codelineno-1-1>)python3 -m venv .venv
    
Activate the Python virtual environment:

Windows Command PromptWindows PowerShellMacOS / Linux
    
    [](<https://adk.dev/get-started/python/#__codelineno-2-1>).venv\Scripts\activate.bat
    
    [](<https://adk.dev/get-started/python/#__codelineno-3-1>).venv\Scripts\Activate.ps1
    
    [](<https://adk.dev/get-started/python/#__codelineno-4-1>)source .venv/bin/activate
    
## Create an agent project[¶](<https://adk.dev/get-started/python/#create-an-agent-project> "Permanent link")

Run the `adk create` command to start a new agent project.
    
    [](<https://adk.dev/get-started/python/#__codelineno-5-1>)adk create my_agent
    
### Explore the agent project[¶](<https://adk.dev/get-started/python/#explore-the-agent-project> "Permanent link")

The created agent project has the following structure, with the `agent.py` file containing the main control code for the agent.
    
    [](<https://adk.dev/get-started/python/#__codelineno-6-1>)my_agent/
    [](<https://adk.dev/get-started/python/#__codelineno-6-2>)    agent.py      # main agent code
    [](<https://adk.dev/get-started/python/#__codelineno-6-3>)    .env          # API keys or project IDs
    [](<https://adk.dev/get-started/python/#__codelineno-6-4>)    __init__.py
    
## Update your agent project[¶](<https://adk.dev/get-started/python/#update-your-agent-project> "Permanent link")

The `agent.py` file contains a `root_agent` definition which is the only required element of an ADK agent. You can also define tools for the agent to use. Update the generated `agent.py` code to include a `get_current_time` tool for use by the agent, as shown in the following code:
    
    [](<https://adk.dev/get-started/python/#__codelineno-7-1>)from google.adk.agents.llm_agent import Agent
    [](<https://adk.dev/get-started/python/#__codelineno-7-2>)
    [](<https://adk.dev/get-started/python/#__codelineno-7-3>)# Mock tool implementation
    [](<https://adk.dev/get-started/python/#__codelineno-7-4>)def get_current_time(city: str) -> dict:
    [](<https://adk.dev/get-started/python/#__codelineno-7-5>)    """Returns the current time in a specified city."""
    [](<https://adk.dev/get-started/python/#__codelineno-7-6>)    return {"status": "success", "city": city, "time": "10:30 AM"}
    [](<https://adk.dev/get-started/python/#__codelineno-7-7>)
    [](<https://adk.dev/get-started/python/#__codelineno-7-8>)root_agent = Agent(
    [](<https://adk.dev/get-started/python/#__codelineno-7-9>)    model='gemini-flash-latest',
    [](<https://adk.dev/get-started/python/#__codelineno-7-10>)    name='root_agent',
    [](<https://adk.dev/get-started/python/#__codelineno-7-11>)    description="Tells the current time in a specified city.",
    [](<https://adk.dev/get-started/python/#__codelineno-7-12>)    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    [](<https://adk.dev/get-started/python/#__codelineno-7-13>)    tools=[get_current_time],
    [](<https://adk.dev/get-started/python/#__codelineno-7-14>))
    
### Set your API key[¶](<https://adk.dev/get-started/python/#set-your-api-key> "Permanent link")

This project uses the Gemini API, which requires an API key. If you don't already have Gemini API key, create a key in Google AI Studio on the [API Keys](<https://aistudio.google.com/app/apikey>) page.

In a terminal window, write your API key into an `.env` file as an environment variable:

MacOS / LinuxWindows PowerShellWindows Command Prompt

Update: my_agent/.env
    
    [](<https://adk.dev/get-started/python/#__codelineno-8-1>)echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > .env
    
Update: my_agent/.env
    
    [](<https://adk.dev/get-started/python/#__codelineno-9-1>)echo 'GOOGLE_API_KEY="YOUR_API_KEY"' > .env
    
Update: my_agent/.env
    
    [](<https://adk.dev/get-started/python/#__codelineno-10-1>)echo GOOGLE_API_KEY="YOUR_API_KEY" > .env
    
Using other AI models with ADK

ADK supports the use of many generative AI models. For more information on configuring other models in ADK agents, see [Models & Authentication](<https://adk.dev/agents/models>).

## Run your agent[¶](<https://adk.dev/get-started/python/#run-your-agent> "Permanent link")

You can run your ADK agent with an interactive command-line interface using the `adk run` command or the ADK web user interface provided by the ADK using the `adk web` command. Both these options allow you to test and interact with your agent.

### Run with command-line interface[¶](<https://adk.dev/get-started/python/#run-with-command-line-interface> "Permanent link")

Run your agent using the `adk run` command-line tool.
    
    [](<https://adk.dev/get-started/python/#__codelineno-11-1>)adk run my_agent
    
![adk-run.png](https://adk.dev/assets/adk-run.png)

### Run with web interface[¶](<https://adk.dev/get-started/python/#run-with-web-interface> "Permanent link")

The ADK framework provides web interface you can use to test and interact with your agent. You can start the web interface using the following command:
    
    [](<https://adk.dev/get-started/python/#__codelineno-12-1>)adk web --port 8000
    
Note

Run this command from the **parent directory** that contains your `my_agent/` folder. For example, if your agent is inside `agents/my_agent/`, run `adk web` from the `agents/` directory.

This command starts a web server with a chat interface for your agent. You can access the web interface at `http://localhost:8000`. Select the agent at the upper left corner and type a request.

![adk-web-dev-ui-chat.png](https://adk.dev/assets/adk-web-dev-ui-chat.png)

Caution: ADK Web for development only

ADK Web is **_not meant for use in production deployments_**. You should use ADK Web for development and debugging purposes only.

## Next: Build your agent[¶](<https://adk.dev/get-started/python/#next-build-your-agent> "Permanent link")

Now that you have ADK installed and your first agent running, try building your own agent with our build guides:

  * [Build your agent](<https://adk.dev/tutorials/>)

Back to top 