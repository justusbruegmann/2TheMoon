from datetime import datetime

from .base import Insert


class TestInsert(Insert):
    number: int | None
    text: str | None
    bool: bool | None
    timestamptz: datetime | None

class Test(TestInsert):
    id: int
    created_at: datetime
