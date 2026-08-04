# Authentication - Agent Development Kit (ADK)

> Source: [https://adk.dev/tools-custom/authentication/](https://adk.dev/tools-custom/authentication/)

[ Skip to content ](<https://adk.dev/tools-custom/authentication/#authenticating-with-tools>)

[ ](<https://github.com/google/adk-docs/edit/main/docs/tools-custom/authentication.md> "Edit this page on GitHub") [ ](<https://adk.dev/tools-custom/authentication/index.md> "View this page as Markdown")

# Authenticating with tools[¶](<https://adk.dev/tools-custom/authentication/#authenticating-with-tools> "Permanent link")

Supported in ADKPython v0.1.0

The tools and services you use within ADK agents may require access to protected resources, such as user data in email or calendar applications, or sales records in databases. Getting access to these resources typically requires an authentication process that includes credentials and access keys which must be carefully managed and protected. The requirements for managing authentication data can also change if you are running your agent locally or deploying it to a hosted service. If multiple users, with potentially different access permissions, are interacting with the agent, this creates another layer of authentication management requirements.

WARNING: Credential storage and security risks

Storing sensitive credentials such as access tokens and especially refresh tokens directly in the session state can pose security risks depending on your session storage backend, your **_SessionService_** implementation, and overall application security posture. Carefully consider how you manage credentials in ADK agents before deploying them for general use.

## Authentication and credential management[¶](<https://adk.dev/tools-custom/authentication/#authentication-and-credential-management> "Permanent link")

There are several ways to manage authentication and credentials in ADK agents. Each of these methods carries some amount of risk, so you should carefully consider which approach best serves your application and customers.

### Recommended: Authentication manager services[¶](<https://adk.dev/tools-custom/authentication/#authentication-manager> "Permanent link")

When deploying agents to production hosted environments, your agent's ability to properly authenticate to restricted tools and services becomes more challenging and more important to properly manage. This authentication challenge can become even more complicated when users of your agent have varying levels of access to restricted tools and data.

Rather than writing code to handle the authentication process and credential management for various tools used by your agent, use an _authentication manager_ service that manages _both_ for you. This service should handle the storage of keys and secrets, as well as the acquisition, management, and storage of OAuth access or refresh tokens. Learn more about [Agent Identity integration](<https://adk.dev/integrations/agent-identity/>) with ADK.

### Self-managed authentication[¶](<https://adk.dev/tools-custom/authentication/#self-managed-authentication> "Permanent link")

If you decide to manage your own authentication process with ADK helper functions and your own code, consider these recommendations:

  * **API keys and client secrets:** For any API keys and client secrets used inside ADK code, when running on a local compute environment use a local `.env` file excluded from version control. When your agent is hosted or otherwise in a production environment, use a secrets manager. For more details on secrets managers, see the [next section](<https://adk.dev/tools-custom/authentication/#secrets-manager>).
  * **Interactive authentication:** When using interactive three-legged auth (3LO) OAuth or OpenID Connect (OIDC) for authentication to tools, write a service on the client application to acquire, manage access, and refresh tokens. Make sure to store these tokens against an authenticated user identifier in an encrypted database.

### Secrets manager services[¶](<https://adk.dev/tools-custom/authentication/#secrets-manager> "Permanent link")

For production environments, if you are not using an [authentication manager](<https://adk.dev/tools-custom/authentication/#authentication-manager>) service, you should store credentials in a dedicated secret manager service to protect that data. With this approach, a secret manager securely stores the credentials for any tools or services accessed by the agent as needed, and those secrets are not resident in agent's operating memory. For example, a custom ADK Tool using this method would have only short-lived access tokens or secure references in session memory, and retrieve longer-lived refresh tokens from the secrets manager when needed. When selecting a secrets manager, consider services from well-established providers, such as [Google Cloud Secret Manager](<https://cloud.google.com/security/products/secret-manager>) or other secret management services.

### Local encrypted secrets storage[¶](<https://adk.dev/tools-custom/authentication/#local-encrypted-secrets-storage> "Permanent link")

For agent applications that are less security sensitive, keeping credentials in local, encrypted storage can be a viable option. Consider using dedicated local secrets storage system or encrypting the data in a local database using a robust encryption library, and then managing the encryption keys securely using a key management service. Take care to only keep short-lived access tokens in operating memory and access long-lived credentials and refresh tokens from encrypted local storage only when needed.

### In-memory secrets[¶](<https://adk.dev/tools-custom/authentication/#in-memory-secrets> "Permanent link")

This method _should only be used in the early development_ and testing of your agent. With this approach, credentials are stored in the current **_InMemorySessionService_** instance. The data exists only in session memory and is not persisted. However, you should carefully consider the risks of using this method based on how long an agent session may last, who has access to the agent, and the security of the environment where the agent is running.

## Framework components[¶](<https://adk.dev/tools-custom/authentication/#framework-components> "Permanent link")

Within the ADK framework, the **_AuthScheme_** and **_AuthCredential_** are the key components for handling authentication methods and managing credential data:

  * **_AuthScheme_** : Defines _how_ an API expects authentication credentials, such as an API Key in a header or an OAuth 2.0 Bearer token. ADK supports the same types of authentication schemes as OpenAPI 3.0 and uses specific classes for credential types, including **_APIKey_** , **_HTTPBearer_** , **_OAuth2_** , and **_OpenIdConnectWithConfig_**. For more details on each OpenAPI credential type, see [OpenAPI doc: Authentication](<https://swagger.io/docs/specification/v3_0/authentication/>).

  * **_AuthCredential_** : Holds the _initial_ information needed to _start_ the authentication process, such as your application's OAuth Client ID or Secret, or an API key value. An instance of this class includes an **auth_type** , such as `API_KEY`, `OAUTH2`, `SERVICE_ACCOUNT`, specifying the credential type.

The general authentication flow involves providing these details when configuring a tool. ADK then attempts to automatically exchange the initial credential, such as an access token, before the tool makes an API call. For flows requiring user interaction, including OAuth consent, ADK triggers a specific interactive process with your **_Agent Client_** application.

### Supported initial credential types[¶](<https://adk.dev/tools-custom/authentication/#supported-initial-credential-types> "Permanent link")

  * **API_KEY:** Provides simple key-value authentication, which usually requires no authentication exchange.
  * **HTTP:** Provides Basic Auth which is not recommended and may not be supported for exchange, or already obtained Bearer tokens. Bearer tokens do not require an authentication exchange.
  * **OAUTH2:** Provides standard OAuth 2.0 authentication flows, and requires configuration with client ID, secret, and scopes. This method often triggers an interactive flow for user consent.
  * **OPEN_ID_CONNECT:** Provides authentication based on OpenID Connect. Similar to OAuth2, this type often requires configuration and user interaction.
  * **SERVICE_ACCOUNT:** Provides Google Cloud Service Account credentials as a JSON key or Application Default Credentials. This type typically exchanges a Bearer token.

## Tools and integrations quick guide[¶](<https://adk.dev/tools-custom/authentication/#tools-and-integrations-quick-guide> "Permanent link")

Here is a quick guide to authentication for key ADK toolsets:

  * [**_RestApiTool_**](<https://adk.dev/tools-custom/openapi-tools/>): Set `auth_scheme` and `auth_credential` during initialization
  * [**_OpenAPIToolset_**](<https://adk.dev/tools-custom/openapi-tools/>): Set `auth_scheme` and `auth_credential` during initialization
  * [**_APIHubToolset_**](<https://adk.dev/integrations/apigee-api-hub/>): Set `auth_scheme` and `auth_credential` during initialization, _if_ the API requires authentication.
  * [**_ApplicationIntegrationToolset_**](<https://adk.dev/integrations/application-integration/>): Set `auth_scheme` and `auth_credential` during initialization, _if_ the API requires authentication.
  * [**_GoogleApiToolSet_**](<https://github.com/google/adk-python/blob/main/src/google/adk/tools/google_api_tool/google_api_toolset.py>): Use this toolset's specific authentication method.

For more authentication details for other pre-built tools and integrations see the [ADK Integrations](<https://adk.dev/integrations>) catalog.

* * *

## Build agentic applications with authenticated tools[¶](<https://adk.dev/tools-custom/authentication/#build-agentic-applications-with-authenticated-tools> "Permanent link")

This section focuses on using pre-existing tools (like those from `RestApiTool/ OpenAPIToolset`, `APIHubToolset`, `GoogleApiToolSet`) that require authentication within your agentic application. Your main responsibility is configuring the tools and handling the client-side part of interactive authentication flows (if required by the tool).

### Configure tools with authentication[¶](<https://adk.dev/tools-custom/authentication/#configure-tools-with-authentication> "Permanent link")

When adding an authenticated tool to your agent, you need to provide its required `AuthScheme` and your application's initial `AuthCredential`.

You can configure authentication differently depending on your toolset type, OpenAPI-based or Google API toolsets, and, for services protected by Cloud IAM, whether the service needs an ID token instead of an access token. The following subsections cover each case.

#### Use OpenAPI-based toolsets (`OpenAPIToolset`, `APIHubToolset`, etc.)[¶](<https://adk.dev/tools-custom/authentication/#use-openapi-based-toolsets-openapitoolset-apihubtoolset-etc> "Permanent link")

Pass the scheme and credential during toolset initialization. The toolset applies them to all generated tools. Here are few ways to create tools with authentication in ADK.

API KeyOAuth2Service AccountOpenID connect

Create a tool requiring an API Key.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-1>)from google.adk.tools.openapi_tool.auth.auth_helpers import token_to_scheme_credential
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-2>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-3>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-4>)auth_scheme, auth_credential = token_to_scheme_credential(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-5>)    "apikey", "query", "apikey", "YOUR_API_KEY_STRING"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-6>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-7>)sample_api_toolset = OpenAPIToolset(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-8>)    spec_str="...",  # Fill this with an OpenAPI spec string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-9>)    spec_str_type="yaml",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-10>)    auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-11>)    auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-0-12>))
    
Create a tool requiring OAuth2.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-1>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-2>)from fastapi.openapi.models import OAuth2
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-3>)from fastapi.openapi.models import OAuthFlowAuthorizationCode
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-4>)from fastapi.openapi.models import OAuthFlows
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-5>)from google.adk.auth import AuthCredential
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-6>)from google.adk.auth import AuthCredentialTypes
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-7>)from google.adk.auth import OAuth2Auth
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-8>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-9>)auth_scheme = OAuth2(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-10>)    flows=OAuthFlows(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-11>)        authorizationCode=OAuthFlowAuthorizationCode(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-12>)            authorizationUrl="https://accounts.google.com/o/oauth2/auth",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-13>)            tokenUrl="https://oauth2.googleapis.com/token",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-14>)            scopes={
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-15>)                "https://www.googleapis.com/auth/calendar": "calendar scope"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-16>)            },
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-17>)        )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-18>)    )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-19>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-20>)auth_credential = AuthCredential(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-21>)    auth_type=AuthCredentialTypes.OAUTH2,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-22>)    oauth2=OAuth2Auth(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-23>)        client_id=YOUR_OAUTH_CLIENT_ID,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-24>)        client_secret=YOUR_OAUTH_CLIENT_SECRET
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-25>)    ),
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-26>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-27>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-28>)calendar_api_toolset = OpenAPIToolset(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-29>)    spec_str=google_calendar_openapi_spec_str, # Fill this with an openapi spec
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-30>)    spec_str_type='yaml',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-31>)    auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-32>)    auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-1-33>))
    
