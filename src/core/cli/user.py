import click

from pydantic import ValidationError

from core.domain.services.user import UserService
from core.schemas.user.create_user import CreateUserInDTO, CreateUserStdinDTO
from shared.exceptions import AlreadyExists
from utils.async_utils import async_exec


def get_user_service() -> UserService:
    import app.app_container as container

    return container.AppContainer().user_service


async def _create_admin(email: str, first_name: str, password: str) -> None:
    try:
        in_data = CreateUserStdinDTO(email=email, first_name=first_name, password=password)
    except ValidationError as e:
        for error in e.errors():
            message = f'Error: {error}'
            raise click.BadParameter(message)

    user_service = get_user_service()
    in_dto = CreateUserInDTO(**in_data.model_dump(), is_admin=True)
    try:
        await user_service.create_user(in_dto)
        print(f'The User {first_name}, {email} has been created')
    except AlreadyExists as e:
        print(f'Error: {e.message}')
        raise click.Abort()


@click.argument('email')
@click.argument('first_name')
@click.option('--password', '-p', help='Enter a password', prompt=True)
def create_admin(email: str, first_name: str, password: str) -> None:
    async_exec(_create_admin, email, first_name, password)
