from typing import List, Optional, Generic, TypeVar
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field
from models import ExhibitFieldType

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class DepartmentOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class StaffProfileOut(BaseModel):
    staff_code: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[str] = None
    department_id: Optional[int] = None
    department_name: Optional[str] = None
    designation: Optional[str] = None
    joining_date: Optional[date] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    nationality: Optional[str] = None
    qualification: Optional[str] = None
    bank_name: Optional[str] = None
    account_no: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_no: Optional[str] = None
    aadhaar_no: Optional[str] = None
    pf_no: Optional[str] = None
    esi_no: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    profile: Optional[StaffProfileOut] = None
    model_config = ConfigDict(from_attributes=True)


class RoleCapabilitiesOut(BaseModel):
    role: str
    capabilities: List[str]
    is_admin: bool
    is_subject_scoped: bool


class ClassOut(BaseModel):
    id: int
    name: str
    display_order: int
    model_config = ConfigDict(from_attributes=True)


class SubjectOut(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    chapter_count: int
    model_config = ConfigDict(from_attributes=True)


class ExhibitOut(BaseModel):
    id: int
    field_key: str
    field_type: str  # from ExhibitFieldType enum
    field_value: Optional[str] = None
    file_key: Optional[str] = None
    file_url: Optional[str] = None  # computed: "/uploads/{file_key}"
    sort_order: int = 0
    model_config = ConfigDict(from_attributes=True)


class ConceptImageOut(BaseModel):
    id: int
    filename: str
    original_name: str
    sort_order: int
    url: str  # computed: "/uploads/{filename}"
    model_config = ConfigDict(from_attributes=True)


class ConceptOut(BaseModel):
    id: int
    s_no: Optional[str]
    title: str
    display_order: int
    concept_description: Optional[str]
    sessions: Optional[str]
    learning_outcomes: Optional[str]
    integration_other_sub: Optional[str]
    teaching_materials_methods: Optional[str]
    library: Optional[str]
    activity: Optional[str]
    life_lesson: Optional[str]
    remarks: Optional[str]
    exhibit_ref: Optional[str]
    exhibits: List[ExhibitOut]
    images: List[ConceptImageOut] = []
    model_config = ConfigDict(from_attributes=True)


class ChapterSummaryOut(BaseModel):
    id: int
    title: str
    aim: Optional[str]
    sessions_total: int
    concept_count: int
    pdf_url: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class SubjectNestedOut(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    class_name: Optional[str] = None
    class_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class ClassNestedOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ChapterDetailOut(BaseModel):
    id: int
    title: str
    aim: Optional[str]
    order_index: int
    pdf_url: Optional[str] = None
    subject: SubjectNestedOut
    class_: ClassNestedOut = Field(alias="class")
    concepts: List[ConceptOut]
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ChapterPortalSummaryOut(BaseModel):
    id: int
    title: str
    aim: Optional[str]
    sessions_total: int
    concept_count: int
    is_approved: bool
    pending_change_summary: Optional[str] = None
    subject_id: int
    subject_name: str
    class_id: int
    class_name: str
    pdf_url: Optional[str] = None


class ChapterUpdateIn(BaseModel):
    title: Optional[str] = None
    aim: Optional[str] = None
    order_index: Optional[int] = None
    subject_id: Optional[int] = None


class ChapterCreateIn(BaseModel):
    title: str
    aim: Optional[str] = None
    subject_id: int
    order_index: Optional[int] = None


class UploadResultOut(BaseModel):
    ok: bool
    chapter_title: str
    concepts_count: int
    exhibits_count: int


class UserCreateIn(BaseModel):
    name: str
    email: str
    password: str
    role: str


class UserUpdateIn(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class StaffCreateIn(BaseModel):
    name: str
    email: str
    password: str
    role: str
    staff_code: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    designation: Optional[str] = None
    joining_date: Optional[date] = None
    address: Optional[str] = None


class StaffUpdateIn(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None
    # Profile fields
    staff_code: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    department_id: Optional[int] = None
    designation: Optional[str] = None
    joining_date: Optional[date] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None
    marital_status: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    nationality: Optional[str] = None
    qualification: Optional[str] = None
    bank_name: Optional[str] = None
    account_no: Optional[str] = None
    ifsc_code: Optional[str] = None
    pan_no: Optional[str] = None
    aadhaar_no: Optional[str] = None
    pf_no: Optional[str] = None
    esi_no: Optional[str] = None


class StaffListOut(BaseModel):
    items: List[UserOut]
    total: int


class DepartmentCreateIn(BaseModel):
    name: str
    description: Optional[str] = None


class DepartmentUpdateIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: str


class AdminResetPasswordIn(BaseModel):
    new_password: str


class SubjectAssignIn(BaseModel):
    subject_ids: List[int]


class UserFullOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class ConceptUpdateIn(BaseModel):
    s_no: Optional[str] = None
    title: Optional[str] = None
    display_order: Optional[int] = None
    concept_description: Optional[str] = None
    sessions: Optional[str] = None
    learning_outcomes: Optional[str] = None
    integration_other_sub: Optional[str] = None
    teaching_materials_methods: Optional[str] = None
    library: Optional[str] = None
    activity: Optional[str] = None
    life_lesson: Optional[str] = None
    remarks: Optional[str] = None
    exhibit_ref: Optional[str] = None


class ConceptCreateIn(BaseModel):
    chapter_id: int
    s_no: Optional[str] = None
    title: str
    display_order: Optional[int] = 0
    concept_description: Optional[str] = None
    sessions: Optional[str] = None
    learning_outcomes: Optional[str] = None
    integration_other_sub: Optional[str] = None
    teaching_materials_methods: Optional[str] = None
    library: Optional[str] = None
    activity: Optional[str] = None
    life_lesson: Optional[str] = None
    remarks: Optional[str] = None
    exhibit_ref: Optional[str] = None


class SubjectCreateIn(BaseModel):
    name: str
    class_id: int
    icon: Optional[str] = None
    color: Optional[str] = None


class SubjectUpdateIn(BaseModel):
    name: Optional[str] = None
    class_id: Optional[int] = None
    icon: Optional[str] = None
    color: Optional[str] = None


class SubjectFullOut(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    class_id: int
    class_name: str
    model_config = ConfigDict(from_attributes=True)


class ExhibitUpdateIn(BaseModel):
    field_key: Optional[str] = None
    field_type: Optional[str] = None
    field_value: Optional[str] = None


class ExhibitCreateIn(BaseModel):
    field_key: str
    field_type: str = "string"  # default to string type
    field_value: Optional[str] = None
    sort_order: Optional[int] = 0


class AcademicYearOut(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class AcademicYearCreateIn(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_active: bool = True


class LoginIn(BaseModel):
    email: str
    password: str


class RefreshTokenIn(BaseModel):
    refreshToken: str


class WebsiteAuthUserOut(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    role: str
    is_active: bool


class ContactSubmissionIn(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    subject: str
    message: str


class MarketingCategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    created_at: str
    updated_at: str


class MarketingCategoryCreateIn(BaseModel):
    name: str
    description: Optional[str] = None


class MarketingCategoryUpdateIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class GalleryPhotoOut(BaseModel):
    id: int
    album_id: int
    image_url: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    display_order: int
    model_config = ConfigDict(from_attributes=True)


class GalleryPhotoCreateIn(BaseModel):
    image_url: str
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    display_order: Optional[int] = 0


class GalleryPhotoUpdateIn(BaseModel):
    image_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    caption: Optional[str] = None
    display_order: Optional[int] = None


class GalleryAlbumOut(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None
    photo_count: int
    photos: List[GalleryPhotoOut] = []
    model_config = ConfigDict(from_attributes=True)


class GalleryAlbumCreateIn(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None


class GalleryAlbumUpdateIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    cover_image_url: Optional[str] = None
    category: Optional[str] = None
    date: Optional[str] = None


class PageContentOut(BaseModel):
    id: int
    slug: str
    title: str
    content: str
    is_active: bool
    created_at: str
    updated_at: str
    model_config = ConfigDict(from_attributes=True)


class PageContentCreateIn(BaseModel):
    slug: str
    title: str
    content: str
    is_active: bool = True


class PageContentUpdateIn(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_active: Optional[bool] = None


class NewsArticleCreateIn(BaseModel):
    title: str
    excerpt: Optional[str] = None
    content: str
    featured_image_url: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = "draft"


class NewsArticleUpdateIn(BaseModel):
    title: Optional[str] = None
    excerpt: Optional[str] = None
    content: Optional[str] = None
    featured_image_url: Optional[str] = None
    category_id: Optional[int] = None
    status: Optional[str] = None


class EventCreateIn(BaseModel):
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: date
    end_date: date
    featured_image_url: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = "upcoming"


class EventUpdateIn(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    featured_image_url: Optional[str] = None
    capacity: Optional[int] = None
    status: Optional[str] = None


class SectionOut(BaseModel):
    id: int
    class_id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ClassCreateIn(BaseModel):
    name: str
    display_order: Optional[int] = 0


class ClassUpdateIn(BaseModel):
    name: Optional[str] = None
    display_order: Optional[int] = None


class SectionCreateIn(BaseModel):
    class_id: int
    name: str


class ERPRoleMatrixOut(BaseModel):
    role: str
    capabilities: List[str]


class StudentProfileOut(BaseModel):
    blood_group: Optional[str] = None
    category: Optional[str] = None
    religion: Optional[str] = None
    nationality: Optional[str] = None
    mother_tongue: Optional[str] = None
    previous_school: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    vision: Optional[str] = None
    is_transport: Optional[bool] = None
    pickup_route: Optional[str] = None
    drop_route: Optional[str] = None
    bank_name: Optional[str] = None
    account_no: Optional[str] = None
    ifsc_code: Optional[str] = None
    aadhaar_no: Optional[str] = None
    pen_no: Optional[str] = None
    apaar_id: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class StudentProfileUpdateIn(BaseModel):
    blood_group: Optional[str] = None
    category: Optional[str] = None
    religion: Optional[str] = None
    nationality: Optional[str] = None
    mother_tongue: Optional[str] = None
    previous_school: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    vision: Optional[str] = None
    is_transport: Optional[bool] = None
    pickup_route: Optional[str] = None
    drop_route: Optional[str] = None
    bank_name: Optional[str] = None
    account_no: Optional[str] = None
    ifsc_code: Optional[str] = None
    aadhaar_no: Optional[str] = None
    pen_no: Optional[str] = None
    apaar_id: Optional[str] = None


class GuardianOut(BaseModel):
    id: int
    name: str
    relation: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_primary: bool = False
    model_config = ConfigDict(from_attributes=True)


class GuardianUpsertIn(BaseModel):
    name: str
    relation: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    is_primary: bool = False


class StudentOut(BaseModel):
    id: int
    admission_no: str
    roll_no: Optional[str]
    first_name: str
    last_name: Optional[str]
    date_of_birth: Optional[date]
    gender: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    address: Optional[str]
    class_id: int
    class_name: Optional[str] = None
    section_id: Optional[int]
    section_name: Optional[str] = None
    academic_year_id: int
    academic_year_name: Optional[str] = None
    status: str
    is_active: bool
    profile: Optional[StudentProfileOut] = None
    guardians: Optional[List[GuardianOut]] = None
    model_config = ConfigDict(from_attributes=True)


class StudentListOut(BaseModel):
    items: List[StudentOut]
    total: int


class StudentCreateIn(BaseModel):
    admission_no: str
    roll_no: Optional[str] = None
    first_name: str
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    class_id: int
    section_id: Optional[int] = None
    academic_year_id: int
    status: str = "active"


class StudentUpdateIn(BaseModel):
    admission_no: Optional[str] = None
    roll_no: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None
    class_id: Optional[int] = None
    section_id: Optional[int] = None
    academic_year_id: Optional[int] = None
    status: Optional[str] = None
    is_active: Optional[bool] = None


class AttendanceEntryOut(BaseModel):
    id: int
    session_id: int
    student_id: int
    student_name: Optional[str] = None
    admission_no: Optional[str] = None
    status: str
    remarks: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class AttendanceSessionOut(BaseModel):
    id: int
    class_id: int
    class_name: Optional[str] = None
    section_id: Optional[int] = None
    section_name: Optional[str] = None
    academic_year_id: int
    academic_year_name: Optional[str] = None
    attendance_date: date
    marked_by_id: int
    marked_by_name: Optional[str] = None
    marked_at: Optional[datetime] = None
    remarks: Optional[str] = None
    entries_count: int = 0
    model_config = ConfigDict(from_attributes=True)


class AttendanceSessionCreateIn(BaseModel):
    class_id: int
    section_id: int
    academic_year_id: int
    attendance_date: date
    remarks: Optional[str] = None


class AttendanceEntryCreateIn(BaseModel):
    student_id: int
    status: str
    remarks: Optional[str] = None


class AttendanceEntryUpdateIn(BaseModel):
    status: str
    remarks: Optional[str] = None


class BulkAttendanceMarkIn(BaseModel):
    entries: List[AttendanceEntryCreateIn]


class AttendanceSummaryOut(BaseModel):
    total_entries: int
    present: int
    absent: int
    late: int
    leave: int


class FeeHeadOut(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str] = None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class FeeHeadCreateIn(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    is_active: bool = True


class FeeHeadUpdateIn(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class FeeStructureItemOut(BaseModel):
    id: int
    fee_head_id: int
    fee_head_name: Optional[str] = None
    amount: float
    due_day: Optional[int] = None


class FeeStructureItemCreateIn(BaseModel):
    fee_head_id: int
    amount: float
    due_day: Optional[int] = None


class FeeStructureOut(BaseModel):
    id: int
    name: str
    class_id: int
    class_name: Optional[str] = None
    academic_year_id: int
    academic_year_name: Optional[str] = None
    is_active: bool
    items: List[FeeStructureItemOut] = []
    model_config = ConfigDict(from_attributes=True)


class FeeStructureCreateIn(BaseModel):
    name: str
    class_id: int
    academic_year_id: int
    is_active: bool = True
    items: List[FeeStructureItemCreateIn] = []


class StudentFeeAssignmentOut(BaseModel):
    id: int
    student_id: int
    student_name: Optional[str] = None
    fee_structure_id: int
    fee_structure_name: Optional[str] = None
    academic_year_id: int
    academic_year_name: Optional[str] = None
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class StudentFeeAssignmentCreateIn(BaseModel):
    student_id: int
    fee_structure_id: int
    academic_year_id: int
    effective_from: Optional[date] = None
    effective_to: Optional[date] = None
    is_active: bool = True


class FeeInvoiceOut(BaseModel):
    id: int
    invoice_no: str
    student_id: int
    student_name: Optional[str] = None
    academic_year_id: int
    academic_year_name: Optional[str] = None
    invoice_date: date
    due_date: Optional[date] = None
    total_amount: float
    discount_amount: float
    paid_amount: float
    balance_amount: float
    status: str
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class FeeInvoiceCreateIn(BaseModel):
    invoice_no: str
    student_id: int
    academic_year_id: int
    invoice_date: date
    due_date: Optional[date] = None
    total_amount: float
    discount_amount: float = 0.0
    notes: Optional[str] = None


class FeeReceiptOut(BaseModel):
    id: int
    receipt_no: str
    invoice_id: int
    student_id: int
    student_name: Optional[str] = None
    receipt_date: date
    amount: float
    payment_mode: str
    reference_no: Optional[str] = None
    notes: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class FeeReceiptCreateIn(BaseModel):
    receipt_no: str
    invoice_id: int
    receipt_date: date
    amount: float
    payment_mode: str = "cash"
    reference_no: Optional[str] = None
    notes: Optional[str] = None


class AuditLogOut(BaseModel):
    id: int
    actor_user_id: Optional[int] = None
    entity_type: str
    entity_id: str
    action: str
    change_summary: Optional[str] = None
    before_payload: Optional[str] = None
    after_payload: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: Optional[datetime] = None
    model_config = ConfigDict(from_attributes=True)


class AuditLogListOut(BaseModel):
    items: List[AuditLogOut]
    total: int
