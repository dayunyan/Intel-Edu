'use client';

import { useEffect, useState, useCallback } from 'react';
import { Card, Row, Col, Spin, Alert, message, Descriptions, Statistic } from 'antd';
import { analysis } from '@/services/api';
import { BehaviorChart } from '@/components/charts/BehaviorChart';
import { KnowledgeChart } from '@/components/charts/KnowledgeChart';
import type { ReportAnalysisData } from '@/types/analysis';

export default function AnalysisPage({ params }: { params: { id: string } }) {
  const [loading, setLoading] = useState(true);
  const [data, setData] = useState<ReportAnalysisData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalysisData = useCallback(async () => {
    try {
      setLoading(true);
      const response = await analysis.getReportAnalysis(parseInt(params.id));
      setData(response.data);
      setError(null);
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || '获取数据失败';
      setError(errorMessage);
      message.error(errorMessage);
    } finally {
      setLoading(false);
    }
  }, [params.id]);

  useEffect(() => {
    fetchAnalysisData();
    // 设置定时刷新，每分钟更新一次数据
    const timer = setInterval(fetchAnalysisData, 60000);
    return () => clearInterval(timer);
  }, [fetchAnalysisData]);

  if (loading) return <Spin size="large" className="flex justify-center items-center min-h-screen" />;
  if (error) return <Alert type="error" message={error} className="m-4" />;
  if (!data) return null;

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-6">学生分析报告</h2>
      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card title="行为分析">
            <Row gutter={[16, 16]}>
              <Col span={6}>
                <Card>
                  <Statistic 
                    title="总学习时长" 
                    value={data.behavior_analysis.total_study_time} 
                    suffix="分钟"
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card>
                  <Statistic 
                    title="专注度" 
                    value={data.behavior_analysis.attention_rate * 100} 
                    suffix="%" 
                  />
                </Card>
              </Col>
              <Col span={6}>
                <Card>
                  <Statistic 
                    title="分心次数" 
                    value={data.behavior_analysis.distraction_count} 
                    suffix="次"
                  />
                </Card>
              </Col>
            </Row>
            <BehaviorChart data={data.behavior_analysis.behavior_trend} loading={loading} />
          </Card>
        </Col>

        <Col span={24}>
          <Card title="知识掌握分析">
            {data.knowledge_analysis.map((subject, index) => (
              <Card key={index} className="mb-4">
                <h3 className="text-lg font-bold mb-4">{subject.subject}</h3>
                <Row gutter={[16, 16]}>
                  <Col span={12}>
                    <KnowledgeChart data={subject.knowledge_trend} loading={loading} />
                  </Col>
                  <Col span={12}>
                    <Descriptions title="详细分析" column={1}>
                      <Descriptions.Item label="掌握程度">
                        {(subject.mastery_level * 100).toFixed(1)}%
                      </Descriptions.Item>
                      <Descriptions.Item label="薄弱点">
                        {subject.weak_points.join('、')}
                      </Descriptions.Item>
                      <Descriptions.Item label="改进建议">
                        {subject.improvement_suggestions.join('、')}
                      </Descriptions.Item>
                    </Descriptions>
                  </Col>
                </Row>
              </Card>
            ))}
          </Card>
        </Col>

        <Col span={24}>
          <Card title="总体评价">
            <Alert
              message="整体评价"
              description={data.overall_evaluation}
              type="info"
              showIcon
            />
            <div className="mt-4">
              <h4 className="font-bold mb-2">改进建议：</h4>
              <ul className="list-disc pl-5">
                {data.suggestions.map((suggestion, index) => (
                  <li key={index}>{suggestion}</li>
                ))}
              </ul>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
} 