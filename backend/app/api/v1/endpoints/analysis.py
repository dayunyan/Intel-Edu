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
    student_report = await analysis_service.analyze_report_by_days(student_id, days=7)
    analysis_service.record_analysis_result(student_report)

    return student_report

@router.get("/report/30days/{student_id}", response_model=StudentReport)
async def generate_student_report_by_days(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    student_report = await analysis_service.analyze_report_by_days(student_id, days=30)
    analysis_service.record_analysis_result(student_report)

    return student_report

@router.get("/trend/30days/{student_id}", response_model=Dict[str, List[Dict]])
async def generate_student_trend_by_days(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    trend_data = await analysis_service.generate_analysis_trend_by_days(student_id, days=30)
    return trend_data

@router.get("/trend/90days/{student_id}", response_model=Dict[str, List[Dict]])
async def generate_student_trend_by_days(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    trend_data = await analysis_service.generate_analysis_trend_by_days(student_id, days=90)
    return trend_data

@router.post("/save-report", response_model=StudentReport)
async def save_student_report(report: StudentReport, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    saved_report = analysis_service.record_analysis_result(report)
    return saved_report
