from datetime import datetime, timezone

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_user_db
from app.main import app
from shared.database import DatabaseError
from shared.database.models.test import Test


client = TestClient(app)

VALID_HEADERS = {"Authorization": "Bearer test-token"}
VALID_PAYLOAD = {
    "number": 3,
    "bool": True,
    "text": "Hello World! (or Foo Bar as python nerds would say)",
    "timestamptz": datetime.now(timezone.utc).isoformat()
}
NEWLY_CREATED_ROW_ID = None


class FakeTestTable:
    """In-memory stand-in for shared.database.Table(Test), scoped to one test."""

    def __init__(self):
        self._rows: dict[int, Test] = {}
        self._next_id = 1

    def find(self, **_filters):
        return list(self._rows.values())

    def get(self, **filters):
        return self._rows.get(filters["id"])

    def insert(self, *rows):
        created = []
        for row in rows:
            test_row = Test(id=self._next_id, created_at=datetime.now(timezone.utc), **row.model_dump())
            self._rows[self._next_id] = test_row
            created.append(test_row)
            self._next_id += 1
        return created

    def update(self, values, **filters):
        row = self._rows.get(filters["id"])
        if row is None:
            return []
        updated = row.model_copy(update=values)
        self._rows[filters["id"]] = updated
        return [updated]

    def delete(self, **filters):
        row = self._rows.pop(filters["id"], None)
        return [row] if row else []


class FakeDatabase:
    def __init__(self):
        self.test = FakeTestTable()


class UnreachableDatabase:
    """Simulates a Supabase/network failure so routes' except DatabaseError paths are exercised."""

    class _FailingTable:
        def __getattr__(self, _name):
            def _raise(*_args, **_kwargs):
                raise DatabaseError("simulated outage")
            return _raise

    test = _FailingTable()


@pytest.fixture(scope="module")
def fake_db():
    """Overrides get_user_db for the rest of this module so routes hit an
    in-memory table instead of Supabase. Not autouse: the auth-boundary tests
    below need the real dependency (incl. HTTPBearer) to still run."""
    db = FakeDatabase()
    app.dependency_overrides[get_user_db] = lambda: db
    yield db
    app.dependency_overrides.pop(get_user_db, None)


def test_get_database_rejects_missing_token():
    response = client.get("/test/database")
    assert response.status_code == 401


def test_get_database_rejects_non_bearer_scheme():
    response = client.get("/test/database", headers={"Authorization": "Basic wrong"})
    assert response.status_code == 401


def test_get_database_returns_503_when_db_unreachable():
    app.dependency_overrides[get_user_db] = lambda: UnreachableDatabase()
    try:
        response = client.get("/test/database", headers=VALID_HEADERS)
    finally:
        app.dependency_overrides.pop(get_user_db, None)
    assert response.status_code == 503


def test_get_database_reachable_with_valid_token(fake_db):
    response = client.get("/test/database", headers=VALID_HEADERS)

    assert response.status_code == 200
    json = response.json()
    assert json is not None and json.get("success") is True


# CRUD operations against the fake in-memory table
def test_post_valid_payload(fake_db):
    response = client.post("/test/database", json=VALID_PAYLOAD, headers=VALID_HEADERS)
    assert response.status_code == 201
    # Store newly created id to be referenced in other tests
    r = response.json()
    global NEWLY_CREATED_ROW_ID
    NEWLY_CREATED_ROW_ID = r["data"]["id"]

def test_post_invalid_payload(fake_db):
    response = client.post("/test/database", json={"number": "asdf"}, headers=VALID_HEADERS)
    assert response.status_code == 422

def test_get_one_valid_id(fake_db):
    if NEWLY_CREATED_ROW_ID is None:
        pytest.skip("NEWLY_CREATED_ROW_ID is None")
    response = client.get(f"/test/database/{NEWLY_CREATED_ROW_ID}", headers=VALID_HEADERS)
    assert response.status_code == 200

def test_get_one_invalid_id(fake_db):
    response = client.get("/test/database/-1", headers=VALID_HEADERS)
    assert response.status_code == 404

def test_patch_valid_payload(fake_db):
    if NEWLY_CREATED_ROW_ID is None:
        pytest.skip("NEWLY_CREATED_ROW_ID is None")
    response = client.patch(f"/test/database/{NEWLY_CREATED_ROW_ID}", json={"number": 123}, headers=VALID_HEADERS)
    assert response.status_code == 200
    assert response.json()["data"]["number"] == 123

def test_patch_invalid_payload(fake_db):
    if NEWLY_CREATED_ROW_ID is None:
        pytest.skip("NEWLY_CREATED_ROW_ID is None")
    response = client.patch(f"/test/database/{NEWLY_CREATED_ROW_ID}", json={"number": "asdf"}, headers=VALID_HEADERS)
    assert response.status_code == 422


def test_delete_valid_id(fake_db):
    if NEWLY_CREATED_ROW_ID is None:
        pytest.skip("NEWLY_CREATED_ROW_ID is None")
    response = client.delete(f"/test/database/{NEWLY_CREATED_ROW_ID}", headers=VALID_HEADERS)
    assert response.status_code == 200


def test_delete_invalid_id(fake_db):
    if NEWLY_CREATED_ROW_ID is None:
        pytest.skip("NEWLY_CREATED_ROW_ID is None")
    response = client.delete(f"/test/database/{NEWLY_CREATED_ROW_ID}", headers=VALID_HEADERS)
    assert response.status_code == 404
