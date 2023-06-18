from core.data.repositories.ports.user import AbstractUserRepository
from infra.database.sqlalchemy.session import AbstractDatabase


class UserRepositoryContainerMixin:
    db: AbstractDatabase
    user_repository: AbstractUserRepository

    def _get_user_repository(self) -> AbstractUserRepository:
        from core.data.repositories.user import UserRepository

        return UserRepository(self.db.session)
