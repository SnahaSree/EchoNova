from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_current_user
from app.schemas.relationship import GraphResponse
from app.services.graph_service import graph_service


router = APIRouter(
    prefix="/graph",
    tags=["Knowledge Graph"],
)


CurrentUser = Annotated[
    dict,
    Depends(get_current_user),
]


@router.get(
    "/{entity_id}",
    response_model=GraphResponse,
)
def get_graph(
    entity_id: str,
    current_user: CurrentUser,
    depth: int = Query(
        default=1,
        ge=1,
        le=3,
    ),
):
    return graph_service.build_graph(
        root_entity_id=entity_id,
        current_user_id=str(
            current_user["_id"]
        ),
        depth=depth,
    )