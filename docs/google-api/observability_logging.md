# Logging - Agent Development Kit (ADK)

> Source: [https://adk.dev/observability/logging/](https://adk.dev/observability/logging/)

[ Skip to content ](<https://adk.dev/observability/logging/#agent-activity-logging>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/observability/logging.md> "Edit this page on GitHub") [ ](<https://adk.dev/observability/logging/index.md> "View this page as Markdown")

# Agent activity logging[¶](<https://adk.dev/observability/logging/#agent-activity-logging> "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0Kotlin v0.1.0

Agent Development Kit (ADK) provides flexible and powerful logging capabilities to monitor agent behavior and debug issues effectively.

## Logging philosophy[¶](<https://adk.dev/observability/logging/#logging-philosophy> "Permanent link")

ADK's approach to logging is to provide detailed diagnostic information without being overly verbose by default. It is designed to be configured by the application developer, allowing you to tailor the log output to your specific needs, whether in a development or production environment.

  * **Standard Library Integration:** ADK uses the standard logging facilities of the host language (e.g., Python's `logging` module, Go's `log` package).
  * **Structured GenAI Logging:** ADK uses OpenTelemetry to log structured events for GenAI requests and responses, allowing for advanced monitoring and debugging in cloud environments.
  * **User-Configured:** While ADK provides defaults and integration with its CLI tools, it is ultimately the responsibility of the application developer to configure logging to suit their specific environment.

## Logging schema[¶](<https://adk.dev/observability/logging/#logging-schema> "Permanent link")

ADK emits logs using standard library facilities and structured GenAI events via OpenTelemetry.

### Structured GenAI logs[¶](<https://adk.dev/observability/logging/#structured-genai-logs> "Permanent link")

Structured GenAI logs emitted via OpenTelemetry follow the [Semantic Conventions for GenAI](<https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-events.md>).

By default prompt content is elided in logs for security. You can enable prompt logging using environment variables or programmatic configuration (see Setup section below).

### Log levels (Python)[¶](<https://adk.dev/observability/logging/#log-levels-python> "Permanent link")

The following table describes what is logged at different levels in Python when using the standard logger:

Level | Description | Type of Information Logged  
---|---|---  
**`DEBUG`** | **Crucial for debugging.** The most verbose level for fine-grained diagnostic information. | 

  * **Full LLM Prompts:** The complete request sent to the language model, including system instructions, history, and tools.
  * Detailed API responses from services.
  * Internal state transitions and variable values.

**`INFO`** | General information about the agent's lifecycle. | 

  * Agent initialization and startup.
  * Session creation and deletion events.
  * Execution of a tool, including its name and arguments.

**`WARNING`** | Indicates a potential issue or deprecated feature use. The agent continues to function, but attention may be required. | 

  * Use of deprecated methods or parameters.
  * Non-critical errors that the system recovered from.

**`ERROR`** | A serious error that prevented an operation from completing. | 

  * Failed API calls to external services (e.g., LLM, Session Service).
  * Unhandled exceptions during agent execution.
  * Configuration errors.

Note

It is recommended to use `INFO` or `WARNING` in production environments. Only enable `DEBUG` when actively troubleshooting an issue, as `DEBUG` logs can be very verbose and may contain sensitive information.

## Logging setup[¶](<https://adk.dev/observability/logging/#logging-setup> "Permanent link")

### Logging in ADK Web[¶](<https://adk.dev/observability/logging/#logging-in-adk-web> "Permanent link")

When running agents using the ADK's `adk web`, `adk api_server`, `adk deploy cloud_run` and `adk deploy gke` commands, you can control the log verbosity or destination.

#### Logging level[¶](<https://adk.dev/observability/logging/#logging-level> "Permanent link")

To start the web server with `DEBUG` level logging, run:
    
    [](<https://adk.dev/observability/logging/#__codelineno-0-1>)adk web --log_level DEBUG path/to/your/agents_dir
    
The available log levels for the `--log_level` option are: `DEBUG`, `INFO` (default), `WARNING`, `ERROR`, `CRITICAL`.

#### Capture prompt content[¶](<https://adk.dev/observability/logging/#capture-prompt-content> "Permanent link")

By default a prompt content is elided in logs for security. You can enable prompt logging using the environment variable:
    
    [](<https://adk.dev/observability/logging/#__codelineno-1-1>)export OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true
    
Warning

The `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT` setting logs the full content of user prompts and agent responses. This is useful for debugging but may capture sensitive data or PII. In production, set this to false or ensure you have appropriate data handling policies in place.

#### OTLP export[¶](<https://adk.dev/observability/logging/#otlp-export> "Permanent link")

To export logs to an OTLP-compatible backend, set the standard OTel environment variables:
    
    [](<https://adk.dev/observability/logging/#__codelineno-2-1>)export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT="http://your-collector:4318/v1/logs"
    [](<https://adk.dev/observability/logging/#__codelineno-2-2>)adk web path/to/your/agents_dir
    
Note

You can also set the general `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable if you would like to send metrics and traces to the same endpoint in addition to logs.

#### GCP export setup[¶](<https://adk.dev/observability/logging/#gcp-export-setup> "Permanent link")

You can enable GCP export using the `--otel_to_cloud` flag:
    
    [](<https://adk.dev/observability/logging/#__codelineno-3-1>)adk web --otel_to_cloud path/to/your/agents_dir
    
### Python programmatic setup[¶](<https://adk.dev/observability/logging/#python-programmatic-setup> "Permanent link")

In Python, ADK uses the standard `logging` module and OpenTelemetry for structured GenAI logs.

#### Logging level[¶](<https://adk.dev/observability/logging/#logging-level_1> "Permanent link")

To enable detailed logging, including `DEBUG` level messages, add the following to the top of your script:
    
    [](<https://adk.dev/observability/logging/#__codelineno-4-1>)import logging
    [](<https://adk.dev/observability/logging/#__codelineno-4-2>)
    [](<https://adk.dev/observability/logging/#__codelineno-4-3>)logging.basicConfig(
    [](<https://adk.dev/observability/logging/#__codelineno-4-4>)    level=logging.DEBUG,
    [](<https://adk.dev/observability/logging/#__codelineno-4-5>)    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
    [](<https://adk.dev/observability/logging/#__codelineno-4-6>))
    
#### Capture prompt content[¶](<https://adk.dev/observability/logging/#capture-prompt-content_1> "Permanent link")

You can enable full prompt logging programmatically by setting an environment variable:
    
    [](<https://adk.dev/observability/logging/#__codelineno-5-1>)import os
    [](<https://adk.dev/observability/logging/#__codelineno-5-2>)
    [](<https://adk.dev/observability/logging/#__codelineno-5-3>)os.environ["OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT"] = "true"
    
#### OTLP export[¶](<https://adk.dev/observability/logging/#otlp-export_1> "Permanent link")

To export logs to an OpenTelemetry Collector (or an OTLP-compatible backend) programmatically:
    
    [](<https://adk.dev/observability/logging/#__codelineno-6-1>)from google.adk.telemetry.setup import maybe_set_otel_providers
    [](<https://adk.dev/observability/logging/#__codelineno-6-2>)import os
    [](<https://adk.dev/observability/logging/#__codelineno-6-3>)
    [](<https://adk.dev/observability/logging/#__codelineno-6-4>)os.environ["OTEL_EXPORTER_OTLP_LOGS_ENDPOINT"] = "http://your-collector:4318/v1/logs"
    [](<https://adk.dev/observability/logging/#__codelineno-6-5>)os.environ["OTEL_SERVICE_NAME"] = "your-adk-agent"
    [](<https://adk.dev/observability/logging/#__codelineno-6-6>)os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "key1=value1,key2=value2"
    [](<https://adk.dev/observability/logging/#__codelineno-6-7>)maybe_set_otel_providers()
    
#### GCP export setup[¶](<https://adk.dev/observability/logging/#gcp-export-setup_1> "Permanent link")

To export logs to Google Cloud Logging programmatically, use the OpenTelemetry Google Cloud exporter. Here is an example in Python:
    
    [](<https://adk.dev/observability/logging/#__codelineno-7-1>)from google.adk.telemetry.google_cloud import get_gcp_exporters
    [](<https://adk.dev/observability/logging/#__codelineno-7-2>)from google.adk.telemetry.setup import maybe_set_otel_providers
    [](<https://adk.dev/observability/logging/#__codelineno-7-3>)import os
    [](<https://adk.dev/observability/logging/#__codelineno-7-4>)
    [](<https://adk.dev/observability/logging/#__codelineno-7-5>)gcp_exporters = get_gcp_exporters(
    [](<https://adk.dev/observability/logging/#__codelineno-7-6>)  enable_cloud_logging = True,
    [](<https://adk.dev/observability/logging/#__codelineno-7-7>))
    [](<https://adk.dev/observability/logging/#__codelineno-7-8>)os.environ["OTEL_SERVICE_NAME"] = "your-adk-agent"
    [](<https://adk.dev/observability/logging/#__codelineno-7-9>)os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "key1=value1,key2=value2"
    [](<https://adk.dev/observability/logging/#__codelineno-7-10>)maybe_set_otel_providers([gcp_exporters])
    
### Kotlin programmatic setup[¶](<https://adk.dev/observability/logging/#kotlin-programmatic-setup> "Permanent link")

In Kotlin, ADK uses standard JVM logging facilities (defaulting to Flogger) and OpenTelemetry for structured GenAI logs.

#### Capture prompt content[¶](<https://adk.dev/observability/logging/#capture-prompt-content_2> "Permanent link")

You can enable full prompt logging by configuring the global `TelemetryConfig`:
    
    [](<https://adk.dev/observability/logging/#__codelineno-8-1>)--8<-- "examples/kotlin/snippets/observability/LoggingExamples.kt:
    [](<https://adk.dev/observability/logging/#__codelineno-8-2>)capture_content"
    
#### Activity logging with Plugins[¶](<https://adk.dev/observability/logging/#activity-logging-with-plugins> "Permanent link")

To get detailed logs of agent activity (user messages, model requests/responses, tool calls) in the console, use the `LoggingPlugin`:
    
    [](<https://adk.dev/observability/logging/#__codelineno-9-1>)// Use the LoggingPlugin for structured activity logging to the console
    [](<https://adk.dev/observability/logging/#__codelineno-9-2>)val runner =
    [](<https://adk.dev/observability/logging/#__codelineno-9-3>)    InMemoryRunner(
    [](<https://adk.dev/observability/logging/#__codelineno-9-4>)        App(appName = agent.name, rootAgent = agent, plugins = listOf(LoggingPlugin())),
    [](<https://adk.dev/observability/logging/#__codelineno-9-5>)    )
    
### Go programmatic setup[¶](<https://adk.dev/observability/logging/#go-programmatic-setup> "Permanent link")

In Go, ADK uses the `google.golang.org/adk/v2/telemetry` package for OpenTelemetry configuration and the standard `log` package for general events.

#### Capture prompt content[¶](<https://adk.dev/observability/logging/#capture-prompt-content_3> "Permanent link")

You can enable full prompt logging programmatically when initializing telemetry:
    
    [](<https://adk.dev/observability/logging/#__codelineno-10-1>)package main
    [](<https://adk.dev/observability/logging/#__codelineno-10-2>)
    [](<https://adk.dev/observability/logging/#__codelineno-10-3>)import (
    [](<https://adk.dev/observability/logging/#__codelineno-10-4>)    "context"
    [](<https://adk.dev/observability/logging/#__codelineno-10-5>)    "google.golang.org/adk/v2/telemetry"
    [](<https://adk.dev/observability/logging/#__codelineno-10-6>))
    [](<https://adk.dev/observability/logging/#__codelineno-10-7>)
    [](<https://adk.dev/observability/logging/#__codelineno-10-8>)func main() {
    [](<https://adk.dev/observability/logging/#__codelineno-10-9>)    ctx := context.Background()
    [](<https://adk.dev/observability/logging/#__codelineno-10-10>)    tp, err := telemetry.New(ctx,
    [](<https://adk.dev/observability/logging/#__codelineno-10-11>)        telemetry.WithGenAICaptureMessageContent(true),
    [](<https://adk.dev/observability/logging/#__codelineno-10-12>)    )
    [](<https://adk.dev/observability/logging/#__codelineno-10-13>)    if err != nil {
    [](<https://adk.dev/observability/logging/#__codelineno-10-14>)        // handle error
    [](<https://adk.dev/observability/logging/#__codelineno-10-15>)    }
    [](<https://adk.dev/observability/logging/#__codelineno-10-16>)    defer tp.Shutdown(ctx)
    [](<https://adk.dev/observability/logging/#__codelineno-10-17>)    tp.SetGlobalOtelProviders()
    [](<https://adk.dev/observability/logging/#__codelineno-10-18>)}
    
#### OTLP export[¶](<https://adk.dev/observability/logging/#otlp-export_2> "Permanent link")

To export logs to an OTLP-compatible backend, configure the standard OpenTelemetry environment variables (e.g., `OTEL_EXPORTER_OTLP_ENDPOINT` or `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`). The ADK telemetry package will automatically use these settings when initialized.

#### GCP export setup[¶](<https://adk.dev/observability/logging/#gcp-export-setup_2> "Permanent link")

To export logs to Google Cloud Logging, use the `WithOtelToCloud` option:
    
    [](<https://adk.dev/observability/logging/#__codelineno-11-1>)package main
    [](<https://adk.dev/observability/logging/#__codelineno-11-2>)
    [](<https://adk.dev/observability/logging/#__codelineno-11-3>)import (
    [](<https://adk.dev/observability/logging/#__codelineno-11-4>)    "context"
    [](<https://adk.dev/observability/logging/#__codelineno-11-5>)    "google.golang.org/adk/v2/telemetry"
    [](<https://adk.dev/observability/logging/#__codelineno-11-6>))
    [](<https://adk.dev/observability/logging/#__codelineno-11-7>)
    [](<https://adk.dev/observability/logging/#__codelineno-11-8>)func main() {
    [](<https://adk.dev/observability/logging/#__codelineno-11-9>)    ctx := context.Background()
    [](<https://adk.dev/observability/logging/#__codelineno-11-10>)    tp, err := telemetry.New(ctx,
    [](<https://adk.dev/observability/logging/#__codelineno-11-11>)        telemetry.WithOtelToCloud(true),
    [](<https://adk.dev/observability/logging/#__codelineno-11-12>)    )
    [](<https://adk.dev/observability/logging/#__codelineno-11-13>)    if err != nil {
    [](<https://adk.dev/observability/logging/#__codelineno-11-14>)        // handle error
    [](<https://adk.dev/observability/logging/#__codelineno-11-15>)    }
    [](<https://adk.dev/observability/logging/#__codelineno-11-16>)    defer tp.Shutdown(ctx)
    [](<https://adk.dev/observability/logging/#__codelineno-11-17>)    tp.SetGlobalOtelProviders()
    [](<https://adk.dev/observability/logging/#__codelineno-11-18>)}
    
If using the Go launcher, you can also enable GCP export via the CLI flag:
    
    [](<https://adk.dev/observability/logging/#__codelineno-12-1>)go run main.go web -otel_to_cloud
    
General events (like server startup or HTTP requests) are logged using the standard Go `log` package. These logs are written to `stderr` by default.

## Understanding log output[¶](<https://adk.dev/observability/logging/#understanding-log-output> "Permanent link")

### Sample Python log entry[¶](<https://adk.dev/observability/logging/#sample-python-log-entry> "Permanent link")
    
    [](<https://adk.dev/observability/logging/#__codelineno-13-1>)2025-07-08 11:22:33,456 - DEBUG - google_adk.models.google_llm - LLM Request: contents { ... }
    
Log Segment | Format Specifier | Meaning  
---|---|---  
`2025-07-08 11:22:33,456` | `%(asctime)s` | Timestamp  
`DEBUG` | `%(levelname)s` | Severity level  
`google_adk.models.google_llm` | `%(name)s` | Logger name (the module that produced the log)  
`LLM Request: contents { ... }` | `%(message)s` | The actual log message  
  
By reading the logger name, you can immediately pinpoint the source of the log and understand its context within the agent's architecture.

### Debugging example[¶](<https://adk.dev/observability/logging/#debugging-example> "Permanent link")

After enabling `DEBUG` logging (see [Logging level](<https://adk.dev/observability/logging/#logging-level>) above), run your agent and look for messages from the `google.adk.models.google_llm` logger. The output shows the full LLM request and response:
    
    [](<https://adk.dev/observability/logging/#__codelineno-14-1>)2025-07-10 15:26:13,778 - DEBUG - google_adk.google.adk.models.google_llm -
    [](<https://adk.dev/observability/logging/#__codelineno-14-2>)LLM Request:
    [](<https://adk.dev/observability/logging/#__codelineno-14-3>)-----------------------------------------------------------
    [](<https://adk.dev/observability/logging/#__codelineno-14-4>)System Instruction:
    [](<https://adk.dev/observability/logging/#__codelineno-14-5>)      You roll dice and answer questions about the outcome of the dice rolls.
    [](<https://adk.dev/observability/logging/#__codelineno-14-6>)      ...
    [](<https://adk.dev/observability/logging/#__codelineno-14-7>)-----------------------------------------------------------
    [](<https://adk.dev/observability/logging/#__codelineno-14-8>)Contents:
    [](<https://adk.dev/observability/logging/#__codelineno-14-9>){"parts":[{"text":"Roll a 6 sided dice"}],"role":"user"}
    [](<https://adk.dev/observability/logging/#__codelineno-14-10>){"parts":[{"function_call":{"args":{"sides":6},"name":"roll_die"}}],"role":"model"}
    [](<https://adk.dev/observability/logging/#__codelineno-14-11>){"parts":[{"function_response":{"name":"roll_die","response":{"result":2}}}],"role":"user"}
    [](<https://adk.dev/observability/logging/#__codelineno-14-12>)-----------------------------------------------------------
    [](<https://adk.dev/observability/logging/#__codelineno-14-13>)Functions:
    [](<https://adk.dev/observability/logging/#__codelineno-14-14>)roll_die: {'sides': {'type': <Type.INTEGER: 'INTEGER'>}}
    [](<https://adk.dev/observability/logging/#__codelineno-14-15>)check_prime: {'nums': {'items': {'type': <Type.INTEGER: 'INTEGER'>}, 'type': <Type.ARRAY: 'ARRAY'>}}
    [](<https://adk.dev/observability/logging/#__codelineno-14-16>)-----------------------------------------------------------
    [](<https://adk.dev/observability/logging/#__codelineno-14-17>)2025-07-10 15:26:14,309 - INFO - google_adk.google.adk.models.google_llm -
    [](<https://adk.dev/observability/logging/#__codelineno-14-18>)LLM Response:
    [](<https://adk.dev/observability/logging/#__codelineno-14-19>)-----------------------------------------------------------
    [](<https://adk.dev/observability/logging/#__codelineno-14-20>)Text:
    [](<https://adk.dev/observability/logging/#__codelineno-14-21>)I have rolled a 6 sided die, and the result is 2.
    [](<https://adk.dev/observability/logging/#__codelineno-14-22>)...
    
From this output you can verify:

  * Is the system instruction correct?
  * Is the conversation history (`user` and `model` turns) accurate?
  * Are the correct tools being provided to the model?
  * Are the tools correctly called by the model?
  * How long it takes for the model to respond?

Back to top 