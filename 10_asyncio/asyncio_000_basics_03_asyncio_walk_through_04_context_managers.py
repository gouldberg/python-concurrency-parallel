import asyncio
import time

from contextlib import contextmanager
from contextlib import asynccontextmanager


# ----------------------------------------------------------------------------
# Async Context Managers:  async with
# ----------------------------------------------------------------------------

async def get_conn(host, port):
    class Conn:
        async def close(self):
            await asyncio.sleep(0)
    await asyncio.sleep(0)
    return Conn()


# NOTE:
# __aenter__ and __aexit__ are useful
# only if you need to await something inside the enter and exit methods.

class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    # Instead of the __enter__() special method for synchronous context managers,
    # the new __aenter__() special method is used.
    # This special method must be an async def method.
    async def __aenter__(self):
        self.conn = await get_conn(self.host, self.port)
        return self.conn

    # Likewise, instead of __exit__(), use __aexit__().
    # The parameters are identical to those for __exit__() and
    # are populated if an exception was raised in the body of the context manager.
    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()


async def main():
    async with Connection('localhost', 9001) as conn:
        # <do stuff with conn >
        pass


# ----------
asyncio.run(main())


# ----------------------------------------------------------------------------
# contextlib way (blocking)
# ----------------------------------------------------------------------------

def download_webpage(url):
    class Data:
        pass
    return Data()


def update_stats(url):
    pass


def process(data):
    pass


# The @contextmanager decorator transforms a generator function into a context manager.
@contextmanager
def web_page(url):
    # ----------
    # This function call (which I made up for this example) looks suspiciously
    # like the sort of thing that will want to use a network interface,
    # which is many orders of magnitude slower than “normal” CPU-bound code.
    # This context manager must be used in a dedicated thread;
    # otherwise, the whole program will be paused while waiting for data.
    data = download_webpage(url)
    yield data
    # ----------
    # Imagine that we update some statistics every time we process data from a URL,
    # such as the number of times the URL has been downloaded.
    # From a concurrency perspective,
    # we would need to know whether this function involves I/O internally,
    # such as writing to a database over a network.
    # If so, update_stats() is also a blocking call.
    update_stats(url)


# Our context manager is being used.
# Note specifically how the network call (to download_webpage() ) is hidden inside the construction of the context manager.
with web_page('google.com') as data:
    # This function call, process(), might also be blocking.
    # We'd have to look at what the function does,
    # because the distinction between what is blocking or non-blocking is not clear-cut. It might be:
    #   • Innocuous and non-blocking (fast and CPU-bound)
    #   • Mildly blocking (fast and I/O-bound, perhaps something like fast
    #     disk access instead of network I/O)
    #   • Blocking (slow and I/O-bound)
    #   • Diabolical (slow and CPU-bound)
    # For the sake of simplicity in this example,
    # let's presume that the call to process() is a fast, 
    # CPU-bound operation and therefore non-blocking.
    process(data)


# ----------------------------------------------------------------------------
# asynccontextmanager (non-blocking)
# ----------------------------------------------------------------------------

async def download_webpage(url):
    class Data:
        pass
    await asyncio.sleep(0)
    return Data()


async def update_stats(url):
    await asyncio.sleep(0)


def process(data):
    pass


# The new @asynccontextmanager decorator is used in exactly the same way.
@asynccontextmanager
async def web_page(url):
    # Added the await keyword, which tells us that this coroutine will allow the event loop to run other tasks
    # while we wait for the network call to complete.
    # ---------
    # convert it into a coroutine.
    data = await download_webpage(url)
    # When called, it will return an asynchronous generator.
    yield data
    # ---------
    await update_stats(url)


async def main():
    # async with instead of a plain with.
    async with web_page('google.com') as data:
        process(data)

asyncio.run(main())


# ----------------------------------------------------------------------------
# Run in executor (non-blocking)
# ----------------------------------------------------------------------------

def download_webpage(url):
    class Data:
        pass
    return Data()


def update_stats(url):
    pass


def process(data):
    pass


# ----------
# Assume we are unable to modify blocking calls.
# We will use and executor to run the blocking calls in a separate thread.
@asynccontextmanager
async def web_page(url):
    loop = asyncio.get_event_loop()
    # We call the executor.
    # The signature is AbstractEventLoop.run_in_executor (executor, func, *args).
    # If you want to use the default executor (which is a ThreadPoolExecutor),
    # you must pass None as the value for the executor argument.
    data = await loop.run_in_executor(None, download_webpage, url)
    yield data
    # Note that you must use the await keyword in front. 
    # If you forget, the execution of the asynchronous generator (i.e., your async context manager) 
    # will not wait for the call to complete before proceeding.
    await loop.run_in_executor(None, update_stats, url)


async def main():
    async with web_page('google.com') as data:
        process(data)

asyncio.run(main())
