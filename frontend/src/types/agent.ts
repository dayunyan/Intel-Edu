export interface Agent {
  id: number;
  student_id: number;
  name: string;
  avatar_url: string;
  description: string;
  created_at: string;
  updated_at: string;
}

// 添加一个工具函数来处理 URL
export const getFullImageUrl = (url: string | null) => {
  if (!url) return null;
  if (url.startsWith('http')) return url;
  return `${process.env.NEXT_PUBLIC_API_BASE_URL}${url}`;
}; 