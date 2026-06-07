import io
import json
import os
import re
import tempfile
import uuid
import shutil
import zipfile
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from posixpath import normpath
from typing import List, Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Request, UploadFile, File, Form, status
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import Date, DateTime, Integer, Numeric, text
from sqlalchemy.orm import Session

from audit import write_audit_log
from auth import (
    create_access_token,
    get_current_user,
    get_role_capabilities,
    has_admin_access,
    has_subject_scoped_access,
    hash_password,
    require_admin,
    verify_password,
)
from config import UPLOADS_DIR
from database import Base, get_db
from limiter import limiter
from models import User, UserRole, TeacherSubject, Subject, Class, Chapter, Concept, Exhibit, ConceptImage, ExhibitFieldType
from schemas import (
    TokenOut,
    UserOut,
    RoleCapabilitiesOut,
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
    ChangePasswordIn,
)
from xlsx_parser import parse_xlsx

router = APIRouter()

BACKUP_FORMAT_VERSION = 1


def _safe_upload_name(filename: Optional[str]) -> str:
    original_name = filename or "upload"
    suffix = Path(original_name).suffix.lower()
    stem = Path(original_name).stem or "upload"
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", stem).strip("._") or "upload"
    return f"{uuid.uuid4()}_{safe_stem}{suffix}"


def _client_ip(request: Optional[Request]) -> Optional[str]:
    return request.client.host if request and request.client else None


def _write_security_event(
    db: Session,
    *,
    request: Optional[Request],
    action: str,
    entity_id: str,
    actor_user_id: Optional[int] = None,
    change_summary: Optional[str] = None,
    payload: Optional[dict] = None,
) -> None:
    write_audit_log(
        db,
        actor_user_id=actor_user_id,
        entity_type="security_event",
        entity_id=entity_id,
        action=action,
        change_summary=change_summary,
        after_payload=payload,
        ip_address=_client_ip(request),
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != UserRole.super_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required",
        )
    return current_user


def _serialize_db_value(value):
    if value is None:
        return None
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if hasattr(value, "value"):
        return value.value
    return value


def _deserialize_db_value(column, value):
    if value is None:
        return None
    column_type = column.type
    if isinstance(column_type, DateTime):
        return datetime.fromisoformat(value)
    if isinstance(column_type, Date):
        return date.fromisoformat(value)
    if isinstance(column_type, Numeric):
        return Decimal(str(value))
    return value


def _export_database(db: Session) -> dict:
    tables = {}
    for table in Base.metadata.sorted_tables:
        rows = []
        for row in db.execute(table.select()).mappings():
            rows.append({
                column.name: _serialize_db_value(row[column.name])
                for column in table.columns
            })
        tables[table.name] = rows
    return {
        "format": "dvm-lesson-portal-db-json",
        "version": BACKUP_FORMAT_VERSION,
        "tables": tables,
    }


def _restore_database(db: Session, payload: dict) -> int:
    if payload.get("version") != BACKUP_FORMAT_VERSION or "tables" not in payload:
        raise HTTPException(status_code=400, detail="Unsupported backup database format")

    restored_tables = 0
    try:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())

        for table in Base.metadata.sorted_tables:
            rows = payload["tables"].get(table.name, [])
            if not rows:
                continue
            converted_rows = [
                {
                    column.name: _deserialize_db_value(column, row.get(column.name))
                    for column in table.columns
                }
                for row in rows
            ]
            db.execute(table.insert(), converted_rows)
            restored_tables += 1

        if db.bind and db.bind.dialect.name == "postgresql":
            _reset_postgres_sequences(db)
        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Database restore failed: {exc}") from exc

    return restored_tables


def _reset_postgres_sequences(db: Session) -> None:
    for table in Base.metadata.sorted_tables:
        for column in table.primary_key.columns:
            if not isinstance(column.type, Integer):
                continue
            sequence = db.execute(
                text("SELECT pg_get_serial_sequence(:table_name, :column_name)"),
                {"table_name": table.name, "column_name": column.name},
            ).scalar()
            if sequence:
                db.execute(
                    text(
                        "SELECT setval(:sequence_name, "
                        f"COALESCE((SELECT MAX({column.name}) FROM {table.name}), 1), true)"
                    ),
                    {"sequence_name": sequence},
                )


def _add_uploads_to_archive(archive: zipfile.ZipFile) -> int:
    uploads_root = Path(UPLOADS_DIR)
    if not uploads_root.exists():
        return 0

    count = 0
    for path in uploads_root.rglob("*"):
        if not path.is_file():
            continue
        archive.write(path, f"uploads/{path.relative_to(uploads_root).as_posix()}")
        count += 1
    return count


