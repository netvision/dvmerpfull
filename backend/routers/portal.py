import tempfile
import os
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, require_admin, verify_password
from database import get_db
from models import User, UserRole, TeacherSubject, Subject, Chapter, Concept, Exhibit
from schemas import (
    TokenOut,
    UserOut,
    ChapterDetailOut,
    SubjectNestedOut,
    ClassNestedOut,
    ConceptOut,
    ExhibitOut,
    ChapterPortalSummaryOut,
    ChapterUpdateIn,
    ChapterCreateIn,
    UploadResultOut,
)
from xlsx_parser import parse_xlsx

router = APIRouter()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _check_subject_access(db: Session, user: User, subject_id: int):
    """Raise 403 if teacher doesn't have access to this subject."""
    if user.role == UserRole.admin:
        return  # admin has access to everything
    access = db.query(TeacherSubject).filter(
        TeacherSubject.teacher_id == user.id,
        TeacherSubject.subject_id == subject_id,
    ).first()
    if not access:
        raise HTTPException(status_code=403, detail="Not authorized for this subject")


def _delete_chapter_cascade(db: Session, chapter: Chapter):
    """Delete a chapter and all its concepts/exhibits."""
    for concept in db.query(Concept).filter(Concept.chapter_id == chapter.id).all():
        db.query(Exhibit).filter(Exhibit.concept_id == concept.id).delete()
        db.delete(concept)
    db.delete(chapter)
    db.flush()


def _build_chapter_detail(db: Session, chapter: Chapter) -> ChapterDetailOut:
    """Build a ChapterDetailOut from a Chapter ORM object."""
    subject = chapter.subject
    cls = subject.cls

    concepts_out = []
    for concept in chapter.concepts:
        exhibits_out = [
            ExhibitOut(
                id=ex.id,
                field_key=ex.field_key,
                field_value=ex.field_value,
            )
            for ex in concept.exhibits
        ]
        concepts_out.append(
            ConceptOut(
                id=concept.id,
                s_no=concept.s_no,
                title=concept.title,
                sessions=concept.sessions,
                learning_outcomes=concept.learning_outcomes,
                integration_other_sub=concept.integration_other_sub,
                library=concept.library,
                activity=concept.activity,
                life_lesson=concept.life_lesson,
                remarks=concept.remarks,
                exhibit_ref=concept.exhibit_ref,
                exhibits=exhibits_out,
            )
        )

    return ChapterDetailOut(
        id=chapter.id,
        title=chapter.title,
        aim=chapter.aim,
        subject=SubjectNestedOut(
            id=subject.id,
            name=subject.name,
            icon=subject.icon,
            color=subject.color,
        ),
        **{"class": ClassNestedOut(id=cls.id, name=cls.name)},
        concepts=concepts_out,
    )


# ---------------------------------------------------------------------------
# Auth routes (existing)
# ---------------------------------------------------------------------------

@router.post("/auth/login", response_model=TokenOut)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate with email (username field) and password, return JWT."""
    user: User | None = db.query(User).filter(User.email == form_data.username).first()
    if user is None or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    token = create_access_token(data={"sub": user.email})
    return TokenOut(access_token=token, token_type="bearer")


@router.get("/auth/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    """Return the currently authenticated user's profile."""
    return UserOut(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        role=current_user.role.value,
    )


# ---------------------------------------------------------------------------
# Chapter CRUD routes
# ---------------------------------------------------------------------------

