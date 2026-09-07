from datetime import datetime, timezone
from typing import Any

from pymongo.collection import Collection

from app.database.connection import mongodb


class UserRepository:
    @property
    def collection(self) -> Collection:
        return mongodb.database["users"]

    def create(
        self,
        email: str,
        password_hash: str,
    ) -> str:
        now = datetime.now(timezone.utc)

        document = {
            "email": email.lower().strip(),
            "password_hash": password_hash,
            "role": "USER",
            "is_active": True,
            "created_at": now,
            "updated_at": now,
        }

        result = self.collection.insert_one(document)

        return str(result.inserted_id)

    def find_by_email(self, email: str) -> dict[str, Any] | None:
        return self.collection.find_one(
            {"email": email.lower().strip()}
        )

    def find_by_id(self, user_id: str) -> dict[str, Any] | None:
        from bson import ObjectId

        if not ObjectId.is_valid(user_id):
            return None

        return self.collection.find_one(
            {"_id": ObjectId(user_id)}
        )


user_repository = UserRepository()