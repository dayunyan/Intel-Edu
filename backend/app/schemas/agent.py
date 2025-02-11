from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class AgentBase(BaseModel):
    student_id: int
    name: str
    avatar_url: Optional[str] = None
    description: Optional[str] = None

class AgentCreate(AgentBase):
    pass

class AgentUpdate(AgentBase):
    id: int

class AgentInDB(AgentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True