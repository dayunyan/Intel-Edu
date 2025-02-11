from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base, TimeStampMixin


class AIAgent(Base, TimeStampMixin):
    __tablename__ = 'ai_agents'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    name = Column(String, nullable=False)  # 智能体名称
    avatar_url = Column(String)  # 头像链接
    description = Column(String)  # 描述文本，包含角色、语气、性格等设定

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "avatar_url": self.avatar_url,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
