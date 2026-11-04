import asyncio
import logging

import numpy

from redis.asyncio import Redis

from gameserver.config import Settings

logger = logging.getLogger(__name__)

class GameLoop:
    def __init__(self, redis: Redis, settings: Settings) -> None:
        self._redis = redis
        self._settings = settings
        self._tick = 0
        self._rng = numpy.random.default_rng()
        self._price = 100.0

    async def run(self) -> None:
        loop =  asyncio.get_running_loop()
        interval = 1/self._settings.ticks_per_s
        next_tick = loop.time()
        while True:
            await self._step()
            next_tick += interval
            delay = next_tick - loop.time()
            # if the servers misses its delay we don't want to fire multiple ticks at once
            if delay < 0:
                next_tick = loop.time()
                delay = 0.0
            await asyncio.sleep(delay)

    async def _step(self) -> None:
        self._tick += 1
        self._price *= float(numpy.exp(self._rng.normal(0.0,0.01)))
        logger.info("tick=%d price=%.2f", self._tick, self._price)
        # here goes the stuff that writes to the redis stream

        # update the healthcheck file so we know we still runnin
        self._settings.healthcheck_path.touch()