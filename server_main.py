import socket
from threading import Thread
import json


# handler to receive data from client class
class ClientHandler(Thread):
    def __init__(self, cs, address):
        Thread.__init__(self)
        self.cs = cs
        self.address = address
        self.cs.setblocking(0)

    def recvall(self, sock, buff):
        data = ""
        while 1:
            part = sock.recv(buff)
            data += part
            print part
            if len(part) < buff:
                break  # exit loop on last part of message
        return data

    def run(self):
        while 1:
            try:
                msg = self.recvall(self.cs, 1024)
                print address[0] + " > " + msg
            except socket.error:
                '''nothing'''




clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
PORT = 1234
s.bind(("0.0.0.0", PORT))
s.listen(5)
print "server started on " + socket.gethostbyname(socket.gethostname()) + ", " + str(PORT)

while 1:
    print "looking for client"
    client_socket, address = s.accept()
    client_socket.sendall("hello, world!")
    print "client found"
    ch = ClientHandler(client_socket, address)
    ch.start()

    clients.append(ch)

    print "client connected"
    print "client thread started"
    print clients
