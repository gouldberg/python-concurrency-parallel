import asyncio
from aioredis import create_redis
import time


# ----------------------------------------------------------------------------
# traditional non-async iterator
# ----------------------------------------------------------------------------

class A:
    # An iterator must implement the __iter__() special method.
    def __iter__(self):
        # Initialize some state to the “starting” state.
        self.x = 0
        # The __iter__() special method must return an iterable; i.e.,
        # an object that implements the __next__() special method.
        # In this case, it’s the same instance,
        # because A itself also implements the __next__() special method.
        return self

    # This will be called for every step in the iteration sequence until...
    def __next__(self):
        if self.x > 2:
            # ...StopIteration is raised.
            raise StopIteration
        else:
            self.x += 1
        # The returned values for each iteration are generated.
        return self.x


for i in A():
    print(i)


# ----------------------------------------------------------------------------
# Async iterator for fetching data from Redis
# ----------------------------------------------------------------------------

# Mock Redis interface
class Redis:
    async def get(self, key):
        await asyncio.sleep(0)
        return 'value'


class OneAtATime:
    def __init__(self, redis, keys):
        self.redis = redis
        self.keys = keys

    # __aiter__() to set things up for iteration. 
    # # return self because OneAtATime also implements the __anext__() coroutine method.
    def __aiter__(self):
        self.ikeys = iter(self.keys)
        return self

    # Note that the __anext__() method is declared with async def,
    # while the __aiter__() method is declared only with def .
    async def __anext__(self):
        try:
            k = next(self.ikeys)
        # When self.ikeys is exhausted, we handle the StopIteration and
        # simply turn it into a StopAsyncIteration!
        # This is how you signal stop from inside an async iterator.
        except StopIteration:
            raise StopAsyncIteration
        # We can await the data, which means that
        # other code can run on the event loop while we wait on network I/O.
        value = await self.redis.get(k)
        return value


# Mock create_redis
# Real one: aioredis.create_redis
async def create_redis(socket):
    await asyncio.sleep(0)
    return Redis()


async def do_something_with(value):
    await asyncio.sleep(0)


async def main():
    # We use the high-level interface in aioredis to get a connection.
    redis = await create_redis(('localhost', 6379))
    # ----------
    # Imagine that each of the values associated with these keys
    # is quite large and stored in the Redis instance.
    keys = ['Americas', 'Africa', 'Europe', 'Asia']
    # ----------
    # async for:
    #   the point is that iteration is able to suspend itself while waiting for the next datum to arrive.
    async for value in OneAtATime(redis, keys):
        # For completeness, imagine that we also perform some I/O-bound activity on the fetched value
        # perhaps a simple data transformation and then it gets sent on to another destination.
        await do_something_with(value)


asyncio.run(main())


# ----------------------------------------------------------------------------
# Async generators
# ----------------------------------------------------------------------------

# Mock Redis interface
class Redis:
    async def get(self, key):
        await asyncio.sleep(0)
        return 'value'


# Mock create_redis
# Real one: aioredis.create_redis
async def create_redis(socket):
    await asyncio.sleep(0)
    return Redis()


async def do_something_with(value):
    await asyncio.sleep(0)


# asynchronous generator function.
async def one_at_a_time(redis, keys):
    for k in keys:
        # we just loop over the keys directly and obtain the value...
        value = await redis.get(k)
        # ...and then yield it to the caller, just like a normal generator.
        yield value


async def main():
    redis = await create_redis(('localhost', 6379))
    keys = ['Americas', 'Africa', 'Europe', 'Asia']
    async for value in one_at_a_time(redis, keys):
        await do_something_with(value)


asyncio.run(main())