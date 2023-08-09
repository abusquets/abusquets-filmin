from typing import List, Optional

from filmin.domain.entities.genre import Genre
from filmin.domain.ports.repositories.genre import AbstractGenreRepository
from filmin.schemas.genre import CreateGenreInDTO, UpdateGenreInDTO
from shared.api.schemas.page import PageParams


class GenreService:
    def __init__(self, genre_repository: AbstractGenreRepository):
        self.genre_repository = genre_repository

    async def get_genre_by_id(self, code: str) -> Genre:
        return await self.genre_repository.get_by_id(code)

    async def get_genres(self, *, page_params: Optional[PageParams] = None) -> List[Genre]:
        if not page_params:
            ret = await self.genre_repository.get_all()
        else:
            ret = await self.genre_repository.get_xpage(page_params.page, page_params.size)
        return ret

    async def create_genre(self, in_dto: CreateGenreInDTO) -> Genre:
        return await self.genre_repository.create(in_dto)

    async def update_genre(self, code: str, in_dto: UpdateGenreInDTO) -> Genre:
        return await self.genre_repository.update(code, in_dto)
