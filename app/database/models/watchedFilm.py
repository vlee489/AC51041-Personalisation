"""Model that defines a watched film"""
from typing import List, Dict, Union, TypedDict
from bson import ObjectId
from datetime import datetime


class WatchedFilmDict(TypedDict):
    id: ObjectId
    user_oid: ObjectId
    film_id: ObjectId
    pos: float
    date_time: datetime


class WatchedFilm:
    id: ObjectId
    user_oid: ObjectId
    film_id: ObjectId
    pos: float
    date_time: datetime

    def __init__(self, id: ObjectId, user_oid: ObjectId, film_id: ObjectId, pos: float, date_time: datetime):
        self.id = id
        self.user_oid = user_oid
        self.film_id = film_id
        self.pos = pos
        self.date_time = date_time

    @property
    def dict(self) -> dict:
        return {
            "id": str(self.id),
            "user_oid": str(self.user_oid),
            "film_id": str(self.film_id),
            "pos": self.pos,
            "date_time": self.date_time
        }

    @classmethod
    def from_dict(cls, data: dict):
        for field in ["_id", "user_oid", "film_id", "pos", "date_time"]:
            if field not in data:
                raise ValueError(f"Field {field} missing")
        return cls(data["_id"], data["user_oid"], data["film_id"], data["pos"], data["date_time"])
