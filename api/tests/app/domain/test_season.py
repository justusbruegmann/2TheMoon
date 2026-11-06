from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.season import get_current_season
from shared.database.models import Season, SeasonStatus
from ..conftest import FakeTable


class FakeDb:
    def __init__(self, seasons):
        self.seasons = FakeTable(Season, rows=seasons)


def make_season(**overrides):
    defaults = {
            "id": uuid4(),
            "name": "Season 1",
            "starting_balance": Decimal("1000"),
            "starts_at": datetime.now(UTC),
            "ends_at": None,
            "status": SeasonStatus.ACTIVE,
            "created_at": datetime.now(UTC),
    }
    return Season(**{**defaults, **overrides})


def test_get_current_season_returns_matching_season():
    season = make_season()
    db = FakeDb([season])

    assert get_current_season(db) == season


def test_get_current_season_returns_none_when_no_season_found():
    db = FakeDb([])

    assert get_current_season(db) is None
