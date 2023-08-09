from core.domain.entities.value_objects import CountryId
from core.domain.services.country import CountryService
from shared.presenter import AbstractPresenter


class GetAllCountriesUseCase:
    def __init__(self, presenter: AbstractPresenter, service: CountryService):
        self.presenter = presenter
        self.service = service

    async def execute(self) -> None:
        await self.presenter.present(await self.service.get_all_countries())


class GetCountryUseCase:
    def __init__(self, presenter: AbstractPresenter, service: CountryService):
        self.presenter = presenter
        self.service = service

    async def execute(self, country_id: CountryId) -> None:
        await self.presenter.present(await self.service.get_country_by_id(country_id))
