from typing import Dict, List, Union

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from filmin.api.schemas.genre import (
    CreateGenreRequestDTO,
    CreateGenreResponseDTO,
    UpdateGenreRequestDTO,
    UpdatePartialGenreRequestDTO,
)
from filmin.data.repositories.ports.genre import AbstractGenreRepository
from filmin.domain.schemas.genre import Genre
from filmin.schemas.genre import CreateGenreInDTO, UpdatePartialGenreInDTO

from app.exceptions import EmptyPayloadException
from app.schemas import Session
from app.session_deps import check_access_token, is_admin_session
from shared.api.schemas.page import PagedResponseSchema, PageParams


router = APIRouter(prefix='/genre')


def get_genre_repository() -> AbstractGenreRepository:
    from app.app_container import AppContainer

    return AppContainer().genre_repository


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
    genre_repository: AbstractGenreRepository = Depends(get_genre_repository),
    _: Session = Depends(check_access_token),
) -> Genre:
    return await genre_repository.get_by_id(code)


@router.get(
    '',
    response_model=PagedResponseSchema[Genre],
    responses={
        200: {'description': 'Successful Response'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def list_genre(
    page_params: PageParams = Depends(),
    genre_repository: AbstractGenreRepository = Depends(get_genre_repository),
    _: Session = Depends(check_access_token),
) -> Dict[str, Union[int, List[Genre]]]:
    count, items = await genre_repository.get_xpage(**page_params.dict())
    return {
        'total': count,
        'results': items,
        'page': page_params.page,
        'size': page_params.size,
    }


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
    genre_repository: AbstractGenreRepository = Depends(get_genre_repository),
    _: Session = Depends(is_admin_session),
) -> Genre:
    in_dto = CreateGenreInDTO.parse_obj(request_data.dict())
    return await genre_repository.create(in_dto)


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
    genre_repository: AbstractGenreRepository = Depends(get_genre_repository),
    _: Session = Depends(is_admin_session),
) -> Genre:
    in_data = request_data.dict()
    in_dto = UpdatePartialGenreInDTO.parse_obj(in_data)
    return await genre_repository.update(code, in_dto)


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
    genre_repository: AbstractGenreRepository = Depends(get_genre_repository),
    _: Session = Depends(is_admin_session),
) -> Genre:
    in_data = request_data.dict(exclude_unset=True)
    if not in_data.keys():
        raise EmptyPayloadException()
    in_dto = UpdatePartialGenreInDTO.parse_obj(in_data)
    return await genre_repository.update(code, in_dto)
