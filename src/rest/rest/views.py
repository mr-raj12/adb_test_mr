"""The /todos endpoint.

The view stays small: validate the input, call the repository, turn the
result (or error) into a response. Validation and Mongo access live in their
own modules.
"""
import logging

from pymongo.errors import PyMongoError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .repositories import TodoRepository
from .validators import TodoValidationError, validate_todo_payload

logger = logging.getLogger(__name__)


class TodoListView(APIView):
    """GET to list todos, POST to add one."""

    def get_repository(self) -> TodoRepository:
        # A method so tests can swap in a repository backed by a fake db.
        return TodoRepository()

    def get(self, request):
        try:
            todos = self.get_repository().list()
        except PyMongoError:
            logger.exception("Failed to list todos")
            return Response(
                {"detail": "Unable to fetch todos."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            [todo.to_dict() for todo in todos], status=status.HTTP_200_OK
        )

    def post(self, request):
        try:
            description = validate_todo_payload(request.data)
        except TodoValidationError as exc:
            return Response(
                {"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            todo = self.get_repository().create(description)
        except PyMongoError:
            logger.exception("Failed to create todo")
            return Response(
                {"detail": "Unable to create todo."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(todo.to_dict(), status=status.HTTP_201_CREATED)
