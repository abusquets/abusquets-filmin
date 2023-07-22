from datetime import datetime, timedelta
import logging

from typing import Literal, Optional, Type
import uuid

from jose import JWTError, jwt

from config import settings
from infra.cache.ports import AbstractCacheRepository


logguer = logging.getLogger(settings.APP_LOGGER_NAME)


class TokenService:
    def __init__(self, cache_repository: Optional[AbstractCacheRepository] = None) -> None:
        self.cache_repository = cache_repository

    @classmethod
    def _create_token(
        cls: Type['TokenService'], type_token: Literal['a', 'r'], subject: str, claims: dict, expiration_minutes: int
    ) -> str:
        now = datetime.utcnow()
        expires = datetime.utcnow() + timedelta(minutes=expiration_minutes)
        payload = {
            'type': type_token,
            'nbf': now,
            'iat': now,
            'exp': expires,
            'sub': subject,
            'jit': uuid.uuid4().hex,
        } | claims

        return jwt.encode(payload | claims, settings.JWT_SECRET_KEY, settings.JWT_ALGORITHM)

    def create_access_token(self, subject: str, claims: dict) -> str:
        return self._create_token('a', subject, claims, settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    def create_refresh_token(self, subject: str, claims: dict) -> str:
        return self._create_token('r', subject, claims, settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    def decode_token(self, token: str) -> Optional[dict]:
        claims = None
        try:
            claims = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except JWTError:
            logguer.debug('Token verification failed!', extra={'token': token})
        return claims

    async def revoke_access_token(self, token: str) -> None:
        if not self.cache_repository:
            raise ValueError('Cache repository not set!')
        await self.cache_repository.set(token, 'true', settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    async def revoke_refresh_token(self, token: str) -> None:
        if not self.cache_repository:
            raise ValueError('Cache repository not set!')
        await self.cache_repository.set(token, 'true', settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)
