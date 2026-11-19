from uuid import uuid4

import pytest
from shared.database.models import Holding

from .conftest import FakeTable, VALID_HEADERS, client, override_user_db

USER_ID = uuid4()
PORTFOLIO_ID = str(uuid4())
ASSET_A = uuid4()
ASSET_B = uuid4()
HOLDING_A = {"portfolio_id": PORTFOLIO_ID, "asset_id": str(ASSET_A), "quantity": "1.5"}
HOLDING_B = {"portfolio_id": PORTFOLIO_ID, "asset_id": str(ASSET_B), "quantity": "2"}


class FakeDatabase:
    def __init__(self):
        self.holdings = FakeTable(Holding, lambda: {"id": uuid4(), "user_id": USER_ID})


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for this module.
    # The auth-boundary tests below need the real dependency (incl. HTTPBearer) to still run.
    ################################################
    db = FakeDatabase()

    # One holding per asset the user bought, so the GET returns a list of two
    db.holdings.insert(Holding(**HOLDING_A), Holding(**HOLDING_B))

    with override_user_db(db):
        yield db


###################
# Unit Tests
###################

def test_get_all_holdings_returns_list(fake_db):
    response = client.get(f"/holdings/{USER_ID}", headers=VALID_HEADERS)

    assert response.status_code == 200
    data = response.json()["data"]
    assert isinstance(data, list)
    assert {h["asset_id"] for h in data} == {str(ASSET_A), str(ASSET_B)}


def test_get_unknown_user_id_returns_empty_list(fake_db):
    response = client.get(f"/holdings/{uuid4()}", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"] == []


def test_get_filtered_by_asset_returns_only_that_holding(fake_db):
    response = client.get(f"/holdings/{USER_ID}?asset_id={ASSET_A}", headers=VALID_HEADERS)

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["asset_id"] == str(ASSET_A)


def test_get_filtered_by_unknown_asset_returns_404(fake_db):
    response = client.get(f"/holdings/{USER_ID}?asset_id={uuid4()}", headers=VALID_HEADERS)
    assert response.status_code == 404
