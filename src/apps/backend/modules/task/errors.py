from modules.application.errors import AppError
from modules.task.types import TaskErrorCode


class TaskNotFoundError(AppError):
    def __init__(self, task_id: str) -> None:
        super().__init__(
            code=TaskErrorCode.NOT_FOUND, http_status_code=404, message=f"Task with id {task_id} not found."
        )


class TaskBadRequestError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.BAD_REQUEST, http_status_code=400, message=message)


class CommentNotFoundError(AppError):
    def __init__(self, comment_id: str) -> None:
        super().__init__(
            code=TaskErrorCode.COMMENT_NOT_FOUND, http_status_code=404, message=f"Comment with id {comment_id} not found."
        )


class CommentBadRequestError(AppError):
    def __init__(self, message: str) -> None:
        super().__init__(code=TaskErrorCode.COMMENT_BAD_REQUEST, http_status_code=400, message=message)
