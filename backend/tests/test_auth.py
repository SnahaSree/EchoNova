from fastapi.testclient import TestClient

from app.main import app


def test_register_validation():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": "invalid-email",
                "password": "123",
            },
        )

    assert response.status_code == 422