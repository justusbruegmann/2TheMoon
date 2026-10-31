from datetime import datetime
from uuid import UUID

from .base import Insert


class ChatMessageInsert(Insert):
    sender_id: UUID
    message: str


class ChatMessage(ChatMessageInsert):
    id: UUID
    created_at: datetime
