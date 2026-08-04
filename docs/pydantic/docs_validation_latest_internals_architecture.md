# Architecture | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/internals/architecture/](https://pydantic.dev/docs/validation/latest/internals/architecture/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/internals/architecture/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Architecture

Starting with Pydantic V2, part of the codebase is written in Rust in a separate package called `pydantic-core`. This was done partly in order to improve validation and serialization performance (with the cost of limited customization and extendibility of the internal logic).

This architecture documentation will first cover how the two `pydantic` and `pydantic-core` packages interact together, then will go through the architecture specifics for various patterns (model definition, validation, serialization, JSON Schema).

Usage of the Pydantic library can be divided into two parts:

  * Model definition, done in the `pydantic` package.
  * Model validation and serialization, done in the `pydantic-core` package.

## Model definition

[](<https://pydantic.dev/docs/validation/latest/internals/architecture/#model-definition>)

Whenever a Pydantic [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>) is defined, the metaclass will analyze the body of the model to collect a number of elements:

  * Defined annotations to build model fields (collected in the [`model_fields`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_fields>) attribute).
  * Model configuration, set with [`model_config`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_config>).
  * Additional validators/serializers.
  * Private attributes, class variables, identification of generic parametrization, etc.

### Communicating between `pydantic` and `pydantic-core`: the core schema

[](<https://pydantic.dev/docs/validation/latest/internals/architecture/#communicating-between-pydantic-and-pydantic-core-the-core-schema>)

We then need a way to communicate the collected information from the model definition to `pydantic-core`, so that validation and serialization is performed accordingly. To do so, Pydantic uses the concept of a core schema: a structured (and serializable) Python dictionary (represented using [`TypedDict`](<https://docs.python.org/3/library/typing.html#typing.TypedDict>) definitions) describing a specific validation and serialization logic. It is the core data structure used to communicate between the `pydantic` and `pydantic-core` packages. Every core schema has a required `type` key, and extra properties depending on this `type`.

The generation of a core schema is handled in a single place, by the `GenerateSchema` class (no matter if it is for a Pydantic model or anything else).

In the case of a Pydantic model, a core schema will be constructed and set as the [`__pydantic_core_schema__`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_core_schema__>) attribute.

To illustrate what a core schema looks like, we will take the example of the [`bool`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema>) core schema:
    
    class BoolSchema(TypedDict, total=False):
        type: Required[Literal['bool']]
        strict: bool
        ref: str
        metadata: Any
        serialization: SerSchema
    
When defining a Pydantic model with a boolean field:
    
    from pydantic import BaseModel, Field
    
    class Model(BaseModel):
        foo: bool = Field(strict=True)
    
The core schema for the `foo` field will look like:
    
    {
        'type': 'bool',
        'strict': True,
    }
    
As seen in the [`BoolSchema`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema>) definition, the serialization logic is also defined in the core schema. If we were to define a custom serialization function for `foo` , the `serialization` key would look like:

For example using the [`field_serializer`](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer>) decorator:
    
    class Model(BaseModel):
    foo: bool = Field(strict=True)
    
    @field_serializer('foo', mode='plain')
    def serialize_foo(self, value: bool) -> Any:
    ...
    
    {
        'type': 'function-plain',
        'function': <function Model.serialize_foo at 0x111>,
        'is_field_serializer': True,
        'info_arg': False,
        'return_schema': {'type': 'int'},
    }
    
Note that this is also a core schema definition, just that it is only relevant for `pydantic-core` during serialization.

Core schemas cover a broad scope, and are used whenever we want to communicate between the Python and Rust side. While the previous examples were related to validation and serialization, it could in theory be used for anything: error management, extra metadata, etc.

### JSON Schema generation

[](<https://pydantic.dev/docs/validation/latest/internals/architecture/#json-schema-generation>)

You may have noticed that the previous serialization core schema has a `return_schema` key. This is because the core schema is also used to generate the corresponding JSON Schema.

Similar to how the core schema is generated, the JSON Schema generation is handled by the [`GenerateJsonSchema`](<https://pydantic.dev/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema>) class. The [`generate`](<https://pydantic.dev/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema.generate>) method is the main entry point and is given the core schema of that model.

Coming back to our `bool` field example, the [`bool_schema`](<https://pydantic.dev/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema.bool_schema>) method will be given the previously generated [boolean core schema](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema>) and will return the following JSON Schema:
    
    {
        {"type": "boolean"}
    }
    
### Customizing the core schema and JSON schema

[](<https://pydantic.dev/docs/validation/latest/internals/architecture/#customizing-the-core-schema-and-json-schema>)

While the `GenerateSchema` and [`GenerateJsonSchema`](<https://pydantic.dev/docs/validation/latest/api/pydantic/json_schema/#pydantic.json_schema.GenerateJsonSchema>) classes handle the creation of the corresponding schemas, Pydantic offers a way to customize them in some cases, following a wrapper pattern. This customization is done through the `__get_pydantic_core_schema__` and `__get_pydantic_json_schema__` methods.

To understand this wrapper pattern, we will take the example of metadata classes used with [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>), where the `__get_pydantic_core_schema__` method can be used:
    
    from typing import Annotated, Any
    
    from pydantic_core import CoreSchema
    
    from pydantic import GetCoreSchemaHandler, TypeAdapter
    
    class MyStrict:
      @classmethod
      def __get_pydantic_core_schema__(
          cls, source: Any, handler: GetCoreSchemaHandler
      ) -> CoreSchema:
          schema = handler(source)  # (1)
          schema['strict'] = True
          return schema
    
    class MyGt:
      @classmethod
      def __get_pydantic_core_schema__(
          cls, source: Any, handler: GetCoreSchemaHandler
      ) -> CoreSchema:
          schema = handler(source)  # (2)
          schema['gt'] = 1
          return schema
    
    ta = TypeAdapter(Annotated[int, MyStrict(), MyGt()])

`MyStrict` is the first annotation to be applied. At this point, `schema = {'type': 'int'}`.

`MyGt` is the last annotation to be applied. At this point, `schema = {'type': 'int', 'strict': True}`.

When the `GenerateSchema` class builds the core schema for `Annotated[int, MyStrict(), MyGt()]`, it will create an instance of a `GetCoreSchemaHandler` to be passed to the `MyGt.__get_pydantic_core_schema__` method. 

In the case of our [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>) pattern, the `GetCoreSchemaHandler` is defined in a nested way. Calling it will recursively call the other `__get_pydantic_core_schema__` methods until it reaches the `int` annotation, where a simple `{'type': 'int'}` schema is returned.

The `source` argument depends on the core schema generation pattern. In the case of [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>), the `source` will be the type being annotated. When [defining a custom type](<https://pydantic.dev/docs/validation/latest/concepts/types#as-a-method-on-a-custom-type>), the `source` will be the actual class where `__get_pydantic_core_schema__` is defined.

## Model validation and serialization

[](<https://pydantic.dev/docs/validation/latest/internals/architecture/#model-validation-and-serialization>)

While model definition was scoped to the _class_ level (i.e. when defining your model), model validation and serialization happens at the _instance_ level. Both these concepts are handled in `pydantic-core` (providing a 5 to 20 performance increase compared to Pydantic V1), by using the previously built core schema.

`pydantic-core` exposes a [`SchemaValidator`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator>) and [`SchemaSerializer`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer>) class to perform these tasks:
    
    from pydantic import BaseModel
    
    class Model(BaseModel):
      foo: int
    
    model = Model.model_validate({'foo': 1})  # (1)
    dumped = model.model_dump()  # (2)

The provided data is sent to `pydantic-core` by using the [`SchemaValidator.validate_python`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python>) method. `pydantic-core` will validate (following the core schema of the model) the data and populate the model's `__dict__` attribute.

The `model` instance is sent to `pydantic-core` by using the [`SchemaSerializer.to_python`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python>) method. `pydantic-core` will read the instance's `__dict__` attribute and built the appropriate result (again, following the core schema of the model).

Was this page helpful?

Thanks for your feedback!