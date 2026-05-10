from typing import List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import or_, func
from sqlalchemy.orm import Session

from audit import write_audit_log
from auth import require_capability, hash_password
from database import get_db
from models import User, StaffProfile, UserRole, Department
from schemas import (
    StaffCreateIn,
    StaffUpdateIn,
    StaffListOut,
    UserOut,
    DepartmentOut,
)

router = APIRouter(prefix="/staff")


def _staff_to_out(user: User) -> UserOut:
    return UserOut.model_validate(user)


def _staff_snapshot(user: User) -> dict:
    snapshot = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role.value if hasattr(user.role, "value") else str(user.role),
        "is_active": user.is_active,
    }
    if user.profile:
        p = user.profile
        snapshot["profile"] = {
            "staff_code": p.staff_code,
            "department": p.department,
            "designation": p.designation,
            "phone": p.phone,
        }
    return snapshot


@router.get("/", response_model=StaffListOut)
def list_staff(
    q: Optional[str] = Query(None, description="Search by name, email, or staff code"),
    role: Optional[str] = None,
    department: Optional[str] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _user: User = Depends(require_capability("user_management")),
    db: Session = Depends(get_db),
):
    query = db.query(User).filter(User.role != UserRole.super_admin)

    if role:
        try:
            query = query.filter(User.role == UserRole(role))
        except ValueError:
            pass

    if department:
        query = query.join(StaffProfile).filter(
            or_(
                StaffProfile.department.ilike(f"%{department}%"),
                StaffProfile.dept_link.has(Department.name.ilike(f"%{department}%"))
            )
        )

    if q:
        like_q = f"%{q.strip()}%"
        # Search in User name/email OR StaffProfile staff_code/phone
        query = query.outerjoin(StaffProfile).filter(
            or_(
                User.name.ilike(like_q),
                User.email.ilike(like_q),
                StaffProfile.staff_code.ilike(like_q),
                StaffProfile.phone.ilike(like_q),
            )
        )

    total = query.count()
    rows = query.order_by(User.name).offset(offset).limit(limit).all()
    items = [_staff_to_out(row) for row in rows]
    return StaffListOut(items=items, total=total)


@router.get("/{staff_id}", response_model=UserOut)
def get_staff_detail(
    staff_id: int,
    _user: User = Depends(require_capability("user_management")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == staff_id).first()
    if not user or user.role == UserRole.super_admin:
        raise HTTPException(status_code=404, detail="Staff member not found")
    return _staff_to_out(user)


@router.post("/", response_model=UserOut, status_code=201)
def create_staff(
    body: StaffCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("user_management")),
    db: Session = Depends(get_db),
):
    # Check if email exists
    existing = db.query(User).filter(User.email == body.email.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # Validate role
    try:
        role_enum = UserRole(body.role)
        if role_enum == UserRole.super_admin:
            raise ValueError("Cannot create super_admin via this endpoint")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role: {body.role}")

    # Create User
    user = User(
        name=body.name,
        email=body.email.lower(),
        hashed_password=hash_password(body.password),
        role=role_enum,
        is_active=True,
    )
    db.add(user)
    db.flush()

    # Create Profile
    profile = StaffProfile(
        user_id=user.id,
        staff_code=body.staff_code,
        date_of_birth=body.date_of_birth,
        gender=body.gender,
        phone=body.phone,
        department_id=body.department_id,
        designation=body.designation,
        joining_date=body.joining_date,
        address=body.address,
    )
    db.add(profile)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="user",
        entity_id=str(user.id),
        action="create",
        change_summary=f"Staff member created: {user.name} ({user.role.value})",
        after_payload=_staff_snapshot(user),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(user)
    return _staff_to_out(user)


@router.put("/{staff_id}", response_model=UserOut)
def update_staff(
    staff_id: int,
    body: StaffUpdateIn,
    request: Request,
    current_user: User = Depends(require_capability("user_management")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == staff_id).first()
    if not user or user.role == UserRole.super_admin:
        raise HTTPException(status_code=404, detail="Staff member not found")

    before = _staff_snapshot(user)

    # Update User fields
    if body.name is not None:
        user.name = body.name
    if body.email is not None:
        email = body.email.lower()
        if email != user.email:
            existing = db.query(User).filter(User.email == email).first()
            if existing:
                raise HTTPException(status_code=400, detail="Email already in use")
            user.email = email
    if body.role is not None:
        try:
            role_enum = UserRole(body.role)
            if role_enum != UserRole.super_admin:
                user.role = role_enum
        except ValueError:
            pass
    if body.is_active is not None:
        user.is_active = body.is_active

    # Update Profile fields
    if user.profile is None:
        user.profile = StaffProfile(user_id=user.id)
        db.add(user.profile)
        db.flush()

    p = user.profile
    # Only update fields that were actually provided in the request
    update_data = body.model_dump(exclude_unset=True)
    profile_fields = [
        "staff_code", "date_of_birth", "gender", "phone", "department_id", 
        "designation", "joining_date", "address", "blood_group", 
        "marital_status", "city", "state", "nationality", 
        "qualification", "bank_name", "account_no", "ifsc_code", 
        "pan_no", "aadhaar_no", "pf_no", "esi_no"
    ]
    for field in profile_fields:
        if field in update_data:
            setattr(p, field, update_data[field])

    after = _staff_snapshot(user)
    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="user",
        entity_id=str(user.id),
        action="update",
        change_summary=f"Staff member updated: {user.name}",
        before_payload=before,
        after_payload=after,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(user)
    return _staff_to_out(user)


@router.delete("/{staff_id}", status_code=204)
def delete_staff(
    staff_id: int,
    request: Request,
    current_user: User = Depends(require_capability("user_management")),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == staff_id).first()
    if not user or user.role == UserRole.super_admin:
        raise HTTPException(status_code=404, detail="Staff member not found")

    before = _staff_snapshot(user)
    user.is_active = False

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="user",
        entity_id=str(user.id),
        action="deactivate",
        change_summary=f"Staff member deactivated: {user.name}",
        before_payload=before,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    return None
