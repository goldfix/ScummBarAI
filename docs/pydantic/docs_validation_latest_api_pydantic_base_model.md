# BaseModel | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/](https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# BaseModel

Pydantic models are simply classes which inherit from `BaseModel` and define fields as annotated attributes.

## BaseModel 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>)

A base class for creating Pydantic models.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#attributes>)

#### __class_vars__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__class_vars__>)

The names of the class variables defined on the model.

**Type:** [`set`](<https://docs.python.org/3/reference/expressions.html#set>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]

#### __private_attributes__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__private_attributes__>)

Metadata about the private attributes of the model.

**Type:** [`Dict`](<https://docs.python.org/3/library/typing.html#typing.Dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `ModelPrivateAttr`]

#### __signature__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__signature__>)

The synthesized `__init__` [`Signature`](<https://docs.python.org/3/library/inspect.html#inspect.Signature>) of the model.

**Type:** `Signature`

#### __pydantic_complete__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_complete__>)

Whether model building is completed, or if there are still undefined fields.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### __pydantic_core_schema__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_core_schema__>)

The core schema of the model.

**Type:** `CoreSchema`

#### __pydantic_custom_init__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_custom_init__>)

Whether the model has a custom `__init__` function.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### __pydantic_decorators__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_decorators__>)

Metadata containing the decorators defined on the model. This replaces `Model.__validators__` and `Model.__root_validators__` from Pydantic V1.

**Type:** `_decorators.DecoratorInfos`

#### __pydantic_generic_metadata__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_generic_metadata__>)

A dictionary containing metadata about generic Pydantic models. The `origin` and `args` items map to the [`__origin__`](<https://docs.python.org/3/library/stdtypes.html#genericalias.__origin__>) and [`__args__`](<https://docs.python.org/3/library/stdtypes.html#genericalias.__args__>) attributes of [generic aliases](<https://docs.python.org/3/library/stdtypes.html#types-genericalias>), and the `parameter` item maps to the `__parameter__` attribute of generic classes.

**Type:** `_generics.PydanticGenericMetadata`

#### __pydantic_parent_namespace__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_parent_namespace__>)

Parent namespace of the model, used for automatic rebuilding of models.

**Type:** [`Dict`](<https://docs.python.org/3/library/typing.html#typing.Dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### __pydantic_post_init__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_post_init__>)

The name of the post-init method for the model, if defined.

**Type:** [`None`](<https://docs.python.org/3/library/constants.html#None>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘model_post_init’]

#### __pydantic_root_model__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_root_model__>)

Whether the model is a [`RootModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/root_model/#pydantic.root_model.RootModel>).

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### __pydantic_serializer__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_serializer__>)

The `pydantic-core` `SchemaSerializer` used to dump instances of the model.

**Type:** `SchemaSerializer`

#### __pydantic_validator__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_validator__>)

The `pydantic-core` `SchemaValidator` used to validate instances of the model.

**Type:** `SchemaValidator` | `PluggableSchemaValidator`

#### __pydantic_fields__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_fields__>)

A dictionary of field names and their corresponding [`FieldInfo`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo>) objects.

**Type:** [`Dict`](<https://docs.python.org/3/library/typing.html#typing.Dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `FieldInfo`]

#### __pydantic_computed_fields__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_computed_fields__>)

A dictionary of computed field names and their corresponding [`ComputedFieldInfo`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo>) objects.

**Type:** [`Dict`](<https://docs.python.org/3/library/typing.html#typing.Dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `ComputedFieldInfo`]

#### __pydantic_extra__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_extra__>)

A dictionary containing extra values, if [`extra`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>) is set to `'allow'`.

**Type:** [`Dict`](<https://docs.python.org/3/library/typing.html#typing.Dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### __pydantic_fields_set__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_fields_set__>)

The names of fields explicitly set during instantiation.

**Type:** [`set`](<https://docs.python.org/3/reference/expressions.html#set>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]

#### __pydantic_private__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__pydantic_private__>)

Values of private attributes set on the model instance.

**Type:** [`Dict`](<https://docs.python.org/3/library/typing.html#typing.Dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#methods>)

#### __init__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.__init__>)
    
    def __init__(**data: Any) -> None
    
Raises [`ValidationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError>) if the input data cannot be validated to form a valid model.

`self` is explicitly positional-only to allow `self` as a field name.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

#### model_fields 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_fields>)

`@classmethod`
    
    def model_fields(cls) -> dict[str, FieldInfo]
    
A mapping of field names to their respective [`FieldInfo`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo>) instances.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-1>)

[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `FieldInfo`]

#### model_computed_fields 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_computed_fields>)

`@classmethod`
    
    def model_computed_fields(cls) -> dict[str, ComputedFieldInfo]
    
A mapping of computed field names to their respective [`ComputedFieldInfo`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo>) instances.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-2>)

[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `ComputedFieldInfo`]

#### model_construct 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_construct>)

`@classmethod`
    
    def model_construct(cls, _fields_set: set[str] | None = None, **values: Any) -> Self
    
Creates a new instance of the `Model` class with validated data.

Creates a new model setting `__dict__` and `__pydantic_fields_set__` from trusted or pre-validated data. Default values are respected, but no other validation is performed.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-3>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>) — A new instance of the `Model` class with validated data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters>)

**`_fields_set`** : [`set`](<https://docs.python.org/3/reference/expressions.html#set>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_construct\(_fields_set\)>)

A set of field names that were originally explicitly set during instantiation. If provided, this is directly used for the [`model_fields_set`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_fields_set>) attribute. Otherwise, the field names from the `values` argument will be used.

**`values`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `{}`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_construct\(values\)>)

Trusted or pre-validated data dictionary.

#### model_copy 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_copy>)
    
    def model_copy(*, update: Mapping[str, Any] | None = None, deep: bool = False) -> Self
    
Returns a copy of the model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-4>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>) — New model instance.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-1>)

