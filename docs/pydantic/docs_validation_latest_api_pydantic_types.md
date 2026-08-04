# Pydantic Types | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/types/](https://pydantic.dev/docs/validation/latest/api/pydantic/types/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Pydantic Types

The types module contains custom types used by pydantic.

## Strict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Strict>)

**Bases:** `PydanticMetadata`, `BaseMetadata`

A field metadata class to indicate that a field should be validated in strict mode. Use this class as an annotation via [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>), as seen below.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#attributes>)

#### strict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Strict.strict>)

Whether to validate the field in strict mode.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

## AllowInfNan 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.AllowInfNan>)

**Bases:** `PydanticMetadata`

A field metadata class to indicate that a field should allow `-inf`, `inf`, and `nan`.

Use this class as an annotation via [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>), as seen below.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#attributes-1>)

#### allow_inf_nan 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.AllowInfNan.allow_inf_nan>)

Whether to allow `-inf`, `inf`, and `nan`. Defaults to `True`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

## StringConstraints 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints>)

**Bases:** `GroupedMetadata`

A field metadata class to apply constraints to `str` types. Use this class as an annotation via [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>), as seen below.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#attributes-2>)

#### strip_whitespace 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.strip_whitespace>)

Whether to remove leading and trailing whitespace.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### to_upper 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.to_upper>)

Whether to convert the string to uppercase.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### to_lower 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.to_lower>)

Whether to convert the string to lowercase.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### strict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.strict>)

Whether to validate the string in strict mode.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### min_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.min_length>)

The minimum length of the string.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### max_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.max_length>)

The maximum length of the string.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### pattern 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.pattern>)

