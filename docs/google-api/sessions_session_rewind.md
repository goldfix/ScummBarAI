# Rewind sessions - Agent Development Kit (ADK)

> Source: [https://adk.dev/sessions/session/rewind/](https://adk.dev/sessions/session/rewind/)

[ Skip to content ](<https://adk.dev/sessions/session/rewind/#rewind-sessions-for-agents>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/sessions/session/rewind.md> "Edit this page on GitHub") [ ](<https://adk.dev/sessions/session/rewind/index.md> "View this page as Markdown")

# Rewind sessions for agents[¶](<https://adk.dev/sessions/session/rewind/#rewind-sessions-for-agents> "Permanent link")

Supported in ADKPython v1.17.0

The ADK session Rewind feature allows you to revert a session to a previous request state, enabling you to undo mistakes, explore alternative paths, or restart a process from a known good point. This document provides an overview of the feature, how to use it, and its limitations.

## Rewind a session[¶](<https://adk.dev/sessions/session/rewind/#rewind-a-session> "Permanent link")

When you rewind a session, you specify a user request, or **_invocation_** , that you want to undo, and the system undoes that request and the requests after it. So if you have three requests (A, B, C) and you want to return to the state at request A, you specify B, which undoes the changes from requests B and C. You rewind a session by using the rewind method on a **_Runner_** instance, specifying the user, session, and invocation id, as shown in the following code snippet:
    
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-1>)# Create runner
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-2>)runner = InMemoryRunner(
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-3>)    agent=agent.root_agent,
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-4>)    app_name=APP_NAME,
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-5>))
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-6>)
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-7>)# Create a session
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-8>)session = await runner.session_service.create_session(
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-9>)    app_name=APP_NAME, user_id=USER_ID
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-10>))
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-11>)# call agent with wrapper function "call_agent_async()"
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-12>)await call_agent_async(
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-13>)    runner, USER_ID, session.id, "set state color to red"
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-14>))
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-15>)# ... more agent calls ...
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-16>)events_list = await call_agent_async(
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-17>)    runner, USER_ID, session.id, "update state color to blue"
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-18>))
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-19>)
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-20>)# get invocation id
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-21>)rewind_invocation_id=events_list[1].invocation_id
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-22>)
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-23>)# rewind invocations (state color: red)
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-24>)await runner.rewind_async(
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-25>)    user_id=USER_ID,
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-26>)    session_id=session.id,
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-27>)    rewind_before_invocation_id=rewind_invocation_id,
    [](<https://adk.dev/sessions/session/rewind/#__codelineno-0-28>))
    
When you call the **_rewind_** method, all ADK managed session-level resources are restored to the state they were in _before_ the request you specified with the **_invocation id_**. However, global resources, such as app-level or user-level state and artifacts, are not restored. For a complete example of an agent session rewind, see the [rewind_session](<https://github.com/google/adk-python/tree/main/contributing/samples/context_management/rewind_session>) sample code. For more information on the limitations of the Rewind feature, see [Limitations](<https://adk.dev/sessions/session/rewind/#limitations>).

## How it works[¶](<https://adk.dev/sessions/session/rewind/#how-it-works> "Permanent link")

The Rewind feature creates a special **_rewind_** request that restores the session's state and artifacts to their condition _before_ the rewind point specified by an invocation id. This approach means that all requests, including rewound requests, are preserved in the log for later debugging, analysis, or auditing. After the rewind, the system ignores the rewound requests when it prepares the next requests for the AI model. This behavior means the AI model used by the agent effectively forgets any interactions from the rewind point up to the next request.

## Limitations[¶](<https://adk.dev/sessions/session/rewind/#limitations> "Permanent link")

The Rewind feature has some limitations that you should be aware of when using it with your agent workflow:

  * **Global agent resources:** App-level and user-level state and artifacts are _not_ restored by the rewind feature. Only session-level state and artifacts are restored.
  * **External dependencies:** The rewind feature does not manage external dependencies. If a tool in your agent interacts with external systems, it is your responsibility to handle the restoration of those systems to their prior state.
  * **Atomicity:** State updates, artifact updates, and event persistence are not performed in a single atomic transaction. Therefore, you should avoid rewinding active sessions or concurrently manipulating session artifacts during a rewind to prevent inconsistencies.

Back to top 