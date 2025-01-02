from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime


class BehaviorAnalysis(BaseModel):
    total_study_time: float
    attention_rate: float
    distraction_count: int
    behavior_trend: List[Dict[str, Any]]


class KnowledgeAnalysis(BaseModel):
    subject: str
    mastery_level: float
    weak_points: List[str]
    improvement_suggestions: List[str]
    knowledge_trend: List[Dict[str, Any]]


class StudyReport(BaseModel):
    student_id: int
    report_date: datetime
    behavior_analysis: BehaviorAnalysis
    knowledge_analysis: List[KnowledgeAnalysis]
    overall_evaluation: str
    suggestions: List[str]

    class Config:
        from_attributes = True
