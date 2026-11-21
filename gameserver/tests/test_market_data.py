from datetime import UTC, datetime
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from shared.database.models import Asset, AssetKind, PriceHistory

from gameserver.market_data import load_start_prices


def make_asset() -> Asset:
    return Asset(
        id=uuid4(), created_at=datetime.now(UTC), ticker="AAPL", name="Apple", kind=AssetKind.STOCK
    )


def make_candle(asset: Asset, close: str) -> PriceHistory:
    price = Decimal(close)
    return PriceHistory(
        season_id=uuid4(),
        asset_id=asset.id,
        open=price,
        close=price,
        high=price,
        low=price,
        recorded_at=datetime.now(UTC),
    )


def test_uses_latest_close() -> None:
    asset = make_asset()
    db = MagicMock()
    db.assets.find.return_value = [asset]
    db.price_history.find.return_value = [make_candle(asset, "187.5")]

    assert load_start_prices(db, 100.0) == {asset.id: 187.5}


def test_uses_default_without_history() -> None:
    asset = make_asset()
    db = MagicMock()
    db.assets.find.return_value = [asset]
    db.price_history.find.return_value = []

    assert load_start_prices(db, 100.0) == {asset.id: 100.0}
