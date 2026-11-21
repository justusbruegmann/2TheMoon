import asyncio
import json
import logging
from uuid import UUID

import numpy

from redis.asyncio import Redis

from gameserver.config import Settings

logger = logging.getLogger(__name__)

class GameLoop:
    def __init__(self, redis: Redis, settings: Settings, start_prices: dict[UUID, float]) -> None:
        if not start_prices:
            raise ValueError("Game Server got no Assets")
        self.redis = redis
        self.settings = settings
        self.tick = 0
        self.rng = numpy.random.default_rng()
        self.prices = dict(start_prices)

    async def run(self) -> None:
        loop =  asyncio.get_running_loop()
        interval = 1/self.settings.ticks_per_s
        next_tick = loop.time()
        while True:
            await self.step()
            next_tick += interval
            delay = next_tick - loop.time()
            # if the servers misses its delay we don't want to fire multiple ticks at once
            if delay < 0:
                next_tick = loop.time()
                delay = 0.0
            await asyncio.sleep(delay)

    async def step(self) -> None:
        self.tick += 1
        self.update_prices()
        await self.publish_prices()
        # Because Healtcheck is after the publish to redis, if redis breaks, so will the healthcheck of the gameserver
        self.settings.healthcheck_path.touch()

    def update_prices(self) -> None:
        for asset_id in self.prices:
            factor = numpy.exp(self.rng.normal(0.0, self.settings.volatility))
            self.prices[asset_id] *= float(factor)

    async def publish_prices(self) -> None:
        prices = {str(asset_id): round(price, 4) for asset_id, price in self.prices.items()}

        await self.redis.xadd(
            self.settings.market_stream, 
            {"tick": self.tick, "prices": json.dumps(prices)},
            maxlen=self.settings.market_stream_maxlen,
            approximate=True,
        )

        logger.debug("tick=%d published %d prices", self.tick, len(prices))