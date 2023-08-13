from filmin.domain.entities.genre import Genre
from filmin.schemas.genre import CreateGenreInDTO, UpdatePartialGenreInDTO
from shared.repository.ports.generic import AbstractRepository


class AbstractGenreRepository(AbstractRepository[Genre, CreateGenreInDTO, UpdatePartialGenreInDTO]):
    key = 'code'
