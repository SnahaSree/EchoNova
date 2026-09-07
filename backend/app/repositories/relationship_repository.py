from datetime import datetime, timezone
from typing import Any

from bson import ObjectId
from pymongo.collection import Collection

from app.database.connection import mongodb


class RelationshipRepository:
    @property
    def collection(self) -> Collection:
        return mongodb.database["relationships"]

    def create(
        self,
        document: dict[str, Any],
    ) -> str:
        result = self.collection.insert_one(document)

        return str(result.inserted_id)

    def find_by_id(
        self,
        relationship_id: str,
    ) -> dict[str, Any] | None:
        if not ObjectId.is_valid(relationship_id):
            return None

        return self.collection.find_one(
            {"_id": ObjectId(relationship_id)}
        )

    def find_existing(
        self,
        source_entity_id: str,
        target_entity_id: str,
        relationship_type: str,
    ) -> dict[str, Any] | None:
        return self.collection.find_one(
            {
                "source_entity_id": source_entity_id,
                "target_entity_id": target_entity_id,
                "relationship_type": relationship_type,
            }
        )

    def find_related(
        self,
        entity_id: str,
    ) -> list[dict[str, Any]]:
        return list(
            self.collection.find(
                {
                    "$or": [
                        {"source_entity_id": entity_id},
                        {"target_entity_id": entity_id},
                    ]
                }
            )
        )

    def delete(
        self,
        relationship_id: str,
    ) -> bool:
        if not ObjectId.is_valid(relationship_id):
            return False

        result = self.collection.delete_one(
            {"_id": ObjectId(relationship_id)}
        )

        return result.deleted_count == 1

    def update_timestamp(
        self,
        relationship_id: str,
    ) -> None:
        if not ObjectId.is_valid(relationship_id):
            return

        self.collection.update_one(
            {"_id": ObjectId(relationship_id)},
            {
                "$set": {
                    "updated_at": datetime.now(
                        timezone.utc
                    )
                }
            },
        )


relationship_repository = RelationshipRepository()