**`update`** : [`Mapping`](<https://docs.python.org/3/library/typing.html#typing.Mapping>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_copy\(update\)>)

Values to change/add in the new model. Note: the data is not validated before creating the new model. You should trust this data.

**`deep`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_copy\(deep\)>)

Set to `True` to make a deep copy of the model.

#### model_dump 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump>)
    
    def model_dump(
        *,
        mode: Literal['json', 'python'] | str = 'python',
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
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
    ) -> dict[str, Any]
    
Generate a dictionary representation of the model, optionally specifying which fields to include or exclude.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-5>)

[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] — A dictionary representation of the model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-2>)

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘json’, ‘python’] | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `'python'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(mode\)>)

The mode in which `to_python` should run. If mode is ‘json’, the output will only contain JSON serializable types. If mode is ‘python’, the output may contain non-JSON-serializable Python objects.

**`include`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(include\)>)

A set of fields to include in the output.

**`exclude`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(exclude\)>)

A set of fields to exclude from the output.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(context\)>)

Additional context to pass to the serializer.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(by_alias\)>)

Whether to use the field’s alias in the dictionary key if defined.

**`exclude_unset`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(exclude_unset\)>)

Whether to exclude fields that have not been explicitly set.

**`exclude_defaults`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(exclude_defaults\)>)

Whether to exclude fields that are set to their default value.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(exclude_none\)>)

Whether to exclude fields that have a value of `None`.

**`exclude_computed_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(exclude_computed_fields\)>)

Whether to exclude computed fields. While this can be useful for round-tripping, it is usually recommended to use the dedicated `round_trip` parameter instead.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(round_trip\)>)

If True, dumped values should be valid as input for non-idempotent types such as Json[T].

**`warnings`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘none’, ‘warn’, ‘error’] _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(warnings\)>)

How to handle serialization errors. False/“none” ignores them, True/“warn” logs errors, “error” raises a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>).

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(fallback\)>)

A function to call when an unknown value is encountered. If not provided, a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

#### model_dump_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json>)
    
    def model_dump_json(
        *,
        indent: int | None = None,
        ensure_ascii: bool = False,
        include: IncEx | None = None,
        exclude: IncEx | None = None,
        context: Any | None = None,
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
    ) -> str
    
Generates a JSON representation of the model using Pydantic’s `to_json` method.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-6>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — A JSON string representation of the model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-3>)

**`indent`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(indent\)>)

Indentation to use in the JSON output. If None is passed, the output will be compact.

**`ensure_ascii`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(ensure_ascii\)>)

If `True`, the output is guaranteed to have all incoming non-ASCII characters escaped. If `False` (the default), these characters will be output as-is.

**`include`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(include\)>)

Field(s) to include in the JSON output.

**`exclude`** : `IncEx` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(exclude\)>)

Field(s) to exclude from the JSON output.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(context\)>)

Additional context to pass to the serializer.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(by_alias\)>)

Whether to serialize using field aliases.

**`exclude_unset`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(exclude_unset\)>)

Whether to exclude fields that have not been explicitly set.

**`exclude_defaults`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(exclude_defaults\)>)

Whether to exclude fields that are set to their default value.

**`exclude_none`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(exclude_none\)>)

Whether to exclude fields that have a value of `None`.

