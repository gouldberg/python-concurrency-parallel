import time
from multiprocessing import Process, Pool
import multiprocessing


# ----------------------------------------------------------------------------
# count
# ----------------------------------------------------------------------------

def count(count_to: int) -> int:
    start = time.time()
    counter = 0
    while counter < count_to:
        counter = counter + 1
    end = time.time()
    print(f'Finished counting to {count_to} in {end - start}')
    return counter


# ----------------------------------------------------------------------------
# say hello
# ----------------------------------------------------------------------------

def say_hello(name: str) -> str:
    return f'Hi there, {name}'


# CPU cores count
print(f'multiprocessing cpu count : {multiprocessing.cpu_count()}')

if __name__ == '__main__':
    # Create a new process pool.
    with Pool() as process_pool:
        # Run in separate process and get result
        # By apply method, we do not need to start the process or call join on it ourselves.
        # NOTE: This apply method blocks until our function completes.
        hi_jeff = process_pool.apply(say_hello, args=('Jeff',))
        hi_john = process_pool.apply(say_hello, args=('John',))
    
        print(hi_jeff)
        print(hi_john)


# ----------------------------------------------------------------------------
# apply_async:
# Since we call get on hi_jeff first, our program here would block some seconds before printing our hi_john message
# even though we were ready after shorter seconds.
# ----------------------------------------------------------------------------

if __name__ == '__main__':
    with Pool() as process_pool:
        # apply_async method returns AsyncResult instantly and will start running the process
        # in the background.
        hi_jeff = process_pool.apply_async(say_hello, args=('Jeff',))
        hi_john = process_pool.apply_async(say_hello, args=('John',))

        # Once we have an AsyncResult, we can use its get method to block and obtain the results
        # of our function call.
        print(hi_jeff.get())
        print(hi_john.get())

