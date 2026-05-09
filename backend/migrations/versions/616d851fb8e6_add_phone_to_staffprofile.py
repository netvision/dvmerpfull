"""Add phone to StaffProfile

Revision ID: 616d851fb8e6
Revises: 966345270a17
Create Date: 2026-05-09 17:35:31.499694

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '616d851fb8e6'
down_revision: Union[str, Sequence[str], None] = '966345270a17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch_alter_table for SQLite compatibility
    op.add_column('staff_profiles', sa.Column('phone', sa.String(), nullable=True))
    
    # We skip altering the 'users' role column for now because SQLite doesn't 
    # support ALTER COLUMN and it's already working as a string column.
    pass


def downgrade() -> None:
    op.drop_column('staff_profiles', 'phone')
