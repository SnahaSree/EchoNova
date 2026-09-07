from collections import deque

from fastapi import HTTPException, status

from app.repositories.entity_repository import (
    entity_repository,
)
from app.repositories.relationship_repository import (
    relationship_repository,
)
from app.schemas.relationship import (
    GraphEdge,
    GraphNode,
    GraphResponse,
)


class GraphService:
    def build_graph(
        self,
        root_entity_id: str,
        current_user_id: str,
        depth: int = 1,
    ) -> GraphResponse:
        if depth < 1 or depth > 3:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Graph depth must be between 1 and 3.",
            )

        root = entity_repository.find_by_id(
            root_entity_id
        )

        if not root:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Entity not found.",
            )

        self._check_access(
            root,
            current_user_id,
        )

        nodes: dict[str, GraphNode] = {}
        edges: dict[str, GraphEdge] = {}

        queue = deque(
            [(root_entity_id, 0)]
        )

        visited: set[str] = {
            root_entity_id
        }

        nodes[root_entity_id] = (
            self._to_node(root)
        )

        while queue:
            current_id, current_depth = (
                queue.popleft()
            )

            if current_depth >= depth:
                continue

            relationships = (
                relationship_repository.find_related(
                    current_id
                )
            )

            for relationship in relationships:
                source_id = relationship[
                    "source_entity_id"
                ]

                target_id = relationship[
                    "target_entity_id"
                ]

                next_id = (
                    target_id
                    if source_id == current_id
                    else source_id
                )

                next_entity = (
                    entity_repository.find_by_id(
                        next_id
                    )
                )

                if not next_entity:
                    continue

                try:
                    self._check_access(
                        next_entity,
                        current_user_id,
                    )
                except HTTPException:
                    continue

                relationship_id = str(
                    relationship["_id"]
                )

                if relationship_id not in edges:
                    edges[relationship_id] = (
                        GraphEdge(
                            id=relationship_id,
                            source=source_id,
                            target=target_id,
                            relationship_type=(
                                relationship[
                                    "relationship_type"
                                ]
                            ),
                            strength=relationship.get(
                                "strength",
                                1.0,
                            ),
                        )
                    )

                if next_id not in visited:
                    visited.add(next_id)

                    nodes[next_id] = (
                        self._to_node(
                            next_entity
                        )
                    )

                    queue.append(
                        (
                            next_id,
                            current_depth + 1,
                        )
                    )

        return GraphResponse(
            nodes=list(nodes.values()),
            edges=list(edges.values()),
        )

    @staticmethod
    def _to_node(
        entity: dict,
    ) -> GraphNode:
        return GraphNode(
            id=str(entity["_id"]),
            name=entity["name"],
            entity_type=entity["entity_type"],
        )

    @staticmethod
    def _check_access(
        entity: dict,
        current_user_id: str,
    ) -> None:
        if (
            entity.get("visibility")
            == "public"
        ):
            return

        if (
            entity.get("owner_id")
            == current_user_id
        ):
            return

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Entity not found.",
        )


graph_service = GraphService()