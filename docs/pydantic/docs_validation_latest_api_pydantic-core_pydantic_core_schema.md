# pydantic_core.core_schema | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/](https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# pydantic_core.core_schema

This module contains definitions to build schemas which `pydantic_core` can validate and serialize.

## CoreConfig 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig>)

**Bases:** [`TypedDict`](<https://docs.python.org/3/library/typing.html#typing.TypedDict>)

Base class for schema configuration options.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#attributes>)

#### title 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.title>)

The name of the configuration.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### strict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.strict>)

Whether the configuration should strictly adhere to specified rules.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### extra_fields_behavior 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.extra_fields_behavior>)

The behavior for handling extra fields.

**Type:** `ExtraBehavior`

#### typed_dict_total 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.typed_dict_total>)

Whether the TypedDict should be considered total. Default is `True`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### from_attributes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.from_attributes>)

Whether to use attributes for models, dataclasses, and tagged union keys.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### loc_by_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.loc_by_alias>)

Whether to use the used alias (or first alias for “field required” errors) instead of `field_names` to construct error `loc`s. Default is `True`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### revalidate_instances 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.revalidate_instances>)

Whether instances of models and dataclasses should re-validate. Default is ‘never’.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘always’, ‘never’, ‘subclass-instances’]

#### validate_default 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.validate_default>)

Whether to validate default values during validation. Default is `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### str_max_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.str_max_length>)

The maximum length for string fields.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>)

#### str_min_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.str_min_length>)

The minimum length for string fields.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>)

#### str_strip_whitespace 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.str_strip_whitespace>)

Whether to strip whitespace from string fields.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### str_to_lower 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.str_to_lower>)

Whether to convert string fields to lowercase.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### str_to_upper 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.str_to_upper>)

Whether to convert string fields to uppercase.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### allow_inf_nan 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.allow_inf_nan>)

Whether to allow infinity and NaN values for float fields. Default is `True`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### ser_json_timedelta 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.ser_json_timedelta>)

The serialization option for `timedelta` values. Default is ‘iso8601’. Note that if ser_json_temporal is set, then this param will be ignored.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘float’]

#### ser_json_temporal 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.ser_json_temporal>)

The serialization option for datetime like values. Default is ‘iso8601’. The types this covers are datetime, date, time and timedelta. If this is set, it will take precedence over ser_json_timedelta

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘seconds’, ‘milliseconds’]

#### ser_json_bytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.ser_json_bytes>)

The serialization option for `bytes` values. Default is ‘utf8’.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘utf8’, ‘base64’, ‘hex’]

#### ser_json_inf_nan 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.ser_json_inf_nan>)

The serialization option for infinity and NaN values in float fields. Default is ‘null’.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘null’, ‘constants’, ‘strings’]

#### val_json_bytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.val_json_bytes>)

The validation option for `bytes` values, complementing ser_json_bytes. Default is ‘utf8’.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘utf8’, ‘base64’, ‘hex’]

#### hide_input_in_errors 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.hide_input_in_errors>)

Whether to hide input data from `ValidationError` representation.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### validation_error_cause 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.validation_error_cause>)

Whether to add user-python excs to the **cause** of a ValidationError. Requires exceptiongroup backport pre Python 3.11.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### coerce_numbers_to_str 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.coerce_numbers_to_str>)

Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### regex_engine 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.regex_engine>)

The regex engine to use for regex pattern validation. Default is ‘rust-regex’. See `StringSchema`.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘rust-regex’, ‘python-re’]

#### cache_strings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.cache_strings>)

Whether to cache strings. Default is `True`, `True` or `'all'` is required to cache strings during general validation since validators don’t know if they’re in a key or a value.

**Type:** [`Union`](<https://docs.python.org/3/library/typing.html#typing.Union>)[[`bool`](<https://docs.python.org/3/library/functions.html#bool>), [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘all’, ‘keys’, ‘none’]]

#### validate_by_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.validate_by_alias>)

Whether to use the field’s alias when validating against the provided input data. Default is `True`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### validate_by_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.validate_by_name>)

Whether to use the field’s name when validating against the provided input data. Default is `False`. Replacement for `populate_by_name`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### serialize_by_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.serialize_by_alias>)

Whether to serialize by alias. Default is `False`, expected to change to `True` in V3.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### polymorphic_serialization 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.polymorphic_serialization>)

Whether to enable polymorphic serialization for models and dataclasses. Default is `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### url_preserve_empty_path 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.CoreConfig.url_preserve_empty_path>)

Whether to preserve empty URL paths when validating values for a URL type. Defaults to `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

## SerializationInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo>)

**Bases:** `Protocol[ContextT]`

Extra data used during serialization.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#attributes-1>)

#### include 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.include>)

The `include` argument set during serialization.

**Type:** `IncExCall`

#### exclude 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.exclude>)

The `exclude` argument set during serialization.

**Type:** `IncExCall`

#### context 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.context>)

The current serialization context.

**Type:** `ContextT`

#### mode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.mode>)

The serialization mode set during serialization.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘python’, ‘json’] | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### by_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.by_alias>)

The `by_alias` argument set during serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### exclude_unset 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.exclude_unset>)

The `exclude_unset` argument set during serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### exclude_defaults 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.exclude_defaults>)

The `exclude_defaults` argument set during serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### exclude_none 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.exclude_none>)

The `exclude_none` argument set during serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### exclude_computed_fields 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.exclude_computed_fields>)

The `exclude_computed_fields` argument set during serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### serialize_as_any 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.serialize_as_any>)

The `serialize_as_any` argument set during serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### polymorphic_serialization 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.polymorphic_serialization>)

The `polymorphic_serialization` argument set during serialization, if any.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### round_trip 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.SerializationInfo.round_trip>)

The `round_trip` argument set during serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

## FieldSerializationInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.FieldSerializationInfo>)

**Bases:** `SerializationInfo[ContextT]`, [`Protocol`](<https://docs.python.org/3/library/typing.html#typing.Protocol>)

Extra data used during field serialization.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#attributes-2>)

#### field_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.FieldSerializationInfo.field_name>)

The name of the current field being serialized.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## ValidationInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo>)

**Bases:** `Protocol[ContextT]`

Extra data used during validation.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#attributes-3>)

#### context 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.context>)

The current validation context.

**Type:** `ContextT`

#### config 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.config>)

The CoreConfig that applies to this validation.

**Type:** `CoreConfig` | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### mode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.mode>)

The type of input data we are currently validating.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘python’, ‘json’]

#### data 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.data>)

The data being validated for this model.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]

#### field_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.ValidationInfo.field_name>)

The name of the current field being validated if this validator is attached to a model field.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

## simple_ser_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.simple_ser_schema>)
    
    def simple_ser_schema(type: ExpectedSerializationTypes) -> SimpleSerSchema
    
Returns a schema for serialization with a custom type.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns>)

`SimpleSerSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters>)

**`type`** : `ExpectedSerializationTypes`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.simple_ser_schema\(type\)>)

The type to use for serialization

## plain_serializer_function_ser_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.plain_serializer_function_ser_schema>)
    
    def plain_serializer_function_ser_schema(
        function: SerializerFunction,
        *,
        is_field_serializer: bool | None = None,
        info_arg: bool | None = None,
        return_schema: CoreSchema | None = None,
        when_used: WhenUsed = 'always',
    ) -> PlainSerializerFunctionSerSchema
    
Returns a schema for serialization with a function, can be either a “general” or “field” function.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-1>)

`PlainSerializerFunctionSerSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-1>)

**`function`** : `SerializerFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.plain_serializer_function_ser_schema\(function\)>)

The function to use for serialization

**`is_field_serializer`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.plain_serializer_function_ser_schema\(is_field_serializer\)>)

Whether the serializer is for a field, e.g. takes `model` as the first argument, and `info` includes `field_name`

**`info_arg`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.plain_serializer_function_ser_schema\(info_arg\)>)

Whether the function takes an `info` argument

**`return_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.plain_serializer_function_ser_schema\(return_schema\)>)

Schema to use for serializing return value

**`when_used`** : `WhenUsed` _Default:_ `'always'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.plain_serializer_function_ser_schema\(when_used\)>)

When the function should be called

## wrap_serializer_function_ser_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.wrap_serializer_function_ser_schema>)
    
    def wrap_serializer_function_ser_schema(
        function: WrapSerializerFunction,
        *,
        is_field_serializer: bool | None = None,
        info_arg: bool | None = None,
        schema: CoreSchema | None = None,
        return_schema: CoreSchema | None = None,
        when_used: WhenUsed = 'always',
    ) -> WrapSerializerFunctionSerSchema
    
Returns a schema for serialization with a wrap function, can be either a “general” or “field” function.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-2>)

`WrapSerializerFunctionSerSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-2>)

**`function`** : `WrapSerializerFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.wrap_serializer_function_ser_schema\(function\)>)

The function to use for serialization

**`is_field_serializer`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.wrap_serializer_function_ser_schema\(is_field_serializer\)>)

Whether the serializer is for a field, e.g. takes `model` as the first argument, and `info` includes `field_name`

**`info_arg`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.wrap_serializer_function_ser_schema\(info_arg\)>)

Whether the function takes an `info` argument

**`schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.wrap_serializer_function_ser_schema\(schema\)>)

The schema to use for the inner serialization

**`return_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.wrap_serializer_function_ser_schema\(return_schema\)>)

Schema to use for serializing return value

**`when_used`** : `WhenUsed` _Default:_ `'always'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.wrap_serializer_function_ser_schema\(when_used\)>)

When the function should be called

## format_ser_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.format_ser_schema>)
    
    def format_ser_schema(
        formatting_string: str,
        *,
        when_used: WhenUsed = 'json-unless-none',
    ) -> FormatSerSchema
    
Returns a schema for serialization using python’s `format` method.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-3>)

`FormatSerSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-3>)

**`formatting_string`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.format_ser_schema\(formatting_string\)>)

String defining the format to use

**`when_used`** : `WhenUsed` _Default:_ `'json-unless-none'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.format_ser_schema\(when_used\)>)

Same meaning as for [general_function_plain_ser_schema], but with a different default

## to_string_ser_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.to_string_ser_schema>)
    
    def to_string_ser_schema(
        *,
        when_used: WhenUsed = 'json-unless-none',
    ) -> ToStringSerSchema
    
Returns a schema for serialization using python’s `str()` / `__str__` method.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-4>)

`ToStringSerSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-4>)