Create a tool requiring Service Account.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-1>)from google.adk.tools.openapi_tool.auth.auth_helpers import service_account_dict_to_scheme_credential
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-2>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-3>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-4>)service_account_cred = json.loads(service_account_json_str)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-5>)auth_scheme, auth_credential = service_account_dict_to_scheme_credential(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-6>)    config=service_account_cred,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-7>)    scopes=["https://www.googleapis.com/auth/cloud-platform"],
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-8>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-9>)sample_toolset = OpenAPIToolset(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-10>)    spec_str=sa_openapi_spec_str, # Fill this with an openapi spec
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-11>)    spec_str_type='json',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-12>)    auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-13>)    auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-2-14>))
    
Create a tool requiring OpenID connect.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-1>)from google.adk.auth.auth_schemes import OpenIdConnectWithConfig
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-2>)from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-3>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-4>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-5>)auth_scheme = OpenIdConnectWithConfig(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-6>)    authorization_endpoint=OAUTH2_AUTH_ENDPOINT_URL,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-7>)    token_endpoint=OAUTH2_TOKEN_ENDPOINT_URL,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-8>)    scopes=['openid', 'YOUR_OAUTH_SCOPES']
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-9>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-10>)auth_credential = AuthCredential(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-11>)    auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-12>)    oauth2=OAuth2Auth(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-13>)        client_id="...",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-14>)        client_secret="...",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-15>)    )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-16>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-17>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-18>)userinfo_toolset = OpenAPIToolset(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-19>)    spec_str=content, # Fill in an actual spec
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-20>)    spec_str_type='yaml',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-21>)    auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-22>)    auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-3-23>))
    
#### Use Google API toolsets (e.g., `calendar_tool_set`)[¶](<https://adk.dev/tools-custom/authentication/#use-google-api-toolsets-eg-calendar_tool_set> "Permanent link")

These toolsets often have dedicated configuration methods.

Tip: For how to create a Google OAuth Client ID & Secret, see this guide: [Get your Google API Client ID](<https://developers.google.com/identity/gsi/web/guides/get-google-api-clientid#get_your_google_api_client_id>)
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-1>)# Example: Configuring Google Calendar Tools
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-2>)from google.adk.tools.google_api_tool import calendar_tool_set
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-3>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-4>)client_id = "YOUR_GOOGLE_OAUTH_CLIENT_ID.apps.googleusercontent.com"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-5>)client_secret = "YOUR_GOOGLE_OAUTH_CLIENT_SECRET"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-6>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-7>)# Use the specific configure method for this toolset type
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-8>)calendar_tool_set.configure_auth(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-9>)    client_id=oauth_client_id, client_secret=oauth_client_secret
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-10>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-11>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-4-12>)# agent = LlmAgent(..., tools=calendar_tool_set.get_tool('calendar_tool_set'))
    
#### Use ID token[¶](<https://adk.dev/tools-custom/authentication/#use-id-token> "Permanent link")

