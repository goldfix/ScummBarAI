# Standard deployment - Agent Development Kit (ADK)

> Source: [https://adk.dev/deploy/agent-runtime/deploy/](https://adk.dev/deploy/agent-runtime/deploy/)

[ Skip to content ](<https://adk.dev/deploy/agent-runtime/deploy/#deploy-to-agent-runtime>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/deploy/agent-runtime/deploy.md> "Edit this page on GitHub") [ ](<https://adk.dev/deploy/agent-runtime/deploy/index.md> "View this page as Markdown")

# Deploy to Agent Runtime[¶](<https://adk.dev/deploy/agent-runtime/deploy/#deploy-to-agent-runtime> "Permanent link")

Supported in ADKPythonGo v1.2.0

This deployment procedure describes how to perform a standard deployment of ADK agent code to Google Cloud [Agent Runtime](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/overview>). You should follow this deployment path if you have an existing Google Cloud project and if you want to carefully manage deploying an ADK agent to Agent Runtime environment. These instructions use Cloud Console, the gcloud command line interface, and the ADK command line interface (ADK CLI). This path is recommended for users who are already familiar with configuring Google Cloud projects, and users preparing for production deployments.

These instructions describe how to deploy an ADK project to Google Cloud Agent Runtime environment, which includes the following stages:

  * [Setup Google Cloud project](<https://adk.dev/deploy/agent-runtime/deploy/#setup-cloud-project>)
  * [Prepare agent project folder](<https://adk.dev/deploy/agent-runtime/deploy/#define-your-agent>)
  * [Deploy the agent](<https://adk.dev/deploy/agent-runtime/deploy/#deploy-agent>)

## Setup Google Cloud project[¶](<https://adk.dev/deploy/agent-runtime/deploy/#setup-cloud-project> "Permanent link")

To deploy your agent to Agent Runtime, you need a Google Cloud project:

  1. **Sign into Google Cloud** :

     * If you're an **existing user** of Google Cloud:
       * Sign in via <https://console.cloud.google.com>
       * If you previously used a Free Trial that has expired, you may need to upgrade to a [Paid billing account](<https://docs.cloud.google.com/free/docs/free-cloud-features#how-to-upgrade>).
     * If you are a **new user** of Google Cloud:
       * You can sign up for the [Free Trial program](<https://docs.cloud.google.com/free/docs/free-cloud-features>). The Free Trial gets you a $300 Welcome credit to spend over 91 days on various [Google Cloud products](<https://docs.cloud.google.com/free/docs/free-cloud-features#during-free-trial>) and you won't be billed. During the Free Trial, you also get access to the [Google Cloud Free Tier](<https://docs.cloud.google.com/free/docs/free-cloud-features#free-tier>), which gives you free usage of select products up to specified monthly limits, and to product-specific free trials.
  2. **Create a Google Cloud project**

     * If you already have an existing Google Cloud project, you can use it, but be aware this process is likely to add new services to the project.
     * If you want to create a new Google Cloud project, you can create a new one on the [Create Project](<https://console.cloud.google.com/projectcreate>) page.
  3. **Get your Google Cloud Project ID**

     * You need your Google Cloud Project ID, which you can find on your GCP homepage. Make sure to note the Project ID (alphanumeric with hyphens), _not_ the project number (numeric).

![Google Cloud Project ID](https://adk.dev/assets/project-id.png)

  4. **Enable Agent Platform in your project**

     * To use Agent Runtime, you need to [enable the Agent Platform API](<https://console.cloud.google.com/apis/library/aiplatform.googleapis.com>). Click on the "Enable" button to enable the API. Once enabled, it should say "API Enabled".
  5. **Enable Cloud Resource Manager API in your project**

     * To use Agent Runtime, you need to [enable the Cloud Resource Manager API](<https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview>). Click on the "Enable" button to enable the API. Once enabled, it should say "API Enabled".

## Set up your coding environment[¶](<https://adk.dev/deploy/agent-runtime/deploy/#prerequisites-coding-env> "Permanent link")

Now that you prepared your Google Cloud project, you can return to your coding environment. These steps require access to a terminal within your coding environment to run command line instructions.

### Authenticate your coding environment with Google Cloud[¶](<https://adk.dev/deploy/agent-runtime/deploy/#authenticate-your-coding-environment-with-google-cloud> "Permanent link")

  * You need to authenticate your coding environment so that you and your code can interact with Google Cloud. To do so, you need the gcloud CLI. If you have never used the gcloud CLI, you need to first [download and install it](<https://docs.cloud.google.com/sdk/docs/install-sdk>) before continuing with the steps below:

  * Run the following command in your terminal to access your Google Cloud project as a user:
        
        [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-0-1>)gcloud auth login
        
After authenticating, you should see the message `You are now authenticated with the gcloud CLI!`.

  * Run the following command to authenticate your code so that it can work with Google Cloud:
        
        [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-1-1>)gcloud auth application-default login
        
After authenticating, you should see the message `You are now authenticated with the gcloud CLI!`.

  * (Optional) If you need to set or change your default project in gcloud, you can use:
        
        [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-2-1>)gcloud config set project MY-PROJECT-ID
        
### Define your agent[¶](<https://adk.dev/deploy/agent-runtime/deploy/#define-your-agent> "Permanent link")

With your Google Cloud and coding environment prepared, you're ready to deploy your agent. The instructions assume that you have an agent project folder, such as:

PythonGo
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-3-1>)multi_tool_agent/
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-3-2>)├── .env
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-3-3>)├── __init__.py
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-3-4>)└── agent.py
    
For more details on the project files and format, see the [multi_tool_agent](<https://github.com/google/adk-docs/tree/main/examples/python/snippets/get-started/multi_tool_agent>) code sample.
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-4-1>)multi_tool_agent/
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-4-2>)├── go.mod
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-4-3>)├── go.sum
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-4-4>)└── main.go
    
## Deploy the agent[¶](<https://adk.dev/deploy/agent-runtime/deploy/#deploy-agent> "Permanent link")

You can deploy from your terminal using the `adk deploy` command line tool. This process packages your code, builds it into a container, and deploys it to the managed Agent Runtime service. This process can take several minutes.

The following example deploy command uses the `multi_tool_agent` sample code as the project to be deployed:

PythonGo
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-1>)PROJECT_ID=my-project-id
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-2>)LOCATION_ID=us-central1
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-3>)
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-4>)adk deploy agent_engine \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-5>)        --project=$PROJECT_ID \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-6>)        --region=$LOCATION_ID \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-7>)        --display_name="My First Agent" \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-5-8>)        multi_tool_agent
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-1>)PROJECT_ID=my-project-id
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-2>)LOCATION_ID=us-central1
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-3>)
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-4>)adkgo deploy agentengine \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-5>)    -e ./main.go \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-6>)    -s "multi_tool_agent" \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-7>)    -p $PROJECT_ID \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-8>)    -r $LOCATION_ID \
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-6-9>)    -d .
    
