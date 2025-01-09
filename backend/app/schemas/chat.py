from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MessageBase(BaseModel):
    timestamp: str
    role: str
    content: str

class ChatBase(BaseModel):
    student_id: int
    timestamp: datetime
    messages: List[MessageBase]

class ChatCreate(ChatBase):
    pass

class ChatUpdate(ChatBase):
    id: int

class ChatInDB(ChatBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True