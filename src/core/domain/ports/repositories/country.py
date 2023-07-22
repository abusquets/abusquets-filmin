from core.domain.dtos.country.create_country import CreateCountryInDTO
from core.domain.dtos.country.update_country import UpdatePartialCountryInDTO
from core.domain.entities.country import Country
from shared.repository.ports.generic import AbstractRepository


class AbstractCountryRepository(AbstractRepository[Country, CreateCountryInDTO, UpdatePartialCountryInDTO]):
    pass
