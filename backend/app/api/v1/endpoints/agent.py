from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.agent import AIAgent
from app.schemas.agent import AgentCreate, AgentUpdate, AgentInDB
import aiofiles
import os
from app.services.file_service import FileService
from app.services.chat import ChatService

router = APIRouter()

# 创建智能体的API接口
@router.post("/", response_model=AgentInDB, status_code=status.HTTP_201_CREATED)
async def create_agent(
    student_id: int = Form(...),
    name: str = Form(...),
    description: str = Form(...),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        avatar_url = None
        if avatar:
            file_service = FileService()
            avatar_url = await file_service.save_avatar(avatar)

        new_agent = AIAgent(
            student_id=student_id,
            name=name,
            description=description,
            avatar_url=avatar_url
        )
        
        db.add(new_agent)
        db.commit()
        db.refresh(new_agent)
        
        return AgentInDB(**new_agent.to_dict())
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建智能体失败: {str(e)}"
        )

# 获取所有智能体的API接口
@router.get("/", response_model=List[AgentInDB])
def get_agents(
    db: Session = Depends(get_db)
):
    agents = db.query(AIAgent).all()
    return [AgentInDB(**agent.to_dict()) for agent in agents]

# 获取单个智能体的API接口
@router.get("/{agent_id}", response_model=AgentInDB)
def get_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    agent = db.query(AIAgent).filter(AIAgent.id == agent_id).first()
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    return AgentInDB(**agent.to_dict())

# 获取学生的所有智能体
@router.get("/student/{student_id}", response_model=List[AgentInDB])
def get_student_agents(
    student_id: int,
    db: Session = Depends(get_db)
):
    agents = db.query(AIAgent).filter(AIAgent.student_id == student_id).all()
    return [AgentInDB(**agent.to_dict()) for agent in agents]

# 删除智能体的API接口
@router.delete("/{agent_id}", status_code=status.HTTP_200_OK)
def delete_agent(
    agent_id: int,
    db: Session = Depends(get_db)
):
    try:
        # 先删除该智能体的所有对话
        chat_service = ChatService(db)
        chat_service.delete_chats_by_agent(agent_id)
        
        # 删除智能体
        agent = db.query(AIAgent).filter(AIAgent.id == agent_id).first()
        if not agent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="智能体不存在"
            )
            
        # 如果有头像，删除头像文件
        if agent.avatar_url:
            file_service = FileService()
            file_service.delete_file(agent.avatar_url)
            
        db.delete(agent)
        db.commit()
        return {"message": "删除成功"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除智能体失败: {str(e)}"
        )
