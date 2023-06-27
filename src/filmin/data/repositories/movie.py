from typing import Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import registry, relationship

from filmin.data.repositories.ports.genre import AbstractGenreRepository
from filmin.domain.schemas.genre import Genre
from filmin.domain.schemas.movie import Movie
from filmin.domain.schemas.movie_collection import MovieCollection
from filmin.schemas.movie import CreateMovieInDTO, UpdatePartialMovieInDTO

from .ports.movie import AbstractMovieRepository
from infra.database.sqlalchemy.models.filmin.collection import movie_collection
from infra.database.sqlalchemy.models.filmin.movie import movie, movie_genre
from shared.repository.sqlalchemy import SqlAlchemyRepository


mapper_registry = registry()
mapper_registry.map_imperatively(MovieCollection, movie_collection)
mapper_registry.map_imperatively(
    Movie,
    movie,
    properties={
        'collection': relationship(MovieCollection, lazy='joined'),
        'genres': relationship(Genre, secondary=movie_genre, lazy='selectin'),
    },
)


class MovieRepository(
    SqlAlchemyRepository[Movie, CreateMovieInDTO, UpdatePartialMovieInDTO],
    AbstractMovieRepository,
):
    def __init__(self, session: AsyncSession, genre_repository: AbstractGenreRepository) -> None:
        super().__init__(session)
        self.genre_repository = genre_repository

    async def create(self, data: CreateMovieInDTO) -> Movie:
        async with self.session_factory() as session:
            instance = self.entity(**data.dict(exclude={'genres'}))
            if data.genres:
                for g in data.genres:
                    instance.genres.append(await self.genre_repository.get_by_id(g))
            session.add(instance)
        return await self.get_by_id(str(instance.uuid))

    async def update(self, uuid: str, data: UpdatePartialMovieInDTO) -> Movie:
        to_update = data.dict(exclude_unset=True)
        if not to_update:
            raise ValueError('No data to update')

        async with self.session_factory() as session:
            instance = await self.get_by_id(uuid)
            new_genres: Optional[List[str]] = to_update.pop('genres', None)
            if new_genres is not None:
                current_genres: Dict[str, Genre] = {g.code: g for g in instance.genres}
                # Look for new genres
                for code in new_genres:
                    if code not in current_genres:
                        instance.genres.append(await self.genre_repository.get_by_id(code))

                # Look for genres to remove
                for genre in instance.genres:
                    if genre.code not in new_genres:
                        instance.genres.remove(genre)

            for key, value in to_update.items():
                setattr(instance, key, value)

            session.add(instance)

        return await self.get_by_id(str(instance.uuid))
