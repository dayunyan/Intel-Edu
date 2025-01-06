export interface BehaviorStatistic {
    behavior_type: string;
    count: number;
}

export interface ProgressStatistic {
    completeness_avg: number;
    duration_avg: number;
}

export interface MistakeStatistic {
    position: string;
    count: number;
}

export interface QuestionStatistic {
    position: string;
    count: number;
}

export interface StudentStatistic {
    behavior_count: number;
    progress_count: number;
    behavior_statistics: BehaviorStatistic;
    progress_statistics: ProgressStatistic;
    mistakes_statistics: MistakeStatistic;
    questions_statistics: QuestionStatistic;
}

// export interface BehaviorData {
//   behavior_trend: {
//     date: string;
//     value: number;
//     type: string;
//   }[];
// }

// export interface KnowledgeData {
//   subject: string;
//   mastery_level: number;
// }

// export interface AttentionData {
//   attention_rate: number;
// }

// export interface WeeklyProgressData {
//   week: string;
//   progress: number;
//   type: string;
// }

// export interface SubjectDistributionData {
//   subject: string;
//   value: number;
// }

// export interface ChartProps {
//   data: BehaviorData | KnowledgeData[] | AttentionData | WeeklyProgressData[] | SubjectDistributionData[];
//   loading?: boolean;
// } 