**`when_used`** : `WhenUsed` _Default:_ `'json-unless-none'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.to_string_ser_schema\(when_used\)>)

Same meaning as for [general_function_plain_ser_schema], but with a different default

## model_ser_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_ser_schema>)
    
    def model_ser_schema(cls: type[Any], schema: CoreSchema) -> ModelSerSchema
    
Returns a schema for serialization using a model.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-5>)

`ModelSerSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-5>)

**`cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_ser_schema\(cls\)>)

The expected class type, used to generate warnings if the wrong type is passed

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_ser_schema\(schema\)>)

Internal schema to use to serialize the model dict

## invalid_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.invalid_schema>)
    
    def invalid_schema(
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> InvalidSchema
    
Returns an invalid schema, used to indicate that a schema is invalid.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-6>)

`InvalidSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-6>)

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.invalid_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.invalid_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

## computed_field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.computed_field>)
    
    def computed_field(
        property_name: str,
        return_schema: CoreSchema,
        *,
        alias: str | None = None,
        serialization_exclude_if: Callable[[Any], bool] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ComputedField
    
ComputedFields are properties of a model or dataclass that are included in serialization.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-7>)

`ComputedField`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-7>)

**`property_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.computed_field\(property_name\)>)

The name of the property on the model or dataclass

**`return_schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.computed_field\(return_schema\)>)

The schema used for the type returned by the computed field

**`alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.computed_field\(alias\)>)

The name to use in the serialized output

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.computed_field\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

## any_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.any_schema>)
    
    def any_schema(
        *,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> AnySchema
    
Returns a schema that matches any value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.any_schema()
    v = SchemaValidator(schema)
    assert v.validate_python(1) == 1
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-8>)

`AnySchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-8>)

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.any_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.any_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.any_schema\(serialization\)>)

Custom serialization schema

## none_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.none_schema>)
    
    def none_schema(
        *,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> NoneSchema
    
Returns a schema that matches a None value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.none_schema()
    v = SchemaValidator(schema)
    assert v.validate_python(None) is None
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-9>)

`NoneSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-9>)

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.none_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.none_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.none_schema\(serialization\)>)

Custom serialization schema

## bool_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema>)
    
    def bool_schema(
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> BoolSchema
    
Returns a schema that matches a bool value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.bool_schema()
    v = SchemaValidator(schema)
    assert v.validate_python('True') is True
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-10>)

`BoolSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-10>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema\(strict\)>)

Whether the value should be a bool or a value that can be converted to a bool

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bool_schema\(serialization\)>)

Custom serialization schema

## int_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema>)
    
    def int_schema(
        *,
        multiple_of: int | None = None,
        le: int | None = None,
        ge: int | None = None,
        lt: int | None = None,
        gt: int | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> IntSchema
    
Returns a schema that matches a int value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.int_schema(multiple_of=2, le=6, ge=2)
    v = SchemaValidator(schema)
    assert v.validate_python('4') == 4
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-11>)

`IntSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-11>)

**`multiple_of`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(multiple_of\)>)

The value must be a multiple of this number

**`le`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(le\)>)

The value must be less than or equal to this number

**`ge`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(ge\)>)

The value must be greater than or equal to this number

**`lt`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(lt\)>)

The value must be strictly less than this number

**`gt`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(gt\)>)

The value must be strictly greater than this number

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(strict\)>)

Whether the value should be a int or a value that can be converted to a int

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.int_schema\(serialization\)>)

Custom serialization schema

## float_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema>)
    
    def float_schema(
        *,
        allow_inf_nan: bool | None = None,
        multiple_of: float | None = None,
        le: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        gt: float | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> FloatSchema
    
Returns a schema that matches a float value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.float_schema(le=0.8, ge=0.2)
    v = SchemaValidator(schema)
    assert v.validate_python('0.5') == 0.5
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-12>)

`FloatSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-12>)

**`allow_inf_nan`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(allow_inf_nan\)>)

Whether to allow inf and nan values

**`multiple_of`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(multiple_of\)>)

The value must be a multiple of this number

**`le`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(le\)>)

The value must be less than or equal to this number

**`ge`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(ge\)>)

The value must be greater than or equal to this number

**`lt`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(lt\)>)

The value must be strictly less than this number

**`gt`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(gt\)>)

The value must be strictly greater than this number

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(strict\)>)

Whether the value should be a float or a value that can be converted to a float

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.float_schema\(serialization\)>)

Custom serialization schema

## decimal_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema>)
    
    def decimal_schema(
        *,
        allow_inf_nan: bool | None = None,
        multiple_of: Decimal | None = None,
        le: Decimal | None = None,
        ge: Decimal | None = None,
        lt: Decimal | None = None,
        gt: Decimal | None = None,
        max_digits: int | None = None,
        decimal_places: int | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> DecimalSchema
    
Returns a schema that matches a decimal value, e.g.:
    
    from decimal import Decimal
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.decimal_schema(le=0.8, ge=0.2)
    v = SchemaValidator(schema)
    assert v.validate_python('0.5') == Decimal('0.5')
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-13>)

`DecimalSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-13>)

**`allow_inf_nan`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(allow_inf_nan\)>)

Whether to allow inf and nan values

**`multiple_of`** : `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(multiple_of\)>)

The value must be a multiple of this number

**`le`** : `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(le\)>)

The value must be less than or equal to this number

**`ge`** : `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(ge\)>)

The value must be greater than or equal to this number

**`lt`** : `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(lt\)>)

The value must be strictly less than this number

**`gt`** : `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(gt\)>)

The value must be strictly greater than this number

**`max_digits`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(max_digits\)>)

The maximum number of decimal digits allowed

**`decimal_places`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(decimal_places\)>)

The maximum number of decimal places allowed

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(strict\)>)

Whether the value should be a float or a value that can be converted to a float

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.decimal_schema\(serialization\)>)

Custom serialization schema

## complex_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.complex_schema>)
    
    def complex_schema(
        *,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> ComplexSchema
    
Returns a schema that matches a complex value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.complex_schema()
    v = SchemaValidator(schema)
    assert v.validate_python('1+2j') == complex(1, 2)
    assert v.validate_python(complex(1, 2)) == complex(1, 2)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-14>)

`ComplexSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-14>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.complex_schema\(strict\)>)

Whether the value should be a complex object instance or a value that can be converted to a complex object

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.complex_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.complex_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.complex_schema\(serialization\)>)

Custom serialization schema

## str_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema>)
    
    def str_schema(
        *,
        pattern: str | Pattern[str] | None = None,
        max_length: int | None = None,
        min_length: int | None = None,
        strip_whitespace: bool | None = None,
        to_lower: bool | None = None,
        to_upper: bool | None = None,
        regex_engine: Literal['rust-regex', 'python-re'] | None = None,
        strict: bool | None = None,
        coerce_numbers_to_str: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> StringSchema
    
Returns a schema that matches a string value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.str_schema(max_length=10, min_length=2)
    v = SchemaValidator(schema)
    assert v.validate_python('hello') == 'hello'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-15>)

`StringSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-15>)

**`pattern`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`Pattern`](<https://docs.python.org/3/library/typing.html#typing.Pattern>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(pattern\)>)

A regex pattern that the value must match

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(max_length\)>)

The value must be at most this length

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(min_length\)>)

The value must be at least this length

**`strip_whitespace`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(strip_whitespace\)>)

Whether to strip whitespace from the value

**`to_lower`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(to_lower\)>)

Whether to convert the value to lowercase

**`to_upper`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(to_upper\)>)

Whether to convert the value to uppercase

**`regex_engine`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘rust-regex’, ‘python-re’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(regex_engine\)>)

The regex engine to use for pattern validation. Default is ‘rust-regex’.

  * `rust-regex` uses the [`regex`](<https://docs.rs/regex>) Rust crate, which is non-backtracking and therefore more DDoS resistant, but does not support all regex features.
  * `python-re` use the [`re`](<https://docs.python.org/3/library/re.html>) module, which supports all regex features, but may be slower.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(strict\)>)

Whether the value should be a string or a value that can be converted to a string

**`coerce_numbers_to_str`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(coerce_numbers_to_str\)>)

Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.str_schema\(serialization\)>)

Custom serialization schema

## bytes_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bytes_schema>)
    
    def bytes_schema(
        *,
        max_length: int | None = None,
        min_length: int | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> BytesSchema
    
Returns a schema that matches a bytes value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.bytes_schema(max_length=10, min_length=2)
    v = SchemaValidator(schema)
    assert v.validate_python(b'hello') == b'hello'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-16>)

`BytesSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-16>)

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bytes_schema\(max_length\)>)

The value must be at most this length

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bytes_schema\(min_length\)>)

The value must be at least this length

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bytes_schema\(strict\)>)

Whether the value should be a bytes or a value that can be converted to a bytes

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bytes_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bytes_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.bytes_schema\(serialization\)>)

Custom serialization schema

## date_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema>)
    
    def date_schema(
        *,
        strict: bool | None = None,
        le: date | None = None,
        ge: date | None = None,
        lt: date | None = None,
        gt: date | None = None,
        now_op: Literal['past', 'future'] | None = None,
        now_utc_offset: int | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> DateSchema
    
Returns a schema that matches a date value, e.g.:
    
    from datetime import date
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.date_schema(le=date(2020, 1, 1), ge=date(2019, 1, 1))
    v = SchemaValidator(schema)
    assert v.validate_python(date(2019, 6, 1)) == date(2019, 6, 1)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-17>)

`DateSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-17>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(strict\)>)

Whether the value should be a date or a value that can be converted to a date

**`le`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(le\)>)

The value must be less than or equal to this date

**`ge`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(ge\)>)

The value must be greater than or equal to this date

**`lt`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(lt\)>)

The value must be strictly less than this date

**`gt`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(gt\)>)

The value must be strictly greater than this date

**`now_op`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘past’, ‘future’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(now_op\)>)

The value must be in the past or future relative to the current date

**`now_utc_offset`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(now_utc_offset\)>)

The value must be in the past or future relative to the current date with this utc offset

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.date_schema\(serialization\)>)

Custom serialization schema

## time_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema>)
    
    def time_schema(
        *,
        strict: bool | None = None,
        le: time | None = None,
        ge: time | None = None,
        lt: time | None = None,
        gt: time | None = None,
        tz_constraint: Literal['aware', 'naive'] | int | None = None,
        microseconds_precision: Literal['truncate', 'error'] = 'truncate',
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> TimeSchema
    
Returns a schema that matches a time value, e.g.:
    
    from datetime import time
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.time_schema(le=time(12, 0, 0), ge=time(6, 0, 0))
    v = SchemaValidator(schema)
    assert v.validate_python(time(9, 0, 0)) == time(9, 0, 0)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-18>)

`TimeSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-18>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(strict\)>)

Whether the value should be a time or a value that can be converted to a time

**`le`** : [`time`](<https://docs.python.org/3/library/time.html#module-time>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(le\)>)

The value must be less than or equal to this time

**`ge`** : [`time`](<https://docs.python.org/3/library/time.html#module-time>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(ge\)>)

The value must be greater than or equal to this time

**`lt`** : [`time`](<https://docs.python.org/3/library/time.html#module-time>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(lt\)>)

The value must be strictly less than this time

**`gt`** : [`time`](<https://docs.python.org/3/library/time.html#module-time>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(gt\)>)

The value must be strictly greater than this time

**`tz_constraint`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘aware’, ‘naive’] | [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(tz_constraint\)>)

The value must be timezone aware or naive, or an int to indicate required tz offset

**`microseconds_precision`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘truncate’, ‘error’] _Default:_ `'truncate'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(microseconds_precision\)>)

The behavior when seconds have more than 6 digits or microseconds is too large

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.time_schema\(serialization\)>)

Custom serialization schema

## datetime_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema>)
    
    def datetime_schema(
        *,
        strict: bool | None = None,
        le: datetime | None = None,
        ge: datetime | None = None,
        lt: datetime | None = None,
        gt: datetime | None = None,
        now_op: Literal['past', 'future'] | None = None,
        tz_constraint: Literal['aware', 'naive'] | int | None = None,
        now_utc_offset: int | None = None,
        microseconds_precision: Literal['truncate', 'error'] = 'truncate',
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> DatetimeSchema
    
Returns a schema that matches a datetime value, e.g.:
    
    from datetime import datetime
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.datetime_schema()
    v = SchemaValidator(schema)
    now = datetime.now()
    assert v.validate_python(str(now)) == now
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-19>)

`DatetimeSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-19>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(strict\)>)

Whether the value should be a datetime or a value that can be converted to a datetime

**`le`** : [`datetime`](<https://docs.python.org/3/library/datetime.html#module-datetime>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(le\)>)

The value must be less than or equal to this datetime

**`ge`** : [`datetime`](<https://docs.python.org/3/library/datetime.html#module-datetime>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(ge\)>)

The value must be greater than or equal to this datetime

**`lt`** : [`datetime`](<https://docs.python.org/3/library/datetime.html#module-datetime>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(lt\)>)

The value must be strictly less than this datetime

**`gt`** : [`datetime`](<https://docs.python.org/3/library/datetime.html#module-datetime>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(gt\)>)

The value must be strictly greater than this datetime

**`now_op`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘past’, ‘future’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(now_op\)>)

The value must be in the past or future relative to the current datetime

**`tz_constraint`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘aware’, ‘naive’] | [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(tz_constraint\)>)

The value must be timezone aware or naive, or an int to indicate required tz offset TODO: use of a tzinfo where offset changes based on the datetime is not yet supported

**`now_utc_offset`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(now_utc_offset\)>)

The value must be in the past or future relative to the current datetime with this utc offset

**`microseconds_precision`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘truncate’, ‘error’] _Default:_ `'truncate'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(microseconds_precision\)>)

The behavior when seconds have more than 6 digits or microseconds is too large

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.datetime_schema\(serialization\)>)

Custom serialization schema

## timedelta_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema>)
    
    def timedelta_schema(
        *,
        strict: bool | None = None,
        le: timedelta | None = None,
        ge: timedelta | None = None,
        lt: timedelta | None = None,
        gt: timedelta | None = None,
        microseconds_precision: Literal['truncate', 'error'] = 'truncate',
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> TimedeltaSchema
    
Returns a schema that matches a timedelta value, e.g.:
    
    from datetime import timedelta
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.timedelta_schema(le=timedelta(days=1), ge=timedelta(days=0))
    v = SchemaValidator(schema)
    assert v.validate_python(timedelta(hours=12)) == timedelta(hours=12)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-20>)

`TimedeltaSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-20>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(strict\)>)

Whether the value should be a timedelta or a value that can be converted to a timedelta

**`le`** : `timedelta` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(le\)>)

The value must be less than or equal to this timedelta

**`ge`** : `timedelta` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(ge\)>)

The value must be greater than or equal to this timedelta

**`lt`** : `timedelta` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(lt\)>)

The value must be strictly less than this timedelta

**`gt`** : `timedelta` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(gt\)>)

The value must be strictly greater than this timedelta

**`microseconds_precision`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘truncate’, ‘error’] _Default:_ `'truncate'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(microseconds_precision\)>)

The behavior when seconds have more than 6 digits or microseconds is too large

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.timedelta_schema\(serialization\)>)

Custom serialization schema

## literal_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.literal_schema>)
    
    def literal_schema(
        expected: list[Any],
        *,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> LiteralSchema
    
Returns a schema that matches a literal value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.literal_schema(['hello', 'world'])
    v = SchemaValidator(schema)
    assert v.validate_python('hello') == 'hello'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-21>)

`LiteralSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-21>)

**`expected`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.literal_schema\(expected\)>)

The value must be one of these values

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.literal_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.literal_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.literal_schema\(serialization\)>)

Custom serialization schema

## enum_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema>)
    
    def enum_schema(
        cls: Any,
        members: list[Any],
        *,
        sub_type: Literal['str', 'int', 'float'] | None = None,
        missing: Callable[[Any], Any] | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> EnumSchema
    
Returns a schema that matches an enum value, e.g.:
    
    from enum import Enum
    from pydantic_core import SchemaValidator, core_schema
    
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
    
    schema = core_schema.enum_schema(Color, list(Color.__members__.values()))
    v = SchemaValidator(schema)
    assert v.validate_python(2) is Color.GREEN
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-22>)

`EnumSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-22>)

**`cls`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(cls\)>)

The enum class

**`members`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(members\)>)

The members of the enum, generally `list(MyEnum.__members__.values())`

**`sub_type`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘str’, ‘int’, ‘float’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(sub_type\)>)

The type of the enum, either ‘str’ or ‘int’ or None for plain enums

**`missing`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(missing\)>)

A function to use when the value is not found in the enum, from `_missing_`

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(strict\)>)

Whether to use strict mode, defaults to False

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.enum_schema\(serialization\)>)

Custom serialization schema

## missing_sentinel_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.missing_sentinel_schema>)
    
    def missing_sentinel_schema(
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> MissingSentinelSchema
    
Returns a schema for the `MISSING` sentinel.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-23>)

`MissingSentinelSchema`

## is_instance_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_instance_schema>)
    
    def is_instance_schema(
        cls: Any,
        *,
        cls_repr: str | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> IsInstanceSchema
    
Returns a schema that checks if a value is an instance of a class, equivalent to python’s `isinstance` method, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    class A:
        pass
    
    schema = core_schema.is_instance_schema(cls=A)
    v = SchemaValidator(schema)
    v.validate_python(A())
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-24>)

`IsInstanceSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-23>)

**`cls`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_instance_schema\(cls\)>)

The value must be an instance of this class

**`cls_repr`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_instance_schema\(cls_repr\)>)

If provided this string is used in the validator name instead of `repr(cls)`

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_instance_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_instance_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_instance_schema\(serialization\)>)

Custom serialization schema

## is_subclass_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_subclass_schema>)
    
    def is_subclass_schema(
        cls: type[Any],
        *,
        cls_repr: str | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> IsInstanceSchema
    
Returns a schema that checks if a value is a subtype of a class, equivalent to python’s `issubclass` method, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    class A:
        pass
    
    class B(A):
        pass
    
    schema = core_schema.is_subclass_schema(cls=A)
    v = SchemaValidator(schema)
    v.validate_python(B)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-25>)

`IsInstanceSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-24>)

**`cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_subclass_schema\(cls\)>)

The value must be a subclass of this class

**`cls_repr`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_subclass_schema\(cls_repr\)>)

If provided this string is used in the validator name instead of `repr(cls)`

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_subclass_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_subclass_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.is_subclass_schema\(serialization\)>)

Custom serialization schema

## callable_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.callable_schema>)
    
    def callable_schema(
        *,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> CallableSchema
    
Returns a schema that checks if a value is callable, equivalent to python’s `callable` method, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.callable_schema()
    v = SchemaValidator(schema)
    v.validate_python(min)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-26>)

`CallableSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-25>)

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.callable_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.callable_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.callable_schema\(serialization\)>)

Custom serialization schema

## list_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema>)
    
    def list_schema(
        items_schema: CoreSchema | None = None,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        fail_fast: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: IncExSeqOrElseSerSchema | None = None,
    ) -> ListSchema
    
Returns a schema that matches a list value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.list_schema(core_schema.int_schema(), min_length=0, max_length=10)
    v = SchemaValidator(schema)
    assert v.validate_python(['4']) == [4]
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-27>)

`ListSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-26>)

**`items_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(items_schema\)>)

The value must be a list of items that match this schema

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(min_length\)>)

The value must be a list with at least this many items

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(max_length\)>)

The value must be a list with at most this many items

**`fail_fast`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(fail_fast\)>)

Stop validation on the first error

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(strict\)>)

The value must be a list with exactly this many items

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `IncExSeqOrElseSerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.list_schema\(serialization\)>)

Custom serialization schema

## tuple_positional_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_positional_schema>)
    
    def tuple_positional_schema(
        items_schema: list[CoreSchema],
        *,
        extras_schema: CoreSchema | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: IncExSeqOrElseSerSchema | None = None,
    ) -> TupleSchema
    
Returns a schema that matches a tuple of schemas, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.tuple_positional_schema(
        [core_schema.int_schema(), core_schema.str_schema()]
    )
    v = SchemaValidator(schema)
    assert v.validate_python((1, 'hello')) == (1, 'hello')
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-28>)

`TupleSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-27>)

**`items_schema`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`CoreSchema`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_positional_schema\(items_schema\)>)

The value must be a tuple with items that match these schemas

**`extras_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_positional_schema\(extras_schema\)>)

The value must be a tuple with items that match this schema This was inspired by JSON schema’s `prefixItems` and `items` fields. In python’s `typing.Tuple`, you can’t specify a type for “extra” items — they must all be the same type if the length is variable. So this field won’t be set from a `typing.Tuple` annotation on a pydantic model.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_positional_schema\(strict\)>)

The value must be a tuple with exactly this many items

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_positional_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_positional_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `IncExSeqOrElseSerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_positional_schema\(serialization\)>)

Custom serialization schema

## tuple_variable_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema>)
    
    def tuple_variable_schema(
        items_schema: CoreSchema | None = None,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: IncExSeqOrElseSerSchema | None = None,
    ) -> TupleSchema
    