**`exclude_computed_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(exclude_computed_fields\)>)

Whether to exclude computed fields. While this can be useful for round-tripping, it is usually recommended to use the dedicated `round_trip` parameter instead.

**`round_trip`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(round_trip\)>)

If True, dumped values should be valid as input for non-idempotent types such as Json[T].

**`warnings`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘none’, ‘warn’, ‘error’] _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(warnings\)>)

How to handle serialization errors. False/“none” ignores them, True/“warn” logs errors, “error” raises a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>).

**`fallback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(fallback\)>)

A function to call when an unknown value is encountered. If not provided, a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) error is raised.

**`serialize_as_any`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(serialize_as_any\)>)

Whether to serialize fields with duck-typing serialization behavior.

**`polymorphic_serialization`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_dump_json\(polymorphic_serialization\)>)

Whether to use model and dataclass polymorphic serialization for this call.

#### model_json_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema>)

`@classmethod`
    
    def model_json_schema(
        cls,
        by_alias: bool = True,
        ref_template: str = DEFAULT_REF_TEMPLATE,
        schema_generator: type[GenerateJsonSchema] = GenerateJsonSchema,
        mode: JsonSchemaMode = 'validation',
        *,
        union_format: Literal['any_of', 'primitive_type_array'] = 'any_of',
    ) -> dict[str, Any]
    
Generates a JSON schema for a model class.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-7>)

[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] — The JSON schema for the given model class.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-4>)

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema\(by_alias\)>)

Whether to use attribute aliases or not.

**`ref_template`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `DEFAULT_REF_TEMPLATE`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema\(ref_template\)>)

The reference template.

**`union_format`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘any_of’, ‘primitive_type_array’] _Default:_ `'any_of'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema\(union_format\)>)

The format to use when combining schemas from unions together. Can be one of:

  * `'any_of'`: Use the [`anyOf`](<https://json-schema.org/understanding-json-schema/reference/combining#anyOf>) keyword to combine schemas (the default).
  * `'primitive_type_array'`: Use the [`type`](<https://json-schema.org/understanding-json-schema/reference/type>) keyword as an array of strings, containing each type of the combination. If any of the schemas is not a primitive type (`string`, `boolean`, `null`, `integer` or `number`) or contains constraints/metadata, falls back to `any_of`.

**`schema_generator`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`GenerateJsonSchema`] _Default:_ `GenerateJsonSchema`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema\(schema_generator\)>)

To override the logic used to generate the JSON schema, as a subclass of `GenerateJsonSchema` with your desired modifications

**`mode`** : `JsonSchemaMode` _Default:_ `'validation'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_json_schema\(mode\)>)

The mode in which to generate the schema.

#### model_parametrized_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_parametrized_name>)

`@classmethod`
    
    def model_parametrized_name(cls, params: tuple[type[Any], ...]) -> str
    
Compute the class name for parametrizations of generic classes.

This method can be overridden to achieve a custom naming scheme for generic BaseModels.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-8>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — String representing the new class where `params` are passed to `cls` as type variables.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-5>)

**`params`** : [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], …] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_parametrized_name\(params\)>)

Tuple of types of the class. Given a generic class `Model` with 2 type variables and a concrete model `Model[str, int]`, the value `(str, int)` would be passed to `params`.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#raises>)

  * `TypeError` — Raised when trying to generate concrete names for non-generic models.

#### model_post_init 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_post_init>)
    
    def model_post_init(context: Any, /) -> None
    
Override this method to perform additional initialization after `__init__` and `model_construct`. This is useful if you want to do some validation that requires the entire model to be initialized.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-9>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

#### model_rebuild 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild>)

`@classmethod`
    
    def model_rebuild(
        cls,
        *,
        force: bool = False,
        raise_errors: bool = True,
        _parent_namespace_depth: int = 2,
        _types_namespace: MappingNamespace | None = None,
    ) -> bool | None
    
Try to rebuild the pydantic-core schema for the model.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during the initial attempt to build the schema, and automatic rebuilding fails.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-10>)

