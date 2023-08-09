from typing import Optional

from pydantic import BaseModel, Field

from core.domain.entities.user import User
from shared.repository.ports.generic import AbstractRepository


class CreateUserInDTO(BaseModel):
    email: str = Field(max_length=255)
    first_name: str = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255, default=None)
    password: str
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)

    # Hauriem d'haver encriptat la contrasenya abans de guardar-la a la base de dades


class UpdatePartialUserInDTO(BaseModel):
    email: Optional[str] = Field(max_length=255)
    first_name: Optional[str] = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255)
    password: Optional[str] = Field(max_length=255)


class AbstractUserRepository(AbstractRepository[User, CreateUserInDTO, UpdatePartialUserInDTO]):
    pass
