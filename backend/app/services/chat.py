import json
from sqlalchemy.orm import Session
from typing import Any, List, Dict
from datetime import datetime, timedelta
from app.models.chat import Chat
from app.services.student_data_service import StudentDataService
from fastapi import HTTPException
from app.core.formate import serialize_date
from sqlalchemy.orm.attributes import flag_modified
from app.services.file_service import FileService
from app.services.llm_service import LLMService
from app.models.agent import AIAgent
from app.models.user import Student

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()

    async def create_chat(self, student_id: int, agent_id: int=None) -> Chat:
        current_time = datetime.now()
        
        # 获取学生信息
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail=f"学生ID {student_id} 不存在")
        
        # 获取AI角色信息
        agent = None
        if agent_id:
            agent = self.db.query(AIAgent).filter(AIAgent.id == agent_id).first()
            if not agent:
                raise HTTPException(status_code=404, detail=f"AI角色ID {agent_id} 不存在")
        
        # 创建初始消息
        initial_messages = [
            dict(
                timestamp=serialize_date(current_time),
                role="system",
                content="你是一个教育辅导助手，你的任务是帮助学生学习和解答问题。"
            )
        ]
        
        # 获取AI响应
        student_info = {
            "id": student.id,
            "username": student.username,
            "full_name": student.full_name,
            "gender": student.gender.value if student.gender else None,
            "age": student.age,
            "grade": student.grade
        }
        
        role_name = "教育辅导助手"
        role_description = "教育辅导助手"
        if agent:
            role_name = agent.name or role_name
            role_description = agent.description or role_description
        
        answer = await self._get_response(initial_messages, role_name, role_description, student_info)
        initial_messages.append(
            dict(
                timestamp=serialize_date(answer['timestamp']),
                role="assistant",
                content=answer['content']
            )
        )
        
        # 创建数据库记录
        db_chat = Chat(
            student_id=student_id,
            agent_id=agent_id,
            timestamp=current_time,
            messages=initial_messages
        )
        
        self.db.add(db_chat)
        self.db.commit()
        self.db.refresh(db_chat)
        
        return db_chat
    
    def update_chat(self, chat: Chat) -> Chat:
        try:
            flag_modified(chat, "messages")
            
            self.db.commit()
            self.db.refresh(chat)
            return chat
        except Exception as e:
            self.db.rollback()
            print(f"更新失败的消息内容: {chat.messages} \n {str(e)}")
            raise RuntimeError(f"更新数据库失败：{str(e)}")
    
    def get_chat_by_id(self, chat_id: int) -> Chat:
        return self.db.query(Chat).filter(Chat.id == chat_id).first()

    def get_chats_by_student(self, student_id: int) -> List[Chat]:
        return self.db.query(Chat).filter(Chat.student_id == student_id).all()
    
    async def _get_response(self, messages: List[Dict[str, Any]], role_name:str, role_description: str, student_info: Dict[str, Any] = None) -> dict:
        try:
            # 获取最新的用户消息
            latest_message = messages[-1]
            
            # 调用LLM服务获取回复
            response = await self.llm_service.generate_chat_response(
                role_name=role_name,
                role_description=role_description,
                messages=messages,
                student_info=student_info
            )
            
            # 构建回复
            answer = {
                'timestamp': response.get('timestamp', datetime.now()),
                'content': response.get('content', '我是AI助手，很抱歉，我现在无法回答您的问题。请稍后再试。')
            }
            
            # 如果需要，可以在这里添加更多的处理逻辑
            
            return answer
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取AI响应失败: {str(e)}")
    
    async def get_answer(self, chat_id: int, chat_data: Dict[str, Any]) -> dict:
        # 获取chat_id对应的chat
        chat = self.get_chat_by_id(chat_id)
        
        # 获取学生信息
        student = self.db.query(Student).filter(Student.id == chat.student_id).first()
        student_info = None
        if student:
            student_info = {
                "id": student.id,
                "username": student.username,
                "full_name": student.full_name,
                "gender": student.gender.value if student.gender else None,
                "age": student.age,
                "grade": student.grade
            }
        
        # 获取AI角色信息
        role_name = "教育辅导助手"
        role_description = "教育辅导助手"
        if chat.agent_id:
            agent = self.db.query(AIAgent).filter(AIAgent.id == chat.agent_id).first()
            if agent:
                role_name = agent.name or role_name
                role_description = agent.description or role_description
        
        # 将chat_data添加到chat的messages中
        chat.messages.append(chat_data)
        
        # 大模型生成答案
        answer = await self._get_response(chat.messages, role_name, role_description, student_info)
        
        # 将答案添加到chat的messages中
        chat.timestamp = answer['timestamp']
        chat.messages.append(dict(
            timestamp=serialize_date(answer['timestamp']), 
            role="assistant", 
            content=answer['content']
        ))
        
        # 将chat更新到数据库
        chat = self.update_chat(chat)
        
        # 记录进度
        await self.record_progress(chat_id, chat.student_id, chat_data, answer)
        
        return chat.messages[-1]
    
    async def record_progress(self, chat_id: int, student_id: int, question: Dict[str, Any], answer: Dict[str, Any]) -> None:
        service = StudentDataService(self.db)
        progress = await service.record_question(chat_id, student_id, question, answer)
        return progress

    def get_chats_by_agent_and_student(self, agent_id: int, student_id: int) -> List[Chat]:
        chats = self.db.query(Chat).filter(
            Chat.agent_id == agent_id,
            Chat.student_id == student_id
        ).order_by(Chat.updated_at.desc()).all()
        
        # 确保所有对话都被正确加载
        for chat in chats:
            self.db.refresh(chat)
        
        return chats

    def delete_chat(self, chat_id: int) -> bool:
        try:
            chat = self.get_chat_by_id(chat_id)
            if chat:
                self.db.delete(chat)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"删除对话失败：{str(e)}")

    def delete_chats_by_agent(self, agent_id: int) -> bool:
        try:
            chats = self.db.query(Chat).filter(Chat.agent_id == agent_id).all()
            
            # 删除所有对话中的图片
            file_service = FileService()
            for chat in chats:
                for message in chat.messages:
                    if 'images' in message:
                        for image in message['images']:
                            file_service.delete_file(image['url'].replace('http://localhost:8000', ''))
                
                self.db.delete(chat)
                
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"删除智能体对话失败：{str(e)}")