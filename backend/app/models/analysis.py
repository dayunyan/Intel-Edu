from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from .base import Base, TimeStampMixin

""" JSON template for evaluation_metrics in AnalysisResult
#TODO: 需要根据实际情况修改
{
    # 自我管理
    "attention_rate": 0.85,
    "emotion_management_level": 0.8,
    "independent_learning_level": 0.8,
    "self_reflection_level": 0.8,
    "self_control_summary": "The student has a good self-control ability, and can control his emotions well."
    # 知识掌握
    "progress_rate": 0.75,
    "knowledge_master_level": 0.8,
    "knowledge_weak_points": ["知识点1", "知识点2", "知识点3"],
    "knowledge_improvement_suggestions": ["建议1", "建议2", "建议3"],
    "knowledge_summary": "The student has a good knowledge of the subject, and can master the basic knowledge well."
    # 问题解决与创新
    "identify_problem_level": 0.8,
    "problem_solving_level": 0.8,
    "innovation_level": 0.8,
    "problem_solving_and_innovation_summary": "The student has a good problem-solving ability, and can solve the problem well."
    # 语言与沟通
    "language_expression_level": 0.8,
    "reading_comprehension_level": 0.8,
    "language_and_communication_summary": "The student has a good language expression ability, and can express himself well."
}
"""

class AnalysisResult(Base, TimeStampMixin):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    analysis_type = Column(String) # 7days, 30days
    analysis_timestamp = Column(DateTime)
    analysis_report = Column(String)
    evaluation_metrics = Column(JSON)
