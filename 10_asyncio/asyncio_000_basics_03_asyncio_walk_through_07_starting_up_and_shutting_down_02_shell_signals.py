import asyncio

# Import the signal values from the standard library signal module.
from signal import SIGINT, SIGTERM


# ----------------------------------------------------------------------------
# Using KeyboardInterrupt as SIGINT handler
# ----------------------------------------------------------------------------

async def main():
    while True:
        print('<Your app is running>')
        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = loop.create_task(main())
    try:
        loop.run_until_complete(task)
    # In this case, only Ctrl-C will stop the loop.
    # Then we handle KeyboardInterrupt and do all the necessary cleanup bits
    except KeyboardInterrupt:
        print('Got signal: SIGINT, shutting down.')
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()


# ----------------------------------------------------------------------------
# Handle both SIGINT and SIGTERM, but stop the loop only once
# ----------------------------------------------------------------------------

async def main():
    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    # This time, our main() coroutine is going to do some cleanup internally.
    # When the cancellation signal is received (initiated by cancelling each of the tasks),
    # there will be a period of 3 seconds where main() will continue running
    # during the run_until_complete() phase of the shutdown process.
    except asyncio.CancelledError:
        for i in range(3):
            print('<Your app is shutting down...>')
            await asyncio.sleep(1)


# callback handler for when we receive a signal.
# configured on the loop via the call to add_signal_handler().
def handler(sig):
    # ----------
    # stop the loop:
    #   this will unblock the loop.run_forever() call and 
    #   allow pending task collection and cancellation, and the run_complete() for shutdown.
    loop.stop()
    print(f'Got signal: {sig!s}, shutting down.')
    # ----------
    # Since we are now in shutdown mode, we don't want another SIGINT or SIGTERM to trigger this handler again:
    # that would call loop.stop() during the run_until_complete() phase,
    # which would interfere with our shutdown process.
    # Therefore, we remove the signal handler for SIGTERM from the loop.
    loop.remove_signal_handler(SIGTERM)
    # ----------
    # This is a "gotcha" : we can't simply remove the handler for SIGINT,
    # because if we did that, KeyboardInterrupt would again become the handler for SIGINT,
    # the same as it was before we added our own handlers.
    # Instead, we set an empty lambda function as the handler.
    # This means that KeyboardInterrupt stays away, and SIGINT (and Ctrl-C) has no effect.
    loop.add_signal_handler(SIGINT, lambda: None)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # ----------
    # Setting a handler on SIGINT means a KeyboardInterrupt will no longer be raised on SIGINT.
    # The raising of a KeyboardInterrupt is the “default” handler for SIGINT and is preconfigured in Python
    # until you do something to change the handler, as we’re doing here.
    for sig in (SIGTERM, SIGINT):
        loop.add_signal_handler(sig, handler, sig)
    loop.create_task(main())
    # ----------
    # execution blocks on run_forever() until something stops the loop.
    # In this case, the loop will be stopped inside handler() if either SIGINT or SIGTERM is sent to our process.
    loop.run_forever()
    tasks = asyncio.all_tasks(loop=loop)
    for t in tasks:
        t.cancel()
    group = asyncio.gather(*tasks, return_exceptions=True)
    loop.run_until_complete(group)
    loop.close()


# ----------------------------------------------------------------------------
# Signal handling when using asyncio.run()
# ----------------------------------------------------------------------------

async def main():
    loop = asyncio.get_running_loop()
    for sig in (SIGTERM, SIGINT):
        # Because asyncio.run() takes control of the event loop startup,
        # our first opportunity to change signal handling behavior will be in the main() function.
        loop.add_signal_handler(sig, handler, sig)
    try:
        while True:
            print('<Your app is running>')
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        for i in range(3):
            print('<Your app is shutting down...>')
            await asyncio.sleep(1)


def handler(sig):
    loop = asyncio.get_running_loop()
    # initiate task cancellation here, which will ultimately result in the main() task exiting;
    # when that happens, the cleanup handling inside asyncio.run() will take over.
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()
    print(f'Got signal: {sig!s}, shutting down.')
    loop.remove_signal_handler(SIGTERM)
    loop.add_signal_handler(SIGINT, lambda: None)


if __name__ == '__main__':
    asyncio.run(main())
