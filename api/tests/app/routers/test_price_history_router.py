from datetime import datetime, timezone
from uuid import uuid4

import pytest

from shared.database.models import PriceHistory, PriceHistoryInsert
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
