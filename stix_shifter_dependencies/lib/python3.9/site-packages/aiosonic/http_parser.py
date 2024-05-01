from typing import TYPE_CHECKING, AsyncIterator, Dict, Iterator, List
from urllib.parse import ParseResult, urlencode, urlparse

from onecache import CacheDecorator

from aiosonic.connection import Connection
from aiosonic.types import BodyType, DataType, ParsedBodyType

if TYPE_CHECKING:
    from aiosonic import HeadersType

REPLACEABLE_HEADERS = {"host", "user-agent"}
_LRU_CACHE_SIZE = 512

# Functions with cache
@CacheDecorator(_LRU_CACHE_SIZE)
def get_url_parsed(url: str) -> ParseResult:
    """Get url parsed.

    With CacheDecorator for the sake of speed.
    """
    return urlparse(url)


async def parse_headers_iterator(connection: Connection):
    """Transform loop to iterator."""
    while True:
        # StreamReader already buffers data reading so it is efficient.
        res_data = await connection.reader.readline()
        if b": " not in res_data and b":" not in res_data:
            break
        yield res_data


def headers_iterator(headers: 'HeadersType'):
    iterator = headers if isinstance(headers, List) else headers.items()
    for key, data in iterator:
        yield key, data


def add_header(headers: 'HeadersType', key: str, value: str, replace=False):
    """Safe add header method."""
    if isinstance(headers, List):
        if replace:
            included = [item for item in headers if item[0].lower() == key.lower()]
            if included:
                headers.remove(included[0])
        headers.append((key, value))
    else:
        headers[key] = value


def add_headers(headers: 'HeadersType', headers_to_add: 'HeadersType'):
    """Safe add multiple headers."""
    for key, data in headers_iterator(headers_to_add):
        replace = key.lower() in REPLACEABLE_HEADERS
        add_header(headers, key, data, replace)


def setup_body_request(data: DataType, headers: 'HeadersType') -> ParsedBodyType:
    """Get body to be sent."""

    if isinstance(data, (AsyncIterator, Iterator)):
        add_header(headers, "Transfer-Encoding", "chunked")
        return data
    else:
        body: BodyType = b""
        content_type = None

        if isinstance(data, (Dict, tuple)):
            body = urlencode(data)
            content_type = "application/x-www-form-urlencoded"
        else:
            body = data
            content_type = "text/plain"

        if "content-type" not in headers:
            add_header(headers, "Content-Type", content_type)

        body = body.encode() if isinstance(body, str) else body
        add_header(headers, "Content-Length", str(len(body)))
        return body
