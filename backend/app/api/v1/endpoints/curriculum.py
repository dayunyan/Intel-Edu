from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.curriculum import Subject, Book, Chapter, Section
from app.models.classes import Class
from app.schemas.curriculum import (
    SubjectCreate, SubjectUpdate, SubjectResponse,
    BookResponse, ChapterResponse, SectionResponse,
    ClassResponse
)
from app.models.user import User

router = APIRouter()

@router.get("/subjects", response_model=List[SubjectResponse])
def get_subjects(db: Session = Depends(get_db)):
    subjects = db.query(Subject).all()
    for subject in subjects:
        teacher = db.query(User).filter(User.id == subject.teacher_id).first()
        subject.teacher_name = teacher.full_name if teacher else "未知"
    return subjects

@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.get("/subjects/{subject_id}/books", response_model=List[BookResponse])
def get_books(subject_id: int, db: Session = Depends(get_db)):
    return db.query(Book).filter(Book.subject_id == subject_id).all()

@router.get("/books/{book_id}/chapters", response_model=List[ChapterResponse])
def get_chapters(book_id: int, db: Session = Depends(get_db)):
    return db.query(Chapter).filter(Chapter.book_id == book_id).all()

@router.get("/chapters/{chapter_id}/sections", response_model=List[SectionResponse])
def get_sections(chapter_id: int, db: Session = Depends(get_db)):
    return db.query(Section).filter(Section.chapter_id == chapter_id).all()

@router.get("/schedule", response_model=List[ClassResponse])
def get_schedule(db: Session = Depends(get_db)):
    classes = db.query(Class).all()
    for class_obj in classes:
        teacher = db.query(User).filter(User.id == class_obj.teacher_id).first()
        class_obj.teacher_name = teacher.full_name if teacher else "未知"
    return classes

@router.post("/subjects", response_model=SubjectResponse)
def create_subject(subject: SubjectCreate, db: Session = Depends(get_db)):
    db_subject = Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.put("/subjects/{subject_id}", response_model=SubjectResponse)
def update_subject(subject_id: int, subject: SubjectUpdate, db: Session = Depends(get_db)):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    for field, value in subject.dict(exclude_unset=True).items():
        setattr(db_subject, field, value)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db.delete(db_subject)
    db.commit()
    return {"message": "Subject deleted successfully"}