from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TokenOut(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str  # "admin" or "teacher"
    model_config = ConfigDict(from_attributes=True)


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
    field_value: Optional[str]
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
    sessions: Optional[str]
    learning_outcomes: Optional[str]
    integration_other_sub: Optional[str]
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
    model_config = ConfigDict(from_attributes=True)


class SubjectNestedOut(BaseModel):
    id: int
    name: str
    icon: Optional[str]
    color: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ClassNestedOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class ChapterDetailOut(BaseModel):
    id: int
    title: str
    aim: Optional[str]
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
    subject_name: str
    class_name: str


class ChapterUpdateIn(BaseModel):
    title: Optional[str] = None
    aim: Optional[str] = None
    order_index: Optional[int] = None


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
    role: str  # "admin" or "teacher"


class UserUpdateIn(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


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
    sessions: Optional[str] = None
    learning_outcomes: Optional[str] = None
    integration_other_sub: Optional[str] = None
    library: Optional[str] = None
    activity: Optional[str] = None
    life_lesson: Optional[str] = None
    remarks: Optional[str] = None
    exhibit_ref: Optional[str] = None


class ConceptCreateIn(BaseModel):
    chapter_id: int
    s_no: Optional[str] = None
    title: str
    sessions: Optional[str] = None
    learning_outcomes: Optional[str] = None
    integration_other_sub: Optional[str] = None
    library: Optional[str] = None
    activity: Optional[str] = None
    life_lesson: Optional[str] = None
    remarks: Optional[str] = None
    exhibit_ref: Optional[str] = None


class ExhibitUpdateIn(BaseModel):
    field_key: Optional[str] = None
    field_value: Optional[str] = None


class ExhibitCreateIn(BaseModel):
    field_key: str
    field_value: Optional[str] = None
    sort_order: Optional[int] = 0
