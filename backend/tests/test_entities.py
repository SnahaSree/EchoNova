from pydantic import ValidationError

from app.schemas.entity import EntityCreate


def test_entity_name_required():
    try:
        EntityCreate(
            entity_type="concept",
            description="test",
        )
    except ValidationError:
        return

    raise AssertionError(
        "Expected validation error."
    )


def test_entity_name_length_limit():
    try:
        EntityCreate(
            name="A" * 201,
            entity_type="concept",
        )
    except ValidationError:
        return

    raise AssertionError(
        "Expected validation error."
    )