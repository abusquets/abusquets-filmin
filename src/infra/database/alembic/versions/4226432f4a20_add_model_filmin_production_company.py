"""add model filmin.production_company

Revision ID: 4226432f4a20
Revises: e484f9d6a6af
Create Date: 2023-06-27 04:44:52.438170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4226432f4a20'
down_revision = 'e484f9d6a6af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'filmin_production_company',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_filmin_production_company')),
        sa.UniqueConstraint('uuid', name=op.f('uq_filmin_production_company_uuid')),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('filmin_production_company')
    # ### end Alembic commands ###