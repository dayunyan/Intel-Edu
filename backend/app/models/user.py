from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from .base import Base, TimeStampMixin
import enum
from sqlalchemy import event
from sqlalchemy.schema import DDL


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"


class Gender(str, enum.Enum):
    MALE = "male"
    FEMALE = "female"


class User(Base, TimeStampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole))
    full_name = Column(String)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        event.listen(
            User.__table__, 
            'before_create',
            self.create_enum_type
        )

    def create_enum_type(self):
        return DDL(
            """
            DO $$ 
            BEGIN 
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'userrole') THEN
                    CREATE TYPE userrole AS ENUM ('ADMIN', 'TEACHER', 'STUDENT');
                END IF;
            END
            $$;
            """
        )

class Teacher(Base, TimeStampMixin):
    __tablename__ = "teachers"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    username = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    gender = Column(Enum(Gender))
    age = Column(Integer)
    education = Column(String)
    experience = Column(String)
    description = Column(String, nullable=True)

class Student(Base, TimeStampMixin):
    __tablename__ = "students"

    id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    username = Column(String)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    gender = Column(Enum(Gender))
    age = Column(Integer)
    grade = Column(Integer)
    class_id = Column(Integer, ForeignKey("classes.id"))
    description = Column(String, nullable=True)

