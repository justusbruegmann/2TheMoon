import asyncio
from pathlib import Path
from unittest.mock import AsyncMock

import pytest
from gameserver.config import Settings
from gameserver.loop import GameLoop
from redis.asyncio import Redis

@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        redis_url="redis://localhost:6379",
        healthcheck_path=tmp_path / "healthcheck"
    )

@pytest.fixture
def redis() -> AsyncMock:
    return AsyncMock(spec=Redis)

@pytest.fixture
def game_loop(redis: AsyncMock, settings: Settings) -> GameLoop:
    return GameLoop(redis, settings)

async def test_step_increments_tick(game_loop: GameLoop) -> None:
    await game_loop._step()
    await game_loop._step()

    assert game_loop._tick == 2

async def test_step_touches_healthcheck_file(game_loop: GameLoop, settings: Settings) -> None:
    assert not settings.healthcheck_path.exists()

    await game_loop._step()

    assert settings.healthcheck_path.exists()

async def test_run_ticks_until_cancelled(redis: AsyncMock, settings: Settings) -> None:
    fast_settings = settings.model_copy(update={"ticks_per_s": 100.0})
    game_loop = GameLoop(redis, fast_settings)

    task = asyncio.create_task(game_loop.run())
    await asyncio.sleep(0.1)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert game_loop._tick >= 3