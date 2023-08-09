from filmin.domain.schemas.movie import Movie
from filmin.schemas.movie import CreateMovieInDTO, UpdatePartialMovieInDTO
from shared.repository.ports.generic import AbstractRepository


class AbstractMovieRepository(AbstractRepository[Movie, CreateMovieInDTO, UpdatePartialMovieInDTO]):
    pass