@router.get("/chapters", response_model=List[ChapterPortalSummaryOut])
def list_chapters(
    class_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    List chapters. Admin gets all; teacher gets only chapters in assigned subjects.
    Optional query params: class_id, subject_id.
    """
    query = db.query(Chapter).join(Chapter.subject).join(Subject.cls)

    if current_user.role == UserRole.teacher:
        # Restrict to teacher's assigned subjects
        assigned_subject_ids = [
            ts.subject_id for ts in current_user.teacher_subjects
        ]
        query = query.filter(Chapter.subject_id.in_(assigned_subject_ids))

    if subject_id is not None:
        query = query.filter(Chapter.subject_id == subject_id)

    if class_id is not None:
        query = query.filter(Subject.class_id == class_id)

    chapters = query.order_by(Chapter.subject_id, Chapter.order_index, Chapter.id).all()

    result = []
    for chapter in chapters:
        concept_count = len(chapter.concepts)
        sessions_total = 0
        for concept in chapter.concepts:
            if concept.sessions is not None:
                try:
                    sessions_total += int(concept.sessions)
                except (ValueError, TypeError):
                    pass
        result.append(
            ChapterPortalSummaryOut(
                id=chapter.id,
                title=chapter.title,
                aim=chapter.aim,
                sessions_total=sessions_total,
                concept_count=concept_count,
                subject_name=chapter.subject.name,
                class_name=chapter.subject.cls.name,
            )
        )
    return result


@router.get("/chapters/{chapter_id}", response_model=ChapterDetailOut)
def get_chapter(
    chapter_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return full chapter detail. Teacher must own the subject."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    _check_subject_access(db, current_user, chapter.subject_id)
    return _build_chapter_detail(db, chapter)


@router.put("/chapters/{chapter_id}", response_model=ChapterDetailOut)
def update_chapter(
    chapter_id: int,
    body: ChapterUpdateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update chapter-level fields. Teacher must own the subject; admin can edit all."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    _check_subject_access(db, current_user, chapter.subject_id)

    if body.title is not None:
        chapter.title = body.title
    if body.aim is not None:
        chapter.aim = body.aim
    if body.order_index is not None:
        chapter.order_index = body.order_index

    db.commit()
    db.refresh(chapter)
    return _build_chapter_detail(db, chapter)


@router.post("/chapters", response_model=ChapterDetailOut, status_code=201)
def create_chapter(
    body: ChapterCreateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new chapter. Admin only."""
    subject = db.query(Subject).filter(Subject.id == body.subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    chapter = Chapter(
        title=body.title,
        aim=body.aim,
        subject_id=body.subject_id,
        order_index=body.order_index if body.order_index is not None else 0,
    )
    db.add(chapter)
    db.commit()
    db.refresh(chapter)
    return _build_chapter_detail(db, chapter)


@router.delete("/chapters/{chapter_id}")
def delete_chapter(
    chapter_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a chapter and cascade to concepts/exhibits. Admin only."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    _delete_chapter_cascade(db, chapter)
    db.commit()
    return {"ok": True}


# ---------------------------------------------------------------------------
# Upload route
# ---------------------------------------------------------------------------

@router.post("/upload", response_model=UploadResultOut)
async def upload_xlsx(
    file: UploadFile = File(...),
    subject_id: int = Form(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Upload an xlsx lesson plan file and upsert into DB.
    Teacher may only upload to their assigned subjects; admin can upload to any.
    """
    _check_subject_access(db, current_user, subject_id)

    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    # Save to temp file
    suffix = os.path.splitext(file.filename or "upload")[1] or ".xlsx"
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    try:
        contents = await file.read()
        with os.fdopen(tmp_fd, "wb") as tmp_file:
            tmp_file.write(contents)

        try:
            data = parse_xlsx(tmp_path)
        except Exception as exc:
            raise HTTPException(status_code=422, detail=f"Failed to parse xlsx: {exc}")
    finally:
        # Clean up temp file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

    # Delete existing chapter with same title for upsert idempotency
    existing = db.query(Chapter).filter(
        Chapter.subject_id == subject_id,
        Chapter.title == data["title"],
    ).first()
    if existing:
        _delete_chapter_cascade(db, existing)
        db.flush()

    # Create new chapter
    chapter = Chapter(
        title=data["title"],
        aim=data["aim"],
        subject_id=subject_id,
        order_index=1,
    )
    db.add(chapter)
    db.flush()

    concepts_count = 0
    exhibits_count = 0
    exhibits_map: dict = data.get("exhibits", {})

    for concept_data in data["concepts"]:
        if not concept_data.get("title"):
            continue

        concept = Concept(
            chapter_id=chapter.id,
            s_no=concept_data.get("s_no"),
            title=concept_data["title"],
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
        concepts_count += 1

        exhibit_ref = concept_data.get("exhibit_ref", "")
        if exhibit_ref and exhibit_ref in exhibits_map:
            for field_key, field_value in exhibits_map[exhibit_ref].get("fields", {}).items():
                db.add(Exhibit(
                    concept_id=concept.id,
                    field_key=field_key,
                    field_value=str(field_value) if field_value else None,
                ))
                exhibits_count += 1

    db.commit()

    return UploadResultOut(
        ok=True,
        chapter_title=data["title"],
        concepts_count=concepts_count,
        exhibits_count=exhibits_count,
    )
