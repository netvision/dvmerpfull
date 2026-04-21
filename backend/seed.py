"""
seed.py - Seed the SQLite database with lesson plan data from xlsx files.

Idempotent: safe to run multiple times.
"""
import io
import os
import sys

# Ensure imports resolve relative to this file's directory
sys.path.insert(0, os.path.dirname(__file__))

# Force UTF-8 output so Hindi/special characters print correctly on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
else:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import bcrypt as _bcrypt
from sqlalchemy import text

from database import SessionLocal, engine
from models import Base, Class, Subject, Chapter, Concept, Exhibit, User, UserRole
from xlsx_parser import parse_xlsx

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

XLSX_DIR = os.path.join(os.path.dirname(__file__), "..", )

SUBJECT_META = {
    "English":        {"icon": "📖", "color": "#4f46e5"},
    "Mathematics":    {"icon": "➗", "color": "#10b981"},
    "Science":        {"icon": "🔬", "color": "#f59e0b"},
    "Social Science": {"icon": "🌍", "color": "#ef4444"},
    "Hindi":          {"icon": "🔤", "color": "#8b5cf6"},
}

# filename (relative to XLSX_DIR) -> (class_name, subject_name, order_index)
FILE_MAP = [
    ("class6_english_chapter1.xlsx",  "Class 6", "English",        1),
    ("class6_english_poem1.xlsx",     "Class 6", "English",        2),
    ("class6_sst_chapter1.xlsx",      "Class 6", "Social Science", 1),
    ("class6_science_chapter1.xlsx",  "Class 6", "Science",        1),
    ("class6_hindi_chapter1.xlsx",    "Class 6", "Hindi",          1),
    ("class6-maths-chapter1.xlsx",    "Class 6", "Mathematics",    1),
]

DEFAULT_SUPER_ADMIN_EMAIL = os.getenv("SEED_SUPER_ADMIN_EMAIL", "admin@dalmiatrusts.in")
DEFAULT_SUPER_ADMIN_PASSWORD = os.getenv("SEED_SUPER_ADMIN_PASSWORD", "admin123")
DEFAULT_ROLE_USER_PASSWORD = os.getenv("SEED_DEFAULT_USER_PASSWORD", "welcome@123")
CREATE_ROLE_USERS = os.getenv("SEED_CREATE_ROLE_USERS", "1").strip().lower() in {"1", "true", "yes"}
FORCE_PASSWORD_RESET = os.getenv("SEED_FORCE_PASSWORD_RESET", "0").strip().lower() in {"1", "true", "yes"}

ROLE_BOOTSTRAP_USERS = [
    ("Teacher User", "teacher@dalmiatrusts.in", UserRole.teacher),
    ("Subject Head User", "subjecthead@dalmiatrusts.in", UserRole.subject_head),
    ("Mentor User", "mentor@dalmiatrusts.in", UserRole.mentor),
    ("HM User", "hm@dalmiatrusts.in", UserRole.hm),
    ("Principal User", "principal@dalmiatrusts.in", UserRole.principal),
]

def _hash_password(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt()).decode()


def _normalize_legacy_admin_role(db) -> None:
    """Normalize legacy 'admin' rows to 'super_admin' before ORM user queries.

    This protects seeding on databases that temporarily contain both enum labels
    after partial/older migrations.
    """
    dialect = db.bind.dialect.name
    if dialect == "postgresql":
        db.execute(text("""
            DO $$
            BEGIN
                IF EXISTS (
                    SELECT 1
                    FROM pg_type t
                    JOIN pg_enum e ON e.enumtypid = t.oid
                    WHERE t.typname = 'userrole' AND e.enumlabel = 'admin'
                ) AND EXISTS (
                    SELECT 1
                    FROM pg_type t
                    JOIN pg_enum e ON e.enumtypid = t.oid
                    WHERE t.typname = 'userrole' AND e.enumlabel = 'super_admin'
                ) THEN
                    UPDATE users SET role = 'super_admin' WHERE role = 'admin';
                END IF;
            END $$;
        """))
    else:
        db.execute(text("UPDATE users SET role = 'super_admin' WHERE role = 'admin'"))
    db.flush()


def _upsert_user(db, *, name: str, email: str, role: UserRole, password: str) -> tuple[User, bool]:
    """Create or update a user with the provided role and password."""
    user = db.query(User).filter(User.email == email).first()
    created = False
    if user is None:
        user = User(
            name=name,
            email=email,
            hashed_password=_hash_password(password),
            role=role,
            is_active=True,
        )
        db.add(user)
        created = True
    else:
        user.name = name
        user.role = role
        user.is_active = True
        if FORCE_PASSWORD_RESET:
            user.hashed_password = _hash_password(password)
    db.flush()
    return user, created


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_or_create_class(db, name: str) -> Class:
    obj = db.query(Class).filter(Class.name == name).first()
    if obj is None:
        obj = Class(name=name)
        db.add(obj)
        db.flush()
    return obj


def get_or_create_subject(db, name: str, class_id: int) -> Subject:
    obj = db.query(Subject).filter(
        Subject.name == name,
        Subject.class_id == class_id,
    ).first()
    if obj is None:
        meta = SUBJECT_META.get(name, {})
        obj = Subject(
            name=name,
            icon=meta.get("icon"),
            color=meta.get("color"),
            class_id=class_id,
        )
        db.add(obj)
        db.flush()
    else:
        # Update icon/color in case they changed
        meta = SUBJECT_META.get(name, {})
        obj.icon = meta.get("icon")
        obj.color = meta.get("color")
        db.flush()
    return obj


