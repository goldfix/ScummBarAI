# Artifacts - Agent Development Kit (ADK)

> Source: [https://adk.dev/artifacts/](https://adk.dev/artifacts/)

[ Skip to content ](<https://adk.dev/artifacts/#artifacts>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/artifacts/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/artifacts/index.md> "View this page as Markdown")

# Artifacts[¶](<https://adk.dev/artifacts/#artifacts> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.6.1Go v0.1.0Java v0.1.0Kotlin v0.1.0

In ADK, **Artifacts** represent a crucial mechanism for managing named, versioned binary data associated either with a specific user interaction session or persistently with a user across multiple sessions. They allow your agents and tools to handle data beyond simple text strings, enabling richer interactions involving files, images, audio, and other binary formats.

Note

The specific parameters or method names for the primitives may vary slightly by SDK language (e.g., `save_artifact` in Python, `saveArtifact` in Java). Refer to the language-specific API documentation for details.

## What are Artifacts?[¶](<https://adk.dev/artifacts/#what-are-artifacts> "Permanent link")

  * **Definition:** An Artifact is essentially a piece of binary data (like the content of a file) identified by a unique `filename` string within a specific scope (session or user). Each time you save an artifact with the same filename, a new version is created.

  * **Representation:** Artifacts are consistently represented using the standard `google.genai.types.Part` object. The core data is typically stored within an inline data structure of the `Part` (accessed via `inline_data`), which itself contains:

    * `data`: The raw binary content as bytes.
    * `mime_type`: A string indicating the type of the data (e.g., `"image/png"`, `"application/pdf"`). This is essential for correctly interpreting the data later.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/artifacts/#__codelineno-0-1>)# Example of how an artifact might be represented as a types.Part
    [](<https://adk.dev/artifacts/#__codelineno-0-2>)import google.genai.types as types
    [](<https://adk.dev/artifacts/#__codelineno-0-3>)
    [](<https://adk.dev/artifacts/#__codelineno-0-4>)# Assume 'image_bytes' contains the binary data of a PNG image
    [](<https://adk.dev/artifacts/#__codelineno-0-5>)image_bytes = b'\x89PNG\r\n\x1a\n...' # Placeholder for actual image bytes
    [](<https://adk.dev/artifacts/#__codelineno-0-6>)
    [](<https://adk.dev/artifacts/#__codelineno-0-7>)image_artifact = types.Part(
    [](<https://adk.dev/artifacts/#__codelineno-0-8>)    inline_data=types.Blob(
    [](<https://adk.dev/artifacts/#__codelineno-0-9>)        mime_type="image/png",
    [](<https://adk.dev/artifacts/#__codelineno-0-10>)        data=image_bytes
    [](<https://adk.dev/artifacts/#__codelineno-0-11>)    )
    [](<https://adk.dev/artifacts/#__codelineno-0-12>))
    [](<https://adk.dev/artifacts/#__codelineno-0-13>)
    [](<https://adk.dev/artifacts/#__codelineno-0-14>)# You can also use the convenience constructor:
    [](<https://adk.dev/artifacts/#__codelineno-0-15>)# image_artifact_alt = types.Part.from_bytes(data=image_bytes, mime_type="image/png")
    [](<https://adk.dev/artifacts/#__codelineno-0-16>)
    [](<https://adk.dev/artifacts/#__codelineno-0-17>)print(f"Artifact MIME Type: {image_artifact.inline_data.mime_type}")
    [](<https://adk.dev/artifacts/#__codelineno-0-18>)print(f"Artifact Data (first 10 bytes): {image_artifact.inline_data.data[:10]}...")
    
    [](<https://adk.dev/artifacts/#__codelineno-1-1>)import {createPartFromBase64, type Part} from '@google/genai';
    [](<https://adk.dev/artifacts/#__codelineno-1-2>)
    [](<https://adk.dev/artifacts/#__codelineno-1-3>)// Assume 'imageBytes' contains the binary data of a PNG image.
    [](<https://adk.dev/artifacts/#__codelineno-1-4>)const imageBytes = new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
    [](<https://adk.dev/artifacts/#__codelineno-1-5>)
    [](<https://adk.dev/artifacts/#__codelineno-1-6>)// Using Buffer.from(bytes).toString('base64') for Node.js environments.
    [](<https://adk.dev/artifacts/#__codelineno-1-7>)const imageArtifact: Part = createPartFromBase64(
    [](<https://adk.dev/artifacts/#__codelineno-1-8>)  Buffer.from(imageBytes).toString('base64'),
    [](<https://adk.dev/artifacts/#__codelineno-1-9>)  'image/png',
    [](<https://adk.dev/artifacts/#__codelineno-1-10>));
    [](<https://adk.dev/artifacts/#__codelineno-1-11>)
    [](<https://adk.dev/artifacts/#__codelineno-1-12>)console.log(`Artifact MIME Type: ${imageArtifact.inlineData?.mimeType}`);
    [](<https://adk.dev/artifacts/#__codelineno-1-13>)// Note: Accessing raw bytes would require decoding from base64.
    
    [](<https://adk.dev/artifacts/#__codelineno-2-1>)import (
    [](<https://adk.dev/artifacts/#__codelineno-2-2>)  "log"
    [](<https://adk.dev/artifacts/#__codelineno-2-3>)
    [](<https://adk.dev/artifacts/#__codelineno-2-4>)  "google.golang.org/genai"
    [](<https://adk.dev/artifacts/#__codelineno-2-5>))
    [](<https://adk.dev/artifacts/#__codelineno-2-6>)
    [](<https://adk.dev/artifacts/#__codelineno-2-7>)// Create a byte slice with the image data.
    [](<https://adk.dev/artifacts/#__codelineno-2-8>)imageBytes, err := os.ReadFile("image.png")
    [](<https://adk.dev/artifacts/#__codelineno-2-9>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-2-10>)    log.Fatalf("Failed to read image file: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-2-11>)}
    [](<https://adk.dev/artifacts/#__codelineno-2-12>)
    [](<https://adk.dev/artifacts/#__codelineno-2-13>)// Create a new artifact with the image data.
    [](<https://adk.dev/artifacts/#__codelineno-2-14>)imageArtifact := &genai.Part{
    [](<https://adk.dev/artifacts/#__codelineno-2-15>)    InlineData: &genai.Blob{
    [](<https://adk.dev/artifacts/#__codelineno-2-16>)        MIMEType: "image/png",
    [](<https://adk.dev/artifacts/#__codelineno-2-17>)        Data:     imageBytes,
    [](<https://adk.dev/artifacts/#__codelineno-2-18>)    },
    [](<https://adk.dev/artifacts/#__codelineno-2-19>)}
    [](<https://adk.dev/artifacts/#__codelineno-2-20>)log.Printf("Artifact MIME Type: %s", imageArtifact.InlineData.MIMEType)
    [](<https://adk.dev/artifacts/#__codelineno-2-21>)log.Printf("Artifact Data (first 8 bytes): %x...", imageArtifact.InlineData.Data[:8])
    
    [](<https://adk.dev/artifacts/#__codelineno-3-1>)import com.google.genai.types.Part;
    [](<https://adk.dev/artifacts/#__codelineno-3-2>)import java.nio.charset.StandardCharsets;
    [](<https://adk.dev/artifacts/#__codelineno-3-3>)
    [](<https://adk.dev/artifacts/#__codelineno-3-4>)public class ArtifactExample {
    [](<https://adk.dev/artifacts/#__codelineno-3-5>)    public static void main(String[] args) {
    [](<https://adk.dev/artifacts/#__codelineno-3-6>)        // Assume 'imageBytes' contains the binary data of a PNG image
    [](<https://adk.dev/artifacts/#__codelineno-3-7>)        byte[] imageBytes = {(byte) 0x89, (byte) 0x50, (byte) 0x4E, (byte) 0x47, (byte) 0x0D, (byte) 0x0A, (byte) 0x1A, (byte) 0x0A, (byte) 0x01, (byte) 0x02}; // Placeholder for actual image bytes
    [](<https://adk.dev/artifacts/#__codelineno-3-8>)
    [](<https://adk.dev/artifacts/#__codelineno-3-9>)        // Create an image artifact using Part.fromBytes
    [](<https://adk.dev/artifacts/#__codelineno-3-10>)        Part imageArtifact = Part.fromBytes(imageBytes, "image/png");
    [](<https://adk.dev/artifacts/#__codelineno-3-11>)
    [](<https://adk.dev/artifacts/#__codelineno-3-12>)        System.out.println("Artifact MIME Type: " + imageArtifact.inlineData().get().mimeType().get());
    [](<https://adk.dev/artifacts/#__codelineno-3-13>)        System.out.println(
    [](<https://adk.dev/artifacts/#__codelineno-3-14>)            "Artifact Data (first 10 bytes): "
    [](<https://adk.dev/artifacts/#__codelineno-3-15>)                + new String(imageArtifact.inlineData().get().data().get(), 0, 10, StandardCharsets.UTF_8)
    [](<https://adk.dev/artifacts/#__codelineno-3-16>)                + "...");
    [](<https://adk.dev/artifacts/#__codelineno-3-17>)    }
    [](<https://adk.dev/artifacts/#__codelineno-3-18>)}
    
    [](<https://adk.dev/artifacts/#__codelineno-4-1>)fun artifactRepresentationExample() {
    [](<https://adk.dev/artifacts/#__codelineno-4-2>)    // Assume 'imageBytes' contains the binary data of a PNG image
    [](<https://adk.dev/artifacts/#__codelineno-4-3>)    val imageBytes = byteArrayOf(0x89.toByte(), 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A)
    [](<https://adk.dev/artifacts/#__codelineno-4-4>)
    [](<https://adk.dev/artifacts/#__codelineno-4-5>)    val imageArtifact =
    [](<https://adk.dev/artifacts/#__codelineno-4-6>)        Part(
    [](<https://adk.dev/artifacts/#__codelineno-4-7>)            inlineData =
    [](<https://adk.dev/artifacts/#__codelineno-4-8>)                Blob(
    [](<https://adk.dev/artifacts/#__codelineno-4-9>)                    mimeType = "image/png",
    [](<https://adk.dev/artifacts/#__codelineno-4-10>)                    data = imageBytes,
    [](<https://adk.dev/artifacts/#__codelineno-4-11>)                ),
    [](<https://adk.dev/artifacts/#__codelineno-4-12>)        )
    [](<https://adk.dev/artifacts/#__codelineno-4-13>)
    [](<https://adk.dev/artifacts/#__codelineno-4-14>)    println("Artifact MIME Type: ${imageArtifact.inlineData?.mimeType}")
    [](<https://adk.dev/artifacts/#__codelineno-4-15>)    println("Artifact Data (first 8 bytes): ${imageArtifact.inlineData?.data?.take(8)}")
    [](<https://adk.dev/artifacts/#__codelineno-4-16>)}
    
  * **Persistence & Management:** Artifacts are not stored directly within the agent or session state. Their storage and retrieval are managed by a dedicated **Artifact Service** (an implementation of `BaseArtifactService`, defined in `google.adk.artifacts`. ADK provides various implementations, such as:
    * An in-memory service for testing or temporary storage (e.g., `InMemoryArtifactService` in Python, defined in `google.adk.artifacts.in_memory_artifact_service.py`).
    * A service for persistent storage using Google Cloud Storage (GCS) (e.g., `GcsArtifactService` in Python, defined in `google.adk.artifacts.gcs_artifact_service.py`). The chosen service implementation handles versioning automatically when you save data.

## Why Use Artifacts?[¶](<https://adk.dev/artifacts/#why-use-artifacts> "Permanent link")

While session `state` is suitable for storing small pieces of configuration or conversational context (like strings, numbers, booleans, or small dictionaries/lists), Artifacts are designed for scenarios involving binary or large data:

  1. **Handling Non-Textual Data:** Easily store and retrieve images, audio clips, video snippets, PDFs, spreadsheets, or any other file format relevant to your agent's function.
  2. **Persisting Large Data:** Session state is generally not optimized for storing large amounts of data. Artifacts provide a dedicated mechanism for persisting larger blobs without cluttering the session state.
  3. **User File Management:** Provide capabilities for users to upload files (which can be saved as artifacts) and retrieve or download files generated by the agent (loaded from artifacts).
  4. **Sharing Outputs:** Enable tools or agents to generate binary outputs (like a PDF report or a generated image) that can be saved via `save_artifact` and later accessed by other parts of the application or even in subsequent sessions (if using user namespacing).
  5. **Caching Binary Data:** Store the results of computationally expensive operations that produce binary data (e.g., rendering a complex chart image) as artifacts to avoid regenerating them on subsequent requests.

In essence, whenever your agent needs to work with file-like binary data that needs to be persisted, versioned, or shared, Artifacts managed by an `ArtifactService` are the appropriate mechanism within ADK.

## Common Use Cases[¶](<https://adk.dev/artifacts/#common-use-cases> "Permanent link")

Artifacts provide a flexible way to handle binary data within your ADK applications.

Here are some typical scenarios where they prove valuable:

  * **Generated Reports/Files:**

    * A tool or agent generates a report (e.g., a PDF analysis, a CSV data export, an image chart).
  * **Handling User Uploads:**

    * A user uploads a file (e.g., an image for analysis, a document for summarization) through a front-end interface.
  * **Storing Intermediate Binary Results:**

    * An agent performs a complex multi-step process where one step generates intermediate binary data (e.g., audio synthesis, simulation results).
  * **Persistent User Data:**

    * Storing user-specific configuration or data that isn't a simple key-value state.
  * **Caching Generated Binary Content:**

    * An agent frequently generates the same binary output based on certain inputs (e.g., a company logo image, a standard audio greeting).

## Core Concepts[¶](<https://adk.dev/artifacts/#core-concepts> "Permanent link")

Understanding artifacts involves grasping a few key components: the service that manages them, the data structure used to hold them, and how they are identified and versioned.

### Artifact Service (`BaseArtifactService`)[¶](<https://adk.dev/artifacts/#artifact-service-baseartifactservice> "Permanent link")

  * **Role:** The central component responsible for the actual storage and retrieval logic for artifacts. It defines _how_ and _where_ artifacts are persisted.

  * **Interface:** Defined by the abstract base class `BaseArtifactService`. Any concrete implementation must provide methods for:

    * `Save Artifact`: Stores the artifact data and returns its assigned version number.
    * `Load Artifact`: Retrieves a specific version (or the latest) of an artifact.
    * `List Artifact keys`: Lists the unique filenames of artifacts within a given scope.
    * `Delete Artifact`: Removes an artifact (and potentially all its versions, depending on implementation).
    * `List versions`: Lists all available version numbers for a specific artifact filename.
  * **Configuration:** You provide an instance of an artifact service (e.g., `InMemoryArtifactService`, `GcsArtifactService`) when initializing the `Runner`. The `Runner` then makes this service available to agents and tools via the `InvocationContext`.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/artifacts/#__codelineno-5-1>)from google.adk.runners import Runner
    [](<https://adk.dev/artifacts/#__codelineno-5-2>)from google.adk.artifacts import InMemoryArtifactService # Or GcsArtifactService
    [](<https://adk.dev/artifacts/#__codelineno-5-3>)from google.adk.agents import LlmAgent # Any agent
    [](<https://adk.dev/artifacts/#__codelineno-5-4>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/artifacts/#__codelineno-5-5>)
    [](<https://adk.dev/artifacts/#__codelineno-5-6>)# Example: Configuring the Runner with an Artifact Service
    [](<https://adk.dev/artifacts/#__codelineno-5-7>)my_agent = LlmAgent(name="artifact_user_agent", model="gemini-flash-latest")
    [](<https://adk.dev/artifacts/#__codelineno-5-8>)artifact_service = InMemoryArtifactService() # Choose an implementation
    [](<https://adk.dev/artifacts/#__codelineno-5-9>)session_service = InMemorySessionService()
    [](<https://adk.dev/artifacts/#__codelineno-5-10>)
    [](<https://adk.dev/artifacts/#__codelineno-5-11>)runner = Runner(
    [](<https://adk.dev/artifacts/#__codelineno-5-12>)    agent=my_agent,
    [](<https://adk.dev/artifacts/#__codelineno-5-13>)    app_name="my_artifact_app",
    [](<https://adk.dev/artifacts/#__codelineno-5-14>)    session_service=session_service,
    [](<https://adk.dev/artifacts/#__codelineno-5-15>)    artifact_service=artifact_service # Provide the service instance here
    [](<https://adk.dev/artifacts/#__codelineno-5-16>))
    [](<https://adk.dev/artifacts/#__codelineno-5-17>)# Now, contexts within runs managed by this runner can use artifact methods
    
    [](<https://adk.dev/artifacts/#__codelineno-6-1>)import {
    [](<https://adk.dev/artifacts/#__codelineno-6-2>)  InMemoryArtifactService,
    [](<https://adk.dev/artifacts/#__codelineno-6-3>)  InMemorySessionService,
    [](<https://adk.dev/artifacts/#__codelineno-6-4>)  LlmAgent,
    [](<https://adk.dev/artifacts/#__codelineno-6-5>)  Runner,
    [](<https://adk.dev/artifacts/#__codelineno-6-6>)} from '@google/adk';
    [](<https://adk.dev/artifacts/#__codelineno-6-7>)
    [](<https://adk.dev/artifacts/#__codelineno-6-8>)// Example: Configuring the Runner with an Artifact Service
    [](<https://adk.dev/artifacts/#__codelineno-6-9>)const myAgent = new LlmAgent({
    [](<https://adk.dev/artifacts/#__codelineno-6-10>)  name: 'artifact_user_agent',
    [](<https://adk.dev/artifacts/#__codelineno-6-11>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/artifacts/#__codelineno-6-12>)});
    [](<https://adk.dev/artifacts/#__codelineno-6-13>)const artifactService = new InMemoryArtifactService();
    [](<https://adk.dev/artifacts/#__codelineno-6-14>)const sessionService = new InMemorySessionService();
    [](<https://adk.dev/artifacts/#__codelineno-6-15>)
    [](<https://adk.dev/artifacts/#__codelineno-6-16>)const runner = new Runner({
    [](<https://adk.dev/artifacts/#__codelineno-6-17>)  agent: myAgent,
    [](<https://adk.dev/artifacts/#__codelineno-6-18>)  appName: 'my_artifact_app',
    [](<https://adk.dev/artifacts/#__codelineno-6-19>)  sessionService: sessionService,
    [](<https://adk.dev/artifacts/#__codelineno-6-20>)  artifactService: artifactService,
    [](<https://adk.dev/artifacts/#__codelineno-6-21>)});
    [](<https://adk.dev/artifacts/#__codelineno-6-22>)// Now, contexts within runs managed by this runner can use artifact methods.
    
    [](<https://adk.dev/artifacts/#__codelineno-7-1>)import (
    [](<https://adk.dev/artifacts/#__codelineno-7-2>)  "context"
    [](<https://adk.dev/artifacts/#__codelineno-7-3>)  "log"
    [](<https://adk.dev/artifacts/#__codelineno-7-4>)
    [](<https://adk.dev/artifacts/#__codelineno-7-5>)  "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/artifacts/#__codelineno-7-6>)  "google.golang.org/adk/v2/artifact"
    [](<https://adk.dev/artifacts/#__codelineno-7-7>)  "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/artifacts/#__codelineno-7-8>)  "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/artifacts/#__codelineno-7-9>)  "google.golang.org/adk/v2/session"
    [](<https://adk.dev/artifacts/#__codelineno-7-10>)  "google.golang.org/genai"
    [](<https://adk.dev/artifacts/#__codelineno-7-11>))
    [](<https://adk.dev/artifacts/#__codelineno-7-12>)
    [](<https://adk.dev/artifacts/#__codelineno-7-13>)// Create a new context.
    [](<https://adk.dev/artifacts/#__codelineno-7-14>)ctx := context.Background()
    [](<https://adk.dev/artifacts/#__codelineno-7-15>)// Set the app name.
    [](<https://adk.dev/artifacts/#__codelineno-7-16>)const appName = "my_artifact_app"
    [](<https://adk.dev/artifacts/#__codelineno-7-17>)// Create a new Gemini model.
    [](<https://adk.dev/artifacts/#__codelineno-7-18>)model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    [](<https://adk.dev/artifacts/#__codelineno-7-19>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-7-20>)    log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-7-21>)}
    [](<https://adk.dev/artifacts/#__codelineno-7-22>)
    [](<https://adk.dev/artifacts/#__codelineno-7-23>)// Create a new LLM agent.
    [](<https://adk.dev/artifacts/#__codelineno-7-24>)myAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/artifacts/#__codelineno-7-25>)    Model:       model,
    [](<https://adk.dev/artifacts/#__codelineno-7-26>)    Name:        "artifact_user_agent",
    [](<https://adk.dev/artifacts/#__codelineno-7-27>)    Instruction: "You are an agent that describes images.",
    [](<https://adk.dev/artifacts/#__codelineno-7-28>)    BeforeModelCallbacks: []llmagent.BeforeModelCallback{
    [](<https://adk.dev/artifacts/#__codelineno-7-29>)        BeforeModelCallback,
    [](<https://adk.dev/artifacts/#__codelineno-7-30>)    },
    [](<https://adk.dev/artifacts/#__codelineno-7-31>)})
    [](<https://adk.dev/artifacts/#__codelineno-7-32>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-7-33>)    log.Fatalf("Failed to create agent: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-7-34>)}
    [](<https://adk.dev/artifacts/#__codelineno-7-35>)
    [](<https://adk.dev/artifacts/#__codelineno-7-36>)// Create a new in-memory artifact service.
    [](<https://adk.dev/artifacts/#__codelineno-7-37>)artifactService := artifact.InMemoryService()
    [](<https://adk.dev/artifacts/#__codelineno-7-38>)// Create a new in-memory session service.
    [](<https://adk.dev/artifacts/#__codelineno-7-39>)sessionService := session.InMemoryService()
    [](<https://adk.dev/artifacts/#__codelineno-7-40>)
    [](<https://adk.dev/artifacts/#__codelineno-7-41>)// Create a new runner.
    [](<https://adk.dev/artifacts/#__codelineno-7-42>)r, err := runner.New(runner.Config{
    [](<https://adk.dev/artifacts/#__codelineno-7-43>)    Agent:           myAgent,
    [](<https://adk.dev/artifacts/#__codelineno-7-44>)    AppName:         appName,
    [](<https://adk.dev/artifacts/#__codelineno-7-45>)    SessionService:  sessionService,
    [](<https://adk.dev/artifacts/#__codelineno-7-46>)    ArtifactService: artifactService, // Provide the service instance here
    [](<https://adk.dev/artifacts/#__codelineno-7-47>)})
    [](<https://adk.dev/artifacts/#__codelineno-7-48>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-7-49>)    log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-7-50>)}
    [](<https://adk.dev/artifacts/#__codelineno-7-51>)log.Printf("Runner created successfully: %v", r)
    
    [](<https://adk.dev/artifacts/#__codelineno-8-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/artifacts/#__codelineno-8-2>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/artifacts/#__codelineno-8-3>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/artifacts/#__codelineno-8-4>)import com.google.adk.artifacts.InMemoryArtifactService;
    [](<https://adk.dev/artifacts/#__codelineno-8-5>)
    [](<https://adk.dev/artifacts/#__codelineno-8-6>)// Example: Configuring the Runner with an Artifact Service
    [](<https://adk.dev/artifacts/#__codelineno-8-7>)LlmAgent myAgent =  LlmAgent.builder()
    [](<https://adk.dev/artifacts/#__codelineno-8-8>)  .name("artifact_user_agent")
    [](<https://adk.dev/artifacts/#__codelineno-8-9>)  .model("gemini-flash-latest")
    [](<https://adk.dev/artifacts/#__codelineno-8-10>)  .build();
    [](<https://adk.dev/artifacts/#__codelineno-8-11>)InMemoryArtifactService artifactService = new InMemoryArtifactService(); // Choose an implementation
    [](<https://adk.dev/artifacts/#__codelineno-8-12>)InMemorySessionService sessionService = new InMemorySessionService();
    [](<https://adk.dev/artifacts/#__codelineno-8-13>)
    [](<https://adk.dev/artifacts/#__codelineno-8-14>)Runner runner = new Runner(myAgent, "my_artifact_app", artifactService, sessionService); // Provide the service instance here
    [](<https://adk.dev/artifacts/#__codelineno-8-15>)// Now, contexts within runs managed by this runner can use artifact methods
    
    [](<https://adk.dev/artifacts/#__codelineno-9-1>)fun configureRunnerExample() {
    [](<https://adk.dev/artifacts/#__codelineno-9-2>)    val myAgent =
    [](<https://adk.dev/artifacts/#__codelineno-9-3>)        LlmAgent(name = "artifact_user_agent", model = Gemini(name = "gemini-flash-latest"))
    [](<https://adk.dev/artifacts/#__codelineno-9-4>)    val artifactService = InMemoryArtifactService()
    [](<https://adk.dev/artifacts/#__codelineno-9-5>)    val sessionService = InMemorySessionService()
    [](<https://adk.dev/artifacts/#__codelineno-9-6>)
    [](<https://adk.dev/artifacts/#__codelineno-9-7>)    val runner =
    [](<https://adk.dev/artifacts/#__codelineno-9-8>)        InMemoryRunner(
    [](<https://adk.dev/artifacts/#__codelineno-9-9>)            agent = myAgent,
    [](<https://adk.dev/artifacts/#__codelineno-9-10>)            appName = "my_artifact_app",
    [](<https://adk.dev/artifacts/#__codelineno-9-11>)            sessionService = sessionService,
    [](<https://adk.dev/artifacts/#__codelineno-9-12>)            artifactService = artifactService,
    [](<https://adk.dev/artifacts/#__codelineno-9-13>)        )
    [](<https://adk.dev/artifacts/#__codelineno-9-14>)}
    
### Artifact Data[¶](<https://adk.dev/artifacts/#artifact-data> "Permanent link")

  * **Standard Representation:** Artifact content is universally represented using the `google.genai.types.Part` object, the same structure used for parts of LLM messages.

  * **Key Attribute (`inline_data`):** For artifacts, the most relevant attribute is `inline_data`, which is a `google.genai.types.Blob` object containing:

    * `data` (`bytes`): The raw binary content of the artifact.
    * `mime_type` (`str`): A standard MIME type string (e.g., `'application/pdf'`, `'image/png'`, `'audio/mpeg'`) describing the nature of the binary data. **This is crucial for correct interpretation when loading the artifact.**

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/artifacts/#__codelineno-10-1>)import google.genai.types as types
    [](<https://adk.dev/artifacts/#__codelineno-10-2>)
    [](<https://adk.dev/artifacts/#__codelineno-10-3>)# Example: Creating an artifact Part from raw bytes
    [](<https://adk.dev/artifacts/#__codelineno-10-4>)pdf_bytes = b'%PDF-1.4...' # Your raw PDF data
    [](<https://adk.dev/artifacts/#__codelineno-10-5>)pdf_mime_type = "application/pdf"
    [](<https://adk.dev/artifacts/#__codelineno-10-6>)
    [](<https://adk.dev/artifacts/#__codelineno-10-7>)# Using the constructor
    [](<https://adk.dev/artifacts/#__codelineno-10-8>)pdf_artifact_py = types.Part(
    [](<https://adk.dev/artifacts/#__codelineno-10-9>)    inline_data=types.Blob(data=pdf_bytes, mime_type=pdf_mime_type)
    [](<https://adk.dev/artifacts/#__codelineno-10-10>))
    [](<https://adk.dev/artifacts/#__codelineno-10-11>)
    [](<https://adk.dev/artifacts/#__codelineno-10-12>)# Using the convenience class method (equivalent)
    [](<https://adk.dev/artifacts/#__codelineno-10-13>)pdf_artifact_alt_py = types.Part.from_bytes(data=pdf_bytes, mime_type=pdf_mime_type)
    [](<https://adk.dev/artifacts/#__codelineno-10-14>)
    [](<https://adk.dev/artifacts/#__codelineno-10-15>)print(f"Created Python artifact with MIME type: {pdf_artifact_py.inline_data.mime_type}")
    
    [](<https://adk.dev/artifacts/#__codelineno-11-1>)import {createPartFromBase64, type Part} from '@google/genai';
    [](<https://adk.dev/artifacts/#__codelineno-11-2>)
    [](<https://adk.dev/artifacts/#__codelineno-11-3>)// Example: Creating an artifact Part from raw bytes.
    [](<https://adk.dev/artifacts/#__codelineno-11-4>)const pdfBytes = new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d, 0x31, 0x2e, 0x34]);
    [](<https://adk.dev/artifacts/#__codelineno-11-5>)const pdfMimeType = 'application/pdf';
    [](<https://adk.dev/artifacts/#__codelineno-11-6>)
    [](<https://adk.dev/artifacts/#__codelineno-11-7>)// Using Buffer.from(bytes).toString('base64') for Node.js environments.
    [](<https://adk.dev/artifacts/#__codelineno-11-8>)const pdfArtifact: Part = createPartFromBase64(
    [](<https://adk.dev/artifacts/#__codelineno-11-9>)  Buffer.from(pdfBytes).toString('base64'),
    [](<https://adk.dev/artifacts/#__codelineno-11-10>)  pdfMimeType,
    [](<https://adk.dev/artifacts/#__codelineno-11-11>));
    [](<https://adk.dev/artifacts/#__codelineno-11-12>)console.log(`Created TypeScript artifact with MIME Type: ${pdfArtifact.inlineData?.mimeType}`);
    
    [](<https://adk.dev/artifacts/#__codelineno-12-1>)import (
    [](<https://adk.dev/artifacts/#__codelineno-12-2>)  "log"
    [](<https://adk.dev/artifacts/#__codelineno-12-3>)  "os"
    [](<https://adk.dev/artifacts/#__codelineno-12-4>)
    [](<https://adk.dev/artifacts/#__codelineno-12-5>)  "google.golang.org/genai"
    [](<https://adk.dev/artifacts/#__codelineno-12-6>))
    [](<https://adk.dev/artifacts/#__codelineno-12-7>)
    [](<https://adk.dev/artifacts/#__codelineno-12-8>)// Load imageBytes from a file
    [](<https://adk.dev/artifacts/#__codelineno-12-9>)imageBytes, err := os.ReadFile("image.png")
    [](<https://adk.dev/artifacts/#__codelineno-12-10>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-12-11>)    log.Fatalf("Failed to read image file: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-12-12>)}
    [](<https://adk.dev/artifacts/#__codelineno-12-13>)
    [](<https://adk.dev/artifacts/#__codelineno-12-14>)// genai.NewPartFromBytes is a convenience function that is a shorthand for
    [](<https://adk.dev/artifacts/#__codelineno-12-15>)// creating a &genai.Part with the InlineData field populated.
    [](<https://adk.dev/artifacts/#__codelineno-12-16>)// Create a new artifact from the image data.
    [](<https://adk.dev/artifacts/#__codelineno-12-17>)imageArtifact := genai.NewPartFromBytes([]byte(imageBytes), "image/png")
    [](<https://adk.dev/artifacts/#__codelineno-12-18>)
    [](<https://adk.dev/artifacts/#__codelineno-12-19>)log.Printf("Artifact MIME Type: %s", imageArtifact.InlineData.MIMEType)
    
    [](<https://adk.dev/artifacts/#__codelineno-13-1>)import com.google.genai.types.Blob;
    [](<https://adk.dev/artifacts/#__codelineno-13-2>)import com.google.genai.types.Part;
    [](<https://adk.dev/artifacts/#__codelineno-13-3>)import java.nio.charset.StandardCharsets;
    [](<https://adk.dev/artifacts/#__codelineno-13-4>)
    [](<https://adk.dev/artifacts/#__codelineno-13-5>)public class ArtifactDataExample {
    [](<https://adk.dev/artifacts/#__codelineno-13-6>)  public static void main(String[] args) {
    [](<https://adk.dev/artifacts/#__codelineno-13-7>)    // Example: Creating an artifact Part from raw bytes
    [](<https://adk.dev/artifacts/#__codelineno-13-8>)    byte[] pdfBytes = "%PDF-1.4...".getBytes(StandardCharsets.UTF_8); // Your raw PDF data
    [](<https://adk.dev/artifacts/#__codelineno-13-9>)    String pdfMimeType = "application/pdf";
    [](<https://adk.dev/artifacts/#__codelineno-13-10>)
    [](<https://adk.dev/artifacts/#__codelineno-13-11>)    // Using the Part.fromBlob() constructor with a Blob
    [](<https://adk.dev/artifacts/#__codelineno-13-12>)    Blob pdfBlob = Blob.builder()
    [](<https://adk.dev/artifacts/#__codelineno-13-13>)        .data(pdfBytes)
    [](<https://adk.dev/artifacts/#__codelineno-13-14>)        .mimeType(pdfMimeType)
    [](<https://adk.dev/artifacts/#__codelineno-13-15>)        .build();
    [](<https://adk.dev/artifacts/#__codelineno-13-16>)    Part pdfArtifactJava = Part.builder().inlineData(pdfBlob).build();
    [](<https://adk.dev/artifacts/#__codelineno-13-17>)
    [](<https://adk.dev/artifacts/#__codelineno-13-18>)    // Using the convenience static method Part.fromBytes() (equivalent)
    [](<https://adk.dev/artifacts/#__codelineno-13-19>)    Part pdfArtifactAltJava = Part.fromBytes(pdfBytes, pdfMimeType);
    [](<https://adk.dev/artifacts/#__codelineno-13-20>)
    [](<https://adk.dev/artifacts/#__codelineno-13-21>)    // Accessing mimeType, note the use of Optional
    [](<https://adk.dev/artifacts/#__codelineno-13-22>)    String mimeType = pdfArtifactJava.inlineData()
    [](<https://adk.dev/artifacts/#__codelineno-13-23>)        .flatMap(Blob::mimeType)
    [](<https://adk.dev/artifacts/#__codelineno-13-24>)        .orElse("unknown");
    [](<https://adk.dev/artifacts/#__codelineno-13-25>)    System.out.println("Created Java artifact with MIME type: " + mimeType);
    [](<https://adk.dev/artifacts/#__codelineno-13-26>)
    [](<https://adk.dev/artifacts/#__codelineno-13-27>)    // Accessing data
    [](<https://adk.dev/artifacts/#__codelineno-13-28>)    byte[] data = pdfArtifactJava.inlineData()
    [](<https://adk.dev/artifacts/#__codelineno-13-29>)        .flatMap(Blob::data)
    [](<https://adk.dev/artifacts/#__codelineno-13-30>)        .orElse(new byte[0]);
    [](<https://adk.dev/artifacts/#__codelineno-13-31>)    System.out.println("Java artifact data (first 10 bytes): "
    [](<https://adk.dev/artifacts/#__codelineno-13-32>)        + new String(data, 0, Math.min(data.length, 10), StandardCharsets.UTF_8) + "...");
    [](<https://adk.dev/artifacts/#__codelineno-13-33>)  }
    [](<https://adk.dev/artifacts/#__codelineno-13-34>)}
    
    [](<https://adk.dev/artifacts/#__codelineno-14-1>)fun artifactDataExample() {
    [](<https://adk.dev/artifacts/#__codelineno-14-2>)    val pdfBytes = "%PDF-1.4...".toByteArray()
    [](<https://adk.dev/artifacts/#__codelineno-14-3>)    val pdfMimeType = "application/pdf"
    [](<https://adk.dev/artifacts/#__codelineno-14-4>)
    [](<https://adk.dev/artifacts/#__codelineno-14-5>)    val pdfArtifact =
    [](<https://adk.dev/artifacts/#__codelineno-14-6>)        Part(
    [](<https://adk.dev/artifacts/#__codelineno-14-7>)            inlineData =
    [](<https://adk.dev/artifacts/#__codelineno-14-8>)                Blob(
    [](<https://adk.dev/artifacts/#__codelineno-14-9>)                    data = pdfBytes,
    [](<https://adk.dev/artifacts/#__codelineno-14-10>)                    mimeType = pdfMimeType,
    [](<https://adk.dev/artifacts/#__codelineno-14-11>)                ),
    [](<https://adk.dev/artifacts/#__codelineno-14-12>)        )
    [](<https://adk.dev/artifacts/#__codelineno-14-13>)
    [](<https://adk.dev/artifacts/#__codelineno-14-14>)    println("Created Kotlin artifact with MIME type: ${pdfArtifact.inlineData?.mimeType}")
    [](<https://adk.dev/artifacts/#__codelineno-14-15>)}
    
### Filename[¶](<https://adk.dev/artifacts/#filename> "Permanent link")

  * **Identifier:** A simple string used to name and retrieve an artifact within its specific namespace.
  * **Uniqueness:** Filenames must be unique within their scope (either the session or the user namespace).
  * **Best Practice:** Use descriptive names, potentially including file extensions (e.g., `"monthly_report.pdf"`, `"user_avatar.jpg"`), although the extension itself doesn't dictate behavior – the `mime_type` does.

### Versioning[¶](<https://adk.dev/artifacts/#versioning> "Permanent link")

  * **Automatic Versioning:** The artifact service automatically handles versioning. When you call `save_artifact`, the service determines the next available version number (typically starting from 0 and incrementing) for that specific filename and scope.
  * **Returned by`save_artifact`:** The `save_artifact` method returns the integer version number that was assigned to the newly saved artifact.
  * **Retrieval:**
  * `load_artifact(..., version=None)` (default): Retrieves the _latest_ available version of the artifact.
  * `load_artifact(..., version=N)`: Retrieves the specific version `N`.
  * **Listing Versions:** The `list_versions` method (on the service, not context) can be used to find all existing version numbers for an artifact.

### Namespacing (Session vs. User)[¶](<https://adk.dev/artifacts/#namespacing-session-vs-user> "Permanent link")

  * **Concept:** Artifacts can be scoped either to a specific session or more broadly to a user across all their sessions within the application. This scoping is determined by the `filename` format and handled internally by the `ArtifactService`.

  * **Default (Session Scope):** If you use a plain filename like `"report.pdf"`, the artifact is associated with the specific `app_name`, `user_id`, _and_ `session_id`. It's only accessible within that exact session context.

  * **User Scope (`"user:"` prefix):** If you prefix the filename with `"user:"`, like `"user:profile.png"`, the artifact is associated only with the `app_name` and `user_id`. It can be accessed or updated from _any_ session belonging to that user within the app.

PythonTypescriptGoJavaKotlin
    
    [](<https://adk.dev/artifacts/#__codelineno-15-1>)# Example illustrating namespace difference (conceptual)
    [](<https://adk.dev/artifacts/#__codelineno-15-2>)
    [](<https://adk.dev/artifacts/#__codelineno-15-3>)# Session-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-15-4>)session_report_filename = "summary.txt"
    [](<https://adk.dev/artifacts/#__codelineno-15-5>)
    [](<https://adk.dev/artifacts/#__codelineno-15-6>)# User-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-15-7>)user_config_filename = "user:settings.json"
    [](<https://adk.dev/artifacts/#__codelineno-15-8>)
    [](<https://adk.dev/artifacts/#__codelineno-15-9>)# When saving 'summary.txt' via context.save_artifact,
    [](<https://adk.dev/artifacts/#__codelineno-15-10>)# it's tied to the current app_name, user_id, and session_id.
    [](<https://adk.dev/artifacts/#__codelineno-15-11>)
    [](<https://adk.dev/artifacts/#__codelineno-15-12>)# When saving 'user:settings.json' via context.save_artifact,
    [](<https://adk.dev/artifacts/#__codelineno-15-13>)# the ArtifactService implementation should recognize the "user:" prefix
    [](<https://adk.dev/artifacts/#__codelineno-15-14>)# and scope it to app_name and user_id, making it accessible across sessions for that user.
    
    [](<https://adk.dev/artifacts/#__codelineno-16-1>)// Example illustrating namespace difference (conceptual)
    [](<https://adk.dev/artifacts/#__codelineno-16-2>)
    [](<https://adk.dev/artifacts/#__codelineno-16-3>)// Session-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-16-4>)const sessionReportFilename = "summary.txt";
    [](<https://adk.dev/artifacts/#__codelineno-16-5>)
    [](<https://adk.dev/artifacts/#__codelineno-16-6>)// User-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-16-7>)const userConfigFilename = "user:settings.json";
    [](<https://adk.dev/artifacts/#__codelineno-16-8>)
    [](<https://adk.dev/artifacts/#__codelineno-16-9>)// When saving 'summary.txt' via context.saveArtifact, it's tied to the current appName, userId, and sessionId.
    [](<https://adk.dev/artifacts/#__codelineno-16-10>)// When saving 'user:settings.json' via context.saveArtifact, the ArtifactService implementation recognizes the "user:" prefix and scopes it to appName and userId, making it accessible across sessions for that user.
    
    [](<https://adk.dev/artifacts/#__codelineno-17-1>)import (
    [](<https://adk.dev/artifacts/#__codelineno-17-2>)  "log"
    [](<https://adk.dev/artifacts/#__codelineno-17-3>))
    [](<https://adk.dev/artifacts/#__codelineno-17-4>)
    [](<https://adk.dev/artifacts/#__codelineno-17-5>)// Note: Namespacing is only supported when using the GCS ArtifactService implementation.
    [](<https://adk.dev/artifacts/#__codelineno-17-6>)// A session-scoped artifact is only available within the current session.
    [](<https://adk.dev/artifacts/#__codelineno-17-7>)sessionReportFilename := "summary.txt"
    [](<https://adk.dev/artifacts/#__codelineno-17-8>)// A user-scoped artifact is available across all sessions for the current user.
    [](<https://adk.dev/artifacts/#__codelineno-17-9>)userConfigFilename := "user:settings.json"
    [](<https://adk.dev/artifacts/#__codelineno-17-10>)
    [](<https://adk.dev/artifacts/#__codelineno-17-11>)// When saving 'summary.txt' via ctx.Artifacts().Save,
    [](<https://adk.dev/artifacts/#__codelineno-17-12>)// it's tied to the current app_name, user_id, and session_id.
    [](<https://adk.dev/artifacts/#__codelineno-17-13>)// ctx.Artifacts().Save(sessionReportFilename, *artifact);
    [](<https://adk.dev/artifacts/#__codelineno-17-14>)
    [](<https://adk.dev/artifacts/#__codelineno-17-15>)// When saving 'user:settings.json' via ctx.Artifacts().Save,
    [](<https://adk.dev/artifacts/#__codelineno-17-16>)// the ArtifactService implementation should recognize the "user:" prefix
    [](<https://adk.dev/artifacts/#__codelineno-17-17>)// and scope it to app_name and user_id, making it accessible across sessions for that user.
    [](<https://adk.dev/artifacts/#__codelineno-17-18>)// ctx.Artifacts().Save(userConfigFilename, *artifact);
    
    [](<https://adk.dev/artifacts/#__codelineno-18-1>)// Example illustrating namespace difference (conceptual)
    [](<https://adk.dev/artifacts/#__codelineno-18-2>)
    [](<https://adk.dev/artifacts/#__codelineno-18-3>)// Session-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-18-4>)String sessionReportFilename = "summary.txt";
    [](<https://adk.dev/artifacts/#__codelineno-18-5>)
    [](<https://adk.dev/artifacts/#__codelineno-18-6>)// User-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-18-7>)String userConfigFilename = "user:settings.json"; // The "user:" prefix is key
    [](<https://adk.dev/artifacts/#__codelineno-18-8>)
    [](<https://adk.dev/artifacts/#__codelineno-18-9>)// When saving 'summary.txt' via context.save_artifact,
    [](<https://adk.dev/artifacts/#__codelineno-18-10>)// it's tied to the current app_name, user_id, and session_id.
    [](<https://adk.dev/artifacts/#__codelineno-18-11>)// artifactService.saveArtifact(appName, userId, sessionId1, sessionReportFilename, someData);
    [](<https://adk.dev/artifacts/#__codelineno-18-12>)
    [](<https://adk.dev/artifacts/#__codelineno-18-13>)// When saving 'user:settings.json' via context.save_artifact,
    [](<https://adk.dev/artifacts/#__codelineno-18-14>)// the ArtifactService implementation should recognize the "user:" prefix
    [](<https://adk.dev/artifacts/#__codelineno-18-15>)// and scope it to app_name and user_id, making it accessible across sessions for that user.
    [](<https://adk.dev/artifacts/#__codelineno-18-16>)// artifactService.saveArtifact(appName, userId, sessionId1, userConfigFilename, someData);
    
    [](<https://adk.dev/artifacts/#__codelineno-19-1>)fun namespacingExample() {
    [](<https://adk.dev/artifacts/#__codelineno-19-2>)    // Session-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-19-3>)    val sessionReportFilename = "summary.txt"
    [](<https://adk.dev/artifacts/#__codelineno-19-4>)
    [](<https://adk.dev/artifacts/#__codelineno-19-5>)    // User-specific artifact filename
    [](<https://adk.dev/artifacts/#__codelineno-19-6>)    val userConfigFilename = "user:settings.json"
    [](<https://adk.dev/artifacts/#__codelineno-19-7>)}
    
These core concepts work together to provide a flexible system for managing binary data within the ADK framework.

## Interacting with Artifacts (via Context Objects)[¶](<https://adk.dev/artifacts/#interacting-with-artifacts-via-context-objects> "Permanent link")

The primary way you interact with artifacts within your agent's logic (specifically within callbacks or tools) is through methods provided by the `CallbackContext` and `ToolContext` objects. These methods abstract away the underlying storage details managed by the `ArtifactService`.

_(Note: In TypeScript,`CallbackContext` and `ToolContext` are unified into a single `Context` type.)_

### Prerequisite: Configuring the `ArtifactService`[¶](<https://adk.dev/artifacts/#prerequisite-configuring-the-artifactservice> "Permanent link")

Before you can use any artifact methods via the context objects, you **must** provide an instance of a [`BaseArtifactService` implementation](<https://adk.dev/artifacts/#available-implementations>) (like [`InMemoryArtifactService`](<https://adk.dev/artifacts/#inmemoryartifactservice>) or [`GcsArtifactService`](<https://adk.dev/artifacts/#gcsartifactservice>)) when initializing your `Runner`.

PythonTypescriptGoJavaKotlin

In Python, you provide this instance when initializing your `Runner`.
    
    [](<https://adk.dev/artifacts/#__codelineno-20-1>)from google.adk.runners import Runner
    [](<https://adk.dev/artifacts/#__codelineno-20-2>)from google.adk.artifacts import InMemoryArtifactService # Or GcsArtifactService
    [](<https://adk.dev/artifacts/#__codelineno-20-3>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/artifacts/#__codelineno-20-4>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/artifacts/#__codelineno-20-5>)
    [](<https://adk.dev/artifacts/#__codelineno-20-6>)# Your agent definition
    [](<https://adk.dev/artifacts/#__codelineno-20-7>)agent = LlmAgent(name="my_agent", model="gemini-flash-latest")
    [](<https://adk.dev/artifacts/#__codelineno-20-8>)
    [](<https://adk.dev/artifacts/#__codelineno-20-9>)# Instantiate the desired artifact service
    [](<https://adk.dev/artifacts/#__codelineno-20-10>)artifact_service = InMemoryArtifactService()
    [](<https://adk.dev/artifacts/#__codelineno-20-11>)
    [](<https://adk.dev/artifacts/#__codelineno-20-12>)# Provide it to the Runner
    [](<https://adk.dev/artifacts/#__codelineno-20-13>)runner = Runner(
    [](<https://adk.dev/artifacts/#__codelineno-20-14>)    agent=agent,
    [](<https://adk.dev/artifacts/#__codelineno-20-15>)    app_name="artifact_app",
    [](<https://adk.dev/artifacts/#__codelineno-20-16>)    session_service=InMemorySessionService(),
    [](<https://adk.dev/artifacts/#__codelineno-20-17>)    artifact_service=artifact_service # Service must be provided here
    [](<https://adk.dev/artifacts/#__codelineno-20-18>))
    
If no `artifact_service` is configured in the `InvocationContext` (which happens if it's not passed to the `Runner`), calling `save_artifact`, `load_artifact`, or `list_artifacts` on the context objects will raise a `ValueError`.
    
    [](<https://adk.dev/artifacts/#__codelineno-21-1>)import {
    [](<https://adk.dev/artifacts/#__codelineno-21-2>)  InMemoryArtifactService,
    [](<https://adk.dev/artifacts/#__codelineno-21-3>)  InMemorySessionService,
    [](<https://adk.dev/artifacts/#__codelineno-21-4>)  LlmAgent,
    [](<https://adk.dev/artifacts/#__codelineno-21-5>)  Runner,
    [](<https://adk.dev/artifacts/#__codelineno-21-6>)} from '@google/adk';
    [](<https://adk.dev/artifacts/#__codelineno-21-7>)
    [](<https://adk.dev/artifacts/#__codelineno-21-8>)// Your agent definition.
    [](<https://adk.dev/artifacts/#__codelineno-21-9>)const agent = new LlmAgent({
    [](<https://adk.dev/artifacts/#__codelineno-21-10>)  name: 'my_agent',
    [](<https://adk.dev/artifacts/#__codelineno-21-11>)  model: 'gemini-flash-latest',
    [](<https://adk.dev/artifacts/#__codelineno-21-12>)});
    [](<https://adk.dev/artifacts/#__codelineno-21-13>)
    [](<https://adk.dev/artifacts/#__codelineno-21-14>)// Instantiate the desired artifact service.
    [](<https://adk.dev/artifacts/#__codelineno-21-15>)const artifactService = new InMemoryArtifactService();
    [](<https://adk.dev/artifacts/#__codelineno-21-16>)
    [](<https://adk.dev/artifacts/#__codelineno-21-17>)// Provide it to the Runner.
    [](<https://adk.dev/artifacts/#__codelineno-21-18>)const runner = new Runner({
    [](<https://adk.dev/artifacts/#__codelineno-21-19>)  agent: agent,
    [](<https://adk.dev/artifacts/#__codelineno-21-20>)  appName: 'artifact_app',
    [](<https://adk.dev/artifacts/#__codelineno-21-21>)  sessionService: new InMemorySessionService(),
    [](<https://adk.dev/artifacts/#__codelineno-21-22>)  artifactService: artifactService,
    [](<https://adk.dev/artifacts/#__codelineno-21-23>)});
    [](<https://adk.dev/artifacts/#__codelineno-21-24>)// If no artifactService is configured, calling artifact methods on context objects will throw an error.
    
In Java, if an `ArtifactService` instance is not available (e.g., `null`) when artifact operations are attempted, it would typically result in a `NullPointerException` or a custom error, depending on how your application is structured. Robust applications often use dependency injection frameworks to manage service lifecycles and ensure availability.
    
    [](<https://adk.dev/artifacts/#__codelineno-22-1>)import (
    [](<https://adk.dev/artifacts/#__codelineno-22-2>)  "context"
    [](<https://adk.dev/artifacts/#__codelineno-22-3>)  "log"
    [](<https://adk.dev/artifacts/#__codelineno-22-4>)
    [](<https://adk.dev/artifacts/#__codelineno-22-5>)  "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/artifacts/#__codelineno-22-6>)  "google.golang.org/adk/v2/artifact"
    [](<https://adk.dev/artifacts/#__codelineno-22-7>)  "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/artifacts/#__codelineno-22-8>)  "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/artifacts/#__codelineno-22-9>)  "google.golang.org/adk/v2/session"
    [](<https://adk.dev/artifacts/#__codelineno-22-10>)  "google.golang.org/genai"
    [](<https://adk.dev/artifacts/#__codelineno-22-11>))
    [](<https://adk.dev/artifacts/#__codelineno-22-12>)
    [](<https://adk.dev/artifacts/#__codelineno-22-13>)// Create a new context.
    [](<https://adk.dev/artifacts/#__codelineno-22-14>)ctx := context.Background()
    [](<https://adk.dev/artifacts/#__codelineno-22-15>)// Set the app name.
    [](<https://adk.dev/artifacts/#__codelineno-22-16>)const appName = "my_artifact_app"
    [](<https://adk.dev/artifacts/#__codelineno-22-17>)// Create a new Gemini model.
    [](<https://adk.dev/artifacts/#__codelineno-22-18>)model, err := gemini.NewModel(ctx, "gemini-2.5-flash", &genai.ClientConfig{})
    [](<https://adk.dev/artifacts/#__codelineno-22-19>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-22-20>)    log.Fatalf("Failed to create model: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-22-21>)}
    [](<https://adk.dev/artifacts/#__codelineno-22-22>)
    [](<https://adk.dev/artifacts/#__codelineno-22-23>)// Create a new LLM agent.
    [](<https://adk.dev/artifacts/#__codelineno-22-24>)myAgent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/artifacts/#__codelineno-22-25>)    Model:       model,
    [](<https://adk.dev/artifacts/#__codelineno-22-26>)    Name:        "artifact_user_agent",
    [](<https://adk.dev/artifacts/#__codelineno-22-27>)    Instruction: "You are an agent that describes images.",
    [](<https://adk.dev/artifacts/#__codelineno-22-28>)    BeforeModelCallbacks: []llmagent.BeforeModelCallback{
    [](<https://adk.dev/artifacts/#__codelineno-22-29>)        BeforeModelCallback,
    [](<https://adk.dev/artifacts/#__codelineno-22-30>)    },
    [](<https://adk.dev/artifacts/#__codelineno-22-31>)})
    [](<https://adk.dev/artifacts/#__codelineno-22-32>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-22-33>)    log.Fatalf("Failed to create agent: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-22-34>)}
    [](<https://adk.dev/artifacts/#__codelineno-22-35>)
    [](<https://adk.dev/artifacts/#__codelineno-22-36>)// Create a new in-memory artifact service.
    [](<https://adk.dev/artifacts/#__codelineno-22-37>)artifactService := artifact.InMemoryService()
    [](<https://adk.dev/artifacts/#__codelineno-22-38>)// Create a new in-memory session service.
    [](<https://adk.dev/artifacts/#__codelineno-22-39>)sessionService := session.InMemoryService()
    [](<https://adk.dev/artifacts/#__codelineno-22-40>)
    [](<https://adk.dev/artifacts/#__codelineno-22-41>)// Create a new runner.
    [](<https://adk.dev/artifacts/#__codelineno-22-42>)r, err := runner.New(runner.Config{
    [](<https://adk.dev/artifacts/#__codelineno-22-43>)    Agent:           myAgent,
    [](<https://adk.dev/artifacts/#__codelineno-22-44>)    AppName:         appName,
    [](<https://adk.dev/artifacts/#__codelineno-22-45>)    SessionService:  sessionService,
    [](<https://adk.dev/artifacts/#__codelineno-22-46>)    ArtifactService: artifactService, // Provide the service instance here
    [](<https://adk.dev/artifacts/#__codelineno-22-47>)})
    [](<https://adk.dev/artifacts/#__codelineno-22-48>)if err != nil {
    [](<https://adk.dev/artifacts/#__codelineno-22-49>)    log.Fatalf("Failed to create runner: %v", err)
    [](<https://adk.dev/artifacts/#__codelineno-22-50>)}
    [](<https://adk.dev/artifacts/#__codelineno-22-51>)log.Printf("Runner created successfully: %v", r)
    
In Java, you would instantiate a `BaseArtifactService` implementation and then ensure it's accessible to the parts of your application that manage artifacts. This is often done through dependency injection or by explicitly passing the service instance.
    
    [](<https://adk.dev/artifacts/#__codelineno-23-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/artifacts/#__codelineno-23-2>)import com.google.adk.artifacts.InMemoryArtifactService; // Or GcsArtifactService
    [](<https://adk.dev/artifacts/#__codelineno-23-3>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/artifacts/#__codelineno-23-4>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/artifacts/#__codelineno-23-5>)
    [](<https://adk.dev/artifacts/#__codelineno-23-6>)public class SampleArtifactAgent {
    [](<https://adk.dev/artifacts/#__codelineno-23-7>)
    [](<https://adk.dev/artifacts/#__codelineno-23-8>)  public static void main(String[] args) {
    [](<https://adk.dev/artifacts/#__codelineno-23-9>)
    [](<https://adk.dev/artifacts/#__codelineno-23-10>)    // Your agent definition
    [](<https://adk.dev/artifacts/#__codelineno-23-11>)    LlmAgent agent = LlmAgent.builder()
    [](<https://adk.dev/artifacts/#__codelineno-23-12>)        .name("my_agent")
    [](<https://adk.dev/artifacts/#__codelineno-23-13>)        .model("gemini-flash-latest")
    [](<https://adk.dev/artifacts/#__codelineno-23-14>)        .build();
    [](<https://adk.dev/artifacts/#__codelineno-23-15>)
    [](<https://adk.dev/artifacts/#__codelineno-23-16>)    // Instantiate the desired artifact service
    [](<https://adk.dev/artifacts/#__codelineno-23-17>)    InMemoryArtifactService artifactService = new InMemoryArtifactService();
    [](<https://adk.dev/artifacts/#__codelineno-23-18>)
    [](<https://adk.dev/artifacts/#__codelineno-23-19>)    // Provide it to the Runner
    [](<https://adk.dev/artifacts/#__codelineno-23-20>)    Runner runner = new Runner(agent,
    [](<https://adk.dev/artifacts/#__codelineno-23-21>)        "APP_NAME",
    [](<https://adk.dev/artifacts/#__codelineno-23-22>)        artifactService, // Service must be provided here
    [](<https://adk.dev/artifacts/#__codelineno-23-23>)        new InMemorySessionService());
    [](<https://adk.dev/artifacts/#__codelineno-23-24>)
    [](<https://adk.dev/artifacts/#__codelineno-23-25>)  }
    [](<https://adk.dev/artifacts/#__codelineno-23-26>)}
    
In Kotlin, you provide this instance when initializing your `Runner`.
    
    [](<https://adk.dev/artifacts/#__codelineno-24-1>)fun configureRunnerExample() {
    [](<https://adk.dev/artifacts/#__codelineno-24-2>)    val myAgent =
    [](<https://adk.dev/artifacts/#__codelineno-24-3>)        LlmAgent(name = "artifact_user_agent", model = Gemini(name = "gemini-flash-latest"))
    [](<https://adk.dev/artifacts/#__codelineno-24-4>)    val artifactService = InMemoryArtifactService()
    [](<https://adk.dev/artifacts/#__codelineno-24-5>)    val sessionService = InMemorySessionService()
    [](<https://adk.dev/artifacts/#__codelineno-24-6>)
    [](<https://adk.dev/artifacts/#__codelineno-24-7>)    val runner =
    [](<https://adk.dev/artifacts/#__codelineno-24-8>)        InMemoryRunner(
    [](<https://adk.dev/artifacts/#__codelineno-24-9>)            agent = myAgent,
    [](<https://adk.dev/artifacts/#__codelineno-24-10>)            appName = "my_artifact_app",
    [](<https://adk.dev/artifacts/#__codelineno-24-11>)            sessionService = sessionService,
    [](<https://adk.dev/artifacts/#__codelineno-24-12>)            artifactService = artifactService,
    [](<https://adk.dev/artifacts/#__codelineno-24-13>)        )
    [](<https://adk.dev/artifacts/#__codelineno-24-14>)}
    
If no `artifactService` is configured, calling `saveArtifact`, `loadArtifact`, or `listArtifacts` on the context objects will throw an exception.

### Accessing Methods[¶](<https://adk.dev/artifacts/#accessing-methods> "Permanent link")

The artifact interaction methods are available directly on instances of `CallbackContext` (passed to agent and model callbacks) and `ToolContext` (passed to tool callbacks) in Python, Go, and Java and available on the unified `Context` in TypeScript.

#### Saving Artifacts[¶](<https://adk.dev/artifacts/#saving-artifacts> "Permanent link")

  * **Code Example:**

PythonTypescriptGoJavaKotlin
        
        [](<https://adk.dev/artifacts/#__codelineno-25-1>)import google.genai.types as types
        [](<https://adk.dev/artifacts/#__codelineno-25-2>)from google.adk.agents.callback_context import CallbackContext # Or ToolContext
        [](<https://adk.dev/artifacts/#__codelineno-25-3>)
        [](<https://adk.dev/artifacts/#__codelineno-25-4>)async def save_generated_report_py(context: CallbackContext, report_bytes: bytes):
        [](<https://adk.dev/artifacts/#__codelineno-25-5>)    """Saves generated PDF report bytes as an artifact."""
        [](<https://adk.dev/artifacts/#__codelineno-25-6>)    report_artifact = types.Part.from_bytes(
        [](<https://adk.dev/artifacts/#__codelineno-25-7>)        data=report_bytes,
        [](<https://adk.dev/artifacts/#__codelineno-25-8>)        mime_type="application/pdf"
        [](<https://adk.dev/artifacts/#__codelineno-25-9>)    )
        [](<https://adk.dev/artifacts/#__codelineno-25-10>)    filename = "generated_report.pdf"
        [](<https://adk.dev/artifacts/#__codelineno-25-11>)
        [](<https://adk.dev/artifacts/#__codelineno-25-12>)    try:
        [](<https://adk.dev/artifacts/#__codelineno-25-13>)        version = await context.save_artifact(filename=filename, artifact=report_artifact)
        [](<https://adk.dev/artifacts/#__codelineno-25-14>)        print(f"Successfully saved Python artifact '{filename}' as version {version}.")
        [](<https://adk.dev/artifacts/#__codelineno-25-15>)        # The event generated after this callback will contain:
        [](<https://adk.dev/artifacts/#__codelineno-25-16>)        # event.actions.artifact_delta == {"generated_report.pdf": version}
        [](<https://adk.dev/artifacts/#__codelineno-25-17>)    except ValueError as e:
        [](<https://adk.dev/artifacts/#__codelineno-25-18>)        print(f"Error saving Python artifact: {e}. Is ArtifactService configured in Runner?")
        [](<https://adk.dev/artifacts/#__codelineno-25-19>)    except Exception as e:
        [](<https://adk.dev/artifacts/#__codelineno-25-20>)        # Handle potential storage errors (e.g., GCS permissions)
        [](<https://adk.dev/artifacts/#__codelineno-25-21>)        print(f"An unexpected error occurred during Python artifact save: {e}")
        [](<https://adk.dev/artifacts/#__codelineno-25-22>)
        [](<https://adk.dev/artifacts/#__codelineno-25-23>)# --- Example Usage Concept (Python) ---
        [](<https://adk.dev/artifacts/#__codelineno-25-24>)# async def main_py():
        [](<https://adk.dev/artifacts/#__codelineno-25-25>)#   callback_context: CallbackContext = ... # obtain context
        [](<https://adk.dev/artifacts/#__codelineno-25-26>)#   report_data = b'...' # Assume this holds the PDF bytes
        [](<https://adk.dev/artifacts/#__codelineno-25-27>)#   await save_generated_report_py(callback_context, report_data)
        
        [](<https://adk.dev/artifacts/#__codelineno-26-1>)import {Context} from '@google/adk';
        [](<https://adk.dev/artifacts/#__codelineno-26-2>)import {createPartFromBase64, type Part} from '@google/genai';
        [](<https://adk.dev/artifacts/#__codelineno-26-3>)
        [](<https://adk.dev/artifacts/#__codelineno-26-4>)async function saveGeneratedReport(context: Context, reportBytes: Uint8Array): Promise<void> {
        [](<https://adk.dev/artifacts/#__codelineno-26-5>)  /** Saves generated PDF report bytes as an artifact. */
        [](<https://adk.dev/artifacts/#__codelineno-26-6>)  const reportArtifact: Part = createPartFromBase64(
        [](<https://adk.dev/artifacts/#__codelineno-26-7>)    Buffer.from(reportBytes).toString('base64'),
        [](<https://adk.dev/artifacts/#__codelineno-26-8>)    'application/pdf',
        [](<https://adk.dev/artifacts/#__codelineno-26-9>)  );
        [](<https://adk.dev/artifacts/#__codelineno-26-10>)
        [](<https://adk.dev/artifacts/#__codelineno-26-11>)  const filename = 'generated_report.pdf';
        [](<https://adk.dev/artifacts/#__codelineno-26-12>)
        [](<https://adk.dev/artifacts/#__codelineno-26-13>)  try {
        [](<https://adk.dev/artifacts/#__codelineno-26-14>)    const version = await context.saveArtifact(filename, reportArtifact);
        [](<https://adk.dev/artifacts/#__codelineno-26-15>)    console.log(`Successfully saved TypeScript artifact '${filename}' as version ${version}.`);
        [](<https://adk.dev/artifacts/#__codelineno-26-16>)  } catch (e: any) {
        [](<https://adk.dev/artifacts/#__codelineno-26-17>)    console.error(
        [](<https://adk.dev/artifacts/#__codelineno-26-18>)      `Error saving TypeScript artifact: ${e.message}. Is ArtifactService configured in Runner?`,
        [](<https://adk.dev/artifacts/#__codelineno-26-19>)    );
        [](<https://adk.dev/artifacts/#__codelineno-26-20>)  }
        [](<https://adk.dev/artifacts/#__codelineno-26-21>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-27-1>)import (
        [](<https://adk.dev/artifacts/#__codelineno-27-2>)  "log"
        [](<https://adk.dev/artifacts/#__codelineno-27-3>)
        [](<https://adk.dev/artifacts/#__codelineno-27-4>)  "google.golang.org/adk/v2/agent"
        [](<https://adk.dev/artifacts/#__codelineno-27-5>)  "google.golang.org/adk/v2/model"
        [](<https://adk.dev/artifacts/#__codelineno-27-6>)  "google.golang.org/genai"
        [](<https://adk.dev/artifacts/#__codelineno-27-7>))
        [](<https://adk.dev/artifacts/#__codelineno-27-8>)
        [](<https://adk.dev/artifacts/#__codelineno-27-9>)// saveReportCallback is a BeforeModel callback that saves a report from session state.
        [](<https://adk.dev/artifacts/#__codelineno-27-10>)func saveReportCallback(ctx agent.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
        [](<https://adk.dev/artifacts/#__codelineno-27-11>)    // Get the report data from the session state.
        [](<https://adk.dev/artifacts/#__codelineno-27-12>)    reportData, err := ctx.State().Get("report_bytes")
        [](<https://adk.dev/artifacts/#__codelineno-27-13>)    if err != nil {
        [](<https://adk.dev/artifacts/#__codelineno-27-14>)        log.Printf("No report data found in session state: %v", err)
        [](<https://adk.dev/artifacts/#__codelineno-27-15>)        return nil, nil // No report to save, continue normally.
        [](<https://adk.dev/artifacts/#__codelineno-27-16>)    }
        [](<https://adk.dev/artifacts/#__codelineno-27-17>)
        [](<https://adk.dev/artifacts/#__codelineno-27-18>)    // Check if the report data is in the expected format.
        [](<https://adk.dev/artifacts/#__codelineno-27-19>)    reportBytes, ok := reportData.([]byte)
        [](<https://adk.dev/artifacts/#__codelineno-27-20>)    if !ok {
        [](<https://adk.dev/artifacts/#__codelineno-27-21>)        log.Printf("Report data in session state was not in the expected byte format.")
        [](<https://adk.dev/artifacts/#__codelineno-27-22>)        return nil, nil
        [](<https://adk.dev/artifacts/#__codelineno-27-23>)    }
        [](<https://adk.dev/artifacts/#__codelineno-27-24>)
        [](<https://adk.dev/artifacts/#__codelineno-27-25>)    // Create a new artifact with the report data.
        [](<https://adk.dev/artifacts/#__codelineno-27-26>)    reportArtifact := &genai.Part{
        [](<https://adk.dev/artifacts/#__codelineno-27-27>)        InlineData: &genai.Blob{
        [](<https://adk.dev/artifacts/#__codelineno-27-28>)            MIMEType: "application/pdf",
        [](<https://adk.dev/artifacts/#__codelineno-27-29>)            Data:     reportBytes,
        [](<https://adk.dev/artifacts/#__codelineno-27-30>)        },
        [](<https://adk.dev/artifacts/#__codelineno-27-31>)    }
        [](<https://adk.dev/artifacts/#__codelineno-27-32>)    // Set the filename for the artifact.
        [](<https://adk.dev/artifacts/#__codelineno-27-33>)    filename := "generated_report.pdf"
        [](<https://adk.dev/artifacts/#__codelineno-27-34>)    // Save the artifact to the artifact service.
        [](<https://adk.dev/artifacts/#__codelineno-27-35>)    _, err = ctx.Artifacts().Save(ctx, filename, reportArtifact)
        [](<https://adk.dev/artifacts/#__codelineno-27-36>)    if err != nil {
        [](<https://adk.dev/artifacts/#__codelineno-27-37>)        log.Printf("An unexpected error occurred during Go artifact save: %v", err)
        [](<https://adk.dev/artifacts/#__codelineno-27-38>)        // Depending on requirements, you might want to return an error to the user.
        [](<https://adk.dev/artifacts/#__codelineno-27-39>)        return nil, nil
        [](<https://adk.dev/artifacts/#__codelineno-27-40>)    }
        [](<https://adk.dev/artifacts/#__codelineno-27-41>)    log.Printf("Successfully saved Go artifact '%s'.", filename)
        [](<https://adk.dev/artifacts/#__codelineno-27-42>)    // Return nil to continue to the next callback or the model.
        [](<https://adk.dev/artifacts/#__codelineno-27-43>)    return nil, nil
        [](<https://adk.dev/artifacts/#__codelineno-27-44>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-28-1>)import com.google.adk.agents.CallbackContext;
        [](<https://adk.dev/artifacts/#__codelineno-28-2>)import com.google.adk.artifacts.BaseArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-28-3>)import com.google.adk.artifacts.InMemoryArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-28-4>)import com.google.genai.types.Part;
        [](<https://adk.dev/artifacts/#__codelineno-28-5>)import java.nio.charset.StandardCharsets;
        [](<https://adk.dev/artifacts/#__codelineno-28-6>)
        [](<https://adk.dev/artifacts/#__codelineno-28-7>)public class SaveArtifactExample {
        [](<https://adk.dev/artifacts/#__codelineno-28-8>)
        [](<https://adk.dev/artifacts/#__codelineno-28-9>)public void saveGeneratedReport(CallbackContext callbackContext, byte[] reportBytes) {
        [](<https://adk.dev/artifacts/#__codelineno-28-10>)// Saves generated PDF report bytes as an artifact.
        [](<https://adk.dev/artifacts/#__codelineno-28-11>)Part reportArtifact = Part.fromBytes(reportBytes, "application/pdf");
        [](<https://adk.dev/artifacts/#__codelineno-28-12>)String filename = "generatedReport.pdf";
        [](<https://adk.dev/artifacts/#__codelineno-28-13>)
        [](<https://adk.dev/artifacts/#__codelineno-28-14>)    callbackContext.saveArtifact(filename, reportArtifact);
        [](<https://adk.dev/artifacts/#__codelineno-28-15>)    System.out.println("Successfully saved Java artifact '" + filename);
        [](<https://adk.dev/artifacts/#__codelineno-28-16>)    // The event generated after this callback will contain:
        [](<https://adk.dev/artifacts/#__codelineno-28-17>)    // event().actions().artifactDelta == {"generated_report.pdf": version}
        [](<https://adk.dev/artifacts/#__codelineno-28-18>)}
        [](<https://adk.dev/artifacts/#__codelineno-28-19>)
        [](<https://adk.dev/artifacts/#__codelineno-28-20>)// --- Example Usage Concept (Java) ---
        [](<https://adk.dev/artifacts/#__codelineno-28-21>)public static void main(String[] args) {
        [](<https://adk.dev/artifacts/#__codelineno-28-22>)    BaseArtifactService service = new InMemoryArtifactService(); // Or GcsArtifactService
        [](<https://adk.dev/artifacts/#__codelineno-28-23>)    SaveArtifactExample myTool = new SaveArtifactExample();
        [](<https://adk.dev/artifacts/#__codelineno-28-24>)    byte[] reportData = "...".getBytes(StandardCharsets.UTF_8); // PDF bytes
        [](<https://adk.dev/artifacts/#__codelineno-28-25>)    CallbackContext callbackContext; // ... obtain callback context from your app
        [](<https://adk.dev/artifacts/#__codelineno-28-26>)    myTool.saveGeneratedReport(callbackContext, reportData);
        [](<https://adk.dev/artifacts/#__codelineno-28-27>)    // Due to async nature, in a real app, ensure program waits or handles completion.
        [](<https://adk.dev/artifacts/#__codelineno-28-28>)  }
        [](<https://adk.dev/artifacts/#__codelineno-28-29>)}
        
In Kotlin, you access the `ArtifactService` from the `ToolContext` (or `CallbackContext` via `invocationContext`) to save an artifact.
        
        [](<https://adk.dev/artifacts/#__codelineno-29-1>)suspend fun saveGeneratedReport(
        [](<https://adk.dev/artifacts/#__codelineno-29-2>)    context: ToolContext,
        [](<https://adk.dev/artifacts/#__codelineno-29-3>)    reportBytes: ByteArray,
        [](<https://adk.dev/artifacts/#__codelineno-29-4>)) {
        [](<https://adk.dev/artifacts/#__codelineno-29-5>)    val reportArtifact =
        [](<https://adk.dev/artifacts/#__codelineno-29-6>)        Part(
        [](<https://adk.dev/artifacts/#__codelineno-29-7>)            inlineData =
        [](<https://adk.dev/artifacts/#__codelineno-29-8>)                Blob(
        [](<https://adk.dev/artifacts/#__codelineno-29-9>)                    data = reportBytes,
        [](<https://adk.dev/artifacts/#__codelineno-29-10>)                    mimeType = "application/pdf",
        [](<https://adk.dev/artifacts/#__codelineno-29-11>)                ),
        [](<https://adk.dev/artifacts/#__codelineno-29-12>)        )
        [](<https://adk.dev/artifacts/#__codelineno-29-13>)    val filename = "generated_report.pdf"
        [](<https://adk.dev/artifacts/#__codelineno-29-14>)
        [](<https://adk.dev/artifacts/#__codelineno-29-15>)    val service = context.invocationContext.artifactService
        [](<https://adk.dev/artifacts/#__codelineno-29-16>)    if (service != null) {
        [](<https://adk.dev/artifacts/#__codelineno-29-17>)        val version =
        [](<https://adk.dev/artifacts/#__codelineno-29-18>)            service.saveArtifact(
        [](<https://adk.dev/artifacts/#__codelineno-29-19>)                context.invocationContext.session.key,
        [](<https://adk.dev/artifacts/#__codelineno-29-20>)                filename,
        [](<https://adk.dev/artifacts/#__codelineno-29-21>)                reportArtifact,
        [](<https://adk.dev/artifacts/#__codelineno-29-22>)            )
        [](<https://adk.dev/artifacts/#__codelineno-29-23>)        println("Successfully saved Kotlin artifact '$filename' as version $version.")
        [](<https://adk.dev/artifacts/#__codelineno-29-24>)    } else {
        [](<https://adk.dev/artifacts/#__codelineno-29-25>)        println("Artifact service not available.")
        [](<https://adk.dev/artifacts/#__codelineno-29-26>)    }
        [](<https://adk.dev/artifacts/#__codelineno-29-27>)}
        
#### Loading Artifacts[¶](<https://adk.dev/artifacts/#loading-artifacts> "Permanent link")

  * **Code Example:**

PythonTypescriptGoJavaKotlin
        
        [](<https://adk.dev/artifacts/#__codelineno-30-1>)import google.genai.types as types
        [](<https://adk.dev/artifacts/#__codelineno-30-2>)from google.adk.agents.callback_context import CallbackContext # Or ToolContext
        [](<https://adk.dev/artifacts/#__codelineno-30-3>)
        [](<https://adk.dev/artifacts/#__codelineno-30-4>)async def process_latest_report_py(context: CallbackContext):
        [](<https://adk.dev/artifacts/#__codelineno-30-5>)    """Loads the latest report artifact and processes its data."""
        [](<https://adk.dev/artifacts/#__codelineno-30-6>)    filename = "generated_report.pdf"
        [](<https://adk.dev/artifacts/#__codelineno-30-7>)    try:
        [](<https://adk.dev/artifacts/#__codelineno-30-8>)        # Load the latest version
        [](<https://adk.dev/artifacts/#__codelineno-30-9>)        report_artifact = await context.load_artifact(filename=filename)
        [](<https://adk.dev/artifacts/#__codelineno-30-10>)
        [](<https://adk.dev/artifacts/#__codelineno-30-11>)        if report_artifact and report_artifact.inline_data:
        [](<https://adk.dev/artifacts/#__codelineno-30-12>)            print(f"Successfully loaded latest Python artifact '{filename}'.")
        [](<https://adk.dev/artifacts/#__codelineno-30-13>)            print(f"MIME Type: {report_artifact.inline_data.mime_type}")
        [](<https://adk.dev/artifacts/#__codelineno-30-14>)            # Process the report_artifact.inline_data.data (bytes)
        [](<https://adk.dev/artifacts/#__codelineno-30-15>)            pdf_bytes = report_artifact.inline_data.data
        [](<https://adk.dev/artifacts/#__codelineno-30-16>)            print(f"Report size: {len(pdf_bytes)} bytes.")
        [](<https://adk.dev/artifacts/#__codelineno-30-17>)            # ... further processing ...
        [](<https://adk.dev/artifacts/#__codelineno-30-18>)        else:
        [](<https://adk.dev/artifacts/#__codelineno-30-19>)            print(f"Python artifact '{filename}' not found.")
        [](<https://adk.dev/artifacts/#__codelineno-30-20>)
        [](<https://adk.dev/artifacts/#__codelineno-30-21>)        # Example: Load a specific version (if version 0 exists)
        [](<https://adk.dev/artifacts/#__codelineno-30-22>)        # specific_version_artifact = await context.load_artifact(filename=filename, version=0)
        [](<https://adk.dev/artifacts/#__codelineno-30-23>)        # if specific_version_artifact:
        [](<https://adk.dev/artifacts/#__codelineno-30-24>)        #     print(f"Loaded version 0 of '{filename}'.")
        [](<https://adk.dev/artifacts/#__codelineno-30-25>)
        [](<https://adk.dev/artifacts/#__codelineno-30-26>)    except ValueError as e:
        [](<https://adk.dev/artifacts/#__codelineno-30-27>)        print(f"Error loading Python artifact: {e}. Is ArtifactService configured?")
        [](<https://adk.dev/artifacts/#__codelineno-30-28>)    except Exception as e:
        [](<https://adk.dev/artifacts/#__codelineno-30-29>)        # Handle potential storage errors
        [](<https://adk.dev/artifacts/#__codelineno-30-30>)        print(f"An unexpected error occurred during Python artifact load: {e}")
        [](<https://adk.dev/artifacts/#__codelineno-30-31>)
        [](<https://adk.dev/artifacts/#__codelineno-30-32>)# --- Example Usage Concept (Python) ---
        [](<https://adk.dev/artifacts/#__codelineno-30-33>)# async def main_py():
        [](<https://adk.dev/artifacts/#__codelineno-30-34>)#   callback_context: CallbackContext = ... # obtain context
        [](<https://adk.dev/artifacts/#__codelineno-30-35>)#   await process_latest_report_py(callback_context)
        
        [](<https://adk.dev/artifacts/#__codelineno-31-1>)import {Context} from '@google/adk';
        [](<https://adk.dev/artifacts/#__codelineno-31-2>)
        [](<https://adk.dev/artifacts/#__codelineno-31-3>)async function processLatestReport(context: Context): Promise<void> {
        [](<https://adk.dev/artifacts/#__codelineno-31-4>)  /** Loads the latest report artifact and processes its data. */
        [](<https://adk.dev/artifacts/#__codelineno-31-5>)  const filename = 'generated_report.pdf';
        [](<https://adk.dev/artifacts/#__codelineno-31-6>)  try {
        [](<https://adk.dev/artifacts/#__codelineno-31-7>)    // Load the latest version
        [](<https://adk.dev/artifacts/#__codelineno-31-8>)    const reportArtifact = await context.loadArtifact(filename);
        [](<https://adk.dev/artifacts/#__codelineno-31-9>)
        [](<https://adk.dev/artifacts/#__codelineno-31-10>)    if (reportArtifact?.inlineData) {
        [](<https://adk.dev/artifacts/#__codelineno-31-11>)      console.log(`Successfully loaded latest TypeScript artifact '${filename}'.`);
        [](<https://adk.dev/artifacts/#__codelineno-31-12>)      console.log(`MIME Type: ${reportArtifact.inlineData.mimeType}`);
        [](<https://adk.dev/artifacts/#__codelineno-31-13>)      // Process the reportArtifact.inlineData.data (base64 string)
        [](<https://adk.dev/artifacts/#__codelineno-31-14>)      const pdfData = Buffer.from(reportArtifact.inlineData.data || '', 'base64');
        [](<https://adk.dev/artifacts/#__codelineno-31-15>)      console.log(`Report size: ${pdfData.length} bytes.`);
        [](<https://adk.dev/artifacts/#__codelineno-31-16>)      // ... further processing ...
        [](<https://adk.dev/artifacts/#__codelineno-31-17>)    } else {
        [](<https://adk.dev/artifacts/#__codelineno-31-18>)      console.log(`TypeScript artifact '${filename}' not found.`);
        [](<https://adk.dev/artifacts/#__codelineno-31-19>)    }
        [](<https://adk.dev/artifacts/#__codelineno-31-20>)  } catch (e: any) {
        [](<https://adk.dev/artifacts/#__codelineno-31-21>)    console.error(
        [](<https://adk.dev/artifacts/#__codelineno-31-22>)      `Error loading TypeScript artifact: ${e.message}. Is ArtifactService configured?`,
        [](<https://adk.dev/artifacts/#__codelineno-31-23>)    );
        [](<https://adk.dev/artifacts/#__codelineno-31-24>)  }
        [](<https://adk.dev/artifacts/#__codelineno-31-25>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-32-1>)import (
        [](<https://adk.dev/artifacts/#__codelineno-32-2>)  "log"
        [](<https://adk.dev/artifacts/#__codelineno-32-3>)
        [](<https://adk.dev/artifacts/#__codelineno-32-4>)  "google.golang.org/adk/v2/agent"
        [](<https://adk.dev/artifacts/#__codelineno-32-5>)  "google.golang.org/adk/v2/model"
        [](<https://adk.dev/artifacts/#__codelineno-32-6>))
        [](<https://adk.dev/artifacts/#__codelineno-32-7>)
        [](<https://adk.dev/artifacts/#__codelineno-32-8>)// loadArtifactsCallback is a BeforeModel callback that loads a specific artifact
        [](<https://adk.dev/artifacts/#__codelineno-32-9>)// and adds its content to the LLM request.
        [](<https://adk.dev/artifacts/#__codelineno-32-10>)func loadArtifactsCallback(ctx agent.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
        [](<https://adk.dev/artifacts/#__codelineno-32-11>)    log.Println("[Callback] loadArtifactsCallback triggered.")
        [](<https://adk.dev/artifacts/#__codelineno-32-12>)    // In a real app, you would parse the user's request to find a filename.
        [](<https://adk.dev/artifacts/#__codelineno-32-13>)    // For this example, we'll hardcode a filename to demonstrate.
        [](<https://adk.dev/artifacts/#__codelineno-32-14>)    const filenameToLoad = "generated_report.pdf"
        [](<https://adk.dev/artifacts/#__codelineno-32-15>)
        [](<https://adk.dev/artifacts/#__codelineno-32-16>)    // Load the artifact from the artifact service.
        [](<https://adk.dev/artifacts/#__codelineno-32-17>)    loadedPartResponse, err := ctx.Artifacts().Load(ctx, filenameToLoad)
        [](<https://adk.dev/artifacts/#__codelineno-32-18>)    if err != nil {
        [](<https://adk.dev/artifacts/#__codelineno-32-19>)        log.Printf("Callback could not load artifact '%s': %v", filenameToLoad, err)
        [](<https://adk.dev/artifacts/#__codelineno-32-20>)        return nil, nil // File not found or error, continue to model.
        [](<https://adk.dev/artifacts/#__codelineno-32-21>)    }
        [](<https://adk.dev/artifacts/#__codelineno-32-22>)
        [](<https://adk.dev/artifacts/#__codelineno-32-23>)    loadedPart := loadedPartResponse.Part
        [](<https://adk.dev/artifacts/#__codelineno-32-24>)
        [](<https://adk.dev/artifacts/#__codelineno-32-25>)    log.Printf("Callback successfully loaded artifact '%s'.", filenameToLoad)
        [](<https://adk.dev/artifacts/#__codelineno-32-26>)
        [](<https://adk.dev/artifacts/#__codelineno-32-27>)    // Ensure there's at least one content in the request to append to.
        [](<https://adk.dev/artifacts/#__codelineno-32-28>)    if len(req.Contents) == 0 {
        [](<https://adk.dev/artifacts/#__codelineno-32-29>)        req.Contents = []*genai.Content{{Parts: []*genai.Part{
        [](<https://adk.dev/artifacts/#__codelineno-32-30>)            genai.NewPartFromText("SYSTEM: The following file is provided for context:\n"),
        [](<https://adk.dev/artifacts/#__codelineno-32-31>)        }}}
        [](<https://adk.dev/artifacts/#__codelineno-32-32>)    }
        [](<https://adk.dev/artifacts/#__codelineno-32-33>)
        [](<https://adk.dev/artifacts/#__codelineno-32-34>)    // Add the loaded artifact to the request for the model.
        [](<https://adk.dev/artifacts/#__codelineno-32-35>)    lastContent := req.Contents[len(req.Contents)-1]
        [](<https://adk.dev/artifacts/#__codelineno-32-36>)    lastContent.Parts = append(lastContent.Parts, loadedPart)
        [](<https://adk.dev/artifacts/#__codelineno-32-37>)    log.Printf("Added artifact '%s' to LLM request.", filenameToLoad)
        [](<https://adk.dev/artifacts/#__codelineno-32-38>)
        [](<https://adk.dev/artifacts/#__codelineno-32-39>)    // Return nil to continue to the next callback or the model.
        [](<https://adk.dev/artifacts/#__codelineno-32-40>)    return nil, nil // Continue to next callback or LLM call
        [](<https://adk.dev/artifacts/#__codelineno-32-41>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-33-1>)import com.google.adk.artifacts.BaseArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-33-2>)import com.google.genai.types.Part;
        [](<https://adk.dev/artifacts/#__codelineno-33-3>)import io.reactivex.rxjava3.core.MaybeObserver;
        [](<https://adk.dev/artifacts/#__codelineno-33-4>)import io.reactivex.rxjava3.disposables.Disposable;
        [](<https://adk.dev/artifacts/#__codelineno-33-5>)import java.util.Optional;
        [](<https://adk.dev/artifacts/#__codelineno-33-6>)
        [](<https://adk.dev/artifacts/#__codelineno-33-7>)public class MyArtifactLoaderService {
        [](<https://adk.dev/artifacts/#__codelineno-33-8>)
        [](<https://adk.dev/artifacts/#__codelineno-33-9>)    private final BaseArtifactService artifactService;
        [](<https://adk.dev/artifacts/#__codelineno-33-10>)    private final String appName;
        [](<https://adk.dev/artifacts/#__codelineno-33-11>)
        [](<https://adk.dev/artifacts/#__codelineno-33-12>)    public MyArtifactLoaderService(BaseArtifactService artifactService, String appName) {
        [](<https://adk.dev/artifacts/#__codelineno-33-13>)        this.artifactService = artifactService;
        [](<https://adk.dev/artifacts/#__codelineno-33-14>)        this.appName = appName;
        [](<https://adk.dev/artifacts/#__codelineno-33-15>)    }
        [](<https://adk.dev/artifacts/#__codelineno-33-16>)
        [](<https://adk.dev/artifacts/#__codelineno-33-17>)    public void processLatestReportJava(String userId, String sessionId, String filename) {
        [](<https://adk.dev/artifacts/#__codelineno-33-18>)        // Load the latest version by passing Optional.empty() for the version
        [](<https://adk.dev/artifacts/#__codelineno-33-19>)        artifactService
        [](<https://adk.dev/artifacts/#__codelineno-33-20>)                .loadArtifact(appName, userId, sessionId, filename, Optional.empty())
        [](<https://adk.dev/artifacts/#__codelineno-33-21>)                .subscribe(
        [](<https://adk.dev/artifacts/#__codelineno-33-22>)                        new MaybeObserver<Part>() {
        [](<https://adk.dev/artifacts/#__codelineno-33-23>)                            @Override
        [](<https://adk.dev/artifacts/#__codelineno-33-24>)                            public void onSubscribe(Disposable d) {
        [](<https://adk.dev/artifacts/#__codelineno-33-25>)                                // Optional: handle subscription
        [](<https://adk.dev/artifacts/#__codelineno-33-26>)                            }
        [](<https://adk.dev/artifacts/#__codelineno-33-27>)
        [](<https://adk.dev/artifacts/#__codelineno-33-28>)                            @Override
        [](<https://adk.dev/artifacts/#__codelineno-33-29>)                            public void onSuccess(Part reportArtifact) {
        [](<https://adk.dev/artifacts/#__codelineno-33-30>)                                System.out.println(
        [](<https://adk.dev/artifacts/#__codelineno-33-31>)                                        "Successfully loaded latest Java artifact '" + filename + "'.");
        [](<https://adk.dev/artifacts/#__codelineno-33-32>)                                reportArtifact
        [](<https://adk.dev/artifacts/#__codelineno-33-33>)                                        .inlineData()
        [](<https://adk.dev/artifacts/#__codelineno-33-34>)                                        .ifPresent(
        [](<https://adk.dev/artifacts/#__codelineno-33-35>)                                                blob -> {
        [](<https://adk.dev/artifacts/#__codelineno-33-36>)                                                    System.out.println(
        [](<https://adk.dev/artifacts/#__codelineno-33-37>)                                                            "MIME Type: " + blob.mimeType().orElse("N/A"));
        [](<https://adk.dev/artifacts/#__codelineno-33-38>)                                                    byte[] pdfBytes = blob.data().orElse(new byte[0]);
        [](<https://adk.dev/artifacts/#__codelineno-33-39>)                                                    System.out.println("Report size: " + pdfBytes.length + " bytes.");
        [](<https://adk.dev/artifacts/#__codelineno-33-40>)                                                    // ... further processing of pdfBytes ...
        [](<https://adk.dev/artifacts/#__codelineno-33-41>)                                                });
        [](<https://adk.dev/artifacts/#__codelineno-33-42>)                            }
        [](<https://adk.dev/artifacts/#__codelineno-33-43>)
        [](<https://adk.dev/artifacts/#__codelineno-33-44>)                            @Override
        [](<https://adk.dev/artifacts/#__codelineno-33-45>)                            public void onError(Throwable e) {
        [](<https://adk.dev/artifacts/#__codelineno-33-46>)                                // Handle potential storage errors or other exceptions
        [](<https://adk.dev/artifacts/#__codelineno-33-47>)                                System.err.println(
        [](<https://adk.dev/artifacts/#__codelineno-33-48>)                                        "An error occurred during Java artifact load for '"
        [](<https://adk.dev/artifacts/#__codelineno-33-49>)                                                + filename
        [](<https://adk.dev/artifacts/#__codelineno-33-50>)                                                + "': "
        [](<https://adk.dev/artifacts/#__codelineno-33-51>)                                                + e.getMessage());
        [](<https://adk.dev/artifacts/#__codelineno-33-52>)                            }
        [](<https://adk.dev/artifacts/#__codelineno-33-53>)
        [](<https://adk.dev/artifacts/#__codelineno-33-54>)                            @Override
        [](<https://adk.dev/artifacts/#__codelineno-33-55>)                            public void onComplete() {
        [](<https://adk.dev/artifacts/#__codelineno-33-56>)                                // Called if the artifact (latest version) is not found
        [](<https://adk.dev/artifacts/#__codelineno-33-57>)                                System.out.println("Java artifact '" + filename + "' not found.");
        [](<https://adk.dev/artifacts/#__codelineno-33-58>)                            }
        [](<https://adk.dev/artifacts/#__codelineno-33-59>)                        });
        [](<https://adk.dev/artifacts/#__codelineno-33-60>)
        [](<https://adk.dev/artifacts/#__codelineno-33-61>)        // Example: Load a specific version (e.g., version 0)
        [](<https://adk.dev/artifacts/#__codelineno-33-62>)        /*
        [](<https://adk.dev/artifacts/#__codelineno-33-63>)        artifactService.loadArtifact(appName, userId, sessionId, filename, Optional.of(0))
        [](<https://adk.dev/artifacts/#__codelineno-33-64>)            .subscribe(part -> {
        [](<https://adk.dev/artifacts/#__codelineno-33-65>)                System.out.println("Loaded version 0 of Java artifact '" + filename + "'.");
        [](<https://adk.dev/artifacts/#__codelineno-33-66>)            }, throwable -> {
        [](<https://adk.dev/artifacts/#__codelineno-33-67>)                System.err.println("Error loading version 0 of '" + filename + "': " + throwable.getMessage());
        [](<https://adk.dev/artifacts/#__codelineno-33-68>)            }, () -> {
        [](<https://adk.dev/artifacts/#__codelineno-33-69>)                System.out.println("Version 0 of Java artifact '" + filename + "' not found.");
        [](<https://adk.dev/artifacts/#__codelineno-33-70>)            });
        [](<https://adk.dev/artifacts/#__codelineno-33-71>)        */
        [](<https://adk.dev/artifacts/#__codelineno-33-72>)    }
        [](<https://adk.dev/artifacts/#__codelineno-33-73>)
        [](<https://adk.dev/artifacts/#__codelineno-33-74>)    // --- Example Usage Concept (Java) ---
        [](<https://adk.dev/artifacts/#__codelineno-33-75>)    public static void main(String[] args) {
        [](<https://adk.dev/artifacts/#__codelineno-33-76>)        // BaseArtifactService service = new InMemoryArtifactService(); // Or GcsArtifactService
        [](<https://adk.dev/artifacts/#__codelineno-33-77>)        // MyArtifactLoaderService loader = new MyArtifactLoaderService(service, "myJavaApp");
        [](<https://adk.dev/artifacts/#__codelineno-33-78>)        // loader.processLatestReportJava("user123", "sessionABC", "java_report.pdf");
        [](<https://adk.dev/artifacts/#__codelineno-33-79>)        // Due to async nature, in a real app, ensure program waits or handles completion.
        [](<https://adk.dev/artifacts/#__codelineno-33-80>)    }
        [](<https://adk.dev/artifacts/#__codelineno-33-81>)}
        
In Kotlin, you can load an artifact directly from the `ToolContext` (or `CallbackContext`) using `context.loadArtifact(name)`.
        
        [](<https://adk.dev/artifacts/#__codelineno-34-1>)suspend fun processLatestReport(context: ToolContext) {
        [](<https://adk.dev/artifacts/#__codelineno-34-2>)    val filename = "generated_report.pdf"
        [](<https://adk.dev/artifacts/#__codelineno-34-3>)    val reportArtifact = context.loadArtifact(filename)
        [](<https://adk.dev/artifacts/#__codelineno-34-4>)
        [](<https://adk.dev/artifacts/#__codelineno-34-5>)    if (reportArtifact != null && reportArtifact.inlineData != null) {
        [](<https://adk.dev/artifacts/#__codelineno-34-6>)        println("Successfully loaded latest Kotlin artifact '$filename'.")
        [](<https://adk.dev/artifacts/#__codelineno-34-7>)        println("MIME Type: ${reportArtifact.inlineData?.mimeType}")
        [](<https://adk.dev/artifacts/#__codelineno-34-8>)        val pdfBytes = reportArtifact.inlineData?.data
        [](<https://adk.dev/artifacts/#__codelineno-34-9>)        println("Report size: ${pdfBytes?.size} bytes.")
        [](<https://adk.dev/artifacts/#__codelineno-34-10>)    } else {
        [](<https://adk.dev/artifacts/#__codelineno-34-11>)        println("Kotlin artifact '$filename' not found.")
        [](<https://adk.dev/artifacts/#__codelineno-34-12>)    }
        [](<https://adk.dev/artifacts/#__codelineno-34-13>)}
        
#### Using `LoadArtifactsTool`[¶](<https://adk.dev/artifacts/#using-loadartifactstool> "Permanent link")

You can add `LoadArtifactsTool` when the model should decide which available artifacts to load before answering. This is useful when users ask follow-up questions about uploaded files or large generated outputs that are stored as artifacts instead of kept in the conversation context.

`LoadArtifactsTool` lists available artifacts in the model instructions. When the model calls the `load_artifacts` tool, ADK temporarily appends the selected artifact contents to that request so the model can answer with the file content in context. The loaded artifact content is not permanently saved back into the session history, so the model should call the tool again when it needs the same artifact in a later turn.

PythonGoKotlin
    
    [](<https://adk.dev/artifacts/#__codelineno-35-1>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/artifacts/#__codelineno-35-2>)from google.adk.tools.load_artifacts_tool import LoadArtifactsTool
    [](<https://adk.dev/artifacts/#__codelineno-35-3>)
    [](<https://adk.dev/artifacts/#__codelineno-35-4>)root_agent = LlmAgent(
    [](<https://adk.dev/artifacts/#__codelineno-35-5>)    name="artifact_reader",
    [](<https://adk.dev/artifacts/#__codelineno-35-6>)    model="gemini-flash-latest",
    [](<https://adk.dev/artifacts/#__codelineno-35-7>)    instruction=(
    [](<https://adk.dev/artifacts/#__codelineno-35-8>)        "Answer questions about available user files. "
    [](<https://adk.dev/artifacts/#__codelineno-35-9>)        "Call load_artifacts before answering when you need file contents."
    [](<https://adk.dev/artifacts/#__codelineno-35-10>)    ),
    [](<https://adk.dev/artifacts/#__codelineno-35-11>)    tools=[
    [](<https://adk.dev/artifacts/#__codelineno-35-12>)        LoadArtifactsTool(),
    [](<https://adk.dev/artifacts/#__codelineno-35-13>)    ],
    [](<https://adk.dev/artifacts/#__codelineno-35-14>))
    
Make sure the `Runner` for this agent is configured with an `artifact_service`; otherwise artifact listing and loading will fail. If your artifacts need human-readable summaries, subclass `LoadArtifactsTool` and customize its request instructions before loading the selected artifact contents.
    
    [](<https://adk.dev/artifacts/#__codelineno-36-1>)import (
    [](<https://adk.dev/artifacts/#__codelineno-36-2>)  "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/artifacts/#__codelineno-36-3>)  "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/artifacts/#__codelineno-36-4>)  "google.golang.org/adk/v2/tool/loadartifactstool"
    [](<https://adk.dev/artifacts/#__codelineno-36-5>))
    [](<https://adk.dev/artifacts/#__codelineno-36-6>)
    [](<https://adk.dev/artifacts/#__codelineno-36-7>)agent, err := llmagent.New(llmagent.Config{
    [](<https://adk.dev/artifacts/#__codelineno-36-8>)    Name:        "artifact_reader",
    [](<https://adk.dev/artifacts/#__codelineno-36-9>)    Model:       model,
    [](<https://adk.dev/artifacts/#__codelineno-36-10>)    Instruction: "Answer questions about available user files. " +
    [](<https://adk.dev/artifacts/#__codelineno-36-11>)        "When user asks about artifacts, load them and describe them.",
    [](<https://adk.dev/artifacts/#__codelineno-36-12>)    Tools: []tool.Tool{
    [](<https://adk.dev/artifacts/#__codelineno-36-13>)        loadartifactstool.New(),
    [](<https://adk.dev/artifacts/#__codelineno-36-14>)    },
    [](<https://adk.dev/artifacts/#__codelineno-36-15>)})
    
Make sure the `runner.Config` for this agent includes an `ArtifactService`; otherwise artifact listing and loading will fail.
    
    [](<https://adk.dev/artifacts/#__codelineno-37-1>)fun loadArtifactsToolExample() {
    [](<https://adk.dev/artifacts/#__codelineno-37-2>)    val rootAgent =
    [](<https://adk.dev/artifacts/#__codelineno-37-3>)        LlmAgent(
    [](<https://adk.dev/artifacts/#__codelineno-37-4>)            name = "artifact_reader",
    [](<https://adk.dev/artifacts/#__codelineno-37-5>)            model = Gemini(name = "gemini-flash-latest"),
    [](<https://adk.dev/artifacts/#__codelineno-37-6>)            instruction =
    [](<https://adk.dev/artifacts/#__codelineno-37-7>)                Instruction(
    [](<https://adk.dev/artifacts/#__codelineno-37-8>)                    "Answer questions about available user files. " +
    [](<https://adk.dev/artifacts/#__codelineno-37-9>)                        "Call load_artifacts before answering when you need file contents.",
    [](<https://adk.dev/artifacts/#__codelineno-37-10>)                ),
    [](<https://adk.dev/artifacts/#__codelineno-37-11>)            tools = listOf(LoadArtifactsTool()),
    [](<https://adk.dev/artifacts/#__codelineno-37-12>)        )
    [](<https://adk.dev/artifacts/#__codelineno-37-13>)}
    
Make sure the `Runner` for this agent is configured with an `artifactService`; otherwise artifact listing and loading will fail.

#### Listing Artifact Filenames[¶](<https://adk.dev/artifacts/#listing-artifact-filenames> "Permanent link")

  * **Code Example:**

PythonTypescriptGoJava
        
        [](<https://adk.dev/artifacts/#__codelineno-38-1>)from google.adk.tools.tool_context import ToolContext
        [](<https://adk.dev/artifacts/#__codelineno-38-2>)
        [](<https://adk.dev/artifacts/#__codelineno-38-3>)def list_user_files_py(tool_context: ToolContext) -> str:
        [](<https://adk.dev/artifacts/#__codelineno-38-4>)    """Tool to list available artifacts for the user."""
        [](<https://adk.dev/artifacts/#__codelineno-38-5>)    try:
        [](<https://adk.dev/artifacts/#__codelineno-38-6>)        available_files = await tool_context.list_artifacts()
        [](<https://adk.dev/artifacts/#__codelineno-38-7>)        if not available_files:
        [](<https://adk.dev/artifacts/#__codelineno-38-8>)            return "You have no saved artifacts."
        [](<https://adk.dev/artifacts/#__codelineno-38-9>)        else:
        [](<https://adk.dev/artifacts/#__codelineno-38-10>)            # Format the list for the user/LLM
        [](<https://adk.dev/artifacts/#__codelineno-38-11>)            file_list_str = "\n".join([f"- {fname}" for fname in available_files])
        [](<https://adk.dev/artifacts/#__codelineno-38-12>)            return f"Here are your available Python artifacts:\n{file_list_str}"
        [](<https://adk.dev/artifacts/#__codelineno-38-13>)    except ValueError as e:
        [](<https://adk.dev/artifacts/#__codelineno-38-14>)        print(f"Error listing Python artifacts: {e}. Is ArtifactService configured?")
        [](<https://adk.dev/artifacts/#__codelineno-38-15>)        return "Error: Could not list Python artifacts."
        [](<https://adk.dev/artifacts/#__codelineno-38-16>)    except Exception as e:
        [](<https://adk.dev/artifacts/#__codelineno-38-17>)        print(f"An unexpected error occurred during Python artifact list: {e}")
        [](<https://adk.dev/artifacts/#__codelineno-38-18>)        return "Error: An unexpected error occurred while listing Python artifacts."
        [](<https://adk.dev/artifacts/#__codelineno-38-19>)
        [](<https://adk.dev/artifacts/#__codelineno-38-20>)# This function would typically be wrapped in a FunctionTool
        [](<https://adk.dev/artifacts/#__codelineno-38-21>)# from google.adk.tools import FunctionTool
        [](<https://adk.dev/artifacts/#__codelineno-38-22>)# list_files_tool = FunctionTool(func=list_user_files_py)
        
        [](<https://adk.dev/artifacts/#__codelineno-39-1>)import {Context} from '@google/adk';
        [](<https://adk.dev/artifacts/#__codelineno-39-2>)
        [](<https://adk.dev/artifacts/#__codelineno-39-3>)async function listUserFiles(context: Context): Promise<string> {
        [](<https://adk.dev/artifacts/#__codelineno-39-4>)  /** Tool to list available artifacts for the user. */
        [](<https://adk.dev/artifacts/#__codelineno-39-5>)  try {
        [](<https://adk.dev/artifacts/#__codelineno-39-6>)    const availableFiles = await context.listArtifacts();
        [](<https://adk.dev/artifacts/#__codelineno-39-7>)    if (!availableFiles || availableFiles.length === 0) {
        [](<https://adk.dev/artifacts/#__codelineno-39-8>)      return 'You have no saved artifacts.';
        [](<https://adk.dev/artifacts/#__codelineno-39-9>)    } else {
        [](<https://adk.dev/artifacts/#__codelineno-39-10>)      // Format the list for the user/LLM
        [](<https://adk.dev/artifacts/#__codelineno-39-11>)      const fileListStr = availableFiles.map((fname) => `- ${fname}`).join('\n');
        [](<https://adk.dev/artifacts/#__codelineno-39-12>)      return `Here are your available TypeScript artifacts:\n${fileListStr}`;
        [](<https://adk.dev/artifacts/#__codelineno-39-13>)    }
        [](<https://adk.dev/artifacts/#__codelineno-39-14>)  } catch (e: any) {
        [](<https://adk.dev/artifacts/#__codelineno-39-15>)    console.error(
        [](<https://adk.dev/artifacts/#__codelineno-39-16>)      `Error listing TypeScript artifacts: ${e.message}. Is ArtifactService configured?`,
        [](<https://adk.dev/artifacts/#__codelineno-39-17>)    );
        [](<https://adk.dev/artifacts/#__codelineno-39-18>)    return 'Error: Could not list TypeScript artifacts.';
        [](<https://adk.dev/artifacts/#__codelineno-39-19>)  }
        [](<https://adk.dev/artifacts/#__codelineno-39-20>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-40-1>)import (
        [](<https://adk.dev/artifacts/#__codelineno-40-2>)  "fmt"
        [](<https://adk.dev/artifacts/#__codelineno-40-3>)  "log"
        [](<https://adk.dev/artifacts/#__codelineno-40-4>)  "strings"
        [](<https://adk.dev/artifacts/#__codelineno-40-5>)
        [](<https://adk.dev/artifacts/#__codelineno-40-6>)  "google.golang.org/adk/v2/agent"
        [](<https://adk.dev/artifacts/#__codelineno-40-7>)  "google.golang.org/adk/v2/model"
        [](<https://adk.dev/artifacts/#__codelineno-40-8>)  "google.golang.org/genai"
        [](<https://adk.dev/artifacts/#__codelineno-40-9>))
        [](<https://adk.dev/artifacts/#__codelineno-40-10>)
        [](<https://adk.dev/artifacts/#__codelineno-40-11>)// listUserFilesCallback is a BeforeModel callback that lists available artifacts
        [](<https://adk.dev/artifacts/#__codelineno-40-12>)// and adds the list as context to the LLM request.
        [](<https://adk.dev/artifacts/#__codelineno-40-13>)func listUserFilesCallback(ctx agent.Context, req *model.LLMRequest) (*model.LLMResponse, error) {
        [](<https://adk.dev/artifacts/#__codelineno-40-14>)    log.Println("[Callback] listUserFilesCallback triggered.")
        [](<https://adk.dev/artifacts/#__codelineno-40-15>)    // List the available artifacts from the artifact service.
        [](<https://adk.dev/artifacts/#__codelineno-40-16>)    listResponse, err := ctx.Artifacts().List(ctx)
        [](<https://adk.dev/artifacts/#__codelineno-40-17>)    if err != nil {
        [](<https://adk.dev/artifacts/#__codelineno-40-18>)        log.Printf("An unexpected error occurred during Go artifact list: %v", err)
        [](<https://adk.dev/artifacts/#__codelineno-40-19>)        return nil, nil // Continue, but log the error.
        [](<https://adk.dev/artifacts/#__codelineno-40-20>)    }
        [](<https://adk.dev/artifacts/#__codelineno-40-21>)
        [](<https://adk.dev/artifacts/#__codelineno-40-22>)    availableFiles := listResponse.FileNames
        [](<https://adk.dev/artifacts/#__codelineno-40-23>)
        [](<https://adk.dev/artifacts/#__codelineno-40-24>)    log.Printf("Found %d available files.", len(availableFiles))
        [](<https://adk.dev/artifacts/#__codelineno-40-25>)
        [](<https://adk.dev/artifacts/#__codelineno-40-26>)    // If there are available files, add them to the LLM request.
        [](<https://adk.dev/artifacts/#__codelineno-40-27>)    if len(availableFiles) > 0 {
        [](<https://adk.dev/artifacts/#__codelineno-40-28>)        var fileListStr strings.Builder
        [](<https://adk.dev/artifacts/#__codelineno-40-29>)        fileListStr.WriteString("SYSTEM: The following files are available:\n")
        [](<https://adk.dev/artifacts/#__codelineno-40-30>)        for _, fname := range availableFiles {
        [](<https://adk.dev/artifacts/#__codelineno-40-31>)            fileListStr.WriteString(fmt.Sprintf("- %s\n", fname))
        [](<https://adk.dev/artifacts/#__codelineno-40-32>)        }
        [](<https://adk.dev/artifacts/#__codelineno-40-33>)        // Prepend this information to the user's request for the model.
        [](<https://adk.dev/artifacts/#__codelineno-40-34>)        if len(req.Contents) > 0 {
        [](<https://adk.dev/artifacts/#__codelineno-40-35>)            lastContent := req.Contents[len(req.Contents)-1]
        [](<https://adk.dev/artifacts/#__codelineno-40-36>)            if len(lastContent.Parts) > 0 {
        [](<https://adk.dev/artifacts/#__codelineno-40-37>)                fileListStr.WriteString("\n") // Add a newline for separation.
        [](<https://adk.dev/artifacts/#__codelineno-40-38>)                lastContent.Parts[0] = genai.NewPartFromText(fileListStr.String() + lastContent.Parts[0].Text)
        [](<https://adk.dev/artifacts/#__codelineno-40-39>)                log.Println("Added file list to LLM request context.")
        [](<https://adk.dev/artifacts/#__codelineno-40-40>)            }
        [](<https://adk.dev/artifacts/#__codelineno-40-41>)        }
        [](<https://adk.dev/artifacts/#__codelineno-40-42>)        log.Printf("Available files:\n%s", fileListStr.String())
        [](<https://adk.dev/artifacts/#__codelineno-40-43>)    } else {
        [](<https://adk.dev/artifacts/#__codelineno-40-44>)        log.Println("No available files found to list.")
        [](<https://adk.dev/artifacts/#__codelineno-40-45>)    }
        [](<https://adk.dev/artifacts/#__codelineno-40-46>)
        [](<https://adk.dev/artifacts/#__codelineno-40-47>)    // Return nil to continue to the next callback or the model.
        [](<https://adk.dev/artifacts/#__codelineno-40-48>)    return nil, nil // Continue to next callback or LLM call
        [](<https://adk.dev/artifacts/#__codelineno-40-49>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-41-1>)import com.google.adk.artifacts.BaseArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-41-2>)import com.google.adk.artifacts.ListArtifactsResponse;
        [](<https://adk.dev/artifacts/#__codelineno-41-3>)import com.google.common.collect.ImmutableList;
        [](<https://adk.dev/artifacts/#__codelineno-41-4>)import io.reactivex.rxjava3.core.SingleObserver;
        [](<https://adk.dev/artifacts/#__codelineno-41-5>)import io.reactivex.rxjava3.disposables.Disposable;
        [](<https://adk.dev/artifacts/#__codelineno-41-6>)
        [](<https://adk.dev/artifacts/#__codelineno-41-7>)public class MyArtifactListerService {
        [](<https://adk.dev/artifacts/#__codelineno-41-8>)
        [](<https://adk.dev/artifacts/#__codelineno-41-9>)    private final BaseArtifactService artifactService;
        [](<https://adk.dev/artifacts/#__codelineno-41-10>)    private final String appName;
        [](<https://adk.dev/artifacts/#__codelineno-41-11>)
        [](<https://adk.dev/artifacts/#__codelineno-41-12>)    public MyArtifactListerService(BaseArtifactService artifactService, String appName) {
        [](<https://adk.dev/artifacts/#__codelineno-41-13>)        this.artifactService = artifactService;
        [](<https://adk.dev/artifacts/#__codelineno-41-14>)        this.appName = appName;
        [](<https://adk.dev/artifacts/#__codelineno-41-15>)    }
        [](<https://adk.dev/artifacts/#__codelineno-41-16>)
        [](<https://adk.dev/artifacts/#__codelineno-41-17>)    // Example method that might be called by a tool or agent logic
        [](<https://adk.dev/artifacts/#__codelineno-41-18>)    public void listUserFilesJava(String userId, String sessionId) {
        [](<https://adk.dev/artifacts/#__codelineno-41-19>)        artifactService
        [](<https://adk.dev/artifacts/#__codelineno-41-20>)                .listArtifactKeys(appName, userId, sessionId)
        [](<https://adk.dev/artifacts/#__codelineno-41-21>)                .subscribe(
        [](<https://adk.dev/artifacts/#__codelineno-41-22>)                        new SingleObserver<ListArtifactsResponse>() {
        [](<https://adk.dev/artifacts/#__codelineno-41-23>)                            @Override
        [](<https://adk.dev/artifacts/#__codelineno-41-24>)                            public void onSubscribe(Disposable d) {
        [](<https://adk.dev/artifacts/#__codelineno-41-25>)                                // Optional: handle subscription
        [](<https://adk.dev/artifacts/#__codelineno-41-26>)                            }
        [](<https://adk.dev/artifacts/#__codelineno-41-27>)
        [](<https://adk.dev/artifacts/#__codelineno-41-28>)                            @Override
        [](<https://adk.dev/artifacts/#__codelineno-41-29>)                            public void onSuccess(ListArtifactsResponse response) {
        [](<https://adk.dev/artifacts/#__codelineno-41-30>)                                ImmutableList<String> availableFiles = response.filenames();
        [](<https://adk.dev/artifacts/#__codelineno-41-31>)                                if (availableFiles.isEmpty()) {
        [](<https://adk.dev/artifacts/#__codelineno-41-32>)                                    System.out.println(
        [](<https://adk.dev/artifacts/#__codelineno-41-33>)                                            "User "
        [](<https://adk.dev/artifacts/#__codelineno-41-34>)                                                    + userId
        [](<https://adk.dev/artifacts/#__codelineno-41-35>)                                                    + " in session "
        [](<https://adk.dev/artifacts/#__codelineno-41-36>)                                                    + sessionId
        [](<https://adk.dev/artifacts/#__codelineno-41-37>)                                                    + " has no saved Java artifacts.");
        [](<https://adk.dev/artifacts/#__codelineno-41-38>)                                } else {
        [](<https://adk.dev/artifacts/#__codelineno-41-39>)                                    StringBuilder fileListStr =
        [](<https://adk.dev/artifacts/#__codelineno-41-40>)                                            new StringBuilder(
        [](<https://adk.dev/artifacts/#__codelineno-41-41>)                                                    "Here are the available Java artifacts for user "
        [](<https://adk.dev/artifacts/#__codelineno-41-42>)                                                            + userId
        [](<https://adk.dev/artifacts/#__codelineno-41-43>)                                                            + " in session "
        [](<https://adk.dev/artifacts/#__codelineno-41-44>)                                                            + sessionId
        [](<https://adk.dev/artifacts/#__codelineno-41-45>)                                                            + ":\n");
        [](<https://adk.dev/artifacts/#__codelineno-41-46>)                                    for (String fname : availableFiles) {
        [](<https://adk.dev/artifacts/#__codelineno-41-47>)                                        fileListStr.append("- ").append(fname).append("\n");
        [](<https://adk.dev/artifacts/#__codelineno-41-48>)                                    }
        [](<https://adk.dev/artifacts/#__codelineno-41-49>)                                    System.out.println(fileListStr.toString());
        [](<https://adk.dev/artifacts/#__codelineno-41-50>)                                }
        [](<https://adk.dev/artifacts/#__codelineno-41-51>)                            }
        [](<https://adk.dev/artifacts/#__codelineno-41-52>)
        [](<https://adk.dev/artifacts/#__codelineno-41-53>)                            @Override
        [](<https://adk.dev/artifacts/#__codelineno-41-54>)                            public void onError(Throwable e) {
        [](<https://adk.dev/artifacts/#__codelineno-41-55>)                                System.err.println(
        [](<https://adk.dev/artifacts/#__codelineno-41-56>)                                        "Error listing Java artifacts for user "
        [](<https://adk.dev/artifacts/#__codelineno-41-57>)                                                + userId
        [](<https://adk.dev/artifacts/#__codelineno-41-58>)                                                + " in session "
        [](<https://adk.dev/artifacts/#__codelineno-41-59>)                                                + sessionId
        [](<https://adk.dev/artifacts/#__codelineno-41-60>)                                                + ": "
        [](<https://adk.dev/artifacts/#__codelineno-41-61>)                                                + e.getMessage());
        [](<https://adk.dev/artifacts/#__codelineno-41-62>)                                // In a real application, you might return an error message to the user/LLM
        [](<https://adk.dev/artifacts/#__codelineno-41-63>)                            }
        [](<https://adk.dev/artifacts/#__codelineno-41-64>)                        });
        [](<https://adk.dev/artifacts/#__codelineno-41-65>)    }
        [](<https://adk.dev/artifacts/#__codelineno-41-66>)
        [](<https://adk.dev/artifacts/#__codelineno-41-67>)    // --- Example Usage Concept (Java) ---
        [](<https://adk.dev/artifacts/#__codelineno-41-68>)    public static void main(String[] args) {
        [](<https://adk.dev/artifacts/#__codelineno-41-69>)        // BaseArtifactService service = new InMemoryArtifactService(); // Or GcsArtifactService
        [](<https://adk.dev/artifacts/#__codelineno-41-70>)        // MyArtifactListerService lister = new MyArtifactListerService(service, "myJavaApp");
        [](<https://adk.dev/artifacts/#__codelineno-41-71>)        // lister.listUserFilesJava("user123", "sessionABC");
        [](<https://adk.dev/artifacts/#__codelineno-41-72>)        // Due to async nature, in a real app, ensure program waits or handles completion.
        [](<https://adk.dev/artifacts/#__codelineno-41-73>)    }
        [](<https://adk.dev/artifacts/#__codelineno-41-74>)}
        
Kotlin
    
    [](<https://adk.dev/artifacts/#__codelineno-42-1>)suspend fun listUserFiles(context: ToolContext): String {
    [](<https://adk.dev/artifacts/#__codelineno-42-2>)    val availableFiles = context.listArtifacts()
    [](<https://adk.dev/artifacts/#__codelineno-42-3>)    if (availableFiles.isEmpty()) {
    [](<https://adk.dev/artifacts/#__codelineno-42-4>)        return "You have no saved artifacts."
    [](<https://adk.dev/artifacts/#__codelineno-42-5>)    } else {
    [](<https://adk.dev/artifacts/#__codelineno-42-6>)        val fileListStr = availableFiles.joinToString("\n") { "- $it" }
    [](<https://adk.dev/artifacts/#__codelineno-42-7>)        return "Here are your available Kotlin artifacts:\n$fileListStr"
    [](<https://adk.dev/artifacts/#__codelineno-42-8>)    }
    [](<https://adk.dev/artifacts/#__codelineno-42-9>)}
    
These methods for saving, loading, and listing provide a convenient and consistent way to manage binary data persistence within ADK, whether using Python's context objects or directly interacting with the `BaseArtifactService` in Java, regardless of the chosen backend storage implementation.

## Available Implementations[¶](<https://adk.dev/artifacts/#available-implementations> "Permanent link")

ADK provides concrete implementations of the `BaseArtifactService` interface, offering different storage backends suitable for various development stages and deployment needs. These implementations handle the details of storing, versioning, and retrieving artifact data based on the `app_name`, `user_id`, `session_id`, and `filename` (including the `user:` namespace prefix).

### InMemoryArtifactService[¶](<https://adk.dev/artifacts/#inmemoryartifactservice> "Permanent link")

  * **Storage Mechanism:**
    * Python: Uses a Python dictionary (`self.artifacts`) held in the application's memory. The dictionary keys represent the artifact path, and the values are lists of `types.Part`, where each list element is a version.
    * Java: Uses nested `HashMap` instances (`private final Map<String, Map<String, Map<String, Map<String, List<Part>>>>> artifacts;`) held in memory. The keys at each level are `appName`, `userId`, `sessionId`, and `filename` respectively. The innermost `List<Part>` stores the versions of the artifact, where the list index corresponds to the version number.
  * **Key Features:**
    * **Simplicity:** Requires no external setup or dependencies beyond the core ADK library.
    * **Speed:** Operations are typically very fast as they involve in-memory map/dictionary lookups and list manipulations.
    * **Ephemeral:** All stored artifacts are **lost** when the application process terminates. Data does not persist between application restarts.
  * **Use Cases:**
    * Ideal for local development and testing where persistence is not required.
    * Suitable for short-lived demonstrations or scenarios where artifact data is purely temporary within a single run of the application.
  * **Instantiation:**

PythonTypescriptGoJavaKotlin
        
        [](<https://adk.dev/artifacts/#__codelineno-43-1>)from google.adk.artifacts import InMemoryArtifactService
        [](<https://adk.dev/artifacts/#__codelineno-43-2>)
        [](<https://adk.dev/artifacts/#__codelineno-43-3>)# Simply instantiate the class
        [](<https://adk.dev/artifacts/#__codelineno-43-4>)in_memory_service_py = InMemoryArtifactService()
        [](<https://adk.dev/artifacts/#__codelineno-43-5>)
        [](<https://adk.dev/artifacts/#__codelineno-43-6>)# Then pass it to the Runner
        [](<https://adk.dev/artifacts/#__codelineno-43-7>)# runner = Runner(..., artifact_service=in_memory_service_py)
        
        [](<https://adk.dev/artifacts/#__codelineno-44-1>)import {InMemoryArtifactService} from '@google/adk';
        [](<https://adk.dev/artifacts/#__codelineno-44-2>)
        [](<https://adk.dev/artifacts/#__codelineno-44-3>)// Simply instantiate the class
        [](<https://adk.dev/artifacts/#__codelineno-44-4>)const inMemoryService = new InMemoryArtifactService();
        [](<https://adk.dev/artifacts/#__codelineno-44-5>)
        [](<https://adk.dev/artifacts/#__codelineno-44-6>)// This instance would then be provided to your Runner.
        [](<https://adk.dev/artifacts/#__codelineno-44-7>)// const runner = new Runner({
        [](<https://adk.dev/artifacts/#__codelineno-44-8>)//   /* other services */,
        [](<https://adk.dev/artifacts/#__codelineno-44-9>)//   artifactService: inMemoryService
        [](<https://adk.dev/artifacts/#__codelineno-44-10>)// });
        
        [](<https://adk.dev/artifacts/#__codelineno-45-1>)import (
        [](<https://adk.dev/artifacts/#__codelineno-45-2>)  "google.golang.org/adk/v2/artifact"
        [](<https://adk.dev/artifacts/#__codelineno-45-3>))
        [](<https://adk.dev/artifacts/#__codelineno-45-4>)
        [](<https://adk.dev/artifacts/#__codelineno-45-5>)// Simply instantiate the service
        [](<https://adk.dev/artifacts/#__codelineno-45-6>)artifactService := artifact.InMemoryService()
        [](<https://adk.dev/artifacts/#__codelineno-45-7>)log.Printf("InMemoryArtifactService (Go) instantiated: %T", artifactService)
        [](<https://adk.dev/artifacts/#__codelineno-45-8>)
        [](<https://adk.dev/artifacts/#__codelineno-45-9>)// Use the service in your runner
        [](<https://adk.dev/artifacts/#__codelineno-45-10>)// r, _ := runner.New(runner.Config{
        [](<https://adk.dev/artifacts/#__codelineno-45-11>)//  Agent:           agent,
        [](<https://adk.dev/artifacts/#__codelineno-45-12>)//  AppName:         "my_app",
        [](<https://adk.dev/artifacts/#__codelineno-45-13>)//  SessionService:  sessionService,
        [](<https://adk.dev/artifacts/#__codelineno-45-14>)//  ArtifactService: artifactService,
        [](<https://adk.dev/artifacts/#__codelineno-45-15>)// })
        
        [](<https://adk.dev/artifacts/#__codelineno-46-1>)import com.google.adk.artifacts.BaseArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-46-2>)import com.google.adk.artifacts.InMemoryArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-46-3>)
        [](<https://adk.dev/artifacts/#__codelineno-46-4>)public class InMemoryServiceSetup {
        [](<https://adk.dev/artifacts/#__codelineno-46-5>)    public static void main(String[] args) {
        [](<https://adk.dev/artifacts/#__codelineno-46-6>)        // Simply instantiate the class
        [](<https://adk.dev/artifacts/#__codelineno-46-7>)        BaseArtifactService inMemoryServiceJava = new InMemoryArtifactService();
        [](<https://adk.dev/artifacts/#__codelineno-46-8>)
        [](<https://adk.dev/artifacts/#__codelineno-46-9>)        System.out.println("InMemoryArtifactService (Java) instantiated: " + inMemoryServiceJava.getClass().getName());
        [](<https://adk.dev/artifacts/#__codelineno-46-10>)
        [](<https://adk.dev/artifacts/#__codelineno-46-11>)        // This instance would then be provided to your Runner.
        [](<https://adk.dev/artifacts/#__codelineno-46-12>)        // Runner runner = new Runner(
        [](<https://adk.dev/artifacts/#__codelineno-46-13>)        //     /* other services */,
        [](<https://adk.dev/artifacts/#__codelineno-46-14>)        //     inMemoryServiceJava
        [](<https://adk.dev/artifacts/#__codelineno-46-15>)        // );
        [](<https://adk.dev/artifacts/#__codelineno-46-16>)    }
        [](<https://adk.dev/artifacts/#__codelineno-46-17>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-47-1>)fun inMemoryServiceExample() {
        [](<https://adk.dev/artifacts/#__codelineno-47-2>)    val inMemoryService = InMemoryArtifactService()
        [](<https://adk.dev/artifacts/#__codelineno-47-3>)}
        
### GcsArtifactService[¶](<https://adk.dev/artifacts/#gcsartifactservice> "Permanent link")

  * **Storage Mechanism:** Leverages Google Cloud Storage (GCS) for persistent artifact storage. Each version of an artifact is stored as a separate object (blob) within a specified GCS bucket.

  * **Object Naming Convention:** It constructs GCS object names (blob names) using a hierarchical path structure.
  * **Key Features:**
    * **Persistence:** Artifacts stored in GCS persist across application restarts and deployments.
    * **Scalability:** Leverages the scalability and durability of Google Cloud Storage.
    * **Versioning:** Explicitly stores each version as a distinct GCS object. The `saveArtifact` method in `GcsArtifactService`.
    * **Permissions Required:** The application environment needs appropriate credentials (e.g., Application Default Credentials) and IAM permissions to read from and write to the specified GCS bucket.
  * **Use Cases:**
    * Production environments requiring persistent artifact storage.
    * Scenarios where artifacts need to be shared across different application instances or services (by accessing the same GCS bucket).
    * Applications needing long-term storage and retrieval of user or session data.
  * **Instantiation:**

PythonTypescriptJavaKotlin
        
        [](<https://adk.dev/artifacts/#__codelineno-48-1>)from google.adk.artifacts import GcsArtifactService
        [](<https://adk.dev/artifacts/#__codelineno-48-2>)
        [](<https://adk.dev/artifacts/#__codelineno-48-3>)# Specify the GCS bucket name
        [](<https://adk.dev/artifacts/#__codelineno-48-4>)gcs_bucket_name_py = "your-gcs-bucket-for-adk-artifacts" # Replace with your bucket name
        [](<https://adk.dev/artifacts/#__codelineno-48-5>)
        [](<https://adk.dev/artifacts/#__codelineno-48-6>)try:
        [](<https://adk.dev/artifacts/#__codelineno-48-7>)    gcs_service_py = GcsArtifactService(bucket_name=gcs_bucket_name_py)
        [](<https://adk.dev/artifacts/#__codelineno-48-8>)    print(f"Python GcsArtifactService initialized for bucket: {gcs_bucket_name_py}")
        [](<https://adk.dev/artifacts/#__codelineno-48-9>)    # Ensure your environment has credentials to access this bucket.
        [](<https://adk.dev/artifacts/#__codelineno-48-10>)    # e.g., via Application Default Credentials (ADC)
        [](<https://adk.dev/artifacts/#__codelineno-48-11>)
        [](<https://adk.dev/artifacts/#__codelineno-48-12>)    # Then pass it to the Runner
        [](<https://adk.dev/artifacts/#__codelineno-48-13>)    # runner = Runner(..., artifact_service=gcs_service_py)
        [](<https://adk.dev/artifacts/#__codelineno-48-14>)
        [](<https://adk.dev/artifacts/#__codelineno-48-15>)except Exception as e:
        [](<https://adk.dev/artifacts/#__codelineno-48-16>)    # Catch potential errors during GCS client initialization (e.g., auth issues)
        [](<https://adk.dev/artifacts/#__codelineno-48-17>)    print(f"Error initializing Python GcsArtifactService: {e}")
        [](<https://adk.dev/artifacts/#__codelineno-48-18>)    # Handle the error appropriately - maybe fall back to InMemory or raise
        
        [](<https://adk.dev/artifacts/#__codelineno-49-1>)import {GcsArtifactService} from '@google/adk';
        [](<https://adk.dev/artifacts/#__codelineno-49-2>)
        [](<https://adk.dev/artifacts/#__codelineno-49-3>)// Specify the GCS bucket name.
        [](<https://adk.dev/artifacts/#__codelineno-49-4>)const gcsBucketName = 'your-gcs-bucket-for-adk-artifacts';
        [](<https://adk.dev/artifacts/#__codelineno-49-5>)
        [](<https://adk.dev/artifacts/#__codelineno-49-6>)try {
        [](<https://adk.dev/artifacts/#__codelineno-49-7>)  const gcsService = new GcsArtifactService(gcsBucketName);
        [](<https://adk.dev/artifacts/#__codelineno-49-8>)  console.log(`TypeScript GcsArtifactService initialized for bucket: ${gcsBucketName}`);
        [](<https://adk.dev/artifacts/#__codelineno-49-9>)  // Ensure your environment has credentials to access this bucket.
        [](<https://adk.dev/artifacts/#__codelineno-49-10>)  // e.g., via Application Default Credentials (ADC).
        [](<https://adk.dev/artifacts/#__codelineno-49-11>)
        [](<https://adk.dev/artifacts/#__codelineno-49-12>)  // Then pass it to the Runner.
        [](<https://adk.dev/artifacts/#__codelineno-49-13>)  // const runner = new Runner({..., artifactService: gcsService});
        [](<https://adk.dev/artifacts/#__codelineno-49-14>)} catch (e: any) {
        [](<https://adk.dev/artifacts/#__codelineno-49-15>)  // Catch potential errors during GCS client initialization (e.g., auth issues).
        [](<https://adk.dev/artifacts/#__codelineno-49-16>)  console.error(`Error initializing TypeScript GcsArtifactService: ${e.message}`);
        [](<https://adk.dev/artifacts/#__codelineno-49-17>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-50-1>)import com.google.adk.artifacts.BaseArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-50-2>)import com.google.adk.artifacts.GcsArtifactService;
        [](<https://adk.dev/artifacts/#__codelineno-50-3>)import com.google.cloud.storage.Storage;
        [](<https://adk.dev/artifacts/#__codelineno-50-4>)import com.google.cloud.storage.StorageOptions;
        [](<https://adk.dev/artifacts/#__codelineno-50-5>)
        [](<https://adk.dev/artifacts/#__codelineno-50-6>)public class GcsServiceSetup {
        [](<https://adk.dev/artifacts/#__codelineno-50-7>)  public static void main(String[] args) {
        [](<https://adk.dev/artifacts/#__codelineno-50-8>)    // Specify the GCS bucket name
        [](<https://adk.dev/artifacts/#__codelineno-50-9>)    String gcsBucketNameJava = "your-gcs-bucket-for-adk-artifacts"; // Replace with your bucket name
        [](<https://adk.dev/artifacts/#__codelineno-50-10>)
        [](<https://adk.dev/artifacts/#__codelineno-50-11>)    try {
        [](<https://adk.dev/artifacts/#__codelineno-50-12>)      // Initialize the GCS Storage client.
        [](<https://adk.dev/artifacts/#__codelineno-50-13>)      // This will use Application Default Credentials by default.
        [](<https://adk.dev/artifacts/#__codelineno-50-14>)      // Ensure the environment is configured correctly (e.g., GOOGLE_APPLICATION_CREDENTIALS).
        [](<https://adk.dev/artifacts/#__codelineno-50-15>)      Storage storageClient = StorageOptions.getDefaultInstance().getService();
        [](<https://adk.dev/artifacts/#__codelineno-50-16>)
        [](<https://adk.dev/artifacts/#__codelineno-50-17>)      // Instantiate the GcsArtifactService
        [](<https://adk.dev/artifacts/#__codelineno-50-18>)      BaseArtifactService gcsServiceJava =
        [](<https://adk.dev/artifacts/#__codelineno-50-19>)          new GcsArtifactService(gcsBucketNameJava, storageClient);
        [](<https://adk.dev/artifacts/#__codelineno-50-20>)
        [](<https://adk.dev/artifacts/#__codelineno-50-21>)      System.out.println(
        [](<https://adk.dev/artifacts/#__codelineno-50-22>)          "Java GcsArtifactService initialized for bucket: " + gcsBucketNameJava);
        [](<https://adk.dev/artifacts/#__codelineno-50-23>)
        [](<https://adk.dev/artifacts/#__codelineno-50-24>)      // This instance would then be provided to your Runner.
        [](<https://adk.dev/artifacts/#__codelineno-50-25>)      // Runner runner = new Runner(
        [](<https://adk.dev/artifacts/#__codelineno-50-26>)      //     /* other services */,
        [](<https://adk.dev/artifacts/#__codelineno-50-27>)      //     gcsServiceJava
        [](<https://adk.dev/artifacts/#__codelineno-50-28>)      // );
        [](<https://adk.dev/artifacts/#__codelineno-50-29>)
        [](<https://adk.dev/artifacts/#__codelineno-50-30>)    } catch (Exception e) {
        [](<https://adk.dev/artifacts/#__codelineno-50-31>)      // Catch potential errors during GCS client initialization (e.g., auth, permissions)
        [](<https://adk.dev/artifacts/#__codelineno-50-32>)      System.err.println("Error initializing Java GcsArtifactService: " + e.getMessage());
        [](<https://adk.dev/artifacts/#__codelineno-50-33>)      e.printStackTrace();
        [](<https://adk.dev/artifacts/#__codelineno-50-34>)      // Handle the error appropriately
        [](<https://adk.dev/artifacts/#__codelineno-50-35>)    }
        [](<https://adk.dev/artifacts/#__codelineno-50-36>)  }
        [](<https://adk.dev/artifacts/#__codelineno-50-37>)}
        
        [](<https://adk.dev/artifacts/#__codelineno-51-1>)fun gcsServiceExample() {
        [](<https://adk.dev/artifacts/#__codelineno-51-2>)    val gcsBucketName = "your-gcs-bucket-for-adk-artifacts"
        [](<https://adk.dev/artifacts/#__codelineno-51-3>)    try {
        [](<https://adk.dev/artifacts/#__codelineno-51-4>)        // Initialize the GCS Storage client (usually uses Application Default Credentials)
        [](<https://adk.dev/artifacts/#__codelineno-51-5>)        val storage = com.google.cloud.storage.StorageOptions.getDefaultInstance().service
        [](<https://adk.dev/artifacts/#__codelineno-51-6>)        val gcsService = GcsArtifactService(bucketName = gcsBucketName, storageClient = storage)
        [](<https://adk.dev/artifacts/#__codelineno-51-7>)        println("Kotlin GcsArtifactService initialized for bucket: $gcsBucketName")
        [](<https://adk.dev/artifacts/#__codelineno-51-8>)    } catch (e: Exception) {
        [](<https://adk.dev/artifacts/#__codelineno-51-9>)        println("Error initializing Kotlin GcsArtifactService: ${e.message}")
        [](<https://adk.dev/artifacts/#__codelineno-51-10>)    }
        [](<https://adk.dev/artifacts/#__codelineno-51-11>)}
        
Choosing the appropriate `ArtifactService` implementation depends on your application's requirements for data persistence, scalability, and operational environment.

## Best Practices[¶](<https://adk.dev/artifacts/#best-practices> "Permanent link")

To use artifacts effectively and maintainably:

  * **Choose the Right Service:** Use `InMemoryArtifactService` for rapid prototyping, testing, and scenarios where persistence isn't needed. Use `GcsArtifactService` (or implement your own `BaseArtifactService` for other backends) for production environments requiring data persistence and scalability.
  * **Meaningful Filenames:** Use clear, descriptive filenames. Including relevant extensions (`.pdf`, `.png`, `.wav`) helps humans understand the content, even though the `mime_type` dictates programmatic handling. Establish conventions for temporary vs. persistent artifact names.
  * **Specify Correct MIME Types:** Always provide an accurate `mime_type` when creating the `types.Part` for `save_artifact`. This is critical for applications or tools that later `load_artifact` to interpret the `bytes` data correctly. Use standard IANA MIME types where possible.
  * **Understand Versioning:** Remember that `load_artifact()` without a specific `version` argument retrieves the _latest_ version. If your logic depends on a specific historical version of an artifact, be sure to provide the integer version number when loading.
  * **Use Namespacing (`user:`) Deliberately:** Only use the `"user:"` prefix for filenames when the data truly belongs to the user and should be accessible across all their sessions. For data specific to a single conversation or session, use regular filenames without the prefix.
  * **Error Handling:**
    * Always check if an `artifact_service` is actually configured before calling context methods (`save_artifact`, `load_artifact`, `list_artifacts`) – they will raise a `ValueError` if the service is `None`.
    * Check the return value of `load_artifact`, as it will be `None` if the artifact or version doesn't exist. Don't assume it always returns a `Part`.
    * Be prepared to handle exceptions from the underlying storage service, especially with `GcsArtifactService` (e.g., `google.api_core.exceptions.Forbidden` for permission issues, `NotFound` if the bucket doesn't exist, network errors).
  * **Size Considerations:** Artifacts are suitable for typical file sizes, but be mindful of potential costs and performance impacts with extremely large files, especially with cloud storage. `InMemoryArtifactService` can consume significant memory if storing many large artifacts. Evaluate if very large data might be better handled through direct GCS links or other specialized storage solutions rather than passing entire byte arrays in-memory.
  * **Cleanup Strategy:** For persistent storage like `GcsArtifactService`, artifacts remain until explicitly deleted. If artifacts represent temporary data or have a limited lifespan, implement a strategy for cleanup. This might involve:
    * Using GCS lifecycle policies on the bucket.
    * Building specific tools or administrative functions that utilize the `artifact_service.delete_artifact` method (note: delete is _not_ exposed via context objects for safety).
    * Carefully managing filenames to allow pattern-based deletion if needed.

Back to top 