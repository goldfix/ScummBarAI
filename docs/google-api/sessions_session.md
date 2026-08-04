# Session: Tracking individual conversations - Agent Development Kit (ADK)

> Source: [https://adk.dev/sessions/session/](https://adk.dev/sessions/session/)

[ Skip to content ](<https://adk.dev/sessions/session/#session-tracking-individual-conversations>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/sessions/session/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/sessions/session/index.md> "View this page as Markdown")

# Session: Tracking individual conversations[¶](<https://adk.dev/sessions/session/#session-tracking-individual-conversations> "Permanent link")

Supported in ADKPython v0.1.0Typescript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

A `Session` represents a single conversation thread between a user and your agent. Just like you wouldn't start every text message from scratch, agents need context regarding the ongoing interaction. The `Session` object in ADK is designed specifically to track and manage these individual conversation threads.

## `Session` objects[¶](<https://adk.dev/sessions/session/#session-objects> "Permanent link")

When a user starts interacting with your agent, the `SessionService` creates a `Session` object (`google.adk.sessions.Session`). This object acts as the container holding everything related to that _one specific chat thread_. Here are its key properties:

  * **Identification (`id`, `appName`, `userId`):** Unique labels for the conversation.
    * `id`: A unique identifier for _this specific_ conversation thread, essential for retrieving it later. A SessionService object can handle multiple `Session`(s). This field identifies which particular session object are we referring to. For example, "test_id_modification".
    * `app_name`: Identifies which agent application this conversation belongs to. For example, "id_modifier_workflow".
    * `userId`: Links the conversation to a particular user.
  * **History (`events`):** A chronological sequence of all interactions (`Event` objects – user messages, agent responses, tool actions) that have occurred within this specific thread.
  * **Session State (`state`):** A place to store temporary data relevant _only_ to this specific, ongoing conversation. This acts as a scratchpad for the agent during the interaction. We will cover how to use and manage `state` in detail in the next section.
  * **Activity Tracking (`lastUpdateTime`):** A timestamp indicating the last time an event occurred in this conversation thread.

### Example: Examining session properties[¶](<https://adk.dev/sessions/session/#example-examining-session-properties> "Permanent link")

The following code example demonstrates how to list various values stored in a session object:

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/session/#__codelineno-0-1>)from google.adk.sessions import InMemorySessionService, Session
    [](<https://adk.dev/sessions/session/#__codelineno-0-2>)
    [](<https://adk.dev/sessions/session/#__codelineno-0-3>)# Create a simple session to examine its properties
    [](<https://adk.dev/sessions/session/#__codelineno-0-4>)temp_service = InMemorySessionService()
    [](<https://adk.dev/sessions/session/#__codelineno-0-5>)example_session = await temp_service.create_session(
    [](<https://adk.dev/sessions/session/#__codelineno-0-6>)    app_name="my_app",
    [](<https://adk.dev/sessions/session/#__codelineno-0-7>)    user_id="example_user",
    [](<https://adk.dev/sessions/session/#__codelineno-0-8>)    state={"initial_key": "initial_value"} # State can be initialized
    [](<https://adk.dev/sessions/session/#__codelineno-0-9>))
    [](<https://adk.dev/sessions/session/#__codelineno-0-10>)
    [](<https://adk.dev/sessions/session/#__codelineno-0-11>)print(f"--- Examining Session Properties ---")
    [](<https://adk.dev/sessions/session/#__codelineno-0-12>)print(f"ID (`id`):                {example_session.id}")
    [](<https://adk.dev/sessions/session/#__codelineno-0-13>)print(f"Application Name (`app_name`): {example_session.app_name}")
    [](<https://adk.dev/sessions/session/#__codelineno-0-14>)print(f"User ID (`user_id`):         {example_session.user_id}")
    [](<https://adk.dev/sessions/session/#__codelineno-0-15>)print(f"State (`state`):           {example_session.state}") # Note: Only shows initial state here
    [](<https://adk.dev/sessions/session/#__codelineno-0-16>)print(f"Events (`events`):         {example_session.events}") # Initially empty
    [](<https://adk.dev/sessions/session/#__codelineno-0-17>)print(f"Last Update (`last_update_time`): {example_session.last_update_time:.2f}")
    [](<https://adk.dev/sessions/session/#__codelineno-0-18>)print(f"---------------------------------")
    [](<https://adk.dev/sessions/session/#__codelineno-0-19>)
    [](<https://adk.dev/sessions/session/#__codelineno-0-20>)# Clean up (optional for this example)
    [](<https://adk.dev/sessions/session/#__codelineno-0-21>)await temp_service.delete_session(app_name=example_session.app_name,
    [](<https://adk.dev/sessions/session/#__codelineno-0-22>)                            user_id=example_session.user_id, session_id=example_session.id)
    [](<https://adk.dev/sessions/session/#__codelineno-0-23>)print("The final status of temp_service - ", temp_service)
    
    [](<https://adk.dev/sessions/session/#__codelineno-1-1>)import { InMemorySessionService } from "@google/adk";
    [](<https://adk.dev/sessions/session/#__codelineno-1-2>)
    [](<https://adk.dev/sessions/session/#__codelineno-1-3>)// Create a simple session to examine its properties
    [](<https://adk.dev/sessions/session/#__codelineno-1-4>)const tempService = new InMemorySessionService();
    [](<https://adk.dev/sessions/session/#__codelineno-1-5>)const exampleSession = await tempService.createSession({
    [](<https://adk.dev/sessions/session/#__codelineno-1-6>)    appName: "my_app",
    [](<https://adk.dev/sessions/session/#__codelineno-1-7>)    userId: "example_user",
    [](<https://adk.dev/sessions/session/#__codelineno-1-8>)    state: {"initial_key": "initial_value"} // State can be initialized
    [](<https://adk.dev/sessions/session/#__codelineno-1-9>)});
    [](<https://adk.dev/sessions/session/#__codelineno-1-10>)
    [](<https://adk.dev/sessions/session/#__codelineno-1-11>)console.log("--- Examining Session Properties ---");
    [](<https://adk.dev/sessions/session/#__codelineno-1-12>)console.log(`ID ('id'):                ${exampleSession.id}`);
    [](<https://adk.dev/sessions/session/#__codelineno-1-13>)console.log(`Application Name ('appName'): ${exampleSession.appName}`);
    [](<https://adk.dev/sessions/session/#__codelineno-1-14>)console.log(`User ID ('userId'):         ${exampleSession.userId}`);
    [](<https://adk.dev/sessions/session/#__codelineno-1-15>)console.log(`State ('state'):           ${JSON.stringify(exampleSession.state)}`); // Note: Only shows initial state here
    [](<https://adk.dev/sessions/session/#__codelineno-1-16>)console.log(`Events ('events'):         ${JSON.stringify(exampleSession.events)}`); // Initially empty
    [](<https://adk.dev/sessions/session/#__codelineno-1-17>)console.log(`Last Update ('lastUpdateTime'): ${exampleSession.lastUpdateTime}`);
    [](<https://adk.dev/sessions/session/#__codelineno-1-18>)console.log("---------------------------------");
    [](<https://adk.dev/sessions/session/#__codelineno-1-19>)
    [](<https://adk.dev/sessions/session/#__codelineno-1-20>)// Clean up (optional for this example)
    [](<https://adk.dev/sessions/session/#__codelineno-1-21>)const finalStatus = await tempService.deleteSession({
    [](<https://adk.dev/sessions/session/#__codelineno-1-22>)    appName: exampleSession.appName,
    [](<https://adk.dev/sessions/session/#__codelineno-1-23>)    userId: exampleSession.userId,
    [](<https://adk.dev/sessions/session/#__codelineno-1-24>)    sessionId: exampleSession.id
    [](<https://adk.dev/sessions/session/#__codelineno-1-25>)});
    [](<https://adk.dev/sessions/session/#__codelineno-1-26>)console.log("The final status of temp_service - ", finalStatus);
    
    [](<https://adk.dev/sessions/session/#__codelineno-2-1>)appName := "my_go_app"
    [](<https://adk.dev/sessions/session/#__codelineno-2-2>)userID := "example_go_user"
    [](<https://adk.dev/sessions/session/#__codelineno-2-3>)initialState := map[string]any{"initial_key": "initial_value"}
    [](<https://adk.dev/sessions/session/#__codelineno-2-4>)
    [](<https://adk.dev/sessions/session/#__codelineno-2-5>)// Create a session to examine its properties.
    [](<https://adk.dev/sessions/session/#__codelineno-2-6>)createResp, err := inMemoryService.Create(ctx, &session.CreateRequest{
    [](<https://adk.dev/sessions/session/#__codelineno-2-7>)    AppName: appName,
    [](<https://adk.dev/sessions/session/#__codelineno-2-8>)    UserID:  userID,
    [](<https://adk.dev/sessions/session/#__codelineno-2-9>)    State:   initialState,
    [](<https://adk.dev/sessions/session/#__codelineno-2-10>)})
    [](<https://adk.dev/sessions/session/#__codelineno-2-11>)if err != nil {
    [](<https://adk.dev/sessions/session/#__codelineno-2-12>)    log.Fatalf("Failed to create session: %v", err)
    [](<https://adk.dev/sessions/session/#__codelineno-2-13>)}
    [](<https://adk.dev/sessions/session/#__codelineno-2-14>)exampleSession := createResp.Session
    [](<https://adk.dev/sessions/session/#__codelineno-2-15>)
    [](<https://adk.dev/sessions/session/#__codelineno-2-16>)fmt.Println("\n--- Examining Session Properties ---")
    [](<https://adk.dev/sessions/session/#__codelineno-2-17>)fmt.Printf("ID (`ID()`): %s\n", exampleSession.ID())
    [](<https://adk.dev/sessions/session/#__codelineno-2-18>)fmt.Printf("Application Name (`AppName()`): %s\n", exampleSession.AppName())
    [](<https://adk.dev/sessions/session/#__codelineno-2-19>)// To access state, you call Get().
    [](<https://adk.dev/sessions/session/#__codelineno-2-20>)val, _ := exampleSession.State().Get("initial_key")
    [](<https://adk.dev/sessions/session/#__codelineno-2-21>)fmt.Printf("State (`State().Get()`):    initial_key = %v\n", val)
    [](<https://adk.dev/sessions/session/#__codelineno-2-22>)
    [](<https://adk.dev/sessions/session/#__codelineno-2-23>)// Events are initially empty.
    [](<https://adk.dev/sessions/session/#__codelineno-2-24>)fmt.Printf("Events (`Events().Len()`):  %d\n", exampleSession.Events().Len())
    [](<https://adk.dev/sessions/session/#__codelineno-2-25>)fmt.Printf("Last Update (`LastUpdateTime()`): %s\n", exampleSession.LastUpdateTime().Format("2006-01-02 15:04:05"))
    [](<https://adk.dev/sessions/session/#__codelineno-2-26>)fmt.Println("---------------------------------")
    [](<https://adk.dev/sessions/session/#__codelineno-2-27>)
    [](<https://adk.dev/sessions/session/#__codelineno-2-28>)// Clean up the session.
    [](<https://adk.dev/sessions/session/#__codelineno-2-29>)err = inMemoryService.Delete(ctx, &session.DeleteRequest{
    [](<https://adk.dev/sessions/session/#__codelineno-2-30>)    AppName:   exampleSession.AppName(),
    [](<https://adk.dev/sessions/session/#__codelineno-2-31>)    UserID:    exampleSession.UserID(),
    [](<https://adk.dev/sessions/session/#__codelineno-2-32>)    SessionID: exampleSession.ID(),
    [](<https://adk.dev/sessions/session/#__codelineno-2-33>)})
    [](<https://adk.dev/sessions/session/#__codelineno-2-34>)if err != nil {
    [](<https://adk.dev/sessions/session/#__codelineno-2-35>)    log.Fatalf("Failed to delete session: %v", err)
    [](<https://adk.dev/sessions/session/#__codelineno-2-36>)}
    [](<https://adk.dev/sessions/session/#__codelineno-2-37>)fmt.Println("Session deleted successfully.")
    
    [](<https://adk.dev/sessions/session/#__codelineno-3-1>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/sessions/session/#__codelineno-3-2>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/sessions/session/#__codelineno-3-3>)import java.util.concurrent.ConcurrentMap;
    [](<https://adk.dev/sessions/session/#__codelineno-3-4>)import java.util.concurrent.ConcurrentHashMap;
    [](<https://adk.dev/sessions/session/#__codelineno-3-5>)
    [](<https://adk.dev/sessions/session/#__codelineno-3-6>)String sessionId = "123";
    [](<https://adk.dev/sessions/session/#__codelineno-3-7>)String appName = "example-app"; // Example app name
    [](<https://adk.dev/sessions/session/#__codelineno-3-8>)String userId = "example-user"; // Example user id
    [](<https://adk.dev/sessions/session/#__codelineno-3-9>)ConcurrentMap<String, Object> initialState = new ConcurrentHashMap<>(Map.of("newKey", "newValue"));
    [](<https://adk.dev/sessions/session/#__codelineno-3-10>)InMemorySessionService exampleSessionService = new InMemorySessionService();
    [](<https://adk.dev/sessions/session/#__codelineno-3-11>)
    [](<https://adk.dev/sessions/session/#__codelineno-3-12>)// Create Session
    [](<https://adk.dev/sessions/session/#__codelineno-3-13>)Session exampleSession = exampleSessionService.createSession(
    [](<https://adk.dev/sessions/session/#__codelineno-3-14>)    appName, userId, initialState, Optional.of(sessionId)).blockingGet();
    [](<https://adk.dev/sessions/session/#__codelineno-3-15>)System.out.println("Session created successfully.");
    [](<https://adk.dev/sessions/session/#__codelineno-3-16>)
    [](<https://adk.dev/sessions/session/#__codelineno-3-17>)System.out.println("--- Examining Session Properties ---");
    [](<https://adk.dev/sessions/session/#__codelineno-3-18>)System.out.printf("ID (`id`): %s%n", exampleSession.id());
    [](<https://adk.dev/sessions/session/#__codelineno-3-19>)System.out.printf("Application Name (`appName`): %s%n", exampleSession.appName());
    [](<https://adk.dev/sessions/session/#__codelineno-3-20>)System.out.printf("User ID (`userId`): %s%n", exampleSession.userId());
    [](<https://adk.dev/sessions/session/#__codelineno-3-21>)System.out.printf("State (`state`): %s%n", exampleSession.state());
    [](<https://adk.dev/sessions/session/#__codelineno-3-22>)System.out.println("------------------------------------");
    [](<https://adk.dev/sessions/session/#__codelineno-3-23>)
    [](<https://adk.dev/sessions/session/#__codelineno-3-24>)
    [](<https://adk.dev/sessions/session/#__codelineno-3-25>)// Clean up (optional for this example)
    [](<https://adk.dev/sessions/session/#__codelineno-3-26>)var unused = exampleSessionService.deleteSession(appName, userId, sessionId);
    
    [](<https://adk.dev/sessions/session/#__codelineno-4-1>)import com.google.adk.kt.sessions.InMemorySessionService
    [](<https://adk.dev/sessions/session/#__codelineno-4-2>)import com.google.adk.kt.sessions.SessionKey
    [](<https://adk.dev/sessions/session/#__codelineno-4-3>)
    [](<https://adk.dev/sessions/session/#__codelineno-4-4>)val sessionId = "123"
    [](<https://adk.dev/sessions/session/#__codelineno-4-5>)val appName = "example-app"
    [](<https://adk.dev/sessions/session/#__codelineno-4-6>)val userId = "example-user"
    [](<https://adk.dev/sessions/session/#__codelineno-4-7>)val initialState = mapOf("newKey" to "newValue")
    [](<https://adk.dev/sessions/session/#__codelineno-4-8>)val sessionService = InMemorySessionService()
    [](<https://adk.dev/sessions/session/#__codelineno-4-9>)
    [](<https://adk.dev/sessions/session/#__codelineno-4-10>)// Create Session
    [](<https://adk.dev/sessions/session/#__codelineno-4-11>)val exampleSession = sessionService.createSession(
    [](<https://adk.dev/sessions/session/#__codelineno-4-12>)    key = SessionKey(appName, userId, sessionId),
    [](<https://adk.dev/sessions/session/#__codelineno-4-13>)    state = initialState
    [](<https://adk.dev/sessions/session/#__codelineno-4-14>))
    [](<https://adk.dev/sessions/session/#__codelineno-4-15>)println("Session created successfully.")
    [](<https://adk.dev/sessions/session/#__codelineno-4-16>)
    [](<https://adk.dev/sessions/session/#__codelineno-4-17>)println("--- Examining Session Properties ---")
    [](<https://adk.dev/sessions/session/#__codelineno-4-18>)println("ID (`id`):                ${exampleSession.key.id}")
    [](<https://adk.dev/sessions/session/#__codelineno-4-19>)println("Application Name (`appName`): ${exampleSession.key.appName}")
    [](<https://adk.dev/sessions/session/#__codelineno-4-20>)println("User ID (`userId`):         ${exampleSession.key.userId}")
    [](<https://adk.dev/sessions/session/#__codelineno-4-21>)println("State (`state`):           ${exampleSession.state}")
    [](<https://adk.dev/sessions/session/#__codelineno-4-22>)println("------------------------------------")
    [](<https://adk.dev/sessions/session/#__codelineno-4-23>)
    [](<https://adk.dev/sessions/session/#__codelineno-4-24>)// Clean up (optional for this example)
    [](<https://adk.dev/sessions/session/#__codelineno-4-25>)sessionService.deleteSession(exampleSession.key)
    
_(__Note:__The state shown above is only the initial state. State updates happen via events, as discussed in the State section.)_

## Session lifecycle[¶](<https://adk.dev/sessions/session/#session-lifecycle> "Permanent link")

![Session lifecycle](https://adk.dev/assets/event-loop.png)

Here’s a simplified flow of how `Session` and `SessionService` work together during a conversation turn:

  1. **Start or Resume:** Your application needs to use the `SessionService` to either `create_session` (for a new chat) or use an existing session id.
  2. **Context Provided:** The `Runner` gets the appropriate `Session` object from the appropriate service method, providing the agent with access to the corresponding Session's `state` and `events`.
  3. **Agent Processing:** The user prompts the agent with a query. The agent analyzes the query and potentially the session `state` and `events` history to determine the response.
  4. **Response & State Update:** The agent generates a response (and potentially flags data to be updated in the `state`). The `Runner` packages this as an `Event`.
  5. **Save Interaction:** The `Runner` calls `sessionService.append_event(session, event)` with the `session` and the new `event` as the arguments. The service adds the `Event` to the history and updates the session's `state` in storage based on information within the event. The session's `last_update_time` also get updated.
  6. **Ready for Next:** The agent's response goes to the user. The updated `Session` is now stored by the `SessionService`, ready for the next turn (which restarts the cycle at step 1, usually with the continuation of the conversation in the current session).
  7. **End Conversation:** When the conversation is over, your application calls `sessionService.delete_session(...)` to clean up the stored session data if it is no longer required.

This cycle highlights how the `SessionService` ensures conversational continuity by managing the history and state associated with each `Session` object.

## Managing sessions with a `SessionService`[¶](<https://adk.dev/sessions/session/#managing-sessions-with-a-sessionservice> "Permanent link")

As seen above, you don't typically create or manage `Session` objects directly. Instead, you use a **`SessionService`**. This service acts as the central manager responsible for the entire lifecycle of your conversation sessions.

Its core responsibilities include:

  * **Starting New Conversations:** Creating fresh `Session` objects when a user begins an interaction.
  * **Resuming Existing Conversations:** Retrieving a specific `Session` (using its ID) so the agent can continue where it left off.
  * **Saving Progress:** Appending new interactions (`Event` objects) to a session's history. This is also the mechanism through which session `state` gets updated (more in the `State` section).
  * **Listing Conversations:** Finding the active session threads for a particular user and application.
  * **Cleaning Up:** Deleting `Session` objects and their associated data when conversations are finished or no longer needed.

## `SessionService` implementations[¶](<https://adk.dev/sessions/session/#sessionservice-implementations> "Permanent link")

ADK provides different `SessionService` implementations, allowing you to choose the storage backend that best suits your needs:

### `InMemorySessionService`[¶](<https://adk.dev/sessions/session/#inmemorysessionservice> "Permanent link")

  * **How it works:** Stores all session data directly in the application's memory.
  * **Persistence:** None. **All conversation data is lost if the application restarts.**
  * **Requires:** Nothing extra.
  * **Best for:** Quick development, local testing, examples, and scenarios where long-term persistence isn't required.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/session/#__codelineno-5-1>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/sessions/session/#__codelineno-5-2>)session_service = InMemorySessionService()
    
    [](<https://adk.dev/sessions/session/#__codelineno-6-1>)import { InMemorySessionService } from "@google/adk";
    [](<https://adk.dev/sessions/session/#__codelineno-6-2>)const sessionService = new InMemorySessionService();
    
    [](<https://adk.dev/sessions/session/#__codelineno-7-1>)import "google.golang.org/adk/v2/session"
    [](<https://adk.dev/sessions/session/#__codelineno-7-2>)inMemoryService := session.InMemoryService()
    
    [](<https://adk.dev/sessions/session/#__codelineno-8-1>)import com.google.adk.sessions.InMemorySessionService;
    [](<https://adk.dev/sessions/session/#__codelineno-8-2>)InMemorySessionService exampleSessionService = new InMemorySessionService();
    
    [](<https://adk.dev/sessions/session/#__codelineno-9-1>)import com.google.adk.kt.sessions.InMemorySessionService
    [](<https://adk.dev/sessions/session/#__codelineno-9-2>)val sessionService = InMemorySessionService()
    
### `VertexAiSessionService`[¶](<https://adk.dev/sessions/session/#vertexaisessionservice> "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0Java v0.1.0

  * **How it works:** Uses Google Cloud Agent Platform infrastructure via API calls for session management.
  * **Persistence:** Yes. Data is managed reliably and scalably via [Agent Runtime](<https://adk.dev/deploy/agent-runtime/>).
  * **Requires:**
    * A Google Cloud project (`pip install vertexai`)
    * A Google Cloud storage bucket that can be configured by this [step](<https://cloud.google.com/vertex-ai/docs/pipelines/configure-project#storage>).
    * An Agent Runtime resource name/ID that can setup following this [tutorial](<https://adk.dev/deploy/agent-runtime/>).
    * If you do not have a Google Cloud project and you want to try the VertexAiSessionService, see [Agent Platform Express Mode](<https://adk.dev/integrations/express-mode/>).
  * **Best for:** Scalable production applications deployed on Google Cloud, especially when integrating with other Agent Platform features.

PythonGoJava
    
    [](<https://adk.dev/sessions/session/#__codelineno-10-1>)# Requires: pip install google-adk[vertexai]
    [](<https://adk.dev/sessions/session/#__codelineno-10-2>)# Plus GCP setup and authentication
    [](<https://adk.dev/sessions/session/#__codelineno-10-3>)from google.adk.sessions import VertexAiSessionService
    [](<https://adk.dev/sessions/session/#__codelineno-10-4>)
    [](<https://adk.dev/sessions/session/#__codelineno-10-5>)PROJECT_ID = "your-gcp-project-id"
    [](<https://adk.dev/sessions/session/#__codelineno-10-6>)LOCATION = "us-central1"
    [](<https://adk.dev/sessions/session/#__codelineno-10-7>)# The app_name used with this service should be the Reasoning Engine ID or name
    [](<https://adk.dev/sessions/session/#__codelineno-10-8>)REASONING_ENGINE_APP_NAME = "projects/your-gcp-project-id/locations/us-central1/reasoningEngines/your-engine-id"
    [](<https://adk.dev/sessions/session/#__codelineno-10-9>)
    [](<https://adk.dev/sessions/session/#__codelineno-10-10>)session_service = VertexAiSessionService(project=PROJECT_ID, location=LOCATION)
    [](<https://adk.dev/sessions/session/#__codelineno-10-11>)# Use REASONING_ENGINE_APP_NAME when calling service methods, e.g.:
    [](<https://adk.dev/sessions/session/#__codelineno-10-12>)# session_service = await session_service.create_session(app_name=REASONING_ENGINE_APP_NAME, ...)
    
    [](<https://adk.dev/sessions/session/#__codelineno-11-1>)import "google.golang.org/adk/v2/session"
    [](<https://adk.dev/sessions/session/#__codelineno-11-2>)
    [](<https://adk.dev/sessions/session/#__codelineno-11-3>)// 2. VertexAIService
    [](<https://adk.dev/sessions/session/#__codelineno-11-4>)// Before running, ensure your environment is authenticated:
    [](<https://adk.dev/sessions/session/#__codelineno-11-5>)// gcloud auth application-default login
    [](<https://adk.dev/sessions/session/#__codelineno-11-6>)// export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    [](<https://adk.dev/sessions/session/#__codelineno-11-7>)// export GOOGLE_CLOUD_LOCATION="your-gcp-location"
    [](<https://adk.dev/sessions/session/#__codelineno-11-8>)
    [](<https://adk.dev/sessions/session/#__codelineno-11-9>)modelName := "gemini-flash-latest" // Replace with your desired model
    [](<https://adk.dev/sessions/session/#__codelineno-11-10>)vertexService, err := session.VertexAIService(ctx, modelName)
    [](<https://adk.dev/sessions/session/#__codelineno-11-11>)if err != nil {
    [](<https://adk.dev/sessions/session/#__codelineno-11-12>)  log.Printf("Could not initialize VertexAIService (this is expected if the gcloud project is not set): %v", err)
    [](<https://adk.dev/sessions/session/#__codelineno-11-13>)} else {
    [](<https://adk.dev/sessions/session/#__codelineno-11-14>)  fmt.Println("Successfully initialized VertexAIService.")
    [](<https://adk.dev/sessions/session/#__codelineno-11-15>)}
    
    [](<https://adk.dev/sessions/session/#__codelineno-12-1>)// Please look at the set of requirements above, consequently export the following in your bashrc file:
    [](<https://adk.dev/sessions/session/#__codelineno-12-2>)// export GOOGLE_CLOUD_PROJECT=my_gcp_project
    [](<https://adk.dev/sessions/session/#__codelineno-12-3>)// export GOOGLE_CLOUD_LOCATION=us-central1
    [](<https://adk.dev/sessions/session/#__codelineno-12-4>)// export GOOGLE_API_KEY=my_api_key
    [](<https://adk.dev/sessions/session/#__codelineno-12-5>)
    [](<https://adk.dev/sessions/session/#__codelineno-12-6>)import com.google.adk.sessions.VertexAiSessionService;
    [](<https://adk.dev/sessions/session/#__codelineno-12-7>)import java.util.UUID;
    [](<https://adk.dev/sessions/session/#__codelineno-12-8>)
    [](<https://adk.dev/sessions/session/#__codelineno-12-9>)String sessionId = UUID.randomUUID().toString();
    [](<https://adk.dev/sessions/session/#__codelineno-12-10>)String reasoningEngineAppName = "123456789";
    [](<https://adk.dev/sessions/session/#__codelineno-12-11>)String userId = "u_123"; // Example user id
    [](<https://adk.dev/sessions/session/#__codelineno-12-12>)ConcurrentMap<String, Object> initialState = new
    [](<https://adk.dev/sessions/session/#__codelineno-12-13>)    ConcurrentHashMap<>(); // No initial state needed for this example
    [](<https://adk.dev/sessions/session/#__codelineno-12-14>)
    [](<https://adk.dev/sessions/session/#__codelineno-12-15>)VertexAiSessionService sessionService = new VertexAiSessionService();
    [](<https://adk.dev/sessions/session/#__codelineno-12-16>)Session mySession =
    [](<https://adk.dev/sessions/session/#__codelineno-12-17>)    sessionService
    [](<https://adk.dev/sessions/session/#__codelineno-12-18>)        .createSession(reasoningEngineAppName, userId, initialState, Optional.of(sessionId))
    [](<https://adk.dev/sessions/session/#__codelineno-12-19>)        .blockingGet();
    
For more information on connecting to Google Cloud from ADK agents, see [Connect to Google Cloud and Agent Platform](<https://adk.dev/get-started/google-cloud/>).

### `DatabaseSessionService`[¶](<https://adk.dev/sessions/session/#databasesessionservice> "Permanent link")

Supported in ADKPython v0.1.0Go v0.1.0

  * **How it works:** Connects to a relational database (e.g., PostgreSQL, MySQL, SQLite) to store session data persistently in tables.
  * **Persistence:** Yes. Data survives application restarts.
  * **Requires:** A configured database.
  * **Best for:** Applications needing reliable, persistent storage that you manage yourself.

    [](<https://adk.dev/sessions/session/#__codelineno-13-1>)from google.adk.sessions import DatabaseSessionService
    [](<https://adk.dev/sessions/session/#__codelineno-13-2>)# Example using a local SQLite file:
    [](<https://adk.dev/sessions/session/#__codelineno-13-3>)# Note: The implementation requires an async database driver.
    [](<https://adk.dev/sessions/session/#__codelineno-13-4>)# For SQLite, use 'sqlite+aiosqlite' instead of 'sqlite' to ensure async compatibility.
    [](<https://adk.dev/sessions/session/#__codelineno-13-5>)db_url = "sqlite+aiosqlite:///./my_agent_data.db"
    [](<https://adk.dev/sessions/session/#__codelineno-13-6>)session_service = DatabaseSessionService(db_url=db_url)
    
#### Concurrency and locking[¶](<https://adk.dev/sessions/session/#concurrency-and-locking> "Permanent link")

The `DatabaseSessionService` ensures data integrity during concurrent operations through a two-tiered locking architecture:

  * **In-Process locking:** The service uses an internal, in-process lock to serialize `append_event` calls for the same session. This prevents race conditions when multiple requests try to update the same session simultaneously within the same process.
  * **Row-Level locking:** For PostgreSQL, MySQL, and MariaDB, the service uses row-level locking (via `SELECT ... FOR UPDATE`) to prevent race conditions when multiple processes or replicas try to update the same session simultaneously.

Async driver requirement

`DatabaseSessionService` requires an async database driver. When using SQLite, you must use `sqlite+aiosqlite` instead of `sqlite` in your connection string. For other databases (PostgreSQL, MySQL), ensure you're using an async-compatible driver, such as `asyncpg` for PostgreSQL, `aiomysql` for MySQL.

Session database schema change in ADK Python v1.22.0

The schema for the session database changed in ADK Python v1.22.0, which requires migration of the Session Database. For more information, see [Session database schema migration](<https://adk.dev/sessions/session/migrate/>).

## Troubleshoot session errors[¶](<https://adk.dev/sessions/session/#troubleshoot-session-errors> "Permanent link")

During execution, ADK can raise specific exceptions to help you identify configuration or state issues.

### `SessionNotFoundError`[¶](<https://adk.dev/sessions/session/#sessionnotfounderror> "Permanent link")

Raised when a runner attempts to access or execute a session that does not exist in the active session store. Inherits from `ValueError` for backward compatibility.

  * **Common causes:** an invalid, expired, or missing `session_id`; running a session before it has been created.
  * **How to resolve:** ensure the session exists first via `create_session(...)`, or construct the `Runner` with `auto_create_session=True`.

Back to top 