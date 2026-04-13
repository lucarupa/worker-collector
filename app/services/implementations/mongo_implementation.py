from typing import List

from pymongo import MongoClient

from app.services.model.database import Database, T


class MongoDB(Database):
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, connection_string: str, database: str):
        if not hasattr(self, "db"):
            self._client = MongoClient(connection_string)
            self.db = self.connect(database)

    def connect(self, database: str):
        return self._client[database]

    def get_database(self):
        return self.db

    def query(self, collection: str, query: dict) -> List[T]:
        connet = self.db[collection]
        results = connet.find(query)
        return results

    def save(self, collection: str, data: T):
        connet = self.db[collection]
        connet.insert_one(data.__dict__)

    def disconnect(self):
        if self._client:
            self._client.close()
            self._client = None
