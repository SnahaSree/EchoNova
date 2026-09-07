from app.repositories.search_repository import search_repository
from app.schemas.search import SearchResponse, SearchResult


class SearchService:

    def search(
        self,
        query: str,
        current_user_id: str,
        page: int = 1,
        page_size: int = 20,
        entity_type: str | None = None,
    ) -> SearchResponse:

        query = query.strip()

        if not query:
            raise ValueError("Search query cannot be empty.")

        items = search_repository.search(
            query=query,
            current_user_id=current_user_id,
            page=page,
            page_size=page_size,
            entity_type=entity_type,
        )

        total = search_repository.count(
            query=query,
            current_user_id=current_user_id,
            entity_type=entity_type,
        )

        results = [
            SearchResult(
                id=str(item["_id"]),
                name=item["name"],
                entity_type=item["entity_type"],
                description=item.get("description", ""),
                visibility=item["visibility"],
                owner_id=item["owner_id"],
            )
            for item in items
        ]

        return SearchResponse(
            query=query,
            items=results,
            page=page,
            page_size=page_size,
            total=total,
            has_next=(page * page_size) < total,
        )


search_service = SearchService()