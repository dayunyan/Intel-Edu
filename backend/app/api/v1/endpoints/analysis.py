from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime
from app.db.session import get_db
from app.services.analysis import AnalysisService
from app.schemas.analysis import StudentReport

router = APIRouter()

@router.get("/report/7days/{student_id}", response_model=StudentReport)
async def generate_student_report_by_days(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    student_report = analysis_service.analyze_report_by_days(student_id, days=7)
    print(student_report)
    # analysis_service.record_analysis_result(student_report) # 暂时不记录分析结果

    return student_report

@router.get("/report/30days/{student_id}", response_model=StudentReport)
async def generate_student_report_by_days(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    student_report = analysis_service.analyze_report_by_days(student_id, days=30)
    print(student_report)
    # analysis_service.record_analysis_result(student_report) # 暂时不记录分析结果

    return student_report

@router.get("/trend/30days/{student_id}", response_model=Dict[str, List[StudentReport]])
async def generate_student_trend_by_days(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    student_trend = analysis_service.generate_analysis_trend_by_days(student_id, days=30)
    print(student_trend)

    return student_trend

@router.get("/trend/90days/{student_id}", response_model=Dict[str, List[StudentReport]])
async def generate_student_trend_by_days(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    student_trend = analysis_service.generate_analysis_trend_by_days(student_id, days=90)
    print(student_trend)

    return student_trend
