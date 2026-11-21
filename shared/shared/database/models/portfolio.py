from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .base import Insert


class PortfolioInsertExternalPayload(Insert):
    user_id: UUID


class PortfolioInsertInternalPayload(PortfolioInsertExternalPayload):
    season_id: UUID
    cash_balance: Decimal


class Portfolio(PortfolioInsertInternalPayload):
    id: UUID
    created_at: datetime
