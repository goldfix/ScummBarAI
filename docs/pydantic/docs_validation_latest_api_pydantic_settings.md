# Pydantic Settings | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic_settings/](https://pydantic.dev/docs/validation/latest/api/pydantic_settings/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Pydantic Settings

## SettingsError 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SettingsError>)

**Bases:** [`ValueError`](<https://docs.python.org/3/library/exceptions.html#ValueError>)

Base exception for settings-related errors.

## PyprojectTomlConfigSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PyprojectTomlConfigSettingsSource>)

**Bases:** `TomlConfigSettingsSource`

A source class that loads variables from a `pyproject.toml` file.

## JsonConfigSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.JsonConfigSettingsSource>)

**Bases:** `InitSettingsSource`, `ConfigFileSourceMixin`

A source class that loads variables from a JSON file

## NoDecode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.NoDecode>)

Annotation to prevent decoding of a field value.

## SecretsSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource>)

**Bases:** `PydanticBaseEnvSettingsSource`

Source class for loading settings values from secret files.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#methods>)

#### find_case_path 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource.find_case_path>)

`@classmethod`
    
    def find_case_path(
        cls,
        dir_path: Path,
        file_name: str,
        case_sensitive: bool,
    ) -> Path | None
    
Find a file within path’s directory matching filename, optionally ignoring case.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns>)

`Path` | [`None`](<https://docs.python.org/3/library/constants.html#None>) — Whether file path or `None` if file does not exist in directory.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters>)

**`dir_path`** : `Path`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource.find_case_path\(dir_path\)>)

Directory path.

**`file_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource.find_case_path\(file_name\)>)

File name.

**`case_sensitive`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource.find_case_path\(case_sensitive\)>)

Whether to search for file name case sensitively.

#### get_field_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource.get_field_value>)
    
    def get_field_value(field: FieldInfo, field_name: str) -> tuple[Any, str, bool]
    
Gets the value for field from secret file and a flag to determine whether value is complex.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-1>)

[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] — A tuple that contains the value (`None` if the file does not exist), key, and a flag to determine whether value is complex.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-1>)

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource.get_field_value\(field\)>)

The field.

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SecretsSettingsSource.get_field_value\(field_name\)>)

The field name.

## ForceDecode 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.ForceDecode>)

Annotation to force decoding of a field value.

## DotEnvSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.DotEnvSettingsSource>)

**Bases:** `EnvSettingsSource`

Source class for loading settings values from env files.

## YamlConfigSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.YamlConfigSettingsSource>)

**Bases:** `InitSettingsSource`, `ConfigFileSourceMixin`

A source class that loads variables from a yaml file

## EnvSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource>)

**Bases:** `PydanticBaseEnvSettingsSource`

Source class for loading settings values from environment variables.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#methods-1>)

#### get_field_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.get_field_value>)
    
    def get_field_value(field: FieldInfo, field_name: str) -> tuple[Any, str, bool]
    
Gets the value for field from environment variables and a flag to determine whether value is complex.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-2>)

[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] — A tuple that contains the value (`None` if not found), key, and a flag to determine whether value is complex.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-2>)

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.get_field_value\(field\)>)

The field.

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.get_field_value\(field_name\)>)

The field name.

#### prepare_field_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.prepare_field_value>)
    
    def prepare_field_value(
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool,
    ) -> Any
    
Prepare value for the field.

  * Extract value for nested field.
  * Deserialize value to python object for complex field.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-3>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — A tuple contains prepared value for the field.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-3>)

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.prepare_field_value\(field\)>)

The field.

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.prepare_field_value\(field_name\)>)

The field name.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#raises>)

  * `ValuesError` — When There is an error in deserializing value for complex field.

#### next_field 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.next_field>)
    
    def next_field(
        field: FieldInfo | Any | None,
        key: str,
        case_sensitive: bool | None = None,
    ) -> FieldInfo | None
    
Find the field in a sub model by key(env name)

By having the following models:
    
    class SubSubModel(BaseSettings):
        dvals: Dict
    
    class SubModel(BaseSettings):
        vals: list[str]
        sub_sub_model: SubSubModel
    
    class Cfg(BaseSettings):
        sub_model: SubModel
    
##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-4>)

`FieldInfo` | [`None`](<https://docs.python.org/3/library/constants.html#None>) — Field if it finds the next field otherwise `None`.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-4>)

**`field`** : `FieldInfo` | [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.next_field\(field\)>)

The field.

**`key`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.next_field\(key\)>)

The key (env name).

**`case_sensitive`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.next_field\(case_sensitive\)>)

Whether to search for key case sensitively.

#### explode_env_vars 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.explode_env_vars>)
    
    def explode_env_vars(
        field_name: str,
        field: FieldInfo,
        env_vars: Mapping[str, str | None],
    ) -> dict[str, Any]
    
Process env_vars and extract the values of keys containing env_nested_delimiter into nested dictionaries.

This is applied to a single field, hence filtering by env_var prefix.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-5>)

[`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] — A dictionary contains extracted values from nested env values.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-5>)

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.explode_env_vars\(field_name\)>)

