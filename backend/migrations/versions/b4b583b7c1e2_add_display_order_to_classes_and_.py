"""Add display_order to classes and concepts

Revision ID: b4b583b7c1e2
Revises: 5c2ffbd3294f
Create Date: 2026-05-05 12:19:16.031340

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4b583b7c1e2'
down_revision: Union[str, Sequence[str], None] = '5c2ffbd3294f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('classes', sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('concepts', sa.Column('display_order', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('concepts', 'display_order')
    op.drop_column('classes', 'display_order')
