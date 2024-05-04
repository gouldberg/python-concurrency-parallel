import asyncio, signal
import socket
from asyncio import AbstractEventLoop
from typing import Set, List

import logging

from util import delay
from util import async_timed

# For this application, we need to connecting to a server with Telnet.
#   - install telnet:  apt-get install telnet
#   - connect to localhost on port 8000:  telnet localhost 8000
#   - send message (for example):  'testing123' in command terminal


# ----------------------------------------------------------------------------
# Building an asyncio echo server with graceful shutdown
#   - This server can handle many users concurrently, all within one single thread.
#   - Assuming we have at least one client connected, if we stop this application with either CTRL-C
#     or we issue kill command to our process, our shutdown logic will execute.
#     We will see the application wait for 2 seconds, while it allows our echo tasks some time to finish
#     before it stops running.
#   - But this is not a production-worthy shutdown.
#       - We do not shut down our connection listener while we are waiting for our echo tasks to complete.
#         As we are shutting down, a new connection could come in and then we won't be able to add a 2-second shutdown.
#       - We await every echo task we are shutting down and only catch TimeoutExceptions. 
#         If one of our tasks threw something other than that, we would capture that exception and any other subsequent tasks
#         that may have had an exception will be ignored.
# ----------------------------------------------------------------------------

async def echo(connection: socket, loop: AbstractEventLoop) -> None:
    try:
        # Loop forever waiting for data from a client connection
        while data := await loop.sock_recv(connection, 1024):
            print('got data!')
            if data == b'boom\r\n':
                raise Exception('Unexpected network error')
            # Once we have data, send it back to that client.
            await loop.sock_sendall(connection, data)
    except Exception as ex:
        logging.exception(ex)
    finally:
        # shut down the socket
        connection.close()


echo_tasks = []

# Coroutine for listening for connections.
async def connection_listener(server_socket, loop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Got a connection from {address}')
        # ----------
        # Whenever we get a connection, create an echo task to listen for client data.
        # Once a client connects, or coroutine spawns an echo task for each client
        # which then listens for data and writes it back out to the client.
        echo_task = asyncio.create_task(echo(connection, loop))
        echo_tasks.append(echo_task)

# ----------
# graceful shutdown
class GracefulExit(SystemExit):
    pass

def shutdown():
    raise GracefulExit()

async def close_echo_tasks(echo_tasks: List[asyncio.Task]):
    # Any echo tasks will have 2 seconds to finish before cancel them.
    waiters = [asyncio.wait_for(task, 2) for task in echo_tasks]
    for task in waiters:
        try:
            await task
        # We expect this to be thrown from our tasks after 2 seconds.
        except asyncio.exceptions.TimeoutError:
            # We expect a timeout error here
            pass

# ----------
@async_timed()
async def main():
    # ----------
    # server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket.socket()
    # ----------
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    # ----------
    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(getattr(signal, signame), shutdown)
    # Start the coroutine to listen for connections.    
    await connection_listener(server_socket, loop)
    

loop = asyncio.new_event_loop()

try:
    loop.run_until_complete(main())
except GracefulExit:
    loop.run_until_complete(close_echo_tasks(echo_tasks))
finally:
    loop.close()
