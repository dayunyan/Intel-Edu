'use client';

import { useState } from 'react';
import { Form, Input, Button, message, Divider } from 'antd';
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
        localStorage.setItem('userRole', response.data.role);
        localStorage.setItem('userName', response.data.username);
        message.success('登录成功');
        router.push('/dashboard');
      } else {
        await auth.register({
          ...values,
          role: 'STUDENT'
        });
        message.success('注册成功，请登录');
        setIsLogin(true);
      }
    } catch (error) {
      message.error(isLogin ? '登录失败' : '注册失败');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="bg-white rounded-lg shadow-lg p-8 flex w-[800px]">
        <div className="w-1/2 flex items-center justify-center border-r border-gray-200">
          <Image
            src="/logo.png"
            alt="Logo"
            width={200}
            height={200}
            priority
          />
        </div>
        <div className="w-1/2 pl-8">
          <h1 className="text-2xl font-bold mb-6 text-center">
            {isLogin ? '登录' : '注册'}
          </h1>
          <Form form={form} onFinish={onFinish} layout="vertical">
            <Form.Item
              name="username"
              rules={[{ required: true, message: '请输入用户名' }]}
            >
              <Input placeholder="用户名" className="rounded-lg" />
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
                  <Input placeholder="邮箱" className="rounded-lg" />
                </Form.Item>
                <Form.Item
                  name="full_name"
                  rules={[{ required: true, message: '请输入姓名' }]}
                >
                  <Input placeholder="姓名" className="rounded-lg" />
                </Form.Item>
              </>
            )}
            <Form.Item
              name="password"
              rules={[{ required: true, message: '请输入密码' }]}
            >
              <Input.Password placeholder="密码" className="rounded-lg" />
            </Form.Item>
            <Form.Item>
              <Button type="primary" htmlType="submit" block className="rounded-lg">
                {isLogin ? '登录' : '注册'}
              </Button>
            </Form.Item>
          </Form>
          <div className="text-center">
            <Button type="link" onClick={() => setIsLogin(!isLogin)}>
              {isLogin ? '没有账号？立即注册' : '已有账号？立即登录'}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
} 