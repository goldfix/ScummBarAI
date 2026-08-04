# Introduction to A2A - Agent Development Kit (ADK)

> Source: [https://adk.dev/a2a/intro/](https://adk.dev/a2a/intro/)

[ Skip to content ](<https://adk.dev/a2a/intro/#introduction-to-a2a>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/a2a/intro.md> "Edit this page on GitHub") [ ](<https://adk.dev/a2a/intro/index.md> "View this page as Markdown")

# Introduction to A2A[¶](<https://adk.dev/a2a/intro/#introduction-to-a2a> "Permanent link")

As you build more complex agentic systems, you will find that a single agent is often not enough. You will want to create specialized agents that can collaborate to solve a problem. The [**Agent2Agent (A2A) Protocol**](<https://a2a-protocol.org>) is the standard that allows these agents to communicate with each other.

## When to use A2A vs. local sub-agents[¶](<https://adk.dev/a2a/intro/#when-to-use-a2a-vs-local-sub-agents> "Permanent link")

  * **Local Sub-Agents:** These are agents that run _within the same application process_ as your main agent. They are like internal modules or libraries, used to organize your code into logical, reusable components. Communication between a main agent and its local sub-agents is very fast because it happens directly in memory, without network overhead.

  * **Remote Agents (A2A):** These are independent agents that run as separate services, communicating over a network. A2A defines the standard protocol for this communication.

Consider using **A2A** when:

  * The agent you need to talk to is a **separate, standalone service** (e.g., a specialized financial modeling agent).
  * The agent is maintained by a **different team or organization**.
  * You need to connect agents written in **different programming languages or agent frameworks**.
  * You want to enforce a **strong, formal contract** (the A2A protocol) between your system's components.

### When to use A2A: concrete examples[¶](<https://adk.dev/a2a/intro/#when-to-use-a2a-concrete-examples> "Permanent link")

  * **Integrating with a Third-Party Service:** Your main agent needs to get real-time stock prices from an external financial data provider. This provider exposes its data through an A2A-compatible agent.
  * **Microservices Architecture:** You have a large system broken down into smaller, independent services (e.g., an Order Processing Agent, an Inventory Management Agent, a Shipping Agent). A2A is ideal for these services to communicate with each other across network boundaries.
  * **Cross-Language Communication:** Your core business logic is in a Python agent, but you have a legacy system or a specialized component written in Java that you want to integrate as an agent. A2A provides the standardized communication layer.
  * **Formal API Enforcement:** You are building a platform where different teams contribute agents, and you need a strict contract for how these agents interact to ensure compatibility and stability.

### When NOT to use A2A: concrete examples (prefer local sub-agents)[¶](<https://adk.dev/a2a/intro/#when-not-to-use-a2a-concrete-examples-prefer-local-sub-agents> "Permanent link")

  * **Internal Code Organization:** You are breaking down a complex task within a single agent into smaller, manageable functions or modules (e.g., a `DataValidator` sub-agent that cleans input data before processing). These are best handled as local sub-agents for performance and simplicity.
  * **Performance-Critical Internal Operations:** A sub-agent is responsible for a high-frequency, low-latency operation that is tightly coupled with the main agent's execution (e.g., a `RealTimeAnalytics` sub-agent that processes data streams within the same application).
  * **Shared Memory/Context:** When sub-agents need direct access to the main agent's internal state or shared memory for efficiency, A2A's network overhead and serialization/deserialization would be counterproductive.
  * **Simple Helper Functions:** For small, reusable pieces of logic that don't require independent deployment or complex state management, a simple function or class within the same agent is more appropriate than a separate A2A agent.

## The A2A workflow in ADK: a simplified view[¶](<https://adk.dev/a2a/intro/#the-a2a-workflow-in-adk-a-simplified-view> "Permanent link")

Agent Development Kit (ADK) simplifies the process of building and connecting agents using the A2A protocol. Here's a straightforward breakdown of how it works:

  1. **Making an Agent Accessible (Exposing):** You start with an existing ADK agent that you want other agents to be able to interact with. ADK provides a simple way to "expose" this agent, turning it into an **A2AServer**. This server acts as a public interface, allowing other agents to send requests to your agent over a network. Think of it like setting up a web server for your agent.

  2. **Connecting to an Accessible Agent (Consuming):** In a separate agent (which could be running on the same machine or a different one), you'll use a special ADK component called `RemoteA2aAgent`. This `RemoteA2aAgent` acts as a client that knows how to communicate with the **A2AServer** you exposed earlier. It handles all the complexities of network communication, authentication, and data formatting behind the scenes.

From your perspective as a developer, once you've set up this connection, interacting with the remote agent feels just like interacting with a local tool or function. ADK abstracts away the network layer, making distributed agent systems as easy to work with as local ones.

## Supported capabilities in A2A[¶](<https://adk.dev/a2a/intro/#supported-capabilities-in-a2a> "Permanent link")

ADK's A2A integration provides three core capabilities for complex agentic systems:

  * **Reasoning:** Preserves a model's reasoning/thought traces when messages pass between agents over A2A.
  * **Long-Running Tools:** Tracks tool calls that run longer than a standard response, so long-running operations don't time out.
  * **Artifacts:** Passes file artifacts (such as generated files) between agents over A2A.

## Visualizing the A2A workflow[¶](<https://adk.dev/a2a/intro/#visualizing-the-a2a-workflow> "Permanent link")

To further clarify the A2A workflow, let's look at the "before and after" for both exposing and consuming agents, and then the combined system.

### Exposing an agent[¶](<https://adk.dev/a2a/intro/#exposing-an-agent> "Permanent link")

**Before Exposing:** Your agent code runs as a standalone component, but in this scenario, you want to expose it so that other remote agents can interact with your agent.
    
    [](<https://adk.dev/a2a/intro/#__codelineno-0-1>)+-------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-0-2>)| Your Agent Code   |
    [](<https://adk.dev/a2a/intro/#__codelineno-0-3>)|   (Standalone)    |
    [](<https://adk.dev/a2a/intro/#__codelineno-0-4>)+-------------------+
    
**After Exposing:** Your agent code is integrated with an `A2AServer` (an ADK component), making it accessible over a network to other remote agents.
    
    [](<https://adk.dev/a2a/intro/#__codelineno-1-1>)+-----------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-1-2>)|   A2A Server    |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-3>)| (ADK Component) |<--------+
    [](<https://adk.dev/a2a/intro/#__codelineno-1-4>)+-----------------+         |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-5>)        |                   |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-6>)        v                   |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-7>)+-------------------+       |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-8>)| Your Agent Code   |       |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-9>)| (Now Accessible)  |       |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-10>)+-------------------+       |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-11>)                            |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-12>)                            | (Network Communication)
    [](<https://adk.dev/a2a/intro/#__codelineno-1-13>)                            v
    [](<https://adk.dev/a2a/intro/#__codelineno-1-14>)+-----------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-1-15>)|       Remote Agent(s)       |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-16>)|    (Can now communicate)    |
    [](<https://adk.dev/a2a/intro/#__codelineno-1-17>)+-----------------------------+
    
### Consuming an agent[¶](<https://adk.dev/a2a/intro/#consuming-an-agent> "Permanent link")

**Before Consuming:** Your agent (referred to as the "Root Agent" in this context) is the application you are developing that needs to interact with a remote agent. Before consuming, it lacks the direct mechanism to do so.
    
    [](<https://adk.dev/a2a/intro/#__codelineno-2-1>)+----------------------+         +-------------------------------------------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-2-2>)|      Root Agent      |         |                        Remote Agent                         |
    [](<https://adk.dev/a2a/intro/#__codelineno-2-3>)| (Your existing code) |         | (External Service that you want your Root Agent to talk to) |
    [](<https://adk.dev/a2a/intro/#__codelineno-2-4>)+----------------------+         +-------------------------------------------------------------+
    
**After Consuming:** Your Root Agent uses a `RemoteA2aAgent` (an ADK component that acts as a client-side proxy for the remote agent) to establish communication with the remote agent.
    
    [](<https://adk.dev/a2a/intro/#__codelineno-3-1>)+----------------------+         +-----------------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-3-2>)|      Root Agent      |         |         RemoteA2aAgent            |
    [](<https://adk.dev/a2a/intro/#__codelineno-3-3>)| (Your existing code) |<------->|         (ADK Client Proxy)        |
    [](<https://adk.dev/a2a/intro/#__codelineno-3-4>)+----------------------+         |                                   |
    [](<https://adk.dev/a2a/intro/#__codelineno-3-5>)                                 |  +-----------------------------+  |
    [](<https://adk.dev/a2a/intro/#__codelineno-3-6>)                                 |  |         Remote Agent        |  |
    [](<https://adk.dev/a2a/intro/#__codelineno-3-7>)                                 |  |      (External Service)     |  |
    [](<https://adk.dev/a2a/intro/#__codelineno-3-8>)                                 |  +-----------------------------+  |
    [](<https://adk.dev/a2a/intro/#__codelineno-3-9>)                                 +-----------------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-3-10>)      (Now talks to remote agent via RemoteA2aAgent)
    
### Final system (combined view)[¶](<https://adk.dev/a2a/intro/#final-system-combined-view> "Permanent link")

This diagram shows how the consuming and exposing parts connect to form a complete A2A system.
    
    [](<https://adk.dev/a2a/intro/#__codelineno-4-1>)Consuming Side:
    [](<https://adk.dev/a2a/intro/#__codelineno-4-2>)+----------------------+         +-----------------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-4-3>)|      Root Agent      |         |         RemoteA2aAgent            |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-4>)| (Your existing code) |<------->|         (ADK Client Proxy)        |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-5>)+----------------------+         |                                   |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-6>)                                 |  +-----------------------------+  |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-7>)                                 |  |         Remote Agent        |  |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-8>)                                 |  |      (External Service)     |  |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-9>)                                 |  +-----------------------------+  |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-10>)                                 +-----------------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-4-11>)                                                 |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-12>)                                                 | (Network Communication)
    [](<https://adk.dev/a2a/intro/#__codelineno-4-13>)                                                 v
    [](<https://adk.dev/a2a/intro/#__codelineno-4-14>)Exposing Side:
    [](<https://adk.dev/a2a/intro/#__codelineno-4-15>)                                               +-----------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-4-16>)                                               |   A2A Server    |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-17>)                                               | (ADK Component) |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-18>)                                               +-----------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-4-19>)                                                       |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-20>)                                                       v
    [](<https://adk.dev/a2a/intro/#__codelineno-4-21>)                                               +-------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-4-22>)                                               | Your Agent Code   |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-23>)                                               | (Exposed Service) |
    [](<https://adk.dev/a2a/intro/#__codelineno-4-24>)                                               +-------------------+
    
## Concrete use case: customer service and product catalog agents[¶](<https://adk.dev/a2a/intro/#concrete-use-case-customer-service-and-product-catalog-agents> "Permanent link")

Let's consider a practical example: a **Customer Service Agent** that needs to retrieve product information from a separate **Product Catalog Agent**.

### Before A2A[¶](<https://adk.dev/a2a/intro/#before-a2a> "Permanent link")

Initially, your Customer Service Agent might not have a direct, standardized way to query the Product Catalog Agent, especially if it's a separate service or managed by a different team.
    
    [](<https://adk.dev/a2a/intro/#__codelineno-5-1>)+-------------------------+         +--------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-5-2>)| Customer Service Agent  |         |  Product Catalog Agent   |
    [](<https://adk.dev/a2a/intro/#__codelineno-5-3>)| (Needs Product Info)    |         | (Contains Product Data)  |
    [](<https://adk.dev/a2a/intro/#__codelineno-5-4>)+-------------------------+         +--------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-5-5>)      (No direct, standardized communication)
    
### After A2A[¶](<https://adk.dev/a2a/intro/#after-a2a> "Permanent link")

By using the A2A Protocol, the Product Catalog Agent can expose its functionality as an A2A service. Your Customer Service Agent can then easily consume this service using ADK's `RemoteA2aAgent`.
    
    [](<https://adk.dev/a2a/intro/#__codelineno-6-1>)+-------------------------+         +-----------------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-6-2>)| Customer Service Agent  |         |         RemoteA2aAgent            |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-3>)| (Your Root Agent)       |<------->|         (ADK Client Proxy)        |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-4>)+-------------------------+         |                                   |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-5>)                                    |  +-----------------------------+  |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-6>)                                    |  |     Product Catalog Agent   |  |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-7>)                                    |  |      (External Service)     |  |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-8>)                                    |  +-----------------------------+  |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-9>)                                    +-----------------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-6-10>)                                                 |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-11>)                                                 | (Network Communication)
    [](<https://adk.dev/a2a/intro/#__codelineno-6-12>)                                                 v
    [](<https://adk.dev/a2a/intro/#__codelineno-6-13>)                                               +-----------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-6-14>)                                               |   A2A Server    |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-15>)                                               | (ADK Component) |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-16>)                                               +-----------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-6-17>)                                                       |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-18>)                                                       v
    [](<https://adk.dev/a2a/intro/#__codelineno-6-19>)                                               +------------------------+
    [](<https://adk.dev/a2a/intro/#__codelineno-6-20>)                                               | Product Catalog Agent  |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-21>)                                               | (Exposed Service)      |
    [](<https://adk.dev/a2a/intro/#__codelineno-6-22>)                                               +------------------------+
    
In this setup, first, the Product Catalog Agent needs to be exposed via an A2A Server. Then, the Customer Service Agent can simply call methods on the `RemoteA2aAgent` as if it were a tool, and the ADK handles all the underlying communication to the Product Catalog Agent. This allows for clear separation of concerns and easy integration of specialized agents.

## Next steps[¶](<https://adk.dev/a2a/intro/#next-steps> "Permanent link")

Now that you understand the "why" of A2A, let's dive into the "how."

  * **Continue to the next guide:** Quickstart: Exposing Your Agent, [in Python](<https://adk.dev/a2a/quickstart-exposing/>), [in Go](<https://adk.dev/a2a/quickstart-exposing-go/>), [in Java](<https://adk.dev/a2a/quickstart-exposing-java/>)

Back to top 