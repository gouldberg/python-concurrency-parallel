import asyncio
from util import delay
from util import async_timed


# ----------------------------------------------------------------------------
# Manually creating the event loop
# ----------------------------------------------------------------------------

async def main():
    await asyncio.sleep(1)


loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
finally:
    # If we want any special cleanup logic, we do so here in finally clause.
    loop.close()


# ----------------------------------------------------------------------------
# Accessing the event loop
#
#   get_running_loop() gets you access the event loop.
#   This potentially create a new event loop if it is called when one is not already running.
#   Recommended to use get_running_loop
#   as this will throw an exception if an event loop is'nt running, avoiding any surprises.
# ----------------------------------------------------------------------------

@async_timed()
async def call_later():
    print("I'm being called in the future!")


@async_timed()
async def main():    
    loop = asyncio.get_running_loop()
    loop.call_soon(call_later)
    await delay(1)


asyncio.run(main())

