import api from './api';
import type { Message, Chat } from '@/types/chat';

export const chatApi = {
  // 开始新对话
  startChat: (studentId: number) => 
    api.post<Chat>(`/chat/start/${studentId}`),
  
  // 发送消息
  sendMessage: (chatId: number, message: Message) =>
    api.post<Message>(`/chat/message/${chatId}`, message),
  
  // 获取历史对话
  getHistory: (studentId: number) =>
    api.get<Chat[]>(`/chat/history/${studentId}`),
  
  // 获取单个对话详情
  getChat: (chatId: number) =>
    api.get<Chat>(`/chat/${chatId}`)
}; 