from datetime import datetime, timezone
from uuid import uuid4

import pytest

from shared.database.models import Portfolio, PortfolioInsert
from .conftest import FakeTable, VALID_HEADERS, client, override_user_db

VALID_PAYLOAD = {
        "user_id": str(uuid4()),
        "season_id": str(uuid4()),
        "cash_balance": "1000.0",
}
NEWLY_CREATED_PORTFOLIO_ID = None


class FakeDatabase:
    def __init__(self):
        self.portfolios = FakeTable(Portfolio, lambda: {"id": uuid4(), "created_at": datetime.now(timezone.utc)})


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for this module.
    # The auth-boundary tests below need the real dependency (incl. HTTPBearer) to still run.
    ################################################
    db = FakeDatabase()

    # Add a row to the table
    new_row = db.portfolios.insert(PortfolioInsert(**VALID_PAYLOAD))[0]
    global NEWLY_CREATED_PORTFOLIO_ID
    NEWLY_CREATED_PORTFOLIO_ID = str(new_row.id)

    with override_user_db(db):
        yield db


###################
# Unit Tests
###################

def test_get_one_valid_id(fake_db):
    response = client.get(f"/portfolios/{NEWLY_CREATED_PORTFOLIO_ID}", headers=VALID_HEADERS)
    assert response.status_code == 200


def test_get_one_invalid_id(fake_db):
    response = client.get(f"/portfolios/{uuid4()}", headers=VALID_HEADERS)
    assert response.status_code == 404


def test_post_valid_payload(fake_db):
    response = client.post("/portfolios/", json=VALID_PAYLOAD, headers=VALID_HEADERS)
    assert response.status_code == 201


def test_post_invalid_payload(fake_db):
    response = client.post("/portfolios/", json={"user_id": str(uuid4())}, headers=VALID_HEADERS)
    assert response.status_code == 422
