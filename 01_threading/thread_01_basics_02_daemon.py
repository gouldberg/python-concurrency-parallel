import logging
import time
from threading import Thread


# ----------------------------------------------------------------------------
# myworker1 to be Daemon
#   デーモンとは、メインメモリ上に常駐して機能を提供するプログラム
#   デーモンでない生存中のスレッドが全てなくなるとPythonプログラムは終了
# ----------------------------------------------------------------------------
# Now the myworker1 sleep(10) is longer than myworkder2,3 (sleep(5)).
# If myworkder1 IS NOT joined by thread1.join(), MainThread ends by NOT waiting for myworkder1
# If myworkder1 IS joined by thread1.join(), MainThread ends by waiting for ending of myworkder1
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")

# myworker1 sleep(10) is longer than myworker2,3 (sleep(5))
def myworker1():
    logging.debug("start")
    time.sleep(10)
    logging.debug("end")

def myworker2():
    logging.debug("start")
    time.sleep(5)
    logging.debug("end")

def myworker3(x: int, y: int):
    logging.debug("start")
    logging.debug(f"x: {x}, y:{y}")
    time.sleep(5)
    logging.debug("end")


# ----------
# main
def main():
    logging.debug("start")

    # create threads : thread1 to be daemon
    thread1 = Thread(target=myworker1, name="myworker1", daemon=True)
    thread2 = Thread(target=myworker2, name="myworker2")
    thread3 = Thread(target=myworker3, name="myworker3", args=(10,), kwargs={"y": 20})

    # start threads
    thread1.start()
    thread2.start()
    thread3.start()

    # thread1.join() is not required
    # thread1.join()
    thread2.join()
    thread3.join()

    logging.debug("end")


if __name__ == "__main__":
    main()

