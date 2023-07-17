from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter

from core.domain.schemas.country import Country
from core.domain.services.country import CountryService


router = APIRouter(prefix='/country')


def get_country_service() -> CountryService:
    from app.app_container import AppContainer

    return AppContainer().country_service


@router.get(
    '/{code}',
    responses={
        200: {'description': 'Successful Response'},
        404: {'description': 'Country not found'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def get_country(code: str, country_service: CountryService = Depends(get_country_service)) -> Country:
    return await country_service.get_country_by_id(code)


@router.get(
    '',
    responses={200: {'description': 'Successful Response'}},
)
async def list_countries(
    country_service: CountryService = Depends(get_country_service),
) -> List[Country]:
    return await country_service.get_all_countries()
