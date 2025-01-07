import { Card, Row, Col, Statistic, Alert, List } from 'antd';

interface MetricsPanelProps {
  title: string;
  metrics: Record<string, number | string[]>;
  summary?: string;
}

export const MetricsPanel = ({ title, metrics, summary }: MetricsPanelProps) => {
  // 分离数值型指标和数组型指标
  const numberMetrics = Object.entries(metrics).filter(([_, value]) => typeof value === 'number');
  const arrayMetrics = Object.entries(metrics).filter(([_, value]) => Array.isArray(value));

  return (
    <Card title={title} className="mb-4">
      {/* 数值型指标展示 */}
      <Row gutter={[16, 16]}>
        {numberMetrics.map(([key, value]) => (
          <Col span={6} key={key}>
            <Card>
              <Statistic
                title={key}
                value={value as number * 100}
                suffix="%"
                precision={1}
              />
            </Card>
          </Col>
        ))}
      </Row>

      {/* 数组型指标展示 */}
      <div className="mt-6">
        {arrayMetrics.map(([key, value]) => (
          <div key={key} className="mt-4">
            <Alert
              type="info"
              message={key === 'knowledge_weak_points' ? '薄弱知识点' : '改进建议'}
              description={
                <List
                  size="small"
                  dataSource={value as string[]}
                  renderItem={(item) => (
                    <List.Item>
                      {key === 'knowledge_weak_points' ? '🔖 ' : '💡 '}
                      {item}
                    </List.Item>
                  )}
                />
              }
            />
          </div>
        ))}
      </div>

      {/* 总结展示 */}
      {summary && (
        <div className="mt-4 p-4 bg-gray-50 rounded">
          <p className="text-gray-600">{summary}</p>
        </div>
      )}
    </Card>
  );
}; 