from typing import List, Optional

from filmin.domain.entities.production_company import ProductionCompany
from filmin.domain.ports.repositories.production_company import AbstractProductionCompanyRepository
from filmin.schemas.production_company import CreateProductionCompanyInDTO, UpdateProductionCompanyInDTO
from shared.api.schemas.page import PageParams


class ProductionCompanyService:
    def __init__(self, production_company_repository: AbstractProductionCompanyRepository):
        self.production_company_repository = production_company_repository

    async def get_production_company_by_id(self, uuid: str) -> ProductionCompany:
        return await self.production_company_repository.get_by_id(uuid)

    async def get_production_companies(self, *, page_params: Optional[PageParams] = None) -> List[ProductionCompany]:
        if page_params is None:
            ret = await self.production_company_repository.get_all()
        else:
            ret = await self.production_company_repository.get_xpage(page_params.page, page_params.size)
        return ret

    async def create_production_company(self, in_data: CreateProductionCompanyInDTO) -> ProductionCompany:
        return await self.production_company_repository.create(in_data)

    async def update_production_company(self, uuid: str, in_data: UpdateProductionCompanyInDTO) -> ProductionCompany:
        return await self.production_company_repository.update(uuid, in_data)
