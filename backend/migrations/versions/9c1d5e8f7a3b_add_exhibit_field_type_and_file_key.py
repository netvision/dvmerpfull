"""Add field_type and file_key columns to exhibits table.

Revision ID: 9c1d5e8f7a3b
Revises: b8509007a626
Create Date: 2026-04-20 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c1d5e8f7a3b'
down_revision = 'b8509007a626'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the enum type for field_type
    exhibit_field_type_enum = sa.Enum(
        'string', 'audio', 'image', 'video', 'link',
        name='exhibitfieldtype'
    )
    exhibit_field_type_enum.create(op.get_bind())
    
    # Add columns to exhibits table
    op.add_column('exhibits', sa.Column('field_type', exhibit_field_type_enum, nullable=False, server_default='string'))
    op.add_column('exhibits', sa.Column('file_key', sa.String(), nullable=True))
    
    # Create indexes on file_key for faster lookups
    op.create_index('ix_exhibits_file_key', 'exhibits', ['file_key'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_exhibits_file_key', table_name='exhibits')
    
    # Drop columns
    op.drop_column('exhibits', 'file_key')
    op.drop_column('exhibits', 'field_type')
    
    # Drop the enum type
    sa.Enum(
        'string', 'audio', 'image', 'video', 'link',
        name='exhibitfieldtype'
    ).drop(op.get_bind())
