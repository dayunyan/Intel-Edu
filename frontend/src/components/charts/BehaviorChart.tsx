import { Line } from '@ant-design/plots';
import { Spin } from 'antd';

interface BehaviorChartProps {
  data: {
    date: string;
    value: number;
    type: string;
  }[];
  loading?: boolean;
}

export const BehaviorChart = ({ data, loading }: BehaviorChartProps) => {
  if (loading) return <Spin />;

  const config = {
    data,
    xField: 'date',
    yField: 'value',
    seriesField: 'type',
    legend: { position: 'top' },
    smooth: true,
  };

  return <Line {...config} />;
}; 