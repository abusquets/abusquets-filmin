import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, Table
from sqlalchemy.types import Integer, String

from infra.database.sqlalchemy.sqlalchemy import metadata


production_company = Table(
    'filmin_production_company',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4),
    Column('name', String(255), nullable=False),
)
