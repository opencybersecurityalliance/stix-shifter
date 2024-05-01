try:
    # new Python 3.8 timeout exception
    from asyncio.exceptions import TimeoutError as TimeoutException
except ImportError:
    from concurrent.futures._base import TimeoutError as TimeoutException


# General
class MissingWriterException(Exception):
    pass


# timeouts
class BaseTimeout(Exception):
    pass


class ConnectTimeout(BaseTimeout):
    pass


class ReadTimeout(BaseTimeout):
    pass


class RequestTimeout(BaseTimeout):
    pass


class ConnectionPoolAcquireTimeout(BaseTimeout):
    pass


# parsing
class HttpParsingError(Exception):
    pass


# Redirects
class MaxRedirects(Exception):
    pass


# Reconnect
class ConnectionDisconnected(Exception):
    pass


# HTTP2
class MissingEvent(Exception):
    pass
