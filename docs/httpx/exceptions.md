# Exceptions - HTTPX

> Source: [https://www.python-httpx.org/exceptions/](https://www.python-httpx.org/exceptions/)

[ Skip to content ](<https://www.python-httpx.org/exceptions/#exceptions>)

# Exceptions

This page lists exceptions that may be raised when using HTTPX.

For an overview of how to work with HTTPX exceptions, see [Exceptions (Quickstart)](<https://www.python-httpx.org/quickstart/#exceptions>).

## The exception hierarchy

  * HTTPError
    * RequestError
      * TransportError
        * TimeoutException
          * ConnectTimeout
          * ReadTimeout
          * WriteTimeout
          * PoolTimeout
        * NetworkError
          * ConnectError
          * ReadError
          * WriteError
          * CloseError
        * ProtocolError
          * LocalProtocolError
          * RemoteProtocolError
        * ProxyError
        * UnsupportedProtocol
      * DecodingError
      * TooManyRedirects
    * HTTPStatusError
  * InvalidURL
  * CookieConflict
  * StreamError
    * StreamConsumed
    * ResponseNotRead
    * RequestNotRead
    * StreamClosed

* * *

## Exception classes

_class_`httpx.**HTTPError**`(_message_)

Base class for `RequestError` and `HTTPStatusError`.

Useful for `try...except` blocks when issuing a request, and then calling `.raise_for_status()`.

For example:
    
    try:
        response = httpx.get("https://www.example.com")
        response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"HTTP Exception for {exc.request.url} - {exc}")
    
_class_`httpx.**RequestError**`(_message_ , _*_ , _request=None_)

Base class for all exceptions that may occur when issuing a `.request()`.

_class_`httpx.**TransportError**`(_message_ , _*_ , _request=None_)

Base class for all exceptions that occur at the level of the Transport API.

_class_`httpx.**TimeoutException**`(_message_ , _*_ , _request=None_)

The base class for timeout errors.

An operation has timed out.

_class_`httpx.**ConnectTimeout**`(_message_ , _*_ , _request=None_)

Timed out while connecting to the host.

_class_`httpx.**ReadTimeout**`(_message_ , _*_ , _request=None_)

Timed out while receiving data from the host.

_class_`httpx.**WriteTimeout**`(_message_ , _*_ , _request=None_)

Timed out while sending data to the host.

_class_`httpx.**PoolTimeout**`(_message_ , _*_ , _request=None_)

Timed out waiting to acquire a connection from the pool.

_class_`httpx.**NetworkError**`(_message_ , _*_ , _request=None_)

The base class for network-related errors.

An error occurred while interacting with the network.

_class_`httpx.**ConnectError**`(_message_ , _*_ , _request=None_)

Failed to establish a connection.

_class_`httpx.**ReadError**`(_message_ , _*_ , _request=None_)

Failed to receive data from the network.

_class_`httpx.**WriteError**`(_message_ , _*_ , _request=None_)

Failed to send data through the network.

_class_`httpx.**CloseError**`(_message_ , _*_ , _request=None_)

Failed to close a connection.

_class_`httpx.**ProtocolError**`(_message_ , _*_ , _request=None_)

The protocol was violated.

_class_`httpx.**LocalProtocolError**`(_message_ , _*_ , _request=None_)

A protocol was violated by the client.

For example if the user instantiated a `Request` instance explicitly, failed to include the mandatory `Host:` header, and then issued it directly using `client.send()`.

_class_`httpx.**RemoteProtocolError**`(_message_ , _*_ , _request=None_)

The protocol was violated by the server.

For example, returning malformed HTTP.

_class_`httpx.**ProxyError**`(_message_ , _*_ , _request=None_)

An error occurred while establishing a proxy connection.

_class_`httpx.**UnsupportedProtocol**`(_message_ , _*_ , _request=None_)

Attempted to make a request to an unsupported protocol.

For example issuing a request to `ftp://www.example.com`.

_class_`httpx.**DecodingError**`(_message_ , _*_ , _request=None_)

Decoding of the response failed, due to a malformed encoding.

_class_`httpx.**TooManyRedirects**`(_message_ , _*_ , _request=None_)

Too many redirects.

_class_`httpx.**HTTPStatusError**`(_message_ , _*_ , _request_ , _response_)

The response had an error HTTP status of 4xx or 5xx.

May be raised when calling `response.raise_for_status()`

_class_`httpx.**InvalidURL**`(_message_)

URL is improperly formed or cannot be parsed.

_class_`httpx.**CookieConflict**`(_message_)

Attempted to lookup a cookie by name, but multiple cookies existed.

Can occur when calling `response.cookies.get(...)`.

_class_`httpx.**StreamError**`(_message_)

The base class for stream exceptions.

The developer made an error in accessing the request stream in an invalid way.

_class_`httpx.**StreamConsumed**`()

Attempted to read or stream content, but the content has already been streamed.

_class_`httpx.**StreamClosed**`()

Attempted to read or stream response content, but the request has been closed.

_class_`httpx.**ResponseNotRead**`()

Attempted to access streaming response content, without having called `read()`.

_class_`httpx.**RequestNotRead**`()

Attempted to access streaming request content, without having called `read()`.