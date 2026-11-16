from uuid import UUID

from shared.database import Database


# Get starting prices for every asset with its history, later we have to see how to set the starting price when the asset has no history, now it will only be 100
def load_start_prices(db: Database, default_price: float) -> dict[UUID, float]:
    prices: dict[UUID, float] = {}
    for asset in db.assets.find():
        latest = db.price_history.find(
            order_by="recorded_at", desc=True, limit=1, asset_id=asset.id
        )
        prices[asset.id] = float(latest[0].close) if latest else default_price
    return prices