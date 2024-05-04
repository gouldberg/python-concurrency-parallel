import asyncio
from asyncio import Future


# ----------------------------------------------------------------------------
# future:
#   A future is a Python object that contains a single value that you expect to get at some point in the future but may not yet have.
#   Usually, when you create a future, it does not have any value it wraps around because it does not yet exist.
#   In this state, it is considered incomplete, unresolved, or simply not done.
#   Then, once you get a result, you can set the value of the future.
#   This will complete the future;
#   at that time, we can considered it finished and extract the result from the future.
# ----------------------------------------------------------------------------

# create a future by calling its constructor.
my_future = Future()

print(f'Is my_future done ? {my_future.done()}')

my_future.set_result(42)

print(f'Is my_future done ? {my_future.done()}')

# We don't call the result method before the result is set
# because the result method will throw an invalid state exception if we do so.
print(f'What is the result of my_future? {my_future.result()}')


# ----------------------------------------------------------------------------
# Awaiting a future
#   In the world of asyncio, you should rarely need to deal with futures.
#   That said, you will run into some asyncio APIs which return futures, and you may need to work with callback-based code, which can require futures.
# ----------------------------------------------------------------------------

# create a task to asynchronously set the value of the future.
def make_request() -> Future:
    future = Future()
    asyncio.create_task(set_future_value(future))
    return future


# wait 1 second before setting the value of the future.
async def set_future_value(future) -> None:
    await asyncio.sleep(1)
    future.set_result(42)


async def main():
    future = make_request()
    print(f'Is the future done? {future.done()}')
    
    # pause main until the future's value is set.
    value = await future
    print(f'Is the future done? {future.done()}')
    print(value)
    

asyncio.run(main())