If your agent calls a restricted service, for example a private Cloud Run or Cloud Function, the agent needs to prove your identity, not just your permissions. If you are calling a service that is accessed using Cloud IAM, you should use an ID token.

  * **Access Token (Default)** : It calls Google APIs (Drive, BigQuery). Think of it as your keycard.

  * **ID Token** : It calls your own services secured by IAM. Think of it as your passport.

##### Configuration[¶](<https://adk.dev/tools-custom/authentication/#configuration> "Permanent link")

To implement ID token authentication, configure your ServiceAccount with the following parameters, ensuring you specify the target service's URL as the `audience`.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-1>)from google.adk.auth.auth_credential import ServiceAccount
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-2>)from google.adk.tools.openapi_tool.auth.auth_helpers import service_account_scheme_credential
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-3>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-4>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-5>)# Configure the ServiceAccount to use ID token authentication.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-6>)# Replace <YOUR_AUDIENCE_URL> with the URL of the service you are calling.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-7>)sa_config = ServiceAccount(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-8>)    use_default_credential=True,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-9>)    use_id_token=True,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-10>)    audience="<YOUR_AUDIENCE_URL>",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-11>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-12>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-13>)auth_scheme, auth_credential = service_account_scheme_credential(sa_config)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-14>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-15>)sample_toolset = OpenAPIToolset(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-16>)    spec_str=sa_openapi_spec_str, # Fill this with an OpenAPI spec
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-17>)    spec_str_type="json",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-18>)    auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-19>)    auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-5-20>))
    
Troubleshooting authentication errors

If you receive an authentication error, verify that your service account has the 'Cloud Run Invoker' or equivalent role on the target service.

##### Key takeaways[¶](<https://adk.dev/tools-custom/authentication/#key-takeaways> "Permanent link")

  * **Audience Requirement** : The `audience` is a security feature that binds the token to a specific destination, preventing it from being "replayed" against other services.

  * **No Auto-Refresh** : Unlike standard OAuth2 access tokens for users, service-account ID tokens are fetched at the time of the request. They do not auto-refresh on a background timer.

  * **The Flow** : You define the intent and ADK handles the handshake, fetches the token from Google's auth servers, and injects it into your outgoing HTTP headers.

##### ServiceAccount configuration parameters[¶](<https://adk.dev/tools-custom/authentication/#serviceaccount-configuration-parameters> "Permanent link")

  * `service_account_credential` (Optional): Provide the path or dict for your service account JSON key file. Use this if you are running locally or outside of Google Cloud.

  * `use_default_credential` (Optional): Set to True to use Application Default Credentials (ADC). Recommended if your agent is already running within Google Cloud, for example on Cloud Run or Cloud Functions, as it avoids the need for local key files.

  * `use_id_token` (Required for IAM): Set to True to enable ID token-based authentication. This switches the ADK from requesting an Access Token, for Google APIs, to an ID Token, for your own IAM-secured services.

  * `audience` (Required if use_id_token=True): The URL of the service you are calling, for example, `https://my-service.run.app`. This is a security binding that ensures the token is valid only for that specific destination.

  * `scopes` (Optional): Use it only when requesting Access Tokens for Google Cloud APIs, like Drive or BigQuery. You do not need to set this if you are using ID tokens for private service authentication.

Pair `use_id_token` with `audience`

Always use `use_id_token=True` and `audience` together. If you provide one without the other, the ADK will raise an error to prevent accidental misconfiguration.

#### Use external access tokens[¶](<https://adk.dev/tools-custom/authentication/#use-external-access-tokens> "Permanent link")

The `external_access_token_key` feature allows your agent to use an existing access token provided by the runtime environment, such as a token provided by a frontend application, instead of starting a new authentication flow. When configured, the credential manager skips standard OAuth flows. Instead, retrieves the key in the agent's `tool_context.state` and directly uses the token for authentication. The use of this configuration parameter is mutually exclusive, and cannot include `credentials`, `client_id`, `client_secret`, or scopes parameters in the same configuration block.

Follow this example to configure the key:
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-1>)from google.adk.auth.auth_credential import AuthCredential
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-2>)from google.adk.auth.auth_credential import AuthCredentialTypes
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-3>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-4>)# Configure the tool to look for "my_frontend_token" in the session state
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-5>)credentials_config = AuthCredential(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-6>)    auth_type=AuthCredentialTypes.GOOGLE_CREDENTIALS,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-7>)    google_credentials_config={
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-8>)        # Do not hardcode authentication keys in production code
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-9>)        "external_access_token_key": "get_my_frontend_token" 
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-10>)    }
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-6-11>))
    
#### Authentication request flow[¶](<https://adk.dev/tools-custom/authentication/#authentication-request-flow> "Permanent link")

This diagram visualizes the end-to-end authentication handshake, tracing the path from the initial user query to the point where the ADK captures a credential request, handles the redirection flow, and retries the tool call once authorized.

![Authentication](https://adk.dev/assets/auth_part1.svg)

### Handle the interactive OAuth/OIDC flow (client-side)[¶](<https://adk.dev/tools-custom/authentication/#handle-the-interactive-oauthoidc-flow-client-side> "Permanent link")

If a tool requires user login/consent (typically OAuth 2.0 or OIDC), the ADK framework pauses execution and signals your **_Agent Client_** application. There are two cases:

  * **_Agent Client_** application runs the agent directly (via `runner.run_async`) in the same process. e.g. UI backend, CLI app, or Spark job etc.
  * **_Agent Client_** application interacts with ADK's fastapi server via `/run` or `/run_sse` endpoint. While ADK's fastapi server could be setup on the same server or different server as **_Agent Client_** application

The second case is a special case of first case, because `/run` or `/run_sse` endpoint also invokes `runner.run_async`. The only differences are:

  * Whether to call a python function to run the agent (first case) or call a service endpoint to run the agent (second case).
  * Whether the result events are in-memory objects (first case) or serialized json string in http response (second case).

Below sections focus on the first case and you should be able to map it to the second case very straightforward. We will also describe some differences to handle for the second case if necessary.

Here's the step-by-step process for your client application:

**Step 1: Run Agent & Detect Auth Request**

  * Initiate the agent interaction using `runner.run_async`.
  * Iterate through the yielded events.
  * Look for a specific function call event whose function call has a special name: `adk_request_credential`. This event signals that user interaction is needed. You can use helper functions to identify this event and extract necessary information. (For the second case, the logic is similar. You deserialize the event from the http response).

    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-1>)# runner = Runner(...)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-2>)# session = await session_service.create_session(...)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-3>)# content = types.Content(...) # User's initial query
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-4>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-5>)print("\nRunning agent...")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-6>)events_async = runner.run_async(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-7>)    session_id=session.id, user_id='user', new_message=content
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-8>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-9>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-10>)auth_request_function_call_id, auth_config = None, None
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-11>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-12>)async for event in events_async:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-13>)    # Use helper to check for the specific auth request event
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-14>)    if (auth_request_function_call := get_auth_request_function_call(event)):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-15>)        print("--> Authentication required by agent.")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-16>)        # Store the ID needed to respond later
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-17>)        if not (auth_request_function_call_id := auth_request_function_call.id):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-18>)            raise ValueError(f'Cannot get function call id from function call: {auth_request_function_call}')
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-19>)        # Get the AuthConfig containing the auth_uri etc.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-20>)        auth_config = get_auth_config(auth_request_function_call)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-21>)        break # Stop processing events for now, need user interaction
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-22>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-23>)if not auth_request_function_call_id:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-24>)    print("\nAuth not required or agent finished.")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-7-25>)    # return # Or handle final response if received
    
