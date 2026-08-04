# pydantic_core | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/](https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# pydantic_core

## SchemaValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator>)

`SchemaValidator` is the Python wrapper for `pydantic-core`’s Rust validation logic, internally it owns one `CombinedValidator` which may in turn own more `CombinedValidator`s which make up the full schema validator.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes>)

#### title 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.title>)

The title of the schema, as used in the heading of [`ValidationError.__str__()`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError>).

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#methods>)

#### validate_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python>)
    
    def validate_python(
        input: Any,
        *,
        strict: bool | None = None,
        extra: ExtraBehavior | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        self_instance: Any | None = None,
        allow_partial: bool | Literal['off', 'on', 'trailing-strings'] = False,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Any
    
Validate a Python object against the schema and return the validated object.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The validated object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters>)

**`input`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(input\)>)

The Python object to validate.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(strict\)>)

Whether to validate the object in strict mode. If `None`, the value of [`CoreConfig.strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`extra`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. If `None`, the value of [`CoreConfig.extra_fields_behavior`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`from_attributes`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(from_attributes\)>)

Whether to validate objects as inputs to models by extracting attributes. If `None`, the value of [`CoreConfig.from_attributes`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(context\)>)

The context to use for validation, this is passed to functional validators as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.context>).

**`self_instance`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(self_instance\)>)

An instance of a model set attributes on from validation, this is used when running validation from the `__init__` method of a model.

**`allow_partial`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘off’, ‘on’, ‘trailing-strings’] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(allow_partial\)>)

Whether to allow partial validation; if `True` errors in the last element of sequences and mappings are ignored. `'trailing-strings'` means any final unfinished JSON string is included in the result.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises>)

  * `ValidationError` — If validation fails.
  * `Exception` — Other error types maybe raised if internal errors occur.

#### isinstance_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.isinstance_python>)
    
    def isinstance_python(
        input: Any,
        *,
        strict: bool | None = None,
        extra: ExtraBehavior | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        self_instance: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> bool
    
Similar to [`validate_python()`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_python>) but returns a boolean.

Arguments match `validate_python()`. This method will not raise `ValidationError`s but will raise internal errors.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-1>)

[`bool`](<https://docs.python.org/3/library/functions.html#bool>) — `True` if validation succeeds, `False` if validation fails.

#### validate_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json>)
    
    def validate_json(
        input: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        extra: ExtraBehavior | None = None,
        context: Any | None = None,
        self_instance: Any | None = None,
        allow_partial: bool | Literal['off', 'on', 'trailing-strings'] = False,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Any
    
Validate JSON data directly against the schema and return the validated Python object.

This method should be significantly faster than `validate_python(json.loads(json_data))` as it avoids the need to create intermediate Python objects

It also handles constructing the correct Python type even in strict mode, where `validate_python(json.loads(json_data))` would fail validation.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-2>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The validated Python object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-1>)

**`input`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) | [`bytearray`](<https://docs.python.org/3/library/stdtypes.html#bytearray>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(input\)>)

The JSON data to validate.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(strict\)>)

Whether to validate the object in strict mode. If `None`, the value of [`CoreConfig.strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`extra`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. If `None`, the value of [`CoreConfig.extra_fields_behavior`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(context\)>)

The context to use for validation, this is passed to functional validators as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.context>).

**`self_instance`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(self_instance\)>)

An instance of a model set attributes on from validation.

**`allow_partial`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘off’, ‘on’, ‘trailing-strings’] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(allow_partial\)>)

Whether to allow partial validation; if `True` incomplete JSON will be parsed successfully and errors in the last element of sequences and mappings are ignored. `'trailing-strings'` means any final unfinished JSON string is included in the result.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_json\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-1>)

  * `ValidationError` — If validation fails or if the JSON data is invalid.
  * `Exception` — Other error types maybe raised if internal errors occur.

#### validate_strings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings>)
    
    def validate_strings(
        input: _StringInput,
        *,
        strict: bool | None = None,
        extra: ExtraBehavior | None = None,
        context: Any | None = None,
        allow_partial: bool | Literal['off', 'on', 'trailing-strings'] = False,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Any
    
Validate a string against the schema and return the validated Python object.

This is similar to `validate_json` but applies to scenarios where the input will be a string but not JSON data, e.g. URL fragments, query parameters, etc.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-3>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The validated Python object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-2>)

