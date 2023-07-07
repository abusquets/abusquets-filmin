from filmin.di.mixins import FilminContainerMixin

from core.di.mixins import CoreContainerMixin
from infra.database.sqlalchemy.session import AbstractDatabase
from utils.di import DIContainer


class AppContainerMixin:
    db: AbstractDatabase

    def _get_db(self) -> AbstractDatabase:
        from infra.database.sqlalchemy.session import Database

        return Database()


class AppContainer(CoreContainerMixin, FilminContainerMixin, AppContainerMixin, DIContainer):
    pass
