import asyncio
from .async_timer import async_timed


# ----------------------------------------------------------------------------
# delay
# ----------------------------------------------------------------------------

# asyncio.sleep itself is coroutine, requiring await keyword
# this means, when a coroutine awaits it, other code will be able to run.

@async_timed()
async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


