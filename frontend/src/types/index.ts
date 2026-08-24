export type Priority = 'low' | 'medium' | 'high';

export type Role = 'admin' | 'manager' | 'employee';

export interface User {
  id: string;
  email: string;
  role: Role;
}

export interface Task {
  id: string;
  name: string;
  description: string;
  completed: boolean;
  priority: Priority;
  created_at: string;
}

export interface TaskCreate {
  name: string;
  description: string;
  completed?: boolean;
  priority?: Priority;
}

export interface TaskUpdate {
  name?: string;
  description?: string;
  completed?: boolean;
  priority?: Priority;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface ValidationErrorItem {
  loc: (string | number)[];
  msg: string;
  type: string;
}

export interface ApiErrorShape {
  detail: string | ValidationErrorItem[];
}
