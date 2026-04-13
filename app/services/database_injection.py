from injector import Module, Binder, singleton

from app.services.implementations.mongo_implementation import MongoDB
from app.services.model.database import Database


class DatabaseModule(Module):
    def __init__(self, connection_string: str, database: str):
        self.connection_string = connection_string
        self.database = database

    def configure(self, binder: Binder):
        binder.bind(
            Database,
            to=lambda: MongoDB(
                connection_string=self.connection_string, database=self.database
            ),
            scope=singleton
        )
