import logging
import time
from multiprocessing.dummy import Pool as ThreadPool


# ----------------------------------------------------------------------------
# multiprocessing.dummy:
# 同じAPIを利用してマルチスレッドを実現したい場合には、multiprocessing.dummyが便利
# これにより、コードの大部分を変更することなく、プロセスの代わりにスレッドを使用して並列処理を行うことができる
# queue.Queueを利用して作成したスレッドプールと同じような動作をPoolクラスで実現できる
# ----------------------------------------------------------------------------

# ここも参考にするとよい
# https://tech.nkhn37.net/python-multiprocessing-basics/

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")

# スレッドプールのサイズ
THREAD_POOL_SIZE = 3


def myworker(x: int):
    logging.debug("start")

    time.sleep(1)

    logging.debug(f"end: {x}")


def main():
    logging.debug("start")

    # 表示したい値のリスト
    vals = [i for i in range(10)]

    # スレッドプールの使用
    with ThreadPool(THREAD_POOL_SIZE) as pool:
        results = pool.map_async(myworker, vals)

        # map_asyncは非同期なので↓はすぐに表示
        logging.debug("execute")

        # getを実行したら動作する
        logging.debug(results)
        results.get()

    logging.debug("end")


if __name__ == "__main__":
    main()
