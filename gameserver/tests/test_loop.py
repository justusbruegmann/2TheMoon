import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest
from redis.asyncio import Redis

from gameserver.config import Settings
from gameserver.loop import GameLoop


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(redis_url="redis://localhost:6379", healthcheck_path=tmp_path / "healthcheck")


@pytest.fixture
def redis() -> AsyncMock:
    mock = AsyncMock(spec=Redis)
    mock.xadd = AsyncMock()
    return mock


@pytest.fixture
def game_loop(redis: AsyncMock, settings: Settings) -> GameLoop:
    return GameLoop(redis, settings, {uuid4(): 100.0, uuid4(): 50.0})


def test_no_assets_raises(redis: AsyncMock, settings: Settings) -> None:
    with pytest.raises(ValueError):
        GameLoop(redis, settings, {})


async def test_step_increments_tick(game_loop: GameLoop) -> None:
    await game_loop.step()
    await game_loop.step()

    assert game_loop.tick == 2


async def test_step_touches_healthcheck_file(game_loop: GameLoop, settings: Settings) -> None:
    await game_loop.step()

    assert settings.healthcheck_path.exists()


async def test_update_prices_changes_prices(game_loop: GameLoop) -> None:
    before = dict(game_loop.prices)

    game_loop.update_prices()

    assert game_loop.prices.keys() == before.keys()
    assert game_loop.prices != before
    assert all(price > 0 for price in game_loop.prices.values())


async def test_step_writes_prices_to_stream(
    game_loop: GameLoop, redis: AsyncMock, settings: Settings
) -> None:
    await game_loop.step()

    stream, fields = redis.xadd.await_args.args
    assert stream == settings.market_stream
    assert fields["tick"] == 1
    assert set(json.loads(fields["prices"])) == {str(asset_id) for asset_id in game_loop.prices}


async def test_run_ticks_until_cancelled(redis: AsyncMock, settings: Settings) -> None:
    fast_settings = settings.model_copy(update={"ticks_per_s": 100.0})
    game_loop = GameLoop(redis, fast_settings, {uuid4(): 100.0})

    task = asyncio.create_task(game_loop.run())
    await asyncio.sleep(0.1)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task

    assert game_loop.tick >= 3
