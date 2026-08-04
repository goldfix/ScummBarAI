# API Server - Agent Development Kit (ADK)

> Source: [https://adk.dev/runtime/api-server/](https://adk.dev/runtime/api-server/)

[ Skip to content ](<https://adk.dev/runtime/api-server/#use-the-api-server>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/runtime/api-server.md> "Edit this page on GitHub") [ ](<https://adk.dev/runtime/api-server/index.md> "View this page as Markdown")

# Use the API Server[¶](<https://adk.dev/runtime/api-server/#use-the-api-server> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0

Before you deploy your agent, you should test it to ensure that it is working as intended. Use the API server in ADK to expose your agents through a REST API for programmatic testing and integration.

![ADK API Server](https://adk.dev/assets/adk-api-server.png)

## Start the API server[¶](<https://adk.dev/runtime/api-server/#start-the-api-server> "Permanent link")

Use the following command to run your agent in an ADK API server:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-0-1>)adk api_server
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-1-1>)npx adk api_server
    
In Go, there is no standalone `adk` CLI. Instead, you embed the launcher directly in your agent's `main.go`. The `full.NewLauncher()` helper bundles the REST API, Web UI, and other modes into a single binary:

main.go
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-1>)import (
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-2>)    "google.golang.org/adk/v2/cmd/launcher"
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-3>)    "google.golang.org/adk/v2/cmd/launcher/full"
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-4>))
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-5>)
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-6>)func main() {
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-7>)    // ... build your agent and config ...
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-8>)    l := full.NewLauncher()
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-9>)    if err := l.Execute(ctx, config, os.Args[1:]); err != nil {
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-10>)        log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-11>)    }
    [](<https://adk.dev/runtime/api-server/#__codelineno-2-12>)}
    
Then start the API server by passing the `web` and `api` subcommands on the command line:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-3-1>)go run agent.go web api
    
The `web` keyword activates the HTTP server. `api` adds the ADK REST API backend and registers all routes under the `/api` path prefix by default.

Make sure to update the port number.

MavenGradle

