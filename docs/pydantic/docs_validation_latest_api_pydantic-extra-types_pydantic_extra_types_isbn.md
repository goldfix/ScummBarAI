# ISBN | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# ISBN

The `pydantic_extra_types.isbn` module provides functionality to receive and validate ISBN.

ISBN (International Standard Book Number) is a numeric commercial book identifier which is intended to be unique. This module provides an ISBN type for Pydantic models.

## ISBN 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.ISBN>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

Represents a ISBN and provides methods for conversion, validation, and serialization.
    
    from pydantic import BaseModel
    
    from pydantic_extra_types.isbn import ISBN
    
    class Book(BaseModel):
        isbn: ISBN
    
    book = Book(isbn='8537809667')
    print(book)
    # > isbn='9788537809662'
    
### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#methods>)

#### validate_isbn_format 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.ISBN.validate_isbn_format>)

`@staticmethod`
    
    def validate_isbn_format(value: str) -> None
    
Validate a ISBN format from the provided str value.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#returns>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#parameters>)

**`value`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.ISBN.validate_isbn_format\(value\)>)

The str value representing the ISBN in 10 or 13 digits.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#raises>)

  * `PydanticCustomError` — If the ISBN is not valid.

#### convert_isbn10_to_isbn13 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.ISBN.convert_isbn10_to_isbn13>)

`@staticmethod`
    
    def convert_isbn10_to_isbn13(value: str) -> str
    
Convert an ISBN-10 to ISBN-13.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#returns-1>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The converted ISBN or the original value if no conversion is necessary.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#parameters-1>)

**`value`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.ISBN.convert_isbn10_to_isbn13\(value\)>)

The ISBN-10 value to be converted.

## isbn10_digit_calc 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.isbn10_digit_calc>)
    
    def isbn10_digit_calc(isbn: str) -> str
    
Calculate the ISBN-10 check digit from the provided str value. More information on the validation algorithm on [Wikipedia](<https://en.wikipedia.org/wiki/ISBN#Check_digits>)

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#returns-2>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The calculated last digit of the ISBN-10 value.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#parameters-2>)

**`isbn`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.isbn10_digit_calc\(isbn\)>)

The str value representing the ISBN in 10 digits.

## isbn13_digit_calc 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.isbn13_digit_calc>)
    
    def isbn13_digit_calc(isbn: str) -> str
    
Calc a ISBN-13 last digit from the provided str value. More information on the validation algorithm on [Wikipedia](<https://en.wikipedia.org/wiki/ISBN#Check_digits>)

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#returns-3>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The calculated last digit of the ISBN-13 value.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#parameters-3>)

**`isbn`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_isbn/#pydantic_extra_types.isbn.isbn13_digit_calc\(isbn\)>)

The str value representing the ISBN in 13 digits.

Was this page helpful?

Thanks for your feedback!