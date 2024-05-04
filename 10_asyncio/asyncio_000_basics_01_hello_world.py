import time
import asyncio


# ----------------------------------------------------------------------------
# asyncio hello-world 
# ----------------------------------------------------------------------------

async def main():
    # ctime: システム時間を ASCII 文字列に変換する 
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


# ----------
# Get loop instance before running any coroutines.
loop = asyncio.get_event_loop()

# ----------
# create_task() schedules coroutine to be run n the loop.
# returned task object can be used to monitor the status of the task.
# You can cancel the task with task.cancel()
task = loop.create_task(main())

# ----------
# block the current thread, which will usually be the main thread.
# run_until_complete() will keep the loop running only until the given coroutine completes.
# but all OTHER tasks schedules on the loop will also run while the loop is running.
# Internally, asyncio.run() calls run_until_complete() and blocks the main thread in the same way.
loop.run_until_complete(task)


pending = asyncio.all_tasks(loop=loop)

for task in pending:
    task.cancel()
    

# ----------
# gather the still-pending tasks
# NOTE: asyncio.run() will do all of the cancelling, gathering, and waiting for pending tasks to finish up.
group = asyncio.gather(*pending, return_exceptions=True)

# after still-pending tasks are gathered, run_until_complete() again until those tasks are done. 
loop.run_until_complete(group)


# ----------
# This must be called on a stopped loop, and it will clear all queues and shut down the executor.
# A stopped loop can be restarted, but a closed loop s gone for good.
# Internally, asyncio.run() will close the loop before returning. run() creates a new event loop every time you call it.
loop.close()
