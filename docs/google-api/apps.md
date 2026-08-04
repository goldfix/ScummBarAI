# App workflow management class - Agent Development Kit (ADK)

> Source: [https://adk.dev/apps/](https://adk.dev/apps/)

[ Skip to content ](<https://adk.dev/apps/#app-workflow-management-class>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/apps/index.md> "Edit this page on GitHub") [ ](<https://adk.dev/apps/index.md> "View this page as Markdown")

# App workflow management class[¶](<https://adk.dev/apps/#app-workflow-management-class> "Permanent link")

Supported in ADKPython v1.14.0Java v0.1.0

The **_App_** class is a top-level container for an entire Agent Development Kit (ADK) agent workflow. It is designed to manage the lifecycle, configuration, and state for a collection of agents grouped by a **_root agent_**. The **App** class separates the concerns of an agent workflow's overall operational infrastructure from individual agents' task-oriented reasoning.

Defining an **_App_** object in your ADK workflow is optional and changes how you organize your agent code and run your agents. From a practical perspective, you use the **_App_** class to configure the following features for your agent workflow:

  * [**Context caching**](<https://adk.dev/context/caching/>)
  * [**Context compression**](<https://adk.dev/context/compaction/>)
  * [**Agent resume**](<https://adk.dev/runtime/resume/>)
  * [**Plugins**](<https://adk.dev/plugins/>)

This guide explains how to use the App class for configuring and managing your ADK agent workflows.

## Purpose of App Class[¶](<https://adk.dev/apps/#purpose-of-app-class> "Permanent link")

The **_App_** class addresses several architectural issues that arise when building complex agentic systems:

  * **Centralized configuration:** Provides a single, centralized location for managing shared resources like API keys and database clients, avoiding the need to pass configuration down through every agent.
  * **Lifecycle management:** The **_App_** class includes **_on startup_** and **_on shutdown_** hooks, which allow for reliable management of persistent resources such as database connection pools or in-memory caches that need to exist across multiple invocations.
  * **State scope:** It defines an explicit boundary for application-level state with an `app:*` prefix making the scope and lifetime of this state clear to developers.
  * **Unit of deployment:** The **_App_** concept establishes a formal _deployable unit_ , simplifying versioning, testing, and serving of agentic applications.

## Define an App object[¶](<https://adk.dev/apps/#define-an-app-object> "Permanent link")

The **_App_** class is used as the primary container of your agent workflow and contains the root agent of the project. The **_root agent_** is the container for the primary controller agent and any additional sub-agents.

### Define app with root agent[¶](<https://adk.dev/apps/#define-app-with-root-agent> "Permanent link")

Create a **_root agent_** for your workflow by creating a subclass from the **_Agent_** base class. Then define an **_App_** object and configure it with the **_root agent_** object and optional features, as shown in the following sample code:

PythonJava

agent.py
    
    [](<https://adk.dev/apps/#__codelineno-0-1>)from google.adk.agents.llm_agent import Agent
    [](<https://adk.dev/apps/#__codelineno-0-2>)from google.adk.apps import App
    [](<https://adk.dev/apps/#__codelineno-0-3>)
    [](<https://adk.dev/apps/#__codelineno-0-4>)root_agent = Agent(
    [](<https://adk.dev/apps/#__codelineno-0-5>)    model='gemini-flash-latest',
    [](<https://adk.dev/apps/#__codelineno-0-6>)    name='greeter_agent',
    [](<https://adk.dev/apps/#__codelineno-0-7>)    description='An agent that provides a friendly greeting.',
    [](<https://adk.dev/apps/#__codelineno-0-8>)    instruction='Reply with Hello, World!',
    [](<https://adk.dev/apps/#__codelineno-0-9>))
    [](<https://adk.dev/apps/#__codelineno-0-10>)
    [](<https://adk.dev/apps/#__codelineno-0-11>)app = App(
    [](<https://adk.dev/apps/#__codelineno-0-12>)    name="agents",
    [](<https://adk.dev/apps/#__codelineno-0-13>)    root_agent=root_agent,
    [](<https://adk.dev/apps/#__codelineno-0-14>)    # Optionally include App-level features:
    [](<https://adk.dev/apps/#__codelineno-0-15>)    # plugins, context_cache_config, resumability_config
    [](<https://adk.dev/apps/#__codelineno-0-16>))
    
AgentConfiguration.java
    
    [](<https://adk.dev/apps/#__codelineno-1-1>)import com.google.adk.agents.LlmAgent;
    [](<https://adk.dev/apps/#__codelineno-1-2>)import com.google.adk.apps.App;
    [](<https://adk.dev/apps/#__codelineno-1-3>)
    [](<https://adk.dev/apps/#__codelineno-1-4>)LlmAgent rootAgent = LlmAgent.builder()
    [](<https://adk.dev/apps/#__codelineno-1-5>)    .model("gemini-flash-latest")
    [](<https://adk.dev/apps/#__codelineno-1-6>)    .name("greeter_agent")
    [](<https://adk.dev/apps/#__codelineno-1-7>)    .description("An agent that provides a friendly greeting.")
    [](<https://adk.dev/apps/#__codelineno-1-8>)    .instruction("Reply with Hello, World!")
    [](<https://adk.dev/apps/#__codelineno-1-9>)    .build();
    [](<https://adk.dev/apps/#__codelineno-1-10>)
    [](<https://adk.dev/apps/#__codelineno-1-11>)App app = App.builder()
    [](<https://adk.dev/apps/#__codelineno-1-12>)    .name("agents")
    [](<https://adk.dev/apps/#__codelineno-1-13>)    .rootAgent(rootAgent)
    [](<https://adk.dev/apps/#__codelineno-1-14>)    // Optionally include App-level features:
    [](<https://adk.dev/apps/#__codelineno-1-15>)    // .plugins(plugins)
    [](<https://adk.dev/apps/#__codelineno-1-16>)    // .contextCacheConfig(contextCacheConfig)
    [](<https://adk.dev/apps/#__codelineno-1-17>)    // .eventsCompactionConfig(eventsCompactionConfig)
    [](<https://adk.dev/apps/#__codelineno-1-18>)    .build();
    
Recommended: Use `app` variable name

In your agent project code, set your **_App_** object to the variable name `app` so it is compatible with the ADK command line interface runner tools.

### Run your App agent[¶](<https://adk.dev/apps/#run-your-app-agent> "Permanent link")

You can use the **_Runner_** class to run your agent workflow using the `app` parameter, as shown in the following code sample:

PythonJava

main.py
    
    [](<https://adk.dev/apps/#__codelineno-2-1>)import asyncio
    [](<https://adk.dev/apps/#__codelineno-2-2>)from dotenv import load_dotenv
    [](<https://adk.dev/apps/#__codelineno-2-3>)from google.adk.runners import InMemoryRunner
    [](<https://adk.dev/apps/#__codelineno-2-4>)from agent import app # import code from agent.py
    [](<https://adk.dev/apps/#__codelineno-2-5>)
    [](<https://adk.dev/apps/#__codelineno-2-6>)load_dotenv() # load API keys and settings
    [](<https://adk.dev/apps/#__codelineno-2-7>)# Set a Runner using the imported application object
    [](<https://adk.dev/apps/#__codelineno-2-8>)runner = InMemoryRunner(app=app)
    [](<https://adk.dev/apps/#__codelineno-2-9>)
    [](<https://adk.dev/apps/#__codelineno-2-10>)async def main():
    [](<https://adk.dev/apps/#__codelineno-2-11>)    try:  # run_debug() requires ADK Python 1.18 or higher:
    [](<https://adk.dev/apps/#__codelineno-2-12>)        response = await runner.run_debug("Hello there!")
    [](<https://adk.dev/apps/#__codelineno-2-13>)
    [](<https://adk.dev/apps/#__codelineno-2-14>)    except Exception as e:
    [](<https://adk.dev/apps/#__codelineno-2-15>)        print(f"An error occurred during agent execution: {e}")
    [](<https://adk.dev/apps/#__codelineno-2-16>)
    [](<https://adk.dev/apps/#__codelineno-2-17>)if __name__ == "__main__":
    [](<https://adk.dev/apps/#__codelineno-2-18>)    asyncio.run(main())
    
AppMain.java
    
    [](<https://adk.dev/apps/#__codelineno-3-1>)import com.google.adk.agents.Content;
    [](<https://adk.dev/apps/#__codelineno-3-2>)import com.google.adk.runner.Runner;
    [](<https://adk.dev/apps/#__codelineno-3-3>)
    [](<https://adk.dev/apps/#__codelineno-3-4>)public class AppMain {
    [](<https://adk.dev/apps/#__codelineno-3-5>)
    [](<https://adk.dev/apps/#__codelineno-3-6>)  public static void main(String[] args) throws Exception {
    [](<https://adk.dev/apps/#__codelineno-3-7>)    // Set a Runner using the application object
    [](<https://adk.dev/apps/#__codelineno-3-8>)
    [](<https://adk.dev/apps/#__codelineno-3-9>)    App app = ...;
    [](<https://adk.dev/apps/#__codelineno-3-10>)
    [](<https://adk.dev/apps/#__codelineno-3-11>)    Runner runner = Runner.builder()
    [](<https://adk.dev/apps/#__codelineno-3-12>)        .app(app) // Use the 'app' object defined previously
    [](<https://adk.dev/apps/#__codelineno-3-13>)        .build();
    [](<https://adk.dev/apps/#__codelineno-3-14>)
    [](<https://adk.dev/apps/#__codelineno-3-15>)    runner.runAsync("user", "session-1", Content.fromParts(Part.fromText("Hello there!")))
    [](<https://adk.dev/apps/#__codelineno-3-16>)        .filter(event -> event.finalResponse() && event.content().isPresent())
    [](<https://adk.dev/apps/#__codelineno-3-17>)        .blockingSubscribe(event -> System.out.println("Response: " + event.stringifyContent()));
    [](<https://adk.dev/apps/#__codelineno-3-18>)  }
    [](<https://adk.dev/apps/#__codelineno-3-19>)}
    
Version requirement for `Runner.run_debug()`

The `Runner.run_debug()` command requires ADK Python v1.18.0 or higher. You can also use `Runner.run()`, which requires more setup code. For more details, see the

PythonJava

Run your App agent with the `main.py` code using the following command:
    
    [](<https://adk.dev/apps/#__codelineno-4-1>)python3 main.py
    
Run your App agent with the `AppMain.java` code using your build tool (e.g. Gradle `application` plugin):
    
    [](<https://adk.dev/apps/#__codelineno-5-1>)./gradlew run
    
## Next steps[¶](<https://adk.dev/apps/#next-steps> "Permanent link")

For a more complete sample code implementation, see the [Hello World App](<https://github.com/google/adk-python/tree/main/contributing/samples/core/app>) code example.

Back to top 