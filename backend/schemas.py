from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


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
