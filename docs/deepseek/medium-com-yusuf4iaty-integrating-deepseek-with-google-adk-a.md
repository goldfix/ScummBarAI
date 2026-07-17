### Integrating DeepSeek with Google ADK: A Complete Guide to Building Custom LLM Adapters

Press enter or click to view image in full size

## Introduction

Google’s Agent Development Kit (ADK) provides a powerful framework for building AI agents with tools, memory, and structured workflows. While it natively supports Gemini models, the extensible architecture allows integration with third-party LLMs like DeepSeek.

In this article, I’ll walk you through how I integrated DeepSeek into a Spring Boot application using Google ADK, creating a custom LLM adapter and connection class that bridges the DeepSeek Java SDK with ADK’s reactive architecture.

## Understanding the Architecture

### Google ADK’s LLM Abstraction

At the core of ADK’s LLM support is the \`BaseLlm\` abstract class:

```
public abstract class BaseLlm {
    private final String model;

    public BaseLlm(String model) {
        this.model = model;
    }

    public String model() {
        return model;
    }

    // Generate content with optional streaming
    public abstract Flowable<LlmResponse> generateContent(LlmRequest llmRequest, boolean stream);

    // Create a live connection for bidirectional communication
    public abstract BaseLlmConnection connect(LlmRequest llmRequest);
}
```

The key methods we need to implement are:

\- \*\*\`generateContent()\`\*\*: Handles text generation with optional streaming support

- \*\*\`connect()\`\*\*: Creates a persistent connection for multi-turn conversations

### The Connection Interface

For live connections, ADK uses \`BaseLlmConnection\`:

```
public interface BaseLlmConnection {
    Completable sendContent(Content content);
    Completable sendHistory(List<Content> history);
    Completable sendRealtime(Blob blob);
    Flowable<LlmResponse> receive();
    void close();
    void close(Throwable error);
}
```

## Setting Up the DeepSeek Java SDK

First, add the DeepSeek Java SDK dependency to your \`pom.xml\`:

```
<dependency>
    <groupId>io.github.pig-mesh</groupId>
    <artifactId>deepseek4j-core</artifactId>
    <version>1.4.7</version>
</dependency>
```

Configure your API key in \`application.properties\`:

````
```properties
com.ai.agent.aiModel=deepseek-chat
com.ai.agent.apiKey=${DEEPSEEK_API_KEY:your-api-key-here}
```
````

## Building the DeepSeekLlmAdapter

The adapter bridges DeepSeek’s API with ADK’s expected interfaces. Here’s the complete implementation:

### Core Structure

```
public class DeepSeekLlmAdapter extends BaseLlm {

    private static final Logger logger = LoggerFactory.getLogger(DeepSeekLlmAdapter.class);
    private final DeepSeekClient deepSeekClient;

    public DeepSeekLlmAdapter(String modelName, String apiKey) {
        super(modelName);
        Objects.requireNonNull(apiKey, "apiKey cannot be null");
        this.deepSeekClient = DeepSeekClient.builder()
                .openAiApiKey(apiKey)
                .build();
    }

    // Builder pattern for flexible construction
    public static Builder builder() {
        return new Builder();
    }
}
```

### The Builder Pattern

Following the same pattern as Gemini, we use a builder for flexible instantiation:

```
public static class Builder {
    private String modelName;
    private String apiKey;
    private DeepSeekClient deepSeekClient;

    public Builder modelName(String modelName) {
        this.modelName = modelName;
        return this;
    }

    public Builder apiKey(String apiKey) {
        this.apiKey = apiKey;
        return this;
    }

    public Builder deepSeekClient(DeepSeekClient deepSeekClient) {
        this.deepSeekClient = deepSeekClient;
        return this;
    }

