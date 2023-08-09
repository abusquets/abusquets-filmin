import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.schema import Column, Table
from sqlalchemy.types import Boolean, Integer, String, Text

from infra.database.sqlalchemy.sqlalchemy import metadata


users = Table(
    'core_user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('uuid', UUID(as_uuid=True), unique=True, default=uuid.uuid4),
    Column('first_name', String(255), nullable=False),
    Column('last_name', String(255), nullable=True),
    Column('email', String(255), unique=True, nullable=False),
    Column('password', Text(), nullable=False),
    Column('is_active', Boolean(), nullable=False, default=True),
    Column('is_admin', Boolean(), nullable=False, default=False),
)
