"""
Read-only AI Agent API — /api/agent/*

Authentication: X-API-Key header checked against AGENT_API_KEY env var.
All endpoints are GET-only and never expose sensitive financial/identity fields.
Every request is written to the audit log.
"""

from __future__ import annotations

import os
from datetime import date
from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from audit import write_audit_log
from database import get_db
from limiter import limiter
from models import (
    AcademicYear,
    AttendanceEntry,
    AttendanceStatus,
    Class,
    Guardian,
    Section,
    Student,
    StudentGuardian,
    StudentStatus,
    User,
)

router = APIRouter(prefix="/agent", tags=["agent"])

# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
AGENT_API_KEY = os.getenv("AGENT_API_KEY", "")


def verify_agent_key(request: Request) -> str:
    """Validate the X-API-Key header against AGENT_API_KEY env var."""
    if not AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Agent API is not configured on this server.",
        )
    key = request.headers.get("X-API-Key", "")
    if key != AGENT_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or missing API key.",
        )
    return key


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _fmt(v: Any, fallback: str = "unknown") -> str:
    return str(v).strip() if v else fallback


def _fmt_date(d: Optional[date]) -> Optional[str]:
    return d.isoformat() if d else None


def _student_summary(student: Student) -> str:
    primary = next(
        (link for link in student.guardians if link.is_primary),
        student.guardians[0] if student.guardians else None,
    )
    guardian_str = ""
    if primary:
        g = primary.guardian
        guardian_str = f", guardian: {g.name} ({g.relation or 'Parent'}) {g.phone or ''}"

    return (
        f"{student.first_name} {student.last_name or ''}, "
        f"{student.cls.name if student.cls else 'Unknown Class'}"
        f"{' ' + student.section.name if student.section else ''}, "
        f"Adm# {student.admission_no}, "
        f"status: {student.status.value if hasattr(student.status, 'value') else student.status}"
        f"{guardian_str}"
    ).strip()


def _student_to_dict(student: Student) -> dict:
    primary_link = next(
        (link for link in student.guardians if link.is_primary),
        student.guardians[0] if student.guardians else None,
    )
    primary_guardian = None
    if primary_link:
        g = primary_link.guardian
        primary_guardian = f"{g.name} ({g.relation or 'Guardian'}) — {g.phone or 'no phone'}"

    return {
        "id": student.id,
        "full_name": f"{student.first_name} {student.last_name or ''}".strip(),
        "admission_no": student.admission_no,
        "roll_no": student.roll_no,
        "class": student.cls.name if student.cls else None,
        "section": student.section.name if student.section else None,
        "academic_year": student.academic_year.name if student.academic_year else None,
        "gender": student.gender,
        "date_of_birth": _fmt_date(student.date_of_birth),
        "phone": student.phone,
        "email": student.email,
        "status": student.status.value if hasattr(student.status, "value") else str(student.status),
        "primary_guardian": primary_guardian,
        "natural_summary": _student_summary(student),
    }


