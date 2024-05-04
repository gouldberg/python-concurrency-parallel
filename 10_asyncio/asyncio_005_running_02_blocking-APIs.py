import asyncio
import requests
from util import delay
from util import async_timed


# ----------------------------------------------------------------------------
# Incorrectly using a blocking API in a coroutine
#   These APIs block the main thread. When we run a blocking API call inside a coroutine,
#   we're blocking the event loop thread itself, meaning that we stop any other coroutines or tasks from executing.
#   Examples of blocking API call include libraries such as requests, or time.sleep.
#   Blocking API:  Generally, any function that performs I/O that is not a coroutine or performs time-consuming CPU
#   operations can be considered blocking.
# ----------------------------------------------------------------------------

@async_timed()
async def get_example_status() -> int:
    return requests.get('http://www.example.com').status_code


@async_timed()
async def main():
    task_1 = asyncio.create_task(get_example_status())
    task_2 = asyncio.create_task(get_example_status())
    task_3 = asyncio.create_task(get_example_status())
    await task_1
    await task_2
    await task_3


# The total runtime of the main coroutine is roughly the sum of time for all the tasks to get the status we ran,
# meaning that we did not have any concurrency advantage
# This is because the requests library is blocking, meaning it will block whichever thread it is run on.
# Since asyncio only has one thread, the requests library blocks the event loop fom doing anything concurrently.

asyncio.run(main(), debug=True


# -->
# You need to use a library that supports coroutines and utilizes non-blocking sockets.
# This means that if the library you are using does not return coroutines and you aren't using await in yor own coroutines.
# you're likely making a blocking call.

# We can use a library such as aiohttp, which uses non-blocking sockets and returns coroutines to get proper concurrency.
# If you need to use the requests library, you can still use async syntax, but you'll need to explicitly tell asyncio to use
# multithreading with a thread pool executor.


