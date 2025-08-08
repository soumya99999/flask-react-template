from modules.application.common.types import PaginationResult
from modules.task.internal.comment_reader import CommentReader
from modules.task.internal.comment_writer import CommentWriter
from modules.task.internal.task_reader import TaskReader
from modules.task.internal.task_writer import TaskWriter
from modules.task.types import (
    Comment,
    CommentDeletionResult,
    CreateCommentParams,
    CreateTaskParams,
    DeleteCommentParams,
    DeleteTaskParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    GetPaginatedTasksParams,
    GetTaskParams,
    Task,
    TaskDeletionResult,
    UpdateCommentParams,
    UpdateTaskParams,
)


class TaskService:
    @staticmethod
    def create_task(*, params: CreateTaskParams) -> Task:
        return TaskWriter.create_task(params=params)

    @staticmethod
    def get_task(*, params: GetTaskParams) -> Task:
        return TaskReader.get_task(params=params)

    @staticmethod
    def get_paginated_tasks(*, params: GetPaginatedTasksParams) -> PaginationResult[Task]:
        return TaskReader.get_paginated_tasks(params=params)

    @staticmethod
    def update_task(*, params: UpdateTaskParams) -> Task:
        return TaskWriter.update_task(params=params)

    @staticmethod
    def delete_task(*, params: DeleteTaskParams) -> TaskDeletionResult:
        return TaskWriter.delete_task(params=params)

    # Comment-related methods
    @staticmethod
    def create_comment(*, params: CreateCommentParams) -> Comment:
        return CommentWriter.create_comment(params=params)

    @staticmethod
    def get_comment(*, params: GetCommentParams) -> Comment:
        return CommentReader.get_comment(params=params)

    @staticmethod
    def get_paginated_comments(*, params: GetPaginatedCommentsParams) -> PaginationResult[Comment]:
        return CommentReader.get_paginated_comments(params=params)

    @staticmethod
    def update_comment(*, params: UpdateCommentParams) -> Comment:
        return CommentWriter.update_comment(params=params)

    @staticmethod
    def delete_comment(*, params: DeleteCommentParams) -> CommentDeletionResult:
        return CommentWriter.delete_comment(params=params)