_Helper functions`helpers.py`:_
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-1>)from google.adk.events import Event
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-2>)from google.adk.auth import AuthConfig # Import necessary type
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-3>)from google.genai import types
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-4>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-5>)def get_auth_request_function_call(event: Event) -> types.FunctionCall:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-6>)    # Get the special auth request function call from the event
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-7>)    if not event.content or not event.content.parts:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-8>)        return
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-9>)    for part in event.content.parts:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-10>)        if (
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-11>)            part
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-12>)            and part.function_call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-13>)            and part.function_call.name == 'adk_request_credential'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-14>)            and event.long_running_tool_ids
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-15>)            and part.function_call.id in event.long_running_tool_ids
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-16>)        ):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-17>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-18>)            return part.function_call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-19>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-20>)def get_auth_config(auth_request_function_call: types.FunctionCall) -> AuthConfig:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-21>)    # Extracts the AuthConfig object from the arguments of the auth request function call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-22>)    if not auth_request_function_call.args or not (auth_config := auth_request_function_call.args.get('authConfig')):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-23>)        raise ValueError(f'Cannot get auth config from function call: {auth_request_function_call}')
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-24>)    if isinstance(auth_config, dict):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-25>)        auth_config = AuthConfig.model_validate(auth_config)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-26>)    elif not isinstance(auth_config, AuthConfig):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-27>)        raise ValueError(f'Cannot get auth config {auth_config} is not an instance of AuthConfig.')
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-8-28>)    return auth_config
    
**Step 2: Redirect User for Authorization**

  * Get the authorization URL (`auth_uri`) from the `auth_config` extracted in the previous step.
  * **Crucially, append your application's** redirect_uri as a query parameter to this `auth_uri`. This `redirect_uri` must be pre-registered with your OAuth provider (e.g., [Google Cloud Console](<https://developers.google.com/identity/protocols/oauth2/web-server#creatingcred>), [Okta admin panel](<https://developer.okta.com/docs/guides/sign-into-web-app-redirect/spring-boot/main/#create-an-app-integration-in-the-admin-console>)).
  * Direct the user to this complete URL (e.g., open it in their browser).

    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-1>)# (Continuing after detecting auth needed)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-2>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-3>)if auth_request_function_call_id and auth_config:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-4>)    # Get the base authorization URL from the AuthConfig
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-5>)    base_auth_uri = auth_config.exchanged_auth_credential.oauth2.auth_uri
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-6>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-7>)    if base_auth_uri:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-8>)        redirect_uri = 'http://localhost:8000/callback' # MUST match your OAuth client app config
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-9>)        # Append redirect_uri (use urlencode in production)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-10>)        auth_request_uri = base_auth_uri + f'&redirect_uri={redirect_uri}'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-11>)        # Now you need to redirect your end user to this auth_request_uri or ask them to open this auth_request_uri in their browser
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-12>)        # This auth_request_uri should be served by the corresponding auth provider and the end user should login and authorize your application to access their data
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-13>)        # And then the auth provider will redirect the end user to the redirect_uri you provided
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-14>)        # Next step: Get this callback URL from the user (or your web server handler)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-15>)    else:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-16>)         print("ERROR: Auth URI not found in auth_config.")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-9-17>)         # Handle error
    
**Step 3. Handle the Redirect Callback (Client):**

  * Your application must have a mechanism (e.g., a web server route at the `redirect_uri`) to receive the user after they authorize the application with the provider.
  * The provider redirects the user to your `redirect_uri` and appends an `authorization_code` (and potentially `state`, `scope`) as query parameters to the URL.
  * Capture the **full callback URL** from this incoming request.
  * (This step happens outside the main agent execution loop, in your web server or equivalent callback handler.)

**Step 4. Send Authentication Result Back to ADK (Client):**

  * Once you have the full callback URL (containing the authorization code), retrieve the `auth_request_function_call_id` and the `auth_config` object saved in Client Step 1.
  * Set the captured callback URL in the `exchanged_auth_credential.oauth2.auth_response_uri` field. Also ensure `exchanged_auth_credential.oauth2.redirect_uri` contains the redirect URI you used.
  * Create a `types.Content` object containing a `types.Part` with a `types.FunctionResponse`.
    * Set `name` to `"adk_request_credential"`. (Note: This is a special name for ADK to proceed with authentication. Do not use other names.)
    * Set `id` to the `auth_request_function_call_id` you saved.
    * Set `response` to the _serialized_ (e.g., `.model_dump()`) updated `AuthConfig` object.
  * Call `runner.run_async` **again** for the same session, passing this `FunctionResponse` content as the `new_message`.

    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-1>)# (Continuing after user interaction)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-2>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-3>)    # Simulate getting the callback URL (e.g., from user paste or web handler)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-4>)    auth_response_uri = await get_user_input(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-5>)        f'Paste the full callback URL here:\n> '
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-6>)    )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-7>)    auth_response_uri = auth_response_uri.strip() # Clean input
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-8>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-9>)    if not auth_response_uri:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-10>)        print("Callback URL not provided. Aborting.")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-11>)        return
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-12>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-13>)    # Update the received AuthConfig with the callback details
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-14>)    auth_config.exchanged_auth_credential.oauth2.auth_response_uri = auth_response_uri
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-15>)    # Also include the redirect_uri used, as the token exchange might need it
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-16>)    auth_config.exchanged_auth_credential.oauth2.redirect_uri = redirect_uri
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-17>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-18>)    # Construct the FunctionResponse Content object
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-19>)    auth_content = types.Content(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-20>)        role='user', # Role can be 'user' when sending a FunctionResponse
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-21>)        parts=[
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-22>)            types.Part(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-23>)                function_response=types.FunctionResponse(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-24>)                    id=auth_request_function_call_id,       # Link to the original request
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-25>)                    name='adk_request_credential', # Special framework function name
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-26>)                    response=auth_config.model_dump() # Send back the *updated* AuthConfig
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-27>)                )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-28>)            )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-29>)        ],
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-30>)    )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-31>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-32>)    # --- Resume Execution ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-33>)    print("\nSubmitting authentication details back to the agent...")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-34>)    events_async_after_auth = runner.run_async(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-35>)        session_id=session.id,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-36>)        user_id='user',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-37>)        new_message=auth_content, # Send the FunctionResponse back
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-38>)    )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-39>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-40>)    # --- Process Final Agent Output ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-41>)    print("\n--- Agent Response after Authentication ---")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-42>)    async for event in events_async_after_auth:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-43>)        # Process events normally, expecting the tool call to succeed now
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-10-44>)        print(event) # Print the full event for inspection
    
Note: Authorization response with Resume feature

