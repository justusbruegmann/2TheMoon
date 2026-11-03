from datetime import datetime, timezone
from uuid import uuid4

import pytest

from shared.database.models import Asset, AssetInsert
from .conftest import FakeTable, VALID_HEADERS, client, override_user_db


VALID_PAYLOAD = {
        "ticker": "MOON",
        "name": "2TheMoon AG",
        "kind": "stock",
}
NEWLY_CREATED_ASSET_ID = None


class FakeDatabase:
    def __init__(self):
        self.assets = FakeTable(Asset, lambda: {"id": uuid4(), "created_at": datetime.now(timezone.utc)})


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for this module.
    # The auth-boundary tests below need the real dependency (incl. HTTPBearer) to still run.
    ################################################
    db = FakeDatabase()

    # Add a row to the table to be retrieved in a GET request
    new_row = db.assets.insert(AssetInsert(**VALID_PAYLOAD))[0]
    global NEWLY_CREATED_ASSET_ID
    NEWLY_CREATED_ASSET_ID = str(new_row.id)

    with override_user_db(db):
        yield db


###################
# Unit Tests
###################

# def test_post_valid_payload(fake_db):
#     response = client.post("/assets/", json=VALID_PAYLOAD, headers=VALID_HEADERS)
#     assert response.status_code == 201
#     # Store newly created id to be referenced in other tests
#     r = response.json()
#     global NEWLY_CREATED_ASSET_ID
#     NEWLY_CREATED_ASSET_ID = r["data"]["id"]
#
#
# def test_post_invalid_payload(fake_db):
#     response = client.post("/assets/", json={"ticker": "AAPL"}, headers=VALID_HEADERS)
#     assert response.status_code == 422


def test_get_one_valid_id(fake_db):
    response = client.get(f"/assets/{NEWLY_CREATED_ASSET_ID}", headers=VALID_HEADERS)
    assert response.status_code == 200


def test_get_one_invalid_id(fake_db):
    response = client.get(f"/assets/{uuid4()}", headers=VALID_HEADERS)
    assert response.status_code == 404

# def test_patch_valid_payload(fake_db):
#     response = client.patch(
#         f"/assets/{NEWLY_CREATED_ASSET_ID}",
#         json={**VALID_PAYLOAD, "ticker": "AAPL2"},
#         headers=VALID_HEADERS,
#     )
#     assert response.status_code == 200
#     assert response.json()["data"]["ticker"] == "AAPL2"
#
#
# def test_patch_invalid_payload(fake_db):
#     response = client.patch(f"/assets/{NEWLY_CREATED_ASSET_ID}", json={"kind": "wrong"}, headers=VALID_HEADERS)
#     assert response.status_code == 422
#
#
# def test_delete_valid_id(fake_db):
#     response = client.delete(f"/assets/{NEWLY_CREATED_ASSET_ID}", headers=VALID_HEADERS)
#     assert response.status_code == 204
#
#
# def test_delete_invalid_id(fake_db):
#     response = client.delete(f"/assets/{uuid4()}", headers=VALID_HEADERS)
#     assert response.status_code == 404