For `region`, you can find a list of the supported regions on the [Agent Builder locations page](<https://docs.cloud.google.com/agent-builder/locations#supported-regions-agent-engine>).

PythonGo

To learn about the CLI options for the `adk deploy agent_engine` command, see the [ADK CLI Reference](<https://adk.dev/api-reference/cli/#adk-deploy-agent-engine>).

To learn about the CLI options for the `adkgo deploy agentengine` command you can run `adkgo help deploy agentengine` which will display available options. The most important are: 
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-7-1>)-e, --entry_point_path string   Path to an entry point (go 'main')
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-7-2>)-s, --name string               Agent Engine name
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-7-3>)-p, --project_name string       GCP Project Name
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-7-4>)-r, --region string             GCP Region
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-7-5>)-d, --source_dir string         Directory to archive, defaults to current working directory
    
### Deploy command output[¶](<https://adk.dev/deploy/agent-runtime/deploy/#deploy-command-output> "Permanent link")

Once successfully deployed, you should see the following output:

PythonGo
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-8-1>)Creating AgentEngine
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-8-2>)Create AgentEngine backing LRO: projects/123456789/locations/us-central1/reasoningEngines/751619551677906944/operations/2356952072064073728
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-8-3>)View progress and logs at https://console.cloud.google.com/logs/query?project=hopeful-sunset-478017-q0
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-8-4>)AgentEngine created. Resource name: projects/123456789/locations/us-central1/reasoningEngines/751619551677906944
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-8-5>)To use this AgentEngine in another session:
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-8-6>)agent_engine = vertexai.agent_engines.get('projects/123456789/locations/us-central1/reasoningEngines/751619551677906944')
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-8-7>)Cleaning up the temp folder: /var/folders/k5/pv70z5m92s30k0n7hfkxszfr00mz24/T/agent_engine_deploy_src/20251219_134245
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-1>)Computing flags & preparing temp : Starting
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-2>)
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-3>)...
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-4>)
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-5>)    >  [Deployed Reasoning Engine: projects/887748635400/locations/us-central1/reasoningEngines/751619551677906944]
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-6>)    >  [Display Name: simpleText]
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-7>)
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-8>)Deploying to Agent Engine : Finished successfully
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-9>)Cleaning temp : Starting
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-10>)    >  [Clean temp starting with /tmp/agentEngine_20260424_141040__2470352066]
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-11>)
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-9-12>)Cleaning temp : Finished successfully
    
