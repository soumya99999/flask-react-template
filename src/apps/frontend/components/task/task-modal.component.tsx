import React from 'react';

import {
  H2,
  VerticalStackLayout,
} from 'frontend/components';
import { Task, TaskFormData } from 'frontend/types';
import { TaskForm } from './task-form.component';

interface TaskModalProps {
  isOpen: boolean;
  task?: Task | null;
  onClose: () => void;
  onSubmit: (data: TaskFormData) => Promise<void>;
  isLoading?: boolean;
}

export const TaskModal: React.FC<TaskModalProps> = ({
  isOpen,
  task,
  onClose,
  onSubmit,
  isLoading = false,
}) => {
  if (!isOpen) return null;

  const isEditing = !!task;
  const initialData = task ? { title: task.title, description: task.description } : undefined;

  const handleSubmit = async (data: TaskFormData) => {
    await onSubmit(data);
    onClose();
  };

  const handleCancel = () => {
    onClose();
  };

  return (
    <div className="task-modal-overlay">
      <div className="task-modal-content">
        <VerticalStackLayout gap={24}>
          <H2>{isEditing ? 'Edit Task' : 'Create New Task'}</H2>
          
          <TaskForm
            initialData={initialData}
            onSubmit={handleSubmit}
            onCancel={handleCancel}
            isLoading={isLoading}
            submitLabel={isEditing ? 'Update Task' : 'Create Task'}
            cancelLabel="Cancel"
          />
        </VerticalStackLayout>
      </div>
    </div>
  );
};
