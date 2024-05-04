import logging
import time
from threading import Thread
from threading import Timer


# ----------------------------------------------------------------------------
# myworker3 thread is created by threading.Timer and start 5 seconds with delay 
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")

def myworker1():
    logging.debug("start")
    time.sleep(5)
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

    thread1 = Thread(target=myworker1, name="myworker1")
    thread2 = Thread(target=myworker2, name="myworker2")

    # thread 3 start after 5 seconds
    thread3 = Timer(5, myworker3, args=(10,), kwargs={"y": 20})

    # start threads
    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()

    logging.debug("end")


if __name__ == "__main__":
    main()