If your ADK agent workflow is configured with the [Resume](<https://adk.dev/runtime/resume/>) feature, you also must include the Invocation ID (`invocation_id`) parameter with the authorization response. The Invocation ID you provide must be the same invocation that generated the authorization request, otherwise the system starts a new invocation with the authorization response. If your agent uses the Resume feature, consider including the Invocation ID as a parameter with your authorization request, so it can be included with the authorization response. For more details on using the Resume feature, see [Resume stopped agents](<https://adk.dev/runtime/resume/>).

**Step 5: ADK Handles Token Exchange & Tool Retry and gets Tool result**

  * ADK receives the `FunctionResponse` for `adk_request_credential`.
  * It uses the information in the updated `AuthConfig` (including the callback URL containing the code) to perform the OAuth **token exchange** with the provider's token endpoint, obtaining the access token (and possibly refresh token).
  * ADK internally makes these tokens available by setting them in the session state.
  * ADK **automatically retries** the original tool call (the one that initially failed due to missing auth).
  * This time, the tool finds the valid tokens (via `tool_context.get_auth_response()`) and successfully executes the authenticated API call.
  * The agent receives the actual result from the tool and generates its final response to the user.

* * *

The sequence diagram of auth response flow, where the **_Agent Client_** sends back the auth response and ADK retries the tool, is as follows:

![Authentication](https://adk.dev/assets/auth_part2.svg)

## Build custom tools (`FunctionTool`) requiring authentication[¶](<https://adk.dev/tools-custom/authentication/#build-custom-tools-functiontool-requiring-authentication> "Permanent link")

This section focuses on implementing the authentication logic _inside_ your custom Python function when creating a new ADK Tool. We will implement a `FunctionTool` as an example.

### Prerequisites[¶](<https://adk.dev/tools-custom/authentication/#prerequisites> "Permanent link")

Your function signature _must_ include [`tool_context: ToolContext`](<https://adk.dev/tools-custom/#tool-context>). ADK automatically injects this object, providing access to state and auth mechanisms.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-1>)from google.adk.tools import FunctionTool, ToolContext
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-2>)from typing import Dict
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-3>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-4>)def my_authenticated_tool_function(param1: str, ..., tool_context: ToolContext) -> dict:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-5>)    # ... your logic ...
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-6>)    pass
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-7>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-11-8>)my_tool = FunctionTool(func=my_authenticated_tool_function)
    
### Authentication Logic within the Tool Function[¶](<https://adk.dev/tools-custom/authentication/#authentication-logic-within-the-tool-function> "Permanent link")

Implement the following steps inside your function:

**Step 1: Check for Cached & Valid Credentials:**

Inside your tool function, first check if valid credentials (e.g., access/refresh tokens) are already stored from a previous run in this session. Credentials for the current sessions should be stored in `tool_context.invocation_context.session.state` (a dictionary of state) Check existence of existing credentials by checking `tool_context.invocation_context.session.state.get(credential_name, None)`.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-1>)from google.oauth2.credentials import Credentials
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-2>)from google.auth.transport.requests import Request
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-3>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-4>)# Inside your tool function
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-5>)TOKEN_CACHE_KEY = "my_tool_tokens" # Choose a unique key
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-6>)SCOPES = ["scope1", "scope2"] # Define required scopes
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-7>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-8>)creds = None
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-9>)cached_token_info = tool_context.state.get(TOKEN_CACHE_KEY)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-10>)if cached_token_info:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-11>)    try:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-12>)        creds = Credentials.from_authorized_user_info(cached_token_info, SCOPES)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-13>)        if not creds.valid and creds.expired and creds.refresh_token:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-14>)            creds.refresh(Request())
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-15>)            tool_context.state[TOKEN_CACHE_KEY] = json.loads(creds.to_json()) # Update cache
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-16>)        elif not creds.valid:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-17>)            creds = None # Invalid, needs re-auth
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-18>)            tool_context.state[TOKEN_CACHE_KEY] = None
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-19>)    except Exception as e:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-20>)        print(f"Error loading/refreshing cached creds: {e}")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-21>)        creds = None
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-22>)        tool_context.state[TOKEN_CACHE_KEY] = None
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-23>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-24>)if creds and creds.valid:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-25>)    # Skip to Step 5: Make Authenticated API Call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-26>)    pass
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-27>)else:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-28>)    # Proceed to Step 2...
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-12-29>)    pass
    
**Step 2: Check for Auth Response from Client**

  * If Step 1 didn't yield valid credentials, check if the client just completed the interactive flow by calling `exchanged_credential = tool_context.get_auth_response()`.
  * This returns the updated `exchanged_credential` object sent back by the client (containing the callback URL in `auth_response_uri`).

    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-1>)# Use auth_scheme and auth_credential configured in the tool.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-2>)# exchanged_credential: AuthCredential | None
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-3>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-4>)exchanged_credential = tool_context.get_auth_response(AuthConfig(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-5>)  auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-6>)  raw_auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-7>)))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-8>)# If exchanged_credential is not None, then there is already an exchanged credential from the auth response.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-9>)if exchanged_credential:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-10>)   # ADK exchanged the access token already for us
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-11>)        access_token = exchanged_credential.oauth2.access_token
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-12>)        refresh_token = exchanged_credential.oauth2.refresh_token
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-13>)        creds = Credentials(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-14>)            token=access_token,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-15>)            refresh_token=refresh_token,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-16>)            token_uri=auth_scheme.flows.authorizationCode.tokenUrl,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-17>)            client_id=auth_credential.oauth2.client_id,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-18>)            client_secret=auth_credential.oauth2.client_secret,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-19>)            scopes=list(auth_scheme.flows.authorizationCode.scopes.keys()),
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-20>)        )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-13-21>)    # Cache the token in session state and call the API, skip to step 5
    
**Step 3: Initiate Authentication Request**

If no valid credentials (Step 1.) and no auth response (Step 2.) are found, the tool needs to start the OAuth flow. Define the AuthScheme and initial AuthCredential and call `tool_context.request_credential()`. Return a response indicating authorization is needed.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-1>)# Use auth_scheme and auth_credential configured in the tool.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-2>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-3>)  tool_context.request_credential(AuthConfig(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-4>)    auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-5>)    raw_auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-6>)  ))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-7>)  return {'pending': true, 'message': 'Awaiting user authentication.'}
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-8>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-14-9>)# By setting request_credential, ADK detects a pending authentication event. It pauses execution and ask end user to login.
    
**Step 4: Exchange Authorization Code for Tokens**

ADK automatically generates oauth authorization URL and presents it to your **_Agent Client_** application. your **_Agent Client_** application should follow the same way described in [Build agentic applications with authenticated tools](<https://adk.dev/tools-custom/authentication/#build-agentic-applications-with-authenticated-tools>) to redirect the user to the authorization URL (with `redirect_uri` appended). Once a user completes the login flow, ADK extracts the authentication callback url from **_Agent Client_** applications, automatically parses the auth code, and generates auth token. At the next Tool call, `tool_context.get_auth_response` in step 2 will contain a valid credential to use in subsequent API calls.

**Step 5: Cache Obtained Credentials**

After successfully obtaining the token from ADK (Step 2) or if the token is still valid (Step 1), **immediately store** the new `Credentials` object in `tool_context.state` (serialized, e.g., as JSON) using your cache key.
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-15-1>)# Inside your tool function, after obtaining 'creds' (either refreshed or newly exchanged)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-15-2>)# Cache the new/refreshed tokens
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-15-3>)tool_context.state[TOKEN_CACHE_KEY] = json.loads(creds.to_json())
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-15-4>)print(f"DEBUG: Cached/updated tokens under key: {TOKEN_CACHE_KEY}")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-15-5>)# Proceed to Step 6 (Make API Call)
    
