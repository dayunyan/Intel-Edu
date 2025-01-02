from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base, TimeStampMixin


class Subject(Base, TimeStampMixin):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, unique=True)
    description = Column(String, nullable=True)

class Book(Base, TimeStampMixin):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    name = Column(String, unique=True)
    description = Column(String, nullable=True)
    order = Column(Integer)

class Chapter(Base, TimeStampMixin):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    name = Column(String)
    description = Column(String, nullable=True)
    order = Column(Integer)


class Section(Base, TimeStampMixin):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    name = Column(String)
    description = Column(String, nullable=True)
    order = Column(Integer)
