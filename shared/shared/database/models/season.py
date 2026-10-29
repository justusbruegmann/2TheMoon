from datetime import datetime
from decimal import Decimal
from uuid import UUID

from .base import Insert
from .enums import SeasonStatus


class SeasonInsert(Insert):
    name: str
    starting_balance: Decimal
    starts_at: datetime
    ends_at: datetime | None = None
    status: SeasonStatus = SeasonStatus.UPCOMING


class Season(SeasonInsert):
    id: UUID
    created_at: datetime
