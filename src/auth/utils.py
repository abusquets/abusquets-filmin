from datetime import datetime, timedelta
import logging

from typing import Literal, Optional
import uuid

from jose import JWTError, jwt

from config import settings


logguer = logging.getLogger(settings.APP_LOGGER_NAME)


def _create_token(type_token: Literal['a', 'r'], subject: str, claims: dict, expiration_minutes: int) -> str:
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


def create_access_token(subject: str, claims: dict) -> str:
    return _create_token('a', subject, claims, settings.ACCESS_TOKEN_EXPIRE_MINUTES)


def create_refresh_token(subject: str, claims: dict) -> str:
    return _create_token('r', subject, claims, settings.REFRESH_TOKEN_EXPIRE_MINUTES)


def decode_token(token: str) -> Optional[dict]:
    claims = None
    try:
        claims = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        logguer.debug('Token verification failed!', extra={'token': token})
    return claims
