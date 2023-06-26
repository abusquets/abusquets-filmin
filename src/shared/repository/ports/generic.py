import abc
import datetime

from decimal import Decimal
from typing import Dict, Generic, List, Optional, Tuple, TypeVar, Union

from pydantic import BaseModel


EntityT = TypeVar('EntityT')
CreateT = TypeVar('CreateT', bound=BaseModel)
UpdateT = TypeVar('UpdateT', bound=BaseModel)

FilterBy = Dict[str, Optional[Union[int, Decimal, str, datetime.date, datetime.datetime, bool]]]


class AbstractRepository(Generic[EntityT, CreateT, UpdateT], abc.ABC):
    @abc.abstractmethod
    async def get_by_id(self, uuid: str) -> EntityT:
        ...

    @abc.abstractmethod
    async def get_all(self) -> List[EntityT]:
        ...

    @abc.abstractmethod
    async def get_xpage(self, page: int, size: int) -> Tuple[int, List[EntityT]]:
        ...

    @abc.abstractmethod
    async def filter(self, by: FilterBy) -> List[EntityT]:
        ...

    @abc.abstractmethod
    async def create(self, data: CreateT) -> EntityT:
        ...

    @abc.abstractmethod
    async def update(self, uuid: str, data: UpdateT) -> EntityT:
        ...
