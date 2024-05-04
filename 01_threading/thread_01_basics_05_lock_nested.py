import logging
import time
from threading import Thread, RLock


# ----------------------------------------------------------------------------
# Nested Rock by RLock
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")

# now the lock is RLock
def mycounter(d: dict, lock: RLock):
    with lock:
        tmp = d["x"]
        time.sleep(1)
        d["x"] = tmp + 1
        # Nested lock
        with lock:
            tmp = d["x"]
            time.sleep(1)
            d["x"] = tmp + 1


def main():
    logging.debug("start")
    data = {"x": 0}
    thread_num = 5

    # ----------
    # now the lock is RLock
    lock = RLock()

    # args have lock
    threads = [
        Thread(target=mycounter, args=(data, lock)) for _ in range(thread_num)
    ]

    # all threads start almost simultaneously
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    logging.debug(data)
    logging.debug("end")


if __name__ == "__main__":
    main()
