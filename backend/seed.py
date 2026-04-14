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

def _hash_password(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt()).decode()


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
        # 4. Default admin user
        # ------------------------------------------------------------------
        admin = db.query(User).filter(User.email == "admin@dalmiatrusts.in").first()
        if admin is None:
            hashed = _hash_password("admin123")
            admin = User(
                name="Admin",
                email="admin@dalmiatrusts.in",
                hashed_password=hashed,
                role=UserRole.admin,
                is_active=True,
            )
            db.add(admin)
            db.commit()
            print("Created admin user: admin@dalmiatrusts.in / admin123")
        else:
            print("Admin user already exists — skipping.")

        print("\nSeeding complete.")

    finally:
        db.close()


if __name__ == "__main__":
    seed()
