from core.domain.schemas.country import Country
from core.schemas.country.create_country import CreateCountryInDTO
from core.schemas.country.update_country import UpdatePartialCountryInDTO
from shared.repository.ports.generic import AbstractRepository


class AbstractCountryRepository(AbstractRepository[Country, CreateCountryInDTO, UpdatePartialCountryInDTO]):
    pass
