# Functional Serializers | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/](https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Functional Serializers

This module contains related classes and functions for serialization.

## PlainSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.PlainSerializer>)

Plain serializers use a function to modify the output of serialization.

This is particularly helpful when you want to customize the serialization for annotated types. Consider an input of `list`, which will be serialized into a space-delimited string.
    
    from typing import Annotated
    
    from pydantic import BaseModel, PlainSerializer
    
    CustomStr = Annotated[
        list, PlainSerializer(lambda x: ' '.join(x), return_type=str)
    ]
    
    class StudentModel(BaseModel):
        courses: CustomStr
    
    student = StudentModel(courses=['Math', 'Chemistry', 'English'])
    print(student.model_dump())
    #> {'courses': 'Math Chemistry English'}
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#attributes>)

#### func 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.PlainSerializer.func>)

The serializer function.

**Type:** `core_schema.SerializerFunction`

#### return_type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.PlainSerializer.return_type>)

The return type for the function. If omitted it will be inferred from the type annotation.

**Type:** [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

#### when_used 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.PlainSerializer.when_used>)

Determines when this serializer should be used. Accepts a string with values `'always'`, `'unless-none'`, `'json'`, and `'json-unless-none'`. Defaults to ‘always’.

**Type:** `WhenUsed`

## WrapSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.WrapSerializer>)

Wrap serializers receive the raw inputs along with a handler function that applies the standard serialization logic, and can modify the resulting value before returning it as the final output of serialization.

For example, here’s a scenario in which a wrap serializer transforms timezones to UTC **and** utilizes the existing `datetime` serialization logic.
    
    from datetime import datetime, timezone
    from typing import Annotated, Any
    
    from pydantic import BaseModel, WrapSerializer
    
    class EventDatetime(BaseModel):
        start: datetime
        end: datetime
    
    def convert_to_utc(value: Any, handler, info) -> dict[str, datetime]:
        # Note that `handler` can actually help serialize the `value` for
        # further custom serialization in case it's a subclass.
        partial_result = handler(value, info)
        if info.mode == 'json':
            return {
                k: datetime.fromisoformat(v).astimezone(timezone.utc)
                for k, v in partial_result.items()
            }
        return {k: v.astimezone(timezone.utc) for k, v in partial_result.items()}
    
    UTCEventDatetime = Annotated[EventDatetime, WrapSerializer(convert_to_utc)]
    
    class EventModel(BaseModel):
        event_datetime: UTCEventDatetime
    
    dt = EventDatetime(
        start='2024-01-01T07:00:00-08:00', end='2024-01-03T20:00:00+06:00'
    )
    event = EventModel(event_datetime=dt)
    print(event.model_dump())
    '''
    {
        'event_datetime': {
            'start': datetime.datetime(
                2024, 1, 1, 15, 0, tzinfo=datetime.timezone.utc
            ),
            'end': datetime.datetime(
                2024, 1, 3, 14, 0, tzinfo=datetime.timezone.utc
            ),
        }
    }
    '''
    
    print(event.model_dump_json())
    '''
    {"event_datetime":{"start":"2024-01-01T15:00:00Z","end":"2024-01-03T14:00:00Z"}}
    '''
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#attributes-1>)

#### func 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.WrapSerializer.func>)

The serializer function to be wrapped.

**Type:** `core_schema.WrapSerializerFunction`

#### return_type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.WrapSerializer.return_type>)

The return type for the function. If omitted it will be inferred from the type annotation.

**Type:** [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

#### when_used 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.WrapSerializer.when_used>)

Determines when this serializer should be used. Accepts a string with values `'always'`, `'unless-none'`, `'json'`, and `'json-unless-none'`. Defaults to ‘always’.

**Type:** `WhenUsed`

## SerializeAsAny 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.SerializeAsAny>)

Annotation used to mark a type as having duck-typing serialization behavior.

See [usage documentation](<https://pydantic.dev/docs/validation/latest/concepts/serialization#serializing-with-duck-typing>) for more details.

## field_serializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer>)
    
    def field_serializer(
        field: str,
        /,
        *fields: str,
        mode: Literal['wrap'],
        return_type: Any = ...,
        when_used: WhenUsed = ...,
        check_fields: bool | None = ...,
    ) -> Callable[[_FieldWrapSerializerT], _FieldWrapSerializerT]
    def field_serializer(
        field: str,
        /,
        *fields: str,
        mode: Literal['plain'] = ...,
        return_type: Any = ...,
        when_used: WhenUsed = ...,
        check_fields: bool | None = ...,
    ) -> Callable[[_FieldPlainSerializerT], _FieldPlainSerializerT]
    
Decorator that enables custom field serialization.

In the below example, a field of type `set` is used to mitigate duplication. A `field_serializer` is used to serialize the data as a sorted list.
    
    from pydantic import BaseModel, field_serializer
    
    class StudentModel(BaseModel):
        name: str = 'Jane'
        courses: set[str]
    
        @field_serializer('courses', when_used='json')
        def serialize_courses_in_order(self, courses: set[str]):
            return sorted(courses)
    
    student = StudentModel(courses={'Math', 'Chemistry', 'English'})
    print(student.model_dump_json())
    #> {"name":"Jane","courses":["Chemistry","English","Math"]}
    
See [the usage documentation](<https://pydantic.dev/docs/validation/latest/concepts/serialization#serializers>) for more information.

Four signatures are supported for the decorated serializer:

  * `(self, value: Any, info: FieldSerializationInfo)`
  * `(self, value: Any, nxt: SerializerFunctionWrapHandler, info: FieldSerializationInfo)`
  * `(value: Any, info: SerializationInfo)`
  * `(value: Any, nxt: SerializerFunctionWrapHandler, info: SerializationInfo)`

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#returns>)

[`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`_FieldWrapSerializerT`], `_FieldWrapSerializerT`] | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`_FieldPlainSerializerT`], `_FieldPlainSerializerT`]

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#parameters>)

**`*fields`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `()`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer\(*fields\)>)

The field names the serializer should apply to.

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘plain’, ‘wrap’] _Default:_ `'plain'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer\(mode\)>)

The serialization mode.

  * `plain` means the function will be called instead of the default serialization logic,
  * `wrap` means the function will be called with an argument to optionally call the default serialization logic.

**`return_type`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `PydanticUndefined`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer\(return_type\)>)

Optional return type for the function, if omitted it will be inferred from the type annotation.

**`when_used`** : `WhenUsed` _Default:_ `'always'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer\(when_used\)>)

Determines the serializer will be used for serialization.

**`check_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer\(check_fields\)>)

Whether to check that the fields actually exist on the model.

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#raises>)

  * `PydanticUserError` —
  * If the decorator is used without any arguments (at least one field name must be provided).
  * If the provided field names are not strings.

## model_serializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.model_serializer>)
    
    def model_serializer(f: _ModelPlainSerializerT, /) -> _ModelPlainSerializerT
    def model_serializer(
        *,
        mode: Literal['wrap'],
        when_used: WhenUsed = 'always',
        return_type: Any = ...,
    ) -> Callable[[_ModelWrapSerializerT], _ModelWrapSerializerT]
    def model_serializer(
        *,
        mode: Literal['plain'] = ...,
        when_used: WhenUsed = 'always',
        return_type: Any = ...,
    ) -> Callable[[_ModelPlainSerializerT], _ModelPlainSerializerT]
    
Decorator that enables custom model serialization.

This is useful when a model need to be serialized in a customized manner, allowing for flexibility beyond just specific fields.

An example would be to serialize temperature to the same temperature scale, such as degrees Celsius.
    
    from typing import Literal
    
    from pydantic import BaseModel, model_serializer
    
    class TemperatureModel(BaseModel):
        unit: Literal['C', 'F']
        value: int
    
        @model_serializer()
        def serialize_model(self):
            if self.unit == 'F':
                return {'unit': 'C', 'value': int((self.value - 32) / 1.8)}
            return {'unit': self.unit, 'value': self.value}
    
    temperature = TemperatureModel(unit='F', value=212)
    print(temperature.model_dump())
    #> {'unit': 'C', 'value': 100}
    
Two signatures are supported for `mode='plain'`, which is the default:

  * `(self)`
  * `(self, info: SerializationInfo)`

And two other signatures for `mode='wrap'`:

  * `(self, nxt: SerializerFunctionWrapHandler)`

  * `(self, nxt: SerializerFunctionWrapHandler, info: SerializationInfo)`

See [the usage documentation](<https://pydantic.dev/docs/validation/latest/concepts/serialization#serializers>) for more information.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#returns-1>)

`_ModelPlainSerializerT` | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`_ModelWrapSerializerT`], `_ModelWrapSerializerT`] | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`_ModelPlainSerializerT`], `_ModelPlainSerializerT`] — The decorator function.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#parameters-1>)

