from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.student_data import StudentBehavior
from app.core.auth import oauth2_scheme
from datetime import datetime

router = APIRouter()

@router.post("/behaviors/")
def create_behavior(
    behavior_data: dict,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    behavior = StudentBehavior(
        student_id=behavior_data["student_id"],
        behavior_type=behavior_data["behavior_type"],
        timestamp=datetime.fromisoformat(behavior_data["timestamp"]),
        duration=behavior_data["duration"],
        details=behavior_data["details"]
    )
    db.add(behavior)
    db.commit()
    db.refresh(behavior)
    return behavior

@router.get("/statistics/{student_id}")
def get_student_statistics(
    student_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    behavior_count = db.query(StudentBehavior).filter(
        StudentBehavior.student_id == student_id
    ).count()
    
    return {
        "behavior_count": behavior_count,
        "progress_count": 0  # 这里需要实现进度统计
    }
