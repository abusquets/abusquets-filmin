from typing import List

from filmin.adapters.api.http.schemas.genre import GenreListPagedResponse, GenreResponse
from filmin.domain.entities.genre import Genre
from shared.api.schemas.page import PageParams
from shared.presenter import AbstractPresenter


class GenrePresenter(AbstractPresenter[Genre, GenreResponse]):
    result: GenreResponse

    async def present(self, data: Genre) -> None:
        self.result = GenreResponse.model_validate(data, from_attributes=True)


class GenrePagedListPresenter(AbstractPresenter[List[Genre], List[GenreResponse]]):
    result: GenreListPagedResponse

    def __init__(self, page_params: PageParams) -> None:
        self.page_params = page_params

    async def present(self, data: List[Genre]) -> None:
        list_items = [GenreResponse.model_validate(item, from_attributes=True) for item in data]
        self.result = GenreListPagedResponse(
            results=list_items,
            total=len(list_items),
            page=self.page_params.page,
            size=self.page_params.size,
        )