**`f`** : `_ModelPlainSerializerT` | `_ModelWrapSerializerT` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.model_serializer\(f\)>)

The function to be decorated.

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘plain’, ‘wrap’] _Default:_ `'plain'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.model_serializer\(mode\)>)

The serialization mode.

  * `'plain'` means the function will be called instead of the default serialization logic
  * `'wrap'` means the function will be called with an argument to optionally call the default serialization logic.

**`when_used`** : `WhenUsed` _Default:_ `'always'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.model_serializer\(when_used\)>)

Determines when this serializer should be used.

**`return_type`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `PydanticUndefined`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.model_serializer\(return_type\)>)

The return type for the function. If omitted it will be inferred from the type annotation.

## FieldPlainSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.FieldPlainSerializer>)

A field serializer method or function in `plain` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `'core_schema.SerializerFunction | _Partial'`

## FieldWrapSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.FieldWrapSerializer>)

A field serializer method or function in `wrap` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `'core_schema.WrapSerializerFunction | _Partial'`

## FieldSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.FieldSerializer>)

A field serializer method or function.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `'FieldPlainSerializer | FieldWrapSerializer'`

## ModelPlainSerializerWithInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.ModelPlainSerializerWithInfo>)

A model serializer method with the `info` argument, in `plain` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `Callable[[Any, SerializationInfo[Any]], Any]`

## ModelPlainSerializerWithoutInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.ModelPlainSerializerWithoutInfo>)

A model serializer method without the `info` argument, in `plain` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `Callable[[Any], Any]`

## ModelPlainSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.ModelPlainSerializer>)

A model serializer method in `plain` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `'ModelPlainSerializerWithInfo | ModelPlainSerializerWithoutInfo'`

## ModelWrapSerializerWithInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.ModelWrapSerializerWithInfo>)

A model serializer method with the `info` argument, in `wrap` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `Callable[[Any, SerializerFunctionWrapHandler, SerializationInfo[Any]], Any]`

## ModelWrapSerializerWithoutInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.ModelWrapSerializerWithoutInfo>)

A model serializer method without the `info` argument, in `wrap` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `Callable[[Any, SerializerFunctionWrapHandler], Any]`

## ModelWrapSerializer 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.ModelWrapSerializer>)

A model serializer method in `wrap` mode.

**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `'ModelWrapSerializerWithInfo | ModelWrapSerializerWithoutInfo'`

Was this page helpful?

Thanks for your feedback!