from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.student_data import StudentBehavior
from app.services.student_data_service import StudentDataService
from app.schemas.student_data import StudentStatistics, BehaviorCreate

router = APIRouter()

@router.post("/behaviors/")
def create_behavior(
    behavior_data: BehaviorCreate,
    db: Session = Depends(get_db),
):
    try:
        service = StudentDataService(db)
        behavior = service.record_behavior(behavior_data)
        return behavior
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"记录行为失败: {str(e)}")

@router.get("/statistics/1days/{student_id}", response_model=StudentStatistics)
def get_student_statistics_1days(
    student_id: int,
    db: Session = Depends(get_db),
):
    try:
        studata_service = StudentDataService(db)
        statistics = studata_service.get_student_statistics_by_time(student_id, 1)
        return StudentStatistics(**statistics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")

@router.get("/statistics/7days/{student_id}", response_model=StudentStatistics)
def get_student_statistics_7days(
    student_id: int,
    db: Session = Depends(get_db),
):
    try:
        studata_service = StudentDataService(db)
        statistics = studata_service.get_student_statistics_by_time(student_id, 7)
        return StudentStatistics(**statistics)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")

@router.get("/statistics/30days/{student_id}", response_model=StudentStatistics)
def get_student_statistics_30days(
    student_id: int,
    db: Session = Depends(get_db),
):
    try:
        studata_service = StudentDataService(db)
        statistics = studata_service.get_student_statistics_by_time(student_id, 30)
        return StudentStatistics(**statistics)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"获取统计数据失败: {str(e)}")
