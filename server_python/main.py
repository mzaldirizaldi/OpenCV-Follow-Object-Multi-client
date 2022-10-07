import socket
from threading import Thread

host = '192.168.18.229'
port = 9999
client_sockets = set()
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    s.bind((host, port))
    print(f'Running the server on: {host} : {port}')
except socket.error as e:
    print(str(e))

print ('Waiting for a connection..')
s.listen()

def listen_for_client(cs):
    while True:
        try:
            msg = cs.recv(1024).decode('utf-8')

        except Exception as e:
            print(e)
            client_sockets.remove(cs)

        for client_socket in client_sockets:
            client_socket.send(msg.encode())

while True:
    client_socket, client_address = s.accept()
    client_socket.send('\n'.encode())
    print("Connection from: " + client_address[0] + ':' + str(client_address[1]))
    client_sockets.add(client_socket)
    t = Thread(target=listen_for_client, args=(client_socket,))
    t.daemon = True
    t.start()

for cs in client_sockets:
    cs.close()
s.close()