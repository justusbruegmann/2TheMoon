from datetime import UTC, datetime
from decimal import Decimal
from uuid import uuid4

from app.domain.season import get_current_season
from shared.database.models import Season, SeasonStatus


class FakeSeasonsTable:
    #################################
    # get_current_season() needs to run a query directly, so this testing table mocks the test data behind the
    # _run() function
    #################################
    def __init__(self, seasons):
        self._seasons = seasons
        self.client = self
        self.name = "season"
        self.columns = "id"

    def table(self, _name):
        return self

    def select(self, *_args, **_kwargs):
        return self

    def or_(self, *_args, **_kwargs):
        return self

    def limit(self, *_args, **_kwargs):
        return self

    def _run(self, _query):
        return self._seasons


class FakeDb:
    def __init__(self, seasons):
        self.seasons = FakeSeasonsTable(seasons)


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
