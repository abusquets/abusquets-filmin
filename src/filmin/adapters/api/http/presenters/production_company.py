from typing import List

from filmin.adapters.api.http.schemas.production_company import (
    ProductionCompanyListPagedResponse,
    ProductionCompanyResponse,
)
from filmin.domain.entities.production_company import ProductionCompany
from shared.api.schemas.page import PageParams
from shared.presenter import AbstractPresenter


class ProductionCompanyPresenter(AbstractPresenter[ProductionCompany, ProductionCompanyResponse]):
    result: ProductionCompanyResponse

    async def present(self, data: ProductionCompany) -> None:
        self.result = ProductionCompanyResponse.model_validate(data, from_attributes=True)


class ProductionCompanyPagedListPresenter(AbstractPresenter[List[ProductionCompany], List[ProductionCompanyResponse]]):
    result: ProductionCompanyListPagedResponse

    def __init__(self, page_params: PageParams) -> None:
        self.page_params = page_params

    async def present(self, data: List[ProductionCompany]) -> None:
        list_items = [ProductionCompanyResponse.model_validate(item, from_attributes=True) for item in data]
        self.result = ProductionCompanyListPagedResponse(
            results=list_items,
            total=len(list_items),
            page=self.page_params.page,
            size=self.page_params.size,
        )
