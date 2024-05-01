# copied from aiohttp

import asyncio
import socket
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type, Union

__all__ = ("ThreadedResolver", "AsyncResolver", "DefaultResolver")

try:
    import aiodns

    # aiodns_default = hasattr(aiodns.DNSResolver, 'gethostbyname')
except ImportError:  # pragma: no cover
    aiodns = None

aiodns_default = False


def get_loop():
    return asyncio.get_running_loop()


class AbstractResolver(ABC):
    """Abstract DNS resolver."""

    @abstractmethod
    async def resolve(
        self, host: str, port: int, family: int
    ) -> List[Dict[str, Any]]:
        """Return IP address for given hostname"""

    @abstractmethod
    async def close(self) -> None:
        """Release resolver"""


class ThreadedResolver(AbstractResolver):
    """Use Executor for synchronous getaddrinfo() calls, which defaults to
    concurrent.futures.ThreadPoolExecutor.
    """

    def __init__(self) -> None:
        self._loop = None

    @property
    def loop(self):
        if not self._loop:
            self._loop = get_loop()
        return self._loop

    async def resolve(
        self, hostname: str, port: int = 0, family: int = socket.AF_INET
    ) -> List[Dict[str, Any]]:
        infos = await self.loop.getaddrinfo(
            hostname,
            port,
            type=socket.SOCK_STREAM,
            family=family,
            flags=socket.AI_ADDRCONFIG,
        )

        hosts = []
        for family, _, proto, _, address in infos:
            if family == socket.AF_INET6 and address[3]:  # type: ignore[misc]
                # This is essential for link-local IPv6 addresses.
                # LL IPv6 is a VERY rare case. Strictly speaking, we should use
                # getnameinfo() unconditionally, but performance makes sense.
                host, _port = socket.getnameinfo(
                    address, socket.NI_NUMERICHOST | socket.NI_NUMERICSERV
                )
                port = int(_port)
            else:
                host, port = address[:2]
            hosts.append(
                {
                    "hostname": hostname,
                    "host": host,
                    "port": port,
                    "family": family,
                    "proto": proto,
                    "flags": socket.AI_NUMERICHOST | socket.AI_NUMERICSERV,
                }
            )

        return hosts

    async def close(self) -> None:
        pass


class AsyncResolver(AbstractResolver):
    """Use the `aiodns` package to make asynchronous DNS lookups"""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        if aiodns is None:
            raise RuntimeError("Resolver requires aiodns library")

        self._loop = get_loop()
        self._resolver = aiodns.DNSResolver(*args, loop=self._loop, **kwargs)

    async def resolve(
        self, host: str, port: int = 0, family: int = socket.AF_INET
    ) -> List[Dict[str, Any]]:
        try:
            resp = await self._resolver.gethostbyname(host, family)
        except aiodns.error.DNSError as exc:
            msg = exc.args[1] if len(exc.args) >= 1 else "DNS lookup failed"
            raise OSError(msg) from exc
        hosts = []
        for address in resp.addresses:
            hosts.append(
                {
                    "hostname": host,
                    "host": address,
                    "port": port,
                    "family": family,
                    "proto": 0,
                    "flags": socket.AI_NUMERICHOST | socket.AI_NUMERICSERV,
                }
            )

        if not hosts:
            raise OSError("DNS lookup failed")

        return hosts

    async def close(self) -> None:
        self._resolver.cancel()


_DefaultType = Type[Union[AsyncResolver, ThreadedResolver]]
DefaultResolver: _DefaultType = (
    AsyncResolver if aiodns_default else ThreadedResolver
)
