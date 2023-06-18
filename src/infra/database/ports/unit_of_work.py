import abc

from types import TracebackType
from typing import Any, Callable, Coroutine, Optional, Self, Type


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def __aenter__(self) -> Self:
        ...

    @abc.abstractmethod
    async def __aexit__(
        self, exc_type: Optional[Type[BaseException]], exc: Optional[BaseException], tb: Optional[TracebackType]
    ) -> None:
        ...

    @abc.abstractmethod
    async def commit(self) -> None:
        ...

    @abc.abstractmethod
    async def rollback(self) -> None:
        ...

    @abc.abstractmethod
    def run_after_commit(self, fn: Callable[..., Coroutine[Any, Any, Any]]) -> None:
        ...