def _log_agent(db: Session, request: Request, action: str, detail: str):
    write_audit_log(
        db,
        actor_user_id=None,
        entity_type="agent_query",
        entity_id=None,
        action=action,
        change_summary=detail,
        before_payload=None,
        after_payload=None,
        ip_address=request.client.host if request.client else None,
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/stats")
@limiter.limit("60/minute")
def agent_stats(
    request: Request,
    _key: str = Depends(verify_agent_key),
    db: Session = Depends(get_db),
):
    """Overall school statistics — total students, staff, class breakdown."""
    total_students = db.query(func.count(Student.id)).scalar()
    total_staff = db.query(func.count(User.id)).scalar()

    active_students = db.query(func.count(Student.id)).filter(
        Student.status == StudentStatus.active
    ).scalar()

    # Current academic year
    current_year = (
        db.query(AcademicYear)
        .filter(AcademicYear.is_active == True)
        .order_by(AcademicYear.start_date.desc())
        .first()
    )

    # Class breakdown
    class_rows = (
        db.query(Class.name, func.count(Student.id))
        .join(Student, Student.class_id == Class.id)
        .group_by(Class.id)
        .order_by(Class.display_order.asc(), Class.id.asc())
        .all()
    )

    # Gender breakdown
    gender_rows = (
        db.query(Student.gender, func.count(Student.id))
        .filter(Student.gender.isnot(None))
        .group_by(Student.gender)
        .all()
    )

    result = {
        "total_students": total_students,
        "active_students": active_students,
        "total_staff": total_staff,
        "academic_year": current_year.name if current_year else "N/A",
        "class_breakdown": [{"class": r[0], "count": r[1]} for r in class_rows],
        "gender_breakdown": {r[0]: r[1] for r in gender_rows if r[0]},
        "natural_summary": (
            f"The school has {total_students} students ({active_students} active) "
            f"and {total_staff} staff members in the {current_year.name if current_year else 'current'} academic year."
        ),
    }

    _log_agent(db, request, "stats", "Agent fetched school stats")
    return result


@router.get("/students")
@limiter.limit("60/minute")
def agent_search_students(
    request: Request,
    q: Optional[str] = Query(None, description="Search by name or admission number"),
    class_name: Optional[str] = Query(None),
    section: Optional[str] = Query(None),
    status_filter: Optional[str] = Query(None, alias="status"),
    limit: int = Query(20, ge=1, le=100),
    _key: str = Depends(verify_agent_key),
    db: Session = Depends(get_db),
):
    """Search students. Returns up to 100 results."""
    query = db.query(Student)

    if q:
        like = f"%{q.strip()}%"
        from sqlalchemy import or_
        query = query.filter(or_(
            Student.first_name.ilike(like),
            Student.last_name.ilike(like),
            Student.admission_no.ilike(like),
        ))

    if class_name:
        query = query.join(Class, Student.class_id == Class.id).filter(
            Class.name.ilike(f"%{class_name}%")
        )

    if section:
        query = query.join(Section, Student.section_id == Section.id).filter(
            Section.name.ilike(f"%{section}%")
        )

    if status_filter:
        try:
            query = query.filter(Student.status == StudentStatus(status_filter))
        except ValueError:
            pass

    rows = query.order_by(Student.first_name).limit(limit).all()
    items = [_student_to_dict(s) for s in rows]

    _log_agent(db, request, "search_students", f"Agent searched students: q={q!r} class={class_name!r}")

    return {
        "count": len(items),
        "query": q,
        "results": items,
        "natural_summary": (
            f"Found {len(items)} student(s)" +
            (f" matching '{q}'" if q else "") +
            (f" in {class_name}" if class_name else "") + "."
            if items else f"No students found matching your criteria."
        ),
    }


@router.get("/students/{student_id}")
@limiter.limit("60/minute")
def agent_get_student(
    student_id: int,
    request: Request,
    _key: str = Depends(verify_agent_key),
    db: Session = Depends(get_db),
):
    """Get full student record (profile + guardians). Excludes sensitive financial fields."""
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    result = _student_to_dict(student)

    # Add extended profile (excluding financial/identity sensitive fields)
    if student.profile:
        p = student.profile
        result["profile"] = {
            "blood_group": p.blood_group,
            "category": p.category,
            "religion": p.religion,
            "nationality": p.nationality,
            "mother_tongue": p.mother_tongue,
            "previous_school": p.previous_school,
            "height": p.height,
            "weight": p.weight,
            "vision": p.vision,
            "is_transport": p.is_transport,
            "pickup_route": p.pickup_route,
            "drop_route": p.drop_route,
            # bank_name, account_no, aadhaar_no, pen_no etc. intentionally excluded
        }

    # All guardians
    result["guardians"] = [
        {
            "name": link.guardian.name,
            "relation": link.guardian.relation,
            "phone": link.guardian.phone,
            "email": link.guardian.email,
            "is_primary": link.is_primary,
        }
        for link in student.guardians
    ]

    _log_agent(db, request, "get_student", f"Agent fetched student id={student_id}")
    return result


@router.get("/staff")
@limiter.limit("60/minute")
def agent_search_staff(
    request: Request,
    q: Optional[str] = Query(None, description="Search by name, email, or department"),
    department: Optional[str] = Query(None),
    limit: int = Query(20, ge=1, le=100),
    _key: str = Depends(verify_agent_key),
    db: Session = Depends(get_db),
):
    """Search staff members."""
    from sqlalchemy import or_
    from models import StaffProfile, UserRole

    query = db.query(User).filter(User.role != UserRole.super_admin)

    if q:
        like = f"%{q.strip()}%"
        query = query.filter(or_(
            User.name.ilike(like),
            User.email.ilike(like),
        ))

    rows = query.order_by(User.name).limit(limit).all()

    def _staff_dict(u: User) -> dict:
        p = u.profile
        summary = f"{u.name}, {p.designation or p.department or u.role}"
        if p and p.department:
            summary += f", {p.department}"

        return {
            "id": u.id,
            "name": u.name,
            "email": u.email,
            "role": u.role.value if hasattr(u.role, "value") else str(u.role),
            "designation": p.designation if p else None,
            "department": p.department if p else None,
            "phone": None,  # not stored on User; kept for schema consistency
            "natural_summary": summary,
        }

    items = [_staff_dict(u) for u in rows]

    if department:
        items = [i for i in items if i["department"] and department.lower() in i["department"].lower()]

    _log_agent(db, request, "search_staff", f"Agent searched staff: q={q!r} dept={department!r}")

    return {
        "count": len(items),
        "query": q,
        "results": items,
        "natural_summary": (
            f"Found {len(items)} staff member(s)" +
            (f" matching '{q}'" if q else "") + "."
            if items else "No staff found matching your criteria."
        ),
    }


@router.get("/attendance")
@limiter.limit("60/minute")
def agent_attendance(
    request: Request,
    student_id: Optional[int] = Query(None),
    admission_no: Optional[str] = Query(None),
    _key: str = Depends(verify_agent_key),
    db: Session = Depends(get_db),
):
    """Attendance summary for a specific student."""
    if not student_id and not admission_no:
        raise HTTPException(status_code=400, detail="Provide student_id or admission_no.")

    student = None
    if student_id:
        student = db.query(Student).filter(Student.id == student_id).first()
    elif admission_no:
        student = db.query(Student).filter(Student.admission_no == admission_no).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not found.")

    entries = db.query(AttendanceEntry).filter(AttendanceEntry.student_id == student.id).all()

    total = len(entries)
    present = sum(1 for e in entries if e.status == AttendanceStatus.present)
    absent = sum(1 for e in entries if e.status == AttendanceStatus.absent)
    late = sum(1 for e in entries if e.status == AttendanceStatus.late)
    leave = total - present - absent - late
    pct = round(present / total * 100, 1) if total else 0

    name = f"{student.first_name} {student.last_name or ''}".strip()

    _log_agent(db, request, "attendance", f"Agent fetched attendance for student id={student.id}")

    return {
        "student_id": student.id,
        "student_name": name,
        "admission_no": student.admission_no,
        "total_days": total,
        "present": present,
        "absent": absent,
        "late": late,
        "leave": leave,
        "attendance_percentage": pct,
        "natural_summary": (
            f"{name} has attended {present} out of {total} days "
            f"({pct}% attendance). "
            f"Absent: {absent}, Late: {late}."
        ) if total else f"No attendance records found for {name}.",
    }


@router.get("/verify-phone")
@limiter.limit("30/minute")
def agent_verify_phone(
    request: Request,
    phone: str = Query(..., description="Phone number to verify (digits only)"),
    _key: str = Depends(verify_agent_key),
    db: Session = Depends(get_db),
):
    """
    Verify a phone number and return the caller's role + authorized student IDs.

    Roles:
    - staff    → full access to all data
    - guardian → can only access their linked children's data
    - unknown  → no access to personal data

    Used by the Telegram bot to authenticate users who share their contact.
    """
    from models import StaffProfile, StudentGuardian

    # Normalize phone — strip country code prefix if present
    digits = "".join(c for c in phone if c.isdigit())
    # Match last 10 digits to handle +91XXXXXXXXXX format
    phone_10 = digits[-10:] if len(digits) >= 10 else digits

    def _phone_match(stored: str) -> bool:
        if not stored:
            return False
        stored_digits = "".join(c for c in stored if c.isdigit())
        return stored_digits[-10:] == phone_10 if len(stored_digits) >= 10 else stored_digits == phone_10

    # 1. Check staff
    staff_profiles = db.query(StaffProfile).all()
    for profile in staff_profiles:
        if _phone_match(profile.phone or ""):
            user = profile.user
            _log_agent(db, request, "verify_phone", f"Staff auth: {user.name} ({phone_10})")
            return {
                "role": "staff",
                "name": user.name,
                "authorized_student_ids": [],  # empty = all access
                "natural_summary": f"Authenticated as staff: {user.name}",
            }

    # 2. Check guardian phone
    guardians = db.query(Guardian).all()
    for g in guardians:
        if _phone_match(g.phone or ""):
            links = db.query(StudentGuardian).filter(StudentGuardian.guardian_id == g.id).all()
            student_ids = [link.student_id for link in links]
            student_names = []
            for sid in student_ids:
                s = db.query(Student).filter(Student.id == sid).first()
                if s:
                    student_names.append(f"{s.first_name} {s.last_name or ''}".strip())

            _log_agent(db, request, "verify_phone", f"Guardian auth: {g.name} ({phone_10}) → students {student_ids}")
            return {
                "role": "guardian",
                "name": g.name,
                "authorized_student_ids": student_ids,
                "authorized_student_names": student_names,
                "natural_summary": (
                    f"Authenticated as guardian: {g.name}. "
                    f"Children: {', '.join(student_names) or 'none found'}."
                ),
            }

    # 3. Check student's own phone
    students = db.query(Student).all()
    for s in students:
        if _phone_match(s.phone or ""):
            _log_agent(db, request, "verify_phone", f"Student auth: {s.first_name} ({phone_10})")
            return {
                "role": "guardian",  # treat same as guardian — own data only
                "name": f"{s.first_name} {s.last_name or ''}".strip(),
                "authorized_student_ids": [s.id],
                "authorized_student_names": [f"{s.first_name} {s.last_name or ''}".strip()],
                "natural_summary": f"Authenticated as student: {s.first_name}.",
            }

    # 4. Not found
    _log_agent(db, request, "verify_phone", f"Unknown phone: {phone_10}")
    return {
        "role": "unknown",
        "name": None,
        "authorized_student_ids": [],
        "natural_summary": "Phone number not found in school records.",
    }

