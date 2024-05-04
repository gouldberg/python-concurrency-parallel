import logging
import time
from threading import Thread, Lock


# ----------------------------------------------------------------------------
# lock each thread
#   - data is accessed by each thread with lock, and value x is shared by all threads and updated.
#   - without lock, value x is all 1 (not shared across threads)
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")


def mycounter(d: dict, lock: Lock):
    with lock:
        logging.debug("start")

        tmp = d["x"]
        time.sleep(1)
        d["x"] = tmp + 1

        logging.debug(f"end {d}")

    # # with句を使わない場合の以下と同じ
    # # ロックを取得
    # lock.acquire()
    # # 以下のブロックがロックされる
    # tmp = d["x"]
    # time.sleep(1)
    # d["x"] = tmp + 1
    # # ロックをリリース
    # lock.release()


def main():
    logging.debug("start")
    data = {"x": 0}
    thread_num = 5

    # ----------
    lock = Lock()

    # args have lock
    threads = [
        Thread(target=mycounter, args=(data, lock)) for _ in range(thread_num)
    ]

    # all threads start almost simultanesouly
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    logging.debug(data)
    logging.debug("end")

if __name__ == "__main__":
    main()