Returns a schema that matches a tuple of a given schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.tuple_variable_schema(
        items_schema=core_schema.int_schema(), min_length=0, max_length=10
    )
    v = SchemaValidator(schema)
    assert v.validate_python(('1', 2, 3)) == (1, 2, 3)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-29>)

`TupleSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-28>)

**`items_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema\(items_schema\)>)

The value must be a tuple with items that match this schema

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema\(min_length\)>)

The value must be a tuple with at least this many items

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema\(max_length\)>)

The value must be a tuple with at most this many items

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema\(strict\)>)

The value must be a tuple with exactly this many items

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema\(ref\)>)

Optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `IncExSeqOrElseSerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_variable_schema\(serialization\)>)

Custom serialization schema

## tuple_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema>)
    
    def tuple_schema(
        items_schema: list[CoreSchema],
        *,
        variadic_item_index: int | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        fail_fast: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: IncExSeqOrElseSerSchema | None = None,
    ) -> TupleSchema
    
Returns a schema that matches a tuple of schemas, with an optional variadic item, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.tuple_schema(
        [core_schema.int_schema(), core_schema.str_schema(), core_schema.float_schema()],
        variadic_item_index=1,
    )
    v = SchemaValidator(schema)
    assert v.validate_python((1, 'hello', 'world', 1.5)) == (1, 'hello', 'world', 1.5)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-30>)

`TupleSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-29>)

**`items_schema`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`CoreSchema`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(items_schema\)>)

The value must be a tuple with items that match these schemas

**`variadic_item_index`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(variadic_item_index\)>)

The index of the schema in `items_schema` to be treated as variadic (following PEP 646)

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(min_length\)>)

The value must be a tuple with at least this many items

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(max_length\)>)

The value must be a tuple with at most this many items

**`fail_fast`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(fail_fast\)>)

Stop validation on the first error

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(strict\)>)

The value must be a tuple with exactly this many items

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(ref\)>)

Optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `IncExSeqOrElseSerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tuple_schema\(serialization\)>)

Custom serialization schema

## set_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema>)
    
    def set_schema(
        items_schema: CoreSchema | None = None,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        fail_fast: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> SetSchema
    
Returns a schema that matches a set of a given schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.set_schema(
        items_schema=core_schema.int_schema(), min_length=0, max_length=10
    )
    v = SchemaValidator(schema)
    assert v.validate_python({1, '2', 3}) == {1, 2, 3}
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-31>)

`SetSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-30>)

**`items_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(items_schema\)>)

The value must be a set with items that match this schema

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(min_length\)>)

The value must be a set with at least this many items

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(max_length\)>)

The value must be a set with at most this many items

**`fail_fast`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(fail_fast\)>)

Stop validation on the first error

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(strict\)>)

The value must be a set with exactly this many items

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.set_schema\(serialization\)>)

Custom serialization schema

## frozenset_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema>)
    
    def frozenset_schema(
        items_schema: CoreSchema | None = None,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        fail_fast: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> FrozenSetSchema
    
Returns a schema that matches a frozenset of a given schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.frozenset_schema(
        items_schema=core_schema.int_schema(), min_length=0, max_length=10
    )
    v = SchemaValidator(schema)
    assert v.validate_python(frozenset(range(3))) == frozenset({0, 1, 2})
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-32>)

`FrozenSetSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-31>)

**`items_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(items_schema\)>)

The value must be a frozenset with items that match this schema

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(min_length\)>)

The value must be a frozenset with at least this many items

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(max_length\)>)

The value must be a frozenset with at most this many items

**`fail_fast`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(fail_fast\)>)

Stop validation on the first error

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(strict\)>)

The value must be a frozenset with exactly this many items

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.frozenset_schema\(serialization\)>)

Custom serialization schema

## generator_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.generator_schema>)
    
    def generator_schema(
        items_schema: CoreSchema | None = None,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: IncExSeqOrElseSerSchema | None = None,
    ) -> GeneratorSchema
    
Returns a schema that matches a generator value, e.g.:
    
    from typing import Iterator
    from pydantic_core import SchemaValidator, core_schema
    
    def gen() -> Iterator[int]:
        yield 1
    
    schema = core_schema.generator_schema(items_schema=core_schema.int_schema())
    v = SchemaValidator(schema)
    v.validate_python(gen())
    
Unlike other types, validated generators do not raise ValidationErrors eagerly, but instead will raise a ValidationError when a violating value is actually read from the generator. This is to ensure that “validated” generators retain the benefit of lazy evaluation.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-33>)

`GeneratorSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-32>)

**`items_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.generator_schema\(items_schema\)>)

The value must be a generator with items that match this schema

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.generator_schema\(min_length\)>)

The value must be a generator that yields at least this many items

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.generator_schema\(max_length\)>)

The value must be a generator that yields at most this many items

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.generator_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.generator_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `IncExSeqOrElseSerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.generator_schema\(serialization\)>)

Custom serialization schema

## dict_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema>)
    
    def dict_schema(
        keys_schema: CoreSchema | None = None,
        values_schema: CoreSchema | None = None,
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        fail_fast: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> DictSchema
    
Returns a schema that matches a dict value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.dict_schema(
        keys_schema=core_schema.str_schema(), values_schema=core_schema.int_schema()
    )
    v = SchemaValidator(schema)
    assert v.validate_python({'a': '1', 'b': 2}) == {'a': 1, 'b': 2}
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-34>)

`DictSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-33>)

**`keys_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(keys_schema\)>)

The value must be a dict with keys that match this schema

**`values_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(values_schema\)>)

The value must be a dict with values that match this schema

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(min_length\)>)

The value must be a dict with at least this many items

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(max_length\)>)

The value must be a dict with at most this many items

**`fail_fast`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(fail_fast\)>)

Stop validation on the first error

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(strict\)>)

Whether the keys and values should be validated with strict mode

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dict_schema\(serialization\)>)

Custom serialization schema

## no_info_before_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_before_validator_function>)
    
    def no_info_before_validator_function(
        function: NoInfoValidatorFunction,
        schema: CoreSchema,
        *,
        ref: str | None = None,
        json_schema_input_schema: CoreSchema | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> BeforeValidatorFunctionSchema
    
Returns a schema that calls a validator function before validating, no `info` argument is provided, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: bytes) -> str:
        return v.decode() + 'world'
    
    func_schema = core_schema.no_info_before_validator_function(
        function=fn, schema=core_schema.str_schema()
    )
    schema = core_schema.typed_dict_schema({'a': core_schema.typed_dict_field(func_schema)})
    
    v = SchemaValidator(schema)
    assert v.validate_python({'a': b'hello '}) == {'a': 'hello world'}
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-35>)

`BeforeValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-34>)

**`function`** : `NoInfoValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_before_validator_function\(function\)>)

The validator function to call

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_before_validator_function\(schema\)>)

The schema to validate the output of the validator function

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_before_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`json_schema_input_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_before_validator_function\(json_schema_input_schema\)>)

The core schema to be used to generate the corresponding JSON Schema input type

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_before_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_before_validator_function\(serialization\)>)

Custom serialization schema

## with_info_before_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function>)
    
    def with_info_before_validator_function(
        function: WithInfoValidatorFunction,
        schema: CoreSchema,
        *,
        field_name: str | None = None,
        ref: str | None = None,
        json_schema_input_schema: CoreSchema | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> BeforeValidatorFunctionSchema
    
Returns a schema that calls a validator function before validation, the function is called with an `info` argument, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: bytes, info: core_schema.ValidationInfo) -> str:
        assert info.data is not None
        assert info.field_name is not None
        return v.decode() + 'world'
    
    func_schema = core_schema.with_info_before_validator_function(
        function=fn, schema=core_schema.str_schema()
    )
    schema = core_schema.typed_dict_schema({'a': core_schema.typed_dict_field(func_schema)})
    
    v = SchemaValidator(schema)
    assert v.validate_python({'a': b'hello '}) == {'a': 'hello world'}
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-36>)

`BeforeValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-35>)

**`function`** : `WithInfoValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function\(function\)>)

The validator function to call

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function\(field_name\)>)

The name of the field this validator is applied to, if any (deprecated)

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function\(schema\)>)

The schema to validate the output of the validator function

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`json_schema_input_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function\(json_schema_input_schema\)>)

The core schema to be used to generate the corresponding JSON Schema input type

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_before_validator_function\(serialization\)>)

Custom serialization schema

## no_info_after_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_after_validator_function>)
    
    def no_info_after_validator_function(
        function: NoInfoValidatorFunction,
        schema: CoreSchema,
        *,
        ref: str | None = None,
        json_schema_input_schema: CoreSchema | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> AfterValidatorFunctionSchema
    
Returns a schema that calls a validator function after validating, no `info` argument is provided, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: str) -> str:
        return v + 'world'
    
    func_schema = core_schema.no_info_after_validator_function(fn, core_schema.str_schema())
    schema = core_schema.typed_dict_schema({'a': core_schema.typed_dict_field(func_schema)})
    
    v = SchemaValidator(schema)
    assert v.validate_python({'a': b'hello '}) == {'a': 'hello world'}
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-37>)

`AfterValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-36>)

**`function`** : `NoInfoValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_after_validator_function\(function\)>)

The validator function to call after the schema is validated

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_after_validator_function\(schema\)>)

The schema to validate before the validator function

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_after_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`json_schema_input_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_after_validator_function\(json_schema_input_schema\)>)

The core schema to be used to generate the corresponding JSON Schema input type

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_after_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_after_validator_function\(serialization\)>)

Custom serialization schema

## with_info_after_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_after_validator_function>)
    
    def with_info_after_validator_function(
        function: WithInfoValidatorFunction,
        schema: CoreSchema,
        *,
        field_name: str | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> AfterValidatorFunctionSchema
    
Returns a schema that calls a validator function after validation, the function is called with an `info` argument, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: str, info: core_schema.ValidationInfo) -> str:
        assert info.data is not None
        assert info.field_name is not None
        return v + 'world'
    
    func_schema = core_schema.with_info_after_validator_function(
        function=fn, schema=core_schema.str_schema()
    )
    schema = core_schema.typed_dict_schema({'a': core_schema.typed_dict_field(func_schema)})
    
    v = SchemaValidator(schema)
    assert v.validate_python({'a': b'hello '}) == {'a': 'hello world'}
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-38>)

`AfterValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-37>)

**`function`** : `WithInfoValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_after_validator_function\(function\)>)

The validator function to call after the schema is validated

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_after_validator_function\(schema\)>)

