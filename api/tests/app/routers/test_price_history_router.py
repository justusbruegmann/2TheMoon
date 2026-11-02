from datetime import datetime, timezone
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.dependencies import get_user_db
from app.main import app
from shared.database.models import PriceHistory, PriceHistoryInsert



client = TestClient(app)

VALID_HEADERS = {"Authorization": "Bearer test-token"}
GAMESERVER_HEADERS = {**VALID_HEADERS, "Authorization_Gameserver": settings.gameserver_shared_secret}
VALID_PAYLOAD = {
    "season_id": str(uuid4()),
    "asset_id": str(uuid4()),
    "open": "1.0",
    "close": "1.5",
    "high": "2.0",
    "low": "0.5",
}
NEWLY_CREATED_PRICE_HISTORY_ID = None


class FakePriceHistoryTable:
    #################################
    # Fixture that simulates the price_history table
    #################################
    def __init__(self):
        self._rows: dict[str, PriceHistory] = {}

    def find(self, **_filters):
        return list(self._rows.values())

    def get(self, **filters):
        return self._rows.get(str(filters["id"]))

    def insert(self, *rows):
        created = []
        for row in rows:
            entry = PriceHistory(recorded_at=datetime.now(timezone.utc), **row.model_dump(exclude={"recorded_at"}))
            self._rows[str(uuid4())] = entry
            created.append(entry)
        return created


class FakeDatabase:
    def __init__(self):
        self.price_history = FakePriceHistoryTable()


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for this module.
    # The auth-boundary tests below need the real dependency (incl. HTTPBearer) to still run.
    ################################################
    db = FakeDatabase()

    # Add a row to the table to be retrieved in a GET request
    db.price_history.insert(PriceHistoryInsert(**VALID_PAYLOAD))
    global NEWLY_CREATED_PRICE_HISTORY_ID
    NEWLY_CREATED_PRICE_HISTORY_ID = next(iter(db.price_history._rows))

    app.dependency_overrides[get_user_db] = lambda: db
    yield db
    app.dependency_overrides.pop(get_user_db, None)


###################
# Unit Tests
###################

def test_get_all(fake_db):
    response = client.get("/price_history/", headers=VALID_HEADERS)
    assert response.status_code == 200


def test_get_one_valid_id(fake_db):
    response = client.get(f"/price_history/{NEWLY_CREATED_PRICE_HISTORY_ID}", headers=VALID_HEADERS)
    assert response.status_code == 200


def test_get_one_invalid_id(fake_db):
    response = client.get(f"/price_history/{uuid4()}", headers=VALID_HEADERS)
    assert response.status_code == 404


def test_post_valid_payload(fake_db):
    response = client.post("/price_history/", json=VALID_PAYLOAD, headers=GAMESERVER_HEADERS)
    assert response.status_code == 201


def test_post_invalid_payload(fake_db):
    response = client.post("/price_history/", json={"asset_id": str(uuid4())}, headers=GAMESERVER_HEADERS)
    assert response.status_code == 422


def test_post_missing_gameserver_auth(fake_db):
    response = client.post("/price_history/", json=VALID_PAYLOAD, headers=VALID_HEADERS)
    assert response.status_code == 401
