from sqlalchemy.orm import registry

from .ports.genre import AbstractGenreRepository
from filmin.domain.schemas.genre import Genre
from filmin.infra.database.sqlalchemy.models.genre import genres
from filmin.schemas.genre import CreateGenreInDTO, UpdatePartialGenreInDTO
from shared.repository.sqlalchemy import SqlAlchemyRepository


mapper_registry = registry()
mapper_registry.map_imperatively(Genre, genres)


class GenreRepository(
    SqlAlchemyRepository[Genre, CreateGenreInDTO, UpdatePartialGenreInDTO],
    AbstractGenreRepository,
):
    key = 'code'
