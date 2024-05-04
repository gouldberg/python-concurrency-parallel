import socket

# For this application, we need to connecting to a server with Telnet.
#   - install telnet:  apt-get install telnet
#   - connect to localhost on port 8000:  telnet localhost 8000
#   - send message (for example):  'testing123' in command terminal


# ----------------------------------------------------------------------------
# Non-blocking socket
#   The application with this code comes at a cost.
#     - code quality: Catching exceptions any time we might not yet have data will quickly get verbose and is potentially error-prone.
#     - resource issue: We are constantly looping and getting exceptions as fast as we can inside out application, leading to a workload that is CPU heavy.
# ----------------------------------------------------------------------------

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()

##### Mark the server socket as non-blocking #####
server_socket.setblocking(False)

connections = []


# Use except BlockingIOError:
# Without this, Our application crashes almost instantly. We'll get thrown a BlockingIOError
# because our server socket has no connection yet and therefore no data to process.

try:
    while True:
        try:
            connection, client_address = server_socket.accept()
            ##### Mark the client socket as non-blocking
            connection.setblocking(False)
            print(f'I got a connection from {client_address}!')
            connections.append(connection)
        except BlockingIOError:
            pass
        for connection in connections:
            try:
                buffer = b''
                while buffer[-2:] != b'\r\n':
                    data = connection.recv(2)
                    if not data:
                        break
                    else:
                        print(f'I got data: {data}!')
                        buffer = buffer + data    
                print(f'All the data is : {buffer}')
                connection.send(buffer)
            except BlockingIOError:
                pass
finally:
    server_socket.close()


