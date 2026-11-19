from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from shared.database.models import Portfolio, PortfolioInsert, Season, SeasonStatus
from .conftest import FakeTable, VALID_HEADERS, client, override_user_db

USER_ID = uuid4()
SEASON_ID = uuid4()
VALID_PAYLOAD = {
        "user_id": str(USER_ID),
        "season_id": str(SEASON_ID),
        "cash_balance": "1000.0",
}


class FakeDatabase:
    def __init__(self):
        self.portfolios = FakeTable(Portfolio, lambda: {"id": uuid4(), "created_at": datetime.now(UTC)})
        self.seasons = FakeTable(Season, rows=[Season(
                id=SEASON_ID,
                name="Current season",
                starting_balance=Decimal("1000"),
                starts_at=datetime.now(UTC),
                ends_at=None,
                status=SeasonStatus.ACTIVE,
                created_at=datetime.now(UTC),
        )])


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for this module.
    # The auth-boundary tests below need the real dependency (incl. HTTPBearer) to still run.
    ################################################
    db = FakeDatabase()

    # Add a row to the table
    db.portfolios.insert(PortfolioInsert(**VALID_PAYLOAD))

    with override_user_db(db):
        yield db


###################
# Unit Tests
###################

def test_get_one_valid_user_and_season(fake_db):
    response = client.get(
            "/portfolios/", params={"user_id": str(USER_ID), "season_id": str(SEASON_ID)}, headers=VALID_HEADERS
    )
    assert response.status_code == 200


def test_get_one_defaults_to_current_season(fake_db):
    response = client.get("/portfolios/", params={"user_id": str(USER_ID)}, headers=VALID_HEADERS)
    assert response.status_code == 200


def test_get_one_unknown_user(fake_db):
    response = client.get(
            "/portfolios/", params={"user_id": str(uuid4()), "season_id": str(SEASON_ID)}, headers=VALID_HEADERS
    )
    assert response.status_code == 404


def test_get_one_missing_user_id(fake_db):
    response = client.get("/portfolios/", params={"season_id": str(SEASON_ID)}, headers=VALID_HEADERS)
    assert response.status_code == 422


def test_post_valid_payload(fake_db):
    response = client.post("/portfolios/", json=VALID_PAYLOAD, headers=VALID_HEADERS)
    assert response.status_code == 201


def test_post_invalid_payload(fake_db):
    response = client.post("/portfolios/", json={"user_id": str(uuid4())}, headers=VALID_HEADERS)
    assert response.status_code == 422