def _safe_upload_member_path(member_name: str) -> Optional[Path]:
    if not member_name.startswith("uploads/") or member_name.endswith("/"):
        return None
    normalized = normpath(member_name).replace("\\", "/")
    if normalized.startswith("../") or normalized == ".." or not normalized.startswith("uploads/"):
        raise HTTPException(status_code=400, detail="Backup archive contains an unsafe upload path")
    relative = normalized.removeprefix("uploads/").strip("/")
    if not relative:
        return None
    return Path(relative)


def _stage_uploads_from_archive(archive: zipfile.ZipFile, stage_dir: Path) -> int:
    count = 0
    for member in archive.infolist():
        relative = _safe_upload_member_path(member.filename)
        if relative is None:
            continue
        target = stage_dir / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(member) as source, target.open("wb") as output:
            shutil.copyfileobj(source, output)
        count += 1
    return count


def _replace_uploads_from_stage(stage_dir: Path) -> None:
    uploads_root = Path(UPLOADS_DIR)
    uploads_root.mkdir(parents=True, exist_ok=True)
    for child in uploads_root.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()
    for staged in stage_dir.rglob("*"):
        if not staged.is_file():
            continue
        target = uploads_root / staged.relative_to(stage_dir)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(staged, target)

def _check_subject_access(db: Session, user: User, subject_id: int):
    """Raise 403 if teacher doesn't have access to this subject."""
    if has_admin_access(user):
        return
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


def _requires_verification(user: User) -> bool:
    """Only teacher-originated content changes require HM/Principal verification."""
    return user.role == UserRole.teacher


def _can_verify_changes(user: User) -> bool:
    return user.role in {UserRole.hm, UserRole.principal, UserRole.super_admin}


def _mark_chapter_approval_state(chapter: Chapter, actor: User, change_summary: Optional[str] = None):
    """Apply approval rules after content changes.
    
    NOTE: Approval system is temporarily disabled. All changes are auto-approved.
    """
    # TEMPORARY: Always auto-approve to skip the verification workflow
    chapter.is_approved = True
    chapter.pending_change_summary = None
    chapter.approval_requested_by_id = None
    if actor.role == UserRole.super_admin:
        chapter.approved_by_id = actor.id
        chapter.approved_at = datetime.now(timezone.utc)


def _build_chapter_detail(db: Session, chapter: Chapter) -> ChapterDetailOut:
    """Build a ChapterDetailOut from a Chapter ORM object."""
    subject = chapter.subject
    cls = subject.cls

    def _order_key(c):
        return (c.display_order, c.id)

    concepts_out = []
    for concept in sorted(chapter.concepts, key=_order_key):
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
                field_type=ex.field_type,
                field_value=ex.field_value,
                file_key=ex.file_key,
                file_url=f"/uploads/{ex.file_key}" if ex.file_key else None,
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
                display_order=concept.display_order,
                concept_description=concept.concept_description,
                sessions=concept.sessions,
                learning_outcomes=concept.learning_outcomes,
                integration_other_sub=concept.integration_other_sub,
                teaching_materials_methods=concept.teaching_materials_methods,
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


def _chapter_snapshot(chapter: Chapter) -> dict:
    return {
        "id": chapter.id,
        "title": chapter.title,
        "aim": chapter.aim,
        "subject_id": chapter.subject_id,
        "order_index": chapter.order_index,
        "is_approved": chapter.is_approved,
        "pending_change_summary": chapter.pending_change_summary,
        "approval_requested_by_id": chapter.approval_requested_by_id,
        "approved_by_id": chapter.approved_by_id,
        "approved_at": chapter.approved_at,
        "pdf_filename": chapter.pdf_filename,
    }


def _concept_snapshot(concept: Concept) -> dict:
    return {
        "id": concept.id,
        "chapter_id": concept.chapter_id,
        "s_no": concept.s_no,
        "title": concept.title,
        "concept_description": concept.concept_description,
        "sessions": concept.sessions,
        "learning_outcomes": concept.learning_outcomes,
        "integration_other_sub": concept.integration_other_sub,
        "teaching_materials_methods": concept.teaching_materials_methods,
        "library": concept.library,
        "activity": concept.activity,
        "life_lesson": concept.life_lesson,
        "remarks": concept.remarks,
        "exhibit_ref": concept.exhibit_ref,
    }


