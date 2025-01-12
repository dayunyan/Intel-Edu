export interface ImageInfo {
  url: string;
  filename: string;
}

export interface Message {
  timestamp: string;
  role: 'system' | 'user' | 'assistant';
  content: string;
  images?: ImageInfo[];
}

export interface Chat {
  id: number;
  student_id: number;
  timestamp: string;
  messages: Message[];
  created_at: string;
  updated_at: string;
}
