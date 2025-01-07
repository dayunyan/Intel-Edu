export interface EvaluationMetric {
  [key: string]: number | string[] | string;
}

export interface AnalysisData {
  student_id: number
  analysis_type: string // 7days, 30days
  analysis_timestamp: Date
  analysis_report: string
  evaluation_metrics: EvaluationMetric
}

export interface AnalysisTrendData {
  [key: string]: AnalysisData[];
}