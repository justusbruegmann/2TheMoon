from datetime import datetime
from uuid import UUID

from .base import Insert


class MarketEventInsert(Insert):
    season_id: UUID
    label: str
    description: str
    affected_industries: list[str] = []
    starts_at: datetime
    ends_at: datetime


class MarketEvent(MarketEventInsert):
    id: UUID
    created_at: datetime
