import axios, { AxiosError } from 'axios';
import type { ApiErrorShape } from '../types';

export const TOKEN_STORAGE_KEY = 'task_manager_token';

export const apiClient = axios.create({
  baseURL: '/api',
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let onUnauthorized: (() => void) | null = null;

export function setUnauthorizedHandler(handler: () => void) {
  onUnauthorized = handler;
}

apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    const isLoginRequest = error.config?.url?.includes('/login/');
    if (error.response?.status === 401 && !isLoginRequest) {
      onUnauthorized?.();
    }
    return Promise.reject(error);
  },
);

export function getErrorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const data = error.response?.data as ApiErrorShape | undefined;
    if (data?.detail) {
      if (typeof data.detail === 'string') {
        return data.detail;
      }
      return data.detail.map((item) => item.msg).join(', ');
    }
    if (error.message) {
      return error.message;
    }
  }
  return 'Something went wrong. Please try again.';
}
