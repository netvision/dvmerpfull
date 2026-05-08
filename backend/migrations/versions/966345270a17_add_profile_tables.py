"""Add profile tables

Revision ID: 966345270a17
Revises: b4b583b7c1e2
Create Date: 2026-05-08 08:46:42.066416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '966345270a17'
down_revision: Union[str, Sequence[str], None] = 'b4b583b7c1e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('staff_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('staff_code', sa.String(), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=True),
    sa.Column('gender', sa.String(), nullable=True),
    sa.Column('blood_group', sa.String(), nullable=True),
    sa.Column('marital_status', sa.String(), nullable=True),
    sa.Column('department', sa.String(), nullable=True),
    sa.Column('designation', sa.String(), nullable=True),
    sa.Column('joining_date', sa.Date(), nullable=True),
    sa.Column('address', sa.Text(), nullable=True),
    sa.Column('city', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('nationality', sa.String(), nullable=True),
    sa.Column('qualification', sa.String(), nullable=True),
    sa.Column('bank_name', sa.String(), nullable=True),
    sa.Column('account_no', sa.String(), nullable=True),
    sa.Column('ifsc_code', sa.String(), nullable=True),
    sa.Column('pan_no', sa.String(), nullable=True),
    sa.Column('aadhaar_no', sa.String(), nullable=True),
    sa.Column('pf_no', sa.String(), nullable=True),
    sa.Column('esi_no', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_staff_profiles_id'), 'staff_profiles', ['id'], unique=False)
    op.create_index(op.f('ix_staff_profiles_staff_code'), 'staff_profiles', ['staff_code'], unique=True)

    op.create_table('student_profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=False),
    sa.Column('blood_group', sa.String(), nullable=True),
    sa.Column('category', sa.String(), nullable=True),
    sa.Column('religion', sa.String(), nullable=True),
    sa.Column('nationality', sa.String(), nullable=True),
    sa.Column('mother_tongue', sa.String(), nullable=True),
    sa.Column('previous_school', sa.String(), nullable=True),
    sa.Column('height', sa.Float(), nullable=True),
    sa.Column('weight', sa.Float(), nullable=True),
    sa.Column('vision', sa.String(), nullable=True),
    sa.Column('is_transport', sa.Boolean(), nullable=True),
    sa.Column('pickup_route', sa.String(), nullable=True),
    sa.Column('drop_route', sa.String(), nullable=True),
    sa.Column('bank_name', sa.String(), nullable=True),
    sa.Column('account_no', sa.String(), nullable=True),
    sa.Column('ifsc_code', sa.String(), nullable=True),
    sa.Column('aadhaar_no', sa.String(), nullable=True),
    sa.Column('pen_no', sa.String(), nullable=True),
    sa.Column('apaar_id', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('student_id')
    )
    op.create_index(op.f('ix_student_profiles_id'), 'student_profiles', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_student_profiles_id'), table_name='student_profiles')
    op.drop_table('student_profiles')
    op.drop_index(op.f('ix_staff_profiles_staff_code'), table_name='staff_profiles')
    op.drop_index(op.f('ix_staff_profiles_id'), table_name='staff_profiles')
    op.drop_table('staff_profiles')
