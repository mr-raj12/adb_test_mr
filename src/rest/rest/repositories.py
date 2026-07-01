"""Reading and writing todos in Mongo.

The view talks to this class instead of touching Mongo itself, so all the
collection/query details stay in one file and tests can pass in a fake db.
"""
from typing import List, Optional

from pymongo.collection import Collection
from pymongo.database import Database

from .entities import Todo
from .mongo import get_database


class TodoRepository:
    COLLECTION_NAME = "todos"

    def __init__(self, database: Optional[Database] = None):
        # Tests pass a mongomock db here; in the app we use the real one.
        self._db = database if database is not None else get_database()

    @property
    def _collection(self) -> Collection:
        return self._db[self.COLLECTION_NAME]

    def list(self) -> List[Todo]:
        """Every todo, newest first."""
        cursor = self._collection.find().sort("_id", -1)
        return [Todo.from_document(document) for document in cursor]

    def create(self, description: str) -> Todo:
        # We already know the id and description after insert, so there's no
        # need to read the document back.
        result = self._collection.insert_one({"description": description})
        return Todo(id=str(result.inserted_id), description=description)
