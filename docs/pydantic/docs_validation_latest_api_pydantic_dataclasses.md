# Pydantic Dataclasses | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/](https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Pydantic Dataclasses

Provide an enhanced dataclass that performs validation.

## dataclass 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass>)
    
    def dataclass(
        *,
        init: Literal[False] = False,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool = False,
        config: ConfigDict | type[object] | None = None,
        validate_on_init: bool | None = None,
        kw_only: bool = ...,
        slots: bool = ...,
    ) -> Callable[[type[_T]], type[PydanticDataclass]]
    def dataclass(
        _cls: type[_T],
        *,
        init: Literal[False] = False,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool | None = None,
        config: ConfigDict | type[object] | None = None,
        validate_on_init: bool | None = None,
        kw_only: bool = ...,
        slots: bool = ...,
    ) -> type[PydanticDataclass]
    def dataclass(
        *,
        init: Literal[False] = False,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool | None = None,
        config: ConfigDict | type[object] | None = None,
        validate_on_init: bool | None = None,
    ) -> Callable[[type[_T]], type[PydanticDataclass]]
    def dataclass(
        _cls: type[_T],
        *,
        init: Literal[False] = False,
        repr: bool = True,
        eq: bool = True,
        order: bool = False,
        unsafe_hash: bool = False,
        frozen: bool | None = None,
        config: ConfigDict | type[object] | None = None,
        validate_on_init: bool | None = None,
    ) -> type[PydanticDataclass]
    
A decorator used to create a Pydantic-enhanced dataclass, similar to the standard Python `dataclass`, but with added validation.

This function should be used similarly to `dataclasses.dataclass`.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#returns>)

[`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`type`](<https://docs.python.org/3/glossary.html#term-type>)[`_T`]], [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`PydanticDataclass`]] | [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`PydanticDataclass`] — A decorator that accepts a class as its argument and returns a Pydantic `dataclass`.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#parameters>)

**`_cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`_T`] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(_cls\)>)

The target `dataclass`.

**`init`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[[`False`](<https://docs.python.org/3/library/constants.html#False>)] _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(init\)>)

Included for signature compatibility with `dataclasses.dataclass`, and is passed through to `dataclasses.dataclass` when appropriate. If specified, must be set to `False`, as pydantic inserts its own `__init__` function.

**`repr`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(repr\)>)

A boolean indicating whether to include the field in the `__repr__` output.

**`eq`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(eq\)>)

Determines if a `__eq__` method should be generated for the class.

**`order`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(order\)>)

Determines if comparison magic methods should be generated, such as `__lt__`, but not `__eq__`.

**`unsafe_hash`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(unsafe_hash\)>)

Determines if a `__hash__` method should be included in the class, as in `dataclasses.dataclass`.

**`frozen`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(frozen\)>)

Determines if the generated class should be a ‘frozen’ `dataclass`, which does not allow its attributes to be modified after it has been initialized. If not set, the value from the provided `config` argument will be used (and will default to `False` otherwise).

**`config`** : [`ConfigDict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict>) | [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`object`](<https://docs.python.org/3/glossary.html#term-object>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(config\)>)

The Pydantic config to use for the `dataclass`.

**`validate_on_init`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(validate_on_init\)>)

A deprecated parameter included for backwards compatibility; in V2, all Pydantic dataclasses are validated on init.

**`kw_only`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(kw_only\)>)

Determines if `__init__` method parameters must be specified by keyword only. Defaults to `False`.

**`slots`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.dataclass\(slots\)>)

Determines if the generated class should be a ‘slots’ `dataclass`, which does not allow the addition of new attributes after instantiation.

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#raises>)

  * `AssertionError` — Raised if `init` is not `False` or `validate_on_init` is `False`.

## rebuild_dataclass 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.rebuild_dataclass>)
    
    def rebuild_dataclass(
        cls: type[PydanticDataclass],
        *,
        force: bool = False,
        raise_errors: bool = True,
        _parent_namespace_depth: int = 2,
        _types_namespace: MappingNamespace | None = None,
    ) -> bool | None
    
Try to rebuild the pydantic-core schema for the dataclass.

This may be necessary when one of the annotations is a ForwardRef which could not be resolved during the initial attempt to build the schema, and automatic rebuilding fails.

This is analogous to `BaseModel.model_rebuild`.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#returns-1>)

[`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) — Returns `None` if the schema is already “complete” and rebuilding was not required. [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) — If rebuilding _was_ required, returns `True` if rebuilding was successful, otherwise `False`.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#parameters-1>)

**`cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`PydanticDataclass`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.rebuild_dataclass\(cls\)>)

The class to rebuild the pydantic-core schema for.

**`force`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.rebuild_dataclass\(force\)>)

Whether to force the rebuilding of the schema, defaults to `False`.

**`raise_errors`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.rebuild_dataclass\(raise_errors\)>)

Whether to raise errors, defaults to `True`.

**`_parent_namespace_depth`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) _Default:_ `2`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.rebuild_dataclass\(_parent_namespace_depth\)>)

The depth level of the parent namespace, defaults to 2.

**`_types_namespace`** : `MappingNamespace` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.rebuild_dataclass\(_types_namespace\)>)

The types namespace, defaults to `None`.

## is_pydantic_dataclass 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.is_pydantic_dataclass>)
    
    def is_pydantic_dataclass(class_: type[Any], /) -> TypeGuard[type[PydanticDataclass]]
    
Whether a class is a pydantic dataclass.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#returns-2>)

[`TypeGuard`](<https://docs.python.org/3/library/typing.html#typing.TypeGuard>)[[`type`](<https://docs.python.org/3/glossary.html#term-type>)[`PydanticDataclass`]] — `True` if the class is a pydantic dataclass, `False` otherwise.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#parameters-2>)

**`class_`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/dataclasses/#pydantic.dataclasses.is_pydantic_dataclass\(class_\)>)

The class.

Was this page helpful?

Thanks for your feedback!