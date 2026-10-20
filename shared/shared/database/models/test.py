from datetime import datetime

from .base import Insert


class TestInsert(Insert):
    number: int
    text: str
    bool: bool
    timestamptz: datetime

class Test(TestInsert):
    id: int
    created_at: datetime
