from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter

from app.app_container import AppContainer
from core.adapters.api.http.country_presenter import CountryListPresenter, CountryPresenter, CountryResponse
from core.domain.services.country import CountryService
from core.domain.use_cases.country import GetAllCountriesUseCase, GetCountryUseCase


router = APIRouter(prefix='/country')


@router.get(
    '/{code}',
    responses={
        200: {'description': 'Successful Response'},
        404: {'description': 'Country not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def get_country(code: str, container: AppContainer = Depends(AppContainer)) -> CountryResponse:
    service = CountryService(container.country_repository)
    presenter = CountryPresenter()
    usecase = GetCountryUseCase(presenter, service)
    await usecase.execute(code)
    return presenter.result


@router.get(
    '',
    responses={200: {'description': 'Successful Response'}},
)
async def list_countries(
    container: AppContainer = Depends(AppContainer),
) -> List[CountryResponse]:
    service = CountryService(container.country_repository)
    presenter = CountryListPresenter()
    usecase = GetAllCountriesUseCase(presenter, service)
    await usecase.execute()
    return presenter.result
