# Installation | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/get-started/install/](https://pydantic.dev/docs/validation/latest/get-started/install/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/get-started/install/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Installation

Installation is as simple as:

  * [ pip ](<https://pydantic.dev/docs/validation/latest/get-started/install/#tab-panel-761>)
  * [ uv ](<https://pydantic.dev/docs/validation/latest/get-started/install/#tab-panel-762>)

Terminal
    
    pip install pydantic
    
Terminal
    
    uv add pydantic
    
Pydantic has a few dependencies:

  * [`pydantic-core`](<https://pypi.org/project/pydantic-core/>): Core validation logic for Pydantic written in Rust.
  * [`typing-extensions`](<https://pypi.org/project/typing-extensions/>): Backport of the standard library [typing](<https://docs.python.org/3/library/typing.html#module-typing>) module.
  * [`annotated-types`](<https://pypi.org/project/annotated-types/>): Reusable constraint types to use with [`typing.Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>).

If you’ve got Python 3.9+ and `pip` installed, you’re good to go.

Pydantic is also available on [conda](<https://www.anaconda.com>) under the [conda-forge](<https://conda-forge.org>) channel:

Terminal
    
    conda install pydantic -c conda-forge
    
## Optional dependencies

[](<https://pydantic.dev/docs/validation/latest/get-started/install/#optional-dependencies>)

Pydantic has the following optional dependencies:

  * `email`: Email validation provided by the [email-validator](<https://pypi.org/project/email-validator/>) package.
  * `timezone`: Fallback IANA time zone database provided by the [tzdata](<https://pypi.org/project/tzdata/>) package.

To install optional dependencies along with Pydantic:

  * [ pip ](<https://pydantic.dev/docs/validation/latest/get-started/install/#tab-panel-763>)
  * [ uv ](<https://pydantic.dev/docs/validation/latest/get-started/install/#tab-panel-764>)

Terminal
    
    # with the `email` extra:
    pip install 'pydantic[email]'
    # or with `email` and `timezone` extras:
    pip install 'pydantic[email,timezone]'
    
Terminal
    
    # with the `email` extra:
    uv add 'pydantic[email]'
    # or with `email` and `timezone` extras:
    uv add 'pydantic[email,timezone]'
    
Of course, you can also install requirements manually with `pip install email-validator tzdata`.

## Install from repository

[](<https://pydantic.dev/docs/validation/latest/get-started/install/#install-from-repository>)

And if you prefer to install Pydantic directly from the repository:

  * [ pip ](<https://pydantic.dev/docs/validation/latest/get-started/install/#tab-panel-765>)
  * [ uv ](<https://pydantic.dev/docs/validation/latest/get-started/install/#tab-panel-766>)

Terminal
    
    pip install 'git+https://github.com/pydantic/pydantic@main'
    # or with `email` and `timezone` extras:
    pip install 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
    
Terminal
    
    uv add 'git+https://github.com/pydantic/pydantic@main'
    # or with `email` and `timezone` extras:
    uv add 'git+https://github.com/pydantic/pydantic@main#egg=pydantic[email,timezone]'
    
Was this page helpful?

Thanks for your feedback!