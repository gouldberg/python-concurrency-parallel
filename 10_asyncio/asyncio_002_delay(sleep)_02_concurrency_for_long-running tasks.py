import asyncio
from util import delay
from util import async_timed

# ----------------------------------------------------------------------------
# Creating a task
# ----------------------------------------------------------------------------

@async_timed()
async def main():
    # ----------
    # create task
    sleep_for_three = asyncio.create_task(delay(3))

    # error
    # sleep_for_three = asyncio.create_task(delay_no_asyncio(3))

    # ----------
    # This print statement is executed immediately after we run the task.
    print(type(sleep_for_three))

    # ----------
    # this will suspend our main coroutine until we have a result from our task.
    result = await sleep_for_three

    # if no await keyword, the task would be scheduled to run, but it would almost immediately be stopped and
    # cleaned up when asyncio.run shut down the event loop
    # result = sleep_for_three

    # ----------
    print(result)

asyncio.run(main())


# ----------------------------------------------------------------------------
# Running multiple tasks concurrently
# ----------------------------------------------------------------------------

@async_timed()
async def main_2():
    sleep_for_three = asyncio.create_task(delay(3))
    sleep_again = asyncio.create_task(delay(3))
    sleep_once_more = asyncio.create_task(delay(3))

    # All three tasks start running and will carry out any sleep operations concurrently.
    await sleep_for_three
    await sleep_again
    await sleep_once_more


# This will complete in about 3 seconds for its concurrency (not 9 seconds)
asyncio.run(main_2())


# ----------------------------------------------------------------------------
# Running while other operations complete
# ----------------------------------------------------------------------------

@async_timed()
async def hello_every_second():
    for i in range(2):
        await asyncio.sleep(1)
        print("I'm running other code while I'm waiting!")


@async_timed()
async def main_3():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))

    # this can be run while first_delay and second_delay are running
    await hello_every_second()

    await first_delay
    await second_delay


@async_timed()
async def main_4():
    first_delay = asyncio.create_task(delay(3))
    second_delay = asyncio.create_task(delay(3))
    
    await first_delay
    await second_delay

    # this run after first_delay and second_delay are finished
    await hello_every_second()



# ----------
# this took almost 3 seconds
asyncio.run(main_3())


# this took almost 5 seconds
asyncio.run(main_4())
