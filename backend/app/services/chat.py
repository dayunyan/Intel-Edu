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

class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, student_id: int, agent_id: int=None) -> Chat:
        current_time = datetime.now()
        
        # 创建初始消息
        initial_messages = [
            dict(
                timestamp=serialize_date(current_time),
                role="system",
                content="You are a helpful assistant."
            )
        ]
        
        # 获取AI响应
        answer = self._get_response(initial_messages)
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

    def get_chat_by_student_id(self, student_id: int) -> List[Chat]:
        return self.db.query(Chat).filter(Chat.student_id == student_id).all()
    
    def _get_response(self, messages: List[Dict[str, Any]]) -> dict:
        try:
            current_time = datetime.now()
            
            # 获取最新的用户消息
            latest_message = messages[-1]
            content = latest_message.get('content', '')
            images = latest_message.get('images', [])
            
            # 根据是否包含图片构建不同的提示词
            if images:
                image_urls = [img['url'] for img in images]
                prompt = f"用户发送了以下图片：{image_urls}\n并附带文本消息：{content}\n"
            else:
                prompt = f"用户发送了文本消息：{content}\n"
            
            # TODO: 调用实际的AI模型处理图文消息
            answer = {
                'timestamp': current_time,
                'subject': '数学',
                'book': '数学教材第3册',
                'chapter': '第3章',
                'section': '第2节',
                'content': f'这是一条处理了图片和文本的AI回答。收到的文本是：{content}' + 
                          (f'，收到的图片数量是：{len(images)}' if images else '')
            }
            return answer
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"获取AI响应失败: {str(e)}")
    
    def get_answer(self, chat_id: int, chat_data: Dict[str, Any]) -> dict:
        # 获取chat_id对应的chat
        chat = self.get_chat_by_id(chat_id)
        # 将chat_data添加到chat的messages中
        chat.messages.append(chat_data)
        # 大模型生成答案
        answer = self._get_response(chat.messages)
        # 将答案添加到chat的messages中
        chat.timestamp = answer['timestamp']
        chat.messages.append(dict(timestamp=serialize_date(answer['timestamp']), role="assistant", content=answer['content']))
        # 将chat更新到数据库
        chat = self.update_chat(chat)
        print(chat.messages)
        # 记录进度
        self.record_progress(chat_id, chat.student_id, chat_data, answer)
        
        return chat.messages[-1]
    
    def record_progress(self,chat_id: int,student_id: int, question: Dict[str, Any], answer: Dict[str, Any]) -> None:
        service = StudentDataService(self.db)
        progress = service.record_question(chat_id, student_id, question, answer)
        
        return

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