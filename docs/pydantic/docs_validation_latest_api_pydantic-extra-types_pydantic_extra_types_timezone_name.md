# Timezone Name | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Timezone Name

Time zone name validation and serialization module.

## TimeZoneName 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/#pydantic_extra_types.timezone_name.TimeZoneName>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

TimeZoneName is a custom string subclass for validating and serializing timezone names.

The TimeZoneName class uses the IANA Time Zone Database for validation. It supports both strict and non-strict modes for timezone name validation.

## Examples:

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/#examples>)

Some examples of using the TimeZoneName class:

### Normal usage:

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/#normal-usage>)
    
    from pydantic_extra_types.timezone_name import TimeZoneName
    from pydantic import BaseModel
    class Location(BaseModel):
        city: str
        timezone: TimeZoneName
    
    loc = Location(city="New York", timezone="America/New_York")
    print(loc.timezone)
    
    >> America/New_York
    
### Non-strict mode:

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/#non-strict-mode>)
    
    from pydantic_extra_types.timezone_name import TimeZoneName, timezone_name_settings
    
    @timezone_name_settings(strict=False)
    class TZNonStrict(TimeZoneName):
        pass
    
    tz = TZNonStrict("america/new_york")
    
    print(tz)
    
    >> america/new_york
    
## get_timezones 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/#pydantic_extra_types.timezone_name.get_timezones>)
    
    def get_timezones() -> set[str]
    
Determine the timezone provider and return available timezones.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_timezone_name/#returns>)

[`set`](<https://docs.python.org/3/reference/expressions.html#set>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]

Was this page helpful?

Thanks for your feedback!