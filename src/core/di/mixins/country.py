from core.data.repositories.ports.country import AbstractCountryRepository
from core.domain.services.country import CountryService
from infra.database.sqlalchemy.session import AbstractDatabase


class CountryContainerMixin:
    db: AbstractDatabase
    country_repository: AbstractCountryRepository
    country_service: CountryService

    def _get_country_repository(self) -> AbstractCountryRepository:
        from core.data.repositories.country import CountryRepository

        return CountryRepository(self.db.session)

    def _get_country_service(self) -> CountryService:
        return CountryService(self.country_repository)
