from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from audit import write_audit_log
from auth import hash_password, require_admin
from database import get_db
from models import Subject, TeacherSubject, User, UserRole
from schemas import (
    AdminResetPasswordIn,
    SubjectAssignIn,
    SubjectNestedOut,
    UserCreateIn,
    UserFullOut,
    UserUpdateIn,
)

router = APIRouter()

SUBJECT_ASSIGNABLE_ROLES = {
    UserRole.teacher,
    UserRole.subject_head,
    UserRole.mentor,
}


def _valid_role_names() -> str:
    return ", ".join([role.value for role in UserRole])


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _user_to_out(user: User) -> UserFullOut:
    return UserFullOut(
        id=user.id,
        name=user.name,
        email=user.email,
        role=user.role.value,
        is_active=user.is_active,
    )


def _user_snapshot(user: User) -> dict:
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, "value") else str(user.role),
        "is_active": user.is_active,
    }


# ---------------------------------------------------------------------------
# GET /api/users/
# ---------------------------------------------------------------------------

@router.get("/", response_model=List[UserFullOut])
def list_users(
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Return all users. Admin only."""
    users = db.query(User).order_by(User.id).all()
    return [_user_to_out(u) for u in users]


# ---------------------------------------------------------------------------
# POST /api/users/
# ---------------------------------------------------------------------------

@router.post("/", response_model=UserFullOut, status_code=status.HTTP_201_CREATED)
def create_user(
    body: UserCreateIn,
    request: Request,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Create a new user. Admin only. Returns 400 if email already exists."""
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    try:
        role_enum = UserRole[body.role]
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role '{body.role}'. Must be one of: {_valid_role_names()}.",
        )

    user = User(
        name=body.name,
        email=body.email,
        hashed_password=hash_password(body.password),
        role=role_enum,
        is_active=True,
    )
    db.add(user)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=admin_user.id,
        entity_type="user",
        entity_id=str(user.id),
        action="create",
        change_summary=f"User created: {user.email}",
        after_payload=_user_snapshot(user),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(user)
    return _user_to_out(user)


# ---------------------------------------------------------------------------
# PUT /api/users/{user_id}
# ---------------------------------------------------------------------------

@router.put("/{user_id}", response_model=UserFullOut)
def update_user(
    user_id: int,
    body: UserUpdateIn,
    request: Request,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Update user fields. Admin only. Returns 404 if not found, 400 on email conflict."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    before = _user_snapshot(user)

    if body.email is not None and body.email != user.email:
        conflict = db.query(User).filter(User.email == body.email).first()
        if conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use",
            )
        user.email = body.email

    if body.name is not None:
        user.name = body.name

    if body.role is not None:
        try:
            user.role = UserRole[body.role]
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role '{body.role}'. Must be one of: {_valid_role_names()}.",
            )

    if body.is_active is not None:
        user.is_active = body.is_active

    after = _user_snapshot(user)
    write_audit_log(
        db,
        actor_user_id=admin_user.id,
        entity_type="user",
        entity_id=str(user.id),
        action="update",
        change_summary=f"User updated: {user.email}",
        before_payload=before,
        after_payload=after,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(user)
    return _user_to_out(user)


# ---------------------------------------------------------------------------
# POST /api/users/{user_id}/subjects  — replace subject assignment
# ---------------------------------------------------------------------------

@router.post("/{user_id}/subjects")
def assign_subjects(
    user_id: int,
    body: SubjectAssignIn,
    request: Request,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Replace all subject assignments for a teacher. Admin only."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.role not in SUBJECT_ASSIGNABLE_ROLES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Subjects can only be assigned to teacher, subject_head, or mentor roles",
        )

    before_subject_ids = [
        row.subject_id
        for row in db.query(TeacherSubject).filter(TeacherSubject.teacher_id == user_id).all()
    ]

    # Validate all subject IDs exist
    if body.subject_ids:
        found = (
            db.query(Subject.id)
            .filter(Subject.id.in_(body.subject_ids))
            .all()
        )
        found_ids = {row.id for row in found}
        missing = set(body.subject_ids) - found_ids
        if missing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Subject IDs not found: {sorted(missing)}",
            )

    # Delete existing assignments then insert new ones
    db.query(TeacherSubject).filter(TeacherSubject.teacher_id == user_id).delete()

    for sid in body.subject_ids:
        db.add(TeacherSubject(teacher_id=user_id, subject_id=sid))

    write_audit_log(
        db,
        actor_user_id=admin_user.id,
        entity_type="teacher_subject",
        entity_id=str(user_id),
        action="replace",
        change_summary=f"Subject assignments updated for user {user.email}",
        before_payload={"subject_ids": before_subject_ids},
        after_payload={"subject_ids": body.subject_ids},
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    return {"ok": True, "assigned": body.subject_ids}


# ---------------------------------------------------------------------------
# GET /api/users/{user_id}/subjects
# ---------------------------------------------------------------------------

@router.get("/{user_id}/subjects", response_model=List[SubjectNestedOut])
def get_user_subjects(
    user_id: int,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Return subjects assigned to a teacher. Admin only."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    subjects = (
        db.query(Subject)
        .join(TeacherSubject, TeacherSubject.subject_id == Subject.id)
        .filter(TeacherSubject.teacher_id == user_id)
        .order_by(Subject.id)
        .all()
    )
    return [
        SubjectNestedOut(id=s.id, name=s.name, icon=s.icon, color=s.color)
        for s in subjects
    ]


@router.post("/{user_id}/reset-password")
def admin_reset_password(
    user_id: int,
    body: AdminResetPasswordIn,
    request: Request,
    admin_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Reset/change any user's password. Admin only."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not body.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password is required")
    if len(body.new_password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New password must be at least 6 characters")

    user.hashed_password = hash_password(body.new_password)

    write_audit_log(
        db,
        actor_user_id=admin_user.id,
        entity_type="user",
        entity_id=str(user.id),
        action="reset_password",
        change_summary=f"Password reset by admin for user {user.email}",
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    return {"ok": True, "message": "Password reset successfully"}