**Step 6: Make Authenticated API Call**

  * Once you have a valid `Credentials` object (`creds` from Step 1 or Step 4), use it to make the actual call to the protected API using the appropriate client library (e.g., `googleapiclient`, `requests`). Pass the `credentials=creds` argument.
  * Include error handling, especially for `HttpError` 401/403, which might mean the token expired or was revoked between calls. If you get such an error, consider clearing the cached token (`tool_context.state.pop(...)`) and potentially returning the `auth_required` status again to force re-authentication.

    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-1>)# Inside your tool function, using the valid 'creds' object
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-2>)# Ensure creds is valid before proceeding
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-3>)if not creds or not creds.valid:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-4>)   return {"status": "error", "error_message": "Cannot proceed without valid credentials."}
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-5>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-6>)try:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-7>)   service = build("calendar", "v3", credentials=creds) # Example
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-8>)   api_result = service.events().list(...).execute()
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-9>)   # Proceed to Step 7
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-10>)except Exception as e:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-11>)   # Handle API errors (e.g., check for 401/403, maybe clear cache and re-request auth)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-12>)   print(f"ERROR: API call failed: {e}")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-16-13>)   return {"status": "error", "error_message": f"API call failed: {e}"}
    
**Step 7: Return Tool Result**

  * After a successful API call, process the result into a dictionary format that is useful for the LLM.
  * **Crucially, include a** along with the data.

    [](<https://adk.dev/tools-custom/authentication/#__codelineno-17-1>)# Inside your tool function, after successful API call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-17-2>)    processed_result = [...] # Process api_result for the LLM
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-17-3>)    return {"status": "success", "data": processed_result}
    
Full Code

Tools and AgentAgent CLIHelperSpec

tools_and_agent.py
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-1>)# Copyright 2026 Google LLC
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-2>)#
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-3>)# Licensed under the Apache License, Version 2.0 (the "License");
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-4>)# you may not use this file except in compliance with the License.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-5>)# You may obtain a copy of the License at
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-6>)#
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-7>)#     http://www.apache.org/licenses/LICENSE-2.0
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-8>)#
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-9>)# Unless required by applicable law or agreed to in writing, software
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-10>)# distributed under the License is distributed on an "AS IS" BASIS,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-11>)# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-12>)# See the License for the specific language governing permissions and
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-13>)# limitations under the License.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-14>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-15>)import os
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-16>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-17>)from google.adk.auth.auth_schemes import OpenIdConnectWithConfig
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-18>)from google.adk.auth.auth_credential import AuthCredential, AuthCredentialTypes, OAuth2Auth
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-19>)from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-20>)from google.adk.agents.llm_agent import LlmAgent
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-21>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-22>)# --- Authentication Configuration ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-23>)# This section configures how the agent will handle authentication using OpenID Connect (OIDC),
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-24>)# often layered on top of OAuth 2.0.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-25>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-26>)# Define the Authentication Scheme using OpenID Connect.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-27>)# This object tells the ADK *how* to perform the OIDC/OAuth2 flow.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-28>)# It requires details specific to your Identity Provider (IDP), like Google OAuth, Okta, Auth0, etc.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-29>)# Note: Replace the example Okta URLs and credentials with your actual IDP details.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-30>)# All following fields are required, and available from your IDP.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-31>)auth_scheme = OpenIdConnectWithConfig(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-32>)    # The URL of the IDP's authorization endpoint where the user is redirected to log in.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-33>)    authorization_endpoint="https://your-endpoint.okta.com/oauth2/v1/authorize",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-34>)    # The URL of the IDP's token endpoint where the authorization code is exchanged for tokens.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-35>)    token_endpoint="https://your-token-endpoint.okta.com/oauth2/v1/token",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-36>)    # The scopes (permissions) your application requests from the IDP.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-37>)    # 'openid' is standard for OIDC. 'profile' and 'email' request user profile info.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-38>)    scopes=['openid', 'profile', "email"]
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-39>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-40>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-41>)# Define the Authentication Credentials for your specific application.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-42>)# This object holds the client identifier and secret that your application uses
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-43>)# to identify itself to the IDP during the OAuth2 flow.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-44>)# !! SECURITY WARNING: Avoid hardcoding secrets in production code. !!
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-45>)# !! Use environment variables or a secret management system instead. !!
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-46>)auth_credential = AuthCredential(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-47>)  auth_type=AuthCredentialTypes.OPEN_ID_CONNECT,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-48>)  oauth2=OAuth2Auth(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-49>)    client_id="CLIENT_ID",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-50>)    client_secret="CLIENT_SECRET",
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-51>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-52>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-53>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-54>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-55>)# --- Toolset Configuration from OpenAPI Specification ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-56>)# This section defines a sample set of tools the agent can use, configured with Authentication
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-57>)# from steps above.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-58>)# This sample set of tools use endpoints protected by Okta and requires an OpenID Connect flow
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-59>)# to acquire end user credentials.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-60>)with open(os.path.join(os.path.dirname(__file__), 'spec.yaml'), 'r') as f:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-61>)    spec_content = f.read()
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-62>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-63>)userinfo_toolset = OpenAPIToolset(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-64>)   spec_str=spec_content,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-65>)   spec_str_type='yaml',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-66>)   # ** Crucially, associate the authentication scheme and credentials with these tools. **
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-67>)   # This tells the ADK that the tools require the defined OIDC/OAuth2 flow.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-68>)   auth_scheme=auth_scheme,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-69>)   auth_credential=auth_credential,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-70>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-71>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-72>)# --- Agent Configuration ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-73>)# Configure and create the main LLM Agent.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-74>)root_agent = LlmAgent(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-75>)    model='gemini-2.0-flash',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-76>)    name='enterprise_assistant',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-77>)    instruction='Help user integrate with multiple enterprise systems, including retrieving user information which may require authentication.',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-78>)    tools=[userinfo_toolset],
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-79>))
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-80>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-81>)# --- Ready for Use ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-82>)# The `root_agent` is now configured with tools protected by OIDC/OAuth2 authentication.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-83>)# When the agent attempts to use one of these tools, the ADK framework will automatically
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-84>)# trigger the authentication flow defined by `auth_scheme` and `auth_credential`
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-85>)# if valid credentials are not already available in the session.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-86>)# The subsequent interaction flow would guide the user through the login process and handle
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-87>)# token exchanging, and automatically attach the exchanged token to the endpoint defined in
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-18-88>)# the tool.
    
