import asyncio


# ----------------------------------------------------------------------------
# Use event loop to execute coroutines
# ----------------------------------------------------------------------------

async def f():
    await asyncio.sleep(0)
    return 111


# Obtain a loop.
loop = asyncio.get_event_loop()

coro = f()

# Run the coroutine to completion.
# Internally, this is doing all those .send(None) method calls for us, and it detects completion of our coroutine
# with the StopIteration exception, which also contains our return value.
loop.run_until_complete(coro)


# ----------------------------------------------------------------------------
# Event loop:  get_event_loop(), callable from anywhere
#   - This works only within the same thread and get the same event loop.
#     It will fail if called inside a new thread unless you specifically create a new loop with new_event_loop(),
#     AND set that new instance to e the loop for that thread by calling set_event_loop().
# ----------------------------------------------------------------------------

loop = asyncio.get_event_loop()

loop2 = asyncio.get_event_loop()


# Both identifiers, loop and loop2 , refer to the same instance.
print(f'loop  : {loop}')
print(f'loop2 : {loop2}')

print(loop is loop2)


# ----------------------------------------------------------------------------
# Event loop:  get_running_loop() (>= Python3.8), callable from inside the context of a coroutine
#   - Accept a loop parameter, just in case your users are doing something unusual with even loop policies.
#   ^ It can be called only within the context of a coroutine, a task, or a function called from one of those.
#   - Always provides the CURRENT running event loop
#   - simplify the spawning of background tasks
# ----------------------------------------------------------------------------

