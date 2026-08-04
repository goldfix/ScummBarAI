# Linting | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/integrations/dev-tools/linting/](https://pydantic.dev/docs/validation/latest/integrations/dev-tools/linting/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/integrations/dev-tools/linting/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Linting

## Flake8 plugin

[](<https://pydantic.dev/docs/validation/latest/integrations/dev-tools/linting/#flake8-plugin>)

If using Flake8 in your project, a [plugin](<https://pypi.org/project/flake8-pydantic/>) is available and can be installed using the following:

Terminal
    
    pip install flake8-pydantic
    
The lint errors provided by this plugin are namespaced under the `PYDXXX` code. To ignore some unwanted rules, the Flake8 configuration can be adapted:
    
    [flake8]
    extend-ignore = PYD001,PYD002
    
Was this page helpful?

Thanks for your feedback!