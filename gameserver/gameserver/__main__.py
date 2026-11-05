import asyncio
import logging
import signal
from contextlib import suppress

from redis.asyncio import Redis

from gameserver.config import Settings
from gameserver.loop import GameLoop


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    redis = Redis.from_url(settings.redis_url, decode_responses=True)

    try:
        await redis.ping()
        stop = asyncio.Event()
        running_loop = asyncio.get_running_loop()
        # docker stop sends SIGTERM signal, STRG+C sends SIGINT signal
        # tell the programm what to do when the signal arrives, in this case set the stop event
        for sig in (signal.SIGINT, signal.SIGTERM):
            running_loop.add_signal_handler(sig, stop.set)
        # create and start game loop
        task = asyncio.create_task(GameLoop(redis, settings).run())
        # let the main wait until SIGINT or SIGTERM event gets triggered and sets the stop event
        # the event loop will still run even though main is waiting
        await stop.wait()
        # stops game loop and throws CancelledError exception
        task.cancel()
        # catch/supress that exception so the gameloops doesn't closes safely and wait for the termination of the task
        with suppress(asyncio.CancelledError):
            await task
    finally:
        await redis.aclose()

if __name__ == "__main__":
    asyncio.run(main())