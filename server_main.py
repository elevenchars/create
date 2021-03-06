import socket
from threading import Thread
import json

import plugins # so i can get __all__
from plugins import *


# handler to receive data from client class
class ClientHandler(Thread):
    def __init__(self, cs, address):  # initialize instance variables
        Thread.__init__(self)
        self.cs = cs
        self.address = address
        self.confirmed = False
        self.name = ""
        self.cs.setblocking(1)
        self.stopped = False
        self.commands = []
        self.populate_commands()

    def populate_commands(self):  # import all commands in plugins package
        for command_name in plugins.__all__:
            self.commands.append(getattr(plugins, command_name).Command(self))

    def is_command(self, message):  # determine if input string matches the format
        if (message.startswith("/")):
            return True
        return False

    def find_command(self, message):  # find command that matches the input string
        if (self.is_command(message)):
            for command in self.commands:
                print command.get_command()
                if message.split(" ")[0] == command.get_command():
                    return command
        return None

    def recvall(self, sock, buff):  # make sure all data is received
        data = ""
        while 1:
            part = sock.recv(buff)
            if(part == ""):
                break
            data += part
            print part
            if len(part) < buff:
                break  # exit loop on last part of message
        return data

    def send_to_all(self, msg):  # wrapper method so Command classes can access send_to_clients
        send_to_clients(msg)

    def run(self):  # main loop
        while not self.stopped:
            try:
                msg = json.loads(self.recvall(self.cs, 1024))  # load message from client
                if (not self.confirmed):  # confirmation process, make sure it is actually a client and name is unique
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
                else:  # send message once confirmed
                    print self.name + " > " + msg["body"]
                    msg["name"] = self.name
                    print msg["body"]
                    if(self.is_command(str(msg["body"]))):  # parse command
                        current = self.find_command(str(msg["body"]))
                        if(current):  # if command is in plugins
                            current.execute(str(msg["body"]))  # execute the command
                        else:
                            self.cs.sendall(json.dumps({"type": "message",  # command not found, so send error message to client
                                                        "body": "sorry, command not found"}))
                    else:
                        send_to_clients(msg)
            except (socket.error, Exception) as e:  # print errors for debugging, kill thread
                print self.name + " !! " + str(e)
                clients.remove(self)
                self.stop()
        print "STOPPED " + self.name + " THREAD"

    def stop(self):  # stop while loop to kill thread
        self.stopped = True


def send_to_clients(msg):  # send message to all clients, and remove disconnected clients if necessary
    for client in clients[:]:
        try:
            client.cs.sendall(json.dumps(msg))
        except socket.error, e:
            if e.errno == socket.errno.ECONNRESET:
                print "socket killed! removing from list"
                client.stop()
                clients.remove(client)


def name_in_use(name):  # check all clients to see if name is in use
    for client in clients:
        if(name == client.name):
            return True
    return False

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create server
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

PORT = 1234
s.bind(("0.0.0.0", PORT))
s.listen(5)
print "server started on " + socket.gethostbyname(socket.gethostname()) + ", " + str(PORT)

while 1:  # main loop to find clients
    print "looking for client"
    client_socket, address = s.accept()
    print "client found"
    ch = ClientHandler(client_socket, address)
    ch.start()

    clients.append(ch)

    print "client connected"
    print "client thread started"
    print clients
