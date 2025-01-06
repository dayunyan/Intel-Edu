import { Line } from '@ant-design/plots';
import { Alert, Spin } from 'antd';
import { METRIC_GROUPS } from '@/constants/metrics';
import { AnalysisData, EvaluationMetric, AnalysisTrendData } from '@/types/analysis';
    
interface MetricsChartProps {
  data: AnalysisTrendData;
  loading?: boolean;
}

export const MetricsChart = ({ data, loading }: MetricsChartProps) => {
  if (loading) return <Spin />;
  if (!data) return <Alert type="warning" message="暂无数据" />;

  // 获取所有数值类型的指标
  const allMetrics = Object.values(METRIC_GROUPS).flatMap(group => 
    group.metrics.filter(metric => 
      typeof Object.values(data)[0]?.[0]?.evaluation_metrics[metric] === 'number'
    )
  );

  // 处理数据为图表所需格式
  const chartData = Object.entries(data).flatMap(([date, dayData]) =>
    allMetrics.map(metric => ({
      date,
      metric,
      value: dayData[0]?.evaluation_metrics[metric] as number  // 选择每个日期中的第一个数据
    }))
  ).filter(item => item.value !== undefined);

  const config = {
    data: chartData,
    xField: 'date',
    yField: 'value',
    seriesField: 'metric',
    yAxis: {
      label: {
        formatter: (v: string) => `${(Number(v) * 100).toFixed(1)}%`,
      },
      max: 1,
      min: 0,
    },
    tooltip: {
      formatter: (datum: any) => ({
        name: datum.metric,
        value: `${(datum.value * 100).toFixed(1)}%`
      }),
    },
    legend: {
      position: 'top',
    },
    smooth: true,
    animation: {
      appear: {
        animation: 'path-in',
        duration: 1000,
      },
    },
  };

  return <Line {...config} />;
}; 