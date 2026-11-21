from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest
from shared.database.models import Holding, Portfolio, Season, SeasonStatus

from .conftest import FakeTable, VALID_HEADERS, client, override_user_db

USER_ID = uuid4()
EMPTY_USER_ID = uuid4()
OTHER_USER_ID = uuid4()

SEASON_ID = uuid4()
SEASON_START_BALANCE = Decimal("1000")

PORTFOLIO_ID = uuid4()
EMPTY_PORTFOLIO_ID = uuid4()
OTHER_PORTFOLIO_ID = uuid4()

ASSET_A = uuid4()
ASSET_B = uuid4()

HOLDING_A = {"portfolio_id": PORTFOLIO_ID, "asset_id": ASSET_A, "quantity": "1.5"}
HOLDING_B = {"portfolio_id": PORTFOLIO_ID, "asset_id": ASSET_B, "quantity": "2"}
# Same asset as HOLDING_A, but in another user's portfolio, so it must never show up in USER_ID's response.
OTHER_USERS_HOLDING = {"portfolio_id": OTHER_PORTFOLIO_ID, "asset_id": ASSET_A, "quantity": "99"}


def _season(season_id=SEASON_ID, ends_at=None, status=SeasonStatus.ACTIVE):
    return Season(
            id=season_id,
            name=f"Season {season_id}",
            starting_balance=SEASON_START_BALANCE,
            starts_at=datetime.now(UTC) - timedelta(days=30),
            ends_at=ends_at,
            status=status,
            created_at=datetime.now(UTC),
    )


def _portfolio(portfolio_id, user_id, season_id=SEASON_ID):
    # Build the Portfolio row directly so the fake table's id/created_at are present.
    return Portfolio(
            id=portfolio_id,
            created_at=datetime.now(UTC),
            user_id=user_id,
            season_id=season_id,
            cash_balance=SEASON_START_BALANCE,
    )


class FakeDatabase:
    ################################################
    # holdings_get resolves the user's portfolio in the current season first (holdings carry no user_id),
    # so the fake needs the seasons and portfolios tables as well.
    # NOTE: FakeTable ignores ends_at/status filters and returns rows in insertion order,
    # so the current season must be listed first.
    ################################################
    def __init__(self, seasons=None, portfolios=()):
        self.seasons = FakeTable(Season, rows=seasons if seasons is not None else [_season()])
        self.portfolios = FakeTable(Portfolio, rows=portfolios)
        self.holdings = FakeTable(Holding, lambda: {"id": uuid4()})


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for this module.
    ################################################
    db = FakeDatabase(portfolios=[
            _portfolio(PORTFOLIO_ID, USER_ID),
            _portfolio(EMPTY_PORTFOLIO_ID, EMPTY_USER_ID),
            _portfolio(OTHER_PORTFOLIO_ID, OTHER_USER_ID),
    ])

    # One holding per asset the user bought, so the GET returns a list of two
    db.holdings.insert(Holding(**HOLDING_A), Holding(**HOLDING_B), Holding(**OTHER_USERS_HOLDING))

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
    # Only this user's portfolio, so the other user's holding on ASSET_A is not part of the response.
    assert len(data) == 2


def test_get_empty_portfolio_returns_empty_list(fake_db):
    response = client.get(f"/holdings/{EMPTY_USER_ID}", headers=VALID_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"] == []


def test_get_unknown_user_id_returns_404(fake_db):
    # An unknown user has no portfolio in the current season, so portfolio_get_one's 404 is handed through.
    response = client.get(f"/holdings/{uuid4()}", headers=VALID_HEADERS)

    assert response.status_code == 404


def test_get_filtered_by_asset_returns_only_that_holding(fake_db):
    response = client.get(f"/holdings/{USER_ID}?asset_id={ASSET_A}", headers=VALID_HEADERS)

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["asset_id"] == str(ASSET_A)
    assert Decimal(data[0]["quantity"]) == Decimal("1.5")


def test_get_filtered_by_unknown_asset_returns_404(fake_db):
    response = client.get(f"/holdings/{USER_ID}?asset_id={uuid4()}", headers=VALID_HEADERS)
    assert response.status_code == 404


def test_get_without_active_season_returns_404():
    db = FakeDatabase(seasons=[], portfolios=[_portfolio(PORTFOLIO_ID, USER_ID)])

    with override_user_db(db):
        response = client.get(f"/holdings/{USER_ID}", headers=VALID_HEADERS)

    assert response.status_code == 404
