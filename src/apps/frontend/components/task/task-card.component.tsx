import React from 'react';

import {
  Button,
  Flex,
  FlexItem,
  H2,
  ParagraphMedium,
  VerticalStackLayout,
} from 'frontend/components';
import { Task } from 'frontend/types';
import { ButtonKind } from 'frontend/types/button';

interface TaskCardProps {
  task: Task;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  isDeleting?: boolean;
}

export const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onEdit,
  onDelete,
  isDeleting = false,
}) => {
  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      onDelete(task.id);
    }
  };

  return (
    <div className="task-card">
      <VerticalStackLayout gap={12}>
        <Flex justifyContent="between" alignItems="start">
          <FlexItem flex="flex1">
            <H2>{task.title}</H2>
          </FlexItem>
          <FlexItem>
            <Flex gap={8}>
              <Button
                kind={ButtonKind.TERTIARY}
                onClick={() => onEdit(task)}
                disabled={isDeleting}
              >
                Edit
              </Button>
              <Button
                kind={ButtonKind.TERTIARY}
                onClick={handleDelete}
                disabled={isDeleting}
                isLoading={isDeleting}
              >
                Delete
              </Button>
            </Flex>
          </FlexItem>
        </Flex>
        
        <ParagraphMedium>{task.description}</ParagraphMedium>
      </VerticalStackLayout>
    </div>
  );
};
