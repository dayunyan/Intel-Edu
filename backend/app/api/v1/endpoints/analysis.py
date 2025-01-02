from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.db.session import get_db
from app.services.analysis import AnalysisService
from app.schemas.analysis import StudyReport, BehaviorAnalysis, KnowledgeAnalysis
from app.models.student_data import StudentBehavior
from app.core.auth import oauth2_scheme

router = APIRouter()


@router.get("/behavior/{student_id}")
def get_behavior_analysis(
    student_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    behaviors = db.query(StudentBehavior).filter(
        StudentBehavior.student_id == student_id
    ).all()
    
    total_time = sum(b.duration for b in behaviors)
    attention_time = sum(b.duration for b in behaviors if b.behavior_type == "attention")
    
    return {
        "attention_rate": attention_time / total_time if total_time > 0 else 0,
        "participation_rate": len(behaviors) / 10,  # 假设每天预期10个行为
        "total_study_time": total_time,
        "distraction_count": len([b for b in behaviors if b.behavior_type == "distraction"]),
        "behavior_trend": []  # 这里需要实现趋势分析
    }


@router.get("/knowledge/{student_id}", response_model=List[KnowledgeAnalysis])
def analyze_student_knowledge(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    return analysis_service.analyze_knowledge(student_id)


@router.get("/report/{student_id}", response_model=StudyReport)
async def generate_study_report(student_id: int, db: Session = Depends(get_db)):
    analysis_service = AnalysisService(db)
    behavior_analysis = analysis_service.analyze_behavior(student_id)
    knowledge_analysis = analysis_service.analyze_knowledge(student_id)

    # 生成整体评价和建议
    overall_evaluation = "根据分析结果生成的整体评价..."
    suggestions = ["建议1...", "建议2...", "建议3..."]

    return StudyReport(
        student_id=student_id,
        report_date=datetime.now(),
        behavior_analysis=behavior_analysis,
        knowledge_analysis=knowledge_analysis,
        overall_evaluation=overall_evaluation,
        suggestions=suggestions,
    )
