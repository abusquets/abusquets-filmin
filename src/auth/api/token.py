from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from app.schemas import DetailResponse, Session
from app.session_deps import check_access_token, check_refresh_token
from auth.api.schemas import LoginResponse, ProtectedResponse, RefreshTokenResponse, UserAuthRequest
from auth.utils import create_access_token, create_refresh_token
from config import settings
from core.data.repositories.ports.user import AbstractUserRepository
from core.domain.schemas.user import User
from infra.cache.ports import AbstractCacheRepository
from shared.repository.ports.generic import FilterBy


router = APIRouter()


def get_user_repository() -> AbstractUserRepository:
    from app.app_container import AppContainer

    return AppContainer().user_repository


@router.post(
    '/login',
    summary='Create access and refresh tokens for user',
    responses={
        200: {'description': 'Successful Response'},
        401: {'description': 'Unauthorized'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def login(
    payload: UserAuthRequest,
    user_repository: AbstractUserRepository = Depends(get_user_repository),
) -> LoginResponse:
    by: FilterBy = {'email': payload.email}
    users = await user_repository.filter_by(by)

    if not users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')
    user = users[0]

    hashed_pass = user.password

    if not User.verify_password(payload.password, hashed_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password')

    claims: Dict[str, Any] = {
        'profile': {'first_name': user.first_name, 'last_name': user.last_name, 'is_admin': user.is_admin}
    }
    access_token: str = create_access_token(user.email, claims)
    refresh_token: str = create_refresh_token(user.email, claims)

    return LoginResponse(access_token=access_token, refresh_token=refresh_token)


@router.get(
    '/protected',
    summary='Get current session - example of protected endpoint',
    responses={
        200: {'description': 'Successful Response'},
        403: {'description': 'Permission denied'},
        422: {'description': 'Unprocessable Entity'},
    },
)
async def protected(current_session: Session = Depends(check_access_token)) -> ProtectedResponse:
    return ProtectedResponse(username=current_session.username)


@router.post('/refresh-token', summary='Refresh access token')
async def refresh(session: Session = Depends(check_refresh_token)) -> RefreshTokenResponse:
    profile = session.profile
    claims: Dict[str, Any] = {
        'profile': {'first_name': profile.first_name, 'last_name': profile.last_name, 'is_admin': profile.is_admin}
    }
    access_token: str = create_access_token(session.username, claims)
    return RefreshTokenResponse(access_token=access_token)


def get_cache_repository() -> AbstractCacheRepository:
    from app.app_container import AppContainer

    return AppContainer().cache_repository


@router.delete('/access-revoke')
async def access_revoke(
    session: Session = Depends(check_access_token),
    cache_repository: AbstractCacheRepository = Depends(get_cache_repository),
) -> DetailResponse:
    await cache_repository.set(session.uuid, 'true', settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    return DetailResponse(detail='Access Token has been revoked')


@router.delete('/refresh-revoke')
async def refresh_revoke(
    session: Session = Depends(check_refresh_token),
    cache_repository: AbstractCacheRepository = Depends(get_cache_repository),
) -> DetailResponse:
    await cache_repository.set(session.uuid, 'true', settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    return DetailResponse(detail='Refresh Token has been revoked')
