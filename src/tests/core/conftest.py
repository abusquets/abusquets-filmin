from typing import Any

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.sqlalchemy.models.core.country import countries


@pytest_asyncio.fixture(scope='session')
async def country_spain(migrate_db: Any, async_session_maker: AsyncSession) -> None:
    async with async_session_maker() as session:
        statement = countries.insert().values(code='ES', name='Spain')
        await session.execute(statement)
        await session.commit()
