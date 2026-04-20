"""expand_user_roles

Revision ID: 7f0f2e7b5d4c
Revises: b8509007a626
Create Date: 2026-04-20 11:30:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "7f0f2e7b5d4c"
down_revision: Union[str, Sequence[str], None] = "b8509007a626"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'subject_head'")
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'mentor'")
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'hm'")
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'principal'")
        op.execute("ALTER TYPE userrole ADD VALUE IF NOT EXISTS 'super_admin'")

    # Preserve existing privileged users when moving from legacy role naming.
    op.execute("UPDATE users SET role = 'super_admin' WHERE role = 'admin'")


def downgrade() -> None:
    """Downgrade schema."""
    # PostgreSQL enum values are not dropped here; remap role values only.
    op.execute("UPDATE users SET role = 'admin' WHERE role = 'super_admin'")
