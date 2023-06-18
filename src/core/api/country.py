from typing import List

from fastapi import Depends
from fastapi.routing import APIRouter

from core.data.repositories.ports.country import AbstractCountryRepository
from core.domain.schemas.country import Country


router = APIRouter(prefix='/country')


def create_country_repository() -> AbstractCountryRepository:
    from app.app_container import AppContainer

    return AppContainer().country_repository


@router.get('/{code}')
async def get_country(
    code: str, country_repository: AbstractCountryRepository = Depends(create_country_repository)
) -> Country:
    return await country_repository.get_by_id(code)


@router.get('')
async def list_countries(
    country_repository: AbstractCountryRepository = Depends(create_country_repository),
) -> List[Country]:
    return await country_repository.get_all()
