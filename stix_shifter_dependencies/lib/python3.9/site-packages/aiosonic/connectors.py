"""Connector stuffs."""
import random
from asyncio import sleep as asyncio_sleep
from asyncio import wait_for
from typing import TYPE_CHECKING, Coroutine
from urllib.parse import ParseResult

# import h2.connection (unused)
from onecache import ExpirableCache

# from concurrent import futures (unused)
from aiosonic.exceptions import (
    ConnectionPoolAcquireTimeout,
    ConnectTimeout,
    HttpParsingError,
    TimeoutException,
)
from aiosonic.pools import SmartPool
from aiosonic.resolver import DefaultResolver
from aiosonic.timeout import Timeouts

if TYPE_CHECKING:
    from aiosonic.connection import Connection


class TCPConnector:
    """TCPConnector.

    Holds the main logic for making connections to destination hosts.

    Params:
        * **pool_size**: size for pool of connections
        * **timeouts**: global timeouts to use for connections with this connector. default: :class:`aiosonic.timeout.Timeouts` instance with default args.
        * **connection_cls**: connection class to be used. default: :class:`aiosonic.connection.Connection`
        * **pool_cls**: pool class to be used. default: :class:`aiosonic.pools.SmartPool`
        * **resolver**: resolver to be used. default: :class:`aiosonic.resolver.DefaultResolver`
        * **ttl_dns_cache**: ttl in milliseconds for dns cache. default: `10000` 10 seconds
        * **use_dns_cache**: Flag to indicate usage of dns cache. default: `True`

    """

    def __init__(
        self,
        pool_size: int = 25,
        timeouts: Timeouts = None,
        connection_cls=None,
        pool_cls=None,
        resolver=None,
        ttl_dns_cache=10000,
        use_dns_cache=True,
    ):
        from aiosonic.connection import Connection  # avoid circular dependency

        self.pool_size = pool_size
        connection_cls = connection_cls or Connection
        pool_cls = pool_cls or SmartPool
        self.pool = pool_cls(self, pool_size, connection_cls)
        self.timeouts = timeouts or Timeouts()
        self.resolver = resolver or DefaultResolver()
        self.use_dns_cache = use_dns_cache
        if self.use_dns_cache:
            self.cache = ExpirableCache(512, ttl_dns_cache)

    async def acquire(
        self, urlparsed: ParseResult, verify, ssl, timeouts, http2
    ) -> "Connection":
        """Acquire connection."""
        if not urlparsed.hostname:
            raise HttpParsingError("missing hostname")

        # Faster without timeout
        if not self.timeouts.pool_acquire:
            conn = await self.pool.acquire(urlparsed)
            return await self.after_acquire(
                urlparsed, conn, verify, ssl, timeouts, http2
            )

        try:
            conn = await wait_for(
                self.pool.acquire(urlparsed), self.timeouts.pool_acquire
            )
            return await self.after_acquire(
                urlparsed, conn, verify, ssl, timeouts, http2
            )
        except TimeoutException:
            raise ConnectionPoolAcquireTimeout()

    async def after_acquire(self, urlparsed, conn, verify, ssl, timeouts, http2):
        dns_info = await self.__resolve_dns(urlparsed.hostname, urlparsed.port)

        try:
            await wait_for(
                conn.connect(urlparsed, dns_info, verify, ssl, http2),
                timeout=timeouts.sock_connect,
            )
        except TimeoutException:
            raise ConnectTimeout()
        return conn

    async def release(self, conn):
        """Release connection."""
        res = self.pool.release(conn)
        if isinstance(res, Coroutine):
            await res

    async def wait_free_pool(self):
        """Wait until free pool."""
        while True:
            if self.pool.is_all_free():
                return True
            asyncio_sleep(0.02)  # pragma: no cover

    async def cleanup(self):
        """Cleanup connector connections."""
        await self.pool.cleanup()

    async def __resolve_dns(self, host: str, port: int):
        key = f"{host}-{port}"
        dns_data = self.cache.get(key)
        if not dns_data:
            dns_data = await self.resolver.resolve(host, port)
            self.cache.set(key, dns_data)
        return random.choice(dns_data)
