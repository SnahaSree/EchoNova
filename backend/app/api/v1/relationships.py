from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.api.dependencies import get_current_user
from app.schemas.relationship import (
    RelationshipCreate,
    RelationshipPublic,
)
from app.services.relationship_service import (
    relationship_service,
)


router = APIRouter(
    prefix="/relationships",
    tags=["Relationships"],
)


CurrentUser = Annotated[
    dict,
    Depends(get_current_user),
]


@router.post(
    "",
    response_model=RelationshipPublic,
    status_code=status.HTTP_201_CREATED,
)
def create_relationship(
    data: RelationshipCreate,
    current_user: CurrentUser,
):
    relationship = relationship_service.create(
        data,
        str(current_user["_id"]),
    )

    return _serialize_relationship(
        relationship
    )


@router.get(
    "/entity/{entity_id}",
    response_model=list[RelationshipPublic],
)
def get_related_relationships(
    entity_id: str,
    current_user: CurrentUser,
):
    relationships = (
        relationship_service.get_related(
            entity_id,
            str(current_user["_id"]),
        )
    )

    return [
        _serialize_relationship(item)
        for item in relationships
    ]


@router.delete(
    "/{relationship_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_relationship(
    relationship_id: str,
    current_user: CurrentUser,
):
    relationship_service.delete(
        relationship_id,
        str(current_user["_id"]),
    )


def _serialize_relationship(
    relationship: dict,
) -> dict:
    return {
        "id": str(relationship["_id"]),
        "source_entity_id": (
            relationship["source_entity_id"]
        ),
        "target_entity_id": (
            relationship["target_entity_id"]
        ),
        "relationship_type": (
            relationship["relationship_type"]
        ),
        "description": relationship.get(
            "description",
            "",
        ),
        "strength": relationship.get(
            "strength",
            1.0,
        ),
        "created_at": relationship[
            "created_at"
        ],
        "updated_at": relationship[
            "updated_at"
        ],
    }