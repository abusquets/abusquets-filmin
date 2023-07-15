from typing import Any, AsyncContextManager, Callable

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.sqlalchemy.models.core.country import countries


AsyncSessionCtxT = Callable[[], AsyncContextManager[AsyncSession]]


@pytest_asyncio.fixture(scope='session')
async def country_spain(migrate_db: Any, async_session_maker: AsyncSessionCtxT) -> None:
    async with async_session_maker() as session:
        statement = countries.insert().values(code='ES', name='Spain')
        await session.execute(statement)
        await session.commit()
