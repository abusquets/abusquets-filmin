from filmin.domain.entities.production_company import ProductionCompany
from filmin.schemas.production_company import CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO
from shared.repository.ports.generic import AbstractRepository


class AbstractProductionCompanyRepository(
    AbstractRepository[ProductionCompany, CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO]
):
    pass
