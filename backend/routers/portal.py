import tempfile
import os
import uuid
import shutil
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request, UploadFile, File, Form, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, require_admin, verify_password
from config import UPLOADS_DIR
from database import get_db
from limiter import limiter
from models import User, UserRole, TeacherSubject, Subject, Class, Chapter, Concept, Exhibit, ConceptImage
from schemas import (
    TokenOut,
    UserOut,
    ChapterDetailOut,
    SubjectNestedOut,
    SubjectCreateIn,
    SubjectUpdateIn,
    SubjectFullOut,
    ClassNestedOut,
    ConceptOut,
    ConceptImageOut,
    ExhibitOut,
    ChapterPortalSummaryOut,
    ChapterUpdateIn,
    ChapterCreateIn,
    UploadResultOut,
    ConceptUpdateIn,
    ConceptCreateIn,
    ExhibitUpdateIn,
    ExhibitCreateIn,
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
        ordered_exhibits = (
            db.query(Exhibit)
            .filter(Exhibit.concept_id == concept.id)
            .order_by(Exhibit.sort_order)
            .all()
        )
        exhibits_out = [
            ExhibitOut(
                id=ex.id,
                field_key=ex.field_key,
                field_value=ex.field_value,
                sort_order=ex.sort_order,
            )
            for ex in ordered_exhibits
        ]
        ordered_images = (
            db.query(ConceptImage)
            .filter(ConceptImage.concept_id == concept.id)
            .order_by(ConceptImage.sort_order)
            .all()
        )
        images_out = [_build_image_out(img) for img in ordered_images]
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
                images=images_out,
            )
        )

    return ChapterDetailOut(
        id=chapter.id,
        title=chapter.title,
        aim=chapter.aim,
        pdf_url=f"/uploads/{chapter.pdf_filename}" if chapter.pdf_filename else None,
        subject=SubjectNestedOut(
            id=subject.id,
            name=subject.name,
            icon=subject.icon,
            color=subject.color,
            class_name=cls.name,
            class_id=cls.id,
        ),
        **{"class": ClassNestedOut(id=cls.id, name=cls.name)},
        concepts=concepts_out,
    )


# ---------------------------------------------------------------------------
# Auth routes (existing)
# ---------------------------------------------------------------------------

