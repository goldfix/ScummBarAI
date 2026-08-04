# Python - Agent Development Kit (ADK)

> Source: [https://adk.dev/get-started/streaming/quickstart-streaming/](https://adk.dev/get-started/streaming/quickstart-streaming/)

[ Skip to content ](<https://adk.dev/get-started/streaming/quickstart-streaming/#build-a-streaming-agent-with-python>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/get-started/streaming/quickstart-streaming.md> "Edit this page on GitHub") [ ](<https://adk.dev/get-started/streaming/quickstart-streaming/index.md> "View this page as Markdown")

# Build a streaming agent with Python[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#build-a-streaming-agent-with-python> "Permanent link")

With this quickstart, you'll learn to create a simple agent and use ADK Streaming to enable voice and video communication with it that is low-latency and bidirectional. We will install ADK, set up a basic "Google Search" agent, try running the agent with Streaming with `adk web` tool, and then explain how to build a simple asynchronous web app by yourself using ADK Streaming and [FastAPI](<https://fastapi.tiangolo.com/>).

**Note:** This guide assumes you have experience using a terminal in Windows, Mac, and Linux environments.

## Supported models for voice/video streaming[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#supported-models> "Permanent link")

In order to use voice/video streaming in ADK, you will need to use Gemini models that support the Live API. You can find the **model ID(s)** that supports the Gemini Live API in the documentation:

  * [Google AI Studio: Gemini Live API](<https://ai.google.dev/gemini-api/docs/models#live-api>)
  * [Agent Platform: Gemini Live API](<https://cloud.google.com/vertex-ai/generative-ai/docs/live-api>)

## 1\. Setup Environment & Install ADK[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#setup-environment-install-adk> "Permanent link")

Create & Activate Virtual Environment (Recommended):
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-0-1>)# Create
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-0-2>)python3 -m venv .venv
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-0-3>)# Activate (each new terminal)
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-0-4>)# macOS/Linux: source .venv/bin/activate
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-0-5>)# Windows CMD: .venv\Scripts\activate.bat
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-0-6>)# Windows PowerShell: .venv\Scripts\Activate.ps1
    
Install ADK:
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-1-1>)pip install google-adk
    
## 2\. Project Structure[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#project-structure> "Permanent link")

Create the following folder structure with empty files:
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-2-1>)adk-streaming/  # Project folder
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-2-2>)└── app/ # the web app folder
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-2-3>)    ├── .env # Gemini API key
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-2-4>)    └── google_search_agent/ # Agent folder
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-2-5>)        ├── __init__.py # Python package
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-2-6>)        └── agent.py # Agent definition
    
### agent.py[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#agentpy> "Permanent link")

Copy-paste the following code block into the `agent.py` file.

For `model`, please double-check the model ID as described earlier in the [Models section](<https://adk.dev/get-started/streaming/quickstart-streaming/#supported-models>).
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-1>)from google.adk.agents import Agent
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-2>)from google.adk.tools import google_search  # Import the tool
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-3>)
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-4>)root_agent = Agent(
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-5>)   # A unique name for the agent.
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-6>)   name="basic_search_agent",
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-7>)   # The Large Language Model (LLM) that agent will use.
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-8>)   # Please fill in the latest model id that supports live from
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-9>)   # https://adk.dev/get-started/streaming/quickstart-streaming/#supported-models
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-10>)   model="...",
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-11>)   # A short description of the agent's purpose.
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-12>)   description="Agent to answer questions using Google Search.",
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-13>)   # Instructions to set the agent's behavior.
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-14>)   instruction="You are an expert researcher. You always stick to the facts.",
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-15>)   # Add google_search tool to perform grounding with Google search.
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-16>)   tools=[google_search]
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-3-17>))
    
`agent.py` is where all your agent(s)' logic will be stored, and you must have a `root_agent` defined.

