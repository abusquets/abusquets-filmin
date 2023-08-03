import asyncio

from asyncio import current_task
from typing import Any, AsyncGenerator, Generator, Iterator

from httpx import AsyncClient
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.app_container import AppContainer, AppContainerMixin
from app.asgi import app
from auth.utils import create_access_token
from config import settings
from core.data.repositories.ports.user import AbstractUserRepository
from core.domain.schemas.user import User
from core.schemas.user.create_user import CreateUserInDTO
from infra.cache.memory_cache import MemoryCache
from infra.cache.ports import AbstractCacheRepository
import infra.database.sqlalchemy.models  # noqa

from infra.database.sqlalchemy.sqlalchemy import metadata
from utils.di import di_singleton


@pytest.fixture(scope='session')
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
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


@pytest.fixture(scope='session', autouse=True)
def engine() -> Generator:
    yield create_async_engine(settings.DATABASE_URL, future=True, echo=False)


@pytest.fixture(scope='session')
def async_session_maker(engine: AsyncEngine) -> Generator:
    yield async_scoped_session(
        sessionmaker(engine, expire_on_commit=False, class_=AsyncSession), scopefunc=current_task
    )


async def create_all(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
        await conn.run_sync(metadata.create_all)


async def drop_all(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope='session', autouse=True)
def migrate_db(event_loop: asyncio.AbstractEventLoop, engine: AsyncEngine) -> Iterator[None]:
    event_loop.run_until_complete(create_all(engine))
    yield
    event_loop.run_until_complete(drop_all(engine))


@pytest_asyncio.fixture(scope='session')
async def async_root_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest_asyncio.fixture(scope='session')
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test/api/v1') as ac:
        yield ac


@pytest_asyncio.fixture(scope='session')
async def app_container(migrate_db: Any) -> AsyncGenerator:
    yield AppContainer()


@pytest_asyncio.fixture(scope='session')
async def user_repository(app_container: AppContainer) -> AsyncGenerator:
    yield app_container.user_repository


@pytest_asyncio.fixture(scope='session')
async def admin_user(user_repository: AbstractUserRepository) -> AsyncGenerator[User, None]:
    in_dto = CreateUserInDTO(email='admin@filmin.poc', first_name='Admin', password='123456', is_admin=True)
    yield await user_repository.create(in_dto)
    await user_repository.delete(in_dto.email)


@pytest_asyncio.fixture(scope='session')
async def normal_user(user_repository: AbstractUserRepository) -> AsyncGenerator[User, None]:
    in_dto = CreateUserInDTO(email='user@filmin.poc', first_name='Example', password='123456', is_admin=False)
    yield await user_repository.create(in_dto)
    await user_repository.delete(in_dto.email)


@pytest.fixture(scope='session')
def admin_access_token(admin_user: User) -> str:
    return create_access_token(
        admin_user.email, {'profile': {'first_name': admin_user.first_name, 'is_admin': admin_user.is_admin}}
    )


@pytest.fixture(scope='session')
def normal_user_access_token(normal_user: User) -> str:
    return create_access_token(
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
