import json
import unittest

from modules.task.errors import CommentBadRequestError, CommentNotFoundError, TaskErrorCode
from modules.task.types import Comment
from .base_test_task import BaseTestTask


class TestCommentApi(BaseTestTask):
    def test_create_comment_success(self):
        """Test successful comment creation"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        comment_data = {"content": "This is a test comment"}
        response = self.make_authenticated_request(
            method="POST", account_id=account.id, token=token, task_id=task.id, data=comment_data
        )

        assert response.status_code == 201
        self.assert_comment_response(
            response.json,
            task_id=task.id,
            account_id=account.id,
            content="This is a test comment",
        )

    def test_create_comment_missing_content(self):
        """Test comment creation with missing content"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        comment_data = {}
        response = self.make_authenticated_request(
            method="POST", account_id=account.id, token=token, task_id=task.id, data=comment_data
        )

        self.assert_error_response(response, 400, TaskErrorCode.COMMENT_BAD_REQUEST)

    def test_create_comment_empty_content(self):
        """Test comment creation with empty content"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        comment_data = {"content": ""}
        response = self.make_authenticated_request(
            method="POST", account_id=account.id, token=token, task_id=task.id, data=comment_data
        )

        self.assert_error_response(response, 400, TaskErrorCode.COMMENT_BAD_REQUEST)

    def test_create_comment_missing_request_body(self):
        """Test comment creation with missing request body"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        response = self.make_authenticated_request(
            method="POST", account_id=account.id, token=token, task_id=task.id, data=None
        )

        self.assert_error_response(response, 400, TaskErrorCode.COMMENT_BAD_REQUEST)

    def test_create_comment_unauthenticated(self):
        """Test comment creation without authentication"""
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        comment_data = {"content": "This is a test comment"}
        response = self.make_unauthenticated_request(
            method="POST", account_id=account.id, task_id=task.id, data=comment_data
        )

        assert response.status_code == 401

    def test_get_comment_success(self):
        """Test successful comment retrieval"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        response = self.make_authenticated_request(
            method="GET", account_id=account.id, token=token, task_id=task.id, comment_id=comment.id
        )

        assert response.status_code == 200
        self.assert_comment_response(response.json, expected_comment=comment)

    def test_get_comment_not_found(self):
        """Test comment retrieval with non-existent comment"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        response = self.make_authenticated_request(
            method="GET", account_id=account.id, token=token, task_id=task.id, comment_id="507f1f77bcf86cd799439011"
        )

        self.assert_error_response(response, 404, TaskErrorCode.COMMENT_NOT_FOUND)

    def test_get_comment_unauthenticated(self):
        """Test comment retrieval without authentication"""
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        response = self.make_unauthenticated_request(
            method="GET", account_id=account.id, task_id=task.id, comment_id=comment.id
        )

        assert response.status_code == 401

    def test_get_comments_success(self):
        """Test successful paginated comments retrieval"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comments = self.create_multiple_test_comments(task_id=task.id, account_id=account.id, count=3)

        response = self.make_authenticated_request(
            method="GET", account_id=account.id, token=token, task_id=task.id
        )

        assert response.status_code == 200
        self.assert_pagination_response(response.json, expected_items_count=3, expected_total_count=3)

    def test_get_comments_empty(self):
        """Test comments retrieval for task with no comments"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        response = self.make_authenticated_request(
            method="GET", account_id=account.id, token=token, task_id=task.id
        )

        assert response.status_code == 200
        self.assert_pagination_response(response.json, expected_items_count=0, expected_total_count=0)

    def test_get_comments_with_pagination(self):
        """Test comments retrieval with pagination parameters"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        self.create_multiple_test_comments(task_id=task.id, account_id=account.id, count=5)

        response = self.make_authenticated_request(
            method="GET", account_id=account.id, token=token, task_id=task.id, query_params="page=1&size=2"
        )

        assert response.status_code == 200
        self.assert_pagination_response(response.json, expected_items_count=2, expected_total_count=5, expected_page=1, expected_size=2)

    def test_get_comments_unauthenticated(self):
        """Test comments retrieval without authentication"""
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        response = self.make_unauthenticated_request(method="GET", account_id=account.id, task_id=task.id)

        assert response.status_code == 401

    def test_update_comment_success(self):
        """Test successful comment update"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        update_data = {"content": "Updated comment content"}
        response = self.make_authenticated_request(
            method="PATCH", account_id=account.id, token=token, task_id=task.id, comment_id=comment.id, data=update_data
        )

        assert response.status_code == 200
        self.assert_comment_response(
            response.json,
            task_id=task.id,
            account_id=account.id,
            content="Updated comment content",
        )

    def test_update_comment_missing_content(self):
        """Test comment update with missing content"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        update_data = {}
        response = self.make_authenticated_request(
            method="PATCH", account_id=account.id, token=token, task_id=task.id, comment_id=comment.id, data=update_data
        )

        self.assert_error_response(response, 400, TaskErrorCode.COMMENT_BAD_REQUEST)

    def test_update_comment_empty_content(self):
        """Test comment update with empty content"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        update_data = {"content": ""}
        response = self.make_authenticated_request(
            method="PATCH", account_id=account.id, token=token, task_id=task.id, comment_id=comment.id, data=update_data
        )

        self.assert_error_response(response, 400, TaskErrorCode.COMMENT_BAD_REQUEST)

    def test_update_comment_missing_request_body(self):
        """Test comment update with missing request body"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        response = self.make_authenticated_request(
            method="PATCH", account_id=account.id, token=token, task_id=task.id, comment_id=comment.id, data=None
        )

        self.assert_error_response(response, 400, TaskErrorCode.COMMENT_BAD_REQUEST)

    def test_update_comment_not_found(self):
        """Test comment update with non-existent comment"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        update_data = {"content": "Updated comment content"}
        response = self.make_authenticated_request(
            method="PATCH", account_id=account.id, token=token, task_id=task.id, comment_id="507f1f77bcf86cd799439011", data=update_data
        )

        self.assert_error_response(response, 404, TaskErrorCode.COMMENT_NOT_FOUND)

    def test_update_comment_unauthenticated(self):
        """Test comment update without authentication"""
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        update_data = {"content": "Updated comment content"}
        response = self.make_unauthenticated_request(
            method="PATCH", account_id=account.id, task_id=task.id, comment_id=comment.id, data=update_data
        )

        assert response.status_code == 401

    def test_delete_comment_success(self):
        """Test successful comment deletion"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        response = self.make_authenticated_request(
            method="DELETE", account_id=account.id, token=token, task_id=task.id, comment_id=comment.id
        )

        assert response.status_code == 204

    def test_delete_comment_not_found(self):
        """Test comment deletion with non-existent comment"""
        account, token = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)

        response = self.make_authenticated_request(
            method="DELETE", account_id=account.id, token=token, task_id=task.id, comment_id="507f1f77bcf86cd799439011"
        )

        self.assert_error_response(response, 404, TaskErrorCode.COMMENT_NOT_FOUND)

    def test_delete_comment_unauthenticated(self):
        """Test comment deletion without authentication"""
        account, _ = self.create_account_and_get_token()
        task = self.create_test_task(account_id=account.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account.id)

        response = self.make_unauthenticated_request(
            method="DELETE", account_id=account.id, task_id=task.id, comment_id=comment.id
        )

        assert response.status_code == 401

    def test_cross_account_comment_access(self):
        """Test that users cannot access comments from other accounts"""
        account1, token1 = self.create_account_and_get_token(username="user1@example.com")
        account2, token2 = self.create_account_and_get_token(username="user2@example.com")
        
        task1 = self.create_test_task(account_id=account1.id)
        task2 = self.create_test_task(account_id=account2.id)
        
        comment1 = self.create_test_comment(task_id=task1.id, account_id=account1.id)
        comment2 = self.create_test_comment(task_id=task2.id, account_id=account2.id)

        # User1 tries to access User2's comment
        response = self.make_cross_account_request(
            method="GET", target_account_id=account2.id, auth_token=token1, task_id=task2.id, comment_id=comment2.id
        )

        self.assert_error_response(response, 404, TaskErrorCode.COMMENT_NOT_FOUND)

        # User2 tries to access User1's comment
        response = self.make_cross_account_request(
            method="GET", target_account_id=account1.id, auth_token=token2, task_id=task1.id, comment_id=comment1.id
        )

        self.assert_error_response(response, 404, TaskErrorCode.COMMENT_NOT_FOUND)

    def test_comment_ownership_validation(self):
        """Test that users can only update/delete their own comments"""
        account1, token1 = self.create_account_and_get_token(username="user1@example.com")
        account2, token2 = self.create_account_and_get_token(username="user2@example.com")
        
        task = self.create_test_task(account_id=account1.id)
        comment = self.create_test_comment(task_id=task.id, account_id=account1.id)

        # User2 tries to update User1's comment
        update_data = {"content": "Unauthorized update"}
        response = self.make_cross_account_request(
            method="PATCH", target_account_id=account1.id, auth_token=token2, task_id=task.id, comment_id=comment.id, data=update_data
        )

        self.assert_error_response(response, 404, TaskErrorCode.COMMENT_NOT_FOUND)

        # User2 tries to delete User1's comment
        response = self.make_cross_account_request(
            method="DELETE", target_account_id=account1.id, auth_token=token2, task_id=task.id, comment_id=comment.id
        )

        self.assert_error_response(response, 404, TaskErrorCode.COMMENT_NOT_FOUND)
