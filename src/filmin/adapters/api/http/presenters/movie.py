from typing import List

from filmin.adapters.api.http.schemas.movie import (
    MovieListPagedResponse,
    MovieResponse,
)
from filmin.domain.entities.movie import Movie
from shared.api.schemas.page import PageParams
from shared.presenter import AbstractPresenter


class MoviePresenter(AbstractPresenter[Movie, MovieResponse]):
    result: MovieResponse

    async def present(self, data: Movie) -> None:
        self.result = MovieResponse.model_validate(data, from_attributes=True)


class MoviePagedListPresenter(AbstractPresenter[List[Movie], List[MovieResponse]]):
    result: MovieListPagedResponse

    def __init__(self, page_params: PageParams) -> None:
        self.page_params = page_params

    async def present(self, data: List[Movie]) -> None:
        list_items = [MovieResponse.model_validate(item, from_attributes=True) for item in data]
        self.result = MovieListPagedResponse(
            results=list_items,
            total=len(list_items),
            page=self.page_params.page,
            size=self.page_params.size,
        )
