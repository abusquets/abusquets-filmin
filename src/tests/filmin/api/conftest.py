import datetime

from typing import Any, AsyncGenerator

import pytest_asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from infra.database.sqlalchemy.models.filmin.collection import movie_collection
from infra.database.sqlalchemy.models.filmin.genre import genres
from infra.database.sqlalchemy.models.filmin.movie import movie, movie_genre


@pytest_asyncio.fixture(scope='session')
async def genre_western(migrate_db: Any, async_session_maker: AsyncSession) -> str:
    async with async_session_maker() as session:
        statement = genres.insert().values(code='western', name='Western')
        await session.execute(statement)
        await session.commit()
        return 'western'


@pytest_asyncio.fixture(scope='session')
async def genre_comedy(migrate_db: Any, async_session_maker: AsyncSession) -> str:
    async with async_session_maker() as session:
        statement = genres.insert().values(code='comedy', name='Comedy')
        await session.execute(statement)
        await session.commit()
        return 'comedy'


@pytest_asyncio.fixture(scope='session')
async def genre_animation(migrate_db: Any, async_session_maker: AsyncSession) -> str:
    async with async_session_maker() as session:
        statement = genres.insert().values(code='animation', name='Animation')
        await session.execute(statement)
        await session.commit()
        return 'animation'


@pytest_asyncio.fixture(scope='session')
async def genre_fake(migrate_db: Any, async_session_maker: AsyncSession) -> str:
    async with async_session_maker() as session:
        statement = genres.insert().values(code='fake-genre', name='Fake Genre')
        await session.execute(statement)
        await session.commit()
        return 'fake-genre'


@pytest_asyncio.fixture(scope='session')
async def collection_toy_story(migrate_db: Any, async_session_maker: AsyncSession) -> str:
    async with async_session_maker() as session:
        stmt = movie_collection.insert().values(name='Toy Story Collection').returning(movie_collection.c.uuid)
        result = await session.execute(stmt)
        await session.commit()
        return str(result.scalar_one())


@pytest_asyncio.fixture(scope='session')
async def collection_fake(migrate_db: Any, async_session_maker: AsyncSession) -> str:
    async with async_session_maker() as session:
        stmt = movie_collection.insert().values(name='Fake Collection').returning(movie_collection.c.uuid)
        result = await session.execute(stmt)
        await session.commit()
        return str(result.scalar_one())


@pytest_asyncio.fixture(scope='function')
async def movie_toy_story2(
    migrate_db: Any,
    async_session_maker: AsyncSession,
    collection_toy_story: str,
    genre_comedy: str,
    genre_animation: str,
) -> AsyncGenerator:
    async with async_session_maker() as session:
        data = {
            'title': 'Toy Story 2',
            'release_date': datetime.datetime.strptime('2000-10-30', '%Y-%m-%d').date(),
            'budget': 30000000,
            'revenue': 373554033,
            'collection_id': collection_toy_story,
            'original_language': 'en',
            'overview': 'Test overview',
        }

        stmt = movie.insert().values(**data).returning(movie.c.uuid)
        result = await session.execute(stmt)
        movie_uuid = str(result.scalar_one())

        data = {
            'movie_id': movie_uuid,
            'genre_id': genre_comedy,
        }
        stmt = movie_genre.insert().values(**data)
        await session.execute(stmt)

        data = {
            'movie_id': movie_uuid,
            'genre_id': genre_animation,
        }
        stmt = movie_genre.insert().values(**data)
        await session.execute(stmt)

        await session.commit()

        yield movie_uuid

        stmt = movie_genre.delete().where(movie_genre.c.movie_id == movie_uuid)
        await session.execute(stmt)

        stmt = movie.delete().where(movie.c.uuid == movie_uuid)
        await session.execute(stmt)

        await session.commit()


@pytest_asyncio.fixture(scope='function')
async def clean_movie(async_session_maker: AsyncSession) -> AsyncGenerator:
    yield
    async with async_session_maker() as session:
        stmt = movie_genre.delete()
        await session.execute(stmt)

        stmt = movie.delete()
        await session.execute(stmt)

        await session.commit()