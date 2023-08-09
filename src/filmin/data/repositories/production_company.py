from sqlalchemy.orm import registry

from .ports.production_company import AbstractProductionCompanyRepository
from filmin.domain.schemas.production_company import ProductionCompany
from filmin.infra.database.sqlalchemy.models import production_company
from filmin.schemas.production_company import CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO
from shared.repository.sqlalchemy import SqlAlchemyRepository


mapper_registry = registry()

mapper_registry.map_imperatively(
    ProductionCompany,
    production_company,
)


class ProductionCompanyRepository(
    SqlAlchemyRepository[ProductionCompany, CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO],
    AbstractProductionCompanyRepository,
):
    pass
