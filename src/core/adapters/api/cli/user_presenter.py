from typing import Optional

from pydantic import BaseModel

from core.domain.entities.user import User
from core.domain.entities.value_objects import UserId
from shared.presenter import AbstractPresenter


class UserResponse(BaseModel):
    uuid: UserId
    email: str
    first_name: str
    last_name: Optional[str]
    is_admin: bool = False
    is_active: bool = True


class UserPresenter(AbstractPresenter[User, UserResponse]):
    result: UserResponse

    async def present(self, data: User) -> None:
        self.result = UserResponse.model_validate(data, from_attributes=True)
