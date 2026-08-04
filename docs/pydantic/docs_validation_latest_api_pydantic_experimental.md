# Experimental | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/](https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Experimental

## Pipeline API

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pipeline-api>)

Experimental pipeline API functionality. Be careful with this API, it’s subject to change.

## _Pipeline 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline>)

**Bases:** `Generic[_InT, _OutT]`

Abstract representation of a chain of validation, transformation, and parsing steps.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#methods>)

#### transform 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.transform>)
    
    def transform(func: Callable[[_OutT], _NewOutT]) -> _Pipeline[_InT, _NewOutT]
    
Transform the output of the previous step.

If used as the first step in a pipeline, the type of the field is used. That is, the transformation is applied to after the value is parsed to the field’s type.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns>)

`_Pipeline`[`_InT`, `_NewOutT`]

#### validate_as 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.validate_as>)
    
    def validate_as(
        tp: type[_NewOutT],
        *,
        strict: bool = False,
    ) -> _Pipeline[_InT, _NewOutT]
    def validate_as(tp: ellipsis, *, strict: bool = False) -> _Pipeline[_InT, Any]
    def validate_as(tp: Any, *, strict: bool = ...) -> _Pipeline[_InT, Any]
    
Validate / parse the input into a new type.

If no type is provided, the type of the field is used.

Types are parsed in Pydantic’s `lax` mode by default, but you can enable `strict` mode by passing `strict=True`.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-1>)

`_Pipeline`[`_InT`, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]

#### validate_as_deferred 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.validate_as_deferred>)
    
    def validate_as_deferred(
        func: Callable[[], type[_NewOutT]],
    ) -> _Pipeline[_InT, _NewOutT]
    
Parse the input into a new type, deferring resolution of the type until the current class is fully defined.

This is useful when you need to reference the class in it’s own type annotations.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-2>)

`_Pipeline`[`_InT`, `_NewOutT`]

#### constrain 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.constrain>)
    
    def constrain(constraint: annotated_types.Ge) -> _Pipeline[_InT, _NewOutGe]
    def constrain(constraint: annotated_types.Gt) -> _Pipeline[_InT, _NewOutGt]
    def constrain(constraint: annotated_types.Le) -> _Pipeline[_InT, _NewOutLe]
    def constrain(constraint: annotated_types.Lt) -> _Pipeline[_InT, _NewOutLt]
    def constrain(constraint: annotated_types.Len) -> _Pipeline[_InT, _NewOutLen]
    def constrain(constraint: annotated_types.MultipleOf) -> _Pipeline[_InT, _NewOutT]
    def constrain(constraint: annotated_types.Timezone) -> _Pipeline[_InT, _NewOutDatetime]
    def constrain(constraint: annotated_types.Predicate) -> _Pipeline[_InT, _OutT]
    def constrain(constraint: annotated_types.Interval) -> _Pipeline[_InT, _NewOutInterval]
    def constrain(constraint: _Eq) -> _Pipeline[_InT, _OutT]
    def constrain(constraint: _NotEq) -> _Pipeline[_InT, _OutT]
    def constrain(constraint: _In) -> _Pipeline[_InT, _OutT]
    def constrain(constraint: _NotIn) -> _Pipeline[_InT, _OutT]
    def constrain(constraint: Pattern[str]) -> _Pipeline[_InT, _NewOutT]
    
Constrain a value to meet a certain condition.

We support most conditions from `annotated_types`, as well as regular expressions.

Most of the time you’ll be calling a shortcut method like `gt`, `lt`, `len`, etc so you don’t need to call this directly.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-3>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

#### predicate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.predicate>)
    
    def predicate(func: Callable[[_NewOutT], bool]) -> _Pipeline[_InT, _NewOutT]
    
Constrain a value to meet a certain predicate.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-4>)

`_Pipeline`[`_InT`, `_NewOutT`]

#### gt 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.gt>)
    
    def gt(gt: _NewOutGt) -> _Pipeline[_InT, _NewOutGt]
    
Constrain a value to be greater than a certain value.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-5>)

`_Pipeline`[`_InT`, `_NewOutGt`]

#### lt 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.lt>)
    
    def lt(lt: _NewOutLt) -> _Pipeline[_InT, _NewOutLt]
    
Constrain a value to be less than a certain value.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-6>)

`_Pipeline`[`_InT`, `_NewOutLt`]

#### ge 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.ge>)
    
    def ge(ge: _NewOutGe) -> _Pipeline[_InT, _NewOutGe]
    
