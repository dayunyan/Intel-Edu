'use client';

import { useState, useRef, useEffect } from 'react';
import { Input, Button, List, Avatar, Menu, Dropdown, message, Upload, Progress } from 'antd';
import { SendOutlined, RobotOutlined, UserOutlined, DownOutlined, PlusOutlined, AppstoreOutlined, HeartOutlined, PictureOutlined, SearchOutlined, EditOutlined, BookOutlined, BarsOutlined, RobotFilled, MehTwoTone, MessageOutlined, MehOutlined } from '@ant-design/icons';
import { chatApi } from '@/services/chat';
import type { Chat, Message } from '@/types/chat';
import router from 'next/router';
import { useRouter, useSearchParams } from 'next/navigation';
import type { RcFile, UploadFile } from 'antd/es/upload/interface';
import { Agent } from '@/types/agent';
import { agentApi } from '@/services/agent';
import { getFullImageUrl } from '@/types/agent';
import { ChatService } from '@/services/chatService';

export default function ChatPage() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [inputValue, setInputValue] = useState('');
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const [isRecentConversationsOpen, setIsRecentConversationsOpen] = useState(false);
    const [currentChatId, setCurrentChatId] = useState<number | null>(null);
    const [loading, setLoading] = useState(false);
    const [chatHistory, setChatHistory] = useState<Chat[]>([]);
    const router = useRouter();
    const searchParams = useSearchParams();
    const [fileList, setFileList] = useState<UploadFile[]>([]);
    const [uploading, setUploading] = useState(false);
    const [agents, setAgents] = useState<Agent[]>([]);
    const [currentAgent, setCurrentAgent] = useState<Agent | null>(null);

    const filterMessages = (msgs: Message[]) => {
        return msgs.filter(msg => msg.role!== 'system');
    };
    // 抽取的聊天服务
    const chatService = new ChatService({
        setCurrentAgent,
        setCurrentChatId,
        setMessages,
        setLoading,
        filterMessages
    });

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

    useEffect(() => {
        const fetchAgents = async () => {
          try {
            const studentId = parseInt(localStorage.getItem('userId') || '0');
            const response = await agentApi.getAgents(studentId);
            setAgents(response.data);
          } catch (error) {
            message.error('获取智能体列表失败');
          }
        };
        
        fetchAgents();
      }, []);
      
    // 初始化页面
    useEffect(() => {
        const agentId = searchParams.get('agentId');
        const chatId = searchParams.get('chatId');
        chatService.initializeChat(agentId, chatId);
    }, [searchParams]);

    // 选择智能体
    const selectAgent = async (agentId: number) => {
        await chatService.selectAgent(agentId);
    };

    // 开始新对话
    const startNewChat = async () => {
        if (currentAgent) {
            await chatService.createNewChat(currentAgent.id);
        }
    };

    const loadHistoryChat = async (chatId: number) => {
        await chatService.loadHistoryChat(chatId);
    };

    const sendMessage = async () => {
        if ((!inputValue.trim() && fileList.length === 0) || !currentChatId) return;

        try {
            setLoading(true);
            const newMessage: Message = {
                timestamp: new Date().toISOString(),
                role: 'user',
                content: inputValue.trim(),
                images: fileList
                    .filter(file => file.status === 'done')
                    .map(file => ({
                        url: file.url!,
                        filename: file.name
                    }))
            };

            const response = await chatApi.sendMessage(currentChatId, newMessage);
            setMessages([...messages, newMessage, response.data]);
            setInputValue('');
            setFileList([]); // 清空已上传的图片列表
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
            onClick: async () => {
                await router.push('/chat/history');
            }
        });

    const mainMenuItems = [
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
                        icon={<MessageOutlined />}
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
              <Dropdown
                menu={{
                  items: [
                    {
                      key: 'createAgent',
                      icon: <div style={{
                        width: '16px',
                        height: '16px',
                        backgroundColor: '#a0a0a0',
                        borderRadius: '12px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center'
                      }}>
                        <PlusOutlined style={{ color: '#fff' }} />
                      </div>,
                      label: '创建智能体',
                      onClick: () => router.push('/agent/create')
                    },
                    ...(agents?.slice(0, 5).map(agent => ({
                      key: agent.id.toString(),
                      icon: <Avatar 
                        src={getFullImageUrl(agent.avatar_url)} 
                        size={24}
                        style={{
                          objectFit: 'cover',
                          backgroundColor: '#f0f0f0'
                        }}
                      />,
                      label: agent.name,
                      onClick: () => selectAgent(agent.id)
                    })) || []),
                    {
                      key: 'viewAllAgents',
                      icon: <BarsOutlined />,
                      label: '查看全部...',
                      onClick: () => router.push('/agent/list')
                    }
                  ]
                }}
                trigger={['click']}
              >
                <Button 
                  type="link" 
                  icon={<RobotOutlined />}
                >
                  我的智能体
                </Button>
              </Dropdown>
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

    const handleUpload = async (file: File) => {
        const newFile: UploadFile = {
            uid: Date.now().toString(),
            name: file.name,
            status: 'uploading',
            percent: 0,
            originFileObj: file as RcFile,
        };

        setFileList(prev => [...prev, newFile]);

        try {
            const formData = new FormData();
            formData.append('file', file);

            const xhr = new XMLHttpRequest();
            xhr.open('POST', 'http://localhost:8000/api/v1/chat/upload-image', true);

            // 处理上传进度
            xhr.upload.onprogress = (event) => {
                if (event.lengthComputable) {
                    const percent = Math.round((event.loaded * 100) / event.total);
                    setFileList(prev => prev.map(item => {
                        if (item.uid === newFile.uid) {
                            return { ...item, percent };
                        }
                        return item;
                    }));
                }
            };

            // 处理上传完成
            xhr.onload = () => {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    setFileList(prev => prev.map(item => {
                        if (item.uid === newFile.uid) {
                            return { 
                                ...item, 
                                status: 'done', 
                                percent: 100,
                                url: response.url 
                            };
                        }
                        return item;
                    }));
                } else {
                    message.error(xhr.statusText);
                    throw new Error('上传失败');
                }
            };

            // 处理上传错误
            xhr.onerror = () => {
                setFileList(prev => prev.map(item => {
                    if (item.uid === newFile.uid) {
                        return { ...item, status: 'error' };
                    }
                    return item;
                }));
                message.error('上传图片失败');
            };

            xhr.send(formData);

        } catch (error) {
            setFileList(prev => prev.map(item => {
                if (item.uid === newFile.uid) {
                    return { ...item, status: 'error' };
                }
                return item;
            }));
            message.error('上传图片失败');
        }
    };

    const MessageItem = ({ message }: { message: Message }) => (
        <div style={{ 
            width: '100%',
            display: 'flex',
            justifyContent: message.role === 'user' ? 'flex-end' : 'flex-start',
            gap: '8px',
            marginBottom: '12px',
        }}>
            {message.role !== 'user' && (
                currentAgent ? (
                    <Avatar 
                        src={getFullImageUrl(currentAgent.avatar_url)}
                        style={{ flexShrink: 0 }}
                    />
                ) : (
                    <Avatar 
                        icon={<RobotOutlined />} 
                        style={{ backgroundColor: '#A6A6FA', flexShrink: 0 }}
                    />
                )
            )}
            <div style={{ 
                maxWidth: '70%',
                flexShrink: 1,
            }}>
                {message.images && message.images.length > 0 && (
                    <div style={{ 
                        display: 'flex', 
                        flexWrap: 'wrap', 
                        gap: '8px',
                        marginBottom: '8px' 
                    }}>
                        {message.images.map((img, index) => (
                            <img 
                                key={index}
                                src={img.url}
                                alt={img.filename}
                                style={{
                                    maxWidth: '200px',
                                    maxHeight: '200px',
                                    borderRadius: '8px'
                                }}
                            />
                        ))}
                    </div>
                )}
                <div style={{
                    padding: '12px',
                    backgroundColor: message.role === 'user' ? '#1890ff' : '#f0f2f5',
                    color: message.role === 'user' ? '#fff' : '#000',
                    borderRadius: '8px',
                    wordBreak: 'break-word'
                }}>
                    {message.content}
                </div>
            </div>
            {message.role === 'user' && (
                <Avatar 
                    icon={<UserOutlined />} 
                    style={{ backgroundColor: '#1677ff', flexShrink: 0 }}
                />
            )}
        </div>
    );

    const AgentInfo = () => (
        <div style={{
            position: 'absolute',
            left: '50%',
            transform: 'translateX(-50%)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
        }}>
            {currentAgent ? (
                <>
                    <Avatar 
                        src={getFullImageUrl(currentAgent.avatar_url)}
                        size={32}
                        style={{ objectFit: 'cover' }}
                    />
                    <span>{currentAgent.name}</span>
                </>
            ) : (
                <>
                    <Avatar 
                        icon={<RobotOutlined />}
                        size={32}
                        style={{ backgroundColor: '#A6A6FA' }}
                    />
                    <span>我不是AI</span>
                </>
            )}
        </div>
    )

    return (
        <div style={{ height: '95vh', display: 'flex', flexDirection: 'column' }}>
            {/* 头部区域 */}
            <div style={{ backgroundColor: '#f0f2f5', padding: '16px', borderBottom: '1px solid #e0e0e0', display: 'flex', justifyContent:'space-between', alignItems: 'center' }}>
                {/* 左侧菜单图标 */}
                <Menu
                    mode="horizontal"
                    selectable={false}
                    items={mainMenuItems}
                    style={{
                        background: 'transparent',
                        border: 'none',
                        position: 'relative'
                    }}
                />
                <AgentInfo />
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
                                <MessageItem message={msg} />
                            </List.Item>
                        )}
                    />
                    <div ref={messagesEndRef} />
                </div>
            </div>
            {/* 输入框和发送按钮区域 */}
            <div style={{ backgroundColor: '#f0f2f5', padding: '16px', borderTop: '1px solid #e0e0e0', display: 'flex', justifyContent: 'center' }}>
                <div style={{ maxWidth: '800px', width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', backgroundColor: '#fff', borderRadius: '8px', padding: '4px' }}>
                    {/* 图片预览区域 */}
                    {fileList.length > 0 && (
                        <div style={{ 
                            padding: '4px',
                            backgroundColor: '#fff',
                            borderRadius: '8px',
                            marginBottom: '4px',
                            display: 'flex',
                            flexWrap: 'wrap',
                            gap: '12px',
                            width: '100%',  // 确保容器占满宽度
                            justifyContent: 'flex-start'  // 左对齐
                        }}>
                            {fileList.map(file => (
                                <div key={file.uid} style={{ 
                                    position: 'relative',
                                    width: '50px',
                                    height: '50px',
                                    borderRadius: '8px',
                                    overflow: 'hidden'
                                }}>
                                    <img
                                        src={file.originFileObj ? URL.createObjectURL(file.originFileObj) : ''}
                                        alt={file.name}
                                        style={{
                                            width: '100%',
                                            height: '100%',
                                            objectFit: 'cover'
                                        }}
                                    />
                                    {/* 删除按钮 */}
                                    <div 
                                        style={{
                                            position: 'absolute',
                                            top: 0,
                                            right: 0,
                                            width: '16px',
                                            height: '16px',
                                            backgroundColor: 'rgba(0,0,0,0.5)',
                                            borderRadius: '0 8px 0 8px',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center',
                                            cursor: 'pointer',
                                            color: '#fff',
                                            fontSize: '12px',
                                            zIndex: 2
                                        }}
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setFileList(prev => prev.filter(item => item.uid !== file.uid));
                                        }}
                                    >
                                        ×
                                    </div>
                                    {file.status === 'uploading' && (
                                        <div style={{
                                            position: 'absolute',
                                            top: 0,
                                            left: 0,
                                            right: 0,
                                            bottom: 0,
                                            backgroundColor: 'rgba(0,0,0,0.5)',
                                            display: 'flex',
                                            alignItems: 'center',
                                            justifyContent: 'center'
                                        }}>
                                            <Progress 
                                                type="circle" 
                                                percent={file.percent} 
                                                width={30}
                                                strokeColor="#fff"
                                                trailColor="rgba(255,255,255,0.3)"
                                            />
                                        </div>
                                    )}
                                </div>
                            ))}
                        </div>
                    )}
                    <div style={{ maxWidth: '800px', width: '100%', display: 'flex', alignItems: 'center', backgroundColor: '#fff', borderRadius: '8px', padding: '4px' }}>
                        <Input.TextArea
                            value={inputValue}
                            onChange={e => setInputValue(e.target.value)}
                            onPressEnter={(e) => {
                                if (!e.shiftKey) {
                                    e.preventDefault();
                                    sendMessage();
                                }
                            }}
                            onPaste={(e) => {
                                const items = e.clipboardData.items;
                                for (let i = 0; i < items.length; i++) {
                                    const item = items[i];
                                    if (item.type.indexOf('image') !== -1) {
                                        e.preventDefault();
                                        const file = item.getAsFile();
                                        if (file) {
                                            handleUpload(file);
                                        }
                                    }
                                }
                            }}
                            placeholder="输入消息..."
                            autoSize={{ minRows: 1, maxRows: 6 }}
                            style={{ flex: 1, border: 'none', outline: 'none', padding: '8px' }}
                        />
                        <Upload
                            showUploadList={false}
                            beforeUpload={(file) => {
                                handleUpload(file as File);
                                return false;
                            }}
                        >
                            <Button type="text" icon={<PictureOutlined />} />
                        </Upload>
                        <Button type="primary" icon={<SendOutlined />} onClick={sendMessage}>
                            发送
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
}