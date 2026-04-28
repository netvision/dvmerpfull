"""add_concept_description

Revision ID: e5c1a9b4d221
Revises: d3b98e1c4a77
Create Date: 2026-04-28 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e5c1a9b4d221'
down_revision: Union[str, Sequence[str], None] = 'd3b98e1c4a77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('concepts', sa.Column('concept_description', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('concepts', 'concept_description')
