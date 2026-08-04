# Observability for agents - Agent Development Kit (ADK)

> Source: [https://adk.dev/observability/](https://adk.dev/observability/)

[ Skip to content ](<https://adk.dev/observability/#observability-for-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/observability/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/observability/index.md> "View this page as Markdown")

# Observability for agents[¶](<https://adk.dev/observability/#observability-for-agents> "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0Kotlin v0.1.0

Observability for agents enables measurement of a system's internal state, including reasoning traces, tool calls, and latent model outputs, by analyzing its external telemetry and structured logs. When building agents, you may need these features to help debug and diagnose their in-process behavior. Basic input and output monitoring is typically insufficient for agents with any significant level of complexity.

Agent Development Kit (ADK) provides built-in observability through [logging](<https://adk.dev/observability/logging/>), [metrics](<https://adk.dev/observability/metrics/>), and [traces](<https://adk.dev/observability/traces/>) to help you monitor and debug your agents. However, you may need to consider more advanced [observability ADK Integrations](<https://adk.dev/integrations/?topic=observability>) for monitoring and analysis.

## Quick Start: Enabling Observability in Kotlin[¶](<https://adk.dev/observability/#quick-start-enabling-observability-in-kotlin> "Permanent link")

In Kotlin, you can enable comprehensive observability by configuring OpenTelemetry for traces and using the `LoggingPlugin` for detailed console output.
    
    [](<https://adk.dev/observability/#__codelineno-0-1>)// 1. Configure OpenTelemetry (Traces)
    [](<https://adk.dev/observability/#__codelineno-0-2>)// ADK Kotlin uses GlobalOpenTelemetry to resolve its tracer on the JVM.
    [](<https://adk.dev/observability/#__codelineno-0-3>)val spanExporter = OtlpGrpcSpanExporter.builder().setEndpoint("http://localhost:4317").build()
    [](<https://adk.dev/observability/#__codelineno-0-4>)
    [](<https://adk.dev/observability/#__codelineno-0-5>)val resource =
    [](<https://adk.dev/observability/#__codelineno-0-6>)    Resource.getDefault()
    [](<https://adk.dev/observability/#__codelineno-0-7>)        .merge(
    [](<https://adk.dev/observability/#__codelineno-0-8>)            Resource.create(
    [](<https://adk.dev/observability/#__codelineno-0-9>)                Attributes.of(AttributeKey.stringKey("service.name"), "my-kotlin-agent"),
    [](<https://adk.dev/observability/#__codelineno-0-10>)            ),
    [](<https://adk.dev/observability/#__codelineno-0-11>)        )
    [](<https://adk.dev/observability/#__codelineno-0-12>)
    [](<https://adk.dev/observability/#__codelineno-0-13>)val tracerProvider =
    [](<https://adk.dev/observability/#__codelineno-0-14>)    SdkTracerProvider.builder()
    [](<https://adk.dev/observability/#__codelineno-0-15>)        .addSpanProcessor(BatchSpanProcessor.builder(spanExporter).build())
    [](<https://adk.dev/observability/#__codelineno-0-16>)        .setResource(resource)
    [](<https://adk.dev/observability/#__codelineno-0-17>)        .build()
    [](<https://adk.dev/observability/#__codelineno-0-18>)
    [](<https://adk.dev/observability/#__codelineno-0-19>)OpenTelemetrySdk.builder().setTracerProvider(tracerProvider).buildAndRegisterGlobal()
    [](<https://adk.dev/observability/#__codelineno-0-20>)
    [](<https://adk.dev/observability/#__codelineno-0-21>)// 2. Optional: Configure ADK Telemetry behavior
    [](<https://adk.dev/observability/#__codelineno-0-22>)// Enable capturing full message content in traces (use with caution in production)
    [](<https://adk.dev/observability/#__codelineno-0-23>)TelemetryConfig.captureMessageContent = true
    [](<https://adk.dev/observability/#__codelineno-0-24>)
    [](<https://adk.dev/observability/#__codelineno-0-25>)// 3. Initialize Agent and Runner with LoggingPlugin for console output
    [](<https://adk.dev/observability/#__codelineno-0-26>)val agent = LlmAgent(name = "my_agent", model = Gemini(name = "gemini-flash-latest"))
    [](<https://adk.dev/observability/#__codelineno-0-27>)
    [](<https://adk.dev/observability/#__codelineno-0-28>)val runner =
    [](<https://adk.dev/observability/#__codelineno-0-29>)    InMemoryRunner(
    [](<https://adk.dev/observability/#__codelineno-0-30>)        App(appName = "my_agent", rootAgent = agent, plugins = listOf(LoggingPlugin())),
    [](<https://adk.dev/observability/#__codelineno-0-31>)    )
    [](<https://adk.dev/observability/#__codelineno-0-32>)
    [](<https://adk.dev/observability/#__codelineno-0-33>)// The runner will now automatically emit traces via GlobalOpenTelemetry
    [](<https://adk.dev/observability/#__codelineno-0-34>)// and log activity to the console via the LoggingPlugin.
    [](<https://adk.dev/observability/#__codelineno-0-35>)runner.run(
    [](<https://adk.dev/observability/#__codelineno-0-36>)    userId = "user123",
    [](<https://adk.dev/observability/#__codelineno-0-37>)    sessionId = "session456",
    [](<https://adk.dev/observability/#__codelineno-0-38>)    newMessage = Content.fromText(Role.USER, "Hello!"),
    [](<https://adk.dev/observability/#__codelineno-0-39>))
    
ADK Integrations for observability

For a list of pre-built observability libraries for ADK, see [Tools and Integrations](<https://adk.dev/integrations/?topic=observability>).

Back to top 