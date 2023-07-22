from typing import Optional

import click

from pydantic import BaseModel, Field, ValidationError

from app.app_container import AppContainer
from core.adapters.api.cli.user_presenter import UserPresenter
from core.domain.services.user import CreateUserInDTO, UserService
from core.domain.use_cases.user import CreateUserUseCase
from shared.exceptions import AlreadyExists
from utils.async_utils import async_exec


class CreateUserStdinDTO(BaseModel):
    email: str = Field(max_length=255)
    first_name: str = Field(max_length=255)
    last_name: Optional[str] = Field(max_length=255, default=None)
    password: str = Field(max_length=255, min_length=4)


async def _create_admin(email: str, first_name: str, password: str) -> None:
    # Validate input
    try:
        in_data = CreateUserStdinDTO(email=email, first_name=first_name, password=password)
    except ValidationError as e:
        for error in e.errors():
            message = f'Error: {error}'
            raise click.BadParameter(message)

    repo = AppContainer().user_repository
    user_service = UserService(repo)
    in_dto = CreateUserInDTO(**in_data.model_dump(), is_admin=True)
    presenter = UserPresenter()
    use_case = CreateUserUseCase(presenter=presenter, service=user_service)
    try:
        await use_case.execute(in_dto)
        user = presenter.result
        print(f'The User {user.first_name}, {user.email} has been created')
    except AlreadyExists as e:
        print(f'Error: {e.message}')
        raise click.Abort()


@click.argument('email')
@click.argument('first_name')
@click.option('--password', '-p', help='Enter a password', prompt=True)
def create_admin(email: str, first_name: str, password: str) -> None:
    async_exec(_create_admin, email, first_name, password)
