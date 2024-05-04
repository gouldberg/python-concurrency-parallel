import socket
import selectors
from selectors import SelectorKey
from typing import List, Tuple

# For this application, we need to connecting to a server with Telnet.
#   - install telnet:  apt-get install telnet
#   - connect to localhost on port 8000:  telnet localhost 8000
#   - send message (for example):  'testing123' in command terminal


# ----------------------------------------------------------------------------
# Using the selectors module to build a socket event loop
# ----------------------------------------------------------------------------

selector = selectors.DefaultSelector()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
##### Mark the server socket as non-blocking #####
server_socket.setblocking(False)
server_socket.bind(server_address)
server_socket.listen()

# ----------
selector.register(server_socket, selectors.EVENT_READ)
# ----------

while True:
    # Create a selector that will timeout after 1 second.
    events: List[Tuple[SelectorKey, int]] = selector.select(timeout=1)
    # ----------
    # If there are no events, print it out.
    # This happens when a timeout occurs.
    if len(events) == 0:
        print('No events, waiting a bit more!')
    # ----------
    for event, _ in events:
        # ----------
        # Get the socket for the event, which is stored in the fileobj field.
        event_socket = event.fileobj
        # If the event socket is the same as server socket, we know this is a connection attempt.
        if event_socket == server_socket:
            connection, address = server_socket.accept()
            connection.setblocking(False)
            print(f'I got a connection from {address}')
            # Register the client that connected with our selector.
            selector.register(connection, selectors.EVENT_READ)
        else:
            # If the event socket is not the server socket, receive data from the client, and echo it back.
            data = event_socket.recv(1024)
            print(f'I got some data: {data}')
            event_socket.send(data)
