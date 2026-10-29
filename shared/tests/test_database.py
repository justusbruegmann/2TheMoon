import json
from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID

import httpx
import pytest
from supabase import ClientOptions, create_client

from shared.database import Database, DatabaseError, get_public_db, get_secret_db
from shared.database.database import get_settings
from shared.database.models import TradeInsert, TradeOperation, UserAsset

PORTFOLIO_ID = UUID("30000000-0000-0000-0000-000000000001")
SEASON_ID = UUID("10000000-0000-0000-0000-000000000001")
ASSET_ID = UUID("20000000-0000-0000-0000-000000000001")
NOW = "2026-10-20T09:00:00+00:00"
TRADE_ROW = {
    "id": "40000000-0000-0000-0000-000000000001",
    "portfolio_id": str(PORTFOLIO_ID),
    "season_id": str(SEASON_ID),
    "asset_id": str(ASSET_ID),
    "operation": "buy",
    "quantity": "1.50000000",
    "execution_price": "12345678901234.12345678",
    "fee": "0.00000000",
    "executed_at": NOW,
    "created_at": NOW,
}


class FakeServer:
    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.response = httpx.Response(200, json=[])

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self.response

    @property
    def params(self) -> dict[str, str]:
        return dict(self.requests[-1].url.params)


@pytest.fixture
def server() -> FakeServer:
    return FakeServer()


@pytest.fixture
def db(server: FakeServer) -> Database:
    http = httpx.Client(
        base_url="https://x.supabase.co/rest/v1", transport=httpx.MockTransport(server)
    )
    options = ClientOptions(auto_refresh_token=False, persist_session=False, httpx_client=http)
    return Database(create_client("https://x.supabase.co", "sb_secret_test", options))


def test_find_applies_filters_order_and_limit(db: Database, server: FakeServer) -> None:
    server.response = httpx.Response(200, json=[TRADE_ROW])

    trades = db.trades.find(portfolio_id=PORTFOLIO_ID, order_by="executed_at", desc=True, limit=10)

    assert len(trades) == 1
    assert server.requests[-1].url.path == "/rest/v1/trade"
    assert server.params["portfolio_id"] == f"eq.{PORTFOLIO_ID}"
    assert server.params["order"] == "executed_at.desc"
    assert server.params["limit"] == "10"


def test_numeric_columns_keep_full_precision(db: Database, server: FakeServer) -> None:
    server.response = httpx.Response(200, json=[TRADE_ROW])

    trade = db.trades.get(id=TRADE_ROW["id"])

    assert trade is not None
    assert trade.execution_price == Decimal("12345678901234.12345678")
    assert "execution_price::text" in server.params["select"]


def test_get_returns_none_when_nothing_matches(db: Database) -> None:
    assert db.seasons.get(status="active") is None


def test_insert_sends_payload_and_uses_database_defaults(db: Database, server: FakeServer) -> None:
    server.response = httpx.Response(201, json=[TRADE_ROW])
    trade = TradeInsert(
        portfolio_id=PORTFOLIO_ID,
        season_id=SEASON_ID,
        asset_id=ASSET_ID,
        operation=TradeOperation.BUY,
        quantity=Decimal("1.5"),
        execution_price=Decimal("189.12"),
    )

    created = db.trades.insert(trade)

    request = server.requests[-1]
    body = json.loads(request.content)
    assert created[0].operation is TradeOperation.BUY
    assert request.method == "POST"
    assert body == [{**trade.to_payload()}]
    assert "executed_at" not in body[0]
    assert body[0]["quantity"] == "1.5"
    assert "missing=default" in request.headers["prefer"]


def test_upsert_uses_conflict_columns(db: Database, server: FakeServer) -> None:
    row = {
        "portfolio_id": str(PORTFOLIO_ID),
        "asset_id": str(ASSET_ID),
        "quantity": "2",
        "average_buy_price": None,
    }
    server.response = httpx.Response(201, json=[row])

    holding = db.user_assets.upsert(
        UserAsset(portfolio_id=PORTFOLIO_ID, asset_id=ASSET_ID, quantity=Decimal(2)),
        on_conflict="portfolio_id,asset_id",
    )

    assert holding.quantity == Decimal(2)
    assert server.params["on_conflict"] == "portfolio_id,asset_id"
    assert "resolution=merge-duplicates" in server.requests[-1].headers["prefer"]


def test_update_and_delete_filter_rows(db: Database, server: FakeServer) -> None:
    db.portfolios.update({"cash_balance": "500"}, id=PORTFOLIO_ID)
    assert server.requests[-1].method == "PATCH"
    assert json.loads(server.requests[-1].content) == {"cash_balance": "500"}
    assert server.params["id"] == f"eq.{PORTFOLIO_ID}"

    db.market_events.delete(season_id=SEASON_ID)
    assert server.requests[-1].method == "DELETE"
    assert server.params["season_id"] == f"eq.{SEASON_ID}"


def test_update_and_delete_without_filter_are_refused(db: Database, server: FakeServer) -> None:
    with pytest.raises(ValueError):
        db.portfolios.update({"cash_balance": "0"})
    with pytest.raises(ValueError):
        db.trades.delete()
    assert server.requests == []


def test_errors_are_wrapped(db: Database, server: FakeServer) -> None:
    server.response = httpx.Response(409, json={"code": "23505", "message": "duplicate key"})

    with pytest.raises(DatabaseError, match="season"):
        db.seasons.find()


def test_insert_payload_skips_unset_optional_fields() -> None:
    payload = TradeInsert(
        portfolio_id=PORTFOLIO_ID,
        season_id=SEASON_ID,
        asset_id=ASSET_ID,
        operation=TradeOperation.SELL,
        quantity=Decimal(1),
        execution_price=Decimal(1),
        executed_at=datetime(2026, 10, 20, tzinfo=UTC),
    ).to_payload()

    assert payload["operation"] == "sell"
    assert payload["executed_at"] == "2026-10-20T00:00:00Z"
    assert payload["fee"] == "0"


@pytest.fixture
def settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SUPABASE_URL", "https://x.supabase.co")
    monkeypatch.setenv("SUPABASE_PUBLISHABLE_KEY", "sb_publishable_test")
    monkeypatch.setenv("SUPABASE_SECRET_KEY", "sb_secret_test")
    get_settings.cache_clear()
    get_secret_db.cache_clear()


def test_public_db_queries_as_the_user(settings: None) -> None:
    client = get_public_db("user-jwt").trades.client

    assert client.supabase_key == "sb_publishable_test"
    assert client.postgrest.headers["authorization"] == "Bearer user-jwt"


def test_public_db_requires_token(settings: None) -> None:
    with pytest.raises(ValueError):
        get_public_db("")


def test_secret_db_uses_secret_key_and_is_reused(settings: None) -> None:
    db = get_secret_db()

    assert db.trades.client.supabase_key == "sb_secret_test"
    assert get_secret_db() is db


def test_secret_db_fails_clearly_without_key(
    settings: None, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("SUPABASE_SECRET_KEY", "")
    get_settings.cache_clear()

    with pytest.raises(RuntimeError, match="SUPABASE_SECRET_KEY"):
        get_secret_db()
