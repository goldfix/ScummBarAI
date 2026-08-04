# OpenAPI tools - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools-custom/openapi-tools/](https://adk.dev/tools-custom/openapi-tools/)

[ Skip to content ](<https://adk.dev/tools-custom/openapi-tools/#integrate-rest-apis-with-openapi>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools-custom/openapi-tools.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools-custom/openapi-tools/index.md> "View this page as Markdown")

# Integrate REST APIs with OpenAPI[¶](<https://adk.dev/tools-custom/openapi-tools/#integrate-rest-apis-with-openapi> "Permanent link")

Supported in ADKPython v0.1.0

ADK simplifies interacting with external REST APIs by automatically generating callable tools directly from an [OpenAPI Specification (v3.x)](<https://swagger.io/specification/>). This eliminates the need to manually define individual function tools for each API endpoint.

Core Benefit

Use `OpenAPIToolset` to instantly create agent tools (`RestApiTool`) from your existing API documentation (OpenAPI spec), enabling agents to seamlessly call your web services.

## Key components[¶](<https://adk.dev/tools-custom/openapi-tools/#key-components> "Permanent link")

  * **`OpenAPIToolset`** : This is the primary class you'll use. You initialize it with your OpenAPI specification, and it handles the parsing and generation of tools.
  * **`RestApiTool`** : This class represents a single, callable API operation (like `GET /pets/{petId}` or `POST /pets`). `OpenAPIToolset` creates one `RestApiTool` instance for each operation defined in your spec.

## How it works[¶](<https://adk.dev/tools-custom/openapi-tools/#how-it-works> "Permanent link")

The process involves these main steps when you use `OpenAPIToolset`:

  1. **Initialization & Parsing**:

     * You provide the OpenAPI specification to `OpenAPIToolset` either as a Python dictionary, a JSON string, or a YAML string.
     * The toolset internally parses the spec, resolving any internal references (`$ref`) to understand the complete API structure.
  2. **Operation Discovery** :

     * It identifies all valid API operations (e.g., `GET`, `POST`, `PUT`, `DELETE`) defined within the `paths` object of your specification.
  3. **Tool Generation** :

     * For each discovered operation, `OpenAPIToolset` automatically creates a corresponding `RestApiTool` instance.
     * **Tool Name** : Derived from the `operationId` in the spec (converted to `snake_case`, max 60 chars). If `operationId` is missing, a name is generated from the method and path.
     * **Tool Description** : Uses the `summary` or `description` from the operation for the LLM.
     * **API Details** : Stores the required HTTP method, path, server base URL, parameters (path, query, header, cookie), and request body schema internally.
  4. **`RestApiTool` Functionality**: Each generated `RestApiTool`:

     * **Schema Generation** : Dynamically creates a `FunctionDeclaration` based on the operation's parameters and request body. This schema tells the LLM how to call the tool (what arguments are expected).
     * **Execution** : When the LLM calls the tool, the tool constructs the HTTP request, including the URL, headers, query parameters, and body, using the LLM's arguments and the OpenAPI specification. The tool handles authentication if configured, and executes the API call asynchronously using the `httpx` library.
     * **Response Handling** : Returns the API response (typically JSON) back to the agent flow.
  5. **Authentication** : You can configure global authentication (like API keys or OAuth - see [Authentication](<https://adk.dev/tools-custom/authentication/>) for details) when initializing `OpenAPIToolset`. This authentication configuration is automatically applied to all generated `RestApiTool` instances.

## Usage workflow[¶](<https://adk.dev/tools-custom/openapi-tools/#usage-workflow> "Permanent link")

Follow these steps to integrate an OpenAPI spec into your agent:

  1. **Obtain Spec** : Get your OpenAPI specification document (e.g., load from a `.json` or `.yaml` file, fetch from a URL).
  2. **Instantiate Toolset** : Create an `OpenAPIToolset` instance, passing the spec content and type (`spec_str`/`spec_dict`, `spec_str_type`). Provide authentication details (`auth_scheme`, `auth_credential`) if required by the API.
         
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-1>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-2>)
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-3>)# Example with a JSON string
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-4>)openapi_spec_json = '...' # Your OpenAPI JSON string
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-5>)toolset = OpenAPIToolset(spec_str=openapi_spec_json, spec_str_type="json")
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-6>)
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-7>)# Example with a dictionary
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-8>)# openapi_spec_dict = {...} # Your OpenAPI spec as a dict
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-0-9>)# toolset = OpenAPIToolset(spec_dict=openapi_spec_dict)
         
  3. **Add to Agent** : Include the retrieved tools in your `LlmAgent`'s `tools` list.
         
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-1>)from google.adk.agents import LlmAgent
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-2>)
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-3>)my_agent = LlmAgent(
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-4>)    name="api_interacting_agent",
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-5>)    model="gemini-flash-latest", # Or your preferred model
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-6>)    tools=[toolset], # Pass the toolset
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-7>)    # ... other agent config ...
         [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-1-8>))
         
  4. **Instruct agent** : Update your agent's instructions to inform it about the new API capabilities and the names of the tools it can use (e.g., `list_pets`, `create_pet`). The tool descriptions generated from the spec will also help the LLM.

  5. **Run agent** : Execute your agent using the `Runner`. When the LLM determines it needs to call one of the APIs, it will generate a function call targeting the appropriate `RestApiTool`, which will then handle the HTTP request automatically.

