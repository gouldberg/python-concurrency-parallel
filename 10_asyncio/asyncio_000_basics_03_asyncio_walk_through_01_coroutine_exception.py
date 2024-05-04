import asyncio
import inspect


# ----------------------------------------------------------------------------
# Async functions are functions, not coroutines
# ----------------------------------------------------------------------------

# This is the simplest possible declaration of a coroutine: it looks like a
# regular function, except that it begins with the keywords async def.

async def f():
    return 123

# The precise type of f is not "coroutine", just an ordinary function.
# Strictly speaking, this is coroutine function.
print(f'type : {type(f)}')
print(inspect.iscoroutinefunction(f))
print(inspect.iscoroutine(f))


# This is coroutine
coro = f()
print(f'type : {type(coro)}')
print(inspect.iscoroutinefunction(coro))
print(inspect.iscoroutine(coro))


# This behavior is identical to the way generator function.

def g():
    yield 123

_g = g()

print(f'type : {type(g)}')  # function
print(inspect.isgeneratorfunction(g))
print(inspect.isgenerator(g))

print(f'type : {type(_g)}')  # generator
print(inspect.isgeneratorfunction(_g))
print(inspect.isgenerator(_g))


# ----------------------------------------------------------------------------
# Start and End of executing coroutine
# ----------------------------------------------------------------------------

async def f():
    return 123

coro = f()

try:
    # A coroutine is initiated by “sending” it a None.
    # Internally, this is what the event loop is going to be doing to your precious coroutines;
    # you will never have to do this manually. 
    # All the coroutines you make will be executed either with loop.create_task(coro) or await coro.
    # It’s the loop that does the .send(None) behind the scenes.
    coro.send(None)
except StopIteration as e:
    # When the coroutine returns, a special kind of exception is raised, called StopIteration.
    # Note that we can access the return value of the coroutine via the value attribute of the exception itself.
    # Again, you don’t need to know that it works like this:
    # from your point of view, async def functions will simply return a value with the return statement,
    # just like normal functions.
    print('The answer was:', e.value)


# ----------------------------------------------------------------------------
# calling async function produces a coroutine, meaning as we are allowed to await it.
# ----------------------------------------------------------------------------

async def f():
    await asyncio.sleep(1.0)
    return 123


async def main():
    # Calling f() produces a coroutine; this means we are allowed to await it.
    # The value of the result variable will be 123 when f() completes.
    result = await f()
    return result

# this return the result
res = asyncio.run(main())

print(res)


# ----------------------------------------------------------------------------
# coro.throw() to inject exceptions into a coroutine
# ----------------------------------------------------------------------------

async def f():
    await asyncio.sleep(0)

coro = f()

coro.send(None)

# Instead of doing another send(),
# we call throw() and provide an exception class and a value.
# This raises an exception inside our coroutine, at the await point.
coro.throw(Exception, 'blah')


# ----------------------------------------------------------------------------
# Exception is injected into the coroutine from outside by event loop
# ----------------------------------------------------------------------------

async def f():
    try:
        while True:
            await asyncio.sleep(0)
    # Our coroutine function now handles an exception.
    # In fact, it handles the specific exception type used throughout the asyncio library for task cancellation:
    # asyncio.CancelledError.
    # Note that the exception is being injected into the coroutine from outside;
    # i.e., by the event loop, which we’re still simulating with manual send() and throw() commands.
    # In real code, which you’ll see later, CancelledError is raised inside the task-wrapped coroutine when tasks are cancelled.
    except asyncio.CancelledError:
        # A simple message to say that the task got cancelled.
        # Note that by handling the exception, we ensure it will no longer propagate and
        # our coroutine will return .
        print('I was cancelled!')
    else:
        return 111

coro = f()
coro.send(None)
coro.send(None)

# Here we throw() the CancelledError exception.
coro.throw(asyncio.CancelledError)

# After we run, we should notice:
# - As expected, we see our cancellation message being printed.
# - Our coroutine exits normally. (Recall that the StopIteration exception is the normal way that coroutines exit.)


# ----------------------------------------------------------------------------
# Exception with awaitable:  Absorb cancel and move on
#   - DON'T DO THIS, this is only for educational purposes
# ----------------------------------------------------------------------------

async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        print('Nope!')
        # Instead of printing a message, what happens if after cancellation,
        # we just go right back to awaiting another awaitable?
        while True:
            await asyncio.sleep(0)
    else:
        return 111

coro = f()

coro.send(None)

# Unsurprisingly, our outer coroutine continues to live, and it immediately
# suspends again inside the new coroutine.
coro.throw(asyncio.CancelledError)

# Everything proceeds normally, and our coroutine continues to suspend and
# resume as expected.
coro.send(None)

