"""add_website_cms_tables

Revision ID: aac2d0e9f3b1
Revises: e5c1a9b4d221
Create Date: 2026-04-30 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "aac2d0e9f3b1"
down_revision: Union[str, Sequence[str], None] = "e5c1a9b4d221"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


news_status_enum = postgresql.ENUM(
    "draft",
    "published",
    "archived",
    name="newsstatus",
    create_type=False,
)
event_status_enum = postgresql.ENUM(
    "upcoming",
    "ongoing",
    "completed",
    "cancelled",
    name="eventstatus",
    create_type=False,
)


def upgrade() -> None:
    bind = op.get_bind()
    news_status_enum.create(bind, checkfirst=True)
    event_status_enum.create(bind, checkfirst=True)

    op.create_table(
        "cms_categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_cms_categories_id"), "cms_categories", ["id"], unique=False)

    op.create_table(
        "cms_news",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("excerpt", sa.Text(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("featured_image_url", sa.String(), nullable=True),
        sa.Column("author_id", sa.Integer(), nullable=True),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("status", news_status_enum, nullable=False, server_default="draft"),
        sa.Column("views", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["category_id"], ["cms_categories.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_cms_news_id"), "cms_news", ["id"], unique=False)

    op.create_table(
        "cms_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("location", sa.String(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("featured_image_url", sa.String(), nullable=True),
        sa.Column("organizer_id", sa.Integer(), nullable=True),
        sa.Column("capacity", sa.Integer(), nullable=True),
        sa.Column("registered_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", event_status_enum, nullable=False, server_default="upcoming"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["organizer_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_cms_events_id"), "cms_events", ["id"], unique=False)

    op.create_table(
        "cms_achievers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("photo_url", sa.String(), nullable=True),
        sa.Column("achievement", sa.Text(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("display_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cms_achievers_id"), "cms_achievers", ["id"], unique=False)

    op.create_table(
        "cms_contact_submissions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_cms_contact_submissions_id"), "cms_contact_submissions", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_cms_contact_submissions_id"), table_name="cms_contact_submissions")
    op.drop_table("cms_contact_submissions")
    op.drop_index(op.f("ix_cms_achievers_id"), table_name="cms_achievers")
    op.drop_table("cms_achievers")
    op.drop_index(op.f("ix_cms_events_id"), table_name="cms_events")
    op.drop_table("cms_events")
    op.drop_index(op.f("ix_cms_news_id"), table_name="cms_news")
    op.drop_table("cms_news")
    op.drop_index(op.f("ix_cms_categories_id"), table_name="cms_categories")
    op.drop_table("cms_categories")
    news_status_enum.drop(op.get_bind(), checkfirst=True)
    event_status_enum.drop(op.get_bind(), checkfirst=True)
