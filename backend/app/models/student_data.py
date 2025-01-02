from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from .base import Base, TimeStampMixin


class StudentBehavior(Base, TimeStampMixin):
    __tablename__ = "student_behaviors"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    class_id = Column(Integer, ForeignKey("classes.id"))
    behavior_type = Column(String)  # attention, distraction等
    timestamp = Column(DateTime)
    details = Column(JSON)


class StudentProgress(Base, TimeStampMixin):
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    chapter_id = Column(Integer, ForeignKey("chapters.id"))
    section_id = Column(Integer, ForeignKey("sections.id"))
    completeness = Column(Float) # 完成度
    duration = Column(Float) # 学习时长
    mistakes = Column(JSON) # 错误
    questions = Column(JSON) # 问题


# class StudentQuestion(Base, TimeStampMixin):
#     __tablename__ = "student_questions"

#     id = Column(Integer, primary_key=True, index=True)
#     student_id = Column(Integer, ForeignKey("users.id"))
#     subject = Column(String)
#     chapter = Column(String)
#     section = Column(String)
#     question_content = Column(String)
#     question_type = Column(String)  # 知识点理解/作业相关/其他
#     timestamp = Column(DateTime)
#     ai_response = Column(String)
#     follow_up_questions = Column(Integer, default=0)  # 追问次数