    public DeepSeekLlmAdapter build() {
        Objects.requireNonNull(modelName, "modelName must be set.");

        if (deepSeekClient != null) {
            return new DeepSeekLlmAdapter(deepSeekClient, modelName);
        } else if (apiKey != null) {
            return new DeepSeekLlmAdapter(modelName, apiKey);
        } else {
            throw new IllegalStateException("Either apiKey or deepSeekClient must be set.");
        }
    }
}
```

### Implementing generateContent()

The heart of the adapter is the content generation method, supporting both sync and streaming modes:

```
@Override
public Flowable<LlmResponse> generateContent(LlmRequest request, boolean stream) {
    String effectiveModelName = request.model().orElse(model());

    if (stream) {
        return generateContentStreaming(request, effectiveModelName);
    } else {
        return Flowable.defer(() -> {
            try {
                LlmResponse response = generateContentSync(request, effectiveModelName);
                return Flowable.just(response);
            } catch (Exception e) {
                return Flowable.error(e);
            }
        });
    }
}
```

### Handling Streaming Responses

Streaming is where things get interesting. DeepSeek uses Reactor’s \`Flux\`, but ADK expects RxJava3’s \`Flowable\`. Here’s how to bridge them:

```
private Flowable<LlmResponse> generateContentStreaming(LlmRequest request, String effectiveModelName) {
    List<Message> messages = convertToDeepSeekMessages(request);

    ChatCompletionRequest chatRequest = ChatCompletionRequest.builder()
            .model(effectiveModelName)
            .messages(messages)
            .stream(true)
            .build();

    // Bridge Reactor Flux to RxJava3 Flowable
    return Flowable.create(emitter -> {
        deepSeekClient.chatFluxCompletion(chatRequest)
                .filter(response -> response.choices() != null && !response.choices().isEmpty())
                .subscribe(
                        response -> {
                            try {
                                LlmResponse llmResponse = convertStreamingResponseToLlmResponse(response);
                                emitter.onNext(llmResponse);
                            } catch (Exception e) {
                                emitter.onError(e);
                            }
                        },
                        emitter::onError,
                        emitter::onComplete
                );
    }, BackpressureStrategy.BUFFER);
}
```

### Converting Streaming Responses

DeepSeek’s streaming responses use \`delta\` objects instead of complete \`message\` objects:

```
private LlmResponse convertStreamingResponseToLlmResponse(ChatCompletionResponse response) {
    String contentText = response.choices().stream()
            .findFirst()
            .map(choice -> {
                // Streaming responses use delta
                if (choice.delta() != null && choice.delta().content() != null) {
                    return choice.delta().content();
                }
                // Fall back to message for non-streaming
                if (choice.message() != null && choice.message().content() != null) {
                    return choice.message().content();
                }
                return "";
            })
            .orElse("");

    Content content = Content.builder()
            .role("model")
            .parts(List.of(Part.fromText(contentText)))
            .build();

    return LlmResponse.builder()
            .content(content)
            .partial(true)  // Mark as partial for streaming
            .build();
}
```

### Message Format Conversion

ADK uses Google’s \`Content\` format, while DeepSeek expects its own message types:

```
private List<Message> convertToDeepSeekMessages(LlmRequest request) {
    List<Message> messages = new ArrayList<>();

    // Add system instruction if present
    Optional<GenerateContentConfig> configOpt = request.config();
    if (configOpt.isPresent()) {
        GenerateContentConfig config = configOpt.get();
        config.systemInstruction().ifPresent(sysContent -> {
            String systemText = extractTextFromContent(sysContent);
            if (!systemText.isBlank()) {
                messages.add(SystemMessage.from(systemText));
            }
        });
    }

    // Add conversation contents
    List<Content> contents = request.contents();
    if (contents != null) {
        for (Content content : contents) {
            String text = extractTextFromContent(content);
            String role = content.role().orElse("user");

            if ("user".equalsIgnoreCase(role)) {
                messages.add(UserMessage.from(text));
            } else if ("model".equalsIgnoreCase(role) || "assistant".equalsIgnoreCase(role)) {
                messages.add(AssistantMessage.from(text));
            }
        }
    }

    return messages;
}
```

## Building the DeepSeekLlmConnection

For persistent connections and multi-turn conversations, we implement \`BaseLlmConnection\`:

```
public class DeepSeekLlmConnection implements BaseLlmConnection {

    private final DeepSeekClient deepSeekClient;
    private final String modelName;
    private final List<Message> messages;
    private final StringBuilder accumulatedResponse = new StringBuilder();

