from asyncio import log
from datetime import datetime, timezone
from email import header

import pytest
from fastapi.testclient import TestClient

from app.main import app



client = TestClient(app)

VALID_HEADERS = {
    "token-name": "my-secret"
}
VALID_PAYLOAD = {
    "number": 3,
    "bool": True,
    "text": "Hello World! (or Foo Bar as python nerds would say)",
    "timestamptz": datetime.now(timezone.utc).isoformat()
}
NEWLY_CREATED_ROW_ID = None


def test_get_database_reachable_with_valid_token():
    response = client.get("/test/database", headers=VALID_HEADERS)

    assert response.status_code == 200
    json = response.json()
    assert json is not None and json.get("success") is True


def test_get_database_rejects_missing_token():
    response = client.get("/test/database")

    assert response.status_code == 422


def test_get_database_rejects_invalid_token():
    response = client.get("/test/database", headers={"token-name": "wrong"})

    assert response.status_code == 400


# CRUD operations on the live table
def test_post_valid_payload():
    response = client.post("/test/database", json=VALID_PAYLOAD, headers=VALID_HEADERS)
    assert response.status_code == 201
    # Store newly created id to be referenced in other tests
    r = response.json()
    print(r)
    global NEWLY_CREATED_ROW_ID
    NEWLY_CREATED_ROW_ID = r["data"]["id"]
    print(NEWLY_CREATED_ROW_ID)

def test_post_invalid_payload():
    response = client.post("/test/database", json={"number": "asdf"}, headers=VALID_HEADERS)
    assert response.status_code == 422

def test_get_one_valid_id():
    if NEWLY_CREATED_ROW_ID is None:
        pytest.skip("No row was created yet")
    response = client.get(f"/test/database/${NEWLY_CREATED_ROW_ID}", headers=VALID_HEADERS)
    assert response.status_code == 200

def test_get_one_invalid_id():
    response = client.get("/test/database/-1", headers=VALID_HEADERS)
    assert response.status_code == 404
