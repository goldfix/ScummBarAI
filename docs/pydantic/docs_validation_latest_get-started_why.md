# Why use Pydantic | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/get-started/why/](https://pydantic.dev/docs/validation/latest/get-started/why/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/get-started/why/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Why use Pydantic

Today, Pydantic is downloaded many times a month and used by some of the largest and most recognisable organisations in the world.

It’s hard to know why so many people have adopted Pydantic since its inception six years ago, but here are a few guesses.

## Type hints powering schema validation 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#type-hints>)

The schema that Pydantic validates against is generally defined by Python [type hints](<https://docs.python.org/3/glossary.html#term-type-hint>).

Type hints are great for this since, if you’re writing modern Python, you already know how to use them. Using type hints also means that Pydantic integrates well with static typing tools (like [mypy](<https://www.mypy-lang.org/>) and [Pyright](<https://github.com/microsoft/pyright/>)) and IDEs (like [PyCharm](<https://www.jetbrains.com/pycharm/>) and [VSCode](<https://code.visualstudio.com/>)).

Example - just type hints
    
    from typing import Annotated, Literal
    
    from annotated_types import Gt
    
    from pydantic import BaseModel
    
    class Fruit(BaseModel):
      name: str  # (1)
      color: Literal['red', 'green']  # (2)
      weight: Annotated[float, Gt(0)]  # (3)
      bazam: dict[str, list[tuple[int, bool, float]]]  # (4)
    
    print(
      Fruit(
          name='Apple',
          color='red',
          weight=4.2,
          bazam={'foobar': [(1, True, 0.1)]},
      )
    )
    #> name='Apple' color='red' weight=4.2 bazam={'foobar': [(1, True, 0.1)]}

The `name` field is simply annotated with `str` — any string is allowed.

The [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>) type is used to enforce that `color` is either `'red'` or `'green'`.

Even when we want to apply constraints not encapsulated in Python types, we can use [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>) and [`annotated-types`](<https://github.com/annotated-types/annotated-types>) to enforce constraints while still keeping typing support.

I'm not claiming "bazam" is really an attribute of fruit, but rather to show that arbitrarily complex types can easily be validated.

## Performance

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#performance>)

Pydantic’s core validation logic is implemented in a separate package ([`pydantic-core`](<https://pypi.org/project/pydantic-core>)), where validation for most types is implemented in Rust.

As a result, Pydantic is among the fastest data validation libraries for Python.

Performance Example - Pydantic vs. dedicated code

In general, dedicated code should be much faster than a general-purpose validator, but in this example Pydantic is >300% faster than dedicated code when parsing JSON and validating URLs.

Performance Example
    
    import json
    import timeit
    from urllib.parse import urlparse
    
    import requests
    
    from pydantic import HttpUrl, TypeAdapter
    
    reps = 7
    number = 100
    r = requests.get('https://api.github.com/emojis')
    r.raise_for_status()
    emojis_json = r.content
    
    def emojis_pure_python(raw_data):
        data = json.loads(raw_data)
        output = {}
        for key, value in data.items():
            assert isinstance(key, str)
            url = urlparse(value)
            assert url.scheme in ('https', 'http')
            output[key] = url
    
    emojis_pure_python_times = timeit.repeat(
        'emojis_pure_python(emojis_json)',
        globals={
            'emojis_pure_python': emojis_pure_python,
            'emojis_json': emojis_json,
        },
        repeat=reps,
        number=number,
    )
    print(f'pure python: {min(emojis_pure_python_times) / number * 1000:0.2f}ms')
    #> pure python: 5.32ms
    
    type_adapter = TypeAdapter(dict[str, HttpUrl])
    emojis_pydantic_times = timeit.repeat(
        'type_adapter.validate_json(emojis_json)',
        globals={
            'type_adapter': type_adapter,
            'HttpUrl': HttpUrl,
            'emojis_json': emojis_json,
        },
        repeat=reps,
        number=number,
    )
    print(f'pydantic: {min(emojis_pydantic_times) / number * 1000:0.2f}ms')
    #> pydantic: 1.54ms
    
    print(
        f'Pydantic {min(emojis_pure_python_times) / min(emojis_pydantic_times):0.2f}x faster'
    )
    #> Pydantic 3.45x faster
    
Unlike other performance-centric libraries written in compiled languages, Pydantic also has excellent support for customizing validation via [functional validators](<https://pydantic.dev/docs/validation/latest/get-started/why/#customisation>).

## Serialization

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#serialization>)

Pydantic provides functionality to serialize model in three ways:

  1. To a Python `dict` made up of the associated Python objects.
  2. To a Python `dict` made up only of “jsonable” types.
  3. To a JSON string.

In all three modes, the output can be customized by excluding specific fields, excluding unset fields, excluding default values, and excluding `None` values.

Example - Serialization 3 ways
    
    from datetime import datetime
    
    from pydantic import BaseModel
    
    class Meeting(BaseModel):
        when: datetime
        where: bytes
        why: str = 'No idea'
    
    m = Meeting(when='2020-01-01T12:00', where='home')
    print(m.model_dump(exclude_unset=True))
    #> {'when': datetime.datetime(2020, 1, 1, 12, 0), 'where': b'home'}
    print(m.model_dump(exclude={'where'}, mode='json'))
    #> {'when': '2020-01-01T12:00:00', 'why': 'No idea'}
    print(m.model_dump_json(exclude_defaults=True))
    #> {"when":"2020-01-01T12:00:00","where":"home"}
    
## JSON Schema

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#json-schema>)

A [JSON Schema](<https://json-schema.org/>) can be generated for any Pydantic schema — allowing self-documenting APIs and integration with a wide variety of tools which support the JSON Schema format.

Example - JSON Schema
    
    from datetime import datetime
    
    from pydantic import BaseModel
    
    class Address(BaseModel):
        street: str
        city: str
        zipcode: str
    
    class Meeting(BaseModel):
        when: datetime
        where: Address
        why: str = 'No idea'
    
    print(Meeting.model_json_schema())
    """
    {
        '$defs': {
            'Address': {
                'properties': {
                    'street': {'title': 'Street', 'type': 'string'},
                    'city': {'title': 'City', 'type': 'string'},
                    'zipcode': {'title': 'Zipcode', 'type': 'string'},
                },
                'required': ['street', 'city', 'zipcode'],
                'title': 'Address',
                'type': 'object',
            }
        },
        'properties': {
            'when': {'format': 'date-time', 'title': 'When', 'type': 'string'},
            'where': {'$ref': '#/$defs/Address'},
            'why': {'default': 'No idea', 'title': 'Why', 'type': 'string'},
        },
        'required': ['when', 'where'],
        'title': 'Meeting',
        'type': 'object',
    }
    """
    
Pydantic is compliant with the latest version of JSON Schema specification ([2020-12](<https://json-schema.org/draft/2020-12/release-notes.html>)), which is compatible with [OpenAPI 3.1](<https://spec.openapis.org/oas/v3.1.0.html>).

## Strict mode and data coercion 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#strict-lax>)

By default, Pydantic is tolerant to common incorrect types and coerces data to the right type — e.g. a numeric string passed to an `int` field will be parsed as an `int`.

Pydantic also has as [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), where types are not coerced and a validation error is raised unless the input data exactly matches the expected schema.

But strict mode would be pretty useless when validating JSON data since JSON doesn’t have types matching many common Python types like [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>), [`UUID`](<https://docs.python.org/3/library/uuid.html#uuid.UUID>) or [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>).

To solve this, Pydantic can parse and validate JSON in one step. This allows sensible data conversion (e.g. when parsing strings into [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) objects). Since the JSON parsing is implemented in Rust, it’s also very performant.

Example - Strict mode that's actually useful
    
    from datetime import datetime
    
    from pydantic import BaseModel, ValidationError
    
    class Meeting(BaseModel):
        when: datetime
        where: bytes
    
    m = Meeting.model_validate({'when': '2020-01-01T12:00', 'where': 'home'})
    print(m)
    #> when=datetime.datetime(2020, 1, 1, 12, 0) where=b'home'
    try:
        m = Meeting.model_validate(
            {'when': '2020-01-01T12:00', 'where': 'home'}, strict=True
        )
    except ValidationError as e:
        print(e)
        """
        2 validation errors for Meeting
        when
          Input should be a valid datetime [type=datetime_type, input_value='2020-01-01T12:00', input_type=str]
        where
          Input should be a valid bytes [type=bytes_type, input_value='home', input_type=str]
        """
    
    m_json = Meeting.model_validate_json(
        '{"when": "2020-01-01T12:00", "where": "home"}'
    )
    print(m_json)
    #> when=datetime.datetime(2020, 1, 1, 12, 0) where=b'home'
    
## Dataclasses, TypedDicts, and more 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#dataclasses-typeddict-more>)

Pydantic provides four ways to create schemas and perform validation and serialization:

  1. [`BaseModel`](<https://pydantic.dev/docs/validation/latest/concepts/models>) — Pydantic’s own super class with many common utilities available via instance methods.
  2. [Pydantic dataclasses](<https://pydantic.dev/docs/validation/latest/concepts/dataclasses>) — a wrapper around standard dataclasses with additional validation performed.
  3. [`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) — a general way to adapt any type for validation and serialization. This allows types like [`TypedDict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types#typeddict>) and [`NamedTuple`](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types#named-tuples>) to be validated as well as simple types (like [`int`](<https://docs.python.org/3/library/functions.html#int>) or [`timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>)) — [all types](<https://pydantic.dev/docs/validation/latest/concepts/types>) supported can be used with [`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>).
  4. [`validate_call`](<https://pydantic.dev/docs/validation/latest/concepts/validation_decorator>) — a decorator to perform validation when calling a function.

Example - schema based on a `TypedDict`
    
    from datetime import datetime
    
    from typing_extensions import NotRequired, TypedDict
    
    from pydantic import TypeAdapter
    
    class Meeting(TypedDict):
      when: datetime
      where: bytes
      why: NotRequired[str]
    
    meeting_adapter = TypeAdapter(Meeting)
    m = meeting_adapter.validate_python(  # (1)
      {'when': '2020-01-01T12:00', 'where': 'home'}
    )
    print(m)
    #> {'when': datetime.datetime(2020, 1, 1, 12, 0), 'where': b'home'}
    meeting_adapter.dump_python(m, exclude={'where'})  # (2)
    
    print(meeting_adapter.json_schema())  # (3)
    """
    {
      'properties': {
          'when': {'format': 'date-time', 'title': 'When', 'type': 'string'},
          'where': {'format': 'binary', 'title': 'Where', 'type': 'string'},
          'why': {'title': 'Why', 'type': 'string'},
      },
      'required': ['when', 'where'],
      'title': 'Meeting',
      'type': 'object',
    }
    """

[`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) for a [`TypedDict`](<https://docs.python.org/3/library/typing.html#typing.TypedDict>) performing validation, it can also validate JSON data directly with [`validate_json`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json>).

[`dump_python`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python>) to serialise a [`TypedDict`](<https://docs.python.org/3/library/typing.html#typing.TypedDict>) to a python object, it can also serialise to JSON with [`dump_json`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json>).

[`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) can also generate a JSON Schema.

## Customisation

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#customisation>)

Functional validators and serializers, as well as a powerful protocol for custom types, means the way Pydantic operates can be customized on a per-field or per-type basis.

Customisation Example - wrap validators

“wrap validators” are new in Pydantic V2 and are one of the most powerful ways to customize validation.
    
    from datetime import datetime, timezone
    from typing import Any
    
    from pydantic_core.core_schema import ValidatorFunctionWrapHandler
    
    from pydantic import BaseModel, field_validator
    
    class Meeting(BaseModel):
        when: datetime
    
        @field_validator('when', mode='wrap')
        def when_now(
            cls, input_value: Any, handler: ValidatorFunctionWrapHandler
        ) -> datetime:
            if input_value == 'now':
                return datetime.now()
            when = handler(input_value)
            # in this specific application we know tz naive datetimes are in UTC
            if when.tzinfo is None:
                when = when.replace(tzinfo=timezone.utc)
            return when
    
    print(Meeting(when='2020-01-01T12:00+01:00'))
    #> when=datetime.datetime(2020, 1, 1, 12, 0, tzinfo=TzInfo(3600))
    print(Meeting(when='now'))
    #> when=datetime.datetime(2032, 1, 2, 3, 4, 5, 6)
    print(Meeting(when='2020-01-01T12:00'))
    #> when=datetime.datetime(2020, 1, 1, 12, 0, tzinfo=datetime.timezone.utc)
    
## Ecosystem

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#ecosystem>)

At the time of writing there are 466,400 repositories on GitHub and 8,119 packages on PyPI that depend on Pydantic.

Some notable libraries that depend on Pydantic:

  * [`huggingface/transformers`](<https://github.com/huggingface/transformers>) 138,570 stars
  * [`hwchase17/langchain`](<https://github.com/hwchase17/langchain>) 99,542 stars
  * [`tiangolo/fastapi`](<https://github.com/tiangolo/fastapi>) 80,497 stars
  * [`apache/airflow`](<https://github.com/apache/airflow>) 38,577 stars
  * [`lm-sys/FastChat`](<https://github.com/lm-sys/FastChat>) 37,650 stars
  * [`microsoft/DeepSpeed`](<https://github.com/microsoft/DeepSpeed>) 36,521 stars
  * [`OpenBB-finance/OpenBBTerminal`](<https://github.com/OpenBB-finance/OpenBBTerminal>) 35,971 stars
  * [`gradio-app/gradio`](<https://github.com/gradio-app/gradio>) 35,740 stars
  * [`ray-project/ray`](<https://github.com/ray-project/ray>) 35,176 stars
  * [`pola-rs/polars`](<https://github.com/pola-rs/polars>) 31,698 stars
  * [`Lightning-AI/lightning`](<https://github.com/Lightning-AI/lightning>) 28,902 stars
  * [`mindsdb/mindsdb`](<https://github.com/mindsdb/mindsdb>) 27,141 stars
  * [`embedchain/embedchain`](<https://github.com/embedchain/embedchain>) 24,379 stars
  * [`pynecone-io/reflex`](<https://github.com/pynecone-io/reflex>) 21,558 stars
  * [`heartexlabs/label-studio`](<https://github.com/heartexlabs/label-studio>) 20,571 stars
  * [`Sanster/lama-cleaner`](<https://github.com/Sanster/lama-cleaner>) 20,313 stars
  * [`mlflow/mlflow`](<https://github.com/mlflow/mlflow>) 19,393 stars
  * [`RasaHQ/rasa`](<https://github.com/RasaHQ/rasa>) 19,337 stars
  * [`spotDL/spotify-downloader`](<https://github.com/spotDL/spotify-downloader>) 18,604 stars
  * [`chroma-core/chroma`](<https://github.com/chroma-core/chroma>) 17,393 stars
  * [`airbytehq/airbyte`](<https://github.com/airbytehq/airbyte>) 17,120 stars
  * [`openai/evals`](<https://github.com/openai/evals>) 15,437 stars
  * [`tiangolo/sqlmodel`](<https://github.com/tiangolo/sqlmodel>) 15,127 stars
  * [`ydataai/ydata-profiling`](<https://github.com/ydataai/ydata-profiling>) 12,687 stars
  * [`pyodide/pyodide`](<https://github.com/pyodide/pyodide>) 12,653 stars
  * [`dagster-io/dagster`](<https://github.com/dagster-io/dagster>) 12,440 stars
  * [`PaddlePaddle/PaddleNLP`](<https://github.com/PaddlePaddle/PaddleNLP>) 12,312 stars
  * [`matrix-org/synapse`](<https://github.com/matrix-org/synapse>) 11,857 stars
  * [`lucidrains/DALLE2-pytorch`](<https://github.com/lucidrains/DALLE2-pytorch>) 11,207 stars
  * [`great-expectations/great_expectations`](<https://github.com/great-expectations/great_expectations>) 10,164 stars
  * [`modin-project/modin`](<https://github.com/modin-project/modin>) 10,002 stars
  * [`aws/serverless-application-model`](<https://github.com/aws/serverless-application-model>) 9,402 stars
  * [`sqlfluff/sqlfluff`](<https://github.com/sqlfluff/sqlfluff>) 8,535 stars
  * [`replicate/cog`](<https://github.com/replicate/cog>) 8,344 stars
  * [`autogluon/autogluon`](<https://github.com/autogluon/autogluon>) 8,326 stars
  * [`lucidrains/imagen-pytorch`](<https://github.com/lucidrains/imagen-pytorch>) 8,164 stars
  * [`brycedrennan/imaginAIry`](<https://github.com/brycedrennan/imaginAIry>) 8,050 stars
  * [`vitalik/django-ninja`](<https://github.com/vitalik/django-ninja>) 7,685 stars
  * [`NVlabs/SPADE`](<https://github.com/NVlabs/SPADE>) 7,632 stars
  * [`bridgecrewio/checkov`](<https://github.com/bridgecrewio/checkov>) 7,340 stars
  * [`bentoml/BentoML`](<https://github.com/bentoml/BentoML>) 7,322 stars
  * [`skypilot-org/skypilot`](<https://github.com/skypilot-org/skypilot>) 7,113 stars
  * [`apache/iceberg`](<https://github.com/apache/iceberg>) 6,853 stars
  * [`deeppavlov/DeepPavlov`](<https://github.com/deeppavlov/DeepPavlov>) 6,777 stars
  * [`PrefectHQ/marvin`](<https://github.com/PrefectHQ/marvin>) 5,454 stars
  * [`NVIDIA/NeMo-Guardrails`](<https://github.com/NVIDIA/NeMo-Guardrails>) 4,383 stars
  * [`microsoft/FLAML`](<https://github.com/microsoft/FLAML>) 4,035 stars
  * [`jina-ai/discoart`](<https://github.com/jina-ai/discoart>) 3,846 stars
  * [`docarray/docarray`](<https://github.com/docarray/docarray>) 3,007 stars
  * [`aws-powertools/powertools-lambda-python`](<https://github.com/aws-powertools/powertools-lambda-python>) 2,980 stars
  * [`roman-right/beanie`](<https://github.com/roman-right/beanie>) 2,172 stars
  * [`art049/odmantic`](<https://github.com/art049/odmantic>) 1,096 stars

More libraries using Pydantic can be found at [`Kludex/awesome-pydantic`](<https://github.com/Kludex/awesome-pydantic>).

## Organisations using Pydantic 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#using-pydantic>)

Some notable companies and organisations using Pydantic together with comments on why/how we know they’re using Pydantic.

The organisations below are included because they match one or more of the following criteria:

  * Using Pydantic as a dependency in a public repository.
  * Referring traffic to the Pydantic documentation site from an organization-internal domain — specific referrers are not included since they’re generally not in the public domain.
  * Direct communication between the Pydantic team and engineers employed by the organization about usage of Pydantic within the organization.

We’ve included some extra detail where appropriate and already in the public domain.

### Adobe 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-adobe>)

[`adobe/dy-sql`](<https://github.com/adobe/dy-sql>) uses Pydantic.

### Amazon and AWS 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-amazon>)

  * [powertools-lambda-python](<https://github.com/aws-powertools/powertools-lambda-python>)
  * [awslabs/gluonts](<https://github.com/awslabs/gluonts>)
  * AWS [sponsored Samuel Colvin $5,000](<https://twitter.com/samuel_colvin/status/1549383169006239745>) to work on Pydantic in 2022

### Anthropic 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-anthropic>)

[`anthropics/anthropic-sdk-python`](<https://github.com/anthropics/anthropic-sdk-python>) uses Pydantic.

### Apple 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-apple>)

_(Based on the criteria described above)_

### ASML 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-asml>)

_(Based on the criteria described above)_

### AstraZeneca 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-astrazeneca>)

[Multiple repos](<https://github.com/search?q=org%3AAstraZeneca+pydantic&type=code>) in the `AstraZeneca` GitHub org depend on Pydantic.

### Cisco Systems 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-cisco>)

  * Pydantic is listed in their report of [Open Source Used In RADKit](<https://www.cisco.com/c/dam/en_us/about/doing_business/open_source/docs/RADKit-149-1687424532.pdf>).
  * [`cisco/webex-assistant-sdk`](<https://github.com/cisco/webex-assistant-sdk>)

### Capital One 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-capital_one>)

_(Based on the criteria described above)_

### Comcast 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-comcast>)

_(Based on the criteria described above)_

### Datadog 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-datadog>)

  * Extensive use of Pydantic in [`DataDog/integrations-core`](<https://github.com/DataDog/integrations-core>) and other repos
  * Communication with engineers from Datadog about how they use Pydantic.

### Facebook 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-facebook>)

[Multiple repos](<https://github.com/search?q=org%3Afacebookresearch+pydantic&type=code>) in the `facebookresearch` GitHub org depend on Pydantic.

### GitHub 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-github>)

GitHub sponsored Pydantic $750 in 2022

### Google 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-google>)

Extensive use of Pydantic in [`google/turbinia`](<https://github.com/google/turbinia>) and other repos.

### HSBC 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-hsbc>)

_(Based on the criteria described above)_

### IBM 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-ibm>)

[Multiple repos](<https://github.com/search?q=org%3AIBM+pydantic&type=code>) in the `IBM` GitHub org depend on Pydantic.

### Intel 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-intel>)

_(Based on the criteria described above)_

### Intuit 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-intuit>)

_(Based on the criteria described above)_

### Intergovernmental Panel on Climate Change 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-ipcc>)

[Tweet](<https://twitter.com/daniel_huppmann/status/1563461797973110785>) explaining how the IPCC use Pydantic.

### JPMorgan 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-jpmorgan>)

_(Based on the criteria described above)_

### Jupyter 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-jupyter>)

  * The developers of the Jupyter notebook are using Pydantic [for subprojects](<https://github.com/pydantic/pydantic/issues/773>)
  * Through the FastAPI-based Jupyter server [Jupyverse](<https://github.com/jupyter-server/jupyverse>)
  * [FPS](<https://github.com/jupyter-server/fps>)’s configuration management.

### Microsoft 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-microsoft>)

  * [DeepSpeed](<https://github.com/microsoft/DeepSpeed>) deep learning optimisation library uses Pydantic extensively
  * [Multiple repos](<https://github.com/search?q=org%3Amicrosoft%20pydantic&type=code>) in the `microsoft` GitHub org depend on Pydantic, in particular their
  * Pydantic is also [used](<https://github.com/search?q=org%3AAzure%20pydantic&type=code>) in the `Azure` GitHub org
  * [Comments](<https://github.com/tiangolo/fastapi/pull/26>) on GitHub show Microsoft engineers using Pydantic as part of Windows and Office

### Molecular Science Software Institute 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-molssi>)

[Multiple repos](<https://github.com/search?q=org%3AMolSSI%20pydantic&type=code>) in the `MolSSI` GitHub org depend on Pydantic.

### NASA 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-nasa>)

[Multiple repos](<https://github.com/search?q=org%3Anasa%20pydantic&type=code>) in the `NASA` GitHub org depend on Pydantic.

NASA are also using Pydantic via FastAPI in their JWST project to process images from the James Webb Space Telescope, see [this tweet](<https://twitter.com/benjamin_falk/status/1546947039363305472>).

### Netflix 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-netflix>)

[Multiple repos](<https://github.com/search?q=org%3Anetflix%20pydantic&type=code>) in the `Netflix` GitHub org depend on Pydantic.

### NSA 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-nsa>)

The [`nsacyber/WALKOFF`](<https://github.com/nsacyber/WALKOFF>) repo depends on Pydantic.

### NVIDIA 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-nvidia>)

[Multiple repositories](<https://github.com/search?q=org%3ANVIDIA%20pydantic&type=code>) in the `NVIDIA` GitHub org depend on Pydantic.

Their “Omniverse Services” depends on Pydantic according to [their documentation](<https://web.archive.org/web/20220628161919/https://docs.omniverse.nvidia.com/prod_services/prod_services/core/index.html>).

### OpenAI 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-openai>)

OpenAI use Pydantic for their ChatCompletions API, as per [this](<https://github.com/pydantic/pydantic/discussions/6372>) discussion on GitHub.

Anecdotally, OpenAI use Pydantic extensively for their internal services.

### Oracle 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-oracle>)

_(Based on the criteria described above)_

### Palantir 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-palantir>)

_(Based on the criteria described above)_

### Qualcomm 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-qualcomm>)

_(Based on the criteria described above)_

### Red Hat 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-redhat>)

_(Based on the criteria described above)_

### Revolut 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-revolut>)

Anecdotally, all internal services at Revolut are built with FastAPI and therefore Pydantic.

### Robusta 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-robusta>)

The [`robusta-dev/robusta`](<https://github.com/robusta-dev/robusta>) repo depends on Pydantic.

### Salesforce 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-salesforce>)

Salesforce [sponsored Samuel Colvin $10,000](<https://twitter.com/samuel_colvin/status/1501288247670063104>) to work on Pydantic in 2022.

### Starbucks 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-starbucks>)

_(Based on the criteria described above)_

### Texas Instruments 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-ti>)

_(Based on the criteria described above)_

### Twilio 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-twilio>)

_(Based on the criteria described above)_

### Twitter 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-twitter>)

Twitter’s [`the-algorithm`](<https://github.com/twitter/the-algorithm>) repo where they [open sourced](<https://blog.twitter.com/engineering/en_us/topics/open-source/2023/twitter-recommendation-algorithm>) their recommendation engine uses Pydantic.

### UK Home Office 

[](<https://pydantic.dev/docs/validation/latest/get-started/why/#org-ukhomeoffice>)

_(Based on the criteria described above)_

Was this page helpful?

Thanks for your feedback!