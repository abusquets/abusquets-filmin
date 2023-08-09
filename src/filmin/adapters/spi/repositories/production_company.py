from sqlalchemy.orm import registry

from filmin.domain.entities.production_company import ProductionCompany
from filmin.domain.ports.repositories.production_company import AbstractProductionCompanyRepository
from filmin.infra.database.sqlalchemy.models import production_company
from filmin.schemas.production_company import CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO
from shared.repository.sqlalchemy import SqlAlchemyRepository


mapper_registry = registry()

mapper_registry.map_imperatively(
    ProductionCompany,
    production_company.production_company,
)


class ProductionCompanyRepository(
    SqlAlchemyRepository[ProductionCompany, CreateProductionCompanyInDTO, UpdatePartialProductionCompanyInDTO],
    AbstractProductionCompanyRepository,
):
    pass
