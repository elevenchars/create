import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER = raw_input("Please type in the server's address: ")
PORT = int(raw_input("Please type in the server's port: "))

print "connecting to server"
s.connect((SERVER, PORT))
print "connected!"
resp = ""
#while(json.load(resp)["verified"] != "true"):
#    name = raw_input("sorry, that name is invalid")
name = raw_input("what is your name?")
while 1:
    s.sendall(raw_input("input: "))