The field name.

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.explode_env_vars\(field\)>)

The field.

**`env_vars`** : [`Mapping`](<https://docs.python.org/3/library/typing.html#typing.Mapping>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.EnvSettingsSource.explode_env_vars\(env_vars\)>)

Environment variables.

## TomlConfigSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.TomlConfigSettingsSource>)

**Bases:** `InitSettingsSource`, `ConfigFileSourceMixin`

A source class that loads variables from a TOML file

## SettingsConfigDict 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SettingsConfigDict>)

**Bases:** [`ConfigDict`](<https://pydantic.dev/docs/validation/latest/api/pydantic/config/#pydantic.config.ConfigDict>)

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#attributes>)

#### yaml_config_section 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SettingsConfigDict.yaml_config_section>)

Specifies the section in a YAML file from which to load the settings. Supports dot-notation for nested paths (e.g., ‘config.app.settings’). If provided, the settings will be loaded from the specified section. This is useful when the YAML file contains multiple configuration sections and you only want to load a specific subset into your settings model.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### pyproject_toml_depth 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SettingsConfigDict.pyproject_toml_depth>)

Number of levels **up** from the current working directory to attempt to find a pyproject.toml file.

This is only used when a pyproject.toml file is not found in the current working directory.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>)

#### pyproject_toml_table_header 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.SettingsConfigDict.pyproject_toml_table_header>)

Header of the TOML table within a pyproject.toml file to use when filling variables. This is supplied as a `tuple[str, ...]` instead of a `str` to accommodate for headers containing a `.`.

For example, `toml_table_header = ("tool", "my.tool", "foo")` can be used to fill variable values from a table with header `[tool."my.tool".foo]`.

To use the root table, exclude this config setting or provide an empty tuple.

**Type:** [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), …]

## PydanticBaseSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource>)

**Bases:** `ABC`

Abstract base class for settings sources, every settings source classes should inherit from it.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#attributes-1>)

#### current_state 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.current_state>)

The current state of the settings, populated by the previous settings sources.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]

#### settings_sources_data 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.settings_sources_data>)

The state of all previous settings sources.

**Type:** [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]]

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#methods-2>)

#### get_field_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.get_field_value>)

`@abstractmethod`
    
    def get_field_value(field: FieldInfo, field_name: str) -> tuple[Any, str, bool]
    
Gets the value, the key for model creation, and a flag to determine whether value is complex.

This is an abstract method that should be overridden in every settings source classes.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-6>)

[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`bool`](<https://docs.python.org/3/library/functions.html#bool>)] — A tuple that contains the value, key and a flag to determine whether value is complex.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-6>)

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.get_field_value\(field\)>)

The field.

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.get_field_value\(field_name\)>)

The field name.

#### field_is_complex 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.field_is_complex>)
    
    def field_is_complex(field: FieldInfo) -> bool
    
Checks whether a field is complex, in which case it will attempt to be parsed as JSON.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-7>)

[`bool`](<https://docs.python.org/3/library/functions.html#bool>) — Whether the field is complex.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-7>)

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.field_is_complex\(field\)>)

The field.

#### prepare_field_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.prepare_field_value>)
    
    def prepare_field_value(
        field_name: str,
        field: FieldInfo,
        value: Any,
        value_is_complex: bool,
    ) -> Any
    
Prepares the value of a field.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-8>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The prepared value.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-8>)

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.prepare_field_value\(field_name\)>)

The field name.

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.prepare_field_value\(field\)>)

The field.

**`value`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.prepare_field_value\(value\)>)

The value of the field that has to be prepared.

**`value_is_complex`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.prepare_field_value\(value_is_complex\)>)

A flag to determine whether value is complex.

#### decode_complex_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.decode_complex_value>)
    
    def decode_complex_value(field_name: str, field: FieldInfo, value: Any) -> Any
    
Decode the value for a complex field

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-9>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — The decoded value for further preparation

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-9>)

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.decode_complex_value\(field_name\)>)

The field name.

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.decode_complex_value\(field\)>)

The field.

**`value`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.PydanticBaseSettingsSource.decode_complex_value\(value\)>)

The value of the field that has to be prepared.

## BaseSettings 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings>)

**Bases:** [`BaseModel`](<https://pydantic.dev/docs/validation/latest/api/pydantic/base_model/#pydantic.BaseModel>)

Base class for settings, allowing values to be overridden by environment variables.

This is useful in production for secrets you do not wish to save in code, it plays nicely with docker(-compose), Heroku and any 12 factor app design.

All the below attributes can be set via `model_config`.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#constructor-parameters>)

**`_case_sensitive`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_case_sensitive\)>)

Whether environment and CLI variable names should be read with case-sensitivity. Defaults to `None`.

**`_nested_model_default_partial_update`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_nested_model_default_partial_update\)>)

Whether to allow partial updates on nested model default object fields. Defaults to `False`.

**`_env_prefix`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_prefix\)>)

Prefix for all environment variables. Defaults to `None`.

**`_env_prefix_target`** : `EnvPrefixTarget` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_prefix_target\)>)

Targets to which `_env_prefix` is applied. Default: `variable`.

**`_env_file`** : `DotenvType` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `ENV_FILE_SENTINEL`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_file\)>)

The env file(s) to load settings values from. Defaults to `Path('')`, which means that the value from `model_config['env_file']` should be used. You can also pass `None` to indicate that environment variables should not be loaded from an env file.

**`_env_file_encoding`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_file_encoding\)>)

The env file encoding, e.g. `'latin-1'`. Defaults to `None`.

**`_env_ignore_empty`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_ignore_empty\)>)

Ignore environment variables where the value is an empty string. Default to `False`.

**`_env_nested_delimiter`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_nested_delimiter\)>)

The nested env values delimiter. Defaults to `None`.

**`_env_nested_max_split`** : [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_nested_max_split\)>)

The nested env values maximum nesting. Defaults to `None`, which means no limit.

**`_env_parse_none_str`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_parse_none_str\)>)

The env string value that should be parsed (e.g. “null”, “void”, “None”, etc.) into `None` type(None). Defaults to `None` type(None), which means no parsing should occur.

**`_env_parse_enums`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_env_parse_enums\)>)

Parse enum field names to values. Defaults to `None.`, which means no parsing should occur.

