import api from './api';
import type { Message, Chat } from '@/types/chat';

export const chatApi = {
  // 开始新对话
  startChat: (studentId: number, agentId?: number) => 
    api.post<Chat>(`/chat/start/${studentId}`, { agent_id: agentId }),
  
  // 发送消息
  sendMessage: (chatId: number, message: Message) =>
    api.post<Message>(`/chat/message/${chatId}`, message),
  
  // 获取历史对话
  getHistory: (studentId: number) =>
    api.get<Chat[]>(`/chat/history/${studentId}`),
  
  // 获取单个对话详情
  getChat: (chatId: number) =>
    api.get<Chat>(`/chat/${chatId}`),
  
  uploadImage: (formData: FormData) =>
    api.post('/chat/upload-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),

  // 获取智能体的对话记录
  getAgentChats: (studentId: number, agentId: number) =>
    api.get<Chat[]>(`/chat/agent/${agentId}/student/${studentId}`),

  deleteChat: (chatId: number) =>
    api.delete(`/chat/${chatId}`),
}; 