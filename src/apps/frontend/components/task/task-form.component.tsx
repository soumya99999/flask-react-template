import React, { useState, useEffect } from 'react';

import {
  Button,
  FormControl,
  Input,
  VerticalStackLayout,
} from 'frontend/components';
import { TaskFormData, TaskFormErrors } from 'frontend/types';

interface TaskFormProps {
  initialData?: TaskFormData;
  onSubmit: (data: TaskFormData) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
  submitLabel?: string;
  cancelLabel?: string;
}

export const TaskForm: React.FC<TaskFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
  isLoading = false,
  submitLabel = 'Save Task',
  cancelLabel = 'Cancel',
}) => {
  const [formData, setFormData] = useState<TaskFormData>({
    title: '',
    description: '',
  });
  const [errors, setErrors] = useState<TaskFormErrors>({});

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    }
  }, [initialData]);

  const validateForm = (): boolean => {
    const newErrors: TaskFormErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (validateForm()) {
      try {
        await onSubmit(formData);
      } catch (error) {
        // Error handling is done in the parent component
      }
    }
  };

  const handleInputChange = (field: keyof TaskFormData, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <VerticalStackLayout gap="16px">
        <FormControl
          label="Title"
          error={errors.title}
          required
        >
          <Input
            value={formData.title}
            onChange={(e) => handleInputChange('title', e.target.value)}
            placeholder="Enter task title"
            disabled={isLoading}
          />
        </FormControl>

        <FormControl
          label="Description"
          error={errors.description}
          required
        >
          <Input
            value={formData.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            placeholder="Enter task description"
            disabled={isLoading}
            multiline
            rows={4}
          />
        </FormControl>

        <VerticalStackLayout gap="8px">
          <Button
            type="submit"
            disabled={isLoading}
            loading={isLoading}
            fullWidth
          >
            {submitLabel}
          </Button>
          
          <Button
            type="button"
            variant="secondary"
            onClick={onCancel}
            disabled={isLoading}
            fullWidth
          >
            {cancelLabel}
          </Button>
        </VerticalStackLayout>
      </VerticalStackLayout>
    </form>
  );
};
