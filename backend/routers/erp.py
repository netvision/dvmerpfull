from decimal import Decimal
from typing import List, Optional
from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import and_, func, or_
from sqlalchemy.orm import Session

from audit import write_audit_log
from auth import ROLE_CAPABILITIES, get_current_user, require_admin, require_capability
from database import get_db
from models import (
    AcademicYear,
    AuditLog,
    AttendanceEntry,
    AttendanceSession,
    AttendanceStatus,
    Class,
    FeeHead,
    FeeInvoice,
    FeeReceipt,
    FeeStructure,
    FeeStructureItem,
    InvoiceStatus,
    PaymentMode,
    Section,
    Student,
    StudentFeeAssignment,
    StudentStatus,
    User,
)
from schemas import (
        AuditLogListOut,
        AuditLogOut,
    AcademicYearOut,
    AcademicYearCreateIn,
    AttendanceEntryCreateIn,
    AttendanceEntryOut,
    AttendanceEntryUpdateIn,
    AttendanceSummaryOut,
    AttendanceSessionCreateIn,
    AttendanceSessionOut,
    BulkAttendanceMarkIn,
    ClassCreateIn,
    ClassOut,
    ERPRoleMatrixOut,
    FeeHeadCreateIn,
    FeeHeadOut,
    FeeHeadUpdateIn,
    FeeInvoiceCreateIn,
    FeeInvoiceOut,
    FeeReceiptCreateIn,
    FeeReceiptOut,
    FeeStructureCreateIn,
    FeeStructureOut,
    FeeStructureItemOut,
    SectionCreateIn,
    SectionOut,
    StudentFeeAssignmentCreateIn,
    StudentFeeAssignmentOut,
    StudentCreateIn,
    StudentOut,
    StudentListOut,
    StudentUpdateIn,
)

router = APIRouter(prefix="/erp")


def _student_status_from_str(raw: str) -> StudentStatus:
    try:
        return StudentStatus(raw)
    except ValueError:
        allowed = ", ".join([s.value for s in StudentStatus])
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid student status '{raw}'. Must be one of: {allowed}",
        )


def _validate_student_refs(
    db: Session,
    *,
    class_id: int,
    section_id: Optional[int],
    academic_year_id: int,
) -> tuple[Class, Optional[Section], AcademicYear]:
    cls = db.query(Class).filter(Class.id == class_id).first()
    if cls is None:
        raise HTTPException(status_code=404, detail="Class not found")

    academic_year = db.query(AcademicYear).filter(AcademicYear.id == academic_year_id).first()
    if academic_year is None:
        raise HTTPException(status_code=404, detail="Academic year not found")

    section = None
    if section_id is not None:
        section = db.query(Section).filter(Section.id == section_id).first()
        if section is None:
            raise HTTPException(status_code=404, detail="Section not found")
        if section.class_id != class_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Section does not belong to the selected class",
            )

    return cls, section, academic_year


def _student_to_out(student: Student) -> StudentOut:
    return StudentOut(
        id=student.id,
        admission_no=student.admission_no,
        roll_no=student.roll_no,
        first_name=student.first_name,
        last_name=student.last_name,
        date_of_birth=student.date_of_birth,
        gender=student.gender,
        phone=student.phone,
        email=student.email,
        address=student.address,
        class_id=student.class_id,
        class_name=student.cls.name if student.cls else None,
        section_id=student.section_id,
        section_name=student.section.name if student.section else None,
        academic_year_id=student.academic_year_id,
        academic_year_name=student.academic_year.name if student.academic_year else None,
        status=student.status.value if hasattr(student.status, "value") else str(student.status),
        is_active=student.is_active,
    )


def _student_snapshot(student: Student) -> dict:
    return {
        "id": student.id,
        "admission_no": student.admission_no,
        "roll_no": student.roll_no,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "date_of_birth": student.date_of_birth,
        "gender": student.gender,
        "phone": student.phone,
        "email": student.email,
        "address": student.address,
        "class_id": student.class_id,
        "section_id": student.section_id,
        "academic_year_id": student.academic_year_id,
        "status": student.status.value if hasattr(student.status, "value") else str(student.status),
        "is_active": student.is_active,
    }


@router.get("/rbac-matrix", response_model=List[ERPRoleMatrixOut])
def get_rbac_matrix(current_user: User = Depends(get_current_user)):
    del current_user
    return [
        ERPRoleMatrixOut(role=role.value, capabilities=caps)
        for role, caps in ROLE_CAPABILITIES.items()
    ]


