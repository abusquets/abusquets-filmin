from typing import Optional

from pydantic import BaseModel, Field, validator

from core.domain.schemas.user import User


class CreateUserInDTO(BaseModel):
    email: str = Field(max_length=255)
    first_name: str = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255, default=None)
    password: str
    is_admin: bool = Field(default=False)
    is_active: bool = Field(default=True)

    @validator('password', pre=True, always=True)
    def check_password(cls, v: str) -> str:
        return User.encrypt_password(v)


class CreateUserStdinDTO(BaseModel):
    email: str = Field(max_length=255)
    first_name: str = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255, default=None)
    password: str = Field(max_length=255, min_length=4)
