from datetime import datetime
from uuid import UUID

from .base import Insert
from .enums import AssetKind


class AssetInsert(Insert):
    ticker: str
    name: str
    kind: AssetKind
    industry: list[str] = []
    creator_id: UUID | None = None


class Asset(AssetInsert):
    id: UUID
    created_at: datetime
