from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.status import HTTP_403_FORBIDDEN

from auth.utils import decode_token

from app.schemas import Session


async def get_current_session(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Session:
    token = credentials.credentials

    if not token:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail='Invalid authentication credentials.',
        )

    claims = decode_token(token)

    if claims is None:
        raise HTTPException(status_code=403, detail='Invalid token or expired token.')

    return Session(username=claims.get('sub'), profile=claims.get('profile'))


async def is_admin_session(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> Session:
    session = await get_current_session(credentials)

    if not session.profile.is_admin:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail='Not authorized.')

    return session
