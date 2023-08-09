from sqlalchemy.orm import registry

from filmin.domain.entities.genre import Genre
from filmin.domain.ports.repositories.genre import AbstractGenreRepository
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
