# Multi-tool agent - Agent Development Kit (ADK)

> Source: [https://adk.dev/tutorials/multi-tool-agent/](https://adk.dev/tutorials/multi-tool-agent/)

[ Skip to content ](<https://adk.dev/tutorials/multi-tool-agent/#build-a-multi-tool-agent>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tutorials/multi-tool-agent.md> "Edit this page on GitHub") [ ](<https://adk.dev/tutorials/multi-tool-agent/index.md> "View this page as Markdown")

# Build a multi-tool agent[¶](<https://adk.dev/tutorials/multi-tool-agent/#build-a-multi-tool-agent> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

This quickstart guides you through installing Agent Development Kit (ADK), setting up a basic agent with multiple tools, and running it locally either in the terminal or in the interactive, browser-based dev UI.

This quickstart assumes a local IDE (VS Code, PyCharm, IntelliJ IDEA, etc.) with Python 3.10+ or Java 17+ and terminal access. This method runs the application entirely on your machine and is recommended for internal development.

## 1\. Set up Environment & Install ADK[¶](<https://adk.dev/tutorials/multi-tool-agent/#set-up-environment-install-adk> "Permanent link")

PythonTypeScriptGoJavaKotlin

Create & Activate Virtual Environment (Recommended):
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-0-1>)# Create
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-0-2>)python3 -m venv .venv
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-0-3>)# Activate (each new terminal)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-0-4>)# macOS/Linux: source .venv/bin/activate
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-0-5>)# Windows CMD: .venv\Scripts\activate.bat
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-0-6>)# Windows PowerShell: .venv\Scripts\Activate.ps1
    
Install ADK:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-1-1>)pip install google-adk
    
Create a new project directory, initialize it, and install dependencies:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-2-1>)mkdir my-adk-agent
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-2-2>)cd my-adk-agent
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-2-3>)npm init -y
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-2-4>)npm install @google/adk @google/adk-devtools
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-2-5>)npm install -D typescript
    
Create a `tsconfig.json` file with the following content. This configuration ensures your project correctly handles modern Node.js modules.

tsconfig.json
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-1>){
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-2>)  "compilerOptions": {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-3>)    "target": "es2020",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-4>)    "module": "nodenext",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-5>)    "moduleResolution": "nodenext",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-6>)    "esModuleInterop": true,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-7>)    "strict": true,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-8>)    "skipLibCheck": true,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-9>)    // set to false to allow CommonJS module syntax:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-10>)    "verbatimModuleSyntax": false
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-11>)  }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-3-12>)}
    
## Create a new Go module[¶](<https://adk.dev/tutorials/multi-tool-agent/#create-a-new-go-module> "Permanent link")

If you are starting a new project, you can create a new Go module:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-4-1>)mkdir my-adk-agent
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-4-2>)cd my-adk-agent
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-4-3>)go mod init example.com/my-agent
    
## Install ADK[¶](<https://adk.dev/tutorials/multi-tool-agent/#install-adk> "Permanent link")

To add the ADK to your project, run the following command:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-5-1>)go get google.golang.org/adk/v2
    
This will add the ADK as a dependency to your `go.mod` file.

To install ADK Java and set up the environment, see the [Java Quickstart](<https://adk.dev/get-started/java/>).

To install ADK Kotlin and set up the environment, see the [Kotlin Quickstart](<https://adk.dev/get-started/kotlin/>).

## 2\. Create Agent Project[¶](<https://adk.dev/tutorials/multi-tool-agent/#create-agent-project> "Permanent link")

### Project structure[¶](<https://adk.dev/tutorials/multi-tool-agent/#project-structure> "Permanent link")

PythonTypeScriptGoJavaKotlin

You will need to create the following project structure:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-6-1>)parent_folder/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-6-2>)    multi_tool_agent/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-6-3>)        __init__.py
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-6-4>)        agent.py
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-6-5>)        .env
    
Create the folder `multi_tool_agent`:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-7-1>)mkdir multi_tool_agent/
    
Note for Windows users

When using ADK on Windows for the next few steps, we recommend creating Python files using File Explorer or an IDE because the following commands (`mkdir`, `echo`) typically generate files with null bytes and/or incorrect encoding.

### `__init__.py`[¶](<https://adk.dev/tutorials/multi-tool-agent/#__init__py> "Permanent link")

Now create an `__init__.py` file in the folder:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-8-1>)echo "from . import agent" > multi_tool_agent/__init__.py
    
Your `__init__.py` should now look like this:

multi_tool_agent/__init__.py
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-9-1>)from . import agent
    
### `agent.py`[¶](<https://adk.dev/tutorials/multi-tool-agent/#agentpy> "Permanent link")

Create an `agent.py` file in the same folder:

OS X & LinuxWindows
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-10-1>)touch multi_tool_agent/agent.py
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-11-1>)type nul > multi_tool_agent/agent.py
    
Copy and paste the following code into `agent.py`:

