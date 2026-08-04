# Test deployed agents - Agent Development Kit (ADK)

> Source: [https://adk.dev/deploy/agent-runtime/test/](https://adk.dev/deploy/agent-runtime/test/)

[ Skip to content ](<https://adk.dev/deploy/agent-runtime/test/#test-deployed-agents-in-agent-runtime>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/deploy/agent-runtime/test.md> "Edit this page on GitHub") [ ](<https://adk.dev/deploy/agent-runtime/test/index.md> "View this page as Markdown")

# Test deployed agents in Agent Runtime[¶](<https://adk.dev/deploy/agent-runtime/test/#test-deployed-agents-in-agent-runtime> "Permanent link")

Supported in ADKPythonGo v1.2.0

These instructions explain how to test an ADK agent deployed to the [Agent Runtime](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview>) runtime environment. Before using these instructions, you need to have completed the deployment of your agent to the Agent Runtime runtime environment using one of the [available methods](<https://adk.dev/deploy/agent-runtime/>). This guide shows you how to view, interact, and test your deployed agent through the Google Cloud Console, and interact with the agent using REST API calls or the Agent Platform SDK for Python.

## View deployed agent in Cloud Console[¶](<https://adk.dev/deploy/agent-runtime/test/#view-deployed-agent-in-cloud-console> "Permanent link")

To view your deployed agent in the Cloud Console:

  * Navigate to the Agent Runtime page in the Google Cloud Console: <https://console.cloud.google.com/vertex-ai/agents/agent-engines>

This page lists all deployed agents in your currently selected Google Cloud project. If you do not see your agent listed, make sure you have your target project selected in Google Cloud Console. For more information on selecting an existing Google Cloud project, see [Creating and managing projects](<https://cloud.google.com/resource-manager/docs/creating-managing-projects#identifying_projects>).

## Find Google Cloud project information[¶](<https://adk.dev/deploy/agent-runtime/test/#find-google-cloud-project-information> "Permanent link")

You need the address and resource identification for your project (`PROJECT_ID`, `LOCATION_ID`, `RESOURCE_ID`) to be able to test your deployment. You can use Cloud Console or the `gcloud` command line tool to find this information.

Agent Platform express mode API key

If you are using Agent Platform express mode, you can skip this step and use your API key.

To find your project information with Google Cloud Console:

  1. In the Google Cloud Console, navigate to the Agent Runtime page: <https://console.cloud.google.com/vertex-ai/agents/agent-engines>

  2. Choose the instance you want to view.

  3. At the top of the page, select **Copy query URL** , which should be in this format:
         
         https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines/$(RESOURCE_ID):query
         
To find your project information with the `gcloud` command line tool:

  1. In your development environment, make sure you are authenticated to Google Cloud and run the following command to list your project:
         
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-0-1>)gcloud projects list
         
  2. With the Project ID you used for deployment, run this command to get the additional details:
         
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-1-1>)gcloud asset search-all-resources \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-1-2>)    --scope=projects/$(PROJECT_ID) \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-1-3>)    --asset-types='aiplatform.googleapis.com/ReasoningEngine' \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-1-4>)    --format="table(name,assetType,location,reasoning_engine_id)"
         
## Test using REST calls[¶](<https://adk.dev/deploy/agent-runtime/test/#test-using-rest-calls> "Permanent link")

A simple way to interact with your deployed agent in Agent Runtime is to use REST calls with the `curl` tool. This section describes how to check your connection to the agent and also to test processing of a request by the deployed agent.

### Check connection to agent[¶](<https://adk.dev/deploy/agent-runtime/test/#check-connection-to-agent> "Permanent link")

You can check your connection to the running agent using the **Query URL** available in the Agent Runtime section of the Cloud Console. This check does not execute the deployed agent, but returns information about the agent.

To send a REST call and get a response from deployed agent:

  * In a terminal window of your development environment, build a request and execute it:

Google Cloud ProjectAgent Platform express mode
        
        [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-2-1>)curl -X GET \
        [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-2-2>)    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
        [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-2-3>)    "https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines"
        
        [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-3-1>)curl -X GET \
        [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-3-2>)    -H "x-goog-api-key:YOUR-EXPRESS-MODE-API-KEY" \
        [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-3-3>)    "https://aiplatform.googleapis.com/v1/reasoningEngines"
        
