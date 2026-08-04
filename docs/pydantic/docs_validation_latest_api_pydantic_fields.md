# Fields | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/fields/](https://pydantic.dev/docs/validation/latest/api/pydantic/fields/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Fields

Defining fields on models.

## FieldInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo>)

**Bases:** `Representation`

This class holds information about a field.

`FieldInfo` is used for any field definition regardless of whether the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function is explicitly used.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#attributes>)

#### annotation 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.annotation>)

The type annotation of the field.

**Type:** [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### default 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.default>)

The default value of the field.

**Type:** [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

#### default_factory 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.default_factory>)

A callable to generate the default value. The callable can either take 0 arguments (in which case it is called as is) or a single argument containing the already validated data.

**Type:** [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.alias>)

The alias name of the field.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### alias_priority 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.alias_priority>)

The priority of the field’s alias.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### validation_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.validation_alias>)

The validation alias of the field.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`AliasPath`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasPath>) | [`AliasChoices`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasChoices>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### serialization_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.serialization_alias>)

The serialization alias of the field.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### title 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.title>)

The title of the field.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### field_title_generator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.field_title_generator>)

A callable that takes a field name and returns title for it.

**Type:** [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `FieldInfo`], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### description 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.description>)

The description of the field.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### examples 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.examples>)

List of examples of the field.

**Type:** [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### exclude 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.exclude>)

Whether to exclude the field from the model serialization.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### exclude_if 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.exclude_if>)

A callable that determines whether to exclude a field during serialization based on its value.

**Type:** [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### discriminator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.discriminator>)

Field name or Discriminator for discriminating the type in a tagged union.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`types.Discriminator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Discriminator>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### deprecated 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.deprecated>)

A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport, or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.

**Type:** `Deprecated` | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### json_schema_extra 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.json_schema_extra>)

A dict or callable to provide extra JSON schema properties.

**Type:** `JsonDict` | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`JsonDict`], [`None`](<https://docs.python.org/3/library/constants.html#None>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### frozen 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.frozen>)

Whether the field is frozen.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### validate_default 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.validate_default>)

Whether to validate the default value of the field.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### repr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.repr>)

Whether to include the field in representation of the model.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### init 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.init>)

Whether the field should be included in the constructor of the dataclass.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### init_var 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.init_var>)

Whether the field should _only_ be included in the constructor of the dataclass, and not stored.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### kw_only 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.kw_only>)

Whether the field should be a keyword-only argument in the constructor of the dataclass.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### metadata 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.metadata>)

The metadata list. Contains all the data that isn’t expressed as direct `FieldInfo` attributes, including:

  * Type-specific constraints, such as `gt` or `min_length` (these are converted to metadata classes such as `annotated_types.Gt`).
  * Any other arbitrary object used within [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>) metadata (e.g. [custom types handlers](<https://pydantic.dev/docs/validation/latest/concepts/types#as-an-annotation>) or any object not recognized by Pydantic).

**Type:** [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#methods>)

#### _construct 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._construct>)

`@classmethod`
    
    def _construct(cls, metadata: list[Any], **attr_overrides: Any) -> Self
    
Construct the final `FieldInfo` instance, by merging the possibly existing `FieldInfo` instances from the metadata.

With the following example:
    
    class Model(BaseModel):
        f: Annotated[int, Gt(1), Field(description='desc', lt=2)]
    
`metadata` refers to the metadata elements of the `Annotated` form. This metadata is iterated over from left to right:

  * If the element is a `Field()` function (which is itself a `FieldInfo` instance), the field attributes (such as `description`) are saved to be set on the final `FieldInfo` instance. On the other hand, some kwargs (such as `lt`) are stored as `metadata` (see `FieldInfo.__init__()`, calling `FieldInfo._collect_metadata()`). In this case, the final metadata list is extended with the one from this instance.
  * Else, the element is considered as a single metadata object, and is appended to the final metadata list.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>) — The final merged `FieldInfo` instance.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters>)

**`metadata`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._construct\(metadata\)>)

The list of metadata elements to merge together. If the `FieldInfo` instance to be constructed is for a field with an assigned `Field()`, this `Field()` assignment should be added as the last element of the provided metadata.

**`**attr_overrides`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `{}`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._construct\(**attr_overrides\)>)

Extra attributes that should be set on the final merged `FieldInfo` instance.

#### _from_dataclass_field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._from_dataclass_field>)

`@staticmethod`
    
    def _from_dataclass_field(dc_field: DataclassField[Any]) -> FieldInfo
    
Return a new `FieldInfo` instance from a `dataclasses.Field` instance.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-1>)

`FieldInfo` — The corresponding `FieldInfo` instance.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-1>)

**`dc_field`** : `DataclassField`[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._from_dataclass_field\(dc_field\)>)

The `dataclasses.Field` instance to convert.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#raises>)

  * `TypeError` — If any of the `FieldInfo` kwargs does not match the `dataclass.Field` kwargs.

#### _collect_metadata 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._collect_metadata>)

`@staticmethod`
    
    def _collect_metadata(kwargs: dict[str, Any]) -> list[Any]
    
Collect annotations from kwargs.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-2>)

[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] — A list of metadata objects - a combination of `annotated_types.BaseMetadata` and `PydanticMetadata`.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-2>)

**`kwargs`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._collect_metadata\(kwargs\)>)

Keyword arguments passed to the function.

#### get_default 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.get_default>)
    
    def get_default(
        *,
        call_default_factory: Literal[True],
        validated_data: dict[str, Any] | None = None,
    ) -> Any
    def get_default(*, call_default_factory: Literal[False] = ...) -> Any
    
Get the default value.

We expose an option for whether to call the default_factory (if present), as calling it may result in side effects that we want to avoid. However, there are times when it really should be called (namely, when instantiating a model via `model_construct`).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-3>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The default value, calling the default factory if requested or `PydanticUndefined` if not set.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-3>)

**`call_default_factory`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.get_default\(call_default_factory\)>)

Whether to call the default factory or not.

**`validated_data`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.get_default\(validated_data\)>)

The already validated data to be passed to the default factory.

#### is_required 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.is_required>)
    
    def is_required() -> bool
    
Check if the field is required (i.e., does not have a default value or factory).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-4>)

[`bool`](<https://docs.python.org/3/library/functions.html#bool>) — `True` if the field is required, `False` otherwise.

#### asdict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo.asdict>)
    
    def asdict() -> _FieldInfoAsDict
    
Return a dictionary representation of the `FieldInfo` instance.

The returned value is a dictionary with three items:

  * `annotation`: The type annotation of the field.
  * `metadata`: The metadata list.
  * `attributes`: A mapping of the remaining `FieldInfo` attributes to their values (e.g. `alias`, `title`).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-5>)

`_FieldInfoAsDict`

#### _copy 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo._copy>)
    
    def _copy() -> Self
    
Return a copy of the `FieldInfo` instance.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-6>)

[`Self`](<https://docs.python.org/3/library/typing.html#typing.Self>)

## ModelPrivateAttr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr>)

**Bases:** `Representation`

A descriptor for private attributes in class models.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#attributes-1>)

#### default 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr.default>)

The default value of the attribute if not provided.

#### default_factory 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr.default_factory>)

A callable to generate the default value. The callable can either take 0 arguments (in which case it is called as is) or a single argument containing the validated data (the model’s [`__dict__`](<https://docs.python.org/3/reference/datamodel.html#object.__dict__>)) and the already initialized private attributes.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#methods-1>)

#### __getattr__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr.__getattr__>)
    
    def __getattr__(item: str) -> Any
    
This function improves compatibility with custom descriptors by ensuring delegation happens as expected when the default value of a private attribute is a descriptor.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-7>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

#### __set_name__ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr.__set_name__>)
    
    def __set_name__(cls: type[Any], name: str) -> None
    
Preserve `__set_name__` protocol defined in <https://peps.python.org/pep-0487>.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-8>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

#### get_default 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr.get_default>)
    
    def get_default(
        *,
        call_default_factory: Literal[True],
        validated_data: dict[str, Any] | None = None,
    ) -> Any
    def get_default(*, call_default_factory: Literal[False] = ...) -> Any
    
Get the default value.

We expose an option for whether to call the default_factory (if present), as calling it may result in side effects that we want to avoid. However, there are times when it really should be called (namely, when instantiating a model via `model_construct`).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-9>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The default value, calling the default factory if requested or `None` if not set.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-4>)

**`call_default_factory`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr.get_default\(call_default_factory\)>)

Whether to call the default factory or not.

**`validated_data`** : [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr.get_default\(validated_data\)>)

The already validated data to be passed to the default factory.

## ComputedFieldInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo>)

A container for data from `@computed_field` so that we can access it while building the pydantic-core schema.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#attributes-2>)

#### decorator_repr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.decorator_repr>)

A class variable representing the decorator string, ‘@computed_field’.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### wrapped_property 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.wrapped_property>)

The wrapped computed field property.

**Type:** [`property`](<https://docs.python.org/3/library/functions.html#property>)

#### return_type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.return_type>)

The type of the computed field property’s return value.

**Type:** [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

#### alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.alias>)

The alias of the property to be used during serialization.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### alias_priority 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.alias_priority>)

The priority of the alias. This affects whether an alias generator is used.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### title 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.title>)

Title of the computed field to include in the serialization JSON schema.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### field_title_generator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.field_title_generator>)

A callable that takes a field name and returns title for it.

**Type:** [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `ComputedFieldInfo`], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### description 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.description>)

Description of the computed field to include in the serialization JSON schema.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### deprecated 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.deprecated>)

A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport, or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.

**Type:** `Deprecated` | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### examples 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.examples>)

Example values of the computed field to include in the serialization JSON schema.

**Type:** [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### json_schema_extra 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.json_schema_extra>)

A dict or callable to provide extra JSON schema properties.

**Type:** `JsonDict` | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`JsonDict`], [`None`](<https://docs.python.org/3/library/constants.html#None>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### repr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo.repr>)

A boolean indicating whether to include the field in the **repr** output.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#methods-2>)

#### _update_from_config 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo._update_from_config>)
    
    def _update_from_config(config_wrapper: ConfigWrapper, name: str) -> None
    
Update the instance from the configuration set on the class this computed field belongs to.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-10>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

#### _apply_alias_generator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo._apply_alias_generator>)
    
    def _apply_alias_generator(
        alias_generator: Callable[[str], str] | AliasGenerator,
        name: str,
    ) -> None
    
Apply an alias generator to aliases if appropriate.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-11>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-5>)

**`alias_generator`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`AliasGenerator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasGenerator>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo._apply_alias_generator\(alias_generator\)>)

A callable that takes a string and returns a string, or an `AliasGenerator` instance.

**`name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ComputedFieldInfo._apply_alias_generator\(name\)>)

The name of the computed field from which to generate the alias.

## Field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>)
    
    def Field(
        default: ellipsis,
        *,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        exclude_if: Callable[[Any], bool] | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | re.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
    ) -> Any
    def Field(
        default: Any,
        *,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        exclude_if: Callable[[Any], bool] | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: Literal[True],
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | re.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
    ) -> Any
    def Field(
        default: _T,
        *,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        exclude_if: Callable[[Any], bool] | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: Literal[False] = ...,
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | re.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
    ) -> _T
    def Field(
        *,
        default_factory: Callable[[], Any] | Callable[[dict[str, Any]], Any],
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        exclude_if: Callable[[Any], bool] | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: Literal[True],
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | re.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
    ) -> Any
    def Field(
        *,
        default_factory: Callable[[], _T] | Callable[[dict[str, Any]], _T],
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        exclude_if: Callable[[Any], bool] | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: Literal[False] | None = _Unset,
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | re.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
    ) -> _T
    def Field(
        *,
        alias: str | None = _Unset,
        alias_priority: int | None = _Unset,
        validation_alias: str | AliasPath | AliasChoices | None = _Unset,
        serialization_alias: str | None = _Unset,
        title: str | None = _Unset,
        field_title_generator: Callable[[str, FieldInfo], str] | None = _Unset,
        description: str | None = _Unset,
        examples: list[Any] | None = _Unset,
        exclude: bool | None = _Unset,
        exclude_if: Callable[[Any], bool] | None = _Unset,
        discriminator: str | types.Discriminator | None = _Unset,
        deprecated: Deprecated | str | bool | None = _Unset,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = _Unset,
        frozen: bool | None = _Unset,
        validate_default: bool | None = _Unset,
        repr: bool = _Unset,
        init: bool | None = _Unset,
        init_var: bool | None = _Unset,
        kw_only: bool | None = _Unset,
        pattern: str | re.Pattern[str] | None = _Unset,
        strict: bool | None = _Unset,
        coerce_numbers_to_str: bool | None = _Unset,
        gt: annotated_types.SupportsGt | None = _Unset,
        ge: annotated_types.SupportsGe | None = _Unset,
        lt: annotated_types.SupportsLt | None = _Unset,
        le: annotated_types.SupportsLe | None = _Unset,
        multiple_of: float | None = _Unset,
        allow_inf_nan: bool | None = _Unset,
        max_digits: int | None = _Unset,
        decimal_places: int | None = _Unset,
        min_length: int | None = _Unset,
        max_length: int | None = _Unset,
        union_mode: Literal['smart', 'left_to_right'] = _Unset,
        fail_fast: bool | None = _Unset,
        **extra: Unpack[_EmptyKwargs],
    ) -> Any
    
Create a field for objects that can be configured.

Used to provide extra information about a field, either for the model schema or complex validation. Some arguments apply only to number fields (`int`, `float`, `Decimal`) and some apply only to `str`.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-12>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — A new [`FieldInfo`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.FieldInfo>). The return annotation is `Any` so `Field` can be used on type-annotated fields without causing a type error.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-6>)

**`default`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `PydanticUndefined`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(default\)>)

Default value if the field is not set.

**`default_factory`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(default_factory\)>)

A callable to generate the default value. The callable can either take 0 arguments (in which case it is called as is) or a single argument containing the already validated data.

**`alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(alias\)>)

The name to use for the attribute when validating or serializing by alias. This is often used for things like converting between snake and camel case.

**`alias_priority`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(alias_priority\)>)

Priority of the alias. This affects whether an alias generator is used.

**`validation_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`AliasPath`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasPath>) | [`AliasChoices`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasChoices>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(validation_alias\)>)

Like `alias`, but only affects validation, not serialization.

**`serialization_alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(serialization_alias\)>)