def _exhibit_snapshot(exhibit: Exhibit) -> dict:
    return {
        "id": exhibit.id,
        "concept_id": exhibit.concept_id,
        "field_key": exhibit.field_key,
        "field_type": exhibit.field_type.value if hasattr(exhibit.field_type, "value") else str(exhibit.field_type),
        "field_value": exhibit.field_value,
        "file_key": exhibit.file_key,
        "sort_order": exhibit.sort_order,
    }


def _image_snapshot(img: ConceptImage) -> dict:
    return {
        "id": img.id,
        "concept_id": img.concept_id,
        "filename": img.filename,
        "original_name": img.original_name,
        "sort_order": img.sort_order,
    }


def _subject_snapshot(subject: Subject) -> dict:
    return {
        "id": subject.id,
        "name": subject.name,
        "class_id": subject.class_id,
        "icon": subject.icon,
        "color": subject.color,
    }


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
        _write_security_event(
            db,
            request=request,
            action="login_failed",
            entity_id=form_data.username,
            actor_user_id=user.id if user else None,
            change_summary="Login failed: invalid credentials",
            payload={
                "email": form_data.username,
                "reason": "invalid_credentials",
            },
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        _write_security_event(
            db,
            request=request,
            action="login_blocked",
            entity_id=str(user.id),
            actor_user_id=user.id,
            change_summary="Login blocked for inactive user",
            payload={
                "email": user.email,
                "reason": "inactive_user",
            },
        )
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
        )
    token = create_access_token(data={"sub": user.email})

    _write_security_event(
        db,
        request=request,
        action="login_success",
        entity_id=str(user.id),
        actor_user_id=user.id,
        change_summary="User logged in successfully",
        payload={
            "email": user.email,
            "role": user.role.value,
        },
    )
    db.commit()

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


@router.get("/auth/capabilities", response_model=RoleCapabilitiesOut)
def auth_capabilities(current_user: User = Depends(get_current_user)):
    """Return the capability matrix for the authenticated role."""
    return RoleCapabilitiesOut(
        role=current_user.role.value,
        capabilities=get_role_capabilities(current_user),
        is_admin=has_admin_access(current_user),
        is_subject_scoped=has_subject_scoped_access(current_user),
    )


