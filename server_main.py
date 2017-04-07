import socket
from threading import Thread


class ClientHandler(Thread):
    def __init__(self, cs, address):
        Thread.__init__(self)
        self.cs = cs
        self.address = address
        self.cs.setblocking(0)

    def run(self):
        while 1:
            try:
                data = self.cs.recv(512)
                print address[0] + " > " + data
            except socket.error:
                '''nothing'''


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
    print "client connected"
    ch.start()
