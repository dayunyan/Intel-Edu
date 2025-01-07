'use client';
import { useState } from 'react';
import { Form, Input, Button, message, Select } from 'antd';
import { useRouter } from 'next/navigation';
import { auth } from '@/services/api';
import Image from 'next/image';

export default function LoginPage() {
    const [form] = Form.useForm();
    const router = useRouter();
    const [isLogin, setIsLogin] = useState(true);


    const onFinish = async (values: any) => {
        try {
            if (isLogin) {
                const response = await auth.login(values.username, values.password);
                document.cookie = `token=${response.data.access_token}; path=/`;
                localStorage.setItem('userId', response.data.id);
                localStorage.setItem('userRole', response.data.role);
                localStorage.setItem('userName', response.data.username);
                message.success('登录成功');
                router.push(response.data.role === 'teacher' ? '/students' : '/dashboard');
            } else {
                await auth.register({
                  ...values,
                  role: values.role.toUpperCase()
                });
                message.success('注册成功，请登录');
                setIsLogin(true);
            }
        } catch (error: any) {
            message.error(`${isLogin? '登录失败' : '注册失败'}: ${error.response.data.detail}`);
        }
    };

    return (
        <div style={{
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            backgroundColor: '#f5f7fa'
        }}>
            {/* 整体圆角矩形卡片容器 */}
            <div style={{
                backgroundColor: 'white',
                borderRadius: '24px',
                boxShadow: '0 10px 25px rgba(0, 0, 0, 0.05)',
                padding: '40px',
                maxWidth: '800px',
                width: '90%'
            }}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    gap: '40px'
                }}>
                    {/* 左侧 Logo 区域 */}
                    <div style={{
                        width: '25%',
                        display: 'flex',
                        justifyContent: 'center',
                        alignItems: 'center',
                        padding: '20px'
                    }}>
                        <div style={{ 
                            position: 'relative',
                            width: '80px',
                            height: '80px'
                        }}>
                            <Image
                                src="/logo.png"
                                alt="Logo"
                                width={80}
                                height={80}
                                style={{ 
                                    objectFit: 'contain',
                                }}
                            />
                        </div>
                    </div>
                    {/* 右侧表单区域 */}
                    <div style={{ 
                        width: '70%',
                        padding: '20px'
                    }}>
                        <h1 style={{
                            fontSize: '20px',
                            fontWeight: 'bold',
                            marginBottom: '20px',
                            textAlign: 'center',
                            color: '#333'
                        }}>
                            {isLogin? '欢迎登录' : '用户注册'}
                        </h1>
                        <Form
                            form={form}
                            onFinish={onFinish}
                            layout="vertical"
                        >
                            <Form.Item
                                name="username"
                                rules={[{ required: true, message: '请输入用户名' }]}
                            >
                                <Input placeholder="用户名" style={{
                                    borderRadius: '12px',
                                    height: '45px',
                                    border: '1px solid #e2e8f0',
                                    backgroundColor: '#f8fafc'
                                }} />
                            </Form.Item>

                            {!isLogin && (
                                <>
                                    <Form.Item
                                        name="email"
                                        rules={[
                                            { required: true, message: '请输入邮箱' },
                                            { type: 'email', message: '请输入有效的邮箱地址' }
                                        ]}
                                    >
                                        <Input placeholder="邮箱" style={{
                                            borderRadius: '8px',
                                            height: '40px',
                                            border: '1px solid #ccc',
                                            backgroundColor: '#f8f8f8'
                                        }} />
                                    </Form.Item>
                                    <Form.Item
                                        name="full_name"
                                        rules={[{ required: true, message: '请输入姓名' }]}
                                    >
                                        <Input placeholder="姓名" style={{
                                            borderRadius: '8px',
                                            height: '40px',
                                            border: '1px solid #ccc',
                                            backgroundColor: '#f8f8f8'
                                        }} />
                                    </Form.Item>
                                    <Form.Item
                                        name="role"
                                        rules={[{ required: true, message: '请选择角色' }]}
                                    >
                                        <Select options={[{ label: '学生', value: 'STUDENT' }, { label: '教师', value: 'TEACHER' }]} />
                                    </Form.Item>
                                </>
                            )}

                            <Form.Item
                                name="password"
                                rules={[{ required: true, message: '请输入密码' }]}
                            >
                                <Input.Password placeholder="密码" style={{
                                    borderRadius: '8px',
                                    height: '40px',
                                    border: '1px solid #ccc',
                                    backgroundColor: '#f8f8f8'
                                }} />
                            </Form.Item>
                            {!isLogin && (
                              <Form.Item
                                  name="confirm_password"
                                  dependencies={['password']}
                                  rules={[
                                      { required: true, message: '请确认密码' },
                                      ({ getFieldValue }) => ({
                                          validator(_, value) {
                                              if (!value || getFieldValue('password') === value) {
                                                  return Promise.resolve();
                                              }
                                              return Promise.reject(new Error('确认密码不一致'));
                                          },
                                      }),
                                  ]}
                              >
                                  <Input.Password placeholder="确认密码" style={{
                                      borderRadius: '8px',
                                      height: '40px',
                                      border: '1px solid #ccc',
                                      backgroundColor: '#f8f8f8'
                                  }} />
                              </Form.Item>
                            )}

                            <Form.Item>
                                <Button
                                    type="primary"
                                    htmlType="submit"
                                    block
                                    style={{
                                        borderRadius: '12px',
                                        height: '45px',
                                        fontSize: '16px',
                                        fontWeight: '600',
                                        backgroundColor: '#3b82f6',
                                        border: 'none',
                                        boxShadow: '0 2px 4px rgba(59, 130, 246, 0.2)'
                                    }}
                                >
                                    {isLogin? '登录' : '注册'}
                                </Button>
                            </Form.Item>
                        </Form>

                        <div style={{
                            textAlign: 'center',
                            marginTop: '15px'
                        }}>
                            <Button
                                type="link"
                                onClick={() => setIsLogin(!isLogin)}
                                style={{
                                    fontSize: '14px',
                                    color: '#4299e1'
                                }}
                            >
                                {isLogin? '没有账号？立即注册' : '已有账号？立即登录'}
                            </Button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}