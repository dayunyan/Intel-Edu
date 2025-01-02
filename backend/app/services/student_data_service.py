from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
from app.models.student_data import StudentBehavior, StudentProgress
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

    def get_student_statistics(self, student_id: int, days: int = 30) -> Dict:
        start_date = datetime.now() - timedelta(days=days)
        
        # 获取行为统计
        behaviors = self.db.query(StudentBehavior).filter(
            StudentBehavior.student_id == student_id,
            StudentBehavior.timestamp >= start_date
        ).all()
        
        # 获取学习进度
        progress = self.db.query(StudentProgress).filter(
            StudentProgress.student_id == student_id,
            StudentProgress.created_at >= start_date
        ).all()
        

        return {
            "behavior_count": len(behaviors),
            "progress_count": len(progress),
            "average_score": sum(p.score for p in progress) / len(progress) if progress else 0,
            "attention_rate": self._calculate_attention_rate(behaviors),
            "weak_points": self._identify_weak_points(progress)
        }

    def _calculate_attention_rate(self, behaviors: List[StudentBehavior]) -> float:
        if not behaviors:
            return 0.0
        attention_time = sum(b.duration for b in behaviors if b.behavior_type == "attention")
        total_time = sum(b.duration for b in behaviors)
        return attention_time / total_time if total_time > 0 else 0

    def _identify_weak_points(self, progress_records: List[StudentProgress]) -> List[Dict]:
        weak_points = []
        for record in progress_records:
            if record.score < 60:
                weak_points.append({
                    "subject": record.subject,
                    "chapter": record.chapter,
                    "section": record.section,
                    "score": record.score
                })
        return weak_points 