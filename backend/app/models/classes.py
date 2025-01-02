from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from .base import Base, TimeStampMixin


class Class(Base, TimeStampMixin):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    teacher_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, unique=True)
    date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)
    description = Column(String, nullable=True)

