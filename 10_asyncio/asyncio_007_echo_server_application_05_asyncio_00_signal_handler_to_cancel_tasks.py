import asyncio, signal
from asyncio import AbstractEventLoop
from typing import Set

from util import delay
from util import async_timed


# ----------------------------------------------------------------------------
# Listening for signals
# ----------------------------------------------------------------------------

def cancel_tasks():
    print('Got a SIGINT!')
    tasks: Set[asyncio.Task] = asyncio.all_tasks()
    print(f'Cancelling {len(tasks)} task(s).')
    [task.cancel() for task in tasks]


@async_timed()
async def main():
    loop: AbstractEventLoop = asyncio.get_running_loop()
    # ----------
    # add_signal_handler can safely interact with the event loop.
    # This function takes in a signal we want to listen for and a function that we'll call
    # when our application receives that signal
    loop.add_signal_handler(signal.SIGINT, cancel_tasks)
    await delay(10)


# When we run this application,
# we'll see that our delay coroutine starts right away and waits for 10 seconds.
# If we press CRL-C within these 10 seconds we should see 'got a SIGINT!' printed out,
# followed by a message that we're canceling our tasks.
# We should also see a CancelledError thrown from asyncio.run(main()) 
asyncio.run(main())
