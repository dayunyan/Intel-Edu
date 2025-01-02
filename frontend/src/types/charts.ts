export interface BehaviorData {
  behavior_trend: {
    date: string;
    value: number;
    type: string;
  }[];
}

export interface KnowledgeData {
  subject: string;
  mastery_level: number;
}

export interface AttentionData {
  attention_rate: number;
}

export interface WeeklyProgressData {
  week: string;
  progress: number;
  type: string;
}

export interface SubjectDistributionData {
  subject: string;
  value: number;
}

export interface ChartProps {
  data: BehaviorData | KnowledgeData[] | AttentionData | WeeklyProgressData[] | SubjectDistributionData[];
  loading?: boolean;
} 