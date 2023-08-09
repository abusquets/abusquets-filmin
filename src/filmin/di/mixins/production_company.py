from filmin.adapters.spi.repositories.production_company import ProductionCompanyRepository
from filmin.domain.ports.repositories.production_company import AbstractProductionCompanyRepository
from infra.database.sqlalchemy.session import AbstractDatabase


class ProductionCompanyContainerMixin:
    db: AbstractDatabase
    production_company_repository: AbstractProductionCompanyRepository

    def _get_production_company_repository(self) -> AbstractProductionCompanyRepository:
        return ProductionCompanyRepository(self.db.session)
