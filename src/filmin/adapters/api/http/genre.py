from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.app_container import AppContainer
from app.exceptions import EmptyPayloadExceptionError
from app.schemas import Session
from app.session_deps import check_access_token, is_admin_session
from filmin.adapters.api.http.presenters.genre import GenrePagedListPresenter, GenrePresenter
from filmin.adapters.api.http.schemas.genre import (
    CreateGenreRequestDTO,
    CreateGenreResponseDTO,
    GenreListPagedResponse,
    GenreResponse,
    UpdateGenreRequestDTO,
    UpdatePartialGenreRequestDTO,
)
from filmin.domain.entities.genre import Genre
from filmin.domain.services.genre import GenreService
from filmin.domain.use_cases.genre import CreateGenreUseCase, GetGenresUseCase, GetGenreUseCase, UpdateGenreUseCase
from filmin.schemas.genre import CreateGenreInDTO, UpdatePartialGenreInDTO
from shared.api.schemas.page import PageParams


router = APIRouter(prefix='/genre')


@router.get(
    '/{code}',
    responses={
        200: {'description': 'Successful Response'},
        404: {'description': 'Genre not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def get_genre(
    code: str,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(check_access_token),
) -> GenreResponse:
    service = GenreService(container.genre_repository)
    presenter = GenrePresenter()
    usecase = GetGenreUseCase(presenter, service)
    await usecase.execute(code)
    return presenter.result


@router.get(
    '',
    responses={
        200: {'description': 'Successful Response'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def list_genres(
    page_params: PageParams = Depends(),
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(check_access_token),
) -> GenreListPagedResponse:
    service = GenreService(container.genre_repository)
    presenter = GenrePagedListPresenter(page_params)
    usecase = GetGenresUseCase(presenter, service)
    await usecase.execute(page_params)
    return presenter.result


@router.post(
    '',
    response_class=JSONResponse,
    response_model=CreateGenreResponseDTO,
    status_code=201,
    responses={
        201: {'description': 'Item created'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def create_genre(
    request_data: CreateGenreRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> Genre:
    in_dto = CreateGenreInDTO.model_validate(request_data.model_dump())
    service = GenreService(container.genre_repository)
    presenter = GenrePresenter()
    usecase = CreateGenreUseCase(presenter, service)
    await usecase.execute(in_dto)
    return presenter.result


@router.put(
    '/{code}',
    responses={
        200: {'description': 'Item updated'},
        404: {'description': 'Item not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def update_genre(
    code: str,
    request_data: UpdateGenreRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> GenreResponse:
    in_data = request_data.model_dump()
    in_dto = UpdatePartialGenreInDTO.model_validate(in_data)
    service = GenreService(container.genre_repository)
    presenter = GenrePresenter()
    usecase = UpdateGenreUseCase(presenter, service)
    await usecase.execute(code, in_dto)
    return presenter.result


@router.patch(
    '/{code}',
    responses={
        200: {'description': 'Item updated'},
        404: {'description': 'Item not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def update_genre_partially(
    code: str,
    request_data: UpdatePartialGenreRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> GenreResponse:
    in_data = request_data.model_dump(exclude_unset=True)
    if not in_data.keys():
        raise EmptyPayloadExceptionError()
    in_dto = UpdatePartialGenreInDTO.model_validate(in_data)

    service = GenreService(container.genre_repository)
    presenter = GenrePresenter()
    usecase = UpdateGenreUseCase(presenter, service)
    await usecase.execute(code, in_dto)
    return presenter.result
