from filmin.data.repositories.ports.production_company import AbstractProductionCompanyRepository

from infra.database.sqlalchemy.session import AbstractDatabase


class ProductionCompanyContainerMixin:
    db: AbstractDatabase
    production_company_repository: AbstractProductionCompanyRepository

    def _get_production_company_repository(self) -> AbstractProductionCompanyRepository:
        from filmin.data.repositories.production_company import ProductionCompanyRepository

        return ProductionCompanyRepository(self.db.session)
