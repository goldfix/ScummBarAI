# Configuration | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/config/](https://pydantic.dev/docs/validation/latest/api/pydantic/config/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Configuration

Configuration for Pydantic models.

## ConfigDict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict>)

**Bases:** [`TypedDict`](<https://docs.python.org/3/library/typing.html#typing.TypedDict>)

A TypedDict for configuring Pydantic behaviour.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#attributes>)

#### title 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.title>)

The title for the generated JSON schema, defaults to the model’s name

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### model_title_generator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.model_title_generator>)

A callable that takes a model class and returns the title for it. Defaults to `None`.

**Type:** [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`type`](<https://docs.python.org/3/glossary.html#term-type>)], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### field_title_generator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.field_title_generator>)

A callable that takes a field’s name and info and returns title for it. Defaults to `None`.

**Type:** [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `FieldInfo` | `ComputedFieldInfo`], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### str_to_lower 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.str_to_lower>)

Whether to convert all characters to lowercase for str types. Defaults to `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### str_to_upper 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.str_to_upper>)

Whether to convert all characters to uppercase for str types. Defaults to `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### str_strip_whitespace 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.str_strip_whitespace>)

Whether to strip leading and trailing whitespace for str types.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### str_min_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.str_min_length>)

The minimum length for str types. Defaults to `None`.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>)

#### str_max_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.str_max_length>)

The maximum length for str types. Defaults to `None`.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### extra 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.extra>)

Whether to ignore, allow, or forbid extra data during model initialization. Defaults to `'ignore'`.

Three configuration values are available:

  * `'ignore'`: Providing extra data is ignored (the default):

    from pydantic import BaseModel, ConfigDict
    
    class User(BaseModel):
      model_config = ConfigDict(extra='ignore')  # (1)
    
      name: str
    
    user = User(name='John Doe', age=20)  # (2)
    print(user)
    #> name='John Doe'

This is the default behaviour.

The `age` argument is ignored.

  * `'forbid'`: Providing extra data is not permitted, and a [`ValidationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError>) will be raised if this is the case:
        
        from pydantic import BaseModel, ConfigDict, ValidationError
        
        class Model(BaseModel):
            x: int
        
            model_config = ConfigDict(extra='forbid')
        
        try:
            Model(x=1, y='a')
        except ValidationError as exc:
            print(exc)
            """
            1 validation error for Model
            y
              Extra inputs are not permitted [type=extra_forbidden, input_value='a', input_type=str]
            """
        
  * `'allow'`: Providing extra data is allowed and stored in the `__pydantic_extra__` dictionary attribute:
        
        from pydantic import BaseModel, ConfigDict
        
        class Model(BaseModel):
            x: int
        
            model_config = ConfigDict(extra='allow')
        
        m = Model(x=1, y='a')
        assert m.__pydantic_extra__ == {'y': 'a'}
        
By default, no validation will be applied to these extra items, but you can set a type for the values by overriding the type annotation for `__pydantic_extra__`:

    from pydantic import BaseModel, ConfigDict, Field, ValidationError
    
    class Model(BaseModel):
      __pydantic_extra__: dict[str, int] = Field(init=False)  # (1)
    
      x: int
    
      model_config = ConfigDict(extra='allow')
    
    try:
      Model(x=1, y='a')
    except ValidationError as exc:
      print(exc)
      """
      1 validation error for Model
      y
        Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
      """
    
    m = Model(x=1, y='2')
    assert m.x == 1
    assert m.y == 2
    assert m.model_dump() == {'x': 1, 'y': 2}
    assert m.__pydantic_extra__ == {'y': 2}

The `= Field(init=False)` does not have any effect at runtime, but prevents the `__pydantic_extra__` field from being included as a parameter to the model's `__init__` method by type checkers.

As well as specifying an `extra` configuration value on the model, you can also provide it as an argument to the validation methods. This will override any `extra` configuration value set on the model:
    
    from pydantic import BaseModel, ConfigDict, ValidationError
    
    class Model(BaseModel):
        x: int
        model_config = ConfigDict(extra="allow")
    
    try:
        # Override model config and forbid extra fields just this time
        Model.model_validate({"x": 1, "y": 2}, extra="forbid")
    except ValidationError as exc:
        print(exc)
        """
        1 validation error for Model
        y
          Extra inputs are not permitted [type=extra_forbidden, input_value=2, input_type=int]
        """
    
**Type:** `ExtraValues` | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### frozen 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.frozen>)

Whether models are faux-immutable, i.e. whether `__setattr__` is allowed, and also generates a `__hash__()` method for the model. This makes instances of the model potentially hashable if all the attributes are hashable. Defaults to `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### populate_by_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.populate_by_name>)

Whether an aliased field may be populated by its name as given by the model attribute, as well as the alias. Defaults to `False`.
    
    from pydantic import BaseModel, ConfigDict, Field
    
    class Model(BaseModel):
      model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    
      my_field: str = Field(alias='my_alias')  # (1)
    
    m = Model(my_alias='foo')  # (2)
    print(m)
    #> my_field='foo'
    
    m = Model(my_field='foo')  # (3)
    print(m)
    #> my_field='foo'

The field `'my_field'` has an alias `'my_alias'`.

The model is populated by the alias `'my_alias'`.

The model is populated by the attribute name `'my_field'`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### use_enum_values 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.use_enum_values>)

Whether to populate models with the `value` property of enums, rather than the raw enum. This may be useful if you want to serialize `model.model_dump()` later. Defaults to `False`.
    
    from enum import Enum
    from typing import Optional
    
    from pydantic import BaseModel, ConfigDict, Field
    
    class SomeEnum(Enum):
        FOO = 'foo'
        BAR = 'bar'
        BAZ = 'baz'
    
    class SomeModel(BaseModel):
        model_config = ConfigDict(use_enum_values=True)
    
        some_enum: SomeEnum
        another_enum: Optional[SomeEnum] = Field(
            default=SomeEnum.FOO, validate_default=True
        )
    
    model1 = SomeModel(some_enum=SomeEnum.BAR)
    print(model1.model_dump())
    #> {'some_enum': 'bar', 'another_enum': 'foo'}
    
    model2 = SomeModel(some_enum=SomeEnum.BAR, another_enum=SomeEnum.BAZ)
    print(model2.model_dump())
    #> {'some_enum': 'bar', 'another_enum': 'baz'}
    
**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### validate_assignment 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_assignment>)

Whether to validate the data when the model is changed. Defaults to `False`.

The default behavior of Pydantic is to validate the data when the model is created.

In case the user changes the data after the model is created, the model is _not_ revalidated.
    
    from pydantic import BaseModel
    
    class User(BaseModel):
      name: str
    
    user = User(name='John Doe')  # (1)
    print(user)
    #> name='John Doe'
    user.name = 123  # (1)
    print(user)
    #> name=123

The validation happens only when the model is created.

The validation does not happen when the data is changed.

In case you want to revalidate the model when the data is changed, you can use `validate_assignment=True`:
    
    from pydantic import BaseModel, ValidationError
    
    class User(BaseModel, validate_assignment=True):  # (1)
      name: str
    
    user = User(name='John Doe')  # (2)
    print(user)
    #> name='John Doe'
    try:
      user.name = 123  # (3)
    except ValidationError as e:
      print(e)
      '''
      1 validation error for User
      name
        Input should be a valid string [type=string_type, input_value=123, input_type=int]
      '''

You can either use class keyword arguments, or `model_config` to set `validate_assignment=True`.

The validation happens when the model is created.

The validation _also_ happens when the data is changed.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### arbitrary_types_allowed 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.arbitrary_types_allowed>)

Whether arbitrary types are allowed for field types. Defaults to `False`.
    
    from pydantic import BaseModel, ConfigDict, ValidationError
    
    # This is not a pydantic model, it's an arbitrary class
    class Pet:
        def __init__(self, name: str):
            self.name = name
    
    class Model(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
    
        pet: Pet
        owner: str
    
    pet = Pet(name='Hedwig')
    # A simple check of instance type is used to validate the data
    model = Model(owner='Harry', pet=pet)
    print(model)
    #> pet=<__main__.Pet object at 0x0123456789ab> owner='Harry'
    print(model.pet)
    #> <__main__.Pet object at 0x0123456789ab>
    print(model.pet.name)
    #> Hedwig
    print(type(model.pet))
    #> <class '__main__.Pet'>
    try:
        # If the value is not an instance of the type, it's invalid
        Model(owner='Harry', pet='Hedwig')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        pet
          Input should be an instance of Pet [type=is_instance_of, input_value='Hedwig', input_type=str]
        '''
    
    # Nothing in the instance of the arbitrary type is checked
    # Here name probably should have been a str, but it's not validated
    pet2 = Pet(name=42)
    model2 = Model(owner='Harry', pet=pet2)
    print(model2)
    #> pet=<__main__.Pet object at 0x0123456789ab> owner='Harry'
    print(model2.pet)
    #> <__main__.Pet object at 0x0123456789ab>
    print(model2.pet.name)
    #> 42
    print(type(model2.pet))
    #> <class '__main__.Pet'>
    
**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### from_attributes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.from_attributes>)

Whether to build models and look up discriminators of tagged unions using python object attributes.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### loc_by_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.loc_by_alias>)

Whether to use the actual key provided in the data (e.g. alias) for error `loc`s rather than the field’s name. Defaults to `True`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### alias_generator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.alias_generator>)

A callable that takes a field name and returns an alias for it or an instance of [`AliasGenerator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasGenerator>). Defaults to `None`.

When using a callable, the alias generator is used for both validation and serialization. If you want to use different alias generators for validation and serialization, you can use [`AliasGenerator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasGenerator>) instead.

If data source field names do not match your code style (e.g. CamelCase fields), you can automatically generate aliases using `alias_generator`. Here’s an example with a basic callable:
    
    from pydantic import BaseModel, ConfigDict
    from pydantic.alias_generators import to_pascal
    
    class Voice(BaseModel):
        model_config = ConfigDict(alias_generator=to_pascal)
    
        name: str
        language_code: str
    
    voice = Voice(Name='Filiz', LanguageCode='tr-TR')
    print(voice.language_code)
    #> tr-TR
    print(voice.model_dump(by_alias=True))
    #> {'Name': 'Filiz', 'LanguageCode': 'tr-TR'}
    
If you want to use different alias generators for validation and serialization, you can use [`AliasGenerator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasGenerator>).
    
    from pydantic import AliasGenerator, BaseModel, ConfigDict
    from pydantic.alias_generators import to_camel, to_pascal
    
    class Athlete(BaseModel):
        first_name: str
        last_name: str
        sport: str
    
        model_config = ConfigDict(
            alias_generator=AliasGenerator(
                validation_alias=to_camel,
                serialization_alias=to_pascal,
            )
        )
    
    athlete = Athlete(firstName='John', lastName='Doe', sport='track')
    print(athlete.model_dump(by_alias=True))
    #> {'FirstName': 'John', 'LastName': 'Doe', 'Sport': 'track'}
    
**Type:** [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)], [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`AliasGenerator`](<https://pydantic.dev/docs/validation/latest/api/pydantic/aliases/#pydantic.aliases.AliasGenerator>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### ignored_types 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.ignored_types>)

A tuple of types that may occur as values of class attributes without annotations. This is typically used for custom descriptors (classes that behave like `property`). If an attribute is set on a class without an annotation and has a type that is not in this tuple (or otherwise recognized by _pydantic_), an error will be raised. Defaults to `()`.

**Type:** [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`type`](<https://docs.python.org/3/glossary.html#term-type>), …]

#### allow_inf_nan 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.allow_inf_nan>)

Whether to allow infinity (`+inf` an `-inf`) and NaN values to float and decimal fields. Defaults to `True`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### json_schema_extra 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.json_schema_extra>)

A dict or callable to provide extra JSON schema properties. Defaults to `None`.

**Type:** `JsonDict` | `JsonSchemaExtraCallable` | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### json_encoders 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.json_encoders>)

A `dict` of custom JSON encoders for specific types. Defaults to `None`.

⚠ Deprecated in v2

This configuration option is a carryover from v1. We originally planned to remove it in v2 but didn’t have a 1:1 replacement so we are keeping it for now. It is still deprecated and will likely be removed in the future.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`object`](<https://docs.python.org/3/glossary.html#term-object>)], `JsonEncoder`] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### strict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.strict>)

Whether strict validation is applied to all fields on the model.

By default, Pydantic attempts to coerce values to the correct type, when possible.

There are situations in which you may want to disable this behavior, and instead raise an error if a value’s type does not match the field’s type annotation.

To configure strict mode for all fields on a model, you can set `strict=True` on the model.
    
    from pydantic import BaseModel, ConfigDict
    
    class Model(BaseModel):
        model_config = ConfigDict(strict=True)
    
        name: str
        age: int
    
See [Strict Mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>) for more details.

See the [Conversion Table](<https://pydantic.dev/docs/validation/latest/concepts/conversion_table>) for more details on how Pydantic converts data in both strict and lax modes.

✦ New in v2

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### revalidate_instances 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.revalidate_instances>)

When and how to revalidate models and dataclasses during validation. Can be one of:

  * `'never'`: will _not_ revalidate models and dataclasses during validation
  * `'always'`: will revalidate models and dataclasses during validation
  * `'subclass-instances'`: will revalidate models and dataclasses during validation if the instance is a subclass of the model or dataclass

The default is `'never'` (no revalidation).

This configuration only affects _the current model_ it is applied on, and does _not_ propagate to the models referenced in fields.
    
    from pydantic import BaseModel
    
    class User(BaseModel, revalidate_instances='never'):  # (1)
      name: str
    
    class Transaction(BaseModel):
      user: User
    
    my_user = User(name='John')
    t = Transaction(user=my_user)
    
    my_user.name = 1  # (2)
    t = Transaction(user=my_user)  # (3)
    print(t)
    #> user=User(name=1)

This is the default behavior.

The assignment is _not_ validated, unless you set [`validate_assignment`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_assignment>) in the configuration.

Since `revalidate_instances` is set to `'never'`, the user instance is not revalidated.

Here is an example demonstrating the behavior of `'subclass-instances'`:
    
    from pydantic import BaseModel
    
    class User(BaseModel, revalidate_instances='subclass-instances'):
      name: str
    
    class SubUser(User):
      age: int
    
    class Transaction(BaseModel):
      user: User
    
    my_user = User(name='John')
    my_user.name = 1  # (1)
    t = Transaction(user=my_user)  # (2)
    print(t)
    #> user=User(name=1)
    
    my_sub_user = SubUser(name='John', age=20)
    t = Transaction(user=my_sub_user)
    print(t)  # (3)
    #> user=User(name='John')

The assignment is _not_ validated, unless you set [`validate_assignment`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_assignment>) in the configuration.

Because `my_user` is a "direct" instance of `User`, it is _not_ being revalidated. It would have been the case if `revalidate_instances` was set to `'always'`.

Because `my_sub_user` is an instance of a `User` subclass, it is being revalidated. In this case, Pydantic coerces `my_sub_user` to the defined `User` class defined on `Transaction`. If one of its fields had an invalid value, a validation error would have been raised.

✦ New in v2

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘always’, ‘never’, ‘subclass-instances’]

#### ser_json_timedelta 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.ser_json_timedelta>)

The format of JSON serialized timedeltas. Accepts the string values of `'iso8601'` and `'float'`. Defaults to `'iso8601'`.

  * `'iso8601'` will serialize timedeltas to [ISO 8601 text format](<https://en.wikipedia.org/wiki/ISO_8601#Durations>).
  * `'float'` will serialize timedeltas to the total number of seconds.

↻ Changed in v2.12

It is now recommended to use the [`ser_json_temporal`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.ser_json_temporal>) setting. `ser_json_timedelta` will be deprecated in v3.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘float’]

#### ser_json_temporal 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.ser_json_temporal>)

The format of JSON serialized temporal types from the [`datetime`](<https://docs.python.org/3/library/datetime.html#module-datetime>) module. This includes:

  * [`datetime.datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>)
  * [`datetime.date`](<https://docs.python.org/3/library/datetime.html#datetime.date>)
  * [`datetime.time`](<https://docs.python.org/3/library/datetime.html#datetime.time>)
  * [`datetime.timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>)

Can be one of:

  * `'iso8601'` will serialize date-like types to [ISO 8601 text format](<https://en.wikipedia.org/wiki/ISO_8601#Durations>).
  * `'milliseconds'` will serialize date-like types to a floating point number of milliseconds since the epoch.
  * `'seconds'` will serialize date-like types to a floating point number of seconds since the epoch.

Defaults to `'iso8601'`.

✦ New in v2.12

This setting replaces [`ser_json_timedelta`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.ser_json_timedelta>), which will be deprecated in v3. `ser_json_temporal` adds more configurability for the other temporal types.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘iso8601’, ‘seconds’, ‘milliseconds’]

#### val_temporal_unit 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.val_temporal_unit>)

The unit to assume for validating numeric input for datetime-like types ([`datetime.datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) and [`datetime.date`](<https://docs.python.org/3/library/datetime.html#datetime.date>)). Can be one of:

  * `'seconds'` will validate date or time numeric inputs as seconds since the [epoch](<https://en.wikipedia.org/wiki/Unix_time>).

  * `'milliseconds'` will validate date or time numeric inputs as milliseconds since the [epoch](<https://en.wikipedia.org/wiki/Unix_time>).

  * `'infer'` will infer the unit from the string numeric input on unix time as:

    * seconds since the [epoch](<https://en.wikipedia.org/wiki/Unix_time>) if $-2^{10} <= v <= 2^{10}$
    * milliseconds since the [epoch](<https://en.wikipedia.org/wiki/Unix_time>) (if $v < -2^{10}$ or $v > 2^{10}$).

Defaults to `'infer'`.

✦ New in v2.12

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘seconds’, ‘milliseconds’, ‘infer’]

#### ser_json_bytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.ser_json_bytes>)

The encoding of JSON serialized bytes. Defaults to `'utf8'`. Set equal to `val_json_bytes` to get back an equal value after serialization round trip.

  * `'utf8'` will serialize bytes to UTF-8 strings.
  * `'base64'` will serialize bytes to URL safe base64 strings.
  * `'hex'` will serialize bytes to hexadecimal strings.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘utf8’, ‘base64’, ‘hex’]

#### val_json_bytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.val_json_bytes>)

✦ New in v2.9

The encoding of JSON serialized bytes to decode. Defaults to `'utf8'`. Set equal to `ser_json_bytes` to get back an equal value after serialization round trip.

  * `'utf8'` will deserialize UTF-8 strings to bytes.
  * `'base64'` will deserialize URL safe base64 strings to bytes.
  * `'hex'` will deserialize hexadecimal strings to bytes.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘utf8’, ‘base64’, ‘hex’]

#### ser_json_inf_nan 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.ser_json_inf_nan>)

The encoding of JSON serialized infinity and NaN float values. Defaults to `'null'`.

  * `'null'` will serialize infinity and NaN values as `null`.
  * `'constants'` will serialize infinity and NaN values as `Infinity` and `NaN`.
  * `'strings'` will serialize infinity as string `"Infinity"` and NaN as string `"NaN"`.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘null’, ‘constants’, ‘strings’]

#### validate_default 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_default>)

Whether to validate default values during validation. Defaults to `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### validate_return 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_return>)

Whether to validate the return value from call validators. Defaults to `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### protected_namespaces 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.protected_namespaces>)

A tuple of strings and/or regex patterns that prevent models from having fields with names that conflict with its existing members/methods.

Strings are matched on a prefix basis. For instance, with `'dog'`, having a field named `'dog_name'` will be disallowed.

Regex patterns are matched on the entire field name. For instance, with the pattern `'^dog, having a field named `’dog’` will be disallowed,`, having a field named �IC1� will be disallowed, but `'dog_name'` will be accepted.

Defaults to `('model_validate', 'model_dump')`. This default is used to prevent collisions with the existing (and possibly future) [validation](<https://pydantic.dev/docs/validation/latest/concepts/models#validating-data>) and [serialization](<https://pydantic.dev/docs/validation/latest/concepts/serialization#serializing-data>) methods.
    
    import warnings
    
    from pydantic import BaseModel
    
    warnings.filterwarnings('error')  # Raise warnings as errors
    
    try:
    
        class Model(BaseModel):
            model_dump_something: str
    
    except UserWarning as e:
        print(e)
        '''
        Field 'model_dump_something' in 'Model' conflicts with protected namespace 'model_dump'.
    
        You may be able to solve this by setting the 'protected_namespaces' configuration to ('model_validate',).
        '''
    
You can customize this behavior using the `protected_namespaces` setting:
    
    import re
    import warnings
    
    from pydantic import BaseModel, ConfigDict
    
    with warnings.catch_warnings(record=True) as caught_warnings:
        warnings.simplefilter('always')  # Catch all warnings
    
        class Model(BaseModel):
            safe_field: str
            also_protect_field: str
            protect_this: str
    
            model_config = ConfigDict(
                protected_namespaces=(
                    'protect_me_',
                    'also_protect_',
                    re.compile('^protect_this$'),
                )
            )
    
    for warning in caught_warnings:
        print(f'{warning.message}')
        '''
        Field 'also_protect_field' in 'Model' conflicts with protected namespace 'also_protect_'.
        You may be able to solve this by setting the 'protected_namespaces' configuration to ('protect_me_', re.compile('^protect_this$'))`.
    
        Field 'protect_this' in 'Model' conflicts with protected namespace 're.compile('^protect_this$')'.
        You may be able to solve this by setting the 'protected_namespaces' configuration to ('protect_me_', 'also_protect_')`.
        '''
    
While Pydantic will only emit a warning when an item is in a protected namespace but does not actually have a collision, an error _is_ raised if there is an actual collision with an existing attribute:
    
    from pydantic import BaseModel, ConfigDict
    
    try:
    
        class Model(BaseModel):
            model_validate: str
    
            model_config = ConfigDict(protected_namespaces=('model_',))
    
    except ValueError as e:
        print(e)
        '''
        Field 'model_validate' conflicts with member <bound method BaseModel.model_validate of <class 'pydantic.main.BaseModel'>> of protected namespace 'model_'.
        '''
    
↻ Changed in v2.10

The default protected namespaces was changed from `('model_',)` to `('model_validate', 'model_dump')`, to allow for fields like `model_id`, `model_name` to be used.

**Type:** [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`Pattern`](<https://docs.python.org/3/library/typing.html#typing.Pattern>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)], …]

#### hide_input_in_errors 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.hide_input_in_errors>)

Whether to hide inputs when printing errors. Defaults to `False`.

Pydantic shows the input value and type when it raises `ValidationError` during the validation.
    
    from pydantic import BaseModel, ValidationError
    
    class Model(BaseModel):
        a: str
    
    try:
        Model(a=123)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        a
          Input should be a valid string [type=string_type, input_value=123, input_type=int]
        '''
    
You can hide the input value and type by setting the `hide_input_in_errors` config to `True`.
    
    from pydantic import BaseModel, ConfigDict, ValidationError
    
    class Model(BaseModel):
        a: str
        model_config = ConfigDict(hide_input_in_errors=True)
    
    try:
        Model(a=123)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        a
          Input should be a valid string [type=string_type]
        '''
    
**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### defer_build 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.defer_build>)

Whether to defer model validator and serializer construction until the first model validation. Defaults to False.

This can be useful to avoid the overhead of building models which are only used nested within other models, or when you want to manually define type namespace via [`Model.model_rebuild(_types_namespace=...)`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_rebuild>).

↻ Changed in v2.10

The setting also applies to [Pydantic dataclasses](<https://pydantic.dev/docs/validation/latest/concepts/dataclasses>) and [type adapters](<https://pydantic.dev/docs/validation/latest/concepts/type_adapter>).

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### plugin_settings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.plugin_settings>)

A `dict` of settings for plugins. Defaults to `None`.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`object`](<https://docs.python.org/3/glossary.html#term-object>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### schema_generator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.schema_generator>)

The `GenerateSchema` class to use during core schema generation.

⚠ Deprecated in v2.10

The `GenerateSchema` class is private and highly subject to change.

**Type:** [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`_GenerateSchema`] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### json_schema_serialization_defaults_required 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.json_schema_serialization_defaults_required>)

Whether fields with default values should be marked as required in the serialization schema. Defaults to `False`.

This ensures that the serialization schema will reflect the fact a field with a default will always be present when serializing the model, even though it is not required for validation.

However, there are scenarios where this may be undesirable — in particular, if you want to share the schema between validation and serialization, and don’t mind fields with defaults being marked as not required during serialization. See [#7209](<https://github.com/pydantic/pydantic/issues/7209>) for more details.
    
    from pydantic import BaseModel, ConfigDict
    
    class Model(BaseModel):
        a: str = 'a'
    
        model_config = ConfigDict(json_schema_serialization_defaults_required=True)
    
    print(Model.model_json_schema(mode='validation'))
    '''
    {
        'properties': {'a': {'default': 'a', 'title': 'A', 'type': 'string'}},
        'title': 'Model',
        'type': 'object',
    }
    '''
    print(Model.model_json_schema(mode='serialization'))
    '''
    {
        'properties': {'a': {'default': 'a', 'title': 'A', 'type': 'string'}},
        'required': ['a'],
        'title': 'Model',
        'type': 'object',
    }
    '''
    
✦ New in v2.4

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### json_schema_mode_override 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.json_schema_mode_override>)

If not `None`, the specified mode will be used to generate the JSON schema regardless of what `mode` was passed to the function call. Defaults to `None`.

This provides a way to force the JSON schema generation to reflect a specific mode, e.g., to always use the validation schema.

It can be useful when using frameworks (such as FastAPI) that may generate different schemas for validation and serialization that must both be referenced from the same schema; when this happens, we automatically append `-Input` to the definition reference for the validation schema and `-Output` to the definition reference for the serialization schema. By specifying a `json_schema_mode_override` though, this prevents the conflict between the validation and serialization schemas (since both will use the specified schema), and so prevents the suffixes from being added to the definition references.
    
    from pydantic import BaseModel, ConfigDict, Json
    
    class Model(BaseModel):
        a: Json[int]  # requires a string to validate, but will dump an int
    
    print(Model.model_json_schema(mode='serialization'))
    '''
    {
        'properties': {'a': {'title': 'A', 'type': 'integer'}},
        'required': ['a'],
        'title': 'Model',
        'type': 'object',
    }
    '''
    
    class ForceInputModel(Model):
        # the following ensures that even with mode='serialization', we
        # will get the schema that would be generated for validation.
        model_config = ConfigDict(json_schema_mode_override='validation')
    
    print(ForceInputModel.model_json_schema(mode='serialization'))
    '''
    {
        'properties': {
            'a': {
                'contentMediaType': 'application/json',
                'contentSchema': {'type': 'integer'},
                'title': 'A',
                'type': 'string',
            }
        },
        'required': ['a'],
        'title': 'ForceInputModel',
        'type': 'object',
    }
    '''
    
✦ New in v2.4

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘validation’, ‘serialization’, [`None`](<https://docs.python.org/3/library/constants.html#None>)]

#### coerce_numbers_to_str 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.coerce_numbers_to_str>)

If `True`, enables automatic coercion of any `Number` type to `str` in “lax” (non-strict) mode. Defaults to `False`.

Pydantic doesn’t allow number types (`int`, `float`, `Decimal`) to be coerced as type `str` by default.
    
    from decimal import Decimal
    
    from pydantic import BaseModel, ConfigDict, ValidationError
    
    class Model(BaseModel):
        value: str
    
    try:
        print(Model(value=42))
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        value
          Input should be a valid string [type=string_type, input_value=42, input_type=int]
        '''
    
    class Model(BaseModel):
        model_config = ConfigDict(coerce_numbers_to_str=True)
    
        value: str
    
    repr(Model(value=42).value)
    #> "42"
    repr(Model(value=42.13).value)
    #> "42.13"
    repr(Model(value=Decimal('42.13')).value)
    #> "42.13"
    
**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### regex_engine 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.regex_engine>)

The regex engine to be used for pattern validation. Defaults to `'rust-regex'`.

  * `'rust-regex'` uses the [`regex`](<https://docs.rs/regex>) Rust crate, which is non-backtracking and therefore more DDoS resistant, but does not support all regex features.
  * `'python-re'` use the [`re`](<https://docs.python.org/3/library/re.html#module-re>) module, which supports all regex features, but may be slower.

    from pydantic import BaseModel, ConfigDict, Field, ValidationError
    
    class Model(BaseModel):
        model_config = ConfigDict(regex_engine='python-re')
    
        value: str = Field(pattern=r'^abc(?=def)')
    
    print(Model(value='abcdef').value)
    #> abcdef
    
    try:
        print(Model(value='abxyzcdef'))
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        value
          String should match pattern '^abc(?=def)' [type=string_pattern_mismatch, input_value='abxyzcdef', input_type=str]
        '''
    
✦ New in v2.5

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘rust-regex’, ‘python-re’]

#### validation_error_cause 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validation_error_cause>)

If `True`, Python exceptions that were part of a validation failure will be shown as an exception group as a cause. Can be useful for debugging. Defaults to `False`.

✦ New in v2.5

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### use_attribute_docstrings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.use_attribute_docstrings>)

Whether docstrings of attributes (bare string literals immediately following the attribute declaration) should be used for field descriptions. Defaults to `False`.
    
    from pydantic import BaseModel, ConfigDict, Field
    
    class Model(BaseModel):
        model_config = ConfigDict(use_attribute_docstrings=True)
    
        x: str
        """
        Example of an attribute docstring
        """
    
        y: int = Field(description="Description in Field")
        """
        Description in Field overrides attribute docstring
        """
    
    print(Model.model_fields["x"].description)
    # > Example of an attribute docstring
    print(Model.model_fields["y"].description)
    # > Description in Field
    
This requires the source code of the class to be available at runtime (and so won’t work in the interactive interpreter shell).

✦ New in v2.7

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### cache_strings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.cache_strings>)

Whether to cache strings to avoid constructing new Python objects. Defaults to True.

Enabling this setting should significantly improve validation performance while increasing memory usage slightly.

  * `True` or `'all'` (the default): cache all strings
  * `'keys'`: cache only dictionary keys
  * `False` or `'none'`: no caching

✦ New in v2.7

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘all’, ‘keys’, ‘none’]

#### validate_by_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_by_alias>)

Whether an aliased field may be populated by its alias. Defaults to `True`.

Here’s an example of disabling validation by alias:
    
    from pydantic import BaseModel, ConfigDict, Field
    
    class Model(BaseModel):
      model_config = ConfigDict(validate_by_name=True, validate_by_alias=False)
    
      my_field: str = Field(validation_alias='my_alias')  # (1)
    
    m = Model(my_field='foo')  # (2)
    print(m)
    #> my_field='foo'

The field `'my_field'` has an alias `'my_alias'`.

The model can only be populated by the attribute name `'my_field'`.

✦ New in v2.11

This setting was introduced in conjunction with [`validate_by_name`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_by_name>) to empower users with more fine grained validation control.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### validate_by_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_by_name>)

Whether an aliased field may be populated by its name as given by the model attribute. Defaults to `False`.
    
    from pydantic import BaseModel, ConfigDict, Field
    
    class Model(BaseModel):
      model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)
    
      my_field: str = Field(validation_alias='my_alias')  # (1)
    
    m = Model(my_alias='foo')  # (2)
    print(m)
    #> my_field='foo'
    
    m = Model(my_field='foo')  # (3)
    print(m)
    #> my_field='foo'

The field `'my_field'` has an alias `'my_alias'`.

The model is populated by the alias `'my_alias'`.

The model is populated by the attribute name `'my_field'`.

✦ New in v2.11

This setting was introduced in conjunction with [`validate_by_alias`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.validate_by_alias>) to empower users with more fine grained validation control. It is an alternative to [`populate_by_name`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.populate_by_name>), that enables validation by name **and** by alias.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### serialize_by_alias 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.serialize_by_alias>)

Whether an aliased field should be serialized by its alias. Defaults to `False`.

Note: In v2.11, `serialize_by_alias` was introduced to address the [popular request](<https://github.com/pydantic/pydantic/issues/8379>) for consistency with alias behavior for validation and serialization settings. In v3, the default value is expected to change to `True` for consistency with the validation default.
    
    from pydantic import BaseModel, ConfigDict, Field
    
    class Model(BaseModel):
      model_config = ConfigDict(serialize_by_alias=True)
    
      my_field: str = Field(serialization_alias='my_alias')  # (1)
    
    m = Model(my_field='foo')
    print(m.model_dump())  # (2)
    #> {'my_alias': 'foo'}

The field `'my_field'` has an alias `'my_alias'`.

The model is serialized using the alias `'my_alias'` for the `'my_field'` attribute.

✦ New in v2.11

This setting was introduced to address the [popular request](<https://github.com/pydantic/pydantic/issues/8379>) for consistency with alias behavior for validation and serialization.

In v3, the default value is expected to change to `True` for consistency with the validation default.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### url_preserve_empty_path 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.url_preserve_empty_path>)

Whether to preserve empty URL paths when validating values for a URL type. Defaults to `False`.
    
    from pydantic import AnyUrl, BaseModel, ConfigDict
    
    class Model(BaseModel):
        model_config = ConfigDict(url_preserve_empty_path=True)
    
        url: AnyUrl
    
    m = Model(url='http://example.com')
    print(m.url)
    #> http://example.com
    
✦ New in v2.12

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

#### polymorphic_serialization 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.polymorphic_serialization>)

Whether to use polymorphic serialization for subclasses of the model or Pydantic dataclass. Defaults to `False`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

## with_config 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.with_config>)
    
    def with_config(*, config: ConfigDict) -> Callable[[_TypeT], _TypeT]
    def with_config(config: ConfigDict, /) -> Callable[[_TypeT], _TypeT]
    def with_config(**config: Unpack[ConfigDict]) -> Callable[[_TypeT], _TypeT]
    
A convenience decorator to set a [Pydantic configuration](<https://pydantic.dev/docs/validation/latest/api/pydantic/config>) on a `TypedDict` or a `dataclass` from the standard library.

Although the configuration can be set using the `__pydantic_config__` attribute, it does not play well with type checkers, especially with `TypedDict`.

⚠ Deprecated in v2.11, removed in v3

Passing `config` as a keyword argument.

↻ Changed in v2.11

Keyword arguments can be provided directly instead of a config dictionary.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#returns>)

[`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`_TypeT`], `_TypeT`]

## ExtraValues 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ExtraValues>)

**Default:** `Literal['allow', 'ignore', 'forbid']`

Alias generators for converting between different capitalization conventions.

## to_pascal 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.alias_generators.to_pascal>)
    
    def to_pascal(snake: str) -> str
    
Convert a snake_case string to PascalCase.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#returns-1>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The PascalCase string.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#parameters>)

**`snake`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.alias_generators.to_pascal\(snake\)>)

The string to convert.

## to_camel 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.alias_generators.to_camel>)
    
    def to_camel(snake: str) -> str
    
Convert a snake_case string to camelCase.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#returns-2>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The converted camelCase string.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#parameters-1>)

**`snake`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.alias_generators.to_camel\(snake\)>)

The string to convert.

## to_snake 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.alias_generators.to_snake>)
    
    def to_snake(camel: str) -> str
    
Convert a PascalCase, camelCase, or kebab-case string to snake_case.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#returns-3>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The converted string in snake_case.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#parameters-2>)

**`camel`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.alias_generators.to_snake\(camel\)>)

The string to convert.

Was this page helpful?

Thanks for your feedback!