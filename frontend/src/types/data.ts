export interface StudentData {
  id: number;
  username: string;
  full_name: string;
  email: string | null;
  gender: 'MALE' | 'FEMALE';
  age: number;
  grade: number;
  class_id: number;
  class_name: string;
  description: string;
  created_at: string;
  updated_at: string;
}

export interface TableRecord {
  key: string | number;
  [key: string]: any;
}