@router.get("/lookups/academic-years", response_model=List[AcademicYearOut])
def list_academic_years(
    _user: User = Depends(require_capability("erp_student_read")),
    db: Session = Depends(get_db),
):
    rows = db.query(AcademicYear).order_by(AcademicYear.start_date.desc(), AcademicYear.id.desc()).all()
    return rows


@router.get("/lookups/classes", response_model=List[ClassOut])
def list_classes(
    _user: User = Depends(require_capability("erp_student_read")),
    db: Session = Depends(get_db),
):
    return db.query(Class).order_by(Class.id).all()


@router.post("/lookups/classes", response_model=ClassOut, status_code=201)
def create_class_lookup(
    body: ClassCreateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Class name is required")

    existing = db.query(Class).filter(func.lower(Class.name) == name.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Class with this name already exists")

    row = Class(name=name)
    db.add(row)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="class",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Class created: {row.name}",
        after_payload={"id": row.id, "name": row.name},
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return row


@router.get("/lookups/sections", response_model=List[SectionOut])
def list_sections(
    class_id: Optional[int] = Query(None),
    _user: User = Depends(require_capability("erp_student_read")),
    db: Session = Depends(get_db),
):
    query = db.query(Section)
    if class_id is not None:
        query = query.filter(Section.class_id == class_id)
    return query.order_by(Section.class_id, Section.id).all()


@router.post("/lookups/sections", response_model=SectionOut, status_code=201)
def create_section_lookup(
    body: SectionCreateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Section name is required")

    cls = db.query(Class).filter(Class.id == body.class_id).first()
    if cls is None:
        raise HTTPException(status_code=404, detail="Class not found")

    existing = db.query(Section).filter(
        and_(Section.class_id == body.class_id, func.lower(Section.name) == name.lower())
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Section already exists for this class")

    row = Section(class_id=body.class_id, name=name)
    db.add(row)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="section",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Section created: {name} for class {body.class_id}",
        after_payload={"id": row.id, "class_id": row.class_id, "name": row.name},
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return row


@router.post("/lookups/academic-years", response_model=AcademicYearOut, status_code=201)
def create_academic_year_lookup(
    body: AcademicYearCreateIn,
    request: Request,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    name = body.name.strip()
    if not name:
        raise HTTPException(status_code=400, detail="Academic year name is required")
    if body.start_date >= body.end_date:
        raise HTTPException(status_code=400, detail="start_date must be before end_date")

    existing = db.query(AcademicYear).filter(func.lower(AcademicYear.name) == name.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Academic year with this name already exists")

    row = AcademicYear(
        name=name,
        start_date=body.start_date,
        end_date=body.end_date,
        is_active=body.is_active,
    )
    db.add(row)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="academic_year",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Academic year created: {row.name}",
        after_payload={
            "id": row.id,
            "name": row.name,
            "start_date": str(row.start_date),
            "end_date": str(row.end_date),
            "is_active": row.is_active,
        },
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return row


@router.get("/students", response_model=StudentListOut)
def list_students(
    class_id: Optional[int] = None,
    section_id: Optional[int] = None,
    academic_year_id: Optional[int] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    q: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    _user: User = Depends(require_capability("erp_student_read")),
    db: Session = Depends(get_db),
):
    query = db.query(Student)

    if class_id is not None:
        query = query.filter(Student.class_id == class_id)
    if section_id is not None:
        query = query.filter(Student.section_id == section_id)
    if academic_year_id is not None:
        query = query.filter(Student.academic_year_id == academic_year_id)
    if status_filter is not None:
        query = query.filter(Student.status == _student_status_from_str(status_filter))

    if q:
        like_q = f"%{q.strip()}%"
        query = query.filter(
            or_(
                Student.admission_no.ilike(like_q),
                Student.roll_no.ilike(like_q),
                Student.first_name.ilike(like_q),
                Student.last_name.ilike(like_q),
            )
        )

    total = query.count()
    rows = query.order_by(Student.id.desc()).offset(offset).limit(limit).all()
    items = [_student_to_out(row) for row in rows]
    return StudentListOut(items=items, total=total)


@router.get("/students/{student_id}", response_model=StudentOut)
def get_student(
    student_id: int,
    _user: User = Depends(require_capability("erp_student_read")),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return _student_to_out(student)


@router.post("/students", response_model=StudentOut, status_code=201)
def create_student(
    body: StudentCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_student_write")),
    db: Session = Depends(get_db),
):
    existing = db.query(Student).filter(Student.admission_no == body.admission_no).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admission number already exists",
        )

    _validate_student_refs(
        db,
        class_id=body.class_id,
        section_id=body.section_id,
        academic_year_id=body.academic_year_id,
    )

    student = Student(
        admission_no=body.admission_no,
        roll_no=body.roll_no,
        first_name=body.first_name,
        last_name=body.last_name,
        date_of_birth=body.date_of_birth,
        gender=body.gender,
        phone=body.phone,
        email=body.email,
        address=body.address,
        class_id=body.class_id,
        section_id=body.section_id,
        academic_year_id=body.academic_year_id,
        status=_student_status_from_str(body.status),
        is_active=True,
    )
    db.add(student)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="student",
        entity_id=str(student.id),
        action="create",
        change_summary=f"Student created: {student.admission_no}",
        before_payload=None,
        after_payload=_student_snapshot(student),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(student)
    return _student_to_out(student)


@router.put("/students/{student_id}", response_model=StudentOut)
def update_student(
    student_id: int,
    body: StudentUpdateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_student_write")),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    before = _student_snapshot(student)

    if body.admission_no is not None and body.admission_no != student.admission_no:
        duplicate = db.query(Student).filter(Student.admission_no == body.admission_no).first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admission number already exists",
            )
        student.admission_no = body.admission_no

    if body.roll_no is not None:
        student.roll_no = body.roll_no
    if body.first_name is not None:
        student.first_name = body.first_name
    if body.last_name is not None:
        student.last_name = body.last_name
    if body.date_of_birth is not None:
        student.date_of_birth = body.date_of_birth
    if body.gender is not None:
        student.gender = body.gender
    if body.phone is not None:
        student.phone = body.phone
    if body.email is not None:
        student.email = body.email
    if body.address is not None:
        student.address = body.address

    if body.class_id is not None:
        student.class_id = body.class_id
    if "section_id" in body.model_fields_set:
        student.section_id = body.section_id
    if body.academic_year_id is not None:
        student.academic_year_id = body.academic_year_id
    if body.status is not None:
        student.status = _student_status_from_str(body.status)
    if body.is_active is not None:
        student.is_active = body.is_active

    _validate_student_refs(
        db,
        class_id=student.class_id,
        section_id=student.section_id,
        academic_year_id=student.academic_year_id,
    )

    after = _student_snapshot(student)
    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="student",
        entity_id=str(student.id),
        action="update",
        change_summary=f"Student updated: {student.admission_no}",
        before_payload=before,
        after_payload=after,
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(student)
    return _student_to_out(student)


# ============================================================================
# Attendance Module Endpoints
# ============================================================================

def _validate_attendance_refs(db: Session, class_id: int, section_id: int, academic_year_id: int):
    """Validate that class, section, and academic_year exist and are valid."""
    cls = db.query(Class).filter(Class.id == class_id).first()
    if not cls:
        raise HTTPException(status_code=404, detail=f"Class {class_id} not found")

    section = db.query(Section).filter(
        and_(Section.id == section_id, Section.class_id == class_id)
    ).first()
    if not section:
        raise HTTPException(status_code=404, detail=f"Section {section_id} not found for class {class_id}")

    year = db.query(AcademicYear).filter(AcademicYear.id == academic_year_id).first()
    if not year:
        raise HTTPException(status_code=404, detail=f"Academic year {academic_year_id} not found")


def _attendance_session_snapshot(session: AttendanceSession) -> dict:
    """Capture attendance session state as dict for audit logging."""
    return {
        "id": str(session.id),
        "class_id": session.class_id,
        "section_id": session.section_id,
        "academic_year_id": session.academic_year_id,
        "attendance_date": session.attendance_date.isoformat() if session.attendance_date else None,
        "marked_by_id": session.marked_by_id,
        "remarks": session.remarks,
    }


def _attendance_entry_snapshot(entry: AttendanceEntry) -> dict:
    """Capture attendance entry state as dict for audit logging."""
    return {
        "id": str(entry.id),
        "session_id": str(entry.session_id),
        "student_id": str(entry.student_id),
        "status": entry.status.value if entry.status else None,
        "remarks": entry.remarks,
    }


def _attendance_session_to_out(session: AttendanceSession) -> AttendanceSessionOut:
    """Convert ORM session to response DTO."""
    return AttendanceSessionOut(
        id=session.id,
        class_id=session.class_id,
        section_id=session.section_id,
        academic_year_id=session.academic_year_id,
        class_name=session.cls.name if session.cls else None,
        section_name=session.section.name if session.section else None,
        academic_year_name=session.academic_year.name if session.academic_year else None,
        attendance_date=session.attendance_date,
        marked_by_id=session.marked_by_id,
        marked_at=session.marked_at,
        remarks=session.remarks,
        entries_count=len(session.entries) if session.entries else 0,
    )


def _attendance_entry_to_out(entry: AttendanceEntry) -> AttendanceEntryOut:
    """Convert ORM entry to response DTO."""
    return AttendanceEntryOut(
        id=entry.id,
        session_id=entry.session_id,
        student_id=entry.student_id,
        student_name=f"{entry.student.first_name} {entry.student.last_name}" if entry.student else None,
        admission_no=entry.student.admission_no if entry.student else None,
        status=entry.status.value if entry.status else None,
        remarks=entry.remarks,
    )


@router.post("/attendance-sessions", response_model=AttendanceSessionOut, status_code=201)
def create_attendance_session(
    body: AttendanceSessionCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_attendance_write")),
    db: Session = Depends(get_db),
):
    """Create a new attendance session for marking attendance on a specific date."""
    _validate_attendance_refs(db, body.class_id, body.section_id, body.academic_year_id)

    # Check for duplicate session on same date
    existing = db.query(AttendanceSession).filter(
        and_(
            AttendanceSession.class_id == body.class_id,
            AttendanceSession.section_id == body.section_id,
            AttendanceSession.academic_year_id == body.academic_year_id,
            AttendanceSession.attendance_date == body.attendance_date,
        )
    ).first()
    if existing:
        raise HTTPException(
            status_code=409,
            detail=f"Attendance session already exists for class {body.class_id}, section {body.section_id} on {body.attendance_date}",
        )

    session = AttendanceSession(
        class_id=body.class_id,
        section_id=body.section_id,
        academic_year_id=body.academic_year_id,
        attendance_date=body.attendance_date,
        marked_by_id=current_user.id,
        remarks=body.remarks,
    )
    db.add(session)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="attendance_session",
        entity_id=str(session.id),
        action="create",
        change_summary=f"Attendance session created for class {body.class_id}, section {body.section_id} on {body.attendance_date}",
        after_payload=_attendance_session_snapshot(session),
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(session)
    return _attendance_session_to_out(session)


@router.post("/attendance-sessions/{session_id}/mark", response_model=List[AttendanceEntryOut], status_code=201)
def mark_attendance_entries(
    session_id: int,
    body: BulkAttendanceMarkIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_attendance_write")),
    db: Session = Depends(get_db),
):
    """Bulk mark attendance entries for a session."""
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Attendance session {session_id} not found")

    # Validate all students exist in this class/section
    student_ids = [e.student_id for e in body.entries]
    students = db.query(Student).filter(
        and_(
            Student.id.in_(student_ids),
            Student.class_id == session.class_id,
            Student.section_id == session.section_id,
        )
    ).all()
    if len(students) != len(set(student_ids)):
        raise HTTPException(
            status_code=400,
            detail=f"One or more students not found in class {session.class_id}, section {session.section_id}",
        )

    results = []
    for entry_in in body.entries:
        # Check if entry already exists
        existing_entry = db.query(AttendanceEntry).filter(
            and_(
                AttendanceEntry.session_id == session_id,
                AttendanceEntry.student_id == entry_in.student_id,
            )
        ).first()

        if existing_entry:
            before = _attendance_entry_snapshot(existing_entry)
            existing_entry.status = AttendanceStatus(entry_in.status)
            existing_entry.remarks = entry_in.remarks
            after = _attendance_entry_snapshot(existing_entry)
            action = "update"
        else:
            existing_entry = AttendanceEntry(
                session_id=session_id,
                student_id=entry_in.student_id,
                status=AttendanceStatus(entry_in.status),
                remarks=entry_in.remarks,
            )
            db.add(existing_entry)
            db.flush()
            before = None
            after = _attendance_entry_snapshot(existing_entry)
            action = "create"

        write_audit_log(
            db,
            actor_user_id=current_user.id,
            entity_type="attendance_entry",
            entity_id=str(existing_entry.id),
            action=action,
            change_summary=f"Attendance marked for student {entry_in.student_id}: {entry_in.status}",
            before_payload=before,
            after_payload=after,
            ip_address=request.client.host if request.client else None,
        )

        results.append(_attendance_entry_to_out(existing_entry))

    db.commit()
    return results


@router.get("/attendance-sessions", response_model=List[AttendanceSessionOut])
def list_attendance_sessions(
    class_id: Optional[int] = Query(None),
    section_id: Optional[int] = Query(None),
    academic_year_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(require_capability("erp_attendance_read")),
    db: Session = Depends(get_db),
):
    """List attendance sessions with optional filters."""
    query = db.query(AttendanceSession)

    if class_id:
        query = query.filter(AttendanceSession.class_id == class_id)
    if section_id:
        query = query.filter(AttendanceSession.section_id == section_id)
    if academic_year_id:
        query = query.filter(AttendanceSession.academic_year_id == academic_year_id)
    if date_from:
        query = query.filter(AttendanceSession.attendance_date >= date_from)
    if date_to:
        query = query.filter(AttendanceSession.attendance_date <= date_to)

    query = query.order_by(AttendanceSession.attendance_date.desc())
    sessions = query.limit(limit).offset(offset).all()
    return [_attendance_session_to_out(s) for s in sessions]


@router.get("/attendance-sessions/{session_id}/entries", response_model=List[AttendanceEntryOut])
def get_attendance_entries(
    session_id: int,
    current_user: User = Depends(require_capability("erp_attendance_read")),
    db: Session = Depends(get_db),
):
    """Get all attendance entries for a specific session."""
    session = db.query(AttendanceSession).filter(AttendanceSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail=f"Attendance session {session_id} not found")

    entries = db.query(AttendanceEntry).filter(AttendanceEntry.session_id == session_id).all()
    return [_attendance_entry_to_out(e) for e in entries]


@router.get("/attendance-report", response_model=AttendanceSummaryOut)
def get_attendance_summary(
    class_id: Optional[int] = Query(None),
    section_id: Optional[int] = Query(None),
    academic_year_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    current_user: User = Depends(require_capability("erp_attendance_read")),
    db: Session = Depends(get_db),
):
    """Get attendance summary statistics (counts by status)."""
    query = db.query(AttendanceEntry).join(AttendanceSession)

    if class_id:
        query = query.filter(AttendanceSession.class_id == class_id)
    if section_id:
        query = query.filter(AttendanceSession.section_id == section_id)
    if academic_year_id:
        query = query.filter(AttendanceSession.academic_year_id == academic_year_id)
    if date_from:
        query = query.filter(AttendanceSession.attendance_date >= date_from)
    if date_to:
        query = query.filter(AttendanceSession.attendance_date <= date_to)

    entries = query.all()

    # Count by status
    status_counts = {
        "present": sum(1 for e in entries if e.status == AttendanceStatus.present),
        "absent": sum(1 for e in entries if e.status == AttendanceStatus.absent),
        "late": sum(1 for e in entries if e.status == AttendanceStatus.late),
        "leave": sum(1 for e in entries if e.status == AttendanceStatus.leave),
    }

    return AttendanceSummaryOut(
        total_entries=len(entries),
        present=status_counts["present"],
        absent=status_counts["absent"],
        late=status_counts["late"],
        leave=status_counts["leave"],
    )


# ============================================================================
# Fee Module Endpoints
# ============================================================================


def _fee_head_to_out(row: FeeHead) -> FeeHeadOut:
    return FeeHeadOut(
        id=row.id,
        name=row.name,
        code=row.code,
        description=row.description,
        is_active=row.is_active,
    )


def _fee_structure_to_out(row: FeeStructure) -> FeeStructureOut:
    items = []
    for item in row.items:
        items.append(
            FeeStructureItemOut(
                id=item.id,
                fee_head_id=item.fee_head_id,
                fee_head_name=item.fee_head.name if item.fee_head else None,
                amount=float(item.amount),
                due_day=item.due_day,
            )
        )

    return FeeStructureOut(
        id=row.id,
        name=row.name,
        class_id=row.class_id,
        class_name=row.cls.name if row.cls else None,
        academic_year_id=row.academic_year_id,
        academic_year_name=row.academic_year.name if row.academic_year else None,
        is_active=row.is_active,
        items=items,
    )


def _invoice_to_out(row: FeeInvoice) -> FeeInvoiceOut:
    return FeeInvoiceOut(
        id=row.id,
        invoice_no=row.invoice_no,
        student_id=row.student_id,
        student_name=(f"{row.student.first_name} {row.student.last_name}" if row.student else None),
        academic_year_id=row.academic_year_id,
        academic_year_name=row.academic_year.name if row.academic_year else None,
        invoice_date=row.invoice_date,
        due_date=row.due_date,
        total_amount=float(row.total_amount),
        discount_amount=float(row.discount_amount),
        paid_amount=float(row.paid_amount),
        balance_amount=float(row.balance_amount),
        status=row.status.value if hasattr(row.status, "value") else str(row.status),
        notes=row.notes,
    )


def _receipt_to_out(row: FeeReceipt) -> FeeReceiptOut:
    return FeeReceiptOut(
        id=row.id,
        receipt_no=row.receipt_no,
        invoice_id=row.invoice_id,
        student_id=row.student_id,
        student_name=(f"{row.student.first_name} {row.student.last_name}" if row.student else None),
        receipt_date=row.receipt_date,
        amount=float(row.amount),
        payment_mode=row.payment_mode.value if hasattr(row.payment_mode, "value") else str(row.payment_mode),
        reference_no=row.reference_no,
        notes=row.notes,
    )


def _payment_mode_from_str(raw: str) -> PaymentMode:
    try:
        return PaymentMode(raw)
    except ValueError:
        allowed = ", ".join([v.value for v in PaymentMode])
        raise HTTPException(status_code=400, detail=f"Invalid payment_mode '{raw}'. Must be one of: {allowed}")


@router.get("/fee-heads", response_model=List[FeeHeadOut])
def list_fee_heads(
    _user: User = Depends(require_capability("erp_fee_read")),
    db: Session = Depends(get_db),
):
    rows = db.query(FeeHead).order_by(FeeHead.name.asc()).all()
    return [_fee_head_to_out(r) for r in rows]


@router.post("/fee-heads", response_model=FeeHeadOut, status_code=201)
def create_fee_head(
    body: FeeHeadCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_fee_write")),
    db: Session = Depends(get_db),
):
    code = body.code.strip().upper()
    if not code:
        raise HTTPException(status_code=400, detail="Fee head code is required")

    existing = db.query(FeeHead).filter(func.lower(FeeHead.code) == code.lower()).first()
    if existing:
        raise HTTPException(status_code=400, detail="Fee head code already exists")

    row = FeeHead(
        name=body.name.strip(),
        code=code,
        description=body.description,
        is_active=body.is_active,
    )
    db.add(row)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="fee_head",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Fee head created: {row.code}",
        after_payload={"id": row.id, "name": row.name, "code": row.code, "is_active": row.is_active},
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return _fee_head_to_out(row)


@router.put("/fee-heads/{fee_head_id}", response_model=FeeHeadOut)
def update_fee_head(
    fee_head_id: int,
    body: FeeHeadUpdateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_fee_write")),
    db: Session = Depends(get_db),
):
    row = db.query(FeeHead).filter(FeeHead.id == fee_head_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Fee head not found")

    before = {"name": row.name, "description": row.description, "is_active": row.is_active}
    if body.name is not None:
        row.name = body.name.strip()
    if body.description is not None:
        row.description = body.description
    if body.is_active is not None:
        row.is_active = body.is_active

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="fee_head",
        entity_id=str(row.id),
        action="update",
        change_summary=f"Fee head updated: {row.code}",
        before_payload=before,
        after_payload={"name": row.name, "description": row.description, "is_active": row.is_active},
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return _fee_head_to_out(row)


@router.get("/fee-structures", response_model=List[FeeStructureOut])
def list_fee_structures(
    class_id: Optional[int] = Query(None),
    academic_year_id: Optional[int] = Query(None),
    _user: User = Depends(require_capability("erp_fee_read")),
    db: Session = Depends(get_db),
):
    query = db.query(FeeStructure)
    if class_id is not None:
        query = query.filter(FeeStructure.class_id == class_id)
    if academic_year_id is not None:
        query = query.filter(FeeStructure.academic_year_id == academic_year_id)
    rows = query.order_by(FeeStructure.id.desc()).all()
    return [_fee_structure_to_out(r) for r in rows]


@router.post("/fee-structures", response_model=FeeStructureOut, status_code=201)
def create_fee_structure(
    body: FeeStructureCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_fee_write")),
    db: Session = Depends(get_db),
):
    cls = db.query(Class).filter(Class.id == body.class_id).first()
    if cls is None:
        raise HTTPException(status_code=404, detail="Class not found")

    year = db.query(AcademicYear).filter(AcademicYear.id == body.academic_year_id).first()
    if year is None:
        raise HTTPException(status_code=404, detail="Academic year not found")

    duplicate = db.query(FeeStructure).filter(
        and_(
            FeeStructure.name == body.name,
            FeeStructure.class_id == body.class_id,
            FeeStructure.academic_year_id == body.academic_year_id,
        )
    ).first()
    if duplicate:
        raise HTTPException(status_code=400, detail="Fee structure already exists for this scope")

    row = FeeStructure(
        name=body.name.strip(),
        class_id=body.class_id,
        academic_year_id=body.academic_year_id,
        is_active=body.is_active,
    )
    db.add(row)
    db.flush()

    for item in body.items:
        head = db.query(FeeHead).filter(FeeHead.id == item.fee_head_id).first()
        if head is None:
            raise HTTPException(status_code=404, detail=f"Fee head {item.fee_head_id} not found")
        db.add(
            FeeStructureItem(
                fee_structure_id=row.id,
                fee_head_id=item.fee_head_id,
                amount=Decimal(str(item.amount)),
                due_day=item.due_day,
            )
        )

    db.flush()
    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="fee_structure",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Fee structure created: {row.name}",
        after_payload={
            "id": row.id,
            "name": row.name,
            "class_id": row.class_id,
            "academic_year_id": row.academic_year_id,
            "items_count": len(body.items),
        },
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return _fee_structure_to_out(row)


@router.post("/fee-assignments", response_model=StudentFeeAssignmentOut, status_code=201)
def create_fee_assignment(
    body: StudentFeeAssignmentCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_fee_write")),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == body.student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    structure = db.query(FeeStructure).filter(FeeStructure.id == body.fee_structure_id).first()
    if structure is None:
        raise HTTPException(status_code=404, detail="Fee structure not found")

    row = StudentFeeAssignment(
        student_id=body.student_id,
        fee_structure_id=body.fee_structure_id,
        academic_year_id=body.academic_year_id,
        effective_from=body.effective_from,
        effective_to=body.effective_to,
        is_active=body.is_active,
    )
    db.add(row)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="fee_assignment",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Fee assignment created for student {row.student_id}",
        after_payload={
            "student_id": row.student_id,
            "fee_structure_id": row.fee_structure_id,
            "academic_year_id": row.academic_year_id,
            "is_active": row.is_active,
        },
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return StudentFeeAssignmentOut(
        id=row.id,
        student_id=row.student_id,
        student_name=f"{row.student.first_name} {row.student.last_name}" if row.student else None,
        fee_structure_id=row.fee_structure_id,
        fee_structure_name=row.fee_structure.name if row.fee_structure else None,
        academic_year_id=row.academic_year_id,
        academic_year_name=row.academic_year.name if row.academic_year else None,
        effective_from=row.effective_from,
        effective_to=row.effective_to,
        is_active=row.is_active,
    )


@router.get("/fee-invoices", response_model=List[FeeInvoiceOut])
def list_fee_invoices(
    student_id: Optional[int] = Query(None),
    _user: User = Depends(require_capability("erp_fee_read")),
    db: Session = Depends(get_db),
):
    query = db.query(FeeInvoice)
    if student_id is not None:
        query = query.filter(FeeInvoice.student_id == student_id)
    rows = query.order_by(FeeInvoice.id.desc()).all()
    return [_invoice_to_out(r) for r in rows]


@router.post("/fee-invoices", response_model=FeeInvoiceOut, status_code=201)
def create_fee_invoice(
    body: FeeInvoiceCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_fee_write")),
    db: Session = Depends(get_db),
):
    existing = db.query(FeeInvoice).filter(FeeInvoice.invoice_no == body.invoice_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Invoice number already exists")

    student = db.query(Student).filter(Student.id == body.student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    year = db.query(AcademicYear).filter(AcademicYear.id == body.academic_year_id).first()
    if year is None:
        raise HTTPException(status_code=404, detail="Academic year not found")

    total_amount = Decimal(str(body.total_amount))
    discount_amount = Decimal(str(body.discount_amount))
    if discount_amount < 0 or total_amount < 0:
        raise HTTPException(status_code=400, detail="Amounts must be non-negative")
    if discount_amount > total_amount:
        raise HTTPException(status_code=400, detail="Discount cannot exceed total amount")

    balance_amount = total_amount - discount_amount
    row = FeeInvoice(
        invoice_no=body.invoice_no.strip(),
        student_id=body.student_id,
        academic_year_id=body.academic_year_id,
        invoice_date=body.invoice_date,
        due_date=body.due_date,
        total_amount=total_amount,
        discount_amount=discount_amount,
        paid_amount=Decimal("0"),
        balance_amount=balance_amount,
        status=InvoiceStatus.issued,
        notes=body.notes,
    )
    db.add(row)
    db.flush()

    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="fee_invoice",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Fee invoice created: {row.invoice_no}",
        after_payload={
            "invoice_no": row.invoice_no,
            "student_id": row.student_id,
            "total_amount": str(row.total_amount),
            "balance_amount": str(row.balance_amount),
            "status": row.status.value,
        },
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return _invoice_to_out(row)


@router.get("/fee-receipts", response_model=List[FeeReceiptOut])
def list_fee_receipts(
    invoice_id: Optional[int] = Query(None),
    _user: User = Depends(require_capability("erp_fee_read")),
    db: Session = Depends(get_db),
):
    query = db.query(FeeReceipt)
    if invoice_id is not None:
        query = query.filter(FeeReceipt.invoice_id == invoice_id)
    rows = query.order_by(FeeReceipt.id.desc()).all()
    return [_receipt_to_out(r) for r in rows]


@router.post("/fee-receipts", response_model=FeeReceiptOut, status_code=201)
def create_fee_receipt(
    body: FeeReceiptCreateIn,
    request: Request,
    current_user: User = Depends(require_capability("erp_fee_write")),
    db: Session = Depends(get_db),
):
    existing = db.query(FeeReceipt).filter(FeeReceipt.receipt_no == body.receipt_no).first()
    if existing:
        raise HTTPException(status_code=400, detail="Receipt number already exists")

    invoice = db.query(FeeInvoice).filter(FeeInvoice.id == body.invoice_id).first()
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")

    amount = Decimal(str(body.amount))
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Receipt amount must be greater than 0")
    if amount > invoice.balance_amount:
        raise HTTPException(status_code=400, detail="Receipt amount cannot exceed invoice balance")

    row = FeeReceipt(
        receipt_no=body.receipt_no.strip(),
        invoice_id=invoice.id,
        student_id=invoice.student_id,
        receipt_date=body.receipt_date,
        amount=amount,
        payment_mode=_payment_mode_from_str(body.payment_mode),
        reference_no=body.reference_no,
        notes=body.notes,
        received_by_id=current_user.id,
    )
    db.add(row)

    invoice.paid_amount = invoice.paid_amount + amount
    invoice.balance_amount = invoice.balance_amount - amount
    if invoice.balance_amount <= 0:
        invoice.status = InvoiceStatus.paid
    elif invoice.paid_amount > 0:
        invoice.status = InvoiceStatus.partially_paid

    db.flush()
    write_audit_log(
        db,
        actor_user_id=current_user.id,
        entity_type="fee_receipt",
        entity_id=str(row.id),
        action="create",
        change_summary=f"Fee receipt created: {row.receipt_no}",
        after_payload={
            "receipt_no": row.receipt_no,
            "invoice_id": row.invoice_id,
            "amount": str(row.amount),
            "payment_mode": row.payment_mode.value,
        },
        ip_address=request.client.host if request.client else None,
    )

    db.commit()
    db.refresh(row)
    return _receipt_to_out(row)


@router.get("/audit-logs", response_model=AuditLogListOut)
def list_audit_logs(
    entity_type: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    actor_user_id: Optional[int] = Query(None),
    date_from: Optional[date] = Query(None),
    date_to: Optional[date] = Query(None),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    _user: User = Depends(require_capability("erp_audit_read")),
    db: Session = Depends(get_db),
):
    query = db.query(AuditLog)

    if entity_type:
        query = query.filter(AuditLog.entity_type == entity_type)
    if action:
        query = query.filter(AuditLog.action == action)
    if actor_user_id is not None:
        query = query.filter(AuditLog.actor_user_id == actor_user_id)
    if date_from:
        query = query.filter(func.date(AuditLog.created_at) >= date_from)
    if date_to:
        query = query.filter(func.date(AuditLog.created_at) <= date_to)

    total = query.count()
    rows = query.order_by(AuditLog.id.desc()).offset(offset).limit(limit).all()

    return AuditLogListOut(
        items=[
            AuditLogOut(
                id=row.id,
                actor_user_id=row.actor_user_id,
                entity_type=row.entity_type,
                entity_id=row.entity_id,
                action=row.action,
                change_summary=row.change_summary,
                before_payload=row.before_payload,
                after_payload=row.after_payload,
                ip_address=row.ip_address,
                created_at=row.created_at,
            )
            for row in rows
        ],
        total=total,
    )
