# TypeAdapter | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/](https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# TypeAdapter

## TypeAdapter 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>)

**Bases:** `Generic[T]`

Type adapters provide a flexible way to perform validation and serialization based on a Python type.

A `TypeAdapter` instance exposes some of the functionality from `BaseModel` instance methods for types that do not have such methods (such as dataclasses, primitive types, and more).

**Note:** `TypeAdapter` instances are not types, and cannot be used as type annotations for fields.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#constructor-parameters>)

**`type`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.__init__\(type\)>)

The type associated with the `TypeAdapter`.

**`config`** : [`ConfigDict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.__init__\(config\)>)

Configuration for the `TypeAdapter`, should be a dictionary conforming to [`ConfigDict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict>).

**`_parent_depth`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) _Default:_ `2`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.__init__\(_parent_depth\)>)

Depth at which to search for the [parent frame](<https://docs.python.org/3/reference/datamodel.html#frame-objects>). This frame is used when resolving forward annotations during schema building, by looking for the globals and locals of this frame. Defaults to 2, which will result in the frame where the `TypeAdapter` was instantiated.

**`module`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.__init__\(module\)>)

The module that passes to plugin if provided.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#attributes>)

#### core_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.core_schema>)

The core schema for the type.

**Type:** `CoreSchema`

#### validator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validator>)

The schema validator for the type.

**Type:** `SchemaValidator` | `PluggableSchemaValidator`

#### serializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.serializer>)

The schema serializer for the type.

**Type:** `SchemaSerializer`

#### pydantic_complete 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.pydantic_complete>)

Whether the core schema for the type is successfully built.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

Compatibility with `mypy`

Depending on the type used, `mypy` might raise an error when instantiating a `TypeAdapter`. As a workaround, you can explicitly annotate your variable:
    
    from typing import Union
    
    from pydantic import TypeAdapter
    
    ta: TypeAdapter[Union[str, int]] = TypeAdapter(Union[str, int])  # type: ignore[arg-type]
    
Namespace management nuances and implementation details

Here, we collect some notes on namespace management, and subtle differences from `BaseModel`:

`BaseModel` uses its own `__module__` to find out where it was defined and then looks for symbols to resolve forward references in those globals. On the other hand, `TypeAdapter` can be initialized with arbitrary objects, which may not be types and thus do not have a `__module__` available. So instead we look at the globals in our parent stack frame.

It is expected that the `ns_resolver` passed to this function will have the correct namespace for the type we’re adapting. See the source code for `TypeAdapter.__init__` and `TypeAdapter.rebuild` for various ways to construct this namespace.

This works for the case where this function is called in a module that has the target of forward references in its scope, but does not always work for more complex cases.

For example, take the following:

a.py
    
    IntList = list[int]
    OuterDict = dict[str, 'IntList']
    
b.py
    
    from a import OuterDict
    
    from pydantic import TypeAdapter
    
    IntList = int  # replaces the symbol the forward reference is looking for
    v = TypeAdapter(OuterDict)
    v({'x': 1})  # should fail but doesn't
    
If `OuterDict` were a `BaseModel`, this would work because it would resolve the forward reference within the `a.py` namespace. But `TypeAdapter(OuterDict)` can’t determine what module `OuterDict` came from.

In other words, the assumption that _all_ forward references exist in the module we are being called from is not technically always true. Although most of the time it is and it works fine for recursive models and such, `BaseModel`’s behavior isn’t perfect either and _can_ break in similar ways, so there is no right or wrong between the two.

But at the very least this behavior is _subtly_ different from `BaseModel`’s.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#methods>)

#### rebuild 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.rebuild>)
    
    def rebuild(
        *,
        force: bool = False,
        raise_errors: bool = True,
        _parent_namespace_depth: int = 2,
        _types_namespace: _namespace_utils.MappingNamespace | None = None,
    ) -> bool | None
    
Try to rebuild the pydantic-core schema for the adapter’s type.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during the initial attempt to build the schema, and automatic rebuilding fails.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns>)

