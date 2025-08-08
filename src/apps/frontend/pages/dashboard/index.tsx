import * as React from 'react';
import { useEffect, useState } from 'react';

import { useTaskContext } from 'frontend/contexts';
import { Task, TaskFormData } from 'frontend/types';
import { TaskList } from 'frontend/components/task/task-list.component';
import { TaskModal } from 'frontend/components/task/task-modal.component';

const Dashboard: React.FC = () => {
  const {
    tasks,
    isLoading,
    isCreating,
    isUpdating,
    isDeleting,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    setCurrentTask,
    clearError,
  } = useTaskContext();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  useEffect(() => {
    if (error) {
      console.error('Task error:', error);
      clearError();
    }
  }, [error, clearError]);

  const handleCreateNew = () => {
    setEditingTask(null);
    setIsModalOpen(true);
  };

  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setIsModalOpen(true);
  };

  const handleDelete = async (taskId: string) => {
    try {
      await deleteTask(taskId);
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const handleSubmit = async (data: TaskFormData) => {
    try {
      if (editingTask) {
        await updateTask(editingTask.id, data);
      } else {
        await createTask(data);
      }
    } catch (error) {
      console.error('Failed to save task:', error);
      throw error; // Re-throw to let the form handle the error
    }
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingTask(null);
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <TaskList
        tasks={tasks}
        isLoading={isLoading}
        isDeleting={isDeleting}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onCreateNew={handleCreateNew}
      />

      <TaskModal
        isOpen={isModalOpen}
        task={editingTask}
        onClose={handleCloseModal}
        onSubmit={handleSubmit}
        isLoading={isCreating || isUpdating}
      />
    </div>
  );
};

export default Dashboard;