**`input`** : `_StringInput`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings\(input\)>)

The input as a string, or bytes/bytearray if `strict=False`.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings\(strict\)>)

Whether to validate the object in strict mode. If `None`, the value of [`CoreConfig.strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`extra`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. If `None`, the value of [`CoreConfig.extra_fields_behavior`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings\(context\)>)

The context to use for validation, this is passed to functional validators as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.context>).

**`allow_partial`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘off’, ‘on’, ‘trailing-strings’] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings\(allow_partial\)>)

Whether to allow partial validation; if `True` errors in the last element of sequences and mappings are ignored. `'trailing-strings'` means any final unfinished JSON string is included in the result.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_strings\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-2>)

  * `ValidationError` — If validation fails or if the JSON data is invalid.
  * `Exception` — Other error types maybe raised if internal errors occur.

#### validate_assignment 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment>)
    
    def validate_assignment(
        obj: Any,
        field_name: str,
        field_value: Any,
        *,
        strict: bool | None = None,
        extra: ExtraBehavior | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> dict[str, Any] | tuple[dict[str, Any], dict[str, Any] | None, set[str]]
    
Validate an assignment to a field on a model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-4>)

[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>), [`set`](<https://docs.python.org/3/reference/expressions.html#set>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]] — Either the model dict or a tuple of `(model_data, model_extra, fields_set)`

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-3>)

**`obj`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(obj\)>)

The model instance being assigned to.

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(field_name\)>)

The name of the field to validate assignment for.

**`field_value`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(field_value\)>)

The value to assign to the field.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(strict\)>)

Whether to validate the object in strict mode. If `None`, the value of [`CoreConfig.strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`extra`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. If `None`, the value of [`CoreConfig.extra_fields_behavior`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`from_attributes`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(from_attributes\)>)

Whether to validate objects as inputs to models by extracting attributes. If `None`, the value of [`CoreConfig.from_attributes`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(context\)>)

The context to use for validation, this is passed to functional validators as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.context>).

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.validate_assignment\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-3>)

  * `ValidationError` — If validation fails.
  * `Exception` — Other error types maybe raised if internal errors occur.

#### get_default_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.get_default_value>)
    
    def get_default_value(*, strict: bool | None = None, context: Any = None) -> Some | None
    
Get the default value for the schema, including running default value validation.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-5>)

`Some` | [`None`](<https://docs.python.org/3/library/constants.html#None>) — `None` if the schema has no default value, otherwise a [`Some`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.Some>) containing the default.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-4>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.get_default_value\(strict\)>)

Whether to validate the default value in strict mode. If `None`, the value of [`CoreConfig.strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>) is used.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator.get_default_value\(context\)>)

The context to use for validation, this is passed to functional validators as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.context>).

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-4>)

  * `ValidationError` — If validation fails.
  * `Exception` — Other error types maybe raised if internal errors occur.

## SchemaSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer>)

`SchemaSerializer` is the Python wrapper for `pydantic-core`’s Rust serialization logic, internally it owns one `CombinedSerializer` which may in turn own more `CombinedSerializer`s which make up the full schema serializer.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#methods-1>)

#### to_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python>)
    
    def to_python(
        value: Any,
        *,
        mode: str | None = None,
        include: _IncEx | None = None,
        exclude: _IncEx | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal['none', 'warn', 'error'] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
        polymorphic_serialization: bool | None = None,
        context: Any | None = None,
    ) -> Any
    
Serialize/marshal a Python object to a Python object including transforming and filtering data.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-6>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The serialized Python object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-5>)

**`value`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(value\)>)

The Python object to serialize.

**`mode`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(mode\)>)

The serialization mode to use, either `'python'` or `'json'`, defaults to `'python'`. In JSON mode, all values are converted to JSON compatible types, e.g. `None`, `int`, `float`, `str`, `list`, `dict`.

**`include`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(include\)>)

A set of fields to include, if `None` all fields are included.

**`exclude`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(exclude\)>)

A set of fields to exclude, if `None` no fields are excluded.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(by_alias\)>)

Whether to use the alias names of fields.

**`exclude_unset`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(exclude_unset\)>)

Whether to exclude fields that are not set, e.g. are not included in `__pydantic_fields_set__`.

**`exclude_defaults`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(exclude_defaults\)>)

Whether to exclude fields that are equal to their default value.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(exclude_none\)>)

Whether to exclude fields that have a value of `None`.

**`exclude_computed_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(exclude_computed_fields\)>)

Whether to exclude computed fields.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(round_trip\)>)

