"""add_pending_change_summary_to_chapters

Revision ID: d3b98e1c4a77
Revises: a11d7f6e2c3b
Create Date: 2026-04-26 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd3b98e1c4a77'
down_revision: Union[str, Sequence[str], None] = 'a11d7f6e2c3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chapters', sa.Column('pending_change_summary', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('chapters', 'pending_change_summary')
