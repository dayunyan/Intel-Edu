from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Body
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.student_data_service import StudentDataService
from app.schemas.chat import ChatBase, ChatCreate, ChatUpdate, ChatInDB, MessageBase
from app.services.chat import ChatService
from app.services.file_service import FileService
import os

router = APIRouter()

#TODO: 需要添加角色选项
@router.post("/start/{student_id}", response_model=ChatInDB)
async def start_chat(
    student_id: int,
    chat_data: dict = Body(default={'agent_id': None}),
    db: Session = Depends(get_db)
):
    try:
        chat_service = ChatService(db)
        chat = await chat_service.create_chat(student_id, chat_data.get('agent_id'))
        return ChatInDB(**chat.to_dict())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建对话失败: {str(e)}"
        )

@router.get("/history/{student_id}", response_model=List[ChatInDB])
async def get_student_chat_history(
    student_id: int,
    db: Session = Depends(get_db)
):
    try:
        chat_service = ChatService(db)
        chats = chat_service.get_chats_by_student(student_id)
        if not chats:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="未找到该学生的对话记录"
            )
        return [ChatInDB(**chat.to_dict()) for chat in chats]
    except HTTPException as he:
        raise he
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取对话历史失败: {str(e)}"
        )

@router.post("/message/{chat_id}", response_model=MessageBase)
async def send_message(
    chat_id: int,
    chat_data: MessageBase,
    db: Session = Depends(get_db)
):
    try:
        chat_service = ChatService(db)
        message = await chat_service.get_answer(chat_id, chat_data.model_dump())
        return MessageBase(**message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送消息失败: {str(e)}"
        )

@router.get("/{chat_id}", response_model=ChatInDB)
async def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
):
    chat_service = ChatService(db)
    chat = chat_service.get_chat_by_id(chat_id)
    return ChatInDB(**chat.to_dict())

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        file_service = FileService()
        file_path = await file_service.save_file(file)
        
        # 获取服务器URL
        server_url = os.getenv("SERVER_URL", "http://localhost:8000")
        
        if not file_path:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="保存文件失败"
            )
            
        return {
            "url": f"{server_url}{file_path}",  # 修改为你的实际域名和端口
            "filename": os.path.basename(file_path)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传图片失败: {str(e)}"
        )

@router.get("/agent/{agent_id}/student/{student_id}", response_model=List[ChatInDB])
async def get_agent_chats(
    agent_id: int,
    student_id: int,
    db: Session = Depends(get_db)
):
    try:
        chat_service = ChatService(db)
        chats = chat_service.get_chats_by_agent_and_student(agent_id, student_id)
        return [ChatInDB(**chat.to_dict()) for chat in chats]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取智能体对话记录失败: {str(e)}"
        )

@router.delete("/{chat_id}", status_code=status.HTTP_200_OK)
async def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):
    try:
        chat_service = ChatService(db)
        chat_service.delete_chat(chat_id)
        return {"message": "对话已删除"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除对话失败: {str(e)}"
        )
