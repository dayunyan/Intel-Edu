from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import UserRole, Gender


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    role: str


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str


class UserInDB(UserBase):
    id: int
    role: UserRole

    class Config:
        from_attributes = True

# class StudentInDB(BaseModel):
#     id: int
#     username: str
#     full_name: str
#     gender: Gender
#     age: int
#     grade: int
#     class_id: int
#     description: Optional[str] = None

#     class Config:
#         from_attributes = True

