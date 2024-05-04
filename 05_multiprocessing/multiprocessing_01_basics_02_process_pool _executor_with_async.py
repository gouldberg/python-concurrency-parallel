import time
import asyncio
from asyncio.events import AbstractEventLoop
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from typing import List
from util import delay
from util import async_timed


# ----------------------------------------------------------------------------
# concurrent.futures:
#   - This module contains executors for both processes and threads that can be used on their own but also interoperate with asyncio.
#   - Executor abstract class defines 2 methods for running work asynchronously.
#      1. submit:  take a callable and return a Future. This is equivalent to the Pool.apply_async
#      2. map:  take a callable and a list of function arguments and then execute each argument in the list asynchronously.
#               It returns an iterator of the results of our calls similarly to asyncio.as_completed in that results are available
#               once they complete.
# ----------------------------------------------------------------------------

def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter = counter + 1
    end = time.time()
    print(f'Finished counting to {count_to} in {end - start}')
    return counter


# While it seems that this works the same as asyncio.as_completed, 
# the order of iteration is deterministic based on the order we passed in the numbers list.
# This means that if 100000000 was our first number, we'd stuck waiting for that call to finish
# before we could print out the other results that completed earlier.
# This means we are not quite as responsive as asyncio.as_completed.

if __name__ == '__main__':
    with ProcessPoolExecutor() as process_pool:
        numbers = [1, 3, 5, 22, 100000000]
        for result in process_pool.map(count, numbers):
            print(result)


# ----------------------------------------------------------------------------
# Process pool executors with the asyncio event loop
# ----------------------------------------------------------------------------

def count(count_to: int) -> int:
    counter = 0
    while counter < count_to:
        counter = counter + 1
    return counter


@async_timed()
async def main():
    with ProcessPoolExecutor() as process_pool:
        # create a partially applied function for countdown with its argument.
        loop: AbstractEventLoop = asyncio.get_running_loop()

        nums = [1, 3, 5, 22, 100000000]

        # submit each call to the process pool and append it to a list
        calls: List[partial[int]] = [partial(count, num) for num in nums]
        call_coros = []
        
        for call in calls:
            call_coros.append(loop.run_in_executor(process_pool, call))
        
        # wait for all results to finish.
        results = await asyncio.gather(*call_coros)
        
        for result in results:
            print(result)


if __name__ == '__main__':
    asyncio.run(main())