Whether to enable serialization and validation round-trip support.

**`warnings`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘none’, ‘warn’, ‘error’] _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(warnings\)>)

How to handle invalid fields. False/“none” ignores them, True/“warn” logs errors, “error” raises a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>).

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(fallback\)>)

A function to call when an unknown value is encountered, if `None` a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python\(context\)>)

The context to use for serialization, this is passed to functional serializers as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.context>).

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-5>)

  * `PydanticSerializationError` — If serialization fails and no `fallback` function is provided.

#### to_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json>)
    
    def to_json(
        value: Any,
        *,
        indent: int | None = None,
        ensure_ascii: bool = False,
        include: _IncEx | None = None,
        exclude: _IncEx | None = None,
        by_alias: bool | None = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
        exclude_computed_fields: bool = False,
        round_trip: bool = False,
        warnings: bool | Literal['none', 'warn', 'error'] = True,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
        polymorphic_serialization: bool | None = None,
        context: Any | None = None,
    ) -> bytes
    
Serialize a Python object to JSON including transforming and filtering data.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-7>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — JSON bytes.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-6>)

**`value`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(value\)>)

The Python object to serialize.

**`indent`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(indent\)>)

If `None`, the JSON will be compact, otherwise it will be pretty-printed with the indent provided.

**`ensure_ascii`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(ensure_ascii\)>)

If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped. If `False` (the default), these characters will be output as-is.

**`include`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(include\)>)

A set of fields to include, if `None` all fields are included.

**`exclude`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(exclude\)>)

A set of fields to exclude, if `None` no fields are excluded.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(by_alias\)>)

Whether to use the alias names of fields.

**`exclude_unset`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(exclude_unset\)>)

Whether to exclude fields that are not set, e.g. are not included in `__pydantic_fields_set__`.

**`exclude_defaults`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(exclude_defaults\)>)

Whether to exclude fields that are equal to their default value.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(exclude_none\)>)

Whether to exclude fields that have a value of `None`.

**`exclude_computed_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(exclude_computed_fields\)>)

Whether to exclude computed fields.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(round_trip\)>)

Whether to enable serialization and validation round-trip support.

**`warnings`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘none’, ‘warn’, ‘error’] _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(warnings\)>)

How to handle invalid fields. False/“none” ignores them, True/“warn” logs errors, “error” raises a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>).

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(fallback\)>)

A function to call when an unknown value is encountered, if `None` a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json\(context\)>)

The context to use for serialization, this is passed to functional serializers as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.context>).

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-6>)

  * `PydanticSerializationError` — If serialization fails and no `fallback` function is provided.

## ValidationError 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError>)

**Bases:** [`ValueError`](<https://docs.python.org/3/library/exceptions.html#ValueError>)

`ValidationError` is the exception raised by `pydantic-core` when validation fails, it contains a list of errors which detail why validation failed.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-1>)

#### title 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.title>)

The title of the error, as used in the heading of `str(validation_error)`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#methods-2>)

#### from_exception_data 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.from_exception_data>)

`@classmethod`
    
    def from_exception_data(
        cls,
        title: str,
        line_errors: list[InitErrorDetails],
        input_type: Literal['python', 'json'] = 'python',
        hide_input: bool = False,
    ) -> Self
    
Python constructor for a Validation Error.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-8>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>)

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-7>)

**`title`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.from_exception_data\(title\)>)

The title of the error, as used in the heading of `str(validation_error)`

**`line_errors`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`InitErrorDetails`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.from_exception_data\(line_errors\)>)

A list of [`InitErrorDetails`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.InitErrorDetails>) which contain information about errors that occurred during validation.

**`input_type`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘python’, ‘json’] _Default:_ `'python'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.from_exception_data\(input_type\)>)

Whether the error is for a Python object or JSON.

**`hide_input`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.from_exception_data\(hide_input\)>)

