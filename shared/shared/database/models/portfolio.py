from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .base import Insert


class PortfolioInsert(Insert):
    user_id: UUID
    season_id: UUID
    cash_balance: Decimal


class Portfolio(PortfolioInsert):
    id: UUID
    created_at: datetime