    public DeepSeekLlmConnection(DeepSeekClient deepSeekClient, String modelName,
                                  List<Message> initialMessages) {
        this.deepSeekClient = deepSeekClient;
        this.modelName = modelName;
        this.messages = Collections.synchronizedList(new ArrayList<>(initialMessages));
    }
}
```

### Sending Content

```
@Override
public Completable sendContent(Content content) {
    return Completable.fromAction(() -> {
        String text = extractTextFromContent(content);
        messages.add(UserMessage.from(text));
    });
}

@Override
public Completable sendHistory(List<Content> history) {
    return Completable.fromAction(() -> {
        for (Content content : history) {
            String text = extractTextFromContent(content);
            String role = content.role().orElse("user");
            if ("user".equalsIgnoreCase(role)) {
                messages.add(UserMessage.from(text));
            } else if ("model".equalsIgnoreCase(role) || "assistant".equalsIgnoreCase(role)) {
                messages.add(AssistantMessage.from(text));
            }
        }
    });
}
```

### Receiving Streaming Responses

```
@Override
public Flowable<LlmResponse> receive() {
    ChatCompletionRequest chatRequest = ChatCompletionRequest.builder()
            .model(modelName)
            .messages(new ArrayList<>(messages))
            .stream(true)
            .build();

    return Flowable.create(emitter -> {
        deepSeekClient.chatFluxCompletion(chatRequest)
                .filter(response -> response.choices() != null && !response.choices().isEmpty())
                .subscribe(
                        response -> {
                            LlmResponse llmResponse = convertStreamingResponseToLlmResponse(response);
                            emitter.onNext(llmResponse);
                        },
                        emitter::onError,
                        () -> {
                            // Add accumulated response to history on completion
                            if (!accumulatedResponse.isEmpty()) {
                                messages.add(AssistantMessage.from(accumulatedResponse.toString()));
                                accumulatedResponse.setLength(0);
                            }
                            emitter.onComplete();
                        }
                );
    }, BackpressureStrategy.BUFFER);
}
```

### Handling Realtime Streams

DeepSeek doesn’t support realtime audio/video, so we provide a no-op implementation:

````
@Override
public Completable sendRealtime(Blob blob) {
    // DeepSeek doesn't support realtime audio/video streaming
    return Completable.complete();
}
```
````

## Wiring It All Together with Spring Boot

Create a configuration class to set up the agent:

```
@Configuration
@EnableConfigurationProperties(AgentProperties.class)
class AgentConfiguration {

    @Bean
    BaseAgent baseAgent(AgentProperties agentProperties) throws IOException {

        DeepSeekLlmAdapter deepSeekLlm = DeepSeekLlmAdapter.builder()
                .modelName(agentProperties.aiModel())
                .apiKey(agentProperties.apiKey())
                .build();

        return LlmAgent
                .builder()
                .name(agentProperties.name())
                .description(agentProperties.description())
                .model(deepSeekLlm)
                .instruction(agentProperties.systemPrompt()
                    .getContentAsString(Charset.defaultCharset()))
                .tools(
                        FunctionTool.create(AuthorFetcher.class, "fetch")
                )
                .build();
    }
}
```

## Key Differences from Gemini

```
| Feature | Gemini | DeepSeek |
|---------|--------|----------|
| **SDK Client** | `com.google.genai.Client` | `DeepSeekClient` |
| **Streaming Type** | CompletableFuture + ResponseStream | Reactor Flux |
| **Message Format** | `Content` with `Part` | `Message` subclasses |
| **Realtime Support** | Yes (audio/video) | No |
| **Response Structure** | `GenerateContentResponse` | `ChatCompletionResponse` |
```

## Handling the Reactor-to-RxJava Bridge

