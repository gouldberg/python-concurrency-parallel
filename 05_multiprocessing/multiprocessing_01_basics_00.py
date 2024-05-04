import time
from multiprocessing import Process


# ----------------------------------------------------------------------------
# 2 parallel process with multiprocessing
# ----------------------------------------------------------------------------

def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter = counter + 1
    end = time.time()
    print(f'Finished counting to {count_to} in {end - start}')
    return counter


# If you do not add this, you may receive the following error:
#  - An attempt has been made to start a new process before the current process has finished its bootstrapping phase.
# The reason this happens is to prevent others who import our code from accidentally launching multiple processes.

if __name__ == '__main__':
    start_time = time.time()
    
    # Create a process to run the countdown function.
    to_one_hundred_million = Process(target=count, args=(10000000,))
    to_two_hundred_million = Process(target=count, args=(20000000,))

    # Start the process. This method returns instantly.
    to_one_hundred_million.start()
    to_two_hundred_million.start()

    # Wait for the process to finish. This method blocks until the process is done.
    # join() method does not return the value our target function returns.
    # In fact, currently there is no way to get the value our function returns
    # without using shared inter-process memory !!
    to_one_hundred_million.join()
    to_two_hundred_million.join()

    # --> We do not know which process wil complete first...

    end_time = time.time()
    print(f'Completed in {end_time - start_time}')

