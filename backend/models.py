import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Text,
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


class ExhibitFieldType(enum.Enum):
    string = "string"
    audio = "audio"
    image = "image"
    video = "video"
    link = "link"


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

    subjects = relationship("Subject", back_populates="cls")


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
    concepts = relationship("Concept", back_populates="chapter")


class Concept(Base):
    __tablename__ = "concepts"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    s_no = Column(String, nullable=True)
    title = Column(String, nullable=False)
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
