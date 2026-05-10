"""Add admin and accounts roles, and Department model

Revision ID: 01276ba2d282
Revises: 616d851fb8e6
Create Date: 2026-05-10 09:42:47.534515

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '01276ba2d282'
down_revision: Union[str, Sequence[str], None] = '616d851fb8e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Create departments table
    op.create_table('departments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_departments_id'), 'departments', ['id'], unique=False)
    
    # 2. Add department_id to staff_profiles using batch mode for SQLite
    with op.batch_alter_table('staff_profiles') as batch_op:
        batch_op.add_column(sa.Column('department_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_staff_profile_dept', 'departments', ['department_id'], ['id'])

    # 3. Skip altering the 'users' role column for now because SQLite doesn't 
    # support ALTER COLUMN and it's already working as a string column.
    pass


def downgrade() -> None:
    with op.batch_alter_table('staff_profiles') as batch_op:
        batch_op.drop_constraint('fk_staff_profile_dept', type_='foreignkey')
        batch_op.drop_column('department_id')
    
    op.drop_index(op.f('ix_departments_id'), table_name='departments')
    op.drop_table('departments')