**`_cli_prog_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_prog_name\)>)

The CLI program name to display in help text. Defaults to `None` if _cli_parse_args is `None`. Otherwise, defaults to sys.argv[0].

**`_cli_parse_args`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), …] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_parse_args\)>)

The list of CLI arguments to parse. Defaults to None. If set to `True`, defaults to sys.argv[1:].

**`_cli_settings_source`** : `CliSettingsSource`[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_settings_source\)>)

Override the default CLI settings source with a user defined instance. Defaults to None.

**`_cli_parse_none_str`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_parse_none_str\)>)

The CLI string value that should be parsed (e.g. “null”, “void”, “None”, etc.) into `None` type(None). Defaults to _env_parse_none_str value if set. Otherwise, defaults to “null” if _cli_avoid_json is `False`, and “None” if _cli_avoid_json is `True`.

**`_cli_hide_none_type`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_hide_none_type\)>)

Hide `None` values in CLI help text. Defaults to `False`.

**`_cli_avoid_json`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_avoid_json\)>)

Avoid complex JSON objects in CLI help text. Defaults to `False`.

**`_cli_enforce_required`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_enforce_required\)>)

Enforce required fields at the CLI. Defaults to `False`.

**`_cli_use_class_docs_for_groups`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_use_class_docs_for_groups\)>)

Use class docstrings in CLI group help text instead of field descriptions. Defaults to `False`.

**`_cli_exit_on_error`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_exit_on_error\)>)

Determines whether or not the internal parser exits with error info when an error occurs. Defaults to `True`.

**`_cli_prefix`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_prefix\)>)

The root parser command line arguments prefix. Defaults to "".

**`_cli_flag_prefix_char`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_flag_prefix_char\)>)

The flag prefix character to use for CLI optional arguments. Defaults to ’-’.

**`_cli_implicit_flags`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘dual’, ‘toggle’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_implicit_flags\)>)

Controls how `bool` fields are exposed as CLI flags.

  * False (default): no implicit flags are generated; booleans must be set explicitly (e.g. —flag=true).
  * True / ‘dual’: optional boolean fields generate both positive and negative forms (—flag and —no-flag).
  * ‘toggle’: required boolean fields remain in ‘dual’ mode, while optional boolean fields generate a single flag aligned with the default value (if default=False, expose —flag; if default=True, expose —no-flag).

**`_cli_ignore_unknown_args`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_ignore_unknown_args\)>)

Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.

**`_cli_kebab_case`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘all’, ‘no_enums’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_kebab_case\)>)

CLI args use kebab case. Defaults to `False`.

**`_cli_shortcuts`** : [`Mapping`](<https://docs.python.org/3/library/typing.html#typing.Mapping>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_cli_shortcuts\)>)

Mapping of target field name to alias names. Defaults to `None`.

**`_secrets_dir`** : `PathType` | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_secrets_dir\)>)

The secret files directory or a sequence of directories. Defaults to `None`.

**`_build_sources`** : [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[`PydanticBaseSettingsSource`, …], [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.__init__\(_build_sources\)>)

Pre-initialized sources and init kwargs to use for building instantiation values. Defaults to `None`.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#methods-3>)

#### settings_customise_sources 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.settings_customise_sources>)

`@classmethod`
    
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]
    
Define the sources and their order for loading the settings values.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-10>)

[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[`PydanticBaseSettingsSource`, …] — A tuple containing the sources and their order for loading the settings values.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-10>)

**`settings_cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`BaseSettings`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.settings_customise_sources\(settings_cls\)>)

The Settings class.

**`init_settings`** : `PydanticBaseSettingsSource`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.settings_customise_sources\(init_settings\)>)

The `InitSettingsSource` instance.

**`env_settings`** : `PydanticBaseSettingsSource`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.settings_customise_sources\(env_settings\)>)

The `EnvSettingsSource` instance.

**`dotenv_settings`** : `PydanticBaseSettingsSource`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.settings_customise_sources\(dotenv_settings\)>)

The `DotEnvSettingsSource` instance.

**`file_secret_settings`** : `PydanticBaseSettingsSource`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.BaseSettings.settings_customise_sources\(file_secret_settings\)>)

The `SecretsSettingsSource` instance.

## GoogleSecretManagerSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.GoogleSecretManagerSettingsSource>)

**Bases:** `EnvSettingsSource`

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#methods-4>)

#### get_field_value 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.GoogleSecretManagerSettingsSource.get_field_value>)
    
    def get_field_value(field: FieldInfo, field_name: str) -> tuple[Any, str, bool]
    
Override get_field_value to get the secret value from GCP Secret Manager. Look for a SecretVersion metadata field to specify a particular SecretVersion.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-11>)

[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) — A tuple of (value, key, value_is_complex), where `key` is the identifier used [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — to populate the model (either the field name or an alias, depending on [`bool`](<https://docs.python.org/3/library/functions.html#bool>) — configuration).

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-11>)

**`field`** : `FieldInfo`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.GoogleSecretManagerSettingsSource.get_field_value\(field\)>)

The field to get the value for

**`field_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.GoogleSecretManagerSettingsSource.get_field_value\(field_name\)>)

The declared name of the field

## CliSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource>)

**Bases:** `EnvSettingsSource`, `Generic[T]`

Source class for loading settings values from CLI.

### Constructor Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#constructor-parameters-1>)

**`cli_prog_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_prog_name\)>)

The CLI program name to display in help text. Defaults to `None` if cli_parse_args is `None`. Otherwise, defaults to sys.argv[0].

**`cli_parse_args`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), …] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_parse_args\)>)

The list of CLI arguments to parse. Defaults to None. If set to `True`, defaults to sys.argv[1:].

**`cli_parse_none_str`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_parse_none_str\)>)

