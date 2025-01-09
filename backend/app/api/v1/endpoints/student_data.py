from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.student_data import StudentBehavior
from app.services.student_data_service import StudentDataService
from app.schemas.student_data import StudentStatistics

router = APIRouter()

@router.post("/behaviors/")
def create_behavior(
    behavior_data: dict,
    db: Session = Depends(get_db),
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

@router.get("/statistics/1days/{student_id}", response_model=StudentStatistics)
def get_student_statistics_1days(
    student_id: int,
    db: Session = Depends(get_db),
):
    studata_service = StudentDataService(db)
    statistics = studata_service.get_student_statistics_by_time(student_id, 1)
    
    return StudentStatistics(**statistics)

@router.get("/statistics/7days/{student_id}", response_model=StudentStatistics)
def get_student_statistics_7days(
    student_id: int,
    db: Session = Depends(get_db),
):
    studata_service = StudentDataService(db)
    statistics = studata_service.get_student_statistics_by_time(student_id, 7)
    
    return StudentStatistics(**statistics)

@router.get("/statistics/30days/{student_id}", response_model=StudentStatistics)
def get_student_statistics_30days(
    student_id: int,
    db: Session = Depends(get_db),
):
    print(student_id)
    studata_service = StudentDataService(db)
    statistics = studata_service.get_student_statistics_by_time(student_id, 30)
    print(statistics)
    
    return StudentStatistics(**statistics)
