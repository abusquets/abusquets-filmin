from sqlalchemy.schema import Column, Table
from sqlalchemy.types import Integer, String

from infra.database.sqlalchemy.sqlalchemy import metadata


genres = Table(
    'filmin_genre',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String(255), unique=True, nullable=False),
    Column('name', String(255), nullable=False),
)