@router.post("/auth/login", response_model=TokenOut)
@limiter.limit("10/minute")
def login(
    request: Request,
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
# Teacher utility
# ---------------------------------------------------------------------------

@router.get("/my-subjects", response_model=List[SubjectNestedOut])
def my_subjects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return subjects assigned to the current teacher (or all subjects for admin)."""
    if current_user.role == UserRole.admin:
        rows = db.query(Subject).join(Subject.cls).order_by(Subject.id).all()
    else:
        assigned_ids = [ts.subject_id for ts in current_user.teacher_subjects]
        if not assigned_ids:
            return []
        rows = db.query(Subject).filter(Subject.id.in_(assigned_ids)).join(Subject.cls).order_by(Subject.id).all()
    return [
        SubjectNestedOut(
            id=s.id,
            name=s.name,
            icon=s.icon,
            color=s.color,
            class_name=s.cls.name if s.cls else None,
            class_id=s.cls.id if s.cls else None,
        )
        for s in rows
    ]


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
                subject_id=chapter.subject.id,
                subject_name=chapter.subject.name,
                class_id=chapter.subject.cls.id,
                class_name=chapter.subject.cls.name,
                pdf_url=f"/uploads/{chapter.pdf_filename}" if chapter.pdf_filename else None,
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
    if body.subject_id is not None:
        new_subject = db.query(Subject).filter(Subject.id == body.subject_id).first()
        if new_subject is None:
            raise HTTPException(status_code=404, detail="Subject not found")
        _check_subject_access(db, current_user, body.subject_id)
        chapter.subject_id = body.subject_id

    db.commit()
    db.refresh(chapter)
    return _build_chapter_detail(db, chapter)


@router.post("/chapters", response_model=ChapterDetailOut, status_code=201)
def create_chapter(
    body: ChapterCreateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new chapter. Teacher may only create in their assigned subjects."""
    _check_subject_access(db, current_user, body.subject_id)
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


@router.post("/chapters/{chapter_id}/pdf")
async def upload_chapter_pdf(
    chapter_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload or replace the PDF file for a chapter. Teacher must own the subject."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    _check_subject_access(db, current_user, chapter.subject_id)

    fname = (file.filename or "").lower()
    if not fname.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only .pdf files are accepted.")
    ct = (file.content_type or "").split(";")[0].strip()
    if ct and ct not in {"application/pdf", "application/octet-stream"}:
        raise HTTPException(status_code=415, detail=f"Unsupported content type '{ct}'.")

    contents = await file.read()
    if len(contents) > 50 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF exceeds the 50 MB size limit.")

    os.makedirs(UPLOADS_DIR, exist_ok=True)

    # Remove old PDF if replacing
    if chapter.pdf_filename:
        old_path = os.path.join(UPLOADS_DIR, chapter.pdf_filename)
        if os.path.exists(old_path):
            os.remove(old_path)

    unique_name = f"chapter_{chapter_id}_{uuid.uuid4().hex}.pdf"
    with open(os.path.join(UPLOADS_DIR, unique_name), "wb") as f:
        f.write(contents)

    chapter.pdf_filename = unique_name
    db.commit()
    return {"pdf_url": f"/uploads/{unique_name}"}


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

    # ── Validate uploaded file ─────────────────────────────────────────────
    _XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    _ALLOWED_MIME = {_XLSX_MIME, "application/octet-stream", "application/zip"}
    _MAX_BYTES = 10 * 1024 * 1024  # 10 MB

    fname = (file.filename or "").lower()
    if not fname.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only .xlsx files are accepted.")
    ct = (file.content_type or "").split(";")[0].strip()
    if ct and ct not in _ALLOWED_MIME:
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported content type '{ct}'. Upload an .xlsx file.",
        )

    # Save to temp file
    suffix = ".xlsx"
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    try:
        contents = await file.read()
        if len(contents) > _MAX_BYTES:
            raise HTTPException(status_code=413, detail="File exceeds the 10 MB size limit.")
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
            for idx, (field_key, field_value) in enumerate(exhibits_map[exhibit_ref].get("fields", {}).items()):
                db.add(Exhibit(
                    concept_id=concept.id,
                    field_key=field_key,
                    field_value=str(field_value) if field_value is not None else None,
                    sort_order=idx,
                ))
                exhibits_count += 1

    db.commit()

    return UploadResultOut(
        ok=True,
        chapter_title=data["title"],
        concepts_count=concepts_count,
        exhibits_count=exhibits_count,
    )


# ---------------------------------------------------------------------------
# Concept CRUD routes
# ---------------------------------------------------------------------------

def _build_image_out(img: ConceptImage) -> ConceptImageOut:
    """Build a ConceptImageOut from a ConceptImage ORM object."""
    return ConceptImageOut.model_validate({
        "id": img.id,
        "filename": img.filename,
        "original_name": img.original_name,
        "sort_order": img.sort_order,
        "url": f"/uploads/{img.filename}",
    })


def _build_concept_out(db: Session, concept: Concept) -> ConceptOut:
    """Build a ConceptOut from a Concept ORM object."""
    ordered_exhibits = (
        db.query(Exhibit)
        .filter(Exhibit.concept_id == concept.id)
        .order_by(Exhibit.sort_order)
        .all()
    )
    exhibits_out = [
        ExhibitOut(
            id=ex.id,
            field_key=ex.field_key,
            field_value=ex.field_value,
            sort_order=ex.sort_order,
        )
        for ex in ordered_exhibits
    ]
    ordered_images = (
        db.query(ConceptImage)
        .filter(ConceptImage.concept_id == concept.id)
        .order_by(ConceptImage.sort_order)
        .all()
    )
    images_out = [_build_image_out(img) for img in ordered_images]
    return ConceptOut(
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
        images=images_out,
    )


def _get_concept_subject_id(db: Session, concept_id: int) -> int:
    """Return subject_id for a concept's chapter, or raise 404."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    chapter = db.query(Chapter).filter(Chapter.id == concept.chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter.subject_id


@router.put("/concepts/{concept_id}", response_model=ConceptOut)
def update_concept(
    concept_id: int,
    body: ConceptUpdateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update concept fields. Teacher must own the subject; admin can edit all."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    subject_id = _get_concept_subject_id(db, concept_id)
    _check_subject_access(db, current_user, subject_id)

    if body.s_no is not None:
        concept.s_no = body.s_no
    if body.title is not None:
        concept.title = body.title
    if body.sessions is not None:
        concept.sessions = body.sessions
    if body.learning_outcomes is not None:
        concept.learning_outcomes = body.learning_outcomes
    if body.integration_other_sub is not None:
        concept.integration_other_sub = body.integration_other_sub
    if body.library is not None:
        concept.library = body.library
    if body.activity is not None:
        concept.activity = body.activity
    if body.life_lesson is not None:
        concept.life_lesson = body.life_lesson
    if body.remarks is not None:
        concept.remarks = body.remarks
    if body.exhibit_ref is not None:
        concept.exhibit_ref = body.exhibit_ref

    db.commit()
    db.refresh(concept)
    return _build_concept_out(db, concept)


@router.delete("/concepts/{concept_id}")
def delete_concept(
    concept_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a concept and its exhibits. Admin only."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    db.query(Exhibit).filter(Exhibit.concept_id == concept.id).delete()
    db.delete(concept)
    db.commit()
    return {"ok": True}


@router.post("/concepts", response_model=ConceptOut, status_code=201)
def create_concept(
    body: ConceptCreateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new concept inside a chapter. Teacher must own the subject."""
    chapter = db.query(Chapter).filter(Chapter.id == body.chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    _check_subject_access(db, current_user, chapter.subject_id)

    concept = Concept(
        chapter_id=body.chapter_id,
        s_no=body.s_no,
        title=body.title,
        sessions=body.sessions,
        learning_outcomes=body.learning_outcomes,
        integration_other_sub=body.integration_other_sub,
        library=body.library,
        activity=body.activity,
        life_lesson=body.life_lesson,
        remarks=body.remarks,
        exhibit_ref=body.exhibit_ref,
    )
    db.add(concept)
    db.commit()
    db.refresh(concept)
    return _build_concept_out(db, concept)


# ---------------------------------------------------------------------------
# Exhibit CRUD routes
# ---------------------------------------------------------------------------

@router.put("/exhibits/{exhibit_id}", response_model=ExhibitOut)
def update_exhibit(
    exhibit_id: int,
    body: ExhibitUpdateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an exhibit. Teacher must own the subject via concept->chapter->subject."""
    exhibit = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")

    subject_id = _get_concept_subject_id(db, exhibit.concept_id)
    _check_subject_access(db, current_user, subject_id)

    if body.field_key is not None:
        exhibit.field_key = body.field_key
    if body.field_value is not None:
        exhibit.field_value = body.field_value

    db.commit()
    db.refresh(exhibit)
    return ExhibitOut(
        id=exhibit.id,
        field_key=exhibit.field_key,
        field_value=exhibit.field_value,
        sort_order=exhibit.sort_order,
    )


@router.delete("/exhibits/{exhibit_id}")
def delete_exhibit(
    exhibit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an exhibit. Teacher must own the subject."""
    exhibit = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")

    subject_id = _get_concept_subject_id(db, exhibit.concept_id)
    _check_subject_access(db, current_user, subject_id)

    db.delete(exhibit)
    db.commit()
    return {"ok": True}


@router.post("/concepts/{concept_id}/exhibits", response_model=ExhibitOut, status_code=201)
def create_exhibit(
    concept_id: int,
    body: ExhibitCreateIn,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new exhibit for a concept. Teacher must own the subject."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    subject_id = _get_concept_subject_id(db, concept_id)
    _check_subject_access(db, current_user, subject_id)

    exhibit = Exhibit(
        concept_id=concept_id,
        field_key=body.field_key,
        field_value=body.field_value,
        sort_order=body.sort_order if body.sort_order is not None else 0,
    )
    db.add(exhibit)
    db.commit()
    db.refresh(exhibit)
    return ExhibitOut(
        id=exhibit.id,
        field_key=exhibit.field_key,
        field_value=exhibit.field_value,
        sort_order=exhibit.sort_order,
    )


# ---------------------------------------------------------------------------
# Concept Image routes
# ---------------------------------------------------------------------------

@router.post("/concepts/{concept_id}/images", response_model=List[ConceptImageOut], status_code=201)
async def upload_concept_images(
    concept_id: int,
    files: List[UploadFile] = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload one or more images for a concept. Teacher must own the subject."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    subject_id = _get_concept_subject_id(db, concept_id)
    _check_subject_access(db, current_user, subject_id)

    os.makedirs(UPLOADS_DIR, exist_ok=True)

    # Determine starting sort_order (append after existing images)
    existing_count = db.query(ConceptImage).filter(ConceptImage.concept_id == concept_id).count()

    created: List[ConceptImageOut] = []
    for idx, upload in enumerate(files):
        if not (upload.content_type or "").startswith("image/"):
            raise HTTPException(
                status_code=422,
                detail=f"File '{upload.filename}' is not an image (content_type: {upload.content_type})",
            )

        original_name = upload.filename or "image"
        ext = Path(original_name).suffix
        stored_filename = f"{uuid.uuid4().hex}{ext}"
        dest_path = os.path.join(UPLOADS_DIR, stored_filename)

        contents = await upload.read()
        with open(dest_path, "wb") as f:
            f.write(contents)

        img = ConceptImage(
            concept_id=concept_id,
            filename=stored_filename,
            original_name=original_name,
            sort_order=existing_count + idx,
        )
        db.add(img)
        db.flush()
        created.append(_build_image_out(img))

    db.commit()
    return created


@router.delete("/images/{image_id}")
def delete_concept_image(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a concept image (disk + DB row). Teacher must own the subject."""
    img = db.query(ConceptImage).filter(ConceptImage.id == image_id).first()
    if img is None:
        raise HTTPException(status_code=404, detail="Image not found")

    subject_id = _get_concept_subject_id(db, img.concept_id)
    _check_subject_access(db, current_user, subject_id)

    # Remove file from disk (ignore if already missing)
    file_path = os.path.join(UPLOADS_DIR, img.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    db.delete(img)
    db.commit()
    return {"ok": True}


@router.put("/images/{image_id}", response_model=ConceptImageOut)
def update_concept_image(
    image_id: int,
    sort_order: int = Body(..., embed=True),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update sort_order of a concept image. Teacher must own the subject."""
    img = db.query(ConceptImage).filter(ConceptImage.id == image_id).first()
    if img is None:
        raise HTTPException(status_code=404, detail="Image not found")

    subject_id = _get_concept_subject_id(db, img.concept_id)
    _check_subject_access(db, current_user, subject_id)

    img.sort_order = sort_order
    db.commit()
    db.refresh(img)
    return _build_image_out(img)


# ---------------------------------------------------------------------------
# Subject CRUD routes (admin only)
# ---------------------------------------------------------------------------

def _subject_to_out(subject: Subject) -> SubjectFullOut:
    return SubjectFullOut(
        id=subject.id,
        name=subject.name,
        icon=subject.icon,
        color=subject.color,
        class_id=subject.class_id,
        class_name=subject.cls.name,
    )


@router.get("/subjects", response_model=List[SubjectFullOut])
def list_subjects_portal(
    class_id: Optional[int] = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Return all subjects, optionally filtered by class. Admin only."""
    query = db.query(Subject)
    if class_id is not None:
        query = query.filter(Subject.class_id == class_id)
    subjects = query.order_by(Subject.class_id, Subject.id).all()
    return [_subject_to_out(s) for s in subjects]


@router.post("/subjects", response_model=SubjectFullOut, status_code=201)
def create_subject(
    body: SubjectCreateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new subject. Admin only."""
    cls = db.query(Class).filter(Class.id == body.class_id).first()
    if cls is None:
        raise HTTPException(status_code=404, detail="Class not found")
    subject = Subject(
        name=body.name,
        class_id=body.class_id,
        icon=body.icon,
        color=body.color,
    )
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return _subject_to_out(subject)


@router.put("/subjects/{subject_id}", response_model=SubjectFullOut)
def update_subject(
    subject_id: int,
    body: SubjectUpdateIn,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update a subject. Admin only."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    if body.name is not None:
        subject.name = body.name
    if body.icon is not None:
        subject.icon = body.icon
    if body.color is not None:
        subject.color = body.color
    if body.class_id is not None:
        cls = db.query(Class).filter(Class.id == body.class_id).first()
        if cls is None:
            raise HTTPException(status_code=404, detail="Class not found")
        subject.class_id = body.class_id
    db.commit()
    db.refresh(subject)
    return _subject_to_out(subject)


@router.delete("/subjects/{subject_id}")
def delete_subject(
    subject_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a subject. Admin only. Blocked if chapters exist under it."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")
    chapter_count = db.query(Chapter).filter(Chapter.subject_id == subject_id).count()
    if chapter_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete: {chapter_count} chapter(s) exist under this subject. Delete chapters first.",
        )
    db.query(TeacherSubject).filter(TeacherSubject.subject_id == subject_id).delete()
    db.delete(subject)
    db.commit()
    return {"ok": True}
