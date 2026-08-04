# Tool performance - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools-custom/performance/](https://adk.dev/tools-custom/performance/)

[ Skip to content ](<https://adk.dev/tools-custom/performance/#increase-tool-performance-with-parallel-execution>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools-custom/performance.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools-custom/performance/index.md> "View this page as Markdown")

# Increase tool performance with parallel execution[¶](<https://adk.dev/tools-custom/performance/#increase-tool-performance-with-parallel-execution> "Permanent link")

Supported in ADKPython v1.10.0

Starting with Agent Development Kit (ADK) version 1.10.0 for Python, the framework attempts to run any agent-requested [function tools](<https://adk.dev/tools-custom/function-tools/>) in parallel. This behavior can significantly improve the performance and responsiveness of your agents, particularly for agents that rely on multiple external APIs or long-running tasks. For example, if you have 3 tools that each take 2 seconds, by running them in parallel, the total execution time will be closer to 2 seconds, instead of 6 seconds. The ability to run tool functions parallel can improve the performance of your agents, particularly in the following scenarios:

  * **Research tasks:** Where the agent collects information from multiple sources before proceeding to the next stage of the workflow.
  * **API calls:** Where the agent accesses several APIs independently, such as searching for available flights using APIs from multiple airlines.
  * **Publishing and communication tasks:** When the agent needs to publish or communicate through multiple, independent channels or multiple recipients.

However, your custom tools must be built with asynchronous execution support to enable this performance improvement. This guide explains how parallel tool execution works in the ADK and how to build your tools to take full advantage of this processing feature.

Warning

Any ADK Tools that use synchronous processing in a set of tool function calls will block other tools from executing in parallel, even if the other tools allow for parallel execution.

## Build parallel-ready tools[¶](<https://adk.dev/tools-custom/performance/#build-parallel-ready-tools> "Permanent link")

Enable parallel execution of your tool functions by defining them as asynchronous functions. In Python code, this means using `async def` and `await` syntax which allows the ADK to run them concurrently in an `asyncio` event loop. The following sections show examples of agent tools built for parallel processing and asynchronous operations.

### Example of http web call[¶](<https://adk.dev/tools-custom/performance/#example-of-http-web-call> "Permanent link")

The following code example show how to modify the `get_weather()` function to operate asynchronously and allow for parallel execution:
    
    [](<https://adk.dev/tools-custom/performance/#__codelineno-0-1>) async def get_weather(city: str) -> dict:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-0-2>)      async with aiohttp.ClientSession() as session:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-0-3>)          async with session.get(f"http://api.weather.com/{city}") as response:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-0-4>)              return await response.json()
    
### Example of database call[¶](<https://adk.dev/tools-custom/performance/#example-of-database-call> "Permanent link")

The following code example show how to write a database calling function to operate asynchronously:
    
    [](<https://adk.dev/tools-custom/performance/#__codelineno-1-1>)async def query_database(query: str) -> list:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-1-2>)      async with asyncpg.connect("postgresql://...") as conn:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-1-3>)          return await conn.fetch(query)
    
### Example of yielding behavior for long loops[¶](<https://adk.dev/tools-custom/performance/#example-of-yielding-behavior-for-long-loops> "Permanent link")

In cases where a tool is processing multiple requests or numerous long-running requests, consider adding yielding code to allow other tools to execute, as shown in the following code sample:
    
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-1>)async def process_data(data: list) -> dict:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-2>)      results = []
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-3>)      for i, item in enumerate(data):
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-4>)          processed = await process_item(item)  # Yield point
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-5>)          results.append(processed)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-6>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-7>)          # Add periodic yield points for long loops
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-8>)          if i % 100 == 0:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-9>)              await asyncio.sleep(0)  # Yield control
    [](<https://adk.dev/tools-custom/performance/#__codelineno-2-10>)      return {"results": results}
    
Important

Use the `asyncio.sleep()` function for pauses to avoid blocking execution of other functions.

### Example of thread pools for intensive operations[¶](<https://adk.dev/tools-custom/performance/#example-of-thread-pools-for-intensive-operations> "Permanent link")

When performing processing-intensive functions, consider creating thread pools for better management of available computing resources, as shown in the following example:
    
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-1>)async def cpu_intensive_tool(data: list) -> dict:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-2>)      loop = asyncio.get_event_loop()
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-3>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-4>)      # Use thread pool for CPU-bound work
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-5>)      with ThreadPoolExecutor() as executor:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-6>)          result = await loop.run_in_executor(
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-7>)              executor,
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-8>)              expensive_computation,
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-9>)              data
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-10>)          )
    [](<https://adk.dev/tools-custom/performance/#__codelineno-3-11>)      return {"result": result}
    
### Example of process chunking[¶](<https://adk.dev/tools-custom/performance/#example-of-process-chunking> "Permanent link")

When performing processes on long lists or large amounts of data, consider combining a thread pool technique with dividing up processing into chunks of data, and yielding processing time between the chunks, as shown in the following example:
    
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-1>) async def process_large_dataset(dataset: list) -> dict:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-2>)      results = []
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-3>)      chunk_size = 1000
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-4>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-5>)      for i in range(0, len(dataset), chunk_size):
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-6>)          chunk = dataset[i:i + chunk_size]
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-7>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-8>)          # Process chunk in thread pool
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-9>)          loop = asyncio.get_event_loop()
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-10>)          with ThreadPoolExecutor() as executor:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-11>)              chunk_result = await loop.run_in_executor(
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-12>)                  executor, process_chunk, chunk
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-13>)              )
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-14>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-15>)          results.extend(chunk_result)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-16>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-17>)          # Yield control between chunks
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-18>)          await asyncio.sleep(0)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-19>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-4-20>)      return {"total_processed": len(results), "results": results}
    
