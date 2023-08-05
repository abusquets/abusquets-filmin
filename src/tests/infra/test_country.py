import pytest

from sqlalchemy.ext.asyncio import async_scoped_session
from sqlalchemy.sql import text


@pytest.mark.asyncio
async def test_county_table_exists(async_session_maker: async_scoped_session) -> None:
    async with async_session_maker() as session:
        await session.execute(text('SELECT * FROM core_country'))
    assert True
