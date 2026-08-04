# Network Types | Pydantic Docs

> Source: [https://pydantic.dev/docs/validation/latest/api/pydantic/networks/](https://pydantic.dev/docs/validation/latest/api/pydantic/networks/)

[Skip to content](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#_top>)

[ Pydantic Docs ](<https://pydantic.dev/docs/>)

Search ` CtrlK `

# Network Types

The networks module contains types for common network-related fields.

## UrlConstraints 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints>)

Url constraints.

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#attributes>)

#### max_length 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints.max_length>)

The maximum length of the url. Defaults to `None`.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### allowed_schemes 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints.allowed_schemes>)

The allowed schemes. Defaults to `None`.

**Type:** [`list`](<https://docs.python.org/3/glossary.html#term-list>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### host_required 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints.host_required>)

Whether the host is required. Defaults to `None`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### default_host 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints.default_host>)

The default host. Defaults to `None`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### default_port 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints.default_port>)

The default port. Defaults to `None`.

**Type:** [`int`](<https://docs.python.org/3/library/functions.html#int>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### default_path 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints.default_path>)

The default path. Defaults to `None`.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

#### preserve_empty_path 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.UrlConstraints.preserve_empty_path>)

Whether to preserve empty URL paths. Defaults to `None`.

**Type:** [`bool`](<https://docs.python.org/3/library/functions.html#bool>) | [`None`](<https://docs.python.org/3/library/constants.html#None>)

## AnyUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

**Bases:** `_BaseUrl`

Base type for all URLs.

  * Any scheme allowed
  * Top-level domain (TLD) not required
  * Host not required

Assuming an input URL of `http://samuel:pass@example.com:8000/the/path/?query=here#fragment=is;this=bit`, the types export the following properties:

  * `scheme`: the URL scheme (`http`), always set.
  * `host`: the URL host (`example.com`).
  * `username`: optional username if included (`samuel`).
  * `password`: optional password if included (`pass`).
  * `port`: optional port (`8000`).
  * `path`: optional path (`/the/path/`).
  * `query`: optional URL query (for example, `GET` arguments or “search string”, such as `query=here`).
  * `fragment`: optional fragment (`fragment=is;this=bit`).

## AnyHttpUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyHttpUrl>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any http or https URL.

  * TLD not required
  * Host not required

## HttpUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.HttpUrl>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any http or https URL.

  * TLD not required
  * Host not required
  * Max length 2083

    from pydantic import BaseModel, HttpUrl, ValidationError
    
    class MyModel(BaseModel):
      url: HttpUrl
    
    m = MyModel(url='http://www.example.com')  # (1)
    print(m.url)
    #> http://www.example.com/
    
    try:
      MyModel(url='ftp://invalid.url')
    except ValidationError as e:
      print(e)
      '''
      1 validation error for MyModel
      url
        URL scheme should be 'http' or 'https' [type=url_scheme, input_value='ftp://invalid.url', input_type=str]
      '''
    
    try:
      MyModel(url='not a url')
    except ValidationError as e:
      print(e)
      '''
      1 validation error for MyModel
      url
        Input should be a valid URL, relative URL without a base [type=url_parsing, input_value='not a url', input_type=str]
      '''

Note: mypy would prefer `m = MyModel(url=HttpUrl('http://www.example.com'))`, but Pydantic will convert the string to an HttpUrl instance anyway.

“International domains” (e.g. a URL where the host or TLD includes non-ascii characters) will be encoded via [punycode](<https://en.wikipedia.org/wiki/Punycode>) (see [this article](<https://www.xudongz.com/blog/2017/idn-phishing/>) for a good description of why this is important):
    
    from pydantic import BaseModel, HttpUrl
    
    class MyModel(BaseModel):
        url: HttpUrl
    
    m1 = MyModel(url='http://puny£code.com')
    print(m1.url)
    #> http://xn--punycode-eja.com/
    m2 = MyModel(url='https://www.аррӏе.com/')
    print(m2.url)
    #> https://www.xn--80ak6aa92e.com/
    m3 = MyModel(url='https://www.example.珠宝/')
    print(m3.url)
    #> https://www.example.xn--pbt977c/
    
## AnyWebsocketUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyWebsocketUrl>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any ws or wss URL.

  * TLD not required
  * Host not required

## WebsocketUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.WebsocketUrl>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any ws or wss URL.

  * TLD not required
  * Host not required
  * Max length 2083

## FileUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.FileUrl>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any file URL.

  * Host not required

## FtpUrl 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.FtpUrl>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept ftp URL.

  * TLD not required
  * Host not required

## PostgresDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.PostgresDsn>)

**Bases:** `_BaseMultiHostUrl`

A type that will accept any Postgres DSN.

  * User info required
  * TLD not required
  * Host required
  * Supports multiple hosts

If further validation is required, these properties can be used by validators to enforce specific behaviour:
    
    from pydantic import (
        BaseModel,
        HttpUrl,
        PostgresDsn,
        ValidationError,
        field_validator,
    )
    
    class MyModel(BaseModel):
        url: HttpUrl
    
    m = MyModel(url='http://www.example.com')
    
    # the repr() method for a url will display all properties of the url
    print(repr(m.url))
    #> HttpUrl('http://www.example.com/')
    print(m.url.scheme)
    #> http
    print(m.url.host)
    #> www.example.com
    print(m.url.port)
    #> 80
    
    class MyDatabaseModel(BaseModel):
        db: PostgresDsn
    
        @field_validator('db')
        def check_db_name(cls, v):
            assert v.path and len(v.path) > 1, 'database must be provided'
            return v
    
    m = MyDatabaseModel(db='postgres://user:pass@localhost:5432/foobar')
    print(m.db)
    #> postgres://user:pass@localhost:5432/foobar
    
    try:
        MyDatabaseModel(db='postgres://user:pass@localhost:5432')
    except ValidationError as e:
        print(e)
        '''
        1 validation error for MyDatabaseModel
        db
          Assertion failed, database must be provided
        assert (None)
         +  where None = PostgresDsn('postgres://user:pass@localhost:5432').path [type=assertion_error, input_value='postgres://user:pass@localhost:5432', input_type=str]
        '''
    
### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#attributes-1>)

#### host 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.PostgresDsn.host>)

The required URL host.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## CockroachDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.CockroachDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any Cockroach DSN.

  * User info required
  * TLD not required
  * Host required

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#attributes-2>)

#### host 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.CockroachDsn.host>)

The required URL host.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## AmqpDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AmqpDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any AMQP DSN.

  * User info required
  * TLD not required
  * Host not required

## RedisDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.RedisDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any Redis DSN.

  * User info required
  * TLD not required
  * Host required (e.g., `rediss://:pass@localhost`)

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#attributes-3>)

#### host 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.RedisDsn.host>)

The required URL host.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## MongoDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.MongoDsn>)

**Bases:** `_BaseMultiHostUrl`

A type that will accept any MongoDB DSN.

  * User info not required
  * Database name not required
  * Port not required
  * User info may be passed without user part (e.g., `mongodb://mongodb0.example.com:27017`).

## KafkaDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.KafkaDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any Kafka DSN.

  * User info required
  * TLD not required
  * Host not required

## NatsDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.NatsDsn>)

**Bases:** `_BaseMultiHostUrl`

A type that will accept any NATS DSN.

NATS is a connective technology built for the ever increasingly hyper-connected world. It is a single technology that enables applications to securely communicate across any combination of cloud vendors, on-premise, edge, web and mobile, and devices. More: <https://nats.io>

## MySQLDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.MySQLDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any MySQL DSN.

  * User info required
  * TLD not required
  * Host not required

## MariaDBDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.MariaDBDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any MariaDB DSN.

  * User info required
  * TLD not required
  * Host not required

## ClickHouseDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.ClickHouseDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any ClickHouse DSN.

  * User info required
  * TLD not required
  * Host not required

## SnowflakeDsn 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.SnowflakeDsn>)

**Bases:** [`AnyUrl`](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.AnyUrl>)

A type that will accept any Snowflake DSN.

  * User info required
  * TLD not required
  * Host required

### Attributes

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#attributes-4>)

#### host 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.SnowflakeDsn.host>)

The required URL host.

**Type:** [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)

## EmailStr 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.EmailStr>)

Validate email addresses.
    
    from pydantic import BaseModel, EmailStr
    
    class Model(BaseModel):
        email: EmailStr
    
    print(Model(email='contact@mail.com'))
    #> email='contact@mail.com'
    
## NameEmail 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.NameEmail>)

**Bases:** `Representation`

Validate a name and email address combination, as specified by [RFC 5322](<https://datatracker.ietf.org/doc/html/rfc5322#section-3.4>).

The `NameEmail` has two properties: `name` and `email`. In case the `name` is not provided, it’s inferred from the email address.
    
    from pydantic import BaseModel, NameEmail
    
    class User(BaseModel):
        email: NameEmail
    
    user = User(email='Fred Bloggs <fred.bloggs@example.com>')
    print(user.email)
    #> Fred Bloggs <fred.bloggs@example.com>
    print(user.email.name)
    #> Fred Bloggs
    
    user = User(email='fred.bloggs@example.com')
    print(user.email)
    #> fred.bloggs <fred.bloggs@example.com>
    print(user.email.name)
    #> fred.bloggs
    
## IPvAnyAddress 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.IPvAnyAddress>)

Validate an IPv4 or IPv6 address.
    
    from pydantic import BaseModel
    from pydantic.networks import IPvAnyAddress
    
    class IpModel(BaseModel):
        ip: IPvAnyAddress
    
    print(IpModel(ip='127.0.0.1'))
    #> ip=IPv4Address('127.0.0.1')
    
    try:
        IpModel(ip='http://www.example.com')
    except ValueError as e:
        print(e.errors())
        '''
        [
            {
                'type': 'ip_any_address',
                'loc': ('ip',),
                'msg': 'value is not a valid IPv4 or IPv6 address',
                'input': 'http://www.example.com',
            }
        ]
        '''
    
## IPvAnyInterface 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.IPvAnyInterface>)

Validate an IPv4 or IPv6 interface.

## IPvAnyNetwork 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.IPvAnyNetwork>)

Validate an IPv4 or IPv6 network.

## validate_email 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.validate_email>)
    
    def validate_email(value: str) -> tuple[str, str]
    
Email address validation using [email-validator](<https://pypi.org/project/email-validator/>).

### Returns

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#returns>)

[`tuple`](<https://docs.python.org/3/library/stdtypes.html#tuple>)[[`str`](<https://docs.python.org/3/library/stdtypes.html#str>), [`str`](<https://docs.python.org/3/library/stdtypes.html#str>)] — A tuple containing the local part of the email (or the name for “pretty” email addresses) and the normalized email.

### Raises

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#raises>)

  * `PydanticCustomError` — If the email is invalid.

## MAX_EMAIL_LENGTH 

[](<https://pydantic.dev/docs/validation/latest/api/pydantic/networks/#pydantic.networks.MAX_EMAIL_LENGTH>)

Maximum length for an email. A somewhat arbitrary but very generous number compared to what is allowed by most implementations.

**Default:** `2048`

Was this page helpful?

Thanks for your feedback!