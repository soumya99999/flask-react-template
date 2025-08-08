import React from 'react';

import {
  Button,
  Flex,
  FlexItem,
  H2,
  ParagraphMedium,
  Spinner,
  VerticalStackLayout,
} from 'frontend/components';
import { Task } from 'frontend/types';
import { TaskCard } from './task-card.component';

interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  isDeleting: boolean;
  onEdit: (task: Task) => void;
  onDelete: (taskId: string) => void;
  onCreateNew: () => void;
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  isLoading,
  isDeleting,
  onEdit,
  onDelete,
  onCreateNew,
}) => {
  if (isLoading) {
    return (
      <div className="task-loading-state">
        <Spinner />
      </div>
    );
  }

  return (
    <VerticalStackLayout gap={24}>
      <Flex justifyContent="between" alignItems="center">
        <FlexItem>
          <H2>Tasks ({tasks.length})</H2>
        </FlexItem>
        <FlexItem>
          <Button onClick={onCreateNew}>
            Create New Task
          </Button>
        </FlexItem>
      </Flex>

      {tasks.length === 0 ? (
        <div className="task-empty-state">
          <ParagraphMedium>
            No tasks found. Create your first task to get started!
          </ParagraphMedium>
          <Button onClick={onCreateNew}>
            Create Your First Task
          </Button>
        </div>
      ) : (
        <VerticalStackLayout gap={16}>
          {tasks.map((task: Task) => (
            <TaskCard
              key={task.id}
              task={task}
              onEdit={onEdit}
              onDelete={onDelete}
              isDeleting={isDeleting}
            />
          ))}
        </VerticalStackLayout>
      )}
    </VerticalStackLayout>
  );
};
