import asyncio

from asyncio import current_task
from typing import Iterator

from httpx import AsyncClient
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_scoped_session, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.asgi import app
from config import settings
import infra.database.sqlalchemy.models  # noqa

from infra.database.sqlalchemy.sqlalchemy import metadata


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
def engine() -> AsyncEngine:
    yield create_async_engine(settings.DATABASE_URL, future=True, echo=False)


@pytest.fixture(scope='session')
def async_session_maker(engine: AsyncEngine) -> AsyncSession:
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
async def async_client() -> AsyncClient:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac
