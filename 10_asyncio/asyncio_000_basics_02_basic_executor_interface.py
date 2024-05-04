import time
import asyncio


# ----------------------------------------------------------------------------
# Executor interface
#   - asyncio provides an API that is very similar to the API in the concurrent.futures package,
#     (ThreadPoolExecutor, ProcessPoolExecutor)
# ----------------------------------------------------------------------------

async def main():
    # ctime: システム時間を ASCII 文字列に変換する 
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')


##############
# This would have blocked the main thread and prevented your event loop from running.
# This means that you must not make this function a coroutine.
# Indeed, you cannot even call this function from anywhere in the main thread, which is where the asyncio loop is running.

# WE SOLVE THIS PROBLEM BY RUNNING THIS FUNCTION IN AN EXECUTOR !!!
def blocking():
    # NOTE: here 0.5 secs < non-blocking sleep time (1 sec) in main()
    time.sleep(0.5)
    print(f'{time.ctime()} Hello from a thread!')
##############

# ----------
loop = asyncio.get_event_loop()

task = loop.create_task(main())


##############
# This is required to run things in a separate thread or even a separate process.

# Here we pass our blocking function to be run in the default executor.
# run_in_executor() does NOT block the main thread, it only schedules the executor task to run.
# (it returns a Future)
# The executor task will begin executing only after run_until_complete() is called.

# run_in_executor() requires as first parameter the Executor instance to use.
# here in order to use the default, None is required.
loop.run_in_executor(None, blocking)
##############


loop.run_until_complete(task)


# The set of tasks in pending does NOT include an entry for the call to blocking() made in run_in_executor().
# all_tasks() really does return ONLY Tasks, NOT Future.
pending = asyncio.all_tasks(loop=loop)

for task in pending:
    task.cancel()
    

# ----------
group = asyncio.gather(*pending, return_exceptions=True)

loop.run_until_complete(group)

loop.close()

