from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.dependencies import get_current_user
from app.models.entity import EntityType
from app.schemas.entity import (
    EntityCreate,
    EntityListResponse,
    EntityPublic,
    EntityUpdate,
)
from app.services.entity_service import entity_service


router = APIRouter(
    prefix="/entities",
    tags=["Entities"],
)


CurrentUser = Annotated[
    dict,
    Depends(get_current_user),
]


@router.post(
    "",
    response_model=EntityPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_entity(
    data: EntityCreate,
    current_user: CurrentUser,
):
    entity_id = entity_service.create(
        data,
        str(current_user["_id"]),
    )

    entity = entity_service.get(
        entity_id,
        str(current_user["_id"]),
    )

    return _serialize_entity(entity)


@router.get(
    "",
    response_model=EntityListResponse,
)
def list_entities(
    current_user: CurrentUser,
    page: int = Query(
        default=1,
        ge=1,
    ),
    page_size: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    entity_type: EntityType | None = None,
):
    result = entity_service.list(
        current_user_id=str(current_user["_id"]),
        page=page,
        page_size=page_size,
        entity_type=(
            entity_type.value
            if entity_type
            else None
        ),
    )

    return {
        **result,
        "items": [
            _serialize_entity(entity)
            for entity in result["items"]
        ],
    }


@router.get(
    "/{entity_id}",
    response_model=EntityPublic,
)
def get_entity(
    entity_id: str,
    current_user: CurrentUser,
):
    entity = entity_service.get(
        entity_id,
        str(current_user["_id"]),
    )

    return _serialize_entity(entity)


@router.patch(
    "/{entity_id}",
    response_model=EntityPublic,
)
def update_entity(
    entity_id: str,
    data: EntityUpdate,
    current_user: CurrentUser,
):
    entity = entity_service.update(
        entity_id,
        data,
        str(current_user["_id"]),
    )

    return _serialize_entity(entity)


@router.delete(
    "/{entity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_entity(
    entity_id: str,
    current_user: CurrentUser,
):
    entity_service.delete(
        entity_id,
        str(current_user["_id"]),
    )


def _serialize_entity(entity: dict) -> dict:
    return {
        "id": str(entity["_id"]),
        "name": entity["name"],
        "entity_type": entity["entity_type"],
        "description": entity["description"],
        "visibility": entity["visibility"],
        "tags": entity.get("tags", []),
        "image_url": entity.get("image_url"),
        "owner_id": entity.get("owner_id"),
        "created_at": entity["created_at"],
        "updated_at": entity["updated_at"],
    }