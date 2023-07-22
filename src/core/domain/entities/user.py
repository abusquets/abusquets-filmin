from dataclasses import dataclass, field
from typing import Optional
import uuid as uuid_lib

import bcrypt

from core.domain.entities.value_objects import UserId


@dataclass(kw_only=True)
class BaseUser:
    email: str
    first_name: str
    last_name: Optional[str]
    password: str
    is_admin: bool = False
    is_active: bool = True

    @staticmethod
    def encrypt_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        return str(hashed_password.decode())

    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        return bool(bcrypt.hashpw(password.encode(), hashed.encode()) == hashed.encode())


@dataclass(kw_only=True)
class User(BaseUser):
    uuid: UserId = field(default_factory=uuid_lib.uuid4)
