from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .base import Insert


class PortfolioHistoryInsert(Insert):
    portfolio_id: UUID
    cash_balance: Decimal
    user_assets_value: Decimal
    recorded_at: datetime | None = None


class PortfolioHistory(PortfolioHistoryInsert):
    recorded_at: datetime
