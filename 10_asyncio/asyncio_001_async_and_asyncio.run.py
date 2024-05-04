import time
import asyncio

# ----------------------------------------------------------------------------
# coroutines vs. normal function
# ----------------------------------------------------------------------------

async def my_coroutine() -> None:
    print('Hello world')

async def coroutine_add_one(number: int) ->int:
    return number + 1

def add_one(number: int) -> int:
    return number + 1


# ----------
function_result = add_one(1)

# we get a coroutine object
coroutine_result = coroutine_add_one(1)

print(f'Function result is {function_result} and the type is {type(function_result)}')
print(f'Coroutine result is {coroutine_result} and the type is {type(coroutine_result)}')


# ----------------------------------------------------------------------------
# Run Coroutine
# ----------------------------------------------------------------------------

# run coroutine:  It is intended to be the main entry point into the asyncio application.
# - asyncio.run create a brand-new event. Once it successfully does so, it takes whichever coroutine we pass into it
#   and runs it until it completes, returning the result.
# - Do some clean up of anything that might be left running after the main coroutine finishes.
#   Once everything has finished, it shuts down and closes the event loop.
result = asyncio.run(coroutine_add_one(1))

print(f'{result}')


# ----------------------------------------------------------------------------
# Pausing execution with the await keyword
# ----------------------------------------------------------------------------

# add async keyword to add_one function
async def add_one(number: int) -> int:
    return number + 1

# use await keyword
async def main() -> None:

    # Pause parent coroutine (main) and wait for the result of add_one(1)
    # one_plus_one is NOT coroutine object
    one_plus_one = await add_one(1)
    print(one_plus_one)

    # Pause parent coroutine (main) and wait for the result of add_one(2)
    two_plus_one = await add_one(2)
    print(two_plus_one)


asyncio.run(main())
