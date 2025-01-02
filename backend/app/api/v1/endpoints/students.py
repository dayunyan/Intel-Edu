from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.user import User, UserRole, Student, Gender
from app.models.classes import Class
from app.schemas.user import UserInDB
from app.schemas.student import StudentResponse

router = APIRouter()

gender_map = {
    Gender.MALE: "MALE",
    Gender.FEMALE: "FEMALE",
}

@router.get("/", response_model=List[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()
    for student in students:
        class_obj = db.query(Class).filter(Class.id == student.class_id).first()
        student.class_name = class_obj.name if class_obj else "未知"
        student.gender = gender_map[student.gender]
    return students

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    class_obj = db.query(Class).filter(Class.id == student.class_id).first()
    student.class_name = class_obj.name if class_obj else "未知"
    student.gender = gender_map[student.gender]
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student 