def delete_chapter_cascade(db, chapter: Chapter):
    """Delete a chapter and all its concepts/exhibits."""
    for concept in db.query(Concept).filter(Concept.chapter_id == chapter.id).all():
        db.query(Exhibit).filter(Exhibit.concept_id == concept.id).delete()
        db.delete(concept)
    db.delete(chapter)
    db.flush()


# ---------------------------------------------------------------------------
# Main seed routine
# ---------------------------------------------------------------------------

def seed():
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        _normalize_legacy_admin_role(db)
        db.commit()

        # ------------------------------------------------------------------
        # 1. Classes
        # ------------------------------------------------------------------
        cls6 = get_or_create_class(db, "Class 6")
        get_or_create_class(db, "Class 7")   # stub
        get_or_create_class(db, "Class 8")   # stub
        db.commit()

        # ------------------------------------------------------------------
        # 2. Subjects (for Class 6 — the ones we have data for)
        # ------------------------------------------------------------------
        subjects: dict[str, Subject] = {}
        for subject_name in SUBJECT_META:
            subj = get_or_create_subject(db, subject_name, cls6.id)
            subjects[subject_name] = subj
        db.commit()

        # ------------------------------------------------------------------
        # 3. xlsx files -> chapters / concepts / exhibits
        # ------------------------------------------------------------------
        for filename, class_name, subject_name, order_index in FILE_MAP:
            filepath = os.path.join(XLSX_DIR, filename)
            print(f"Seeding {class_name} {subject_name} ({filename})...")

            if not os.path.exists(filepath):
                print(f"  WARNING: file not found: {filepath} — skipping.")
                continue

            data = parse_xlsx(filepath)
            subject = subjects[subject_name]

            # Delete existing chapter(s) with same title for idempotency
            existing = db.query(Chapter).filter(
                Chapter.subject_id == subject.id,
                Chapter.title == data["title"],
            ).all()
            for ch in existing:
                delete_chapter_cascade(db, ch)
            db.flush()

            # Create Chapter
            chapter = Chapter(
                title=data["title"],
                aim=data["aim"],
                subject_id=subject.id,
                order_index=order_index,
            )
            db.add(chapter)
            db.flush()
            print(f"  Chapter: '{chapter.title}' (id={chapter.id})")

            # Create Concepts + Exhibits
            exhibits_map: dict = data.get("exhibits", {})
            concept_count = 0
            exhibit_count = 0

            for concept_data in data["concepts"]:
                title = concept_data.get("title") or ""
                if not title:
                    continue  # skip completely empty concept rows

                concept = Concept(
                    chapter_id=chapter.id,
                    s_no=concept_data.get("s_no"),
                    title=title,
                    sessions=concept_data.get("sessions"),
                    learning_outcomes=concept_data.get("learning_outcomes"),
                    integration_other_sub=concept_data.get("integration_other_sub"),
                    teaching_materials_methods=concept_data.get("teaching_materials_methods"),
                    library=concept_data.get("library"),
                    activity=concept_data.get("activity"),
                    life_lesson=concept_data.get("life_lesson"),
                    remarks=concept_data.get("remarks"),
                    exhibit_ref=concept_data.get("exhibit_ref"),
                )
                db.add(concept)
                db.flush()
                concept_count += 1

                # Link exhibits
                exhibit_ref = concept_data.get("exhibit_ref", "")
                if exhibit_ref and exhibit_ref in exhibits_map:
                    exhibit_data = exhibits_map[exhibit_ref]
                    fields: dict = exhibit_data.get("fields", {})
                    for idx, (field_key, field_value) in enumerate(fields.items()):
                        if not field_key:
                            continue
                        exhibit = Exhibit(
                            concept_id=concept.id,
                            field_key=field_key,
                            field_value=str(field_value) if field_value is not None else None,
                            sort_order=idx,
                        )
                        db.add(exhibit)
                        exhibit_count += 1

            db.commit()
            print(f"  -> {concept_count} concepts, {exhibit_count} exhibit rows")

        # ------------------------------------------------------------------
        # 4. User bootstrap
        # ------------------------------------------------------------------
        super_admin, was_created = _upsert_user(
            db,
            name="Super Admin",
            email=DEFAULT_SUPER_ADMIN_EMAIL,
            role=UserRole.super_admin,
            password=DEFAULT_SUPER_ADMIN_PASSWORD,
        )
        db.commit()
        if was_created:
            print(f"Created super_admin user: {super_admin.email} / {DEFAULT_SUPER_ADMIN_PASSWORD}")
        else:
            print(f"Updated super_admin user: {super_admin.email}")

        if CREATE_ROLE_USERS:
            for name, email, role in ROLE_BOOTSTRAP_USERS:
                _, created = _upsert_user(
                    db,
                    name=name,
                    email=email,
                    role=role,
                    password=DEFAULT_ROLE_USER_PASSWORD,
                )
                msg = "Created" if created else "Updated"
                print(f"{msg} {role.value} user: {email}")
            db.commit()
            print(f"Role users password: {DEFAULT_ROLE_USER_PASSWORD}")
        else:
            print("Skipped role user creation (SEED_CREATE_ROLE_USERS is false).")

        print("\nSeeding complete.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