Whether to hide the input value in the error message.

#### error_count 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.error_count>)
    
    def error_count() -> int
    
##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-9>)

[`int`](<https://docs.python.org/3/library/functions.html#int>) — The number of errors in the validation error.

#### errors 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.errors>)
    
    def errors(
        *,
        include_url: bool = True,
        include_context: bool = True,
        include_input: bool = True,
    ) -> list[ErrorDetails]
    
Details about each error in the validation error.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-10>)

[`list`](<https://docs.python.org/3/glossary.html#term-list>)[`ErrorDetails`] — A list of [`ErrorDetails`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails>) for each error in the validation error.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-8>)

**`include_url`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.errors\(include_url\)>)

Whether to include a URL to documentation on the error each error.

**`include_context`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.errors\(include_context\)>)

Whether to include the context of each error.

**`include_input`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.errors\(include_input\)>)

Whether to include the input value of each error.

#### json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.json>)
    
    def json(
        *,
        indent: int | None = None,
        include_url: bool = True,
        include_context: bool = True,
        include_input: bool = True,
    ) -> str
    
Same as [`errors()`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.errors>) but returns a JSON string.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-11>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — a JSON string.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-9>)

**`indent`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.json\(indent\)>)

The number of spaces to indent the JSON by, or `None` for no indentation - compact JSON.

**`include_url`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.json\(include_url\)>)

Whether to include a URL to documentation on the error each error.

**`include_context`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.json\(include_context\)>)

Whether to include the context of each error.

**`include_input`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError.json\(include_input\)>)

Whether to include the input value of each error.

## ErrorDetails 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails>)

**Bases:** `_TypedDict`

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-2>)

#### type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails.type>)

The type of error that occurred, this is an identifier designed for programmatic use that will change rarely or never.

`type` is unique for each error message, and can hence be used as an identifier to build custom error messages.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### loc 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails.loc>)

Tuple of strings and ints identifying where in the schema the error occurred.

**Type:** [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`int`](<https://docs.python.org/3/library/functions.html#int>) | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), …]

#### msg 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails.msg>)

A human readable error message.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### input 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails.input>)

The input data at this `loc` that caused the error.

**Type:** `_Any`

#### ctx 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails.ctx>)

Values which are required to render the error message, and could hence be useful in rendering custom error messages. Also useful for passing custom error data forward.

**Type:** `_NotRequired`[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `_Any`]]

#### url 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails.url>)

The documentation URL giving information about the error. No URL is available if a [`PydanticCustomError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError>) is used.

**Type:** `_NotRequired`[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]

## InitErrorDetails 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.InitErrorDetails>)

**Bases:** `_TypedDict`

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-3>)

#### type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.InitErrorDetails.type>)

The type of error that occurred, this should be a “slug” identifier that changes rarely or never.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | `PydanticCustomError`

#### loc 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.InitErrorDetails.loc>)

Tuple of strings and ints identifying where in the schema the error occurred.

**Type:** `_NotRequired`[[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`int`](<https://docs.python.org/3/library/functions.html#int>) | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), …]]

#### input 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.InitErrorDetails.input>)

The input data at this `loc` that caused the error.

**Type:** `_Any`

#### ctx 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.InitErrorDetails.ctx>)

Values which are required to render the error message, and could hence be useful in rendering custom error messages. Also useful for passing custom error data forward.

**Type:** `_NotRequired`[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `_Any`]]

## SchemaError 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaError>)

**Bases:** [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception>)

Information about errors that occur while building a [`SchemaValidator`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaValidator>) or [`SchemaSerializer`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer>).

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#methods-3>)

#### error_count 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaError.error_count>)
    
    def error_count() -> int
    
##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-12>)

[`int`](<https://docs.python.org/3/library/functions.html#int>) — The number of errors in the schema.

#### errors 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaError.errors>)
    
    def errors() -> list[ErrorDetails]
    
##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-13>)

[`list`](<https://docs.python.org/3/glossary.html#term-list>)[`ErrorDetails`] — A list of [`ErrorDetails`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorDetails>) for each error in the schema.

## PydanticCustomError 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError>)

**Bases:** [`ValueError`](<https://docs.python.org/3/library/exceptions.html#ValueError>)

A custom exception providing flexible error handling for Pydantic validators.

You can raise this error in custom validators when you’d like flexibility in regards to the error type, message, and context.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#constructor-parameters>)

**`error_type`** : [`LiteralString`](<https://docs.python.org/3/library/typing.html#typing.LiteralString>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError.__init__\(error_type\)>)

The error type.

**`message_template`** : [`LiteralString`](<https://docs.python.org/3/library/typing.html#typing.LiteralString>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError.__init__\(message_template\)>)

The message template.

**`context`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError.__init__\(context\)>)

The data to inject into the message template.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-4>)

#### context 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError.context>)

Values which are required to render the error message, and could hence be useful in passing error data forward.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError.type>)

The error type associated with the error. For consistency with Pydantic, this is typically a snake_case string.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### message_template 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError.message_template>)

The message template associated with the error. This is a string that can be formatted with context variables in `{curly_braces}`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#methods-4>)

#### message 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError.message>)
    
    def message() -> str
    
The formatted message associated with the error. This presents as the message template with context variables appropriately injected.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-14>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## PydanticKnownError 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticKnownError>)

**Bases:** [`ValueError`](<https://docs.python.org/3/library/exceptions.html#ValueError>)

A helper class for raising exceptions that mimic Pydantic’s built-in exceptions, with more flexibility in regards to context.

Unlike [`PydanticCustomError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticCustomError>), the `error_type` argument must be a known `ErrorType`.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#constructor-parameters-1>)

