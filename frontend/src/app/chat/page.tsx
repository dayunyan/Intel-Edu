'use client';

import { useState, useRef, useEffect } from 'react';
import { Input, Button, List, Avatar, Menu, Dropdown, message } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined, DownOutlined, PlusOutlined, AppstoreOutlined, HeartOutlined, PictureOutlined, SearchOutlined, EditOutlined, BookOutlined, BarsOutlined, RobotFilled, MehTwoTone } from '@ant-design/icons';
import { chatApi } from '@/services/chat';
import type { Chat, Message } from '@/types/chat';

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [isRecentConversationsOpen, setIsRecentConversationsOpen] = useState(false);
    const [currentChatId, setCurrentChatId] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [chatHistory, setChatHistory] = useState<Chat[]>([]);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const fetchChatHistory = async () => {
        try {
            const studentId = parseInt(localStorage.getItem('userId') || '0');
            const response = await chatApi.getHistory(studentId);
            setChatHistory(response.data);
        } catch (error) {
            message.error('获取历史对话失败');
        }
    };

    useEffect(() => {
        fetchChatHistory();
    }, []);

    const filterMessages = (msgs: Message[]) => {
        return msgs.filter(msg => msg.role!== 'system');
    };

    const loadHistoryChat = async (chatId: number) => {
        try {
            setLoading(true);
            const response = await chatApi.getChat(chatId);
            setCurrentChatId(response.data.id);
            setMessages(filterMessages(response.data.messages));
        } catch (error) {
            message.error('加载对话失败');
        } finally {
            setLoading(false);
        }
    };

    const startNewChat = async () => {
        try {
            setLoading(true);
            const studentId = parseInt(localStorage.getItem('userId') || '0');
            const response = await chatApi.startChat(studentId);
            setCurrentChatId(response.data.id);
            setMessages(filterMessages(response.data.messages));
            await fetchChatHistory();
        } catch (error) {
            console.error(error);
            message.error('创建对话失败');
        } finally {
            setLoading(false);
        }
    };

    const sendMessage = async () => {
        if (!inputValue.trim() ||!currentChatId) return;

        try {
            setLoading(true);
            const newMessage: Message = {
                timestamp: new Date().toISOString(),
                role: 'user',
                content: inputValue.trim()
            };

            const response = await chatApi.sendMessage(currentChatId, newMessage);
            setMessages([...messages, newMessage, response.data]);
            setInputValue('');
        } catch (error) {
            message.error('发送消息失败');
        } finally {
            setLoading(false);
        }
    };

    const recentConversationsItems = (chatHistory || [])
        .sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime())
        .slice(0, 5)
        .map(chat => {
            const firstUserMessage = chat.messages.find(msg => msg.role === 'user');
            return {
                key: chat.id.toString(),
                label: firstUserMessage?.content || '新对话',
                icon: <EditOutlined />,
                onClick: () => loadHistoryChat(chat.id)
            };
        });


    recentConversationsItems.push({
        key: 'viewAll',
        label: '查看全部...',
        icon: <BarsOutlined />,
        onClick: () => {
            // TODO: 实现跳转到历史对话列表页面的功能
            // router.push('/chat/history');
            console.log('跳转到历史对话列表页面');
            return Promise.resolve();
        }
    });

    const mainMenuItems = [
        {
            key: 'newConversation',
            label: (
                <Button type="link" icon={<PlusOutlined />} onClick={startNewChat}>
                    新对话
                </Button>
            ),
        },
        {
            key:'recentConversations',
            label: (
                <Dropdown
                    menu={{
                        items: recentConversationsItems.length > 0 ? recentConversationsItems.map(item => ({
                            key: item.key,
                            icon: item.icon,
                            label: (
                                <div style={{ 
                                    maxWidth: '160px', 
                                    overflow: 'hidden',
                                    textOverflow: 'ellipsis',
                                    whiteSpace: 'nowrap'
                                }}>
                                    {item.label}
                                </div>
                            ),
                            onClick: item.onClick,
                        })) : [{
                            key: 'noHistory',
                            label: '暂无历史对话',
                            disabled: true,
                        }],
                    }}
                    trigger={['click']}
                >
                    <Button 
                        type="link" 
                        icon={<DownOutlined />}
                        onClick={(e) => {
                            e.stopPropagation();
                            toggleRecentConversations();
                        }}
                    >
                        最近对话
                    </Button>
                </Dropdown>
            ),
        },
        {
            key:'myAgents',
            label: (
                <Button type="link" icon={<MehTwoTone />}>
                    我的智能体
                </Button>
            ),
        },
        {
            key: 'favorites',
            label: (
                <Button type="link" icon={<HeartOutlined />}>
                    收藏夹
                </Button>
            ),
        },
    ];

    const toggleRecentConversations = () => {
        setIsRecentConversationsOpen(!isRecentConversationsOpen);
    };

    return (
        <div style={{ height: '95vh', display: 'flex', flexDirection: 'column' }}>
            {/* 头部区域 */}
            <div style={{ backgroundColor: '#f0f2f5', padding: '16px', borderBottom: '1px solid #e0e0e0', display: 'flex', justifyContent:'space-between', alignItems: 'center' }}>
                {/* 左侧菜单图标 */}
                <Dropdown 
                    menu={{ 
                        items: mainMenuItems, 
                        onClick: toggleRecentConversations 
                    }} 
                    placement="bottomLeft"
                    trigger={['click']}
                >
                    <div style={{ 
                        cursor: 'pointer',
                        width: '240px'  // 固定主菜单宽度
                    }}>
                        <AppstoreOutlined />
                    </div>
                </Dropdown>
                {/* 右侧新对话按钮 */}
                <Button type="primary" icon={<PlusOutlined />} onClick={startNewChat} loading={loading}>
                    新对话
                </Button>
            </div>
            {/* 消息展示区域 */}
            <div style={{ flex: 1, height: '100%', display: 'flex', justifyContent: 'center', padding: '16px', overflow: 'hidden' }}>
                <div style={{ 
                    maxWidth: '800px', 
                    width: '100%', 
                    height: '100%', 
                    overflowY: 'auto',
                    display: 'flex',
                    flexDirection: 'column'
                }}>
                    <List
                        dataSource={messages}
                        renderItem={msg => (
                            <List.Item style={{ border: 'none', padding: '8px 0' }}>
                                <div style={{ 
                                    width: '100%',
                                    display: 'flex',
                                    justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                                    gap: '8px'
                                }}>
                                    {msg.role !== 'user' && (
                                        <Avatar 
                                            icon={<RobotFilled />}
                                            style={{ 
                                                backgroundColor: '#A6A6FA',
                                                flexShrink: 0
                                            }}
                                        />
                                    )}
                                    <div style={{
                                        maxWidth: '70%',
                                        padding: '10px 12px',
                                        borderRadius: '4px',
                                        backgroundColor: msg.role === 'user' ? '#1677ff' : '#E6E6FA',
                                        color: msg.role === 'user' ? '#fff' : '#000',
                                        wordBreak: 'break-word'
                                    }}>
                                        {msg.content}
                                    </div>
                                    {msg.role === 'user' && (
                                        <Avatar 
                                            icon={<UserOutlined />}
                                            style={{ 
                                                backgroundColor: '#1677ff',
                                                flexShrink: 0
                                            }}
                                        />
                                    )}
                                </div>
                            </List.Item>
                        )}
                    />
                    <div ref={messagesEndRef} />
                </div>
            </div>
            {/* 输入框和发送按钮区域 */}
            <div style={{ backgroundColor: '#f0f2f5', padding: '16px', borderTop: '1px solid #e0e0e0', display: 'flex', justifyContent: 'center' }}>
                <div style={{ maxWidth: '800px', width: '100%', display: 'flex', alignItems: 'center', backgroundColor: '#fff', borderRadius: '8px', padding: '4px' }}>
                    <Input
                        value={inputValue}
                        onChange={e => setInputValue(e.target.value)}
                        onPressEnter={sendMessage}
                        placeholder="输入消息..."
                        style={{ flex: 1, border: 'none', outline: 'none', padding: '8px' }}
                    />
                    <Button type="text" icon={<PictureOutlined />} />
                    <Button type="primary" icon={<SendOutlined />} onClick={sendMessage}>
                        发送
                    </Button>
                </div>
            </div>
        </div>
    );
}