One challenge is that DeepSeek4J uses Project Reactor (\`Flux\`), while ADK uses RxJava3 (\`Flowable\`). The solution is using \`Flowable.create()\` with \`BackpressureStrategy.BUFFER\`:

```
return Flowable.create(emitter -> {
    deepSeekClient.chatFluxCompletion(chatRequest)
            .subscribe(
                    response -> emitter.onNext(convertResponse(response)),
                    emitter::onError,
                    emitter::onComplete
            );
}, BackpressureStrategy.BUFFER);
```

This bridges the two reactive worlds seamlessly.

## Best Practices

1\. \*\*Always mark streaming responses as partial\*\*: Set \`.partial(true)\` on \`LlmResponse\` for streaming chunks.

2\. \*\*Accumulate history in connections\*\*: Keep track of the conversation for multi-turn dialogues.

3\. \*\*Handle missing deltas gracefully\*\*: Streaming responses may have empty chunks; filter them out.

4\. \*\*Use thread-safe collections\*\*: When maintaining message history in connections, use \`Collections.synchronizedList()\`.

5\. \*\*Provide no-op implementations for unsupported features\*\*: DeepSeek doesn’t support realtime, but the interface requires the method.

## Conclusion

Integrating DeepSeek with Google ADK demonstrates the framework’s flexibility. By implementing \`BaseLlm\` and \`BaseLlmConnection\`, you can plug in virtually any LLM provider while maintaining ADK’s powerful agent capabilities — tools, memory, and structured workflows.

The key challenges are:

\- \*\*Message format conversion\*\* between ADK’s \`Content\` and DeepSeek’s \`Message\` types

\- \*\*Reactive bridge\*\* between Reactor and RxJava3

\- \*\*Streaming delta handling\*\* for real-time responses

With this pattern, you can extend ADK to support OpenAI, Anthropic, Mistral, or any other LLM with a Java SDK.

## Resources

\- \[Google ADK Documentation\](https://github.com/google/adk-java)

\- \[DeepSeek4J SDK\](https://github.com/pig-mesh/deepseek4j)

\- \[RxJava3 Documentation\](https://github.com/ReactiveX/RxJava)

— -

\*Found this helpful? Follow me for more articles on AI agents and Java development!\*

[AI](https://medium.com/tag/ai?source=---footer_tags--ef04ffce4b53---------------------------------------)

[Deepseek](https://medium.com/tag/deepseek?source=---footer_tags--ef04ffce4b53---------------------------------------)

[Google Adk](https://medium.com/tag/google-adk?source=---footer_tags--ef04ffce4b53---------------------------------------)

[Adk](https://medium.com/tag/adk?source=---footer_tags--ef04ffce4b53---------------------------------------)

[Spring Boot](https://medium.com/tag/spring-boot?source=---footer_tags--ef04ffce4b53---------------------------------------)

[![Youssef Elshiaty](https://miro.medium.com/v2/resize:fill:96:96/1*DLNhyL4tOxkAQKZ1ODPtLA.jpeg)](https://medium.com/@yusuf4iaty?source=---post_author_info--ef04ffce4b53---------------------------------------)

[![Youssef Elshiaty](https://miro.medium.com/v2/resize:fill:128:128/1*DLNhyL4tOxkAQKZ1ODPtLA.jpeg)](https://medium.com/@yusuf4iaty?source=---post_author_info--ef04ffce4b53---------------------------------------)

[**Written by Youssef Elshiaty**](https://medium.com/@yusuf4iaty?source=---post_author_info--ef04ffce4b53---------------------------------------)

[1 follower](https://medium.com/@yusuf4iaty/followers?source=---post_author_info--ef04ffce4b53---------------------------------------)

· [4 following](https://medium.com/@yusuf4iaty/following?source=---post_author_info--ef04ffce4b53---------------------------------------)

IC Software engineer \| Flutter, Android, Java, Springboot, SQL, NoSql, Software design.

[Help](https://help.medium.com/hc/en-us?source=-----ef04ffce4b53---------------------------------------)

[Status](https://status.medium.com/?source=-----ef04ffce4b53---------------------------------------)

[About](https://medium.com/about?autoplay=1&source=-----ef04ffce4b53---------------------------------------)

[Careers](https://medium.com/jobs-at-medium/work-at-medium-959d1a85284e?source=-----ef04ffce4b53---------------------------------------)

[Press](mailto:pressinquiries@medium.com)

[Blog](https://blog.medium.com/?source=-----ef04ffce4b53---------------------------------------)

[Store](https://medium.com/store)

[Privacy](https://policy.medium.com/medium-privacy-policy-f03bf92035c9?source=-----ef04ffce4b53---------------------------------------)

[Rules](https://policy.medium.com/medium-rules-30e5502c4eb4?source=-----ef04ffce4b53---------------------------------------)

[Terms](https://policy.medium.com/medium-terms-of-service-9db0094a1e0f?source=-----ef04ffce4b53---------------------------------------)

[Text to speech](https://speechify.com/medium?source=-----ef04ffce4b53---------------------------------------)
