# Pendulum | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Pendulum

Native Pendulum DateTime object implementation. This is a copy of the Pendulum DateTime object, but with a Pydantic CoreSchema implementation. This allows Pydantic to validate the DateTime object.

## DateTime 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#pydantic_extra_types.pendulum_dt.DateTime>)

**Bases:** `_DateTime`

A `pendulum.DateTime` object. At runtime, this type decomposes into pendulum.DateTime automatically. This type exists because Pydantic throws a fit on unknown types.
    
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import DateTime
    
    class test_model(BaseModel):
        dt: DateTime
    
    print(test_model(dt='2021-01-01T00:00:00+00:00'))
    
    # > test_model(dt=DateTime(2021, 1, 1, 0, 0, 0, tzinfo=FixedTimezone(0, name="+00:00")))
    
## Time 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#pydantic_extra_types.pendulum_dt.Time>)

**Bases:** `_Time`

A `pendulum.Time` object. At runtime, this type decomposes into pendulum.Time automatically. This type exists because Pydantic throws a fit on unknown types.
    
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Time
    
    class test_model(BaseModel):
        dt: Time
    
    print(test_model(dt='00:00:00'))
    
    # > test_model(dt=Time(0, 0, 0))
    
## Date 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#pydantic_extra_types.pendulum_dt.Date>)

**Bases:** `_Date`

A `pendulum.Date` object. At runtime, this type decomposes into pendulum.Date automatically. This type exists because Pydantic throws a fit on unknown types.
    
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Date
    
    class test_model(BaseModel):
        dt: Date
    
    print(test_model(dt='2021-01-01'))
    
    # > test_model(dt=Date(2021, 1, 1))
    
## Duration 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#pydantic_extra_types.pendulum_dt.Duration>)

**Bases:** `_Duration`

A `pendulum.Duration` object. At runtime, this type decomposes into pendulum.Duration automatically. This type exists because Pydantic throws a fit on unknown types.
    
    from pydantic import BaseModel
    from pydantic_extra_types.pendulum_dt import Duration
    
    class test_model(BaseModel):
        delta_t: Duration
    
    print(test_model(delta_t='P1DT25H'))
    
    # > test_model(delta_t=Duration(days=2, hours=1))
    
### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#methods>)

#### to_iso8601_string 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#pydantic_extra_types.pendulum_dt.Duration.to_iso8601_string>)
    
    def to_iso8601_string() -> str
    
Convert a Duration object to an ISO 8601 string.

In addition to the standard ISO 8601 format, this method also supports the representation of fractions of a second and negative durations.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_pendulum_dt/#returns>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The ISO 8601 string representation of the duration.

Was this page helpful?

Thanks for your feedback!