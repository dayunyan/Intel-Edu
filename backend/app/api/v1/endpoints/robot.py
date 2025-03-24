from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.chat import ChatService
from app.schemas.chat import MessageBase, ChatInDB
from app.models.agent import AIAgent
from datetime import datetime
import logging

router = APIRouter()

# 机器人语音交互API
@router.post("/voice_interaction", response_model=Dict[str, Any])
async def robot_voice_interaction(
    interaction_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """
    处理机器人的语音交互请求
    
    Args:
        interaction_data: 包含以下字段的字典
            - messages: 用户多轮对话
            - role_name: 角色名称
            
    Returns:
        Dict[str, Any]: 包含以下字段的字典
            - response: LLM的回复内容
            - role_name: 角色名称
    """
    try:
        messages = interaction_data.get("messages")
        role_name = interaction_data.get("role_name")
        print(messages)
        print(role_name)

        chat_service = ChatService(db)
        
        # 获取LLM回复
        response = await chat_service.get_robot_answer(chat_data=interaction_data)
        # response = {"content": f"你好，我是{role_name}，很高兴为你服务！是的，我是{role_name}，你有什么问题可以问我！"}
        # 添加角色信息
        result = {
            "response": response.get("content", ""),
            "role_name": role_name
        }
        
        return result
    except Exception as e:
        logging.error(f"机器人语音交互失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"机器人语音交互失败: {str(e)}"
        )

# 获取所有可用角色
@router.get("/available_roles", response_model=List[Dict[str, Any]])
async def get_available_roles(
    db: Session = Depends(get_db)
):
    """
    获取所有可用的角色信息
    
    Returns:
        List[Dict[str, Any]]: 角色信息列表
    """
    try:
        # 查询所有角色
        roles = db.query(AIAgent).all()
        
        # 构建返回数据
        result = []
        for role in roles:
            role_data = {
                "id": role.id,
                "name": role.name,
                "description": role.description,
                "avatar_url": role.avatar_url,
                "voice_settings": role.voice_settings
            }
            result.append(role_data)
        
        return result
    except Exception as e:
        logging.error(f"获取可用角色失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取可用角色失败: {str(e)}"
        ) 