Notice how easily you integrated [grounding with Google Search](<https://ai.google.dev/gemini-api/docs/grounding?lang=python#configure-search>) capabilities. The `Agent` class and the `google_search` tool handle the complex interactions with the LLM and grounding with the search API, allowing you to focus on the agent's _purpose_ and _behavior_.

![intro_components.png](https://adk.dev/assets/quickstart-streaming-tool.png)

Copy-paste the following code block to `__init__.py` file.

__init__.py
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-4-1>)from . import agent
    
## 3\. Set up the platform[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#set-up-the-platform> "Permanent link")

To run the agent, choose a platform from either Google AI Studio or Google Cloud Agent Platform:

Gemini - Google AI StudioGemini - Google Cloud Agent Platform

  1. Get an API key from [Google AI Studio](<https://aistudio.google.com/apikey>).
  2. Open the **`.env`** file located inside (`app/`) and copy-paste the following code.

.env
         
         [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-5-1>)GOOGLE_GENAI_USE_ENTERPRISE=FALSE
         [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-5-2>)GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
         
  3. Replace `PASTE_YOUR_ACTUAL_API_KEY_HERE` with your actual `API KEY`.

  1. You need an existing [Google Cloud](<https://cloud.google.com/?e=48754805&hl=en>) account and a project.
     * Set up a [Google Cloud project](<https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal#setup-gcp>)
     * Set up the [gcloud CLI](<https://cloud.google.com/vertex-ai/generative-ai/docs/start/quickstarts/quickstart-multimodal#setup-local>)
     * Authenticate to Google Cloud, from the terminal by running `gcloud auth login`.
     * [Enable the Agent Platform API](<https://console.cloud.google.com/flows/enableapi?apiid=aiplatform.googleapis.com>).
  2. Open the **`.env`** file located inside (`app/`). Copy-paste the following code and update the project ID and location.

.env
         
         [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-6-1>)GOOGLE_GENAI_USE_ENTERPRISE=TRUE
         [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-6-2>)GOOGLE_CLOUD_PROJECT=PASTE_YOUR_ACTUAL_PROJECT_ID
         [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-6-3>)GOOGLE_CLOUD_LOCATION=us-central1
         
For more information on connecting to Google Cloud from ADK agents, see [Connect to Google Cloud and Agent Platform](<https://adk.dev/get-started/google-cloud/>).

## 4\. Try the agent with `adk web`[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#try-the-agent-with-adk-web> "Permanent link")

Now it's ready to try the agent. Run the following command to launch the **dev UI**. First, make sure to set the current directory to `app`:
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-7-1>)cd app
    
Also, set `SSL_CERT_FILE` variable with the following command. This is required for the voice and video tests later.

OS X & LinuxWindows
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-8-1>)export SSL_CERT_FILE=$(python3 -m certifi)
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-9-1>)$env:SSL_CERT_FILE = (python3 -m certifi)
    
Then, run the dev UI:
    
    [](<https://adk.dev/get-started/streaming/quickstart-streaming/#__codelineno-10-1>)adk web
    
Note for Windows users

When hitting the `_make_subprocess_transport NotImplementedError`, consider using `adk web --no-reload` instead.

Caution: ADK Web for development only

ADK Web is **_not meant for use in production deployments_**. You should use ADK Web for development and debugging purposes only.

Open the URL provided (usually `http://localhost:8000` or `http://127.0.0.1:8000`) **directly in your browser**. This connection stays entirely on your local machine. Select `google_search_agent`.

### Try with voice and video[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#try-with-voice-and-video> "Permanent link")

To try with voice, reload the web browser, click the microphone button to enable the voice input, and ask the the following questions in voice. The agent will use the google_search tool to get the latest information to answer those questions. You will hear the answer in voice in real-time.

  * What is the weather in New York?
  * What is the time in New York?
  * What is the weather in Paris?
  * What is the time in Paris?

To try with video, reload the web browser, click the camera button to enable the video input, and ask questions like "What do you see?". The agent will answer what they see in the video input.

#### Caveat[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#caveat> "Permanent link")

  * You can not use text chat with the native-audio models. You will see errors when entering text messages on `adk web`.

### Stop the tool[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#stop-the-tool> "Permanent link")

Stop `adk web` by pressing `Ctrl-C` on the console.

### Note on ADK Streaming[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#note-on-adk-streaming> "Permanent link")

The following features will be supported in the future versions of the ADK Streaming: Callback, LongRunningTool, ExampleTool, and Shell agent (e.g. SequentialAgent).

Congratulations! You've successfully created and interacted with your first Streaming agent using ADK!

## Next steps: build custom streaming app[¶](<https://adk.dev/get-started/streaming/quickstart-streaming/#next-steps-build-custom-streaming-app> "Permanent link")

The [Gemini Live API Toolkit development guide series](<https://adk.dev/streaming/dev-guide/part1/>) gives an overview of the server and client code for a custom asynchronous web app built with ADK Streaming, enabling real-time, bidirectional audio and text communication.

Back to top 