Constrain a value to be greater than or equal to a certain value.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-7>)

`_Pipeline`[`_InT`, `_NewOutGe`]

#### le 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.le>)
    
    def le(le: _NewOutLe) -> _Pipeline[_InT, _NewOutLe]
    
Constrain a value to be less than or equal to a certain value.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-8>)

`_Pipeline`[`_InT`, `_NewOutLe`]

#### len 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.len>)
    
    def len(min_len: int, max_len: int | None = None) -> _Pipeline[_InT, _NewOutLen]
    
Constrain a value to have a certain length.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-9>)

`_Pipeline`[`_InT`, `_NewOutLen`]

#### multiple_of 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.multiple_of>)
    
    def multiple_of(multiple_of: _NewOutDiv) -> _Pipeline[_InT, _NewOutDiv]
    def multiple_of(multiple_of: _NewOutMod) -> _Pipeline[_InT, _NewOutMod]
    
Constrain a value to be a multiple of a certain number.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-10>)

`_Pipeline`[`_InT`, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]

#### eq 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.eq>)
    
    def eq(value: _OutT) -> _Pipeline[_InT, _OutT]
    
Constrain a value to be equal to a certain value.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-11>)

`_Pipeline`[`_InT`, `_OutT`]

#### not_eq 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.not_eq>)
    
    def not_eq(value: _OutT) -> _Pipeline[_InT, _OutT]
    
Constrain a value to not be equal to a certain value.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-12>)

`_Pipeline`[`_InT`, `_OutT`]

#### in_ 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.in_>)
    
    def in_(values: Container[_OutT]) -> _Pipeline[_InT, _OutT]
    
Constrain a value to be in a certain set.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-13>)

`_Pipeline`[`_InT`, `_OutT`]

#### not_in 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.not_in>)
    
    def not_in(values: Container[_OutT]) -> _Pipeline[_InT, _OutT]
    
Constrain a value to not be in a certain set.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-14>)

`_Pipeline`[`_InT`, `_OutT`]

#### otherwise 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.otherwise>)
    
    def otherwise(
        other: _Pipeline[_OtherIn, _OtherOut],
    ) -> _Pipeline[_InT | _OtherIn, _OutT | _OtherOut]
    
Combine two validation chains, returning the result of the first chain if it succeeds, and the second chain if it fails.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-15>)

`_Pipeline`[`_InT` | `_OtherIn`, `_OutT` | `_OtherOut`]

#### then 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.pipeline._Pipeline.then>)
    
    def then(other: _Pipeline[_OutT, _OtherOut]) -> _Pipeline[_InT, _OtherOut]
    
Pipe the result of one validation chain into another.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-16>)

`_Pipeline`[`_InT`, `_OtherOut`]

## Arguments schema API

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#arguments-schema-api>)

Experimental module exposing a function to generate a core schema that validates callable arguments.

## generate_arguments_schema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.arguments_schema.generate_arguments_schema>)
    
    def generate_arguments_schema(
        func: Callable[..., Any],
        schema_type: Literal['arguments', 'arguments-v3'] = 'arguments-v3',
        parameters_callback: Callable[[int, str, Any], Literal['skip'] | None] | None = None,
        config: ConfigDict | None = None,
    ) -> CoreSchema
    
Generate the schema for the arguments of a function.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#returns-17>)

`CoreSchema` — The generated schema.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#parameters>)

**`func`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.arguments_schema.generate_arguments_schema\(func\)>)

The function to generate the schema for.

**`schema_type`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘arguments’, ‘arguments-v3’] _Default:_ `'arguments-v3'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.arguments_schema.generate_arguments_schema\(schema_type\)>)

The type of schema to generate.

**`parameters_callback`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`int`](<https://docs.python.org/3/library/functions.html#int>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘skip’] | [`None`](<https://docs.python.org/3/library/constants.html#None>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.arguments_schema.generate_arguments_schema\(parameters_callback\)>)

A callable that will be invoked for each parameter. The callback should take three required arguments: the index, the name and the type annotation (or [`Parameter.empty`](<https://docs.python.org/3/library/inspect.html#inspect.Parameter.empty>) if not annotated) of the parameter. The callback can optionally return `'skip'`, so that the parameter gets excluded from the resulting schema.

**`config`** : [`ConfigDict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/experimental/#pydantic.experimental.arguments_schema.generate_arguments_schema\(config\)>)

The configuration to use.

Was this page helpful?

Thanks for your feedback!