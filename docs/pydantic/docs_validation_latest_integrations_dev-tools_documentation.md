# Documentation | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/integrations/dev-tools/documentation/](https://pydantic.dev/docs/validation/latest/integrations/dev-tools/documentation/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/integrations/dev-tools/documentation/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Documentation

Pydantic uses [MkDocs](<https://www.mkdocs.org/>) for documentation, together with [mkdocstrings](<https://mkdocstrings.github.io/>). As such, you can make use of Pydantic’s Sphinx object inventory to cross-reference the Pydantic API documentation.

  * [ Sphinx ](<https://pydantic.dev/docs/validation/latest/integrations/dev-tools/documentation/#tab-panel-771>)
  * [ mkdocstrings ](<https://pydantic.dev/docs/validation/latest/integrations/dev-tools/documentation/#tab-panel-772>)

In your [Sphinx configuration](<https://www.sphinx-doc.org/en/master/usage/configuration.html>), add the following to the [`intersphinx` extension configuration](<https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration>):
    
    intersphinx_mapping = {
      'pydantic': ('https://docs.pydantic.dev/latest', None),  # (1)
    }

You can also use `dev` instead of `latest` to target the latest documentation build, up to date with the [`main`](<https://github.com/pydantic/pydantic/tree/main>) branch.

In your [MkDocs configuration](<https://www.mkdocs.org/user-guide/configuration/>), add the following import to your [mkdocstrings plugin configuration](<https://mkdocstrings.github.io/usage/#cross-references-to-other-projects-inventories>):
    
    plugins:
    - mkdocstrings:
      handlers:
        python:
          import:
          - https://docs.pydantic.dev/latest/objects.inv  # (1)

You can also use `dev` instead of `latest` to target the latest documentation build, up to date with the [`main`](<https://github.com/pydantic/pydantic/tree/main>) branch.

Was this page helpful?

Thanks for your feedback!