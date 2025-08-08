import unittest

from modules.task.errors import CommentNotFoundError
from modules.task.task_service import TaskService
from modules.task.types import (
    Comment,
    CreateCommentParams,
    DeleteCommentParams,
    GetCommentParams,
    GetPaginatedCommentsParams,
    UpdateCommentParams,
)
from .base_test_task import BaseTestTask


class TestCommentService(BaseTestTask):
    def test_create_comment_success(self):
        """Test successful comment creation at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)

        create_params = CreateCommentParams(
            task_id=task.id, account_id=account.id, content="Test comment content"
        )

        comment = TaskService.create_comment(params=create_params)

        assert comment.task_id == task.id
        assert comment.account_id == account.id
        assert comment.content == "Test comment content"
        assert comment.id is not None
        assert comment.created_at is not None
        assert comment.updated_at is not None

    def test_get_comment_success(self):
        """Test successful comment retrieval at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        created_comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        get_params = GetCommentParams(task_id=task.id, comment_id=created_comment.id)

        comment = TaskService.get_comment(params=get_params)

        assert comment.id == created_comment.id
        assert comment.task_id == created_comment.task_id
        assert comment.account_id == created_comment.account_id
        assert comment.content == created_comment.content

    def test_get_comment_not_found(self):
        """Test comment retrieval with non-existent comment at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)

        get_params = GetCommentParams(task_id=task.id, comment_id="507f1f77bcf86cd799439011")

        with self.assertRaises(CommentNotFoundError):
            TaskService.get_comment(params=get_params)

    def test_get_paginated_comments_success(self):
        """Test successful paginated comments retrieval at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        created_comments = self.create_multiple_test_comments(task_id=task.id, account_id=account.id, count=3)

        from modules.application.common.types import PaginationParams
        pagination_params = PaginationParams(page=1, size=10, offset=0)
        get_params = GetPaginatedCommentsParams(task_id=task.id, pagination_params=pagination_params)

        pagination_result = TaskService.get_paginated_comments(params=get_params)

        assert len(pagination_result.items) == 3
        assert pagination_result.total_count == 3
        assert pagination_result.total_pages == 1
        assert pagination_result.pagination_params.page == 1
        assert pagination_result.pagination_params.size == 10

    def test_get_paginated_comments_empty(self):
        """Test paginated comments retrieval for task with no comments at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)

        from modules.application.common.types import PaginationParams
        pagination_params = PaginationParams(page=1, size=10, offset=0)
        get_params = GetPaginatedCommentsParams(task_id=task.id, pagination_params=pagination_params)

        pagination_result = TaskService.get_paginated_comments(params=get_params)

        assert len(pagination_result.items) == 0
        assert pagination_result.total_count == 0
        assert pagination_result.total_pages == 0

    def test_update_comment_success(self):
        """Test successful comment update at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        created_comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        update_params = UpdateCommentParams(
            task_id=task.id, comment_id=created_comment.id, account_id=account.id, content="Updated content"
        )

        updated_comment = TaskService.update_comment(params=update_params)

        assert updated_comment.id == created_comment.id
        assert updated_comment.task_id == created_comment.task_id
        assert updated_comment.account_id == created_comment.account_id
        assert updated_comment.content == "Updated content"
        assert updated_comment.updated_at > created_comment.updated_at

    def test_update_comment_not_found(self):
        """Test comment update with non-existent comment at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)

        update_params = UpdateCommentParams(
            task_id=task.id, comment_id="507f1f77bcf86cd799439011", account_id=account.id, content="Updated content"
        )

        with self.assertRaises(CommentNotFoundError):
            TaskService.update_comment(params=update_params)

    def test_update_comment_wrong_owner(self):
        """Test comment update by wrong owner at service level"""
        account1 = self.create_test_account(username="user1@example.com")
        account2 = self.create_test_account(username="user2@example.com")
        task = self.create_test_task(account_id=account1.id)
        created_comment = self.create_test_comment(task_id=task.id, account_id=account1.id)

        update_params = UpdateCommentParams(
            task_id=task.id, comment_id=created_comment.id, account_id=account2.id, content="Updated content"
        )

        with self.assertRaises(CommentNotFoundError):
            TaskService.update_comment(params=update_params)

    def test_delete_comment_success(self):
        """Test successful comment deletion at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        created_comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        delete_params = DeleteCommentParams(
            task_id=task.id, comment_id=created_comment.id, account_id=account.id
        )

        deletion_result = TaskService.delete_comment(params=delete_params)

        assert deletion_result.comment_id == created_comment.id
        assert deletion_result.success is True
        assert deletion_result.deleted_at is not None

        # Verify comment is no longer retrievable
        get_params = GetCommentParams(task_id=task.id, comment_id=created_comment.id)
        with self.assertRaises(CommentNotFoundError):
            TaskService.get_comment(params=get_params)

    def test_delete_comment_not_found(self):
        """Test comment deletion with non-existent comment at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)

        delete_params = DeleteCommentParams(
            task_id=task.id, comment_id="507f1f77bcf86cd799439011", account_id=account.id
        )

        with self.assertRaises(CommentNotFoundError):
            TaskService.delete_comment(params=delete_params)

    def test_delete_comment_wrong_owner(self):
        """Test comment deletion by wrong owner at service level"""
        account1 = self.create_test_account(username="user1@example.com")
        account2 = self.create_test_account(username="user2@example.com")
        task = self.create_test_task(account_id=account1.id)
        created_comment = self.create_test_comment(task_id=task.id, account_id=account1.id)

        delete_params = DeleteCommentParams(
            task_id=task.id, comment_id=created_comment.id, account_id=account2.id
        )

        with self.assertRaises(CommentNotFoundError):
            TaskService.delete_comment(params=delete_params)

    def test_comment_isolation_between_tasks(self):
        """Test that comments are isolated between different tasks"""
        account = self.create_test_account()
        task1 = self.create_test_task(account_id=account.id)
        task2 = self.create_test_task(account_id=account.id)

        comment1 = self.create_test_comment(task_id=task1.id, account_id=account.id)
        comment2 = self.create_test_comment(task_id=task2.id, account_id=account.id)

        # Verify comments belong to different tasks
        assert comment1.task_id == task1.id
        assert comment2.task_id == task2.id
        assert comment1.task_id != comment2.task_id

        # Verify comments can be retrieved independently
        get_params1 = GetCommentParams(task_id=task1.id, comment_id=comment1.id)
        get_params2 = GetCommentParams(task_id=task2.id, comment_id=comment2.id)

        retrieved_comment1 = TaskService.get_comment(params=get_params1)
        retrieved_comment2 = TaskService.get_comment(params=get_params2)

        assert retrieved_comment1.id == comment1.id
        assert retrieved_comment2.id == comment2.id

    def test_comment_pagination_with_multiple_pages(self):
        """Test comment pagination with multiple pages at service level"""
        account = self.create_test_account()
        task = self.create_test_task(account_id=account.id)
        self.create_multiple_test_comments(task_id=task.id, account_id=account.id, count=5)

        from modules.application.common.types import PaginationParams

        # Test first page
        pagination_params1 = PaginationParams(page=1, size=2, offset=0)
        get_params1 = GetPaginatedCommentsParams(task_id=task.id, pagination_params=pagination_params1)
        pagination_result1 = TaskService.get_paginated_comments(params=get_params1)

        assert len(pagination_result1.items) == 2
        assert pagination_result1.total_count == 5
        assert pagination_result1.total_pages == 3

        # Test second page
        pagination_params2 = PaginationParams(page=2, size=2, offset=2)
        get_params2 = GetPaginatedCommentsParams(task_id=task.id, pagination_params=pagination_params2)
        pagination_result2 = TaskService.get_paginated_comments(params=get_params2)

        assert len(pagination_result2.items) == 2
        assert pagination_result2.total_count == 5
        assert pagination_result2.total_pages == 3

        # Test third page
        pagination_params3 = PaginationParams(page=3, size=2, offset=4)
        get_params3 = GetPaginatedCommentsParams(task_id=task.id, pagination_params=pagination_params3)
        pagination_result3 = TaskService.get_paginated_comments(params=get_params3)

        assert len(pagination_result3.items) == 1
        assert pagination_result3.total_count == 5
        assert pagination_result3.total_pages == 3
