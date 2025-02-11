'use client';

import { useState, useEffect } from 'react';
import { Avatar, List, Card, Empty, Modal, message, Button } from 'antd';
import { RobotOutlined, DeleteOutlined, ArrowLeftOutlined } from '@ant-design/icons';
import { agentApi } from '@/services/agent';
import { chatApi } from '@/services/chat';
import { useRouter } from 'next/navigation';
import { getFullImageUrl } from '@/types/agent';
import type { Agent } from '@/types/agent';
import type { Chat, Message } from '@/types/chat';
import styles from './styles.module.css';

export default function AgentListPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [activeAgent, setActiveAgent] = useState<Agent | null>(null);
  const [agentChats, setAgentChats] = useState<{[key: number]: Chat[]}>({});
  const router = useRouter();

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const studentId = parseInt(localStorage.getItem('userId') || '0');
        const response = await agentApi.getAgents(studentId);
        setAgents(response.data);
      } catch (error) {
        console.error('获取智能体列表失败', error);
      }
    };
    fetchAgents();
  }, []);

  useEffect(() => {
    const fetchAgentChats = async (agentId: number) => {
      try {
        const studentId = parseInt(localStorage.getItem('userId') || '0');
        const response = await chatApi.getAgentChats(studentId, agentId);
        setAgentChats(prev => ({
          ...prev,
          [agentId]: response.data
        }));
      } catch (error) {
        console.error('获取智能体对话记录失败', error);
      }
    };

    if (activeAgent) {
      fetchAgentChats(activeAgent.id);
    }
  }, [activeAgent]);

  const startNewChat = async (agentId: number) => {
    const studentId = parseInt(localStorage.getItem('userId') || '0');
    try {
      const response = await chatApi.startChat(studentId, agentId);
      router.push(`/chat?chatId=${response.data.id}&agentId=${agentId}`);
    } catch (error) {
      console.error('创建新对话失败', error);
    }
  };

  const goToChat = (chatId: number, agentId: number) => {
    router.push(`/chat?chatId=${chatId}&agentId=${agentId}`);
  };

  const handleMouseEnter = (agent: Agent) => {
    setActiveAgent(agent);
  };

  const handleMouseLeave = (e: React.MouseEvent) => {
    const chatCard = document.querySelector(`.${styles.chatCard}`);
    if (chatCard && !chatCard.contains(e.relatedTarget as Node)) {
      setActiveAgent(null);
    }
  };

  const handleDeleteAgent = async (agentId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    Modal.confirm({
      title: '确认删除',
      content: '删除智能体将同时删除其所有对话记录，确定要删除吗？',
      okText: '确定',
      cancelText: '取消',
      okButtonProps: { danger: true },
      onOk: async () => {
        try {
          await agentApi.deleteAgent(agentId);
          setAgents(agents.filter(agent => agent.id !== agentId));
          message.success('删除成功');
        } catch (error) {
          message.error('删除失败');
        }
      }
    });
  };

  const handleDeleteChat = async (chatId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这条对话记录吗？',
      okText: '确定',
      cancelText: '取消',
      okButtonProps: { danger: true },
      onOk: async () => {
        try {
          await chatApi.deleteChat(chatId);
          if (activeAgent) {
            setAgentChats(prev => ({
              ...prev,
              [activeAgent.id]: prev[activeAgent.id].filter(chat => chat.id !== chatId)
            }));
          }
          message.success('删除成功');
        } catch (error) {
          message.error('删除失败');
        }
      }
    });
  };

  const getFirstUserMessage = (messages: Message[]): string => {
    const firstUserMessage = messages.find(msg => msg.role === 'user');
    if (!firstUserMessage) return '新对话';
    return firstUserMessage.content;
  };

  return (
    <div className={styles.container}>
      <div className={styles.agentList}>
        <div style={{ display: 'flex', alignItems: 'center', marginBottom: '24px', position: 'relative' }}>
          <Button 
            icon={<ArrowLeftOutlined />} 
            onClick={() => router.back()}
            style={{ position: 'absolute', left: 0 }}
          >
            返回
          </Button>
          <div className={styles.agentListTitle} style={{ margin: '0 auto' }}>我的智能体</div>
        </div>
        <List
          dataSource={agents}
          renderItem={agent => (
            <List.Item
              className={styles.agentItem}
              onClick={() => startNewChat(agent.id)}
              onMouseEnter={() => handleMouseEnter(agent)}
              onMouseLeave={handleMouseLeave}
              actions={[
                <DeleteOutlined
                  key="delete"
                  onClick={(e) => handleDeleteAgent(agent.id, e)}
                  style={{ 
                    fontSize: '24px', 
                    color: '#ff4d4f',
                    backgroundColor: 'rgba(255, 77, 79, 0.1)',
                    padding: '8px',
                    borderRadius: '50%'
                  }}
                />
              ]}
            >
              <List.Item.Meta
                avatar={
                  <Avatar
                    size={48}
                    src={getFullImageUrl(agent.avatar_url)}
                    icon={!agent.avatar_url && <RobotOutlined />}
                  />
                }
                title={agent.name}
                description={agent.description}
              />
            </List.Item>
          )}
        />
      </div>
      <div className={styles.chatList}>
        {activeAgent && (
          <Card 
            title={`${activeAgent.name}的对话记录`}
            className={styles.chatCard}
            onMouseEnter={() => setActiveAgent(activeAgent)}
            onMouseLeave={() => setActiveAgent(null)}
          >
            {agentChats[activeAgent.id]?.length ? (
              <List
                dataSource={agentChats[activeAgent.id]}
                renderItem={chat => (
                  <List.Item
                    className={styles.chatItem}
                    onClick={() => goToChat(chat.id, activeAgent.id)}
                    actions={[
                      <DeleteOutlined
                        key="delete"
                        onClick={(e) => handleDeleteChat(chat.id, e)}
                        style={{ 
                          fontSize: '24px', 
                          color: '#ff4d4f',
                          backgroundColor: 'rgba(255, 77, 79, 0.1)',
                          padding: '8px',
                          borderRadius: '50%'
                        }}
                      />
                    ]}
                  >
                    <List.Item.Meta
                      title={getFirstUserMessage(chat.messages)}
                      description={new Date(chat.timestamp).toLocaleString()}
                      style={{
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap'
                      }}
                    />
                  </List.Item>
                )}
              />
            ) : (
              <Empty description="暂无对话记录" />
            )}
          </Card>
        )}
      </div>
    </div>
  );
} 