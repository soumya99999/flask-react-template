from flask import Blueprint

from modules.task.rest_api.task_view import TaskView


class TaskRouter:
    @staticmethod
    def create_route(*, blueprint: Blueprint) -> Blueprint:
        # Task routes
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks", view_func=TaskView.as_view("task_view"), methods=["POST", "GET"]
        )
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>",
            view_func=TaskView.as_view("task_view_by_id"),
            methods=["GET", "PATCH", "DELETE"],
        )

        # Comment routes
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments",
            view_func=TaskView.as_view("comment_view"),
            methods=["POST", "GET"],
        )
        blueprint.add_url_rule(
            "/accounts/<account_id>/tasks/<task_id>/comments/<comment_id>",
            view_func=TaskView.as_view("comment_view_by_id"),
            methods=["GET", "PATCH", "DELETE"],
        )

        return blueprint
