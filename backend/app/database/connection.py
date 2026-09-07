from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import get_settings


class MongoDB:
    def __init__(self):
        self._client = None
        self._database = None

    def connect(self) -> None:
        settings = get_settings()

        self._client = MongoClient(
            settings.mongodb_uri,
            serverSelectionTimeoutMS=5000,
        )

        self._client.admin.command("ping")

        self._database = self._client[settings.database_name]

    def close(self) -> None:
        if self._client is not None:
            self._client.close()

        self._client = None
        self._database = None

    @property
    def client(self) -> MongoClient:
        if self._client is None:
            raise RuntimeError(
                "MongoDB client is not connected."
            )

        return self._client

    @property
    def database(self) -> Database:
        if self._database is None:
            raise RuntimeError(
                "MongoDB database is not connected."
            )

        return self._database


mongodb = MongoDB()