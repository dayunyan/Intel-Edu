import json
from sqlalchemy.orm import Session
from typing import Any, List, Dict
from datetime import datetime, timedelta
from app.models.chat import Chat
from app.services.student_data_service import StudentDataService
from fastapi import HTTPException
from app.core.formate import serialize_date
from sqlalchemy.orm.attributes import flag_modified

class ChatService:
    def __init__(self, db: Session):
        self.db = db

    def create_chat(self, student_id: int) -> Chat:
        current_time = datetime.now()
        chat = Chat(
            student_id=student_id,
            timestamp=current_time,
            messages=[
                dict(
                    timestamp=serialize_date(current_time),
                    role="system",
                    content="You are a helpful assistant."
                )
            ]
        )
        
        # 获取AI响应
        answer = self._get_response(chat.messages)
        chat.messages.append(
            dict(
                timestamp=serialize_date(answer['timestamp']),
                role="assistant",
                content=answer['content']
            )
        )
        
        # 序列化消息列表中的所有时间戳
        serialized_messages = []
        for msg in chat.messages:
            serialized_messages.append({
                "timestamp": serialize_date(msg['timestamp']),
                "role": msg['role'],
                "content": msg['content']
            })
        
        # 创建数据库记录
        db_chat = Chat(
            student_id=chat.student_id,
            timestamp=chat.timestamp,
            messages=serialized_messages
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
            answer = {
                'timestamp': current_time,
                'subject': '数学',
                'book': '数学教材第3册',
                'chapter': '第3章',
                'section': '第2节',
                'content': '这是一条大模型生成的答案。。。'
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