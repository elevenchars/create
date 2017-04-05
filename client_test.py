import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER = raw_input("Please type in the server's address: ")
PORT = int(raw_input("Please type in the server's port: "))

print "connecting to server"
s.connect((SERVER, PORT))
print "connected!"

while 1:
    s.sendall(raw_input("input: "))
