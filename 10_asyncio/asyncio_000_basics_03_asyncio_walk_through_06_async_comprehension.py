import asyncio
import time


# ----------------------------------------------------------------------------
# Async list, dict, and set comprehensions
# ----------------------------------------------------------------------------

async def doubler(n):
    for i in range(n):
        yield i, i * 2
        # Sleep a little, just to emphasize that this is really an async function.
        await asyncio.sleep(0.1)


# 'async for' instead for 'for'
async def main():
    result = [x async for x in doubler(3)]
    print(result)
    result = {x: y async for x, y in doubler(3)}
    print(result)
    result = {x async for x in doubler(3)}
    print(result)


asyncio.run(main())


# ----------------------------------------------------------------------------
# await f(x) async f, x in ...
# ----------------------------------------------------------------------------

async def f(x):
    await asyncio.sleep(0.1)
    return x + 100


async def factory(n):
    for x in range(n):
        await asyncio.sleep(0.1)
        # The f return value is a coroutine function, not yet a coroutine.
        yield f, x


# This example has been contrived to
# demonstrate a comprehension that includes both async for and await.
async def main():
    # the factory(3) call returns an async generator, which must be driven by iteration.
    # Because it's an async generator, you can't just use for; you must use async for.
    results = [await f(x) async for f, x in factory(3)]
    print('results = ', results)

asyncio.run(main())