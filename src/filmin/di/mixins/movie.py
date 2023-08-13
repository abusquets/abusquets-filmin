from filmin.adapters.spi.repositories.movie import MovieRepository
from filmin.domain.ports.repositories.genre import AbstractGenreRepository
from filmin.domain.ports.repositories.movie import AbstractMovieRepository
from infra.database.sqlalchemy.session import AbstractDatabase


class MovieContainerMixin:
    db: AbstractDatabase
    genre_repository: AbstractGenreRepository
    movie_repository: AbstractMovieRepository

    def _get_movie_repository(self) -> AbstractMovieRepository:
        return MovieRepository(self.db.session, genre_repository=self.genre_repository)
