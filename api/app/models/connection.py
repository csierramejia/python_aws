import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from urllib.parse import quote_plus
from bson.objectid import ObjectId


class DBConnection(object):
    _instance = None

    class Singleton:
        def __init__(self):
            # uri = "mongodb://%s" % ("192.168.55.2:27017/appMovil?retryWrites=false")
            uri = "mongodb://%s:%s@%s" % (
                 quote_plus("appMovil"),
                 quote_plus("qwerty123"),
                 "54.156.37.79:27017/admin?retryWrites=false",
            )

            self.connection = MongoClient(uri)["appMovil"]

    def __init__(self):
        if DBConnection._instance is None:
            DBConnection._instance = DBConnection.Singleton()

    def __getattr__(self, attr):
        return getattr(self._instance, attr)

    def __setattr__(self, attr, value):
        return setattr(self._instance, attr, value)


class Manager:
    @property
    def collection(self):
        return self._collection

    @collection.setter
    def collection(self, value):
        self._collection = value

    def get_connection(self):
        return DBConnection().connection[self.collection]

    def update(self, match, info_update={}, upsert=False):
        if not isinstance(info_update, dict):
            return {"error": {"message": "Update Information not defined"}}

        _id = match.get("_id", "")
        if _id != "":
            match["_id"] = ObjectId(_id)

        connection = self.get_connection()
        connection.update_one(match, {"$set": info_update}, upsert=upsert)
        return "Information Processed Correctly"

    def insert(self, info_insert):
        connection = self.get_connection()
        _insert = connection.insert(info_insert)
        response = str(_insert)
        return response

    def insert_many(self, info_insert):
        connection = self.get_connection()
        _insert = connection.insert_many(info_insert)
        response = str(_insert.inserted_ids)
        return response

    def delete_many(self, match):
        connection = self.get_connection()
        result = connection.delete_many(match)
        return ("delete count:", result.deleted_count)
        # return "Information Deleted Correctly"

    def delete_one(self, match):
        connection = self.get_connection()
        connection.delete_one(match)
        return "Information Deleted Correctly"

    def execute(self, query=[]):
        response = []
        if not isinstance(query, list):
            return {"error": {"message": "Query not defined"}}

        connection = self.get_connection()
        result = connection.aggregate(query)
        for info in result:
            _id = info.get("_id", "")
            if _id != "":
                info["_id"] = str(_id)
            response.append(info)

        return response
