import click

from pydantic import ValidationError

from core.data.repositories.ports.user import AbstractUserRepository
from core.schemas.user.create_user import CreateUserInDTO, CreateUserStdinDTO
from shared.exceptions import AlreadyExists
from utils.async_utils import async_exec


def get_user_repository() -> AbstractUserRepository:
    import app.app_container as container

    return container.AppContainer().user_repository


async def _create_admin(email: str, first_name: str, password: str) -> None:
    try:
        in_data = CreateUserStdinDTO(email=email, first_name=first_name, password=password)
    except ValidationError as e:
        for error in e.errors():
            message = f'Error: {error}'
            raise click.BadParameter(message)

    user_repository = get_user_repository()
    in_dto = CreateUserInDTO(**in_data.dict(), is_admin=True)
    try:
        await user_repository.create(in_dto)
        print(f'The User {first_name}, {email} has been created')
    except AlreadyExists as e:
        print(f'Error: {e.message}')
        raise click.Abort()


@click.argument('email')
@click.argument('first_name')
@click.option('--password', '-p', help='Enter a password', prompt=True)
def create_admin(email: str, first_name: str, password: str) -> None:
    async_exec(_create_admin, email, first_name, password)
