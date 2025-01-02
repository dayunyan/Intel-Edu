export interface Subject {
  id: number;
  name: string;
  description: string;
  teacher_id: number;
  teacher_name: string;
}

export interface Book {
  id: number;
  subject_id: number;
  name: string;
  description: string;
  order: number;
}

export interface Chapter {
  id: number;
  book_id: number;
  name: string;
  description: string;
  order: number;
}

export interface Section {
  id: number;
  chapter_id: number;
  name: string;
  description: string;
  order: number;
}

export interface Class {
  id: number;
  subject_id: number;
  teacher_id: number;
  teacher_name: string;
  name: string;
  date: string;
  start_time: string;
  end_time: string;
  description: string;
} 