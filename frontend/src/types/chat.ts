export interface Message {
  timestamp: string;
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface Chat {
  id: number;
  student_id: number;
  timestamp: string;
  messages: Message[];
  created_at: string;
  updated_at: string;
}


// export interface ChatResponse {
//   data: Chat;
//   message: string;
//   status: number;
// }

// export interface ChatHistoryResponse {
//   data: Chat[];
//   message: string;
//   status: number;
// } 