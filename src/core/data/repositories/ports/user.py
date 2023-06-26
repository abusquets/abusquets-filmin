from core.domain.schemas.user import User
from core.schemas.user.create_user import CreateUserInDTO
from core.schemas.user.update_user import UpdatePartialUserInDTO
from shared.repository.ports.generic import AbstractRepository


class AbstractUserRepository(AbstractRepository[User, CreateUserInDTO, UpdatePartialUserInDTO]):
    pass
