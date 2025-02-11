'use client';

import { useEffect, useState } from 'react';
import { List, Avatar, Card, Button, message, Modal } from 'antd';
import { useRouter } from 'next/navigation';
import { chatApi } from '@/services/chat';
import { agentApi } from '@/services/agent';
import type { Chat } from '@/types/chat';
import type { Agent } from '@/types/agent';
import { RobotOutlined, ArrowLeftOutlined, DeleteOutlined } from '@ant-design/icons';
import { getFullImageUrl } from '@/types/agent';

export default function ChatHistoryPage() {
    const router = useRouter();
    const [chatHistory, setChatHistory] = useState<Chat[]>([]);
    const [loading, setLoading] = useState(false);
    const [agents, setAgents] = useState<{[key: number]: Agent}>({});

    useEffect(() => {
        fetchChatHistory();
        fetchAgents();
    }, []);

    const fetchAgents = async () => {
        try {
            const studentId = parseInt(localStorage.getItem('userId') || '0');
            const response = await agentApi.getAgents(studentId);
            const agentMap = response.data.reduce((acc: {[key: number]: Agent}, agent: Agent) => {
                acc[agent.id] = agent;
                return acc;
            }, {});
            setAgents(agentMap);
        } catch (error) {
            message.error('获取智能体列表失败');
        }
    };

    const fetchChatHistory = async () => {
        try {
            setLoading(true);
            const studentId = parseInt(localStorage.getItem('userId') || '0');
            const response = await chatApi.getHistory(studentId);
            // 按时间戳降序排序
            const sortedHistory = response.data.sort(
                (a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime()
            );
            setChatHistory(sortedHistory);
        } catch (error) {
            message.error('获取历史对话失败');
        } finally {
            setLoading(false);
        }
    };

    const handleChatClick = (chat: Chat) => {
        const agentId = chat.agent_id;
        router.push(`/chat?chatId=${chat.id}${agentId ? `&agentId=${agentId}` : ''}`);
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
                    setChatHistory(prev => prev.filter(chat => chat.id !== chatId));
                    message.success('删除成功');
                } catch (error) {
                    message.error('删除失败');
                }
            }
        });
    };

    return (
        <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
            <div style={{ marginBottom: '20px', display: 'flex', alignItems: 'center', gap: '12px' }}>
                <Button 
                    icon={<ArrowLeftOutlined />} 
                    onClick={() => router.push('/chat')}
                >
                    返回对话
                </Button>
                <h2 style={{ margin: 0 }}>历史对话</h2>
            </div>
            <List
                loading={loading}
                dataSource={chatHistory}
                renderItem={(chat) => {
                    const firstUserMessage = chat.messages.find(msg => msg.role === 'user');
                    const agent = chat.agent_id ? agents[chat.agent_id] : null;
                    return (
                        <Card 
                            style={{ marginBottom: '16px', cursor: 'pointer' }}
                            hoverable
                            onClick={() => handleChatClick(chat)}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', justifyContent: 'space-between' }}>
                                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1 }}>
                                    <Avatar
                                        size={48}
                                        src={agent?.avatar_url ? getFullImageUrl(agent.avatar_url) : undefined}
                                        icon={!agent?.avatar_url && <RobotOutlined />}
                                        style={{ backgroundColor: '#1890ff' }}
                                    />
                                    <div style={{ flex: 1 }}>
                                        <div style={{ 
                                            fontSize: '16px',
                                            whiteSpace: 'nowrap',
                                            overflow: 'hidden',
                                            textOverflow: 'ellipsis'
                                        }}>
                                            {firstUserMessage?.content || '新对话'}
                                        </div>
                                        <div style={{ fontSize: '12px', color: '#999' }}>
                                            {new Date(chat.timestamp).toLocaleString()}
                                        </div>
                                    </div>
                                </div>
                                <DeleteOutlined
                                    onClick={(e) => handleDeleteChat(chat.id, e)}
                                    style={{ 
                                        fontSize: '24px', 
                                        color: '#ff4d4f',
                                        backgroundColor: 'rgba(255, 77, 79, 0.1)',
                                        padding: '8px',
                                        borderRadius: '50%'
                                    }}
                                />
                            </div>
                        </Card>
                    );
                }}
            />
        </div>
    );
} 