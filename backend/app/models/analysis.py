from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from .base import Base, TimeStampMixin

class AnalysisResult(Base, TimeStampMixin):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    analysis_timestamp = Column(DateTime)
    analysis_report = Column(String)
    evaluation_metrics = Column(JSON)