The CLI string value that should be parsed (e.g. “null”, “void”, “None”, etc.) into `None` type(None). Defaults to “null” if cli_avoid_json is `False`, and “None” if cli_avoid_json is `True`.

**`cli_hide_none_type`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_hide_none_type\)>)

Hide `None` values in CLI help text. Defaults to `False`.

**`cli_avoid_json`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_avoid_json\)>)

Avoid complex JSON objects in CLI help text. Defaults to `False`.

**`cli_enforce_required`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_enforce_required\)>)

Enforce required fields at the CLI. Defaults to `False`.

**`cli_use_class_docs_for_groups`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_use_class_docs_for_groups\)>)

Use class docstrings in CLI group help text instead of field descriptions. Defaults to `False`.

**`cli_exit_on_error`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_exit_on_error\)>)

Determines whether or not the internal parser exits with error info when an error occurs. Defaults to `True`.

**`cli_prefix`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_prefix\)>)

Prefix for command line arguments added under the root parser. Defaults to "".

**`cli_flag_prefix_char`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_flag_prefix_char\)>)

The flag prefix character to use for CLI optional arguments. Defaults to ’-’.

**`cli_implicit_flags`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘dual’, ‘toggle’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_implicit_flags\)>)

Controls how `bool` fields are exposed as CLI flags.

  * False (default): no implicit flags are generated; booleans must be set explicitly (e.g. —flag=true).
  * True / ‘dual’: optional boolean fields generate both positive and negative forms (—flag and —no-flag).
  * ‘toggle’: required boolean fields remain in ‘dual’ mode, while optional boolean fields generate a single flag aligned with the default value (if default=False, expose —flag; if default=True, expose —no-flag).

**`cli_ignore_unknown_args`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_ignore_unknown_args\)>)

Whether to ignore unknown CLI args and parse only known ones. Defaults to `False`.

**`cli_kebab_case`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘all’, ‘no_enums’] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_kebab_case\)>)

CLI args use kebab case. Defaults to `False`.

**`cli_shortcuts`** : [`Mapping`](<https://docs.python.org/3/library/typing.html#typing.Mapping>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)]] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(cli_shortcuts\)>)

Mapping of target field name to alias names. Defaults to `None`.

**`case_sensitive`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(case_sensitive\)>)

Whether CLI “—arg” names should be read with case-sensitivity. Defaults to `True`. Note: Case-insensitive matching is only supported on the internal root parser and does not apply to CLI subcommands.

**`root_parser`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(root_parser\)>)

The root parser object.

**`parse_args_method`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(parse_args_method\)>)

The root parser parse args method. Defaults to `argparse.ArgumentParser.parse_args`.

**`add_argument_method`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `ArgumentParser.add_argument`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(add_argument_method\)>)

The root parser add argument method. Defaults to `argparse.ArgumentParser.add_argument`.

**`add_argument_group_method`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `ArgumentParser.add_argument_group`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(add_argument_group_method\)>)

The root parser add argument group method. Defaults to `argparse.ArgumentParser.add_argument_group`.

**`add_parser_method`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `_SubParsersAction.add_parser`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(add_parser_method\)>)

The root parser add new parser (sub-command) method. Defaults to `argparse._SubParsersAction.add_parser`.

**`add_subparsers_method`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `ArgumentParser.add_subparsers`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(add_subparsers_method\)>)

The root parser add subparsers (sub-commands) method. Defaults to `argparse.ArgumentParser.add_subparsers`.

**`format_help_method`** : [`Callable`](<https://docs.python.org/3/library/typing.html#typing.Callable>)[…, [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `ArgumentParser.format_help`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(format_help_method\)>)

The root parser format help method. Defaults to `argparse.ArgumentParser.format_help`.

**`formatter_class`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `RawDescriptionHelpFormatter`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.__init__\(formatter_class\)>)

A class for customizing the root parser help text. Defaults to `argparse.RawDescriptionHelpFormatter`.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#attributes-2>)

#### root_parser 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliSettingsSource.root_parser>)

The connected root parser instance.

**Type:** `T`

## InitSettingsSource 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.InitSettingsSource>)

**Bases:** `PydanticBaseSettingsSource`

Source class for loading values provided during settings class initialization.

## CliApp 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp>)

A utility class for running Pydantic `BaseSettings`, `BaseModel`, or `pydantic.dataclasses.dataclass` as CLI applications.

