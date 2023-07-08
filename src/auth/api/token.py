from typing import Annotated, Any, Dict

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter

from auth.api.schemas import LoginResponse, ProtectedResponse, UserAuthRequest
from auth.utils import create_access_token, create_refresh_token

from app.schemas import Session
from app.session_deps import get_current_session
from core.data.repositories.ports.user import AbstractUserRepository
from core.domain.schemas.user import User
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
def protected(current_session: Annotated[Session, Depends(get_current_session)]) -> ProtectedResponse:
    return ProtectedResponse(username=current_session.username)
