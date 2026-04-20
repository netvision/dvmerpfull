"""Merge multiple heads

Revision ID: 9372cab1cfc2
Revises: 7f0f2e7b5d4c, 9c1d5e8f7a3b
Create Date: 2026-04-20 13:48:54.604098

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9372cab1cfc2'
down_revision: Union[str, Sequence[str], None] = ('7f0f2e7b5d4c', '9c1d5e8f7a3b')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
