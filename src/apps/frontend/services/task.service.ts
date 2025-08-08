import { AxiosResponse } from 'axios';

import APIService from 'frontend/services/api.service';
import { getAccessTokenFromStorage } from 'frontend/utils/storage-util';
import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskListResponse,
} from 'frontend/types';

export default class TaskService extends APIService {
  private getAuthHeaders() {
    const accessToken = getAccessTokenFromStorage();
    return {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    };
  }

  async getTasks(accountId: string, page: number = 1, size: number = 10): Promise<AxiosResponse<TaskListResponse>> {
    return this.apiClient.get(`/accounts/${accountId}/tasks?page=${page}&size=${size}`, {
      headers: this.getAuthHeaders(),
    });
  }

  async getTask(accountId: string, taskId: string): Promise<AxiosResponse<Task>> {
    return this.apiClient.get(`/accounts/${accountId}/tasks/${taskId}`, {
      headers: this.getAuthHeaders(),
    });
  }

  async createTask(accountId: string, taskData: CreateTaskRequest): Promise<AxiosResponse<Task>> {
    return this.apiClient.post(`/accounts/${accountId}/tasks`, taskData, {
      headers: this.getAuthHeaders(),
    });
  }

  async updateTask(accountId: string, taskId: string, taskData: UpdateTaskRequest): Promise<AxiosResponse<Task>> {
    return this.apiClient.patch(`/accounts/${accountId}/tasks/${taskId}`, taskData, {
      headers: this.getAuthHeaders(),
    });
  }

  async deleteTask(accountId: string, taskId: string): Promise<AxiosResponse<void>> {
    return this.apiClient.delete(`/accounts/${accountId}/tasks/${taskId}`, {
      headers: this.getAuthHeaders(),
    });
  }
}