[`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) — Returns `None` if the schema is already “complete” and rebuilding was not required. [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) — If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-6>)

**`force`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild\(force\)>)

Whether to force the rebuilding of the model schema, defaults to `False`.

**`raise_errors`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild\(raise_errors\)>)

Whether to raise errors, defaults to `True`.

**`_parent_namespace_depth`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) _Default:_ `2`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild\(_parent_namespace_depth\)>)

The depth level of the parent namespace, defaults to 2.

**`_types_namespace`** : `MappingNamespace` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild\(_types_namespace\)>)

The types namespace, defaults to `None`.

#### model_validate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate>)

`@classmethod`
    
    def model_validate(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        from_attributes: bool | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self
    
Validate a pydantic model instance.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-11>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>) — The validated model instance.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-7>)

**`obj`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate\(obj\)>)

The object to validate.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate\(strict\)>)

Whether to enforce types strictly.

**`extra`** : `ExtraValues` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. See the [`extra` configuration value](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>) for details.

**`from_attributes`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate\(from_attributes\)>)

Whether to extract data from object attributes.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate\(context\)>)

Additional context to pass to the validator.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#raises-1>)

  * `ValidationError` — If the object could not be validated.

#### model_validate_json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json>)

`@classmethod`
    
    def model_validate_json(
        cls,
        json_data: str | bytes | bytearray,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self
    
Validate the given JSON data against the Pydantic model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-12>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>) — The validated Pydantic model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-8>)

**`json_data`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) | [`bytearray`](<https://docs.python.org/3/library/stdtypes.html#bytearray>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json\(json_data\)>)

The JSON data to validate.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json\(strict\)>)

Whether to enforce types strictly.

**`extra`** : `ExtraValues` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. See the [`extra` configuration value](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>) for details.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json\(context\)>)

Extra variables to pass to the validator.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_json\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#raises-2>)

  * `ValidationError` — If `json_data` is not a JSON string or the object could not be validated.

#### model_validate_strings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings>)

`@classmethod`
    
    def model_validate_strings(
        cls,
        obj: Any,
        *,
        strict: bool | None = None,
        extra: ExtraValues | None = None,
        context: Any | None = None,
        by_alias: bool | None = None,
        by_name: bool | None = None,
    ) -> Self
    
Validate the given object with string data against the Pydantic model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-13>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>) — The validated Pydantic model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-9>)

**`obj`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings\(obj\)>)

The object containing string data to validate.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings\(strict\)>)

Whether to enforce types strictly.

**`extra`** : `ExtraValues` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings\(extra\)>)

Whether to ignore, allow, or forbid extra data during model validation. See the [`extra` configuration value](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>) for details.

**`context`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings\(context\)>)

Extra variables to pass to the validator.

**`by_alias`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings\(by_alias\)>)

Whether to use the field’s alias when validating against the provided input data.

**`by_name`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate_strings\(by_name\)>)

Whether to use the field’s name when validating against the provided input data.

## create_model 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model>)
    
    def create_model(
        model_name: str,
        /,
        *,
        __config__: ConfigDict | None = None,
        __doc__: str | None = None,
        __base__: None = None,
        __module__: str = __name__,
        __validators__: dict[str, Callable[..., Any]] | None = None,
        __cls_kwargs__: dict[str, Any] | None = None,
        __qualname__: str | None = None,
        **field_definitions: Any | tuple[Any, Any],
    ) -> type[BaseModel]
    def create_model(
        model_name: str,
        /,
        *,
        __config__: ConfigDict | None = None,
        __doc__: str | None = None,
        __base__: type[ModelT] | tuple[type[ModelT], ...],
        __module__: str = __name__,
        __validators__: dict[str, Callable[..., Any]] | None = None,
        __cls_kwargs__: dict[str, Any] | None = None,
        __qualname__: str | None = None,
        **field_definitions: Any | tuple[Any, Any],
    ) -> type[ModelT]
    
Dynamically creates and returns a new Pydantic model, in other words, `create_model` dynamically creates a subclass of [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>).

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#returns-14>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[`ModelT`] — The new [model](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>).

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#parameters-10>)

**`model_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(model_name\)>)

The name of the newly created model.

**`__config__`** : [`ConfigDict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(__config__\)>)

The configuration of the new model.

**`__doc__`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(__doc__\)>)

The docstring of the new model.

**`__base__`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`ModelT`] | [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`type`](<https://docs.python.org/3/glossary.html#term-type>)[`ModelT`], …] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(__base__\)>)

The base class or classes for the new model.

**`__module__`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(__module__\)>)

The name of the module that the model belongs to; if `None`, the value is taken from `sys._getframe(1)`

**`__validators__`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(__validators__\)>)

A dictionary of methods that validate fields. The keys are the names of the validation methods to be added to the model, and the values are the validation methods themselves. You can read more about functional validators [here](<https://docs.pydantic.dev/2.9/concepts/validators/#field-validators>).

**`__cls_kwargs__`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(__cls_kwargs__\)>)

A dictionary of keyword arguments for class creation, such as `metaclass`.

**`__qualname__`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(__qualname__\)>)

The qualified name of the newly created model.

**`**field_definitions`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] _Default:_ `{}`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.create_model\(**field_definitions\)>)

Field definitions of the new model. Either:

  * a single element, representing the type annotation of the field.
  * a two-tuple, the first element being the type and the second element the assigned value (either a default or the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function).

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#raises-3>)

  * `PydanticUserError` — If `__base__` and `__config__` are both passed.

Was this page helpful?

Thanks for your feedback!