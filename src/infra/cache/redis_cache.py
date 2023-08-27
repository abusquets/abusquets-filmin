from typing import Any, Optional

from redis import (
    asyncio as aioredis,
)

from infra.cache.ports import AbstractCacheRepository, EncodableT
from utils.singleton import singleton


@singleton
class RedisCache(AbstractCacheRepository):
    def __init__(self, url: str, user: str, password: str) -> None:
        self.redis: Optional[aioredis.Redis] = None
        self.url = url
        self.user = user
        self.password = password

    async def init(self) -> None:
        self.redis = await aioredis.from_url(
            self.url,
            username=self.user,
            password=self.password,
            max_connections=10,
            decode_responses=True,
        )

    async def get_redis(self) -> aioredis.Redis:
        if self.redis is None:
            await self.init()
        if self.redis is None:
            raise Exception('Redis not initialized')
        return self.redis

    async def close(self) -> None:
        await (await self.get_redis()).connection_pool.disconnect()

    async def get(self, key: str) -> Any:
        return await (await self.get_redis()).get(key)

    async def set(self, key: str, value: Optional[EncodableT], expire: int) -> None:
        """expire: expiration in seconds"""
        await self.get_redis()
        if value is None:
            await self.delete(key)
        else:
            await (await self.get_redis()).set(key, value, expire)

    async def delete(self, key: str) -> None:
        await (await self.get_redis()).delete(key)
