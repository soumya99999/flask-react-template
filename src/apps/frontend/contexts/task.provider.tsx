import React, { createContext, PropsWithChildren, useContext, useState, useCallback } from 'react';
import toast from 'react-hot-toast';

import useAsync from 'frontend/contexts/async.hook';
import { TaskService } from 'frontend/services';
import { useAccountContext } from 'frontend/contexts/account.provider';
import {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskListResponse,
  AsyncError,
} from 'frontend/types';
import { Nullable } from 'frontend/types/common-types';

type TaskContextType = {
  tasks: Task[];
  currentTask: Nullable<Task>;
  isLoading: boolean;
  isCreating: boolean;
  isUpdating: boolean;
  isDeleting: boolean;
  error: Nullable<AsyncError>;
  totalCount: number;
  totalPages: number;
  currentPage: number;
  pageSize: number;
  
  // Actions
  fetchTasks: (page?: number, size?: number) => Promise<void>;
  fetchTask: (taskId: string) => Promise<Nullable<Task>>;
  createTask: (taskData: CreateTaskRequest) => Promise<Nullable<Task>>;
  updateTask: (taskId: string, taskData: UpdateTaskRequest) => Promise<Nullable<Task>>;
  deleteTask: (taskId: string) => Promise<boolean>;
  setCurrentTask: (task: Nullable<Task>) => void;
  clearError: () => void;
};

const TaskContext = createContext<Nullable<TaskContextType>>(null);

const taskService = new TaskService();

export const useTaskContext = (): TaskContextType =>
  useContext(TaskContext) as TaskContextType;

export const TaskProvider: React.FC<PropsWithChildren> = ({ children }) => {
  const { accountDetails } = useAccountContext();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [currentTask, setCurrentTask] = useState<Nullable<Task>>(null);
  const [totalCount, setTotalCount] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [error, setError] = useState<Nullable<AsyncError>>(null);

  const clearError = useCallback(() => setError(null), []);

  // Fetch tasks
  const fetchTasksFn = useCallback(async (page: number = 1, size: number = 10) => {
    if (!accountDetails.id) {
      throw new Error('Account ID not available');
    }
    
    const response = await taskService.getTasks(accountDetails.id, page, size);
    const data: TaskListResponse = response.data;
    
    setTasks(data.items);
    setTotalCount(data.total_count);
    setTotalPages(data.total_pages);
    setCurrentPage(data.pagination_params.page);
    setPageSize(data.pagination_params.size);
    
    return data;
  }, [accountDetails.id]);

  const {
    isLoading,
    error: fetchError,
    asyncCallback: fetchTasks,
  } = useAsync(fetchTasksFn);

  // Fetch single task
  const fetchTaskFn = useCallback(async (taskId: string) => {
    if (!accountDetails.id) {
      throw new Error('Account ID not available');
    }
    
    const response = await taskService.getTask(accountDetails.id, taskId);
    return response.data;
  }, [accountDetails.id]);

  const {
    asyncCallback: fetchTask,
  } = useAsync(fetchTaskFn);

  // Create task
  const createTaskFn = useCallback(async (taskData: CreateTaskRequest) => {
    if (!accountDetails.id) {
      throw new Error('Account ID not available');
    }
    
    const response = await taskService.createTask(accountDetails.id, taskData);
    const newTask = response.data;
    
    // Add to current list
    setTasks(prev => [newTask, ...prev]);
    setTotalCount(prev => prev + 1);
    
    toast.success('Task created successfully!');
    return newTask;
  }, [accountDetails.id]);

  const {
    isLoading: isCreating,
    error: createError,
    asyncCallback: createTask,
  } = useAsync(createTaskFn);

  // Update task
  const updateTaskFn = useCallback(async (taskId: string, taskData: UpdateTaskRequest) => {
    if (!accountDetails.id) {
      throw new Error('Account ID not available');
    }
    
    const response = await taskService.updateTask(accountDetails.id, taskId, taskData);
    const updatedTask = response.data;
    
    // Update in current list
    setTasks(prev => prev.map(task => 
      task.id === taskId ? updatedTask : task
    ));
    
    // Update current task if it's the one being edited
    setCurrentTask(prev => prev?.id === taskId ? updatedTask : prev);
    
    toast.success('Task updated successfully!');
    return updatedTask;
  }, [accountDetails.id]);

  const {
    isLoading: isUpdating,
    error: updateError,
    asyncCallback: updateTask,
  } = useAsync(updateTaskFn);

  // Delete task
  const deleteTaskFn = useCallback(async (taskId: string) => {
    if (!accountDetails.id) {
      throw new Error('Account ID not available');
    }
    
    await taskService.deleteTask(accountDetails.id, taskId);
    
    // Remove from current list
    setTasks(prev => prev.filter(task => task.id !== taskId));
    setTotalCount(prev => prev - 1);
    
    // Clear current task if it's the one being deleted
    setCurrentTask(prev => prev?.id === taskId ? null : prev);
    
    toast.success('Task deleted successfully!');
    return true;
  }, [accountDetails.id]);

  const {
    isLoading: isDeleting,
    error: deleteError,
    asyncCallback: deleteTask,
  } = useAsync(deleteTaskFn);

  // Combine all errors
  const combinedError = fetchError || createError || updateError || deleteError || error;

  return (
    <TaskContext.Provider
      value={{
        tasks,
        currentTask,
        isLoading,
        isCreating,
        isUpdating,
        isDeleting,
        error: combinedError,
        totalCount,
        totalPages,
        currentPage,
        pageSize,
        fetchTasks,
        fetchTask,
        createTask,
        updateTask,
        deleteTask,
        setCurrentTask,
        clearError,
      }}
    >
      {children}
    </TaskContext.Provider>
  );
};
