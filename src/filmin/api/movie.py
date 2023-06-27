from typing import Dict, List, Union

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from filmin.api.schemas.movie import (
    CreateMovieRequestDTO,
    CreateMovieResponseDTO,
    UpdatePartialMovieRequestDTO,
)
from filmin.data.repositories.ports.movie import AbstractMovieRepository
from filmin.domain.schemas.movie import Movie
from filmin.schemas.movie import CreateMovieInDTO, UpdatePartialMovieInDTO

from app.exceptions import EmptyPayloadException
from shared.api.schemas.page import PagedResponseSchema, PageParams


router = APIRouter(prefix='/movie')


def get_movie_repository() -> AbstractMovieRepository:
    from app.app_container import AppContainer

    return AppContainer().movie_repository


@router.get(
    '/{uuid}',
    responses={
        200: {'description': 'Successful Response'},
        404: {'description': 'Movie not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def get_movie(
    uuid: str,
    movie_repository: AbstractMovieRepository = Depends(get_movie_repository),
) -> Movie:
    return await movie_repository.get_by_id(uuid)


@router.get(
    '',
    response_model=PagedResponseSchema[Movie],
    responses={
        200: {'description': 'Successful Response'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def list_movie(
    page_params: PageParams = Depends(),
    movie_repository: AbstractMovieRepository = Depends(get_movie_repository),
) -> Dict[str, Union[int, List[Movie]]]:
    count, items = await movie_repository.get_xpage(**page_params.dict())
    return {
        'total': count,
        'results': items,
        'page': page_params.page,
        'size': page_params.size,
    }


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
    movie_repository: AbstractMovieRepository = Depends(get_movie_repository),
) -> Movie:
    in_dto = CreateMovieInDTO.parse_obj(request_data.dict())
    return await movie_repository.create(in_dto)


# @router.put(
#     '/{uuid}',
#     status_code=204,
#     responses={
#         204: {'description': 'Item updated'},
#         404: {'description': 'Item not found'},
#         422: {'description': 'Unprocessable Entity'},
#     },
# )
# async def update_movie(
#     uuid: str,
#     request_data: UpdateMovieRequestDTO,
#     movie_repository: AbstractMovieRepository = Depends(get_movie_repository),
# ) -> None:
#     in_data = request_data.dict()
#     in_dto = UpdatePartialMovieInDTO.parse_obj(in_data)
#     await movie_repository.update(uuid, in_dto)


@router.patch(
    '/{uuid}',
    status_code=200,
    responses={
        200: {'description': 'Item updated'},
        404: {'description': 'Item not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def update_movie_partially(
    uuid: str,
    request_data: UpdatePartialMovieRequestDTO,
    movie_repository: AbstractMovieRepository = Depends(get_movie_repository),
) -> Movie:
    in_data = request_data.dict(exclude_unset=True)
    if not in_data.keys():
        raise EmptyPayloadException()
    in_dto = UpdatePartialMovieInDTO.parse_obj(in_data)
    return await movie_repository.update(uuid, in_dto)
