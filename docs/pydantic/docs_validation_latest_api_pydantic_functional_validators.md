# Functional Validators | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/](https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Functional Validators

This module contains related classes and functions for validation.

## AfterValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.AfterValidator>)

A metadata class that indicates that a validation should be applied **after** the inner validation logic.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#attributes>)

#### func 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.AfterValidator.func>)

The validator function.

**Type:** `core_schema.NoInfoValidatorFunction` | `core_schema.WithInfoValidatorFunction`

## BeforeValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.BeforeValidator>)

A metadata class that indicates that a validation should be applied **before** the inner validation logic.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#attributes-1>)

#### func 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.BeforeValidator.func>)

The validator function.

**Type:** `core_schema.NoInfoValidatorFunction` | `core_schema.WithInfoValidatorFunction`

#### json_schema_input_type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.BeforeValidator.json_schema_input_type>)

The input type used to generate the appropriate JSON Schema (in validation mode). The actual input type is `Any`.

**Type:** [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

## PlainValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.PlainValidator>)

A metadata class that indicates that a validation should be applied **instead** of the inner validation logic.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#attributes-2>)

#### func 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.PlainValidator.func>)

The validator function.

**Type:** `core_schema.NoInfoValidatorFunction` | `core_schema.WithInfoValidatorFunction`

#### json_schema_input_type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.PlainValidator.json_schema_input_type>)

The input type used to generate the appropriate JSON Schema (in validation mode). The actual input type is `Any`.

**Type:** [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

## WrapValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.WrapValidator>)

A metadata class that indicates that a validation should be applied **around** the inner validation logic.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#attributes-3>)

#### func 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.WrapValidator.func>)

The validator function.

**Type:** `core_schema.NoInfoWrapValidatorFunction` | `core_schema.WithInfoWrapValidatorFunction`

#### json_schema_input_type 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.WrapValidator.json_schema_input_type>)

The input type used to generate the appropriate JSON Schema (in validation mode). The actual input type is `Any`.

**Type:** [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)
    
    from datetime import datetime
    from typing import Annotated
    
    from pydantic import BaseModel, ValidationError, WrapValidator
    
    def validate_timestamp(v, handler):
        if v == 'now':
            # we don't want to bother with further validation, just return the new value
            return datetime.now()
        try:
            return handler(v)
        except ValidationError:
            # validation failed, in this case we want to return a default value
            return datetime(2000, 1, 1)
    
    MyTimestamp = Annotated[datetime, WrapValidator(validate_timestamp)]
    
    class Model(BaseModel):
        a: MyTimestamp
    
    print(Model(a='now').a)
    #> 2032-01-02 03:04:05.000006
    print(Model(a='invalid').a)
    #> 2000-01-01 00:00:00
    
## ModelWrapValidatorHandler 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ModelWrapValidatorHandler>)

**Bases:** `ValidatorFunctionWrapHandler`, `Protocol[_ModelTypeCo]`

`@model_validator` decorated function handler argument type. This is used when `mode='wrap'`.

## ModelWrapValidatorWithoutInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ModelWrapValidatorWithoutInfo>)

**Bases:** `Protocol[_ModelType]`

A `@model_validator` decorated function signature. This is used when `mode='wrap'` and the function does not have info argument.

## ModelWrapValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ModelWrapValidator>)

**Bases:** `Protocol[_ModelType]`

A `@model_validator` decorated function signature. This is used when `mode='wrap'`.

## FreeModelBeforeValidatorWithoutInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.FreeModelBeforeValidatorWithoutInfo>)

**Bases:** [`Protocol`](<https://docs.python.org/3/library/typing.html#typing.Protocol>)

A `@model_validator` decorated function signature. This is used when `mode='before'` and the function does not have info argument.

## ModelBeforeValidatorWithoutInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ModelBeforeValidatorWithoutInfo>)

**Bases:** [`Protocol`](<https://docs.python.org/3/library/typing.html#typing.Protocol>)

A `@model_validator` decorated function signature. This is used when `mode='before'` and the function does not have info argument.

## FreeModelBeforeValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.FreeModelBeforeValidator>)

**Bases:** [`Protocol`](<https://docs.python.org/3/library/typing.html#typing.Protocol>)

A `@model_validator` decorated function signature. This is used when `mode='before'`.

## ModelBeforeValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ModelBeforeValidator>)

**Bases:** [`Protocol`](<https://docs.python.org/3/library/typing.html#typing.Protocol>)

A `@model_validator` decorated function signature. This is used when `mode='before'`.

## InstanceOf 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.InstanceOf>)

Generic type for annotating a type that is an instance of a given class.

## SkipValidation 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.SkipValidation>)

If this is applied as an annotation (e.g., via `x: Annotated[int, SkipValidation]`), validation will be skipped. You can also use `SkipValidation[int]` as a shorthand for `Annotated[int, SkipValidation]`.

This can be useful if you want to use a type annotation for documentation/IDE/type-checking purposes, and know that it is safe to skip validation for one or more of the fields.

Because this converts the validation schema to `any_schema`, subsequent annotation-applied transformations may not have the expected effects. Therefore, when used, this annotation should generally be the final annotation applied to a type.

## ValidateAs 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ValidateAs>)

A helper class to validate a custom type from a type that is natively supported by Pydantic.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#constructor-parameters>)

**`from_type`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`_FromTypeT`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ValidateAs.__init__\(from_type\)>)

The type natively supported by Pydantic to use to perform validation.

**`instantiation_hook`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[`_FromTypeT`], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ValidateAs.__init__\(instantiation_hook\)>)

A callable taking the validated type as an argument, and returning the populated custom type.

## field_validator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator>)
    
    def field_validator(
        field: str,
        /,
        *fields: str,
        mode: Literal['wrap'],
        check_fields: bool | None = ...,
        json_schema_input_type: Any = ...,
    ) -> Callable[[_V2WrapValidatorType], _V2WrapValidatorType]
    def field_validator(
        field: str,
        /,
        *fields: str,
        mode: Literal['before', 'plain'],
        check_fields: bool | None = ...,
        json_schema_input_type: Any = ...,
    ) -> Callable[[_V2BeforeAfterOrPlainValidatorType], _V2BeforeAfterOrPlainValidatorType]
    def field_validator(
        field: str,
        /,
        *fields: str,
        mode: Literal['after'] = ...,
        check_fields: bool | None = ...,
    ) -> Callable[[_V2BeforeAfterOrPlainValidatorType], _V2BeforeAfterOrPlainValidatorType]
    
Decorate methods on the class indicating that they should be used to validate fields.

Example usage:
    
    from typing import Any
    
    from pydantic import (
        BaseModel,
        ValidationError,
        field_validator,
    )
    
    class Model(BaseModel):
        a: str
    
        @field_validator('a')
        @classmethod
        def ensure_foobar(cls, v: Any):
            if 'foobar' not in v:
                raise ValueError('"foobar" not found in a')
            return v
    
    print(repr(Model(a='this is foobar good')))
    #> Model(a='this is foobar good')
    
    try:
        Model(a='snap')
    except ValidationError as exc_info:
        print(exc_info)
        '''
        1 validation error for Model
        a
          Value error, "foobar" not found in a [type=value_error, input_value='snap', input_type=str]
        '''
    
For more in depth examples, see [Field Validators](<https://pydantic.dev/docs/validation/latest/concepts/validators#field-validators>).

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#returns>)

[`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)], [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#parameters>)

**`*fields`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `()`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator\(*fields\)>)

The field names the validator should apply to.

**`mode`** : `FieldValidatorModes` _Default:_ `'after'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator\(mode\)>)

Specifies whether to validate the fields before or after validation.

**`check_fields`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator\(check_fields\)>)

Whether to check that the fields actually exist on the model.

**`json_schema_input_type`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `PydanticUndefined`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.field_validator\(json_schema_input_type\)>)

The input type of the function. This is only used to generate the appropriate JSON Schema (in validation mode) and can only specified when `mode` is either `'before'`, `'plain'` or `'wrap'`.

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#raises>)

  * `PydanticUserError` —
  * If the decorator is used without any arguments (at least one field name must be provided).
  * If the provided field names are not strings.
  * If `json_schema_input_type` is provided with an unsupported `mode`.
  * If the decorator is applied to an instance method.

## model_validator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.model_validator>)
    
    def model_validator(
        *,
        mode: Literal['wrap'],
    ) -> Callable[[_AnyModelWrapValidator[_ModelType]], _decorators.PydanticDescriptorProxy[_decorators.ModelValidatorDecoratorInfo]]
    def model_validator(
        *,
        mode: Literal['before'],
    ) -> Callable[[_AnyModelBeforeValidator], _decorators.PydanticDescriptorProxy[_decorators.ModelValidatorDecoratorInfo]]
    def model_validator(
        *,
        mode: Literal['after'],
    ) -> Callable[[_AnyModelAfterValidator[_ModelType]], _decorators.PydanticDescriptorProxy[_decorators.ModelValidatorDecoratorInfo]]
    
Decorate model methods for validation purposes.

Example usage:
    
    from typing_extensions import Self
    
    from pydantic import BaseModel, ValidationError, model_validator
    
    class Square(BaseModel):
        width: float
        height: float
    
        @model_validator(mode='after')
        def verify_square(self) -> Self:
            if self.width != self.height:
                raise ValueError('width and height do not match')
            return self
    
    s = Square(width=1, height=1)
    print(repr(s))
    #> Square(width=1.0, height=1.0)
    
    try:
        Square(width=1, height=2)
    except ValidationError as e:
        print(e)
        '''
        1 validation error for Square
          Value error, width and height do not match [type=value_error, input_value={'width': 1, 'height': 2}, input_type=dict]
        '''
    
For more in depth examples, see [Model Validators](<https://pydantic.dev/docs/validation/latest/concepts/validators#model-validators>).

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#returns-1>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — A decorator that can be used to decorate a function to be used as a model validator.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#parameters-1>)

**`mode`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘wrap’, ‘before’, ‘after’] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.model_validator\(mode\)>)

A required string literal that specifies the validation mode. It can be one of the following: ‘wrap’, ‘before’, or ‘after’.

## ModelAfterValidatorWithoutInfo 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ModelAfterValidatorWithoutInfo>)

A `@model_validator` decorated function signature. This is used when `mode='after'` and the function does not have info argument.

**Default:** `Callable[[_ModelType], _ModelType]`

## ModelAfterValidator 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/functional_validators/#pydantic.functional_validators.ModelAfterValidator>)

A `@model_validator` decorated function signature. This is used when `mode='after'`.

**Default:** `Callable[[_ModelType, core_schema.ValidationInfo[Any]], _ModelType]`

Was this page helpful?

Thanks for your feedback!