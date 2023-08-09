from typing import AsyncContextManager, Callable

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from core.infra.database.sqlalchemy.models.country import countries


AsyncSessionCtxT = Callable[[], AsyncContextManager[AsyncSession]]


@pytest_asyncio.fixture(scope='session')
async def country_spain(async_session_maker: AsyncSessionCtxT) -> None:
    async with async_session_maker() as session:
        statement = countries.insert().values(code='ES', name='Spain')
        await session.execute(statement)
        await session.commit()