[`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) — Returns `None` if the schema is already “complete” and rebuilding was not required. [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) — If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters>)

**`force`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.rebuild\(force\)>)

Whether to force the rebuilding of the type adapter’s schema, defaults to `False`.

**`raise_errors`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.rebuild\(raise_errors\)>)

Whether to raise errors, defaults to `True`.

**`_parent_namespace_depth`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) _Default:_ `2`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.rebuild\(_parent_namespace_depth\)>)

Depth at which to search for the [parent frame](<https://docs.python.org/3/reference/datamodel.html#frame-objects>). This frame is used when resolving forward annotations during schema rebuilding, by looking for the locals of this frame. Defaults to 2, which will result in the frame where the method was called.

**`_types_namespace`** : `_namespace_utils.MappingNamespace` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.rebuild\(_types_namespace\)>)

An explicit types namespace to use, instead of using the local namespace from the parent frame. Defaults to `None`.

#### validate_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python>)
    
    def validate_python(
        object: Any,
        /,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        experimental_allow_partial: bool | Literal['off', 'on', 'trailing-strings'] = False,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> T
    
Validate a Python object against the model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-1>)

`T` — The validated object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-1>)

**`object`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(object\)>)

The Python object to validate against the model.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(strict\)>)

Whether to strictly check types.

**`extra`** : `ExtraValues` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. See the [`extra` configuration value](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>) for details.

**`from_attributes`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(from_attributes\)>)

Whether to extract data from object attributes.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(context\)>)

Additional context to pass to the validator.

**`experimental_allow_partial`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘off’, ‘on’, ‘trailing-strings’] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(experimental_allow_partial\)>)

**Experimental** whether to enable [partial validation](<https://pydantic.dev/docs/validation/latest/concepts/experimental#partial-validation>), e.g. to process streams.

  * False / ‘off’: Default behavior, no partial validation.
  * True / ‘on’: Enable partial validation.
  * ‘trailing-strings’: Enable partial validation and allow trailing strings in the input.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_python\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

#### validate_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json>)
    
    def validate_json(
        data: str | bytes | bytearray,
        /,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        experimental_allow_partial: bool | Literal['off', 'on', 'trailing-strings'] = False,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> T
    
Validate a JSON string or bytes against the model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-2>)

`T` — The validated object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-2>)

**`data`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) | [`bytearray`](<https://docs.python.org/3/library/stdtypes.html#bytearray>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json\(data\)>)

The JSON data to validate against the model.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json\(strict\)>)

Whether to strictly check types.

**`extra`** : `ExtraValues` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. See the [`extra` configuration value](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>) for details.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json\(context\)>)

Additional context to use during validation.

**`experimental_allow_partial`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘off’, ‘on’, ‘trailing-strings’] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json\(experimental_allow_partial\)>)

**Experimental** whether to enable [partial validation](<https://pydantic.dev/docs/validation/latest/concepts/experimental#partial-validation>), e.g. to process streams.

  * False / ‘off’: Default behavior, no partial validation.
  * True / ‘on’: Enable partial validation.
  * ‘trailing-strings’: Enable partial validation and allow trailing strings in the input.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_json\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

#### validate_strings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings>)
    
    def validate_strings(
        obj: Any,
        /,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        experimental_allow_partial: bool | Literal['off', 'on', 'trailing-strings'] = False,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> T
    
Validate object contains string data against the model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-3>)

`T` — The validated object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-3>)

**`obj`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings\(obj\)>)

The object contains string data to validate.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings\(strict\)>)

Whether to strictly check types.

**`extra`** : `ExtraValues` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. See the [`extra` configuration value](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>) for details.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings\(context\)>)

Additional context to use during validation.

**`experimental_allow_partial`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘off’, ‘on’, ‘trailing-strings’] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings\(experimental_allow_partial\)>)

**Experimental** whether to enable [partial validation](<https://pydantic.dev/docs/validation/latest/concepts/experimental#partial-validation>), e.g. to process streams.

  * False / ‘off’: Default behavior, no partial validation.
  * True / ‘on’: Enable partial validation.
  * ‘trailing-strings’: Enable partial validation and allow trailing strings in the input.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.validate_strings\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

#### get_default_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.get_default_value>)
    
    def get_default_value(
        *,
        strict: bool | None = None,
        context: Any | None = None,
    ) -> Some[T] | None
    
Get the default value for the wrapped type.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-4>)

`Some`[`T`] | [`None`](<https://docs.python.org/3/library/constants.html#None>) — The default value wrapped in a `Some` if there is one or None if not.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-4>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.get_default_value\(strict\)>)

Whether to strictly check types.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.get_default_value\(context\)>)

Additional context to pass to the validator.

#### dump_python 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python>)
    
    def dump_python(
        instance: T,
        /,
        *,
        mode: Literal['json', 'python'] = 'python',
        include: IncEx | None = None,
        exclude: IncEx | None = None,
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
    
Dump an instance of the adapted type to a Python object.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-5>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The serialized object.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-5>)

**`instance`** : `T`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(instance\)>)

The Python object to serialize.

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘json’, ‘python’] _Default:_ `'python'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(mode\)>)