Like `alias`, but only affects serialization, not validation.

**`title`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(title\)>)

Human-readable title.

**`field_title_generator`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `FieldInfo`], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(field_title_generator\)>)

A callable that takes a field name and returns title for it.

**`description`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(description\)>)

Human-readable description.

**`examples`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(examples\)>)

Example values for this field.

**`exclude`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(exclude\)>)

Whether to exclude the field from the model serialization.

**`exclude_if`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(exclude_if\)>)

A callable that determines whether to exclude a field during serialization based on its value.

**`discriminator`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`types.Discriminator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Discriminator>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(discriminator\)>)

Field name or Discriminator for discriminating the type in a tagged union.

**`deprecated`** : `Deprecated` | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(deprecated\)>)

A deprecation message, an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport, or a boolean. If `True`, a default deprecation message will be emitted when accessing the field.

**`json_schema_extra`** : `JsonDict` | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`JsonDict`], [`None`](<https://docs.python.org/3/library/constants.html#None>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(json_schema_extra\)>)

A dict or callable to provide extra JSON schema properties.

**`frozen`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(frozen\)>)

Whether the field is frozen. If true, attempts to change the value on an instance will raise an error.

**`validate_default`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(validate_default\)>)

If `True`, apply validation to the default value every time you create an instance. Otherwise, for performance reasons, the default value of the field is trusted and not validated.

**`repr`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(repr\)>)

A boolean indicating whether to include the field in the `__repr__` output.

**`init`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(init\)>)

Whether the field should be included in the constructor of the dataclass. (Only applies to dataclasses.)

**`init_var`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(init_var\)>)

Whether the field should _only_ be included in the constructor of the dataclass. (Only applies to dataclasses.)

**`kw_only`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(kw_only\)>)

Whether the field should be a keyword-only argument in the constructor of the dataclass. (Only applies to dataclasses.)

**`coerce_numbers_to_str`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(coerce_numbers_to_str\)>)

Whether to enable coercion of any `Number` type to `str` (not applicable in `strict` mode).

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(strict\)>)

If `True`, strict validation is applied to the field. See [Strict Mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>) for details.

**`gt`** : `annotated_types.SupportsGt` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(gt\)>)

Greater than. If set, value must be greater than this. Only applicable to numbers.

**`ge`** : `annotated_types.SupportsGe` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(ge\)>)

Greater than or equal. If set, value must be greater than or equal to this. Only applicable to numbers.

**`lt`** : `annotated_types.SupportsLt` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(lt\)>)

Less than. If set, value must be less than this. Only applicable to numbers.

**`le`** : `annotated_types.SupportsLe` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(le\)>)

Less than or equal. If set, value must be less than or equal to this. Only applicable to numbers.

**`multiple_of`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(multiple_of\)>)

Value must be a multiple of this. Only applicable to numbers.

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(min_length\)>)

Minimum length for iterables.

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(max_length\)>)

Maximum length for iterables.

**`pattern`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`re.Pattern`](<https://docs.python.org/3/library/re.html#re.Pattern>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(pattern\)>)

Pattern for strings (a regular expression).

**`allow_inf_nan`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(allow_inf_nan\)>)

Allow `inf`, `-inf`, `nan`. Only applicable to float and [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) numbers.

**`max_digits`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(max_digits\)>)

Maximum number of allow digits for strings.

**`decimal_places`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(decimal_places\)>)

Maximum number of decimal places allowed for numbers.

**`union_mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘smart’, ‘left_to_right’] _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(union_mode\)>)

