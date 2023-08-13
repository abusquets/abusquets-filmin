from typing import AsyncContextManager, Callable, Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import registry, relationship

from filmin.domain.entities.genre import Genre
from filmin.domain.entities.movie import Movie
from filmin.domain.entities.movie_collection import MovieCollection
from filmin.domain.ports.repositories.genre import AbstractGenreRepository
from filmin.domain.ports.repositories.movie import AbstractMovieRepository
from filmin.infra.database.sqlalchemy.models.collection import movie_collection
from filmin.infra.database.sqlalchemy.models.movie import movie, movie_genre
from filmin.schemas.movie import CreateMovieInDTO, UpdatePartialMovieInDTO
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

AsyncSessionCtxT = Callable[[], AsyncContextManager[AsyncSession]]


class MovieRepository(
    SqlAlchemyRepository[Movie, CreateMovieInDTO, UpdatePartialMovieInDTO],
    AbstractMovieRepository,
):
    def __init__(self, session: AsyncSessionCtxT, genre_repository: AbstractGenreRepository) -> None:
        super().__init__(session)
        self.genre_repository = genre_repository

    async def create(self, data: CreateMovieInDTO) -> Movie:
        async with self.session_factory() as session:
            in_data = data.model_dump(exclude={'genres', 'collection_id'})
            instance = self.entity(**in_data)
            if data.genres:
                for g in data.genres:
                    instance.genres.append(await self.genre_repository.get_by_id(g))
            session.add(instance)
        return await self.get_by_id(str(instance.uuid))

    async def update(self, uuid: str, data: UpdatePartialMovieInDTO) -> Movie:
        to_update = data.model_dump(exclude_unset=True)
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
