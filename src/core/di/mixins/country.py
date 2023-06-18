from core.data.repositories.ports.country import AbstractCountryRepository
from infra.database.sqlalchemy.session import AbstractDatabase


class CountryRepositoryContainerMixin:
    db: AbstractDatabase
    country_repository: AbstractCountryRepository

    def _get_country_repository(self) -> AbstractCountryRepository:
        from core.data.repositories.country import CountryRepository

        return CountryRepository(self.db.session)