The strategy to apply when validating a union. Can be `smart` (the default), or `left_to_right`. See [Union Mode](<https://pydantic.dev/docs/validation/latest/concepts/unions#union-modes>) for details.

**`fail_fast`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_Unset`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(fail_fast\)>)

If `True`, validation will stop on the first error. If `False`, all validation errors will be collected. This option can be applied only to iterable types (list, tuple, set, and frozenset).

**`extra`** : [`Unpack`](<https://docs.python.org/3/library/typing.html#typing.Unpack>)[`_EmptyKwargs`] _Default:_ `{}`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field\(extra\)>)

(Deprecated) Extra fields that will be included in the JSON schema.

## PrivateAttr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.PrivateAttr>)
    
    def PrivateAttr(default: _T, *, init: Literal[False] = False) -> _T
    def PrivateAttr(
        *,
        default_factory: Callable[[], _T] | Callable[[dict[str, Any]], _T],
        init: Literal[False] = False,
    ) -> _T
    def PrivateAttr(*, init: Literal[False] = False) -> Any
    
Indicates that an attribute is intended for private use and not handled during normal validation/serialization.

Private attributes are not validated by Pydantic, so it’s up to you to ensure they are used in a type-safe manner.

Private attributes are stored in `__private_attributes__` on the model.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-13>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — An instance of [`ModelPrivateAttr`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.ModelPrivateAttr>) class.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-7>)

**`default`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `PydanticUndefined`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.PrivateAttr\(default\)>)

The attribute’s default value. Defaults to Undefined.

**`default_factory`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.PrivateAttr\(default_factory\)>)

A callable to generate the default value. The callable can either take 0 arguments (in which case it is called as is) or a single argument containing the validated data (the model’s [`__dict__`](<https://docs.python.org/3/reference/datamodel.html#object.__dict__>)) and the already initialized private attributes. If both `default` and `default_factory` are set, an error will be raised.

**`init`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[[`False`](<https://docs.python.org/3/library/constants.html#False>)] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.PrivateAttr\(init\)>)

Whether the attribute should be included in the constructor of the dataclass. Always `False`.

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#raises-1>)

  * `ValueError` — If both `default` and `default_factory` are set.

## computed_field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field>)
    
    def computed_field(func: PropertyT, /) -> PropertyT
    def computed_field(
        *,
        alias: str | None = None,
        alias_priority: int | None = None,
        exclude_if: Callable[[Any], bool] | None = None,
        title: str | None = None,
        field_title_generator: Callable[[str, ComputedFieldInfo], str] | None = None,
        description: str | None = None,
        deprecated: Deprecated | str | bool | None = None,
        examples: list[Any] | None = None,
        json_schema_extra: JsonDict | Callable[[JsonDict], None] | None = None,
        repr: bool = True,
        return_type: Any = PydanticUndefined,
    ) -> Callable[[PropertyT], PropertyT]
    
Decorator to include `property` and `cached_property` when serializing models or dataclasses.

This is useful for fields that are computed from other fields, or for fields that are expensive to compute and should be cached.
    
    from pydantic import BaseModel, computed_field
    
    class Rectangle(BaseModel):
        width: int
        length: int
    
        @computed_field
        @property
        def area(self) -> int:
            return self.width * self.length
    
    print(Rectangle(width=3, length=2).model_dump())
    #> {'width': 3, 'length': 2, 'area': 6}
    
If applied to functions not yet decorated with `@property` or `@cached_property`, the function is automatically wrapped with `property`. Although this is more concise, you will lose IntelliSense in your IDE, and confuse static type checkers, thus explicit use of `@property` is recommended.
    
    import random
    
    from pydantic import BaseModel, computed_field
    
    class Square(BaseModel):
        width: float
    
        @computed_field
        def area(self) -> float:  # converted to a `property` by `computed_field`
            return round(self.width**2, 2)
    
        @area.setter
        def area(self, new_area: float) -> None:
            self.width = new_area**0.5
    
        @computed_field(alias='the magic number', repr=False)
        def random_number(self) -> int:
            return random.randint(0, 1_000)
    
    square = Square(width=1.3)
    
    # `random_number` does not appear in representation
    print(repr(square))
    #> Square(width=1.3, area=1.69)
    
    print(square.random_number)
    #> 3
    
    square.area = 4
    
    print(square.model_dump_json(by_alias=True))
    #> {"width":2.0,"area":4.0,"the magic number":3}
    
    from pydantic import BaseModel, computed_field
    
    class Parent(BaseModel):
        a: str
    
    try:
    
        class Child(Parent):
            @computed_field
            @property
            def a(self) -> str:
                return 'new a'
    
    except TypeError as e:
        print(e)
        '''
        Field 'a' of class 'Child' overrides symbol of same name in a parent class. This override with a computed_field is incompatible.
        '''
    
Private properties decorated with `@computed_field` have `repr=False` by default.
    
    from functools import cached_property
    
    from pydantic import BaseModel, computed_field
    
    class Model(BaseModel):
        foo: int
    
        @computed_field
        @cached_property
        def _private_cached_property(self) -> int:
            return -self.foo
    
        @computed_field
        @property
        def _private_property(self) -> int:
            return -self.foo
    
    m = Model(foo=1)
    print(repr(m))
    #> Model(foo=1)
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#returns-14>)

`PropertyT` | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`PropertyT`], `PropertyT`] — A proxy wrapper for the property.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#parameters-8>)

**`func`** : `PropertyT` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(func\)>)

the function to wrap.

**`alias`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(alias\)>)

alias to use when serializing this computed field, only used when `by_alias=True`

**`alias_priority`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(alias_priority\)>)

priority of the alias. This affects whether an alias generator is used

**`exclude_if`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(exclude_if\)>)

A callable that determines whether to exclude this computed field during serialization based on its value.

**`title`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(title\)>)

Title to use when including this computed field in JSON Schema

**`field_title_generator`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `ComputedFieldInfo`], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(field_title_generator\)>)

A callable that takes a field name and returns title for it.

**`description`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(description\)>)

Description to use when including this computed field in JSON Schema, defaults to the function’s docstring

**`deprecated`** : `Deprecated` | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(deprecated\)>)

A deprecation message (or an instance of `warnings.deprecated` or the `typing_extensions.deprecated` backport). to be emitted when accessing the field. Or a boolean. This will automatically be set if the property is decorated with the `deprecated` decorator.

**`examples`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(examples\)>)

Example values to use when including this computed field in JSON Schema

**`json_schema_extra`** : `JsonDict` | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`JsonDict`], [`None`](<https://docs.python.org/3/library/constants.html#None>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(json_schema_extra\)>)

A dict or callable to provide extra JSON schema properties.

**`repr`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(repr\)>)

whether to include this computed field in model repr. Default is `False` for private properties and `True` for public properties.

**`return_type`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `PydanticUndefined`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.computed_field\(return_type\)>)

optional return for serialization logic to expect when serializing to JSON, if included this must be correct, otherwise a `TypeError` is raised. If you don’t include a return type Any is used, which does runtime introspection to handle arbitrary objects.

Was this page helpful?

Thanks for your feedback!