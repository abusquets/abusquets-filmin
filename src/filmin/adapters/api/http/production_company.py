from typing import Annotated
import uuid

from fastapi import Depends
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.app_container import AppContainer
from app.exceptions import EmptyPayloadExceptionError
from app.schemas import Session
from app.session_deps import check_access_token, is_admin_session
from filmin.adapters.api.http.presenters.production_company import (
    ProductionCompanyPagedListPresenter,
    ProductionCompanyPresenter,
)
from filmin.adapters.api.http.schemas.production_company import (
    CreateProductionCompanyRequestDTO,
    CreateProductionCompanyResponseDTO,
    ProductionCompanyListPagedResponse,
    ProductionCompanyResponse,
    UpdatePartialProductionCompanyRequestDTO,
    UpdateProductionCompanyRequestDTO,
)
from filmin.domain.entities.production_company import ProductionCompany
from filmin.domain.services.production_company import ProductionCompanyService
from filmin.domain.use_cases.production_company import (
    CreateProductionCompanyUseCase,
    GetProductionCompaniesUseCase,
    GetProductionCompanyUseCase,
    UpdateProductionCompanyUseCase,
)
from filmin.schemas.production_company import CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO
from shared.api.schemas.page import PageParams


router = APIRouter(prefix='/production-company')


@router.get(
    '/{uuid}',
    responses={
        200: {'description': 'Successful Response'},
        404: {'description': 'ProductionCompany not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def get_production_company(
    uuid: Annotated[str, uuid.UUID],
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(check_access_token),
) -> ProductionCompanyResponse:
    service = ProductionCompanyService(container.production_company_repository)
    presenter = ProductionCompanyPresenter()
    usecase = GetProductionCompanyUseCase(presenter, service)
    await usecase.execute(uuid)
    return presenter.result


@router.get(
    '',
    responses={
        200: {'description': 'Successful Response'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def list_production_companies(
    page_params: PageParams = Depends(),
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(check_access_token),
) -> ProductionCompanyListPagedResponse:
    service = ProductionCompanyService(container.production_company_repository)
    presenter = ProductionCompanyPagedListPresenter(page_params)
    usecase = GetProductionCompaniesUseCase(presenter, service)
    await usecase.execute(page_params)
    return presenter.result


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
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> ProductionCompany:
    in_dto = CreateProductionCompanyInDTO.model_validate(request_data.model_dump())
    service = ProductionCompanyService(container.production_company_repository)
    presenter = ProductionCompanyPresenter()
    usecase = CreateProductionCompanyUseCase(presenter, service)
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
async def update_production_company(
    uuid: Annotated[str, uuid.UUID],
    request_data: UpdateProductionCompanyRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> ProductionCompanyResponse:
    in_data = request_data.model_dump()
    in_dto = UpdatePartialProductionCompanyInDTO.model_validate(in_data)
    service = ProductionCompanyService(container.production_company_repository)
    presenter = ProductionCompanyPresenter()
    usecase = UpdateProductionCompanyUseCase(presenter, service)
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
async def update_production_company_partially(
    uuid: Annotated[str, uuid.UUID],
    request_data: UpdatePartialProductionCompanyRequestDTO,
    container: AppContainer = Depends(AppContainer),
    _: Session = Depends(is_admin_session),
) -> ProductionCompanyResponse:
    in_data = request_data.model_dump(exclude_unset=True)
    if not in_data.keys():
        raise EmptyPayloadExceptionError()
    in_dto = UpdatePartialProductionCompanyInDTO.model_validate(in_data)

    service = ProductionCompanyService(container.production_company_repository)
    presenter = ProductionCompanyPresenter()
    usecase = UpdateProductionCompanyUseCase(presenter, service)
    await usecase.execute(uuid, in_dto)
    return presenter.result
