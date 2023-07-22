from typing import List

from pydantic import BaseModel

from core.domain.entities.country import Country
from shared.presenter import AbstractPresenter


class CountryResponse(BaseModel):
    code: str
    name: str


class CountryPresenter(AbstractPresenter[Country, CountryResponse]):
    result: CountryResponse

    async def present(self, data: Country) -> None:
        self.result = CountryResponse.model_validate(data, from_attributes=True)


class CountryListPresenter(AbstractPresenter[List[Country], List[CountryResponse]]):
    result: List[CountryResponse]

    async def present(self, data: List[Country]) -> None:
        self.result = [CountryResponse.model_validate(item, from_attributes=True) for item in data]
