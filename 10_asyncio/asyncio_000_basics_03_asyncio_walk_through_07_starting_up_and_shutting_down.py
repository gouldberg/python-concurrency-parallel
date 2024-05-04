import asyncio
from asyncio import StreamREader, StreamWriter

import time


# ----------------------------------------------------------------------------
# Destroyer of pending tasks
# ----------------------------------------------------------------------------

async def f(delay):
    await asyncio.sleep(delay)

loop = asyncio.get_event_loop()

# Task 1 will run for 1 second.
t1 = loop.create_task(f(1))

# Task 2 will run for 2 seconds.
t2 = loop.create_task(f(2))

# Run only until task 1 is complete.
loop.run_until_complete(t1)

loop.close()


# -->
# If you run this scrip by 'python3 .....py' in terminal,
# following output is produced:
#  Task was destroyed but it is pending!

# This error is telling you that some tasks had not yet been completed when the loop was closed.
# Still, asyncio.run() does all of collecting all unfinished tasks, cancelling them,
# and then letting them all finish before closing the loop.


# ----------------------------------------------------------------------------
# Asyncio application life cycle based on the TCP echo server
# NOTE:  After starting server, you can telnet to and interact with it.
#   - 'telnet 127.0.0.1 8888'
#
# --> The client (Telenet) closed the connection before the server was stopped.
#     If we shut down the server while a connection is active, exception handler for CancelledError is raised.
# ----------------------------------------------------------------------------

# This echo() coroutine function will be used (by the server)
# to create a coroutine for each connection made.
# The function is using the streams API for networking with asyncio .

async def echo(reader: StreamReader, writer: StreamWriter):
    print('New connection.')
    try:
        while data := await reader.readline():
            # Return the data back to the sender.
            writer.write(data.upper())
            await writer.drain()
        print('Leaving Connection.')
    except asyncio.CancelledError:
        print('Connection dropped!')


async def main(host='127.0.0.1', port=8888):
    # starting a TCP server.
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')


# ----------------------------------------------------------------------------
# Creating a task inside a cancellation handler of our existing "echo" task  -->  still bugs.
#
#  --> When we press Ctrl-C, all the currently active tasks are collected and cancelled.
#      At this point, only those tasks are then awaited, and asyncio.run() returns immediately after that.
#      The new task created inside the cancellation handler of our existing "echo" task is created only after asyncio.run()
#      had collected and cancelled all the tasks in the process.
# ----------------------------------------------------------------------------

# Pretend that this coroutine actually contacts an external server to submit event notifications.
async def send_event(msg: str):
    await asyncio.sleep(1)


async def echo(reader: StreamReader, writer: StreamWriter):
    print('New connection.')
    try:
        while (data := await reader.readline()):
            writer.write(data.upper())
            await writer.drain()
        print('Leaving Connection.')
    except asyncio.CancelledError:
        msg = 'Connection dropped!'
        print(msg)
        # Because the event notifier involves network access,
        # it is common for such calls to be made in a separate async task;
        # that's why we're using the create_task() function here.
        asyncio.create_task(send_event(msg))


async def main(host='127.0.0.1', port=8888):
    server = await asyncio.start_server(echo, host, port)
    async with server:
        await server.serve_forever()
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')


# ----------------------------------------------------------------------------
# Option-A:  wrap the executor call inside a coroutine
# ----------------------------------------------------------------------------

async def main():
    loop = asyncio.get_running_loop()
    # The idea aims at fixing the shortcoming that run_in_executor() returns only a Future instance and not a task.
    # We can’t capture the job in all_tasks() (used within asyncio.run()),
    # but we can use await on the future.
    # The first part of the plan is to create a future inside the main() function.
    future = loop.run_in_executor(None, blocking)
    try:
        print(f'{time.ctime()} Hello!')
        await asyncio.sleep(1.0)
        print(f'{time.ctime()} Goodbye!')
    finally:
        # We can use the try/finally structure to ensure that we wait for the future to be finished
        # before the main() function returns.
        await future


def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')


# ----------------------------------------------------------------------------
# Option-B:  add the executor future to the gathered tasks
# ----------------------------------------------------------------------------

# This utility function make_coro() simply waits for the future to complete
# but crucially, it continues to wait for the future even inside the exception handler for CancelledError.
async def make_coro(future):
    try:
        return await future
    except asyncio.CancelledError:
        return await future


async def main():
    loop = asyncio.get_running_loop()
    future = loop.run_in_executor(None, blocking)
    # We take the future returned from the run_in_executor() call and
    # pass it into a new utility function, make_coro(). 
    # The important point here is that we’re using create_task(), 
    # which means that this task will appear in the list of all_tasks() within the shutdown handling of asyncio.run(),
    # and will receive a cancellation during the shutdown process.
    asyncio.create_task(make_coro(future))
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Bye!')


# ----------------------------------------------------------------------------
# Option-C: just like camping, bring your own loop and your own
# ----------------------------------------------------------------------------

from concurrent.futures import ThreadPoolExecutor as Executor


async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')
    loop.stop()


def blocking():
    time.sleep(2.0)
    print(f"{time.ctime()} Hello from a thread!")


loop = asyncio.get_event_loop()

# This time, we create our own executor instance.
executor = Executor()

# We have to set our custom executor as the default one for the loop. This
# means that anywhere the code calls run_in_executor(), it’ll be using our
# custom instance.
loop.set_default_executor(executor)
loop.create_task(main())

# As before, we run the blocking function.
future = loop.run_in_executor(None, blocking)

try:
    loop.run_forever()
except KeyboardInterrupt:
    print('Cancelled')

tasks = asyncio.all_tasks(loop=loop)

for t in tasks:
    t.cancel()

group = asyncio.gather(*tasks, return_exceptions=True)

loop.run_until_complete(group)


# Finally, we can explicitly wait for all the executor jobs to finish before closing the loop.
# This will avoid the "Event loop is closed" messages that we saw before.
# We can do this because we have access to the executor object;
# the default executor is not exposed in the asyncio API, which is why we cannot call shutdown() on it
# and were forced to create our own executor instance.

executor.shutdown(wait=True)

loop.close()
