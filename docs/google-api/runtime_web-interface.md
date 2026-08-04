# Use the Web Interface - Agent Development Kit (ADK)

> Source: [https://adk.dev/runtime/web-interface/](https://adk.dev/runtime/web-interface/)

[ Skip to content ](<https://adk.dev/runtime/web-interface/#use-the-web-interface>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/runtime/web-interface/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/runtime/web-interface/index.md> "View this page as Markdown")

# Use the Web Interface[¶](<https://adk.dev/runtime/web-interface/#use-the-web-interface> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0

The ADK web interface lets you test your agents directly in the browser. This tool provides a simple way to interactively develop and debug your agents.

![ADK Web Interface](https://adk.dev/assets/adk-web-dev-ui-chat.png)

Caution: ADK Web for development only

ADK Web is **_not meant for use in production deployments_**. You should use ADK Web for development and debugging purposes only.

Key features of the ADK web interface include:

  * **Chat interface** : Send messages to your agents and view responses in real-time
  * **Session management** : Create and switch between sessions
  * **State inspection** : View and modify session state during development
  * **Event history** : Inspect all events generated during agent execution
  * **Visual Builder** : Design agents visually with a drag-and-drop workflow editor and an AI-powered assistant (Python only, [learn more](<https://adk.dev/visual-builder/>))

## Start the web interface[¶](<https://adk.dev/runtime/web-interface/#start-the-web-interface> "Permanent link")

Use the following command to start the ADK web interface:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-0-1>)adk web
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-1-1>)npx adk web
    
In Go, the web interface is not a standalone CLI tool. Instead, you embed the launcher directly in your agent's `main.go` and pass arguments at runtime. The `full.NewLauncher()` helper bundles the web server, REST API, and Web UI into a single binary:

main.go
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-1>)import (
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-2>)    "google.golang.org/adk/v2/cmd/launcher"
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-3>)    "google.golang.org/adk/v2/cmd/launcher/full"
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-4>))
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-5>)
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-6>)func main() {
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-7>)    // ... build your agent and config ...
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-8>)    l := full.NewLauncher()
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-9>)    if err := l.Execute(ctx, config, os.Args[1:]); err != nil {
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-10>)        log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-11>)    }
    [](<https://adk.dev/runtime/web-interface/#__codelineno-2-12>)}
    
Then start the web interface by passing the `web`, `api`, and `webui` subcommands on the command line:
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-3-1>)go run agent.go web api webui
    
The `web` keyword activates the HTTP server. `api` adds the ADK REST API backend, and `webui` serves the browser-based chat interface. Both `api` and `webui` are required to use the web interface together; either can be omitted if you only need the API or UI independently.

Make sure to update the port number.

MavenGradle

