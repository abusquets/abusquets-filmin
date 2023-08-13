import asyncio

from asyncio import current_task
from typing import AsyncGenerator, Generator, Iterator

from httpx import AsyncClient
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.app_container import AppContainer, AppContainerMixin
from app.asgi import app
from auth.domain.services.token import TokenService
from config import settings
from core.domain.entities.user import User
from core.domain.ports.repositories.user import AbstractUserRepository, CreateUserInDTO
import core.infra.database.sqlalchemy.models  # noqa
import filmin.infra.database.sqlalchemy.models  # noqa

from infra.cache.memory_cache import MemoryCache
from infra.cache.ports import AbstractCacheRepository
import infra.database.sqlalchemy.models  # noqa
from infra.database.sqlalchemy.sqlalchemy import metadata
from utils.di import di_singleton


def pytest_addoption(parser: pytest.Parser) -> None:
    # NOTE: when adding or removing an option,
    # remove to remove/add from app/conftest.py:addoption_params
    parser.addoption('--no-db', default=False, action='store_true', help='Disable testing database')


def addoption_params(config: pytest.Config) -> dict[str, bool]:
    return {
        'no-db': config.getoption('--no-db'),
    }


def pytest_configure(config: pytest.Config) -> None:
    params = addoption_params(config)
    if not params.get('no-db'):
        next(_event_loop()).run_until_complete(create_all(_engine()))


def pytest_unconfigure(config: pytest.Config) -> None:
    params = addoption_params(config)
    if not params.get('no-db'):
        next(_event_loop()).run_until_complete(drop_all(_engine()))


def _event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError as e:
        if str(e).startswith('There is no current event loop in thread'):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        else:
            raise

    yield loop
    loop.close()


@pytest.fixture(scope='session')
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    yield from _event_loop()


def _engine() -> AsyncEngine:
    return create_async_engine(settings.DATABASE_URL, future=True, echo=False)


@pytest.fixture(scope='session', autouse=True)
def engine() -> Generator:
    yield _engine()


@pytest.fixture(scope='session')
def async_session_maker(engine: AsyncEngine) -> Generator:
    yield async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession), scopefunc=current_task
    )


# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all, checkfirst=True)


async def create_all(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)
    await engine.dispose()


async def drop_all(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
    await engine.dispose()


# async def disconnect() -> None:
#     if engine:
#         await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def async_root_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture(scope='session')
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test/api/v1') as ac:
        yield ac


@pytest_asyncio.fixture(scope='session')
async def app_container() -> AsyncGenerator:
    yield AppContainer()


@pytest_asyncio.fixture(scope='session')
async def user_repository(app_container: AppContainer) -> AsyncGenerator[AbstractUserRepository, None]:
    yield app_container.user_repository


@pytest_asyncio.fixture(scope='session')
async def token_service(app_container: AppContainer) -> AsyncGenerator[TokenService, None]:
    yield app_container.token_service


@pytest_asyncio.fixture(scope='session')
async def admin_user(user_repository: AbstractUserRepository) -> AsyncGenerator[User, None]:
    # We have to encrypt the password here because the password is not encrypted in the repository
    password = User.encrypt_password('123456')
    in_dto = CreateUserInDTO(email='admin@filmin.poc', first_name='Admin', password=password, is_admin=True)
    yield await user_repository.create(in_dto)
    await user_repository.delete(in_dto.email)


@pytest_asyncio.fixture(scope='session')
async def normal_user(user_repository: AbstractUserRepository) -> AsyncGenerator[User, None]:
    # We have to encrypt the password here because the password is not encrypted in the repository
    password = User.encrypt_password('123456')
    in_dto = CreateUserInDTO(email='user@filmin.poc', first_name='Example', password=password, is_admin=False)
    yield await user_repository.create(in_dto)
    await user_repository.delete(in_dto.email)


@pytest.fixture(scope='session')
def admin_access_token(admin_user: User, token_service: TokenService) -> str:
    return token_service.create_access_token(
        admin_user.email, {'profile': {'first_name': admin_user.first_name, 'is_admin': admin_user.is_admin}}
    )


@pytest.fixture(scope='session')
def normal_user_access_token(normal_user: User, token_service: TokenService) -> str:
    return token_service.create_access_token(
        normal_user.email, {'profile': {'first_name': normal_user.first_name, 'is_admin': normal_user.is_admin}}
    )


@pytest_asyncio.fixture(scope='session')
async def async_admin_client(admin_access_token: str) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test/api/v1') as ac:
        ac.headers.update({'Authorization': f'Bearer {admin_access_token}'})
        yield ac


@pytest_asyncio.fixture(scope='session')
async def async_normal_client(normal_user_access_token: str) -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test/api/v1') as ac:
        ac.headers.update({'Authorization': f'Bearer {normal_user_access_token}'})
        yield ac


@pytest.fixture(autouse=True)
def memory_cache_database(monkeypatch: pytest.MonkeyPatch) -> Generator[None, None, None]:
    @di_singleton
    def fake_cache_gateway() -> AbstractCacheRepository:
        return MemoryCache()

    monkeypatch.setattr(AppContainerMixin, '_get_cache_repository', lambda _: fake_cache_gateway())

    yield
