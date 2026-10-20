from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .base import Insert
from .enums import TradeOperation


class TradeInsert(Insert):
    portfolio_id: UUID
    season_id: UUID
    asset_id: UUID
    operation: TradeOperation
    quantity: Decimal
    execution_price: Decimal
    fee: Decimal = Decimal(0)
    executed_at: datetime | None = None


class Trade(TradeInsert):
    id: UUID
    executed_at: datetime
    created_at: datetime
