from uuid import uuid4

import pytest

from shared.database.models import Holding
from .conftest import FakeTable, VALID_HEADERS, client, override_user_db

VALID_PAYLOAD = {
    "portfolio_id": str(uuid4()),
    "asset_id": str(uuid4()),
    "quantity": "1.5",
}
NEWLY_CREATED_HOLDING_ID = None


class FakeDatabase:
    def __init__(self):
        self.holdings = FakeTable(Holding, lambda: {"id": uuid4()})


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for this module.
    # The auth-boundary tests below need the real dependency (incl. HTTPBearer) to still run.
    ################################################
    db = FakeDatabase()

    # Add a row to the table to be retrieved in a GET request
    db.holdings.insert(Holding(**VALID_PAYLOAD))
    global NEWLY_CREATED_HOLDING_ID
    NEWLY_CREATED_HOLDING_ID = next(iter(db.holdings._rows))

    with override_user_db(db):
        yield db


###################
# Unit Tests
###################

def test_get_one_valid_id(fake_db):
    response = client.get(f"/holdings/{NEWLY_CREATED_HOLDING_ID}", headers=VALID_HEADERS)
    assert response.status_code == 200


def test_get_one_invalid_id(fake_db):
    response = client.get(f"/holdings/{uuid4()}", headers=VALID_HEADERS)
    assert response.status_code == 404
