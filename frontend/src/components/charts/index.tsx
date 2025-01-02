'use client';

import { Line, Bar, Pie } from '@ant-design/plots';
import { Alert, Spin } from 'antd';
import { ChartProps, BehaviorData, KnowledgeData, AttentionData, WeeklyProgressData, SubjectDistributionData } from '@/types/charts';


export const KnowledgeChart = ({ data }: ChartProps) => {
  try {
    const formattedData = (data as KnowledgeData[]).map(item => ({
      subject: item.subject,
      value: item.mastery_level * 100,
    }));

    const config = {
      data: formattedData,
      xField: 'subject',
      yField: 'value',
      label: {
        position: 'middle',
        style: {
          fill: '#FFFFFF',
          opacity: 0.6,
        },
      },
    };

    return <Bar {...config} />;
  } catch (error) {
    return <Alert type="error" message="知识掌握度数据格式错误" />;
  }
};

export const AttentionChart = ({ data }: ChartProps) => {
  try {
    const attentionData = data as AttentionData;
    const chartData = [
      { type: '专注', value: attentionData.attention_rate * 100 },
      { type: '分心', value: (1 - attentionData.attention_rate) * 100 },
    ];

    const config = {
      data: chartData,
      angleField: 'value',
      colorField: 'type',
      radius: 0.8,
      label: {
        type: 'outer',
        content: '{name} {percentage}',
      },
    };

    return <Pie {...config} />;
  } catch (error) {
    return <Alert type="error" message="注意力数据格式错误" />;
  }
};

export const WeeklyProgressChart = ({ data }: ChartProps) => {
  try {
    const weeklyProgressData = data as WeeklyProgressData[];
    const config = {
      data: weeklyProgressData,
      xField: 'week',
      yField: 'progress',
      seriesField: 'type',
      isStack: true,
      legend: { position: 'top' },
    };
    return <Bar {...config} />;
  } catch (error) {
    return <Alert type="error" message="每周学习进度数据格式错误" />;
  }
};

export const SubjectDistributionChart = ({ data }: ChartProps) => {
  try {
    const subjectDistributionData = data as SubjectDistributionData[];
    const config = {
      data: subjectDistributionData,
      angleField: 'value',
      colorField: 'subject',
      radius: 0.8,
      label: {
        type: 'outer',
        content: '{name} {percentage}',
      },
    };
    return <Pie {...config} />;
  } catch (error) {
    return <Alert type="error" message="学科分布数据格式错误" />;
  }
};