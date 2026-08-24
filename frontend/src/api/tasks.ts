import { apiClient } from './client';
import type { Task, TaskCreate, TaskUpdate } from '../types';

export async function listTasks(): Promise<Task[]> {
  const { data } = await apiClient.get<Task[]>('/tasks/');
  return data;
}

export async function getTask(id: string): Promise<Task> {
  const { data } = await apiClient.get<Task>(`/tasks/${id}`);
  return data;
}

export async function createTask(payload: TaskCreate): Promise<Task> {
  const { data } = await apiClient.post<Task>('/tasks/', payload);
  return data;
}

export async function updateTask(id: string, payload: TaskUpdate): Promise<Task> {
  const { data } = await apiClient.patch<Task>(`/tasks/${id}`, payload);
  return data;
}

export async function deleteTask(id: string): Promise<void> {
  await apiClient.delete(`/tasks/${id}`);
}
