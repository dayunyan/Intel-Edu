'use client';

import { useState, useRef, useEffect } from 'react';
import { Input, Button, List, Avatar, Menu, Dropdown, message } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined, DownOutlined, PlusOutlined, AppstoreOutlined, HeartOutlined, PictureOutlined, SearchOutlined, EditOutlined, BookOutlined } from '@ant-design/icons';
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

    const loadHistoryChat = async (chatId: number) => {
        try {
            setLoading(true);
            const response = await chatApi.getChat(chatId);
            setCurrentChatId(response.data.id);
            setMessages(response.data.messages);
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
            setMessages(response.data.messages);
            await fetchChatHistory();
        } catch (error) {
            console.error(error);
            message.error('创建对话失败');
        } finally {
            setLoading(false);
        }
    };
    
    const sendMessage = async () => {
        if (!inputValue.trim() || !currentChatId) return;
        
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

    const recentConversationsItems = (chatHistory || []).map(chat => {
        const firstUserMessage = chat.messages.find(msg => msg.role === 'user');
        // const firstUserMessage = chat.messages[0];
        return {
            key: chat.id.toString(),
            label: firstUserMessage?.content || '新对话',
            icon: <EditOutlined />,
            onClick: () => loadHistoryChat(chat.id)
        };
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
                <>
                    <Button type="link" icon={<DownOutlined />}>
                        最近对话
                    </Button>
                    <Menu>
                        {recentConversationsItems.length > 0 ? (
                            recentConversationsItems.map(item => (
                                <Menu.Item key={item.key} icon={item.icon} onClick={item.onClick}>
                                    {item.label}
                                </Menu.Item>
                            ))
                        ) : (
                            <Menu.Item disabled>暂无历史对话</Menu.Item>
                        )}
                    </Menu>
                </>
            ),
        },
        {
            key:'myAgents',
            label: (
                <Button type="link" icon={<AppstoreOutlined />}>
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
        <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
            {/* 头部区域 */}
            <div style={{ backgroundColor: '#f0f2f5', padding: '16px', borderBottom: '1px solid #e0e0e0', display: 'flex', justifyContent:'space-between', alignItems: 'center' }}>
                {/* 左侧菜单图标 */}
                <Dropdown overlay={() => (
                        <Menu items={mainMenuItems} onClick={toggleRecentConversations} />
                    )} placement="bottomLeft">
                    <div style={{ cursor: 'pointer' }}>
                        <AppstoreOutlined />
                    </div>
                </Dropdown>
                {/* 右侧新对话按钮 */}
                <Button type="primary" icon={<PlusOutlined />} onClick={startNewChat} loading={loading}>
                    新对话
                </Button>
            </div>
            {/* 消息展示区域 */}
            <div style={{ flex: 1, display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '16px' }}>
                <div style={{ maxWidth: '600px', width: '100%' }}>
                    <List
                        dataSource={messages}
                        renderItem={msg => (
                            <List.Item className={`flex border-0 ${msg.role === 'user'? 'justify-end' : 'justify-start'}`}>
                                <div className={`flex items-start gap-2 max-w-[70%] ${msg.role === 'user'? 'flex-row-reverse' : ''}`}>
                                    <Avatar icon={msg.role === 'user'? <UserOutlined /> : <RobotOutlined />} />
                                    <div className={`p-3 rounded-lg ${
                                        msg.role === 'user'? 'bg-blue-500 text-white' : 'bg-white shadow-sm'
                                        }`}>
                                        {msg.content}
                                    </div>
                                </div>
                            </List.Item>
                        )}
                    />
                    <div ref={messagesEndRef} />
                </div>
            </div>
            {/* 输入框和发送按钮区域 */}
            <div style={{ backgroundColor: '#f0f2f5', padding: '16px', borderTop: '1px solid #e0e0e0', display: 'flex', justifyContent: 'center' }}>
                <div style={{ maxWidth: '600px', width: '100%', display: 'flex', alignItems: 'center', backgroundColor: '#fff', borderRadius: '8px', padding: '4px' }}>
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