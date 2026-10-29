from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .base import Insert


class PriceHistoryInsert(Insert):
    season_id: UUID
    asset_id: UUID
    open: Decimal
    close: Decimal
    high: Decimal
    low: Decimal
    recorded_at: datetime | None = None


class PriceHistory(PriceHistoryInsert):
    recorded_at: datetime
