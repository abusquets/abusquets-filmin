from sqlalchemy.orm import registry

from filmin.domain.schemas.genre import Genre
from filmin.schemas.genre import CreateGenreInDTO, UpdatePartialGenreInDTO

from .ports.genre import AbstractGenreRepository
from infra.database.sqlalchemy.models.filmin.genre import genres
from shared.repository.sqlalchemy import SqlAlchemyRepository


mapper_registry = registry()
mapper_registry.map_imperatively(Genre, genres)


class GenreRepository(
    SqlAlchemyRepository[Genre, CreateGenreInDTO, UpdatePartialGenreInDTO],
    AbstractGenreRepository,
):
    key = 'code'
