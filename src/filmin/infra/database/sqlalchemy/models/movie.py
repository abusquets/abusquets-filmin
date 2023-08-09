import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, Table, UniqueConstraint
from sqlalchemy.types import BigInteger, Date, Float, Integer, String, Text

from infra.database.sqlalchemy.sqlalchemy import metadata


movie = Table(
    'filmin_movie',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4),
    Column('title', String(255), nullable=False),
    Column('release_date', Date, nullable=True),
    Column('budget', BigInteger, nullable=True),
    Column('revenue', BigInteger, nullable=True),
    Column('popularity', Float, nullable=True),
    Column('runtime', BigInteger, nullable=True),
    Column('rating', Float, nullable=True),
    Column('original_language', String(2), nullable=True),
    Column('collection_id', UUID, ForeignKey('filmin_collection.uuid')),
    Column('overview', Text, nullable=True),
)

movie_genre = Table(
    'filmin_movie_genre',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('movie_id', UUID, ForeignKey('filmin_movie.uuid')),
    Column('genre_id', String(255), ForeignKey('filmin_genre.code')),
    UniqueConstraint('movie_id', 'genre_id', name='unique_filmin_movie_genre'),
)
