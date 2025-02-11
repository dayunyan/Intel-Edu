import api from './api';
import type { Agent } from '@/types/agent';

export const agentApi = {
  // 创建智能体
  createAgent: (data: FormData) => 
    api.post<Agent>('/agent', data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }),
  
  // 获取学生的所有智能体
  getAgents: (studentId: number) => 
    api.get<Agent[]>(`/agent/student/${studentId}`),
  
  // 获取单个智能体详情
  getAgent: (agentId: number) => 
    api.get<Agent>(`/agent/${agentId}`),
  
  deleteAgent: (agentId: number) =>
    api.delete(`/agent/${agentId}`),
};
