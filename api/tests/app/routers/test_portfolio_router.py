from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import pytest

from shared.database.models import Portfolio, PortfolioInsertInternalPayload, Season, SeasonStatus
from .conftest import FakeTable, VALID_HEADERS, client, override_user_db

USER_ID = uuid4()
OTHER_USER_ID = uuid4()
SEASON_ID = uuid4()
PAST_SEASON_ID = uuid4()
SEASON_START_BALANCE = Decimal("1000")


class FakeDatabase:
    def __init__(self, seasons=None, portfolios=()):
        self.portfolios = FakeTable(
            Portfolio, lambda: {"id": uuid4(), "created_at": datetime.now(UTC)}, rows=portfolios
        )
        # NOTE: FakeTable ignores ends_at/status filters and returns rows in insertion order,
        # so the current season must be listed first.
        self.seasons = FakeTable(Season, rows=seasons if seasons is not None else [_season(SEASON_ID)])


def _season(season_id, starting_balance=SEASON_START_BALANCE, ends_at=None, status=SeasonStatus.ACTIVE):
    return Season(
            id=season_id,
            name=f"Season {season_id}",
            starting_balance=starting_balance,
            starts_at=datetime.now(UTC) - timedelta(days=30),
            ends_at=ends_at,
            status=status,
            created_at=datetime.now(UTC),
    )


def _existing_portfolio(user_id=USER_ID, season_id=SEASON_ID):
    # Build the Portfolio row directly so the fake table's id/created_at are present.
    return Portfolio(
            id=uuid4(),
            created_at=datetime.now(UTC),
            user_id=user_id,
            season_id=season_id,
            cash_balance=SEASON_START_BALANCE,
    )


@pytest.fixture(scope="module")
def fake_db():
    ################################################
    # Overrides get_user_db for the GET tests in this module.
    # The auth-boundary tests below need the real dependency (incl. HTTPBearer) to still run.
    ################################################
    db = FakeDatabase(portfolios=[_existing_portfolio()])

    with override_user_db(db):
        yield db


@pytest.fixture
def make_post_db():
    # Function-scoped factory so each POST test sets up its own seasons without affecting others.
    def _make(seasons=None, portfolios=None):
        if portfolios is None:
            portfolios = [_existing_portfolio()]
        return FakeDatabase(seasons=seasons, portfolios=portfolios)
    return _make


@pytest.fixture
def post_db(make_post_db):
    db = make_post_db()
    with override_user_db(db):
        yield db


###################
# GET Unit Tests
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


###################
# POST Unit Tests
###################

def test_post_creates_portfolio_for_user_in_current_season(post_db):
    response = client.post("/portfolios/", json={"user_id": str(OTHER_USER_ID)}, headers=VALID_HEADERS)

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["user_id"] == str(OTHER_USER_ID)
    assert data["season_id"] == str(SEASON_ID)

    stored = post_db.portfolios.get(user_id=OTHER_USER_ID, season_id=SEASON_ID)
    assert stored is not None


def test_post_cash_balance_is_derived_from_season_starting_balance(make_post_db):
    # Use a starting balance that differs from the default, so a hard-coded value would fail.
    db = make_post_db(seasons=[_season(SEASON_ID, starting_balance=Decimal("7500"))])

    with override_user_db(db):
        response = client.post("/portfolios/", json={"user_id": str(OTHER_USER_ID)}, headers=VALID_HEADERS)

    assert response.status_code == 201
    assert Decimal(response.json()["data"]["cash_balance"]) == Decimal("7500")


def test_post_rejects_duplicate_portfolio_in_same_season(post_db):
    response = client.post("/portfolios/", json={"user_id": str(USER_ID)}, headers=VALID_HEADERS)

    assert response.status_code == 400
    assert len(post_db.portfolios.find(user_id=USER_ID, season_id=SEASON_ID)) == 1


def test_post_allows_portfolio_in_new_season_for_same_user(make_post_db):
    # USER_ID already has a portfolio in the past season, so a new current season must be allowed.
    # The current season is listed first (see FakeDatabase note).
    past_season = _season(PAST_SEASON_ID, ends_at=datetime.now(UTC) - timedelta(days=1), status=SeasonStatus.ENDED)
    past_portfolio = _existing_portfolio(season_id=PAST_SEASON_ID)
    db = make_post_db(seasons=[_season(SEASON_ID), past_season], portfolios=[past_portfolio])

    with override_user_db(db):
        response = client.post("/portfolios/", json={"user_id": str(USER_ID)}, headers=VALID_HEADERS)

    assert response.status_code == 201
    assert response.json()["data"]["season_id"] == str(SEASON_ID)


def test_post_without_active_season_returns_404(make_post_db):
    db = make_post_db(seasons=[])

    with override_user_db(db):
        response = client.post("/portfolios/", json={"user_id": str(OTHER_USER_ID)}, headers=VALID_HEADERS)

    assert response.status_code == 404
    assert db.portfolios.find(user_id=OTHER_USER_ID) == []


def test_post_rejects_season_id_in_body(post_db):
    response = client.post(
        "/portfolios/",
        json={"user_id": str(OTHER_USER_ID), "season_id": str(PAST_SEASON_ID)},
        headers=VALID_HEADERS,
    )

    assert response.status_code == 422
    assert post_db.portfolios.find(user_id=OTHER_USER_ID) == []


def test_post_rejects_cash_balance_in_body(post_db):
    response = client.post(
        "/portfolios/",
        json={"user_id": str(OTHER_USER_ID), "cash_balance": "999999"},
        headers=VALID_HEADERS,
    )

    assert response.status_code == 422
    assert post_db.portfolios.find(user_id=OTHER_USER_ID) == []


def test_post_missing_user_id(post_db):
    response = client.post("/portfolios/", json={}, headers=VALID_HEADERS)
    assert response.status_code == 422


def test_post_invalid_user_id_format(post_db):
    response = client.post("/portfolios/", json={"user_id": "not-a-uuid"}, headers=VALID_HEADERS)
    assert response.status_code == 422
