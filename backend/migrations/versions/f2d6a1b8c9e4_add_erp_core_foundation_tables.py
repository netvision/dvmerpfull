"""add_erp_core_foundation_tables

Revision ID: f2d6a1b8c9e4
Revises: e5c1a9b4d221
Create Date: 2026-04-28 18:40:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "f2d6a1b8c9e4"
down_revision: Union[str, Sequence[str], None] = "e5c1a9b4d221"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


student_status_enum = postgresql.ENUM(
    "active", "inactive", "tc", "passout", name="studentstatus", create_type=False
)
attendance_status_enum = postgresql.ENUM(
    "present", "absent", "late", "leave", name="attendancestatus", create_type=False
)
invoice_status_enum = postgresql.ENUM(
    "draft",
    "issued",
    "partially_paid",
    "paid",
    "cancelled",
    name="invoicestatus",
    create_type=False,
)
payment_mode_enum = postgresql.ENUM(
    "cash", "bank", "upi", "card", "other", name="paymentmode", create_type=False
)


def upgrade() -> None:
    bind = op.get_bind()
    student_status_enum.create(bind, checkfirst=True)
    attendance_status_enum.create(bind, checkfirst=True)
    invoice_status_enum.create(bind, checkfirst=True)
    payment_mode_enum.create(bind, checkfirst=True)

    op.create_table(
        "academic_years",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_index(op.f("ix_academic_years_id"), "academic_years", ["id"], unique=False)

    op.create_table(
        "sections",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("class_id", "name", name="uq_sections_class_name"),
    )
    op.create_index(op.f("ix_sections_id"), "sections", ["id"], unique=False)

    op.create_table(
        "guardians",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("relation", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_guardians_id"), "guardians", ["id"], unique=False)

    op.create_table(
        "fee_heads",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("code", sa.String(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_fee_heads_id"), "fee_heads", ["id"], unique=False)

    op.create_table(
        "students",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("admission_no", sa.String(), nullable=False),
        sa.Column("roll_no", sa.String(), nullable=True),
        sa.Column("first_name", sa.String(), nullable=False),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("gender", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("section_id", sa.Integer(), nullable=True),
        sa.Column("academic_year_id", sa.Integer(), nullable=False),
        sa.Column("status", student_status_enum, nullable=False, server_default="active"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["academic_year_id"], ["academic_years.id"]),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
        sa.ForeignKeyConstraint(["section_id"], ["sections.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("admission_no"),
    )
    op.create_index(op.f("ix_students_id"), "students", ["id"], unique=False)

    op.create_table(
        "student_guardians",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("guardian_id", sa.Integer(), nullable=False),
        sa.Column("is_primary", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.ForeignKeyConstraint(["guardian_id"], ["guardians.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "guardian_id", name="uq_student_guardian_pair"),
    )
    op.create_index(op.f("ix_student_guardians_id"), "student_guardians", ["id"], unique=False)

    op.create_table(
        "attendance_sessions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("section_id", sa.Integer(), nullable=True),
        sa.Column("academic_year_id", sa.Integer(), nullable=False),
        sa.Column("attendance_date", sa.Date(), nullable=False),
        sa.Column("marked_by_id", sa.Integer(), nullable=False),
        sa.Column("marked_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["academic_year_id"], ["academic_years.id"]),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
        sa.ForeignKeyConstraint(["marked_by_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["section_id"], ["sections.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "class_id",
            "section_id",
            "academic_year_id",
            "attendance_date",
            name="uq_attendance_session_slot",
        ),
    )
    op.create_index(op.f("ix_attendance_sessions_id"), "attendance_sessions", ["id"], unique=False)

    op.create_table(
        "attendance_entries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("status", attendance_status_enum, nullable=False, server_default="present"),
        sa.Column("remarks", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["session_id"], ["attendance_sessions.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id", "student_id", name="uq_attendance_entry"),
    )
    op.create_index(op.f("ix_attendance_entries_id"), "attendance_entries", ["id"], unique=False)

    op.create_table(
        "fee_structures",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("class_id", sa.Integer(), nullable=False),
        sa.Column("academic_year_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["academic_year_id"], ["academic_years.id"]),
        sa.ForeignKeyConstraint(["class_id"], ["classes.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "class_id", "academic_year_id", name="uq_fee_structure_scope"),
    )
    op.create_index(op.f("ix_fee_structures_id"), "fee_structures", ["id"], unique=False)

    op.create_table(
        "fee_structure_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fee_structure_id", sa.Integer(), nullable=False),
        sa.Column("fee_head_id", sa.Integer(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("due_day", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["fee_head_id"], ["fee_heads.id"]),
        sa.ForeignKeyConstraint(["fee_structure_id"], ["fee_structures.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("fee_structure_id", "fee_head_id", name="uq_fee_structure_item"),
    )
    op.create_index(op.f("ix_fee_structure_items_id"), "fee_structure_items", ["id"], unique=False)

    op.create_table(
        "student_fee_assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("fee_structure_id", sa.Integer(), nullable=False),
        sa.Column("academic_year_id", sa.Integer(), nullable=False),
        sa.Column("effective_from", sa.Date(), nullable=True),
        sa.Column("effective_to", sa.Date(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.ForeignKeyConstraint(["academic_year_id"], ["academic_years.id"]),
        sa.ForeignKeyConstraint(["fee_structure_id"], ["fee_structures.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("student_id", "fee_structure_id", "academic_year_id", name="uq_student_fee_assignment"),
    )
    op.create_index(op.f("ix_student_fee_assignments_id"), "student_fee_assignments", ["id"], unique=False)

    op.create_table(
        "fee_invoices",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("invoice_no", sa.String(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("academic_year_id", sa.Integer(), nullable=False),
        sa.Column("invoice_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("total_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("discount_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("paid_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("balance_amount", sa.Numeric(precision=12, scale=2), nullable=False, server_default="0"),
        sa.Column("status", invoice_status_enum, nullable=False, server_default="issued"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["academic_year_id"], ["academic_years.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("invoice_no"),
    )
    op.create_index(op.f("ix_fee_invoices_id"), "fee_invoices", ["id"], unique=False)

    op.create_table(
        "fee_receipts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("receipt_no", sa.String(), nullable=False),
        sa.Column("invoice_id", sa.Integer(), nullable=False),
        sa.Column("student_id", sa.Integer(), nullable=False),
        sa.Column("receipt_date", sa.Date(), nullable=False),
        sa.Column("amount", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("payment_mode", payment_mode_enum, nullable=False, server_default="cash"),
        sa.Column("reference_no", sa.String(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("received_by_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["invoice_id"], ["fee_invoices.id"]),
        sa.ForeignKeyConstraint(["received_by_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["student_id"], ["students.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("receipt_no"),
    )
    op.create_index(op.f("ix_fee_receipts_id"), "fee_receipts", ["id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("actor_user_id", sa.Integer(), nullable=True),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("action", sa.String(), nullable=False),
        sa.Column("change_summary", sa.Text(), nullable=True),
        sa.Column("before_payload", sa.Text(), nullable=True),
        sa.Column("after_payload", sa.Text(), nullable=True),
        sa.Column("ip_address", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()

    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_table("audit_logs")

    op.drop_index(op.f("ix_fee_receipts_id"), table_name="fee_receipts")
    op.drop_table("fee_receipts")

    op.drop_index(op.f("ix_fee_invoices_id"), table_name="fee_invoices")
    op.drop_table("fee_invoices")

    op.drop_index(op.f("ix_student_fee_assignments_id"), table_name="student_fee_assignments")
    op.drop_table("student_fee_assignments")

    op.drop_index(op.f("ix_fee_structure_items_id"), table_name="fee_structure_items")
    op.drop_table("fee_structure_items")

    op.drop_index(op.f("ix_fee_structures_id"), table_name="fee_structures")
    op.drop_table("fee_structures")

    op.drop_index(op.f("ix_attendance_entries_id"), table_name="attendance_entries")
    op.drop_table("attendance_entries")

    op.drop_index(op.f("ix_attendance_sessions_id"), table_name="attendance_sessions")
    op.drop_table("attendance_sessions")

    op.drop_index(op.f("ix_student_guardians_id"), table_name="student_guardians")
    op.drop_table("student_guardians")

    op.drop_index(op.f("ix_students_id"), table_name="students")
    op.drop_table("students")

    op.drop_index(op.f("ix_fee_heads_id"), table_name="fee_heads")
    op.drop_table("fee_heads")

    op.drop_index(op.f("ix_guardians_id"), table_name="guardians")
    op.drop_table("guardians")

    op.drop_index(op.f("ix_sections_id"), table_name="sections")
    op.drop_table("sections")

    op.drop_index(op.f("ix_academic_years_id"), table_name="academic_years")
    op.drop_table("academic_years")

    payment_mode_enum.drop(bind, checkfirst=True)
    invoice_status_enum.drop(bind, checkfirst=True)
    attendance_status_enum.drop(bind, checkfirst=True)
    student_status_enum.drop(bind, checkfirst=True)
