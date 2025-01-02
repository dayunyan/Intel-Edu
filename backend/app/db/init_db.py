# backend/app/db/init_db.py
from sqlalchemy.orm import Session
from datetime import datetime, date, time
from app.models.user import User, Student, Teacher, UserRole, Gender
from app.models.curriculum import Subject, Book, Chapter, Section
from app.models.student_data import StudentBehavior, StudentProgress
from app.models.classes import Class
from app.models.analysis import AnalysisResult
from app.core.auth import get_password_hash

# 基础用户数据
USERS = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": get_password_hash("admin123"),
        "role": UserRole.ADMIN,
        "full_name": "系统管理员",
    },
    {
        "username": "teacher1",
        "email": "teacher1@example.com",
        "hashed_password": get_password_hash("teacher123"),
        "role": UserRole.TEACHER,
        "full_name": "张老师",
    },
    {
        "username": "teacher2",
        "email": "teacher2@example.com",
        "hashed_password": get_password_hash("teacher123"),
        "role": UserRole.TEACHER,
        "full_name": "李老师",
    },
    {
        "username": "teacher3",
        "email": "teacher3@example.com",
        "hashed_password": get_password_hash("teacher123"),
        "role": UserRole.TEACHER,
        "full_name": "王老师",
    },
    {
        "username": "student1",
        "email": "student1@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生一",
    },
    {
        "username": "student2",
        "email": "student2@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生二",
    },
    {
        "username": "student3",
        "email": "student3@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生三",
    },
]

# 教师信息
TEACHERS = [
    {
        "username": "teacher1",
        "full_name": "张老师",
        "email": "teacher1@example.com",
        "gender": Gender.MALE,
        "age": 35,
        "education": "硕士",
        "experience": "10年教学经验",
        "description": "数学教师",
    },
    {
        "username": "teacher2",
        "full_name": "李老师",
        "email": "teacher2@example.com",
        "gender": Gender.FEMALE,
        "age": 40,
        "education": "博士",
        "experience": "15年教学经验",
        "description": "语文教师",
    },
    {
        "username": "teacher3",
        "full_name": "王老师",
        "email": "teacher3@example.com",
        "gender": Gender.MALE,
        "age": 32,
        "education": "硕士",
        "experience": "8年教学经验",
        "description": "英语教师",
    },
]

# 学科信息
SUBJECTS = [
    {
        "name": "数学",
        "description": "初中数学课程",
        "teacher_username": "teacher1",
    },
    {
        "name": "语文",
        "description": "初中语文课程",
        "teacher_username": "teacher2",
    },
    {
        "name": "英语",
        "description": "初中英语课程",
        "teacher_username": "teacher3",
    },
]

def init_db(db: Session) -> None:
    # 清空所有表
    for table in reversed([User, Teacher, Subject, Book, Chapter, Section, Class, Student, StudentBehavior, StudentProgress, AnalysisResult]):
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
    for subject in subjects.values():
        class_obj = Class(
            subject_id=subject.id,
            teacher_id=subject.teacher_id,
            name=f"{subject.name}班",
            date=date.today(),
            start_time=time(8, 0),
            end_time=time(9, 40),
            description=f"{subject.name}课程班级"
        )
        db.add(class_obj)
        db.flush()
        classes.append(class_obj)
    
    # 5. 创建学生信息
    students = []
    for username in ["student1", "student2", "student3"]:
        student = Student(
            id=users[username].id,
            username=username,
            full_name=users[username].full_name,
            email=users[username].email,
            gender=Gender.MALE,
            age=15,
            grade=9,
            class_id=classes[0].id,
            description="学生信息"
        )
        db.add(student)
        db.flush()
        students.append(student)
    
    # 6. 创建教材和章节
    for subject in subjects.values():
        # 创建教材
        book = Book(
            subject_id=subject.id,
            name=f"{subject.name}教材",
            description=f"{subject.name}教材描述",
            order=1
        )
        db.add(book)
        db.flush()
        
        # 创建章节
        for i in range(1, 4):
            chapter = Chapter(
                book_id=book.id,
                name=f"第{i}章",
                description=f"{subject.name}第{i}章内容",
                order=i
            )
            db.add(chapter)
            db.flush()
            
            # 创建小节
            for j in range(1, 4):
                section = Section(
                    chapter_id=chapter.id,
                    name=f"第{j}节",
                    description=f"第{i}章第{j}节内容",
                    order=j
                )
                db.add(section)
    
    # 7. 创建学生行为数据
    for student in students:
        for _ in range(3):
            behavior = StudentBehavior(
                student_id=student.id,
                class_id=classes[0].id,
                behavior_type="attention",
                timestamp=datetime.now(),
                details={"location": "classroom", "activity": "listening"}
            )
            db.add(behavior)
    
    # 8. 创建学习进度数据
    for student in students:
        for subject in subjects.values():
            progress = StudentProgress(
                student_id=student.id,
                subject_id=subject.id,
                book_id=1,
                chapter_id=1,
                section_id=1,
                completeness=0.8,
                duration=45.0,
                mistakes=[{"type": "calculation", "description": "计算错误"}],
                questions=[{"id": 1, "correct": True}, {"id": 2, "correct": False}]
            )
            db.add(progress)
    
    # 9. 创建分析结果
    for student in students:
        analysis = AnalysisResult(
            student_id=student.id,
            analysis_timestamp=datetime.now(),
            analysis_report="学习表现良好，需要加强练习",
            evaluation_metrics={
                "attention_rate": 0.85,
                "progress_rate": 0.75,
                "understanding_level": 0.8
            }
        )
        db.add(analysis)
    
    db.commit()
    print("Database initialized successfully")

if __name__ == "__main__":
    from app.db.session import SessionLocal
    db = SessionLocal()
    init_db(db)