## Write parallel-ready prompts and tool descriptions[¶](<https://adk.dev/tools-custom/performance/#write-parallel-ready-prompts-and-tool-descriptions> "Permanent link")

When building prompts for AI models, consider explicitly specifying or hinting that function calls be made in parallel. The following example of an AI prompt directs the model to use tools in parallel:
    
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-1>)When users ask for multiple pieces of information, always call functions in
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-2>)parallel.
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-3>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-4>)  Examples:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-5>)  - "Get weather for London and currency rate USD to EUR" → Call both functions
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-6>)    simultaneously
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-7>)  - "Compare cities A and B" → Call get_weather, get_population, get_distance in
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-8>)    parallel
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-9>)  - "Analyze multiple stocks" → Call get_stock_price for each stock in parallel
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-10>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-5-11>)  Always prefer multiple specific function calls over single complex calls.
    
The following example shows a tool function description that hints at more efficient use through parallel execution:
    
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-1>) async def get_weather(city: str) -> dict:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-2>)      """Get current weather for a single city.
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-3>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-4>)      This function is optimized for parallel execution - call multiple times for different cities.
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-5>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-6>)      Args:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-7>)          city: Name of the city, for example: 'London', 'New York'
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-8>)
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-9>)      Returns:
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-10>)          Weather data including temperature, conditions, humidity
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-11>)      """
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-12>)      await asyncio.sleep(2)  # Simulate API call
    [](<https://adk.dev/tools-custom/performance/#__codelineno-6-13>)      return {"city": city, "temp": 72, "condition": "sunny"}
    
## Next steps[¶](<https://adk.dev/tools-custom/performance/#next-steps> "Permanent link")

For more information on building Tools for agents and function calling, see [Function Tools](<https://adk.dev/tools-custom/function-tools/>). For more detailed examples of tools that take advantage of parallel processing, see the samples in the [adk-python](<https://github.com/google/adk-python/tree/main/contributing/samples/tools/parallel_functions>) repository.

Back to top 