The schema to validate before the validator function

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_after_validator_function\(field_name\)>)

The name of the field this validator is applied to, if any (deprecated)

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_after_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_after_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_after_validator_function\(serialization\)>)

Custom serialization schema

## no_info_wrap_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_wrap_validator_function>)
    
    def no_info_wrap_validator_function(
        function: NoInfoWrapValidatorFunction,
        schema: CoreSchema,
        *,
        ref: str | None = None,
        json_schema_input_schema: CoreSchema | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> WrapValidatorFunctionSchema
    
Returns a schema which calls a function with a `validator` callable argument which can optionally be used to call inner validation with the function logic, this is much like the “onion” implementation of middleware in many popular web frameworks, no `info` argument is passed, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(
        v: str,
        validator: core_schema.ValidatorFunctionWrapHandler,
    ) -> str:
        return validator(input_value=v) + 'world'
    
    schema = core_schema.no_info_wrap_validator_function(
        function=fn, schema=core_schema.str_schema()
    )
    v = SchemaValidator(schema)
    assert v.validate_python('hello ') == 'hello world'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-39>)

`WrapValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-38>)

**`function`** : `NoInfoWrapValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_wrap_validator_function\(function\)>)

The validator function to call

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_wrap_validator_function\(schema\)>)

The schema to validate the output of the validator function

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_wrap_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`json_schema_input_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_wrap_validator_function\(json_schema_input_schema\)>)

The core schema to be used to generate the corresponding JSON Schema input type

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_wrap_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_wrap_validator_function\(serialization\)>)

Custom serialization schema

## with_info_wrap_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function>)
    
    def with_info_wrap_validator_function(
        function: WithInfoWrapValidatorFunction,
        schema: CoreSchema,
        *,
        field_name: str | None = None,
        json_schema_input_schema: CoreSchema | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> WrapValidatorFunctionSchema
    
Returns a schema which calls a function with a `validator` callable argument which can optionally be used to call inner validation with the function logic, this is much like the “onion” implementation of middleware in many popular web frameworks, an `info` argument is also passed, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(
        v: str,
        validator: core_schema.ValidatorFunctionWrapHandler,
        info: core_schema.ValidationInfo,
    ) -> str:
        return validator(input_value=v) + 'world'
    
    schema = core_schema.with_info_wrap_validator_function(
        function=fn, schema=core_schema.str_schema()
    )
    v = SchemaValidator(schema)
    assert v.validate_python('hello ') == 'hello world'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-40>)

`WrapValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-39>)

**`function`** : `WithInfoWrapValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function\(function\)>)

The validator function to call

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function\(schema\)>)

The schema to validate the output of the validator function

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function\(field_name\)>)

The name of the field this validator is applied to, if any (deprecated)

**`json_schema_input_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function\(json_schema_input_schema\)>)

The core schema to be used to generate the corresponding JSON Schema input type

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_wrap_validator_function\(serialization\)>)

Custom serialization schema

## no_info_plain_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_plain_validator_function>)
    
    def no_info_plain_validator_function(
        function: NoInfoValidatorFunction,
        *,
        ref: str | None = None,
        json_schema_input_schema: CoreSchema | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> PlainValidatorFunctionSchema
    
Returns a schema that uses the provided function for validation, no `info` argument is passed, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: str) -> str:
        assert 'hello' in v
        return v + 'world'
    
    schema = core_schema.no_info_plain_validator_function(function=fn)
    v = SchemaValidator(schema)
    assert v.validate_python('hello ') == 'hello world'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-41>)

`PlainValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-40>)

**`function`** : `NoInfoValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_plain_validator_function\(function\)>)

The validator function to call

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_plain_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`json_schema_input_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_plain_validator_function\(json_schema_input_schema\)>)

The core schema to be used to generate the corresponding JSON Schema input type

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_plain_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.no_info_plain_validator_function\(serialization\)>)

Custom serialization schema

## with_info_plain_validator_function 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_plain_validator_function>)
    
    def with_info_plain_validator_function(
        function: WithInfoValidatorFunction,
        *,
        field_name: str | None = None,
        ref: str | None = None,
        json_schema_input_schema: CoreSchema | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> PlainValidatorFunctionSchema
    
Returns a schema that uses the provided function for validation, an `info` argument is passed, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: str, info: core_schema.ValidationInfo) -> str:
        assert 'hello' in v
        return v + 'world'
    
    schema = core_schema.with_info_plain_validator_function(function=fn)
    v = SchemaValidator(schema)
    assert v.validate_python('hello ') == 'hello world'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-42>)

`PlainValidatorFunctionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-41>)

**`function`** : `WithInfoValidatorFunction`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_plain_validator_function\(function\)>)

The validator function to call

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_plain_validator_function\(field_name\)>)

The name of the field this validator is applied to, if any (deprecated)

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_plain_validator_function\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`json_schema_input_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_plain_validator_function\(json_schema_input_schema\)>)

The core schema to be used to generate the corresponding JSON Schema input type

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_plain_validator_function\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_info_plain_validator_function\(serialization\)>)

Custom serialization schema

## with_default_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema>)
    
    def with_default_schema(
        schema: CoreSchema,
        *,
        default: Any = PydanticUndefined,
        default_factory: Union[Callable[[], Any], Callable[[dict[str, Any]], Any], None] = None,
        default_factory_takes_data: bool | None = None,
        on_error: Literal['raise', 'omit', 'default'] | None = None,
        validate_default: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> WithDefaultSchema
    
Returns a schema that adds a default value to the given schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.with_default_schema(core_schema.str_schema(), default='hello')
    wrapper_schema = core_schema.typed_dict_schema(
        {'a': core_schema.typed_dict_field(schema)}
    )
    v = SchemaValidator(wrapper_schema)
    assert v.validate_python({}) == v.validate_python({'a': 'hello'})
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-43>)

`WithDefaultSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-42>)

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(schema\)>)

The schema to add a default value to

**`default`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `PydanticUndefined`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(default\)>)

The default value to use

**`default_factory`** : [`Union`](<https://docs.python.org/3/library/typing.html#typing.Union>)[[`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`None`](<https://docs.python.org/3/library/constants.html#None>)] _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(default_factory\)>)

A callable that returns the default value to use

**`default_factory_takes_data`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(default_factory_takes_data\)>)

Whether the default factory takes a validated data argument

**`on_error`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘raise’, ‘omit’, ‘default’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(on_error\)>)

What to do if the schema validation fails. One of ‘raise’, ‘omit’, ‘default’

**`validate_default`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(validate_default\)>)

Whether the default value should be validated

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(strict\)>)

Whether the underlying schema should be validated with strict mode

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.with_default_schema\(serialization\)>)

Custom serialization schema

## nullable_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.nullable_schema>)
    
    def nullable_schema(
        schema: CoreSchema,
        *,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> NullableSchema
    
Returns a schema that matches a nullable value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.nullable_schema(core_schema.str_schema())
    v = SchemaValidator(schema)
    assert v.validate_python(None) is None
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-44>)

`NullableSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-43>)

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.nullable_schema\(schema\)>)

The schema to wrap

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.nullable_schema\(strict\)>)

Whether the underlying schema should be validated with strict mode

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.nullable_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.nullable_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.nullable_schema\(serialization\)>)

Custom serialization schema

## union_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema>)
    
    def union_schema(
        choices: list[CoreSchema | tuple[CoreSchema, str]],
        *,
        auto_collapse: bool | None = None,
        custom_error_type: str | None = None,
        custom_error_message: str | None = None,
        custom_error_context: dict[str, str | int] | None = None,
        mode: Literal['smart', 'left_to_right'] | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> UnionSchema
    
Returns a schema that matches a union value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.union_schema([core_schema.str_schema(), core_schema.int_schema()])
    v = SchemaValidator(schema)
    assert v.validate_python('hello') == 'hello'
    assert v.validate_python(1) == 1
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-45>)

`UnionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-44>)

**`choices`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`CoreSchema` | [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[`CoreSchema`, [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(choices\)>)

The schemas to match. If a tuple, the second item is used as the label for the case.

**`auto_collapse`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(auto_collapse\)>)

whether to automatically collapse unions with one element to the inner validator, default true

**`custom_error_type`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(custom_error_type\)>)

The custom error type to use if the validation fails

**`custom_error_message`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(custom_error_message\)>)

The custom error message to use if the validation fails

**`custom_error_context`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(custom_error_context\)>)

The custom error context to use if the validation fails

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘smart’, ‘left_to_right’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(mode\)>)

How to select which choice to return

  * `smart` (default) will try to return the choice which is the closest match to the input value
  * `left_to_right` will return the first choice in `choices` which succeeds validation

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.union_schema\(serialization\)>)

Custom serialization schema

## tagged_union_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema>)
    
    def tagged_union_schema(
        choices: dict[Any, CoreSchema],
        discriminator: str | list[str | int] | list[list[str | int]] | Callable[[Any], Any],
        *,
        custom_error_type: str | None = None,
        custom_error_message: str | None = None,
        custom_error_context: dict[str, int | str | float] | None = None,
        strict: bool | None = None,
        from_attributes: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> TaggedUnionSchema
    
Returns a schema that matches a tagged union value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    apple_schema = core_schema.typed_dict_schema(
        {
            'foo': core_schema.typed_dict_field(core_schema.str_schema()),
            'bar': core_schema.typed_dict_field(core_schema.int_schema()),
        }
    )
    banana_schema = core_schema.typed_dict_schema(
        {
            'foo': core_schema.typed_dict_field(core_schema.str_schema()),
            'spam': core_schema.typed_dict_field(
                core_schema.list_schema(items_schema=core_schema.int_schema())
            ),
        }
    )
    schema = core_schema.tagged_union_schema(
        choices={
            'apple': apple_schema,
            'banana': banana_schema,
        },
        discriminator='foo',
    )
    v = SchemaValidator(schema)
    assert v.validate_python({'foo': 'apple', 'bar': '123'}) == {'foo': 'apple', 'bar': 123}
    assert v.validate_python({'foo': 'banana', 'spam': [1, 2, 3]}) == {
        'foo': 'banana',
        'spam': [1, 2, 3],
    }
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-46>)

`TaggedUnionSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-45>)

**`choices`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>), `CoreSchema`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(choices\)>)

The schemas to match When retrieving a schema from `choices` using the discriminator value, if the value is a str, it should be fed back into the `choices` map until a schema is obtained (This approach is to prevent multiple ownership of a single schema in Rust)

**`discriminator`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)] | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)]] | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(discriminator\)>)

The discriminator to use to determine the schema to use

  * If `discriminator` is a str, it is the name of the attribute to use as the discriminator
  * If `discriminator` is a list of int/str, it should be used as a “path” to access the discriminator
  * If `discriminator` is a list of lists, each inner list is a path, and the first path that exists is used
  * If `discriminator` is a callable, it should return the discriminator when called on the value to validate; the callable can return `None` to indicate that there is no matching discriminator present on the input

**`custom_error_type`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(custom_error_type\)>)

The custom error type to use if the validation fails

**`custom_error_message`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(custom_error_message\)>)

The custom error message to use if the validation fails

**`custom_error_context`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`float`](<https://docs.python.org/3/library/functions.html#float>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(custom_error_context\)>)

The custom error context to use if the validation fails

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(strict\)>)

Whether the underlying schemas should be validated with strict mode

**`from_attributes`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(from_attributes\)>)

Whether to use the attributes of the object to retrieve the discriminator value

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.tagged_union_schema\(serialization\)>)

Custom serialization schema

## chain_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.chain_schema>)
    
    def chain_schema(
        steps: list[CoreSchema],
        *,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> ChainSchema
    
Returns a schema that chains the provided validation schemas, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: str, info: core_schema.ValidationInfo) -> str:
        assert 'hello' in v
        return v + ' world'
    
    fn_schema = core_schema.with_info_plain_validator_function(function=fn)
    schema = core_schema.chain_schema(
        [fn_schema, fn_schema, fn_schema, core_schema.str_schema()]
    )
    v = SchemaValidator(schema)
    assert v.validate_python('hello') == 'hello world world world'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-47>)

`ChainSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-46>)

**`steps`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`CoreSchema`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.chain_schema\(steps\)>)

The schemas to chain

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.chain_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.chain_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.chain_schema\(serialization\)>)

Custom serialization schema

## lax_or_strict_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.lax_or_strict_schema>)
    
    def lax_or_strict_schema(
        lax_schema: CoreSchema,
        strict_schema: CoreSchema,
        *,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> LaxOrStrictSchema
    
Returns a schema that uses the lax or strict schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    def fn(v: str, info: core_schema.ValidationInfo) -> str:
        assert 'hello' in v
        return v + ' world'
    
    lax_schema = core_schema.int_schema(strict=False)
    strict_schema = core_schema.int_schema(strict=True)
    
    schema = core_schema.lax_or_strict_schema(
        lax_schema=lax_schema, strict_schema=strict_schema, strict=True
    )
    v = SchemaValidator(schema)
    assert v.validate_python(123) == 123
    
    schema = core_schema.lax_or_strict_schema(
        lax_schema=lax_schema, strict_schema=strict_schema, strict=False
    )
    v = SchemaValidator(schema)
    assert v.validate_python('123') == 123
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-48>)

`LaxOrStrictSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-47>)

**`lax_schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.lax_or_strict_schema\(lax_schema\)>)

The lax schema to use

**`strict_schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.lax_or_strict_schema\(strict_schema\)>)

The strict schema to use

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.lax_or_strict_schema\(strict\)>)

Whether the strict schema should be used

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.lax_or_strict_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.lax_or_strict_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.lax_or_strict_schema\(serialization\)>)

Custom serialization schema

## json_or_python_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_or_python_schema>)
    
    def json_or_python_schema(
        json_schema: CoreSchema,
        python_schema: CoreSchema,
        *,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> JsonOrPythonSchema
    
Returns a schema that uses the Json or Python schema depending on the input:
    
    from pydantic_core import SchemaValidator, ValidationError, core_schema
    
    v = SchemaValidator(
        core_schema.json_or_python_schema(
            json_schema=core_schema.int_schema(),
            python_schema=core_schema.int_schema(strict=True),
        )
    )
    
    assert v.validate_json('"123"') == 123
    
    try:
        v.validate_python('123')
    except ValidationError:
        pass
    else:
        raise AssertionError('Validation should have failed')
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-49>)

`JsonOrPythonSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-48>)

**`json_schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_or_python_schema\(json_schema\)>)

The schema to use for Json inputs

**`python_schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_or_python_schema\(python_schema\)>)

The schema to use for Python inputs

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_or_python_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_or_python_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_or_python_schema\(serialization\)>)

Custom serialization schema

## typed_dict_field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field>)
    
    def typed_dict_field(
        schema: CoreSchema,
        *,
        required: bool | None = None,
        validation_alias: str | list[str | int] | list[list[str | int]] | None = None,
        serialization_alias: str | None = None,
        serialization_exclude: bool | None = None,
        metadata: dict[str, Any] | None = None,
        serialization_exclude_if: Callable[[Any], bool] | None = None,
    ) -> TypedDictField
    
Returns a schema that matches a typed dict field, e.g.:
    
    from pydantic_core import core_schema
    
    field = core_schema.typed_dict_field(schema=core_schema.int_schema(), required=True)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-50>)

`TypedDictField`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-49>)

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field\(schema\)>)

The schema to use for the field

**`required`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field\(required\)>)

Whether the field is required, otherwise uses the value from `total` on the typed dict

**`validation_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)] | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field\(validation_alias\)>)

The alias(es) to use to find the field in the validation data

**`serialization_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field\(serialization_alias\)>)

The alias to use as a key when serializing

**`serialization_exclude`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field\(serialization_exclude\)>)

Whether to exclude the field when serializing

**`serialization_exclude_if`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field\(serialization_exclude_if\)>)

A callable that determines whether to exclude the field when serializing based on its value.

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_field\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

## typed_dict_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema>)
    
    def typed_dict_schema(
        fields: dict[str, TypedDictField],
        *,
        cls: type[Any] | None = None,
        cls_name: str | None = None,
        computed_fields: list[ComputedField] | None = None,
        strict: bool | None = None,
        extras_schema: CoreSchema | None = None,
        extra_behavior: ExtraBehavior | None = None,
        total: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
        config: CoreConfig | None = None,
    ) -> TypedDictSchema
    
Returns a schema that matches a typed dict, e.g.:
    
    from typing_extensions import TypedDict
    
    from pydantic_core import SchemaValidator, core_schema
    
    class MyTypedDict(TypedDict):
        a: str
    
    wrapper_schema = core_schema.typed_dict_schema(
        {'a': core_schema.typed_dict_field(core_schema.str_schema())}, cls=MyTypedDict
    )
    v = SchemaValidator(wrapper_schema)
    assert v.validate_python({'a': 'hello'}) == {'a': 'hello'}
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-51>)

`TypedDictSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-50>)

**`fields`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `TypedDictField`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(fields\)>)

The fields to use for the typed dict

**`cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(cls\)>)

The class to use for the typed dict

**`cls_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(cls_name\)>)

The name to use in error locations. Falls back to `cls.__name__`, or the validator name if no class is provided.

**`computed_fields`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`ComputedField`] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(computed_fields\)>)

Computed fields to use when serializing the model, only applies when directly inside a model

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(strict\)>)

Whether the typed dict is strict

**`extras_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(extras_schema\)>)

The extra validator to use for the typed dict

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`extra_behavior`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(extra_behavior\)>)

The extra behavior to use for the typed dict

**`total`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(total\)>)

Whether the typed dict is total, otherwise uses `typed_dict_total` from config

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema\(serialization\)>)

Custom serialization schema

## model_field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field>)
    
    def model_field(
        schema: CoreSchema,
        *,
        validation_alias: str | list[str | int] | list[list[str | int]] | None = None,
        serialization_alias: str | None = None,
        serialization_exclude: bool | None = None,
        serialization_exclude_if: Callable[[Any], bool] | None = None,
        frozen: bool | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> ModelField
    
Returns a schema for a model field, e.g.:
    
    from pydantic_core import core_schema
    
    field = core_schema.model_field(schema=core_schema.int_schema())
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-52>)

`ModelField`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-51>)

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field\(schema\)>)

The schema to use for the field

**`validation_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)] | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field\(validation_alias\)>)

The alias(es) to use to find the field in the validation data

**`serialization_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field\(serialization_alias\)>)

The alias to use as a key when serializing

**`serialization_exclude`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field\(serialization_exclude\)>)

Whether to exclude the field when serializing

**`serialization_exclude_if`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field\(serialization_exclude_if\)>)

A Callable that determines whether to exclude a field during serialization based on its value.

**`frozen`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field\(frozen\)>)

Whether the field is frozen

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_field\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

## model_fields_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema>)
    
    def model_fields_schema(
        fields: dict[str, ModelField],
        *,
        model_name: str | None = None,
        computed_fields: list[ComputedField] | None = None,
        strict: bool | None = None,
        extras_schema: CoreSchema | None = None,
        extras_keys_schema: CoreSchema | None = None,
        extra_behavior: ExtraBehavior | None = None,
        from_attributes: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> ModelFieldsSchema
    
Returns a schema that matches the fields of a Pydantic model, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    wrapper_schema = core_schema.model_fields_schema(
        {'a': core_schema.model_field(core_schema.str_schema())}
    )
    v = SchemaValidator(wrapper_schema)
    print(v.validate_python({'a': 'hello'}))
    #> ({'a': 'hello'}, None, {'a'})
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-53>)

`ModelFieldsSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-52>)

**`fields`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `ModelField`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(fields\)>)

The fields of the model

**`model_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(model_name\)>)

The name of the model, used for error messages, defaults to “Model”

**`computed_fields`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`ComputedField`] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(computed_fields\)>)

Computed fields to use when serializing the model, only applies when directly inside a model

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(strict\)>)

Whether the model is strict

**`extras_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(extras_schema\)>)

The schema to use when validating extra input data

**`extras_keys_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(extras_keys_schema\)>)

The schema to use when validating the keys of extra input data

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`extra_behavior`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(extra_behavior\)>)

The extra behavior to use for the model fields

**`from_attributes`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(from_attributes\)>)

Whether the model fields should be populated from attributes

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_fields_schema\(serialization\)>)

Custom serialization schema

## model_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema>)
    
    def model_schema(
        cls: type[Any],
        schema: CoreSchema,
        *,
        generic_origin: type[Any] | None = None,
        custom_init: bool | None = None,
        root_model: bool | None = None,
        post_init: str | None = None,
        revalidate_instances: Literal['always', 'never', 'subclass-instances'] | None = None,
        strict: bool | None = None,
        frozen: bool | None = None,
        extra_behavior: ExtraBehavior | None = None,
        config: CoreConfig | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> ModelSchema
    
A model schema generally contains a typed-dict schema. It will run the typed dict validator, then create a new class and set the dict and fields set returned from the typed dict validator to `__dict__` and `__pydantic_fields_set__` respectively.

Example:
    
    from pydantic_core import CoreConfig, SchemaValidator, core_schema
    
    class MyModel:
        __slots__ = (
            '__dict__',
            '__pydantic_fields_set__',
            '__pydantic_extra__',
            '__pydantic_private__',
        )
    
    schema = core_schema.model_schema(
        cls=MyModel,
        config=CoreConfig(str_max_length=5),
        schema=core_schema.model_fields_schema(
            fields={'a': core_schema.model_field(core_schema.str_schema())},
        ),
    )
    v = SchemaValidator(schema)
    assert v.isinstance_python({'a': 'hello'}) is True
    assert v.isinstance_python({'a': 'too long'}) is False
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-54>)

`ModelSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-53>)

**`cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(cls\)>)

The class to use for the model

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(schema\)>)

The schema to use for the model

**`generic_origin`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(generic_origin\)>)

The origin type used for this model, if it’s a parametrized generic. Ex, if this model schema represents `SomeModel[int]`, generic_origin is `SomeModel`

**`custom_init`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(custom_init\)>)

Whether the model has a custom init method

**`root_model`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(root_model\)>)

Whether the model is a `RootModel`

**`post_init`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(post_init\)>)

The call after init to use for the model

**`revalidate_instances`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘always’, ‘never’, ‘subclass-instances’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(revalidate_instances\)>)

whether instances of models and dataclasses (including subclass instances) should re-validate defaults to config.revalidate_instances, else ‘never’

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(strict\)>)

Whether the model is strict

**`frozen`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(frozen\)>)

Whether the model is frozen

**`extra_behavior`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(extra_behavior\)>)

The extra behavior to use for the model, used in serialization

**`config`** : `CoreConfig` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(config\)>)

The config to use for the model

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.model_schema\(serialization\)>)

Custom serialization schema

## dataclass_field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field>)
    
    def dataclass_field(
        name: str,
        schema: CoreSchema,
        *,
        kw_only: bool | None = None,
        init: bool | None = None,
        init_only: bool | None = None,
        validation_alias: str | list[str | int] | list[list[str | int]] | None = None,
        serialization_alias: str | None = None,
        serialization_exclude: bool | None = None,
        metadata: dict[str, Any] | None = None,
        serialization_exclude_if: Callable[[Any], bool] | None = None,
        frozen: bool | None = None,
    ) -> DataclassField
    
Returns a schema for a dataclass field, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    field = core_schema.dataclass_field(
        name='a', schema=core_schema.str_schema(), kw_only=False
    )
    schema = core_schema.dataclass_args_schema('Foobar', [field])
    v = SchemaValidator(schema)
    assert v.validate_python({'a': 'hello'}) == ({'a': 'hello'}, None)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-55>)

`DataclassField`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-54>)

**`name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(name\)>)

The name to use for the argument parameter

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(schema\)>)

The schema to use for the argument parameter

**`kw_only`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(kw_only\)>)

Whether the field can be set with a positional argument as well as a keyword argument

**`init`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(init\)>)

Whether the field should be validated during initialization

**`init_only`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(init_only\)>)

Whether the field should be omitted from `__dict__` and passed to `__post_init__`

**`validation_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)] | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(validation_alias\)>)

The alias(es) to use to find the field in the validation data

**`serialization_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(serialization_alias\)>)

The alias to use as a key when serializing

**`serialization_exclude`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(serialization_exclude\)>)

Whether to exclude the field when serializing

**`serialization_exclude_if`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(serialization_exclude_if\)>)

A callable that determines whether to exclude the field when serializing based on its value.

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`frozen`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_field\(frozen\)>)

Whether the field is frozen

## dataclass_args_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema>)
    
    def dataclass_args_schema(
        dataclass_name: str,
        fields: list[DataclassField],
        *,
        computed_fields: list[ComputedField] | None = None,
        collect_init_only: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
        extra_behavior: ExtraBehavior | None = None,
    ) -> DataclassArgsSchema
    
Returns a schema for validating dataclass arguments, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    field_a = core_schema.dataclass_field(
        name='a', schema=core_schema.str_schema(), kw_only=False
    )
    field_b = core_schema.dataclass_field(
        name='b', schema=core_schema.bool_schema(), kw_only=False
    )
    schema = core_schema.dataclass_args_schema('Foobar', [field_a, field_b])
    v = SchemaValidator(schema)
    assert v.validate_python({'a': 'hello', 'b': True}) == ({'a': 'hello', 'b': True}, None)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-56>)

`DataclassArgsSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-55>)

**`dataclass_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(dataclass_name\)>)

The name of the dataclass being validated

**`fields`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`DataclassField`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(fields\)>)

The fields to use for the dataclass

**`computed_fields`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`ComputedField`] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(computed_fields\)>)

Computed fields to use when serializing the dataclass

**`collect_init_only`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(collect_init_only\)>)

Whether to collect init only fields into a dict to pass to `__post_init__`

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(serialization\)>)

Custom serialization schema

**`extra_behavior`** : `ExtraBehavior` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_args_schema\(extra_behavior\)>)

How to handle extra fields

## dataclass_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema>)
    
    def dataclass_schema(
        cls: type[Any],
        schema: CoreSchema,
        fields: list[str],
        *,
        generic_origin: type[Any] | None = None,
        cls_name: str | None = None,
        post_init: bool | None = None,
        revalidate_instances: Literal['always', 'never', 'subclass-instances'] | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
        frozen: bool | None = None,
        slots: bool | None = None,
        config: CoreConfig | None = None,
    ) -> DataclassSchema
    
Returns a schema for a dataclass. As with `ModelSchema`, this schema can only be used as a field within another schema, not as the root type.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-57>)

`DataclassSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-56>)

**`cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(cls\)>)

The dataclass type, used to perform subclass checks

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(schema\)>)

The schema to use for the dataclass fields

**`fields`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(fields\)>)

Fields of the dataclass, this is used in serialization and in validation during re-validation and while validating assignment

**`generic_origin`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(generic_origin\)>)

The origin type used for this dataclass, if it’s a parametrized generic. Ex, if this model schema represents `SomeDataclass[int]`, generic_origin is `SomeDataclass`

**`cls_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(cls_name\)>)

The name to use in error locs, etc; this is useful for generics (default: `cls.__name__`)

**`post_init`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(post_init\)>)

Whether to call `__post_init__` after validation

**`revalidate_instances`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘always’, ‘never’, ‘subclass-instances’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(revalidate_instances\)>)

whether instances of models and dataclasses (including subclass instances) should re-validate defaults to config.revalidate_instances, else ‘never’

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(strict\)>)

Whether to require an exact instance of `cls`

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(serialization\)>)

Custom serialization schema

**`frozen`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(frozen\)>)

Whether the dataclass is frozen

**`slots`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.dataclass_schema\(slots\)>)

Whether `slots=True` on the dataclass, means each field is assigned independently, rather than simply setting `__dict__`, default false

## arguments_parameter 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_parameter>)
    
    def arguments_parameter(
        name: str,
        schema: CoreSchema,
        *,
        mode: Literal['positional_only', 'positional_or_keyword', 'keyword_only'] | None = None,
        alias: str | list[str | int] | list[list[str | int]] | None = None,
    ) -> ArgumentsParameter
    
Returns a schema that matches an argument parameter, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    param = core_schema.arguments_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    schema = core_schema.arguments_schema([param])
    v = SchemaValidator(schema)
    assert v.validate_python(('hello',)) == (('hello',), {})
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-58>)

`ArgumentsParameter`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-57>)

**`name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_parameter\(name\)>)

The name to use for the argument parameter

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_parameter\(schema\)>)

The schema to use for the argument parameter

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘positional_only’, ‘positional_or_keyword’, ‘keyword_only’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_parameter\(mode\)>)

The mode to use for the argument parameter

**`alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)] | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_parameter\(alias\)>)

The alias to use for the argument parameter

## arguments_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema>)
    
    def arguments_schema(
        arguments: list[ArgumentsParameter],
        *,
        validate_by_name: bool | None = None,
        validate_by_alias: bool | None = None,
        var_args_schema: CoreSchema | None = None,
        var_kwargs_mode: VarKwargsMode | None = None,
        var_kwargs_schema: CoreSchema | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> ArgumentsSchema
    
Returns a schema that matches an arguments schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    param_a = core_schema.arguments_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    param_b = core_schema.arguments_parameter(
        name='b', schema=core_schema.bool_schema(), mode='positional_only'
    )
    schema = core_schema.arguments_schema([param_a, param_b])
    v = SchemaValidator(schema)
    assert v.validate_python(('hello', True)) == (('hello', True), {})
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-59>)

`ArgumentsSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-58>)

**`arguments`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`ArgumentsParameter`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(arguments\)>)

The arguments to use for the arguments schema

**`validate_by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(validate_by_name\)>)

Whether to populate by the parameter names, defaults to `False`.

**`validate_by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(validate_by_alias\)>)

Whether to populate by the parameter aliases, defaults to `True`.

**`var_args_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(var_args_schema\)>)

The variable args schema to use for the arguments schema

**`var_kwargs_mode`** : `VarKwargsMode` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(var_kwargs_mode\)>)

The validation mode to use for variadic keyword arguments. If `'uniform'`, every value of the keyword arguments will be validated against the `var_kwargs_schema` schema. If `'unpacked-typed-dict'`, the `var_kwargs_schema` argument must be a [`typed_dict_schema`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.typed_dict_schema>)

**`var_kwargs_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(var_kwargs_schema\)>)

The variable kwargs schema to use for the arguments schema

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_schema\(serialization\)>)

Custom serialization schema

## arguments_v3_parameter 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_parameter>)
    
    def arguments_v3_parameter(
        name: str,
        schema: CoreSchema,
        *,
        mode: Literal['positional_only', 'positional_or_keyword', 'keyword_only', 'var_args', 'var_kwargs_uniform', 'var_kwargs_unpacked_typed_dict'] | None = None,
        alias: str | list[str | int] | list[list[str | int]] | None = None,
    ) -> ArgumentsV3Parameter
    
Returns a schema that matches an argument parameter, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    param = core_schema.arguments_v3_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    schema = core_schema.arguments_v3_schema([param])
    v = SchemaValidator(schema)
    assert v.validate_python({'a': 'hello'}) == (('hello',), {})
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-60>)

`ArgumentsV3Parameter`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-59>)

**`name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_parameter\(name\)>)

The name to use for the argument parameter

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_parameter\(schema\)>)

The schema to use for the argument parameter

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘positional_only’, ‘positional_or_keyword’, ‘keyword_only’, ‘var_args’, ‘var_kwargs_uniform’, ‘var_kwargs_unpacked_typed_dict’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_parameter\(mode\)>)

