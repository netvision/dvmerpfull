"""merge heads

Revision ID: 4982db7e4c20
Revises: 4f77a8c2d2ef, 9372cab1cfc2
Create Date: 2026-04-21 09:29:49.783055

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4982db7e4c20'
down_revision: Union[str, Sequence[str], None] = ('4f77a8c2d2ef', '9372cab1cfc2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
