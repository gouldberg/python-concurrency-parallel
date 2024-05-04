import asyncio
from util import delay
from util import async_timed


# ----------------------------------------------------------------------------
# Attempting to run CPU-bound code concurrently
# ----------------------------------------------------------------------------

@async_timed()
async def cpu_bound_work() -> int:
    counter = 0
    for _ in range(100000000):
        counter = counter + 1
    return counter

# this code still executes sequentially.
@async_timed()
async def main():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    await task_one
    await task_two

# debug=True is debug mode

# total almost 7-8 secs.
# Debug mode message ('Executing ....') shows that firstly task_one is taking too long
# therefore blocking the event loop from running any other tasks.
# The default settings will log a warning if a coroutine takes longer than 100 milliseconds.
asyncio.run(main(), debug=True)


# ----------------------------------------------------------------------------
# CPU-bound code with a task
# ----------------------------------------------------------------------------

# delay will not run concurrently alongside the CPU-bound work.
# because we create the two CPU-bound tasks first, which in effect, blocks the event loop from running anything else.
@async_timed()
async def main_2():
    task_one = asyncio.create_task(cpu_bound_work())
    task_two = asyncio.create_task(cpu_bound_work())
    delay_task = asyncio.create_task(delay(4))
    await task_one
    await task_two
    await delay_task

# total almost 11-12 secs.
asyncio.run(main_2(), debug=True)


