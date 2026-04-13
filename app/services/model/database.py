from abc import ABC, abstractmethod
from typing import TypeVar, List

T = TypeVar("T")


class Database(ABC):
    @abstractmethod
    def connect(self, database: str):
        pass

    def get_database(self):
        pass

    @abstractmethod
    def query(self, collection: str, query: dict) -> List[T]:
        pass

    @abstractmethod
    def save(self, collection: str, data: T):
        pass

    @abstractmethod
    def disconnect(self):
        pass
