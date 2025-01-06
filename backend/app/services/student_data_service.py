import json
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
from app.models.student_data import StudentBehavior, StudentProgress
from app.models.curriculum import Subject, Book, Chapter, Section
from app.schemas.student_data import BehaviorCreate, ProgressCreate

class StudentDataService:
    def __init__(self, db: Session):
        self.db = db

    def record_behavior(self, behavior: BehaviorCreate) -> StudentBehavior:
        db_behavior = StudentBehavior(**behavior.model_dump())
        self.db.add(db_behavior)
        self.db.commit()
        self.db.refresh(db_behavior)
        return db_behavior

    def record_progress(self, progress: ProgressCreate) -> StudentProgress:
        db_progress = StudentProgress(**progress.model_dump())
        self.db.add(db_progress)
        self.db.commit()
        self.db.refresh(db_progress)
        return db_progress

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
                if datetime.strptime(m["timestamp"], '%Y-%m-%d %H:%M:%S') >= start_date:
                    mistakes[f'{subjects[p.subject_id]}-{books[p.book_id]}-{chapters[p.chapter_id]}-{sections[p.section_id]}'].append(m)
            for q in p.questions:
                if datetime.strptime(q["timestamp"], '%Y-%m-%d %H:%M:%S') >= start_date:
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
    