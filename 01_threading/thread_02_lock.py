import time
from threading import Thread, Barrier
from threading import Lock

# ----------------------------------------------------------------------------
# no lock
# ----------------------------------------------------------------------------

class Counter:
    def __init__(self):
        self.count = 0

    def increment(self, offset):
        self.count += offset


def worker(sensor_index, how_many, counter):
    # I have a barrier in here so the workers synchronize
    # when they start counting, otherwise it's hard to get a race
    # because the overhead of starting a thread is high.
    BARRIER.wait()
    for _ in range(how_many):
        # Read from the sensor
        # Nothing actually happens here, but this is where
        # the blocking I/O would go.
        counter.increment(1)

BARRIER = Barrier(5)

how_many = 10**5

counter = Counter()
threads = []
for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()


expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')


# ----------------------------------------------------------------------------
# with lock
# ----------------------------------------------------------------------------

class LockingCounter:
    def __init__(self):
        self.lock = Lock()
        self.count = 0

    def increment(self, offset):
        with self.lock:
            self.count += offset

BARRIER = Barrier(5)
counter = LockingCounter()

for i in range(5):
    thread = Thread(target=worker,
                    args=(i, how_many, counter))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

expected = how_many * 5
found = counter.count
print(f'Counter should be {expected}, got {found}')