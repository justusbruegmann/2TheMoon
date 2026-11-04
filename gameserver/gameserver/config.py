from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str
    ticks_per_s: float = Field(default=1.0, gt=0)
    healthcheck_path: Path = Path("/tmp/healthcheck")