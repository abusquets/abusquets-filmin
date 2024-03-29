"""add filmin models

Revision ID: 978d329a4fcc
Revises: 440f205f8ac8
Create Date: 2023-08-27 07:14:21.693124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '978d329a4fcc'
down_revision = '440f205f8ac8'
branch_labels = ('filmin',)
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'filmin_collection',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.UUID(), nullable=False),  # type: ignore
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_filmin_collection')),
        sa.UniqueConstraint('uuid', name=op.f('uq_filmin_collection_uuid')),
    )
    op.create_table(
        'filmin_genre',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('code', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_filmin_genre')),
        sa.UniqueConstraint('code', name=op.f('uq_filmin_genre_code')),
    )
    op.create_table(
        'filmin_production_company',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.UUID(), nullable=False),  # type: ignore
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_filmin_production_company')),
        sa.UniqueConstraint('uuid', name=op.f('uq_filmin_production_company_uuid')),
    )
    op.create_table(
        'filmin_movie',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.UUID(), nullable=False),  # type: ignore
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('release_date', sa.Date(), nullable=True),
        sa.Column('budget', sa.BigInteger(), nullable=True),
        sa.Column('revenue', sa.BigInteger(), nullable=True),
        sa.Column('popularity', sa.Float(), nullable=True),
        sa.Column('runtime', sa.BigInteger(), nullable=True),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.Column('original_language', sa.String(length=2), nullable=True),
        sa.Column('collection_id', sa.UUID(), nullable=True),  # type: ignore
        sa.Column('overview', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ['collection_id'], ['filmin_collection.uuid'], name=op.f('fk_filmin_movie_collection_id_filmin_collection')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_filmin_movie')),
        sa.UniqueConstraint('uuid', name=op.f('uq_filmin_movie_uuid')),
    )
    op.create_table(
        'filmin_movie_genre',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('movie_id', sa.UUID(), nullable=True),  # type: ignore
        sa.Column('genre_id', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ['genre_id'], ['filmin_genre.code'], name=op.f('fk_filmin_movie_genre_genre_id_filmin_genre')
        ),
        sa.ForeignKeyConstraint(
            ['movie_id'], ['filmin_movie.uuid'], name=op.f('fk_filmin_movie_genre_movie_id_filmin_movie')
        ),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_filmin_movie_genre')),
        sa.UniqueConstraint('movie_id', 'genre_id', name='unique_filmin_movie_genre'),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('filmin_movie_genre')
    op.drop_table('filmin_movie')
    op.drop_table('filmin_production_company')
    op.drop_table('filmin_genre')
    op.drop_table('filmin_collection')
    # ### end Alembic commands ###
