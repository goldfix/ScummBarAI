# Memory - Agent Development Kit (ADK)

> Source: [https://adk.dev/sessions/memory/](https://adk.dev/sessions/memory/)

[ Skip to content ](<https://adk.dev/sessions/memory/#memory-long-term-knowledge-with-memoryservice>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/sessions/memory.md> "Edit this page on GitHub") [ ](<https://adk.dev/sessions/memory/index.md> "View this page as Markdown")

# Memory: Long-term knowledge with `MemoryService`[¶](<https://adk.dev/sessions/memory/#memory-long-term-knowledge-with-memoryservice> "Permanent link")

Supported in ADKPython v0.1.0TypeScript v0.2.0Go v0.1.0Java v0.1.0Kotlin v0.1.0

While a `Session` tracks the history (`events`) and temporary data (`state`) of a single conversation, an agent may need to recall information from past interactions. This is where the concept of **Long-Term Knowledge** and the **`MemoryService`** come into play. Think of it this way:

  * **`Session` / `State`:** It's your short-term memory during one specific chat.
  * **Long-Term Knowledge (`MemoryService`)**: It's a searchable archive or knowledge library the agent can consult, potentially containing information from many past chats or other sources.

## The `MemoryService` role[¶](<https://adk.dev/sessions/memory/#the-memoryservice-role> "Permanent link")

The `BaseMemoryService` (or `Service` in Go) defines the interface for managing this searchable, long-term knowledge store. It supports these operations:

  * **Ingesting Information:**
    * **`add_session_to_memory`** : Takes a completed `Session` and adds relevant information to the long-term knowledge store. This approach is ideal for automatically capturing the essence of a conversation.
    * **`add_events_to_memory`** : Appends a delta of events (for example, the latest turn) without re-ingesting the full session. Useful when you want to write to memory partway through a long-running session.
    * **`add_memory`** : Adds explicit `MemoryEntry` objects directly to the memory. This method gives you fine-grained control and is useful for injecting specific facts from other sources.
  * **Searching Information (`search_memory`):** Lets an agent (typically via a `Tool`) query the knowledge store and retrieve relevant snippets or context based on a search query.

`add_events_to_memory` and `add_memory` are optional and are not implemented by every service, so confirm that your chosen service supports them before relying on them.

## Choose the right memory service[¶](<https://adk.dev/sessions/memory/#choose-the-right-memory-service> "Permanent link")

The Python ADK ships three `MemoryService` implementations. Use the table below to decide which is the best fit for your agent.

**Feature** | **InMemoryMemoryService** | **VertexAiMemoryBankService** | **VertexAiRagMemoryService**  
---|---|---|---  
**Persistence** | None, data is lost on restart | Yes, managed by the Agent Platform | Yes, stored in Knowledge Engine  
**Primary Use Case** | Prototyping, local development, and simple testing. | Building meaningful, evolving memories from user conversations. | Vector-search retrieval over the full conversation corpus, or alongside other RAG-indexed content.  
**Memory Extraction** | Stores full conversation | Extracts [meaningful information](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/generate-memories>) from conversations and consolidates it with existing memories powered by LLM | Stores full conversation, indexed by [Knowledge Engine](<https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview>).  
**Search Capability** | Basic keyword matching. | Advanced semantic search. | Vector similarity search over Knowledge Engine.  
**Setup Complexity** | None. It's the default. | Low. Requires an [Agent Runtime](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview>) instance on Agent Platform. | Medium. Requires [Knowledge Engine](<https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/manage-your-rag-corpus>).  
**Dependencies** | None. | Google Cloud Project, Agent Platform API | Google Cloud Project, Knowledge Engine, the Agent Platform SDK (optional install).  
**When to use it** | When you want to search across multiple sessions’ chat histories for prototyping. | When you want your agent to remember and learn from past interactions. | When you already have RAG infrastructure or want to retrieve over raw conversation transcripts.  
  
`VertexAiRagMemoryService` is only exported from `google.adk.memory` when the Agent Platform SDK is installed. Memory Bank and RAG-backed memory are documented in [Memory Bank](<https://adk.dev/sessions/memory/#memory-bank>) and [RAG Memory](<https://adk.dev/sessions/memory/#rag-memory>) below.

## `InMemoryMemoryService`[¶](<https://adk.dev/sessions/memory/#inmemorymemoryservice> "Permanent link")

The `InMemoryMemoryService` stores session information in the application's memory and performs basic keyword matching for searches. It requires no setup and is best for prototyping and simple testing scenarios where persistence isn't required.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/memory/#__codelineno-0-1>)from google.adk.memory import InMemoryMemoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-0-2>)memory_service = InMemoryMemoryService()
    
    [](<https://adk.dev/sessions/memory/#__codelineno-1-1>)import { InMemoryMemoryService } from '@google/adk';
    [](<https://adk.dev/sessions/memory/#__codelineno-1-2>)const memoryService = new InMemoryMemoryService();
    
    [](<https://adk.dev/sessions/memory/#__codelineno-2-1>)import (
    [](<https://adk.dev/sessions/memory/#__codelineno-2-2>)  "google.golang.org/adk/v2/memory"
    [](<https://adk.dev/sessions/memory/#__codelineno-2-3>)  "google.golang.org/adk/v2/session"
    [](<https://adk.dev/sessions/memory/#__codelineno-2-4>))
    [](<https://adk.dev/sessions/memory/#__codelineno-2-5>)
    [](<https://adk.dev/sessions/memory/#__codelineno-2-6>)// Services must be shared across runners to share state and memory.
    [](<https://adk.dev/sessions/memory/#__codelineno-2-7>)sessionService := session.InMemoryService()
    [](<https://adk.dev/sessions/memory/#__codelineno-2-8>)memoryService := memory.InMemoryService()
    
    [](<https://adk.dev/sessions/memory/#__codelineno-3-1>)import com.google.adk.memory.InMemoryMemoryService;
    [](<https://adk.dev/sessions/memory/#__codelineno-3-2>)
    [](<https://adk.dev/sessions/memory/#__codelineno-3-3>)InMemoryMemoryService memoryService = new InMemoryMemoryService();
    
    [](<https://adk.dev/sessions/memory/#__codelineno-4-1>)fun instantiateMemoryService() {
    [](<https://adk.dev/sessions/memory/#__codelineno-4-2>)    val memoryService = InMemoryMemoryService()
    [](<https://adk.dev/sessions/memory/#__codelineno-4-3>)}
    
**Example: Add and search memory**

This example demonstrates the basic flow using the `InMemoryMemoryService` for simplicity.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/memory/#__codelineno-5-1>)import asyncio
    [](<https://adk.dev/sessions/memory/#__codelineno-5-2>)from google.adk.agents import LlmAgent
    [](<https://adk.dev/sessions/memory/#__codelineno-5-3>)from google.adk.sessions import InMemorySessionService, Session
    [](<https://adk.dev/sessions/memory/#__codelineno-5-4>)from google.adk.memory import InMemoryMemoryService # Import MemoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-5-5>)from google.adk.runners import Runner
    [](<https://adk.dev/sessions/memory/#__codelineno-5-6>)from google.adk.tools import load_memory # Tool to query memory
    [](<https://adk.dev/sessions/memory/#__codelineno-5-7>)from google.genai.types import Content, Part
    [](<https://adk.dev/sessions/memory/#__codelineno-5-8>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-9>)# --- Constants ---
    [](<https://adk.dev/sessions/memory/#__codelineno-5-10>)APP_NAME = "memory_example_app"
    [](<https://adk.dev/sessions/memory/#__codelineno-5-11>)USER_ID = "mem_user"
    [](<https://adk.dev/sessions/memory/#__codelineno-5-12>)MODEL = "gemini-flash-latest" # Use a valid model
    [](<https://adk.dev/sessions/memory/#__codelineno-5-13>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-14>)# --- Agent Definitions ---
    [](<https://adk.dev/sessions/memory/#__codelineno-5-15>)# Agent 1: Simple agent to capture information
    [](<https://adk.dev/sessions/memory/#__codelineno-5-16>)info_capture_agent = LlmAgent(
    [](<https://adk.dev/sessions/memory/#__codelineno-5-17>)    model=MODEL,
    [](<https://adk.dev/sessions/memory/#__codelineno-5-18>)    name="InfoCaptureAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-5-19>)    instruction="Acknowledge the user's statement.",
    [](<https://adk.dev/sessions/memory/#__codelineno-5-20>))
    [](<https://adk.dev/sessions/memory/#__codelineno-5-21>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-22>)# Agent 2: Agent that can use memory
    [](<https://adk.dev/sessions/memory/#__codelineno-5-23>)memory_recall_agent = LlmAgent(
    [](<https://adk.dev/sessions/memory/#__codelineno-5-24>)    model=MODEL,
    [](<https://adk.dev/sessions/memory/#__codelineno-5-25>)    name="MemoryRecallAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-5-26>)    instruction="Answer the user's question. Use the 'load_memory' tool "
    [](<https://adk.dev/sessions/memory/#__codelineno-5-27>)                "if the answer might be in past conversations.",
    [](<https://adk.dev/sessions/memory/#__codelineno-5-28>)    tools=[load_memory] # Give the agent the tool
    [](<https://adk.dev/sessions/memory/#__codelineno-5-29>))
    [](<https://adk.dev/sessions/memory/#__codelineno-5-30>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-31>)# --- Services ---
    [](<https://adk.dev/sessions/memory/#__codelineno-5-32>)# Services must be shared across runners to share state and memory
    [](<https://adk.dev/sessions/memory/#__codelineno-5-33>)session_service = InMemorySessionService()
    [](<https://adk.dev/sessions/memory/#__codelineno-5-34>)memory_service = InMemoryMemoryService() # Use in-memory for demo
    [](<https://adk.dev/sessions/memory/#__codelineno-5-35>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-36>)async def run_scenario():
    [](<https://adk.dev/sessions/memory/#__codelineno-5-37>)    # --- Scenario ---
    [](<https://adk.dev/sessions/memory/#__codelineno-5-38>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-39>)    # Turn 1: Capture some information in a session
    [](<https://adk.dev/sessions/memory/#__codelineno-5-40>)    print("--- Turn 1: Capturing Information ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-41>)    runner1 = Runner(
    [](<https://adk.dev/sessions/memory/#__codelineno-5-42>)        # Start with the info capture agent
    [](<https://adk.dev/sessions/memory/#__codelineno-5-43>)        agent=info_capture_agent,
    [](<https://adk.dev/sessions/memory/#__codelineno-5-44>)        app_name=APP_NAME,
    [](<https://adk.dev/sessions/memory/#__codelineno-5-45>)        session_service=session_service,
    [](<https://adk.dev/sessions/memory/#__codelineno-5-46>)        memory_service=memory_service # Provide the memory service to the Runner
    [](<https://adk.dev/sessions/memory/#__codelineno-5-47>)    )
    [](<https://adk.dev/sessions/memory/#__codelineno-5-48>)    session1_id = "session_info"
    [](<https://adk.dev/sessions/memory/#__codelineno-5-49>)    await runner1.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session1_id)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-50>)    user_input1 = Content(parts=[Part(text="My favorite project is Project Alpha.")], role="user")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-51>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-52>)    # Run the agent
    [](<https://adk.dev/sessions/memory/#__codelineno-5-53>)    final_response_text = "(No final response)"
    [](<https://adk.dev/sessions/memory/#__codelineno-5-54>)    async for event in runner1.run_async(user_id=USER_ID, session_id=session1_id, new_message=user_input1):
    [](<https://adk.dev/sessions/memory/#__codelineno-5-55>)        if event.is_final_response() and event.content and event.content.parts:
    [](<https://adk.dev/sessions/memory/#__codelineno-5-56>)            final_response_text = event.content.parts[0].text
    [](<https://adk.dev/sessions/memory/#__codelineno-5-57>)    print(f"Agent 1 Response: {final_response_text}")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-58>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-59>)    # Get the completed session
    [](<https://adk.dev/sessions/memory/#__codelineno-5-60>)    completed_session1 = await runner1.session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session1_id)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-61>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-62>)    # Add this session's content to the Memory Service
    [](<https://adk.dev/sessions/memory/#__codelineno-5-63>)    print("\n--- Adding Session 1 to Memory ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-64>)    await memory_service.add_session_to_memory(completed_session1)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-65>)    print("Session added to memory.")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-66>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-67>)    # Turn 2: Recall the information in a new session
    [](<https://adk.dev/sessions/memory/#__codelineno-5-68>)    print("\n--- Turn 2: Recalling Information ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-69>)    runner2 = Runner(
    [](<https://adk.dev/sessions/memory/#__codelineno-5-70>)        # Use the second agent, which has the memory tool
    [](<https://adk.dev/sessions/memory/#__codelineno-5-71>)        agent=memory_recall_agent,
    [](<https://adk.dev/sessions/memory/#__codelineno-5-72>)        app_name=APP_NAME,
    [](<https://adk.dev/sessions/memory/#__codelineno-5-73>)        session_service=session_service, # Reuse the same service
    [](<https://adk.dev/sessions/memory/#__codelineno-5-74>)        memory_service=memory_service   # Reuse the same service
    [](<https://adk.dev/sessions/memory/#__codelineno-5-75>)    )
    [](<https://adk.dev/sessions/memory/#__codelineno-5-76>)    session2_id = "session_recall"
    [](<https://adk.dev/sessions/memory/#__codelineno-5-77>)    await runner2.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session2_id)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-78>)    user_input2 = Content(parts=[Part(text="What is my favorite project?")], role="user")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-79>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-80>)    # Run the second agent
    [](<https://adk.dev/sessions/memory/#__codelineno-5-81>)    final_response_text_2 = "(No final response)"
    [](<https://adk.dev/sessions/memory/#__codelineno-5-82>)    async for event in runner2.run_async(user_id=USER_ID, session_id=session2_id, new_message=user_input2):
    [](<https://adk.dev/sessions/memory/#__codelineno-5-83>)        if event.is_final_response() and event.content and event.content.parts:
    [](<https://adk.dev/sessions/memory/#__codelineno-5-84>)            final_response_text_2 = event.content.parts[0].text
    [](<https://adk.dev/sessions/memory/#__codelineno-5-85>)    print(f"Agent 2 Response: {final_response_text_2}")
    [](<https://adk.dev/sessions/memory/#__codelineno-5-86>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-87>)# To run this example, you can use the following snippet:
    [](<https://adk.dev/sessions/memory/#__codelineno-5-88>)# asyncio.run(run_scenario())
    [](<https://adk.dev/sessions/memory/#__codelineno-5-89>)
    [](<https://adk.dev/sessions/memory/#__codelineno-5-90>)# await run_scenario()
    
    [](<https://adk.dev/sessions/memory/#__codelineno-6-1>)import {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-2>)    InMemoryMemoryService,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-3>)    InMemorySessionService,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-4>)    LOAD_MEMORY,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-5>)    LlmAgent,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-6>)    Runner
    [](<https://adk.dev/sessions/memory/#__codelineno-6-7>)} from '@google/adk';
    [](<https://adk.dev/sessions/memory/#__codelineno-6-8>)import { createUserContent } from '@google/genai';
    [](<https://adk.dev/sessions/memory/#__codelineno-6-9>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-10>)// --- Constants ---
    [](<https://adk.dev/sessions/memory/#__codelineno-6-11>)const APP_NAME = "memory_example_app";
    [](<https://adk.dev/sessions/memory/#__codelineno-6-12>)const USER_ID = "mem_user";
    [](<https://adk.dev/sessions/memory/#__codelineno-6-13>)const MODEL = "gemini-2.5-flash";
    [](<https://adk.dev/sessions/memory/#__codelineno-6-14>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-15>)// --- Agent Definitions ---
    [](<https://adk.dev/sessions/memory/#__codelineno-6-16>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-17>)// Agent 1: Simple agent to capture information
    [](<https://adk.dev/sessions/memory/#__codelineno-6-18>)const infoCaptureAgent = new LlmAgent({
    [](<https://adk.dev/sessions/memory/#__codelineno-6-19>)    model: MODEL,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-20>)    name: "InfoCaptureAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-6-21>)    instruction: "Acknowledge the user's statement concisely.",
    [](<https://adk.dev/sessions/memory/#__codelineno-6-22>)});
    [](<https://adk.dev/sessions/memory/#__codelineno-6-23>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-24>)// Agent 2: Agent that can use memory
    [](<https://adk.dev/sessions/memory/#__codelineno-6-25>)const memoryRecallAgent = new LlmAgent({
    [](<https://adk.dev/sessions/memory/#__codelineno-6-26>)    model: MODEL,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-27>)    name: "MemoryRecallAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-6-28>)    instruction: "Answer the user's question. Use the 'load_memory' tool if the answer might be in past conversations.",
    [](<https://adk.dev/sessions/memory/#__codelineno-6-29>)    tools: [LOAD_MEMORY]
    [](<https://adk.dev/sessions/memory/#__codelineno-6-30>)});
    [](<https://adk.dev/sessions/memory/#__codelineno-6-31>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-32>)// Export for 'adk run' compatibility (to avoid 'No BaseAgent found' error)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-33>)export const root_agent = memoryRecallAgent;
    [](<https://adk.dev/sessions/memory/#__codelineno-6-34>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-35>)// --- Services ---
    [](<https://adk.dev/sessions/memory/#__codelineno-6-36>)const sessionService = new InMemorySessionService();
    [](<https://adk.dev/sessions/memory/#__codelineno-6-37>)const memoryService = new InMemoryMemoryService();
    [](<https://adk.dev/sessions/memory/#__codelineno-6-38>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-39>)async function runScenario() {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-40>)    // --- Turn 1: Capture some information in a session ---
    [](<https://adk.dev/sessions/memory/#__codelineno-6-41>)    console.log("--- Turn 1: Capturing Information ---");
    [](<https://adk.dev/sessions/memory/#__codelineno-6-42>)    const runner1 = new Runner({
    [](<https://adk.dev/sessions/memory/#__codelineno-6-43>)        agent: infoCaptureAgent,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-44>)        appName: APP_NAME,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-45>)        sessionService,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-46>)        memoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-6-47>)    });
    [](<https://adk.dev/sessions/memory/#__codelineno-6-48>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-49>)    const session1Id = "session_info";
    [](<https://adk.dev/sessions/memory/#__codelineno-6-50>)    await sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: session1Id });
    [](<https://adk.dev/sessions/memory/#__codelineno-6-51>)    const userInput1 = createUserContent("My favorite project is Project Alpha.");
    [](<https://adk.dev/sessions/memory/#__codelineno-6-52>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-53>)    let finalResponseText = "(No final response)";
    [](<https://adk.dev/sessions/memory/#__codelineno-6-54>)    for await (const event of runner1.runAsync({ userId: USER_ID, sessionId: session1Id, newMessage: userInput1 })) {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-55>)        // Capture any text response from the agent
    [](<https://adk.dev/sessions/memory/#__codelineno-6-56>)        if (event.author === infoCaptureAgent.name && event.content?.parts) {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-57>)            const text = event.content.parts.map(p => p.text || "").join("").trim();
    [](<https://adk.dev/sessions/memory/#__codelineno-6-58>)            if (text) finalResponseText = text;
    [](<https://adk.dev/sessions/memory/#__codelineno-6-59>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-6-60>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-6-61>)    console.log(`Agent 1 Response: ${finalResponseText}`);
    [](<https://adk.dev/sessions/memory/#__codelineno-6-62>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-63>)    // Get the completed session and add to Memory
    [](<https://adk.dev/sessions/memory/#__codelineno-6-64>)    const completedSession1 = await sessionService.getSession({ appName: APP_NAME, userId: USER_ID, sessionId: session1Id });
    [](<https://adk.dev/sessions/memory/#__codelineno-6-65>)    console.log("\n--- Adding Session 1 to Memory ---");
    [](<https://adk.dev/sessions/memory/#__codelineno-6-66>)    if (completedSession1) {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-67>)        await memoryService.addSessionToMemory(completedSession1);
    [](<https://adk.dev/sessions/memory/#__codelineno-6-68>)        console.log("Session added to memory.");
    [](<https://adk.dev/sessions/memory/#__codelineno-6-69>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-6-70>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-71>)    // --- Turn 2: Recall the information in a new session ---
    [](<https://adk.dev/sessions/memory/#__codelineno-6-72>)    console.log("\n--- Turn 2: Recalling Information ---");
    [](<https://adk.dev/sessions/memory/#__codelineno-6-73>)    const runner2 = new Runner({
    [](<https://adk.dev/sessions/memory/#__codelineno-6-74>)        agent: memoryRecallAgent,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-75>)        appName: APP_NAME,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-76>)        sessionService,
    [](<https://adk.dev/sessions/memory/#__codelineno-6-77>)        memoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-6-78>)    });
    [](<https://adk.dev/sessions/memory/#__codelineno-6-79>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-80>)    const session2Id = "session_recall";
    [](<https://adk.dev/sessions/memory/#__codelineno-6-81>)    await sessionService.createSession({ appName: APP_NAME, userId: USER_ID, sessionId: session2Id });
    [](<https://adk.dev/sessions/memory/#__codelineno-6-82>)    const userInput2 = createUserContent("What is my favorite project?");
    [](<https://adk.dev/sessions/memory/#__codelineno-6-83>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-84>)    let finalResponseText2 = "(No final response)";
    [](<https://adk.dev/sessions/memory/#__codelineno-6-85>)    for await (const event of runner2.runAsync({ userId: USER_ID, sessionId: session2Id, newMessage: userInput2 })) {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-86>)        // Capture any text response from the agent
    [](<https://adk.dev/sessions/memory/#__codelineno-6-87>)        if (event.author === memoryRecallAgent.name && event.content?.parts) {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-88>)            const text = event.content.parts.map(p => p.text || "").join("").trim();
    [](<https://adk.dev/sessions/memory/#__codelineno-6-89>)            if (text) finalResponseText2 = text;
    [](<https://adk.dev/sessions/memory/#__codelineno-6-90>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-6-91>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-6-92>)    console.log(`Agent 2 Response: ${finalResponseText2}`);
    [](<https://adk.dev/sessions/memory/#__codelineno-6-93>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-94>)    // Exit immediately to prevent the ADK CLI from starting an interactive loop
    [](<https://adk.dev/sessions/memory/#__codelineno-6-95>)    process.exit(0);
    [](<https://adk.dev/sessions/memory/#__codelineno-6-96>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-6-97>)
    [](<https://adk.dev/sessions/memory/#__codelineno-6-98>)// Execute the scenario
    [](<https://adk.dev/sessions/memory/#__codelineno-6-99>)runScenario().catch(err => {
    [](<https://adk.dev/sessions/memory/#__codelineno-6-100>)    console.error(err);
    [](<https://adk.dev/sessions/memory/#__codelineno-6-101>)    process.exit(1);
    [](<https://adk.dev/sessions/memory/#__codelineno-6-102>)});
    
    [](<https://adk.dev/sessions/memory/#__codelineno-7-1>)import (
    [](<https://adk.dev/sessions/memory/#__codelineno-7-2>)    "context"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-3>)    "fmt"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-4>)    "log"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-5>)    "strings"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-6>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-7>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-8>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-9>)    "google.golang.org/adk/v2/memory"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-10>)    "google.golang.org/adk/v2/model/gemini"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-11>)    "google.golang.org/adk/v2/runner"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-12>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-13>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-14>)    "google.golang.org/adk/v2/tool/functiontool"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-15>)    "google.golang.org/genai"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-16>))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-17>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-18>)const (
    [](<https://adk.dev/sessions/memory/#__codelineno-7-19>)    appName = "go_memory_example_app"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-20>)    userID  = "go_mem_user"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-21>)    modelID = "gemini-2.5-flash"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-22>))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-23>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-24>)// Args defines the input structure for the memory search tool.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-25>)type Args struct {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-26>)    Query string `json:"query" jsonschema:"The query to search for in the memory."`
    [](<https://adk.dev/sessions/memory/#__codelineno-7-27>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-7-28>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-29>)// Result defines the output structure for the memory search tool.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-30>)type Result struct {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-31>)    Results []string `json:"results"`
    [](<https://adk.dev/sessions/memory/#__codelineno-7-32>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-7-33>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-34>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-35>)// memorySearchToolFunc is the implementation of the memory search tool.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-36>)// This function demonstrates accessing memory via agent.Context.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-37>)func memorySearchToolFunc(tctx agent.Context, args Args) (Result, error) {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-38>)    fmt.Printf("Tool: Searching memory for query: '%s'\n", args.Query)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-39>)    // The SearchMemory function is available on the context.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-40>)    searchResults, err := tctx.SearchMemory(context.Background(), args.Query)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-41>)    if err != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-42>)        log.Printf("Error searching memory: %v", err)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-43>)        return Result{}, fmt.Errorf("failed memory search")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-44>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-45>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-46>)    var results []string
    [](<https://adk.dev/sessions/memory/#__codelineno-7-47>)    for _, res := range searchResults.Memories {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-48>)        if res.Content != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-49>)            results = append(results, textParts(res.Content)...)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-50>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-51>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-52>)    return Result{Results: results}, nil
    [](<https://adk.dev/sessions/memory/#__codelineno-7-53>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-7-54>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-55>)// Define a tool that can search memory.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-56>)var memorySearchTool = must(functiontool.New(
    [](<https://adk.dev/sessions/memory/#__codelineno-7-57>)    functiontool.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-7-58>)        Name:        "search_past_conversations",
    [](<https://adk.dev/sessions/memory/#__codelineno-7-59>)        Description: "Searches past conversations for relevant information.",
    [](<https://adk.dev/sessions/memory/#__codelineno-7-60>)    },
    [](<https://adk.dev/sessions/memory/#__codelineno-7-61>)    memorySearchToolFunc,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-62>)))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-63>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-64>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-65>)// This example demonstrates how to use the MemoryService in the Go ADK.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-66>)// It covers two main scenarios:
    [](<https://adk.dev/sessions/memory/#__codelineno-7-67>)// 1. Adding a completed session to memory and recalling it in a new session.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-68>)// 2. Searching memory from within a custom tool using the agent.Context.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-69>)func main() {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-70>)    ctx := context.Background()
    [](<https://adk.dev/sessions/memory/#__codelineno-7-71>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-72>)    // --- Services ---
    [](<https://adk.dev/sessions/memory/#__codelineno-7-73>)    // Services must be shared across runners to share state and memory.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-74>)    sessionService := session.InMemoryService()
    [](<https://adk.dev/sessions/memory/#__codelineno-7-75>)    memoryService := memory.InMemoryService() // Use in-memory for this demo.
    [](<https://adk.dev/sessions/memory/#__codelineno-7-76>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-77>)    // --- Scenario 1: Capture information in one session ---
    [](<https://adk.dev/sessions/memory/#__codelineno-7-78>)    fmt.Println("--- Turn 1: Capturing Information ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-79>)    infoCaptureAgent := must(llmagent.New(llmagent.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-7-80>)        Name:        "InfoCaptureAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-7-81>)        Model:       must(gemini.NewModel(ctx, modelID, nil)),
    [](<https://adk.dev/sessions/memory/#__codelineno-7-82>)        Instruction: "Acknowledge the user's statement.",
    [](<https://adk.dev/sessions/memory/#__codelineno-7-83>)    }))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-84>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-85>)    runner1 := must(runner.New(runner.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-7-86>)        AppName:        appName,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-87>)        Agent:          infoCaptureAgent,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-88>)        SessionService: sessionService,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-89>)        MemoryService:  memoryService, // Provide the memory service to the Runner
    [](<https://adk.dev/sessions/memory/#__codelineno-7-90>)    }))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-91>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-92>)    session1ID := "session_info"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-93>)    must(sessionService.Create(ctx, &session.CreateRequest{AppName: appName, UserID: userID, SessionID: session1ID}))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-94>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-95>)    userInput1 := genai.NewContentFromText("My favorite project is Project Alpha.", "user")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-96>)    var finalResponseText string
    [](<https://adk.dev/sessions/memory/#__codelineno-7-97>)    for event, err := range runner1.Run(ctx, userID, session1ID, userInput1, agent.RunConfig{}) {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-98>)        if err != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-99>)            log.Printf("Agent 1 Error: %v", err)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-100>)            continue
    [](<https://adk.dev/sessions/memory/#__codelineno-7-101>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-102>)        if event.LLMResponse.Content != nil && !event.LLMResponse.Partial {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-103>)            finalResponseText = strings.Join(textParts(event.LLMResponse.Content), "")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-104>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-105>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-106>)    fmt.Printf("Agent 1 Response: %s\n", finalResponseText)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-107>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-108>)    // Add the completed session to the Memory Service
    [](<https://adk.dev/sessions/memory/#__codelineno-7-109>)    fmt.Println("\n--- Adding Session 1 to Memory ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-110>)    resp, err := sessionService.Get(ctx, &session.GetRequest{AppName: appName, UserID: userID, SessionID: session1ID})
    [](<https://adk.dev/sessions/memory/#__codelineno-7-111>)    if err != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-112>)        log.Fatalf("Failed to get completed session: %v", err)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-113>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-114>)    if err := memoryService.AddSessionToMemory(ctx, resp.Session); err != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-115>)        log.Fatalf("Failed to add session to memory: %v", err)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-116>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-117>)    fmt.Println("Session added to memory.")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-118>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-119>)    // --- Scenario 2: Recall the information in a new session using a tool ---
    [](<https://adk.dev/sessions/memory/#__codelineno-7-120>)    fmt.Println("\n--- Turn 2: Recalling Information ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-121>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-122>)    memoryRecallAgent := must(llmagent.New(llmagent.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-7-123>)        Name:        "MemoryRecallAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-7-124>)        Model:       must(gemini.NewModel(ctx, modelID, nil)),
    [](<https://adk.dev/sessions/memory/#__codelineno-7-125>)        Instruction: "Answer the user's question. Use the 'search_past_conversations' tool if the answer might be in past conversations.",
    [](<https://adk.dev/sessions/memory/#__codelineno-7-126>)        Tools:       []tool.Tool{memorySearchTool}, // Give the agent the tool
    [](<https://adk.dev/sessions/memory/#__codelineno-7-127>)    }))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-128>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-129>)    runner2 := must(runner.New(runner.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-7-130>)        Agent:          memoryRecallAgent,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-131>)        AppName:        appName,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-132>)        SessionService: sessionService,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-133>)        MemoryService:  memoryService,
    [](<https://adk.dev/sessions/memory/#__codelineno-7-134>)    }))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-135>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-136>)    session2ID := "session_recall"
    [](<https://adk.dev/sessions/memory/#__codelineno-7-137>)    must(sessionService.Create(ctx, &session.CreateRequest{AppName: appName, UserID: userID, SessionID: session2ID}))
    [](<https://adk.dev/sessions/memory/#__codelineno-7-138>)    userInput2 := genai.NewContentFromText("What is my favorite project?", "user")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-139>)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-140>)    var finalResponseText2 string
    [](<https://adk.dev/sessions/memory/#__codelineno-7-141>)    for event, err := range runner2.Run(ctx, userID, session2ID, userInput2, agent.RunConfig{}) {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-142>)        if err != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-143>)            log.Printf("Agent 2 Error: %v", err)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-144>)            continue
    [](<https://adk.dev/sessions/memory/#__codelineno-7-145>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-146>)        if event.LLMResponse.Content != nil && !event.LLMResponse.Partial {
    [](<https://adk.dev/sessions/memory/#__codelineno-7-147>)            finalResponseText2 = strings.Join(textParts(event.LLMResponse.Content), "")
    [](<https://adk.dev/sessions/memory/#__codelineno-7-148>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-149>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-7-150>)    fmt.Printf("Agent 2 Response: %s\n", finalResponseText2)
    [](<https://adk.dev/sessions/memory/#__codelineno-7-151>)}
    
    [](<https://adk.dev/sessions/memory/#__codelineno-8-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-2>)import com.google.adk.agents.RunConfig;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-3>)import com.google.adk.events.Event;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-4>)import com.google.adk.runner.InMemoryRunner;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-5>)import com.google.adk.sessions.Session;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-6>)import com.google.adk.tools.LoadMemoryTool;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-7>)import com.google.genai.types.Content;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-8>)import com.google.genai.types.Part;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-9>)import java.util.Optional;
    [](<https://adk.dev/sessions/memory/#__codelineno-8-10>)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-11>)public class MemoryExample {
    [](<https://adk.dev/sessions/memory/#__codelineno-8-12>)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-13>)  public static void main(String[] args) {
    [](<https://adk.dev/sessions/memory/#__codelineno-8-14>)    String appName = "memory_example_app";
    [](<https://adk.dev/sessions/memory/#__codelineno-8-15>)    String userId = "mem_user";
    [](<https://adk.dev/sessions/memory/#__codelineno-8-16>)    String model = "gemini-flash-latest";
    [](<https://adk.dev/sessions/memory/#__codelineno-8-17>)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-18>)    // An agent that can recall past information using the load_memory tool.
    [](<https://adk.dev/sessions/memory/#__codelineno-8-19>)    LlmAgent agent =
    [](<https://adk.dev/sessions/memory/#__codelineno-8-20>)        LlmAgent.builder()
    [](<https://adk.dev/sessions/memory/#__codelineno-8-21>)            .model(model)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-22>)            .name("MemoryAgent")
    [](<https://adk.dev/sessions/memory/#__codelineno-8-23>)            .instruction(
    [](<https://adk.dev/sessions/memory/#__codelineno-8-24>)                "Answer the user's question. Use the 'load_memory' tool "
    [](<https://adk.dev/sessions/memory/#__codelineno-8-25>)                    + "if the answer might be in past conversations.")
    [](<https://adk.dev/sessions/memory/#__codelineno-8-26>)            .tools(new LoadMemoryTool())
    [](<https://adk.dev/sessions/memory/#__codelineno-8-27>)            .build();
    [](<https://adk.dev/sessions/memory/#__codelineno-8-28>)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-29>)    // InMemoryRunner bundles in-memory session and memory services and shares
    [](<https://adk.dev/sessions/memory/#__codelineno-8-30>)    // them across every session it creates.
    [](<https://adk.dev/sessions/memory/#__codelineno-8-31>)    InMemoryRunner runner = new InMemoryRunner(agent, appName);
    [](<https://adk.dev/sessions/memory/#__codelineno-8-32>)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-33>)    // --- Turn 1: capture information in one session ---
    [](<https://adk.dev/sessions/memory/#__codelineno-8-34>)    Session captureSession =
    [](<https://adk.dev/sessions/memory/#__codelineno-8-35>)        runner.sessionService().createSession(appName, userId).blockingGet();
    [](<https://adk.dev/sessions/memory/#__codelineno-8-36>)    Content statement =
    [](<https://adk.dev/sessions/memory/#__codelineno-8-37>)        Content.fromParts(Part.fromText("My favorite project is Project Alpha."));
    [](<https://adk.dev/sessions/memory/#__codelineno-8-38>)    runner
    [](<https://adk.dev/sessions/memory/#__codelineno-8-39>)        .runAsync(userId, captureSession.id(), statement, RunConfig.builder().build())
    [](<https://adk.dev/sessions/memory/#__codelineno-8-40>)        .blockingSubscribe();
    [](<https://adk.dev/sessions/memory/#__codelineno-8-41>)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-42>)    // Persist the finished session to memory.
    [](<https://adk.dev/sessions/memory/#__codelineno-8-43>)    Session completedSession =
    [](<https://adk.dev/sessions/memory/#__codelineno-8-44>)        runner
    [](<https://adk.dev/sessions/memory/#__codelineno-8-45>)            .sessionService()
    [](<https://adk.dev/sessions/memory/#__codelineno-8-46>)            .getSession(appName, userId, captureSession.id(), Optional.empty())
    [](<https://adk.dev/sessions/memory/#__codelineno-8-47>)            .blockingGet();
    [](<https://adk.dev/sessions/memory/#__codelineno-8-48>)    runner.memoryService().addSessionToMemory(completedSession).blockingAwait();
    [](<https://adk.dev/sessions/memory/#__codelineno-8-49>)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-50>)    // --- Turn 2: recall the information in a new session ---
    [](<https://adk.dev/sessions/memory/#__codelineno-8-51>)    Session recallSession =
    [](<https://adk.dev/sessions/memory/#__codelineno-8-52>)        runner.sessionService().createSession(appName, userId).blockingGet();
    [](<https://adk.dev/sessions/memory/#__codelineno-8-53>)    Content question = Content.fromParts(Part.fromText("What is my favorite project?"));
    [](<https://adk.dev/sessions/memory/#__codelineno-8-54>)    runner
    [](<https://adk.dev/sessions/memory/#__codelineno-8-55>)        .runAsync(userId, recallSession.id(), question, RunConfig.builder().build())
    [](<https://adk.dev/sessions/memory/#__codelineno-8-56>)        .blockingForEach(
    [](<https://adk.dev/sessions/memory/#__codelineno-8-57>)            (Event event) -> {
    [](<https://adk.dev/sessions/memory/#__codelineno-8-58>)              if (event.finalResponse()) {
    [](<https://adk.dev/sessions/memory/#__codelineno-8-59>)                event
    [](<https://adk.dev/sessions/memory/#__codelineno-8-60>)                    .content()
    [](<https://adk.dev/sessions/memory/#__codelineno-8-61>)                    .flatMap(Content::parts)
    [](<https://adk.dev/sessions/memory/#__codelineno-8-62>)                    .ifPresent(
    [](<https://adk.dev/sessions/memory/#__codelineno-8-63>)                        parts ->
    [](<https://adk.dev/sessions/memory/#__codelineno-8-64>)                            parts.forEach(part -> part.text().ifPresent(System.out::println)));
    [](<https://adk.dev/sessions/memory/#__codelineno-8-65>)              }
    [](<https://adk.dev/sessions/memory/#__codelineno-8-66>)            });
    [](<https://adk.dev/sessions/memory/#__codelineno-8-67>)  }
    [](<https://adk.dev/sessions/memory/#__codelineno-8-68>)}
    
    [](<https://adk.dev/sessions/memory/#__codelineno-9-1>)fun main() =
    [](<https://adk.dev/sessions/memory/#__codelineno-9-2>)    runBlocking {
    [](<https://adk.dev/sessions/memory/#__codelineno-9-3>)        // --- Constants ---
    [](<https://adk.dev/sessions/memory/#__codelineno-9-4>)        val appName = "memory_example_app"
    [](<https://adk.dev/sessions/memory/#__codelineno-9-5>)        val userId = "mem_user"
    [](<https://adk.dev/sessions/memory/#__codelineno-9-6>)        val model = Gemini(name = "gemini-flash-latest")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-7>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-8>)        // --- Agent Definitions ---
    [](<https://adk.dev/sessions/memory/#__codelineno-9-9>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-10>)        // Agent 1: Simple agent to capture information
    [](<https://adk.dev/sessions/memory/#__codelineno-9-11>)        val infoCaptureAgent =
    [](<https://adk.dev/sessions/memory/#__codelineno-9-12>)            LlmAgent(
    [](<https://adk.dev/sessions/memory/#__codelineno-9-13>)                name = "InfoCaptureAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-9-14>)                model = model,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-15>)                instruction = Instruction("Acknowledge the user's statement."),
    [](<https://adk.dev/sessions/memory/#__codelineno-9-16>)            )
    [](<https://adk.dev/sessions/memory/#__codelineno-9-17>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-18>)        // Agent 2: Agent that can use memory
    [](<https://adk.dev/sessions/memory/#__codelineno-9-19>)        val memoryRecallAgent =
    [](<https://adk.dev/sessions/memory/#__codelineno-9-20>)            LlmAgent(
    [](<https://adk.dev/sessions/memory/#__codelineno-9-21>)                name = "MemoryRecallAgent",
    [](<https://adk.dev/sessions/memory/#__codelineno-9-22>)                model = model,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-23>)                instruction =
    [](<https://adk.dev/sessions/memory/#__codelineno-9-24>)                    Instruction(
    [](<https://adk.dev/sessions/memory/#__codelineno-9-25>)                        "Answer the user's question. Use the 'load_memory' tool " +
    [](<https://adk.dev/sessions/memory/#__codelineno-9-26>)                            "if the answer might be in past conversations.",
    [](<https://adk.dev/sessions/memory/#__codelineno-9-27>)                    ),
    [](<https://adk.dev/sessions/memory/#__codelineno-9-28>)                tools = listOf(LoadMemoryTool()), // Give the agent the tool
    [](<https://adk.dev/sessions/memory/#__codelineno-9-29>)            )
    [](<https://adk.dev/sessions/memory/#__codelineno-9-30>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-31>)        // --- Services ---
    [](<https://adk.dev/sessions/memory/#__codelineno-9-32>)        // Services must be shared across runners to share state and memory
    [](<https://adk.dev/sessions/memory/#__codelineno-9-33>)        val sessionService = InMemorySessionService()
    [](<https://adk.dev/sessions/memory/#__codelineno-9-34>)        val memoryService = InMemoryMemoryService()
    [](<https://adk.dev/sessions/memory/#__codelineno-9-35>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-36>)        // --- Turn 1: Capturing Information ---
    [](<https://adk.dev/sessions/memory/#__codelineno-9-37>)        println("--- Turn 1: Capturing Information ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-38>)        val runner1 =
    [](<https://adk.dev/sessions/memory/#__codelineno-9-39>)            InMemoryRunner(
    [](<https://adk.dev/sessions/memory/#__codelineno-9-40>)                agent = infoCaptureAgent,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-41>)                appName = appName,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-42>)                sessionService = sessionService,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-43>)                memoryService = memoryService,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-44>)            )
    [](<https://adk.dev/sessions/memory/#__codelineno-9-45>)        val sessionId1 = "session_info"
    [](<https://adk.dev/sessions/memory/#__codelineno-9-46>)        val userInput1 = Content.fromText(Role.USER, "My favorite project is Project Alpha.")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-47>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-48>)        // Run the agent
    [](<https://adk.dev/sessions/memory/#__codelineno-9-49>)        runner1
    [](<https://adk.dev/sessions/memory/#__codelineno-9-50>)            .runAsync(
    [](<https://adk.dev/sessions/memory/#__codelineno-9-51>)                userId = userId,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-52>)                sessionId = sessionId1,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-53>)                newMessage = userInput1,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-54>)            ).collect { event ->
    [](<https://adk.dev/sessions/memory/#__codelineno-9-55>)                event.content?.parts?.forEach { part ->
    [](<https://adk.dev/sessions/memory/#__codelineno-9-56>)                    if (!part.text.isNullOrBlank()) {
    [](<https://adk.dev/sessions/memory/#__codelineno-9-57>)                        println("Agent Response: ${part.text}")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-58>)                    }
    [](<https://adk.dev/sessions/memory/#__codelineno-9-59>)                }
    [](<https://adk.dev/sessions/memory/#__codelineno-9-60>)            }
    [](<https://adk.dev/sessions/memory/#__codelineno-9-61>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-62>)        // Get the completed session using SessionKey
    [](<https://adk.dev/sessions/memory/#__codelineno-9-63>)        val session1 = sessionService.getSession(SessionKey(appName, userId, sessionId1))
    [](<https://adk.dev/sessions/memory/#__codelineno-9-64>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-65>)        // Add this session's content to the Memory Service
    [](<https://adk.dev/sessions/memory/#__codelineno-9-66>)        println("\n--- Adding Session 1 to Memory ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-67>)        if (session1 != null) {
    [](<https://adk.dev/sessions/memory/#__codelineno-9-68>)            memoryService.addSessionToMemory(session1)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-69>)            println("Session added to memory.")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-70>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-9-71>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-72>)        // --- Turn 2: Recalling Information ---
    [](<https://adk.dev/sessions/memory/#__codelineno-9-73>)        println("\n--- Turn 2: Recalling Information ---")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-74>)        val runner2 =
    [](<https://adk.dev/sessions/memory/#__codelineno-9-75>)            InMemoryRunner(
    [](<https://adk.dev/sessions/memory/#__codelineno-9-76>)                agent = memoryRecallAgent,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-77>)                appName = appName,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-78>)                sessionService = sessionService, // Reuse the same service
    [](<https://adk.dev/sessions/memory/#__codelineno-9-79>)                memoryService = memoryService, // Reuse the same service
    [](<https://adk.dev/sessions/memory/#__codelineno-9-80>)            )
    [](<https://adk.dev/sessions/memory/#__codelineno-9-81>)        val sessionId2 = "session_recall"
    [](<https://adk.dev/sessions/memory/#__codelineno-9-82>)        val userInput2 = Content.fromText(Role.USER, "What is my favorite project?")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-83>)
    [](<https://adk.dev/sessions/memory/#__codelineno-9-84>)        // Run the second agent
    [](<https://adk.dev/sessions/memory/#__codelineno-9-85>)        runner2
    [](<https://adk.dev/sessions/memory/#__codelineno-9-86>)            .runAsync(
    [](<https://adk.dev/sessions/memory/#__codelineno-9-87>)                userId = userId,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-88>)                sessionId = sessionId2,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-89>)                newMessage = userInput2,
    [](<https://adk.dev/sessions/memory/#__codelineno-9-90>)            ).collect { event ->
    [](<https://adk.dev/sessions/memory/#__codelineno-9-91>)                event.content?.parts?.forEach { part ->
    [](<https://adk.dev/sessions/memory/#__codelineno-9-92>)                    if (!part.text.isNullOrBlank()) {
    [](<https://adk.dev/sessions/memory/#__codelineno-9-93>)                        println("Agent Response: ${part.text}")
    [](<https://adk.dev/sessions/memory/#__codelineno-9-94>)                    }
    [](<https://adk.dev/sessions/memory/#__codelineno-9-95>)                }
    [](<https://adk.dev/sessions/memory/#__codelineno-9-96>)            }
    [](<https://adk.dev/sessions/memory/#__codelineno-9-97>)    }
    
### Search memory within a tool[¶](<https://adk.dev/sessions/memory/#search-memory-within-a-tool> "Permanent link")

You can also search memory from within a custom tool by using the tool context.

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/memory/#__codelineno-10-1>)from google.adk.tools import ToolContext
    [](<https://adk.dev/sessions/memory/#__codelineno-10-2>)
    [](<https://adk.dev/sessions/memory/#__codelineno-10-3>)async def search_past_conversations(
    [](<https://adk.dev/sessions/memory/#__codelineno-10-4>)    query: str, tool_context: ToolContext
    [](<https://adk.dev/sessions/memory/#__codelineno-10-5>)) -> dict:
    [](<https://adk.dev/sessions/memory/#__codelineno-10-6>)    response = await tool_context.search_memory(query)
    [](<https://adk.dev/sessions/memory/#__codelineno-10-7>)    return {
    [](<https://adk.dev/sessions/memory/#__codelineno-10-8>)        "results": [
    [](<https://adk.dev/sessions/memory/#__codelineno-10-9>)            part.text
    [](<https://adk.dev/sessions/memory/#__codelineno-10-10>)            for entry in response.memories
    [](<https://adk.dev/sessions/memory/#__codelineno-10-11>)            for part in (entry.content.parts or [])
    [](<https://adk.dev/sessions/memory/#__codelineno-10-12>)            if part.text
    [](<https://adk.dev/sessions/memory/#__codelineno-10-13>)        ]
    [](<https://adk.dev/sessions/memory/#__codelineno-10-14>)    }
    
    [](<https://adk.dev/sessions/memory/#__codelineno-11-1>)// Within a tool implementation
    [](<https://adk.dev/sessions/memory/#__codelineno-11-2>)async runAsync({ args, toolContext }: RunAsyncToolRequest) {
    [](<https://adk.dev/sessions/memory/#__codelineno-11-3>)  const query = args['query'] as string;
    [](<https://adk.dev/sessions/memory/#__codelineno-11-4>)  const response = await toolContext.searchMemory(query);
    [](<https://adk.dev/sessions/memory/#__codelineno-11-5>)  // process response
    [](<https://adk.dev/sessions/memory/#__codelineno-11-6>)  return {
    [](<https://adk.dev/sessions/memory/#__codelineno-11-7>)    memories: response.memories.map(m => m.content.parts?.map(p => p.text).join(' ')).join('\n')
    [](<https://adk.dev/sessions/memory/#__codelineno-11-8>)  };
    [](<https://adk.dev/sessions/memory/#__codelineno-11-9>)}
    
    [](<https://adk.dev/sessions/memory/#__codelineno-12-1>)// memorySearchToolFunc is the implementation of the memory search tool.
    [](<https://adk.dev/sessions/memory/#__codelineno-12-2>)// This function demonstrates accessing memory via agent.Context.
    [](<https://adk.dev/sessions/memory/#__codelineno-12-3>)func memorySearchToolFunc(tctx agent.Context, args Args) (Result, error) {
    [](<https://adk.dev/sessions/memory/#__codelineno-12-4>)    fmt.Printf("Tool: Searching memory for query: '%s'\n", args.Query)
    [](<https://adk.dev/sessions/memory/#__codelineno-12-5>)    // The SearchMemory function is available on the context.
    [](<https://adk.dev/sessions/memory/#__codelineno-12-6>)    searchResults, err := tctx.SearchMemory(context.Background(), args.Query)
    [](<https://adk.dev/sessions/memory/#__codelineno-12-7>)    if err != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-12-8>)        log.Printf("Error searching memory: %v", err)
    [](<https://adk.dev/sessions/memory/#__codelineno-12-9>)        return Result{}, fmt.Errorf("failed memory search")
    [](<https://adk.dev/sessions/memory/#__codelineno-12-10>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-12-11>)
    [](<https://adk.dev/sessions/memory/#__codelineno-12-12>)    var results []string
    [](<https://adk.dev/sessions/memory/#__codelineno-12-13>)    for _, res := range searchResults.Memories {
    [](<https://adk.dev/sessions/memory/#__codelineno-12-14>)        if res.Content != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-12-15>)            results = append(results, textParts(res.Content)...)
    [](<https://adk.dev/sessions/memory/#__codelineno-12-16>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-12-17>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-12-18>)    return Result{Results: results}, nil
    [](<https://adk.dev/sessions/memory/#__codelineno-12-19>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-12-20>)
    [](<https://adk.dev/sessions/memory/#__codelineno-12-21>)// Define a tool that can search memory.
    [](<https://adk.dev/sessions/memory/#__codelineno-12-22>)var memorySearchTool = must(functiontool.New(
    [](<https://adk.dev/sessions/memory/#__codelineno-12-23>)    functiontool.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-12-24>)        Name:        "search_past_conversations",
    [](<https://adk.dev/sessions/memory/#__codelineno-12-25>)        Description: "Searches past conversations for relevant information.",
    [](<https://adk.dev/sessions/memory/#__codelineno-12-26>)    },
    [](<https://adk.dev/sessions/memory/#__codelineno-12-27>)    memorySearchToolFunc,
    [](<https://adk.dev/sessions/memory/#__codelineno-12-28>)))
    
    [](<https://adk.dev/sessions/memory/#__codelineno-13-1>)// Within a tool implementation
    [](<https://adk.dev/sessions/memory/#__codelineno-13-2>)public Single<ToolOutput> execute(ToolContext context) {
    [](<https://adk.dev/sessions/memory/#__codelineno-13-3>)  String query = ...; // get query from arguments
    [](<https://adk.dev/sessions/memory/#__codelineno-13-4>)  return context.searchMemory(query)
    [](<https://adk.dev/sessions/memory/#__codelineno-13-5>)      .map(response -> {
    [](<https://adk.dev/sessions/memory/#__codelineno-13-6>)          // process response
    [](<https://adk.dev/sessions/memory/#__codelineno-13-7>)          return new ToolOutput(response.memories().toString());
    [](<https://adk.dev/sessions/memory/#__codelineno-13-8>)      });
    [](<https://adk.dev/sessions/memory/#__codelineno-13-9>)}
    
    [](<https://adk.dev/sessions/memory/#__codelineno-14-1>)suspend fun searchWithinTool(
    [](<https://adk.dev/sessions/memory/#__codelineno-14-2>)    context: ToolContext,
    [](<https://adk.dev/sessions/memory/#__codelineno-14-3>)    args: Map<String, Any>,
    [](<https://adk.dev/sessions/memory/#__codelineno-14-4>)): String {
    [](<https://adk.dev/sessions/memory/#__codelineno-14-5>)    val query = args["query"] as String
    [](<https://adk.dev/sessions/memory/#__codelineno-14-6>)    val response =
    [](<https://adk.dev/sessions/memory/#__codelineno-14-7>)        context.invocationContext.memoryService?.searchMemory(
    [](<https://adk.dev/sessions/memory/#__codelineno-14-8>)            appName = context.invocationContext.session.key.appName,
    [](<https://adk.dev/sessions/memory/#__codelineno-14-9>)            userId = context.invocationContext.session.key.userId,
    [](<https://adk.dev/sessions/memory/#__codelineno-14-10>)            query = query,
    [](<https://adk.dev/sessions/memory/#__codelineno-14-11>)        )
    [](<https://adk.dev/sessions/memory/#__codelineno-14-12>)    // process response
    [](<https://adk.dev/sessions/memory/#__codelineno-14-13>)    return response?.memories?.joinToString("\n") {
    [](<https://adk.dev/sessions/memory/#__codelineno-14-14>)        it.content.parts.joinToString(" ") { p -> p.text ?: "" }
    [](<https://adk.dev/sessions/memory/#__codelineno-14-15>)    } ?: ""
    [](<https://adk.dev/sessions/memory/#__codelineno-14-16>)}
    
## Memory Bank[¶](<https://adk.dev/sessions/memory/#memory-bank> "Permanent link")

The `VertexAiMemoryBankService` connects your agent to [Memory Bank](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/memory-bank/overview>), a fully managed Google Cloud service that provides sophisticated, persistent memory capabilities for conversational agents.

### How it works[¶](<https://adk.dev/sessions/memory/#how-it-works> "Permanent link")

The service handles two key operations:

  * **Generating Memories:** At the end of a conversation, you can send the session's events to the Memory Bank, which intelligently processes and stores the information as "memories."
  * **Retrieving Memories:** Your agent code can issue a search query against the Memory Bank to retrieve relevant memories from past conversations.

### Direct memory ingestion with `add_memory`[¶](<https://adk.dev/sessions/memory/#direct-memory-ingestion-with-add_memory> "Permanent link")

Besides generating memories from session history, `VertexAiMemoryBankService` also supports direct memory ingestion via the `add_memory` method. This method gives you precise control over the facts stored in the Memory Bank.

How it works depends on the `enable_consolidation` option:

  * **Direct Creation (Default):** By default, `add_memory` calls the underlying `memories.create` API. Each `MemoryEntry` you provide is added as a distinct, separate memory item.
        
        [](<https://adk.dev/sessions/memory/#__codelineno-15-1>)from google.adk.memory import VertexAiMemoryBankService
        [](<https://adk.dev/sessions/memory/#__codelineno-15-2>)from google.adk.memory.memory_entry import MemoryEntry
        [](<https://adk.dev/sessions/memory/#__codelineno-15-3>)from google.genai.types import Content, Part
        [](<https://adk.dev/sessions/memory/#__codelineno-15-4>)
        [](<https://adk.dev/sessions/memory/#__codelineno-15-5>)memory_service = VertexAiMemoryBankService(...)
        [](<https://adk.dev/sessions/memory/#__codelineno-15-6>)
        [](<https://adk.dev/sessions/memory/#__codelineno-15-7>)await memory_service.add_memory(
        [](<https://adk.dev/sessions/memory/#__codelineno-15-8>)    app_name="my-app",
        [](<https://adk.dev/sessions/memory/#__codelineno-15-9>)    user_id="user-123",
        [](<https://adk.dev/sessions/memory/#__codelineno-15-10>)    memories=[
        [](<https://adk.dev/sessions/memory/#__codelineno-15-11>)        MemoryEntry(content=Content(parts=[Part(text="The user's favorite color is blue.")]))
        [](<https://adk.dev/sessions/memory/#__codelineno-15-12>)    ]
        [](<https://adk.dev/sessions/memory/#__codelineno-15-13>))
        
  * **Creation with Consolidation:** If you set `enable_consolidation` to `True` in the `custom_metadata`, the service uses the `memories.generate` API. This setting allows the Memory Bank to intelligently consolidate the new memory items with existing related memories, preventing redundancy and building a more coherent knowledge base.
        
        [](<https://adk.dev/sessions/memory/#__codelineno-16-1>)await memory_service.add_memory(
        [](<https://adk.dev/sessions/memory/#__codelineno-16-2>)    app_name="my-app",
        [](<https://adk.dev/sessions/memory/#__codelineno-16-3>)    user_id="user-123",
        [](<https://adk.dev/sessions/memory/#__codelineno-16-4>)    memories=[
        [](<https://adk.dev/sessions/memory/#__codelineno-16-5>)        MemoryEntry(content=Content(parts=[Part(text="The user's favorite color is light blue.")]))
        [](<https://adk.dev/sessions/memory/#__codelineno-16-6>)    ],
        [](<https://adk.dev/sessions/memory/#__codelineno-16-7>)    custom_metadata={"enable_consolidation": True}
        [](<https://adk.dev/sessions/memory/#__codelineno-16-8>))
        
### Prerequisites[¶](<https://adk.dev/sessions/memory/#prerequisites> "Permanent link")

Before you can use this feature, you must have:

  1. **A Google Cloud Project:** With the Agent Platform API enabled.
  2. **An Agent Runtime:** You need to create an Agent Runtime on Agent Platform. You do not need to deploy your agent to Agent Runtime to use Memory Bank. This setup will provide you with the **Agent Runtime ID** required for configuration.
  3. **Authentication:** Ensure your local environment is authenticated to access Google Cloud services. The simplest way is to run:
         
         [](<https://adk.dev/sessions/memory/#__codelineno-17-1>)gcloud auth application-default login
         
  4. **Environment Variables:** The service requires your Google Cloud Project ID and Location. Set them as environment variables:
         
         [](<https://adk.dev/sessions/memory/#__codelineno-18-1>)export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
         [](<https://adk.dev/sessions/memory/#__codelineno-18-2>)export GOOGLE_CLOUD_LOCATION="your-gcp-location"
         
For more information on connecting to Google Cloud from ADK agents, see [Connect to Google Cloud and Agent Platform](<https://adk.dev/get-started/google-cloud/>).

### Configuration[¶](<https://adk.dev/sessions/memory/#configuration> "Permanent link")

To connect your agent to the Memory Bank, you use the `--memory_service_uri` flag when starting the ADK server (`adk web` or `adk api_server`). The Uniform Resource Identifier (URI) must be in the format `agentengine://<agent_engine_id>`.

bash
    
    [](<https://adk.dev/sessions/memory/#__codelineno-19-1>)adk web path/to/your/agents_dir --memory_service_uri="agentengine://1234567890"
    
Or, you can configure your agent to use the Memory Bank by manually instantiating the `VertexAiMemoryBankService` and passing it to the `Runner`.

Python
    
    [](<https://adk.dev/sessions/memory/#__codelineno-20-1>)from google import adk
    [](<https://adk.dev/sessions/memory/#__codelineno-20-2>)from google.adk.memory import VertexAiMemoryBankService
    [](<https://adk.dev/sessions/memory/#__codelineno-20-3>)
    [](<https://adk.dev/sessions/memory/#__codelineno-20-4>)memory_service = VertexAiMemoryBankService(
    [](<https://adk.dev/sessions/memory/#__codelineno-20-5>)    project="PROJECT_ID",
    [](<https://adk.dev/sessions/memory/#__codelineno-20-6>)    location="LOCATION",
    [](<https://adk.dev/sessions/memory/#__codelineno-20-7>)    agent_engine_id="AGENT_ENGINE_ID"
    [](<https://adk.dev/sessions/memory/#__codelineno-20-8>))
    [](<https://adk.dev/sessions/memory/#__codelineno-20-9>)
    [](<https://adk.dev/sessions/memory/#__codelineno-20-10>)runner = adk.Runner(
    [](<https://adk.dev/sessions/memory/#__codelineno-20-11>)    ...
    [](<https://adk.dev/sessions/memory/#__codelineno-20-12>)    memory_service=memory_service
    [](<https://adk.dev/sessions/memory/#__codelineno-20-13>))
    
## RAG memory[¶](<https://adk.dev/sessions/memory/#rag-memory> "Permanent link")

The `VertexAiRagMemoryService` stores conversations in [Knowledge Engine](<https://cloud.google.com/vertex-ai/generative-ai/docs/rag-engine/rag-overview>) and retrieves them by vector similarity. Use it when you already have RAG infrastructure or want raw transcript retrieval rather than the LLM-extracted memories produced by Memory Bank. Requires the Agent Platform SDK.

Python
    
    [](<https://adk.dev/sessions/memory/#__codelineno-21-1>)from google.adk.memory import VertexAiRagMemoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-21-2>)
    [](<https://adk.dev/sessions/memory/#__codelineno-21-3>)memory_service = VertexAiRagMemoryService(
    [](<https://adk.dev/sessions/memory/#__codelineno-21-4>)    rag_corpus="projects/PROJECT_ID/locations/LOCATION/ragCorpora/CORPUS_ID",
    [](<https://adk.dev/sessions/memory/#__codelineno-21-5>)    similarity_top_k=5,
    [](<https://adk.dev/sessions/memory/#__codelineno-21-6>)    vector_distance_threshold=0.6,
    [](<https://adk.dev/sessions/memory/#__codelineno-21-7>))
    
## Use memory in your agent[¶](<https://adk.dev/sessions/memory/#use-memory-in-your-agent> "Permanent link")

When a memory service is configured, your agent can use a tool or callback to retrieve memories. ADK includes two pre-built tools for retrieving memories:

  * **Preload memory** : Automatically retrieves memory at the beginning of each turn, similar to a callback.
  * **Load memory** : Retrieves memory when your agent decides it would be helpful.

**Example:**

PythonTypeScriptGoJavaKotlin
    
    [](<https://adk.dev/sessions/memory/#__codelineno-22-1>)from google.adk.agents import Agent
    [](<https://adk.dev/sessions/memory/#__codelineno-22-2>)from google.adk.tools import preload_memory
    [](<https://adk.dev/sessions/memory/#__codelineno-22-3>)
    [](<https://adk.dev/sessions/memory/#__codelineno-22-4>)agent = Agent(
    [](<https://adk.dev/sessions/memory/#__codelineno-22-5>)    model=MODEL_ID,
    [](<https://adk.dev/sessions/memory/#__codelineno-22-6>)    name='weather_sentiment_agent',
    [](<https://adk.dev/sessions/memory/#__codelineno-22-7>)    instruction="...",
    [](<https://adk.dev/sessions/memory/#__codelineno-22-8>)    tools=[preload_memory]
    [](<https://adk.dev/sessions/memory/#__codelineno-22-9>))
    
    [](<https://adk.dev/sessions/memory/#__codelineno-23-1>)import { LlmAgent, PRELOAD_MEMORY } from '@google/adk';
    [](<https://adk.dev/sessions/memory/#__codelineno-23-2>)
    [](<https://adk.dev/sessions/memory/#__codelineno-23-3>)const agent = new LlmAgent({
    [](<https://adk.dev/sessions/memory/#__codelineno-23-4>)    model: MODEL_ID,
    [](<https://adk.dev/sessions/memory/#__codelineno-23-5>)    name: 'weather_sentiment_agent',
    [](<https://adk.dev/sessions/memory/#__codelineno-23-6>)    instruction: "...",
    [](<https://adk.dev/sessions/memory/#__codelineno-23-7>)    tools: [PRELOAD_MEMORY]
    [](<https://adk.dev/sessions/memory/#__codelineno-23-8>)});
    
    [](<https://adk.dev/sessions/memory/#__codelineno-24-1>)import (
    [](<https://adk.dev/sessions/memory/#__codelineno-24-2>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/sessions/memory/#__codelineno-24-3>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/sessions/memory/#__codelineno-24-4>)    "google.golang.org/adk/v2/tool/preloadmemorytool"
    [](<https://adk.dev/sessions/memory/#__codelineno-24-5>))
    [](<https://adk.dev/sessions/memory/#__codelineno-24-6>)
    [](<https://adk.dev/sessions/memory/#__codelineno-24-7>)agent, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-24-8>)    Model:       model,
    [](<https://adk.dev/sessions/memory/#__codelineno-24-9>)    Name:        "weather_sentiment_agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-24-10>)    Instruction: "...",
    [](<https://adk.dev/sessions/memory/#__codelineno-24-11>)    Tools:       []tool.Tool{preloadmemorytool.New()},
    [](<https://adk.dev/sessions/memory/#__codelineno-24-12>)})
    
    [](<https://adk.dev/sessions/memory/#__codelineno-25-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/sessions/memory/#__codelineno-25-2>)import com.google.adk.tools.LoadMemoryTool;
    [](<https://adk.dev/sessions/memory/#__codelineno-25-3>)
    [](<https://adk.dev/sessions/memory/#__codelineno-25-4>)LlmAgent agent = new LlmAgent.Builder()
    [](<https://adk.dev/sessions/memory/#__codelineno-25-5>)    .model(MODEL_ID)
    [](<https://adk.dev/sessions/memory/#__codelineno-25-6>)    .name("weather_sentiment_agent")
    [](<https://adk.dev/sessions/memory/#__codelineno-25-7>)    .instruction("...")
    [](<https://adk.dev/sessions/memory/#__codelineno-25-8>)    .tools(new LoadMemoryTool())
    [](<https://adk.dev/sessions/memory/#__codelineno-25-9>)    .build();
    
    [](<https://adk.dev/sessions/memory/#__codelineno-26-1>)fun preloadMemoryAgent(model: Gemini) {
    [](<https://adk.dev/sessions/memory/#__codelineno-26-2>)    val agent =
    [](<https://adk.dev/sessions/memory/#__codelineno-26-3>)        LlmAgent(
    [](<https://adk.dev/sessions/memory/#__codelineno-26-4>)            model = model,
    [](<https://adk.dev/sessions/memory/#__codelineno-26-5>)            name = "weather_sentiment_agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-26-6>)            instruction = Instruction("..."),
    [](<https://adk.dev/sessions/memory/#__codelineno-26-7>)            tools = listOf(PreloadMemoryTool()),
    [](<https://adk.dev/sessions/memory/#__codelineno-26-8>)        )
    [](<https://adk.dev/sessions/memory/#__codelineno-26-9>)}
    
To extract memories from your session, you need to call `add_session_to_memory`. For example, you can automate this step with a callback:

PythonTypeScriptGoKotlin
    
    [](<https://adk.dev/sessions/memory/#__codelineno-27-1>)from google.adk.agents import Agent
    [](<https://adk.dev/sessions/memory/#__codelineno-27-2>)from google.adk.tools import preload_memory
    [](<https://adk.dev/sessions/memory/#__codelineno-27-3>)
    [](<https://adk.dev/sessions/memory/#__codelineno-27-4>)async def auto_save_session_to_memory_callback(callback_context):
    [](<https://adk.dev/sessions/memory/#__codelineno-27-5>)    await callback_context.add_session_to_memory()
    [](<https://adk.dev/sessions/memory/#__codelineno-27-6>)
    [](<https://adk.dev/sessions/memory/#__codelineno-27-7>)agent = Agent(
    [](<https://adk.dev/sessions/memory/#__codelineno-27-8>)    model=MODEL,
    [](<https://adk.dev/sessions/memory/#__codelineno-27-9>)    name="Generic_QA_Agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-27-10>)    instruction="Answer the user's questions",
    [](<https://adk.dev/sessions/memory/#__codelineno-27-11>)    tools=[preload_memory],
    [](<https://adk.dev/sessions/memory/#__codelineno-27-12>)    after_agent_callback=auto_save_session_to_memory_callback,
    [](<https://adk.dev/sessions/memory/#__codelineno-27-13>))
    
    [](<https://adk.dev/sessions/memory/#__codelineno-28-1>)import { LlmAgent, PRELOAD_MEMORY, SingleAgentCallback } from '@google/adk';
    [](<https://adk.dev/sessions/memory/#__codelineno-28-2>)
    [](<https://adk.dev/sessions/memory/#__codelineno-28-3>)const autoSaveSessionToMemoryCallback: SingleAgentCallback = async (callbackContext) => {
    [](<https://adk.dev/sessions/memory/#__codelineno-28-4>)    if (callbackContext.invocationContext.memoryService) {
    [](<https://adk.dev/sessions/memory/#__codelineno-28-5>)        await callbackContext.invocationContext.memoryService.addSessionToMemory(
    [](<https://adk.dev/sessions/memory/#__codelineno-28-6>)            callbackContext.invocationContext.session
    [](<https://adk.dev/sessions/memory/#__codelineno-28-7>)        );
    [](<https://adk.dev/sessions/memory/#__codelineno-28-8>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-28-9>)};
    [](<https://adk.dev/sessions/memory/#__codelineno-28-10>)
    [](<https://adk.dev/sessions/memory/#__codelineno-28-11>)const agent = new LlmAgent({
    [](<https://adk.dev/sessions/memory/#__codelineno-28-12>)    model: MODEL,
    [](<https://adk.dev/sessions/memory/#__codelineno-28-13>)    name: "Generic_QA_Agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-28-14>)    instruction: "Answer the user's questions",
    [](<https://adk.dev/sessions/memory/#__codelineno-28-15>)    tools: [PRELOAD_MEMORY],
    [](<https://adk.dev/sessions/memory/#__codelineno-28-16>)    afterAgentCallback: autoSaveSessionToMemoryCallback,
    [](<https://adk.dev/sessions/memory/#__codelineno-28-17>)});
    
    [](<https://adk.dev/sessions/memory/#__codelineno-29-1>)import (
    [](<https://adk.dev/sessions/memory/#__codelineno-29-2>)    "context"
    [](<https://adk.dev/sessions/memory/#__codelineno-29-3>)    "google.golang.org/adk/v2/agent"
    [](<https://adk.dev/sessions/memory/#__codelineno-29-4>)    "google.golang.org/adk/v2/agent/llmagent"
    [](<https://adk.dev/sessions/memory/#__codelineno-29-5>)    "google.golang.org/adk/v2/session"
    [](<https://adk.dev/sessions/memory/#__codelineno-29-6>)    "google.golang.org/adk/v2/tool"
    [](<https://adk.dev/sessions/memory/#__codelineno-29-7>)    "google.golang.org/adk/v2/tool/loadmemorytool"
    [](<https://adk.dev/sessions/memory/#__codelineno-29-8>))
    [](<https://adk.dev/sessions/memory/#__codelineno-29-9>)
    [](<https://adk.dev/sessions/memory/#__codelineno-29-10>)func autoSaveSessionToMemoryCallback(ctx agent.CallbackContext, s session.Session) (*genai.Content, error) {
    [](<https://adk.dev/sessions/memory/#__codelineno-29-11>)    if err := ctx.Memory().AddSessionToMemory(context.Background(), s); err != nil {
    [](<https://adk.dev/sessions/memory/#__codelineno-29-12>)        return nil, err
    [](<https://adk.dev/sessions/memory/#__codelineno-29-13>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-29-14>)    return nil, nil
    [](<https://adk.dev/sessions/memory/#__codelineno-29-15>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-29-16>)
    [](<https://adk.dev/sessions/memory/#__codelineno-29-17>)agent, _ := llmagent.New(llmagent.Config{
    [](<https://adk.dev/sessions/memory/#__codelineno-29-18>)    Model:               model,
    [](<https://adk.dev/sessions/memory/#__codelineno-29-19>)    Name:                "Generic_QA_Agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-29-20>)    Instruction:         "Answer the user's questions",
    [](<https://adk.dev/sessions/memory/#__codelineno-29-21>)    Tools:               []tool.Tool{loadmemorytool.New()},
    [](<https://adk.dev/sessions/memory/#__codelineno-29-22>)    AfterAgentCallbacks: []agent.AfterAgentCallback{autoSaveSessionToMemoryCallback},
    [](<https://adk.dev/sessions/memory/#__codelineno-29-23>)})
    
    [](<https://adk.dev/sessions/memory/#__codelineno-30-1>)suspend fun autoSaveSessionToMemoryCallback(
    [](<https://adk.dev/sessions/memory/#__codelineno-30-2>)    context: CallbackContext,
    [](<https://adk.dev/sessions/memory/#__codelineno-30-3>)): CallbackChoice<Unit, Content> {
    [](<https://adk.dev/sessions/memory/#__codelineno-30-4>)    context.addSessionToMemory()
    [](<https://adk.dev/sessions/memory/#__codelineno-30-5>)    return CallbackChoice.Continue(Unit)
    [](<https://adk.dev/sessions/memory/#__codelineno-30-6>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-30-7>)
    [](<https://adk.dev/sessions/memory/#__codelineno-30-8>)fun agentWithCallback(model: Gemini) {
    [](<https://adk.dev/sessions/memory/#__codelineno-30-9>)    val agent =
    [](<https://adk.dev/sessions/memory/#__codelineno-30-10>)        LlmAgent(
    [](<https://adk.dev/sessions/memory/#__codelineno-30-11>)            model = model,
    [](<https://adk.dev/sessions/memory/#__codelineno-30-12>)            name = "Generic_QA_Agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-30-13>)            instruction = Instruction("Answer the user's questions"),
    [](<https://adk.dev/sessions/memory/#__codelineno-30-14>)            tools = listOf(PreloadMemoryTool()),
    [](<https://adk.dev/sessions/memory/#__codelineno-30-15>)            afterAgentCallbacks = listOf(AfterAgentCallback(::autoSaveSessionToMemoryCallback)),
    [](<https://adk.dev/sessions/memory/#__codelineno-30-16>)        )
    [](<https://adk.dev/sessions/memory/#__codelineno-30-17>)}
    
## Extend memory capabilities[¶](<https://adk.dev/sessions/memory/#extend-memory-capabilities> "Permanent link")

Memory services extended from `BaseMemoryService` support adding sessions and events to agent memory, including custom metadata. Use the `add_session_to_memory` and `add_events_to_memory` methods of memory services such as `InMemoryMemoryService` to amend memory data, as shown in the following code example:
    
    [](<https://adk.dev/sessions/memory/#__codelineno-31-1>)import asyncio
    [](<https://adk.dev/sessions/memory/#__codelineno-31-2>)from google.adk.memory import InMemoryMemoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-31-3>)
    [](<https://adk.dev/sessions/memory/#__codelineno-31-4>)# Assume my_memory_service is an instance of InMemoryMemoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-31-5>)# and my_latest_events is a list of new adk.Event objects from the latest turn.
    [](<https://adk.dev/sessions/memory/#__codelineno-31-6>)my_latest_events = [...]
    [](<https://adk.dev/sessions/memory/#__codelineno-31-7>)
    [](<https://adk.dev/sessions/memory/#__codelineno-31-8>)async def update_incremental_memory(my_memory_service, my_latest_events):
    [](<https://adk.dev/sessions/memory/#__codelineno-31-9>)    # Example 1: Basic incremental update
    [](<https://adk.dev/sessions/memory/#__codelineno-31-10>)    await my_memory_service.add_events_to_memory(
    [](<https://adk.dev/sessions/memory/#__codelineno-31-11>)        app_name="my-app",
    [](<https://adk.dev/sessions/memory/#__codelineno-31-12>)        user_id="my-user",
    [](<https://adk.dev/sessions/memory/#__codelineno-31-13>)        events=my_latest_events,
    [](<https://adk.dev/sessions/memory/#__codelineno-31-14>)        session_id="my-optional-session-id"
    [](<https://adk.dev/sessions/memory/#__codelineno-31-15>)    )
    [](<https://adk.dev/sessions/memory/#__codelineno-31-16>)
    [](<https://adk.dev/sessions/memory/#__codelineno-31-17>)    # Example 2: Incremental update with Custom Metadata
    [](<https://adk.dev/sessions/memory/#__codelineno-31-18>)    await my_memory_service.add_events_to_memory(
    [](<https://adk.dev/sessions/memory/#__codelineno-31-19>)        app_name="my-app",
    [](<https://adk.dev/sessions/memory/#__codelineno-31-20>)        user_id="my-user",
    [](<https://adk.dev/sessions/memory/#__codelineno-31-21>)        events=my_latest_events,
    [](<https://adk.dev/sessions/memory/#__codelineno-31-22>)        session_id="my-optional-session-id",
    [](<https://adk.dev/sessions/memory/#__codelineno-31-23>)        custom_metadata={
    [](<https://adk.dev/sessions/memory/#__codelineno-31-24>)            "my_custom_key": "my_custom_value"
    [](<https://adk.dev/sessions/memory/#__codelineno-31-25>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-31-26>)    )
    [](<https://adk.dev/sessions/memory/#__codelineno-31-27>)
    [](<https://adk.dev/sessions/memory/#__codelineno-31-28>)async def update_session_memory(my_memory_service, my_completed_session):
    [](<https://adk.dev/sessions/memory/#__codelineno-31-29>)    # Example 3: Applying custom metadata to a full session
    [](<https://adk.dev/sessions/memory/#__codelineno-31-30>)    await my_memory_service.add_session_to_memory(
    [](<https://adk.dev/sessions/memory/#__codelineno-31-31>)        session=my_completed_session,
    [](<https://adk.dev/sessions/memory/#__codelineno-31-32>)        custom_metadata={
    [](<https://adk.dev/sessions/memory/#__codelineno-31-33>)            "category": "user_preference"
    [](<https://adk.dev/sessions/memory/#__codelineno-31-34>)        }
    [](<https://adk.dev/sessions/memory/#__codelineno-31-35>)    )
    
## Advanced concepts[¶](<https://adk.dev/sessions/memory/#advanced-concepts> "Permanent link")

### How memory works in practice[¶](<https://adk.dev/sessions/memory/#how-memory-works-in-practice> "Permanent link")

The memory workflow includes the following steps:

  1. **Session Interaction:** A user interacts with an agent via a `Session`, managed by a `SessionService`. During this interaction, events are recorded and session state may be updated.
  2. **Ingestion into Memory:** When a session concludes or captures significant information, your application calls `memory_service.add_session_to_memory(session)`. This action extracts key data and persists it to your long-term knowledge store, such as the Agent Runtime Memory Bank.
  3. **Later Query:** In a different, or in the same session, you might ask a question requiring past context, for example, "What did we discuss about project X last week?".
  4. **Agent Uses Memory Tool:** An agent equipped with a memory-retrieval tool, such as the built-in `load_memory` tool, recognizes the need for past context. It calls the tool, providing a search query (e.g., "discussion project X last week").
  5. **Search Execution:** The tool internally calls `memory_service.search_memory(app_name=..., user_id=..., query=...)`.
  6. **Results Returned:** The `MemoryService` searches its store, using keyword matching or semantic search, and returns matching snippets as a `SearchMemoryResponse` containing a list of `MemoryEntry` objects, each holding `content`, and all optional: `author`, `timestamp`, and `custom_metadata`.
  7. **Agent Uses Results:** The tool returns these results to the agent, usually as part of the context or function response. The agent can then use this retrieved information to formulate its final answer to the user.

### Can an agent have access to more than one memory service?[¶](<https://adk.dev/sessions/memory/#can-an-agent-have-access-to-more-than-one-memory-service> "Permanent link")

  * **Through Standard Configuration: No.** The framework (`adk web`, `adk api_server`) is designed to be configured with one memory service at a time via the `--memory_service_uri` flag. That single service is wired into the runner and exposed through `tool_context.search_memory()` and `callback_context.search_memory()`.
  * **Within Your Agent's Code: Yes.** You can instantiate a second `BaseMemoryService` and consult it from a custom tool, which already has a `ToolContext` for the framework-configured service.

For example, your agent can use the framework-configured `InMemoryMemoryService` for conversation history and manually instantiate a second service, a `VertexAiMemoryBankService`, a `VertexAiRagMemoryService` over a docs corpus, or any other `BaseMemoryService` implementation, for a separate knowledge base.

#### Example: Use two memory services[¶](<https://adk.dev/sessions/memory/#example-use-two-memory-services> "Permanent link")

PythonKotlin
    
    [](<https://adk.dev/sessions/memory/#__codelineno-32-1>)from google.adk.agents import Agent
    [](<https://adk.dev/sessions/memory/#__codelineno-32-2>)from google.adk.memory import InMemoryMemoryService
    [](<https://adk.dev/sessions/memory/#__codelineno-32-3>)from google.adk.tools import ToolContext
    [](<https://adk.dev/sessions/memory/#__codelineno-32-4>)
    [](<https://adk.dev/sessions/memory/#__codelineno-32-5>)# Second memory service for docs lookup; could be any BaseMemoryService.
    [](<https://adk.dev/sessions/memory/#__codelineno-32-6>)docs_memory = InMemoryMemoryService()
    [](<https://adk.dev/sessions/memory/#__codelineno-32-7>)
    [](<https://adk.dev/sessions/memory/#__codelineno-32-8>)
    [](<https://adk.dev/sessions/memory/#__codelineno-32-9>)async def search_all_memory(query: str, tool_context: ToolContext) -> dict:
    [](<https://adk.dev/sessions/memory/#__codelineno-32-10>)    """Search both the conversational memory and the docs corpus."""
    [](<https://adk.dev/sessions/memory/#__codelineno-32-11>)    conversational = await tool_context.search_memory(query)
    [](<https://adk.dev/sessions/memory/#__codelineno-32-12>)    docs = await docs_memory.search_memory(
    [](<https://adk.dev/sessions/memory/#__codelineno-32-13>)        app_name="docs", user_id="shared", query=query
    [](<https://adk.dev/sessions/memory/#__codelineno-32-14>)    )
    [](<https://adk.dev/sessions/memory/#__codelineno-32-15>)    return {
    [](<https://adk.dev/sessions/memory/#__codelineno-32-16>)        "from_conversations": [
    [](<https://adk.dev/sessions/memory/#__codelineno-32-17>)            part.text
    [](<https://adk.dev/sessions/memory/#__codelineno-32-18>)            for entry in conversational.memories
    [](<https://adk.dev/sessions/memory/#__codelineno-32-19>)            for part in (entry.content.parts or [])
    [](<https://adk.dev/sessions/memory/#__codelineno-32-20>)            if part.text
    [](<https://adk.dev/sessions/memory/#__codelineno-32-21>)        ],
    [](<https://adk.dev/sessions/memory/#__codelineno-32-22>)        "from_docs": [
    [](<https://adk.dev/sessions/memory/#__codelineno-32-23>)            part.text
    [](<https://adk.dev/sessions/memory/#__codelineno-32-24>)            for entry in docs.memories
    [](<https://adk.dev/sessions/memory/#__codelineno-32-25>)            for part in (entry.content.parts or [])
    [](<https://adk.dev/sessions/memory/#__codelineno-32-26>)            if part.text
    [](<https://adk.dev/sessions/memory/#__codelineno-32-27>)        ],
    [](<https://adk.dev/sessions/memory/#__codelineno-32-28>)    }
    [](<https://adk.dev/sessions/memory/#__codelineno-32-29>)
    [](<https://adk.dev/sessions/memory/#__codelineno-32-30>)
    [](<https://adk.dev/sessions/memory/#__codelineno-32-31>)agent = Agent(
    [](<https://adk.dev/sessions/memory/#__codelineno-32-32>)    model="gemini-flash-latest",
    [](<https://adk.dev/sessions/memory/#__codelineno-32-33>)    name="multi_memory_agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-32-34>)    instruction=(
    [](<https://adk.dev/sessions/memory/#__codelineno-32-35>)        "Answer questions using both your conversation history and the "
    [](<https://adk.dev/sessions/memory/#__codelineno-32-36>)        "docs knowledge base. Use the search_all_memory tool."
    [](<https://adk.dev/sessions/memory/#__codelineno-32-37>)    ),
    [](<https://adk.dev/sessions/memory/#__codelineno-32-38>)    tools=[search_all_memory],
    [](<https://adk.dev/sessions/memory/#__codelineno-32-39>))
    
    [](<https://adk.dev/sessions/memory/#__codelineno-33-1>)/**
    [](<https://adk.dev/sessions/memory/#__codelineno-33-2>) * Example of using two memory services in Kotlin.
    [](<https://adk.dev/sessions/memory/#__codelineno-33-3>) */
    [](<https://adk.dev/sessions/memory/#__codelineno-33-4>)suspend fun searchAllMemory(
    [](<https://adk.dev/sessions/memory/#__codelineno-33-5>)    toolContext: ToolContext,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-6>)    query: String,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-7>)    docsMemory: InMemoryMemoryService,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-8>)): Map<String, List<String>> {
    [](<https://adk.dev/sessions/memory/#__codelineno-33-9>)    // Search the conversational memory (configured in the runner)
    [](<https://adk.dev/sessions/memory/#__codelineno-33-10>)    val conversational =
    [](<https://adk.dev/sessions/memory/#__codelineno-33-11>)        toolContext.invocationContext.memoryService?.searchMemory(
    [](<https://adk.dev/sessions/memory/#__codelineno-33-12>)            appName = toolContext.invocationContext.session.key.appName,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-13>)            userId = toolContext.invocationContext.session.key.userId,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-14>)            query = query,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-15>)        )
    [](<https://adk.dev/sessions/memory/#__codelineno-33-16>)
    [](<https://adk.dev/sessions/memory/#__codelineno-33-17>)    // Search a separate docs knowledge base
    [](<https://adk.dev/sessions/memory/#__codelineno-33-18>)    val docs =
    [](<https://adk.dev/sessions/memory/#__codelineno-33-19>)        docsMemory.searchMemory(
    [](<https://adk.dev/sessions/memory/#__codelineno-33-20>)            appName = "docs",
    [](<https://adk.dev/sessions/memory/#__codelineno-33-21>)            userId = "shared",
    [](<https://adk.dev/sessions/memory/#__codelineno-33-22>)            query = query,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-23>)        )
    [](<https://adk.dev/sessions/memory/#__codelineno-33-24>)
    [](<https://adk.dev/sessions/memory/#__codelineno-33-25>)    return mapOf(
    [](<https://adk.dev/sessions/memory/#__codelineno-33-26>)        "from_conversations" to
    [](<https://adk.dev/sessions/memory/#__codelineno-33-27>)            (
    [](<https://adk.dev/sessions/memory/#__codelineno-33-28>)                conversational?.memories?.map {
    [](<https://adk.dev/sessions/memory/#__codelineno-33-29>)                    it.content.parts.joinToString(" ") { p -> p.text ?: "" }
    [](<https://adk.dev/sessions/memory/#__codelineno-33-30>)                } ?: emptyList()
    [](<https://adk.dev/sessions/memory/#__codelineno-33-31>)            ),
    [](<https://adk.dev/sessions/memory/#__codelineno-33-32>)        "from_docs" to
    [](<https://adk.dev/sessions/memory/#__codelineno-33-33>)            docs.memories.map {
    [](<https://adk.dev/sessions/memory/#__codelineno-33-34>)                it.content.parts.joinToString(" ") { p -> p.text ?: "" }
    [](<https://adk.dev/sessions/memory/#__codelineno-33-35>)            },
    [](<https://adk.dev/sessions/memory/#__codelineno-33-36>)    )
    [](<https://adk.dev/sessions/memory/#__codelineno-33-37>)}
    [](<https://adk.dev/sessions/memory/#__codelineno-33-38>)
    [](<https://adk.dev/sessions/memory/#__codelineno-33-39>)fun multiMemoryAgent(model: Gemini) {
    [](<https://adk.dev/sessions/memory/#__codelineno-33-40>)    // docs_memory could be any MemoryService implementation
    [](<https://adk.dev/sessions/memory/#__codelineno-33-41>)    val docsMemory = InMemoryMemoryService()
    [](<https://adk.dev/sessions/memory/#__codelineno-33-42>)
    [](<https://adk.dev/sessions/memory/#__codelineno-33-43>)    val agent =
    [](<https://adk.dev/sessions/memory/#__codelineno-33-44>)        LlmAgent(
    [](<https://adk.dev/sessions/memory/#__codelineno-33-45>)            model = model,
    [](<https://adk.dev/sessions/memory/#__codelineno-33-46>)            name = "multi_memory_agent",
    [](<https://adk.dev/sessions/memory/#__codelineno-33-47>)            instruction =
    [](<https://adk.dev/sessions/memory/#__codelineno-33-48>)                Instruction(
    [](<https://adk.dev/sessions/memory/#__codelineno-33-49>)                    "Answer questions using both your conversation history and the " +
    [](<https://adk.dev/sessions/memory/#__codelineno-33-50>)                        "docs knowledge base. Use the search_all_memory tool.",
    [](<https://adk.dev/sessions/memory/#__codelineno-33-51>)                ),
    [](<https://adk.dev/sessions/memory/#__codelineno-33-52>)            // In a real app, you'd wrap searchAllMemory in a @Tool annotated class
    [](<https://adk.dev/sessions/memory/#__codelineno-33-53>)            // and pass docsMemory to its constructor.
    [](<https://adk.dev/sessions/memory/#__codelineno-33-54>)        )
    [](<https://adk.dev/sessions/memory/#__codelineno-33-55>)}
    
Back to top 