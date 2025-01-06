import { Card, Row, Col, Statistic } from 'antd';

interface MetricsPanelProps {
  title: string;
  metrics: Record<string, number>;
  summary?: string;
}

export const MetricsPanel = ({ title, metrics, summary }: MetricsPanelProps) => {
  return (
    <Card title={title} className="mb-4">
      <Row gutter={[16, 16]}>
        {Object.entries(metrics).map(([key, value]) => (
          <Col span={6} key={key}>
            <Card>
              <Statistic
                title={key}
                value={value * 100}
                suffix="%"
                precision={1}
              />
            </Card>
          </Col>
        ))}
      </Row>
      {summary && (
        <div className="mt-4 p-4 bg-gray-50 rounded">
          <p className="text-gray-600">{summary}</p>
        </div>
      )}
    </Card>
  );
}; 