The output format.

**`include`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(include\)>)

Fields to include in the output.

**`exclude`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(exclude\)>)

Fields to exclude from the output.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(by_alias\)>)

Whether to use alias names for field names.

**`exclude_unset`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(exclude_unset\)>)

Whether to exclude unset fields.

**`exclude_defaults`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(exclude_defaults\)>)

Whether to exclude fields with default values.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(exclude_none\)>)

Whether to exclude fields with None values.

**`exclude_computed_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(exclude_computed_fields\)>)

Whether to exclude computed fields. While this can be useful for round-tripping, it is usually recommended to use the dedicated `round_trip` parameter instead.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(round_trip\)>)

Whether to output the serialized data in a way that is compatible with deserialization.

**`warnings`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘none’, ‘warn’, ‘error’] _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(warnings\)>)

How to handle serialization errors. False/“none” ignores them, True/“warn” logs errors, “error” raises a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>).

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(fallback\)>)

A function to call when an unknown value is encountered. If not provided, a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_python\(context\)>)

Additional context to pass to the serializer.

#### dump_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json>)
    
    def dump_json(
        instance: T,
        /,
        *,
        indent: int | None = None,
        ensure_ascii: bool = False,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
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
    
Serialize an instance of the adapted type to JSON.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-6>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The JSON representation of the given instance as bytes.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-6>)

**`instance`** : `T`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(instance\)>)

The instance to be serialized.

**`indent`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(indent\)>)

Number of spaces for JSON indentation.

**`ensure_ascii`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(ensure_ascii\)>)

If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped. If `False` (the default), these characters will be output as-is.

**`include`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(include\)>)

Fields to include.

**`exclude`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(exclude\)>)

Fields to exclude.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(by_alias\)>)

Whether to use alias names for field names.

**`exclude_unset`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(exclude_unset\)>)

Whether to exclude unset fields.

**`exclude_defaults`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(exclude_defaults\)>)

Whether to exclude fields with default values.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(exclude_none\)>)

Whether to exclude fields with a value of `None`.

**`exclude_computed_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(exclude_computed_fields\)>)

Whether to exclude computed fields. While this can be useful for round-tripping, it is usually recommended to use the dedicated `round_trip` parameter instead.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(round_trip\)>)

Whether to serialize and deserialize the instance to ensure round-tripping.

**`warnings`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘none’, ‘warn’, ‘error’] _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(warnings\)>)

How to handle serialization errors. False/“none” ignores them, True/“warn” logs errors, “error” raises a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>).

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(fallback\)>)

A function to call when an unknown value is encountered. If not provided, a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.dump_json\(context\)>)

Additional context to pass to the serializer.

#### json_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema>)
    
    def json_schema(
        *,
        by_alias: bool = True,
        ref_template: str = DEFAULT_REF_TEMPLATE,
        union_format: Literal['any_of', 'primitive_type_array'] = 'any_of',
        schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
        mode: JsonSchemaMode = 'validation',
    ) -> dict[str, Any]
    
