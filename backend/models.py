import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from database import Base


class UserRole(enum.Enum):
    teacher = "teacher"
    subject_head = "subject_head"
    mentor = "mentor"
    hm = "hm"
    principal = "principal"
    super_admin = "super_admin"


class NewsStatus(enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class EventStatus(enum.Enum):
    upcoming = "upcoming"
    ongoing = "ongoing"
    completed = "completed"
    cancelled = "cancelled"


class ExhibitFieldType(enum.Enum):
    string = "string"
    audio = "audio"
    image = "image"
    video = "video"
    link = "link"


class CMSCategory(Base):
    __tablename__ = "cms_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    news = relationship("CMSNews", back_populates="category")


class CMSNews(Base):
    __tablename__ = "cms_news"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True, index=True)
    excerpt = Column(Text, nullable=True)
    content = Column(Text, nullable=False)
    featured_image_url = Column(String, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("cms_categories.id"), nullable=True)
    status = Column(Enum(NewsStatus), nullable=False, default=NewsStatus.draft)
    views = Column(Integer, nullable=False, default=0)
    published_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    category = relationship("CMSCategory", back_populates="news")
    author = relationship("User")


class CMSEvent(Base):
    __tablename__ = "cms_events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    featured_image_url = Column(String, nullable=True)
    organizer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    capacity = Column(Integer, nullable=True)
    registered_count = Column(Integer, nullable=False, default=0)
    status = Column(Enum(EventStatus), nullable=False, default=EventStatus.upcoming)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    organizer = relationship("User")


class CMSAchiever(Base):
    __tablename__ = "cms_achievers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    achievement = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class CMSContactSubmission(Base):
    __tablename__ = "cms_contact_submissions"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    subject = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class CMSGalleryAlbum(Base):
    __tablename__ = "cms_gallery_albums"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    cover_image_url = Column(String, nullable=True)
    category = Column(String, nullable=True)
    date = Column(String, nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    photos = relationship("CMSGalleryPhoto", back_populates="album", cascade="all, delete-orphan")


class CMSGalleryPhoto(Base):
    __tablename__ = "cms_gallery_photos"

    id = Column(Integer, primary_key=True, index=True)
    album_id = Column(Integer, ForeignKey("cms_gallery_albums.id"), nullable=False)
    image_url = Column(String, nullable=False)
    thumbnail_url = Column(String, nullable=True)
    caption = Column(String, nullable=True)
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    album = relationship("CMSGalleryAlbum", back_populates="photos")


class CMSPageContent(Base):
    __tablename__ = "cms_pages"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, nullable=False, unique=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())


class StudentStatus(enum.Enum):
    active = "active"
    inactive = "inactive"
    tc = "tc"
    passout = "passout"


class AttendanceStatus(enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    leave = "leave"


class InvoiceStatus(enum.Enum):
    draft = "draft"
    issued = "issued"
    partially_paid = "partially_paid"
    paid = "paid"
    cancelled = "cancelled"


class PaymentMode(enum.Enum):
    cash = "cash"
    bank = "bank"
    upi = "upi"
    card = "card"
    other = "other"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.teacher)
    is_active = Column(Boolean, default=True, nullable=False)

    teacher_subjects = relationship("TeacherSubject", back_populates="teacher")


class TeacherSubject(Base):
    """Many-to-many join table between users (teachers) and subjects."""

    __tablename__ = "teacher_subjects"

    teacher_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), primary_key=True)

    teacher = relationship("User", back_populates="teacher_subjects")
    subject = relationship("Subject", back_populates="teacher_subjects")