@router.post("/auth/change-password")
def change_password(
    body: ChangePasswordIn,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Allow a logged-in user to change their own password."""
    if not body.current_password or not body.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current and new password are required")
    if len(body.new_password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 6 characters")
    if not verify_password(body.current_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    if verify_password(body.new_password, current_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be different from current password")

    current_user.hashed_password = hash_password(body.new_password)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="user",
        entity_id=str(current_user.id),
        action="change_password",
        change_summary="User changed own password",
        ip_address=_client_ip(request),
    )

    db.commit()
    return {"ok": True, "message": "Password updated successfully"}


# ---------------------------------------------------------------------------
# Super-admin backup and restore utilities
# ---------------------------------------------------------------------------

@router.get("/utilities/backup")
def download_backup(
    _current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    buffer = io.BytesIO()
    database_payload = _export_database(db)
    manifest = {
        "format": "dvm-lesson-portal-backup",
        "version": BACKUP_FORMAT_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("database.json", json.dumps(database_payload, indent=2))
        manifest["upload_file_count"] = _add_uploads_to_archive(archive)
        archive.writestr("manifest.json", json.dumps(manifest, indent=2))

    buffer.seek(0)
    filename = f"dvm-lesson-portal-backup-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.zip"
    return StreamingResponse(
        buffer,
        media_type="application/zip",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.post("/utilities/restore")
async def restore_backup(
    file: UploadFile = File(...),
    confirm_restore: str = Form(...),
    _current_user: User = Depends(require_super_admin),
    db: Session = Depends(get_db),
):
    if confirm_restore != "RESTORE":
        raise HTTPException(status_code=400, detail="Type RESTORE to confirm this destructive operation")
    if not (file.filename or "").lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Restore file must be a .zip backup archive")

    contents = await file.read()
    try:
        with zipfile.ZipFile(io.BytesIO(contents)) as archive:
            try:
                database_payload = json.loads(archive.read("database.json"))
            except KeyError as exc:
                raise HTTPException(status_code=400, detail="Backup archive is missing database.json") from exc

            with tempfile.TemporaryDirectory() as tmp:
                stage_dir = Path(tmp) / "uploads"
                stage_dir.mkdir()
                upload_count = _stage_uploads_from_archive(archive, stage_dir)
                restored_tables = _restore_database(db, database_payload)
                _replace_uploads_from_stage(stage_dir)
    except zipfile.BadZipFile as exc:
        raise HTTPException(status_code=400, detail="Restore file is not a valid zip archive") from exc

    return {
        "message": "Backup restored successfully",
        "restored_tables": restored_tables,
        "restored_upload_files": upload_count,
    }


# ---------------------------------------------------------------------------
# Teacher utility
# ---------------------------------------------------------------------------

@router.get("/my-subjects", response_model=List[SubjectNestedOut])
def my_subjects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Return subjects assigned to the current user (or all subjects for privileged roles)."""
    if has_admin_access(current_user):
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
    List chapters. Privileged roles get all; scoped roles get assigned subjects only.
    Optional query params: class_id, subject_id.
    """
    query = db.query(Chapter).join(Chapter.subject).join(Subject.cls)

    if has_subject_scoped_access(current_user):
        # Restrict scoped users to assigned subjects
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
                is_approved=chapter.is_approved,
                pending_change_summary=chapter.pending_change_summary,
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
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update chapter-level fields. Teacher must own the subject; admin can edit all."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    _check_subject_access(db, current_user, chapter.subject_id)

    before = _chapter_snapshot(chapter)

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

    changed_fields = []
    if body.title is not None:
        changed_fields.append("title")
    if body.aim is not None:
        changed_fields.append("aim")
    if body.order_index is not None:
        changed_fields.append("order")
    if body.subject_id is not None:
        changed_fields.append("subject")
    summary = f"Chapter updated ({', '.join(changed_fields)})" if changed_fields else "Chapter updated"
    _mark_chapter_approval_state(chapter, current_user, summary)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="chapter",
        entity_id=str(chapter.id),
        action="update",
        change_summary=summary,
        before_payload=before,
        after_payload=_chapter_snapshot(chapter),
        ip_address=_client_ip(request),
    )

    db.commit()
    db.refresh(chapter)
    return _build_chapter_detail(db, chapter)


@router.post("/chapters", response_model=ChapterDetailOut, status_code=201)
def create_chapter(
    body: ChapterCreateIn,
    request: Request,
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
    _mark_chapter_approval_state(chapter, current_user, "New chapter created")
    db.add(chapter)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="chapter",
        entity_id=str(chapter.id),
        action="create",
        change_summary=f"Chapter created: {chapter.title}",
        after_payload=_chapter_snapshot(chapter),
        ip_address=_client_ip(request),
    )

    db.commit()
    db.refresh(chapter)
    return _build_chapter_detail(db, chapter)


@router.post("/chapters/{chapter_id}/approve", response_model=ChapterDetailOut)
def approve_chapter_changes(
    chapter_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Approve pending chapter changes. HM/Principal/Super Admin only."""
    if not _can_verify_changes(current_user):
        raise HTTPException(status_code=403, detail="Only HM or Principal can verify pending changes")

    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    before = _chapter_snapshot(chapter)

    chapter.is_approved = True
    chapter.pending_change_summary = None
    chapter.approval_requested_by_id = None
    chapter.approved_by_id = current_user.id
    chapter.approved_at = datetime.now(timezone.utc)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="chapter",
        entity_id=str(chapter.id),
        action="approve",
        change_summary=f"Chapter approved: {chapter.title}",
        before_payload=before,
        after_payload=_chapter_snapshot(chapter),
        ip_address=_client_ip(request),
    )

    db.commit()
    db.refresh(chapter)
    return _build_chapter_detail(db, chapter)


@router.delete("/chapters/{chapter_id}")
def delete_chapter(
    chapter_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a chapter and cascade to concepts/exhibits. Admin only."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    before = _chapter_snapshot(chapter)

    _delete_chapter_cascade(db, chapter)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="chapter",
        entity_id=str(chapter_id),
        action="delete",
        change_summary=f"Chapter deleted: {before.get('title')}",
        before_payload=before,
        ip_address=_client_ip(request),
    )

    db.commit()
    return {"ok": True}


@router.post("/chapters/{chapter_id}/pdf")
async def upload_chapter_pdf(
    chapter_id: int,
    file: UploadFile = File(...),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload or replace the PDF file for a chapter. Teacher must own the subject."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    _check_subject_access(db, current_user, chapter.subject_id)

    before = _chapter_snapshot(chapter)

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
    _mark_chapter_approval_state(chapter, current_user, "Chapter PDF updated")

    _write_security_event(
        db,
        request=request,
        action="file_upload",
        entity_id=unique_name,
        actor_user_id=current_user.id,
        change_summary=f"Chapter PDF uploaded for chapter {chapter.id}",
        payload={
            "upload_type": "chapter_pdf",
            "chapter_id": chapter.id,
            "subject_id": chapter.subject_id,
            "stored_filename": unique_name,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
        },
    )

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="chapter",
        entity_id=str(chapter.id),
        action="upload_pdf",
        change_summary=f"Chapter PDF uploaded/replaced: {chapter.title}",
        before_payload=before,
        after_payload=_chapter_snapshot(chapter),
        ip_address=_client_ip(request),
    )

    db.commit()
    return {"pdf_url": f"/uploads/{unique_name}"}


