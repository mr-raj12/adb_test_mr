"""Tests for the TODO API.

These use mongomock (an in-memory Mongo) instead of a real database, so the
suite runs on its own without a Mongo container. The repository takes a db
argument, which is what lets us drop the fake one in.
"""
import json

import mongomock
from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from .entities import Todo
from .repositories import TodoRepository
from .validators import TodoValidationError, validate_todo_payload
from .views import TodoListView


def make_repository():
    """A TodoRepository backed by a fresh in-memory Mongo."""
    database = mongomock.MongoClient()["test_db"]
    return TodoRepository(database=database)


class TodoModelTests(SimpleTestCase):
    def test_from_document_stringifies_id(self):
        todo = Todo.from_document({"_id": 123, "description": "x"})
        self.assertEqual(todo.id, "123")
        self.assertEqual(todo.description, "x")

    def test_to_dict_shape(self):
        self.assertEqual(
            Todo(id="1", description="x").to_dict(),
            {"id": "1", "description": "x"},
        )


class ValidatorTests(SimpleTestCase):
    def test_valid_payload_returns_trimmed_description(self):
        self.assertEqual(
            validate_todo_payload({"description": "  hello  "}), "hello"
        )

    def test_missing_description_raises(self):
        with self.assertRaises(TodoValidationError):
            validate_todo_payload({})

    def test_blank_description_raises(self):
        with self.assertRaises(TodoValidationError):
            validate_todo_payload({"description": "   "})

    def test_non_object_payload_raises(self):
        with self.assertRaises(TodoValidationError):
            validate_todo_payload(["not", "an", "object"])

    def test_overlong_description_raises(self):
        with self.assertRaises(TodoValidationError):
            validate_todo_payload({"description": "x" * 1000})


class TodoRepositoryTests(SimpleTestCase):
    def setUp(self):
        self.repo = make_repository()

    def test_list_is_empty_initially(self):
        self.assertEqual(self.repo.list(), [])

    def test_create_returns_todo(self):
        todo = self.repo.create("Learn Docker")
        self.assertIsInstance(todo, Todo)
        self.assertEqual(todo.description, "Learn Docker")
        self.assertIsInstance(todo.id, str)

    def test_create_then_list_newest_first(self):
        self.repo.create("first")
        self.repo.create("second")
        descriptions = [todo.description for todo in self.repo.list()]
        self.assertEqual(descriptions, ["second", "first"])


class TodoListViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # One repository shared across the request(s) in a single test.
        self.repo = make_repository()
        self._orig = TodoListView.get_repository
        TodoListView.get_repository = lambda _self: self.repo

    def tearDown(self):
        TodoListView.get_repository = self._orig

    def _view(self):
        return TodoListView.as_view()

    def _post(self, body):
        return self._view()(
            self.factory.post(
                "/todos", json.dumps(body), content_type="application/json"
            )
        )

    def test_get_returns_empty_list(self):
        response = self._view()(self.factory.get("/todos"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_post_creates_todo(self):
        response = self._post({"description": "Buy milk"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["description"], "Buy milk")
        self.assertIn("id", response.data)

    def test_post_then_get_roundtrip(self):
        self._post({"description": "Walk dog"})
        response = self._view()(self.factory.get("/todos"))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["description"], "Walk dog")

    def test_post_rejects_empty_description(self):
        response = self._post({"description": "   "})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_rejects_missing_description(self):
        response = self._post({})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
