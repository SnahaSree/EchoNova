from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    id: str
    name: str
    entity_type: str
    description: str
    visibility: str
    owner_id: str
    score: float | None = None


class SearchResponse(BaseModel):
    query: str
    items: list[SearchResult]
    page: int
    page_size: int
    total: int
    has_next: bool

class SemanticSearchResponse(BaseModel):
    query: str
    items: list[SearchResult]