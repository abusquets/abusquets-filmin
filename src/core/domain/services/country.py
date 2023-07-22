from typing import List

from core.domain.entities.country import Country
from core.domain.entities.value_objects import CountryId
from core.domain.ports.repositories.country import AbstractCountryRepository


class CountryService:
    def __init__(self, country_repository: AbstractCountryRepository):
        self.country_repository = country_repository

    async def get_country_by_id(self, uuid: CountryId) -> Country:
        return await self.country_repository.get_by_id(uuid)

    async def get_all_countries(self) -> List[Country]:
        return await self.country_repository.get_all()