Note that you now have a `RESOURCE_ID` where your agent has been deployed (which in the example above is `751619551677906944`). You need this ID number along with the other values to use your agent on Agent Runtime.

## Using an agent on Agent Runtime[¶](<https://adk.dev/deploy/agent-runtime/deploy/#using-an-agent-on-agent-runtime> "Permanent link")

Once you have completed deployment of your ADK project, you can query the agent using the Agent Platform SDK, Python requests library, or a REST API client. This section provides some information on what you need to interact with your agent and how to construct URLs to interact with your agent's REST API.

To interact with your agent on Agent Runtime, you need the following:

  * **PROJECT_ID** (example: "my-project-id") which you can find on your [project details page](<https://console.cloud.google.com/iam-admin/settings>)
  * **LOCATION_ID** (example: "us-central1"), that you used to deploy your agent
  * **RESOURCE_ID** (example: "751619551677906944"), which you can find on the [Agent Runtime UI](<https://console.cloud.google.com/vertex-ai/agents/agent-engines>)

The query URL structure is as follows:
    
    [](<https://adk.dev/deploy/agent-runtime/deploy/#__codelineno-10-1>)https://$(LOCATION_ID)-aiplatform.googleapis.com/v1/projects/$(PROJECT_ID)/locations/$(LOCATION_ID)/reasoningEngines/$(RESOURCE_ID):query
    
You can make requests from your agent using this URL structure. For more information on how to make requests, see the instructions in the Agent Runtime documentation [Use an Agent Development Kit agent](<https://docs.cloud.google.com/agent-builder/agent-engine/use/adk#rest-api>). You can also check the Agent Runtime documentation to learn about how to manage your [deployed agent](<https://docs.cloud.google.com/agent-builder/agent-engine/manage/overview>). For more information on testing and interacting with a deployed agent, see [Test deployed agents in Agent Runtime](<https://adk.dev/deploy/agent-runtime/test/>).

### Monitoring and verification[¶](<https://adk.dev/deploy/agent-runtime/deploy/#monitoring-and-verification> "Permanent link")

  * You can monitor the deployment status in the [Agent Runtime UI](<https://console.cloud.google.com/vertex-ai/agents/agent-engines>) in the Google Cloud Console.
  * For additional details, you can visit the Agent Runtime documentation [deploying an agent](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/deploy>) and [managing deployed agents](<https://cloud.google.com/vertex-ai/generative-ai/docs/agent-engine/manage/overview>).

## Test deployed agents[¶](<https://adk.dev/deploy/agent-runtime/deploy/#test-deployed-agents> "Permanent link")

After completing deployment of your ADK agent you should test the workflow in its new hosted environment. For more information on testing an ADK agent deployed to Agent Runtime, see [Test deployed agents in Agent Runtime](<https://adk.dev/deploy/agent-runtime/test/>).

Back to top 