The mode to use for the argument parameter

**`alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)] | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`int`](<https://docs.python.org/3/library/functions.html#int>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_parameter\(alias\)>)

The alias to use for the argument parameter

## arguments_v3_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema>)
    
    def arguments_v3_schema(
        arguments: list[ArgumentsV3Parameter],
        *,
        validate_by_name: bool | None = None,
        validate_by_alias: bool | None = None,
        extra_behavior: Literal['forbid', 'ignore'] | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> ArgumentsV3Schema
    
Returns a schema that matches an arguments schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    param_a = core_schema.arguments_v3_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    param_b = core_schema.arguments_v3_parameter(
        name='kwargs', schema=core_schema.bool_schema(), mode='var_kwargs_uniform'
    )
    schema = core_schema.arguments_v3_schema([param_a, param_b])
    v = SchemaValidator(schema)
    assert v.validate_python({'a': 'hi', 'kwargs': {'b': True}}) == (('hi',), {'b': True})
    
This schema is currently not used by other Pydantic components. In V3, it will most likely become the default arguments schema for the `'call'` schema.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-61>)

`ArgumentsV3Schema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-60>)

**`arguments`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`ArgumentsV3Parameter`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema\(arguments\)>)

The arguments to use for the arguments schema.

**`validate_by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema\(validate_by_name\)>)

Whether to populate by the parameter names, defaults to `False`.

**`validate_by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema\(validate_by_alias\)>)

Whether to populate by the parameter aliases, defaults to `True`.

**`extra_behavior`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘forbid’, ‘ignore’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema\(extra_behavior\)>)

The extra behavior to use.

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places.

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core.

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.arguments_v3_schema\(serialization\)>)

Custom serialization schema.

## call_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema>)
    
    def call_schema(
        arguments: CoreSchema,
        function: Callable[..., Any],
        *,
        function_name: str | None = None,
        return_schema: CoreSchema | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> CallSchema
    
Returns a schema that matches an arguments schema, then calls a function, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    param_a = core_schema.arguments_parameter(
        name='a', schema=core_schema.str_schema(), mode='positional_only'
    )
    param_b = core_schema.arguments_parameter(
        name='b', schema=core_schema.bool_schema(), mode='positional_only'
    )
    args_schema = core_schema.arguments_schema([param_a, param_b])
    
    schema = core_schema.call_schema(
        arguments=args_schema,
        function=lambda a, b: a + str(not b),
        return_schema=core_schema.str_schema(),
    )
    v = SchemaValidator(schema)
    assert v.validate_python((('hello', True))) == 'helloFalse'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-62>)

`CallSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-61>)

**`arguments`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema\(arguments\)>)

The arguments to use for the arguments schema

**`function`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema\(function\)>)

The function to use for the call schema

**`function_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema\(function_name\)>)

The function name to use for the call schema, if not provided `function.__name__` is used

**`return_schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema\(return_schema\)>)

The return schema to use for the call schema

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.call_schema\(serialization\)>)

Custom serialization schema

## custom_error_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema>)
    
    def custom_error_schema(
        schema: CoreSchema,
        custom_error_type: str,
        *,
        custom_error_message: str | None = None,
        custom_error_context: dict[str, Any] | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> CustomErrorSchema
    
Returns a schema that matches a custom error value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.custom_error_schema(
        schema=core_schema.int_schema(),
        custom_error_type='MyError',
        custom_error_message='Error msg',
    )
    v = SchemaValidator(schema)
    v.validate_python(1)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-63>)

`CustomErrorSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-62>)

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema\(schema\)>)

The schema to use for the custom error schema

**`custom_error_type`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema\(custom_error_type\)>)

The custom error type to use for the custom error schema

**`custom_error_message`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema\(custom_error_message\)>)

The custom error message to use for the custom error schema

**`custom_error_context`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema\(custom_error_context\)>)

The custom error context to use for the custom error schema

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.custom_error_schema\(serialization\)>)

Custom serialization schema

## json_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_schema>)
    
    def json_schema(
        schema: CoreSchema | None = None,
        *,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> JsonSchema
    
Returns a schema that matches a JSON value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    dict_schema = core_schema.model_fields_schema(
        {
            'field_a': core_schema.model_field(core_schema.str_schema()),
            'field_b': core_schema.model_field(core_schema.bool_schema()),
        },
    )
    
    class MyModel:
        __slots__ = (
            '__dict__',
            '__pydantic_fields_set__',
            '__pydantic_extra__',
            '__pydantic_private__',
        )
        field_a: str
        field_b: bool
    
    json_schema = core_schema.json_schema(schema=dict_schema)
    schema = core_schema.model_schema(cls=MyModel, schema=json_schema)
    v = SchemaValidator(schema)
    m = v.validate_python('{"field_a": "hello", "field_b": true}')
    assert isinstance(m, MyModel)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-64>)

`JsonSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-63>)

**`schema`** : `CoreSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_schema\(schema\)>)

The schema to use for the JSON schema

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.json_schema\(serialization\)>)

Custom serialization schema

## url_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema>)
    
    def url_schema(
        *,
        max_length: int | None = None,
        allowed_schemes: list[str] | None = None,
        host_required: bool | None = None,
        default_host: str | None = None,
        default_port: int | None = None,
        default_path: str | None = None,
        preserve_empty_path: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> UrlSchema
    
Returns a schema that matches a URL value, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.url_schema()
    v = SchemaValidator(schema)
    print(v.validate_python('https://example.com'))
    #> https://example.com/
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-65>)

`UrlSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-64>)

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(max_length\)>)

The maximum length of the URL

**`allowed_schemes`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(allowed_schemes\)>)

The allowed URL schemes

**`host_required`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(host_required\)>)

Whether the URL must have a host

**`default_host`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(default_host\)>)

The default host to use if the URL does not have a host

**`default_port`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(default_port\)>)

The default port to use if the URL does not have a port

**`default_path`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(default_path\)>)

The default path to use if the URL does not have a path

**`preserve_empty_path`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(preserve_empty_path\)>)

Whether to preserve an empty path or convert it to ’/’, default False

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(strict\)>)

Whether to use strict URL parsing

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.url_schema\(serialization\)>)

Custom serialization schema

## multi_host_url_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema>)
    
    def multi_host_url_schema(
        *,
        max_length: int | None = None,
        allowed_schemes: list[str] | None = None,
        host_required: bool | None = None,
        default_host: str | None = None,
        default_port: int | None = None,
        default_path: str | None = None,
        preserve_empty_path: bool | None = None,
        strict: bool | None = None,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> MultiHostUrlSchema
    
Returns a schema that matches a URL value with possibly multiple hosts, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.multi_host_url_schema()
    v = SchemaValidator(schema)
    print(v.validate_python('redis://localhost,0.0.0.0,127.0.0.1'))
    #> redis://localhost,0.0.0.0,127.0.0.1
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-66>)

`MultiHostUrlSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-65>)

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(max_length\)>)

The maximum length of the URL

**`allowed_schemes`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(allowed_schemes\)>)

The allowed URL schemes

**`host_required`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(host_required\)>)

Whether the URL must have a host

**`default_host`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(default_host\)>)

The default host to use if the URL does not have a host

**`default_port`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(default_port\)>)

The default port to use if the URL does not have a port

**`default_path`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(default_path\)>)

The default path to use if the URL does not have a path

**`preserve_empty_path`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(preserve_empty_path\)>)

Whether to preserve an empty path or convert it to ’/’, default False

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(strict\)>)

Whether to use strict URL parsing

**`ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(ref\)>)

optional unique identifier of the schema, used to reference the schema in other places

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.multi_host_url_schema\(serialization\)>)

Custom serialization schema

## definitions_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.definitions_schema>)
    
    def definitions_schema(
        schema: CoreSchema,
        definitions: list[CoreSchema],
    ) -> DefinitionsSchema
    
Build a schema that contains both an inner schema and a list of definitions which can be used within the inner schema.
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema = core_schema.definitions_schema(
        core_schema.list_schema(core_schema.definition_reference_schema('foobar')),
        [core_schema.int_schema(ref='foobar')],
    )
    v = SchemaValidator(schema)
    assert v.validate_python([1, 2, '3']) == [1, 2, 3]
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-67>)

`DefinitionsSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-66>)

**`schema`** : `CoreSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.definitions_schema\(schema\)>)

The inner schema

**`definitions`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[`CoreSchema`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.definitions_schema\(definitions\)>)

List of definitions which can be referenced within inner schema

## definition_reference_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.definition_reference_schema>)
    
    def definition_reference_schema(
        schema_ref: str,
        ref: str | None = None,
        metadata: dict[str, Any] | None = None,
        serialization: SerSchema | None = None,
    ) -> DefinitionReferenceSchema
    
Returns a schema that points to a schema stored in “definitions”, this is useful for nested recursive models and also when you want to define validators separately from the main schema, e.g.:
    
    from pydantic_core import SchemaValidator, core_schema
    
    schema_definition = core_schema.definition_reference_schema('list-schema')
    schema = core_schema.definitions_schema(
        schema=schema_definition,
        definitions=[
            core_schema.list_schema(items_schema=schema_definition, ref='list-schema'),
        ],
    )
    v = SchemaValidator(schema)
    assert v.validate_python([()]) == [[]]
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-68>)

`DefinitionReferenceSchema`

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#parameters-67>)

**`schema_ref`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.definition_reference_schema\(schema_ref\)>)

The schema ref to use for the definition reference schema

**`metadata`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.definition_reference_schema\(metadata\)>)

Any other information you want to include with the schema, not used by pydantic-core

**`serialization`** : `SerSchema` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.definition_reference_schema\(serialization\)>)

Custom serialization schema

## iter_union_choices 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.iter_union_choices>)
    
    def iter_union_choices(union_schema: UnionSchema) -> Generator[CoreSchema]
    
Iterate over the choices of a `'union'` schema.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#returns-69>)

[`Generator`](<https://docs.python.org/3/library/typing.html#typing.Generator>)[`CoreSchema`]

## WhenUsed 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core_schema/#pydantic_core.core_schema.WhenUsed>)

Values have the following meanings:

  * `'always'` means always use
  * `'unless-none'` means use unless the value is `None`
  * `'json'` means use when serializing to JSON
  * `'json-unless-none'` means use when serializing to JSON and the value is not `None`

**Default:** `Literal['always', 'unless-none', 'json', 'json-unless-none']`

Was this page helpful?

Thanks for your feedback!