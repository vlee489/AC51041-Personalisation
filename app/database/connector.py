"""Database Connector"""
from pymongo import MongoClient, DESCENDING
from typing import Dict, Any, Union, Optional, List
from pymongo.collection import Collection
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime
from .models.watchedFilm import WatchedFilm, WatchedFilmDict
from .models.recommendation import Recommendation, RecommendationDict


class Connector:
    """
    Database connector for Film info
    """
    __uri: str
    __database: str
    _client: MongoClient[Dict[str, Any]]
    _Watch: Collection[WatchedFilmDict]
    _Rec: Collection[RecommendationDict]

    def __init__(self, uri: str, database: str):
        """
        Init
        :param uri: Connection URI
        :return: None
        """
        self.__uri = uri
        self.__database = database
        self._client = MongoClient(self.__uri)
        self._db = self._client[self.__database]
        self._Watch = self._db.Watch
        self._Rec = self._db.Rec

    def add_film_pos(self, user_oid: str, film_id: str, pos: float):
        """
        Update film position
        :param user_oid:
        :param film_id:
        :param pos:
        :return: None
        """
        try:
            film_id = ObjectId(film_id)
            user_id = ObjectId(user_oid)
            self._Watch.update_one({
                "user_oid": user_id,
                "film_id": film_id
            }, {"$set": {
                "pos": pos,
                "date_time": datetime.utcnow()
            }}, upsert=True)
        except InvalidId:
            return None

    def remove_film_pos(self, user_oid: str, film_id: str):
        """
        Remove film pos
        :param user_oid:
        :param film_id:
        :return:
        """
        try:
            film_id = ObjectId(film_id)
            user_id = ObjectId(user_oid)
            self._Watch.delete_one({
                "user_oid": user_id,
                "film_id": film_id
            })
        except InvalidId:
            return None

    def get_to_continue_films(self, user_oid: str, limit: int = 3):
        """
        Get films users are to continue watching
        :param user_oid:
        :param limit:
        :return:
        """
        try:
            user_id = ObjectId(user_oid)
            films = self._Watch.find({"user_oid": user_id}).sort('datetime', DESCENDING).limit(limit)
            return [WatchedFilm.from_dict(f) for f in films]
        except InvalidId:
            return None

    def get_film_pos(self, user_oid: str, film_id: str):
        try:
            film_id = ObjectId(film_id)
            user_id = ObjectId(user_oid)
            film = self._Watch.find_one({
                "user_oid": user_id,
                "film_id": film_id
            })
            if film:
                return WatchedFilm.from_dict(film)
        except InvalidId:
            return None

    def update_rec(self, user_oid: str, tags: List[str], categories: List[str]):
        """
        Update user's recommendation
        :param user_oid:
        :param tags:
        :param categories:
        :return:
        """
        try:
            user_id = ObjectId(user_oid)
            update = {"$inc": {}}
            for tag in tags:
                update["$inc"][f"tags.{tag}"] = 1
            for category in categories:
                update["$inc"][f"tags.{category}"] = 1
            self._Rec.update_one({"user_oid": user_id}, update, upsert=True)
        except InvalidId:
            return None

    def get_recommendation(self, user_oid: str):
        """
        Get user's recommendation
        :param user_oid:
        :return:
        """
        try:
            user_id = ObjectId(user_oid)
            rec = self._Rec.find_one({"user_oid": user_id})
            if rec:
                return Recommendation.from_dict(rec)
        except InvalidId:
            return None

