from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field
from models import ExhibitFieldType


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    model_config = ConfigDict(from_attributes=True)


class RoleCapabilitiesOut(BaseModel):
    role: str
    capabilities: List[str]
    is_admin: bool
    is_subject_scoped: bool


class ClassOut(BaseModel):
    id: int
    name: str
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
