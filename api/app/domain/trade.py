from datetime import datetime
from uuid import UUID

from app.config.dependencies import UserDb
from app.util.response import DomainError
from app.util.time_range import validate_time_range
from shared.database.models import TradeInsert
from shared.database.models.enums import TradeOperation
from shared.database.models.trade import TradeOffer


def trades_get_all(
        db: UserDb,
        start: datetime | None = None,
        end: datetime | None = None,
        ticker: str | None = None,
        operation: str | None = None
):
    validate_time_range(start, end)

    filters = {}
    if start:
        filters["gt"] = {"executed_at": start}
    if end:
        filters["lt"] = {"executed_at": end}

    if operation:
        try:
            filters["operation"] = TradeOperation(operation)
        except ValueError:
            raise DomainError(status_code=400, message=f"Invalid operation '{operation}'")

    if ticker:
        asset = db.assets.find(ticker=ticker, limit=1)
        if not asset:
            raise DomainError(status_code=404, message="Found no asset with this ticker")
        filters["asset_id"] = asset[0].id

    return db.trades.find(**filters)


def trades_get_one(db: UserDb, trade_id: UUID):
    trade = db.trades.get(id=trade_id)
    if trade is None:
        raise DomainError(status_code=404, message="Found no trade with this id")
    return trade



def trades_buy(db: UserDb, payload: TradeOffer):
    # ToDo
    pass


def trades_sell(db: UserDb, payload: TradeOffer):
    # ToDo
    pass


def _post_trade(db: UserDb, payload: TradeInsert):
    return db.trades.insert(payload)[0]
