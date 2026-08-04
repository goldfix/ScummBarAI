# LLMs | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/integrations/llms/](https://pydantic.dev/docs/validation/latest/integrations/llms/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/integrations/llms/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# LLMs

The Pydantic documentation is available in the [llms.txt](<https://llmstxt.org/>) format. This format is defined in Markdown and suited for large language models.

Two formats are available:

  * [llms.txt](<https://docs.pydantic.dev/latest/llms.txt>): a file containing a brief description of the project, along with links to the different sections of the documentation. The structure of this file is described in details in the [format documentation](<https://llmstxt.org/#format>).
  * [llms-full.txt](<https://docs.pydantic.dev/latest/llms-full.txt>): Similar to the `llms.txt` file, but every link content is included. Note that this file may be too large for some LLMs.

As of today, these files _cannot_ be natively leveraged by LLM frameworks or IDEs. Alternatively, a [MCP server](<https://modelcontextprotocol.io/>) can be implemented to properly parse the `llms.txt` file.

Was this page helpful?

Thanks for your feedback!