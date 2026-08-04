# Command Line - Agent Development Kit (ADK)

> Source: [https://adk.dev/runtime/command-line/](https://adk.dev/runtime/command-line/)

[ Skip to content ](<https://adk.dev/runtime/command-line/#use-the-command-line>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/runtime/command-line.md> "Edit this page on GitHub") [ ](<https://adk.dev/runtime/command-line/index.md> "View this page as Markdown")

# Use the Command Line[¶](<https://adk.dev/runtime/command-line/#use-the-command-line> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0

ADK provides an interactive terminal interface for testing your agents. This is useful for quick testing, scripted interactions, and CI/CD pipelines.

![ADK Run](https://adk.dev/assets/adk-run.png)

## Run an agent[¶](<https://adk.dev/runtime/command-line/#run-an-agent> "Permanent link")

Use the following command to run your agent in the ADK command line interface:

PythonTypeScriptGoJava
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-0-1>)adk run my_agent
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-1-1>)npx @google/adk-devtools run agent.ts
    
In Go, the command-line interface is not a standalone `adk` tool. Instead, you embed the launcher directly in your agent's `main.go`. The `full.NewLauncher()` helper bundles the console, web server, and other modes into a single binary, with **console as the default** when no subcommand keyword is given:

main.go
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-1>)import (
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-2>)    "google.golang.org/adk/v2/cmd/launcher"
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-3>)    "google.golang.org/adk/v2/cmd/launcher/full"
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-4>))
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-5>)
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-6>)func main() {
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-7>)    // ... build your agent and config ...
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-8>)    l := full.NewLauncher()
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-9>)    if err := l.Execute(ctx, config, os.Args[1:]); err != nil {
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-10>)        log.Fatalf("Run failed: %v\n\n%s", err, l.CommandLineSyntax())
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-11>)    }
    [](<https://adk.dev/runtime/command-line/#__codelineno-2-12>)}
    
Run the agent in console mode with either of the following commands:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-3-1>)go run agent.go           # console is the default sublauncher
    [](<https://adk.dev/runtime/command-line/#__codelineno-3-2>)go run agent.go console   # or explicitly name the console subcommand
    
Create an `AgentCliRunner` class (see [Java Quickstart](<https://adk.dev/get-started/java/>)) and run:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-4-1>)mvn compile exec:java -Dexec.mainClass="com.example.agent.AgentCliRunner"
    
This starts an interactive session where you can type queries and see agent responses directly in your terminal.

PythonTypeScriptGoJava
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-5-1>)Running agent my_agent, type exit to exit.
    [](<https://adk.dev/runtime/command-line/#__codelineno-5-2>)[user]: What's the weather in New York?
    [](<https://adk.dev/runtime/command-line/#__codelineno-5-3>)[my_agent]: The weather in New York is sunny with a temperature of 25°C.
    [](<https://adk.dev/runtime/command-line/#__codelineno-5-4>)[user]: exit
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-6-1>)Running agent my_agent, type exit to exit.
    [](<https://adk.dev/runtime/command-line/#__codelineno-6-2>)[user]: What's the weather in New York?
    [](<https://adk.dev/runtime/command-line/#__codelineno-6-3>)[my_agent]: The weather in New York is sunny with a temperature of 25°C.
    [](<https://adk.dev/runtime/command-line/#__codelineno-6-4>)[user]: exit
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-7-1>)User -> What's the weather in New York?
    [](<https://adk.dev/runtime/command-line/#__codelineno-7-2>)
    [](<https://adk.dev/runtime/command-line/#__codelineno-7-3>)Agent -> The weather in New York is sunny with a temperature of 25°C.
    [](<https://adk.dev/runtime/command-line/#__codelineno-7-4>)
    [](<https://adk.dev/runtime/command-line/#__codelineno-7-5>)User ->
    
To exit, press **Ctrl+C** or send EOF (**Ctrl+D**).
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-8-1>)Running agent my_agent, type exit to exit.
    [](<https://adk.dev/runtime/command-line/#__codelineno-8-2>)[user]: What's the weather in New York?
    [](<https://adk.dev/runtime/command-line/#__codelineno-8-3>)[my_agent]: The weather in New York is sunny with a temperature of 25°C.
    [](<https://adk.dev/runtime/command-line/#__codelineno-8-4>)[user]: exit
    
## Session options[¶](<https://adk.dev/runtime/command-line/#session-options> "Permanent link")

Python only

The `--save_session`, `--resume`, `--replay`, and `--session_id` options are available in the Python ADK CLI only. The Go console launcher does not support session save/resume/replay via command-line flags. In Go, session persistence is configured in code by providing a persistent `session.Service` implementation (such as `session/database`) to `launcher.Config`.

The `adk run` command includes options for saving, resuming, and replaying sessions.

### Save sessions[¶](<https://adk.dev/runtime/command-line/#save-sessions> "Permanent link")

To save the session when you exit:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-9-1>)adk run --save_session path/to/my_agent
    
You'll be prompted to enter a session ID, and the session will be saved to `path/to/my_agent/<session_id>.session.json`.

You can also specify the session ID upfront:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-10-1>)adk run --save_session --session_id my_session path/to/my_agent
    
### Resume sessions[¶](<https://adk.dev/runtime/command-line/#resume-sessions> "Permanent link")

To continue a previously saved session:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-11-1>)adk run --resume path/to/my_agent/my_session.session.json path/to/my_agent
    
This loads the previous session state and event history, displays it, and allows you to continue the conversation.

### Replay sessions[¶](<https://adk.dev/runtime/command-line/#replay-sessions> "Permanent link")

To replay a session file without interactive input:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-12-1>)adk run --replay path/to/input.json path/to/my_agent
    
The input file should contain initial state and queries:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-13-1>){
    [](<https://adk.dev/runtime/command-line/#__codelineno-13-2>)  "state": {"key": "value"},
    [](<https://adk.dev/runtime/command-line/#__codelineno-13-3>)  "queries": ["What is 2 + 2?", "What is the capital of France?"]
    [](<https://adk.dev/runtime/command-line/#__codelineno-13-4>)}
    
## Storage options[¶](<https://adk.dev/runtime/command-line/#storage-options> "Permanent link")

Python only

The `--session_service_uri` and `--artifact_service_uri` command-line flags are available in the Python ADK CLI only. In Go, session and artifact services are configured in code when constructing `launcher.Config` — for example, using `session/database` for a persistent database-backed session store, or `artifact/gcsartifact` for Cloud Storage-backed artifacts.

Option | Description | Default  
---|---|---  
`--session_service_uri` | Custom session storage URI | SQLite under `.adk/session.db`  
`--artifact_service_uri` | Custom artifact storage URI | Local `.adk/artifacts`  
`--memory_service_uri` | Custom memory service URI | In-memory  
  
### Example with storage options[¶](<https://adk.dev/runtime/command-line/#example-with-storage-options> "Permanent link")
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-14-1>)adk run --session_service_uri "sqlite:///my_sessions.db" path/to/my_agent
    
## All options[¶](<https://adk.dev/runtime/command-line/#all-options> "Permanent link")

PythonGo

Option | Description  
---|---  
`--save_session` | Save the session to a JSON file on exit  
`--session_id` | Session ID to use when saving  
`--resume` | Path to a saved session file to resume  
`--replay` | Path to an input file for non-interactive replay  
`--session_service_uri` | Custom session storage URI  
`--artifact_service_uri` | Custom artifact storage URI  
`--memory_service_uri` | Custom memory service URI  
  
Go flags differ from Python

The Go console launcher does not support `--save_session`, `--resume`, `--replay`, `--session_id`, `--session_service_uri`, or `--artifact_service_uri`. These are Python CLI features. Session and artifact services are configured in Go code via `launcher.Config`.

Flags are passed after the `console` keyword (or directly if `console` is the default):

Flag | Description | Default  
---|---|---  
`-streaming_mode` | Streaming mode for agent responses (`none`|`sse`) | Auto-detected (TTY → `sse`, pipe → `none`)  
`-shutdown-timeout` | Graceful shutdown wait time | `2s`  
`-otel_to_cloud` | Export OpenTelemetry data to GCP | `false`  
  
For example, to force non-streaming output:
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-15-1>)go run agent.go console -streaming_mode none
    
Or to force SSE streaming (token-by-token output):
    
    [](<https://adk.dev/runtime/command-line/#__codelineno-16-1>)go run agent.go -streaming_mode sse
    
Back to top 