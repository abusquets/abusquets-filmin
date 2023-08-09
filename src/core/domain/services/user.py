from typing import Type

from pydantic import validator

from core.domain.entities.user import User
from core.domain.ports.repositories.user import (
    AbstractUserRepository,
    CreateUserInDTO as CreateUserInRepoDTO,
)


class CreateUserInDTO(CreateUserInRepoDTO):
    @validator('password', pre=True, always=True)
    @classmethod
    def check_password(cls: Type['CreateUserInDTO'], v: str) -> str:
        return User.encrypt_password(v)


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_in: CreateUserInDTO) -> User:
        user_in_repo = CreateUserInRepoDTO(**user_in.model_dump())
        return await self.user_repository.create(user_in_repo)

    async def get_user_by_username(self, uuid: str) -> User:
        return await self.user_repository.get_by_id(uuid)