multi_tool_agent/agent.py
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-1>)# Copyright 2026 Google LLC
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-2>)#
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-6>)#
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-8>)#
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-13>)# limitations under the License.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-14>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-15>)import datetime
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-16>)from zoneinfo import ZoneInfo
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-17>)from google.adk.agents import Agent
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-18>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-19>)def get_weather(city: str) -> dict:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-20>)    """Retrieves the current weather report for a specified city.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-21>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-22>)    Args:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-23>)        city (str): The name of the city for which to retrieve the weather report.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-24>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-25>)    Returns:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-26>)        dict: status and result or error msg.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-27>)    """
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-28>)    if city.lower() == "new york":
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-29>)        return {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-30>)            "status": "success",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-31>)            "report": (
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-32>)                "The weather in New York is sunny with a temperature of 25 degrees"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-33>)                " Celsius (77 degrees Fahrenheit)."
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-34>)            ),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-35>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-36>)    else:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-37>)        return {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-38>)            "status": "error",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-39>)            "error_message": f"Weather information for '{city}' is not available.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-40>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-41>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-42>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-43>)def get_current_time(city: str) -> dict:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-44>)    """Returns the current time in a specified city.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-45>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-46>)    Args:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-47>)        city (str): The name of the city for which to retrieve the current time.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-48>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-49>)    Returns:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-50>)        dict: status and result or error msg.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-51>)    """
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-52>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-53>)    if city.lower() == "new york":
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-54>)        tz_identifier = "America/New_York"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-55>)    else:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-56>)        return {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-57>)            "status": "error",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-58>)            "error_message": (
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-59>)                f"Sorry, I don't have timezone information for {city}."
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-60>)            ),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-61>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-62>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-63>)    tz = ZoneInfo(tz_identifier)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-64>)    now = datetime.datetime.now(tz)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-65>)    report = (
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-66>)        f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-67>)    )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-68>)    return {"status": "success", "report": report}
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-69>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-70>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-71>)root_agent = Agent(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-72>)    name="weather_time_agent",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-73>)    model="gemini-flash-latest",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-74>)    description=(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-75>)        "Agent to answer questions about the time and weather in a city."
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-76>)    ),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-77>)    instruction=(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-78>)        "You are a helpful agent who can answer user questions about the time and weather in a city."
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-79>)    ),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-80>)    tools=[get_weather, get_current_time],
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-12-81>))
    
### `.env`[¶](<https://adk.dev/tutorials/multi-tool-agent/#env> "Permanent link")

Create a `.env` file in the same folder:

OS X & LinuxWindows
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-13-1>)touch multi_tool_agent/.env
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-14-1>)type nul > multi_tool_agent\.env
    
More instructions about this file are described in the next section on [Set up the model](<https://adk.dev/tutorials/multi-tool-agent/#set-up-the-model>).

You will need to create the following project structure in your `my-adk-agent` directory:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-15-1>)my-adk-agent/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-15-2>)    agent.ts
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-15-3>)    .env
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-15-4>)    package.json
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-15-5>)    tsconfig.json
    
### `agent.ts`[¶](<https://adk.dev/tutorials/multi-tool-agent/#agentts> "Permanent link")

Create an `agent.ts` file in your project folder:

OS X & LinuxWindows
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-16-1>)touch agent.ts
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-17-1>)type nul > agent.ts
    
Copy and paste the following code into `agent.ts`:

agent.ts
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-1>)import 'dotenv/config';
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-2>)import { FunctionTool, LlmAgent } from '@google/adk';
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-3>)import { z } from 'zod';
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-4>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-5>)const getWeather = new FunctionTool({
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-6>)  name: 'get_weather',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-7>)  description: 'Retrieves the current weather report for a specified city.',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-8>)  parameters: z.object({
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-9>)    city: z.string().describe('The name of the city for which to retrieve the weather report.'),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-10>)  }),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-11>)  execute: ({ city }) => {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-12>)    if (city.toLowerCase() === 'new york') {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-13>)      return {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-14>)        status: 'success',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-15>)        report:
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-16>)          'The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit).',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-17>)      };
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-18>)    } else {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-19>)      return {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-20>)        status: 'error',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-21>)        error_message: `Weather information for '${city}' is not available.`,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-22>)      };
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-23>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-24>)  },
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-25>)});
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-26>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-27>)const getCurrentTime = new FunctionTool({
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-28>)  name: 'get_current_time',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-29>)  description: 'Returns the current time in a specified city.',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-30>)  parameters: z.object({
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-31>)    city: z.string().describe("The name of the city for which to retrieve the current time."),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-32>)  }),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-33>)  execute: ({ city }) => {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-34>)    let tz_identifier: string;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-35>)    if (city.toLowerCase() === 'new york') {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-36>)      tz_identifier = 'America/New_York';
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-37>)    } else {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-38>)      return {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-39>)        status: 'error',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-40>)        error_message: `Sorry, I don't have timezone information for ${city}.`,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-41>)      };
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-42>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-43>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-44>)    const now = new Date();
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-45>)    const report = `The current time in ${city} is ${now.toLocaleString('en-US', { timeZone: tz_identifier })}`;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-46>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-47>)    return { status: 'success', report: report };
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-48>)  },
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-49>)});
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-50>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-51>)export const rootAgent = new LlmAgent({
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-52>)  name: 'weather_time_agent',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-53>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-54>)  description: 'Agent to answer questions about the time and weather in a city.',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-55>)  instruction: 'You are a helpful agent who can answer user questions about the time and weather in a city.',
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-56>)  tools: [getWeather, getCurrentTime],
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-18-57>)});
    
### `.env`[¶](<https://adk.dev/tutorials/multi-tool-agent/#env_1> "Permanent link")

Create a `.env` file in the same folder:

OS X & LinuxWindows
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-19-1>)touch .env
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-20-1>)type nul > .env
    
More instructions about this file are described in the next section on [Set up the model](<https://adk.dev/tutorials/multi-tool-agent/#set-up-the-model>).

You will need to create the following project structure:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-21-1>)my-adk-agent/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-21-2>)    agent.go
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-21-3>)    .env
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-21-4>)    go.mod
    
### `agent.go`[¶](<https://adk.dev/tutorials/multi-tool-agent/#agentgo> "Permanent link")

Create an `agent.go` file in your project folder:

OS X & LinuxWindows
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-22-1>)touch agent.go
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-23-1>)type nul > agent.go
    
Copy and paste the following code into `agent.go`:

agent.go
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-1>)package main
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-2>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-3>)import (
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-4>)    "context"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-5>)    "log"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-6>)    "os"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-7>)    "strings"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-8>)    "time"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-9>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-10>)    "google.golang.org/genai"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-11>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-12>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-13>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-14>)    "google.golang.org/adk/v2/cmd/launcher"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-15>)    "google.golang.org/adk/v2/cmd/launcher/full"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-16>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-17>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-18>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-19>))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-20>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-21>)type CityArgs struct {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-22>)    City string `json:"city"`
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-23>)}
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-24>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-25>)func main() {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-26>)    ctx := context.Background()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-27>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-28>)    // 1. Setup the model.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-29>)    // Note: Authentication is handled via GOOGLE_API_KEY environment variable.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-30>)    model, err := gemini.NewModel(ctx, "gemini-flash-latest", &genai.ClientConfig{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-31>)        APIKey: os.Getenv("GOOGLE_API_KEY"),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-32>)    })
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-33>)    if err != nil {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-34>)        log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-35>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-36>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-37>)    weatherTool, err := functiontool.New[CityArgs, map[string]any](
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-38>)        functiontool.Config{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-39>)            Name:        "get_weather",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-40>)            Description: "Retrieves the current weather report for a specified city.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-41>)        },
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-42>)        func(ctx agent.Context, args CityArgs) (map[string]any, error) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-43>)            if strings.EqualFold(args.City, "new york") {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-44>)                return map[string]any{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-45>)                    "status": "success",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-46>)                    "report": "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees Fahrenheit).",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-47>)                }, nil
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-48>)            }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-49>)            return map[string]any{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-50>)                "status":        "error",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-51>)                "error_message": "Weather information for '" + args.City + "' is not available.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-52>)            }, nil
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-53>)        },
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-54>)    )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-55>)    if err != nil {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-56>)        log.Fatalf("Failed to create get_weather tool: %v", err)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-57>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-58>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-59>)    currentTimeTool, err := functiontool.New[CityArgs, map[string]any](
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-60>)        functiontool.Config{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-61>)            Name:        "get_current_time",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-62>)            Description: "Returns the current time in a specified city.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-63>)        },
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-64>)        func(ctx agent.Context, args CityArgs) (map[string]any, error) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-65>)            var tzIdentifier string
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-66>)            if strings.EqualFold(args.City, "new york") {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-67>)                tzIdentifier = "America/New_York"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-68>)            } else {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-69>)                return map[string]any{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-70>)                    "status":        "error",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-71>)                    "error_message": "Sorry, I don't have timezone information for " + args.City + ".",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-72>)                }, nil
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-73>)            }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-74>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-75>)            tz, err := time.LoadLocation(tzIdentifier)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-76>)            if err != nil {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-77>)                return nil, err
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-78>)            }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-79>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-80>)            now := time.Now().In(tz)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-81>)            report := "The current time in " + args.City + " is " + now.Format("2006-01-02 15:04:05 MST-0700")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-82>)            return map[string]any{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-83>)                "status": "success",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-84>)                "report": report,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-85>)            }, nil
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-86>)        },
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-87>)    )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-88>)    if err != nil {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-89>)        log.Fatalf("Failed to create get_current_time tool: %v", err)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-90>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-91>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-92>)    // 2. Define the agent.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-93>)    a, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-94>)        Name:        "weather_time_agent",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-95>)        Model:       model,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-96>)        Description: "Agent to answer questions about the time and weather in a city.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-97>)        Instruction: "You are a helpful agent who can answer user questions about the time and weather in a city.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-98>)        Tools: []tool.Tool{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-99>)            weatherTool,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-100>)            currentTimeTool,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-101>)        },
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-102>)    })
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-103>)    if err != nil {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-104>)        log.Fatalf("Failed to create agent: %v", err)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-105>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-106>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-107>)    // 3. Configure the launcher and run.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-108>)    config := &launcher.Config{
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-109>)        AgentLoader: agent.NewSingleLoader(a),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-110>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-111>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-112>)    l := full.NewLauncher()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-113>)    if err = l.Execute(ctx, config, os.Args[1:]); err != nil {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-114>)        log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-115>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-24-116>)}
    
### `.env`[¶](<https://adk.dev/tutorials/multi-tool-agent/#env_2> "Permanent link")

Create a `.env` file in the same folder:

OS X & LinuxWindows
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-25-1>)touch .env
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-26-1>)type nul > .env
    
Java projects generally feature the following project structure:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-1>)project_folder/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-2>)├── pom.xml (or build.gradle)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-3>)├── src/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-4>)├── └── main/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-5>)│       └── java/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-6>)│           └── agents/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-7>)│               └── multitool/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-27-8>)└── test/
    
### Create `MultiToolAgent.java`[¶](<https://adk.dev/tutorials/multi-tool-agent/#create-multitoolagentjava> "Permanent link")

Create a `MultiToolAgent.java` source file in the `agents.multitool` package in the `src/main/java/agents/multitool/` directory.

Copy and paste the following code into `MultiToolAgent.java`:

agents/multitool/MultiToolAgent.java
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-1>)package agents.multitool;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-2>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-3>)import com.google.adk.agents.BaseAgent;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-4>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-5>)import com.google.adk.events.Event;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-6>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-7>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-8>)import com.google.adk.tools.Annotations.Schema;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-9>)import com.google.adk.tools.FunctionTool;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-10>)import com.google.genai.types.Content;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-11>)import com.google.genai.types.Part;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-12>)import io.reactivex.rxjava3.core.Flowable;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-13>)import java.nio.charset.StandardCharsets;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-14>)import java.text.Normalizer;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-15>)import java.time.ZoneId;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-16>)import java.time.ZonedDateTime;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-17>)import java.time.format.DateTimeFormatter;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-18>)import java.util.Map;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-19>)import java.util.Scanner;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-20>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-21>)public class MultiToolAgent {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-22>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-23>)    private static String USER_ID = "student";
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-24>)    private static String NAME = "multi_tool_agent";
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-25>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-26>)    // The run your agent with Dev UI, the ROOT_AGENT should be a global public static final variable.
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-27>)    public static final BaseAgent ROOT_AGENT = initAgent();
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-28>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-29>)    public static BaseAgent initAgent() {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-30>)        return LlmAgent.builder()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-31>)            .name(NAME)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-32>)            .model("gemini-flash-latest")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-33>)            .description("Agent to answer questions about the time and weather in a city.")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-34>)            .instruction(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-35>)                "You are a helpful agent who can answer user questions about the time and weather"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-36>)                    + " in a city.")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-37>)            .tools(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-38>)                FunctionTool.create(MultiToolAgent.class, "getCurrentTime"),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-39>)                FunctionTool.create(MultiToolAgent.class, "getWeather"))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-40>)            .build();
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-41>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-42>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-43>)    public static Map<String, String> getCurrentTime(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-44>)        @Schema(name = "city",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-45>)                description = "The name of the city for which to retrieve the current time")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-46>)        String city) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-47>)        String normalizedCity =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-48>)            Normalizer.normalize(city, Normalizer.Form.NFD)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-49>)                .trim()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-50>)                .toLowerCase()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-51>)                .replaceAll("(\\p{IsM}+|\\p{IsP}+)", "")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-52>)                .replaceAll("\\s+", "_");
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-53>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-54>)        return ZoneId.getAvailableZoneIds().stream()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-55>)            .filter(zid -> zid.toLowerCase().endsWith("/" + normalizedCity))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-56>)            .findFirst()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-57>)            .map(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-58>)                zid ->
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-59>)                    Map.of(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-60>)                        "status",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-61>)                        "success",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-62>)                        "report",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-63>)                        "The current time in "
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-64>)                            + city
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-65>)                            + " is "
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-66>)                            + ZonedDateTime.now(ZoneId.of(zid))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-67>)                            .format(DateTimeFormatter.ofPattern("HH:mm"))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-68>)                            + "."))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-69>)            .orElse(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-70>)                Map.of(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-71>)                    "status",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-72>)                    "error",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-73>)                    "report",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-74>)                    "Sorry, I don't have timezone information for " + city + "."));
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-75>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-76>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-77>)    public static Map<String, String> getWeather(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-78>)        @Schema(name = "city",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-79>)                description = "The name of the city for which to retrieve the weather report")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-80>)        String city) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-81>)        if (city.toLowerCase().equals("new york")) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-82>)            return Map.of(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-83>)                "status",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-84>)                "success",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-85>)                "report",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-86>)                "The weather in New York is sunny with a temperature of 25 degrees Celsius (77 degrees"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-87>)                    + " Fahrenheit).");
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-88>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-89>)        } else {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-90>)            return Map.of(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-91>)                "status", "error", "report", "Weather information for " + city + " is not available.");
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-92>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-93>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-94>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-95>)    public static void main(String[] args) throws Exception {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-96>)        InMemoryRunner runner = new InMemoryRunner(ROOT_AGENT);
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-97>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-98>)        Session session =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-99>)            runner
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-100>)                .sessionService()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-101>)                .createSession(NAME, USER_ID)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-102>)                .blockingGet();
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-103>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-104>)        try (Scanner scanner = new Scanner(System.in, StandardCharsets.UTF_8)) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-105>)            while (true) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-106>)                System.out.print("\nYou > ");
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-107>)                String userInput = scanner.nextLine();
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-108>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-109>)                if ("quit".equalsIgnoreCase(userInput)) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-110>)                    break;
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-111>)                }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-112>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-113>)                Content userMsg = Content.fromParts(Part.fromText(userInput));
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-114>)                Flowable<Event> events = runner.runAsync(USER_ID, session.id(), userMsg);
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-115>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-116>)                System.out.print("\nAgent > ");
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-117>)                events.blockingForEach(event -> System.out.println(event.stringifyContent()));
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-118>)            }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-119>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-120>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-28-121>)}
    
Kotlin projects generally feature the following project structure:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-29-1>)project_folder/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-29-2>)├── build.gradle.kts
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-29-3>)├── src/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-29-4>)├── └── main/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-29-5>)│       └── kotlin/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-29-6>)│           └── agents/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-29-7>)│               └── multitool/
    
### Create `MultiToolAgent.kt`[¶](<https://adk.dev/tutorials/multi-tool-agent/#create-multitoolagentkt> "Permanent link")

Create a `MultiToolAgent.kt` source file in the `src/main/kotlin/agents/multitool/` directory.

Copy and paste the following code into `MultiToolAgent.kt`:

src/main/kotlin/agents/multitool/MultiToolAgent.kt
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-1>)package agents.multitool
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-2>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-3>)import com.google.adk.kt.agents.Instruction
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-4>)import com.google.adk.kt.agents.LlmAgent
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-5>)import com.google.adk.kt.annotations.Param
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-6>)import com.google.adk.kt.annotations.Tool
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-7>)import com.google.adk.kt.models.Gemini
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-8>)import com.google.adk.kt.runners.InMemoryRunner
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-9>)import com.google.adk.kt.sessions.InMemorySessionService
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-10>)import com.google.adk.kt.sessions.SessionKey
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-11>)import com.google.adk.kt.types.Content
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-12>)import com.google.adk.kt.types.Part
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-13>)import com.google.adk.kt.types.Role
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-14>)import kotlinx.coroutines.flow.toList
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-15>)import kotlinx.coroutines.runBlocking
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-16>)import java.text.Normalizer
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-17>)import java.time.ZoneId
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-18>)import java.time.ZonedDateTime
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-19>)import java.time.format.DateTimeFormatter
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-20>)import java.util.Scanner
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-21>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-22>)class MultiToolService {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-23>)    @Tool
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-24>)    fun getCurrentTime(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-25>)        @Param("The name of the city for which to retrieve the current time") city: String,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-26>)    ): Map<String, String> {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-27>)        val normalizedCity =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-28>)            Normalizer.normalize(city, Normalizer.Form.NFD)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-29>)                .trim()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-30>)                .lowercase()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-31>)                .replace(Regex("(\\p{IsM}+|\\p{IsP}+)"), "")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-32>)                .replace(Regex("\\s+"), "_")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-33>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-34>)        val zoneId =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-35>)            ZoneId.getAvailableZoneIds()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-36>)                .firstOrNull { it.lowercase().endsWith("/$normalizedCity") }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-37>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-38>)        return if (zoneId != null) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-39>)            val time =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-40>)                ZonedDateTime.now(ZoneId.of(zoneId))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-41>)                    .format(DateTimeFormatter.ofPattern("HH:mm"))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-42>)            mapOf(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-43>)                "status" to "success",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-44>)                "report" to "The current time in $city is $time.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-45>)            )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-46>)        } else {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-47>)            mapOf(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-48>)                "status" to "error",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-49>)                "report" to "Sorry, I don't have timezone information for $city.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-50>)            )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-51>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-52>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-53>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-54>)    @Tool
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-55>)    fun getWeather(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-56>)        @Param("The name of the city for which to retrieve the weather report") city: String,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-57>)    ): Map<String, String> {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-58>)        return if (city.lowercase() == "new york") {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-59>)            mapOf(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-60>)                "status" to "success",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-61>)                "report" to "The weather in New York is sunny with a temperature of " +
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-62>)                    "25 degrees Celsius (77 degrees Fahrenheit).",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-63>)            )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-64>)        } else {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-65>)            mapOf(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-66>)                "status" to "error",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-67>)                "report" to "Weather information for $city is not available.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-68>)            )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-69>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-70>)    }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-71>)}
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-72>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-73>)fun main() =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-74>)    runBlocking {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-75>)        val model = Gemini(name = "gemini-flash-latest")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-76>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-77>)        val agent =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-78>)            LlmAgent(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-79>)                name = "multi_tool_agent",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-80>)                model = model,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-81>)                description = "Agent to answer questions about the time and weather in a city.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-82>)                instruction =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-83>)                    Instruction(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-84>)                        "You are a helpful agent who can answer user questions about the " +
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-85>)                            "time and weather in a city.",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-86>)                    ),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-87>)                tools = MultiToolService().generatedTools(),
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-88>)            )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-89>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-90>)        val sessionService = InMemorySessionService()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-91>)        val runner =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-92>)            InMemoryRunner(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-93>)                agent = agent,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-94>)                appName = "multi_tool_app",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-95>)                sessionService = sessionService,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-96>)            )
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-97>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-98>)        val userId = "student"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-99>)        val sessionId = "session_1"
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-100>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-101>)        sessionService.createSession(SessionKey("multi_tool_app", userId, sessionId))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-102>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-103>)        val scanner = Scanner(System.`in`)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-104>)        while (true) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-105>)            print("\nYou > ")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-106>)            val userInput = scanner.nextLine()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-107>)            if (userInput.lowercase() == "quit") break
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-108>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-109>)            val userContent = Content(role = Role.USER, parts = listOf(Part(text = userInput)))
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-110>)            val events =
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-111>)                runner.runAsync(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-112>)                    userId = userId,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-113>)                    sessionId = sessionId,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-114>)                    newMessage = userContent,
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-115>)                ).toList()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-116>)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-117>)            print("\nAgent > ")
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-118>)            for (event in events) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-119>)                event.content?.parts?.forEach { part ->
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-120>)                    part.text?.let { print(it) }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-121>)                }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-122>)            }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-123>)            println()
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-124>)        }
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-30-125>)    }
    
![intro_components.png](https://adk.dev/assets/quickstart-flow-tool.png)

## 3\. Set up the model[¶](<https://adk.dev/tutorials/multi-tool-agent/#set-up-the-model> "Permanent link")

Your agent's ability to understand user requests and generate responses is powered by a generative AI model or Large Language Model (LLM). This guide uses Gemini models as examples, but ADK is compatible with many AI models from Google and other providers. For more information on available models and how to configure them, see [AI Models for ADK agents](<https://adk.dev/agents/models/>).

### Model connection and authentication[¶](<https://adk.dev/tutorials/multi-tool-agent/#model-connection-and-authentication> "Permanent link")

When using an AI model through a service, such as the Gemini API or Gemini Enterprise Agent Platform on Google Cloud, you must provide an API key or authenticate with the service. The most direct way to provide this information is to use environment variables or an `.env` file. The following examples show the most common way to configure an agent for use with the Gemini API or Gemini Enterprise Agent Platform.

Gemini APIGoogle Cloud Agent Platform
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-31-1>)# .env configuration file
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-31-2>)GOOGLE_API_KEY="PASTE_YOUR_GEMINI_API_KEY_HERE"
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-32-1>)# .env configuration file
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-32-2>)GOOGLE_CLOUD_PROJECT=your-project-id
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-32-3>)GOOGLE_CLOUD_LOCATION=location-code        # example: us-central1
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-32-4>)GOOGLE_GENAI_USE_ENTERPRISE=True
    
For more details on connecting ADK agents to Google Cloud hosted models and services, including Gemini Enterprise Agent Platform, see the [Connect to Google Cloud and Agent Platform](<https://adk.dev/get-started/google-cloud/>) guide.

## 4\. Run Your Agent[¶](<https://adk.dev/tutorials/multi-tool-agent/#run-your-agent> "Permanent link")

PythonTypeScriptGoJavaKotlin

Using the terminal, navigate to the parent directory of your agent project (e.g. using `cd ..`):
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-33-1>)parent_folder/      <-- navigate to this directory
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-33-2>)    multi_tool_agent/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-33-3>)        __init__.py
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-33-4>)        agent.py
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-33-5>)        .env
    
There are multiple ways to interact with your agent:

Dev UI (adk web)Terminal (adk run)API Server (adk api_server)

Authentication Setup for Agent Platform Users

If you selected **"Gemini - Google Cloud Agent Platform"** in the previous step, you must authenticate with Google Cloud before launching the dev UI.

Run this command and follow the prompts: 
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-34-1>)gcloud auth application-default login
    
**Note:** Skip this step if you're using "Gemini - Google AI Studio".

Run the following command to launch the **dev UI**.
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-35-1>)adk web
    
Caution: ADK Web for development only

ADK Web is **_not meant for use in production deployments_**. You should use ADK Web for development and debugging purposes only.

Note for Windows users

When hitting the `_make_subprocess_transport NotImplementedError`, consider using `adk web --no-reload` instead.

**Step 1:** Open the URL provided (usually `http://localhost:8000` or `http://127.0.0.1:8000`) directly in your browser.

**Step 2.** In the top-left corner of the UI, you can select your agent in the dropdown. Select "multi_tool_agent".

Troubleshooting

If you do not see "multi_tool_agent" in the dropdown menu, make sure you are running `adk web` in the **parent folder** of your agent folder (i.e. the parent folder of multi_tool_agent).

**Step 3.** Now you can chat with your agent using the textbox:

![adk-web-dev-ui-chat.png](https://adk.dev/assets/adk-web-dev-ui-chat.png)

**Step 4.** By using the `Events` tab at the left, you can inspect individual function calls, responses and model responses by clicking on the actions:

![adk-web-dev-ui-function-call.png](https://adk.dev/assets/adk-web-dev-ui-function-call.png)

On the `Events` tab, you can also click the `Trace` button to see the trace logs for each event that shows the latency of each function calls:

![adk-web-dev-ui-trace.png](https://adk.dev/assets/adk-web-dev-ui-trace.png)

**Step 5.** You can also enable your microphone and talk to your agent:

Model support for voice/video streaming

In order to use voice/video streaming in ADK, you will need to use Gemini models that support the Live API. You can find the **model ID(s)** that supports the Gemini Live API in the documentation:

  * [Google AI Studio: Gemini Live API](<https://ai.google.dev/gemini-api/docs/models#live-api>)
  * [Agent Platform: Gemini Live API](<https://cloud.google.com/vertex-ai/generative-ai/docs/live-api>)

You can then replace the `model` string in `root_agent` in the `agent.py` file you created earlier ([jump to section](<https://adk.dev/tutorials/multi-tool-agent/#agentpy>)). Your code should look something like:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-36-1>)root_agent = Agent(
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-36-2>)    name="weather_time_agent",
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-36-3>)    model="replace-me-with-model-id", #e.g. gemini-2.0-flash-live-001
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-36-4>)    ...
    
![adk-web-dev-ui-audio.png](https://adk.dev/assets/adk-web-dev-ui-audio.png)

Tip

When using `adk run` you can inject prompts into the agent to start by piping text to the command like so:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-37-1>)echo "Please start by listing files" | adk run file_listing_agent
    
Run the following command, to chat with your Weather agent.
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-38-1>)adk run multi_tool_agent
    
![adk-run.png](https://adk.dev/assets/adk-run.png)

To exit, use Cmd/Ctrl+C.

`adk api_server` enables you to create a local FastAPI server in a single command, enabling you to test local cURL requests before you deploy your agent.

![adk-api-server.png](https://adk.dev/assets/adk-api-server.png)

To learn how to use `adk api_server` for testing, refer to the [documentation on using the API server](<https://adk.dev/runtime/api-server/>).

Using the terminal, navigate to your agent project directory:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-39-1>)my-adk-agent/      <-- navigate to this directory
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-39-2>)    agent.ts
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-39-3>)    .env
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-39-4>)    package.json
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-39-5>)    tsconfig.json
    
There are multiple ways to interact with your agent:

Dev UI (adk web)Terminal (adk run)API Server (adk api_server)

Run the following command to launch the **dev UI**.
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-40-1>)npx adk web
    
**Step 1:** Open the URL provided (usually `http://localhost:8000` or `http://127.0.0.1:8000`) directly in your browser.

**Step 2.** In the top-left corner of the UI, select your agent from the dropdown. The agents are listed by their filenames, so you should select "agent".

Troubleshooting

If you do not see "agent" in the dropdown menu, make sure you are running `npx adk web` in the directory containing your `agent.ts` file.

**Step 3.** Now you can chat with your agent using the textbox:

![adk-web-dev-ui-chat.png](https://adk.dev/assets/adk-web-dev-ui-chat.png)

**Step 4.** By using the `Events` tab at the left, you can inspect individual function calls, responses and model responses by clicking on the actions:

![adk-web-dev-ui-function-call.png](https://adk.dev/assets/adk-web-dev-ui-function-call.png)

On the `Events` tab, you can also click the `Trace` button to see the trace logs for each event that shows the latency of each function calls:

![adk-web-dev-ui-trace.png](https://adk.dev/assets/adk-web-dev-ui-trace.png)

Run the following command to chat with your agent.
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-41-1>)npx adk run agent.ts
    
![adk-run.png](https://adk.dev/assets/adk-run.png)

To exit, use Cmd/Ctrl+C.

`npx adk api_server` enables you to create a local Express.js server in a single command, enabling you to test local cURL requests before you deploy your agent.

![adk-api-server.png](https://adk.dev/assets/adk-api-server.png)

To learn how to use `api_server` for testing, refer to the [documentation on testing](<https://adk.dev/runtime/api-server/>).

Using the terminal, navigate to your agent project directory:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-42-1>)my-adk-agent/      <-- navigate to this directory
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-42-2>)    agent.go
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-42-3>)    .env
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-42-4>)    go.mod
    
There are multiple ways to interact with your agent:

Dev UI (web)Terminal (console)

Run the following command to launch the **dev UI**. You must specify which sub-launchers to activate (e.g., `webui`, `api`).
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-43-1>)go run agent.go web webui api
    
**Step 1:** Open the URL provided (usually `http://localhost:8080`) directly in your browser.

**Step 2.** In the top-left corner of the UI, select your agent from the dropdown. It should be "weather_time_agent".

**Step 3.** Now you can chat with your agent using the textbox.

Run the following command to chat with your agent in the terminal.
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-44-1>)go run agent.go console
    
**Note:** If `console` is the first sublauncher in your code (as it is with `full.NewLauncher()`), you can also just run `go run agent.go`.

To exit, use Cmd/Ctrl+C.

Using the terminal, navigate to the parent directory of your agent project (e.g. using `cd ..`):
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-1>)project_folder/                <-- navigate to this directory
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-2>)├── pom.xml (or build.gradle)
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-3>)├── src/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-4>)├── └── main/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-5>)│       └── java/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-6>)│           └── agents/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-7>)│               └── multitool/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-8>)│                   └── MultiToolAgent.java
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-45-9>)└── test/
    
Dev UIMavenGradle

Run the following command from the terminal to launch the Dev UI.

**DO NOT change the main class name of the Dev UI server.**

terminal
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-46-1>)mvn exec:java \
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-46-2>)    -Dexec.mainClass="com.google.adk.web.AdkWebServer" \
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-46-3>)    -Dexec.args="--adk.agents.source-dir=src/main/java" \
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-46-4>)    -Dexec.classpathScope="compile"
    
**Step 1:** Open the URL provided (usually `http://localhost:8080` or `http://127.0.0.1:8080`) directly in your browser.

**Step 2.** In the top-left corner of the UI, you can select your agent in the dropdown. Select "multi_tool_agent".

Troubleshooting

If you do not see "multi_tool_agent" in the dropdown menu, make sure you are running the `mvn` command at the location where your Java source code is located (usually `src/main/java`).

**Step 3.** Now you can chat with your agent using the textbox:

![adk-web-dev-ui-chat.png](https://adk.dev/assets/adk-web-dev-ui-chat.png)

**Step 4.** You can also inspect individual function calls, responses and model responses by clicking on the actions:

![adk-web-dev-ui-function-call.png](https://adk.dev/assets/adk-web-dev-ui-function-call.png)

Caution: ADK Web for development only

ADK Web is **_not meant for use in production deployments_**. You should use ADK Web for development and debugging purposes only.

With Maven, run the `main()` method of your Java class with the following command:

terminal
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-47-1>)mvn compile exec:java -Dexec.mainClass="agents.multitool.MultiToolAgent"
    
With Gradle, the `build.gradle` or `build.gradle.kts` build file should have the following Java plugin in its `plugins` section:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-48-1>)plugins {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-48-2>)    id('java')
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-48-3>)    // other plugins
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-48-4>)}
    
Then, elsewhere in the build file, at the top-level, create a new task to run the `main()` method of your agent:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-49-1>)tasks.register('runAgent', JavaExec) {
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-49-2>)    classpath = sourceSets.main.runtimeClasspath
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-49-3>)    mainClass = 'agents.multitool.MultiToolAgent'
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-49-4>)}
    
Finally, on the command-line, run the following command:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-50-1>)gradle runAgent
    
Using the terminal, navigate to your agent project directory:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-1>)project_folder/                <-- navigate to this directory
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-2>)├── build.gradle.kts
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-3>)├── src/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-4>)├── └── main/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-5>)│       └── kotlin/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-6>)│           └── agents/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-7>)│               └── multitool/
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-51-8>)│                   └── MultiToolAgent.kt
    
### Run your Agent[¶](<https://adk.dev/tutorials/multi-tool-agent/#run-your-agent_1> "Permanent link")

You can run the `main()` method of your Kotlin class using Gradle:
    
    [](<https://adk.dev/tutorials/multi-tool-agent/#__codelineno-52-1>)./gradlew run
    
Or if you are using IntelliJ IDEA, you can just click the green run arrow next to the `main()` function.

### 📝 Example prompts to try[¶](<https://adk.dev/tutorials/multi-tool-agent/#example-prompts-to-try> "Permanent link")

  * What is the weather in New York?
  * What is the time in New York?
  * What is the weather in Paris?
  * What is the time in Paris?

## 🎉 Congratulations![¶](<https://adk.dev/tutorials/multi-tool-agent/#congratulations> "Permanent link")

You've successfully created and interacted with your first agent using ADK!

* * *

## 🛣️ Next steps[¶](<https://adk.dev/tutorials/multi-tool-agent/#next-steps> "Permanent link")

  * **Go to the tutorial** : Learn how to add memory, session, state to your agent: [tutorial](<https://adk.dev/tutorials/>).
  * **Delve into advanced configuration:** Explore the [setup](<https://adk.dev/get-started/installation/>) section for deeper dives into project structure, configuration, and other interfaces.
  * **Understand Core Concepts:** Learn about [agents concepts](<https://adk.dev/agents/>).

Back to top 