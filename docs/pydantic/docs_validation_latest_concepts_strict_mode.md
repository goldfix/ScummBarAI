# Strict Mode | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/concepts/strict_mode/](https://pydantic.dev/docs/validation/latest/concepts/strict_mode/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Strict Mode

API Documentation

[`pydantic.types.Strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Strict>)  

By default, Pydantic will attempt to coerce values to the desired type when possible. For example, you can pass the string `'123'` as the input for the [`int` number type](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types#integers>), and it will be converted to the value `123`. This coercion behavior is useful in many scenarios — think: UUIDs, URL parameters, HTTP headers, environment variables, dates, etc.

However, there are also situations where this is not desirable, and you want Pydantic to error instead of coercing data.

To better support this use case, Pydantic provides a “strict mode”. When strict mode is enabled, Pydantic will be much less lenient when coercing data, and will instead error if the data is not of the correct type.

Most of the time, strict mode will only allow instances of the type to be provided, although looser rules may apply to JSON input (for instance, the [date and time types](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types#date-and-time-types>) allow strings even in strict mode).

The strict behavior for each type can be found in the [standard library types](<https://pydantic.dev/docs/validation/latest/api/pydantic/standard_library_types>) documentation, and is summarized in the [conversion table](<https://pydantic.dev/docs/validation/latest/concepts/conversion_table>).

Here is a brief example showing the validation behavior difference in strict and the default lax mode:
    
    from pydantic import BaseModel, ValidationError
    
    class MyModel(BaseModel):
        x: int
    
    print(MyModel.model_validate({'x': '123'}))  # lax mode
    #> x=123
    
    try:
        MyModel.model_validate({'x': '123'}, strict=True)  # strict mode
    except ValidationError as exc:
        print(exc)
        """
        1 validation error for MyModel
        x
          Input should be a valid integer [type=int_type, input_value='123', input_type=str]
        """
    
Strict mode can be enabled in various ways:

  * [As a validation parameter](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#as-a-validation-parameter>), such as when using [`model_validate()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate>), on Pydantic models.
  * [At the field level](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#at-the-field-level>).
  * [At the configuration level](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#as-a-configuration-value>) (with the possibility to override at the field level).

## As a validation parameter

[](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#as-a-validation-parameter>)

Strict mode can be enaled on a per-validation-call basis, when using the [validation methods](<https://pydantic.dev/docs/validation/latest/concepts/models#validating-data>) on [Pydantic models](<https://pydantic.dev/docs/validation/latest/concepts/models>) and [type adapters](<https://pydantic.dev/docs/validation/latest/concepts/type_adapter>).
    
    from datetime import date
    
    from pydantic import TypeAdapter, ValidationError
    
    print(TypeAdapter(date).validate_python('2000-01-01'))  # OK: lax
    #> 2000-01-01
    
    try:
      # Not OK: strict:
      TypeAdapter(date).validate_python('2000-01-01', strict=True)
    except ValidationError as exc:
      print(exc)
      """
      1 validation error for date
        Input should be a valid date [type=date_type, input_value='2000-01-01', input_type=str]
      """
    
    TypeAdapter(date).validate_json('"2000-01-01"', strict=True)  # (1)
    #> 2000-01-01

As mentioned, strict mode is looser when validating from JSON.

## At the field level

[](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#at-the-field-level>)

Strict mode can be enabled on specific fields, by setting the `strict` parameter of the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function to `True`. Strict mode will be applied for such fields, even when the [validation methods](<https://pydantic.dev/docs/validation/latest/concepts/models#validating-data>) are called in lax mode.
    
    from pydantic import BaseModel, Field, ValidationError
    
    class User(BaseModel):
      name: str
      age: int = Field(strict=True)  # (1)
    
    user = User(name='John', age=42)
    print(user)
    #> name='John' age=42
    
    try:
      another_user = User(name='John', age='42')
    except ValidationError as e:
      print(e)
      """
      1 validation error for User
      age
        Input should be a valid integer [type=int_type, input_value='42', input_type=str]
      """

The strict constraint can also be applied using the [annotated pattern](<https://pydantic.dev/docs/validation/latest/concepts/fields#the-annotated-pattern>): `Annotated[int, Field(strict=True)]`

### Using the `Strict()` metadata class

[](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#using-the-strict-metadata-class>)

API Documentation

[`pydantic.types.Strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Strict>)  

As an alternative to the [`Field()`](<https://pydantic.dev/docs/validation/latest/api/pydantic/fields/#pydantic.fields.Field>) function, Pydantic provides the [`Strict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.Strict>) metadata class, meant to be used with the [annotated pattern](<https://pydantic.dev/docs/validation/latest/concepts/fields#the-annotated-pattern>). It also provides convenience aliases for the most common types (namely [`StrictBool`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictBool>), [`StrictInt`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictInt>), [`StrictFloat`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictFloat>), [`StrictStr`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictStr>) and [`StrictBytes`](<https://pydantic.dev/docs/validation/latest/api/pydantic/types/#pydantic.types.StrictBytes>)).
    
    from typing import Annotated
    from uuid import UUID
    
    from pydantic import BaseModel, Strict, StrictInt
    
    class User(BaseModel):
      id: Annotated[UUID, Strict()]
      age: StrictInt  # (1)

Equivalent to `Annotated[int, Strict()]`.

## As a configuration value

[](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#as-a-configuration-value>)

Strict mode behavior can be controlled at the [configuration](<https://pydantic.dev/docs/validation/latest/concepts/config>) level. When used on a Pydantic model (or model like class such as [dataclasses](<https://pydantic.dev/docs/validation/latest/concepts/dataclasses>)), strictness can still be overridden at the [field level](<https://pydantic.dev/docs/validation/latest/concepts/strict_mode/#at-the-field-level>):
    
    from pydantic import BaseModel, ConfigDict, Field
    
    class User(BaseModel):
        model_config = ConfigDict(strict=True)
    
        name: str
        age: int = Field(strict=False)
    
    print(User(name='John', age='18'))
    #> name='John' age=18
    
Was this page helpful?

Thanks for your feedback!