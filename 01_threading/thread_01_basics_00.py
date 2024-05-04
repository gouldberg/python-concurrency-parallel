import os
import threading

# THIS SHOULD BE REFERENCED !!!
# https://zenn.dev/bluesilvercat/articles/c492339d1cd20c


# ----------------------------------------------------------------------------
# Process ID, num of threads, thread name
# ----------------------------------------------------------------------------

print(f'Python process running with process id : {os.getpid()}')

total_threads =threading.active_count()
thread_name = threading.current_thread().name

# 1 thread(s)
print(f'Python is currently running {total_threads} thread(s)')

# name is MainThread
print(f'The current thread is {thread_name}')


# ----------------------------------------------------------------------------
# Creating a multithreaded Python application
# ----------------------------------------------------------------------------

def hello_from_thread():
    print(f'Python from thread {threading.current_thread()}!')

hello_thread = threading.Thread(target=hello_from_thread)
hello_thread2 = threading.Thread(target=hello_from_thread)

# ----------
hello_thread.start()
hello_thread2.start()
# ----------

thread_list = threading.enumerate()
total_threads = threading.active_count()
thread_name = threading.current_thread().name

# 1 thread(s)
print(f'Python is currently running {thread_list}')
print(f'Python is currently running {total_threads} thread(s)')

# name is MainThread
print(f'The current thread is {thread_name}')

# join will cause the program to pause until the thread we started completed
hello_thread.join()
hello_thread2.join()