With Maven, compile and run the ADK web server: 
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-4-1>)mvn compile exec:java \
    [](<https://adk.dev/runtime/web-interface/#__codelineno-4-2>) -Dexec.args="--adk.agents.source-dir=src/main/java/agents --server.port=8000"
    
With Gradle, the `build.gradle` or `build.gradle.kts` build file should have the following Java plugin in its plugins section:
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-5-1>)plugins {
    [](<https://adk.dev/runtime/web-interface/#__codelineno-5-2>)    id('java')
    [](<https://adk.dev/runtime/web-interface/#__codelineno-5-3>)    // other plugins
    [](<https://adk.dev/runtime/web-interface/#__codelineno-5-4>)}
    
Then, elsewhere in the build file, at the top-level, create a new task:
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-6-1>)tasks.register('runADKWebServer', JavaExec) {
    [](<https://adk.dev/runtime/web-interface/#__codelineno-6-2>)    dependsOn classes
    [](<https://adk.dev/runtime/web-interface/#__codelineno-6-3>)    classpath = sourceSets.main.runtimeClasspath
    [](<https://adk.dev/runtime/web-interface/#__codelineno-6-4>)    mainClass = 'com.google.adk.web.AdkWebServer'
    [](<https://adk.dev/runtime/web-interface/#__codelineno-6-5>)    args '--adk.agents.source-dir=src/main/java/agents', '--server.port=8000'
    [](<https://adk.dev/runtime/web-interface/#__codelineno-6-6>)}
    
Finally, on the command-line, run the following command: 
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-7-1>)gradle runADKWebServer
    
In Java, the web interface and the API server are bundled together.

Once started, the server prints the access URL to the console. Open it in your browser to use the web interface:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-8-1>)+-----------------------------------------------------------------------------+
    [](<https://adk.dev/runtime/web-interface/#__codelineno-8-2>)| ADK Web Server started                                                      |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-8-3>)|                                                                             |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-8-4>)| For local testing, access at http://localhost:8000.                         |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-8-5>)+-----------------------------------------------------------------------------+
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-9-1>)+-----------------------------------------------------------------------------+
    [](<https://adk.dev/runtime/web-interface/#__codelineno-9-2>)| ADK Web Server started                                                      |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-9-3>)|                                                                             |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-9-4>)| For local testing, access at http://localhost:8000.                         |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-9-5>)+-----------------------------------------------------------------------------+
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-10-1>)2025/01/01 00:00:00 Starting the web server: &{port:8080 ...}
    [](<https://adk.dev/runtime/web-interface/#__codelineno-10-2>)2025/01/01 00:00:00 Web servers starts on http://localhost:8080
    [](<https://adk.dev/runtime/web-interface/#__codelineno-10-3>)2025/01/01 00:00:00        webui:  you can access API using http://localhost:8080/ui/
    [](<https://adk.dev/runtime/web-interface/#__codelineno-10-4>)2025/01/01 00:00:00        api:  you can access API using http://localhost:8080/api
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-11-1>)+-----------------------------------------------------------------------------+
    [](<https://adk.dev/runtime/web-interface/#__codelineno-11-2>)| ADK Web Server started                                                      |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-11-3>)|                                                                             |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-11-4>)| For local testing, access at http://localhost:8000.                         |
    [](<https://adk.dev/runtime/web-interface/#__codelineno-11-5>)+-----------------------------------------------------------------------------+
    
## Common options[¶](<https://adk.dev/runtime/web-interface/#common-options> "Permanent link")

PythonTypeScriptGo

Here are some commonly used options for the `adk web` command. Run `adk web --help` to see all available options.

Option | Description | Default  
---|---|---  
`--port` | Port to run the server on | `8000`  
`--host` | Host binding address | `127.0.0.1`  
`--session_service_uri` | Custom session storage URI | In-memory  
`--artifact_service_uri` | Custom artifact storage URI | Local `.adk/artifacts`  
`--reload/--no-reload` | Enable auto-reload on code changes | `true`  
  
For example:
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-12-1>)adk web --port 3000 --session_service_uri "sqlite:///sessions.db"
    
Here are some commonly used options for the `adk web` command. Run `adk web --help` to see all available options.

Option | Description | Default  
---|---|---  
`--port` | Port to run the server on | `8000`  
`--host` | Host binding address | `127.0.0.1`  
`--session_service_uri` | Custom session storage URI | In-memory  
`--artifact_service_uri` | Custom artifact storage URI | Local `.adk/artifacts`  
`--reload/--no-reload` | Enable auto-reload on code changes | `true`  
  
For example:
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-13-1>)adk web --port 3000 --session_service_uri "sqlite:///sessions.db"
    
Go flags differ from Python/TypeScript

The Go web launcher does not use the same flags as `adk web` in Python or TypeScript. Options like `--host`, `--session_service_uri`, `--artifact_service_uri`, and `--reload` are not available. Session and artifact services are configured in Go code when constructing the `launcher.Config`, not via command-line flags.

Flags are split across the `web`, `api`, and `webui` subcommands. Pass flags after the relevant subcommand keyword.

**`web` subcommand flags** (passed directly after `web`):

Flag | Description | Default  
---|---|---  
`-port` | Port for the HTTP server | `8080`  
`-write-timeout` | Timeout for writing HTTP responses | `15s`  
`-read-timeout` | Timeout for reading HTTP requests | `15s`  
`-idle-timeout` | Keep-alive idle connection timeout | `60s`  
`-shutdown-timeout` | Graceful shutdown wait time | `15s`  
`-otel_to_cloud` | Export OpenTelemetry data to GCP | `false`  
  
**`api` subcommand flags** (passed after `api`):

Flag | Description | Default  
---|---|---  
`-webui_address` | WebUI origin allowed for CORS | `localhost:8080`  
`-path_prefix` | URL path prefix for the REST API | `/api`  
`-sse-write-timeout` | Timeout for SSE (streaming) responses | `120s`  
`-trace_capacity` | Max in-memory traces to retain | `10000`  
  
**`webui` subcommand flags** (passed after `webui`):

Flag | Description | Default  
---|---|---  
`-api_server_address` | REST API URL as seen from the browser | `http://localhost:8080/api`  
  
For example, to run on port 9090 with a custom API prefix:
    
    [](<https://adk.dev/runtime/web-interface/#__codelineno-14-1>)go run agent.go web -port 9090 api -path_prefix /myapi webui -api_server_address http://localhost:9090/myapi
    
Back to top 