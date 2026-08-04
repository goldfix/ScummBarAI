# Currency | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_currency_code/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_currency_code/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_currency_code/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Currency

Currency definitions that are based on the [ISO4217](<https://en.wikipedia.org/wiki/ISO_4217>).

## ISO4217 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_currency_code/#pydantic_extra_types.currency_code.ISO4217>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

ISO4217 parses Currency in the [ISO 4217](<https://en.wikipedia.org/wiki/ISO_4217>) format.
    
    from pydantic import BaseModel
    
    from pydantic_extra_types.currency_code import ISO4217
    
    class Currency(BaseModel):
        alpha_3: ISO4217
    
    currency = Currency(alpha_3='AED')
    print(currency)
    # > alpha_3='AED'
    
## Currency 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_currency_code/#pydantic_extra_types.currency_code.Currency>)

**Bases:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

Currency parses currency subset of the [ISO 4217](<https://en.wikipedia.org/wiki/ISO_4217>) format. It excludes bonds testing codes and precious metals.
    
    from pydantic import BaseModel
    
    from pydantic_extra_types.currency_code import Currency
    
    class currency(BaseModel):
        alpha_3: Currency
    
    cur = currency(alpha_3='AED')
    print(cur)
    # > alpha_3='AED'
    
Was this page helpful?

Thanks for your feedback!