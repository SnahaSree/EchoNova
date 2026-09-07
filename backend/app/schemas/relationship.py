from datetime import datetime

from pydantic import BaseModel, Field

from app.models.relationship import RelationshipType


class RelationshipCreate(BaseModel):
    source_entity_id: str = Field(min_length=1)
    target_entity_id: str = Field(min_length=1)
    relationship_type: RelationshipType
    description: str = Field(
        default="",
        max_length=2000,
    )
    strength: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
    )


class RelationshipPublic(BaseModel):
    id: str
    source_entity_id: str
    target_entity_id: str
    relationship_type: RelationshipType
    description: str
    strength: float
    created_at: datetime
    updated_at: datetime


class GraphNode(BaseModel):
    id: str
    name: str
    entity_type: str


class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    relationship_type: RelationshipType
    strength: float


class GraphResponse(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]