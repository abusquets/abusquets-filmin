from filmin.di.mixins import FilminContainerMixin

from auth.di.mixins.token import TokenContainerMixin
from config import settings
from core.di.mixins import CoreContainerMixin
from infra.cache.ports import AbstractCacheRepository
from infra.database.sqlalchemy.session import AbstractDatabase
from utils.di import DIContainer, di_singleton


class AppContainerMixin:
    db: AbstractDatabase
    cache_repository: AbstractCacheRepository

    def _get_db(self) -> AbstractDatabase:
        from infra.database.sqlalchemy.session import Database

        return Database()

    @di_singleton
    def _get_cache_repository(self) -> AbstractCacheRepository:
        from infra.cache.redis_cache import RedisCache

        return RedisCache(
            url=settings.REDIS_URL,
            user=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
        )


# @singleton
class AppContainer(CoreContainerMixin, FilminContainerMixin, TokenContainerMixin, AppContainerMixin, DIContainer):
    pass
