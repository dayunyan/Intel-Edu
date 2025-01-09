'use client';

import { useEffect, useState } from 'react';
import { List, Avatar, Card, Button, message } from 'antd';
import { useRouter } from 'next/navigation';
import { chatApi } from '@/services/chat';
import type { Chat } from '@/types/chat';
import { RobotOutlined, ArrowLeftOutlined } from '@ant-design/icons';

export default function ChatHistoryPage() {
    const router = useRouter();
    const [chatHistory, setChatHistory] = useState<Chat[]>([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchChatHistory();
    }, []);

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

    const handleChatClick = (chatId: number) => {
        router.push(`/chat?id=${chatId}`);
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
                    return (
                        <Card 
                            style={{ marginBottom: '16px', cursor: 'pointer' }}
                            hoverable
                            onClick={() => handleChatClick(chat.id)}
                        >
                            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                                <Avatar icon={<RobotOutlined />} style={{ backgroundColor: '#1677ff' }} />
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
                        </Card>
                    );
                }}
            />
        </div>
    );
} 