Generate a JSON schema for the adapted type.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-7>)

[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] — The JSON schema for the model as a dictionary.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-7>)

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema\(by_alias\)>)

Whether to use alias names for field names.

**`ref_template`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `DEFAULT_REF_TEMPLATE`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema\(ref_template\)>)

The format string used for generating $ref strings.

**`union_format`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘any_of’, ‘primitive_type_array’] _Default:_ `'any_of'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema\(union_format\)>)

The format to use when combining schemas from unions together. Can be one of:

  * `'any_of'`: Use the [`anyOf`](<https://json-schema.org/understanding-json-schema/reference/combining#anyOf>) keyword to combine schemas (the default).
  * `'primitive_type_array'`: Use the [`type`](<https://json-schema.org/understanding-json-schema/reference/type>) keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to `any_of`.

**`schema_generator`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`GenerateJsonSchema`] _Default:_ `GenerateJsonSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema\(schema_generator\)>)

To override the logic used to generate the JSON schema, as a subclass of `GenerateJsonSchema` with your desired modifications

**`mode`** : `JsonSchemaMode` _Default:_ `'validation'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema\(mode\)>)

The mode in which to generate the schema.

**`schema_generator`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`GenerateJsonSchema`] _Default:_ `GenerateJsonSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema\(schema_generator\)>)

The generator class used for creating the schema.

**`mode`** : `JsonSchemaMode` _Default:_ `'validation'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schema\(mode\)>)

The mode to use for schema generation.

#### json_schemas 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas>)

`@staticmethod`
    
    def json_schemas(
        inputs: Iterable[tuple[JsonSchemaKeyT, JsonSchemaMode, TypeAdapter[Any]]],
        /,
        *,
        by_alias: bool = True,
        title: str | None = None,
        description: str | None = None,
        ref_template: str = DEFAULT_REF_TEMPLATE,
        union_format: Literal['any_of', 'primitive_type_array'] = 'any_of',
        schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
    ) -> tuple[dict[tuple[JsonSchemaKeyT, JsonSchemaMode], JsonSchemaValue], JsonSchemaValue]
    
Generate a JSON schema including definitions from multiple type adapters.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#returns-8>)

[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[`JsonSchemaKeyT`, `JsonSchemaMode`], `JsonSchemaValue`], `JsonSchemaValue`] — A tuple where:

  * The first element is a dictionary whose keys are tuples of JSON schema key type and JSON mode, and whose values are the JSON schema corresponding to that pair of inputs. (These schemas may have JsonRef references to definitions that are defined in the second returned element.)
  * The second element is a JSON schema containing all definitions referenced in the first returned element, along with the optional title and description keys.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#parameters-8>)

**`inputs`** : [`Iterable`](<https://docs.python.org/3/library/typing.html#typing.Iterable>)[[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[`JsonSchemaKeyT`, `JsonSchemaMode`, [`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]]] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas\(inputs\)>)

Inputs to schema generation. The first two items will form the keys of the (first) output mapping; the type adapters will provide the core schemas that get converted into definitions in the output JSON schema.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas\(by_alias\)>)

Whether to use alias names.

**`title`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas\(title\)>)

The title for the schema.

**`description`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas\(description\)>)

The description for the schema.

**`ref_template`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `DEFAULT_REF_TEMPLATE`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas\(ref_template\)>)

The format string used for generating $ref strings.

**`union_format`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘any_of’, ‘primitive_type_array’] _Default:_ `'any_of'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas\(union_format\)>)

The format to use when combining schemas from unions together. Can be one of:

  * `'any_of'`: Use the [`anyOf`](<https://json-schema.org/understanding-json-schema/reference/combining#anyOf>) keyword to combine schemas (the default).
  * `'primitive_type_array'`: Use the [`type`](<https://json-schema.org/understanding-json-schema/reference/type>) keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to `any_of`.

**`schema_generator`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`GenerateJsonSchema`] _Default:_ `GenerateJsonSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.json_schemas\(schema_generator\)>)

The generator class used for creating the schema.

Was this page helpful?

Thanks for your feedback!