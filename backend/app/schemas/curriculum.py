from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class SubjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    teacher_id: int

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(SubjectBase):
    name: Optional[str] = None
    teacher_id: Optional[int] = None

class SubjectResponse(SubjectBase):
    id: int
    teacher_name: str  # 添加教师姓名字段

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    name: str
    description: Optional[str] = None
    subject_id: int
    order: int

class BookResponse(BookBase):
    id: int

    class Config:
        orm_mode = True

class ChapterBase(BaseModel):
    name: str
    description: Optional[str] = None
    book_id: int
    order: int

class ChapterResponse(ChapterBase):
    id: int

    class Config:
        orm_mode = True

class SectionBase(BaseModel):
    name: str
    description: Optional[str] = None
    chapter_id: int
    order: int

class SectionResponse(SectionBase):
    id: int

    class Config:
        orm_mode = True

class ClassBase(BaseModel):
    subject_id: int
    teacher_id: int
    name: str
    date: date
    start_time: time
    end_time: time
    description: Optional[str] = None

class ClassResponse(ClassBase):
    id: int
    teacher_name: str  # 添加教师姓名字段

    class Config:
        orm_mode = True 