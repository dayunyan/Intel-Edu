'use client';
import { Layout, Menu, Avatar, Dropdown, message } from 'antd';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import {
  DashboardOutlined,
  UserOutlined,
  BookOutlined,
  BarChartOutlined,
  LogoutOutlined,
  RobotOutlined,
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
    ...(userRole !== 'teacher' ? [{
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: '数据大盘',
      onClick: () => router.push('/dashboard'),
    }] : []),
    ...(userRole !== 'student' ? [{
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
      onClick: () => {
        if (userRole === 'student') {
          const userId = localStorage.getItem('userId') || '';
          router.push(`/analysis/${userId}`);
        } else if (userRole === 'teacher') {
          message.info('请前往学生管理-选择一个学生查看分析');
        }
      },
    },
    {
      key: 'chat',
      icon: <RobotOutlined />,
      label: 'AI 助手',
      onClick: () => router.push('/chat'),
    },
  ];

  const handleLogout = () => {
    document.cookie = 'token=; path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT';
    localStorage.clear();
    router.push('/login');
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Header style={{ padding: '0 24px', background: '#fff', height: '64px' }} className="flex justify-between items-center">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', height: '100%' }}>
          <h1 style={{ marginRight: '16px', textAlign: 'center', margin:"0 0px"}} className="text-xl font-bold">教育辅助系统</h1>
          <Dropdown menu={{
            items: [{
              key: 'logout',
              icon: <LogoutOutlined />,
              label: '退出登录',
              onClick: handleLogout
            }]
          }}>
            <div style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <Avatar icon={<UserOutlined />} style={{ marginRight: '8px' }} />
              <span>{userName}</span>
            </div>
          </Dropdown>
        </div>
      </Header>
      <Layout>
        <Sider width={200} theme="light">
          <Menu
            mode="inline"
            defaultSelectedKeys={userRole !== 'teacher' ? ['dashboard'] : ['students']}
            items={menuItems}
            className="h-full"
          />
        </Sider>
        <Content className="p-6 bg-gray-50">{children}</Content>
      </Layout>
    </Layout>
  );
}