from pydantic import ValidationError

from app.schemas.relationship import (
    RelationshipCreate,
)


def test_relationship_strength_range():
    try:
        RelationshipCreate(
            source_entity_id="a",
            target_entity_id="b",
            relationship_type="related_to",
            strength=1.5,
        )
    except ValidationError:
        return

    raise AssertionError(
        "Expected validation error."
    )


def test_relationship_ids_required():
    try:
        RelationshipCreate(
            source_entity_id="",
            target_entity_id="b",
            relationship_type="related_to",
        )
    except ValidationError:
        return

    raise AssertionError(
        "Expected validation error."
    )