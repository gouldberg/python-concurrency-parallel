import asyncio


# ----------------------------------------------------------------------------
# All the tasks will complete
#  - run_until_complete() and gather(*, return_exceptions=True)
# ----------------------------------------------------------------------------

async def f(delay):
    # It would be awful if someone were to pass in a zero...
    await asyncio.sleep(1 / delay)
    return delay

loop = asyncio.get_event_loop()

for i in range(10):
    loop.create_task(f(i))

pending = asyncio.all_tasks(loop=loop)

group = asyncio.gather(*pending, return_exceptions=True)


# ----------
# 1. run_until_complete() operates on a future; during shutdown, it's the future returned by gather.
# 2. If that future raises an exception, the exception will also be raised out of run_until_complete(), which means that the loop will stop.
# 3. If run_until_complete() is being used on a group future, any exception raised inside any of the subtasks will also be raised
#    in the "group" future if it is not handled in the subtask. Note this includes CancelledError.
# 4. If only some tasks handle CancelledError and others don't, the ones that don't will cause the loop to stop.
#    This means that the loop will be stopped before all the tasks are done.
# 5. For shutdown, we really don't want this behavior.
#    We want run_until_complete() to finish only when all the tasks in the group have finished,
#    regardless of whether some of the tasks raise exceptions.
# 6. Hence we have gather(*, return_exceptions=True):
#    that setting makes the "group" future treat exceptions from the subtasks as returned values,
#    so that they don't bubble out and interfere with run_until_complete()

# An undesirable consequence of capturing exceptions in this way is that
# some errors may escape your attention because they're now (effectively) being handled inside the group task.
# If this is a concern, you can obtain the output list from run_until_complete() and scan it for any subclasses of Exception,
# and then write log messages appropriate for you situation.

# Without return_exceptions=True, if someone were to pass in a zero,
# the ZeroDivisionError would be raised from run_until_complete(), stopping the loop and thus preventing the other tasks from finishing.

results = loop.run_until_complete(group)

print(f'Results: {results}')

loop.close()

