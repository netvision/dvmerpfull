"""add_chapter_approval_fields

Revision ID: 4f2c7b1a9d21
Revises: b8509007a626
Create Date: 2026-04-26 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4f2c7b1a9d21'
down_revision: Union[str, Sequence[str], None] = 'b8509007a626'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('chapters', sa.Column('is_approved', sa.Boolean(), nullable=False, server_default=sa.true()))
    op.add_column('chapters', sa.Column('approval_requested_by_id', sa.Integer(), nullable=True))
    op.add_column('chapters', sa.Column('approved_by_id', sa.Integer(), nullable=True))
    op.add_column('chapters', sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True))
    op.alter_column('chapters', 'is_approved', server_default=None)


def downgrade() -> None:
    op.drop_column('chapters', 'approved_at')
    op.drop_column('chapters', 'approved_by_id')
    op.drop_column('chapters', 'approval_requested_by_id')
    op.drop_column('chapters', 'is_approved')
