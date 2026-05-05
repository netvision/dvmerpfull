"""merge heads

Revision ID: 5c2ffbd3294f
Revises: c1d2e3f4a5b6, f2d6a1b8c9e4
Create Date: 2026-05-05 12:08:37.722736

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c2ffbd3294f'
down_revision: Union[str, Sequence[str], None] = ('c1d2e3f4a5b6', 'f2d6a1b8c9e4')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
