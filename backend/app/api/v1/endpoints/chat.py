from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.student_data_service import StudentDataService
from app.schemas.chat import ChatBase, ChatCreate, ChatUpdate, ChatInDB, MessageBase
from app.services.chat import ChatService
import aiofiles
import os

router = APIRouter()

#TODO: 需要添加角色选项
@router.post("/start/{student_id}", response_model=ChatInDB, status_code=status.HTTP_201_CREATED)
async def start_chat(
    student_id: int,
    db: Session = Depends(get_db)
):
    try:
        chat_service = ChatService(db)
        chat = chat_service.create_chat(student_id)
        return ChatInDB(**chat.to_dict())
    except Exception as e:
        print(e)
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
        chats = chat_service.get_chat_by_student_id(student_id)
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
        answer = chat_service.get_answer(chat_id, chat_data.model_dump())
        return MessageBase(**answer)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发送消息失败: {str(e)}"
        )

@router.get("/{chat_id}", response_model=ChatInDB)
def get_chat(
    chat_id: int,
    db: Session = Depends(get_db),
):
    chat_service = ChatService(db)
    chat = chat_service.get_chat_by_id(chat_id)
    return ChatInDB(**chat.to_dict())

# 在 router 定义下方添加配置
UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    try:
        # 生成唯一的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{timestamp}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, new_filename)
        
        # 异步写入文件
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
            
        # 返回文件访问路径
        return {
            "url": f"http://localhost:8000/uploads/{new_filename}",  # 修改为你的实际域名和端口
            "filename": new_filename
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传图片失败: {str(e)}"
        )