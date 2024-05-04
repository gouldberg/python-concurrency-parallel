import socket

# For this application, we need to connecting to a server with Telnet.
#   - install telnet:  apt-get install telnet
#   - connect to localhost on port 8000:  telnet localhost 8000
#   - send message (for example):  'testing123' in command terminal


# ----------------------------------------------------------------------------
# Multiple connections and the dangers of blocking
# ----------------------------------------------------------------------------

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_address = ('127.0.0.1', 8000)
server_socket.bind(server_address)
server_socket.listen()

connections = []

# We can try this by making one connection with telnet and typing a message.
# Then, once we have done that, we can connect with a second telnet client and send another message.
# However, if we do this, we will notice a problem right away.
# Our first client will work fine and will echo messages back as we'd expect, but our second client won't get anything echoed back to it.
# This is due to the default blocking behavior of sockets.
# The methods accept and recv block until they receive data.
# This means that once the first client connects, we will block waiting for it to send its first echo message to us.
# This causes other clients to be stuck waiting for the next iteration of the loop, which won't happen until the first client sends us data.

try:
    while True:
        connection, client_address = server_socket.accept()
        print(f'I got a connection from {client_address}!')
        connections.append(connection)
        for connection in connections:
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
finally:
    server_socket.close()


