import json
import httpx
from typing import Dict, Any, List, Tuple
from datetime import datetime
from app.core.config import settings
from app.core.prompt_template import (
    SYSTEM_PROMPT_TEMPLATE_ZH_BEHAVIOR,
    SYSTEM_PROMPT_TEMPLATE_ZH_KNOWLEDGE,
    SYSTEM_PROMPT_TEMPLATE_ZH_PROBLEM_SOLVING,
    SYSTEM_PROMPT_TEMPLATE_ZH_LANGUAGE,
    SYSTEM_PROMPT_TEMPLATE_ZH_REPORT,
    SYSTEM_PROMPT_TEMPLATE_ZH_GENERAL
)

class LLMService:
    """
    LLM服务类，用于与LLM服务器通信
    """
    def __init__(self, api_url=None, api_key=None):
        # 使用直接属性访问而不是get方法
        self.analysis_api_url = api_url or f"{settings.LLM_SERVER_URL}/analysis" if hasattr(settings, "LLM_SERVER_URL") else "http://llm-server:8000/api/v1/generate"
        self.chat_api_url = f"{settings.LLM_SERVER_URL}/chat" if hasattr(settings, "LLM_SERVER_URL") else "http://llm-server:8000/api/v1/chat"
        self.api_key = api_key or settings.OPENAI_API_KEY if hasattr(settings, "OPENAI_API_KEY") else None

    
    async def generate_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        向LLM服务器发送分析请求
        
        Args:
            data: 包含学生数据的字典，必须包含analysis_type字段
            
        Returns:
            Dict[str, Any]: LLM服务器返回的分析结果
        """
        try:
            analysis_type = data.get("analysis_type", "")
            
            # 获取系统提示词和用户提示词
            system_prompt, user_prompt = self._create_analysis_prompt(data)
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.analysis_api_url,
                    json={
                        "system": system_prompt,
                        "prompt": user_prompt,
                        "max_tokens": 2000,
                        "temperature": 0.7
                    }
                )
                
                if response.status_code != 200:
                    raise Exception(f"LLM服务器返回错误: {response.status_code}, {response.text}")
                
                result = response.json()
                return self._parse_analysis_result(result, analysis_type)
        except Exception as e:
            # 如果LLM服务器不可用，返回模拟数据
            print(f"LLM服务器请求失败: {str(e)}")
            return self._generate_mock_analysis(data.get("analysis_type", ""))
    
    async def generate_chat_response(self, role_name: str, role_description:str, messages: List[Dict[str, Any]], student_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        向LLM服务器发送聊天请求
        
        Args:
            role: 角色描述
            messages: 聊天历史记录
            student_info: 学生信息（可选）
            
        Returns:
            Dict[str, Any]: LLM服务器返回的聊天结果
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                request_data = {
                    "role_name": role_name,
                    "role_description": role_description,
                    "messages": messages,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_tokens": 1000
                }
                
                # 如果有学生信息，添加到请求中
                if student_info:
                    request_data["student_info"] = student_info
                
                response = await client.post(
                    self.chat_api_url,
                    json=request_data
                )
                
                if response.status_code != 200:
                    raise Exception(f"LLM服务器返回错误: {response.status_code}, {response.text}")
                
                result = response.json()
                return {
                    "content": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                    "timestamp": datetime.now()
                }
        except Exception as e:
            # 如果LLM服务器不可用，返回模拟数据
            print(f"LLM聊天服务器请求失败: {str(e)}")
            return {
                "content": "我是AI助手，很抱歉，我现在无法连接到服务器。请稍后再试。",
                "timestamp": datetime.now()
            }
    
    def _create_analysis_prompt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        根据分析类型创建不同的分析提示词
        
        Args:
            data: 包含学生数据的字典，必须包含analysis_type字段
            
        Returns:
            Tuple[str, str]: 系统提示词和用户提示词
        """
        analysis_type = data.get("analysis_type", "")
        
        if analysis_type == "behavior":
            return self._create_behavior_analysis_prompt(data)
        elif analysis_type == "knowledge":
            return self._create_knowledge_analysis_prompt(data)
        elif analysis_type == "problem_solving":
            return self._create_problem_solving_analysis_prompt(data)
        elif analysis_type == "language":
            return self._create_language_analysis_prompt(data)
        elif analysis_type == "report":
            return self._create_report_analysis_prompt(data)
        else:
            return self._create_general_analysis_prompt(data)
    
    def _create_behavior_analysis_prompt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        创建行为分析提示词
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE_ZH_BEHAVIOR
        user_prompt = f"""
        学生数据:
        {json.dumps(data.get("data", {}), ensure_ascii=False, indent=2)}
        
        请根据学生数据进行行为分析，并根据回答规则生成分析报告。
        """
        return system_prompt, user_prompt
    
    def _create_knowledge_analysis_prompt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        创建知识分析提示词
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE_ZH_KNOWLEDGE
        user_prompt = f"""
        学生数据:
        {json.dumps(data.get("data", {}), ensure_ascii=False, indent=2)}
        
        请根据学生数据进行知识分析，并根据回答规则生成分析报告。
        """
        return system_prompt, user_prompt
    
    def _create_problem_solving_analysis_prompt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        创建问题解决与创新能力分析提示词
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE_ZH_PROBLEM_SOLVING
        user_prompt = f"""
        学生数据:
        {json.dumps(data.get("data", {}), ensure_ascii=False, indent=2)}
        
        请根据学生数据进行问题解决与创新能力分析，并根据回答规则生成分析报告。
        """
        return system_prompt, user_prompt
    
    def _create_language_analysis_prompt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        创建语言与沟通能力分析提示词
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE_ZH_LANGUAGE
        user_prompt = f"""
        学生数据:
        {json.dumps(data.get("data", {}), ensure_ascii=False, indent=2)}
        
        请根据学生数据进行语言与沟通能力分析，并根据回答规则生成分析报告。
        """
        return system_prompt, user_prompt
    
    def _create_report_analysis_prompt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        创建报告分析提示词
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE_ZH_REPORT
        user_prompt = f"""
        学生信息:
        {json.dumps(data.get("data", {}).get("student_info", {}), ensure_ascii=False, indent=2)}
        
        评估指标:
        {json.dumps(data.get("data", {}).get("evaluation_metrics", {}), ensure_ascii=False, indent=2)}

        请根据学生信息和评估指标生成分析报告。
        """
        return system_prompt, user_prompt
    
    def _create_general_analysis_prompt(self, data: Dict[str, Any]) -> Tuple[str, str]:
        """
        创建通用分析提示词
        """
        system_prompt = SYSTEM_PROMPT_TEMPLATE_ZH_GENERAL
        user_prompt = f"""
        学生数据:
        {json.dumps(data.get("data", {}), ensure_ascii=False, indent=2)}
        
        请根据学生数据进行通用分析，并根据回答规则生成分析报告。
        """
        return system_prompt, user_prompt
    
    def _parse_analysis_result(self, result: str, analysis_type: str) -> Dict[str, Any]:
        """
        解析LLM服务器返回的分析结果
        
        Args:
            result: LLM服务器返回的原始结果（字符串格式）
            analysis_type: 分析类型
            
        Returns:
            Dict[str, Any]: 解析后的分析结果
        """
        try:
            print(result)
            # 如果是报告类型，直接返回文本
            if analysis_type == "report":
                return {
                    "analysis_report": result
                }
            # 如果result是字符串，需要先解析成字典
            if isinstance(result, str):
                # 查找JSON代码块的开始和结束
                json_start = result.find("```json\n")
                json_end = result.find("```", json_start + 8) if json_start != -1 else -1
                
                if json_start != -1 and json_end != -1:
                    # 提取JSON字符串并解析
                    json_str = result[json_start + 8:json_end].strip()
                    result_dict = json.loads(json_str)
                else:
                    # 尝试直接解析整个字符串
                    result_dict = json.loads(result)
            else:
                # 如果已经是字典，直接使用
                result_dict = result
            
            
            # 提取评估指标和整体报告
            if isinstance(result_dict, dict):
                # 提取整体报告（如果有）
                overall_report = result_dict.pop("overall_report", "")
                
                return {
                    "evaluation_metrics": result_dict,
                    "analysis_report": overall_report
                }
            else:
                raise Exception("解析后的结果不是有效的字典格式")
        except Exception as e:
            print(f"解析分析结果失败: {str(e)}")
            mock_result = self._generate_mock_analysis(analysis_type)
            return mock_result
    
    def _generate_mock_analysis(self, analysis_type: str) -> Dict[str, Any]:
        """
        根据分析类型生成模拟的分析结果（当LLM服务器不可用时使用）
        
        Args:
            analysis_type: 分析类型
            
        Returns:
            Dict[str, Any]: 模拟的分析结果
        """
        if analysis_type == "behavior":
            return {
                "evaluation_metrics": {
                    "attention_rate": 0.85,
                    "emotion_management_level": 0.8,
                    "independent_learning_level": 0.8,
                    "self_reflection_level": 0.8,
                    "self_control_summary": "该学生具有良好的自我控制能力，能够很好地控制自己的情绪。"
                }
            }
        elif analysis_type == "knowledge":
            return {
                "evaluation_metrics": {
                    "progress_rate": 0.75,
                    "knowledge_master_level": 0.8,
                    "knowledge_weak_points": ["知识点1", "知识点2", "知识点3"],
                    "knowledge_improvement_suggestions": ["建议1", "建议2", "建议3"],
                    "knowledge_summary": "该学生对学科有良好的了解，能够很好地掌握基础知识。"
                }
            }
        elif analysis_type == "problem_solving":
            return {
                "evaluation_metrics": {
                    "identify_problem_level": 0.8,
                    "problem_solving_level": 0.8,
                    "innovation_level": 0.8,
                    "problem_solving_and_innovation_summary": "该学生具有良好的解决问题的能力，能够很好地解决问题。"
                }
            }
        elif analysis_type == "language":
            return {
                "evaluation_metrics": {
                    "language_expression_level": 0.8,
                    "reading_comprehension_level": 0.8,
                    "language_and_communication_summary": "该学生具有良好的语言表达能力，能够很好地表达自己。"
                }
            }
        elif analysis_type == "report":
            return {
                "analysis_report": "该学生具有良好的解决问题的能力，能够很好地解决问题。您可以使用此报告帮助学生改进学习。"
            }
        else:
            # 通用分析结果
            evaluation_metrics = {
                "attention_rate": 0.85,
                "emotion_management_level": 0.8,
                "independent_learning_level": 0.8,
                "self_reflection_level": 0.8,
                "self_control_summary": "该学生具有良好的自我控制能力，能够很好地控制自己的情绪。",
                "progress_rate": 0.75,
                "knowledge_master_level": 0.8,
                "knowledge_weak_points": ["知识点1", "知识点2", "知识点3"],
                "knowledge_improvement_suggestions": ["建议1", "建议2", "建议3"],
                "knowledge_summary": "该学生对学科有良好的了解，能够很好地掌握基础知识。",
                "identify_problem_level": 0.8,
                "problem_solving_level": 0.8,
                "innovation_level": 0.8,
                "problem_solving_and_innovation_summary": "该学生具有良好的解决问题的能力，能够很好地解决问题。",
                "language_expression_level": 0.8,
                "reading_comprehension_level": 0.8,
                "language_and_communication_summary": "该学生具有良好的语言表达能力，能够很好地表达自己。"
            }
            
            analysis_report = "该学生具有良好的解决问题的能力，能够很好地解决问题。您可以使用此报告帮助学生改进学习。"
            
            return {
                "evaluation_metrics": evaluation_metrics,
                "analysis_report": analysis_report
            } 