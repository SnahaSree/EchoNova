from app.schemas.search import SearchResponse


def test_search_response_schema():
    response = SearchResponse(
        query="machine",
        items=[],
        page=1,
        page_size=20,
        total=0,
        has_next=False,
    )

    assert response.query == "machine"
    assert response.total == 0
    assert response.has_next is False


def test_search_response_rejects_invalid_page():
    try:
        SearchResponse(
            query="test",
            items=[],
            page=0,
            page_size=20,
            total=0,
            has_next=False,
        )
        assert False
    except Exception:
        assert True