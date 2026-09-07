from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_current_user
from app.schemas.search import SearchResponse
from app.services.search_service import search_service


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.get(
    "",
    response_model=SearchResponse,
)
def search_entities(
    q: str = Query(
        min_length=1,
        max_length=200,
        description="Search query",
    ),
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    entity_type: str | None = Query(
        default=None,
    ),
    current_user: dict = Depends(get_current_user),
):
    try:
        return search_service.search(
            query=q,
            current_user_id=current_user["id"],
            page=page,
            page_size=page_size,
            entity_type=entity_type,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc