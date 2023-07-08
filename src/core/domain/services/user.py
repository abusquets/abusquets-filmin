from core.data.repositories.ports.user import AbstractUserRepository
from core.domain.schemas.user import User
from core.schemas.user.create_user import CreateUserInDTO


class UserService:
    def __init__(self, user_repository: AbstractUserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_in: CreateUserInDTO) -> User:
        return await self.user_repository.create(user_in)
