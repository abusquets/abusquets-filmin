from typing import Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from app.app_container import AppContainer
from app.schemas import DetailResponse, Session
from app.session_deps import check_access_token, check_refresh_token
from auth.adapters.api.http.schemas import LoginResponse, ProtectedResponse, RefreshTokenResponse, UserAuthRequest
from auth.domain.services.token import TokenService
from core.adapters.api.cli.user_presenter import UserPresenter
from core.domain.services.user import UserService
from core.domain.use_cases.user import GetUserAndVerifyPasswordUseCase, InvalidPasswordException
from shared.exceptions import NotFound


router = APIRouter()


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
    app_container: AppContainer = Depends(AppContainer),
) -> LoginResponse:
    user_presenter = UserPresenter()
    user_service = UserService(app_container.user_repository)
    get_user_use_case = GetUserAndVerifyPasswordUseCase(user_presenter, user_service)

    try:
        await get_user_use_case.execute(payload.email, payload.password)
        user = user_presenter.result
    except (NotFound, InvalidPasswordException) as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect email or password') from exc

    claims: Dict[str, Any] = {
        'profile': {'first_name': user.first_name, 'last_name': user.last_name, 'is_admin': user.is_admin}
    }

    token_service = TokenService()

    access_token: str = token_service.create_access_token(user.email, claims)
    refresh_token: str = token_service.create_refresh_token(user.email, claims)

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
async def refresh(
    session: Session = Depends(check_refresh_token),
    app_container: AppContainer = Depends(AppContainer),
) -> RefreshTokenResponse:
    token_service = TokenService(cache_repository=app_container.cache_repository)

    profile = session.profile
    claims: Dict[str, Any] = {
        'profile': {'first_name': profile.first_name, 'last_name': profile.last_name, 'is_admin': profile.is_admin}
    }
    access_token: str = token_service.create_access_token(session.username, claims)
    return RefreshTokenResponse(access_token=access_token)


@router.delete('/access-revoke')
async def access_revoke(
    session: Session = Depends(check_access_token),
    app_container: AppContainer = Depends(AppContainer),
) -> DetailResponse:
    token_service = TokenService(cache_repository=app_container.cache_repository)
    await token_service.revoke_access_token(session.uuid)
    return DetailResponse(detail='Access Token has been revoked')


@router.delete('/refresh-revoke')
async def refresh_revoke(
    session: Session = Depends(check_refresh_token),
    app_container: AppContainer = Depends(AppContainer),
) -> DetailResponse:
    token_service = TokenService(cache_repository=app_container.cache_repository)
    await token_service.revoke_refresh_token(session.uuid)

    return DetailResponse(detail='Refresh Token has been revoked')
