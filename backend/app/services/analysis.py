import random
from sqlalchemy.orm import Session
from typing import List, Dict
from datetime import datetime, timedelta
from app.models.student_data import StudentBehavior, StudentProgress
from app.models.analysis import AnalysisResult
from app.models.curriculum import Subject
from app.models.scale import TestPaperRecord
from app.schemas.analysis import BehaviorAnalysis, KnowledgeAnalysis, StudentReport
from app.services.llm_service import LLMService
from app.models.user import Student
from app.core.formate import serialize_date
import json

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
        self.llm_service = LLMService()

    def record_analysis_result(self, analysis_result: StudentReport):
        db_analysis_result = AnalysisResult(**analysis_result.model_dump())
        self.db.add(db_analysis_result)
        self.db.commit()
        self.db.refresh(db_analysis_result)
        return db_analysis_result

    async def analyze_behavior_by_days(self, student_id: int, behaviors: List[StudentBehavior]) -> Dict:
        """
        分析学生行为数据
        
        Args:
            student_id: 学生ID
            behaviors: 学生行为数据列表
            
        Returns:
            Dict: 行为分析结果
        """
        # 准备数据
        behavior_data = {
            "behaviors": [
                {
                    "id": behavior.id,
                    "behavior_type": behavior.behavior_type,
                    "timestamp": serialize_date(behavior.timestamp),
                    "details": behavior.details
                }
                for behavior in behaviors
            ]
        }
        
        # 调用LLM服务进行分析
        analysis_result = await self.llm_service.generate_analysis({
            "analysis_type": "behavior",
            "student_id": student_id,
            "data": behavior_data
        })
        
        # 如果LLM服务返回失败，使用默认值
        if not analysis_result or "evaluation_metrics" not in analysis_result:
            return {
                "attention_rate": 0.85,
                "emotion_management_level": 0.8,
                "independent_learning_level": 0.8,
                "self_reflection_level": 0.8,
                "self_control_summary": "该学生具有良好的自我控制能力，能够很好地控制自己的情绪。"
            }
        
        # 提取行为分析相关的指标
        behavior_metrics = {
            "attention_rate": analysis_result["evaluation_metrics"].get("attention_rate", 0.85),
            "emotion_management_level": analysis_result["evaluation_metrics"].get("emotion_management_level", 0.8),
            "independent_learning_level": analysis_result["evaluation_metrics"].get("independent_learning_level", 0.8),
            "self_reflection_level": analysis_result["evaluation_metrics"].get("self_reflection_level", 0.8),
            "self_control_summary": analysis_result["evaluation_metrics"].get("self_control_summary", "该学生具有良好的自我控制能力，能够很好地控制自己的情绪。")
        }
        
        return behavior_metrics

    async def analyze_knowledge_by_days(self, student_id: int, progress_records: List[StudentProgress], test_paper_records: List[TestPaperRecord]) -> Dict:
        """
        分析学生知识掌握情况
        
        Args:
            student_id: 学生ID
            progress_records: 学习进度记录列表
            test_paper_records: 测试记录列表
            
        Returns:
            Dict: 知识分析结果
        """
        # 准备数据
        knowledge_data = {
            "progress_records": [
                {
                    "id": record.id,
                    "subject_id": record.subject_id,
                    "book_id": record.book_id,
                    "chapter_id": record.chapter_id,
                    "section_id": record.section_id,
                    "completeness": record.completeness,
                    "duration": record.duration,
                    "mistakes": record.mistakes,
                    "questions": record.questions,
                    "created_at": serialize_date(record.created_at),
                    "updated_at": serialize_date(record.updated_at)
                }
                for record in progress_records
            ],
            "test_paper_records": [
                {
                    "id": record.id,
                    "test_paper_id": record.test_paper_id,
                    "score": record.score,
                    "content": record.content,
                    "created_at": serialize_date(record.created_at),
                    "updated_at": serialize_date(record.updated_at)
                }
                for record in test_paper_records
            ]
        }
        
        # 调用LLM服务进行分析
        analysis_result = await self.llm_service.generate_analysis({
            "analysis_type": "knowledge",
            "student_id": student_id,
            "data": knowledge_data
        })
        
        # 如果LLM服务返回失败，使用默认值
        if not analysis_result or "evaluation_metrics" not in analysis_result:
            return {
                "progress_rate": 0.75,
                "knowledge_master_level": 0.8,
                "knowledge_weak_points": ["知识点1", "知识点2", "知识点3"],
                "knowledge_improvement_suggestions": ["建议1", "建议2", "建议3"],
                "knowledge_summary": "该学生对学科有良好的了解，能够很好地掌握基础知识。"
            }
        
        # 提取知识分析相关的指标
        knowledge_metrics = {
            "progress_rate": analysis_result["evaluation_metrics"].get("progress_rate", 0.75),
            "knowledge_master_level": analysis_result["evaluation_metrics"].get("knowledge_master_level", 0.8),
            "knowledge_weak_points": analysis_result["evaluation_metrics"].get("knowledge_weak_points", ["知识点1", "知识点2", "知识点3"]),
            "knowledge_improvement_suggestions": analysis_result["evaluation_metrics"].get("knowledge_improvement_suggestions", ["建议1", "建议2", "建议3"]),
            "knowledge_summary": analysis_result["evaluation_metrics"].get("knowledge_summary", "该学生对学科有良好的了解，能够很好地掌握基础知识。")
        }
        
        return knowledge_metrics
    
    async def analyze_problem_solving_and_innovation_by_days(self, student_id: int, progress_records: List[StudentProgress], test_paper_records: List[TestPaperRecord]) -> Dict:
        """
        分析学生问题解决与创新能力
        
        Args:
            student_id: 学生ID
            progress_records: 学习进度记录列表
            test_paper_records: 测试记录列表
            
        Returns:
            Dict: 问题解决与创新能力分析结果
        """
        # 准备数据
        problem_solving_data = {
            "progress_records": [
                {
                    "id": record.id,
                    "subject_id": record.subject_id,
                    "book_id": record.book_id,
                    "chapter_id": record.chapter_id,
                    "section_id": record.section_id,
                    "completeness": record.completeness,
                    "duration": record.duration,
                    "mistakes": record.mistakes,
                    "questions": record.questions,
                    "created_at": serialize_date(record.created_at),
                    "updated_at": serialize_date(record.updated_at)
                }
                for record in progress_records
            ],
            "test_paper_records": [
                {
                    "id": record.id,
                    "test_paper_id": record.test_paper_id,
                    "score": record.score,
                    "content": record.content,
                    "created_at": serialize_date(record.created_at),
                    "updated_at": serialize_date(record.updated_at)
                }
                for record in test_paper_records
            ]
        }
        
        # 调用LLM服务进行分析
        analysis_result = await self.llm_service.generate_analysis({
            "analysis_type": "problem_solving",
            "student_id": student_id,
            "data": problem_solving_data
        })
        
        # 如果LLM服务返回失败，使用默认值
        if not analysis_result or "evaluation_metrics" not in analysis_result:
            return {
                "identify_problem_level": 0.8,
                "problem_solving_level": 0.8,
                "innovation_level": 0.8,
                "problem_solving_and_innovation_summary": "该学生具有良好的解决问题的能力，能够很好地解决问题。"
            }
        
        # 提取问题解决与创新能力分析相关的指标
        problem_solving_metrics = {
            "identify_problem_level": analysis_result["evaluation_metrics"].get("identify_problem_level", 0.8),
            "problem_solving_level": analysis_result["evaluation_metrics"].get("problem_solving_level", 0.8),
            "innovation_level": analysis_result["evaluation_metrics"].get("innovation_level", 0.8),
            "problem_solving_and_innovation_summary": analysis_result["evaluation_metrics"].get("problem_solving_and_innovation_summary", "该学生具有良好的解决问题的能力，能够很好地解决问题。")
        }
        
        return problem_solving_metrics
    
    async def analyze_language_and_communication_by_days(self, student_id: int, progress_records: List[StudentProgress]) -> Dict:
        """
        分析学生语言与沟通能力
        
        Args:
            student_id: 学生ID
            progress_records: 学习进度记录列表
            
        Returns:
            Dict: 语言与沟通能力分析结果
        """
        # 准备数据
        language_data = {
            "progress_records": [
                {
                    "id": record.id,
                    "subject_id": record.subject_id,
                    "book_id": record.book_id,
                    "chapter_id": record.chapter_id,
                    "section_id": record.section_id,
                    "completeness": record.completeness,
                    "duration": record.duration,
                    "mistakes": record.mistakes,
                    "questions": record.questions,
                    "created_at": serialize_date(record.created_at),
                    "updated_at": serialize_date(record.updated_at)
                }
                for record in progress_records
            ]
        }
        
        # 调用LLM服务进行分析
        analysis_result = await self.llm_service.generate_analysis({
            "analysis_type": "language",
            "student_id": student_id,
            "data": language_data
        })
        
        # 如果LLM服务返回失败，使用默认值
        if not analysis_result or "evaluation_metrics" not in analysis_result:
            return {
                "language_expression_level": 0.8,
                "reading_comprehension_level": 0.8,
                "language_and_communication_summary": "该学生具有良好的语言表达能力，能够很好地表达自己。"
            }
        
        # 提取语言与沟通能力分析相关的指标
        language_metrics = {
            "language_expression_level": analysis_result["evaluation_metrics"].get("language_expression_level", 0.8),
            "reading_comprehension_level": analysis_result["evaluation_metrics"].get("reading_comprehension_level", 0.8),
            "language_and_communication_summary": analysis_result["evaluation_metrics"].get("language_and_communication_summary", "该学生具有良好的语言表达能力，能够很好地表达自己。")
        }
        
        return language_metrics
    
    async def generate_analysis_report(self, student_id: int, evaluation_metrics: Dict) -> str:
        """
        生成分析报告
        
        Args:
            student_id: 学生ID
            evaluation_metrics: 评估指标
            
        Returns:
            str: 分析报告
        """
        # 获取学生信息
        student = self.db.query(Student).filter(Student.id == student_id).first()
        
        # 准备数据
        report_data = {
            "student_info": {
                "id": student.id,
                "username": student.username,
                "full_name": student.full_name,
                "gender": student.gender.value if student.gender else None,
                "age": student.age,
                "grade": student.grade
            },
            "evaluation_metrics": evaluation_metrics
        }
        
        # 调用LLM服务生成报告
        analysis_result = await self.llm_service.generate_analysis({
            "analysis_type": "report",
            "student_id": student_id,
            "data": report_data
        })
        
        # 如果LLM服务返回失败，使用默认值
        if not analysis_result or "analysis_report" not in analysis_result:
            return "该学生具有良好的解决问题的能力，能够很好地解决问题。您可以使用此报告帮助学生改进学习。"
        
        return analysis_result["analysis_report"]

    async def analyze_report_by_days(self, student_id: int, days: int = 30) -> StudentReport:
        """
        根据天数分析学生报告
        
        Args:
            student_id: 学生ID
            days: 天数
            
        Returns:
            StudentReport: 学生报告
        """
        # 获取数据
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
        
        # 分析数据
        behavior_analysis = await self.analyze_behavior_by_days(student_id, behaviors)
        knowledge_analysis = await self.analyze_knowledge_by_days(student_id, progress_records, test_paper_records)
        problem_solving_and_innovation_analysis = await self.analyze_problem_solving_and_innovation_by_days(student_id, progress_records, test_paper_records)
        language_and_communication_analysis = await self.analyze_language_and_communication_by_days(student_id, progress_records)
        
        # 合并分析结果
        evaluation_metrics = {**behavior_analysis, **knowledge_analysis, **problem_solving_and_innovation_analysis, **language_and_communication_analysis}
        
        # 生成分析报告
        analysis_report = await self.generate_analysis_report(student_id, evaluation_metrics)
        
        # 创建学生报告
        return StudentReport(
            student_id=student_id,
            analysis_type=f"{days}days",
            analysis_timestamp=datetime.now(),
            analysis_report=analysis_report,
            evaluation_metrics=evaluation_metrics
        )

    async def generate_analysis_trend_by_days(self, student_id: int, days: int = 30) -> Dict[str, List[Dict]]:
        """
        生成分析趋势数据
        
        Args:
            student_id: 学生ID
            days: 天数
            
        Returns:
            Dict[str, List[Dict]]: 分析趋势数据
        """
        # 获取分析结果
        analysis_results = self.db.query(AnalysisResult).filter(
            AnalysisResult.student_id == student_id,
            AnalysisResult.analysis_timestamp >= datetime.now() - timedelta(days=days),
        ).all()
        analysis_results = sorted(analysis_results, key=lambda x: x.analysis_timestamp, reverse=False)
        
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
                analysis_trend[str(date)].append({
                    "student_id": analysis.student_id,
                    "analysis_type": analysis.analysis_type,
                    "analysis_timestamp": serialize_date(analysis.analysis_timestamp),
                    "analysis_report": analysis.analysis_report,
                    "evaluation_metrics": analysis.evaluation_metrics
                })
        
        return analysis_trend

