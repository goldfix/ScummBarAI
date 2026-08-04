# Traces - Agent Development Kit (ADK)

> Source: [https://adk.dev/observability/traces/](https://adk.dev/observability/traces/)

[ Skip to content ](<https://adk.dev/observability/traces/#agent-activity-traces>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/observability/traces.md> "Edit this page on GitHub") [ ](<https://adk.dev/observability/traces/index.md> "View this page as Markdown")

# Agent activity traces[¶](<https://adk.dev/observability/traces/#agent-activity-traces> "Permanent link")

Supported in ADKPython v1.17.0Go v1.0.0Kotlin v0.1.0

Agent Development Kit (ADK) provides distributed tracing capabilities to help you visualize the end-to-end journey of a request as it travels through your agent's architecture. While metrics tell you _how long_ a process took and logs tell you _what_ happened, traces connect these events, showing you exactly _where_ the time was spent and the hierarchical relationship between LLM reasoning, tool calls, and external APIs.

## Traces philosophy[¶](<https://adk.dev/observability/traces/#traces-philosophy> "Permanent link")

ADK's approach to tracing is built on standard protocols to ensure seamless integration with your existing observability stack.

  * **OpenTelemetry Semantic Conventions:** ADK implements the OpenTelemetry (OTel) [Semantic Conventions for GenAI](<https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-agent-spans.md>). This ensures that trace spans and attributes are recorded under standard, predictable names.
  * **OTLP Wire Format:** ADK emits data using the standard OTLP format, ensuring that your traces will seamlessly integrate into any OTel-compatible backend (e.g., Google Cloud Trace, Jaeger, Grafana Tempo, Datadog).
  * **Hierarchical Visualization:** Traces are organized into "Spans." An agent run is a root span, which contains child spans for LLM operations, which may in turn contain child spans for tool executions. This creates a clear "waterfall" view of the agent's reasoning loop.
  * **Context Propagation:** ADK automatically passes trace context across process boundaries, ensuring that if your agent calls an external microservice via a tool, that service's spans are linked to the agent's root trace.

* * *

## Traces schema[¶](<https://adk.dev/observability/traces/#traces-schema> "Permanent link")

When tracing is enabled, ADK automatically instruments key operations following the OpenTelemetry GenAI Semantic Conventions for Agents. A typical trace waterfall includes the following spans:

Span Name | Type | Description | Key Attributes  
---|---|---|---  
**[`invoke_agent`](<https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-agent-spans.md#invoke-agent-client-span>)** | Client / Internal Span | Describes GenAI agent invocation over a remote service or locally. Represents the lifecycle of an agent interaction. | `gen_ai.agent.name`, `gen_ai.system`  
**[`invoke_workflow`](<https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-agent-spans.md#invoke-workflow-span>)** | Child Span | Describes the invocation of a multi-step agentic workflow. | `gen_ai.workflow.name`, `gen_ai.system`  
**[`execute_tool`](<https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-agent-spans.md#execute-tool-span>)** | Child Span | Represents the execution of a specific tool or function call requested by the GenAI system. | `gen_ai.tool.name`, `gen_ai.system`  
**[`generate_content {model.name}`](<https://github.com/open-telemetry/semantic-conventions/blob/main/docs/gen-ai/gen-ai-spans.md>)** | Internal Span | Represents the invocation of the underlying language model (via the GenAI SDK) to generate content. It tracks the request parameters, response details, and usage metrics. | `gen_ai.operation.name`, `gen_ai.system`, `gen_ai.request.model`, `gen_ai.agent.name`, `gen_ai.conversation.id`, `user.id`, `gen_ai.request.top_p`, `gen_ai.request.max_tokens`, `gen_ai.response.finish_reasons`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`  
  
* * *

## Traces export setup[¶](<https://adk.dev/observability/traces/#traces-export-setup> "Permanent link")

### Traces export in ADK Web[¶](<https://adk.dev/observability/traces/#traces-export-in-adk-web> "Permanent link")

If you are running your agent using the `adk web` or `adk api_server` CLI commands, you can configure trace exports.

#### OTLP export[¶](<https://adk.dev/observability/traces/#otlp-export> "Permanent link")

To export traces to an OTLP-compatible backend, set the standard OTel environment variables:
    
    [](<https://adk.dev/observability/traces/#__codelineno-0-1>)export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT="http://your-collector:4318/v1/traces"
    [](<https://adk.dev/observability/traces/#__codelineno-0-2>)adk web path/to/your/agents_dir
    
> **Note:** You can also set the general `OTEL_EXPORTER_OTLP_ENDPOINT` environment variable if you would like to send metrics and logs to the same endpoint in addition to traces.

#### GCP export[¶](<https://adk.dev/observability/traces/#gcp-export> "Permanent link")

To enable trace export to Google Cloud Trace, use the `--otel_to_cloud` flag:
    
    [](<https://adk.dev/observability/traces/#__codelineno-1-1>)adk web --otel_to_cloud path/to/your/agents_dir
    
### Programmatic traces export[¶](<https://adk.dev/observability/traces/#programmatic-traces-export> "Permanent link")

You can also configure trace export programmatically in your application code.

#### OTLP export setup[¶](<https://adk.dev/observability/traces/#otlp-export-setup> "Permanent link")

To enable tracing and export spans to an OpenTelemetry Collector programmatically:
    
    [](<https://adk.dev/observability/traces/#__codelineno-2-1>)from google.adk.telemetry.setup import maybe_set_otel_providers
    [](<https://adk.dev/observability/traces/#__codelineno-2-2>)import os
    [](<https://adk.dev/observability/traces/#__codelineno-2-3>)
    [](<https://adk.dev/observability/traces/#__codelineno-2-4>)os.environ["OTEL_EXPORTER_OTLP_TRACES_ENDPOINT"] = "http://your-collector:4318/v1/traces"
    [](<https://adk.dev/observability/traces/#__codelineno-2-5>)os.environ["OTEL_SERVICE_NAME"] = "your-adk-agent"
    [](<https://adk.dev/observability/traces/#__codelineno-2-6>)os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "key1=value1,key2=value2"
    [](<https://adk.dev/observability/traces/#__codelineno-2-7>)maybe_set_otel_providers()
    
#### GCP export setup[¶](<https://adk.dev/observability/traces/#gcp-export-setup> "Permanent link")

To export traces to Google Cloud Trace programmatically, use the OpenTelemetry Google Cloud exporter. Here is an example in Python:
    
    [](<https://adk.dev/observability/traces/#__codelineno-3-1>)from google.adk.telemetry.google_cloud import get_gcp_exporters
    [](<https://adk.dev/observability/traces/#__codelineno-3-2>)from google.adk.telemetry.setup import maybe_set_otel_providers
    [](<https://adk.dev/observability/traces/#__codelineno-3-3>)import os
    [](<https://adk.dev/observability/traces/#__codelineno-3-4>)
    [](<https://adk.dev/observability/traces/#__codelineno-3-5>)gcp_exporters = get_gcp_exporters(
    [](<https://adk.dev/observability/traces/#__codelineno-3-6>)  enable_cloud_tracing = True,
    [](<https://adk.dev/observability/traces/#__codelineno-3-7>))
    [](<https://adk.dev/observability/traces/#__codelineno-3-8>)os.environ["OTEL_SERVICE_NAME"] = "your-adk-agent"
    [](<https://adk.dev/observability/traces/#__codelineno-3-9>)os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "key1=value1,key2=value2"
    [](<https://adk.dev/observability/traces/#__codelineno-3-10>)maybe_set_otel_providers([gcp_exporters])
    
### Kotlin programmatic setup[¶](<https://adk.dev/observability/traces/#kotlin-programmatic-setup> "Permanent link")

In Kotlin, ADK automatically uses the `GlobalOpenTelemetry` instance to export traces. You should configure your OpenTelemetry SDK before starting the agent.

#### OTLP export setup[¶](<https://adk.dev/observability/traces/#otlp-export-setup_1> "Permanent link")

To enable tracing and export spans to an OpenTelemetry Collector, configure the OpenTelemetry SDK and register it globally:
    
    [](<https://adk.dev/observability/traces/#__codelineno-4-1>)// 1. Configure OpenTelemetry (Traces)
    [](<https://adk.dev/observability/traces/#__codelineno-4-2>)// ADK Kotlin uses GlobalOpenTelemetry to resolve its tracer on the JVM.
    [](<https://adk.dev/observability/traces/#__codelineno-4-3>)val spanExporter = OtlpGrpcSpanExporter.builder().setEndpoint("http://localhost:4317").build()
    [](<https://adk.dev/observability/traces/#__codelineno-4-4>)
    [](<https://adk.dev/observability/traces/#__codelineno-4-5>)val resource =
    [](<https://adk.dev/observability/traces/#__codelineno-4-6>)    Resource.getDefault()
    [](<https://adk.dev/observability/traces/#__codelineno-4-7>)        .merge(
    [](<https://adk.dev/observability/traces/#__codelineno-4-8>)            Resource.create(
    [](<https://adk.dev/observability/traces/#__codelineno-4-9>)                Attributes.of(AttributeKey.stringKey("service.name"), "my-kotlin-agent"),
    [](<https://adk.dev/observability/traces/#__codelineno-4-10>)            ),
    [](<https://adk.dev/observability/traces/#__codelineno-4-11>)        )
    [](<https://adk.dev/observability/traces/#__codelineno-4-12>)
    [](<https://adk.dev/observability/traces/#__codelineno-4-13>)val tracerProvider =
    [](<https://adk.dev/observability/traces/#__codelineno-4-14>)    SdkTracerProvider.builder()
    [](<https://adk.dev/observability/traces/#__codelineno-4-15>)        .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
    [](<https://adk.dev/observability/traces/#__codelineno-4-16>)        .setResource(resource)
    [](<https://adk.dev/observability/traces/#__codelineno-4-17>)        .build()
    [](<https://adk.dev/observability/traces/#__codelineno-4-18>)
    [](<https://adk.dev/observability/traces/#__codelineno-4-19>)OpenTelemetrySdk.builder().setTracerProvider(tracerProvider).buildAndRegisterGlobal()
    [](<https://adk.dev/observability/traces/#__codelineno-4-20>)
    [](<https://adk.dev/observability/traces/#__codelineno-4-21>)// 2. Optional: Configure ADK Telemetry behavior
    [](<https://adk.dev/observability/traces/#__codelineno-4-22>)// Enable capturing full message content in traces (use with caution in production)
    [](<https://adk.dev/observability/traces/#__codelineno-4-23>)TelemetryConfig.captureMessageContent = true
    [](<https://adk.dev/observability/traces/#__codelineno-4-24>)
    [](<https://adk.dev/observability/traces/#__codelineno-4-25>)// 3. Initialize Agent and Runner with LoggingPlugin for console output
    [](<https://adk.dev/observability/traces/#__codelineno-4-26>)val agent = LlmAgent(name = "my_agent", model = Gemini(name = "gemini-flash-latest"))
    [](<https://adk.dev/observability/traces/#__codelineno-4-27>)
    [](<https://adk.dev/observability/traces/#__codelineno-4-28>)val runner =
    [](<https://adk.dev/observability/traces/#__codelineno-4-29>)    InMemoryRunner(
    [](<https://adk.dev/observability/traces/#__codelineno-4-30>)        App(appName = "my_agent", rootAgent = agent, plugins = listOf(LoggingPlugin())),
    [](<https://adk.dev/observability/traces/#__codelineno-4-31>)    )
    [](<https://adk.dev/observability/traces/#__codelineno-4-32>)
    [](<https://adk.dev/observability/traces/#__codelineno-4-33>)// The runner will now automatically emit traces via GlobalOpenTelemetry
    [](<https://adk.dev/observability/traces/#__codelineno-4-34>)// and log activity to the console via the LoggingPlugin.
    [](<https://adk.dev/observability/traces/#__codelineno-4-35>)runner.run(
    [](<https://adk.dev/observability/traces/#__codelineno-4-36>)    userId = "user123",
    [](<https://adk.dev/observability/traces/#__codelineno-4-37>)    sessionId = "session456",
    [](<https://adk.dev/observability/traces/#__codelineno-4-38>)    newMessage = Content.fromText(Role.USER, "Hello!"),
    [](<https://adk.dev/observability/traces/#__codelineno-4-39>))
    
Back to top 