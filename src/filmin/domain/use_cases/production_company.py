from filmin.domain.services.production_company import ProductionCompanyService
from filmin.schemas.production_company import CreateProductionCompanyInDTO
from shared.api.schemas.page import PageParams
from shared.presenter import AbstractPresenter


class GetProductionCompaniesUseCase:
    def __init__(self, presenter: AbstractPresenter, service: ProductionCompanyService):
        self.presenter = presenter
        self.service = service

    async def execute(self, page_params: PageParams) -> None:
        await self.presenter.present(await self.service.get_production_companies(page_params=page_params))


class GetProductionCompanyUseCase:
    def __init__(self, presenter: AbstractPresenter, service: ProductionCompanyService):
        self.presenter = presenter
        self.service = service

    async def execute(self, uuid: str) -> None:
        await self.presenter.present(await self.service.get_production_company_by_id(uuid))


class CreateProductionCompanyUseCase:
    def __init__(self, presenter: AbstractPresenter, service: ProductionCompanyService):
        self.presenter = presenter
        self.service = service

    async def execute(self, in_dto: CreateProductionCompanyInDTO) -> None:
        await self.presenter.present(await self.service.create_production_company(in_dto))


class UpdateProductionCompanyUseCase:
    def __init__(self, presenter: AbstractPresenter, service: ProductionCompanyService):
        self.presenter = presenter
        self.service = service

    async def execute(self, uuid: str, in_data: CreateProductionCompanyInDTO) -> None:
        await self.presenter.present(await self.service.update_production_company(uuid, in_data))
