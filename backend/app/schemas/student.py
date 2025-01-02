from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum
from datetime import datetime

class Gender(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"

class StudentBase(BaseModel):
    username: str
    full_name: str
    email: Optional[EmailStr] = None
    gender: Gender
    age: int
    grade: int
    class_id: int
    class_name: str
    description: Optional[str] = None

class StudentCreate(StudentBase):
    password: str

class StudentUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    grade: Optional[int] = None
    class_id: Optional[int] = None
    class_name: Optional[str] = None
    description: Optional[str] = None
    
class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 