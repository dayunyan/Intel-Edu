'use client';

import { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Spin } from 'antd';
import { Pie, Column, Bar } from '@ant-design/plots';
import { studentData } from '@/services/api';
import type { StudentStatistic } from '@/types/charts';

export default function DashboardPage() {
  const [userRole, setUserRole] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [statistics, setStatistics] = useState<StudentStatistic | null>(null);

  useEffect(() => {
    setUserRole(localStorage.getItem('userRole') || '');
    fetchStudentData();
  }, []);

  const fetchStudentData = async () => {
    try {
      const studentId = parseInt(localStorage.getItem('userId') || '0');
      const response = await studentData.getStatistics(studentId, 30);
      setStatistics(response.data);
    } catch (error) {
      console.error('获取统计数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const StudentDashboard = () => {
    if (loading) return <Spin size="large" />;
    if (!statistics) return null;

    const behaviorData = Object.entries(statistics.behavior_statistics).map(([type, count]) => ({
      type,
      value: count,
    }));

    const mistakesData = Object.entries(statistics.mistakes_statistics).map(([key, count]) => ({
      subject: key,
      count,
    }));

    const questionsData = Object.entries(statistics.questions_statistics).map(([key, count]) => ({
      subject: key,
      count,
    }));

    const pieConfig = {
      appendPadding: 10,
      angleField: 'value',
      colorField: 'type',
      radius: 0.8,
      label: {
        text: 'value',
        position: 'outside',
      },
      interactions: [{ type: 'element-active' }],
    };

    const barConfig = {
      xField: 'subject',
      yField: 'count',
      colorField: 'subject',
      label: {
        position: 'inside',
        style: {
          fill: '#FFFFFF',
          opacity: 0.6,
        },
      },
    };

    const columnConfig = {
      xField: 'subject',
      yField: 'count',
      colorField: 'subject',
      label: {
        position: 'top',
        style: {
          fill: '#FFFFFF',
          opacity: 0.6,
        },
      },
    };

    return (
      <>
        <Row gutter={[16, 16]}>
          <Col span={8}>
            <Card>
              <Statistic 
                title="学习进度完成度" 
                value={statistics.progress_statistics.completeness_avg * 100} 
                suffix="%" 
                precision={1}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic 
                title="平均学习时长" 
                value={statistics.progress_statistics.duration_avg} 
                suffix="分钟"
                precision={0}
              />
            </Card>
          </Col>
          <Col span={8}>
            <Card>
              <Statistic 
                title="行为记录数" 
                value={statistics.behavior_count} 
                suffix="条"
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} className="mt-4">
          <Col span={12}>
            <Card title="行为类型分布">
              <Pie {...pieConfig} data={behaviorData} />
            </Card>
          </Col>
          <Col span={12}>
            <Card title="错题分布">
              <Bar {...barConfig} data={mistakesData} />
            </Card>
          </Col>
        </Row>

        <Row gutter={[16, 16]} className="mt-4">
          <Col span={24}>
            <Card title="提问分布">
              <Column {...columnConfig} data={questionsData} />
            </Card>
          </Col>
        </Row>
      </>
    );
  };

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
            <Statistic title="总学生数" value={42} />
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

  return (
    <Card title={<span style={{ fontSize: '20px' }}>数据总览</span>} className="m-4">
      {userRole === 'TEACHER' ? <TeacherDashboard /> : <StudentDashboard />}
    </Card>
  );
} 