# ---------------------------------------------------------------------------
# Upload route
# ---------------------------------------------------------------------------

@router.post("/editor-images")
async def upload_editor_image(
    file: UploadFile = File(...),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload an inline editor image and return its public uploads URL."""
    if not (file.content_type or "").startswith("image/"):
        raise HTTPException(status_code=422, detail="Only image files are allowed")

    os.makedirs(UPLOADS_DIR, exist_ok=True)

    unique_name = _safe_upload_name(file.filename)
    dest_path = os.path.join(UPLOADS_DIR, unique_name)

    contents = await file.read()
    max_bytes = 5 * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(status_code=413, detail="Image exceeds 5 MB limit")

    with open(dest_path, "wb") as output:
        output.write(contents)

    _write_security_event(
        db,
        request=request,
        action="file_upload",
        entity_id=unique_name,
        actor_user_id=current_user.id,
        change_summary="Editor image uploaded",
        payload={
            "upload_type": "editor_image",
            "stored_filename": unique_name,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
        },
    )
    db.commit()

    return {"url": f"/uploads/{unique_name}"}

@router.post("/upload", response_model=UploadResultOut)
async def upload_xlsx(
    file: UploadFile = File(...),
    subject_id: int = Form(...),
    request: Request = None,
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
    existing_before = _chapter_snapshot(existing) if existing else None
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
    _mark_chapter_approval_state(chapter, current_user, "Chapter content re-uploaded from xlsx")
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
            concept_description=concept_data.get("concept_description"),
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

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="chapter",
        entity_id=str(chapter.id),
        action="upload_xlsx",
        change_summary=f"Chapter uploaded from xlsx: {chapter.title}",
        before_payload=existing_before,
        after_payload={
            **_chapter_snapshot(chapter),
            "concepts_count": concepts_count,
            "exhibits_count": exhibits_count,
        },
        ip_address=_client_ip(request),
    )

    _write_security_event(
        db,
        request=request,
        action="file_upload",
        entity_id=f"xlsx:{subject_id}:{chapter.id}",
        actor_user_id=current_user.id,
        change_summary=f"Lesson xlsx uploaded for subject {subject_id}",
        payload={
            "upload_type": "lesson_xlsx",
            "subject_id": subject_id,
            "chapter_id": chapter.id,
            "chapter_title": chapter.title,
            "original_filename": file.filename,
            "content_type": file.content_type,
            "size_bytes": len(contents),
            "concepts_count": concepts_count,
            "exhibits_count": exhibits_count,
        },
    )

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
            field_type=ex.field_type,
            field_value=ex.field_value,
            file_key=ex.file_key,
            file_url=f"/uploads/{ex.file_key}" if ex.file_key else None,
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
        display_order=concept.display_order,
        concept_description=concept.concept_description,
        sessions=concept.sessions,
        learning_outcomes=concept.learning_outcomes,
        integration_other_sub=concept.integration_other_sub,
        teaching_materials_methods=concept.teaching_materials_methods,
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


def _get_chapter_by_concept_id(db: Session, concept_id: int) -> Chapter:
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")
    chapter = db.query(Chapter).filter(Chapter.id == concept.chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.put("/concepts/{concept_id}", response_model=ConceptOut)
def update_concept(
    concept_id: int,
    body: ConceptUpdateIn,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update concept fields. Teacher must own the subject; admin can edit all."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    before = _concept_snapshot(concept)

    subject_id = _get_concept_subject_id(db, concept_id)
    _check_subject_access(db, current_user, subject_id)

    if body.s_no is not None:
        concept.s_no = body.s_no
    if body.title is not None:
        concept.title = body.title
    if body.display_order is not None:
        concept.display_order = body.display_order
    if body.concept_description is not None:
        concept.concept_description = body.concept_description
    if body.sessions is not None:
        concept.sessions = body.sessions
    if body.learning_outcomes is not None:
        concept.learning_outcomes = body.learning_outcomes
    if body.integration_other_sub is not None:
        concept.integration_other_sub = body.integration_other_sub
    if body.teaching_materials_methods is not None:
        concept.teaching_materials_methods = body.teaching_materials_methods
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

    chapter = _get_chapter_by_concept_id(db, concept_id)
    changed_fields = []
    if body.s_no is not None:
        changed_fields.append("s_no")
    if body.title is not None:
        changed_fields.append("title")
    if body.concept_description is not None:
        changed_fields.append("description")
    if body.sessions is not None:
        changed_fields.append("sessions")
    if body.learning_outcomes is not None:
        changed_fields.append("learning outcomes")
    if body.integration_other_sub is not None:
        changed_fields.append("integration")
    if body.teaching_materials_methods is not None:
        changed_fields.append("teaching methods")
    if body.library is not None:
        changed_fields.append("library")
    if body.activity is not None:
        changed_fields.append("activity")
    if body.life_lesson is not None:
        changed_fields.append("life lesson")
    if body.remarks is not None:
        changed_fields.append("remarks")
    if body.exhibit_ref is not None:
        changed_fields.append("exhibit ref")
    summary = f"Concept '{concept.title}' updated ({', '.join(changed_fields)})" if changed_fields else f"Concept '{concept.title}' updated"
    _mark_chapter_approval_state(chapter, current_user, summary)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="concept",
        entity_id=str(concept.id),
        action="update",
        change_summary=summary,
        before_payload=before,
        after_payload=_concept_snapshot(concept),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(concept)
    return _build_concept_out(db, concept)


@router.delete("/concepts/{concept_id}")
def delete_concept(
    concept_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a concept and its exhibits. Admin only."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    before = _concept_snapshot(concept)

    db.query(Exhibit).filter(Exhibit.concept_id == concept.id).delete()
    db.delete(concept)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="concept",
        entity_id=str(concept_id),
        action="delete",
        change_summary=f"Concept deleted: {before.get('title')}",
        before_payload=before,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    return {"ok": True}


@router.post("/concepts", response_model=ConceptOut, status_code=201)
def create_concept(
    body: ConceptCreateIn,
    request: Request,
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
        display_order=body.display_order,
        concept_description=body.concept_description,
        sessions=body.sessions,
        learning_outcomes=body.learning_outcomes,
        integration_other_sub=body.integration_other_sub,
        teaching_materials_methods=body.teaching_materials_methods,
        library=body.library,
        activity=body.activity,
        life_lesson=body.life_lesson,
        remarks=body.remarks,
        exhibit_ref=body.exhibit_ref,
    )
    db.add(concept)
    _mark_chapter_approval_state(chapter, current_user, f"New concept added: {concept.title}")
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="concept",
        entity_id=str(concept.id),
        action="create",
        change_summary=f"Concept created: {concept.title}",
        after_payload=_concept_snapshot(concept),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(concept)
    return _build_concept_out(db, concept)


# ---------------------------------------------------------------------------
# Exhibit CRUD routes
# ---------------------------------------------------------------------------

@router.put("/exhibits/{exhibit_id}", response_model=ExhibitOut)
async def update_exhibit(
    exhibit_id: int,
    field_key: Optional[str] = Form(None),
    field_type: Optional[str] = Form(None),
    field_value: Optional[str] = Form(None),
    sort_order: Optional[int] = Form(None),
    file: Optional[UploadFile] = File(None),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update an exhibit. Teacher must own the subject via concept->chapter->subject.
    
    To replace the file, provide a new file. To remove it, this endpoint doesn't support
    deletion of files directly - delete and recreate the exhibit instead.
    """
    exhibit = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")

    before = _exhibit_snapshot(exhibit)

    subject_id = _get_concept_subject_id(db, exhibit.concept_id)
    _check_subject_access(db, current_user, subject_id)
    chapter = _get_chapter_by_concept_id(db, exhibit.concept_id)

    # Validate field_type if provided
    if field_type:
        valid_types = ["string", "audio", "image", "video", "link"]
        if field_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"Invalid field_type. Must be one of: {', '.join(valid_types)}")
        exhibit.field_type = field_type

    if field_key is not None:
        exhibit.field_key = field_key
    if field_value is not None:
        exhibit.field_value = field_value
    if sort_order is not None:
        exhibit.sort_order = sort_order

    # Handle file replacement
    if file:
        # Delete old file if exists
        if exhibit.file_key:
            old_path = os.path.join(UPLOADS_DIR, exhibit.file_key)
            if os.path.exists(old_path):
                os.remove(old_path)
        
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        unique_name = _safe_upload_name(file.filename)
        dest_path = os.path.join(UPLOADS_DIR, unique_name)
        
        # Save new file
        with open(dest_path, "wb") as f:
            f.write(await file.read())
        
        exhibit.file_key = unique_name

    changed_fields = []
    if field_key is not None:
        changed_fields.append("field key")
    if field_type is not None:
        changed_fields.append("field type")
    if field_value is not None:
        changed_fields.append("field value")
    if sort_order is not None:
        changed_fields.append("order")
    if file:
        changed_fields.append("file")
    summary = f"Exhibit '{exhibit.field_key}' updated ({', '.join(changed_fields)})" if changed_fields else f"Exhibit '{exhibit.field_key}' updated"
    _mark_chapter_approval_state(chapter, current_user, summary)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="exhibit",
        entity_id=str(exhibit.id),
        action="update",
        change_summary=summary,
        before_payload=before,
        after_payload=_exhibit_snapshot(exhibit),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(exhibit)
    
    file_url = f"/uploads/{exhibit.file_key}" if exhibit.file_key else None
    return ExhibitOut(
        id=exhibit.id,
        field_key=exhibit.field_key,
        field_type=exhibit.field_type,
        field_value=exhibit.field_value,
        file_key=exhibit.file_key,
        file_url=file_url,
        sort_order=exhibit.sort_order,
    )