A regex pattern that the string must match.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`Pattern`](<https://docs.python.org/3/library/typing.html#typing.Pattern>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### ascii_only 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints.ascii_only>)

Whether the string should contain only ASCII characters.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

## ImportString 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ImportString>)

A type that can be used to import a Python object from a string.

`ImportString` expects a string and loads the Python object importable at that dotted path. Attributes of modules may be separated from the module by `:` or `.`, e.g. if `'math:cos'` is provided, the resulting field value would be the function `cos`. If a `.` is used and both an attribute and submodule are present at the same path, the module will be preferred.

On model instantiation, pointers will be evaluated and imported. There is some nuance to this behavior, demonstrated in the examples below.
    
    import math
    
    from pydantic import BaseModel, Field, ImportString, ValidationError
    
    class ImportThings(BaseModel):
        obj: ImportString
    
    # A string value will cause an automatic import
    my_cos = ImportThings(obj='math.cos')
    
    # You can use the imported function as you would expect
    cos_of_0 = my_cos.obj(0)
    assert cos_of_0 == 1
    
    # A string whose value cannot be imported will raise an error
    try:
        ImportThings(obj='foo.bar')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for ImportThings
        obj
          Invalid python path: No module named 'foo' [type=import_error, input_value='foo.bar', input_type=str]
        '''
    
    # Actual python objects can be assigned as well
    my_cos = ImportThings(obj=math.cos)
    my_cos_2 = ImportThings(obj='math.cos')
    my_cos_3 = ImportThings(obj='math:cos')
    assert my_cos == my_cos_2 == my_cos_3
    
    # You can set default field value either as Python object:
    class ImportThingsDefaultPyObj(BaseModel):
        obj: ImportString = math.cos
    
    # or as a string value (but only if used with `validate_default=True`)
    class ImportThingsDefaultString(BaseModel):
        obj: ImportString = Field(default='math.cos', validate_default=True)
    
    my_cos_default1 = ImportThingsDefaultPyObj()
    my_cos_default2 = ImportThingsDefaultString()
    assert my_cos_default1.obj == my_cos_default2.obj == math.cos
    
    # note: this will not work!
    class ImportThingsMissingValidateDefault(BaseModel):
        obj: ImportString = 'math.cos'
    
    my_cos_default3 = ImportThingsMissingValidateDefault()
    assert my_cos_default3.obj == 'math.cos'  # just string, not evaluated
    
Serializing an `ImportString` type to json is also possible.
    
    from pydantic import BaseModel, ImportString
    
    class ImportThings(BaseModel):
        obj: ImportString
    
    # Create an instance
    m = ImportThings(obj='math.cos')
    print(m)
    #> obj=<built-in function cos>
    print(m.model_dump_json())
    #> {"obj":"math.cos"}
    
## UuidVersion 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UuidVersion>)

A field metadata class to indicate a [UUID](<https://docs.python.org/3/library/uuid.html>) version.

Use this class as an annotation via [`Annotated`](<https://docs.python.org/3/library/typing.html#typing.Annotated>), as seen below.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#attributes-3>)

#### uuid_version 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UuidVersion.uuid_version>)

The version of the UUID. Must be one of 1, 3, 4, 5, 6, 7 or 8.

**Type:** [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[1, 3, 4, 5, 6, 7, 8]

## Json 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Json>)

A special type wrapper which loads JSON before parsing.

You can use the `Json` data type to make Pydantic first load a raw JSON string before validating the loaded data into the parametrized type:
    
    from typing import Any
    
    from pydantic import BaseModel, Json, ValidationError
    
    class AnyJsonModel(BaseModel):
        json_obj: Json[Any]
    
    class ConstrainedJsonModel(BaseModel):
        json_obj: Json[list[int]]
    
    print(AnyJsonModel(json_obj='{"b": 1}'))
    #> json_obj={'b': 1}
    print(ConstrainedJsonModel(json_obj='[1, 2, 3]'))
    #> json_obj=[1, 2, 3]
    
    try:
        ConstrainedJsonModel(json_obj=12)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for ConstrainedJsonModel
        json_obj
          JSON input should be string, bytes or bytearray [type=json_type, input_value=12, input_type=int]
        '''
    
    try:
        ConstrainedJsonModel(json_obj='[a, b]')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for ConstrainedJsonModel
        json_obj
          Invalid JSON: expected value at line 1 column 2 [type=json_invalid, input_value='[a, b]', input_type=str]
        '''
    
    try:
        ConstrainedJsonModel(json_obj='["a", "b"]')
    except ValidationError as e:
        print(e)
        '''
        2 validation errors for ConstrainedJsonModel
        json_obj.0
          Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
        json_obj.1
          Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='b', input_type=str]
        '''
    
When you dump the model using `model_dump` or `model_dump_json`, the dumped value will be the result of validation, not the original JSON string. However, you can use the argument `round_trip=True` to get the original JSON string back:
    
    from pydantic import BaseModel, Json
    
    class ConstrainedJsonModel(BaseModel):
        json_obj: Json[list[int]]
    
    print(ConstrainedJsonModel(json_obj='[1, 2, 3]').model_dump_json())
    #> {"json_obj":[1,2,3]}
    print(
        ConstrainedJsonModel(json_obj='[1, 2, 3]').model_dump_json(round_trip=True)
    )
    #> {"json_obj":"[1,2,3]"}
    
## Secret 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Secret>)

**Bases:** `_SecretBase[SecretType]`

A generic base class used for defining a field with sensitive information that you do not want to be visible in logging or tracebacks.

You may either directly parametrize `Secret` with a type, or subclass from `Secret` with a parametrized type. The benefit of subclassing is that you can define a custom `_display` method, which will be used for `repr()` and `str()` methods. The examples below demonstrate both ways of using `Secret` to create a new secret type.

  1. Directly parametrizing `Secret` with a type:

    from pydantic import BaseModel, Secret
    
    SecretBool = Secret[bool]
    
    class Model(BaseModel):
        secret_bool: SecretBool
    
    m = Model(secret_bool=True)
    print(m.model_dump())
    #> {'secret_bool': Secret('**********')}
    
    print(m.model_dump_json())
    #> {"secret_bool":"**********"}
    
    print(m.secret_bool.get_secret_value())
    #> True
    
  2. Subclassing from parametrized `Secret`:

    from datetime import date
    
    from pydantic import BaseModel, Secret
    
    class SecretDate(Secret[date]):
        def _display(self) -> str:
            return '****/**/**'
    
    class Model(BaseModel):
        secret_date: SecretDate
    
    m = Model(secret_date=date(2022, 1, 1))
    print(m.model_dump())
    #> {'secret_date': SecretDate('****/**/**')}
    
    print(m.model_dump_json())
    #> {"secret_date":"****/**/**"}
    
    print(m.secret_date.get_secret_value())
    #> 2022-01-01
    
The value returned by the `_display` method will be used for `repr()` and `str()`.

You can enforce constraints on the underlying type through annotations: For example:
    
    from typing import Annotated
    
    from pydantic import BaseModel, Field, Secret, ValidationError
    
    SecretPosInt = Secret[Annotated[int, Field(gt=0, strict=True)]]
    
    class Model(BaseModel):
      sensitive_int: SecretPosInt
    
    m = Model(sensitive_int=42)
    print(m.model_dump())
    #> {'sensitive_int': Secret('**********')}
    
    try:
      m = Model(sensitive_int=-42)  # (1)
    except ValidationError as exc_info:
      print(exc_info.errors(include_url=False, include_input=False))
      '''
      [
          {
              'type': 'greater_than',
              'loc': ('sensitive_int',),
              'msg': 'Input should be greater than 0',
              'ctx': {'gt': 0},
          }
      ]
      '''
    
    try:
      m = Model(sensitive_int='42')  # (2)
    except ValidationError as exc_info:
      print(exc_info.errors(include_url=False, include_input=False))
      '''
      [
          {
              'type': 'int_type',
              'loc': ('sensitive_int',),
              'msg': 'Input should be a valid integer',
          }
      ]
      '''

The input value is not greater than 0, so it raises a validation error.

The input value is not an integer, so it raises a validation error because the `SecretPosInt` type has strict mode enabled.

## SecretStr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.SecretStr>)

**Bases:** `_SecretField[str]`

A string used for storing sensitive information that you do not want to be visible in logging or tracebacks.

When the secret value is nonempty, it is displayed as `'**********'` instead of the underlying value in calls to `repr()` and `str()`. If the value _is_ empty, it is displayed as `''`.
    
    from pydantic import BaseModel, SecretStr
    
    class User(BaseModel):
        username: str
        password: SecretStr
    
    user = User(username='scolvin', password='password1')
    
    print(user)
    #> username='scolvin' password=SecretStr('**********')
    print(user.password.get_secret_value())
    #> password1
    print((SecretStr('password'), SecretStr('')))
    #> (SecretStr('**********'), SecretStr(''))
    
As seen above, by default, [`SecretStr`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.SecretStr>) (and [`SecretBytes`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.SecretBytes>)) will be serialized as `**********` when serializing to json.

You can use the [`field_serializer`](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_serializers/#pydantic.functional_serializers.field_serializer>) to dump the secret as plain-text when serializing to json.
    
    from pydantic import BaseModel, SecretBytes, SecretStr, field_serializer
    
    class Model(BaseModel):
        password: SecretStr
        password_bytes: SecretBytes
    
        @field_serializer('password', 'password_bytes', when_used='json')
        def dump_secret(self, v):
            return v.get_secret_value()
    
    model = Model(password='IAmSensitive', password_bytes=b'IAmSensitiveBytes')
    print(model)
    #> password=SecretStr('**********') password_bytes=SecretBytes(b'**********')
    print(model.password)
    #> **********
    print(model.model_dump())
    '''
    {
        'password': SecretStr('**********'),
        'password_bytes': SecretBytes(b'**********'),
    }
    '''
    print(model.model_dump_json())
    #> {"password":"IAmSensitive","password_bytes":"IAmSensitiveBytes"}
    
## SecretBytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.SecretBytes>)

**Bases:** `_SecretField[bytes]`

A bytes used for storing sensitive information that you do not want to be visible in logging or tracebacks.

It displays `b'**********'` instead of the string value on `repr()` and `str()` calls. When the secret value is nonempty, it is displayed as `b'**********'` instead of the underlying value in calls to `repr()` and `str()`. If the value _is_ empty, it is displayed as `b''`.
    
    from pydantic import BaseModel, SecretBytes
    
    class User(BaseModel):
        username: str
        password: SecretBytes
    
    user = User(username='scolvin', password=b'password1')
    #> username='scolvin' password=SecretBytes(b'**********')
    print(user.password.get_secret_value())
    #> b'password1'
    print((SecretBytes(b'password'), SecretBytes(b'')))
    #> (SecretBytes(b'**********'), SecretBytes(b''))
    
## PaymentCardNumber 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

Based on: <https://en.wikipedia.org/wiki/Payment_card_number>.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#attributes-4>)

#### masked 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber.masked>)

Mask all but the last 4 digits of the card number.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#methods>)

#### validate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber.validate>)

`@classmethod`
    
    def validate(
        cls,
        input_value: str,
        /,
        _: core_schema.ValidationInfo,
    ) -> PaymentCardNumber
    
Validate the card number and return a `PaymentCardNumber` instance.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns>)

[`PaymentCardNumber`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber>)

#### validate_digits 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber.validate_digits>)

`@classmethod`
    
    def validate_digits(cls, card_number: str) -> None
    
Validate that the card number is all digits.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-1>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

#### validate_luhn_check_digit 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber.validate_luhn_check_digit>)

`@classmethod`
    
    def validate_luhn_check_digit(cls, card_number: str) -> str
    
Based on: <https://en.wikipedia.org/wiki/Luhn_algorithm>.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-2>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### validate_brand 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber.validate_brand>)

`@staticmethod`
    
    def validate_brand(card_number: str) -> PaymentCardBrand
    
Validate length based on BIN for major brands: <https://en.wikipedia.org/wiki/Payment_card_number#Issuer_identification_number_(IIN)>.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-3>)

`PaymentCardBrand`

## ByteSize 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ByteSize>)

**Bases:** [`int`](<https://docs.python.org/3/library/functions.html#int>)

Converts a string representing a number of bytes with units (such as `'1KB'` or `'11.5MiB'`) into an integer.

You can use the `ByteSize` data type to (case-insensitively) convert a string representation of a number of bytes into an integer, and also to print out human-readable strings representing a number of bytes.

In conformance with [IEC 80000-13 Standard](<https://en.wikipedia.org/wiki/ISO/IEC_80000>) we interpret `'1KB'` to mean 1000 bytes, and `'1KiB'` to mean 1024 bytes. In general, including a middle `'i'` will cause the unit to be interpreted as a power of 2, rather than a power of 10 (so, for example, `'1 MB'` is treated as `1_000_000` bytes, whereas `'1 MiB'` is treated as `1_048_576` bytes).
    
    from pydantic import BaseModel, ByteSize
    
    class MyModel(BaseModel):
        size: ByteSize
    
    print(MyModel(size=52000).size)
    #> 52000
    print(MyModel(size='3000 KiB').size)
    #> 3072000
    
    m = MyModel(size='50 PB')
    print(m.size.human_readable())
    #> 44.4PiB
    print(m.size.human_readable(decimal=True))
    #> 50.0PB
    print(m.size.human_readable(separator=' '))
    #> 44.4 PiB
    
    print(m.size.to('TiB'))
    #> 45474.73508864641
    
### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#methods-1>)

#### human_readable 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ByteSize.human_readable>)
    
    def human_readable(decimal: bool = False, separator: str = '') -> str
    
Converts a byte size to a human readable string.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-4>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — A human readable string representation of the byte size.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters>)

**`decimal`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ByteSize.human_readable\(decimal\)>)

If True, use decimal units (e.g. 1000 bytes per KB). If False, use binary units (e.g. 1024 bytes per KiB).

**`separator`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `''`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ByteSize.human_readable\(separator\)>)

A string used to split the value and unit. Defaults to an empty string (”).

#### to 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ByteSize.to>)
    
    def to(unit: str) -> float
    
Converts a byte size to another unit, including both byte and bit units.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-5>)

[`float`](<https://docs.python.org/3/library/functions.html#float>) — The byte size in the new unit.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-1>)

**`unit`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ByteSize.to\(unit\)>)

The unit to convert to. Must be one of the following: B, KB, MB, GB, TB, PB, EB, KiB, MiB, GiB, TiB, PiB, EiB (byte units) and bit, kbit, mbit, gbit, tbit, pbit, ebit, kibit, mibit, gibit, tibit, pibit, eibit (bit units).

## PastDate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PastDate>)

A date in the past.

## FutureDate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FutureDate>)

A date in the future.

## AwareDatetime 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.AwareDatetime>)

A datetime that requires timezone info.

## NaiveDatetime 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NaiveDatetime>)

A datetime that doesn’t require timezone info.

## PastDatetime 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PastDatetime>)

A datetime that must be in the past.

## FutureDatetime 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FutureDatetime>)

A datetime that must be in the future.

## EncoderProtocol 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol>)

**Bases:** [`Protocol`](<https://docs.python.org/3/library/typing.html#typing.Protocol>)

Protocol for encoding and decoding data to and from bytes.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#methods-2>)

#### decode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol.decode>)

`@classmethod`
    
    def decode(cls, data: bytes) -> bytes
    
Decode the data using the encoder.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-6>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The decoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-2>)

**`data`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol.decode\(data\)>)

The data to decode.

#### encode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol.encode>)

`@classmethod`
    
    def encode(cls, value: bytes) -> bytes
    
Encode the data using the encoder.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-7>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The encoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-3>)

**`value`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol.encode\(value\)>)

The data to encode.

#### get_json_format 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol.get_json_format>)

`@classmethod`
    
    def get_json_format(cls) -> str
    
Get the JSON format for the encoded data.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-8>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The JSON format for the encoded data.

## Base64Encoder 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Encoder>)

**Bases:** [`EncoderProtocol`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol>)

Standard (non-URL-safe) Base64 encoder.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#methods-3>)

#### decode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Encoder.decode>)

`@classmethod`
    
    def decode(cls, data: bytes) -> bytes
    
Decode the data from base64 encoded bytes to original bytes data.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-9>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The decoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-4>)

**`data`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Encoder.decode\(data\)>)

The data to decode.

#### encode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Encoder.encode>)

`@classmethod`
    
    def encode(cls, value: bytes) -> bytes
    
Encode the data from bytes to a base64 encoded bytes.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-10>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The encoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-5>)

**`value`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Encoder.encode\(value\)>)

The data to encode.

#### get_json_format 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Encoder.get_json_format>)

`@classmethod`
    
    def get_json_format(cls) -> Literal['base64']
    
Get the JSON format for the encoded data.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-11>)

[`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘base64’] — The JSON format for the encoded data.

## Base64UrlEncoder 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlEncoder>)

**Bases:** [`EncoderProtocol`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncoderProtocol>)

URL-safe Base64 encoder.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#methods-4>)

#### decode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlEncoder.decode>)

`@classmethod`
    
    def decode(cls, data: bytes) -> bytes
    
Decode the data from base64 encoded bytes to original bytes data.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-12>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The decoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-6>)

**`data`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlEncoder.decode\(data\)>)

The data to decode.

#### encode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlEncoder.encode>)

`@classmethod`
    
    def encode(cls, value: bytes) -> bytes
    
Encode the data from bytes to a base64 encoded bytes.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-13>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The encoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-7>)

**`value`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlEncoder.encode\(value\)>)

The data to encode.

#### get_json_format 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlEncoder.get_json_format>)

`@classmethod`
    
    def get_json_format(cls) -> Literal['base64url']
    
Get the JSON format for the encoded data.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-14>)

[`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘base64url’] — The JSON format for the encoded data.

## EncodedBytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedBytes>)

A bytes type that is encoded and decoded using the specified encoder.

`EncodedBytes` needs an encoder that implements `EncoderProtocol` to operate.
    
    from typing import Annotated
    
    from pydantic import BaseModel, EncodedBytes, EncoderProtocol, ValidationError
    
    class MyEncoder(EncoderProtocol):
        @classmethod
        def decode(cls, data: bytes) -> bytes:
            if data == b'**undecodable**':
                raise ValueError('Cannot decode data')
            return data[13:]
    
        @classmethod
        def encode(cls, value: bytes) -> bytes:
            return b'**encoded**: ' + value
    
        @classmethod
        def get_json_format(cls) -> str:
            return 'my-encoder'
    
    MyEncodedBytes = Annotated[bytes, EncodedBytes(encoder=MyEncoder)]
    
    class Model(BaseModel):
        my_encoded_bytes: MyEncodedBytes
    
    # Initialize the model with encoded data
    m = Model(my_encoded_bytes=b'**encoded**: some bytes')
    
    # Access decoded value
    print(m.my_encoded_bytes)
    #> b'some bytes'
    
    # Serialize into the encoded form
    print(m.model_dump())
    #> {'my_encoded_bytes': b'**encoded**: some bytes'}
    
    # Validate encoded data
    try:
        Model(my_encoded_bytes=b'**undecodable**')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        my_encoded_bytes
          Value error, Cannot decode data [type=value_error, input_value=b'**undecodable**', input_type=bytes]
        '''
    
### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#methods-5>)

#### decode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedBytes.decode>)
    
    def decode(data: bytes, _: core_schema.ValidationInfo) -> bytes
    
Decode the data using the specified encoder.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-15>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The decoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-8>)

**`data`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedBytes.decode\(data\)>)

The data to decode.

#### encode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedBytes.encode>)
    
    def encode(value: bytes) -> bytes
    
Encode the data using the specified encoder.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-16>)

[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) — The encoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-9>)

**`value`** : [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedBytes.encode\(value\)>)

The data to encode.

## EncodedStr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedStr>)

A str type that is encoded and decoded using the specified encoder.

`EncodedStr` needs an encoder that implements `EncoderProtocol` to operate.
    
    from typing import Annotated
    
    from pydantic import BaseModel, EncodedStr, EncoderProtocol, ValidationError
    
    class MyEncoder(EncoderProtocol):
        @classmethod
        def decode(cls, data: bytes) -> bytes:
            if data == b'**undecodable**':
                raise ValueError('Cannot decode data')
            return data[13:]
    
        @classmethod
        def encode(cls, value: bytes) -> bytes:
            return b'**encoded**: ' + value
    
        @classmethod
        def get_json_format(cls) -> str:
            return 'my-encoder'
    
    MyEncodedStr = Annotated[str, EncodedStr(encoder=MyEncoder)]
    
    class Model(BaseModel):
        my_encoded_str: MyEncodedStr
    
    # Initialize the model with encoded data
    m = Model(my_encoded_str='**encoded**: some str')
    
    # Access decoded value
    print(m.my_encoded_str)
    #> some str
    
    # Serialize into the encoded form
    print(m.model_dump())
    #> {'my_encoded_str': '**encoded**: some str'}
    
    # Validate encoded data
    try:
        Model(my_encoded_str='**undecodable**')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        my_encoded_str
          Value error, Cannot decode data [type=value_error, input_value='**undecodable**', input_type=str]
        '''
    
### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#methods-6>)

#### decode_str 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedStr.decode_str>)
    
    def decode_str(data: str, _: core_schema.ValidationInfo) -> str
    
Decode the data using the specified encoder.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-17>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The decoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-10>)

**`data`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedStr.decode_str\(data\)>)

The data to decode.

#### encode_str 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedStr.encode_str>)
    
    def encode_str(value: str) -> str
    
Encode the data using the specified encoder.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-18>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The encoded data.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-11>)

**`value`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.EncodedStr.encode_str\(value\)>)

The data to encode.

## GetPydanticSchema 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.GetPydanticSchema>)

A convenience class for creating an annotation that provides pydantic custom type hooks.

This class is intended to eliminate the need to create a custom “marker” which defines the `__get_pydantic_core_schema__` and `__get_pydantic_json_schema__` custom hook methods.

For example, to have a field treated by type checkers as `int`, but by pydantic as `Any`, you can do:
    
    from typing import Annotated, Any
    
    from pydantic import BaseModel, GetPydanticSchema
    
    HandleAsAny = GetPydanticSchema(lambda _s, h: h(Any))
    
    class Model(BaseModel):
        x: Annotated[int, HandleAsAny]  # pydantic sees `x: Any`
    
    print(repr(Model(x='abc').x))
    #> 'abc'
    
## Tag 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Tag>)

Provides a way to specify the expected tag to use for a case of a (callable) discriminated union.

Also provides a way to label a union case in error messages.

When using a callable `Discriminator`, attach a `Tag` to each case in the `Union` to specify the tag that should be used to identify that case. For example, in the below example, the `Tag` is used to specify that if `get_discriminator_value` returns `'apple'`, the input should be validated as an `ApplePie`, and if it returns `'pumpkin'`, the input should be validated as a `PumpkinPie`.

The primary role of the `Tag` here is to map the return value from the callable `Discriminator` function to the appropriate member of the `Union` in question.
    
    from typing import Annotated, Any, Literal, Union
    
    from pydantic import BaseModel, Discriminator, Tag
    
    class Pie(BaseModel):
        time_to_cook: int
        num_ingredients: int
    
    class ApplePie(Pie):
        fruit: Literal['apple'] = 'apple'
    
    class PumpkinPie(Pie):
        filling: Literal['pumpkin'] = 'pumpkin'
    
    def get_discriminator_value(v: Any) -> str:
        if isinstance(v, dict):
            return v.get('fruit', v.get('filling'))
        return getattr(v, 'fruit', getattr(v, 'filling', None))
    
    class ThanksgivingDinner(BaseModel):
        dessert: Annotated[
            Union[
                Annotated[ApplePie, Tag('apple')],
                Annotated[PumpkinPie, Tag('pumpkin')],
            ],
            Discriminator(get_discriminator_value),
        ]
    
    apple_variation = ThanksgivingDinner.model_validate(
        {'dessert': {'fruit': 'apple', 'time_to_cook': 60, 'num_ingredients': 8}}
    )
    print(repr(apple_variation))
    '''
    ThanksgivingDinner(dessert=ApplePie(time_to_cook=60, num_ingredients=8, fruit='apple'))
    '''
    
    pumpkin_variation = ThanksgivingDinner.model_validate(
        {
            'dessert': {
                'filling': 'pumpkin',
                'time_to_cook': 40,
                'num_ingredients': 6,
            }
        }
    )
    print(repr(pumpkin_variation))
    '''
    ThanksgivingDinner(dessert=PumpkinPie(time_to_cook=40, num_ingredients=6, filling='pumpkin'))
    '''
    
See the [Discriminated Unions](<https://pydantic.dev/docs/validation/latest/concepts/unions#discriminated-unions>) concepts docs for more details on how to use `Tag`s.

## Discriminator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Discriminator>)

Provides a way to use a custom callable as the way to extract the value of a union discriminator.

This allows you to get validation behavior like you’d get from `Field(discriminator=<field_name>)`, but without needing to have a single shared field across all the union choices. This also makes it possible to handle unions of models and primitive types with discriminated-union-style validation errors. Finally, this allows you to use a custom callable as the way to identify which member of a union a value belongs to, while still seeing all the performance benefits of a discriminated union.

Consider this example, which is much more performant with the use of `Discriminator` and thus a `TaggedUnion` than it would be as a normal `Union`.
    
    from typing import Annotated, Any, Literal, Union
    
    from pydantic import BaseModel, Discriminator, Tag
    
    class Pie(BaseModel):
        time_to_cook: int
        num_ingredients: int
    
    class ApplePie(Pie):
        fruit: Literal['apple'] = 'apple'
    
    class PumpkinPie(Pie):
        filling: Literal['pumpkin'] = 'pumpkin'
    
    def get_discriminator_value(v: Any) -> str:
        if isinstance(v, dict):
            return v.get('fruit', v.get('filling'))
        return getattr(v, 'fruit', getattr(v, 'filling', None))
    
    class ThanksgivingDinner(BaseModel):
        dessert: Annotated[
            Union[
                Annotated[ApplePie, Tag('apple')],
                Annotated[PumpkinPie, Tag('pumpkin')],
            ],
            Discriminator(get_discriminator_value),
        ]
    
    apple_variation = ThanksgivingDinner.model_validate(
        {'dessert': {'fruit': 'apple', 'time_to_cook': 60, 'num_ingredients': 8}}
    )
    print(repr(apple_variation))
    '''
    ThanksgivingDinner(dessert=ApplePie(time_to_cook=60, num_ingredients=8, fruit='apple'))
    '''
    
    pumpkin_variation = ThanksgivingDinner.model_validate(
        {
            'dessert': {
                'filling': 'pumpkin',
                'time_to_cook': 40,
                'num_ingredients': 6,
            }
        }
    )
    print(repr(pumpkin_variation))
    '''
    ThanksgivingDinner(dessert=PumpkinPie(time_to_cook=40, num_ingredients=6, filling='pumpkin'))
    '''
    
See the [Discriminated Unions](<https://pydantic.dev/docs/validation/latest/concepts/unions#discriminated-unions>) concepts docs for more details on how to use `Discriminator`s.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#attributes-5>)

#### discriminator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Discriminator.discriminator>)

The callable or field name for discriminating the type in a tagged union.

A `Callable` discriminator must extract the value of the discriminator from the input. A `str` discriminator must be the name of a field to discriminate against.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Hashable`](<https://docs.python.org/3/library/typing.html#typing.Hashable>)]

#### custom_error_type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Discriminator.custom_error_type>)

Type to use in [custom errors](<https://pydantic.dev/docs/validation/latest/errors/errors>) replacing the standard discriminated union validation errors.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) **Default:** `None`

#### custom_error_message 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Discriminator.custom_error_message>)

Message to use in custom errors.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) **Default:** `None`

#### custom_error_context 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Discriminator.custom_error_context>)

Context to use in custom errors.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`float`](<https://docs.python.org/3/library/functions.html#float>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) **Default:** `None`

## FailFast 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FailFast>)

**Bases:** `PydanticMetadata`, `BaseMetadata`

A `FailFast` annotation can be used to specify that validation should stop at the first error.

This can be useful when you want to validate a large amount of data and you only need to know if it’s valid or not.

You might want to enable this setting if you want to validate your data faster (basically, if you use this, validation will be more performant with the caveat that you get less information).
    
    from typing import Annotated
    
    from pydantic import BaseModel, FailFast, ValidationError
    
    class Model(BaseModel):
        x: Annotated[list[int], FailFast()]
    
    # This will raise a single error for the first invalid value and stop validation
    try:
        obj = Model(x=[1, 2, 'a', 4, 5, 'b', 7, 8, 9, 'c'])
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        x.2
          Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='a', input_type=str]
        '''
    
