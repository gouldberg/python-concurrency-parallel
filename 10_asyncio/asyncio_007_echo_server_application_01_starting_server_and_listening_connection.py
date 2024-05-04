import socket

# For this application, we need to connecting to a server with Telnet.
#   - install telnet:  apt-get install telnet
#   - connect to localhost on port 8000:  telnet localhost 8000
#   - send message (for example):  'testing123' in command terminal


# ----------------------------------------------------------------------------
# Starting a server and listening for a connection 
# ----------------------------------------------------------------------------

# AF_INET:
# type of address our socket will be able to interact with,
# in this case a hostname and a port number

# SOCK_STREAM:
# we use the TCP protocol for our communication
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_REUSEADDR flag to 1: reuse the port number after we stop and restart the application,
# avoiding any address already in use errors.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# ----------
# bind the socket to an address, 127.0.0.1:8000
# meaning that clients will be able to use this address to send data to our server,
# and if we write data to a client, they will see this as the address that it's coming from.
server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)


# ----------
# for actively listen for connections
# --> This method will block until we get a connection and when we do, it will return a connection and the address of the client that connected.
server_socket.listen()


try:
    connection, client_address = server_socket.accept()
    print(f'I got a connection from {client_address}!')    
    buffer = b''
    # We'll treat the end of input as a carriage return plus a line feed or '\r\n'
    # This is what gets appended to the input when a user presses [Enter] in telnet.
    while buffer[-2:] != b'\r\n':
        # 2: read 2 bytes in a given time.
        data = connection.recv(2)
        if not data:
            break
        else:
            print(f'I got data: {data}!')
            buffer = buffer + data    
    print(f'All the data is : {buffer}')
    # take a message and write it back to the client.
    connection.sendall(buffer)
finally:
    server_socket.close()