class Class(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # e.g. "Class 6"
    display_order = Column(Integer, nullable=False, default=0)

    subjects = relationship("Subject", back_populates="cls")
    sections = relationship("Section", back_populates="cls")
    students = relationship("Student", back_populates="cls")
    attendance_sessions = relationship("AttendanceSession", back_populates="cls")
    fee_structures = relationship("FeeStructure", back_populates="cls")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)

    cls = relationship("Class", back_populates="subjects")
    chapters = relationship("Chapter", back_populates="subject")
    teacher_subjects = relationship("TeacherSubject", back_populates="subject")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    aim = Column(Text, nullable=True)
    pdf_filename = Column(String, nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    order_index = Column(Integer, nullable=False, default=0)
    is_approved = Column(Boolean, nullable=False, default=True)
    pending_change_summary = Column(Text, nullable=True)
    approval_requested_by_id = Column(Integer, nullable=True)
    approved_by_id = Column(Integer, nullable=True)
    approved_at = Column(DateTime(timezone=True), nullable=True)

    subject = relationship("Subject", back_populates="chapters")
    concepts = relationship("Concept", back_populates="chapter", order_by="Concept.display_order")


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    s_no = Column(String, nullable=True)
    title = Column(String, nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    concept_description = Column(Text, nullable=True)
    sessions = Column(String, nullable=True)
    learning_outcomes = Column(Text, nullable=True)
    integration_other_sub = Column(Text, nullable=True)
    teaching_materials_methods = Column(Text, nullable=True)
    library = Column(Text, nullable=True)
    activity = Column(Text, nullable=True)
    life_lesson = Column(Text, nullable=True)
    remarks = Column(Text, nullable=True)
    exhibit_ref = Column(String, nullable=True)

    chapter = relationship("Chapter", back_populates="concepts")
    exhibits = relationship("Exhibit", back_populates="concept")
    images = relationship(
        "ConceptImage",
        back_populates="concept",
        order_by="ConceptImage.sort_order",
        cascade="all, delete-orphan",
    )


class Exhibit(Base):
    __tablename__ = "exhibits"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    field_key = Column(String, nullable=False)
    field_type = Column(Enum(ExhibitFieldType), nullable=False, default=ExhibitFieldType.string)
    field_value = Column(Text, nullable=True)  # for string and link types
    file_key = Column(String, nullable=True)   # for audio/image/video types (stored filename)
    sort_order = Column(Integer, default=0)

    concept = relationship("Concept", back_populates="exhibits")


class ConceptImage(Base):
    __tablename__ = "concept_images"

    id = Column(Integer, primary_key=True, index=True)
    concept_id = Column(Integer, ForeignKey("concepts.id"), nullable=False)
    filename = Column(String, nullable=False)       # stored filename (uuid-based)
    original_name = Column(String, nullable=False)  # original upload name
    sort_order = Column(Integer, default=0)

    concept = relationship("Concept", back_populates="images")


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    students = relationship("Student", back_populates="academic_year")
    attendance_sessions = relationship("AttendanceSession", back_populates="academic_year")
    fee_structures = relationship("FeeStructure", back_populates="academic_year")
    fee_assignments = relationship("StudentFeeAssignment", back_populates="academic_year")
    fee_invoices = relationship("FeeInvoice", back_populates="academic_year")


class Section(Base):
    __tablename__ = "sections"
    __table_args__ = (UniqueConstraint("class_id", "name", name="uq_sections_class_name"),)

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    name = Column(String, nullable=False)

    cls = relationship("Class", back_populates="sections")
    students = relationship("Student", back_populates="section")
    attendance_sessions = relationship("AttendanceSession", back_populates="section")


class Guardian(Base):
    __tablename__ = "guardians"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    relation = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=True)

    student_links = relationship("StudentGuardian", back_populates="guardian")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    admission_no = Column(String, unique=True, nullable=False)
    roll_no = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    status = Column(Enum(StudentStatus), nullable=False, default=StudentStatus.active)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    cls = relationship("Class", back_populates="students")
    section = relationship("Section", back_populates="students")
    academic_year = relationship("AcademicYear", back_populates="students")
    guardians = relationship("StudentGuardian", back_populates="student")
    attendance_entries = relationship("AttendanceEntry", back_populates="student")
    fee_assignments = relationship("StudentFeeAssignment", back_populates="student")
    fee_invoices = relationship("FeeInvoice", back_populates="student")
    fee_receipts = relationship("FeeReceipt", back_populates="student")


class StudentGuardian(Base):
    __tablename__ = "student_guardians"
    __table_args__ = (
        UniqueConstraint("student_id", "guardian_id", name="uq_student_guardian_pair"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    guardian_id = Column(Integer, ForeignKey("guardians.id"), nullable=False)
    is_primary = Column(Boolean, nullable=False, default=False)

    student = relationship("Student", back_populates="guardians")
    guardian = relationship("Guardian", back_populates="student_links")


class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"
    __table_args__ = (
        UniqueConstraint(
            "class_id",
            "section_id",
            "academic_year_id",
            "attendance_date",
            name="uq_attendance_session_slot",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    section_id = Column(Integer, ForeignKey("sections.id"), nullable=True)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    attendance_date = Column(Date, nullable=False)
    marked_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    marked_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    remarks = Column(Text, nullable=True)

    cls = relationship("Class", back_populates="attendance_sessions")
    section = relationship("Section", back_populates="attendance_sessions")
    academic_year = relationship("AcademicYear", back_populates="attendance_sessions")
    entries = relationship("AttendanceEntry", back_populates="session", cascade="all, delete-orphan")


class AttendanceEntry(Base):
    __tablename__ = "attendance_entries"
    __table_args__ = (UniqueConstraint("session_id", "student_id", name="uq_attendance_entry"),)

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("attendance_sessions.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False, default=AttendanceStatus.present)
    remarks = Column(Text, nullable=True)

    session = relationship("AttendanceSession", back_populates="entries")
    student = relationship("Student", back_populates="attendance_entries")


class FeeHead(Base):
    __tablename__ = "fee_heads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    structure_items = relationship("FeeStructureItem", back_populates="fee_head")


class FeeStructure(Base):
    __tablename__ = "fee_structures"
    __table_args__ = (
        UniqueConstraint("name", "class_id", "academic_year_id", name="uq_fee_structure_scope"),
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    cls = relationship("Class", back_populates="fee_structures")
    academic_year = relationship("AcademicYear", back_populates="fee_structures")
    items = relationship("FeeStructureItem", back_populates="fee_structure", cascade="all, delete-orphan")
    assignments = relationship("StudentFeeAssignment", back_populates="fee_structure")


class FeeStructureItem(Base):
    __tablename__ = "fee_structure_items"
    __table_args__ = (
        UniqueConstraint("fee_structure_id", "fee_head_id", name="uq_fee_structure_item"),
    )

    id = Column(Integer, primary_key=True, index=True)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    fee_head_id = Column(Integer, ForeignKey("fee_heads.id"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False, default=0)
    due_day = Column(Integer, nullable=True)

    fee_structure = relationship("FeeStructure", back_populates="items")
    fee_head = relationship("FeeHead", back_populates="structure_items")


class StudentFeeAssignment(Base):
    __tablename__ = "student_fee_assignments"
    __table_args__ = (
        UniqueConstraint("student_id", "fee_structure_id", "academic_year_id", name="uq_student_fee_assignment"),
    )

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    effective_from = Column(Date, nullable=True)
    effective_to = Column(Date, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    student = relationship("Student", back_populates="fee_assignments")
    fee_structure = relationship("FeeStructure", back_populates="assignments")
    academic_year = relationship("AcademicYear", back_populates="fee_assignments")


class FeeInvoice(Base):
    __tablename__ = "fee_invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_no = Column(String, nullable=False, unique=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_years.id"), nullable=False)
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    total_amount = Column(Numeric(12, 2), nullable=False, default=0)
    discount_amount = Column(Numeric(12, 2), nullable=False, default=0)
    paid_amount = Column(Numeric(12, 2), nullable=False, default=0)
    balance_amount = Column(Numeric(12, 2), nullable=False, default=0)
    status = Column(Enum(InvoiceStatus), nullable=False, default=InvoiceStatus.issued)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    student = relationship("Student", back_populates="fee_invoices")
    academic_year = relationship("AcademicYear", back_populates="fee_invoices")
    receipts = relationship("FeeReceipt", back_populates="invoice")


class FeeReceipt(Base):
    __tablename__ = "fee_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_no = Column(String, nullable=False, unique=True)
    invoice_id = Column(Integer, ForeignKey("fee_invoices.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    receipt_date = Column(Date, nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    payment_mode = Column(Enum(PaymentMode), nullable=False, default=PaymentMode.cash)
    reference_no = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    received_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    invoice = relationship("FeeInvoice", back_populates="receipts")
    student = relationship("Student", back_populates="fee_receipts")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    actor_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    action = Column(String, nullable=False)
    change_summary = Column(Text, nullable=True)
    before_payload = Column(Text, nullable=True)
    after_payload = Column(Text, nullable=True)
    ip_address = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
