from typing import Dict, List, Union

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from filmin.api.schemas.production_company import (
    CreateProductionCompanyRequestDTO,
    CreateProductionCompanyResponseDTO,
    UpdatePartialProductionCompanyRequestDTO,
    UpdateProductionCompanyRequestDTO,
)
from filmin.data.repositories.ports.production_company import AbstractProductionCompanyRepository
from filmin.domain.schemas.production_company import ProductionCompany
from filmin.schemas.production_company import CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO

from app.exceptions import EmptyPayloadException
from shared.api.schemas.page import PagedResponseSchema, PageParams


router = APIRouter(prefix='/production-company')


def get_production_company_repository() -> AbstractProductionCompanyRepository:
    from app.app_container import AppContainer

    return AppContainer().production_company_repository


@router.get(
    '/{uuid}',
    responses={
        200: {'description': 'Successful Response'},
        404: {'description': 'Production Company not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def get_production_company(
    uuid: str,
    production_company_repository: AbstractProductionCompanyRepository = Depends(get_production_company_repository),
) -> ProductionCompany:
    return await production_company_repository.get_by_id(uuid)


@router.get(
    '',
    response_model=PagedResponseSchema[ProductionCompany],
    responses={
        200: {'description': 'Successful Response'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def list_production_company(
    page_params: PageParams = Depends(),
    production_company_repository: AbstractProductionCompanyRepository = Depends(get_production_company_repository),
) -> Dict[str, Union[int, List[ProductionCompany]]]:
    count, items = await production_company_repository.get_xpage(**page_params.dict())
    return {
        'total': count,
        'results': items,
        'page': page_params.page,
        'size': page_params.size,
    }


@router.post(
    '',
    response_class=JSONResponse,
    response_model=CreateProductionCompanyResponseDTO,
    status_code=201,
    responses={
        201: {'description': 'Item created'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def create_production_company(
    request_data: CreateProductionCompanyRequestDTO,
    production_company_repository: AbstractProductionCompanyRepository = Depends(get_production_company_repository),
) -> ProductionCompany:
    in_dto = CreateProductionCompanyInDTO.parse_obj(request_data.dict())
    return await production_company_repository.create(in_dto)


@router.put(
    '/{uuid}',
    responses={
        200: {'description': 'Item updated'},
        404: {'description': 'Item not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def update_production_company(
    uuid: str,
    request_data: UpdateProductionCompanyRequestDTO,
    production_company_repository: AbstractProductionCompanyRepository = Depends(get_production_company_repository),
) -> ProductionCompany:
    in_data = request_data.dict()
    in_dto = UpdatePartialProductionCompanyInDTO.parse_obj(in_data)
    return await production_company_repository.update(uuid, in_dto)


@router.patch(
    '/{uuid}',
    responses={
        200: {'description': 'Item updated'},
        404: {'description': 'Item not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def update_production_company_partially(
    uuid: str,
    request_data: UpdatePartialProductionCompanyRequestDTO,
    production_company_repository: AbstractProductionCompanyRepository = Depends(get_production_company_repository),
) -> ProductionCompany:
    in_data = request_data.dict(exclude_unset=True)
    if not in_data.keys():
        raise EmptyPayloadException()
    in_dto = UpdatePartialProductionCompanyInDTO.parse_obj(in_data)
    return await production_company_repository.update(uuid, in_dto)
