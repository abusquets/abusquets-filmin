from filmin.data.repositories.ports.genre import AbstractGenreRepository
from filmin.data.repositories.ports.movie import AbstractMovieRepository

from infra.database.sqlalchemy.session import AbstractDatabase


class MovieContainerMixin:
    db: AbstractDatabase
    genre_repository: AbstractGenreRepository
    movie_repository: AbstractMovieRepository

    def _get_movie_repository(self) -> AbstractMovieRepository:
        from filmin.data.repositories.movie import MovieRepository

        return MovieRepository(self.db.session, genre_repository=self.genre_repository)
