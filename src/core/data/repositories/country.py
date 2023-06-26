from sqlalchemy.orm import registry

from core.data.repositories.ports.country import AbstractCountryRepository
from core.domain.schemas.country import Country
from core.schemas.country.create_country import CreateCountryInDTO
from core.schemas.country.update_country import UpdatePartialCountryInDTO
from infra.database.sqlalchemy.models.core.country import countries
from shared.repository.sqlalchemy import SqlAlchemyRepository


mapper_registry = registry()

mapper_registry.map_imperatively(
    Country,
    countries,
)


class CountryRepository(
    SqlAlchemyRepository[Country, CreateCountryInDTO, UpdatePartialCountryInDTO],
    AbstractCountryRepository,
):
    key = 'code'
