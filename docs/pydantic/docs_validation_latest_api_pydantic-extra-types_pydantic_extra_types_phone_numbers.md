# Phone Numbers | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Phone Numbers

The `pydantic_extra_types.phone_numbers` module provides the [`PhoneNumber`](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumber>) data type.

This class depends on the [phonenumbers](<https://pypi.org/project/phonenumbers/>) package, which is a Python port of Google’s [libphonenumber](<https://github.com/google/libphonenumber/>).

## PhoneNumber 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumber>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

A wrapper around the `phonenumbers.PhoneNumber` object.

It provides class-level configuration points you can change by subclassing:

## Examples

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#examples>)

### Normal usage:

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#normal-usage>)
    
    from pydantic import BaseModel
    from pydantic_extra_types.phone_numbers import PhoneNumber
    
    class Contact(BaseModel):
        name: str
        phone: PhoneNumber
    
    c = Contact(name='Alice', phone='+1 650-253-0000')
    print(c.phone)
    # > tel:+1-650-253-0000 (formatted using RFC3966 by default)
    
### Changing defaults by subclassing:

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#changing-defaults-by-subclassing>)
    
    from pydantic_extra_types.phone_numbers import PhoneNumber
    
    class USPhone(PhoneNumber):
        default_region_code = 'US'
        supported_regions = ['US']
        phone_format = 'NATIONAL'
    
    # Now parsing will accept national numbers for the US
    p = USPhone('650-253-0000')
    print(p)
    # > 650-253-0000
    
### Changing defaults by using the provided validator annotation:

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#changing-defaults-by-using-the-provided-validator-annotation>)
    
    from typing import Annotated, Union
    import phonenumbers
    from pydantic import BaseModel
    from pydantic_extra_types.phone_numbers import PhoneNumberValidator
    
    E164NumberType = Annotated[Union[str, phonenumbers.PhoneNumber], PhoneNumberValidator(number_format='E164')]
    
    class Model(BaseModel):
        phone: E164NumberType
    
    m = Model(phone='+1 650-253-0000')
    print(m.phone)
    # > +16502530000
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#attributes>)

#### default_region_code 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumber.default_region_code>)

The default region code to use when parsing phone numbers without an international prefix.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) **Default:** `None`

#### supported_regions 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumber.supported_regions>)

The supported regions. If empty, all regions are supported.

**Type:** [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] **Default:** `[]`

#### phone_format 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumber.phone_format>)

The format of the phone number.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) **Default:** `'RFC3966'`

## PhoneNumberValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumberValidator>)

An annotation to validate `phonenumbers.PhoneNumber` objects.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#attributes-1>)

#### default_region 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumberValidator.default_region>)

The default region code to use when parsing phone numbers without an international prefix.

If `None` (the default), the region must be supplied in the phone number as an international prefix.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) **Default:** `None`

#### number_format 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumberValidator.number_format>)

The format of the phone number to return. See `phonenumbers.PhoneNumberFormat` for valid values.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) **Default:** `'RFC3966'`

#### supported_regions 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_phone_numbers/#pydantic_extra_types.phone_numbers.PhoneNumberValidator.supported_regions>)

The supported regions. If empty (the default), all regions are supported.

**Type:** [`Sequence`](<https://docs.python.org/3/library/typing.html#typing.Sequence>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) **Default:** `None`

Was this page helpful?

Thanks for your feedback!