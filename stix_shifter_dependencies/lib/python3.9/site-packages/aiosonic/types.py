from typing import AsyncIterator, Dict, Iterator, Sequence, Tuple, Union

# TYPES
ParamsType = Union[
    Dict[str, str],
    Sequence[Tuple[str, str]],
]
#: Data to be sent in requests, allowed types
DataType = Union[
    str,
    bytes,
    dict,
    tuple,
    AsyncIterator[bytes],
    Iterator[bytes],
]
BodyType = Union[
    str,
    bytes,
    AsyncIterator[bytes],
    Iterator[bytes],
]
ParsedBodyType = Union[
    bytes,
    AsyncIterator[bytes],
    Iterator[bytes],
]
