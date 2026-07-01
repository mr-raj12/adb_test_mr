"""The Todo object.

A plain dataclass, not a Django model. Todos are stored in Mongo via the
repository, so this is just the shape we pass around in code instead of bare
dicts.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Todo:
    description: str
    id: Optional[str] = None

    @classmethod
    def from_document(cls, document: dict) -> "Todo":
        # Mongo's _id is an ObjectId; turn it into a string id so callers
        # don't have to deal with BSON types.
        return cls(id=str(document["_id"]), description=document["description"])

    def to_dict(self) -> dict:
        """The JSON we send back to the client."""
        return {"id": self.id, "description": self.description}
