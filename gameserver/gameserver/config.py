from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_url: str
    ticks_per_s: float = Field(default=1.0, gt=0)
    healthcheck_path: Path = Path("/tmp/healthcheck")
    market_stream: str =  "market:prices"
    market_stream_maxlen: int = Field(default=10000, gt=0)
    initial_price: float = Field(default=100.0, gt=0)
    volatility: float = Field(default=0.01, ge=0)