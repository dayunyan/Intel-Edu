import os
import aiofiles
from fastapi import UploadFile
from datetime import datetime
from typing import Optional

class FileService:
    def __init__(self):
        self.avatar_dir = "uploads/avatars"
        self.chat_dir = "uploads/chat"
        os.makedirs(self.avatar_dir, exist_ok=True)
        os.makedirs(self.chat_dir, exist_ok=True)

    async def save_avatar(self, file: UploadFile) -> Optional[str]:
        return await self._save_file(file, self.avatar_dir, "avatar")

    async def save_chat_image(self, file: UploadFile) -> Optional[str]:
        return await self._save_file(file, self.chat_dir, "chat")

    async def _save_file(self, file: UploadFile, directory: str, prefix: str) -> Optional[str]:
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            extension = os.path.splitext(file.filename)[1]
            filename = f"{prefix}_{timestamp}{extension}"
            filepath = os.path.join(directory, filename)

            async with aiofiles.open(filepath, 'wb') as out_file:
                content = await file.read()
                await out_file.write(content)

            # 返回文件URL路径
            return f"/static/{directory.split('/')[-1]}/{filename}"
        except Exception as e:
            print(f"保存文件失败: {str(e)}")
            return None

    def delete_file(self, file_url: str) -> bool:
        try:
            # 从 URL 中提取文件路径
            file_path = file_url.replace('/static/', '')
            full_path = os.path.join(os.getcwd(), 'uploads', file_path)
            
            # 如果文件存在则删除
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
            return False
        except Exception as e:
            print(f"删除文件失败: {str(e)}")
            return False 