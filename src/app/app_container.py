from auth.di.mixins.token import TokenContainerMixin
from config import settings
from core.di.mixins import CoreContainerMixin
from filmin.di.mixins import FilminContainerMixin
from infra.cache.ports import AbstractCacheRepository
from infra.cache.redis_cache import RedisCache
from infra.database.sqlalchemy.session import AbstractDatabase, Database
from utils.di import DIContainer, di_singleton


class AppContainerMixin:
    db: AbstractDatabase
    cache_repository: AbstractCacheRepository

    def _get_db(self) -> AbstractDatabase:
        return Database()

    @di_singleton
    def _get_cache_repository(self) -> AbstractCacheRepository:
        return RedisCache(
            url=settings.REDIS_URL,
            user=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD,
        )


# @singleton
class AppContainer(CoreContainerMixin, FilminContainerMixin, TokenContainerMixin, AppContainerMixin, DIContainer):
    pass
