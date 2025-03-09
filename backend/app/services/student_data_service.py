import json
from sqlalchemy.orm import Session
from typing import Any, List, Dict
from datetime import datetime, timedelta
from app.models.student_data import StudentBehavior, StudentProgress
from app.models.curriculum import Subject, Book, Chapter, Section
from app.schemas.student_data import BehaviorCreate, ProgressCreate
from sqlalchemy.orm.attributes import flag_modified

class StudentDataService:
    def __init__(self, db: Session):
        self.db = db

    async def record_behavior(self, behavior: BehaviorCreate) -> StudentBehavior:
        db_behavior = StudentBehavior(**behavior.model_dump())
        self.db.add(db_behavior)
        self.db.commit()
        self.db.refresh(db_behavior)
        return db_behavior

    async def record_progress(self, progress: ProgressCreate) -> StudentProgress:
        db_progress = StudentProgress(**progress.model_dump())
        self.db.add(db_progress)
        self.db.commit()
        self.db.refresh(db_progress)
        return db_progress
    
    async def record_question(self, chat_id: int,student_id: int, question: Dict[str, Any], answer: Dict[str, Any]) -> StudentProgress:
        try:
            subject = self.db.query(Subject).filter(Subject.name == answer['subject']).first()
            book = self.db.query(Book).filter(Book.subject_id == subject.id, Book.name == answer['book']).first()
            chapter = self.db.query(Chapter).filter(Chapter.book_id == book.id, Chapter.name == answer['chapter']).first()
            section = self.db.query(Section).filter(Section.chapter_id == chapter.id, Section.name == answer['section']).first()
            
            progress = self.db.query(StudentProgress).filter(StudentProgress.student_id == student_id,
                                                            StudentProgress.subject_id == subject.id,
                                                            StudentProgress.book_id == book.id,
                                                            StudentProgress.chapter_id == chapter.id,
                                                            StudentProgress.section_id == section.id).first()
            if progress is None:
                progress = StudentProgress(student_id=student_id,
                                        subject_id=subject.id,
                                        book_id=book.id,
                                        chapter_id=chapter.id,
                                        section_id=section.id,
                                        completeness=0,
                                        duration=0,
                                        mistakes=[],
                                        questions=[
                                            {
                                                "chat_id": chat_id,
                                                "timestamp": question['timestamp'],
                                                "student_question": question['content'],
                                                "ai_response": answer['content'],
                                                "history": [],
                                                "details": {
                                                    "summary": ""
                                                }
                                            }
                                        ])
                self.db.add(progress)
            else:
                progress = self._update_question(progress, chat_id, question, answer)
                flag_modified(progress, "questions")
            self.db.commit()
            self.db.refresh(progress)
            return progress
        except Exception as e:
            self.db.rollback()
            print(f"更新失败的消息内容: {progress.questions} \n {str(e)}")
            raise RuntimeError(f"更新数据库失败：{str(e)}")
        

    def _update_question(self, progress: StudentProgress, chat_id: int, question: Dict[str, Any], answer: Dict[str, Any]) -> StudentProgress:
        """
        更新question
        """
        flag = -1
        for q in progress.questions:
            if 'chat_id' in q.keys() and q['chat_id'] == chat_id:
                temp_chat = {
                    "timestamp": q['timestamp'],
                    "student_question": q['student_question'],
                    "ai_response": q['ai_response']
                }
                q['history'].append(temp_chat)
                q['timestamp'] = question['timestamp']
                q['student_question'] = question['content']
                q['ai_response'] = answer['content']
                flag = chat_id
        if flag == -1:
            progress.questions.append(
                {
                    "chat_id": chat_id,
                    "timestamp": question['timestamp'],
                    "student_question": question['content'],
                    "ai_response": answer['content'],
                    "history": [],
                    "details": {
                        "summary": ""
                    }
                }
            )
            
        return progress
    
    def get_student_statistics_by_time(self, student_id: int, days: int = 30) -> Dict:
        start_date = datetime.now() - timedelta(days=days)
        
        # 获取行为统计
        behaviors = self.db.query(StudentBehavior).filter(
            StudentBehavior.student_id == student_id,
            StudentBehavior.timestamp >= start_date
        ).all()
        
        # 获取progress
        progress = self.db.query(StudentProgress).filter(
            StudentProgress.student_id == student_id,
            StudentProgress.updated_at >= start_date
        ).all()
        
        subjects = {}
        books = {}
        chapters = {}
        sections = {}
        mistakes = {} # 获取最近的progress中的mistake记录
        questions = {} # 获取最近的progress中的question记录
        for p in progress:
            if p.subject_id not in subjects:
                subjects[p.subject_id] = self.db.query(Subject).filter(Subject.id == p.subject_id).first().name
            if p.book_id not in books:
                books[p.book_id] = self.db.query(Book).filter(Book.id == p.book_id).first().name
            if p.chapter_id not in chapters:
                chapters[p.chapter_id] = self.db.query(Chapter).filter(Chapter.id == p.chapter_id).first().name
            if p.section_id not in sections:
                sections[p.section_id] = self.db.query(Section).filter(Section.id == p.section_id).first().name
            if f'{subjects[p.subject_id]}-{books[p.book_id]}-{chapters[p.chapter_id]}-{sections[p.section_id]}' not in mistakes:
                mistakes[f'{subjects[p.subject_id]}-{books[p.book_id]}-{chapters[p.chapter_id]}-{sections[p.section_id]}'] = []
            if f'{subjects[p.subject_id]}-{books[p.book_id]}-{chapters[p.chapter_id]}-{sections[p.section_id]}' not in questions:
                questions[f'{subjects[p.subject_id]}-{books[p.book_id]}-{chapters[p.chapter_id]}-{sections[p.section_id]}'] = []
            for m in p.mistakes:
                if self._parse_timestamp(m["timestamp"]).strftime('%Y-%m-%d %H:%M:%S') >= start_date.strftime('%Y-%m-%d %H:%M:%S'):
                    mistakes[f'{subjects[p.subject_id]}-{books[p.book_id]}-{chapters[p.chapter_id]}-{sections[p.section_id]}'].append(m)
            for q in p.questions:
                if self._parse_timestamp(q["timestamp"]).strftime('%Y-%m-%d %H:%M:%S') >= start_date.strftime('%Y-%m-%d %H:%M:%S'):
                    questions[f'{subjects[p.subject_id]}-{books[p.book_id]}-{chapters[p.chapter_id]}-{sections[p.section_id]}'].append(q)
        

        return {
            "behavior_count": len(behaviors),
            "progress_count": len(progress),
            "behavior_statistics": self._behavior_statistics(behaviors),
            "progress_statistics": self._progress_statistics(progress),
            "mistakes_statistics": self._mistakes_statistics(mistakes),
            "questions_statistics": self._questions_statistics(questions)
        }

    def _behavior_statistics(self, behaviors: List[StudentBehavior]) -> Dict:
        if not behaviors:
            return {}
        statistics = {}
        for behavior in behaviors:
            if behavior.behavior_type not in statistics:
                statistics[behavior.behavior_type] = 0
            statistics[behavior.behavior_type] += 1
        return statistics

    def _progress_statistics(self, progress_records: List[StudentProgress]) -> Dict:
        if not progress_records:
            return {}
        progress_count = len(progress_records)
        completeness_avg = sum(progress.completeness for progress in progress_records) / progress_count
        duration_avg = sum(progress.duration for progress in progress_records) / progress_count
        return {
            "completeness_avg": completeness_avg,
            "duration_avg": duration_avg,
        }
    
    def _mistakes_statistics(self, mistakes: Dict[str, List[Dict]]) -> Dict:
        if not mistakes:
            return {}
        
        mistakes_statistics = {}
        for key, value in mistakes.items():
            if key not in mistakes_statistics:
                mistakes_statistics[key] = 0
            mistakes_statistics[key] += len(value)
        return mistakes_statistics

    def _questions_statistics(self, questions: Dict[str, List[Dict]]) -> Dict:
        if not questions:
            return {}
        questions_statistics = {}
        for key, value in questions.items():
            if key not in questions_statistics:
                questions_statistics[key] = 0
            questions_statistics[key] += len(value)
        return questions_statistics
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """
        解析不同格式的时间戳字符串
        """
        try:
            # 首先尝试解析ISO格式
            if 'T' in timestamp_str:
                # 处理带Z的UTC时间
                if timestamp_str.endswith('Z'):
                    timestamp_str = timestamp_str[:-1] + '+00:00'
                return datetime.fromisoformat(timestamp_str)
            # 然后尝试解析标准格式
            return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            print(f"时间解析错误: {timestamp_str}, {str(e)}")
            # 如果解析失败，返回当前时间
            return datetime.now()
    