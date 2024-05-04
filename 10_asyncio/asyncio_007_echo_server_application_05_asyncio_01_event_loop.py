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
# Building an asyncio echo server
#   - Connect multiple clients concurrently and send data to them concurrently
#   - CPU utilization remains low.
#   - handle exception in coroutine itself.
# ----------------------------------------------------------------------------

# Note that 
#   - exception is handled in coroutine itself.
#   - shut down the socket within the finally block, so we won't be left with a dangling unclosed exception in the event of a failure.
#   - If our task is waiting on a statement such as await loop.sock_recv, and we cancel that task,
#     a CancelledError is thrown from the await loop.sock_recv line.
#     Then our finally block will be executed, since we threw an exception on an await expression when we canceled the task.

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


# Coroutine for listening for connections.
async def listen_for_connection(server_socket: socket, loop: AbstractEventLoop):
    while True:
        connection, address = await loop.sock_accept(server_socket)
        connection.setblocking(False)
        print(f'Got a connection from {address}')
        # ----------
        # Whenever we get a connection, create an echo task to listen for client data.
        # Once a client connects, or coroutine spawns an echo task for each client
        # which then listens for data and writes it back out to the client.
        echo_task = asyncio.create_task(echo(connection, loop))


@async_timed()
async def main():
    # ----------
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # ----------
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('127.0.0.1', 8000)
    server_socket.setblocking(False)
    server_socket.bind(server_address)
    server_socket.listen()
    # ----------
    # Start the coroutine to listen for connections.    
    await listen_for_connection(server_socket, asyncio.get_event_loop())
    

asyncio.run(main())
