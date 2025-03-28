from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class BehaviorBase(BaseModel):
    behavior_type: str
    duration: float
    details: Dict[str, Any]


class BehaviorCreate(BehaviorBase):
    student_id: int
    timestamp: datetime


class BehaviorInDB(BehaviorBase):
    id: int
    student_id: int
    timestamp: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ProgressBase(BaseModel):
    subject: str
    chapter: str
    section: str
    score: float
    mistakes: List[Dict[str, Any]]
    questions: List[Dict[str, Any]]


class ProgressCreate(ProgressBase):
    student_id: int


class ProgressInDB(ProgressBase):
    id: int
    student_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentStatistics(BaseModel):
    behavior_count: int
    progress_count: int
    behavior_statistics: Dict[str, int]
    progress_statistics: Dict[str, float]
    mistakes_statistics: Dict[str, int]
    questions_statistics: Dict[str, int]


