from decimal import Decimal
from uuid import UUID

from .base import Insert


class UserAsset(Insert):
    portfolio_id: UUID
    asset_id: UUID
    quantity: Decimal
    average_buy_price: Decimal | None = None
