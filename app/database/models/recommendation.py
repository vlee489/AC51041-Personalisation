"""Model that defines a user's recommendations"""
from typing import List, Dict, Union, TypedDict
from bson import ObjectId
from datetime import datetime


class RecommendationDict(TypedDict):
    id: ObjectId
    user_oid: ObjectId
    tags: Dict[str, int]
    categories: Dict[str, int]


class Recommendation:
    id: ObjectId
    user_oid: ObjectId
    tags: Dict[str, int]
    categories: Dict[str, int]

    def __init__(self, id: ObjectId, user_oid: ObjectId, tags: Dict[str, int], categories: Dict[str, int]):
        self.id = id
        self.user_oid = user_oid
        self.tags = tags
        self.categories = categories

    @property
    def dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_oid": str(self.user_oid),
            "tags": self.tags,
            "categories": self.categories,
        }

    @classmethod
    def from_dict(cls, data: dict):
        for field in ["_id", "user_oid", "tags", "categories"]:
            if field not in data:
                raise ValueError(f"Field {field} missing")
        return cls(data["_id"], data["user_oid"], data["tags"], data["categories"])
