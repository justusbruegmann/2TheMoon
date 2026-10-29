from typing import Any

from pydantic import BaseModel


class Insert(BaseModel):
    def to_payload(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)
