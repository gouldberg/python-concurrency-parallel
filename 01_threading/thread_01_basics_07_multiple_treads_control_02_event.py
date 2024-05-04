import logging
import time
from threading import Event, Thread

# ----------------------------------------------------------------------------
# Event:
# あるスレッドの結果を待ってから、別スレッドを開始
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")


def myworker(event: Event):
    # event.set()を待機
    event.wait()

    logging.debug("start")
    time.sleep(5)
    logging.debug("end")


def event_trigger(event: Event):
    logging.debug("start")
    time.sleep(5)
    logging.debug("end")

    # wait状態のスレッドを起動
    event.set()


def main():
    logging.debug("start")

    # イベントを生成
    event = Event()

    # スレッドを生成
    trigger_thread = Thread(target=event_trigger, args=(event,))
    thread_num = 3
    threads = [
        Thread(target=myworker, args=(event,)) for _ in range(thread_num)
    ]

    # イベント後に起動するスレッドを開始
    for thread in threads:
        thread.start()

    # イベントのトリガーとなるスレッドを開始
    trigger_thread.start()

    # スレッドの終了を待機
    trigger_thread.join()
    for thread in threads:
        thread.join()

    logging.debug("end")


if __name__ == "__main__":
    main()
