# Type Adapter | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/concepts/type_adapter/](https://pydantic.dev/docs/validation/latest/concepts/type_adapter/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/concepts/type_adapter/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Type Adapter

You may have types that are not `BaseModel`s that you want to validate data against. Or you may want to validate a `list[SomeModel]`, or dump it to JSON.

API Documentation

[`pydantic.type_adapter.TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>)  

For use cases like this, Pydantic provides [`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>), which can be used for type validation, serialization, and JSON schema generation without needing to create a [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>).

A [`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) instance exposes some of the functionality from [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>) instance methods for types that do not have such methods (such as dataclasses, primitive types, and more):
    
    from typing_extensions import TypedDict
    
    from pydantic import TypeAdapter, ValidationError
    
    class User(TypedDict):
        name: str
        id: int
    
    user_list_adapter = TypeAdapter(list[User])
    user_list = user_list_adapter.validate_python([{'name': 'Fred', 'id': '3'}])
    print(repr(user_list))
    #> [{'name': 'Fred', 'id': 3}]
    
    try:
        user_list_adapter.validate_python(
            [{'name': 'Fred', 'id': 'wrong', 'other': 'no'}]
        )
    except ValidationError as e:
        print(e)
        """
        1 validation error for list[User]
        0.id
          Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='wrong', input_type=str]
        """
    
    print(repr(user_list_adapter.dump_json(user_list)))
    #> b'[{"name":"Fred","id":3}]'
    
## Parsing data into a specified type

[](<https://pydantic.dev/docs/validation/latest/concepts/type_adapter/#parsing-data-into-a-specified-type>)

[`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) can be used to apply the parsing logic to populate Pydantic models in a more ad-hoc way. This function behaves similarly to [`BaseModel.model_validate`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel.model_validate>), but works with arbitrary Pydantic-compatible types.

This is especially useful when you want to parse results into a type that is not a direct subclass of [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>). For example:
    
    from pydantic import BaseModel, TypeAdapter
    
    class Item(BaseModel):
        id: int
        name: str
    
    # `item_data` could come from an API call, eg., via something like:
    # item_data = requests.get('https://my-api.com/items').json()
    item_data = [{'id': 1, 'name': 'My Item'}]
    
    items = TypeAdapter(list[Item]).validate_python(item_data)
    print(items)
    #> [Item(id=1, name='My Item')]
    
[`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) is capable of parsing data into any of the types Pydantic can handle as fields of a [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>).

## Rebuilding a `TypeAdapter`’s schema

[](<https://pydantic.dev/docs/validation/latest/concepts/type_adapter/#rebuilding-a-typeadapters-schema>)

✦ New in v2.10

[`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>)’s support deferred schema building and manual rebuilds. This is helpful for the case of:

  * Types with forward references
  * Types for which core schema builds are expensive

When you initialize a [`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) with a type, Pydantic analyzes the type and creates a core schema for it. This core schema contains the information needed to validate and serialize data for that type. See the [architecture documentation](<https://pydantic.dev/docs/validation/latest/internals/architecture>) for more information on core schemas.

If you set [`defer_build`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict.defer_build>) to `True` when initializing a `TypeAdapter`, Pydantic will defer building the core schema until the first time it is needed (for validation or serialization).

In order to manually trigger the building of the core schema, you can call the [`rebuild`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter.rebuild>) method on the [`TypeAdapter`](<https://pydantic.dev/docs/validation/latest/api/pydantic/type_adapter/#pydantic.type_adapter.TypeAdapter>) instance:
    
    from pydantic import ConfigDict, TypeAdapter
    
    ta = TypeAdapter('MyInt', config=ConfigDict(defer_build=True))
    
    # some time later, the forward reference is defined
    MyInt = int
    
    ta.rebuild()
    assert ta.validate_python(1) == 1
    
Was this page helpful?

Thanks for your feedback!