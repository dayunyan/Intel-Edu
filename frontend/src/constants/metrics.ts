export const METRIC_GROUPS = {
  selfManagement: {
    title: '自我管理能力',
    metrics: ['attention_rate', 'emotion_management_level', 'independent_learning_level', 'self_reflection_level'],
    summary: 'self_control_summary'
  },
  knowledge: {
    title: '知识掌握',
    metrics: ['progress_rate', 'knowledge_master_level', 'knowledge_weak_points', 'knowledge_improvement_suggestions'], //"knowledge_weak_points": ["知识点1", "知识点2", "知识点3"],"knowledge_improvement_suggestions": ["建议1", "建议2", "建议3"],
    summary: 'knowledge_summary'
  },
  problemSolving: {
    title: '问题解决与创新',
    metrics: ['identify_problem_level', 'problem_solving_level', 'innovation_level'],
    summary: 'problem_solving_and_innovation_summary'
  },
  communication: {
    title: '语言与沟通',
    metrics: ['language_expression_level', 'reading_comprehension_level'],
    summary: 'language_and_communication_summary'
  }
}; 