If your deployment was successful, this request responds with a list of valid requests and expected data formats.

Remove `:query` parameter for connection URL

If you use the **Query URL** available in the Agent Runtime section of the Cloud Console, make sure to remove the `:query` parameter from end of the address.

Access for agent connections

This connection test requires the calling user has a valid access token for the deployed agent. When testing from other environments, make sure the calling user has access to connect to the agent in your Google Cloud project.

### Send an agent request[¶](<https://adk.dev/deploy/agent-runtime/test/#send-an-agent-request> "Permanent link")

When getting responses from your agent project, you must first create a session, receive a Session ID, and then send your requests using that Session ID. This process is described in the following instructions.

To test interaction with the deployed agent via REST:

  1. In a terminal window of your development environment, create a session by building a request using this template:

Google Cloud ProjectAgent Platform express mode
         
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-4-1>)curl \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-4-2>)    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-4-3>)    -H "Content-Type: application/json" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-4-4>)    https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines/$(RESOURCE_ID):query \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-4-5>)    -d '{"class_method": "async_create_session", "input": {"user_id": "u_123"},}'
         
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-5-1>)curl \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-5-2>)    -H "x-goog-api-key:YOUR-EXPRESS-MODE-API-KEY" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-5-3>)    -H "Content-Type: application/json" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-5-4>)    https://aiplatform.googleapis.com/v1/reasoningEngines/$(RESOURCE_ID):query \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-5-5>)    -d '{"class_method": "async_create_session", "input": {"user_id": "u_123"},}'
         
  2. In the response from the previous command, extract the created **Session ID** from the **id** field:
         
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-1>){
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-2>)    "output": {
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-3>)        "userId": "u_123",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-4>)        "lastUpdateTime": 1757690426.337745,
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-5>)        "state": {},
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-6>)        "id": "4857885913439920384", # Session ID
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-7>)        "appName": "9888888855577777776",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-8>)        "events": []
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-9>)    }
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-6-10>)}
         
  3. In a terminal window of your development environment, send a message to your agent by building a request using this template and the Session ID created in the previous step:

Google Cloud ProjectAgent Platform express mode
         
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-1>)curl \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-2>)-H "Authorization: Bearer $(gcloud auth print-access-token)" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-3>)-H "Content-Type: application/json" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-4>)https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines/$(RESOURCE_ID):streamQuery?alt=sse -d '{
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-5>)"class_method": "async_stream_query",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-6>)"input": {
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-7>)    "user_id": "u_123",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-8>)    "session_id": "4857885913439920384",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-9>)    "message": "Hey whats the weather in new york today?",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-10>)}
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-7-11>)}'
         
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-1>)curl \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-2>)-H "x-goog-api-key:YOUR-EXPRESS-MODE-API-KEY" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-3>)-H "Content-Type: application/json" \
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-4>)https://aiplatform.googleapis.com/v1/reasoningEngines/$(RESOURCE_ID):streamQuery?alt=sse -d '{
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-5>)"class_method": "async_stream_query",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-6>)"input": {
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-7>)    "user_id": "u_123",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-8>)    "session_id": "4857885913439920384",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-9>)    "message": "Hey whats the weather in new york today?",
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-10>)}
         [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-8-11>)}'
         
This request should generate a response from your deployed agent code in JSON format. For more information about interacting with a deployed ADK agent in Agent Runtime using REST calls, see [Manage deployed agents](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/manage/overview#console>) and [Use an Agent Development Kit agent](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/adk>) in the Agent Runtime documentation.

## Test using Python[¶](<https://adk.dev/deploy/agent-runtime/test/#test-using-python> "Permanent link")

You can use Python code for more sophisticated and repeatable testing of your agent deployed in Agent Runtime. These instructions describe how to create a session with the deployed agent, and then send a request to the agent for processing.

### Create a remote session[¶](<https://adk.dev/deploy/agent-runtime/test/#create-a-remote-session> "Permanent link")

Use the `remote_app` object to create a connection to a deployed, remote agent:
    
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-9-1>)# If you are in a new script or used the ADK CLI to deploy, you can connect like this:
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-9-2>)# remote_app = agent_engines.get("your-agent-resource-name")
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-9-3>)remote_session = await remote_app.async_create_session(user_id="u_456")
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-9-4>)print(remote_session)
    
