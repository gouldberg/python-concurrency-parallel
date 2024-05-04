import logging
import time
from threading import Barrier, Thread

# ----------------------------------------------------------------------------
# Barrier:
# Barrierは、複数のスレッドが特定の同期点に達するまで待機し、その後すべてのスレッドが同時に動作を再開するための機構。
# Barrierで指定した数のスレッドがすべてwaitメソッドを呼び出すまで、いずれのスレッドも進行できなくなる。
# ----------------------------------------------------------------------------
# 以下では、スレッドの動作は、起動した後は無限ループになっているため手動で終了する必要
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")


def server(barrier: Barrier):
    logging.debug("start")

    # バリア数スレッドが起動するまで待機
    barrier.wait()

    while True:
        logging.debug("execution")
        time.sleep(5)


def client(barrier: Barrier):
    time.sleep(5)
    logging.debug("start")

    # バリア数スレッドが起動するまで待機
    barrier.wait()

    while True:
        logging.debug("execution")
        time.sleep(5)


def main():
    logging.debug("start")

    # バリアを生成
    barrier = Barrier(2)

    # スレッドの生成
    server_thread = Thread(target=server, args=(barrier,))
    client_thread = Thread(target=client, args=(barrier,))

    # スレッドを開始
    server_thread.start()
    client_thread.start()

    # スレッドの終了を待機
    server_thread.join()
    client_thread.join()

    logging.debug("end")


if __name__ == "__main__":
    main()