agent_cli.py
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-1>)import asyncio
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-2>)from dotenv import load_dotenv
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-3>)from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-4>)from google.adk.runners import Runner
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-5>)from google.adk.sessions import InMemorySessionService
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-6>)from google.genai import types
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-7>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-8>)from .helpers import is_pending_auth_event, get_function_call_id, get_function_call_auth_config, get_user_input
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-9>)from .tools_and_agent import root_agent
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-10>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-11>)load_dotenv()
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-12>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-13>)agent = root_agent
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-14>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-15>)async def async_main():
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-16>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-17>)  Main asynchronous function orchestrating the agent interaction and authentication flow.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-18>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-19>)  # --- Step 1: Service Initialization ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-20>)  # Use in-memory services for session and artifact storage (suitable for demos/testing).
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-21>)  session_service = InMemorySessionService()
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-22>)  artifacts_service = InMemoryArtifactService()
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-23>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-24>)  # Create a new user session to maintain conversation state.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-25>)  session = session_service.create_session(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-26>)      state={},  # Optional state dictionary for session-specific data
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-27>)      app_name='my_app', # Application identifier
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-28>)      user_id='user' # User identifier
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-29>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-30>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-31>)  # --- Step 2: Initial User Query ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-32>)  # Define the user's initial request.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-33>)  query = 'Show me my user info'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-34>)  print(f"user: {query}")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-35>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-36>)  # Format the query into the Content structure expected by the ADK Runner.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-37>)  content = types.Content(role='user', parts=[types.Part(text=query)])
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-38>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-39>)  # Initialize the ADK Runner
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-40>)  runner = Runner(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-41>)      app_name='my_app',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-42>)      agent=agent,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-43>)      artifact_service=artifacts_service,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-44>)      session_service=session_service,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-45>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-46>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-47>)  # --- Step 3: Send Query and Handle Potential Auth Request ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-48>)  print("\nRunning agent with initial query...")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-49>)  events_async = runner.run_async(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-50>)      session_id=session.id, user_id='user', new_message=content
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-51>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-52>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-53>)  # Variables to store details if an authentication request occurs.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-54>)  auth_request_event_id, auth_config = None, None
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-55>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-56>)  # Iterate through the events generated by the first run.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-57>)  async for event in events_async:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-58>)    # Check if this event is the specific 'adk_request_credential' function call.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-59>)    if is_pending_auth_event(event):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-60>)      print("--> Authentication required by agent.")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-61>)      auth_request_event_id = get_function_call_id(event)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-62>)      auth_config = get_function_call_auth_config(event)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-63>)      # Once the auth request is found and processed, exit this loop.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-64>)      # We need to pause execution here to get user input for authentication.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-65>)      break
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-66>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-67>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-68>)  # If no authentication request was detected after processing all events, exit.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-69>)  if not auth_request_event_id or not auth_config:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-70>)      print("\nAuthentication not required for this query or processing finished.")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-71>)      return # Exit the main function
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-72>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-73>)  # --- Step 4: Manual Authentication Step (Simulated OAuth 2.0 Flow) ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-74>)  # This section simulates the user interaction part of an OAuth 2.0 flow.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-75>)  # In a real web application, this would involve browser redirects.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-76>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-77>)  # Define the Redirect URI. This *must* match one of the URIs registered
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-78>)  # with the OAuth provider for your application. The provider sends the user
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-79>)  # back here after they approve the request.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-80>)  redirect_uri = 'http://localhost:8000/dev-ui' # Example for local development
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-81>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-82>)  # Construct the Authorization URL that the user must visit.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-83>)  # This typically includes the provider's authorization endpoint URL,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-84>)  # client ID, requested scopes, response type (e.g., 'code'), and the redirect URI.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-85>)  # Here, we retrieve the base authorization URI from the AuthConfig provided by ADK
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-86>)  # and append the redirect_uri.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-87>)  # NOTE: A robust implementation would use urlencode and potentially add state, scope, etc.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-88>)  auth_request_uri = (
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-89>)      auth_config.exchanged_auth_credential.oauth2.auth_uri
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-90>)      + f'&redirect_uri={redirect_uri}' # Simple concatenation; ensure correct query param format
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-91>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-92>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-93>)  print("\n--- User Action Required ---")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-94>)  # Prompt the user to visit the authorization URL, log in, grant permissions,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-95>)  # and then paste the *full* URL they are redirected back to (which contains the auth code).
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-96>)  auth_response_uri = await get_user_input(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-97>)      f'1. Please open this URL in your browser to log in:\n   {auth_request_uri}\n\n'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-98>)      f'2. After successful login and authorization, your browser will be redirected.\n'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-99>)      f'   Copy the *entire* URL from the browser\'s address bar.\n\n'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-100>)      f'3. Paste the copied URL here and press Enter:\n\n> '
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-101>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-102>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-103>)  # --- Step 5: Prepare Authentication Response for the Agent ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-104>)  # Update the AuthConfig object with the information gathered from the user.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-105>)  # The ADK framework needs the full response URI (containing the code)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-106>)  # and the original redirect URI to complete the OAuth token exchange process internally.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-107>)  auth_config.exchanged_auth_credential.oauth2.auth_response_uri = auth_response_uri
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-108>)  auth_config.exchanged_auth_credential.oauth2.redirect_uri = redirect_uri
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-109>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-110>)  # Construct a FunctionResponse Content object to send back to the agent/runner.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-111>)  # This response explicitly targets the 'adk_request_credential' function call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-112>)  # identified earlier by its ID.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-113>)  auth_content = types.Content(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-114>)      role='user',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-115>)      parts=[
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-116>)          types.Part(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-117>)              function_response=types.FunctionResponse(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-118>)                  # Crucially, link this response to the original request using the saved ID.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-119>)                  id=auth_request_event_id,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-120>)                  # The special name of the function call we are responding to.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-121>)                  name='adk_request_credential',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-122>)                  # The payload containing all necessary authentication details.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-123>)                  response=auth_config.model_dump(),
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-124>)              )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-125>)          )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-126>)      ],
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-127>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-128>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-129>)  # --- Step 6: Resume Execution with Authentication ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-130>)  print("\nSubmitting authentication details back to the agent...")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-131>)  # Run the agent again, this time providing the `auth_content` (FunctionResponse).
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-132>)  # The ADK Runner intercepts this, processes the 'adk_request_credential' response
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-133>)  # (performs token exchange, stores credentials), and then allows the agent
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-134>)  # to retry the original tool call that required authentication, now succeeding with
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-135>)  # a valid access token embedded.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-136>)  events_async = runner.run_async(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-137>)      session_id=session.id,
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-138>)      user_id='user',
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-139>)      new_message=auth_content, # Provide the prepared auth response
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-140>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-141>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-142>)  # Process and print the final events from the agent after authentication is complete.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-143>)  # This stream now contain the actual result from the tool (e.g., the user info).
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-144>)  print("\n--- Agent Response after Authentication ---")
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-145>)  async for event in events_async:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-146>)    print(event)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-147>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-148>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-149>)if __name__ == '__main__':
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-19-150>)  asyncio.run(async_main())
    
