from filmin.domain.services.movie import MovieService
from filmin.schemas.movie import CreateMovieInDTO
from shared.api.schemas.page import PageParams
from shared.presenter import AbstractPresenter


class GetMoviesUseCase:
    def __init__(self, presenter: AbstractPresenter, service: MovieService):
        self.presenter = presenter
        self.service = service

    async def execute(self, page_params: PageParams) -> None:
        await self.presenter.present(await self.service.get_movies(page_params=page_params))


class GetMovieUseCase:
    def __init__(self, presenter: AbstractPresenter, service: MovieService):
        self.presenter = presenter
        self.service = service

    async def execute(self, uuid: str) -> None:
        await self.presenter.present(await self.service.get_movie_by_id(uuid))


class CreateMovieUseCase:
    def __init__(self, presenter: AbstractPresenter, service: MovieService):
        self.presenter = presenter
        self.service = service

    async def execute(self, in_dto: CreateMovieInDTO) -> None:
        await self.presenter.present(await self.service.create_movie(in_dto))


class UpdateMovieUseCase:
    def __init__(self, presenter: AbstractPresenter, service: MovieService):
        self.presenter = presenter
        self.service = service

    async def execute(self, uuid: str, in_data: CreateMovieInDTO) -> None:
        await self.presenter.present(await self.service.update_movie(uuid, in_data))
