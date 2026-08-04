# Country | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Country

Country definitions that are based on the [ISO 3166](<https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>).

## CountryAlpha2 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha2>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

CountryAlpha2 parses country codes in the [ISO 3166-1 alpha-2](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>) format.
    
    from pydantic import BaseModel
    
    from pydantic_extra_types.country import CountryAlpha2
    
    class Product(BaseModel):
        made_in: CountryAlpha2
    
    product = Product(made_in='ES')
    print(product)
    # > made_in='ES'
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#attributes>)

#### alpha3 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha2.alpha3>)

The country code in the [ISO 3166-1 alpha-3](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### numeric_code 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha2.numeric_code>)

The country code in the [ISO 3166-1 numeric](<https://en.wikipedia.org/wiki/ISO_3166-1_numeric>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### short_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha2.short_name>)

The country short name.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## CountryAlpha3 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha3>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

CountryAlpha3 parses country codes in the [ISO 3166-1 alpha-3](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3>) format.
    
    from pydantic import BaseModel
    
    from pydantic_extra_types.country import CountryAlpha3
    
    class Product(BaseModel):
        made_in: CountryAlpha3
    
    product = Product(made_in='USA')
    print(product)
    # > made_in='USA'
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#attributes-1>)

#### alpha2 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha3.alpha2>)

The country code in the [ISO 3166-1 alpha-2](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### numeric_code 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha3.numeric_code>)

The country code in the [ISO 3166-1 numeric](<https://en.wikipedia.org/wiki/ISO_3166-1_numeric>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### short_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryAlpha3.short_name>)

The country short name.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## CountryNumericCode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryNumericCode>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

CountryNumericCode parses country codes in the [ISO 3166-1 numeric](<https://en.wikipedia.org/wiki/ISO_3166-1_numeric>) format.
    
    from pydantic import BaseModel
    
    from pydantic_extra_types.country import CountryNumericCode
    
    class Product(BaseModel):
        made_in: CountryNumericCode
    
    product = Product(made_in='840')
    print(product)
    # > made_in='840'
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#attributes-2>)

#### alpha2 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryNumericCode.alpha2>)

The country code in the [ISO 3166-1 alpha-2](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### alpha3 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryNumericCode.alpha3>)

The country code in the [ISO 3166-1 alpha-3](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### short_name 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryNumericCode.short_name>)

The country short name.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## CountryShortName 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryShortName>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

CountryShortName parses country codes in the short name format.
    
    from pydantic import BaseModel
    
    from pydantic_extra_types.country import CountryShortName
    
    class Product(BaseModel):
        made_in: CountryShortName
    
    product = Product(made_in='United States')
    print(product)
    # > made_in='United States'
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#attributes-3>)

#### alpha2 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryShortName.alpha2>)

The country code in the [ISO 3166-1 alpha-2](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### alpha3 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryShortName.alpha3>)

The country code in the [ISO 3166-1 alpha-3](<https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

#### numeric_code 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_country/#pydantic_extra_types.country.CountryShortName.numeric_code>)

The country code in the [ISO 3166-1 numeric](<https://en.wikipedia.org/wiki/ISO_3166-1_numeric>) format.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

Was this page helpful?

Thanks for your feedback!