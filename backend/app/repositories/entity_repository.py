from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo.collection import Collection

from app.database.connection import mongodb


class EntityRepository:
    @property
    def collection(self) -> Collection:
        return mongodb.database["entities"]

    def create(
        self,
        document: dict[str, Any],
    ) -> str:
        result = self.collection.insert_one(document)
        return str(result.inserted_id)

    def find_by_id(
        self,
        entity_id: str,
    ) -> dict[str, Any] | None:
        if not ObjectId.is_valid(entity_id):
            return None

        return self.collection.find_one(
            {"_id": ObjectId(entity_id)}
        )

    def update(
        self,
        entity_id: str,
        updates: dict[str, Any],
    ) -> dict[str, Any] | None:
        if not ObjectId.is_valid(entity_id):
            return None

        updates["updated_at"] = datetime.now(timezone.utc)

        return self.collection.find_one_and_update(
            {"_id": ObjectId(entity_id)},
            {"$set": updates},
            return_document=True,
        )

    def delete(
        self,
        entity_id: str,
    ) -> bool:
        if not ObjectId.is_valid(entity_id):
            return False

        result = self.collection.delete_one(
            {"_id": ObjectId(entity_id)}
        )

        return result.deleted_count == 1

    def count(
        self,
        current_user_id: str,
        entity_type: str | None = None,
    ) -> int:
        query: dict[str, Any] = {
            "$or": [
                {"visibility": "public"},
                {"owner_id": current_user_id},
            ]
        }

        if entity_type:
            query["entity_type"] = entity_type

        return self.collection.count_documents(query)

    def list_entities(
        self,
        skip: int,
        limit: int,
        current_user_id: str,
        entity_type: str | None = None,
    ) -> list[dict[str, Any]]:
        query: dict[str, Any] = {
            "$or": [
                {"visibility": "public"},
                {"owner_id": current_user_id},
            ]
        }

        if entity_type:
            query["entity_type"] = entity_type

        cursor = (
            self.collection
            .find(query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(limit)
        )

        return list(cursor)


entity_repository = EntityRepository()