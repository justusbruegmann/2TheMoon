from typing import Any

from pydantic import BaseModel, ConfigDict


class Insert(BaseModel):
    # extra="forbid": Do not accept other fields to be passed in a payload; they could possibly overwrite the values
    # we try to set in the domain methods
    model_config = ConfigDict(extra="forbid")

    def to_payload(self) -> dict[str, Any]:
        return self.model_dump(mode="json", exclude_none=True)
