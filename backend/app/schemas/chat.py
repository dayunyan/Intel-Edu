from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ImageInfo(BaseModel):
    url: str
    filename: str

class MessageBase(BaseModel):
    timestamp: str
    role: str
    content: str
    images: Optional[List[ImageInfo]] = None

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