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


class StudentReport(BaseModel):
    student_id: int
    analysis_type: str
    analysis_timestamp: datetime
    analysis_report: str
    evaluation_metrics: Dict[str, Any]

    class Config:
        from_attributes = True