**`error_type`** : `ErrorType`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticKnownError.__init__\(error_type\)>)

The error type.

**`context`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticKnownError.__init__\(context\)>)

The data to inject into the message template.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-5>)

#### context 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticKnownError.context>)

Values which are required to render the error message, and could hence be useful in passing error data forward.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticKnownError.type>)

The type of the error.

**Type:** `ErrorType`

#### message_template 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticKnownError.message_template>)

The message template associated with the provided error type. This is a string that can be formatted with context variables in `{curly_braces}`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#methods-5>)

#### message 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticKnownError.message>)
    
    def message() -> str
    
The formatted message associated with the error. This presents as the message template with context variables appropriately injected.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-15>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## PydanticOmit 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticOmit>)

**Bases:** [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception>)

An exception to signal that a field should be omitted from a generated result.

This could span from omitting a field from a JSON Schema to omitting a field from a serialized result. Upcoming: more robust support for using PydanticOmit in custom serializers is still in development. Right now, this is primarily used in the JSON Schema generation process.

For a more in depth example / explanation, see the [customizing JSON schema](<https://pydantic.dev/docs/validation/latest/concepts/json_schema#customizing-the-json-schema-generation-process>) docs.

## PydanticUseDefault 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticUseDefault>)

**Bases:** [`Exception`](<https://docs.python.org/3/library/exceptions.html#Exception>)

An exception to signal that standard validation either failed or should be skipped, and the default value should be used instead.

This warning can be raised in custom validation functions to redirect the flow of validation.

For an additional example, see the [validating partial json data](<https://pydantic.dev/docs/validation/latest/concepts/json#partial-json-parsing>) section of the Pydantic documentation.

## PydanticSerializationError 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>)

**Bases:** [`ValueError`](<https://docs.python.org/3/library/exceptions.html#ValueError>)

An error raised when an issue occurs during serialization.

In custom serializers, this error can be used to indicate that serialization has failed.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#constructor-parameters-2>)

**`message`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError.__init__\(message\)>)

The message associated with the error.

## PydanticSerializationUnexpectedValue 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationUnexpectedValue>)

**Bases:** [`ValueError`](<https://docs.python.org/3/library/exceptions.html#ValueError>)

An error raised when an unexpected value is encountered during serialization.

This error is often caught and coerced into a warning, as `pydantic-core` generally makes a best attempt at serializing values, in contrast with validation where errors are eagerly raised.

This is often used internally in `pydantic-core` when unexpected types are encountered during serialization, but it can also be used by users in custom serializers, as seen above.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#constructor-parameters-3>)

**`message`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationUnexpectedValue.__init__\(message\)>)

The message associated with the unexpected value.

## Url 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.Url>)

**Bases:** `SupportsAllComparisons`

A URL type, internal logic uses the [url rust crate](<https://docs.rs/url/latest/url/>) originally developed by Mozilla.

## MultiHostUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.MultiHostUrl>)

**Bases:** `SupportsAllComparisons`

A URL type with support for multiple hosts, as used by some databases for DSNs, e.g. `https://foo.com,bar.com/path`.

Internal URL logic uses the [url rust crate](<https://docs.rs/url/latest/url/>) originally developed by Mozilla.

## MultiHostHost 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.MultiHostHost>)

**Bases:** `_TypedDict`

A host part of a multi-host URL.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-6>)

#### username 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.MultiHostHost.username>)

The username part of this host, or `None`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### password 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.MultiHostHost.password>)

The password part of this host, or `None`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### host 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.MultiHostHost.host>)

The host part of this host, or `None`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### port 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.MultiHostHost.port>)

The port part of this host, or `None`.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

## ArgsKwargs 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ArgsKwargs>)

A construct used to store arguments and keyword arguments for a function call.

This data structure is generally used to store information for core schemas associated with functions (like in an arguments schema). This data structure is also currently used for some validation against dataclasses.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-7>)

#### args 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ArgsKwargs.args>)

The arguments (inherently ordered) for a function call.

**Type:** [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>), …]

#### kwargs 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ArgsKwargs.kwargs>)

The keyword arguments for a function call.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

## Some 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.Some>)

**Bases:** `Generic[_T]`

Similar to Rust’s [`Option::Some`](<https://doc.rust-lang.org/std/option/enum.Option.html>) type, this identifies a value as being present, and provides a way to access it.

Generally used in a union with `None` to different between “some value which could be None” and no value.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-8>)

#### value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.Some.value>)

Returns the value wrapped by `Some`.

**Type:** `_T`

## TzInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.TzInfo>)

**Bases:** [`tzinfo`](<https://docs.python.org/3/library/datetime.html#datetime.tzinfo>)

An `pydantic-core` implementation of the abstract [`datetime.tzinfo`](<https://docs.python.org/3/library/datetime.html#datetime.tzinfo>) class.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#methods-6>)

#### tzname 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.TzInfo.tzname>)
    
    def tzname(dt: datetime.datetime | None) -> str | None
    
Return the time zone name corresponding to the [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) object _dt_ , as a string.

For more info, see [`tzinfo.tzname`](<https://docs.python.org/3/library/datetime.html#datetime.tzinfo.tzname>).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-16>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### utcoffset 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.TzInfo.utcoffset>)
    
    def utcoffset(dt: datetime.datetime | None) -> datetime.timedelta | None
    
Return offset of local time from UTC, as a [`timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) object that is positive east of UTC. If local time is west of UTC, this should be negative.

More info can be found at [`tzinfo.utcoffset`](<https://docs.python.org/3/library/datetime.html#datetime.tzinfo.utcoffset>).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-17>)

[`datetime.timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### dst 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.TzInfo.dst>)
    
    def dst(dt: datetime.datetime | None) -> datetime.timedelta | None
    
Return the daylight saving time (DST) adjustment, as a [`timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) object or `None` if DST information isn’t known.

More info can be found at[`tzinfo.dst`](<https://docs.python.org/3/library/datetime.html#datetime.tzinfo.dst>).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-18>)

[`datetime.timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### fromutc 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.TzInfo.fromutc>)
    
    def fromutc(dt: datetime.datetime) -> datetime.datetime
    
Adjust the date and time data associated datetime object _dt_ , returning an equivalent datetime in self’s local time.

More info can be found at [`tzinfo.fromutc`](<https://docs.python.org/3/library/datetime.html#datetime.tzinfo.fromutc>).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-19>)

[`datetime.datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>)

## ErrorTypeInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorTypeInfo>)

**Bases:** `_TypedDict`

Gives information about errors.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#attributes-9>)

#### type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorTypeInfo.type>)

The type of error that occurred, this should be a “slug” identifier that changes rarely or never.

**Type:** `ErrorType`

#### message_template_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorTypeInfo.message_template_python>)

String template to render a human readable error message from using context, when the input is Python.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### example_message_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorTypeInfo.example_message_python>)

Example of a human readable error message, when the input is Python.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### message_template_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorTypeInfo.message_template_json>)

String template to render a human readable error message from using context, when the input is JSON data.

**Type:** `_NotRequired`[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]

#### example_message_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorTypeInfo.example_message_json>)

Example of a human readable error message, when the input is JSON data.

**Type:** `_NotRequired`[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]

#### example_context 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ErrorTypeInfo.example_context>)

Example of context values.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `_Any`] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

## to_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json>)
    
    def to_json(
        value: Any,
        *,
        indent: int | None = None,
        ensure_ascii: bool = False,
        include: _IncEx | None = None,
        exclude: _IncEx | None = None,
        by_alias: bool = True,
        exclude_none: bool = False,
        round_trip: bool = False,
        timedelta_mode: Literal['iso8601', 'float'] = 'iso8601',
        temporal_mode: Literal['iso8601', 'seconds', 'milliseconds'] = 'iso8601',
        bytes_mode: Literal['utf8', 'base64', 'hex'] = 'utf8',
        inf_nan_mode: Literal['null', 'constants', 'strings'] = 'constants',
        serialize_unknown: bool = False,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
        polymorphic_serialization: bool | None = None,
        context: Any | None = None,
    ) -> bytes
    
Serialize a Python object to JSON including transforming and filtering data.

This is effectively a standalone version of [`SchemaSerializer.to_json`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_json>).

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-20>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — JSON bytes.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-10>)

**`value`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(value\)>)

The Python object to serialize.

**`indent`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(indent\)>)

If `None`, the JSON will be compact, otherwise it will be pretty-printed with the indent provided.

**`ensure_ascii`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(ensure_ascii\)>)

If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped. If `False` (the default), these characters will be output as-is.

**`include`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(include\)>)

A set of fields to include, if `None` all fields are included.

**`exclude`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(exclude\)>)

A set of fields to exclude, if `None` no fields are excluded.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(by_alias\)>)

Whether to use the alias names of fields.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(exclude_none\)>)

Whether to exclude fields that have a value of `None`.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(round_trip\)>)

Whether to enable serialization and validation round-trip support.

**`timedelta_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘float’] _Default:_ `'iso8601'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(timedelta_mode\)>)

How to serialize `timedelta` objects, either `'iso8601'` or `'float'`.

**`temporal_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘seconds’, ‘milliseconds’] _Default:_ `'iso8601'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(temporal_mode\)>)

How to serialize datetime-like objects (`datetime`, `date`, `time`), either `'iso8601'`, `'seconds'`, or `'milliseconds'`. `iso8601` returns an ISO 8601 string; `seconds` returns the Unix timestamp in seconds as a float; `milliseconds` returns the Unix timestamp in milliseconds as a float.

**`bytes_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘utf8’, ‘base64’, ‘hex’] _Default:_ `'utf8'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(bytes_mode\)>)

How to serialize `bytes` objects, either `'utf8'`, `'base64'`, or `'hex'`.

**`inf_nan_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘null’, ‘constants’, ‘strings’] _Default:_ `'constants'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(inf_nan_mode\)>)

How to serialize `Infinity`, `-Infinity` and `NaN` values, either `'null'`, `'constants'`, or `'strings'`.

**`serialize_unknown`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(serialize_unknown\)>)

Attempt to serialize unknown types, `str(value)` will be used, if that fails `"<Unserializable {value_type} object>"` will be used.

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(fallback\)>)

A function to call when an unknown value is encountered, if `None` a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_json\(context\)>)

The context to use for serialization, this is passed to functional serializers as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.context>).

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-7>)

  * `PydanticSerializationError` — If serialization fails and no `fallback` function is provided.

## from_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.from_json>)
    
    def from_json(
        data: str | bytes | bytearray,
        *,
        allow_inf_nan: bool = True,
        cache_strings: bool | Literal['all', 'keys', 'none'] = True,
        allow_partial: bool | Literal['off', 'on', 'trailing-strings'] = False,
    ) -> Any
    
Deserialize JSON data to a Python object.

This is effectively a faster version of `json.loads()`, with some extra functionality.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-21>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The deserialized Python object.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-11>)

**`data`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) | [`bytearray`](<https://docs.python.org/3/library/stdtypes.html#bytearray>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.from_json\(data\)>)

The JSON data to deserialize.

**`allow_inf_nan`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.from_json\(allow_inf_nan\)>)

Whether to allow `Infinity`, `-Infinity` and `NaN` values as `json.loads()` does by default.

**`cache_strings`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘all’, ‘keys’, ‘none’] _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.from_json\(cache_strings\)>)

Whether to cache strings to avoid constructing new Python objects, this should have a significant impact on performance while increasing memory usage slightly, `all/True` means cache all strings, `keys` means cache only dict keys, `none/False` means no caching.

**`allow_partial`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘off’, ‘on’, ‘trailing-strings’] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.from_json\(allow_partial\)>)

Whether to allow partial deserialization, if `True` JSON data is returned if the end of the input is reached before the full object is deserialized, e.g. `["aa", "bb", "c` would return `['aa', 'bb']`. `'trailing-strings'` means any final unfinished JSON string is included in the result.

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-8>)

  * `ValueError` — If deserialization fails.

## to_jsonable_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python>)
    
    def to_jsonable_python(
        value: Any,
        *,
        include: _IncEx | None = None,
        exclude: _IncEx | None = None,
        by_alias: bool = True,
        exclude_none: bool = False,
        round_trip: bool = False,
        timedelta_mode: Literal['iso8601', 'float'] = 'iso8601',
        temporal_mode: Literal['iso8601', 'seconds', 'milliseconds'] = 'iso8601',
        bytes_mode: Literal['utf8', 'base64', 'hex'] = 'utf8',
        inf_nan_mode: Literal['null', 'constants', 'strings'] = 'constants',
        serialize_unknown: bool = False,
        fallback: Callable[[Any], Any] | None = None,
        serialize_as_any: bool = False,
        polymorphic_serialization: bool | None = None,
        context: Any | None = None,
    ) -> Any
    
Serialize/marshal a Python object to a JSON-serializable Python object including transforming and filtering data.

This is effectively a standalone version of [`SchemaSerializer.to_python(mode='json')`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.SchemaSerializer.to_python>).

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#returns-22>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The serialized Python object.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#parameters-12>)

**`value`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(value\)>)

The Python object to serialize.

**`include`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(include\)>)

A set of fields to include, if `None` all fields are included.

**`exclude`** : `_IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(exclude\)>)

A set of fields to exclude, if `None` no fields are excluded.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(by_alias\)>)

Whether to use the alias names of fields.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(exclude_none\)>)

Whether to exclude fields that have a value of `None`.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(round_trip\)>)

Whether to enable serialization and validation round-trip support.

**`timedelta_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘float’] _Default:_ `'iso8601'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(timedelta_mode\)>)

How to serialize `timedelta` objects, either `'iso8601'` or `'float'`.

**`temporal_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘seconds’, ‘milliseconds’] _Default:_ `'iso8601'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(temporal_mode\)>)

How to serialize datetime-like objects (`datetime`, `date`, `time`), either `'iso8601'`, `'seconds'`, or `'milliseconds'`. `iso8601` returns an ISO 8601 string; `seconds` returns the Unix timestamp in seconds as a float; `milliseconds` returns the Unix timestamp in milliseconds as a float.

**`bytes_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘utf8’, ‘base64’, ‘hex’] _Default:_ `'utf8'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(bytes_mode\)>)

How to serialize `bytes` objects, either `'utf8'`, `'base64'`, or `'hex'`.

**`inf_nan_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘null’, ‘constants’, ‘strings’] _Default:_ `'constants'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(inf_nan_mode\)>)

How to serialize `Infinity`, `-Infinity` and `NaN` values, either `'null'`, `'constants'`, or `'strings'`.

**`serialize_unknown`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(serialize_unknown\)>)

Attempt to serialize unknown types, `str(value)` will be used, if that fails `"<Unserializable {value_type} object>"` will be used.

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(fallback\)>)

A function to call when an unknown value is encountered, if `None` a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.to_jsonable_python\(context\)>)

The context to use for serialization, this is passed to functional serializers as [`info.context`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.context>).

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#raises-9>)

  * `PydanticSerializationError` — If serialization fails and no `fallback` function is provided.

## __version__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.__version__>)

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

Was this page helpful?

Thanks for your feedback!