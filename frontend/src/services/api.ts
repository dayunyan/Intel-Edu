import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器：添加token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

interface ApiResponse<T> {
  data: T;
  message: string;
  status: number;
}

export interface StudentData {
  id: number;
  full_name: string;
  username: string;
  email: string;
  created_at: string;
  updated_at: string;
}

export interface CurriculumData {
  id: number;
  name: string;
  description: string;
  teacher_id: number;
  teacher_name: string;
}

export const auth = {
  login: (username: string, password: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    
    return api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },
  register: (userData: any) => api.post('/auth/register', userData),
};

export const students = {
  getAll: (): Promise<ApiResponse<StudentData[]>> => api.get('/students'),
  getById: (id: number): Promise<ApiResponse<StudentData>> => api.get(`/students/${id}`),
  getBehaviors: (id: number) => api.get(`/student-data/behaviors/${id}`),
  getProgress: (id: number) => api.get(`/student-data/progress/${id}`),
};

export const subjects = {
  getAll: () => api.get('/subjects'),
  getById: (id: number) => api.get(`/subjects/${id}`),
  create: (data: any) => api.post('/subjects', data),
  update: (id: number, data: any) => api.put(`/subjects/${id}`, data),
};

export const analysis = {
  getReportAnalysis: (studentId: number): Promise<ApiResponse<ReportAnalysisData>> => 
    api.get(`/analysis/report/${studentId}`),
  
  getBehaviorAnalysis: (studentId: number): Promise<ApiResponse<BehaviorAnalysis>> => 
    api.get(`/analysis/behavior/${studentId}`),
  
  getKnowledgeAnalysis: (studentId: number): Promise<ApiResponse<KnowledgeAnalysis[]>> => 
    api.get(`/analysis/knowledge/${studentId}`),
};

export const messages = {
  create: (data: any) => api.post('/messages', data),
  getByStudent: (studentId: number) => api.get(`/messages/student/${studentId}`),
  getByCourse: (courseId: number) => api.get(`/messages/course/${courseId}`),
};

export const curriculum = {
  // 获取所有课程
  getSubjects: (): Promise<ApiResponse<Subject[]>> => api.get('/curriculum/subjects'),
  
  // 获取单个课程
  getSubjectById: (id: number): Promise<ApiResponse<Subject>> => api.get(`/curriculum/subjects/${id}`),
  
  // 获取课程下的教材
  getBooks: (subjectId: number): Promise<ApiResponse<Book[]>> => 
    api.get(`/curriculum/subjects/${subjectId}/books`),
  
  // 获取教材的章节
  getChapters: (bookId: number): Promise<ApiResponse<Chapter[]>> => 
    api.get(`/curriculum/books/${bookId}/chapters`),
  
  // 获取章节的小节
  getSections: (chapterId: number): Promise<ApiResponse<Section[]>> => 
    api.get(`/curriculum/chapters/${chapterId}/sections`),
  
  // 获取课程表
  getSchedule: (): Promise<ApiResponse<Class[]>> => api.get('/curriculum/schedule'),
  
  // 创建课程
  create: (data: Partial<Subject>) => api.post('/curriculum/subjects', data),
  
  // 更新课程
  update: (id: number, data: Partial<Subject>) => api.put(`/curriculum/subjects/${id}`, data),
  
  // 删除课程
  delete: (id: number) => api.delete(`/curriculum/subjects/${id}`),
};

export default api; 