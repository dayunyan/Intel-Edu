# backend/app/db/init_db.py
import random
from sqlalchemy.orm import Session
from datetime import datetime, date, time
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.models.user import User, Student, Teacher, UserRole, Gender
from app.models.curriculum import Subject, Book, Chapter, Section
from app.models.student_data import StudentBehavior, StudentProgress
from app.models.classes import Class
from app.models.analysis import AnalysisResult
from app.models.scale import TestPaper, TestPaperRecord
from app.core.auth import get_password_hash
from app.db.init_const import ANALYSIS_RESULTS, BEHAVIORS, STUDENT_PROGRESS, USERS, TEACHERS, SUBJECTS,CLASSES, STUDENTS, TEST_PAPERS, TEST_PAPER_RECORDS


def init_db(db: Session) -> None:
    # 按照依赖关系的反序删除表数据
    tables_in_order = [
        TestPaperRecord,  # 最底层的依赖表先删除
        TestPaper,
        StudentBehavior,
        StudentProgress,
        AnalysisResult,
        Section,
        Chapter,
        Book,
        Student,
        Class,
        Teacher,
        Subject,
        User,  # 最后删除用户表
    ]
    
    for table in tables_in_order:
        db.query(table).delete()
        db.commit()
    
    # 1. 创建用户
    users = {}
    for user_data in USERS:
        user = User(**user_data)
        db.add(user)
        db.flush()
        users[user.username] = user
    
    # 2. 创建教师信息
    teachers = {}
    for teacher_data in TEACHERS:
        username = teacher_data.pop("username")
        teacher = Teacher(
            id=users[username].id,
            **teacher_data
        )
        db.add(teacher)
        teachers[username] = teacher
    
    # 3. 创建学科
    subjects = {}
    for subject_data in SUBJECTS:
        teacher_username = subject_data.pop("teacher_username")
        subject = Subject(
            teacher_id=users[teacher_username].id,
            **subject_data
        )
        db.add(subject)
        db.flush()
        subjects[subject.name] = subject
        # 更新教师的subject_id
        teachers[teacher_username].subject_id = subject.id
    
    # 4. 创建班级
    classes = []
    for class_data in CLASSES:
        class_obj = Class(
            subject_id=subjects[class_data["subject_name"]].id,
            teacher_id=teachers[class_data["teacher_username"]].id,
            name=f"{class_data['subject_name']}班",
            date=class_data["date"],
            start_time=class_data["start_time"],
            end_time=class_data["end_time"],
            description=f"{class_data['subject_name']}课程班级"
        )
        db.add(class_obj)
        db.flush()
        classes.append(class_obj)
    
    # 5. 创建学生信息
    students = []
    for i,student_data in enumerate(STUDENTS):
        student = Student(
            id=users[student_data["username"]].id,
            username=student_data["username"],
            full_name=student_data["full_name"],
            email=student_data["email"],
            gender=student_data["gender"],
            age=student_data["age"],
            grade=student_data["grade"],
            class_id=classes[i%len(classes)].id,
            description=student_data["description"]
        )
        db.add(student)
        db.flush()
        students.append(student)
    
    # 6. 创建教材和章节
    for subject in subjects.values():
        # 创建教材
        for i in range(1, 4):
            book = Book(
                subject_id=subject.id,
                name=f"{subject.name}教材第{i}册",
                description=f"{subject.name}教材第{i}册描述",
                order=i
            )
            db.add(book)
            db.flush()
        
            # 创建章节
            for j in range(1, 4):
                chapter = Chapter(
                    book_id=book.id,
                    name=f"第{j}章",
                    description=f"{subject.name}教材第{i}册第{j}章内容",
                    order=j
                )
                db.add(chapter)
                db.flush()
                
                # 创建小节
                for k in range(1, 4):
                    section = Section(
                        chapter_id=chapter.id,
                        name=f"第{k}节",
                        description=f"{subject.name}教材第{i}册第{j}章第{k}节内容",
                        order=k
                    )
                    db.add(section)
                    db.flush()
    
    # 7. 创建学生行为数据
    for student in students:
        for _ in range(random.randint(3, 5)):
            behavior = StudentBehavior(
                student_id=student.id,
                class_id=classes[random.randint(0, len(classes)-1)].id,
                behavior_type=random.choice(BEHAVIORS["behavior_type"]),
                timestamp=datetime.now(),
                details={
                    "location": BEHAVIORS["details"]["location"],
                    "time": random.choice(BEHAVIORS["details"]["time"]),
                    "positive-or-negative": random.choice(BEHAVIORS["details"]["positive-or-negative"])
                }
            )
            db.add(behavior)
            db.flush()
    
    # 8. 创建学习进度数据
    for student in students:
        for subject in subjects.values():
            # 获取该书的第一章第一节
            book = db.query(Book).filter(Book.subject_id == subject.id, Book.order == random.randint(1, 3)).first()
            chapter = db.query(Chapter).filter(Chapter.book_id == book.id, Chapter.order == random.randint(1, 3)).first()
            section = db.query(Section).filter(Section.chapter_id == chapter.id, Section.order == random.randint(1, 3)).first()
            progress = StudentProgress(
                student_id=student.id,
                subject_id=subject.id,
                book_id=book.id,
                chapter_id=chapter.id,
                section_id=section.id,
                completeness=random.uniform(0.5, 1.0),
                duration=random.uniform(10.0, 60.0),
                mistakes=[
                    {
                        "timestamp": mistake["timestamp"],
                        "test_question": random.choice(mistake["test_question"]),
                        "correct_answer": random.choice(mistake["correct_answer"]),
                        "mistake_answer": random.choice(mistake["mistake_answer"]),
                        "details": {
                            "type": random.choice(mistake["details"]["type"]),
                            "description": random.choice(mistake["details"]["description"])
                        }
                    } for mistake in STUDENT_PROGRESS["mistake"]
                ],
                questions=[
                    {
                        "timestamp": question["timestamp"],
                        "student_question": random.choice(question["student_question"]),
                        "ai_response": random.choice(question["ai_response"]),
                        "history": [
                        {
                            "timestamp": history["timestamp"],
                            "student_question": random.choice(history["student_question"]),
                            "ai_response": random.choice(history["ai_response"])
                            } for history in question["history"]
                        ],
                        "details": {
                            "summary": question["details"]["summary"]
                        }
                    } for question in STUDENT_PROGRESS["question"]
                ]
            )
            db.add(progress)
            db.flush()
    

    
    # 9. 创建测试试卷
    test_papers = []
    for test_paper_data in TEST_PAPERS:
        test_paper = TestPaper(
            **test_paper_data
        )
        db.add(test_paper)
        db.flush()
        test_papers.append(test_paper)

    # 10. 创建测试记录
    for test_paper_record_data in TEST_PAPER_RECORDS:
        test_paper_record_data["student_id"] = students[test_paper_record_data["student_id"]].id
        test_paper_record_data["test_paper_id"] = test_papers[test_paper_record_data["test_paper_id"]].id
        test_paper_record = TestPaperRecord(
            **test_paper_record_data
        )
        db.add(test_paper_record)
        db.flush()

    # 11. 创建分析结果
    for student in students:
        for analysis_timestamp in ANALYSIS_RESULTS["analysis_timestamp"]:
            analysis = AnalysisResult(
                student_id=student.id,
                analysis_type=ANALYSIS_RESULTS["analysis_type"],
                analysis_timestamp=analysis_timestamp,
                analysis_report=ANALYSIS_RESULTS["analysis_report"],
                evaluation_metrics=ANALYSIS_RESULTS["evaluation_metrics"]
            )
            db.add(analysis)

    db.commit()
    print("Database initialized successfully")

if __name__ == "__main__":
    from app.db.session import SessionLocal
    db = SessionLocal()
    init_db(db)
