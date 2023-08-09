from filmin.adapters.spi.repositories.genre import GenreRepository
from filmin.domain.ports.repositories.genre import AbstractGenreRepository
from infra.database.sqlalchemy.session import AbstractDatabase


class GenreContainerMixin:
    db: AbstractDatabase
    genre_repository: AbstractGenreRepository

    def _get_genre_repository(self) -> AbstractGenreRepository:
        return GenreRepository(self.db.session)
