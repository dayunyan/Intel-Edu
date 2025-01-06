from datetime import datetime, date, time, timedelta
import random
from app.models.user import UserRole, Gender
from app.core.auth import get_password_hash

def serialize_date(obj):
    """序列化日期对象为字符串"""
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, time):
        return obj.strftime('%H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    return obj

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
        "username": "teacher4",
        "email": "teacher4@example.com",
        "hashed_password": get_password_hash("teacher123"),
        "role": UserRole.TEACHER,
        "full_name": "赵老师",
    },
    {
        "username": "teacher5",
        "email": "teacher5@example.com",
        "hashed_password": get_password_hash("teacher123"),
        "role": UserRole.TEACHER,
        "full_name": "孙老师",
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
    {
        "username": "student4",
        "email": "student4@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生四",
    },
    {
        "username": "student5",
        "email": "student5@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生五",
    },
    {
        "username": "student6",
        "email": "student6@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生六",
    },
    {
        "username": "student7",
        "email": "student7@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生七",
    },
    {
        "username": "student8",
        "email": "student8@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生八",
    },
    {
        "username": "student9",
        "email": "student9@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生九",
    },
    {
        "username": "student10",
        "email": "student10@example.com",
        "hashed_password": get_password_hash("student123"),
        "role": UserRole.STUDENT,
        "full_name": "学生十",
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
    {
        "username": "teacher4",
        "full_name": "赵老师",
        "email": "teacher4@example.com",
        "gender": Gender.FEMALE,
        "age": 38,
        "education": "博士",
        "experience": "12年教学经验",
        "description": "物理教师",
    },
    {
        "username": "teacher5",
        "full_name": "孙老师",
        "email": "teacher5@example.com",
        "gender": Gender.MALE,
        "age": 30,
        "education": "硕士",
        "experience": "7年教学经验",
        "description": "历史教师",
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
    {
        "name": "物理",
        "description": "初中物理课程",
        "teacher_username": "teacher4",
    },
    {
        "name": "历史",
        "description": "初中历史课程",
        "teacher_username": "teacher5",
    },
]

# 班级信息
CLASSES = [
    {
        "name": "数学班",
        "description": "数学课程班级",
        "date": date(2025, 1, 1),
        "start_time": time(8, 0, 0),
        "end_time": time(9, 40, 0),
        "subject_name": "数学",
        "teacher_username": "teacher1",
    },
    {
        "name": "语文班",
        "description": "语文课程班级",
        "date": date(2025, 1, 2),
        "start_time": time(10, 0, 0),
        "end_time": time(11, 40, 0),
        "subject_name": "语文",
        "teacher_username": "teacher2",
    },
    {
        "name": "英语班",
        "description": "英语课程班级",
        "date": date(2025, 1, 3),
        "start_time": time(10, 0, 0),
        "end_time": time(11, 40, 0),
        "subject_name": "英语",
        "teacher_username": "teacher3",
    },
    {
        "name": "物理班",
        "description": "物理课程班级",
        "date": date(2024, 12, 31),
        "start_time": time(14, 0, 0),
        "end_time": time(15, 40, 0),
        "subject_name": "物理",
        "teacher_username": "teacher4",
    },
    {
        "name": "历史班",
        "description": "历史课程班级",
        "date": date(2024, 12, 31),
        "start_time": time(16, 0, 0),
        "end_time": time(17, 40, 0),
        "subject_name": "历史",
        "teacher_username": "teacher5",
    },
]

# 学生信息
STUDENTS = [
    {
        "username": "student1",
        "full_name": "学生一",
        "email": "student1@example.com",
        "gender": Gender.MALE,
        "age": 11,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student2",
        "full_name": "学生二",
        "email": "student2@example.com",
        "gender": Gender.FEMALE,
        "age": 12,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student3",
        "full_name": "学生三",
        "email": "student3@example.com",
        "gender": Gender.MALE,
        "age": 13,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student4",
        "full_name": "学生四",
        "email": "student4@example.com",
        "gender": Gender.FEMALE,
        "age": 12,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student5",
        "full_name": "学生五",
        "email": "student5@example.com",
        "gender": Gender.MALE,
        "age": 12,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student6",
        "full_name": "学生六",
        "email": "student6@example.com",
        "gender": Gender.FEMALE,
        "age": 13,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student7",
        "full_name": "学生七",
        "email": "student7@example.com",
        "gender": Gender.MALE,
        "age": 13,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student8",
        "full_name": "学生八",
        "email": "student8@example.com",
        "gender": Gender.FEMALE,
        "age": 13,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student9",
        "full_name": "学生九",
        "email": "student9@example.com",
        "gender": Gender.MALE,
        "age": 13,
        "grade": 7,
        "description": "学生信息",
    },
    {
        "username": "student10",
        "full_name": "学生十",
        "email": "student10@example.com",
        "gender": Gender.FEMALE,
        "age": 13,
        "grade": 7,
        "description": "学生信息",
    },
]

# 学生行为
BEHAVIORS = {
    "behavior_type": ["reading", "writing", "hand-raising", "using phone", "sleeping", "speaking"],
    "timestamp": "2024-10-08 10:00:00",
    "details": {
        "location": "classroom",
        "time": ["in-class", "after-class"],
        "positive-or-negative": ["positive", "negative"]
    }
}

# 学生进度
STUDENT_PROGRESS = {
    "mistake":[
        {
        "timestamp": serialize_date(datetime.now()),
        "test_question": ["1+1=?", "2+2=?", "3+3=?"],
        "correct_answer": ["2", "4", "6"],
        "mistake_answer": ["3", "5", "7"],
        "details": {
            "type": ["calculation", "understanding", "memory", "application", "analysis", "evaluation"],
            "description": ["计算错误", "理解错误", "记忆错误", "应用错误", "分析错误", "评价错误"]
            }
        }
    ],
    "question":[
        {
            "timestamp": serialize_date(datetime.now()),
            "student_question": ["1+1=?", "2+2=?", "3+3=?"],
            "ai_response": ["2", "4", "6"],
            "history":[
                {
                    "timestamp": serialize_date(datetime.now()),
                    "student_question": ["1+1=?", "2+2=?", "3+3=?"],
                    "ai_response": ["2", "4", "6"]
                }
            ],
            "details": {
                "summary": "Firstly, the student asked the question, then the AI answered the question, and finally the student asked the question again."
            }
        }
    ]
}

# 试卷
TEST_PAPERS = [
    {
        "description": "2024-2025学年第一学期北京市第一中学第一次模拟考试·历史",
        "content": [
            {
                "information": {
                    "title": "2024-2025学年第一学期北京市第一中学第一次模拟考试",
                    "subject": "历史",
                    "grade": 7,
                    "date": serialize_date(date(2024, 10, 8)),
                    "duration": 120,
                    "total_score": 100,
                }
            },
            {
                "content": [
                    {
                        "type": "一、选择题",
                        "content": [
                            {
                                "question": "1. 中国历史上第一个统一的封建王朝是哪个？",
                                "options": ["秦朝", "汉朝", "唐朝", "宋朝"],
                                "correct_answer": "秦朝",
                                "score": 2,
                            },
                            {
                                "question": "2. 甲午战争爆发于哪一年？",
                                "options": ["1894年", "1895年", "1896年", "1897年"],
                                "correct_answer": "1894年",
                                "score": 2,
                            },
                            {
                                "question": "3. 鸦片战争爆发于哪一年？",
                                "options": ["1840年", "1841年", "1842年", "1843年"],
                                "correct_answer": "1840年",
                                "score": 2,
                            },
                            {
                                "question": "4. 辛亥革命爆发于哪一年？",
                                "options": ["1911年", "1912年", "1913年", "1914年"],
                                "correct_answer": "1911年",
                                "score": 2,
                            },
                            {
                                "question": "5. 第一次工业革命的特点是什么？",
                                "options": ["蒸汽机", "电力", "计算机", "互联网"],
                                "correct_answer": "蒸汽机",
                                "score": 2,
                            },
                            {
                                "question": "6. 第二次世界大战的爆发原因是什么？",
                                "options": ["德国的侵略", "日本的侵略", "苏联的侵略", "美国的侵略"],
                                "correct_answer": "德国的侵略",
                                "score": 2,
                            },
                            {
                                "question": "7. 五四运动标志着什么？",
                                "options": ["新文化运动的开始", "中国共产党的成立", "中国共产党的成立", "中国共产党的成立"],
                                "correct_answer": "新文化运动的开始",
                                "score": 2,
                            },
                            {
                                "question": "8. 中国共产党的成立时间是什么？",
                                "options": ["1921年", "1922年", "1923年", "1924年"],
                                "correct_answer": "1921年",
                                "score": 2,
                            },
                            {
                                "question": "9. 北宋时期，王安石变法的主要内容是什么？",
                                "options": ["均田制", "科举制", "土地改革", "均田制"],
                                "correct_answer": "均田制",
                                "score": 2,
                            },
                            {
                                "question": "10. 明朝时期，郑和下西洋的主要目的是什么？",
                                "options": ["贸易", "文化交流", "军事征服", "宗教传播"],
                                "correct_answer": "贸易",
                                "score": 2,
                            },
                        ]
                    },
                    {
                        "type": "二、填空题",
                        "content": [
                            {
                                "question": "1. 四大文明古国分别是",
                                "correct_answer": "中国、印度、埃及、巴比伦",
                                "score": 5,
                            },
                            {
                                "question": "2. 中国历史上第一个统一的封建王朝是",
                                "correct_answer": "秦朝",
                                "score": 5,
                            },
                            {
                                "question": "3. 中国共产党在哪里成立的？",
                                "correct_answer": "上海",
                                "score": 5,
                            },
                            {
                                "question": "4. 中国共产党第一次全国代表大会的召开时间是什么？",
                                "correct_answer": "1921年7月",
                                "score": 5,
                            },
                            {
                                "question": "5. 第一次北伐战争的目的是",
                                "correct_answer": "推翻北洋军阀的统治，统一中国",
                                "score": 5,
                            },
                            {
                                "question": "6. 抗日战争持续了  年。",
                                "correct_answer": "14",
                                "score": 5,
                            },
                        ]
                    },
                    {
                        "type": "三、简答题",
                        "content": [
                            {
                                "question": "1. 请简述中国共产党的成立过程。",
                                "correct_answer": "中国共产党的成立过程是：1921年7月，中国共产党第一次全国代表大会在上海举行，标志着中国共产党的正式成立。",
                                "score": 10,
                            },
                            {
                                "question": "2. 请简述第二次工业革命的过程和意义。",
                                "correct_answer": "第二次工业革命的过程是：1870年左右，英国开始进行第二次工业革命，主要内容包括电力的广泛应用、内燃机的发明和使用、化学工业的发展等。第二次工业革命的意义是：推动了生产力的发展，促进了社会经济的进步，改变了人们的生活方式，为现代工业社会的形成奠定了基础。",
                                "score": 10,
                            },
                            {
                                "question": "3. 请简述文艺复兴的背景和意义。",
                                "correct_answer": "文艺复兴的背景是：14世纪末，欧洲开始出现文艺复兴运动，主要原因是：1. 宗教改革的影响：宗教改革使得人们开始重新审视宗教信仰，对传统宗教信仰产生了怀疑和挑战。2. 人文主义的影响：人文主义强调人的价值和尊严，反对宗教神权，主张人的自由和个性发展。3. 科学的发展：科学的发展使得人们开始重新审视自然和人类社会，对传统宗教信仰产生了怀疑和挑战。文艺复兴的意义是：推动了生产力的发展，促进了社会经济的进步，改变了人们的生活方式，为现代工业社会的形成奠定了基础。",
                                "score": 10,
                            },
                            {
                                "question": "4. 请简述第一次大战的背景和意义。",
                                "correct_answer": "第一次大战的背景是：1914年，第一次世界大战爆发，主要原因是：1. 德国的侵略：德国为了争夺世界霸权，发动了第一次世界大战。2. 英国的侵略：英国为了维护自己的殖民地，发动了第一次世界大战。3. 法国的侵略：法国为了维护自己的殖民地，发动了第一次世界大战。第一次大战的意义是：推动了生产力的发展，促进了社会经济的进步，改变了人们的生活方式，为现代工业社会的形成奠定了基础。",
                                "score": 10,
                            },
                            {
                                "question": "5. 请简述解放战争的几大战役的时间、地点、结果以及特点。",
                                "correct_answer": "解放战争的几大战役的时间、地点、结果以及特点是：1. 辽沈战役：1948年9月，东北野战军在辽沈战役中取得了胜利，歼灭了国民党军47万余人，解放了东北全境。2. 淮海战役：1948年11月，华东野战军在淮海战役中取得了胜利，歼灭了国民党军55万余人，解放了华东全境。3. 平津战役：1948年12月，东北野战军和平津战役中取得了胜利，歼灭了国民党军52万余人，解放了华北全境。4. 渡江战役：1949年4月，华东野战军在渡江战役中取得了胜利，歼灭了国民党军43万余人，解放了华东全境。5. 解放战争的特点是：中国共产党领导的解放战争，是中国历史上的一次伟大的革命战争，是中国共产党领导的人民军队，经过艰苦卓绝的斗争，最终取得了胜利。",
                                "score": 10,
                            },
                        ]
                    }
                ]
            }
        ]
    },
]

TEST_PAPER_RECORDS = [
    {
        "student_id": 0,
        "test_paper_id": 0,
        "score": 57,
        "content": {
        "description": "2024-2025学年第一学期北京市第一中学第一次模拟考试·历史",
        "content": [
            {
                "information": {
                    "title": "2024-2025学年第一学期北京市第一中学第一次模拟考试",
                    "subject": "历史",
                    "grade": 7,
                    "date": serialize_date(date(2024, 10, 8)),
                    "duration": 120,
                    "total_score": 100,
                }
            },
            {
                "content": [
                    {
                        "type": "一、选择题",
                        "content": [
                            {
                                "question": "1. 中国历史上第一个统一的封建王朝是哪个？",
                                "options": ["秦朝", "汉朝", "唐朝", "宋朝"],
                                "correct_answer": "秦朝",
                                "score": 2,
                                "answer": "秦朝",
                                "get_score": 2,
                            },
                            {
                                "question": "2. 甲午战争爆发于哪一年？",
                                "options": ["1894年", "1895年", "1896年", "1897年"],
                                "correct_answer": "1894年",
                                "score": 2,
                                "answer": "1895年",
                                "get_score": 0,
                            },
                            {
                                "question": "3. 鸦片战争爆发于哪一年？",
                                "options": ["1840年", "1841年", "1842年", "1843年"],
                                "correct_answer": "1840年",
                                "score": 2,
                                "answer": "1840年",
                                "get_score": 2,
                            },
                            {
                                "question": "4. 辛亥革命爆发于哪一年？",
                                "options": ["1911年", "1912年", "1913年", "1914年"],
                                "correct_answer": "1911年",
                                "score": 2,
                                "answer": "1911年",
                                "get_score": 2,
                            },
                            {
                                "question": "5. 第一次工业革命的特点是什么？",
                                "options": ["蒸汽机", "电力", "计算机", "互联网"],
                                "correct_answer": "蒸汽机",
                                "score": 2,
                                "answer": "蒸汽机",
                                "get_score": 2,
                            },
                            {
                                "question": "6. 第二次世界大战的爆发原因是什么？",
                                "options": ["德国的侵略", "日本的侵略", "苏联的侵略", "美国的侵略"],
                                "correct_answer": "德国的侵略",
                                "score": 2,
                                "answer": "德国的侵略",
                                "get_score": 2,
                            },
                            {
                                "question": "7. 五四运动标志着什么？",
                                "options": ["新文化运动的开始", "中国共产党的成立", "中国摆脱了半殖民地半封建社会", "抗日战争开始"],
                                "correct_answer": "新文化运动的开始",
                                "score": 2,
                                "answer": "中国摆脱了半殖民地半封建社会",
                                "get_score": 0,
                            },
                            {
                                "question": "8. 中国共产党的成立时间是什么？",
                                "options": ["1921年", "1922年", "1923年", "1924年"],
                                "correct_answer": "1921年",
                                "score": 2,
                                "answer": "1921年",
                                "get_score": 2,
                            },
                            {
                                "question": "9. 北宋时期，王安石变法的主要内容是什么？",
                                "options": ["均田制", "科举制", "土地改革", "摊丁入亩"],
                                "correct_answer": "均田制",
                                "score": 2,
                                "answer": "摊丁入亩",
                                "get_score": 0,
                            },
                            {
                                "question": "10. 明朝时期，郑和下西洋的主要目的是什么？",
                                "options": ["贸易", "文化交流", "军事征服", "宗教传播"],
                                "correct_answer": "贸易",
                                "score": 2,
                                "answer": "文化交流",
                                "get_score": 0,
                            },
                        ]
                    },
                    {
                        "type": "二、填空题",
                        "content": [
                            {
                                "question": "1. 四大文明古国分别是",
                                "correct_answer": "中国、印度、埃及、巴比伦",
                                "score": 5,
                                "answer": "中国、印度、埃及、古巴",
                                "get_score": 0,
                            },
                            {
                                "question": "2. 中国历史上第一个统一的封建王朝是",
                                "correct_answer": "秦朝",
                                "score": 5,
                                "answer": "秦朝",
                                "get_score": 5,
                            },
                            {
                                "question": "3. 中国共产党在哪里成立的？",
                                "correct_answer": "上海",
                                "score": 5,
                                "answer": "苏州",
                                "get_score": 0,
                            },
                            {
                                "question": "4. 中国共产党第一次全国代表大会的召开时间是什么？",
                                "correct_answer": "1921年7月",
                                "score": 5,
                                "answer": "1921年7月",
                                "get_score": 5,
                            },
                            {
                                "question": "5. 第一次北伐战争的目的是",
                                "correct_answer": "推翻北洋军阀的统治，统一中国",
                                "score": 5,
                                "answer": "推翻北洋军阀的统治，统一中国",
                                "get_score": 5,
                            },
                            {
                                "question": "6. 抗日战争持续了  年。",
                                "correct_answer": "14",
                                "score": 5,
                                "answer": "8",
                                "get_score": 0,
                            },
                        ]
                    },
                    {
                        "type": "三、简答题",
                        "content": [
                            {
                                "question": "1. 请简述中国共产党的成立过程。",
                                "correct_answer": "中国共产党的成立过程是：1921年7月，中国共产党第一次全国代表大会在上海举行，标志着中国共产党的正式成立。",
                                "score": 10,
                                "answer": "中国共产党的成立过程是：1921年7月，中国共产党第一次全国代表大会在上海举行，标志着中国共产党的正式成立。",
                                "get_score": 10,
                            },
                            {
                                "question": "2. 请简述第二次工业革命的过程和意义。",
                                "correct_answer": "第二次工业革命的过程是：1870年左右，英国开始进行第二次工业革命，主要内容包括电力的广泛应用、内燃机的发明和使用、化学工业的发展等。第二次工业革命的意义是：推动了生产力的发展，促进了社会经济的进步，改变了人们的生活方式，为现代工业社会的形成奠定了基础。",
                                "score": 10,
                                "answer": "第二次工业革命的过程是：1912年，德国开始第二次工业革命，对国内的经济、政治进行了深刻的改革，将德国原本破败不堪的战后经济，发展成为欧洲第一经济体。",
                                "get_score": 0,
                            },
                            {
                                "question": "3. 请简述文艺复兴的背景和意义。",
                                "correct_answer": "文艺复兴的背景是：14世纪末，欧洲开始出现文艺复兴运动，主要原因是：1. 宗教改革的影响：宗教改革使得人们开始重新审视宗教信仰，对传统宗教信仰产生了怀疑和挑战。2. 人文主义的影响：人文主义强调人的价值和尊严，反对宗教神权，主张人的自由和个性发展。3. 科学的发展：科学的发展使得人们开始重新审视自然和人类社会，对传统宗教信仰产生了怀疑和挑战。文艺复兴的意义是：推动了生产力的发展，促进了社会经济的进步，改变了人们的生活方式，为现代工业社会的形成奠定了基础。",
                                "score": 10,
                                "answer": "文艺复兴的背景是：14世纪末，欧洲开始出现文艺复兴运动，主要原因是：1. 宗教改革的影响：宗教改革使得人们开始重新审视宗教信仰，对传统宗教信仰产生了怀疑和挑战。2. 人文主义的影响：人文主义强调人的价值和尊严，反对宗教神权，主张人的自由和个性发展。3. 科学的发展：科学的发展使得人们开始重新审视自然和人类社会，对传统宗教信仰产生了怀疑和挑战。文艺复兴的意义是：推动了生产力的发展，促进了社会经济的进步，改变了人们的生活方式，为现代工业社会的形成奠定了基础。",
                                "get_score": 10,
                            },
                            {
                                "question": "4. 请简述第一次大战的背景和意义。",
                                "correct_answer": "第一次大战的背景是：1914年，第一次世界大战爆发，主要原因是：1. 德国的侵略：德国为了争夺世界霸权，发动了第一次世界大战。2. 英国的侵略：英国为了维护自己的殖民地，发动了第一次世界大战。3. 法国的侵略：法国为了维护自己的殖民地，发动了第一次世界大战。第一次大战的意义是：推动了生产力的发展，促进了社会经济的进步，改变了人们的生活方式，为现代工业社会的形成奠定了基础。",
                                "score": 10,
                                "answer": "第一次大战的背景是：1866年，英国依靠强大的海军力量，击败了法国，成为了世界霸主。",
                                "get_score": 0,
                            },
                            {
                                "question": "5. 请简述解放战争的几大战役的时间、地点、结果以及特点。",
                                "correct_answer": "解放战争的几大战役的时间、地点、结果以及特点是：1. 辽沈战役：1948年9月，东北野战军在辽沈战役中取得了胜利，歼灭了国民党军47万余人，解放了东北全境。2. 淮海战役：1948年11月，华东野战军在淮海战役中取得了胜利，歼灭了国民党军55万余人，解放了华东全境。3. 平津战役：1948年12月，东北野战军和平津战役中取得了胜利，歼灭了国民党军52万余人，解放了华北全境。4. 渡江战役：1949年4月，华东野战军在渡江战役中取得了胜利，歼灭了国民党军43万余人，解放了华东全境。5. 解放战争的特点是：中国共产党领导的解放战争，是中国历史上的一次伟大的革命战争，是中国共产党领导的人民军队，经过艰苦卓绝的斗争，最终取得了胜利。",
                                "score": 10,
                                "answer": "解放战争的几大战役的时间、地点、结果以及特点是：1. 辽沈战役：1948年9月，东北野战军在辽沈战役中取得了胜利，歼灭了国民党军47万余人，解放了东北全境。2. 淮海战役：1948年11月，华东野战军在淮海战役中取得了胜利，歼灭了国民党军55万余人，解放了华东全境。3. 平津战役：1948年12月，东北野战军和平津战役中取得了胜利，歼灭了国民党军52万余人，解放了华北全境。4. 渡江战役：1949年4月，华东野战军在渡江战役中取得了胜利，歼灭了国民党军43万余人，解放了华东全境。5. 解放战争的特点是：中国共产党领导的解放战争，是中国历史上的一次伟大的革命战争，是中国共产党领导的人民军队，经过艰苦卓绝的斗争，最终取得了胜利。",
                                "get_score": 10,
                            },
                        ]
                    }
                ]
            }
        ]
    },
    }
]

# 分析结果
ANALYSIS_RESULTS = {
    "analysis_type": "7days",
    "analysis_timestamp": [datetime.now() - timedelta(days=i) for i in range(90, 0, -7)],
    "analysis_report": "学习表现良好，需要加强练习",
    "evaluation_metrics": {
        # 自我管理
        "attention_rate": random.uniform(0.5, 0.9),
        "emotion_management_level": random.uniform(0.5, 0.9),
        "independent_learning_level": random.uniform(0.5, 0.9),
        "self_reflection_level": random.uniform(0.5, 0.9),
        "self_control_summary": "The student has a good self-control ability, and can control his emotions well.",
        # 知识掌握
        "progress_rate": random.uniform(0.5, 0.9),
        "knowledge_master_level": random.uniform(0.5, 0.9),
        "knowledge_weak_points": ["知识点1", "知识点2", "知识点3"],
        "knowledge_improvement_suggestions": ["建议1", "建议2", "建议3"],
        "knowledge_summary": "The student has a good knowledge of the subject, and can master the basic knowledge well.",
        # 问题解决与创新
        "identify_problem_level": random.uniform(0.5, 0.9),
        "problem_solving_level": random.uniform(0.5, 0.9),
        "innovation_level": random.uniform(0.5, 0.9),
        "problem_solving_and_innovation_summary": "The student has a good problem-solving ability, and can solve the problem well.",
        # 语言与沟通
        "language_expression_level": random.uniform(0.5, 0.9),
        "reading_comprehension_level": random.uniform(0.5, 0.9),
        "language_and_communication_summary": "The student has a good language expression ability, and can express himself well."
    }
}
