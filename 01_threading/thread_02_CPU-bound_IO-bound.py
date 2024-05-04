import time
from threading import Thread

import select
import socket

# ----------------------------------------------------------------------------
# factorize (CPU-bound):  no threading
# ----------------------------------------------------------------------------

def factorize(number):
    for i in range(1, number + 1):
        if number % i == 0:
            yield i


numbers = [2139079, 1214759, 1516637, 1852285]
start = time.time()

for number in numbers:
    list(factorize(number))

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# ----------------------------------------------------------------------------
# factorize (CPU-bound):  threading
# --> Surprisingly, it took MORE time than the case of no threading (CPU-bound computation)
# ----------------------------------------------------------------------------

class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def run(self):
        self.factors = list(factorize(self.number))

start = time.time()

threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# ----------------------------------------------------------------------------
# low-speed system call (IO-bound):  no threading
# ----------------------------------------------------------------------------

def slow_systemcall():
    select.select([socket.socket()], [], [], 0.1)

start = time.time()

for _ in range(5):
    slow_systemcall()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')


# ----------------------------------------------------------------------------
# low-speed system call (IO-bound):  threading
# ----------------------------------------------------------------------------

start = time.time()

threads = []
for _ in range(5):
    thread = Thread(target=slow_systemcall)
    thread.start()
    threads.append(thread)


def compute_helicopter_location(index):
    pass

for i in range(5):
    compute_helicopter_location(i)

for thread in threads:
    thread.join()

end = time.time()
delta = end - start
print(f'Took {delta:.3f} seconds')
