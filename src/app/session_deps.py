from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from app.app_container import AppContainer
from app.schemas import Session
from auth.utils import decode_token
from infra.cache.ports import AbstractCacheRepository


def get_cache_repository() -> AbstractCacheRepository:
    return AppContainer().cache_repository


async def _check_token(
    token_type: str,
    credentials: HTTPAuthorizationCredentials,
    cache_repository: AbstractCacheRepository,
) -> Session:
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials.',
        )

    claims = decode_token(token)

    if claims is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Invalid token or expired token.')

    if claims.get('type') != token_type:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Invalid token.')

    uuid = str(claims.get('jit'))
    if await cache_repository.get(uuid):
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='Revoked token.')

    return Session(uuid=uuid, expires=claims.get('exp'), username=claims.get('sub'), profile=claims.get('profile'))


async def check_access_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    cache_repository: AbstractCacheRepository = Depends(get_cache_repository),
) -> Session:
    return await _check_token('a', credentials, cache_repository)


async def check_refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    cache_repository: AbstractCacheRepository = Depends(get_cache_repository),
) -> Session:
    return await _check_token('r', credentials, cache_repository)


async def is_admin_session(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    cache_repository: AbstractCacheRepository = Depends(get_cache_repository),
) -> Session:
    session = await check_access_token(credentials, cache_repository)

    if not session.profile.is_admin:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not authorized.')

    return session
