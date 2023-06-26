from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import registry

from core.data.repositories.ports.user import AbstractUserRepository
from core.domain.schemas.user import User
from core.schemas.user.create_user import CreateUserInDTO
from core.schemas.user.update_user import UpdatePartialUserInDTO
from infra.database.sqlalchemy.models.core.user import users
from shared.exceptions import AlreadyExists
from shared.repository.sqlalchemy import SqlAlchemyRepository


mapper_registry = registry()


mapper_registry.map_imperatively(
    User,
    users,
)


class UserRepository(
    SqlAlchemyRepository[User, CreateUserInDTO, UpdatePartialUserInDTO],
    AbstractUserRepository,
):
    async def create(self, data: CreateUserInDTO) -> User:
        try:
            ret = await super().create(data)
        except IntegrityError as e:
            if 'duplicate key value violates unique constraint "uq_core_user_email"' in str(e):
                raise AlreadyExists(User.__name__)
        return ret
