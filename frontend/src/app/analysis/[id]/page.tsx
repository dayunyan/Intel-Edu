'use client';

import { useEffect, useState } from 'react';
import { Card, Row, Col, Spin, Alert, Tabs } from 'antd';
import { analysis } from '@/services/api';
import { MetricsChart } from '@/components/charts/MetricsChart';
import { MetricsPanel } from '@/components/analysis/MetricsPanel';
import type { AnalysisData, AnalysisTrendData, EvaluationMetric } from '@/types/analysis';
import { METRIC_GROUPS } from '@/constants/metrics';
const { TabPane } = Tabs;


export default function AnalysisPage({ params }: { params: { id: string } }) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<AnalysisData | null>(null);
  const [trendData, setTrendData] = useState<AnalysisTrendData | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [reportRes, trendRes] = await Promise.all([
          analysis.getAnalysisData(parseInt(params.id), 30),
          analysis.getAnalysisTrend(parseInt(params.id), 30)
        ]);
        setData(reportRes.data);
        
        // 处理趋势数据
        setTrendData(trendRes.data);
        
      } catch (error: any) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [params.id]);

  if (loading) return <Spin size="large" className="flex justify-center items-center min-h-screen" />;
  if (error) return <Alert type="error" message={error} className="m-4" />;
  if (!data) return null;

  return (
    <Card title={<span style={{ fontSize: '20px' }}>学生分析报告</span>} className="m-4">
      <Tabs defaultActiveKey="metrics">
        <TabPane tab="能力指标" key="metrics">
          {Object.entries(METRIC_GROUPS as Record<string, any>).map(([key, group]) => (
            <MetricsPanel
              key={key}
              title={group.title}
              metrics={Object.fromEntries(
                group.metrics.map((metric: string) => [
                  metric,
                  data.evaluation_metrics[metric as keyof EvaluationMetric]
                ])
              )}
              summary={data.evaluation_metrics[group.summary as keyof EvaluationMetric]?.toString()}
            />
          ))}
        </TabPane>

        <TabPane tab="趋势分析" key="trend">
          <Card title="能力指标趋势">
            <MetricsChart data={trendData as AnalysisTrendData} />
          </Card>
        </TabPane>
      </Tabs>

      <Card title="总体评价" className="mt-4">
        <div className="whitespace-pre-wrap">
          {data.analysis_report}
        </div>
      </Card>
    </Card>
  );
} 