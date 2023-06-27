from filmin.data.repositories.ports.genre import AbstractGenreRepository

from infra.database.sqlalchemy.session import AbstractDatabase


class GenreContainerMixin:
    db: AbstractDatabase
    genre_repository: AbstractGenreRepository

    def _get_genre_repository(self) -> AbstractGenreRepository:
        from filmin.data.repositories.genre import GenreRepository

        return GenreRepository(self.db.session)
