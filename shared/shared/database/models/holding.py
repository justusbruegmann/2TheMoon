from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from .base import Insert


class Holding(Insert):
    portfolio_id: UUID
    asset_id: UUID
    quantity: Decimal
    average_buy_price: Decimal | None = None        # weighted by quantity


class HoldingUpdate(BaseModel):
    quantity: Decimal | None = None
    average_buy_price: Decimal | None = None
