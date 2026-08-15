# What's new in Gemini 3.7 Flash  |  Gemini API  |  Google AI for Developers

> Source: [https://ai.google.dev/gemini-api/docs/latest-model](https://ai.google.dev/gemini-api/docs/latest-model)

[ Skip to main content ](<https://ai.google.dev/gemini-api/docs/latest-model#main-content>)

[ ![Gemini API](https://ai.google.dev/_static/googledevai/images/gemini-api-logo.svg) ](<https://ai.google.dev/>)

  * 

  * English
  * Deutsch
  * Español – América Latina
  * Français
  * Indonesia
  * Italiano
  * Polski
  * Português – Brasil
  * Shqip
  * Tiếng Việt
  * Türkçe
  * Русский
  * עברית
  * العربيّة
  * فارسی
  * हिंदी
  * বাংলা
  * ภาษาไทย
  * 中文 – 简体
  * 中文 – 繁體
  * 日本語
  * 한국어

[ Get API key ](<https://aistudio.google.com/apikey>) [ Cookbook ](<https://github.com/google-gemini/cookbook>) [ Community ](<https://discuss.ai.google.dev/c/gemini-api/>) Sign in

The [Interactions API](<https://ai.google.dev/gemini-api/docs/interactions-overview>) is now generally available. We recommend using this API for access to all the latest features and models. 

  * [ Home ](<https://ai.google.dev/>)
  * [ Gemini API ](<https://ai.google.dev/gemini-api>)
  * [ Docs ](<https://ai.google.dev/gemini-api/docs>)

Send feedback 

#  What's new in Gemini 3.7 Flash

[This page](<https://ai.google.dev/gemini-api/docs/latest-model>) [All models](<https://ai.google.dev/gemini-api/docs/models>)

Gemini 3.7 Flash (`gemini-3.7-flash`) is generally available (GA) and ready for production use. It is our most intelligent workhorse model yet for coding and agents.

This guide explains what's new in Gemini 3.7 Flash, API changes, code examples, and migration guidance.

## New model

Model | Model ID | Default thinking level | Pricing | Description  
---|---|---|---|---  
Gemini 3.7 Flash | `gemini-3.7-flash` | `medium` | 3.7 Flash is available through the end of year at an introductory price of $0.75/1M input tokens and $3.75/1M output tokens; see [pricing](<https://ai.google.dev/gemini-api/docs/pricing>) for more details. | Our most capable Flash model, built for complex coding, agentic workflows, and reliable multi-step execution.  
  
Gemini 3.7 Flash supports a 1M token context window, 64k max output tokens, tunable thinking levels (`low`, `medium`, `high`), and the same suite of built-in tools as 3.6 Flash.

For complete specs, see the [Gemini 3.7 Flash model page](<https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash>). For detailed pricing, see the [pricing page](<https://ai.google.dev/gemini-api/docs/pricing>).

## Quickstart

### Python
    
    from google import genai
    
    client = genai.Client()
    
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input="Write a three.js script that renders a realistic 3D black hole."
    )
    
    print(interaction.output_text)
    
### JavaScript
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const interaction = await client.interactions.create({
      model: "gemini-3.7-flash",
      input: "Write a three.js script that renders a realistic 3D black hole.",
    });
    
    console.log(interaction.output_text);
    
### REST
    
    curl "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "model": "gemini-3.7-flash",
        "input": "Write a three.js script that renders a realistic 3D black hole."
      }'
    
## What's new in Gemini 3.7 Flash

  * **Coding and agentic tasks:** Significantly higher quality on real-world software engineering and agentic benchmarks, improving issue resolution and reducing failed agent loops.
  * **Web development and stronger design parity:** Generates higher-fidelity desktop and web application code directly from design mocks, with strong gains in design adherence and in auditing existing codebases against mocks to verify 1:1 design parity.
  * **Promotional pricing:** Gemini 3.7 Flash will be available at an introductory price of $0.75/1M input tokens and $3.75/1M output tokens. We’re also applying this new rate to 3.6 Flash. Introductory pricing expires on December 31, 2026; after, $1.50/1M input tokens and $7.50/1M output tokens will apply.

## Choosing the right model

Reference the below table to review recommended migration targets for your workloads. To upgrade from Gemini 3.5 Flash, Gemini 3 Flash (Preview), or Gemini 3.1 Pro, ensure you remove deprecated sampling parameters (`temperature`, `top_p`, `top_k`) and prefilled model turns. Gemini 3.6 Flash already no longer supported these parameters.

Model | Primary use cases | Recommended migration target  
---|---|---  
**Gemini 3.7 Flash**  
`gemini-3.7-flash` | Code generation, spatial/multimodal reasoning, multi-step agentic workflows, design adherence | **Gemini 3.6 Flash** , **Gemini 3.5 Flash** , **Gemini 3 Flash (Preview)** , or **Gemini 3.1 Pro**  
  
## Understanding reasoning levels

Gemini 3.7 Flash gives developers flexible control over latency and intelligence by adjusting the model's thinking level:

  * **Low thinking effort** : Reduces time-to-answer for latency-critical tasks like incident response pipelines, real-time chat, writing drafts, and fast data analysis.
  * **Medium (default):** Best quality for most tasks. Recommended for complex code and agentic use cases, with higher first-pass accuracy.
  * **High thinking effort** : Maximizes the model's ability to think and use tools. Best for complex reasoning, hard math, and the most difficult coding and agent tasks. Allows extended thoughts and function calls, with higher token consumption and cost.

### Python
    
    from google import genai
    
    client = genai.Client()
    
    interaction = client.interactions.create(
        model="gemini-3.7-flash",
        input="Analyze this payment processing pipeline for race conditions during retry attempts and rewrite the transaction locks safely.",
        generation_config={
            "thinking_level": "medium"  # Balanced reasoning effort for complex tasks
        }
    )
    
    print(interaction.output_text)
    
### JavaScript
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const interaction = await client.interactions.create({
      model: "gemini-3.7-flash",
      input: "Analyze this payment processing pipeline for race conditions during retry attempts and rewrite the transaction locks safely.",
      generation_config: {
        thinking_level: "medium"
      }
    });
    
    console.log(interaction.output_text);
    
### REST
    
    curl "https://generativelanguage.googleapis.com/v1beta/interactions" \
      -H "x-goog-api-key: $GEMINI_API_KEY" \
      -H 'Content-Type: application/json' \
      -X POST \
      -d '{
        "model": "gemini-3.7-flash",
        "input": "Analyze this payment processing pipeline for race conditions during retry attempts and rewrite the transaction locks safely.",
        "generation_config": {
          "thinking_level": "medium"
        }
      }'
    
## Updated Antigravity agent

Due to its improved performance and reasoning, Gemini 3.7 Flash is now the new default model powering the [Antigravity agent](<https://ai.google.dev/gemini-api/docs/antigravity-agent>) in Gemini Managed Agents and [Google Antigravity SDK](<https://antigravity.google/product/antigravity-sdk>).

### Python
    
    from google import genai
    
    client = genai.Client()
    
    interaction = client.interactions.create(
        agent="antigravity-preview-05-2026",
        input=(
            "Audit https://web.dev for performance, Core Web Vitals, and SEO. "
            "Query Google's PageSpeed Insights API for both Mobile and Desktop strategies. "
            "Check search indexing with Google Search for site:web.dev. "
            "Format the output as a side-by-side scorecard table with prioritized fixes."
        ),
        environment="remote",
    )
    
    print(interaction.output_text)
    
### JavaScript
    
    import { GoogleGenAI } from "@google/genai";
    
    const client = new GoogleGenAI({});
    
    const interaction = await client.interactions.create({
      agent: "antigravity-preview-05-2026",
      input: "Audit https://web.dev for performance, Core Web Vitals, and SEO. Query Google's PageSpeed Insights API for both Mobile and Desktop strategies. Check search indexing with Google Search for site:web.dev. Format the output as a side-by-side scorecard table with prioritized fixes.",
      environment: "remote",
    }, { timeout: 300000 });
    
    console.log(interaction.output_text);
    
### REST
    
    curl -X POST "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $GEMINI_API_KEY" \
    -d '{
        "agent": "antigravity-preview-05-2026",
        "input": "Audit https://web.dev for performance, Core Web Vitals, and SEO. Query Google'\''s PageSpeed Insights API for both Mobile and Desktop strategies. Check search indexing with Google Search for site:web.dev. Format the output as a side-by-side scorecard table with prioritized fixes.",
        "environment": "remote"
    }'
    
The underlying Gemini model [can be configured](<https://ai.google.dev/gemini-api/docs/antigravity-agent#model-selection>) using `agent_config`.

## Migration checklist
    
      `/gemini-interactions-api migrate my app to Gemini 3.7 Flash`
    
### Migrate to gemini-3.7-flash

  * **Update Model ID:** Change your target model string to `gemini-3.7-flash`.
  * **Remove deprecated sampling parameters:**
    * Strip `temperature`, `top_p`, and `top_k` from generation configs.
    * Replace `thinking_budget` with the string enum `thinking_level`.
    * Remove `candidate_count` (unsupported in Gemini 3.x).
  * **Enforce turn validation rules:**
    * Standardize multi-turn conversations on server-side `previous_interaction_id`.
    * Remove prefilled model turns.
  * **Audit function calling:**
    * Place multimodal assets inside the response payload.
    * Format inline instructions using `\n\n`.
    * If you see `Malformed_Function_Call` errors tied to pre-tool text, see [Workarounds for pre-tool text requirements](<https://ai.google.dev/gemini-api/docs/function-calling#workarounds-for-pre-tool-text-requirements>).
    * Only if using generateContent API: Ensure all `FunctionResponse` objects include `call_id` and `name`.
  * **Baseline Gemini 3.x requirements:** For SDK updates and thought signature preservation, see the [Gemini 3.5 Migration Checklist](<https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5#migration>).

## Pricing

Introductory pricing applies across Google AI Studio and Gemini Enterprise Agent Platform through December 31, 2026 for both Gemini 3.7 Flash and Gemini 3.6 Flash. From January 1, 2027, standard pricing will take effect. For details, please see [pricing page](<https://ai.google.dev/gemini-api/docs/pricing>).

## Next steps

  * Review API specs on the [Models Overview](<https://ai.google.dev/gemini-api/docs/models>).
  * Explore multi-agent orchestration in the [Interactions API Guide](<https://ai.google.dev/gemini-api/docs/interactions>).
  * Test and refine prompts in [Google AI Studio](<https://aistudio.google.com/>).

Send feedback 

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](<https://creativecommons.org/licenses/by/4.0/>), and code samples are licensed under the [Apache 2.0 License](<https://www.apache.org/licenses/LICENSE-2.0>). For details, see the [Google Developers Site Policies](<https://developers.google.com/site-policies>). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-08-13 UTC.

Need to tell us more?  [[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-08-13 UTC."],[],[]] 