## conint 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conint>)
    
    def conint(
        *,
        strict: bool | None = None,
        gt: int | None = None,
        ge: int | None = None,
        lt: int | None = None,
        le: int | None = None,
        multiple_of: int | None = None,
    ) -> type[int]
    
  * [ :x: Don't do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-701>)
  * [ :white_check_mark: Do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-702>)

    from pydantic import BaseModel, conint
    
    class Foo(BaseModel):
        bar: conint(strict=True, gt=0)
    
    from typing import Annotated
    
    from pydantic import BaseModel, Field
    
    class Foo(BaseModel):
        bar: Annotated[int, Field(strict=True, gt=0)]
    
A wrapper around `int` that allows for additional constraints.
    
    from pydantic import BaseModel, ValidationError, conint
    
    class ConstrainedExample(BaseModel):
        constrained_int: conint(gt=1)
    
    m = ConstrainedExample(constrained_int=2)
    print(repr(m))
    #> ConstrainedExample(constrained_int=2)
    
    try:
        ConstrainedExample(constrained_int=0)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('constrained_int',),
                'msg': 'Input should be greater than 1',
                'input': 0,
                'ctx': {'gt': 1},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-19>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`int`](<https://docs.python.org/3/library/functions.html#int>)] — The wrapped integer type.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-12>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conint\(strict\)>)

Whether to validate the integer in strict mode. Defaults to `None`.

**`gt`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conint\(gt\)>)