helpers.py
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-1>)from google.adk.auth import AuthConfig
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-2>)from google.adk.events import Event
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-3>)import asyncio
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-4>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-5>)# --- Helper Functions ---
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-6>)async def get_user_input(prompt: str) -> str:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-7>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-8>)  Asynchronously prompts the user for input in the console.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-9>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-10>)  Uses asyncio's event loop and run_in_executor to avoid blocking the main
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-11>)  asynchronous execution thread while waiting for synchronous `input()`.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-12>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-13>)  Args:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-14>)    prompt: The message to display to the user.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-15>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-16>)  Returns:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-17>)    The string entered by the user.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-18>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-19>)  loop = asyncio.get_event_loop()
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-20>)  # Run the blocking `input()` function in a separate thread managed by the executor.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-21>)  return await loop.run_in_executor(None, input, prompt)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-22>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-23>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-24>)def is_pending_auth_event(event: Event) -> bool:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-25>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-26>)  Checks if an ADK Event represents a request for user authentication credentials.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-27>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-28>)  The ADK framework emits a specific function call ('adk_request_credential')
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-29>)  when a tool requires authentication that hasn't been previously satisfied.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-30>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-31>)  Args:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-32>)    event: The ADK Event object to inspect.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-33>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-34>)  Returns:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-35>)    True if the event is an 'adk_request_credential' function call, False otherwise.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-36>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-37>)  # Safely checks nested attributes to avoid errors if event structure is incomplete.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-38>)  return (
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-39>)      event.content
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-40>)      and event.content.parts
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-41>)      and event.content.parts[0] # Assuming the function call is in the first part
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-42>)      and event.content.parts[0].function_call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-43>)      # The specific function name indicating an auth request from the ADK framework.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-44>)      and event.content.parts[0].function_call.name == 'adk_request_credential'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-45>)  )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-46>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-47>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-48>)def get_function_call_id(event: Event) -> str:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-49>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-50>)  Extracts the unique ID of the function call from an ADK Event.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-51>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-52>)  This ID is crucial for correlating a function *response* back to the specific
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-53>)  function *call* that the agent initiated to request for auth credentials.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-54>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-55>)  Args:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-56>)    event: The ADK Event object containing the function call.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-57>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-58>)  Returns:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-59>)    The unique identifier string of the function call.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-60>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-61>)  Raises:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-62>)    ValueError: If the function call ID cannot be found in the event structure.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-63>)                (Corrected typo from `contents` to `content` below)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-64>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-65>)  # Navigate through the event structure to find the function call ID.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-66>)  if (
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-67>)      event
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-68>)      and event.content
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-69>)      and event.content.parts
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-70>)      and event.content.parts[0] # Use content, not contents
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-71>)      and event.content.parts[0].function_call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-72>)      and event.content.parts[0].function_call.id
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-73>)  ):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-74>)    return event.content.parts[0].function_call.id
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-75>)  # If the ID is missing, raise an error indicating an unexpected event format.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-76>)  raise ValueError(f'Cannot get function call id from event {event}')
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-77>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-78>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-79>)def get_function_call_auth_config(event: Event) -> AuthConfig:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-80>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-81>)  Extracts the authentication configuration details from an 'adk_request_credential' event.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-82>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-83>)  Client should use this AuthConfig to necessary authentication details (like OAuth codes and state)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-84>)  and sent it back to the ADK to continue OAuth token exchanging.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-85>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-86>)  Args:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-87>)    event: The ADK Event object containing the 'adk_request_credential' call.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-88>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-89>)  Returns:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-90>)    An AuthConfig object populated with details from the function call arguments.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-91>)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-92>)  Raises:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-93>)    ValueError: If the 'auth_config' argument cannot be found in the event.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-94>)                (Corrected typo from `contents` to `content` below)
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-95>)  """
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-96>)  if (
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-97>)      event
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-98>)      and event.content
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-99>)      and event.content.parts
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-100>)      and event.content.parts[0] # Use content, not contents
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-101>)      and event.content.parts[0].function_call
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-102>)      and event.content.parts[0].function_call.args
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-103>)      and event.content.parts[0].function_call.args.get('auth_config')
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-104>)  ):
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-105>)    # Reconstruct the AuthConfig object using the dictionary provided in the arguments.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-106>)    # The ** operator unpacks the dictionary into keyword arguments for the constructor.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-107>)    return AuthConfig(
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-108>)          **event.content.parts[0].function_call.args.get('auth_config')
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-109>)      )
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-20-110>)  raise ValueError(f'Cannot get auth config from event {event}')
    
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-1>)openapi: 3.0.1
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-2>)info:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-3>)title: Okta User Info API
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-4>)version: 1.0.0
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-5>)description: |-
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-6>)   API to retrieve user profile information based on a valid Okta OIDC Access Token.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-7>)   Authentication is handled via OpenID Connect with Okta.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-8>)contact:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-9>)   name: API Support
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-10>)   email: support@example.com # Replace with actual contact if available
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-11>)servers:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-12>)- url: <substitute with your server name>
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-13>)   description: Production Environment
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-14>)paths:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-15>)/okta-jwt-user-api:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-16>)   get:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-17>)      summary: Get Authenticated User Info
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-18>)      description: |-
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-19>)      Fetches profile details for the user
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-20>)      operationId: getUserInfo
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-21>)      tags:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-22>)      - User Profile
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-23>)      security:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-24>)      - okta_oidc:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-25>)            - openid
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-26>)            - email
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-27>)            - profile
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-28>)      responses:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-29>)      '200':
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-30>)         description: Successfully retrieved user information.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-31>)         content:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-32>)            application/json:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-33>)            schema:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-34>)               type: object
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-35>)               properties:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-36>)                  sub:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-37>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-38>)                  description: Subject identifier for the user.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-39>)                  example: "abcdefg"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-40>)                  name:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-41>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-42>)                  description: Full name of the user.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-43>)                  example: "Example LastName"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-44>)                  locale:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-45>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-46>)                  description: User's locale, e.g., en-US or en_US.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-47>)                  example: "en_US"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-48>)                  email:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-49>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-50>)                  format: email
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-51>)                  description: User's primary email address.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-52>)                  example: "username@example.com"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-53>)                  preferred_username:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-54>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-55>)                  description: Preferred username of the user (often the email).
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-56>)                  example: "username@example.com"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-57>)                  given_name:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-58>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-59>)                  description: Given name (first name) of the user.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-60>)                  example: "Example"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-61>)                  family_name:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-62>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-63>)                  description: Family name (last name) of the user.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-64>)                  example: "LastName"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-65>)                  zoneinfo:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-66>)                  type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-67>)                  description: User's timezone, e.g., America/Los_Angeles.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-68>)                  example: "America/Los_Angeles"
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-69>)                  updated_at:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-70>)                  type: integer
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-71>)                  format: int64 # Using int64 for Unix timestamp
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-72>)                  description: Timestamp when the user's profile was last updated (Unix epoch time).
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-73>)                  example: 1743617719
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-74>)                  email_verified:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-75>)                  type: boolean
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-76>)                  description: Indicates if the user's email address has been verified.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-77>)                  example: true
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-78>)               required:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-79>)                  - sub
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-80>)                  - name
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-81>)                  - locale
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-82>)                  - email
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-83>)                  - preferred_username
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-84>)                  - given_name
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-85>)                  - family_name
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-86>)                  - zoneinfo
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-87>)                  - updated_at
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-88>)                  - email_verified
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-89>)      '401':
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-90>)         description: Unauthorized. The provided Bearer token is missing, invalid, or expired.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-91>)         content:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-92>)            application/json:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-93>)            schema:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-94>)               $ref: '#/components/schemas/Error'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-95>)      '403':
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-96>)         description: Forbidden. The provided token does not have the required scopes or permissions to access this resource.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-97>)         content:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-98>)            application/json:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-99>)            schema:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-100>)               $ref: '#/components/schemas/Error'
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-101>)components:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-102>)securitySchemes:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-103>)   okta_oidc:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-104>)      type: openIdConnect
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-105>)      description: Authentication via Okta using OpenID Connect. Requires a Bearer Access Token.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-106>)      openIdConnectUrl: https://your-endpoint.okta.com/.well-known/openid-configuration
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-107>)schemas:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-108>)   Error:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-109>)      type: object
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-110>)      properties:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-111>)      code:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-112>)         type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-113>)         description: An error code.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-114>)      message:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-115>)         type: string
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-116>)         description: A human-readable error message.
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-117>)      required:
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-118>)         - code
    [](<https://adk.dev/tools-custom/authentication/#__codelineno-21-119>)         - message
    
Back to top 