from dataclasses import asdict
from typing import Optional

from flask import jsonify, request
from flask.typing import ResponseReturnValue
from flask.views import MethodView

from modules.application.common.constants import DEFAULT_PAGINATION_PARAMS
from modules.application.common.types import PaginationParams
from modules.authentication.rest_api.access_auth_middleware import access_auth_middleware
from modules.task.errors import CommentBadRequestError, TaskBadRequestError
from modules.task.task_service import TaskService
from modules.task.types import (
    Comment,
    CreateCommentParams,
    CreateTaskParams,
    DeleteCommentParams,
    DeleteTaskParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    GetPaginatedTasksParams,
    GetTaskParams,
    UpdateCommentParams,
    UpdateTaskParams,
)


class TaskView(MethodView):
    @access_auth_middleware
    def post(self, account_id: str, task_id: Optional[str] = None, comment_id: Optional[str] = None) -> ResponseReturnValue:
        # Handle comment creation
        if task_id and comment_id is None:
            return self._handle_create_comment(account_id, task_id)
        
        # Handle task creation
        if task_id is None:
            return self._handle_create_task(account_id)
        
        return self._handle_create_comment(account_id, task_id)

    @access_auth_middleware
    def get(self, account_id: str, task_id: Optional[str] = None, comment_id: Optional[str] = None) -> ResponseReturnValue:
        # Handle comment retrieval
        if task_id and comment_id:
            return self._handle_get_comment(account_id, task_id, comment_id)
        elif task_id and comment_id is None:
            return self._handle_get_comments(account_id, task_id)
        
        # Handle task retrieval
        if task_id:
            return self._handle_get_task(account_id, task_id)
        else:
            return self._handle_get_tasks(account_id)

    @access_auth_middleware
    def patch(self, account_id: str, task_id: str, comment_id: Optional[str] = None) -> ResponseReturnValue:
        # Handle comment update
        if comment_id:
            return self._handle_update_comment(account_id, task_id, comment_id)
        
        # Handle task update
        return self._handle_update_task(account_id, task_id)

    @access_auth_middleware
    def delete(self, account_id: str, task_id: str, comment_id: Optional[str] = None) -> ResponseReturnValue:
        # Handle comment deletion
        if comment_id:
            return self._handle_delete_comment(account_id, task_id, comment_id)
        
        # Handle task deletion
        return self._handle_delete_task(account_id, task_id)

    # Task handlers
    def _handle_create_task(self, account_id: str) -> ResponseReturnValue:
        request_data = request.get_json()

        if request_data is None:
            raise TaskBadRequestError("Request body is required")

        if not request_data.get("title"):
            raise TaskBadRequestError("Title is required")

        if not request_data.get("description"):
            raise TaskBadRequestError("Description is required")

        create_task_params = CreateTaskParams(
            account_id=account_id, title=request_data["title"], description=request_data["description"]
        )

        created_task = TaskService.create_task(params=create_task_params)
        task_dict = asdict(created_task)

        return jsonify(task_dict), 201

    def _handle_get_task(self, account_id: str, task_id: str) -> ResponseReturnValue:
        task_params = GetTaskParams(account_id=account_id, task_id=task_id)
        task = TaskService.get_task(params=task_params)
        task_dict = asdict(task)
        return jsonify(task_dict), 200

    def _handle_get_tasks(self, account_id: str) -> ResponseReturnValue:
        page = request.args.get("page", type=int)
        size = request.args.get("size", type=int)

        if page is not None and page < 1:
            raise TaskBadRequestError("Page must be greater than 0")

        if size is not None and size < 1:
            raise TaskBadRequestError("Size must be greater than 0")

        if page is None:
            page = DEFAULT_PAGINATION_PARAMS.page
        if size is None:
            size = DEFAULT_PAGINATION_PARAMS.size

        pagination_params = PaginationParams(page=page, size=size, offset=0)
        tasks_params = GetPaginatedTasksParams(account_id=account_id, pagination_params=pagination_params)

        pagination_result = TaskService.get_paginated_tasks(params=tasks_params)

        response_data = asdict(pagination_result)

        return jsonify(response_data), 200

    def _handle_update_task(self, account_id: str, task_id: str) -> ResponseReturnValue:
        request_data = request.get_json()

        if request_data is None:
            raise TaskBadRequestError("Request body is required")

        if not request_data.get("title"):
            raise TaskBadRequestError("Title is required")

        if not request_data.get("description"):
            raise TaskBadRequestError("Description is required")

        update_task_params = UpdateTaskParams(
            account_id=account_id, task_id=task_id, title=request_data["title"], description=request_data["description"]
        )

        updated_task = TaskService.update_task(params=update_task_params)
        task_dict = asdict(updated_task)

        return jsonify(task_dict), 200

    def _handle_delete_task(self, account_id: str, task_id: str) -> ResponseReturnValue:
        delete_params = DeleteTaskParams(account_id=account_id, task_id=task_id)

        TaskService.delete_task(params=delete_params)

        return "", 204

    # Comment handlers
    def _handle_create_comment(self, account_id: str, task_id: str) -> ResponseReturnValue:
        request_data = request.get_json()

        if request_data is None:
            raise CommentBadRequestError("Request body is required")

        if not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        create_comment_params = CreateCommentParams(
            task_id=task_id, account_id=account_id, content=request_data["content"]
        )

        created_comment = TaskService.create_comment(params=create_comment_params)
        comment_dict = asdict(created_comment)

        return jsonify(comment_dict), 201

    def _handle_get_comment(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        comment_params = GetCommentParams(task_id=task_id, comment_id=comment_id)
        comment = TaskService.get_comment(params=comment_params)
        comment_dict = asdict(comment)
        return jsonify(comment_dict), 200

    def _handle_get_comments(self, account_id: str, task_id: str) -> ResponseReturnValue:
        page = request.args.get("page", type=int)
        size = request.args.get("size", type=int)

        if page is not None and page < 1:
            raise CommentBadRequestError("Page must be greater than 0")

        if size is not None and size < 1:
            raise CommentBadRequestError("Size must be greater than 0")

        if page is None:
            page = DEFAULT_PAGINATION_PARAMS.page
        if size is None:
            size = DEFAULT_PAGINATION_PARAMS.size

        pagination_params = PaginationParams(page=page, size=size, offset=0)
        comments_params = GetPaginatedCommentsParams(task_id=task_id, pagination_params=pagination_params)

        pagination_result = TaskService.get_paginated_comments(params=comments_params)

        response_data = asdict(pagination_result)

        return jsonify(response_data), 200

    def _handle_update_comment(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        request_data = request.get_json()

        if request_data is None:
            raise CommentBadRequestError("Request body is required")

        if not request_data.get("content"):
            raise CommentBadRequestError("Content is required")

        update_comment_params = UpdateCommentParams(
            task_id=task_id, comment_id=comment_id, account_id=account_id, content=request_data["content"]
        )

        updated_comment = TaskService.update_comment(params=update_comment_params)
        comment_dict = asdict(updated_comment)

        return jsonify(comment_dict), 200

    def _handle_delete_comment(self, account_id: str, task_id: str, comment_id: str) -> ResponseReturnValue:
        delete_params = DeleteCommentParams(task_id=task_id, comment_id=comment_id, account_id=account_id)

        TaskService.delete_comment(params=delete_params)

        return "", 204