Expected output for `create_session` (remote):
    
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-10-1>){'events': [],
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-10-2>)'user_id': 'u_456',
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-10-3>)'state': {},
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-10-4>)'id': '7543472750996750336',
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-10-5>)'app_name': '7917477678498709504',
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-10-6>)'last_update_time': 1743683353.030133}
    
The `id` value is the session ID, and `app_name` is the resource ID of the deployed agent on Agent Runtime.

#### Send queries to your remote agent[¶](<https://adk.dev/deploy/agent-runtime/test/#send-queries-to-your-remote-agent> "Permanent link")
    
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-11-1>)async for event in remote_app.async_stream_query(
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-11-2>)    user_id="u_456",
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-11-3>)    session_id=remote_session["id"],
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-11-4>)    message="whats the weather in new york",
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-11-5>)):
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-11-6>)    print(event)
    
Expected output for `async_stream_query` (remote):
    
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-12-1>){'parts': [{'function_call': {'id': 'af-f1906423-a531-4ecf-a1ef-723b05e85321', 'args': {'city': 'new york'}, 'name': 'get_weather'}}], 'role': 'model'}
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-12-2>){'parts': [{'function_response': {'id': 'af-f1906423-a531-4ecf-a1ef-723b05e85321', 'name': 'get_weather', 'response': {'status': 'success', 'report': 'The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit).'}}}], 'role': 'user'}
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-12-3>){'parts': [{'text': 'The weather in New York is sunny with a temperature of 25 degrees Celsius (41 degrees Fahrenheit).'}], 'role': 'model'}
    
For more information about interacting with a deployed ADK agent in Agent Runtime, see [Manage deployed agents](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/manage/overview>) and [Use a Agent Development Kit agent](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/use/adk>) in the Agent Runtime documentation.

### Sending Multimodal Queries[¶](<https://adk.dev/deploy/agent-runtime/test/#sending-multimodal-queries> "Permanent link")

To send multimodal queries (e.g., including images) to your agent, you can construct the `message` parameter of `async_stream_query` with a list of `types.Part` objects. Each part can be text or an image.

To include an image, you can use `types.Part.from_uri`, providing a Google Cloud Storage (GCS) URI for the image.
    
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-1>)from google.genai import types
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-2>)
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-3>)image_part = types.Part.from_uri(
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-4>)    file_uri="gs://cloud-samples-data/generative-ai/image/scones.jpg",
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-5>)    mime_type="image/jpeg",
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-6>))
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-7>)text_part = types.Part.from_text(
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-8>)    text="What is in this image?",
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-9>))
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-10>)
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-11>)async for event in remote_app.async_stream_query(
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-12>)    user_id="u_456",
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-13>)    session_id=remote_session["id"],
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-14>)    message=[text_part, image_part],
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-15>)):
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-13-16>)    print(event)
    
Note

While the underlying communication with the model may involve Base64 encoding for images, the recommended and supported method for sending image data to an agent deployed on Agent Runtime is by providing a GCS URI.

## Clean up deployments[¶](<https://adk.dev/deploy/agent-runtime/test/#clean-up-deployments> "Permanent link")

If you have performed deployments as tests, it is a good practice to clean up your cloud resources after you have finished. You can delete the deployed Agent Runtime instance to avoid any unexpected charges on your Google Cloud account.
    
    [](<https://adk.dev/deploy/agent-runtime/test/#__codelineno-14-1>)remote_app.delete(force=True)
    
The `force=True` parameter also deletes any child resources that were generated from the deployed agent, such as sessions. You can also delete your deployed agent via the [Agent Runtime UI](<https://console.cloud.google.com/vertex-ai/agents/agent-engines>) on Google Cloud.

Back to top 