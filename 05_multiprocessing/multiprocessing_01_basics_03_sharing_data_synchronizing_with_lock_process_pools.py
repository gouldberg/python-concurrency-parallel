from multiprocessing import Process, Value, Array
from concurrent.futures import ProcessPoolExecutor
import asyncio

# ----------------------------------------------------------------------------
# Not shared
#   Multiprocessing supports two kinds of shared data: values and array.
# ----------------------------------------------------------------------------

def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1


def increment_array(shared_array: Array):
    for index, integer in enumerate(shared_array):
        shared_array[index] = integer + 1


if __name__ == '__main__':
    integer = Value('i', 0)
    integer_array = Array('i', [0, 0])
    
    procs = [
        Process(target=increment_value, args=(integer,)),
        Process(target=increment_array, args=(integer_array,)),
    ]
    
    [p.start() for p in procs]
    [p.join() for p in procs]
    
    print(integer.value)
    print(integer_array[:])


# ----------------------------------------------------------------------------
# Shared data and race condition
# ----------------------------------------------------------------------------

def increment_value(shared_int: Value):
    shared_int.value = shared_int.value + 1


# Sometimes our result is 1 (not 2).
# We have encountered in race condition.
# A race condition occurs when the outcome of a set of operations is dependent on which operation finishes first.
# The problem lies in that incrementing a value involves both read and write operations.
# To increment a value, we first need to read the value, add one to it, then write the result back to memory.

if __name__ == '__main__':
    for _ in range(100):
        integer = Value('i', 0)
        
        procs = [
            Process(target=increment_value, args=(integer,)),
            Process(target=increment_value, args=(integer,)),
        ]
        
        [p.start() for p in procs]
        [p.join() for p in procs]
        
        print(integer.value)
        assert(integer.value == 2)


# ----------------------------------------------------------------------------
# Fix race condition by synchronizing with locks
# ----------------------------------------------------------------------------

# def increment_value(shared_int: Value):
#     shared_int.get_lock().acquire()
#     shared_int.value = shared_int.value + 1
#     shared_int.get_lock().release()


# This is same was above.
# The locks are also context managers, this will acquire and release the lock for us automatically.
def increment_value(shared_int: Value):
    with shared_int.get_lock():
        shared_int.value = shared_int.value + 1


if __name__ == '__main__':
    for _ in range(100):
        integer = Value('i', 0)
        
        procs = [
            Process(target=increment_value, args=(integer,)),
            Process(target=increment_value, args=(integer,)),
        ]
        
        [p.start() for p in procs]
        [p.join() for p in procs]
        
        print(integer.value)
        assert(integer.value == 2)


# ----------------------------------------------------------------------------
# Sharing data with process pools
# ----------------------------------------------------------------------------

shared_counter: Value


def init(counter: Value):
    global shared_counter
    shared_counter = counter


def increment():
    with shared_counter.get_lock():
        shared_counter.value += 1


async def main():
    counter = Value('d', 0)
    # This tells the pool to execute the function init with the argument counter for each process
    with ProcessPoolExecutor(initializer=init, initargs=(counter,)) as pool:
        await asyncio.get_running_loop().run_in_executor(pool, increment)
        print(counter.value)


if __name__ == '__main__':
    asyncio.run(main())
