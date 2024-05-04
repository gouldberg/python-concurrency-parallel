import logging
import time
from queue import Empty, Queue
from threading import Thread


# ----------------------------------------------------------------------------
# 複数スレッドを用いてデータに対して並列処理したい場合、固定数のスレッドプールを用意し、
# 先入れ先出し(First In First Out: FIFO)のキューを使って順次データを取り出して処理するのが一般的な方法
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")

THREAD_POOL_SIZE = 3


def myworker(work_queue):
    logging.debug("start")

    # キューが空でない限り繰り返す
    while not work_queue.empty():
        try:
            item = work_queue.get_nowait()
        except Empty:
            break
        else:
            time.sleep(1)
            logging.debug(item)
            # タスク終了 （work_queue.join()で終了を区別するのに必要）
            work_queue.task_done()

    logging.debug("end")


def main():
    logging.debug("start")

    # キューに投入する
    work_queue = Queue()
    vals = [i for i in range(10)]
    for val in vals:
        work_queue.put(val)

    # スレッドプール用意しスレッド開始
    threads = [
        Thread(target=myworker, args=(work_queue,))
        for _ in range(THREAD_POOL_SIZE)
    ]

    for thread in threads:
        thread.start()

    # キューが空になるまで待機
    work_queue.join()

     # 終了を待機
    for thread in threads:
        thread.join()

    logging.debug("end")


if __name__ == "__main__":
    main()