With Maven, compile and run the ADK web server: 
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-4-1>)mvn compile exec:java \
    [](<https://adk.dev/runtime/api-server/#__codelineno-4-2>) -Dexec.args="--adk.agents.source-dir=src/main/java/agents --server.port=8080"
    
With Gradle, the `build.gradle` or `build.gradle.kts` build file should have the following Java plugin in its plugins section:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-5-1>)plugins {
    [](<https://adk.dev/runtime/api-server/#__codelineno-5-2>)    id('java')
    [](<https://adk.dev/runtime/api-server/#__codelineno-5-3>)    // other plugins
    [](<https://adk.dev/runtime/api-server/#__codelineno-5-4>)}
    
Then, elsewhere in the build file, at the top-level, create a new task:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-6-1>)tasks.register('runADKWebServer', JavaExec) {
    [](<https://adk.dev/runtime/api-server/#__codelineno-6-2>)    dependsOn classes
    [](<https://adk.dev/runtime/api-server/#__codelineno-6-3>)    classpath = sourceSets.main.runtimeClasspath
    [](<https://adk.dev/runtime/api-server/#__codelineno-6-4>)    mainClass = 'com.google.adk.web.AdkWebServer'
    [](<https://adk.dev/runtime/api-server/#__codelineno-6-5>)    args '--adk.agents.source-dir=src/main/java/agents', '--server.port=8080'
    [](<https://adk.dev/runtime/api-server/#__codelineno-6-6>)}
    
Finally, on the command-line, run the following command: 
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-7-1>)gradle runADKWebServer
    
In Java, both the Dev UI and the API server are bundled together.

This command will launch a local web server, where you can run cURL commands or send API requests to test your agent. By default, the server runs on `http://localhost:8000`.

Advanced Usage and Debugging

For a complete reference on all available endpoints, request/response formats, and tips for debugging (including how to use the interactive API documentation), see the **ADK API Server Guide** below.

## Test locally[¶](<https://adk.dev/runtime/api-server/#test-locally> "Permanent link")

Testing locally involves launching a local web server, creating a session, and sending queries to your agent. First, ensure you are in the correct working directory.

For TypeScript, you should be inside the agent project directory itself.
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-8-1>)parent_folder/
    [](<https://adk.dev/runtime/api-server/#__codelineno-8-2>)└── my_sample_agent/  <-- For TypeScript, run commands from here
    [](<https://adk.dev/runtime/api-server/#__codelineno-8-3>)    └── agent.py (or Agent.java or agent.ts)
    
**Launch the Local Server**

Next, launch the local server using the commands listed above.

The output should appear similar to:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-9-1>)INFO:     Started server process [12345]
    [](<https://adk.dev/runtime/api-server/#__codelineno-9-2>)INFO:     Waiting for application startup.
    [](<https://adk.dev/runtime/api-server/#__codelineno-9-3>)INFO:     Application startup complete.
    [](<https://adk.dev/runtime/api-server/#__codelineno-9-4>)INFO:     Uvicorn running on http://localhost:8000 (Press CTRL+C to quit)
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-10-1>)+-----------------------------------------------------------------------------+
    [](<https://adk.dev/runtime/api-server/#__codelineno-10-2>)| ADK Web Server started                                                      |
    [](<https://adk.dev/runtime/api-server/#__codelineno-10-3>)|                                                                             |
    [](<https://adk.dev/runtime/api-server/#__codelineno-10-4>)| For local testing, access at http://localhost:8000.                         |
    [](<https://adk.dev/runtime/api-server/#__codelineno-10-5>)+-----------------------------------------------------------------------------+
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-11-1>)2025/01/01 00:00:00 Starting the web server: &{port:8080 ...}
    [](<https://adk.dev/runtime/api-server/#__codelineno-11-2>)2025/01/01 00:00:00 Web servers starts on http://localhost:8080
    [](<https://adk.dev/runtime/api-server/#__codelineno-11-3>)2025/01/01 00:00:00        api:  you can access API using http://localhost:8080/api
    [](<https://adk.dev/runtime/api-server/#__codelineno-11-4>)2025/01/01 00:00:00        api:      for instance: http://localhost:8080/api/list-apps
    
Go: default port and path prefix

The Go API server defaults to port **8080** (not 8000) and serves all REST endpoints under the **`/api`** path prefix by default. Adjust all example `curl` commands below accordingly:

Python/TypeScript/Java | Go  
---|---  
`http://localhost:8000/list-apps` | `http://localhost:8080/api/list-apps`  
`http://localhost:8000/apps/…` | `http://localhost:8080/api/apps/…`  
`http://localhost:8000/run` | `http://localhost:8080/api/run`  
`http://localhost:8000/run_sse` | `http://localhost:8080/api/run_sse`  
  
The port can be changed with the `-port` flag on the `web` subcommand and the prefix can be changed with the `-path_prefix` flag on the `api` subcommand. For example:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-12-1>)go run agent.go web -port 8000 api -path_prefix ""
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-13-1>)2025-05-13T23:32:08.972-06:00  INFO 37864 --- [ebServer.main()] o.s.b.w.embedded.tomcat.TomcatWebServer  : Tomcat started on port 8080 (http) with context path '/'
    [](<https://adk.dev/runtime/api-server/#__codelineno-13-2>)2025-05-13T23:32:08.980-06:00  INFO 37864 --- [ebServer.main()] com.google.adk.web.AdkWebServer          : Started AdkWebServer in 1.15 seconds (process running for 2.877)
    [](<https://adk.dev/runtime/api-server/#__codelineno-13-3>)2025-05-13T23:32:08.981-06:00  INFO 37864 --- [ebServer.main()] com.google.adk.web.AdkWebServer          : AdkWebServer application started successfully.
    
Your server is now running locally. Ensure you use the correct **_port number_** in all the subsequent commands.

**Create a new session**

With the API server still running, open a new terminal window or tab and create a new session with the agent using:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-14-1>)curl -X POST http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_123 \
    [](<https://adk.dev/runtime/api-server/#__codelineno-14-2>)  -H "Content-Type: application/json" \
    [](<https://adk.dev/runtime/api-server/#__codelineno-14-3>)  -d '{"key1": "value1", "key2": 42}'
    
Let's break down what's happening:

  * `http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_123`: This creates a new session for your agent `my_sample_agent`, which is the name of the agent folder, for a user ID (`u_123`) and for a session ID (`s_123`). You can replace `my_sample_agent` with the name of your agent folder. You can replace `u_123` with a specific user ID, and `s_123` with a specific session ID.
  * `{"key1": "value1", "key2": 42}`: This is optional. You can use this to customize the agent's pre-existing state (dict) when creating the session.

This should return the session information if it was created successfully. The output should appear similar to:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-15-1>){"id":"s_123","appName":"my_sample_agent","userId":"u_123","state":{"key1":"value1","key2":42},"events":[],"lastUpdateTime":1743711430.022186}
    
Info

You cannot create multiple sessions with exactly the same user ID and session ID. If you try to, you may see a response, like: `{"detail":"Session already exists: s_123"}`. To fix this, you can either delete that session (e.g., `s_123`), or choose a different session ID.

**Send a query**

There are two ways to send queries via POST to your agent, via the `/run` or `/run_sse` routes.

  * `POST http://localhost:8000/run`: collects all events as a list and returns the list all at once. Suitable for most users (if you are unsure, we recommend using this one).
  * `POST http://localhost:8000/run_sse`: returns as Server-Sent-Events, which is a stream of event objects. Suitable for those who want to be notified as soon as the event is available. With `/run_sse`, you can also set `streaming` to `true` to enable token-level streaming.

**Using`/run`**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-1>)curl -X POST http://localhost:8000/run \
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-2>)-H "Content-Type: application/json" \
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-3>)-d '{
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-4>)"appName": "my_sample_agent",
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-5>)"userId": "u_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-6>)"sessionId": "s_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-7>)"newMessage": {
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-8>)    "role": "user",
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-9>)    "parts": [{
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-10>)    "text": "Hey whats the weather in new york today"
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-11>)    }]
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-12>)}
    [](<https://adk.dev/runtime/api-server/#__codelineno-16-13>)}'
    
In TypeScript, currently only `camelCase` field names are supported (e.g. `appName`, `userId`, `sessionId`, etc.).

If using `/run`, you will see the full output of events at the same time, as a list, which should appear similar to:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-17-1>)[{"content":{"parts":[{"functionCall":{"id":"af-e75e946d-c02a-4aad-931e-49e4ab859838","args":{"city":"new york"},"name":"get_weather"}}],"role":"model"},"invocationId":"e-71353f1e-aea1-4821-aa4b-46874a766853","author":"weather_time_agent","actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"longRunningToolIds":[],"id":"2Btee6zW","timestamp":1743712220.385936},{"content":{"parts":[{"functionResponse":{"id":"af-e75e946d-c02a-4aad-931e-49e4ab859838","name":"get_weather","response":{"status":"success","report":"The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit)."}}}],"role":"user"},"invocationId":"e-71353f1e-aea1-4821-aa4b-46874a766853","author":"weather_time_agent","actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"id":"PmWibL2m","timestamp":1743712221.895042},{"content":{"parts":[{"text":"OK. The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit).\n"}],"role":"model"},"invocationId":"e-71353f1e-aea1-4821-aa4b-46874a766853","author":"weather_time_agent","actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"id":"sYT42eVC","timestamp":1743712221.899018}]
    
**Using`/run_sse`**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-1>)curl -X POST http://localhost:8000/run_sse \
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-2>)-H "Content-Type: application/json" \
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-3>)-d '{
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-4>)"appName": "my_sample_agent",
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-5>)"userId": "u_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-6>)"sessionId": "s_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-7>)"newMessage": {
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-8>)    "role": "user",
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-9>)    "parts": [{
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-10>)    "text": "Hey whats the weather in new york today"
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-11>)    }]
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-12>)},
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-13>)"streaming": false
    [](<https://adk.dev/runtime/api-server/#__codelineno-18-14>)}'
    
You can set `streaming` to `true` to enable token-level streaming, which means the response will be returned to you in multiple chunks and the output should appear similar to:
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-19-1>)data: {"content":{"parts":[{"functionCall":{"id":"af-f83f8af9-f732-46b6-8cb5-7b5b73bbf13d","args":{"city":"new york"},"name":"get_weather"}}],"role":"model"},"invocationId":"e-3f6d7765-5287-419e-9991-5fffa1a75565","author":"weather_time_agent","actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"longRunningToolIds":[],"id":"ptcjaZBa","timestamp":1743712255.313043}
    [](<https://adk.dev/runtime/api-server/#__codelineno-19-2>)
    [](<https://adk.dev/runtime/api-server/#__codelineno-19-3>)data: {"content":{"parts":[{"functionResponse":{"id":"af-f83f8af9-f732-46b6-8cb5-7b5b73bbf13d","name":"get_weather","response":{"status":"success","report":"The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit)."}}}],"role":"user"},"invocationId":"e-3f6d7765-5287-419e-9991-5fffa1a75565","author":"weather_time_agent","actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"id":"5aocxjaq","timestamp":1743712257.387306}
    [](<https://adk.dev/runtime/api-server/#__codelineno-19-4>)
    [](<https://adk.dev/runtime/api-server/#__codelineno-19-5>)data: {"content":{"parts":[{"text":"OK. The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit).\n"}],"role":"model"},"invocationId":"e-3f6d7765-5287-419e-9991-5fffa1a75565","author":"weather_time_agent","actions":{"stateDelta":{},"artifactDelta":{},"requestedAuthConfigs":{}},"id":"rAnWGSiV","timestamp":1743712257.391317}
    
**Send a query with a base64 encoded file using`/run` or `/run_sse`**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-1>)curl -X POST http://localhost:8000/run \
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-2>)-H 'Content-Type: application/json' \
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-3>)-d '{
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-4>)   "appName":"my_sample_agent",
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-5>)   "userId":"u_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-6>)   "sessionId":"s_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-7>)   "newMessage":{
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-8>)      "role":"user",
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-9>)      "parts":[
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-10>)         {
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-11>)            "text":"Describe this image"
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-12>)         },
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-13>)         {
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-14>)            "inlineData":{
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-15>)               "displayName":"my_image.png",
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-16>)               "data":"iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAACXBIWXMAAAsTAAALEwEAmpw...",
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-17>)               "mimeType":"image/png"
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-18>)            }
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-19>)         }
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-20>)      ]
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-21>)   },
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-22>)   "streaming":false
    [](<https://adk.dev/runtime/api-server/#__codelineno-20-23>)}'
    
Info

If you are using `/run_sse`, you should see each event as soon as it becomes available.

## Integrations[¶](<https://adk.dev/runtime/api-server/#integrations> "Permanent link")

ADK uses [Callbacks](<https://adk.dev/callbacks/>) to integrate with third-party observability tools. These integrations capture detailed traces of agent calls and interactions, which are crucial for understanding behavior, debugging issues, and evaluating performance.

  * [Comet Opik](<https://github.com/comet-ml/opik>) is an open-source LLM observability and evaluation platform that [natively supports ADK](<https://www.comet.com/docs/opik/tracing/integrations/adk>).

## Deploy your agent[¶](<https://adk.dev/runtime/api-server/#deploy-your-agent> "Permanent link")

Now that you've verified the local operation of your agent, you're ready to move on to deploying your agent! Here are some ways you can deploy your agent:

  * Deploy to [Agent Runtime](<https://adk.dev/deploy/agent-runtime/>), a simple way to deploy your ADK agents to a managed service on Agent Platform on Google Cloud.
  * Deploy to [Cloud Run](<https://adk.dev/deploy/cloud-run/>) and have full control over how you scale and manage your agents using serverless architecture on Google Cloud.

## Interactive API docs[¶](<https://adk.dev/runtime/api-server/#interactive-api-docs> "Permanent link")

Python and TypeScript only

Swagger UI interactive documentation is served at `/docs` by the Python and TypeScript ADK API servers only. The Go API server does not expose a `/docs` endpoint. To explore the Go REST API, use the endpoint reference below or send requests directly with `curl`.

The API server automatically generates interactive API documentation using Swagger UI. This is an invaluable tool for exploring endpoints, understanding request formats, and testing your agent directly from your browser.

To access the interactive docs, start the API server and navigate to <http://localhost:8000/docs> in your web browser.

You will see a complete, interactive list of all available API endpoints, which you can expand to see detailed information about parameters, request bodies, and response schemas. You can even click "Try it out" to send live requests to your running agents.

## API endpoints[¶](<https://adk.dev/runtime/api-server/#api-endpoints> "Permanent link")

The following sections detail the primary endpoints for interacting with your agents.

JSON Naming Convention

  * **Both Request and Response bodies** will use `camelCase` for field names (e.g., `"appName"`).

### Utility endpoints[¶](<https://adk.dev/runtime/api-server/#utility-endpoints> "Permanent link")

#### List available agents[¶](<https://adk.dev/runtime/api-server/#list-available-agents> "Permanent link")

Returns a list of all agent applications discovered by the server.

  * **Method:** `GET`
  * **Path:** `/list-apps`

**Example Request**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-21-1>)curl -X GET http://localhost:8000/list-apps
    
**Example Response**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-22-1>)["my_sample_agent", "another_agent"]
    
* * *

### Session management[¶](<https://adk.dev/runtime/api-server/#session-management> "Permanent link")

Sessions store the state and event history for a specific user's interaction with an agent.

#### Update a session[¶](<https://adk.dev/runtime/api-server/#update-a-session> "Permanent link")

Not available in Go

The `PATCH` session update endpoint is not implemented in the Go ADK REST API server. To modify session state in Go, pass a `stateDelta` field in your `/run` or `/run_sse` request body instead.

Updates an existing session.

  * **Method:** `PATCH`
  * **Path:** `/apps/{app_name}/users/{user_id}/sessions/{session_id}`

**Request Body**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-23-1>){
    [](<https://adk.dev/runtime/api-server/#__codelineno-23-2>)  "stateDelta": {
    [](<https://adk.dev/runtime/api-server/#__codelineno-23-3>)    "key1": "value1",
    [](<https://adk.dev/runtime/api-server/#__codelineno-23-4>)    "key2": 42
    [](<https://adk.dev/runtime/api-server/#__codelineno-23-5>)  }
    [](<https://adk.dev/runtime/api-server/#__codelineno-23-6>)}
    
**Example Request**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-24-1>)curl -X PATCH http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_abc \
    [](<https://adk.dev/runtime/api-server/#__codelineno-24-2>)  -H "Content-Type: application/json" \
    [](<https://adk.dev/runtime/api-server/#__codelineno-24-3>)  -d '{"stateDelta":{"visit_count": 5}}'
    
**Example Response**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-25-1>){"id":"s_abc","appName":"my_sample_agent","userId":"u_123","state":{"visit_count":5},"events":[],"lastUpdateTime":1743711430.022186}
    
#### Get a session[¶](<https://adk.dev/runtime/api-server/#get-a-session> "Permanent link")

Retrieves the details of a specific session, including its current state and all associated events.

  * **Method:** `GET`
  * **Path:** `/apps/{app_name}/users/{user_id}/sessions/{session_id}`

**Example Request**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-26-1>)curl -X GET http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_abc
    
**Example Response**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-27-1>){"id":"s_abc","appName":"my_sample_agent","userId":"u_123","state":{"visit_count":5},"events":[...],"lastUpdateTime":1743711430.022186}
    
#### Delete a session[¶](<https://adk.dev/runtime/api-server/#delete-a-session> "Permanent link")

Deletes a session and all of its associated data.

  * **Method:** `DELETE`
  * **Path:** `/apps/{app_name}/users/{user_id}/sessions/{session_id}`

**Example Request**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-28-1>)curl -X DELETE http://localhost:8000/apps/my_sample_agent/users/u_123/sessions/s_abc
    
**Example Response** A successful deletion returns an empty response. Python and TypeScript return a `204 No Content` status code. Go returns `200 OK` with an empty body.

* * *

### Agent execution[¶](<https://adk.dev/runtime/api-server/#agent-execution> "Permanent link")

These endpoints are used to send a new message to an agent and get a response.

#### Run agent (single response)[¶](<https://adk.dev/runtime/api-server/#run-agent-single-response> "Permanent link")

Executes the agent and returns all generated events in a single JSON array after the run is complete.

  * **Method:** `POST`
  * **Path:** `/run`

**Request Body**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-1>){
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-2>)  "appName": "my_sample_agent",
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-3>)  "userId": "u_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-4>)  "sessionId": "s_abc",
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-5>)  "newMessage": {
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-6>)    "role": "user",
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-7>)    "parts": [
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-8>)      { "text": "What is the capital of France?" }
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-9>)    ]
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-10>)  }
    [](<https://adk.dev/runtime/api-server/#__codelineno-29-11>)}
    
In TypeScript, currently only `camelCase` field names are supported (e.g. `appName`, `userId`, `sessionId`, etc.).

**Example Request**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-1>)curl -X POST http://localhost:8000/run \
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-2>)  -H "Content-Type: application/json" \
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-3>)  -d '{
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-4>)    "appName": "my_sample_agent",
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-5>)    "userId": "u_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-6>)    "sessionId": "s_abc",
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-7>)    "newMessage": {
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-8>)      "role": "user",
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-9>)      "parts": [{"text": "What is the capital of France?"}]
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-10>)    }
    [](<https://adk.dev/runtime/api-server/#__codelineno-30-11>)  }'
    
#### Run agent (streaming)[¶](<https://adk.dev/runtime/api-server/#run-agent-streaming> "Permanent link")

Executes the agent and streams events back to the client as they are generated using [Server-Sent Events (SSE)](<https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events>).

  * **Method:** `POST`
  * **Path:** `/run_sse`

**Request Body** The request body is the same as for `/run`, with an additional optional `streaming` flag. 
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-1>){
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-2>)  "appName": "my_sample_agent",
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-3>)  "userId": "u_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-4>)  "sessionId": "s_abc",
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-5>)  "newMessage": {
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-6>)    "role": "user",
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-7>)    "parts": [
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-8>)      { "text": "What is the weather in New York?" }
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-9>)    ]
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-10>)  },
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-11>)  "streaming": true
    [](<https://adk.dev/runtime/api-server/#__codelineno-31-12>)}
    
\- `streaming`: (Optional) Set to `true` to enable token-level streaming for model responses. Defaults to `false`.

**Example Request**
    
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-1>)curl -X POST http://localhost:8000/run_sse \
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-2>)  -H "Content-Type: application/json" \
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-3>)  -d '{
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-4>)    "appName": "my_sample_agent",
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-5>)    "userId": "u_123",
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-6>)    "sessionId": "s_abc",
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-7>)    "newMessage": {
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-8>)      "role": "user",
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-9>)      "parts": [{"text": "What is the weather in New York?"}]
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-10>)    },
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-11>)    "streaming": false
    [](<https://adk.dev/runtime/api-server/#__codelineno-32-12>)  }'
    
Back to top 