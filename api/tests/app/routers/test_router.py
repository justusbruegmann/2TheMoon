from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

VALID_HEADERS = {"token-name": "my-secret"}


def test_get_test_reachable_with_valid_token():
    response = client.get("/test/database", headers=VALID_HEADERS)

    assert response.status_code == 200
    json = response.json()
    assert json is not None and json.get("success") is True


def test_get_test_rejects_missing_token():
    response = client.get("/test/database")

    assert response.status_code == 422


def test_get_test_rejects_invalid_token():
    response = client.get("/test/database", headers={"token-name": "wrong"})

    assert response.status_code == 400
