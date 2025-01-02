'use client';

import { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, List, Timeline } from 'antd';
import { UserOutlined, BookOutlined, ClockCircleOutlined } from '@ant-design/icons';

export default function DashboardPage() {
  const [userRole, setUserRole] = useState<string>('');

  useEffect(() => {
    setUserRole(localStorage.getItem('userRole') || '');
  }, []);

  const TeacherDashboard = () => (
    <>
      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card>
            <Statistic title="班级名称" value="高三一班" />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="总学生数" value={42} prefix={<UserOutlined />} />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="今日在线率" value={95.8} suffix="%" />
          </Card>
        </Col>
      </Row>
      {/* 添加更多教师特定内容 */}
    </>
  );

  const StudentDashboard = () => (
    <>
      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card>
            <Statistic title="今日学习时长" value={324} suffix="分钟" />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="待完成作业" value={3} suffix="项" />
          </Card>
        </Col>
        <Col span={8}>
          <Card>
            <Statistic title="今日专注度" value={88.5} suffix="%" />
          </Card>
        </Col>
      </Row>
      {/* 添加更多学生特定内容 */}
    </>
  );

  return (
    <div>
      <h2 className="text-2xl font-bold mb-6">数据总览</h2>
      {userRole === 'TEACHER' ? <TeacherDashboard /> : <StudentDashboard />}
    </div>
  );
} 