The value must be greater than this.

**`ge`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conint\(ge\)>)

The value must be greater than or equal to this.

**`lt`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conint\(lt\)>)

The value must be less than this.

**`le`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conint\(le\)>)

The value must be less than or equal to this.

**`multiple_of`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conint\(multiple_of\)>)

The value must be a multiple of this.

## confloat 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat>)
    
    def confloat(
        *,
        strict: bool | None = None,
        gt: float | None = None,
        ge: float | None = None,
        lt: float | None = None,
        le: float | None = None,
        multiple_of: float | None = None,
        allow_inf_nan: bool | None = None,
    ) -> type[float]
    
  * [ :x: Don't do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-703>)
  * [ :white_check_mark: Do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-704>)

    from pydantic import BaseModel, confloat
    
    class Foo(BaseModel):
        bar: confloat(strict=True, gt=0)
    
    from typing import Annotated
    
    from pydantic import BaseModel, Field
    
    class Foo(BaseModel):
        bar: Annotated[float, Field(strict=True, gt=0)]
    
A wrapper around `float` that allows for additional constraints.
    
    from pydantic import BaseModel, ValidationError, confloat
    
    class ConstrainedExample(BaseModel):
        constrained_float: confloat(gt=1.0)
    
    m = ConstrainedExample(constrained_float=1.1)
    print(repr(m))
    #> ConstrainedExample(constrained_float=1.1)
    
    try:
        ConstrainedExample(constrained_float=0.9)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('constrained_float',),
                'msg': 'Input should be greater than 1',
                'input': 0.9,
                'ctx': {'gt': 1.0},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-20>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`float`](<https://docs.python.org/3/library/functions.html#float>)] — The wrapped float type.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-13>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat\(strict\)>)

Whether to validate the float in strict mode.

**`gt`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat\(gt\)>)

The value must be greater than this.

**`ge`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat\(ge\)>)

The value must be greater than or equal to this.

**`lt`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat\(lt\)>)

The value must be less than this.

**`le`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat\(le\)>)

The value must be less than or equal to this.

**`multiple_of`** : [`float`](<https://docs.python.org/3/library/functions.html#float>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat\(multiple_of\)>)

The value must be a multiple of this.

**`allow_inf_nan`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confloat\(allow_inf_nan\)>)

Whether to allow `-inf`, `inf`, and `nan`.

## conbytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conbytes>)
    
    def conbytes(
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        strict: bool | None = None,
    ) -> type[bytes]
    
A wrapper around `bytes` that allows for additional constraints.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-21>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>)] — The wrapped bytes type.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-14>)

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conbytes\(min_length\)>)

The minimum length of the bytes.

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conbytes\(max_length\)>)

The maximum length of the bytes.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conbytes\(strict\)>)

Whether to validate the bytes in strict mode.

## constr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr>)
    
    def constr(
        *,
        strip_whitespace: bool | None = None,
        to_upper: bool | None = None,
        to_lower: bool | None = None,
        strict: bool | None = None,
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | Pattern[str] | None = None,
        ascii_only: bool | None = None,
    ) -> type[str]
    
  * [ :x: Don't do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-705>)
  * [ :white_check_mark: Do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-706>)

    from pydantic import BaseModel, constr
    
    class Foo(BaseModel):
        bar: constr(strip_whitespace=True, to_upper=True, pattern=r'^[A-Z]+$')
    
    from typing import Annotated
    
    from pydantic import BaseModel, StringConstraints
    
    class Foo(BaseModel):
        bar: Annotated[
            str,
            StringConstraints(
                strip_whitespace=True, to_upper=True, pattern=r'^[A-Z]+$'
            ),
        ]
    
A wrapper around `str` that allows for additional constraints.
    
    from pydantic import BaseModel, constr
    
    class Foo(BaseModel):
        bar: constr(strip_whitespace=True, to_upper=True)
    
    foo = Foo(bar='  hello  ')
    print(foo)
    #> bar='HELLO'
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-22>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] — The wrapped string type.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-15>)

**`strip_whitespace`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(strip_whitespace\)>)

Whether to remove leading and trailing whitespace.

**`to_upper`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(to_upper\)>)

Whether to turn all characters to uppercase.

**`to_lower`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(to_lower\)>)

Whether to turn all characters to lowercase.

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(strict\)>)

Whether to validate the string in strict mode.

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(min_length\)>)

The minimum length of the string.

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(max_length\)>)

The maximum length of the string.

**`pattern`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`Pattern`](<https://docs.python.org/3/library/typing.html#typing.Pattern>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(pattern\)>)

A regex pattern to validate the string against.

**`ascii_only`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.constr\(ascii_only\)>)

Whether the string should contain only ASCII characters.

## conset 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conset>)
    
    def conset(
        item_type: type[HashableItemType],
        *,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> type[set[HashableItemType]]
    
A wrapper around `typing.Set` that allows for additional constraints.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-23>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`set`](<https://docs.python.org/3/reference/expressions.html#set>)[`HashableItemType`]] — The wrapped set type.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-16>)

**`item_type`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`HashableItemType`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conset\(item_type\)>)

The type of the items in the set.

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conset\(min_length\)>)

The minimum length of the set.

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conset\(max_length\)>)

The maximum length of the set.

## confrozenset 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confrozenset>)
    
    def confrozenset(
        item_type: type[HashableItemType],
        *,
        min_length: int | None = None,
        max_length: int | None = None,
    ) -> type[frozenset[HashableItemType]]
    
A wrapper around `typing.FrozenSet` that allows for additional constraints.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-24>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`frozenset`](<https://docs.python.org/3/library/stdtypes.html#frozenset>)[`HashableItemType`]] — The wrapped frozenset type.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-17>)

**`item_type`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`HashableItemType`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confrozenset\(item_type\)>)

The type of the items in the frozenset.

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confrozenset\(min_length\)>)

The minimum length of the frozenset.

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.confrozenset\(max_length\)>)

The maximum length of the frozenset.

## conlist 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conlist>)
    
    def conlist(
        item_type: type[AnyItemType],
        *,
        min_length: int | None = None,
        max_length: int | None = None,
        unique_items: bool | None = None,
    ) -> type[list[AnyItemType]]
    
A wrapper around [`list`](<https://docs.python.org/3/glossary.html#term-list>) that adds validation.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-25>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[[`list`](<https://docs.python.org/3/glossary.html#term-list>)[`AnyItemType`]] — The wrapped list type.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-18>)

**`item_type`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`AnyItemType`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conlist\(item_type\)>)

The type of the items in the list.

