"""add_teaching_materials_methods_to_concepts

Revision ID: 4f77a8c2d2ef
Revises: b8509007a626
Create Date: 2026-04-21 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f77a8c2d2ef'
down_revision: Union[str, Sequence[str], None] = 'b8509007a626'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('concepts', sa.Column('teaching_materials_methods', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('concepts', 'teaching_materials_methods')
