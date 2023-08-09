from typing import List, Optional

from filmin.domain.entities.movie import Movie
from filmin.domain.ports.repositories.movie import AbstractMovieRepository
from filmin.schemas.movie import CreateMovieInDTO, UpdateMovieInDTO
from shared.api.schemas.page import PageParams


class MovieService:
    def __init__(self, movie_repository: AbstractMovieRepository):
        self.movie_repository = movie_repository

    async def get_movie_by_id(self, uuid: str) -> Movie:
        return await self.movie_repository.get_by_id(uuid)

    async def get_movies(self, *, page_params: Optional[PageParams] = None) -> List[Movie]:
        if not page_params:
            ret = await self.movie_repository.get_all()
        else:
            ret = await self.movie_repository.get_xpage(page_params.page, page_params.size)
        return ret

    async def create_movie(self, in_data: CreateMovieInDTO) -> Movie:
        return await self.movie_repository.create(in_data)

    async def update_movie(self, uuid: str, in_data: UpdateMovieInDTO) -> Movie:
        return await self.movie_repository.update(uuid, in_data)