### Methods

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#methods-5>)

#### run 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run>)

`@staticmethod`
    
    def run(
        model_cls: type[T],
        cli_args: list[str] | Namespace | SimpleNamespace | dict[str, Any] | None = None,
        cli_settings_source: CliSettingsSource[Any] | None = None,
        cli_exit_on_error: bool | None = None,
        cli_cmd_method_name: str = 'cli_cmd',
        **model_init_data: Any,
    ) -> T
    
Runs a Pydantic `BaseSettings`, `BaseModel`, or `pydantic.dataclasses.dataclass` as a CLI application. Running a model as a CLI application requires the `cli_cmd` method to be defined in the model class.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-12>)

`T` — The ran instance of model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-12>)

**`model_cls`** : [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`T`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run\(model_cls\)>)

The model class to run as a CLI application.

**`cli_args`** : [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | `Namespace` | `SimpleNamespace` | [`dict`](<https://docs.python.org/3/reference/expressions.html#dict>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run\(cli_args\)>)

The list of CLI arguments to parse. If `cli_settings_source` is specified, this may also be a namespace or dictionary of pre-parsed CLI arguments. Defaults to `sys.argv[1:]`.

**`cli_settings_source`** : `CliSettingsSource`[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run\(cli_settings_source\)>)

Override the default CLI settings source with a user defined instance. Defaults to `None`.

**`cli_exit_on_error`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run\(cli_exit_on_error\)>)

Determines whether this function exits on error. If model is subclass of `BaseSettings`, defaults to BaseSettings `cli_exit_on_error` value. Otherwise, defaults to `True`.

**`cli_cmd_method_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `'cli_cmd'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run\(cli_cmd_method_name\)>)

The CLI command method name to run. Defaults to “cli_cmd”.

**`model_init_data`** : [`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>) _Default:_ `{}`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run\(model_init_data\)>)

The model init data.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#raises-1>)

  * `SettingsError` — If model_cls is not subclass of `BaseModel` or `pydantic.dataclasses.dataclass`.
  * `SettingsError` — If model_cls does not have a `cli_cmd` entrypoint defined.

#### run_subcommand 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run_subcommand>)

`@staticmethod`
    
    def run_subcommand(
        model: PydanticModel,
        cli_exit_on_error: bool | None = None,
        cli_cmd_method_name: str = 'cli_cmd',
    ) -> PydanticModel
    
Runs the model subcommand. Running a model subcommand requires the `cli_cmd` method to be defined in the nested model subcommand class.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-13>)

`PydanticModel` — The ran subcommand model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-13>)

**`model`** : `PydanticModel`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run_subcommand\(model\)>)

The model to run the subcommand from.

**`cli_exit_on_error`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run_subcommand\(cli_exit_on_error\)>)

Determines whether this function exits with error if no subcommand is found. Defaults to model_config `cli_exit_on_error` value if set. Otherwise, defaults to `True`.

**`cli_cmd_method_name`** : [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) _Default:_ `'cli_cmd'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.run_subcommand\(cli_cmd_method_name\)>)

The CLI command method name to run. Defaults to “cli_cmd”.

##### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#raises-2>)

  * `SystemExit` — When no subcommand is found and cli_exit_on_error=`True` (the default).
  * `SettingsError` — When no subcommand is found and cli_exit_on_error=`False`.

#### serialize 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.serialize>)

`@staticmethod`
    
    def serialize(
        model: PydanticModel,
        list_style: Literal['json', 'argparse', 'lazy'] = 'json',
        dict_style: Literal['json', 'env'] = 'json',
        positionals_first: bool = False,
    ) -> list[str]
    
Serializes the CLI arguments for a Pydantic data model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-14>)

[`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] — The serialized CLI arguments for the data model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-14>)

**`model`** : `PydanticModel`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.serialize\(model\)>)

The data model to serialize.

**`list_style`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘json’, ‘argparse’, ‘lazy’] _Default:_ `'json'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.serialize\(list_style\)>)

Controls how list-valued fields are serialized on the command line.

  * ‘json’ (default): Lists are encoded as a single JSON array. Example: `--tags '["a","b","c"]'`
  * ‘argparse’: Each list element becomes its own repeated flag, following typical `argparse` conventions. Example: `--tags a --tags b --tags c`
  * ‘lazy’: Lists are emitted as a single comma-separated string without JSON quoting or escaping. Example: `--tags a,b,c`

