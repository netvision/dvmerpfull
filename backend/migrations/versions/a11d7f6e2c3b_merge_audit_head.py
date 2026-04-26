"""merge audit head

Revision ID: a11d7f6e2c3b
Revises: 4982db7e4c20, 4f2c7b1a9d21
Create Date: 2026-04-26 13:00:00.000000

"""
from typing import Sequence, Union


# revision identifiers, used by Alembic.
revision: str = 'a11d7f6e2c3b'
down_revision: Union[str, Sequence[str], None] = ('4982db7e4c20', '4f2c7b1a9d21')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
