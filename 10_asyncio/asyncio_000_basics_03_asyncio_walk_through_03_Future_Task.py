import asyncio
from asyncio import Future


# ----------------------------------------------------------------------------
# Creating Task
# ----------------------------------------------------------------------------

# launch completely new tasks inside the coroutine.
# By not awaiting them, they will run independently of the execution context inside coroutine function f()
# f() will exit before the tasks that it launched have completed
async def f():
    loop = asyncio.get_event_loop()
    for i in range():
        loop.create_task('<some other coro>')


# create async task
async def f():
    for i in range():
        asyncio.create_task('<some other coro>')


# ----------------------------------------------------------------------------
# Future: Checking completion status with done()
#   - Future class is actually a superclass of Task, and it provides all of the functionality for interaction with the loop.
#   ^ Future represents a future completion state of some activity and is managed by the loop.
#   - Running a function on an executor will return a Future instance, not a Task.
#
#   - Have a "result" value set (use .set_result(value)) to set it and .result() to obtain it.
#   - Be cancelled with .cancel() (and check for cancellation with .cancelled())
#   - Have additional callback functions added that will be run when the future completes.
# ----------------------------------------------------------------------------

# When a Future instance is created, the toggle is set to "not yet completed",
# but at some later time it will be "completed".
f = Future()

# check the status
print(f.done())


# ----------------------------------------------------------------------------
# Interaction with a Future instance
# ----------------------------------------------------------------------------

async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    # Set the result
    f.set_result('I have finished.')

loop = asyncio.get_event_loop()

# Manually create a Future instance. Note that this instance is (by default)
# tied to our loop, but it is not and will not be attached to any coroutine
# (that’s what Tasks are for).
fut = asyncio.Future()


# Before doing anything, verify that the future is not done yet.
print(fut)
print(fut.done())


# Schedule the main() coroutine, passing the future. 
# Remember, all the main() coroutine does is sleep and then toggle the Future instance. 
# (Note that the main() coroutine will not start running yet: coroutines run only when the loop is running.)
loop.create_task(main(fut))


# Here we use run_until_complete() on a Future instance, rather than a Task instance.
# This is different from what you’ve seen before.
# Now that the loop is running, the main() coroutine will begin executing.
loop.run_until_complete(fut)

print(fut.done())


# Eventually, the future completes when its result is set.
# After completion, the result can be accessed.
print(fut.result())


# ----------------------------------------------------------------------------
# Calling set_result() on a Task:  IS NO LONGER ALLOWED
# ----------------------------------------------------------------------------

from contextlib import suppress

async def main(f: asyncio.Future):
    await asyncio.sleep(1)
    try:
        # A Task instance is being passed in.
        # It satisfies the type signature of the function (because Task is a subclass of Future ),
        # but since Python 3.8, we’re no longer allowed to call set_result() on a Task:
        # an attempt will raise RuntimeError.
        # The idea is that a Task represents a running coroutine,
        # so the result should always come only from that.
        f.set_result('I have finished.')
    except RuntimeError as e:
        print(f'No longer allowed: {e}')
        # We can, however, still cancel() a task,
        # which will raise CancelledError inside the underlying coroutine.
        f.cancel()

loop = asyncio.get_event_loop()


# The only difference is that we create a Task instance instead of a Future.
fut = asyncio.Task(asyncio.sleep(1_000_000))
print(fut.done())

loop.create_task(main(fut))

# Here, 'No longer allowed: Task does not support set_result operation'
with suppress(asyncio.CancelledError):
    loop.run_until_complete(fut)

print(fut.done())

print(fut.cancelled())

