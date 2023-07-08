from core.data.repositories.ports.user import AbstractUserRepository
from core.domain.services.user import UserService
from infra.database.sqlalchemy.session import AbstractDatabase


class UserRepositoryContainerMixin:
    db: AbstractDatabase
    user_repository: AbstractUserRepository

    def _get_user_repository(self) -> AbstractUserRepository:
        from core.data.repositories.user import UserRepository

        return UserRepository(self.db.session)


class UserServiceContainerMixin(UserRepositoryContainerMixin):
    user_service: UserService

    def _get_user_service(self) -> UserService:
        return UserService(self.user_repository)
