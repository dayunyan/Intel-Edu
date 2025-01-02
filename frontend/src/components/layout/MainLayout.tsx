'use client';

import { Layout, Menu, Avatar, Dropdown } from 'antd';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import {
  DashboardOutlined,
  UserOutlined,
  BookOutlined,
  BarChartOutlined,
  LogoutOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [userRole, setUserRole] = useState<string>('');
  const [userName, setUserName] = useState<string>('');

  useEffect(() => {
    setUserRole(localStorage.getItem('userRole') || '');
    setUserName(localStorage.getItem('userName') || '');
  }, []);

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: '数据大盘',
      onClick: () => router.push('/dashboard'),
    },
    ...(userRole !== 'STUDENT' ? [{
      key: 'students',
      icon: <UserOutlined />,
      label: '学生管理',
      onClick: () => router.push('/students'),
    }] : []),
    {
      key: 'courses',
      icon: <BookOutlined />,
      label: '课程管理',
      onClick: () => router.push('/courses'),
    },
    {
      key: 'analysis',
      icon: <BarChartOutlined />,
      label: '数据分析',
      onClick: () => router.push('/analysis'),
    },
  ];

  const handleLogout = () => {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT';
    localStorage.clear();
    router.push('/login');
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ padding: '0 24px', background: '#fff' }} className="flex justify-between items-center">
        <h1 className="text-xl font-bold">教育辅助系统</h1>
        <Dropdown menu={{
          items: [{
            key: 'logout',
            icon: <LogoutOutlined />,
            label: '退出登录',
            onClick: handleLogout
          }]
        }}>
          <div className="flex items-center cursor-pointer">
            <Avatar icon={<UserOutlined />} className="mr-2" />
            <span>{userName}</span>
          </div>
        </Dropdown>
      </Header>
      <Layout>
        <Sider width={200} theme="light">
          <Menu
            mode="inline"
            defaultSelectedKeys={['dashboard']}
            items={menuItems}
            className="h-full"
          />
        </Sider>
        <Content className="p-6 bg-gray-50">{children}</Content>
      </Layout>
    </Layout>
  );
}
