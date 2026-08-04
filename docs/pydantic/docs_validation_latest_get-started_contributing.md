# Contributing | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/get-started/contributing/](https://pydantic.dev/docs/validation/latest/get-started/contributing/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Contributing

We’d love you to contribute to Pydantic!

## Issues

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#issues>)

Questions, feature requests and bug reports are all welcome as [discussions or issues](<https://github.com/pydantic/pydantic/issues/new/choose>). **However, to report a security vulnerability, please see our[security policy](<https://github.com/pydantic/pydantic/security/policy>).**

To make it as simple as possible for us to help you, please include the output of the following call in your issue:

Terminal
    
    python -c "import pydantic.version; print(pydantic.version.version_info())"
    
If you’re using Pydantic prior to **v2.0** please use:

Terminal
    
    python -c "import pydantic.utils; print(pydantic.utils.version_info())"
    
Please try to always include the above unless you’re unable to install Pydantic or **know** it’s not relevant to your question or feature request.

## Pull Requests

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#pull-requests>)

It should be extremely simple to get started and create a Pull Request. Pydantic is released regularly so you should see your improvements release in a matter of days or weeks 🚀.

Unless your change is trivial (typo, docs tweak etc.), please create an issue to discuss the change before creating a pull request.

If you’re looking for something to get your teeth into, check out the [“help wanted”](<https://github.com/pydantic/pydantic/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22>) label on github.

To make contributing as easy and fast as possible, you’ll want to run tests and linting locally. Luckily, Pydantic has few dependencies, doesn’t require compiling and tests don’t need access to databases, etc. Because of this, setting up and running the tests should be very simple.

### Prerequisites

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#prerequisites>)

You’ll need the following prerequisites:

  * Any Python version between **Python 3.9 and 3.12**
  * [**uv**](<https://docs.astral.sh/uv/getting-started/installation/>) or other virtual environment tool
  * [**git**](<https://git-scm.com/>) \- For version control
  * [**make**](<https://www.gnu.org/software/make/>) \- For running development commands (or use `nmake` on Windows)
  * [**Rust**](<https://rustup.rs/>) \- Rust stable (or nightly for coverage)

### Installation and setup

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#installation-and-setup>)

Fork the repository on GitHub and clone your fork locally.

Terminal
    
    # Clone your fork and cd into the repo directory
    git clone git@github.com:<your username>/pydantic.git
    cd pydantic
    
    # Install UV and pre-commit
    # We use pipx here, for other options see:
    # https://docs.astral.sh/uv/getting-started/installation/
    # https://pre-commit.com/#install
    # To get pipx itself:
    # https://pypa.github.io/pipx/
    pipx install uv
    pipx install pre-commit
    
    # Install pydantic, dependencies, test dependencies and doc dependencies
    make install
    
### Check out a new branch and make your changes

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#check-out-a-new-branch-and-make-your-changes>)

Create a new branch for your changes.

Terminal
    
    # Checkout a new branch and make your changes
    git switch -c my-new-feature-branch
    # Make your changes...
    
### Run tests and linting

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#run-tests-and-linting>)

Run tests and linting locally to make sure everything is working as expected.

Terminal
    
    # Run automated code formatting and linting
    make format
    # Pydantic uses ruff, an awesome Python linter written in rust
    # https://github.com/astral-sh/ruff
    
    # Run tests and linting
    make
    # There are a few sub-commands in Makefile like `test`, `testcov` and `lint`
    # which you might want to use, but generally just `make` should be all you need.
    # You can run `make help` to see more options.
    
### Build documentation

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#build-documentation>)

If you’ve made any changes to the documentation (including changes to function signatures, class definitions, or docstrings that will appear in the API documentation), make sure it builds successfully.

We use `mkdocs-material[imaging]` to support social previews (see the [plugin documentation](<https://squidfunk.github.io/mkdocs-material/plugins/requirements/image-processing/>)).

Terminal
    
    # Build documentation
    make docs
    # If you have changed the documentation, make sure it builds successfully.
    # You can also use `uv run mkdocs serve` to serve the documentation at localhost:8000
    
If this isn’t working due to issues with the imaging plugin, try commenting out the `social` plugin line in `mkdocs.yml` and running `make docs` again.

#### Updating the documentation

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#updating-the-documentation>)

We push a new version of the documentation with each minor release, and we push to a `dev` path with each commit to `main`.

If you’re updating the documentation out of cycle with a minor release and want your changes to be reflected on `latest`, do the following:

  1. Open a PR against `main` with your docs changes
  2. Once the PR is merged, checkout the `docs-update` branch. This branch should be up to date with the latest patch release. For example, if the latest release is `v2.9.2`, you should make sure `docs-update` is up to date with the `v2.9.2` tag.
  3. Checkout a new branch from `docs-update` and cherry-pick your changes onto this branch.
  4. Push your changes and open a PR against `docs-update`.
  5. Once the PR is merged, the new docs will be built and deployed.

### Commit and push your changes

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#commit-and-push-your-changes>)

Commit your changes, push your branch to GitHub, and create a pull request.

Please follow the pull request template and fill in as much information as possible. Link to any relevant issues and include a description of your changes.

When your pull request is ready for review, add a comment with the message “please review” and we’ll take a look as soon as we can.

## Documentation style

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#documentation-style>)

Documentation is written in Markdown and built using [Material for MkDocs](<https://squidfunk.github.io/mkdocs-material/>). API documentation is built from docstrings using [mkdocstrings](<https://mkdocstrings.github.io/>).

### Code documentation

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#code-documentation>)

When contributing to Pydantic, please make sure that all code is well documented. The following should be documented using properly formatted docstrings:

  * Modules
  * Class definitions
  * Function definitions
  * Module-level variables

Pydantic uses [Google-style docstrings](<https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>) formatted according to [PEP 257](<https://www.python.org/dev/peps/pep-0257/>) guidelines. (See [Example Google Style Python Docstrings](<https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html>) for further examples.)

[pydocstyle](<https://www.pydocstyle.org/en/stable/index.html>) is used for linting docstrings. You can run `make format` to check your docstrings.

Where this is a conflict between Google-style docstrings and pydocstyle linting, follow the pydocstyle linting hints.

Class attributes and function arguments should be documented in the format “name: description.” When applicable, a return type should be documented with just a description. Types are inferred from the signature.
    
    class Foo:
        """A class docstring.
    
        Attributes:
            bar: A description of bar. Defaults to "bar".
        """
    
        bar: str = 'bar'
    
    def bar(self, baz: int) -> str:
        """A function docstring.
    
        Args:
            baz: A description of `baz`.
    
        Returns:
            A description of the return value.
        """
    
        return 'bar'
    
You may include example code in docstrings. This code should be complete, self-contained, and runnable. Docstring examples are tested, so make sure they are correct and complete. See [`BeforeValidator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.AfterValidator>) for an example.

### Documentation Style

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#documentation-style-1>)

In general, documentation should be written in a friendly, approachable style. It should be easy to read and understand, and should be as concise as possible while still being complete.

Code examples are encouraged, but should be kept short and simple. However, every code example should be complete, self-contained, and runnable. (If you’re not sure how to do this, ask for help!) We prefer print output to naked asserts, but if you’re testing something that doesn’t have a useful print output, asserts are fine.

Pydantic’s unit test will test all code examples in the documentation, so it’s important that they are correct and complete. When adding a new code example, use the following to test examples and update their formatting and output:

Terminal
    
    # Run tests and update code examples
    pytest tests/test_docs.py --update-examples
    
## Debugging Python and Rust

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#debugging-python-and-rust>)

If you’re working with `pydantic` and `pydantic-core`, you might find it helpful to debug Python and Rust code together. Here’s a quick guide on how to do that. This tutorial is done in VSCode, but you can use similar steps in other IDEs.

## Badges

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#badges>)

[![Pydantic v1](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json)](<https://pydantic.dev>) [![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](<https://pydantic.dev>)

Pydantic has a badge that you can use to show that your project uses Pydantic. You can use this badge in your `README.md`:

### With Markdown

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#with-markdown>)
    
    [![Pydantic v1](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json)](https://pydantic.dev)
    
    [![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)
    
### With reStructuredText

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#with-restructuredtext>)
    
    .. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json
        :target: https://pydantic.dev
        :alt: Pydantic
    
    .. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json
        :target: https://pydantic.dev
        :alt: Pydantic
    
### With HTML

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#with-html>)
    
    <a href="https://pydantic.dev"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json" alt="Pydantic Version 1" style="max-width:100%;"></a>
    
    <a href="https://pydantic.dev"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json" alt="Pydantic Version 2" style="max-width:100%;"></a>
    
## Adding your library as part of Pydantic’s third party test suite

[](<https://pydantic.dev/docs/validation/latest/get-started/contributing/#adding-your-library-as-part-of-pydantics-third-party-test-suite>)

To be able to identify regressions early during development, Pydantic runs tests on various third-party projects using Pydantic. We consider adding support for testing new open source projects (that rely heavily on Pydantic) if your said project matches some of the following criteria:

  * The project is actively maintained.
  * The project makes use of Pydantic internals (e.g. relying on the [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>) metaclass, typing utilities).
  * The project is popular enough (although small projects can still be included depending on how Pydantic is being used).
  * The project CI is simple enough to be ported into Pydantic’s testing workflow.

If your project meets some of these criteria, you can [open feature request](<https://github.com/pydantic/pydantic/issues/new?assignees=&labels=feature+request&projects=&template=feature_request.yml>) to discuss the inclusion of your project.

Was this page helpful?

Thanks for your feedback!