## See it in action[¶](<https://adk.dev/tools-custom/openapi-tools/#see-it-in-action> "Permanent link")

This example demonstrates generating tools from a simple Pet Store OpenAPI spec (using `httpbin.org` for mock responses) and interacting with them via an agent.

Code: Pet Store API

openapi_example.py
    
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-1>)# Copyright 2025 Google LLC
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-2>)#
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-6>)#
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-8>)#
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-14>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-15>)import asyncio
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-16>)import uuid # For unique session IDs
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-17>)from dotenv import load_dotenv
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-18>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-19>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-20>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-21>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-22>)from google.genai import types
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-23>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-24>)# --- OpenAPI Tool Imports ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-25>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-26>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-27>)# --- Load Environment Variables (If ADK tools need them, e.g., API keys) ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-28>)load_dotenv() # Create a .env file in the same directory if needed
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-29>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-30>)# --- Constants ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-31>)APP_NAME_OPENAPI = "openapi_petstore_app"
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-32>)USER_ID_OPENAPI = "user_openapi_1"
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-33>)SESSION_ID_OPENAPI = f"session_openapi_{uuid.uuid4()}" # Unique session ID
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-34>)AGENT_NAME_OPENAPI = "petstore_manager_agent"
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-35>)GEMINI_MODEL = "gemini-2.0-flash"
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-36>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-37>)# --- Sample OpenAPI Specification (JSON String) ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-38>)# A basic Pet Store API example using httpbin.org as a mock server
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-39>)openapi_spec_string = """
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-40>){
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-41>)  "openapi": "3.0.0",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-42>)  "info": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-43>)    "title": "Simple Pet Store API (Mock)",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-44>)    "version": "1.0.1",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-45>)    "description": "An API to manage pets in a store, using httpbin for responses."
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-46>)  },
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-47>)  "servers": [
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-48>)    {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-49>)      "url": "https://httpbin.org",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-50>)      "description": "Mock server (httpbin.org)"
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-51>)    }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-52>)  ],
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-53>)  "paths": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-54>)    "/get": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-55>)      "get": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-56>)        "summary": "List all pets (Simulated)",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-57>)        "operationId": "listPets",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-58>)        "description": "Simulates returning a list of pets. Uses httpbin's /get endpoint which echoes query parameters.",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-59>)        "parameters": [
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-60>)          {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-61>)            "name": "limit",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-62>)            "in": "query",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-63>)            "description": "Maximum number of pets to return",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-64>)            "required": false,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-65>)            "schema": { "type": "integer", "format": "int32" }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-66>)          },
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-67>)          {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-68>)             "name": "status",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-69>)             "in": "query",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-70>)             "description": "Filter pets by status",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-71>)             "required": false,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-72>)             "schema": { "type": "string", "enum": ["available", "pending", "sold"] }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-73>)          }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-74>)        ],
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-75>)        "responses": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-76>)          "200": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-77>)            "description": "A list of pets (echoed query params).",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-78>)            "content": { "application/json": { "schema": { "type": "object" } } }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-79>)          }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-80>)        }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-81>)      }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-82>)    },
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-83>)    "/post": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-84>)      "post": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-85>)        "summary": "Create a pet (Simulated)",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-86>)        "operationId": "createPet",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-87>)        "description": "Simulates adding a new pet. Uses httpbin's /post endpoint which echoes the request body.",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-88>)        "requestBody": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-89>)          "description": "Pet object to add",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-90>)          "required": true,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-91>)          "content": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-92>)            "application/json": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-93>)              "schema": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-94>)                "type": "object",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-95>)                "required": ["name"],
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-96>)                "properties": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-97>)                  "name": {"type": "string", "description": "Name of the pet"},
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-98>)                  "tag": {"type": "string", "description": "Optional tag for the pet"}
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-99>)                }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-100>)              }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-101>)            }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-102>)          }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-103>)        },
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-104>)        "responses": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-105>)          "201": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-106>)            "description": "Pet created successfully (echoed request body).",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-107>)            "content": { "application/json": { "schema": { "type": "object" } } }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-108>)          }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-109>)        }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-110>)      }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-111>)    },
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-112>)    "/get?petId={petId}": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-113>)      "get": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-114>)        "summary": "Info for a specific pet (Simulated)",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-115>)        "operationId": "showPetById",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-116>)        "description": "Simulates returning info for a pet ID. Uses httpbin's /get endpoint.",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-117>)        "parameters": [
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-118>)          {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-119>)            "name": "petId",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-120>)            "in": "path",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-121>)            "description": "This is actually passed as a query param to httpbin /get",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-122>)            "required": true,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-123>)            "schema": { "type": "integer", "format": "int64" }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-124>)          }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-125>)        ],
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-126>)        "responses": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-127>)          "200": {
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-128>)            "description": "Information about the pet (echoed query params)",
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-129>)            "content": { "application/json": { "schema": { "type": "object" } } }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-130>)          },
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-131>)          "404": { "description": "Pet not found (simulated)" }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-132>)        }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-133>)      }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-134>)    }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-135>)  }
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-136>)}
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-137>)"""
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-138>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-139>)# --- Create OpenAPIToolset ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-140>)petstore_toolset = OpenAPIToolset(
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-141>)    spec_str=openapi_spec_string,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-142>)    spec_str_type='json',
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-143>)    # No authentication needed for httpbin.org
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-144>))
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-145>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-146>)# --- Agent Definition ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-147>)root_agent = LlmAgent(
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-148>)    name=AGENT_NAME_OPENAPI,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-149>)    model=GEMINI_MODEL,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-150>)    tools=[petstore_toolset], # Pass the list of RestApiTool objects
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-151>)    instruction="""You are a Pet Store assistant managing pets via an API.
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-152>)    Use the available tools to fulfill user requests.
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-153>)    When creating a pet, confirm the details echoed back by the API.
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-154>)    When listing pets, mention any filters used (like limit or status).
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-155>)    When showing a pet by ID, state the ID you requested.
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-156>)    """,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-157>)    description="Manages a Pet Store using tools generated from an OpenAPI spec."
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-158>))
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-159>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-160>)# --- Session and Runner Setup ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-161>)async def setup_session_and_runner():
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-162>)    session_service_openapi = InMemorySessionService()
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-163>)    runner_openapi = Runner(
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-164>)        agent=root_agent,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-165>)        app_name=APP_NAME_OPENAPI,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-166>)        session_service=session_service_openapi,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-167>)    )
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-168>)    await session_service_openapi.create_session(
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-169>)        app_name=APP_NAME_OPENAPI,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-170>)        user_id=USER_ID_OPENAPI,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-171>)        session_id=SESSION_ID_OPENAPI,
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-172>)    )
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-173>)    return runner_openapi
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-174>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-175>)# --- Agent Interaction Function ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-176>)async def call_openapi_agent_async(query, runner_openapi):
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-177>)    print("\n--- Running OpenAPI Pet Store Agent ---")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-178>)    print(f"Query: {query}")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-179>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-180>)    content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-181>)    final_response_text = "Agent did not provide a final text response."
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-182>)    try:
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-183>)        async for event in runner_openapi.run_async(
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-184>)            user_id=USER_ID_OPENAPI, session_id=SESSION_ID_OPENAPI, new_message=content
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-185>)            ):
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-186>)            # Optional: Detailed event logging for debugging
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-187>)            # print(f"  DEBUG Event: Author={event.author}, Type={'Final' if event.is_final_response() else 'Intermediate'}, Content={str(event.content)[:100]}...")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-188>)            if event.get_function_calls():
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-189>)                call = event.get_function_calls()[0]
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-190>)                print(f"  Agent Action: Called function '{call.name}' with args {call.args}")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-191>)            elif event.get_function_responses():
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-192>)                response = event.get_function_responses()[0]
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-193>)                print(f"  Agent Action: Received response for '{response.name}'")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-194>)                # print(f"  Tool Response Snippet: {str(response.response)[:200]}...") # Uncomment for response details
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-195>)            elif event.is_final_response() and event.content and event.content.parts:
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-196>)                # Capture the last final text response
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-197>)                final_response_text = event.content.parts[0].text.strip()
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-198>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-199>)        print(f"Agent Final Response: {final_response_text}")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-200>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-201>)    except Exception as e:
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-202>)        print(f"An error occurred during agent run: {e}")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-203>)        import traceback
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-204>)        traceback.print_exc() # Print full traceback for errors
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-205>)    print("-" * 30)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-206>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-207>)# --- Run Examples ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-208>)async def run_openapi_example():
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-209>)    runner_openapi = await setup_session_and_runner()
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-210>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-211>)    # Trigger listPets
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-212>)    await call_openapi_agent_async("Show me the pets available.", runner_openapi)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-213>)    # Trigger createPet
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-214>)    await call_openapi_agent_async("Please add a new dog named 'Dukey'.", runner_openapi)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-215>)    # Trigger showPetById
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-216>)    await call_openapi_agent_async("Get info for pet with ID 123.", runner_openapi)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-217>)
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-218>)# --- Execute ---
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-219>)if __name__ == "__main__":
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-220>)    print("Executing OpenAPI example...")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-221>)    # Use asyncio.run() for top-level execution
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-222>)    try:
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-223>)        asyncio.run(run_openapi_example())
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-224>)    except RuntimeError as e:
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-225>)        if "cannot be called from a running event loop" in str(e):
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-226>)            print("Info: Cannot run asyncio.run from a running event loop (e.g., Jupyter/Colab).")
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-227>)            # If in Jupyter/Colab, you might need to run like this:
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-228>)            # await run_openapi_example()
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-229>)        else:
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-230>)            raise e
    [](<https://adk.dev/tools-custom/openapi-tools/#__codelineno-2-231>)    print("OpenAPI example finished.")
    
Back to top 