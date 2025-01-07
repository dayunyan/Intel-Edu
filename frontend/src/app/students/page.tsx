'use client';

import { useEffect, useState, useCallback } from 'react';
import { Table, Card, Button, Space, message, Alert, Tag } from 'antd';
import { students } from '@/services/api';
import Link from 'next/link';
import { StudentData } from '@/types/data';
import { ColumnType } from 'antd/es/table';

export default function StudentsPage() {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<StudentData[]>([]);
  const [error, setError] = useState<string | null>(null);

  const fetchStudents = useCallback(async () => {
    try {
      const response = await students.getAll();
      setData(response.data as StudentData[]);
      setError(null);
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || '获取学生列表失败';
      setError(errorMessage);
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchStudents();
    // 设置定时刷新，每30秒更新一次数据
    const timer = setInterval(fetchStudents, 30000);
    return () => clearInterval(timer);
  }, [fetchStudents]);

  const getGenderTag = (gender: string) => {
    const color = gender === 'MALE' ? 'blue' : 'pink';
    const text = gender === 'MALE' ? '男' : '女';
    return <Tag color={color}>{text}</Tag>;
  };

  const getGradeText = (grade: number) => {
    const gradeMap: { [key: number]: string } = {
      7: '初一',
      8: '初二',
      9: '初三'
    };
    return gradeMap[grade] || `${grade}年级`;
  };

  const columns = [
    {
      title: '姓名',
      dataIndex: 'full_name',
      key: 'full_name',
    },
    {
      title: '性别',
      dataIndex: 'gender',
      key: 'gender',
      render: (gender: string) => getGenderTag(gender),
    },
    {
      title: '年龄',
      dataIndex: 'age',
      key: 'age',
      sorter: (a: StudentData, b: StudentData) => a.age - b.age,
    },
    {
      title: '年级',
      dataIndex: 'grade',
      key: 'grade',
      render: (grade: number) => getGradeText(grade),
      filters: [
        { text: '初一', value: 7 },
        { text: '初二', value: 8 },
        { text: '初三', value: 9 },
      ],
      onFilter: (value: number, record: StudentData) => record.grade === value,
    },
    {
      title: '班级',
      dataIndex: 'class_name',
      key: 'class_name',
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: unknown, record: StudentData) => (
        <Space size="middle">
          <Link href={`/analysis/${record.id}`}>
            <Button type="primary">查看分析</Button>
          </Link>
          <Link href={`/students/${record.id}`}>
            <Button>详细信息</Button>
          </Link>
        </Space>
      ),
    },
  ];

  if (error) {
    return <Alert type="error" message={error} className="m-4" />;
  }

  return (
    <Card title={<span style={{ fontSize: '20px' }}>学生管理</span>} className="m-4">
      <Table<StudentData>
        columns={columns as ColumnType<StudentData>[]}
        dataSource={data}
        loading={loading}
        rowKey="id"
        pagination={{
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total) => `共 ${total} 条数据`,
        }}
      />
    </Card>
  );
} 