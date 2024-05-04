import time
import asyncio

# ----------------------------------------------------------------------------
# delay
# ----------------------------------------------------------------------------

# asyncio.sleep itself is coroutine, requiring await keyword
# this means, when a coroutine awaits it, other code will be able to run.

async def delay(delay_seconds: int) -> int:
    print(f'sleeping for {delay_seconds} second(s)')
    await asyncio.sleep(delay_seconds)
    print(f'finished sleeping for {delay_seconds} second(s)')
    return delay_seconds

# This time.sleep() does same thing ...
def delay_no_asyncio(delay_seconds: int) -> int:
    print(f'time.sleep: sleeping for {delay_seconds} second(s)')
    time.sleep(delay_seconds)
    print(f'time.sleep: finished sleeping for {delay_seconds} second(s)')
    return delay_seconds


# ----------------------------------------------------------------------------
# add one and hello world message
# ----------------------------------------------------------------------------

async def add_one(number: int) -> int:
    return number + 1

def add_one_no_async(number: int) -> int:
    return number + 1

async def hello_world_message() -> str:
    await delay(1)
    return 'Hello World!'

def hello_world_message_no_async() -> str:
    delay_no_asyncio(1)
    return 'Hello World!'


# ----------------------------------------------------------------------------
# main: 4 patterns:  sequential model
# ----------------------------------------------------------------------------

async def main_0_0() -> None:
    message = hello_world_message_no_async()
    print(message)
    one_plus_one = add_one_no_async(1)
    print(one_plus_one)


async def main_0_0_2() -> None:
    message = hello_world_message_no_async()
    one_plus_one = add_one_no_async(1)
    print(one_plus_one)
    print(message)


async def main_0_1() -> None:
    message = hello_world_message_no_async()
    print(message)
    one_plus_one = await add_one(1)
    print(one_plus_one)


async def main_1_0() -> None:
    message = await hello_world_message()
    print(message)
    one_plus_one = add_one_no_async(1)
    print(one_plus_one)


async def main_1_1() -> None:
    message = await hello_world_message()
    print(message)
    one_plus_one = await add_one(1)
    print(one_plus_one)


# wait !!
asyncio.run(main_0_0())

# wait !!
asyncio.run(main_0_0_2())

# wait !!
asyncio.run(main_0_1())

# wait !!
asyncio.run(main_1_0())

# wait !!
asyncio.run(main_1_1())

