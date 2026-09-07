from typing import Any

from app.database.connection import mongodb


class SearchRepository:

    @property
    def collection(self):
        return mongodb.database["entities"]

    def search(
        self,
        query: str,
        current_user_id: str,
        page: int,
        page_size: int,
        entity_type: str | None = None,
    ) -> list[dict[str, Any]]:

        authorized_query: dict[str, Any] = {
            "$or": [
                {"visibility": "public"},
                {"owner_id": current_user_id},
            ]
        }

        if entity_type:
            authorized_query["entity_type"] = entity_type

        regex = {
            "$regex": query,
            "$options": "i",
        }

        search_query = {
            "$and": [
                authorized_query,
                {
                    "$or": [
                        {"name": regex},
                        {"description": regex},
                        {"tags": regex},
                    ]
                },
            ]
        }

        skip = (page - 1) * page_size

        return list(
            self.collection
            .find(search_query)
            .sort("created_at", -1)
            .skip(skip)
            .limit(page_size)
        )

    def count(
        self,
        query: str,
        current_user_id: str,
        entity_type: str | None = None,
    ) -> int:

        authorized_query: dict[str, Any] = {
            "$or": [
                {"visibility": "public"},
                {"owner_id": current_user_id},
            ]
        }

        if entity_type:
            authorized_query["entity_type"] = entity_type

        regex = {
            "$regex": query,
            "$options": "i",
        }

        search_query = {
            "$and": [
                authorized_query,
                {
                    "$or": [
                        {"name": regex},
                        {"description": regex},
                        {"tags": regex},
                    ]
                },
            ]
        }

        return self.collection.count_documents(search_query)


search_repository = SearchRepository()