from threading import RLock
import time

from typing import Any, Dict, Union

from infra.cache.ports import AbstractCacheRepository, EncodableT


class MemoryCache(AbstractCacheRepository):
    def __init__(self) -> None:
        self._data: Dict[str, tuple[EncodableT, float]] = {}
        self.lock = RLock()

    async def init(self) -> None:
        pass

    async def close(self) -> None:
        with self.lock:
            self._data = {}

    async def get(self, key: str) -> Any:
        with self.lock:
            ret = self._data.get(key)
            if ret is not None:
                if ret[1] < time.time():
                    return ret[0]
                else:
                    self._data.pop(key, None)

    async def set(self, key: str, value: Union[EncodableT, None], expire: int) -> None:
        with self.lock:
            if value is None:
                self._data.pop(key, None)
            else:
                self._data[key] = (value, time.time() + expire)

    async def delete(self, key: str) -> None:
        with self.lock:
            self._data.pop(key, None)
