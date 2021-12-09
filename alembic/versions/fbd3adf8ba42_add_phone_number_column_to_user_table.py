"""add phone number column to user table

Revision ID: fbd3adf8ba42
Revises: 7ae3e3a1cd91
Create Date: 2021-12-09 19:23:51.176914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbd3adf8ba42'
down_revision = '7ae3e3a1cd91'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("phone_number", sa.String(), nullable=True))
    pass


def downgrade():
    op.drop_column("users", "phone_number")
    pass
