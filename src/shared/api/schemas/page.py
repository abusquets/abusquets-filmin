from enum import IntEnum
from typing import Generic, List, Type, TypeVar

from pydantic import BaseModel, ConstrainedInt, conint
from pydantic.generics import GenericModel


class PageSize(IntEnum):
    x100 = 100
    x250 = 250
    x500 = 500
    x1000 = 1000


PageType: ConstrainedInt = conint(ge=1)

class PageParams(BaseModel):
    page: PageType = 1
    size: PageSize = PageSize.x500

    class Config:
        use_enum_values = True


T = TypeVar('T')


class PagedResponseSchema(GenericModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]
