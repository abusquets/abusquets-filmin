from core.adapters.spi.repositories.country import CountryRepository
from core.domain.ports.repositories.country import AbstractCountryRepository
from infra.database.sqlalchemy.session import AbstractDatabase


class CountryContainerMixin:
    db: AbstractDatabase
    country_repository: AbstractCountryRepository

    def _get_country_repository(self) -> AbstractCountryRepository:
        return CountryRepository(self.db.session)
