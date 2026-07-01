"""Mongo connection helpers.

One place that knows the host/port and hands back a client. We cache the
client so we don't open a new connection pool on every request.
"""
import os
from functools import lru_cache

from pymongo import MongoClient
from pymongo.database import Database

DEFAULT_DB_NAME = "test_db"


def _build_uri() -> str:
    # MONGO_HOST / MONGO_PORT come from the container env (see Dockerfile).
    host = os.environ["MONGO_HOST"]
    port = os.environ["MONGO_PORT"]
    return f"mongodb://{host}:{port}"


@lru_cache(maxsize=1)
def get_client() -> MongoClient:
    """Return the shared Mongo client, creating it on first use."""
    return MongoClient(_build_uri())


def get_database(name: str = DEFAULT_DB_NAME) -> Database:
    return get_client()[name]
