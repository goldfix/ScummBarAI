# agents-cli - Agent Development Kit (ADK)

> Source: [https://adk.dev/deploy/agent-runtime/agents-cli/](https://adk.dev/deploy/agent-runtime/agents-cli/)

[ Skip to content ](<https://adk.dev/deploy/agent-runtime/agents-cli/#deploy-to-agent-runtime-with-agents-cli>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/deploy/agent-runtime/agents-cli.md> "Edit this page on GitHub") [ ](<https://adk.dev/deploy/agent-runtime/agents-cli/index.md> "View this page as Markdown")

# Deploy to Agent Runtime with Agents CLI[¶](<https://adk.dev/deploy/agent-runtime/agents-cli/#deploy-to-agent-runtime-with-agents-cli> "Permanent link")

Supported in ADKPythonGo v1.2.0

This deployment procedure describes how to perform a deployment using [Agents CLI in Agent Platform](<https://google.github.io/agents-cli/>) and the ADK. Deploying to Agent Runtime via Agents CLI provides an accelerated path to a production-ready environment. Agents CLI automatically configures Google Cloud resources, CI/CD pipelines, and Infrastructure-as-Code (Terraform) to support the entire development lifecycle. As a best practice, always ensure you review the generated configurations to align with your organization’s security and compliance standards before production deployment.

This deployment guide uses Agents CLI to apply a project template to your existing project, add deployment artifacts, and prepare your agent project for deployment. These instructions show you how to use Agents CLI to provision a Google Cloud project with services needed for deploying your ADK project, as follows:

  * [Prerequisites](<https://adk.dev/deploy/agent-runtime/agents-cli/#prerequisites-ad>): Set up Google Cloud project, IAM permissions, and install required software.
  * [Prepare your ADK project](<https://adk.dev/deploy/agent-runtime/agents-cli/#prepare-ad>): Modify your existing ADK project files to get ready for deployment.
  * [Connect to your Google Cloud project](<https://adk.dev/deploy/agent-runtime/agents-cli/#connect-ad>): Connect your development environment to Google Cloud and your Google Cloud project.
  * [Deploy your ADK project](<https://adk.dev/deploy/agent-runtime/agents-cli/#deploy-ad>): Provision required services in your Google Cloud project and upload your ADK project code.

For information on testing a deployed agent, see [Test deployed agent](<https://adk.dev/deploy/agent-runtime/test/>). For more information on using Agents CLI and its command line tools, see the [CLI reference](<https://google.github.io/agents-cli/cli/>) and [Guide](<https://google.github.io/agents-cli/>).

### Prerequisites[¶](<https://adk.dev/deploy/agent-runtime/agents-cli/#prerequisites-ad> "Permanent link")

You need the following resources configured to use this deployment path:

  * **Google Cloud Project and Permissions** : A Google Cloud project with [billing enabled](<https://cloud.google.com/billing/docs/how-to/modify-project>). You can use an existing project or create a new one. You must have one of the following IAM roles assigned within this project:
    * **Agent Platform User role** — sufficient to deploy an agent to Agent Runtime.
    * **Owner role** — required for the full production setup (Terraform infrastructure provisioning, CI/CD pipelines, IAM configuration).

Note

An empty project is recommended to avoid conflicts with existing resources. For new projects, see [Creating and managing projects](<https://cloud.google.com/resource-manager/docs/creating-managing-projects>).

  * **Python Environment** : A Python version supported by [Agents CLI](<https://google.github.io/agents-cli/guide/getting-started/>).
  * **uv Tool:** Manage Python development environment and running agents-cli tools. For installation details, see [Install uv](<https://docs.astral.sh/uv/getting-started/installation/>).
  * **Google Cloud CLI tool** : The gcloud command line interface. For installation details, see [Google Cloud Command Line Interface](<https://cloud.google.com/sdk/docs/install>).
  * **Make tool** : Build automation tool. This tool is part of most Unix-based systems, for installation details, see the [Make tool](<https://www.gnu.org/software/make/>) documentation.

### Prepare your ADK project[¶](<https://adk.dev/deploy/agent-runtime/agents-cli/#prepare-ad> "Permanent link")

When you deploy an ADK project to Agent Runtime, you need some additional files to support the deployment operation. The following Agents CLI command backs up your project and then adds files to your project for deployment purposes.

These instructions assume you have an existing ADK project that you are modifying for deployment. If you do not have an ADK project, or want to use a test project, complete one of the [Get started](<https://adk.dev/get-started/>) guides, which creates an agent project. The following instructions use the `my_agent` project as an example.

To prepare your ADK project for deployment to Agent Runtime:

  1. In a terminal window of your development environment, navigate to the **parent directory** that contains your agent folder. For example, if your project structure is:
         
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-0-1>)your-project-directory/
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-0-2>)├── my_agent/
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-0-3>)│   ├── __init__.py
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-0-4>)│   ├── agent.py
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-0-5>)│   └── .env
         
Navigate to `your-project-directory/`

  2. Run the Agents CLI `scaffold enhance` command to add the files required for deployment into your project.
         
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-1-1>)agents-cli scaffold enhance --deployment-target agent_engine
         
  3. Follow the instructions from the Agents CLI tool. In general, you can accept the default answers to all questions. However for the **GCP region** , option, make sure you select one of the [supported regions](<https://docs.cloud.google.com/agent-builder/locations#supported-regions-agent-engine>) for Agent Runtime.

When you successfully complete this process, the tool shows the following message:
    
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-2-1>)> Success! Your agent project is ready.
    
Note

The Agents CLI tool may show a reminder to connect to Google Cloud while running, but that connection is _not required_ at this stage.

For more information about the changes Agents CLI makes to your ADK project, see [Changes to your ADK project](<https://adk.dev/deploy/agent-runtime/agents-cli/#adk-agents-cli-changes>).

### Connect to your Google Cloud project[¶](<https://adk.dev/deploy/agent-runtime/agents-cli/#connect-ad> "Permanent link")

Before you deploy your ADK project, you must connect to Google Cloud and your project. After logging into your Google Cloud account, you should verify that your deployment target project is visible from your account and that it is configured as your current project.

To connect to Google Cloud and list your project:

  1. In a terminal window of your development environment, login to your Google Cloud account:
         
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-3-1>)gcloud auth application-default login
         
  2. Set your target project using the Google Cloud Project ID:
         
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-4-1>)gcloud config set project your-project-id-xxxxx
         
  3. Verify your Google Cloud target project is set:
         
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-5-1>)gcloud config get-value project
         
Once you have successfully connected to Google Cloud and set your Cloud Project ID, you are ready to deploy your ADK project files to Agent Runtime.

### Deploy your ADK project[¶](<https://adk.dev/deploy/agent-runtime/agents-cli/#deploy-ad> "Permanent link")

When using Agents CLI, you deploy using the `agents-cli deploy` command. This command builds a container from your agent code, pushes it to a registry, and deploys it to Agent Runtime in the hosted environment.

Important

_Make sure your Google Cloud target deployment project is set as your_**current project** _before performing these steps_. The `agents-cli deploy` command uses your currently set Google Cloud project when it performs a deployment. For information on setting and checking your current project, see [Connect to your Google Cloud project](<https://adk.dev/deploy/agent-runtime/agents-cli/#connect-ad>).

To deploy your ADK project to Agent Runtime in your Google Cloud project:

  1. In a terminal window, navigate to your agent project directory (e.g., `your-project-directory/`).

  2. Deploy your agent code to the Google Cloud development environment:
         
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-6-1>)agents-cli deploy
         
The command reads your `deployment_target` from `pyproject.toml` and deploys to the configured target (Agent Runtime, Cloud Run, or GKE).

  3. (Optional) To enable observability features like prompt-response logging and content logs, provision the telemetry infrastructure:
         
         [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-7-1>)agents-cli infra single-project
         
For more details, see the [Observability Guide](<https://google.github.io/agents-cli/guide/observability/>).

Once this process completes successfully, you should be able to interact with the agent running on Google Cloud Agent Runtime. For details on testing the deployed agent, see [Test deployed agent](<https://adk.dev/deploy/agent-runtime/test/>).

### Changes to your ADK project[¶](<https://adk.dev/deploy/agent-runtime/agents-cli/#adk-agents-cli-changes> "Permanent link")

The Agents CLI tools add more files to your project for deployment. The procedure below backs up your existing project files before modifying them. This guide uses the [multi_tool_agent](<https://github.com/google/adk-docs/tree/main/examples/python/snippets/get-started/multi_tool_agent>) project as a reference example. The original project has the following file structure to start with:
    
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-8-1>)my_agent/
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-8-2>)├─ __init__.py
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-8-3>)├─ agent.py
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-8-4>)└─ .env
    
After running the Agents CLI scaffold enhance command to add Agent Runtime deployment information, the new structure is as follows:
    
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-1>)my-agent/
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-2>)├─ app/                 # Core application code
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-3>)│   ├─ agent.py         # Main agent logic
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-4>)│   ├─ agent_engine_app.py # Agent Runtime application logic
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-5>)│   └─ utils/           # Utility functions and helpers
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-6>)├─ .cloudbuild/         # CI/CD pipeline configurations for Google Cloud Build
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-7>)├─ deployment/          # Infrastructure and deployment scripts
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-8>)├─ notebooks/           # Jupyter notebooks for prototyping and evaluation
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-9>)├─ tests/               # Unit, integration, and load tests
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-10>)├─ Makefile             # Makefile for common commands
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-11>)├─ GEMINI.md            # AI-assisted development guide
    [](<https://adk.dev/deploy/agent-runtime/agents-cli/#__codelineno-9-12>)└─ pyproject.toml       # Project dependencies and configuration
    
See the _README.md_ file in your updated ADK project folder for more information. For more information on using Agents CLI, see the [Agents CLI documentation](<https://google.github.io/agents-cli/>).

## Test deployed agents[¶](<https://adk.dev/deploy/agent-runtime/agents-cli/#test-deployed-agents> "Permanent link")

After completing deployment of your ADK agent you should test the workflow in its new hosted environment. For more information on testing an ADK agent deployed to Agent Runtime, see [Test deployed agents in Agent Runtime](<https://adk.dev/deploy/agent-runtime/test/>).

Back to top 