# Standard Library Types | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/](https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Standard Library Types

This section enumerates the supported built-in and standard library types: the allowed values, the possible constraints, and whether strictness can be configured.

See also the [conversion table](<https://pydantic.dev/docs/validation/latest/concepts/conversion_table>) for a summary of the allowed values for each type.

## Booleans

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#booleans>)

Built-in type: [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation>)

  * A valid [`bool`](<https://docs.python.org/3/library/functions.html#bool>) instance, i.e. `True` or `False`.
  * The integers `0` or `1`.
  * A string, which when converted to lowercase is one of `'0'`, `'off'`, `'f'`, `'false'`, `'n'`, `'no'`, `'1'`, `'on'` `'t'`, `'true'`, `'y'`, `'yes'`.
  * [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) objects that are valid per the previous rule when decoded to a string.

### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only boolean values are valid. Pydantic provides the [`StrictBool`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictBool>) type as a convenience to [using the `Strict()` metadata class](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode#using-the-strict-metadata-class>).

### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example>)
    
    from pydantic import BaseModel, ValidationError
    
    class BooleanModel(BaseModel):
        bool_value: bool
    
    print(BooleanModel(bool_value=False))
    #> bool_value=False
    print(BooleanModel(bool_value='False'))
    #> bool_value=False
    print(BooleanModel(bool_value=1))
    #> bool_value=True
    try:
        BooleanModel(bool_value=[])
    except ValidationError as e:
        print(str(e))
        """
        1 validation error for BooleanModel
        bool_value
          Input should be a valid boolean [type=bool_type, input_value=[], input_type=list]
        """
    
## Strings

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strings>)

Built-in type: [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-1>)

  * Strings are accepted as-is.
  * [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) and [`bytearray`](<https://docs.python.org/3/library/stdtypes.html#bytearray>) are decoded to UTF-8 strings.
  * [Enums](<https://docs.python.org/3/library/enum.html#module-enum>) are converted using the [`value`](<https://docs.python.org/3/library/enum.html#enum.Enum.value>) attribute, by calling [`str()`](<https://docs.python.org/3/library/stdtypes.html#str>) on it.
  * If [`coerce_numbers_to_str`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.coerce_numbers_to_str>) is set, any number type ([`int`](<https://docs.python.org/3/library/functions.html#int>), [`float`](<https://docs.python.org/3/library/functions.html#float>) and [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>)) will be coerced to a string and accepted as-is.

### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints>)

Strings support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`pattern`| A regex pattern that the string must match| [`pattern`](<https://json-schema.org/understanding-json-schema/reference/string#regexp>) keyword (see [note](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#pattern-constraint-note>) below).  
`min_length`| The minimum length of the string| [`minLength`](<https://json-schema.org/understanding-json-schema/reference/string#length>) keyword  
`max_length`| The maximum length of the string| [`maxLength`](<https://json-schema.org/understanding-json-schema/reference/string#length>) keyword  
`strip_whitespace`| Whether to remove leading and trailing whitespace| N/A  
`to_upper`| Whether to convert the string to uppercase| N/A  
`to_lower`| Whether to convert the string to lowercase| N/A  
`ascii_only`| Whether to allow only ASCII characters| N/A  
  
These constraints can be provided using the [`StringConstraints`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StringConstraints>) metadata type, or using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function (except for `strip_whitespace`, `to_upper`, `to_lower` and `ascii_only`).

The [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library also provides the `MinLen`, `MaxLen` and `Len` metadata types, as well as the `LowerCase`, `UpperCase`, `IsDigit` and `IsAscii` predicates (must be parameterized with `str`, e.g. `LowerCase[str]`).

### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-1>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only string values are valid. Pydantic provides the [`StrictStr`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictStr>) type as a convenience to [using the `Strict()` metadata class](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode#using-the-strict-metadata-class>).

### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-1>)
    
    from typing import Annotated
    
    from pydantic import BaseModel, StringConstraints
    
    class StringModel(BaseModel):
        str_value: str = ""
        constrained_str_value: Annotated[str, StringConstraints(to_lower=True)] = ""
    
    print(StringModel(str_value="test").str_value)
    #> test
    print(StringModel(constrained_str_value='TEST').constrained_str_value)
    #> test
    
## Bytes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#bytes>)

Built-in type: [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>).

See also: [`ByteSize`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.ByteSize>).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-2>)

  * [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) instances are validated as is.
  * Strings and [`bytearray`](<https://docs.python.org/3/library/stdtypes.html#bytearray>) instances are converted as bytes, following the [`val_json_bytes`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.val_json_bytes>) configuration value (despite its name, it applies to both Python and JSON modes).

### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-1>)

Strings support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`min_length`| The minimum length of the bytes| [`minLength`](<https://json-schema.org/understanding-json-schema/reference/string#length>) keyword  
`max_length`| The maximum length of the bytes| [`maxLength`](<https://json-schema.org/understanding-json-schema/reference/string#length>) keyword  
  
The `MinLen` and `MaxLen` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-2>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) instances are valid. Pydantic provides the [`StrictBytes`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictBytes>) type as a convenience to [using the `Strict()` metadata class](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode#using-the-strict-metadata-class>).

In JSON mode, strict mode has no effect.

## Numbers

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#numbers>)

Pydantic supports the following numeric types from the Python standard library:

### Integers

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#integers>)

Built-in type: [`int`](<https://docs.python.org/3/library/functions.html#int>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-3>)

  * Integers are validated as-is.
  * Strings and bytes are attempted to be converted to integers and validated as-is (see the [jiter implementation](<https://docs.rs/jiter/latest/jiter/enum.NumberInt.html#impl-TryFrom%3C%26%5Bu8%5D%3E-for-NumberInt>) for details).
  * Floats are validated as integers, provided the float input is not infinite or a NaN (not-a-number) and the fractional part is 0.
  * [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) instances, provided they are [finite](<https://docs.python.org/3/library/decimal.html#decimal.Decimal.is_finite>) and the denominator is 1.
  * [`Fraction`](<https://docs.python.org/3/library/fractions.html#fractions.Fraction>) instances, provided they are [integers](<https://docs.python.org/3/library/fractions.html#fractions.Fraction.is_integer>).
  * [Enums](<https://docs.python.org/3/library/enum.html#module-enum>) are converted using the [`value`](<https://docs.python.org/3/library/enum.html#enum.Enum.value>) attribute.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-2>)

Integers support the following constraints (numbers must be coercible to integers):

Constraint| Description| JSON Schema  
---|---|---  
`le`| The value must be less than or equal to this number| [`maximum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`ge`| The value must be greater than or equal to this number| [`minimum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`lt`| The value must be strictly less than this number| [`exclusiveMaximum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`gt`| The value must be strictly greater than this number| [`exclusiveMinimum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`multiple_of`| The value must be a multiple of this number| [`multipleOf`](<https://json-schema.org/understanding-json-schema/reference/numeric#multiples>) keyword  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `Le`, `Ge`, `Lt`, `Gt` and `MultipleOf` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

Pydantic also provides the following types to further constrain the allowed integer values:

  * [`PositiveInt`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PositiveInt>): Requires the input to be greater than zero.
  * [`NegativeInt`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NegativeInt>): Requires the input to be less than zero.
  * [`NonPositiveInt`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonPositiveInt>): Requires the input to be less than or equal to zero.
  * [`NonNegativeInt`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonNegativeInt>): Requires the input to be greater than or equal to zero.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-3>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only integer values are valid. Pydantic provides the [`StrictInt`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictInt>) type as a convenience to [using the `Strict()` metadata class](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode#using-the-strict-metadata-class>).

### Floats

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#floats>)

Built-in type: [`float`](<https://docs.python.org/3/library/functions.html#float>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-4>)

  * Floats are validated as-is.
  * String and bytes are attempted to be converted to floats and validated as-is. (see the [Rust implementation](<https://doc.rust-lang.org/src/core/num/dec2flt/mod.rs.html>) for details).
  * If the input has a [`__float__()`](<https://docs.python.org/3/reference/datamodel.html#object.__float__>) method, it will be called to convert the input into a float. If `__float__()` is not defined, it falls back to [`__index__()`](<https://docs.python.org/3/reference/datamodel.html#object.__index__>). This includes (but not limited to) the [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) and [`Fraction`](<https://docs.python.org/3/library/fractions.html#fractions.Fraction>) types.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-3>)

Floats support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`le`| The value must be less than or equal to this number| [`maximum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`ge`| The value must be greater than or equal to this number| [`minimum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`lt`| The value must be strictly less than this number| [`exclusiveMaximum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`gt`| The value must be strictly greater than this number| [`exclusiveMinimum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`multiple_of`| The value must be a multiple of this number| [`multipleOf`](<https://json-schema.org/understanding-json-schema/reference/numeric#multiples>) keyword  
`allow_inf_nan`| Whether to allow NaN (not-a-number) and infinite values| N/A  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function.

The [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library also provides the `Le`, `Ge`, `Lt`, `Gt` and `MultipleOf` metadata types, as well as the `IsFinite`, `IsNotFinite`, `IsNan`, `IsNotNan`, `IsAscii`, `IsInfinite` and `IsNotInfinite` predicates (must be parameterized with `float`, e.g. `IsFinite[float]`). The [`AllowInfNan`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.AllowInfNan>) type can also be used.

Pydantic also provides the following types as convenience aliases:

  * [`PositiveFloat`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PositiveFloat>): Requires the input to be greater than zero.
  * [`NegativeFloat`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NegativeFloat>): Requires the input to be less than zero.
  * [`NonPositiveFloat`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonPositiveFloat>): Requires the input to be less than or equal to zero.
  * [`NonNegativeFloat`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NonNegativeFloat>): Requires the input to be greater than or equal to zero.
  * [`FiniteFloat`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FiniteFloat>): Prevents NaN (not-a-number) and infinite values.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-4>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only float values and inputs having a [`__float__()`](<https://docs.python.org/3/reference/datamodel.html#object.__float__>) or [`__index__()`](<https://docs.python.org/3/reference/datamodel.html#object.__index__>) method are valid. Pydantic provides the [`StrictFloat`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictFloat>) type as a convenience to [using the `Strict()` metadata class](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode#using-the-strict-metadata-class>).

### Integer enums

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#integer-enums>)

Standard library type: [`enum.IntEnum`](<https://docs.python.org/3/library/enum.html#enum.IntEnum>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-5>)

  * If the [`enum.IntEnum`](<https://docs.python.org/3/library/enum.html#enum.IntEnum>) type is used directly, any [`enum.IntEnum`](<https://docs.python.org/3/library/enum.html#enum.IntEnum>) instance is validated as-is
  * If an [`enum.IntEnum`](<https://docs.python.org/3/library/enum.html#enum.IntEnum>) subclass is used as a type, any enum member or value that correspond to the enum members values is validated as-is.

See [Enums](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#enums>) for more details.

### Decimals

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#decimals>)

Standard library type: [`decimal.Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-6>)

  * [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) instances are validated as is.
  * Any value accepted by the [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) constructor.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-4>)

Decimals support the following constraints (numbers must be coercible to decimals):

Constraint| Description| JSON Schema  
---|---|---  
`le`| The value must be less than or equal to this number| [`maximum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`ge`| The value must be greater than or equal to this number| [`minimum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`lt`| The value must be strictly less than this number| [`exclusiveMaximum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`gt`| The value must be strictly greater than this number| [`exclusiveMinimum`](<https://json-schema.org/understanding-json-schema/reference/numeric#range>) keyword  
`multiple_of`| The value must be a multiple of this number| [`multipleOf`](<https://json-schema.org/understanding-json-schema/reference/numeric#multiples>) keyword  
`allow_inf_nan`| Whether to allow NaN (not-a-number) and infinite values| N/A  
`max_digits`| The maximum number of decimal digits allowed. The zero before the decimal point and trailing zeros are not counted.| [`pattern`](<https://json-schema.org/understanding-json-schema/reference/string#regexp>) keyword, to describe the string pattern  
`decimal_places`| The maximum number of decimal places allowed. Trailing zeros are not counted.| [`pattern`](<https://json-schema.org/understanding-json-schema/reference/string#regexp>) keyword, to describe the string pattern  
  
Note that the JSON Schema [`pattern`](<https://json-schema.org/understanding-json-schema/reference/string#regexp>) keyword will be specified in the JSON Schema to describe the string pattern in all cases (and can vary if `max_digits` and/or `decimal_places` is specified).

These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `Le`, `Ge`, `Lt`, `Gt` and `MultipleOf` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library and the [`AllowInfNan`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.AllowInfNan>) type can also be used.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-5>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`decimal.Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) instances are accepted. In JSON mode, strict mode has no effect.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings. A [serializer](<https://pydantic.dev/docs/validation/latest/concepts/serialization#field-plain-serializer>) can be used to override this behavior:
    
    from decimal import Decimal
    from typing import Annotated
    
    from pydantic import BaseModel, PlainSerializer
    
    class Model(BaseModel):
      f: Annotated[Decimal, PlainSerializer(float, when_used='json')]
    
    my_model = Model(f=Decimal('2.1'))
    
    print(my_model.model_dump())  # (1)
    #> {'f': Decimal('2.1')}
    print(my_model.model_dump_json())  # (2)
    #> {"f":2.1}

In Python mode, `f`remains a [`Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) instance.

In JSON mode, `f` is serialized as a float.

### Complex numbers

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#complex-numbers>)

✦ New in v2.9

Built-in type: [`complex`](<https://docs.python.org/3/library/functions.html#complex>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-7>)

  * [`complex`](<https://docs.python.org/3/library/functions.html#complex>) instances are validated as-is.
  * In Python mode, data is validated using the [`complex()`](<https://docs.python.org/3/library/functions.html#complex>) constructor.
  * In JSON mode, string are validated using the [`complex()`](<https://docs.python.org/3/library/functions.html#complex>) constructor, numbers (integers and floats) are used as the real part.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-6>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`complex`](<https://docs.python.org/3/library/functions.html#complex>) instances are accepted. In JSON mode, only strings that are accepted by the [`complex()`](<https://docs.python.org/3/library/functions.html#complex>) constructor are allowed.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-1>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), [`complex`](<https://docs.python.org/3/library/functions.html#complex>) instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

### Fractions

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#fractions>)

✦ New in v2.10

Standard library type: [`fractions.Fraction`](<https://docs.python.org/3/library/fractions.html#fractions.Fraction>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-8>)

  * [`Fraction`](<https://docs.python.org/3/library/fractions.html#fractions.Fraction>) instances are validated as is.
  * Floats, strings and [`decimal.Decimal`](<https://docs.python.org/3/library/decimal.html#decimal.Decimal>) instances are validated using the [`Fraction()`](<https://docs.python.org/3/library/fractions.html#fractions.Fraction>) constructor.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-7>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`Fraction`](<https://docs.python.org/3/library/fractions.html#fractions.Fraction>) instances are accepted. In JSON mode, strict mode has no effect.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-2>)

Fractions are serialized as strings, both in [Python](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>) and [JSON](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>) modes.

## Date and time types

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#date-and-time-types>)

Pydantic supports the following [date and time](<https://docs.python.org/library/datetime.html#available-types>) types from the [`datetime`](<https://docs.python.org/3/library/datetime.html#module-datetime>) standard library:

### Datetimes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#datetimes>)

Standard library type: [`datetime.datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-9>)

  * [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) instances are validated as is.
  * Strings and bytes are validated in two ways: 
    * Strings complying to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) format (both datetime and date). See the [speedate](<https://docs.rs/speedate/>) documentation for more details.
    * Unix timestamps, both as seconds or milliseconds sinch the [epoch](<https://en.wikipedia.org/wiki/Unix_time>). See the [`val_temporal_unit`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.val_temporal_unit>) configuration value for more details.
  * Integers and floats (or types that can be coerced as integers or floats) are validated as unix timestamps, following the same semantics as strings.
  * [`datetime.date`](<https://docs.python.org/3/library/datetime.html#datetime.date>) instances are accepted, and converted to a [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) instance by setting the [`hour`](<https://docs.python.org/3/library/datetime.html#datetime.datetime.hour>), [`minute`](<https://docs.python.org/3/library/datetime.html#datetime.datetime.minute>), [`second`](<https://docs.python.org/3/library/datetime.html#datetime.datetime.second>) and [`microsecond`](<https://docs.python.org/3/library/datetime.html#datetime.datetime.microsecond>) attributes to `0`, and the [`tzinfo`](<https://docs.python.org/3/library/datetime.html#datetime.datetime.tzinfo>) attribute to `None`.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-3>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-5>)

Datetimes support the following constraints (constraint values must be coercible to a [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) instance):

Constraint| Description| JSON Schema  
---|---|---  
`le`| The value must be less than or equal to this datetime| N/A  
`ge`| The value must be greater than or equal to this datetime| N/A  
`lt`| The value must be strictly less than this datetime| N/A  
`gt`| The value must be strictly greater than this datetime| N/A  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `Le`, `Ge`, `Lt` and `Gt` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

Pydantic also provides the following types to further constrain the allowed datetime values:

  * [`AwareDatetime`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.AwareDatetime>): Requires the input to have a timezone.
  * [`NaiveDatetime`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.NaiveDatetime>): Requires the input to _not_ have a timezone.
  * [`PastDatetime`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PastDatetime>): Requires the input to be in the past when validated.
  * [`FutureDatetime`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FutureDatetime>): Requires the input to be in the future when validated.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-8>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`datetime`](<https://docs.python.org/3/library/datetime.html#datetime.datetime>) instances are accepted. In JSON mode, only strings complying to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) format (_only_ datetime) or as unix timestamps are accepted.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-2>)
    
    from datetime import datetime
    from typing import Annotated
    
    from pydantic import AwareDatetime, BaseModel, Field
    
    class Event(BaseModel):
        dt: Annotated[AwareDatetime, Field(gt=datetime(2000, 1, 1))]
    
    event = Event(dt='2032-04-23T10:20:30.400+02:30')
    
    print(event.model_dump())
    """
    {'dt': datetime.datetime(2032, 4, 23, 10, 20, 30, 400000, tzinfo=TzInfo(9000))}
    """
    print(event.model_dump_json())
    #> {"dt":"2032-04-23T10:20:30.400000+02:30"}
    
### Dates

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#dates>)

Standard library type: [`datetime.date`](<https://docs.python.org/3/library/datetime.html#datetime.date>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-10>)

  * [`date`](<https://docs.python.org/3/library/datetime.html#datetime.date>) instances are validated as is.
  * Strings and bytes are validated in two ways: 
    * Strings complying to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) date format. See the [speedate](<https://docs.rs/speedate/>) documentation for more details.
    * Unix timestamps, both as seconds or milliseconds sinch the [epoch](<https://en.wikipedia.org/wiki/Unix_time>). See the [`val_temporal_unit`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.val_temporal_unit>) configuration value for more details.
  * If the validation fails, the input can be [validated as a datetime](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#datetimes>) (including as numbers), provided that the time component is 0 and that it is naive.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-4>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), [`date`](<https://docs.python.org/3/library/datetime.html#datetime.date>) instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-6>)

Dates support the following constraints (constraint values must be coercible to a [`date`](<https://docs.python.org/3/library/datetime.html#datetime.date>) instance):

Constraint| Description| JSON Schema  
---|---|---  
`le`| The value must be less than or equal to this date| N/A  
`ge`| The value must be greater than or equal to this date| N/A  
`lt`| The value must be strictly less than this date| N/A  
`gt`| The value must be strictly greater than this date| N/A  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `Le`, `Ge`, `Lt` and `Gt` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

Pydantic also provides the following types to further constrain the allowed date values:

  * [`PastDate`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PastDate>): Requires the input to be in the past when validated.
  * [`FutureDate`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.FutureDate>): Requires the input to be in the future when validated.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-9>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`date`](<https://docs.python.org/3/library/datetime.html#datetime.date>) instances are accepted. In JSON mode, only strings complying to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) format (_only_ date) or as unix timestamps are accepted.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-3>)
    
    from datetime import date
    
    from pydantic import BaseModel
    
    class Birthday(BaseModel):
        d: date
    
    my_birthday = Birthday(d=1679616000.0)
    
    print(my_birthday.model_dump())
    #> {'d': datetime.date(2023, 3, 24)}
    print(my_birthday.model_dump_json())
    #> {"d":"2023-03-24"}
    
### Time

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#time>)

Standard library type: [`datetime.time`](<https://docs.python.org/3/library/datetime.html#datetime.time>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-11>)

  * [`time`](<https://docs.python.org/3/library/datetime.html#datetime.time>) instances are validated as is.
  * Strings and bytes are validated according to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) time format.
  * Integers and floats (or values that can be coerced to such numbers) are validated as seconds. The value should not exceed 86 399.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-5>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), [`time`](<https://docs.python.org/3/library/datetime.html#datetime.time>) instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-7>)

Time support the following constraints (constraint values must be coercible to a [`time`](<https://docs.python.org/3/library/datetime.html#datetime.time>) instance):

Constraint| Description| JSON Schema  
---|---|---  
`le`| The value must be less than or equal to this time| N/A  
`ge`| The value must be greater than or equal to this time| N/A  
`lt`| The value must be strictly less than this time| N/A  
`gt`| The value must be strictly greater than this time| N/A  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `Le`, `Ge`, `Lt` and `Gt` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-10>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`time`](<https://docs.python.org/3/library/datetime.html#datetime.time>) instances are accepted. In JSON mode, only strings complying to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) format are accepted.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-4>)
    
    from datetime import time
    
    from pydantic import BaseModel
    
    class Meeting(BaseModel):
        t: time
    
    m = Meeting(t=time(4, 8, 16))
    
    print(m.model_dump())
    #> {'t': datetime.time(4, 8, 16)}
    print(m.model_dump_json())
    #> {"t":"04:08:16"}
    
### Timedeltas

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#timedeltas>)

Standard library type: [`datetime.timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-12>)

  * [`timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) instances are validated as is.
  * Strings and bytes are validated according to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) time format.
  * Integers and floats (or values that can be coerced to such numbers) are validated as seconds.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-8>)

Timedeltas support the following constraints (constraint values must be coercible to a [`timedata`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) instance):

| Constraint | Description | JSON Schema | | ---------- | ---------------------------------------------------- -----| ----------- | | `le` | The value must be less than or equal to this timedelta | N/A | | `ge` | The value must be greater than or equal to this timedelta | N/A | | `lt` | The value must be strictly less than this timedelta | N/A | | `gt` | The value must be strictly greater than this timedelta | N/A |

These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `Le`, `Ge`, `Lt` and `Gt` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-6>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), [`timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-11>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`timedelta`](<https://docs.python.org/3/library/datetime.html#datetime.timedelta>) instances are accepted. In JSON mode, only strings complying to the [RFC 3339](<https://datatracker.ietf.org/doc/html/rfc3339>) format are accepted.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-5>)
    
    from datetime import timedelta
    
    from pydantic import BaseModel
    
    class Model(BaseModel):
        td: timedelta
    
    m = Model(td='P3DT12H30M5S')
    
    print(m.model_dump())
    #> {'td': datetime.timedelta(days=3, seconds=45005)}
    print(m.model_dump_json())
    #> {"td":"P3DT12H30M5S"}
    
## Enums

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#enums>)

Standard library type: [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum>).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-13>)

  * If the [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum>) type is used directly, any [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum>) instance is validated as-is.
  * If an [`enum.Enum`](<https://docs.python.org/3/library/enum.html#enum.Enum>) subclass is used as a type, any enum member or value that correspond to the enum members [values](<https://docs.python.org/3/library/enum.html#enum.Enum.value>) is validated as-is.

### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-7>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), enum instances are serialized as is. The [`use_enum_values`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.use_enum_values>) configuration value can be set to use the enum [value](<https://docs.python.org/3/library/enum.html#enum.Enum.value>) during validation (so that it is also used during serialization).

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), enum instances are serialized using their [value](<https://docs.python.org/3/library/enum.html#enum.Enum.value>).

### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-6>)
    
    from enum import Enum, IntEnum
    
    from pydantic import BaseModel, ValidationError
    
    class FruitEnum(str, Enum):
        PEAR = 'pear'
        BANANA = 'banana'
    
    class ToolEnum(IntEnum):
        SPANNER = 1
        WRENCH = 2
    
    class CookingModel(BaseModel):
        fruit: FruitEnum = FruitEnum.PEAR
        tool: ToolEnum = ToolEnum.SPANNER
    
    print(CookingModel())
    #> fruit=<FruitEnum.PEAR: 'pear'> tool=<ToolEnum.SPANNER: 1>
    print(CookingModel(tool=2, fruit='banana'))
    #> fruit=<FruitEnum.BANANA: 'banana'> tool=<ToolEnum.WRENCH: 2>
    try:
        CookingModel(fruit='other')
    except ValidationError as e:
        print(e)
        """
        1 validation error for CookingModel
        fruit
          Input should be 'pear' or 'banana' [type=enum, input_value='other', input_type=str]
        """
    
## None types

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#none-types>)

Supported types: [`None`](<https://docs.python.org/3/library/constants.html#None>), [`NoneType`](<https://docs.python.org/3/library/types.html#types.NoneType>) or `Literal[None]` (they are [equivalent](<https://typing.readthedocs.io/en/latest/spec/special-types.html#none>)).

Allows only `None` as a value.

## Generic collection types

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#generic-collection-types>)

Pydantic supports a wide variety of generic collection types, both built-ins (such as [`list`](<https://docs.python.org/3/glossary.html#term-list>)) and abstract base classes from the [`collections.abc`](<https://docs.python.org/3/library/collections.abc.html#module-collections.abc>) module (such as [`Sequence`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence>)).

In most cases, it is recommended to make use of the built-in types over the abstract ones. Due to [data coercion](<https://pydantic.dev/docs/validation/latest/concepts/models#data-conversion>), using [`list`](<https://docs.python.org/3/glossary.html#term-list>) or [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>) will allow most other iterables as input, with better performance.

### Lists

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#lists>)

Built-in type: [`list`](<https://docs.python.org/3/glossary.html#term-list>) (deprecated alias: [`typing.List`](<https://docs.python.org/3/library/typing.html#typing.List>)).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-14>)

  * Allows [`list`](<https://docs.python.org/3/glossary.html#term-list>), [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>), [`set`](<https://docs.python.org/3/reference/expressions.html#set>) and [`frozenset`](<https://docs.python.org/3/library/stdtypes.html#frozenset>) instances, or any iterable that is _not_ a [string](<https://docs.python.org/3/library/stdtypes.html#str>), [bytes](<https://docs.python.org/3/library/stdtypes.html#bytes>), [bytearray](<https://docs.python.org/3/library/stdtypes.html#bytearray>), [dict](<https://docs.python.org/3/reference/expressions.html#dict>) or [mapping](<https://docs.python.org/3/glossary.html#term-mapping>). Produces a [`list`](<https://docs.python.org/3/glossary.html#term-list>) instance.
  * If a generic parameter is provided, the appropriate validation is applied to all items of the list.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-9>)

Lists support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`min_length`| The list must have at least this many items| [`minItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
`max_length`| The list must have at most this many items| [`maxItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `MinLen` and `MaxLen` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-12>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`list`](<https://docs.python.org/3/glossary.html#term-list>) instances are valid. Strict mode does _not_ apply to the items of the list. The strict constraint must be applied to the parameter type for this to work.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-7>)
    
    from typing import Optional
    
    from pydantic import BaseModel, Field
    
    class Model(BaseModel):
        simple_list: Optional[list[object]] = None
        list_of_ints: Optional[list[int]] = Field(default=None, strict=True)
    
    print(Model(simple_list=('1', '2', '3')).simple_list)
    #> ['1', '2', '3']
    print(Model(list_of_ints=['1', 2, 3]).list_of_ints)
    #> [1, 2, 3]
    
### Tuples

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#tuples>)

Built-in type: [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>) (deprecated alias: [`typing.Tuple`](<https://docs.python.org/3/library/typing.html#typing.Tuple>)).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-15>)

  * Allows [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>), [`list`](<https://docs.python.org/3/glossary.html#term-list>), [`set`](<https://docs.python.org/3/reference/expressions.html#set>) and [`frozenset`](<https://docs.python.org/3/library/stdtypes.html#frozenset>) instances, or any iterable that is _not_ a [string](<https://docs.python.org/3/library/stdtypes.html#str>), [bytes](<https://docs.python.org/3/library/stdtypes.html#bytes>), [bytearray](<https://docs.python.org/3/library/stdtypes.html#bytearray>), [dict](<https://docs.python.org/3/reference/expressions.html#dict>) or [mapping](<https://docs.python.org/3/glossary.html#term-mapping>). Produces a [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>) instance.
  * Appropriate validation is applied to items of the tuple, if [element types](<https://typing.python.org/en/latest/spec/tuples.html#tuple-type-form>) are specified.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-10>)

Lists support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`min_length`| The tuple must have at least this many items| [`minItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
`max_length`| The tuple must have at most this many items| [`maxItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `MinLen` and `MaxLen` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

Additionally, the [`prefixItems`](<https://json-schema.org/understanding-json-schema/reference/array#tupleValidation>) JSON Schema keyword may be used depending on the tuple shape.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-13>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>) instances are valid. Strict mode does _not_ apply to the items of the tuple. The strict constraint must be applied to the parameter types for this to work.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-8>)
    
    from typing import Optional
    
    from pydantic import BaseModel
    
    class Model(BaseModel):
        simple_tuple: Optional[tuple] = None
        tuple_of_different_types: Optional[tuple[int, float, bool]] = None
    
    print(Model(simple_tuple=[1, 2, 3, 4]).simple_tuple)
    #> (1, 2, 3, 4)
    print(Model(tuple_of_different_types=[3, 2, 1]).tuple_of_different_types)
    #> (3, 2.0, True)
    
### Named tuples

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#named-tuples>)

Standard library type: [`typing.NamedTuple`](<https://docs.python.org/3/library/typing.html#typing.NamedTuple>) (and types created by the [`collections.namedtuple()`](<https://docs.python.org/3/library/collections.html#collections.namedtuple>) factory function – each field will implicitly have the type [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-16>)

  * Allows [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>) and [`list`](<https://docs.python.org/3/glossary.html#term-list>) instances. Validate each item according to the field definition.
  * Allows [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>) instances. Keys must match the named tuple field names, and values are validated according to the field definition.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-8>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), named tuples are serialized as tuples. In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as arrays.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-9>)
    
    from typing import NamedTuple
    
    from pydantic import BaseModel
    
    class Point(NamedTuple):
        x: int
        y: int
    
    class Model(BaseModel):
        p: Point
    
    model = Model(p=('1', 2))
    
    print(model.model_dump())
    #> {'p': (1, 2)}
    
### Sets

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#sets>)

Types: [`set`](<https://docs.python.org/3/reference/expressions.html#set>) (or [`collections.abc.MutableSet`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.MutableSet>)) and [`frozenset`](<https://docs.python.org/3/library/stdtypes.html#frozenset>) (or [`collections.abc.Set`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Set>)) (deprecated aliases: [`typing.Set`](<https://docs.python.org/3/library/typing.html#typing.Set>) and [`typing.FrozenSet`](<https://docs.python.org/3/library/typing.html#typing.FrozenSet>)).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-17>)

  * Allows [`set`](<https://docs.python.org/3/reference/expressions.html#set>), [`frozenset`](<https://docs.python.org/3/library/stdtypes.html#frozenset>), [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>) and [`list`](<https://docs.python.org/3/glossary.html#term-list>) instances, or any iterable that is _not_ a [string](<https://docs.python.org/3/library/stdtypes.html#str>), [bytes](<https://docs.python.org/3/library/stdtypes.html#bytes>), [bytearray](<https://docs.python.org/3/library/stdtypes.html#bytearray>), [dict](<https://docs.python.org/3/reference/expressions.html#dict>) or [mapping](<https://docs.python.org/3/glossary.html#term-mapping>). Produces a [`set`](<https://docs.python.org/3/reference/expressions.html#set>) or [`frozenset`](<https://docs.python.org/3/library/stdtypes.html#frozenset>) instance.
  * If a generic parameter is provided, the appropriate validation is applied to all items of the set/frozenset.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-11>)

Sets support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`min_length`| The set must have at least this many items| [`minItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
`max_length`| The set must have at most this many items| [`maxItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `MinLen` and `MaxLen` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-14>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`set`](<https://docs.python.org/3/reference/expressions.html#set>)/[`frozenset`](<https://docs.python.org/3/library/stdtypes.html#frozenset>) instances are valid. Strict mode does _not_ apply to the items of the set. The strict constraint must be applied to the parameter type for this to work.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-9>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), sets are serialized as is. In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as arrays.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-10>)
    
    from typing import Optional
    
    from pydantic import BaseModel
    
    class Model(BaseModel):
        simple_set: Optional[set] = None
        set_of_ints: Optional[frozenset[int]] = None
    
    print(Model(simple_set=['1', '2', '3']).simple_set)
    #> {'1', '2', '3'}
    print(Model(set_of_ints=['1', '2', '3']).set_of_ints)
    #> frozenset({1, 2, 3})
    
#### JSON Schema

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#json-schema>)

Pydantic does best effort to sort default values that are [`collections.abc.Set`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Set>) instances.

### Deque

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#deque>)

Standard library type: [`collections.deque`](<https://docs.python.org/3/library/collections.html#collections.deque>) (deprecated alias: [`typing.Deque`](<https://docs.python.org/3/library/typing.html#typing.Deque>)).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-18>)

Values are first validated as a [list](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#lists>), and then passed to the [`deque`](<https://docs.python.org/3/library/collections.html#collections.deque>) constructor.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-12>)

Deques support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`min_length`| The deque must have at least this many items| [`minItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
`max_length`| The deque must have at most this many items| [`maxItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `MinLen` and `MaxLen` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-15>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`deque`](<https://docs.python.org/3/library/collections.html#collections.deque>) instances are valid. Strict mode does _not_ apply to the items of the deque. The strict constraint must be applied to the parameter type for this to work.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-10>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), deques are serialized as is. In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as arrays.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-11>)
    
    from collections import deque
    
    from pydantic import BaseModel
    
    class Model(BaseModel):
        deque: deque[int]
    
    print(Model(deque=[1, 2, 3]).deque)
    #> deque([1, 2, 3])
    
### Sequences

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#sequences>)

Standard library type: [`collections.abc.Sequence`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence>) (deprecated alias: [`typing.Sequence`](<https://docs.python.org/3/library/typing.html#typing.Sequence>)).

In most cases, you will want to use the built-in types (such as [list](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#lists>) or [tuple](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#tuples>)) as [type coercion](<https://pydantic.dev/docs/validation/latest/concepts/models#data-conversion>) will apply. The [`Sequence`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence>) type can be used when you want to preserve the input type during serialization.

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-19>)

Any [`collections.abc.Sequence`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Sequence>) instance (expect strings and bytes) is accepted. It is converted to a list using the [`list()`](<https://docs.python.org/3/glossary.html#term-list>) constructor, and then converted back to the original input type.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-13>)

Sequences support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`min_length`| The sequence must have at least this many items| [`minItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
`max_length`| The sequence must have at most this many items| [`maxItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `MinLen` and `MaxLen` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

#### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-11>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), sequences are serialized as is. In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as arrays.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-12>)
    
    from collections.abc import Sequence
    
    from pydantic import BaseModel, ValidationError
    
    class Model(BaseModel):
        sequence_of_strs: Sequence[str]
    
    print(Model(sequence_of_strs=['a', 'bc']).sequence_of_strs)
    #> ['a', 'bc']
    print(Model(sequence_of_strs=('a', 'bc')).sequence_of_strs)
    #> ('a', 'bc')
    
    try:
        Model(sequence_of_strs='abc')
    except ValidationError as e:
        print(e)
        """
        1 validation error for Model
        sequence_of_strs
          'str' instances are not allowed as a Sequence value [type=sequence_str, input_value='abc', input_type=str]
        """
    
### Dictionaries

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#dictionaries>)

Built-in type: [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-20>)

  * [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>) instances are accepted as is.
  * [mappings](<https://docs.python.org/3/glossary.html#term-mapping>) instances are accepted and coerced to a [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>).
  * If generic parameters for keys and values are provided, the appropriate validation is applied.

#### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-14>)

Dictionaries support the following constraints:

Constraint| Description| JSON Schema  
---|---|---  
`min_length`| The dictionary must have at least this many items| [`minItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
`max_length`| The dictionary must have at most this many items| [`maxItems`](<https://json-schema.org/understanding-json-schema/reference/array#length>) keyword  
  
These constraints can be provided using the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function. The `MinLen` and `MaxLen` metadata types from the [`annotated-types`](<https://github.com/annotated-types/annotated-types>) library can also be used.

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-16>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>) instances are valid. Strict mode does _not_ apply to the keys and values of the dictionaries. The strict constraint must be applied to the parameter types for this to work.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-13>)
    
    from pydantic import BaseModel, ValidationError
    
    class Model(BaseModel):
        x: dict[str, int]
    
    m = Model(x={'foo': 1})
    print(m.model_dump())
    #> {'x': {'foo': 1}}
    
    try:
        Model(x='test')
    except ValidationError as e:
        print(e)
        """
        1 validation error for Model
        x
          Input should be a valid dictionary [type=dict_type, input_value='test', input_type=str]
        """
    
### Typed dictionaries

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#typed-dictionaries>)

Standard library type: [`typing.TypedDict`](<https://docs.python.org/3/library/typing.html#typing.TypedDict>) (see also: the [typing specification](<https://typing.python.org/en/latest/spec/typeddict.html>)).

[`TypedDict`](<https://docs.python.org/3/library/typing.html#typing.TypedDict>) declares a dictionary type that expects all of its instances to have a certain set of keys where each key is associated with a value of a consistent type.

This type [supports configuration](<https://pydantic.dev/docs/validation/latest/concepts/config#configuration-on-other-supported-types>).

#### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-17>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>) instances are valid (unlike mappings in lax mode). Strict mode does _not_ apply to the values of the typed dictionary. The strict constraint must be applied to the value types for this to work.

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-14>)
    
    from typing_extensions import TypedDict
    
    from pydantic import TypeAdapter, ValidationError
    
    class User(TypedDict):
        name: str
        id: int
    
    ta = TypeAdapter(User)
    
    print(ta.validate_python({'name': 'foo', 'id': 1}))
    #> {'name': 'foo', 'id': 1}
    
    try:
        ta.validate_python({'name': 'foo'})
    except ValidationError as e:
        print(e)
        """
        1 validation error for User
        id
          Field required [type=missing, input_value={'name': 'foo'}, input_type=dict]
        """
    
### Iterables

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#iterables>)

Standard library type: [`collections.abc.Iterable`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable>) (deprecated alias: [`typing.Iterable`](<https://docs.python.org/3/library/typing.html#typing.Iterable>)).

#### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-21>)

Iterables are lazily validated, and wrapped in an internal datastructure that can be iterated over (and will validate the items type while doing so). This means that even if you provide a concrete container such as a list, the validated type will _not_ be of type [`list`](<https://docs.python.org/3/glossary.html#term-list>). However, Pydantic will ensure that the input value is iterable by getting an [iterator](<https://docs.python.org/3/glossary.html#term-iterator>) from it (by calling [`iter()`](<https://docs.python.org/3/library/functions.html#iter>) on the value).

It is recommended to use concrete collection types (such as [lists](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#lists>)) instead, unless you are using an infinite iterator (in which case eagerly validating the input would result in an infinite loop).

#### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-15>)
    
    from collections.abc import Iterable
    
    from pydantic import BaseModel, ValidationError
    
    class Model(BaseModel):
        f: Iterable[str]
    
    m = Model(f=[1, 2])  # Validates fine
    
    try:
        next(m.f)
    except ValidationError as e:
        print(e)
        """
        1 validation error for ValidatorIterator
        0
          Input should be a valid string [type=string_type, input_value=1, input_type=int]
        """
    
## Callable

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#callable>)

Standard library type: [`collections.abc.Callable`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable>) (deprecated alias: [`typing.Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-22>)

Pydantic only validates that the input is a [callable](<https://docs.python.org/3/glossary.html#term-callable>) (using the [`callable()`](<https://docs.python.org/3/library/functions.html#callable>) function). It does _not_ validate the number of parameters or their type, nor the type of the return value.
    
    from typing import Callable
    
    from pydantic import BaseModel
    
    class Foo(BaseModel):
        callback: Callable[[int], int]
    
    m = Foo(callback=lambda x: x)
    print(m)
    #> callback=<function <lambda> at 0x0123456789ab>
    
### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-12>)

Callables are serialized as is. Callables can’t be serialized in [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>) (a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) is raised).

## IP Addresses

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#ip-addresses>)

Standard library types:

  * [`ipaddress.IPv4Address`](<https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Address>)
  * [`ipaddress.IPv4Interface`](<https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Interface>)
  * [`ipaddress.IPv4Network`](<https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv4Network>)
  * [`ipaddress.IPv6Address`](<https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv6Address>)
  * [`ipaddress.IPv6Interface`](<https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv6Interface>)
  * [`ipaddress.IPv6Network`](<https://docs.python.org/3/library/ipaddress.html#ipaddress.IPv6Network>)

See also: the [`IPvAnyAddress`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.IPvAnyAddress>), [`IPvAnyInterface`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.IPvAnyInterface>) and [`IPvAnyNetwork`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.IPvAnyNetwork>) Pydantic types.

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-23>)

  * Instances are validated as is.
  * Other input values are passed to the constructor of the relevant address type.

### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-18>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only the address types are accepted. In JSON mode, strict mode has no effect.

### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-13>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), IP addresses are serialized as is. In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

## UUID

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#uuid>)

Standard library type: [`uuid.UUID`](<https://docs.python.org/3/library/uuid.html#uuid.UUID>).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-24>)

  * [`UUID`](<https://docs.python.org/3/library/uuid.html#uuid.UUID>) instances are validated as is.
  * Strings and bytes are validated as UUIDs, and casted to a [`UUID`](<https://docs.python.org/3/library/uuid.html#uuid.UUID>) instance.

### Constraints

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#constraints-15>)

The [`UUID`](<https://docs.python.org/3/library/uuid.html#uuid.UUID>) type supports a `version` constraint. The [`UuidVersion`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UuidVersion>) metadata type can be used.

Pydantic also provides the following types as convenience aliases: [`UUID1`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID1>), [`UUID3`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID3>), [`UUID4`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID4>), [`UUID5`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID5>), [`UUID6`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID6>), [`UUID7`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID7>), [`UUID8`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.UUID8>).

### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-19>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only [`UUID`](<https://docs.python.org/3/library/uuid.html#uuid.UUID>) instances are accepted. In JSON mode, strict mode has no effect.

### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-14>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), UUIDs are serialized as is. In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-16>)
    
    from typing import Annotated
    from uuid import UUID
    
    from pydantic import BaseModel
    from pydantic.types import UUID7, UuidVersion
    
    class Model(BaseModel):
        u1: UUID7
        u2: Annotated[UUID, UuidVersion(4)]
    
    print(
        Model(
            u1='01999b2c-8353-749b-8dac-859307fae22b',
            u2=UUID('125725f3-e1b4-44e3-90c3-1a20eab12da5'),
        )
    )
    """
    u1=UUID('01999b2c-8353-749b-8dac-859307fae22b') u2=UUID('125725f3-e1b4-44e3-90c3-1a20eab12da5')
    """
    
## Type

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#type>)

Built-in type: [`type`](<https://docs.python.org/3/glossary.html#term-type>) (deprecated alias: [`typing.Type`](<https://docs.python.org/3/library/typing.html#typing.Type>)).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-25>)

Allows any type that is a subclass of the type argument. For instance, with `type[str]`, allows the [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) class or any [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) subclass as an input. If no type argument is provided (i.e. `type` is used as an annotation), allow any class.

### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-15>)

Types are serialized as is. Types can’t be serialized in [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>) (a [`PydanticSerializationError`](<https://pydantic.dev/docs/validation/latest/api/pydantic-core/pydantic_core/#pydantic_core.PydanticSerializationError>) is raised).
    
    from pydantic import BaseModel, ValidationError
    
    class Foo:
        pass
    
    class Bar(Foo):
        pass
    
    class Other:
        pass
    
    class SimpleModel(BaseModel):
        just_subclasses: type[Foo]
    
    SimpleModel(just_subclasses=Foo)
    SimpleModel(just_subclasses=Bar)
    try:
        SimpleModel(just_subclasses=Other)
    except ValidationError as e:
        print(e)
        """
        1 validation error for SimpleModel
        just_subclasses
          Input should be a subclass of Foo [type=is_subclass_of, input_value=<class '__main__.Other'>, input_type=type]
        """
    
## Literals

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#literals>)

Typing construct: [`typing.Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>) (see also: the [typing specification](<https://typing.python.org/en/latest/spec/literal.html#literal>)).

Literals can be used to only allow specific literal values.

Note that Pydantic applies [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>) behavior when validating literal values (see [this issue](<https://github.com/pydantic/pydantic/issues/9991>)).

### Example

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#example-17>)
    
    from typing import Literal
    
    from pydantic import BaseModel, ValidationError
    
    class Pie(BaseModel):
        flavor: Literal['apple', 'pumpkin']
        quantity: Literal[1, 2] = 1
    
    Pie(flavor='apple')
    Pie(flavor='pumpkin')
    try:
        Pie(flavor='cherry')
    except ValidationError as e:
        print(str(e))
        """
        1 validation error for Pie
        flavor
          Input should be 'apple' or 'pumpkin' [type=literal_error, input_value='cherry', input_type=str]
        """
    
    try:
        Pie(flavor='apple', quantity='1')
    except ValidationError as e:
        print(str(e))
        """
        1 validation error for Pie
        quantity
          Input should be 1 or 2 [type=literal_error, input_value='1', input_type=str]
        """
    
## Any

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#any>)

Types: [`typing.Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) or [`object`](<https://docs.python.org/3/glossary.html#term-object>).

Allows any value, including `None`.

## Hashables

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#hashables>)

Standard library type: [`collections.abc.Hashable`](<https://docs.python.org/3/library/collections.abc.html#collections.abc.Hashable>) (deprecated alias: [`typing.Hashable`](<https://docs.python.org/3/library/typing.html#typing.Hashable>)).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-26>)

Any value that is hashable (using `isinstance(value, Hashable)`).

## Regex patterns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#regex-patterns>)

Standard library type: [`re.Pattern`](<https://docs.python.org/3/library/re.html#re.Pattern>) (deprecated alias: [`typing.Pattern`](<https://docs.python.org/3/library/typing.html#typing.Pattern>)).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-27>)

  * For [`Pattern`](<https://docs.python.org/3/library/re.html#re.Pattern>) instances, check that the [`pattern`](<https://docs.python.org/3/library/re.html#re.Pattern.pattern>) attribute is of the right type ([`str`](<https://docs.python.org/3/library/stdtypes.html#str>) or [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) depending on the [`Pattern`](<https://docs.python.org/3/library/re.html#re.Pattern>) type parameter).
  * If the type parameter is [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) or [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>), input values of type [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) (or [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) respectively) are attempted to be compiled using [`re.compile()`](<https://docs.python.org/3/library/re.html#re.compile>).

### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-16>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), [`Pattern`](<https://docs.python.org/3/library/re.html#re.Pattern>) instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

## Paths

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#paths>)

Standard library types:

  * [`pathlib.Path`](<https://docs.python.org/3/library/pathlib.html#pathlib.Path>).
  * [`pathlib.PurePath`](<https://docs.python.org/3/library/pathlib.html#pathlib.PurePath>).
  * [`pathlib.PosixPath`](<https://docs.python.org/3/library/pathlib.html#pathlib.PosixPath>).
  * [`pathlib.PurePosixPath`](<https://docs.python.org/3/library/pathlib.html#pathlib.PurePosixPath>).
  * [`pathlib.PureWindowsPath`](<https://docs.python.org/3/library/pathlib.html#pathlib.PureWindowsPath>).
  * [`os.PathLike`](<https://docs.python.org/3/library/os.html#os.PathLike>) (must be parameterized with [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) or [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)).

### Validation

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#validation-28>)

  * Path instances are validated as is.
  * Strings are accepted and passed to the type constructor. If [`os.PathLike`](<https://docs.python.org/3/library/os.html#os.PathLike>) was used, bytes are accepted if it was parameterized with the [`bytes`](<https://docs.python.org/3/library/stdtypes.html#bytes>) type.

### Strictness

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#strictness-20>)

In [strict mode](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode>), only Path instances are accepted. In JSON mode, strict mode has no effect.

### Serialization

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types/#serialization-17>)

In [Python mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#python-mode>), Path instances are serialized as is.

In [JSON mode](<https://pydantic.dev/docs/validation/latest/concepts/serialization#json-mode>), they are serialized as strings.

Was this page helpful?

Thanks for your feedback!