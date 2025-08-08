export interface Task {
  id: string;
  account_id: string;
  description: string;
  title: string;
}

export interface CreateTaskRequest {
  title: string;
  description: string;
}

export interface UpdateTaskRequest {
  title: string;
  description: string;
}

export interface PaginationParams {
  page: number;
  size: number;
  offset: number;
}

export interface PaginationResult<T> {
  items: T[];
  pagination_params: PaginationParams;
  total_count: number;
  total_pages: number;
}

export interface TaskListResponse extends PaginationResult<Task> {}

export interface TaskFormData {
  title: string;
  description: string;
}

export interface TaskFormErrors {
  title?: string;
  description?: string;
}
