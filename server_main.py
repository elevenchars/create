import socket
from threading import Thread
import json


# handler to receive data from client class
class ClientHandler(Thread):
    def __init__(self, cs, address):
        Thread.__init__(self)
        self.cs = cs
        self.address = address
        self.confirmed = False
        self.name = ""
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
                msg = json.loads(self.recvall(self.cs, 1024))
                if (not self.confirmed):
                    if ("type" in msg and "body" in msg and "name" in msg):
                        if (msg["type"] == "status" and msg["body"] == "newconn" and not name_in_use(msg["name"])):
                            self.cs.sendall(json.dumps({"type": "status",
                                                       "body": "confirm"}))
                            print "client connected and confirmed"
                            self.confirmed = True
                            self.name = msg["name"]
                        else:
                            print "found client, but name is already in use"
                            self.cs.sendall(json.dumps({"type": "status",
                                                        "body": "name in use"}))
                else:
                    print address[0] + " > " + str(msg)
                    send_to_clients(msg)
            except socket.error:
                '''do nothing'''


def send_to_clients(msg):
    for client in clients[:]:
        try:
            client.cs.sendall(json.dumps(msg))
        except socket.error, e:
            if e.errno == socket.errno.ECONNRESET:
                print "socket killed! removing from list"
                clients.remove(client)


def name_in_use(name):
    for client in clients:
        if(name == client.name):
            return True
    return False

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
    print "client found"
    ch = ClientHandler(client_socket, address)
    ch.start()

    clients.append(ch)

    print "client connected"
    print "client thread started"
    print clients