**`min_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conlist\(min_length\)>)

The minimum length of the list. Defaults to None.

**`max_length`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conlist\(max_length\)>)

The maximum length of the list. Defaults to None.

**`unique_items`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.conlist\(unique_items\)>)

Whether the items in the list must be unique. Defaults to None.

## condecimal 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal>)
    
    def condecimal(
        *,
        strict: bool | None = None,
        gt: int | Decimal | None = None,
        ge: int | Decimal | None = None,
        lt: int | Decimal | None = None,
        le: int | Decimal | None = None,
        multiple_of: int | Decimal | None = None,
        max_digits: int | None = None,
        decimal_places: int | None = None,
        allow_inf_nan: bool | None = None,
    ) -> type[Decimal]
    
  * [ :x: Don't do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-707>)
  * [ :white_check_mark: Do this ](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#tab-panel-708>)

    from pydantic import BaseModel, condecimal
    
    class Foo(BaseModel):
        bar: condecimal(strict=True, allow_inf_nan=True)
    
    from decimal import Decimal
    from typing import Annotated
    
    from pydantic import BaseModel, Field
    
    class Foo(BaseModel):
        bar: Annotated[Decimal, Field(strict=True, allow_inf_nan=True)]
    
A wrapper around Decimal that adds validation.
    
    from decimal import Decimal
    
    from pydantic import BaseModel, ValidationError, condecimal
    
    class ConstrainedExample(BaseModel):
        constrained_decimal: condecimal(gt=Decimal('1.0'))
    
    m = ConstrainedExample(constrained_decimal=Decimal('1.1'))
    print(repr(m))
    #> ConstrainedExample(constrained_decimal=Decimal('1.1'))
    
    try:
        ConstrainedExample(constrained_decimal=Decimal('0.9'))
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('constrained_decimal',),
                'msg': 'Input should be greater than 1.0',
                'input': Decimal('0.9'),
                'ctx': {'gt': Decimal('1.0')},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    
### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-26>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[`Decimal`]

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-19>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(strict\)>)

Whether to validate the value in strict mode. Defaults to `None`.

**`gt`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(gt\)>)

The value must be greater than this. Defaults to `None`.

**`ge`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(ge\)>)

The value must be greater than or equal to this. Defaults to `None`.

**`lt`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(lt\)>)

The value must be less than this. Defaults to `None`.

**`le`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(le\)>)

The value must be less than or equal to this. Defaults to `None`.

**`multiple_of`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | `Decimal` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(multiple_of\)>)

The value must be a multiple of this. Defaults to `None`.

**`max_digits`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(max_digits\)>)

The maximum number of digits. Defaults to `None`.

**`decimal_places`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(decimal_places\)>)

The number of decimal places. Defaults to `None`.

**`allow_inf_nan`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condecimal\(allow_inf_nan\)>)

Whether to allow infinity and NaN. Defaults to `None`.

## condate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condate>)
    
    def condate(
        *,
        strict: bool | None = None,
        gt: date | None = None,
        ge: date | None = None,
        lt: date | None = None,
        le: date | None = None,
    ) -> type[date]
    
A wrapper for date that adds constraints.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#returns-27>)

[`type`](<https://docs.python.org/3/glossary.html#term-type>)[`date`] — A date type with the specified constraints.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#parameters-20>)

**`strict`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condate\(strict\)>)

Whether to validate the date value in strict mode. Defaults to `None`.

**`gt`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condate\(gt\)>)

The value must be greater than this. Defaults to `None`.

**`ge`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condate\(ge\)>)

The value must be greater than or equal to this. Defaults to `None`.

**`lt`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condate\(lt\)>)

The value must be less than this. Defaults to `None`.

**`le`** : `date` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.condate\(le\)>)

The value must be less than or equal to this. Defaults to `None`.

## StrictBool 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictBool>)

A boolean that must be either `True` or `False`.

**Default:** `Annotated[bool, Strict()]`

## PositiveInt 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PositiveInt>)

An integer that must be greater than zero.
    
    from pydantic import BaseModel, PositiveInt, ValidationError
    
    class Model(BaseModel):
        positive_int: PositiveInt
    
    m = Model(positive_int=1)
    print(repr(m))
    #> Model(positive_int=1)
    
    try:
        Model(positive_int=-1)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('positive_int',),
                'msg': 'Input should be greater than 0',
                'input': -1,
                'ctx': {'gt': 0},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    
**Default:** `Annotated[int, annotated_types.Gt(0)]`

## NegativeInt 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NegativeInt>)

An integer that must be less than zero.
    
    from pydantic import BaseModel, NegativeInt, ValidationError
    
    class Model(BaseModel):
        negative_int: NegativeInt
    
    m = Model(negative_int=-1)
    print(repr(m))
    #> Model(negative_int=-1)
    
    try:
        Model(negative_int=1)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'less_than',
                'loc': ('negative_int',),
                'msg': 'Input should be less than 0',
                'input': 1,
                'ctx': {'lt': 0},
                'url': 'https://errors.pydantic.dev/2/v/less_than',
            }
        ]
        '''
    
**Default:** `Annotated[int, annotated_types.Lt(0)]`

## NonPositiveInt 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonPositiveInt>)

An integer that must be less than or equal to zero.
    
    from pydantic import BaseModel, NonPositiveInt, ValidationError
    
    class Model(BaseModel):
        non_positive_int: NonPositiveInt
    
    m = Model(non_positive_int=0)
    print(repr(m))
    #> Model(non_positive_int=0)
    
    try:
        Model(non_positive_int=1)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'less_than_equal',
                'loc': ('non_positive_int',),
                'msg': 'Input should be less than or equal to 0',
                'input': 1,
                'ctx': {'le': 0},
                'url': 'https://errors.pydantic.dev/2/v/less_than_equal',
            }
        ]
        '''
    
**Default:** `Annotated[int, annotated_types.Le(0)]`

## NonNegativeInt 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonNegativeInt>)

An integer that must be greater than or equal to zero.
    
    from pydantic import BaseModel, NonNegativeInt, ValidationError
    
    class Model(BaseModel):
        non_negative_int: NonNegativeInt
    
    m = Model(non_negative_int=0)
    print(repr(m))
    #> Model(non_negative_int=0)
    
    try:
        Model(non_negative_int=-1)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than_equal',
                'loc': ('non_negative_int',),
                'msg': 'Input should be greater than or equal to 0',
                'input': -1,
                'ctx': {'ge': 0},
                'url': 'https://errors.pydantic.dev/2/v/greater_than_equal',
            }
        ]
        '''
    
**Default:** `Annotated[int, annotated_types.Ge(0)]`

## StrictInt 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictInt>)

An integer that must be validated in strict mode.
    
    from pydantic import BaseModel, StrictInt, ValidationError
    
    class StrictIntModel(BaseModel):
        strict_int: StrictInt
    
    try:
        StrictIntModel(strict_int=3.14159)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for StrictIntModel
        strict_int
          Input should be a valid integer [type=int_type, input_value=3.14159, input_type=float]
        '''
    
**Default:** `Annotated[int, Strict()]`

## PositiveFloat 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PositiveFloat>)

A float that must be greater than zero.
    
    from pydantic import BaseModel, PositiveFloat, ValidationError
    
    class Model(BaseModel):
        positive_float: PositiveFloat
    
    m = Model(positive_float=1.0)
    print(repr(m))
    #> Model(positive_float=1.0)
    
    try:
        Model(positive_float=-1.0)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than',
                'loc': ('positive_float',),
                'msg': 'Input should be greater than 0',
                'input': -1.0,
                'ctx': {'gt': 0.0},
                'url': 'https://errors.pydantic.dev/2/v/greater_than',
            }
        ]
        '''
    
**Default:** `Annotated[float, annotated_types.Gt(0)]`

## NegativeFloat 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NegativeFloat>)

A float that must be less than zero.
    
    from pydantic import BaseModel, NegativeFloat, ValidationError
    
    class Model(BaseModel):
        negative_float: NegativeFloat
    
    m = Model(negative_float=-1.0)
    print(repr(m))
    #> Model(negative_float=-1.0)
    
    try:
        Model(negative_float=1.0)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'less_than',
                'loc': ('negative_float',),
                'msg': 'Input should be less than 0',
                'input': 1.0,
                'ctx': {'lt': 0.0},
                'url': 'https://errors.pydantic.dev/2/v/less_than',
            }
        ]
        '''
    
**Default:** `Annotated[float, annotated_types.Lt(0)]`

## NonPositiveFloat 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonPositiveFloat>)

A float that must be less than or equal to zero.
    
    from pydantic import BaseModel, NonPositiveFloat, ValidationError
    
    class Model(BaseModel):
        non_positive_float: NonPositiveFloat
    
    m = Model(non_positive_float=0.0)
    print(repr(m))
    #> Model(non_positive_float=0.0)
    
    try:
        Model(non_positive_float=1.0)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'less_than_equal',
                'loc': ('non_positive_float',),
                'msg': 'Input should be less than or equal to 0',
                'input': 1.0,
                'ctx': {'le': 0.0},
                'url': 'https://errors.pydantic.dev/2/v/less_than_equal',
            }
        ]
        '''
    
**Default:** `Annotated[float, annotated_types.Le(0)]`

## NonNegativeFloat 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonNegativeFloat>)

A float that must be greater than or equal to zero.
    
    from pydantic import BaseModel, NonNegativeFloat, ValidationError
    
    class Model(BaseModel):
        non_negative_float: NonNegativeFloat
    
    m = Model(non_negative_float=0.0)
    print(repr(m))
    #> Model(non_negative_float=0.0)
    
    try:
        Model(non_negative_float=-1.0)
    except ValidationError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'greater_than_equal',
                'loc': ('non_negative_float',),
                'msg': 'Input should be greater than or equal to 0',
                'input': -1.0,
                'ctx': {'ge': 0.0},
                'url': 'https://errors.pydantic.dev/2/v/greater_than_equal',
            }
        ]
        '''
    
**Default:** `Annotated[float, annotated_types.Ge(0)]`

## StrictFloat 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictFloat>)

A float that must be validated in strict mode.
    
    from pydantic import BaseModel, StrictFloat, ValidationError
    
    class StrictFloatModel(BaseModel):
        strict_float: StrictFloat
    
    try:
        StrictFloatModel(strict_float='1.0')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for StrictFloatModel
        strict_float
          Input should be a valid number [type=float_type, input_value='1.0', input_type=str]
        '''
    
**Default:** `Annotated[float, Strict(True)]`

## FiniteFloat 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FiniteFloat>)

A float that must be finite (not `-inf`, `inf`, or `nan`).
    
    from pydantic import BaseModel, FiniteFloat
    
    class Model(BaseModel):
        finite: FiniteFloat
    
    m = Model(finite=1.0)
    print(m)
    #> finite=1.0
    
**Default:** `Annotated[float, AllowInfNan(False)]`

## StrictBytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictBytes>)

A bytes that must be validated in strict mode.

**Default:** `Annotated[bytes, Strict()]`

## StrictStr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictStr>)

A string that must be validated in strict mode.

**Default:** `Annotated[str, Strict()]`

## UUID1 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID1>)

A [UUID](<https://docs.python.org/3/library/uuid.html>) that must be version 1.
    
    import uuid
    
    from pydantic import UUID1, BaseModel
    
    class Model(BaseModel):
        uuid1: UUID1
    
    Model(uuid1=uuid.uuid1())
    
**Default:** `Annotated[UUID, UuidVersion(1)]`

## UUID3 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID3>)

A [UUID](<https://docs.python.org/3/library/uuid.html>) that must be version 3.
    
    import uuid
    
    from pydantic import UUID3, BaseModel
    
    class Model(BaseModel):
        uuid3: UUID3
    
    Model(uuid3=uuid.uuid3(uuid.NAMESPACE_DNS, 'pydantic.org'))
    
**Default:** `Annotated[UUID, UuidVersion(3)]`

## UUID4 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID4>)

A [UUID](<https://docs.python.org/3/library/uuid.html>) that must be version 4.
    
    import uuid
    
    from pydantic import UUID4, BaseModel
    
    class Model(BaseModel):
        uuid4: UUID4
    
    Model(uuid4=uuid.uuid4())
    
**Default:** `Annotated[UUID, UuidVersion(4)]`

## UUID5 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID5>)

A [UUID](<https://docs.python.org/3/library/uuid.html>) that must be version 5.
    
    import uuid
    
    from pydantic import UUID5, BaseModel
    
    class Model(BaseModel):
        uuid5: UUID5
    
    Model(uuid5=uuid.uuid5(uuid.NAMESPACE_DNS, 'pydantic.org'))
    
**Default:** `Annotated[UUID, UuidVersion(5)]`

## UUID6 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID6>)

A [UUID](<https://docs.python.org/3/library/uuid.html>) that must be version 6.
    
    import uuid
    
    from pydantic import UUID6, BaseModel
    
    class Model(BaseModel):
        uuid6: UUID6
    
    Model(uuid6=uuid.UUID('1efea953-c2d6-6790-aa0a-69db8c87df97'))
    
**Default:** `Annotated[UUID, UuidVersion(6)]`

## UUID7 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID7>)

A [UUID](<https://docs.python.org/3/library/uuid.html>) that must be version 7.
    
    import uuid
    
    from pydantic import UUID7, BaseModel
    
    class Model(BaseModel):
        uuid7: UUID7
    
    Model(uuid7=uuid.UUID('0194fdcb-1c47-7a09-b52c-561154de0b4a'))
    
**Default:** `Annotated[UUID, UuidVersion(7)]`

## UUID8 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID8>)

A [UUID](<https://docs.python.org/3/library/uuid.html>) that must be version 8.
    
    import uuid
    
    from pydantic import UUID8, BaseModel
    
    class Model(BaseModel):
        uuid8: UUID8
    
    Model(uuid8=uuid.UUID('81a0b92e-6078-8551-9c81-8ccb666bdab8'))
    
**Default:** `Annotated[UUID, UuidVersion(8)]`

## FilePath 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FilePath>)

A path that must point to a file.
    
    from pathlib import Path
    
    from pydantic import BaseModel, FilePath, ValidationError
    
    class Model(BaseModel):
        f: FilePath
    
    path = Path('text.txt')
    path.touch()
    m = Model(f='text.txt')
    print(m.model_dump())
    #> {'f': PosixPath('text.txt')}
    path.unlink()
    
    path = Path('directory')
    path.mkdir(exist_ok=True)
    try:
        Model(f='directory')  # directory
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        f
          Path does not point to a file [type=path_not_file, input_value='directory', input_type=str]
        '''
    path.rmdir()
    
    try:
        Model(f='not-exists-file')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        f
          Path does not point to a file [type=path_not_file, input_value='not-exists-file', input_type=str]
        '''
    
**Default:** `Annotated[Path, PathType('file')]`

## DirectoryPath 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.DirectoryPath>)

A path that must point to a directory.
    
    from pathlib import Path
    
    from pydantic import BaseModel, DirectoryPath, ValidationError
    
    class Model(BaseModel):
        f: DirectoryPath
    
    path = Path('directory/')
    path.mkdir()
    m = Model(f='directory/')
    print(m.model_dump())
    #> {'f': PosixPath('directory')}
    path.rmdir()
    
    path = Path('file.txt')
    path.touch()
    try:
        Model(f='file.txt')  # file
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        f
          Path does not point to a directory [type=path_not_directory, input_value='file.txt', input_type=str]
        '''
    path.unlink()
    
    try:
        Model(f='not-exists-directory')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        f
          Path does not point to a directory [type=path_not_directory, input_value='not-exists-directory', input_type=str]
        '''
    
**Default:** `Annotated[Path, PathType('dir')]`

## NewPath 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NewPath>)

A path for a new file or directory that must not already exist. The parent directory must already exist.

**Default:** `Annotated[Path, PathType('new')]`

## SocketPath 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.SocketPath>)

A path to an existing socket file

**Default:** `Annotated[Path, PathType('socket')]`

## Base64Bytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Bytes>)

A bytes type that is encoded and decoded using the standard (non-URL-safe) base64 encoder.

↻ Changed in v2.10

`Base64Bytes` now uses [`base64.b64encode()`](<https://docs.python.org/3/library/base64.html#base64.b64encode>) and [`base64.b64decode()`](<https://docs.python.org/3/library/base64.html#base64.b64decode>) instead of [`base64.encodebytes()`](<https://docs.python.org/3/library/base64.html#base64.encodebytes>) and [`base64.decodebytes()`](<https://docs.python.org/3/library/base64.html#base64.decodebytes>).

These methods are considered legacy implementation. If you’d still like to use these legacy encoders/decoders, you can achieve this by creating a custom annotated type, like follows:
    
    import base64
    from typing import Annotated, Literal
    
    from pydantic_core import PydanticCustomError
    
    from pydantic import EncodedBytes, EncoderProtocol
    
    class LegacyBase64Encoder(EncoderProtocol):
        @classmethod
        def decode(cls, data: bytes) -> bytes:
            try:
                return base64.decodebytes(data)
            except ValueError as e:
                raise PydanticCustomError(
                    'base64_decode',
                    "Base64 decoding error: '{error}'",
                    {'error': str(e)},
                )
    
        @classmethod
        def encode(cls, value: bytes) -> bytes:
            return base64.encodebytes(value)
    
        @classmethod
        def get_json_format(cls) -> Literal['base64']:
            return 'base64'
    
    LegacyBase64Bytes = Annotated[bytes, EncodedBytes(encoder=LegacyBase64Encoder)]
    
    from pydantic import Base64Bytes, BaseModel, ValidationError
    
    class Model(BaseModel):
        base64_bytes: Base64Bytes
    
    # Initialize the model with base64 data
    m = Model(base64_bytes=b'VGhpcyBpcyB0aGUgd2F5')
    
    # Access decoded value
    print(m.base64_bytes)
    #> b'This is the way'
    
    # Serialize into the base64 form
    print(m.model_dump())
    #> {'base64_bytes': b'VGhpcyBpcyB0aGUgd2F5'}
    
    # Validate base64 data
    try:
        print(Model(base64_bytes=b'undecodable').base64_bytes)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        base64_bytes
          Base64 decoding error: 'Incorrect padding' [type=base64_decode, input_value=b'undecodable', input_type=bytes]
        '''
    
**Default:** `Annotated[bytes, EncodedBytes(encoder=Base64Encoder)]`

## Base64Str 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Str>)

A string type that is encoded and decoded using the standard (non-URL-safe) base64 encoder.

↻ Changed in v2.10

`Base64Str` now uses [`base64.b64encode()`](<https://docs.python.org/3/library/base64.html#base64.b64encode>) and [`base64.b64decode()`](<https://docs.python.org/3/library/base64.html#base64.b64decode>) instead of [`base64.encodebytes()`](<https://docs.python.org/3/library/base64.html#base64.encodebytes>) and [`base64.decodebytes()`](<https://docs.python.org/3/library/base64.html#base64.decodebytes>).

These methods are considered legacy implementation. See the documentation about the [`Base64Bytes`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64Bytes>) type for more information on how to replicate the old behavior with the legacy encoders/decoders.
    
    from pydantic import Base64Str, BaseModel, ValidationError
    
    class Model(BaseModel):
        base64_str: Base64Str
    
    # Initialize the model with base64 data
    m = Model(base64_str='VGhlc2UgYXJlbid0IHRoZSBkcm9pZHMgeW91J3JlIGxvb2tpbmcgZm9y')
    
    # Access decoded value
    print(m.base64_str)
    #> These aren't the droids you're looking for
    
    # Serialize into the base64 form
    print(m.model_dump())
    #> {'base64_str': 'VGhlc2UgYXJlbid0IHRoZSBkcm9pZHMgeW91J3JlIGxvb2tpbmcgZm9y'}
    
    # Validate base64 data
    try:
        print(Model(base64_str='undecodable').base64_str)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        base64_str
          Base64 decoding error: 'Incorrect padding' [type=base64_decode, input_value='undecodable', input_type=str]
        '''
    
**Default:** `Annotated[str, EncodedStr(encoder=Base64Encoder)]`

## Base64UrlBytes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlBytes>)

A bytes type that is encoded and decoded using the URL-safe base64 encoder.
    
    from pydantic import Base64UrlBytes, BaseModel
    
    class Model(BaseModel):
        base64url_bytes: Base64UrlBytes
    
    # Initialize the model with base64 data
    m = Model(base64url_bytes=b'SHc_dHc-TXc==')
    print(m)
    #> base64url_bytes=b'Hw?tw>Mw'
    
**Default:** `Annotated[bytes, EncodedBytes(encoder=Base64UrlEncoder)]`

## Base64UrlStr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Base64UrlStr>)

A str type that is encoded and decoded using the URL-safe base64 encoder.
    
    from pydantic import Base64UrlStr, BaseModel
    
    class Model(BaseModel):
        base64url_str: Base64UrlStr
    
    # Initialize the model with base64 data
    m = Model(base64url_str='SHc_dHc-TXc==')
    print(m)
    #> base64url_str='Hw?tw>Mw'
    
**Default:** `Annotated[str, EncodedStr(encoder=Base64UrlEncoder)]`

## JsonValue 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.JsonValue>)

A `JsonValue` is used to represent a value that can be serialized to JSON.

It may be one of:

  * `list['JsonValue']`
  * `dict[str, 'JsonValue']`
  * `str`
  * `bool`
  * `int`
  * `float`
  * `None`

The following example demonstrates how to use `JsonValue` to validate JSON data, and what kind of errors to expect when input data is not json serializable.
    
    import json
    
    from pydantic import BaseModel, JsonValue, ValidationError
    
    class Model(BaseModel):
        j: JsonValue
    
    valid_json_data = {'j': {'a': {'b': {'c': 1, 'd': [2, None]}}}}
    invalid_json_data = {'j': {'a': {'b': ...}}}
    
    print(repr(Model.model_validate(valid_json_data)))
    #> Model(j={'a': {'b': {'c': 1, 'd': [2, None]}}})
    print(repr(Model.model_validate_json(json.dumps(valid_json_data))))
    #> Model(j={'a': {'b': {'c': 1, 'd': [2, None]}}})
    
    try:
        Model.model_validate(invalid_json_data)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Model
        j.dict.a.dict.b
          input was not a valid JSON value [type=invalid-json-value, input_value=Ellipsis, input_type=ellipsis]
        '''
    
**Type:** [`TypeAlias`](<https://docs.python.org/3/library/typing.html#typing.TypeAlias>) **Default:** `Union[list['JsonValue'], dict[str, 'JsonValue'], str, bool, int, float, None]`

## OnErrorOmit 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.OnErrorOmit>)

When used as an item in a list, the key type in a dict, optional values of a TypedDict, etc. this annotation omits the item from the iteration if there is any error validating it. That is, instead of a [`ValidationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.ValidationError>) being propagated up and the entire iterable being discarded any invalid items are discarded and the valid ones are returned.

**Default:** `Annotated[T, _OnErrorOmit]`

Was this page helpful?

Thanks for your feedback!