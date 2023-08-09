from sqlalchemy.orm import registry

from core.domain.dtos.country.create_country import CreateCountryInDTO
from core.domain.dtos.country.update_country import UpdatePartialCountryInDTO
from core.domain.entities.country import Country
from core.domain.ports.repositories.country import AbstractCountryRepository
from core.infra.database.sqlalchemy.models.country import countries
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
