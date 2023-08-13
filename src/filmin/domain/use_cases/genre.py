from filmin.domain.services.genre import GenreService
from filmin.schemas.genre import CreateGenreInDTO
from shared.api.schemas.page import PageParams
from shared.presenter import AbstractPresenter


class GetGenresUseCase:
    def __init__(self, presenter: AbstractPresenter, service: GenreService):
        self.presenter = presenter
        self.service = service

    async def execute(self, page_params: PageParams) -> None:
        await self.presenter.present(await self.service.get_genres(page_params=page_params))


class GetGenreUseCase:
    def __init__(self, presenter: AbstractPresenter, service: GenreService):
        self.presenter = presenter
        self.service = service

    async def execute(self, code: str) -> None:
        await self.presenter.present(await self.service.get_genre_by_id(code))


class CreateGenreUseCase:
    def __init__(self, presenter: AbstractPresenter, service: GenreService):
        self.presenter = presenter
        self.service = service

    async def execute(self, in_dto: CreateGenreInDTO) -> None:
        await self.presenter.present(await self.service.create_genre(in_dto))


class UpdateGenreUseCase:
    def __init__(self, presenter: AbstractPresenter, service: GenreService):
        self.presenter = presenter
        self.service = service

    async def execute(self, code: str, in_data: CreateGenreInDTO) -> None:
        await self.presenter.present(await self.service.update_genre(code, in_data))