**`dict_style`** : [`Literal`](<https://docs.python.org/3/library/typing.html#typing.Literal>)[‘json’, ‘env’] _Default:_ `'json'`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.serialize\(dict_style\)>)

Controls how dictionary-valued fields are serialized.

  * ‘json’ (default): The entire dictionary is emitted as a single JSON object. Example: `--config '{"host": "localhost", "port": 5432}'`
  * ‘env’: The dictionary is flattened into multiple CLI flags using environment-variable-style assignement. Example: `--config host=localhost --config port=5432`

**`positionals_first`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.serialize\(positionals_first\)>)

Controls whether positional arguments should be serialized first compared to optional arguments. Defaults to `False`.

#### format_help 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.format_help>)

`@staticmethod`
    
    def format_help(
        model: PydanticModel | type[T],
        cli_settings_source: CliSettingsSource[Any] | None = None,
        strip_ansi_color: bool = False,
    ) -> str
    
Return a string containing a help message for a Pydantic model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-15>)

[`str`](<https://docs.python.org/3/library/stdtypes.html#str>) — The help message string for the model.

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-15>)

**`model`** : `PydanticModel` | [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`T`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.format_help\(model\)>)

The model or model class.

**`cli_settings_source`** : `CliSettingsSource`[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.format_help\(cli_settings_source\)>)

Override the default CLI settings source with a user defined instance. Defaults to `None`.

**`strip_ansi_color`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.format_help\(strip_ansi_color\)>)

Strips ANSI color codes from the help message when set to `True`.

#### print_help 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.print_help>)

`@staticmethod`
    
    def print_help(
        model: PydanticModel | type[T],
        cli_settings_source: CliSettingsSource[Any] | None = None,
        file: TextIO | None = None,
        strip_ansi_color: bool = False,
    ) -> None
    
Print a help message for a Pydantic model.

##### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-16>)

[`None`](<https://docs.python.org/3/library/constants.html#None>)

##### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-16>)

**`model`** : `PydanticModel` | [`type`](<https://docs.python.org/3/glossary.html#term-type>)[`T`] 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.print_help\(model\)>)

The model or model class.

**`cli_settings_source`** : `CliSettingsSource`[[`Any`](<https://docs.python.org/3/library/typing.html#typing.Any>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.print_help\(cli_settings_source\)>)

Override the default CLI settings source with a user defined instance. Defaults to `None`.

**`file`** : [`TextIO`](<https://docs.python.org/3/library/typing.html#typing.TextIO>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.print_help\(file\)>)

A text stream to which the help message is written. If `None`, the output is sent to sys.stdout.

**`strip_ansi_color`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `False`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.CliApp.print_help\(strip_ansi_color\)>)

Strips ANSI color codes from the help message when set to `True`.

## get_subcommand 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.get_subcommand>)
    
    def get_subcommand(
        model: PydanticModel,
        is_required: bool = True,
        cli_exit_on_error: bool | None = None,
        _suppress_errors: list[SettingsError | SystemExit] | None = None,
    ) -> PydanticModel | None
    
Get the subcommand from a model.

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#returns-17>)

`PydanticModel` | [`None`](<https://docs.python.org/3/library/constants.html#None>) — The subcommand model if found, otherwise `None`.

### Parameters

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#parameters-17>)

**`model`** : `PydanticModel`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.get_subcommand\(model\)>)

The model to get the subcommand from.

**`is_required`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) _Default:_ `True`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.get_subcommand\(is_required\)>)

Determines whether a model must have subcommand set and raises error if not found. Defaults to `True`.

**`cli_exit_on_error`** : [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>) _Default:_ `None`

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#pydantic_settings.get_subcommand\(cli_exit_on_error\)>)

Determines whether this function exits with error if no subcommand is found. Defaults to model_config `cli_exit_on_error` value if set. Otherwise, defaults to `True`.

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic_settings/#raises-3>)

  * `SystemExit` — When no subcommand is found and is_required=`True` and cli_exit_on_error=`True` (the default).
  * `SettingsError` — When no subcommand is found and is_required=`True` and cli_exit_on_error=`False`.

Was this page helpful?

Thanks for your feedback!