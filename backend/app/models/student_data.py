from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON, DateTime
from .base import Base, TimeStampMixin

""" Template for details in StudentBehavior
#TODO: 需要根据实际情况修改
{
    "behavior_type": "reading" | "writing" | "hand-raising" | "using phone" | "sleeping" | "speaking",
    "timestamp": "2024-10-08 10:00:00",
    "details": {
        "location": "classroom",
        "time": "in-class" | "after-class"
        "positive-or-negative": "positive" | "negative"
    }
}
"""

""" JSON template for mistakes in StudentProgress
#TODO: 需要根据实际情况修改
[
    {
        "timestamp": "2024-10-08 10:00:00",
        "test_question": "1+1=?",
        "correct_answer": "2",
        "mistake_answer": "3",
        "details": {
            "type": "calculation" | "understanding" | "memory" | "application" | "analysis" | "evaluation",
            "description": "计算错误" | "理解错误" | "记忆错误" | "应用错误" | "分析错误" | "评价错误"
        }
    }
]
"""

""" JSON template for questions in StudentProgress
#TODO: 需要根据实际情况修改
[
    {
        "timestamp": "2024-10-08 10:00:00",
        "student_question": "1+1=?",
        "ai_response": "2",
        "history":[
            {
                "timestamp": "2024-10-08 10:00:00",
                "student_question": "1+1=?",
                "ai_response": "2"
            }
        ]
        "details": {
            "summary": "Firstly, the student asked the question, then the AI answered the question, and finally the student asked the question again."
        }
    }
]
"""


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