@router.delete("/exhibits/{exhibit_id}")
def delete_exhibit(
    exhibit_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete an exhibit. Teacher must own the subject. Also deletes associated files."""
    exhibit = db.query(Exhibit).filter(Exhibit.id == exhibit_id).first()
    if exhibit is None:
        raise HTTPException(status_code=404, detail="Exhibit not found")

    before = _exhibit_snapshot(exhibit)

    subject_id = _get_concept_subject_id(db, exhibit.concept_id)
    _check_subject_access(db, current_user, subject_id)
    chapter = _get_chapter_by_concept_id(db, exhibit.concept_id)

    # Delete associated file if exists
    if exhibit.file_key:
        file_path = os.path.join(UPLOADS_DIR, exhibit.file_key)
        if os.path.exists(file_path):
            os.remove(file_path)

    deleted_key = exhibit.field_key
    db.delete(exhibit)
    _mark_chapter_approval_state(chapter, current_user, f"Exhibit removed: {deleted_key}")

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="exhibit",
        entity_id=str(exhibit_id),
        action="delete",
        change_summary=f"Exhibit deleted: {deleted_key}",
        before_payload=before,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    return {"ok": True}


@router.post("/concepts/{concept_id}/exhibits", response_model=ExhibitOut, status_code=201)
async def create_exhibit(
    concept_id: int,
    field_key: str = Form(...),
    field_type: str = Form(default="string"),
    field_value: Optional[str] = Form(None),
    sort_order: Optional[int] = Form(0),
    file: Optional[UploadFile] = File(None),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new exhibit for a concept. Teacher must own the subject.
    
    For file-type exhibits (audio, image, video), provide the file parameter.
    For string/link types, provide field_value.
    """
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    subject_id = _get_concept_subject_id(db, concept_id)
    _check_subject_access(db, current_user, subject_id)
    chapter = _get_chapter_by_concept_id(db, concept_id)

    # Validate field_type
    valid_types = ["string", "audio", "image", "video", "link"]
    if field_type not in valid_types:
        raise HTTPException(status_code=400, detail=f"Invalid field_type. Must be one of: {', '.join(valid_types)}")

    # Handle file upload if provided
    file_key = None
    if file:
        os.makedirs(UPLOADS_DIR, exist_ok=True)
        unique_name = _safe_upload_name(file.filename)
        dest_path = os.path.join(UPLOADS_DIR, unique_name)
        
        # Save file
        with open(dest_path, "wb") as f:
            f.write(await file.read())
        
        file_key = unique_name

    exhibit = Exhibit(
        concept_id=concept_id,
        field_key=field_key,
        field_type=field_type,
        field_value=field_value,
        file_key=file_key,
        sort_order=sort_order if sort_order is not None else 0,
    )
    db.add(exhibit)
    _mark_chapter_approval_state(chapter, current_user, f"New exhibit added: {field_key}")
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="exhibit",
        entity_id=str(exhibit.id),
        action="create",
        change_summary=f"Exhibit created: {field_key}",
        after_payload=_exhibit_snapshot(exhibit),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(exhibit)
    
    file_url = f"/uploads/{file_key}" if file_key else None
    return ExhibitOut(
        id=exhibit.id,
        field_key=exhibit.field_key,
        field_type=exhibit.field_type,
        field_value=exhibit.field_value,
        file_key=file_key,
        file_url=file_url,
        sort_order=exhibit.sort_order,
    )


# ---------------------------------------------------------------------------
# Concept Image routes
# ---------------------------------------------------------------------------

@router.post("/concepts/{concept_id}/images", response_model=List[ConceptImageOut], status_code=201)
async def upload_concept_images(
    concept_id: int,
    files: List[UploadFile] = File(...),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Upload one or more images for a concept. Teacher must own the subject."""
    concept = db.query(Concept).filter(Concept.id == concept_id).first()
    if concept is None:
        raise HTTPException(status_code=404, detail="Concept not found")

    subject_id = _get_concept_subject_id(db, concept_id)
    _check_subject_access(db, current_user, subject_id)
    chapter = _get_chapter_by_concept_id(db, concept_id)

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

    _mark_chapter_approval_state(chapter, current_user, f"{len(created)} concept image(s) added")

    for created_img in created:
        write_audit_log(
            db,
            actor_user_id=current_user.id,
            entity_type="concept_image",
            entity_id=str(created_img.id),
            action="create",
            change_summary=f"Concept image uploaded: {created_img.original_name}",
            after_payload={
                "id": created_img.id,
                "concept_id": concept_id,
                "filename": created_img.filename,
                "original_name": created_img.original_name,
                "sort_order": created_img.sort_order,
            },
            ip_address=request.client.host if request.client else None,
        )

    db.commit()
    return created


@router.delete("/images/{image_id}")
def delete_concept_image(
    image_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Delete a concept image (disk + DB row). Teacher must own the subject."""
    img = db.query(ConceptImage).filter(ConceptImage.id == image_id).first()
    if img is None:
        raise HTTPException(status_code=404, detail="Image not found")

    before = _image_snapshot(img)

    subject_id = _get_concept_subject_id(db, img.concept_id)
    _check_subject_access(db, current_user, subject_id)
    chapter = _get_chapter_by_concept_id(db, img.concept_id)

    # Remove file from disk (ignore if already missing)
    file_path = os.path.join(UPLOADS_DIR, img.filename)
    if os.path.exists(file_path):
        os.remove(file_path)

    deleted_name = img.original_name
    db.delete(img)
    _mark_chapter_approval_state(chapter, current_user, f"Concept image removed: {deleted_name}")

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="concept_image",
        entity_id=str(image_id),
        action="delete",
        change_summary=f"Concept image deleted: {deleted_name}",
        before_payload=before,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    return {"ok": True}


@router.put("/images/{image_id}", response_model=ConceptImageOut)
def update_concept_image(
    image_id: int,
    sort_order: int = Body(..., embed=True),
    request: Request = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Update sort_order of a concept image. Teacher must own the subject."""
    img = db.query(ConceptImage).filter(ConceptImage.id == image_id).first()
    if img is None:
        raise HTTPException(status_code=404, detail="Image not found")

    before = _image_snapshot(img)

    subject_id = _get_concept_subject_id(db, img.concept_id)
    _check_subject_access(db, current_user, subject_id)
    chapter = _get_chapter_by_concept_id(db, img.concept_id)

    img.sort_order = sort_order
    _mark_chapter_approval_state(chapter, current_user, "Concept image order updated")

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="concept_image",
        entity_id=str(img.id),
        action="update",
        change_summary="Concept image order updated",
        before_payload=before,
        after_payload=_image_snapshot(img),
        ip_address=request.client.host if request.client else None,
    )

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
    request: Request,
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
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="subject",
        entity_id=str(subject.id),
        action="create",
        change_summary=f"Subject created: {subject.name}",
        after_payload=_subject_snapshot(subject),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(subject)
    return _subject_to_out(subject)


@router.put("/subjects/{subject_id}", response_model=SubjectFullOut)
def update_subject(
    subject_id: int,
    body: SubjectUpdateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update a subject. Admin only."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    before = _subject_snapshot(subject)
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

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="subject",
        entity_id=str(subject.id),
        action="update",
        change_summary=f"Subject updated: {subject.name}",
        before_payload=before,
        after_payload=_subject_snapshot(subject),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(subject)
    return _subject_to_out(subject)


@router.delete("/subjects/{subject_id}")
def delete_subject(
    subject_id: int,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Delete a subject. Admin only. Blocked if chapters exist under it."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    before = _subject_snapshot(subject)
    chapter_count = db.query(Chapter).filter(Chapter.subject_id == subject_id).count()
    if chapter_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete: {chapter_count} chapter(s) exist under this subject. Delete chapters first.",
        )
    db.query(TeacherSubject).filter(TeacherSubject.subject_id == subject_id).delete()
    db.delete(subject)

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="subject",
        entity_id=str(subject_id),
        action="delete",
        change_summary=f"Subject deleted: {before.get('name')}",
        before_payload=before,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    return {"ok": True}
