from fastapi import APIRouter

from app.api.v1 import (
    auth,
    entities,
    graph,
    relationships,
    users,
)


api_router = APIRouter(
    prefix="/api/v1",
)

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(entities.router)
api_router.include_router(
    relationships.router
)
api_router.include_router(graph.router)