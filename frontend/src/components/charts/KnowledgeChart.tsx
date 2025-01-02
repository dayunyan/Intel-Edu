import { Line } from '@ant-design/plots';
import { Spin } from 'antd';

interface KnowledgeChartProps {
  data: {
    date: string;
    value: number;
    type: string;
  }[];
  loading?: boolean;
}

export const KnowledgeChart = ({ data, loading }: KnowledgeChartProps) => {
  if (loading) return <Spin />;

  const config = {
    data,
    xField: 'date',
    yField: 'value',
  };
};