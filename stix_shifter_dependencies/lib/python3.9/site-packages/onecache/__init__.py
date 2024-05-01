from collections import OrderedDict
from datetime import datetime, timedelta
from typing import Any, Dict, Optional


class CacheValue:
    """Dummy class for handling cache values."""

    def __init__(self, value: Any, expire_at: datetime = None):
        self.value = value
        self.expire_at = expire_at
        self.access = 0

    def expired(self):
        """Check if value is expired."""
        if self.expire_at:
            return datetime.utcnow() > self.expire_at
        return False  # pragma: no cover

    def refresh_ttl(self, expire_at: datetime):
        self.expire_at = expire_at

    def __eq__(self, otherinstance: "CacheValue"):
        return self.value == otherinstance.value


class ExpirableCache(object):
    """
    Class used for custom cache decorator, dummy expirable cache based
    on dict structure.

    Params:
        * **size (int)**: max items in dict. default=512
        * **timeout (int)**: Timeout in milliseconds, if it is None,
            there is no timeout. default=None
        * **refresh_ttl (int)**: Refresh ttl anytime key is accessed. default=False
    """

    def __init__(self, size=512, timeout=None, refresh_ttl=False):
        self.cache: Dict[str, CacheValue] = OrderedDict()
        self.timeout = timeout
        self.size = size
        self.refresh_ttl = refresh_ttl

    def set(self, key, data):
        if len(self.cache) + 1 > self.size and key not in self.cache:
            self._pop_one()

        if self.timeout:
            expire_at = datetime.utcnow() + timedelta(milliseconds=self.timeout)
            self.cache[key] = CacheValue(data, expire_at)
        else:
            self.cache[key] = CacheValue(data)

    def _pop_one(self):
        self.cache.pop(next(iter(self.cache)))

    def get(self, key):
        self._check_expired(key)
        cache_value = self.cache.get(key)
        if cache_value:
            if self.refresh_ttl:
                self.refresh_key_ttl(key)
            return cache_value.value

    def _check_expired(self, key):
        to_rm = []
        if self.timeout:
            for key, cache_value in self.cache.items():
                if cache_value.expired():
                    to_rm.append(key)
        for key in to_rm:
            self._remove_key(key)

    def _remove_key(self, key):
        del self.cache[key]

    def __contains__(self, key):
        self._check_expired(key)
        return key in self.cache

    def refresh_key_ttl(self, key: Any, milliseconds=None):
        """Do refresh of key ttl, if present."""
        cache_value = self.cache.get(key)
        if cache_value and (milliseconds or self.timeout):
            ms = milliseconds if milliseconds else self.timeout
            expire_at = datetime.utcnow() + timedelta(milliseconds=ms)
            cache_value.refresh_ttl(expire_at)

    @classmethod
    def get_key(cls, *args, **kwargs):
        """Helper method to generate keys from *args, **kwargs."""
        sorted_kwargs = sorted(kwargs.items(), key=lambda item: item[0])
        kwargs_list = [f"{key}={cls.serialize_key(val)}" for key, val in sorted_kwargs]
        items = list(args) + kwargs_list
        return "-".join([cls.serialize_key(item) for item in items])

    @classmethod
    def serialize_key(cls, data: Any):
        if isinstance(data, dict):
            return ",".join(
                [f"{key}={cls.serialize_key(val)}" for key, val in data.items()]
            )
        elif isinstance(data, list):
            return ",".join([cls.serialize_key(val) for val in data])
        elif isinstance(data, str):
            return data
        else:
            return str(data)

    def expire(self, *args, **kwargs):
        """Usefull to expire any combination of *args, **kwargs."""
        key = self.get_key(*args, **kwargs)
        if key in self.cache:
            self._remove_key(key)


class LRUCache(ExpirableCache):
    def get(self, key):
        res = super().get(key)
        if res:
            cache_value = self.cache[key]
            if cache_value:
                self._increment(cache_value)
                return res
        return res

    def _increment(self, val: CacheValue):
        val.access += 1

    def _pop_one(self):
        ordered_cache = sorted(self.cache.items(), key=lambda item: item[1].access)
        del self.cache[ordered_cache[0][0]]

    @property
    def access(self):
        """Get accesses as map."""
        return {key: val.access for key, val in self.cache.items()}


# Decorator!
class CacheDecorator:
    """Decorator for ExpirableCache"""

    def __init__(
        self,
        maxsize=512,
        ttl: Optional[int] = None,
        skip_args: bool = False,
        cache_class=LRUCache,
        refresh_ttl: Optional[bool] = False,
    ):
        """
        Args:
            * **maxsize (int)**: Maximun size of cache. default: 512
            * **ttl (int)**: time to expire in milliseconds, if None, it does not expire. default: None
            * **skip_args (bool)**: apply cache as the function doesn't have any arguments, default: False
            * **cache_class (class)**: Class to use for cache instance. default: LRUCache
            * **refresh_ttl (bool)**: if cache with ttl, This flag makes key expiration timestamp to be
                refresh per access. default: False
        """
        self.cache = cache_class(maxsize, ttl, refresh_ttl=refresh_ttl)
        self.maxsize = maxsize
        self.skip_args = skip_args

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            key = "any" if self.skip_args else self.cache.get_key(*args, **kwargs)

            if key not in self.cache:
                resp = func(*args, **kwargs)
                self.cache.set(key, resp)
                return resp
            else:
                return self.cache.get(key)

        wrapper.cache = self.cache

        return wrapper


class AsyncCacheDecorator(CacheDecorator):
    """Async Decorator for ExpirableCache"""

    def __call__(self, func):
        async def async_wrapper(*args, **kwargs):
            key = "any" if self.skip_args else self.cache.get_key(*args, **kwargs)

            if key not in self.cache:
                resp = await func(*args, **kwargs)
                self.cache.set(key, resp)
                return resp
            else:
                return self.cache.get(key)

        async_wrapper.cache = self.cache

        return async_wrapper
