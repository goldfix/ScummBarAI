# Runtime Config - Agent Development Kit (ADK)

> Source: [https://adk.dev/runtime/runconfig/](https://adk.dev/runtime/runconfig/)

[ Skip to content ](<https://adk.dev/runtime/runconfig/#runtime-configuration>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/runtime/runconfig.md> "Edit this page on GitHub") [ ](<https://adk.dev/runtime/runconfig/index.md> "View this page as Markdown")

# Runtime Configuration[¶](<https://adk.dev/runtime/runconfig/#runtime-configuration> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

`RunConfig` controls how agents behave at runtime, including streaming mode, speech settings, LLM call limits, and live agent options. Pass a `RunConfig` to `runner.run_async()` or `runner.run_live()` to override default behavior.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-1>)from google.adk.agents.run_config import RunConfig, StreamingMode
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-3>)config = RunConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-4>)    streaming_mode=StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-5>)    max_llm_calls=200,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-6>))
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-7>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-8>)async for event in runner.run_async(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-9>)    ...,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-10>)    run_config=config,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-11>)):
    [](<https://adk.dev/runtime/runconfig/#__codelineno-0-12>)    ...
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-1-1>)import { RunConfig, StreamingMode } from '@google/adk';
    [](<https://adk.dev/runtime/runconfig/#__codelineno-1-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-1-3>)const config: RunConfig = {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-1-4>)  streamingMode: StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-1-5>)  maxLlmCalls: 200,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-1-6>)};
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-2-1>)import "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/runtime/runconfig/#__codelineno-2-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-2-3>)config := agent.RunConfig{
    [](<https://adk.dev/runtime/runconfig/#__codelineno-2-4>)    StreamingMode: agent.StreamingModeSSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-2-5>)}
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-3-1>)import com.google.adk.agents.RunConfig;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-3-2>)import com.google.adk.agents.RunConfig.StreamingMode;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-3-3>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-3-4>)RunConfig config = RunConfig.builder()
    [](<https://adk.dev/runtime/runconfig/#__codelineno-3-5>)    .streamingMode(StreamingMode.SSE)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-3-6>)    .maxLlmCalls(200)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-3-7>)    .build();
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-4-1>)val config =
    [](<https://adk.dev/runtime/runconfig/#__codelineno-4-2>)    RunConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-4-3>)        streamingMode = StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-4-4>)    )
    [](<https://adk.dev/runtime/runconfig/#__codelineno-4-5>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-4-6>)// Pass it to runner.runAsync
    [](<https://adk.dev/runtime/runconfig/#__codelineno-4-7>)// runner.runAsync(..., runConfig = config)
    
## Manage sessions and context[¶](<https://adk.dev/runtime/runconfig/#manage-sessions-and-context> "Permanent link")

Supported in ADKPython

For long-running sessions, you can control how much history is loaded and whether the context window is compressed:

  * `get_session_config`: Limits which events are fetched when loading a session. Use `num_recent_events` or `after_timestamp` to avoid loading the full event history on every invocation.
  * `context_window_compression`: Enables context window compression for LLM input, useful when sessions approach model context limits.
  * `include_thoughts_from_other_agents`: Controls whether thought parts from other agents are included in the LLM context. Disabled by default.

Python
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-5-1>)from google.adk.agents.run_config import RunConfig
    [](<https://adk.dev/runtime/runconfig/#__codelineno-5-2>)from google.adk.sessions.base_session_service import GetSessionConfig
    [](<https://adk.dev/runtime/runconfig/#__codelineno-5-3>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-5-4>)config = RunConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-5-5>)    get_session_config=GetSessionConfig(num_recent_events=50),
    [](<https://adk.dev/runtime/runconfig/#__codelineno-5-6>))
    
## Enable streaming[¶](<https://adk.dev/runtime/runconfig/#enable-streaming> "Permanent link")

To control how the agent delivers responses, set the `streaming_mode` parameter:

  * **`StreamingMode.NONE`** (default): The runner returns one complete response per turn. Suitable for CLI tools, batch processing, and synchronous workflows.
  * **`StreamingMode.SSE`** : Server-Sent Events streaming. The runner yields partial events as the LLM generates, enabling typewriter-style UIs and real-time chat displays.
  * **`StreamingMode.BIDI`** : Reserved for bidirectional streaming, but **not used** in the standard `run_async()` path. For bidirectional streaming, use `runner.run_live()` instead.

Set `support_cfc=True` alongside `StreamingMode.SSE` to enable Compositional Function Calling (CFC), which allows the model to dynamically compose and execute function calls. CFC uses the Live API under the hood.

Experimental

CFC support is experimental and its API or behavior may change in future releases.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-6-1>)from google.adk.agents.run_config import RunConfig, StreamingMode
    [](<https://adk.dev/runtime/runconfig/#__codelineno-6-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-6-3>)config = RunConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-6-4>)    streaming_mode=StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-6-5>)    support_cfc=True,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-6-6>)    max_llm_calls=150,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-6-7>))
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-7-1>)import { RunConfig, StreamingMode } from '@google/adk';
    [](<https://adk.dev/runtime/runconfig/#__codelineno-7-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-7-3>)const config: RunConfig = {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-7-4>)    streamingMode: StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-7-5>)    supportCfc: true,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-7-6>)    maxLlmCalls: 150,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-7-7>)};
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-8-1>)import "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/runtime/runconfig/#__codelineno-8-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-8-3>)config := agent.RunConfig{
    [](<https://adk.dev/runtime/runconfig/#__codelineno-8-4>)    StreamingMode: agent.StreamingModeSSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-8-5>)}
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-9-1>)import com.google.adk.agents.RunConfig;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-9-2>)import com.google.adk.agents.RunConfig.StreamingMode;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-9-3>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-9-4>)RunConfig config = RunConfig.builder()
    [](<https://adk.dev/runtime/runconfig/#__codelineno-9-5>)    .streamingMode(StreamingMode.SSE)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-9-6>)    .maxLlmCalls(150)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-9-7>)    .build();
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-10-1>)val streamingConfig =
    [](<https://adk.dev/runtime/runconfig/#__codelineno-10-2>)    RunConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-10-3>)        streamingMode = StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-10-4>)    )
    
## Configure audio and speech[¶](<https://adk.dev/runtime/runconfig/#configure-audio-and-speech> "Permanent link")

Supported in ADKPythonTypeScriptJava

For voice-enabled agents, configure speech synthesis, audio transcription, and response modalities.

  * `speech_config`: Sets the voice and language for speech output (e.g., the "Kore" voice with `en-US`).
  * `response_modalities`: Controls output formats. Set to `["AUDIO", "TEXT"]` for agents that both speak and return text.
  * `output_audio_transcription` / `input_audio_transcription`: Enable transcription of audio output from the model and audio input from the user. Both default to `AudioTranscriptionConfig()` in Python.

PythonTypeScriptJava
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-1>)from google.adk.agents.run_config import RunConfig, StreamingMode
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-2>)from google.genai import types
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-3>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-4>)config = RunConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-5>)    speech_config=types.SpeechConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-6>)        language_code="en-US",
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-7>)        voice_config=types.VoiceConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-8>)            prebuilt_voice_config=types.PrebuiltVoiceConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-9>)                voice_name="Kore"
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-10>)            )
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-11>)        ),
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-12>)    ),
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-13>)    response_modalities=["AUDIO", "TEXT"],
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-14>)    streaming_mode=StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-15>)    max_llm_calls=1000,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-11-16>))
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-1>)import { RunConfig, StreamingMode } from '@google/adk';
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-2>)import { Modality } from '@google/genai';
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-3>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-4>)const config: RunConfig = {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-5>)    speechConfig: {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-6>)        languageCode: "en-US",
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-7>)        voiceConfig: {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-8>)            prebuiltVoiceConfig: {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-9>)                voiceName: "Kore"
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-10>)            }
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-11>)        },
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-12>)    },
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-13>)    responseModalities: [Modality.AUDIO, Modality.TEXT],
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-14>)    streamingMode: StreamingMode.SSE,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-15>)    maxLlmCalls: 1000,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-12-16>)};
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-1>)import com.google.adk.agents.RunConfig;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-2>)import com.google.adk.agents.RunConfig.StreamingMode;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-3>)import com.google.common.collect.ImmutableList;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-4>)import com.google.genai.types.Modality;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-5>)import com.google.genai.types.PrebuiltVoiceConfig;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-6>)import com.google.genai.types.SpeechConfig;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-7>)import com.google.genai.types.VoiceConfig;
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-8>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-9>)RunConfig runConfig =
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-10>)    RunConfig.builder()
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-11>)        .streamingMode(StreamingMode.SSE)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-12>)        .maxLlmCalls(1000)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-13>)        .responseModalities(ImmutableList.of(new Modality(Modality.Known.AUDIO), new Modality(Modality.Known.TEXT)))
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-14>)        .speechConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-15>)            SpeechConfig.builder()
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-16>)                .voiceConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-17>)                    VoiceConfig.builder()
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-18>)                        .prebuiltVoiceConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-19>)                            PrebuiltVoiceConfig.builder().voiceName("Kore").build())
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-20>)                        .build())
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-21>)                .languageCode("en-US")
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-22>)                .build())
    [](<https://adk.dev/runtime/runconfig/#__codelineno-13-23>)        .build();
    
## Configure live agents[¶](<https://adk.dev/runtime/runconfig/#configure-live-agents> "Permanent link")

Supported in ADKPythonTypeScript

When using `runner.run_live()`, configure real-time behavior with these additional parameters:

  * `realtime_input_config`: Configures how audio input is received from users.
  * `proactivity`: Allows the model to respond proactively and ignore irrelevant input.
  * `enable_affective_dialog`: When `True`, the model detects user emotions and adapts its tone accordingly.
  * `avatar_config`: Configures an avatar for live agents.
  * `session_resumption`: Enables transparent session resumption across disconnects.
  * `save_live_blob`: When `True`, saves live audio and video data to the session and artifact service.
  * `tool_thread_pool_config`: Runs tool executions in a background thread pool to keep the event loop responsive to user interruptions.
  * `explicit_vad_signal`: Enables explicit voice activity detection (VAD) signals from the model.

Not all parameters are available in every language. See the [API reference](<https://adk.dev/runtime/runconfig/#api-reference>) for language-specific details.

PythonTypeScript
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-14-1>)from google.adk.agents.run_config import RunConfig, ToolThreadPoolConfig
    [](<https://adk.dev/runtime/runconfig/#__codelineno-14-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-14-3>)config = RunConfig(
    [](<https://adk.dev/runtime/runconfig/#__codelineno-14-4>)    save_live_blob=True,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-14-5>)    tool_thread_pool_config=ToolThreadPoolConfig(max_workers=8),
    [](<https://adk.dev/runtime/runconfig/#__codelineno-14-6>))
    
Thread pool and the GIL

Thread pools help with blocking I/O and C extensions that release the GIL (e.g. `time.sleep()`, network calls, numpy). They do **not** help with pure Python CPU-bound code since the GIL prevents true parallel execution of Python bytecode.
    
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-1>)import { RunConfig } from '@google/adk';
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-2>)
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-3>)const config: RunConfig = {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-4>)    enableAffectiveDialog: true,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-5>)    proactivity: {
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-6>)        proactiveAudio: true,
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-7>)    },
    [](<https://adk.dev/runtime/runconfig/#__codelineno-15-8>)};
    
## Configure runtime limits and debugging[¶](<https://adk.dev/runtime/runconfig/#configure-runtime-limits-and-debugging> "Permanent link")

Use these parameters to control runtime guardrails and debugging:

  * `max_llm_calls`: Caps the total number of LLM calls per run (default: 500). Set to 0 or negative for unlimited calls, though this is not recommended for production. Values at or above `sys.maxsize` raise an error.
  * `save_input_blobs_as_artifacts`: When `True`, saves input blobs (e.g., uploaded files) as run artifacts for debugging and auditing.
  * `custom_metadata`: A `dict[str, Any]` of arbitrary metadata attached to the invocation, useful for tracing or logging.

## API reference[¶](<https://adk.dev/runtime/runconfig/#api-reference> "Permanent link")

For the complete list of fields, types, and defaults, see the API reference for your language:

  * [Python API reference](<https://adk.dev/api-reference/python/google-adk.html#google.adk.agents.RunConfig>)
  * [TypeScript API reference](<https://adk.dev/api-reference/typescript/interfaces/RunConfig.html>)
  * [Go API reference](<https://pkg.go.dev/google.golang.org/adk/v2/agent#RunConfig>)
  * [Java API reference](<https://adk.dev/api-reference/java/com/google/adk/agents/RunConfig.html>)
  * [Kotlin API reference](<https://adk.dev/api-reference/kotlin/google-adk-kotlin-core/com.google.adk.kt.agents/-run-config/>)

Back to top 