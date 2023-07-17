import abc

from typing import Any, Union


EncodableT = Union[str, int, float, bytes]


class AbstractCacheRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, key: str) -> Any:
        ...

    @abc.abstractmethod
    async def set(self, key: str, value: Union[EncodableT, None], expire: int) -> None:
        ...

    @abc.abstractmethod
    async def delete(self, key: str) -> None:
        ...

    @abc.abstractmethod
    async def init(self) -> None:
        ...

    @abc.abstractmethod
    async def close(self) -> None:
        ...
