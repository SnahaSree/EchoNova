from app.schemas.search import SemanticSearchResponse


class SemanticSearchService:

    def search(
        self,
        query: str,
        current_user_id: str,
    ) -> SemanticSearchResponse:

        raise NotImplementedError(
            "Semantic search provider is not configured yet."
        )


semantic_search_service = SemanticSearchService()