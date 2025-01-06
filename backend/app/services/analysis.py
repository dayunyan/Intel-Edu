import random
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
from app.models.student_data import StudentBehavior, StudentProgress
from app.models.analysis import AnalysisResult
from app.models.curriculum import Subject
from app.models.scale import TestPaperRecord
from app.schemas.analysis import BehaviorAnalysis, KnowledgeAnalysis, StudentReport

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
class AnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def record_analysis_result(self, analysis_result: StudentReport):
        db_analysis_result = AnalysisResult(**analysis_result.model_dump())
        self.db.add(db_analysis_result)
        self.db.commit()
        self.db.refresh(db_analysis_result)
        return db_analysis_result


    def analyze_behavior_by_days(self, behaviors: List[StudentBehavior]) -> Dict:
        # LLM分析行为数据
        #TODO: 需要实现LLM分析行为数据
        behavior_analysis = {
            "attention_rate": 0.85,
            "emotion_management_level": 0.8,
            "independent_learning_level": 0.8,
            "self_reflection_level": 0.8,
            "self_control_summary": "The student has a good self-control ability, and can control his emotions well."
        }

        return behavior_analysis

    
    def analyze_knowledge_by_days(self, progress_records: List[StudentProgress], test_paper_records: List[TestPaperRecord]) -> Dict:
        #TODO: 需要实现LLM分析知识数据
        knowledge_analysis = {
            "progress_rate": 0.75,
            "knowledge_master_level": 0.8,
            "knowledge_weak_points": ["知识点1", "知识点2", "知识点3"],
            "knowledge_improvement_suggestions": ["建议1...", "建议2...", "建议3..."],
            "knowledge_summary": "The student has a good knowledge of the subject, and can master the basic knowledge well."
        }

        return knowledge_analysis
    
    def analyze_problem_solving_and_innovation_by_days(self, progress_records: List[StudentProgress], test_paper_records: List[TestPaperRecord]) -> Dict:
        #TODO: 需要实现LLM分析问题解决与创新数据
        problem_solving_and_innovation_analysis = {
            "identify_problem_level": 0.8,
            "problem_solving_level": 0.8,
            "innovation_level": 0.8,
            "problem_solving_and_innovation_summary": "The student has a good problem-solving ability, and can solve the problem well."
        }
        return problem_solving_and_innovation_analysis
    
    def analyze_language_and_communication_by_days(self, progress_records: List[StudentProgress]) -> Dict:
        #TODO: 需要实现LLM分析语言与沟通数据
        language_and_communication_analysis = {
            "language_expression_level": 0.8,
            "reading_comprehension_level": 0.8,
            "language_and_communication_summary": "The student has a good language expression ability, and can express himself well."
        }
        return language_and_communication_analysis
    
    def generate_analysis_report(self, evaluation_metrics: Dict) -> str:
        #TODO: 需要实现LLM生成分析报告
        overall_report = "The student has a good problem-solving ability, and can solve the problem well. You can use this report to help the student improve their learning."
        
        return overall_report

    def analyze_report_by_days(self, student_id: int, days: int = 30) -> StudentReport:
        behaviors = self.db.query(StudentBehavior).filter(
            StudentBehavior.student_id == student_id,
            StudentBehavior.timestamp >= datetime.now() - timedelta(days=days),
        ).all()
        progress_records = self.db.query(StudentProgress).filter(
            StudentProgress.student_id == student_id,
            StudentProgress.updated_at >= datetime.now() - timedelta(days=days),
        ).all()
        test_paper_records = self.db.query(TestPaperRecord).filter(
            TestPaperRecord.student_id == student_id,
            TestPaperRecord.updated_at >= datetime.now() - timedelta(days=days),
        ).all()
        
        behavior_analysis = self.analyze_behavior_by_days(behaviors)
        knowledge_analysis = self.analyze_knowledge_by_days(progress_records, test_paper_records)
        problem_solving_and_innovation_analysis = self.analyze_problem_solving_and_innovation_by_days(progress_records, test_paper_records)
        language_and_communication_analysis = self.analyze_language_and_communication_by_days(progress_records)
        
        evaluation_metrics = behavior_analysis | knowledge_analysis | problem_solving_and_innovation_analysis | language_and_communication_analysis
        
        analysis_report = self.generate_analysis_report(evaluation_metrics)
        
        return StudentReport(
            student_id=student_id,
            analysis_type=f"{days}days",
            analysis_timestamp=datetime.now(),
            analysis_report=analysis_report,
            evaluation_metrics=evaluation_metrics
        )


    def generate_analysis_trend_by_days(self, student_id: int, days: int = 30) -> List[Dict]:
        # 生成行为趋势数据的具体实现
        analysis_results = self.db.query(AnalysisResult).filter(
            AnalysisResult.student_id == student_id,
            AnalysisResult.analysis_timestamp >= datetime.now() - timedelta(days=days),
        ).all()
        analysis_results = sorted(analysis_results, key=lambda x: x.analysis_timestamp, reverse=False)
        print(analysis_results)
        # 按日期分组统计数据
        analysis_trend = {}
        # 每隔7天提取一次
        last_date = None
        for analysis in analysis_results:
            date = analysis.analysis_timestamp.date()
            if last_date is None or date - last_date >= timedelta(days=7):
                last_date = date
                analysis_trend[str(date)] = []
            if str(date) in analysis_trend:
                analysis_trend[str(date)].append(analysis)
        return analysis_trend

