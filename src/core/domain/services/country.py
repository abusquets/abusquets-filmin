from typing import List

from core.data.repositories.ports.country import AbstractCountryRepository
from core.domain.schemas.country import Country


class CountryService:
    def __init__(self, country_repository: AbstractCountryRepository):
        self.country_repository = country_repository

    async def get_country_by_id(self, uuid: str) -> Country:
        return await self.country_repository.get_by_id(uuid)

    async def get_all_countries(self) -> List[Country]:
        return await self.country_repository.get_all()
