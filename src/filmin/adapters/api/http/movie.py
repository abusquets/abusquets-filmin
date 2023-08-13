from typing import Annotated
import uuid

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.app_container import AppContainer
from app.exceptions import EmptyPayloadExceptionError
from app.schemas import Session
from app.session_deps import is_admin_session
from filmin.adapters.api.http.presenters.movie import (
    MoviePagedListPresenter,
    MoviePresenter,
)
from filmin.adapters.api.http.schemas.movie import (
    CreateMovieRequestDTO,
    CreateMovieResponseDTO,
    MovieListPagedResponse,
    MovieResponse,
    UpdateMovieRequestDTO,
    UpdatePartialMovieRequestDTO,
)
from filmin.domain.entities.movie import Movie
from filmin.domain.services.movie import MovieService
from filmin.domain.use_cases.movie import (
    CreateMovieUseCase,
    GetMoviesUseCase,
    GetMovieUseCase,
    UpdateMovieUseCase,
)
from filmin.schemas.movie import CreateMovieInDTO, UpdatePartialMovieInDTO
from shared.api.schemas.page import PageParams


router = APIRouter(prefix='/movie')


@router.get(
    '/{uuid}',
    responses={
        200: {'description': 'Successful Response'},
        404: {'description': 'Movie not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def get_movie(
    uuid: Annotated[str, uuid.UUID],
    container: AppContainer = Depends(AppContainer),
) -> MovieResponse:
    service = MovieService(container.movie_repository)
    presenter = MoviePresenter()
    usecase = GetMovieUseCase(presenter, service)
    await usecase.execute(uuid)
    return presenter.result


@router.get(
    '',
    responses={
        200: {'description': 'Successful Response'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def list_movies(
    page_params: PageParams = Depends(),
    container: AppContainer = Depends(AppContainer),
) -> MovieListPagedResponse:
    service = MovieService(container.movie_repository)
    presenter = MoviePagedListPresenter(page_params)
    usecase = GetMoviesUseCase(presenter, service)
    await usecase.execute(page_params)
    return presenter.result


@router.post(
    '',
    response_class=JSONResponse,
    response_model=CreateMovieResponseDTO,
    status_code=201,
    responses={
        201: {'description': 'Item created'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def create_movie(
    request_data: CreateMovieRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> Movie:
    in_dto = CreateMovieInDTO.model_validate(request_data.model_dump())
    service = MovieService(container.movie_repository)
    presenter = MoviePresenter()
    usecase = CreateMovieUseCase(presenter, service)
    await usecase.execute(in_dto)
    return presenter.result


@router.put(
    '/{uuid}',
    responses={
        200: {'description': 'Item updated'},
        404: {'description': 'Item not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def update_movie(
    uuid: Annotated[str, uuid.UUID],
    request_data: UpdateMovieRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> MovieResponse:
    in_data = request_data.model_dump()
    in_dto = UpdatePartialMovieInDTO.model_validate(in_data)
    service = MovieService(container.movie_repository)
    presenter = MoviePresenter()
    usecase = UpdateMovieUseCase(presenter, service)
    await usecase.execute(uuid, in_dto)
    return presenter.result


@router.patch(
    '/{uuid}',
    responses={
        200: {'description': 'Item updated'},
        404: {'description': 'Item not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def update_movie_partially(
    uuid: Annotated[str, uuid.UUID],
    request_data: UpdatePartialMovieRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> MovieResponse:
    in_data = request_data.model_dump(exclude_unset=True)
    if not in_data.keys():
        raise EmptyPayloadExceptionError()
    in_dto = UpdatePartialMovieInDTO.model_validate(in_data)

    service = MovieService(container.movie_repository)
    presenter = MoviePresenter()
    usecase = UpdateMovieUseCase(presenter, service)
    await usecase.execute(uuid, in_dto)
    return presenter.result
