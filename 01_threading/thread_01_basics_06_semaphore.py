import logging
import sqlite3
from threading import Semaphore, Thread


# ----------------------------------------------------------------------------
# Semaphore
#  セマフォは、特定のリソース上で同時に動作できるプロセスやスレッドの数を制御、セマフォにより同時実行数を制限できる。
#  仮想的にデータベースへのアクセス数をセマフォを用いて一定数に制限する例
# ----------------------------------------------------------------------------

logging.basicConfig(level=logging.DEBUG, format="%(threadName)s: %(message)s")


def dbaccess(dbname: str, sema: Semaphore):
    # now not Lock but Semaphore
    with sema:
        logging.debug("start")

        # connect to DB
        conn = sqlite3.connect(dbname)
        curs = conn.cursor()

        # search DB
        select_all_sql = "SELECT * FROM person"
        curs.execute(select_all_sql)
        rows = curs.fetchall()

        # close DB
        curs.close()
        conn.close()
        logging.debug(f"end: {rows}")


def main():
    logging.debug("start")

    # ----------
    # DB Create

    dbname = "test.db"

    conn = sqlite3.connect(dbname)
    curs = conn.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS person ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT"
        ",name VARCHAR"
        ",age INTEGER)"
    )
    insert_sql = "INSERT INTO person(name, age) VALUES(?, ?)"
    curs.execute(insert_sql, ("TARO", 30))
    conn.commit()
    curs.close()
    conn.close()
    # ----------

    # now thread number is 5, but limit to 3 for DB connections 
    max_connections = 3
    thread_num = 5

    # ----------
    # create Semaphore
    sema = Semaphore(max_connections)

    threads = [
        Thread(target=dbaccess, args=(dbname, sema)) for _ in range(thread_num)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    logging.debug("end")


if __name__ == "__main__":
    main()

