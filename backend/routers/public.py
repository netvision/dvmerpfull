from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Class, Subject, Chapter, Concept, Exhibit, ConceptImage
from schemas import (
    ClassOut,
    SubjectOut,
    ChapterSummaryOut,
    ChapterDetailOut,
    SubjectNestedOut,
    ClassNestedOut,
    ConceptOut,
    ConceptImageOut,
    ExhibitOut,
)

router = APIRouter()


@router.get("/classes", response_model=List[ClassOut])
def list_classes(db: Session = Depends(get_db)):
    """Return all classes."""
    return db.query(Class).order_by(Class.id).all()


@router.get("/classes/{class_id}/subjects", response_model=List[SubjectOut])
def list_subjects(class_id: int, db: Session = Depends(get_db)):
    """Return all subjects for a class, with chapter_count."""
    cls = db.query(Class).filter(Class.id == class_id).first()
    if cls is None:
        raise HTTPException(status_code=404, detail="Class not found")

    subjects = db.query(Subject).filter(Subject.class_id == class_id).order_by(Subject.id).all()

    result = []
    for subject in subjects:
        chapter_count = (
            db.query(Chapter).filter(Chapter.subject_id == subject.id).count()
        )
        result.append(
            SubjectOut(
                id=subject.id,
                name=subject.name,
                icon=subject.icon,
                color=subject.color,
                chapter_count=chapter_count,
            )
        )
    return result


@router.get("/subjects/{subject_id}/chapters", response_model=List[ChapterSummaryOut])
def list_chapters(subject_id: int, db: Session = Depends(get_db)):
    """Return all chapters for a subject, with sessions_total and concept_count."""
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found")

    chapters = (
        db.query(Chapter)
        .filter(Chapter.subject_id == subject_id)
        .order_by(Chapter.order_index, Chapter.id)
        .all()
    )

    result = []
    for chapter in chapters:
        concept_count = len(chapter.concepts)
        sessions_total = 0
        for concept in chapter.concepts:
            if concept.sessions is not None:
                try:
                    sessions_total += int(concept.sessions)
                except (ValueError, TypeError):
                    pass
        result.append(
            ChapterSummaryOut(
                id=chapter.id,
                title=chapter.title,
                aim=chapter.aim,
                sessions_total=sessions_total,
                concept_count=concept_count,
                pdf_url=f"/uploads/{chapter.pdf_filename}" if chapter.pdf_filename else None,
            )
        )
    return result


@router.get("/chapters/{chapter_id}", response_model=ChapterDetailOut)
def get_chapter(chapter_id: int, db: Session = Depends(get_db)):
    """Return full detail for a chapter."""
    chapter = db.query(Chapter).filter(Chapter.id == chapter_id).first()
    if chapter is None:
        raise HTTPException(status_code=404, detail="Chapter not found")

    subject = chapter.subject
    cls = subject.cls

    concepts_out = []
    for concept in chapter.concepts:
        ordered_exhibits = (
            db.query(Exhibit)
            .filter(Exhibit.concept_id == concept.id)
            .order_by(Exhibit.sort_order)
            .all()
        )
        exhibits_out = [
            ExhibitOut(
                id=ex.id,
                field_key=ex.field_key,
                field_type=getattr(ex.field_type, "value", ex.field_type) or "string",
                field_value=ex.field_value,
                file_key=ex.file_key,
                file_url=f"/uploads/{ex.file_key}" if ex.file_key else None,
                sort_order=ex.sort_order,
            )
            for ex in ordered_exhibits
        ]
        ordered_images = (
            db.query(ConceptImage)
            .filter(ConceptImage.concept_id == concept.id)
            .order_by(ConceptImage.sort_order)
            .all()
        )
        images_out = [
            ConceptImageOut.model_validate({
                "id": img.id,
                "filename": img.filename,
                "original_name": img.original_name,
                "sort_order": img.sort_order,
                "url": f"/uploads/{img.filename}",
            })
            for img in ordered_images
        ]
        concepts_out.append(
            ConceptOut(
                id=concept.id,
                s_no=concept.s_no,
                title=concept.title,
                sessions=concept.sessions,
                learning_outcomes=concept.learning_outcomes,
                integration_other_sub=concept.integration_other_sub,
                library=concept.library,
                activity=concept.activity,
                life_lesson=concept.life_lesson,
                remarks=concept.remarks,
                exhibit_ref=concept.exhibit_ref,
                exhibits=exhibits_out,
                images=images_out,
            )
        )

    return ChapterDetailOut(
        id=chapter.id,
        title=chapter.title,
        aim=chapter.aim,
        pdf_url=f"/uploads/{chapter.pdf_filename}" if chapter.pdf_filename else None,
        subject=SubjectNestedOut(
            id=subject.id,
            name=subject.name,
            icon=subject.icon,
            color=subject.color,
        ),
        **{"class": ClassNestedOut(id=cls.id, name=cls.name)},
        concepts=concepts_out,
    )
