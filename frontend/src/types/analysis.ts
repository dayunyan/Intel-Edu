export interface AnalysisData {
  student_id: number;
  behavior_data: BehaviorData;
  knowledge_data: KnowledgeData[];
  attention_data: AttentionData;
  weekly_progress: WeeklyProgressData[];
  subject_distribution: SubjectDistributionData[];
}

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

export interface BehaviorAnalysis {
    total_study_time: number
    attention_rate: number
    distraction_count: number
    behavior_trend: {
        date: string
        value: number
        type: string
    }[]
}

export interface KnowledgeAnalysis {
    subject: string
    mastery_level: number
    weak_points: string[]
    improvement_suggestions: string[]
    knowledge_trend: {
        date: string
        value: number
        type: string
    }[]
}

export interface ReportAnalysisData {
    student_id: number
    report_date: string
    behavior_analysis: BehaviorAnalysis
    knowledge_analysis: KnowledgeAnalysis[]
    overall_evaluation: string
    suggestions: string[]
}