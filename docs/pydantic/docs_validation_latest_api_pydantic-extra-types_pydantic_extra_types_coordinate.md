# Coordinate | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/](https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Coordinate

The `pydantic_extra_types.coordinate` module provides the [`Latitude`](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/#pydantic_extra_types.coordinate.Latitude>), [`Longitude`](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/#pydantic_extra_types.coordinate.Longitude>), and [`Coordinate`](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/#pydantic_extra_types.coordinate.Coordinate>) data types.

## Latitude 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/#pydantic_extra_types.coordinate.Latitude>)

**Bases:** [`float`](<https://docs.python.org/3/library/functions.html#float>)

Latitude value should be between -90 and 90, inclusive.

Supports both float and Decimal types.
    
    from decimal import Decimal
    from pydantic import BaseModel
    from pydantic_extra_types.coordinate import Latitude
    
    class Location(BaseModel):
        latitude: Latitude
    
    # Using float
    location1 = Location(latitude=41.40338)
    # Using Decimal
    location2 = Location(latitude=Decimal('41.40338'))
    
## Longitude 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/#pydantic_extra_types.coordinate.Longitude>)

**Bases:** [`float`](<https://docs.python.org/3/library/functions.html#float>)

Longitude value should be between -180 and 180, inclusive.

Supports both float and Decimal types.
    
    from decimal import Decimal
    from pydantic import BaseModel
    
    from pydantic_extra_types.coordinate import Longitude
    
    class Location(BaseModel):
        longitude: Longitude
    
    # Using float
    location1 = Location(longitude=2.17403)
    # Using Decimal
    location2 = Location(longitude=Decimal('2.17403'))
    
## Coordinate 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic-extra-types/pydantic_extra_types_coordinate/#pydantic_extra_types.coordinate.Coordinate>)

**Bases:** `Representation`

Coordinate parses Latitude and Longitude.

You can use the `Coordinate` data type for storing coordinates. Coordinates can be defined using one of the following formats:

  1. Tuple: `(Latitude, Longitude)`. For example: `(41.40338, 2.17403)` or `(Decimal('41.40338'), Decimal('2.17403'))`.
  2. `Coordinate` instance: `Coordinate(latitude=Latitude, longitude=Longitude)`.

    from decimal import Decimal
    from pydantic import BaseModel
    
    from pydantic_extra_types.coordinate import Coordinate
    
    class Location(BaseModel):
        coordinate: Coordinate
    
    # Using float values
    location1 = Location(coordinate=(41.40338, 2.17403))
    # > coordinate=Coordinate(latitude=41.40338, longitude=2.17403)
    
    # Using Decimal values
    location2 = Location(coordinate=(Decimal('41.40338'), Decimal('2.17403')))
    # > coordinate=Coordinate(latitude=41.40338, longitude=2.17403)
    
Was this page helpful?

Thanks for your feedback!