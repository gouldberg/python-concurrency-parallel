import logging
import time
from threading import Thread


# ----------------------------------------------------------------------------
# myworker1 : ends at last with sleep(10)
# myworker3 : arguments included
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")

# sleep(10): end at last
def myworker1():
    logging.debug("start")
    time.sleep(10)
    logging.debug("end")

# sleep(5)
def myworker2():
    logging.debug("start")
    time.sleep(5)
    logging.debug("end")

# sleep(5)
def myworker3(x: int, y: int):
    logging.debug("start")
    logging.debug(f"x: {x}, y:{y}")
    time.sleep(5)
    logging.debug("end")


# ----------
# main
def main():
    logging.debug("start")

    # create threads
    thread1 = Thread(target=myworker1, name="myworker1")
    thread2 = Thread(target=myworker2, name="myworker2")
    thread3 = Thread(target=myworker3, name="myworker3", args=(10,), kwargs={"y": 20})

    # start threads
    thread1.start()
    thread2.start()
    thread3.start()

    # wait for ending threads
    thread1.join()
    thread2.join()
    thread3.join()

    logging.debug("end")


if __name__ == "__main__":
    main()

