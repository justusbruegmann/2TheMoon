from datetime import datetime, timezone
from uuid import uuid4

import pytest

from shared.database.models import Asset, AssetInsert, PriceHistory, PriceHistoryInsert
from .conftest import FakeTable, GAMESERVER_HEADERS, VALID_HEADERS, client, override_user_db

VALID_PAYLOAD = {
        "season_id": str(uuid4()),
        "asset_id": str(uuid4()),
        "open": "1.0",
        "close": "1.5",
        "high": "2.0",
        "low": "0.5",
}
NEWLY_CREATED_PRICE_HISTORY_ID = None


class FakeDatabase:
    def __init__(self):
        self.price_history = FakeTable(PriceHistory, lambda: {"recorded_at": datetime.now(timezone.utc)})
        self.assets = FakeTable(Asset, lambda: {"id": uuid4(), "created_at": datetime.now(timezone.utc)})


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

    with override_user_db(db):
        yield db


###################
# Unit Tests
###################

def test_get_all(fake_db):
    response = client.get("/price_history/", headers=VALID_HEADERS)
    assert response.status_code == 200


def test_get_all_includes_entry_overlapping_window():
    recorded_at = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    db = FakeDatabase()
    db.price_history = FakeTable(PriceHistory, lambda: {"recorded_at": recorded_at})
    db.price_history.insert(PriceHistoryInsert(**VALID_PAYLOAD))

    with override_user_db(db):
        # candle covers [11:55, 12:00]; query window [11:58, 11:59] overlaps it
        response = client.get(
            "/price_history/",
            params={"start": "2024-01-01T11:58:00Z", "end": "2024-01-01T11:59:00Z"},
            headers=VALID_HEADERS,
        )
    assert len(response.json()["data"]) == 1


def test_get_all_excludes_entry_outside_window():
    recorded_at = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
    db = FakeDatabase()
    db.price_history = FakeTable(PriceHistory, lambda: {"recorded_at": recorded_at})
    db.price_history.insert(PriceHistoryInsert(**VALID_PAYLOAD))

    with override_user_db(db):
        # candle covers [11:55, 12:00]; query window [10:00, 11:00] is fully before it
        response = client.get(
            "/price_history/",
            params={"start": "2024-01-01T10:00:00Z", "end": "2024-01-01T11:00:00Z"},
            headers=VALID_HEADERS,
        )
    assert response.json()["data"] == []


def test_get_all_filters_by_ticker():
    db = FakeDatabase()
    asset = db.assets.insert(AssetInsert(ticker="MOON", name="2TheMoon AG", kind="stock"))[0]
    db.price_history.insert(PriceHistoryInsert(**{**VALID_PAYLOAD, "asset_id": str(asset.id)}))
    db.price_history.insert(PriceHistoryInsert(**VALID_PAYLOAD))  # unrelated asset, should not match

    with override_user_db(db):
        response = client.get("/price_history/", params={"ticker": "MOON"}, headers=VALID_HEADERS)

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["asset_id"] == str(asset.id)


def test_get_all_unknown_ticker():
    db = FakeDatabase()
    with override_user_db(db):
        response = client.get("/price_history/", params={"ticker": "DOES_NOT_EXIST"}, headers=VALID_HEADERS)
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
