import asyncio
from util import delay
from util import async_timed
from asyncio import CancelledError


# ----------------------------------------------------------------------------
# Cancelling task
# ----------------------------------------------------------------------------

# Cancelling a task will cause that task to raise a CancelledError when we await it.
# CancelledError can only be thrown from an await statement.
# If we call cancel on a task when it is executing plain Python code,
# that code will run until completion until we hit the next await statement (if one exists)
# and a CancelledError can be raised.
# Calling cancel won't magically stop the task in its tracks; it will only stop the task if you're currently at an await point or its next await point.

@async_timed()
async def main():
    long_task = asyncio.create_task(delay(10))
    
    seconds_elapsed = 0
    
    while not long_task.done():
        print('Task not finished, checking again in a second.')
        await asyncio.sleep(1)
        seconds_elapsed = seconds_elapsed + 1
        if seconds_elapsed == 5:
            long_task.cancel()
    
    try:
        await long_task
    except CancelledError:
        print('Our task was cancelled')


asyncio.run(main())


# ----------------------------------------------------------------------------
# Creating a timeout for a task with wait_for
# ----------------------------------------------------------------------------

# After 1 second our wait_for statement will raise a TimeoutError, which we then handle.
# Original delay task is cancelled.

@async_timed()
async def main_2():
    delay_task = asyncio.create_task(delay(2))
    
    try:
        result = await asyncio.wait_for(delay_task, timeout=1)
        print(result)
    except asyncio.exceptions.TimeoutError:
        print('Got a timeout !')
        print('Was the task cancelled? {delay_task.cancelled()}')


# roughly 1 seconds
asyncio.run(main_2())


# ----------------------------------------------------------------------------
# Shielding a task from cancellation
# ----------------------------------------------------------------------------

# asyncio.shield will prevent cancellation of the coroutine we pass in,
# giving it a "shield", which cancellation requests then ignore.

# The case:  we may want to inform a user that something is taking longe than expected after a certain amount of time
# but not cancel the task when the timeout is exceeded.

@async_timed()
async def main_3():
    task = asyncio.create_task(delay(10))
    
    try:
        # prevent the task from being canceled.
        result = await asyncio.wait_for(asyncio.shield(task), 5)
        print(result)
    except asyncio.exceptions.TimeoutError:
        # now the we need to access the task in the except block.
        print('Task took longer than five seconds, it will finish soon!')
        result = await task
        print(result)


# roughly 10 seconds, but at 5 secs print except message.
asyncio.run(main_3())

