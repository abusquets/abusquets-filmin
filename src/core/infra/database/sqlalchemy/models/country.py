from sqlalchemy.schema import Column, Table
from sqlalchemy.types import Integer, String

from infra.database.sqlalchemy.sqlalchemy import metadata


countries = Table(
    'core_country',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('code', String(2), unique=True),
    Column('name', String(255), nullable=False),
)
