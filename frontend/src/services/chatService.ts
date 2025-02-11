import { message } from 'antd';
import { chatApi } from './chat';
import { agentApi } from './agent';
import type { Message } from '@/types/chat';
import type { Agent } from '@/types/agent';

export class ChatService {
  constructor(private handlers: {
    setCurrentAgent: (agent: Agent | null) => void;
    setCurrentChatId: (id: number) => void;
    setMessages: (messages: Message[]) => void;
    setLoading: (loading: boolean) => void;
    filterMessages: (messages: Message[]) => void;
  }) {}

  async initializeChat(agentId: string | null, chatId: string | null) {
    try {
      if (agentId) {
        const agentResponse = await agentApi.getAgent(parseInt(agentId));
        this.handlers.setCurrentAgent(agentResponse.data);
      }
        
    if (chatId) {
        await this.loadHistoryChat(parseInt(chatId));
    } else {
        await this.createNewChat(parseInt(agentId));
    }
    } catch (error) {
      message.error('初始化对话失败');
    }
  }

  async selectAgent(agentId: number) {
    try {
      const response = await agentApi.getAgent(agentId);
      this.handlers.setCurrentAgent(response.data);
      await this.createNewChat(agentId);
    } catch (error) {
      message.error('选择智能体失败');
    }
  }

  async createNewChat(agentId: number | null) {
    const studentId = parseInt(localStorage.getItem('userId') || '0');
    const chatResponse = await chatApi.startChat(studentId, agentId);
    if (chatResponse.data.agent_id) {
        const agentResponse = await agentApi.getAgent(chatResponse.data.agent_id);
        this.handlers.setCurrentAgent(agentResponse.data);
    }
    this.handlers.setCurrentChatId(chatResponse.data.id);
    this.handlers.setMessages(this.handlers.filterMessages(chatResponse.data.messages));
  }

  async loadHistoryChat(chatId: number) {
    try {
      this.handlers.setLoading(true);
      const response = await chatApi.getChat(chatId);
      
      // 如果对话有关联的智能体，获取智能体信息
      if (response.data.agent_id) {
        const agentResponse = await agentApi.getAgent(response.data.agent_id);
        this.handlers.setCurrentAgent(agentResponse.data);
      }
      
      this.handlers.setCurrentChatId(response.data.id);
      this.handlers.setMessages(this.handlers.filterMessages(response.data.messages));
    } catch (error) {
      message.error('加载对话失败');
    } finally {
      this.handlers.setLoading(false);
    }
  }
} 