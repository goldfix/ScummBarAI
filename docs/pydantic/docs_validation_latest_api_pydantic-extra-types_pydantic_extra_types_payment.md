# Payment | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Payment

The `pydantic_extra_types.payment` module provides the [`PaymentCardNumber`](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber>) data type.

## PaymentCardBrand 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardBrand>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), `Enum`

Payment card brands supported by the [`PaymentCardNumber`](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber>).

## PaymentCardNumber 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

A [payment card number](<https://en.wikipedia.org/wiki/Payment_card_number>).

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#attributes>)

#### strip_whitespace 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.strip_whitespace>)

Whether to strip whitespace from the input value.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) **Default:** `True`

#### min_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.min_length>)

The minimum length of the card number.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) **Default:** `12`

#### max_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.max_length>)

The maximum length of the card number.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) **Default:** `19`

#### bin 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.bin>)

The first 6 digits of the card number.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) **Default:** `card_number[:6]`

#### last4 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.last4>)

The last 4 digits of the card number.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) **Default:** `card_number[(-4):]`

#### brand 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.brand>)

The brand of the card.

**Type:** `PaymentCardBrand` **Default:** `self.validate_brand(card_number)`

#### masked 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.masked>)

The masked card number.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#methods>)

#### validate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate>)

`@classmethod`
    
    def validate(
        cls,
        __input_value: str,
        _: core_schema.ValidationInfo,
    ) -> PaymentCardNumber
    
Validate the `PaymentCardNumber` instance.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#returns>)

[`PaymentCardNumber`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.PaymentCardNumber>) — The validated `PaymentCardNumber` instance.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#parameters>)

**`__input_value`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate\(__input_value\)>)

The input value to validate.

**`_`** : `core_schema.ValidationInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate\(_\)>)

The validation info.

#### validate_digits 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate_digits>)

`@classmethod`
    
    def validate_digits(cls, card_number: str) -> None
    
Validate that the card number is all digits.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#returns-1>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#parameters-1>)

**`card_number`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate_digits\(card_number\)>)

The card number to validate.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#raises>)

  * `PydanticCustomError` — If the card number is not all digits.

#### validate_luhn_check_digit 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate_luhn_check_digit>)

`@classmethod`
    
    def validate_luhn_check_digit(cls, card_number: str) -> str
    
Validate the payment card number. Based on the [Luhn algorithm](<https://en.wikipedia.org/wiki/Luhn_algorithm>).

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#returns-2>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The validated card number.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#parameters-2>)

**`card_number`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate_luhn_check_digit\(card_number\)>)

The card number to validate.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#raises-1>)

  * `PydanticCustomError` — If the card number is not valid.

#### validate_brand 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate_brand>)

`@staticmethod`
    
    def validate_brand(card_number: str) -> PaymentCardBrand
    
Validate length based on [BIN](<https://en.wikipedia.org/wiki/Payment_card_number#Issuer_identification_number_\(IIN\)>) for major brands.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#returns-3>)

`PaymentCardBrand` — The validated card brand.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#parameters-3>)

**`card_number`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#pydantic_extra_types.payment.PaymentCardNumber.validate_brand\(card_number\)>)

The card number to validate.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_payment/#raises-2>)

  * `PydanticCustomError` — If the card number is not valid.

Was this page helpful?

Thanks for your feedback!