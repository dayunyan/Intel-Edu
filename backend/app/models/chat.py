from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, JSON, DateTime
from .base import Base, TimeStampMixin

""" 
JSON template for chat
[
    {
        "timestamp": "2024-10-08 10:00:00",
        "role": "user",
        "content": "1+1=?",
        "images": [
            {
                "url": "http://localhost:8000/uploads/20241008_100000.jpg",
                "filename": "20241008_100000.jpg"
            }
        ]
    },
    {
        "timestamp": "2024-10-08 10:00:00",
        "role": "assistant",
        "content": "2",
    }
]
"""

class Chat(Base, TimeStampMixin):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    agent_id = Column(Integer, ForeignKey("ai_agents.id"), default=None)
    timestamp = Column(DateTime)
    messages = Column(JSON)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "agent_id": self.agent_id,
            "timestamp": self.timestamp,
            "messages": self.messages,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
