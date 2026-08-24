import { apiClient } from './client';
import type { LoginResponse, User } from '../types';

export interface RegisterPayload {
  email: string;
  password: string;
}

export interface LoginPayload {
  email: string;
  password: string;
}

export async function registerUser(payload: RegisterPayload): Promise<User> {
  const { data } = await apiClient.post<User>('/register/', payload);
  return data;
}

export async function loginUser(payload: LoginPayload): Promise<LoginResponse> {
  const body = new URLSearchParams();
  body.set('username', payload.email);
  body.set('password', payload.password);

  const { data } = await apiClient.post<LoginResponse>('/login/', body, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return data;
}
